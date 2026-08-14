---
type: technical-context
spec_version: 1
feature: public-site
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: []
last_review: 2026-08-14
frozen: false
tags: [public-site, technical-context]
---

# Public site — technical context

## Public surface
**Depends on:** notices (running-notice banner); links to public-directory, projects, mahfil, notices, awards, rules, committee, founding-members, technical-team pages
**Exposed to:** none (leaf page)

**Exposes:** nothing programmatic — it is the public entry page.
**Callers MUST NOT:** rely on it for data; it renders other features' public data read-only.

## Implementation status
| Capability | Status | Notes |
|---|---|---|
| Static sections | Done | `index.html` |
| Footer year | Done | `assets/js/app.js` |
| Footer developer credit + branding | Done | `index.html`; credit links to technical-team.html |
| Full public page set (AC4) | Done | nav links every public page; About + History pages added |
| Running-notice banner | Done | homepage reads newest published running notice |
| Public member directory | Done | directory.html (public-directory feature) |

## Logic
- `assets/js/app.js`: sets `#year` to current year.
- `index.html`: full nav to every public page; each section links its module page; a small inline
  script loads the newest published running notice into the hero (falls back to placeholder).
- `about.html` / `history.html`: static Bengali content pages owned by this feature.

## Code file mapping
| File | Purpose |
|---|---|
| `index.html` | Homepage shell: nav, sections, running-notice banner |
| `about.html` | About Us + contact |
| `history.html` | Area History |
| `assets/css/style.css` | Styles |
| `assets/js/app.js` | Footer year |

## API / data contracts
- Homepage: one anon select on `notices` (running, published — RLS-limited). All other data lives
  on the module pages, each behind its own RLS/safe view.

## Known issues
- About/History body copy is placeholder pending client-provided content.
