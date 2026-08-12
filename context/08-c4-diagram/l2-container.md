---
type: c4
level: 2
title: "L2 — Container"
last_review: 2026-08-13
---

# L2 — Containers

Deployable/runnable units.
```mermaid
graph TD
  browser[Browser: static HTML/CSS/JS] --> cdn[supabase-js @2 from CDN]
  browser --> auth[Supabase Auth]
  browser --> db[(Supabase Postgres)]
  statichost[Static host - Netlify/Vercel/etc] --> browser
```
- **Static host**: serves `index.html`, `admin/*`, `assets/*` (no server tier of our own, no build step).
- **Browser**: runs all app logic; talks directly to Supabase using `window.SOT_CONFIG` (anon key).
- **Supabase**: Auth + Postgres (schema in `supabase/schema.sql`). RLS not yet enabled (known gap).
