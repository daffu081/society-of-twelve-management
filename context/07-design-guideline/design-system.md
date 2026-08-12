---
spec_version: 1
type: design-system
title: "Design System"
tags: [design, ui, theme]
file_type: design
frozen: false
last_review: 2026-08-13
---

# Design system
# Tokens extracted from `assets/css/style.css` and the admin inline styles. There is no theming
# layer yet — these are the de-facto values. When you add a CSS var layer, seed it from this table.

## Colour tokens
| Token | Value | Use |
|---|---|---|
| ink / brand-dark | `#111827` | Logo, footer, primary button bg |
| text | `#172033` / `#17202a` | Body text |
| text-muted | `#64748b` | Secondary text, captions |
| link | `#334155` | Nav links |
| bg | `#f6f8fb` (public) / `#f5f7fa` (admin) | Page background |
| bg-accent | `#eef2ff` | Hero band |
| surface | `#ffffff` | Cards, header, login box |
| border | `#e5e7eb` | Card/header borders, inputs |
| input-border | `#d1d5db` | Form fields |
| success | `#16a34a` | Success messages |
| error | `#dc2626` | Error messages |
> Rule: prefer these values over new literals; consolidate into CSS variables when the UI grows.

## Typography
| Style | Value | Use |
|---|---|---|
| Font family | `system-ui, "Noto Sans Bengali", sans-serif` (public); `Arial, sans-serif` (admin) | Bengali-capable system stack |
| Hero title | `clamp(2rem, 5vw, 4rem)` | Landing hero |
| Heading | ~20px bold | Section/card headings |
| Body | ~14–16px | Text |
| Logo weight | 800 | "SOT" mark |

## Spacing scale
Ad-hoc: common values `8 / 12 / 14 / 16 / 22 / 32px`; section padding `60px 5%`, hero `90px 5%`.

## Radius / elevation
- Radius: `8px` (buttons), `10–12px` (inputs/logo), `16–18px` (cards, login box), `999px` (pill).
- Elevation: login box `0 10px 35px rgba(0,0,0,.08)`; otherwise flat with 1px borders.

## Component conventions
- **Logo**: 48px (public) / 45px (admin) dark rounded square, white "SOT", weight 800.
- **Cards**: white, 1px `border`, radius 16px, grid `auto-fit minmax(210–240px, 1fr)`.
- **Buttons**: dark `#111827` bg, white text, radius 8–10px; disabled = opacity .6.
- **Messages**: success green / error red, centered under the form.
- **Header**: sticky white bar with brand + nav.
