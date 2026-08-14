-- Row Level Security for members.
-- Idempotent; apply via the Supabase SQL editor after schema.sql.
--
-- Model:
--   * Active admins (admins.active = true) get full read/write on members.
--   * Anonymous/public gets NO access to the base table — public surfaces come
--     later through a dedicated safe view (public-directory, T03).
--   * A logged-in member reads their own row through the members_self view,
--     which excludes the three private identity fields (NID / birth reg /
--     passport) so they are never returned to a non-admin (AC4). The member may
--     update only permitted fields; a trigger restores everything else (AC5).

-- Is the current auth user an active admin?
create or replace function public.is_active_admin() returns boolean
  language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.admins a
    where a.auth_user_id = auth.uid() and a.active = true
  );
$$;

alter table public.members enable row level security;

-- Admins: full access. Anon has no policy → RLS denies it entirely.
drop policy if exists members_admin_all on public.members;
create policy members_admin_all on public.members
  for all using (public.is_active_admin()) with check (public.is_active_admin());

-- A member may UPDATE their own row (matched by email). No SELECT policy for
-- members on the base table: they read through members_self only, so the
-- private identity columns are never returned to them (AC4).
drop policy if exists members_self_update on public.members;
create policy members_self_update on public.members
  for update
  using (email is not null and lower(email) = lower(auth.jwt() ->> 'email'))
  with check (email is not null and lower(email) = lower(auth.jwt() ->> 'email'));

-- Member-facing view: own row, private identity fields excluded (AC4).
-- security_definer (default) so it bypasses base-table RLS; the WHERE clause
-- scopes it to the caller's own row, so no member SELECT policy is needed.
create or replace view public.members_self as
  select id, member_id, name, father_name, house_name, village, mobile, whatsapp,
         email, dob, blood_group, profession, fee_category, monthly_fee, join_date,
         active, photo_url, education, skills, interests, short_bio,
         show_on_public_directory, created_at, updated_at
  from public.members
  where email is not null and lower(email) = lower(auth.jwt() ->> 'email');
grant select on public.members_self to authenticated;

-- Enforce which columns a non-admin member may change (AC5): only education,
-- skills, interests, short_bio. Everything else (identity, fee, member_id,
-- status, private fields) is restored to its old value on a member edit.
create or replace function public.members_guard_self_edit() returns trigger
  language plpgsql security definer set search_path = public as $$
begin
  if not public.is_active_admin() then
    new.member_id := old.member_id;
    new.name := old.name;
    new.father_name := old.father_name;
    new.house_name := old.house_name;
    new.village := old.village;
    new.mobile := old.mobile;
    new.whatsapp := old.whatsapp;
    new.email := old.email;
    new.dob := old.dob;
    new.blood_group := old.blood_group;
    new.profession := old.profession;
    new.fee_category := old.fee_category;
    new.monthly_fee := old.monthly_fee;
    new.join_date := old.join_date;
    new.active := old.active;
    new.photo_url := old.photo_url;
    new.nid_number := old.nid_number;
    new.birth_registration_id := old.birth_registration_id;
    new.passport_number := old.passport_number;
    new.created_at := old.created_at;
    -- permitted to change: education, skills, interests, short_bio,
    -- and show_on_public_directory (the member owns their public visibility — AC1, public-directory)
  end if;
  return new;
end;
$$;

drop trigger if exists members_guard_self_edit on public.members;
create trigger members_guard_self_edit
  before update on public.members
  for each row execute function public.members_guard_self_edit();

-- Public directory (public-directory feature): a safe, anon-readable view exposing
-- only photo, name, profession and short bio for members who opted in. No private,
-- contact, fee or identity field is present, so none is retrievable by the public (AC2).
-- security_definer (default) so it bypasses base-table RLS; the WHERE clause limits
-- rows to opted-in members only (AC1/BR2).
-- Fee categories (profession-fee): admins manage; no anon access.
alter table public.fee_categories enable row level security;
drop policy if exists fee_categories_admin_all on public.fee_categories;
create policy fee_categories_admin_all on public.fee_categories
  for all using (public.is_active_admin()) with check (public.is_active_admin());

create or replace view public.members_public as
  select name, profession, short_bio, photo_url
  from public.members
  where show_on_public_directory = true and active = true;
grant select on public.members_public to anon, authenticated;
