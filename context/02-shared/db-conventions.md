---
spec_version: 1
type: shared-convention
title: "Database / Persistence Conventions"
tags: [shared, conventions, persistence]
file_type: shared
frozen: false
last_review: 2026-08-13
---

# Persistence conventions
# Read before touching any table, schema, migration, or sync column.

## Identity
- D1: Primary keys are `uuid primary key default gen_random_uuid()` (server-generated via pgcrypto).
- D1b: Some tables also carry a human-facing unique text key: `members.member_id`, `payments.receipt_no`, `notices.ref_no`, `sms_templates.template_key`. Generate these app-side and rely on the DB unique constraint.

## Soft-delete
- D2: Never `DELETE` a domain row. Move it to `public.bin` with `entity_type`, `entity_id`, `deleted_by`, a full `snapshot jsonb`, and `expires_at = now() + 30 days`. Restore = re-insert from snapshot. (ADR-003)

## Money / precision
- D3: Money is `numeric(12,2)` in Postgres. Never use JS floats for money in app logic — read/write as strings or integer minor units and let Postgres hold the canonical value. (ADR-002)

## Timestamps
- D4: Every table has `created_at timestamptz default now()`; mutable tables also `updated_at`. Use DB `now()`, not client time.

## Migrations
- D5: Schema lives in `supabase/schema.sql`, written idempotently (`create table if not exists`). Changes are additive; apply via the Supabase SQL editor. No migration framework yet.

## Access control
- D6: Row-Level Security is NOT yet enabled — writes are currently gated only in the client via the `admins` check. This is a known security gap; add RLS policies before production. (ADR-001)
