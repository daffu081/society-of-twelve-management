---
spec_version: 1
file_type: task
phase: 2
task_id: T25
feature: _cross-cutting
status: done
---

# T25 — Security, privacy & storage

## Description
The security, privacy and storage hardening layer (spec §7, §29–§30) underpinning every feature. Access control is enforced at the database/server layer (RLS + role/permission tables) so hiding menus is never the control; members access only their own records; public access uses explicitly safe views with payment/finance/NID/Birth-ID/Passport never exposed; and file storage separates public images from private identity documents. RLS is never disabled to make a feature work — build this early so the others have enforcement to target.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC2 | Enforced access control | ✅ |
| AC3 | Public exposure is safe-only | ✅ |
| AC4 | Storage separates public and private files | ✅ |

## Implementation approach
1. Enable RLS on every protected table with role/permission-backed policies
2. Build safe public views and verify private fields are unreachable via direct queries
3. Configure storage buckets: public (photos/images) vs private (identity documents)
4. Add direct-access tests proving member isolation and public-safety

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Create | `supabase/rls.sql` | RLS policies for all protected tables |
| Update | `supabase/schema.sql` | role/permission tables + safe views |
| Update | `config.js` | public bucket config only (no secrets) |
| Create | `supabase/storage.md` | public vs private bucket policy notes |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/_cross-cutting/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/_cross-cutting/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/_cross-cutting/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
