---
type: source
title: "Constraints"
last_review: 2026-08-13
---

# Constraints

- C1 (platforms): Web only. Public site in Bengali; admin UI mixed Bn/En.
- C2 (stack): Static HTML/CSS/vanilla JS (no framework, no build) + Supabase (Postgres + Auth). Supabase JS from CDN.
- C3 (budget / time): Volunteer-run community org — assume free/low-cost tiers (static host + Supabase free tier). <!-- TODO(user): confirm budget & timeline. -->
- C4 (legal / compliance): Stores personal data (NID, birth-registration, passport, mobile). Handle as sensitive; public exposure only via explicit `show_on_public_directory` consent.
