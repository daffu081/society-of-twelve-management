---
spec_version: 1
type: shared-convention
title: "Tech Stack"
tags: [shared, dependencies, stack]
file_type: shared
frozen: false
last_review: 2026-08-13
---

# Tech stack
# The single source of truth for dependencies. Adding a package? Add a row + (if material) an ADR.

| Concern | Choice | Version | Notes |
|---|---|---|---|
| Language | JavaScript (ES2020+), HTML5, CSS3 | — | No transpiler, no bundler |
| Framework | none (vanilla DOM) | — | Static pages, `<script>` tags |
| Build tool | none | — | Files served as-is |
| Client library | @supabase/supabase-js | 2 (CDN `@2`) | Loaded from `cdn.jsdelivr.net` |
| Persistence | Supabase Postgres | cloud | Schema in `supabase/schema.sql` |
| Auth | Supabase Auth (magic-link OTP) | cloud | `signInWithOtp` |
| Config | `config.js` → `window.SOT_CONFIG` | — | `SUPABASE_URL`, `SUPABASE_ANON_KEY` (currently empty) |
| Hosting | static host + Supabase cloud | — | e.g. Netlify/Vercel/GitHub Pages/cPanel |
| Testing | none yet | — | No test runner installed |

## Version policy
Pin Supabase JS to major `@2` via CDN. There is no lockfile because there is no package manager;
if a build step or npm is ever introduced, add an ADR and a manifest first.

## Adding a dependency
1. Justify it against "can vanilla JS / an existing dep do this?".
2. Prefer a CDN `<script>` with a pinned major, or add a row above with an exact version.
3. Introducing npm/a bundler is an architectural change — write an ADR in `04-architecture/decisions/`.
