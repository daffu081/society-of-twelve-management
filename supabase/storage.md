# Storage buckets — public vs private (cross-cutting AC4, spec §30)

File storage separates **public images** from **private identity documents** so a
private document can never be reached by a public URL (BR6). Configure these in the
Supabase dashboard (Storage) or via the SQL below. No secret is needed in the browser —
uploads use the authenticated user's session; the anon key + RLS govern access.

## Buckets

| Bucket | Public? | Holds | Read | Write |
|--------|---------|-------|------|-------|
| `public-media` | **public** | profile photos, committee/project/mahfil/award images | anyone | active admins (members: own photo) |
| `private-docs` | **private** | NID / Birth Registration / Passport scans and any identity document | active admins only | active admins only |

`public-media` URLs are safe to embed on public pages (the `photo_url` / `image_url` /
`cover_url` fields point here). `private-docs` is never linked from a public page and has
no public URL — files are fetched through short-lived signed URLs by admins only.

## Setup (Supabase SQL editor)

```sql
-- create buckets (id, public flag)
insert into storage.buckets (id, name, public)
values ('public-media', 'public-media', true),
       ('private-docs', 'private-docs', false)
on conflict (id) do nothing;

-- public-media: world-readable; only active admins write
create policy "public-media read"  on storage.objects for select
  using (bucket_id = 'public-media');
create policy "public-media write" on storage.objects for insert
  with check (bucket_id = 'public-media' and public.is_active_admin());
create policy "public-media update" on storage.objects for update
  using (bucket_id = 'public-media' and public.is_active_admin());

-- private-docs: NO public read — active admins only, both directions
create policy "private-docs read"  on storage.objects for select
  using (bucket_id = 'private-docs' and public.is_active_admin());
create policy "private-docs write" on storage.objects for insert
  with check (bucket_id = 'private-docs' and public.is_active_admin());
```

## Rules
- Never store an identity document in `public-media`.
- Never make `private-docs` public or link it from a public page.
- Public pages read image URLs from `public-media` only.
- Serve `private-docs` files via `createSignedUrl` (short expiry), never a permanent public URL.
