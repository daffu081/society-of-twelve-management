---
spec_version: 1
type: shared-convention
title: "Dev Setup"
tags: [shared, setup, onboarding]
file_type: shared
frozen: false
last_review: 2026-08-13
---

# Dev setup

## Prerequisites
- A modern browser.
- Any static file server (Python's `http.server` is enough — no toolchain to install).
- A Supabase project (URL + anon key) for anything beyond the public static page.

## First run
```bash
# from the project root
cp config.js config.js.bak 2>/dev/null || true   # config.js is currently empty
# put your Supabase creds in config.js:
#   window.SOT_CONFIG = { SUPABASE_URL: "...", SUPABASE_ANON_KEY: "..." };
python3 -m http.server 8000
# open http://localhost:8000            (public site)
# open http://localhost:8000/admin/login.html   (admin)
```

## Common commands
The command tooling in `.claude/commands/` uses these placeholders — filled for this stack:

| Task | Placeholder | Command |
|---|---|---|
| Install deps | `<pkg-cmd>` | _n/a — no package manager_ |
| Run | `<run-cmd>` | `python3 -m http.server 8000` |
| Test | `<test-cmd>` | _n/a — no test runner yet_ |
| Lint / analyze | `<lint-cmd>` | _n/a — none configured_ |
| Format | `<format-cmd>` | _n/a — none configured_ |
| Build | `<build-cmd>` | _n/a — no build step_ |
| Apply DB schema | — | run `supabase/schema.sql` in the Supabase SQL editor |

Path placeholders used in the tooling: `<src>/` = repo root (`index.html`, `admin/`, `assets/`),
`<tests>/` = _none yet_, `<ext>` = `.js`, `<manifest>` = _none (no package.json)_.
