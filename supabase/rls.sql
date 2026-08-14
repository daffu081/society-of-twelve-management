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

-- Capability check (executive-admins permission matrix): super_admin has everything;
-- an executive admin needs the capability flag in admins.permissions jsonb (ADR-001).
-- Keys follow <area>_read / <area>_write plus extra actions (notices_publish, sms_send,
-- sms_template_edit, birthday_manage, reports_export) — the catalog lives in
-- admin/executives.html.
create or replace function public.has_permission(cap text) returns boolean
  language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.admins a
    where a.auth_user_id = auth.uid() and a.active = true
      and (a.role = 'super_admin' or coalesce((a.permissions ->> cap)::boolean, false))
  );
$$;

-- Is the current auth user an active Super Admin?
create or replace function public.is_super_admin() returns boolean
  language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.admins a
    where a.auth_user_id = auth.uid() and a.active = true and a.role = 'super_admin'
  );
$$;

-- Admins table (executive-admins): each admin reads their own row (the login gate
-- needs it); only Super Admins manage admin rows. Enforced here, not in menus (BR5).
alter table public.admins enable row level security;
drop policy if exists admins_self_read on public.admins;
create policy admins_self_read on public.admins
  for select using (auth_user_id = auth.uid());
drop policy if exists admins_super_all on public.admins;
create policy admins_super_all on public.admins
  for all using (public.is_super_admin()) with check (public.is_super_admin());

-- Never allow the last active Super Admin to be removed, demoted or deactivated (AC5/BR6).
create or replace function public.admins_protect_last_super() returns trigger
  language plpgsql security definer set search_path = public as $$
begin
  if old.role = 'super_admin' and old.active = true
     and (tg_op = 'DELETE' or new.role <> 'super_admin' or new.active = false) then
    if not exists (
      select 1 from public.admins
      where role = 'super_admin' and active = true and id <> old.id
    ) then
      raise exception 'Cannot remove, demote or deactivate the last active Super Admin';
    end if;
  end if;
  if tg_op = 'DELETE' then return old; end if;
  return new;
end;
$$;
drop trigger if exists admins_protect_last_super on public.admins;
create trigger admins_protect_last_super
  before update or delete on public.admins
  for each row execute function public.admins_protect_last_super();

alter table public.members enable row level security;

-- Permission-keyed access (BR5: enforced server-side, not menu-hiding).
-- Anon has no policy → RLS denies it entirely.
drop policy if exists members_admin_all on public.members;
drop policy if exists members_perm_read on public.members;
create policy members_perm_read on public.members
  for select using (public.has_permission('members_read'));
drop policy if exists members_perm_insert on public.members;
create policy members_perm_insert on public.members
  for insert with check (public.has_permission('members_write'));
drop policy if exists members_perm_update on public.members;
create policy members_perm_update on public.members
  for update using (public.has_permission('members_write'))
  with check (public.has_permission('members_write'));

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
-- Payments (payments feature): admins manage; members read their own rows only
-- through the payments_self view; anon gets nothing.
alter table public.payments enable row level security;
drop policy if exists payments_admin_all on public.payments;
drop policy if exists payments_perm_read on public.payments;
create policy payments_perm_read on public.payments
  for select using (public.has_permission('payments_read'));
drop policy if exists payments_perm_insert on public.payments;
create policy payments_perm_insert on public.payments
  for insert with check (public.has_permission('payments_write'));

-- Member-facing view: own payment history, matched by the member's email (AC5).
-- security_definer (default) bypasses base-table RLS; the WHERE clause isolates
-- the caller's own rows, so no member SELECT policy is needed on payments.
create or replace view public.payments_self as
  select p.receipt_no, p.amount, p.purpose, p.payment_method, p.payment_date, p.notes
  from public.payments p
  join public.members m on m.id = p.member_id
  where m.email is not null and lower(m.email) = lower(auth.jwt() ->> 'email');
grant select on public.payments_self to authenticated;

-- Receipt lookup (receipts feature): full receipt fields for one payment, readable by
-- an active admin or the owning member only (email match). Anon gets nothing.
create or replace view public.receipt_self as
  select p.receipt_no, p.amount, p.purpose, p.payment_method, p.payment_date, p.notes,
         m.name as member_name, m.member_id, m.house_name, a.name as recorded_by
  from public.payments p
  join public.members m on m.id = p.member_id
  left join public.admins a on a.id = p.created_by
  where public.is_active_admin()
     or (m.email is not null and lower(m.email) = lower(auth.jwt() ->> 'email'));
grant select on public.receipt_self to authenticated;

