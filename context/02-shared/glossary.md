---
spec_version: 1
type: shared-reference
title: "Glossary"
tags: [shared, glossary, domain]
file_type: shared
frozen: false
last_review: 2026-08-13
---

# Glossary
# One row per domain term that an outsider would misread. Keep it sharp.

| Term | Means | Does NOT mean |
|---|---|---|
| Society of Twelve | The community organization this system serves | A group of exactly twelve people / a company |
| Member | A society member row in `members` (has a `member_id`) | An admin — those live in `admins` |
| Admin | A row in `admins` linked to a Supabase auth user, `active=true` | Any logged-in user |
| Super Admin | `admins.role = 'super_admin'` — full access | Just any admin |
| Executive Admin | `admins.role = 'executive_admin'` — limited by `permissions` jsonb | Super Admin |
| Mahfil | A religious/community gathering event (`mahfils` table) | A generic "project" |
| Running | Currently-active flag on a notice/project/mahfil (surfaced publicly) | Deleted / archived |
| Bin | Soft-delete holding table with 30-day expiry | A permanent audit log |
| Public directory | Members who set `show_on_public_directory = true` | All members |
