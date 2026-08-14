---
spec_version: 1
file_type: task
phase: 2
task_id: T01
feature: member-profile
status: done
---

# T01 — Full member profile

## Description
Phase 01 added only the blood-group field; this task builds the complete member record from spec §6–§7 — the full identity/contact/fee/status/photo/optional-bio field set, the three strictly-private identity documents (NID, Birth Registration, Passport), an auto-generated SOT#### member ID, and member self-service editing of permitted fields. It is the data backbone every downstream feature (payments, dues, directory, receipts) builds on, so it lands first in the phase.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC3 | Full profile captured | ✅ |
| AC4 | Private identity fields stored but hidden | ✅ |
| AC5 | Member self-service edit | ✅ |

## Implementation approach
1. Extend the members table with the full field set and an auto SOT#### id sequence (blood_group already exists)
2. Store NID/Birth-Reg/Passport in a private-only shape and exclude them from every public and member-visible view
3. Build the admin registration/edit form to capture all fields and render the read-only profile
4. Add a member self-service edit page limited to permitted fields (skills, interests, bio) and block identity/fee/status/id edits

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | full member columns + SOT#### id generation |
| Create | `supabase/rls.sql` | hide private identity fields from non-admin/public |
| Update | `admin/members.html` | full registration/edit form + profile view |
| Create | `member/profile.html` | member self-service edit (permitted fields only) |
| Create | `member/member.js` | member portal profile logic |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/member-profile/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/member-profile/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/member-profile/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
