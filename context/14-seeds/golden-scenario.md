---
type: seed
title: "Golden Scenario"
last_review: 2026-08-13
---

# Golden scenario
# One small deterministic dataset integration/E2E tests build on. Derived from the real schema.

## Setup
**admins**
- super: `{ auth_user_id: <seeded-auth-user>, name: "Sakib", email: "super@sot.test", role: "super_admin", active: true }`
- exec:  `{ auth_user_id: <seeded-auth-user-2>, name: "Rahim", email: "exec@sot.test", role: "executive_admin", active: true, permissions: { members: true, payments: true } }`
- inactive: `{ name: "Old Admin", email: "old@sot.test", role: "executive_admin", active: false }`

**members**
- M1: `{ member_id: "SOT-001", name: "Karim", mobile: "01700000001", monthly_fee: 200.00, dob: "1990-08-13", show_on_public_directory: true }`
- M2: `{ member_id: "SOT-002", name: "Jamal", mobile: "01700000002", monthly_fee: 200.00, show_on_public_directory: false }`

**payments**
- P1: `{ receipt_no: "R-0001", member_id: M1, amount: 200.00, purpose: "monthly_fee", payment_method: "cash" }`

**income / expenses**
- I1: `{ source: "monthly_fee", amount: 200.00, payment_id: P1 }`
- E1: `{ category: "mahfil", amount: 50.00 }`

## Expected derived outcomes
- Login as `super` → dashboard shows "Super Admin"; login as `old@sot.test` (inactive) → rejected (AC3 of admin-access).
- Public directory shows **M1 only** (M2 opted out).
- Finance: total income `200.00`, total expenses `50.00`, **balance `150.00`** (exact — ADR-002).
- Today (`2026-08-13`) M1's birthday is due exactly once (M1.dob month/day = 08-13); a second run produces no duplicate (`birthday_logs` unique).
