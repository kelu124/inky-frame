---
name: repo-remotes
description: origin is the user's fork of Pimoroni's repo; what must stay out of upstream PRs and out of commits
metadata:
  type: project
---

`origin` is the user's fork, `git@github.com:kelu124/inky-frame.git`. The code comes from Pimoroni's upstream `inky-frame`. The `gh` CLI is not installed on this machine.

Keep `CLAUDE.md` and `.claude/` out of any PR to Pimoroni.

`examples/inkylauncher/secrets.py` is tracked by git, so never commit real WiFi credentials in it.

**Why:** the scaffolding is personal to this fork, and anything pushed to the fork is public.

**How to apply:** before committing, check that `secrets.py` is not in the diff. For upstream PRs, branch from Pimoroni's history without the scaffolding commits, because the fork's `main` includes them since 2026-11-08.

See also [[project-status]].
