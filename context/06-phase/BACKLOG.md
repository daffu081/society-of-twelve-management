---
type: backlog
title: "Backlog — unphased task ideas"
last_review: 2026-08-13
---

# Backlog

Tasks that should happen *eventually* but are **not** in the active phase. Nothing here is
loaded or worked on — it's a parking lot. Promote into a phase before working on it, then
delete the row.

| # | Title | Type | Note | Added |
|---|---|---|---|---|
| 9 | Fix login.html: remove unused password field | fix | magic-link only | 2026-08-13 |
| 12 | Mobile OTP login | feat | blocked on SMS provider | 2026-08-13 |
| 14 | Deploy runbook: apply `schema.sql` → `rls.sql` → `seed.sql`, deploy `send-receipt-email` fn + set `RESEND_API_KEY`, then grant permission keys to every executive via the T09 matrix | chore | ⚠️ post-T09 RLS, executives have NO area access until keys are granted (super admins unaffected) | 2026-08-14 |
| 15 | Run every feature's manual checks (each `test-context.md`) against a live Supabase project | chore | `config.js` still has placeholder creds; nothing T01–T12 is live-verified yet | 2026-08-14 |
| 16 | RLS on remaining tables: `sms_logs`, `birthday_logs`, `sms_templates`, counters | security | partially covered by T25 hardening; anyone with the anon key can write these today | 2026-08-14 |

_Rows 1–7, 13 delivered by phase-02 T01–T12; rows 8, 10, 11 exist as phase tasks T24, T19, T20._

## Rules
- Backlog rows are never worked on directly — promote first.
- Promoting = adding to the active phase, then deleting the row here.
- If the backlog grows large, that's a signal to start a new phase.
