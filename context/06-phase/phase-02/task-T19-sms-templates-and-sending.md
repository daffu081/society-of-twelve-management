---
spec_version: 1
file_type: task
phase: 2
task_id: T19
feature: sms
status: done
---

# T19 — SMS templates & sending

## Description
SMS layer (spec §11–§12): all message bodies are editable templates in the admin UI, sent through a configurable, replaceable external provider via a secure edge function (secrets never in the browser), under the Society of Twelve sender ID where supported. The six initial Bangla templates use dynamic placeholders resolved before sending, and every send is logged.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC4 | Edit templates | ✅ |
| AC5 | Send and log | ✅ |
| AC6 | Provider is replaceable and secret-safe | ✅ |

## Implementation approach
1. Add sms_templates and sms_log tables seeded with the six Bangla templates
2. Build a template editor gated by sms.template_edit
3. Build the send path via a send-sms edge function holding provider secrets server-side
4. Resolve placeholders, set the sender ID, and log recipient/template/status/trigger/sender on every send

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | sms_templates + sms_log tables |
| Create | `supabase/seed.sql` | six initial Bangla templates |
| Create | `supabase/functions/send-sms/index.ts` | provider-agnostic secure send |
| Create | `admin/sms.html` | template editor + send + log view |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/sms/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/sms/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/sms/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
