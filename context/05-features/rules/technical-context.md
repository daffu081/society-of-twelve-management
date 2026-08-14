---
type: technical-context
spec_version: 1
feature: rules
file_type: technical-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [rules, technical-context]
---

# Rules & Regulations — technical context

## Public surface
**Depends on:** admin-access; executive-admins (`is_super_admin()`).
**Exposed to:** public-site (`rules.html` reads published rows).

**Exposes:**
```
public.rules          -- table; anon sees status = 'published' only (RLS);
                      -- writes are Super-Admin-only
public.rule_versions  -- history table; Super-Admin-only (RLS)
```
**Callers MUST NOT:** write rules from any non-super path; show non-published rules publicly.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Create/edit/publish/archive (super only) | AC1 | ✅ built | needs live Supabase to verify |
| Automatic version history on edit | AC2 | ✅ built | `rules_keep_history` DB trigger |

## Logic
- `admin/rules.html`: Super-Admin-only (client gate + RLS). Create/edit form; list actions
  publish/unpublish/archive; History viewer reads `rule_versions` per rule.
- `rules_keep_history` trigger (in `rls.sql`): on any title/body change, snapshots the old
  content into `rule_versions` and bumps `rules.version` — history is automatic, not client-driven.
- `rules.html` (public): numbered list of published rules ordered by `display_order`.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/rules.html` | Super-Admin rules management + history viewer |
| `rules.html` | Public published-rules page |
| `supabase/schema.sql` | `rules` + `rule_versions` tables |
| `supabase/rls.sql` | rules policies + history trigger |

## API / data contracts
- Select (public, published-only) on `rules`; super-only writes; super-only reads on `rule_versions`.

## Known issues
- Status-only changes (publish/archive) don't create versions — deliberate: only content changes
  are history-worthy.
