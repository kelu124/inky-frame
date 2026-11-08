# TODO

Open work for this repo. Move finished items to `.claude/DONE.md` with their completion date.

## To confirm on the board

- [ ] `examples/image_gallery/sd_photo_frame.py` on battery: unplug USB, check that A and E wake the board and step the right way, and that the picture changes by itself after 8 hours.

## Bugs in the examples

Found by reading the code, see "Known issues" in `docs/examples.md`. None have been reproduced on a board.

- [ ] `examples/inkylauncher/word_clock.py`: shows UTC, with no timezone setting.
- [ ] `examples/inkylauncher/word_clock.py`: at exactly minute 0 it shows the next hour.
- [ ] `examples/inky_frame_quote_of_the_day.py`: never sets the clock, so it can request the wrong date.
- [ ] Image downloads (`inky_frame_placebear.py`, `inky_frame_random_joke.py`, `inky_frame_xkcd_daily.py`, `inkylauncher/daily_xkcd.py`, `inkylauncher/nasa_apod.py`): the full 1 KB buffer is written even after a short read, which can corrupt the file.
- [ ] `examples/inky_frame_news.py`: `get_rss()` returns `False` on a network error, then `len(feed)` crashes.
- [ ] `examples/carbon_intensity.py` and `examples/inkylauncher/carbon_intensity.py`: two sources with the same non-zero percentage end up in one column, because bars are positioned with `power_list.index(p)`.
- [ ] `examples/led_pwm.py`: the fade-up uses the empty `range(65025, 2)`, so it never runs.
- [ ] `examples/inky_frame_random_joke.py`: `randint(0, number_of_lines)` can pick one line past the end and raise a `ValueError`.
- [ ] `examples/README.md`: out of date, refers to PlaceKitten, `network_manager.py`, `WIFI_CONFIG.py` and a `common` directory, none of which exist.

