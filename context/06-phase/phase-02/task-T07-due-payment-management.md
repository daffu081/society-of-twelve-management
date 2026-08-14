---
spec_version: 1
file_type: task
phase: 2
task_id: T07
feature: due-payments
status: done
---

# T07 — Due payment management

## Description
Compute each member's monthly dues from their fee configuration (T04) and payment history (T05), surface Due Members with amounts and last-payment info, and let authorized admins send an editable due reminder (spec §14). Reminder delivery reuses the SMS layer (T19); the reminder text is editable before sending.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Due calculation | ✅ |
| AC2 | Send editable due reminder | ✅ |

## Implementation approach
1. Add a due-calculation query joining fee config and payments per member
2. Build a dashboard due-members list with amounts and last payment
3. Add an editable due-reminder composer gated by permission
4. Send via the T19 SMS path and log the send

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Create | `supabase/rls.sql` | due-calculation view/function |
| Update | `admin/dashboard.html` | due members panel + reminder action |
| Update | `admin/admin.js` | due list + reminder send |
| Update | `supabase/schema.sql` | indexes for due lookups |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/due-payments/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/due-payments/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/due-payments/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
