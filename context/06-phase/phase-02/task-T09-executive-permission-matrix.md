---
spec_version: 1
file_type: task
phase: 2
task_id: T09
feature: executive-admins
status: todo
---

# T09 — Executive permission matrix

## Description
Build the Executive Management screen (spec §16) where the Super Admin assigns granular permissions via a checkbox matrix over every area (members, payments, finance, notices+publish, projects, mahfil, sms+send+template_edit, birthday+manage, awards, rules, reports+export, committee, settings). Permissions are enforced server-side, not just by hiding menus, and the last active Super Admin cannot be removed.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC4 | Assign granular permissions | ⬜ |
| AC5 | Protect the last Super Admin | ⬜ |

## Implementation approach
1. Add role/permission tables and a permission-key catalog
2. Build the checkbox matrix UI to grant/revoke per executive
3. Enforce every key in RLS/server authorization, not only the frontend
4. Add a guard blocking removal/deactivation of the last active Super Admin

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | roles, permissions, admin_permissions tables |
| Create | `supabase/seed.sql` | permission-key catalog |
| Create | `admin/executives.html` | permission checkbox matrix |
| Update | `supabase/rls.sql` | permission enforcement + last-super-admin guard |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/executive-admins/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/executive-admins/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/executive-admins/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
