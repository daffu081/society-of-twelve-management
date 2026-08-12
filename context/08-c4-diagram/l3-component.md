---
type: c4
level: 3
title: "L3 — Component"
last_review: 2026-08-13
---

# L3 — Components (browser container)

```mermaid
graph TD
  config[config.js - SOT_CONFIG] --> adminjs[admin.js - client + auth helpers]
  adminjs --> gate[checkAdminAccess]
  login[login.html] --> adminjs
  dashboard[dashboard.html] --> gate
  gate --> admins[(admins table)]
  index[index.html + app.js] --> public[public content - read only]
  gate -. guards .-> features[future admin pages: members/payments/finance/...]
```
- `admin.js` is the shared spine: creates the Supabase client and exposes `checkAdminAccess()` / `logoutAdmin()`.
- Every admin page loads `config.js` → `admin.js` → its own script, and guards with `checkAdminAccess()`.
- The public page (`index.html` + `app.js`) is a leaf; today it only sets the footer year.
