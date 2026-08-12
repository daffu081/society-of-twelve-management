---
type: requirement
spec_version: 1
title: "<Feature> — requirement"
feature: <feature-slug>
phase: <N>
tags: [<feature-slug>, requirement]
last_review: YYYY-MM-DD
---

# <Feature> — requirement

> **Pure business. Written for a non-technical client.** What they want and why — never how.
> Gathered by `/gather-requirement`. `/create-task` turns the ACs below into tasks;
> `/implement-task` later builds it and records the technical spec in `05-features/`.

## Goal
<!-- One sentence: what the client wants and why. -->

## User stories
- US1: As a <role>, I can <do something>, so that <benefit>.

## Business rules
- BR1: <plain-language constraint — no tech>.

## Acceptance criteria
<!-- Business outcomes only: what the user sees. No file names, classes, or test tiers.
     AC ids are permanent and unique per feature: if this feature already has ACs (an earlier
     phase's requirement, or its 05-features/business-context.md), continue the numbering — never
     restart at AC1, never reuse an id. Already-built ACs are append-only: don't reword in place. -->


### AC1: <title>
- **Trace**: US1, BR1
- **Given**: <starting situation>
- **When**: <the user does something>
- **Then**: <the outcome the client can see>

## Out of scope (not asked for)
- <what the client is explicitly NOT requesting>
