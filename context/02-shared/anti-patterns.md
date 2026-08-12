---
spec_version: 1
type: shared-convention
title: "Anti-patterns"
tags: [shared, conventions, anti-patterns]
file_type: shared
frozen: false
last_review: 2026-08-13
---

# Anti-patterns
# Things the agent must NEVER do. Loaded on every task — keep it short and stack-specific.

## Architecture
- Never add a framework, bundler, or npm dependency without an ADR — this is a deliberately build-free static site.
- Never call across feature boundaries except through a feature's `## Public surface` section.
- Never put secrets in committed files — Supabase creds live in `config.js` (not the service-role key; anon key only in the client).

## Data / persistence
- Never hard-`DELETE` a domain row — move it to `bin` with a snapshot (ADR-003).
- Never use a JS float for money — money is `numeric(12,2)` in Postgres (ADR-002).
- Never trust the auth session alone for authorization — always re-check the `admins` table (`active=true`) (ADR-001).
- Never expose a member's private fields publicly unless `show_on_public_directory = true`.
- Never use the Supabase **service-role** key in client code — anon key only.

## Process
- Never mark a feature Done while its capability is a stub (a dashboard card with no wiring is Not started).
- Never hardcode a Supabase URL/key inline — read `window.SOT_CONFIG`.
- Never swallow a Supabase `error` — log it and surface a message.
