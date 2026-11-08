---
name: test-on-the-board
description: Check the real firmware before installing and don't blame hardware without asking how the user was testing
metadata:
  type: feedback
---

Before installing code on the frame, probe the firmware for what the code uses and run it there. Don't call it working because a desktop simulation passes.

**Why:** the first photo frame passed simulation and lint but crashed on the board's old firmware, twice. Separately, buttons that "did nothing" were simply on USB, while I had suspected the batteries from an indirect clock reading.

**How to apply:** ask or check how the user is testing (USB or battery) before forming a theory. The user confirmed the 2 x AA batteries work, so don't question them again.

"Push the code" can mean putting it on the board rather than `git push`. When the user is testing hardware, it means the board.

See also [[board-workflow]].
