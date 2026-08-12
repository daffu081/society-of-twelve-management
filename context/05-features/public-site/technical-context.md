---
type: technical-context
spec_version: 1
feature: public-site
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: []
last_review: 2026-08-13
frozen: false
tags: [public-site, technical-context]
---

# Public site — technical context

## Public surface
**Depends on:** members, notices, projects, mahfil (for future dynamic content)
**Exposed to:** none (leaf page)

**Exposes:** nothing programmatic — it is the public entry page.
**Callers MUST NOT:** rely on it for data; it renders other features' public data read-only.

## Implementation status
| Capability | Status | Notes |
|---|---|---|
| Static sections | Done | `index.html` |
| Footer year | Done | `assets/js/app.js` |
| Running notices/projects/mahfil surfacing | Not started | placeholder copy only |
| Public member directory | Not started | needs `members` public read |

## Logic
- `assets/js/app.js`: sets `#year` to current year. That is the only behaviour today.

## Code file mapping
| File | Purpose |
|---|---|
| `index.html` | Public page markup (Bengali) |
| `assets/css/style.css` | Styles |
| `assets/js/app.js` | Footer year |

## API / data contracts
- None yet. Future: read-only Supabase selects for published notices, running projects/mahfil, and consenting members.

## Known issues
- All content is placeholder; no Supabase reads wired.
