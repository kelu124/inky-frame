---
name: board-workflow
description: How to install, run and test code on the user's Inky Frame over USB, and how to add new photos
metadata:
  type: reference
---

The frame shows up as `/dev/ttyACM0` and `mpremote` is installed on this machine. CLAUDE.md has the basic commands and the firmware limits.

Installed on the board: `main.py` is the photo frame, `launcher_main.py` is the original launcher, and `photo_frame_last.txt` remembers the current picture.

To see program output, set `PYTHONUNBUFFERED=1` and write to a file. Otherwise `timeout` kills `mpremote` and the output is lost. The program never exits, so a timeout is expected. Any later `mpremote` command interrupts the running program.

To test buttons without a person pressing them, set `inky_frame.button_e.startup_state = True` before the program runs, or from a one-shot `machine.Timer` for a later press. This exercises the real firmware but not the physical wake-up.

The clock reads around 2000-01-01 because nothing sets it. The 8-hour alarm is relative, so that doesn't matter.

New photos: put them in `examples/image_gallery/custom/` (gitignored), run `prepare_photos.py` with `custom/outputs` as the output, and copy the files to the root of the card, which mounted at `/media/kelu/4862-EF8A`. Look at the card first and don't overwrite.

See also [[project-status]] and [[test-on-the-board]].
