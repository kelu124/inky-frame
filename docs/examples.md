# Examples guide (Inky Frame 4.0") <!-- omit in toc -->

What each program in `examples/` does and what it needs, with notes for the 4.0" board (640x400, 7 colours, no PSRAM).

These notes come from reading the code. None of the examples have been run on a board for this guide, and third-party web services may have changed since the code was written.

- [Setting up for the 4.0"](#setting-up-for-the-40)
- [Overview](#overview)
- [Hardware and basics](#hardware-and-basics)
- [Images](#images)
- [Online displays](#online-displays)
- [Inky Launcher](#inky-launcher)
- [Known issues](#known-issues)

## Setting up for the 4.0"

**Select the display.** Every example that draws to the screen defaults to the 7.3" Spectra panel, including `inkylauncher/main.py`. Comment out the Spectra import, which usually spans two lines, and uncomment the 4.0" one:

```python
from picographics import DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
```

**Copy the helpers for online examples.** Standalone online examples import `inky_helper` and read `secrets.py`. Both live in `examples/inkylauncher/`, and both are already on the board if you flashed the `-with-examples` firmware. Put your WiFi details in `secrets.py`:

```python
WIFI_SSID = "your network"
WIFI_PASSWORD = "your password"
```

`examples/inkylauncher/secrets.py` is tracked by git, so don't commit it once it holds real credentials.

**Run on battery from `main.py`.** A button or RTC wake restarts the board and runs `main.py`, so a program that should survive sleep has to be saved under that name on the board.

**Watch the RAM.** The 4.0" framebuffer takes 96,000 of the roughly 166k available on a Pico W. That is why many examples call `gc.collect()` often, and why some of them make their HTTPS request before creating `PicoGraphics`.

## Overview

| Example | What it shows | WiFi | SD card | Repeats | Fit at 640x400 |
| --- | --- | --- | --- | --- | --- |
| `button_test.py` | Toggles button LEDs, no screen | No | No | Polling loop | No screen |
| `button_demo.py` | Screen message per button | No | No | Polling loop | Fits |
| `led_pwm.py` | Fades each LED in turn | No | No | Loop | No screen |
| `sd_test.py` | SD write, append and read | No | Yes | Once | No screen |
| `inky_frame_dithering.py` | Palette and dithering test card | No | No | Once | Fits |
| `inky_frame_rtc_demo.py` | Date and time on a rainbow | If clock unset | No | 2 min | May clip |
| `display_png.py` | PNG with a text caption | No | No | Once | Fits |
| `image_gallery/image_gallery.py` | Five images from flash, by button | No | No | On press | Use `640x400/` |
| `image_gallery/image_gallery_sd.py` | Five images from SD, by button | No | Yes | On press | Use `640x400/` |
| `image_gallery/image_gallery_sd_random.py` | Random SD image | No | Yes | 60 min | Use `640x400/` |
| `carbon_intensity.py` | UK electricity mix chart | Yes | No | Once | Adapts |
| `inky_frame_daily_activity.py` | Random activity idea | Yes | No | 60 s | Long text overlaps |
| `inky_frame_news.py` | Two BBC headlines with QR codes | Yes | No | 60 s | Long text clips |
| `inky_frame_placebear.py` | Bear photo at screen size | Yes | Yes | Once | Adapts |
| `inky_frame_quote_of_the_day.py` | Wikiquote quote of the day | Yes | No | Daily | Adapts |
| `inky_frame_random_joke.py` | Pre-rendered joke image | Yes | Yes | Once | Adapts |
| `inky_frame_xkcd_daily.py` | Pre-rendered xkcd comic | Yes | Yes | Once | Adapts |
| `inkylauncher/` | Five-app menu with sleep between updates | Yes | One app | Per app | Tuned for 4.0" |

## Hardware and basics

### `button_test.py`

Reads the five buttons through the shift register and toggles each button's LED on a press, polling 60 times a second. It never touches the screen, which makes it a quick hardware check.

### `button_demo.py`

Shows "Press any button!", then a coloured "Button X pressed" message at a different height for each button, lighting that button's LED. Every press triggers a full ePaper refresh, so it responds slowly.

### `led_pwm.py`

Cycles through the activity, connection and A to E LEDs, fading each one using PWM. See [Known issues](#known-issues), because the fade-up never runs.

### `sd_test.py`

Mounts the card at `/sd`, writes `/sd/inkytest.txt` (overwriting any existing copy), appends a line, prints the contents to the console and unmounts. Uses the SD pins every SD example shares: SCK 18, MOSI 19, MISO 16, CS 22.

### `inky_frame_dithering.py`

Draws a test card: the eight palette pens, a grey gradient, a rainbow, three blocks of mixed colour with text, and red, green and blue gradients. The layout is hard-coded but fits. The last gradient ends exactly on the bottom row, and the block row leaves the right-hand 40 pixels empty.

### `inky_frame_rtc_demo.py`

Draws a rainbow with the date and time centred on it, then sleeps for two minutes. It only does anything when woken by the RTC or a button, so to test it from Thonny hold a button while it starts. It connects to WiFi for NTP only if the clock reads earlier than 2023. Set `tz_offset` for your timezone. It uses text scale 6 on the 4.0", which is close to the full screen width, so lower `text_scale` if the ends are cut off. On USB it stops after the simulated sleep instead of redrawing.

## Images

Images must be non-progressive JPEGs no larger than the screen. Use the files in `examples/image_gallery/640x400/`, which total about 410 KB and fit in flash on either board. Credits and transfer instructions are in `examples/image_gallery/README.md`.

### `display_png.py`

Draws a "PNG Pencil" caption and decodes `pencil_256x256.png` at (200, 100), which fits on the 4.0". Copy the PNG to the board first, or it prints a message asking you to.

### `image_gallery/image_gallery.py`

Buttons A to E each show one of five images stored in the root of the flash, named by `IMAGE_A` to `IMAGE_E`. After each pass it cuts power, so on battery a button press wakes the board, shows the image and turns it off again.

### `image_gallery/image_gallery_sd.py`

Same as `image_gallery.py`, but the images come from the root of the SD card.

### `image_gallery/image_gallery_sd_random.py`

Shows a random `.jpg` or `.jpeg` from the root of the SD card, then sleeps for `UPDATE_INTERVAL` minutes (60 by default). This is the simplest base for a battery photo frame.

## Online displays

These connect using `inky_helper.network_connect()` and credentials from `secrets.py`.

The `feed2image` examples download images that Pimoroni has already rendered for each screen size, because some of the original sites need TLS 1.3, which the Pico W doesn't support. They include `640x400` in the URL on the 4.0".

### `carbon_intensity.py`

Fetches a regional forecast for a UK postcode from the Carbon Intensity API, then draws a bar chart of the generation mix with the region, gCO2/kWh and time window. Set `POSTCODE` (the default is `S9`). It only covers Great Britain. The layout scales with the screen. It powers off after one update, and a commented-out line switches it to every 30 minutes.

### `inky_frame_daily_activity.py`

Fetches a random activity from a Bored API mirror and draws it on a ruled "notebook page" with its type and number of participants. The activity text has room for about four lines before it reaches the footer. It updates every 60 seconds, which is hard on a battery, so raise `UPDATE_INTERVAL` (in seconds).

### `inky_frame_news.py`

Parses a BBC RSS feed one character at a time to save RAM, then shows the first two stories with a QR code linking to each. Choose the feed by uncommenting a `URL`; the default is science and environment. The layout was written for a taller screen, so the second description has room for about three lines before it runs under the footer bar. It updates every 60 seconds, so raise `UPDATE_INTERVAL` (in seconds) on battery.

### `inky_frame_placebear.py`

Requests a 640x400 JPEG from placebear.com, streams it to `/sd/placebear.jpg` in 1 KB chunks and displays it. Runs once.

### `inky_frame_quote_of_the_day.py`

Fetches today's Wikiquote quote of the day, tidies up its wiki markup and shows it with the date and author. It checks every 60 seconds and redraws only when the date changes, and it stays powered between checks, so it suits USB power better than battery. It parses fixed line positions in the response, so a change in Wikiquote's template would break it.

### `inky_frame_random_joke.py`

Picks a random joke ID from the `feed2image` list, downloads that joke's pre-rendered JPEG to `/sd/random-joke.jpg` and displays it. Runs once.

### `inky_frame_xkcd_daily.py`

Downloads the daily pre-rendered xkcd comic to `/sd/xkcd-daily.jpg` and displays it. Runs once.

## Inky Launcher

`examples/inkylauncher/` is a small app system, and it is what the `-with-examples` firmware installs.

### `main.py`

Shows a menu mapping buttons A to E to the five apps below and saves the choice to `state.json`. On later boots it goes straight to the saved app. Hold A and E, then press Reset, to get back to the menu. Its main loop runs the app's `update()` and `draw()`, then sleeps for `UPDATE_INTERVAL` minutes.

The menu layout already has an offset for the 4.0". The only change needed is the display import.

### Writing your own app

This is the most convenient way to add something of your own. An app is a module that `main.py` imports and drives:

```python
graphics = None         # set by main.py
WIDTH = None            # set by main.py
HEIGHT = None           # set by main.py
UPDATE_INTERVAL = 60    # minutes between updates


def update():
    pass                # fetch data


def draw():
    pass                # draw to graphics, then call graphics.update()
```

To add it to the menu, change the matching `ih.update_state("...")` call and the menu label in `main.py`. Keep `UPDATE_INTERVAL` at 255 or below, since the RTC timer that `ih.sleep()` uses is an 8-bit counter.

### `inky_helper.py`

Shared support code: WiFi connection with the pulsing network LED, RTC sleep, button LED control, `state.json` handling and app loading.

### `nasa_apod.py` (button A)

Gets the title of NASA's Astronomy Picture of the Day and downloads a pre-rendered 640x400 version to flash, then shows it with the title along the bottom. Updates every 240 minutes. It uses NASA's rate-limited `DEMO_KEY`, and you can get your own from api.nasa.gov.

### `word_clock.py` (button B)

Shows a grid of letters with the words for the approximate time in red and the rest in light grey, with a layout specific to the 4.0". It syncs from NTP on each update and updates every 15 minutes. It displays UTC and has no timezone setting.

### `daily_xkcd.py` (button C)

Launcher version of the xkcd example, updating every 240 minutes. It mounts the SD card on import, so it fails at startup if no card is inserted.

### `news_headlines.py` (button D)

Launcher version of the news example, using the technology feed and updating every 90 minutes. A failed fetch shows an error message on screen.

### `carbon_intensity.py` (button E)

Launcher version of the carbon example, updating every 240 minutes. Set `POSTCODE`.

### `secrets.py`

Blank template for your WiFi credentials.

### `lib/`

Libraries copied to the board. `sdcard.mpy` and `urllib/urequest.mpy` duplicate modules this firmware already includes. Nothing in `examples/` currently imports `tinyweb/server.py` or the `logging.mpy` it depends on.

## Known issues

Found while reading the code, and not fixed.

| Where | Problem |
| --- | --- |
| `led_pwm.py` | The fade-up uses `range(65025, 2)`, which is empty, so LEDs jump to full brightness and only fade down. |
| `inky_frame_quote_of_the_day.py` | Never sets the clock, so it requests whatever date the Pico's RTC holds. Thonny sets that clock when connected, which can hide the problem. |
| `inkylauncher/word_clock.py` | Shows UTC. At exactly minute 0 it falls through to the last case and shows the next hour. |
| `inky_frame_news.py` | `get_rss()` returns `False` on a network error, and `len(feed)` then crashes. The launcher version returns `[]` and shows an error. |
| Both `carbon_intensity.py` | Bars are positioned with `power_list.index(p)`, so when two sources share the same non-zero percentage, the second is drawn over the first and its column stays empty. |
| Image downloads (`placebear`, `random_joke`, `xkcd_daily`, `daily_xkcd`, `nasa_apod`) | The loop writes the full 1 KB buffer even after a short read, which can put stale bytes in the file. Check this first if a downloaded image looks corrupted. |
| `inky_frame_random_joke.py` | `randint(0, number_of_lines)` includes one line past the end, so it occasionally fails with a `ValueError`. |
| `examples/README.md` | Out of date. It refers to PlaceKitten, `network_manager.py`, `WIFI_CONFIG.py` and a `common` directory, none of which are in the repo. |
