---
spec_version: 1
type: arch-guidelines
title: "Architecture Guidelines"
tags: [architecture, guidelines, structure]
file_type: architecture
frozen: false
last_review: 2026-08-13
---

# Architecture guidelines

## Shape
This is a **static multi-page site** talking directly to Supabase from the browser. There is no
server tier of our own and no build step. "Backend" = Supabase (Postgres + Auth). Logic lives in
plain `<script>` files that call the Supabase JS client.

## Folder structure (real tree)
```
index.html            # public landing page (Bengali)
config.js             # window.SOT_CONFIG = { SUPABASE_URL, SUPABASE_ANON_KEY }
assets/
  css/style.css       # public site styles
  js/app.js           # public site behaviour (currently: set footer year)
admin/
  login.html          # admin magic-link login
  dashboard.html      # admin dashboard shell (feature cards)
  admin.js            # supabase client, login, checkAdminAccess(), logoutAdmin()
supabase/
  schema.sql          # all tables (idempotent)
docs/
  implementation-plan.md
context/               # the spec (this system)
```

## Rules
- One admin concern per page/script as the site grows: `admin/<concern>.html` + `admin/<concern>.js`, both including `../config.js` then `admin.js` (for the shared client + `checkAdminAccess`).
- `admin.js` owns the shared Supabase client and auth helpers — reuse it, don't create a second client.
- Every admin page runs `checkAdminAccess()` before rendering data.
- All DB shape changes go in `supabase/schema.sql` (idempotent), never ad-hoc in the console only.

## Naming conventions
| Artifact | Convention | Example |
|---|---|---|
| Admin page | `admin/<concern>.html` | `admin/members.html` |
| Admin script | `admin/<concern>.js` | `admin/members.js` |
| DB table | snake_case plural | `sms_logs` |
| Human key column | `<thing>_id` / `<thing>_no` | `member_id`, `receipt_no` |
| CSS class | kebab-case | `.dashboard-grid` |

## Wiring order (per admin page)
1. `<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2">`
2. `<script src="../config.js">` (defines `window.SOT_CONFIG`)
3. `<script src="admin.js">` (creates client + auth helpers)
4. page script / inline script that calls `checkAdminAccess()` then loads data