-- Member dues (due-payments feature): expected total = effective monthly fee ×
-- months from the join month through the current month; due = expected − paid.
-- Admin-only (the WHERE clause returns nothing for non-admins).
-- ponytail: dues assume the fee was constant since joining; per-month fee history
-- can replace months_expected × fee if the society ever needs retroactive accuracy.
create or replace view public.member_dues as
  select m.id, m.member_id, m.name, m.mobile,
         coalesce(m.monthly_fee, fc.monthly_fee, 0) as monthly_fee,
         gs.months_expected,
         coalesce(p.total_paid, 0) as total_paid,
         greatest(coalesce(m.monthly_fee, fc.monthly_fee, 0) * gs.months_expected
                  - coalesce(p.total_paid, 0), 0) as due_amount,
         p.last_payment_date
  from public.members m
  left join public.fee_categories fc on fc.name = m.fee_category
  cross join lateral (
    select (extract(year from age(current_date, coalesce(m.join_date, m.created_at::date))) * 12
          + extract(month from age(current_date, coalesce(m.join_date, m.created_at::date))) + 1)::int
          as months_expected
  ) gs
  left join lateral (
    select sum(amount) as total_paid, max(payment_date) as last_payment_date
    from public.payments where member_id = m.id
  ) p on true
  where m.active = true and public.is_active_admin();
grant select on public.member_dues to authenticated;

-- Finance (finance feature): never public (BR6); executives need the explicit
-- 'finance' permission (BR7). super_admin always passes has_permission().
alter table public.income enable row level security;
alter table public.expenses enable row level security;
drop policy if exists income_finance_all on public.income;
drop policy if exists income_finance_read on public.income;
create policy income_finance_read on public.income
  for select using (public.has_permission('finance_read'));
drop policy if exists income_finance_write on public.income;
create policy income_finance_write on public.income
  for insert with check (public.has_permission('finance_write'));
drop policy if exists expenses_finance_all on public.expenses;
drop policy if exists expenses_finance_read on public.expenses;
create policy expenses_finance_read on public.expenses
  for select using (public.has_permission('finance_read'));
drop policy if exists expenses_finance_write on public.expenses;
create policy expenses_finance_write on public.expenses
  for insert with check (public.has_permission('finance_write'));

-- Cumulative totals computed in SQL (never JS floats — ADR-002); rows only for
-- finance-permitted admins.
create or replace view public.finance_totals as
  select (select coalesce(sum(amount), 0) from public.income)   as total_income,
         (select coalesce(sum(amount), 0) from public.expenses) as total_expense,
         (select coalesce(sum(amount), 0) from public.income)
       - (select coalesce(sum(amount), 0) from public.expenses) as balance
  where public.has_permission('finance_read');
grant select on public.finance_totals to authenticated;

-- Notices (notices feature): public reads published, non-archived notices; admins
-- need notices_read/notices_write; flipping `published` additionally needs
-- notices_publish (enforced by trigger — BR5-style server-side gating).
alter table public.notices enable row level security;
drop policy if exists notices_public_read on public.notices;
create policy notices_public_read on public.notices
  for select using (published = true and coalesce(archived, false) = false);
drop policy if exists notices_perm_read on public.notices;
create policy notices_perm_read on public.notices
  for select using (public.has_permission('notices_read'));
drop policy if exists notices_perm_insert on public.notices;
create policy notices_perm_insert on public.notices
  for insert with check (public.has_permission('notices_write'));
drop policy if exists notices_perm_update on public.notices;
create policy notices_perm_update on public.notices
  for update using (public.has_permission('notices_write'))
  with check (public.has_permission('notices_write'));

create or replace function public.notices_guard_publish() returns trigger
  language plpgsql security definer set search_path = public as $$
begin
  if new.published is distinct from old.published
     and not public.has_permission('notices_publish') then
    raise exception 'Publishing a notice requires the notices_publish permission';
  end if;
  if new.published = true and old.published = false then
    new.published_at := now();
  end if;
  return new;
end;
$$;
drop trigger if exists notices_guard_publish on public.notices;
create trigger notices_guard_publish
  before update on public.notices
  for each row execute function public.notices_guard_publish();

-- Fee categories (profession-fee): any active admin reads (the member form needs
-- them); editing fees is a settings capability. No anon access.
alter table public.fee_categories enable row level security;
drop policy if exists fee_categories_admin_all on public.fee_categories;
drop policy if exists fee_categories_admin_read on public.fee_categories;
create policy fee_categories_admin_read on public.fee_categories
  for select using (public.is_active_admin());
drop policy if exists fee_categories_settings_write on public.fee_categories;
create policy fee_categories_settings_write on public.fee_categories
  for insert with check (public.has_permission('settings_write'));
drop policy if exists fee_categories_settings_update on public.fee_categories;
create policy fee_categories_settings_update on public.fee_categories
  for update using (public.has_permission('settings_write'))
  with check (public.has_permission('settings_write'));

create or replace view public.members_public as
  select name, profession, short_bio, photo_url
  from public.members
  where show_on_public_directory = true and active = true;
grant select on public.members_public to anon, authenticated;
