---
type: test-context
spec_version: 1
feature: projects
file_type: test-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [projects, test-context]
---

# projects — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC3 full details & finance | 🟢 manual | — |
| AC4 soft-delete + restore | 🟢 manual | — |
| AC1/AC2 status + public display | 🟢 manual | — |

## Manual checks
- AC3: save a project with all fields → every field (incl. budget/spent as exact decimal strings,
  image URLs) persists and round-trips through edit.
- AC4: delete a project → it disappears from the list and appears in the Bin panel with a 30-day
  expiry; as Super Admin, restore → it returns intact; purge → it is gone. As an executive, the
  Bin panel is absent and direct bin selects return nothing (RLS).
- AC1/AC2: a running project shows under Running on public `projects.html`; flip to previous →
  it moves sections.
