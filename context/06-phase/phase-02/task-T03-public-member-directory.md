---
spec_version: 1
file_type: task
phase: 2
task_id: T03
feature: public-directory
status: done
---

# T03 — Public member directory

## Description
Expose an opt-in, privacy-safe public directory (spec §7). Members control a Show-on-Public-Directory flag; the public sees only safe fields (photo, name, profession, approved short bio) and never any private/contact/finance data. Enforcement is via a safe public view at the data layer, not hidden UI.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Member controls public visibility | ✅ |
| AC2 | Directory exposes only safe fields | ✅ |

## Implementation approach
1. Add a show_on_public_directory flag to members (member-controlled)
2. Create a safe public view exposing only photo, name, profession and approved bio for opted-in members
3. Build the public directory page reading only that view
4. Add the opt-in toggle to the member portal

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Create | `directory.html` | public directory page (safe view only) |
| Update | `supabase/schema.sql` | show_on_public_directory flag |
| Create | `supabase/rls.sql` | safe public directory view + read policy |
| Update | `member/profile.html` | directory opt-in toggle |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/public-directory/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/public-directory/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/public-directory/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
