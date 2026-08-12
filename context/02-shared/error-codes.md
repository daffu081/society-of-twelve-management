---
spec_version: 1
type: shared-reference
title: "Error Codes"
tags: [shared, reference, errors]
file_type: shared
frozen: false
last_review: 2026-08-13
---

# Error handling

## App error type
There is no custom error type yet. Supabase calls return `{ data, error }`; surface `error.message`
to the user and `console.error(error)` for diagnostics (see `admin/admin.js` for the pattern).
When domain logic grows, introduce a single `AppError(code)` and list codes below.

## Error flow
```
Supabase call returns { data, error }
  → if error: console.error(error) + show error.message (or a mapped code below) in the UI
  → never swallow silently
```

## Domain error codes (canonical list)
Never invent a new code — add a row here first.

| Code | Where thrown | User-facing message |
|---|---|---|
| `AUTH_NO_ACCESS` | `checkAdminAccess()` — user not an active admin | This account does not have active admin access. |
| `AUTH_LINK_FAILED` | login `signInWithOtp` error | Unable to send login link. |
<!-- add one row per real domain error as features are built -->
