---
name: project-status
description: Where the Inky Frame 4.0" tweaking work stands, what is unverified, and the question still open with the user
metadata:
  type: project
---

As of 2026-11-08 the user wants a battery photo frame with no WiFi: a random SD picture every 8 hours, buttons A and E stepping backwards and forwards. It is built as `examples/image_gallery/sd_photo_frame.py` with `prepare_photos.py` for the computer side, and is installed on the user's frame as `main.py` (the old launcher is kept there as `launcher_main.py`). It displayed a picture on the real board on 2026-11-08 over USB, and the user confirmed the A and E buttons work there. Waking from power-off on battery (buttons and the 8-hour alarm) is still to be confirmed.

The frame runs old firmware: MicroPython 1.19.1 from 2023-02-27. Its `inky_frame` module has no `sleep_for`, `turn_off`, `woken_by_*`, `rtc` or colour constants, and `str.endswith()` rejects tuples, so desktop simulation misses real failures. Probe the board and run on it (`mpremote run`) before calling anything done, or ask the user about upgrading the firmware.

The user's power source is 2 x AA rechargeables. The user confirmed these work with the board, so don't raise the voltage again.

The user's photos are in `examples/image_gallery/custom/` (gitignored), prepared into `custom/outputs/` and copied to the root of their 4 GB card on 2026-11-08.

**Why:** the first board test is the real check of decoding, button wake and battery life.

**How to apply:** when the user reports back from hardware, fix what they found. Do not fix the whole bug list in `.claude/TODO.md` unprompted.

Unverified so far:
- Nothing has been run on a board. The TODO bugs come from reading the code.
- The local build steps in `CLAUDE.md` were adapted from CI and never run.
- The SessionStart hook has fired (seen on compaction). The memory redirect to `.claude/memory/` is set in the gitignored `.claude/settings.local.json` and has not yet been seen working in a new session. A fresh clone will not have that file.

See also [[repo-remotes]].
