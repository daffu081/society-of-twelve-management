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
| 1 | Wire members CRUD + public-directory consent | feat | needs `admin/members.*` | 2026-08-13 |
| 2 | Wire payments + receipts | feat | unique receipt_no; refs members | 2026-08-13 |
| 3 | Wire finance (income/expenses + balance) | feat | exact money totals | 2026-08-13 |
| 4 | Wire notices publish + running-on-homepage | feat | ties to public-site | 2026-08-13 |
| 5 | Wire projects + mahfil admin + public render | feat | near-identical CRUD | 2026-08-13 |
| 6 | Executive-admin management + checkbox permissions | feat | super-admin only | 2026-08-13 |
| 7 | Enable Postgres RLS on all tables | security | close the client-only-gate gap (ADR-001) | 2026-08-13 |
| 8 | Bin purge job (delete rows past expires_at) + restore UI | chore | ADR-003 | 2026-08-13 |
| 9 | Fix login.html: remove unused password field | fix | magic-link only | 2026-08-13 |
| 10 | SMS templates/logs + provider integration | feat | blocked on provider | 2026-08-13 |
| 11 | Birthday greeting automation + scheduler | feat | blocked on sms | 2026-08-13 |
| 12 | Mobile OTP login | feat | blocked on SMS provider | 2026-08-13 |
| 13 | Email receipts + Google Sheets export | feat | later-stage plan items | 2026-08-13 |

## Rules
- Backlog rows are never worked on directly — promote first.
- Promoting = adding to the active phase, then deleting the row here.
- If the backlog grows large, that's a signal to start a new phase.
