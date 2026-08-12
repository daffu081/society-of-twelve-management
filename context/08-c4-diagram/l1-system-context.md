---
type: c4
level: 1
title: "L1 — System Context"
last_review: 2026-08-13
---

# L1 — System context

Who uses the system and what it talks to.
```mermaid
graph TD
  visitor[Community visitor] --> site[Society of Twelve site]
  admin[Committee admin] --> site
  site --> supabase[(Supabase: Postgres + Auth)]
  supabase --> email[Email provider - magic link]
  site -. planned .-> sms[SMS provider]
```
- **Visitor**: reads the public Bengali homepage.
- **Admin**: manages members, payments, finance, notices, projects, mahfil.
- **Supabase**: authentication (magic link) + data.
- **SMS provider**: planned, not yet contracted.
