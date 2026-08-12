---
spec_version: 1
type: arch-patterns
title: "Patterns"
tags: [architecture, patterns]
file_type: architecture
frozen: false
last_review: 2026-08-13
---

# Patterns
# Copy-paste reference implementations. Copy these instead of inventing.

## Supabase client (already created in admin.js — reuse, don't recreate)
```js
const { createClient } = window.supabase;
const supabaseClient = createClient(
  window.SOT_CONFIG.SUPABASE_URL,
  window.SOT_CONFIG.SUPABASE_ANON_KEY
);
```

## Guard every admin page
```js
(async () => {
  const result = await checkAdminAccess();   // from admin.js; redirects to login.html if not an active admin
  if (!result) return;
  const { admin } = result;
  // ...load and render feature data here...
})();
```

## Query with error handling (the house style)
```js
const { data, error } = await supabaseClient
  .from("members")
  .select("*")
  .eq("active", true);
if (error) {
  console.error(error);
  message.textContent = error.message || "Something went wrong.";
  return;
}
// use data
```

## Soft-delete (never DELETE) — move to bin
```js
// 1. snapshot the row, 2. insert into bin, 3. remove from source table
const { data: row } = await supabaseClient.from("notices").select("*").eq("id", id).single();
await supabaseClient.from("bin").insert({
  entity_type: "notices", entity_id: id, deleted_by: admin.id, snapshot: row
});
await supabaseClient.from("notices").delete().eq("id", id); // safe: snapshot preserved for 30 days
```

## Executive-admin permission check
```js
// super_admin bypasses; executive_admin must have the capability flag in permissions jsonb
function can(admin, capability) {
  return admin.role === "super_admin" || admin.permissions?.[capability] === true;
}
```
