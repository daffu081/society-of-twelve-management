---
type: test-context
spec_version: 1
feature: rules
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [rules, test-context]
---

# Rules & Regulations — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 manage rules (super only) | 🟢 manual | — |
| AC2 version history | 🟢 manual | — |
| Non-super blocked | 🟢 manual | — |

## Manual checks
- AC1: as Super Admin, create a rule (draft) → publish → it appears on public `rules.html`;
  archive → it disappears. An executive opening `admin/rules.html` sees the super-only message,
  and their direct writes are rejected by RLS.
- AC2: edit a published rule's body → the list shows v2 and History shows v1 with the old text;
  edit again → v3 with two history entries. A publish/unpublish alone does not create a version.
