---
name: project-status
description: Where the Inky Frame 4.0" tweaking work stands, what is unverified, and the question still open with the user
metadata:
  type: project
---

As of 2026-11-08, only scaffolding and docs exist: `CLAUDE.md`, `.claude/`, `docs/examples.md`. No example or firmware code has been changed, and no example has been adapted to the 4.0" yet.

The user was asked what they want the frame to show and has not answered. Ask again at the start of the next working session.

**Why:** the choice decides which example or launcher app to adapt, and so which bugs in `.claude/TODO.md` matter first.

**How to apply:** adapt the closest example or launcher app to `DISPLAY_INKY_FRAME_4` and fix the TODO bugs it touches. Do not fix the whole bug list unprompted.

Unverified so far:
- Nothing has been run on a board. The TODO bugs come from reading the code.
- The local build steps in `CLAUDE.md` were adapted from CI and never run.
- The SessionStart hook has fired (seen on compaction). The memory redirect to `.claude/memory/` is set in the gitignored `.claude/settings.local.json` and has not yet been seen working in a new session. A fresh clone will not have that file.

See also [[repo-remotes]].
