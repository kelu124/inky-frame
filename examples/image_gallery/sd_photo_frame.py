"""
A battery photo frame for the Inky Frame 4.0".

Shows a random picture from the SD card, then powers off for 8 hours.
It doesn't need WiFi.

Button A shows the previous picture and button E shows the next one, in
filename order. The new picture then stays up for another 8 hours.
The other buttons do nothing.

Use prepare_photos.py on your computer to get your pictures ready, then copy
them to the root of the SD card. Pictures must be 640x400 or smaller and saved
as *non-progressive* jpgs.

To run on battery, save this file to the Pico as main.py, because the board
restarts from main.py each time it wakes up.
"""

from machine import SPI, Pin

# Keep the power on while we work, even after a short button press has ended
hold_power = Pin(2, Pin.OUT)
hold_power.value(True)

import os
import random
import sys
import time

import inky_frame
import jpegdec
import sdcard
from pcf85063a import PCF85063A
from picographics import DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
from picographics import PicoGraphics
from pimoroni_i2c import PimoroniI2C

# how long to show each picture (in minutes)
UPDATE_INTERVAL = 8 * 60

BLACK = 0
WHITE = 1

# Remembers the current picture while the power is off. This lives on the
# Pico's flash so that the SD card is only ever read, because writing to it on
# nearly flat batteries can corrupt it.
LAST_PICTURE_FILE = "/photo_frame_last.txt"

# set up the real time clock, which wakes the board up. This talks to the chip
# directly because older firmware has no inky_frame.sleep_for(). A timer left
# running by another program would wake us early, so switch that off.
rtc = PCF85063A(PimoroniI2C(4, 5, 100000))
rtc.enable_timer_interrupt(False)
rtc.clear_timer_flag()

# set up the display
graphics = PicoGraphics(DISPLAY)

# Create a new JPEG decoder for our PicoGraphics
j = jpegdec.JPEG(graphics)


def clear_screen():
    graphics.set_pen(WHITE)
    graphics.clear()


def show_message(message):
    clear_screen()
    graphics.set_pen(BLACK)
    graphics.set_font("bitmap8")
    graphics.text(message, 20, 20, wordwrap=600, scale=3)
    graphics.update()


def read_last_picture():
    try:
        with open(LAST_PICTURE_FILE) as f:
            return f.read().strip()
    except OSError:
        return None


def save_last_picture(name):
    try:
        with open(LAST_PICTURE_FILE, "w") as f:
            f.write(name)
    except OSError as e:
        print(f"Could not save the current picture: {e}")


def find_pictures():
    # Accept .JPG from cameras, and skip the hidden ._ files that macOS adds.
    # Older firmware can't pass a tuple to endswith(), so test each one.
    files = [
        f for f in os.listdir("/sd")
        if (f.lower().endswith(".jpg") or f.lower().endswith(".jpeg")) and not f.startswith(".")
    ]
    files.sort()
    return files


def pictures_to_try(files, last, step):
    # Returns every picture, best choice first, so a bad file can be skipped
    if step != 0:
        here = files.index(last) if last in files else 0
        return [files[(here + step * n) % len(files)] for n in range(1, len(files) + 1)]

    # Random order, with the current picture only as a last resort
    others = [f for f in files if f != last]
    order = []
    while others:
        order.append(others.pop(random.randrange(len(others))))
    if last in files:
        order.append(last)
    return order


def try_picture(filename):
    # The framebuffer is only sent to the screen once a picture has decoded
    clear_screen()
    try:
        j.open_file(filename)
        if j.decode(0, 0, jpegdec.JPEG_SCALE_FULL) is False:
            return False
    except (OSError, RuntimeError) as e:
        print(f"Could not read {filename}: {e}")
        return False
    graphics.update()
    return True


def show_picture(step):
    sd_spi = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
    sd = sdcard.SDCard(sd_spi, Pin(22))
    os.mount(sd, "/sd")
    try:
        show_picture_from_card(step)
    finally:
        os.umount("/sd")


def show_picture_from_card(step):
    files = find_pictures()
    if not files:
        show_message("No .jpg pictures found in the root of the SD card.")
        return

    for name in pictures_to_try(files, read_last_picture(), step):
        print(f"Displaying /sd/{name}")
        if try_picture("/sd/" + name):
            save_last_picture(name)
            return

    show_message("None of the pictures on the SD card could be read. Are they non-progressive jpgs?")


def pressed_step():
    if inky_frame.button_a.is_pressed:
        return -1
    if inky_frame.button_e.is_pressed:
        return 1
    return 0


def power_off_for(minutes):
    year, month, day, hour, minute, second, dow = rtc.datetime()

    # Don't let the alarm time go past while the board is still shutting down
    if second >= 55:
        minute += 1

    wake = time.localtime(time.mktime((year, month, day, hour, minute, second, dow, 0)) + minutes * 60)

    rtc.clear_alarm_flag()
    rtc.set_alarm(0, wake[4], wake[3], wake[2])  # second, minute, hour, day
    rtc.enable_alarm_interrupt(True)

    # Letting go of this pin cuts the power on battery
    time.sleep(0.1)
    hold_power.init(Pin.IN)

    # On USB the board stays on, so watch the buttons until it's time for a new picture
    deadline = time.time() + minutes * 60
    while time.time() < deadline:
        step = pressed_step()
        if step != 0:
            return step
        time.sleep(0.05)
    return 0


step = pressed_step()

# B, C and D wake the board too, but they shouldn't cost a screen refresh
ignore_wake = step == 0 and (
    inky_frame.button_b.is_pressed or inky_frame.button_c.is_pressed or inky_frame.button_d.is_pressed
)

while True:
    hold_power.init(Pin.OUT, value=1)
    inky_frame.led_busy.on()

    # Whatever goes wrong, carry on to the power off below so the batteries don't drain
    try:
        if not ignore_wake:
            show_picture(step)
    except Exception as e:  # noqa: BLE001
        sys.print_exception(e)
        show_message(f"Could not show a picture. Is the SD card in? ({e})")

    inky_frame.led_busy.off()

    print(f"Sleeping for {UPDATE_INTERVAL} minutes")
    step = power_off_for(UPDATE_INTERVAL)
    ignore_wake = False
