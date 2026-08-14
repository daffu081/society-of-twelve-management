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

-- Projects (projects feature): public reads all (running + previous showcase);
-- writes need projects_write. Soft-delete goes through bin (ADR-003).
alter table public.projects enable row level security;
drop policy if exists projects_public_read on public.projects;
create policy projects_public_read on public.projects
  for select using (true);
drop policy if exists projects_perm_insert on public.projects;
create policy projects_perm_insert on public.projects
  for insert with check (public.has_permission('projects_write'));
drop policy if exists projects_perm_update on public.projects;
create policy projects_perm_update on public.projects
  for update using (public.has_permission('projects_write'))
  with check (public.has_permission('projects_write'));
drop policy if exists projects_perm_delete on public.projects;
create policy projects_perm_delete on public.projects
  for delete using (public.has_permission('projects_write'));

-- Mahfil (mahfil feature): public reads published only; writes need mahfil_write.
alter table public.mahfils enable row level security;
drop policy if exists mahfils_public_read on public.mahfils;
create policy mahfils_public_read on public.mahfils
  for select using (published = true);
drop policy if exists mahfils_perm_read on public.mahfils;
create policy mahfils_perm_read on public.mahfils
  for select using (public.has_permission('mahfil_read'));
drop policy if exists mahfils_perm_insert on public.mahfils;
create policy mahfils_perm_insert on public.mahfils
  for insert with check (public.has_permission('mahfil_write'));
drop policy if exists mahfils_perm_update on public.mahfils;
create policy mahfils_perm_update on public.mahfils
  for update using (public.has_permission('mahfil_write'))
  with check (public.has_permission('mahfil_write'));

-- Bin (ADR-003): area-permitted admins insert snapshots when soft-deleting;
-- only a Super Admin reads, restores (delete-after-restore) or purges (BR5).
-- Full bin lifecycle/cleanup is the bin feature (T24).
alter table public.bin enable row level security;
drop policy if exists bin_admin_insert on public.bin;
create policy bin_admin_insert on public.bin
  for insert with check (public.is_active_admin());
drop policy if exists bin_super_read on public.bin;
create policy bin_super_read on public.bin
  for select using (public.is_super_admin());
drop policy if exists bin_super_delete on public.bin;
create policy bin_super_delete on public.bin
  for delete using (public.is_super_admin());

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

-- Committee (committee feature): public reads visible entries; writes need committee_write.
alter table public.committee_members enable row level security;
drop policy if exists committee_public_read on public.committee_members;
create policy committee_public_read on public.committee_members
  for select using (visible = true);
drop policy if exists committee_perm_read on public.committee_members;
create policy committee_perm_read on public.committee_members
  for select using (public.has_permission('committee_read'));
drop policy if exists committee_perm_insert on public.committee_members;
create policy committee_perm_insert on public.committee_members
  for insert with check (public.has_permission('committee_write'));
drop policy if exists committee_perm_update on public.committee_members;
create policy committee_perm_update on public.committee_members
  for update using (public.has_permission('committee_write'))
  with check (public.has_permission('committee_write'));

-- Founding members (founding-members feature): public reads all; writes need committee_write
-- (same custodians as the committee roster — no separate key in the BR4 catalog).
alter table public.founding_members enable row level security;
drop policy if exists founding_public_read on public.founding_members;
create policy founding_public_read on public.founding_members
  for select using (true);
drop policy if exists founding_perm_insert on public.founding_members;
create policy founding_perm_insert on public.founding_members
  for insert with check (public.has_permission('committee_write'));
drop policy if exists founding_perm_update on public.founding_members;
create policy founding_perm_update on public.founding_members
  for update using (public.has_permission('committee_write'))
  with check (public.has_permission('committee_write'));

-- Awards (awards feature): public reads visible awards; writes need awards_write.
alter table public.awards enable row level security;
drop policy if exists awards_public_read on public.awards;
create policy awards_public_read on public.awards
  for select using (visible = true);
drop policy if exists awards_perm_read on public.awards;
create policy awards_perm_read on public.awards
  for select using (public.has_permission('awards_read'));
drop policy if exists awards_perm_insert on public.awards;
create policy awards_perm_insert on public.awards
  for insert with check (public.has_permission('awards_write'));
drop policy if exists awards_perm_update on public.awards;
create policy awards_perm_update on public.awards
  for update using (public.has_permission('awards_write'))
  with check (public.has_permission('awards_write'));

-- Rules (rules feature): public reads published; ONLY Super Admins write (BR2).
alter table public.rules enable row level security;
drop policy if exists rules_public_read on public.rules;
create policy rules_public_read on public.rules
  for select using (status = 'published');
drop policy if exists rules_super_all on public.rules;
create policy rules_super_all on public.rules
  for all using (public.is_super_admin()) with check (public.is_super_admin());

alter table public.rule_versions enable row level security;
drop policy if exists rule_versions_super_all on public.rule_versions;
create policy rule_versions_super_all on public.rule_versions
  for all using (public.is_super_admin()) with check (public.is_super_admin());

-- Version history (AC2): every content change snapshots the previous version.
create or replace function public.rules_keep_history() returns trigger
  language plpgsql security definer set search_path = public as $$
begin
  if new.title is distinct from old.title or new.body is distinct from old.body then
    insert into rule_versions (rule_id, version, title, body, status)
    values (old.id, old.version, old.title, old.body, old.status);
    new.version := old.version + 1;
  end if;
  new.updated_at := now();
  return new;
end;
$$;
drop trigger if exists rules_keep_history on public.rules;
create trigger rules_keep_history
  before update on public.rules
  for each row execute function public.rules_keep_history();

-- SMS (sms feature): templates readable by any active admin, editable only with
-- sms_template_edit; logs readable with sms_read, queueable by active admins.
-- Status updates happen in the send-sms edge function (service role bypasses RLS).
alter table public.sms_templates enable row level security;
drop policy if exists sms_templates_admin_read on public.sms_templates;
create policy sms_templates_admin_read on public.sms_templates
  for select using (public.is_active_admin());
drop policy if exists sms_templates_edit on public.sms_templates;
create policy sms_templates_edit on public.sms_templates
  for update using (public.has_permission('sms_template_edit'))
  with check (public.has_permission('sms_template_edit'));
drop policy if exists sms_templates_insert on public.sms_templates;
create policy sms_templates_insert on public.sms_templates
  for insert with check (public.has_permission('sms_template_edit'));

alter table public.sms_logs enable row level security;
drop policy if exists sms_logs_perm_read on public.sms_logs;
create policy sms_logs_perm_read on public.sms_logs
  for select using (public.has_permission('sms_read'));
drop policy if exists sms_logs_admin_insert on public.sms_logs;
create policy sms_logs_admin_insert on public.sms_logs
  for insert with check (public.is_active_admin());

-- Dashboard aggregates (dashboard feature): money summed in SQL (ADR-002),
-- each view gated on the matching area permission (BR1).
create or replace view public.payments_summary as
  select (select coalesce(sum(amount), 0) from public.payments
            where date_trunc('month', payment_date) = date_trunc('month', now())) as month_collection,
         (select coalesce(sum(amount), 0) from public.payments
            where payment_date::date = current_date) as today_collection
  where public.has_permission('payments_read');
grant select on public.payments_summary to authenticated;

create or replace view public.payments_by_method as
  select payment_method, coalesce(sum(amount), 0) as total, count(*) as n
  from public.payments
  where public.has_permission('payments_read')
  group by payment_method;
grant select on public.payments_by_method to authenticated;

create or replace view public.payments_by_month as
  select to_char(date_trunc('month', payment_date), 'YYYY-MM') as month,
         coalesce(sum(amount), 0) as total
  from public.payments
  where payment_date > now() - interval '6 months'
    and public.has_permission('payments_read')
  group by 1 order by 1;
grant select on public.payments_by_month to authenticated;

create or replace view public.members_by_profession as
  select coalesce(profession, 'Unknown') as profession, count(*) as n
  from public.members
  where active = true and public.has_permission('members_read')
  group by 1 order by n desc;
grant select on public.members_by_profession to authenticated;

-- Reports (reports feature): permission-gated report views. Each view's WHERE
-- clause checks reports_read AND the source area's own permission, so a report
-- returns rows only to admins allowed to see that data (BR3). Exports read the
-- same views, so export inherits the same gating.
create or replace view public.report_member_list as
  select member_id, name, mobile, profession, fee_category, blood_group,
         case when active then 'Active' else 'Inactive' end as status, join_date
  from public.members
  where public.has_permission('reports_read') and public.has_permission('members_read');
grant select on public.report_member_list to authenticated;

create or replace view public.report_payment_history as
  select p.receipt_no, m.member_id, m.name, p.amount, p.purpose, p.payment_method, p.payment_date
  from public.payments p left join public.members m on m.id = p.member_id
  where public.has_permission('reports_read') and public.has_permission('payments_read');
grant select on public.report_payment_history to authenticated;

create or replace view public.report_monthly_collection as
  select to_char(date_trunc('month', payment_date), 'YYYY-MM') as month,
         count(*) as payments, coalesce(sum(amount), 0) as total
  from public.payments
  where public.has_permission('reports_read') and public.has_permission('payments_read')
  group by 1 order by 1 desc;
grant select on public.report_monthly_collection to authenticated;

create or replace view public.report_due_members as
  select member_id, name, mobile, monthly_fee, due_amount, last_payment_date
  from public.member_dues
  where due_amount > 0 and public.has_permission('reports_read');
grant select on public.report_due_members to authenticated;

create or replace view public.report_income as
  select source, amount, income_date, notes from public.income
  where public.has_permission('reports_read') and public.has_permission('finance_read');
grant select on public.report_income to authenticated;

create or replace view public.report_expense as
  select category, amount, expense_date, notes from public.expenses
  where public.has_permission('reports_read') and public.has_permission('finance_read');
grant select on public.report_expense to authenticated;

create or replace view public.report_project_finance as
  select title, status, budget, amount_spent,
         (coalesce(budget,0) - coalesce(amount_spent,0)) as remaining
  from public.projects
  where public.has_permission('reports_read') and public.has_permission('projects_read');
grant select on public.report_project_finance to authenticated;

create or replace view public.report_sms_log as
  select s.template_key, m.name as member, s.recipient_mobile, s.status, s.sent_at, s.created_at
  from public.sms_logs s left join public.members m on m.id = s.member_id
  where public.has_permission('reports_read') and public.has_permission('sms_read');
grant select on public.report_sms_log to authenticated;

create or replace view public.report_birthday_log as
  select b.birthday_year, m.member_id, m.name, b.created_at
  from public.birthday_logs b left join public.members m on m.id = b.member_id
  where public.has_permission('reports_read') and public.has_permission('sms_read');
grant select on public.report_birthday_log to authenticated;

-- Audit log (audit feature): any active admin may append (their own actions);
-- only Super Admins may read the trail (BR — Super-Admin accountability view).
-- A generic trigger captures inserts/updates/deletes on the sensitive tables
-- with actor + old/new snapshots (BR2/BR3). auth.uid() resolves the actor.
alter table public.audit_log enable row level security;
drop policy if exists audit_admin_insert on public.audit_log;
create policy audit_admin_insert on public.audit_log
  for insert with check (public.is_active_admin());
drop policy if exists audit_super_read on public.audit_log;
create policy audit_super_read on public.audit_log
  for select using (public.is_super_admin());

create or replace function public.audit_capture() returns trigger
  language plpgsql security definer set search_path = public as $$
declare a record; aid uuid; aname text;
begin
  select id, name into aid, aname from public.admins where auth_user_id = auth.uid() limit 1;
  insert into public.audit_log (actor_admin_id, actor_name, action, entity_type, entity_id, old_values, new_values)
  values (
    aid, aname, tg_op, tg_table_name,
    coalesce((case when tg_op = 'DELETE' then old.id else new.id end), null),
    case when tg_op in ('UPDATE','DELETE') then to_jsonb(old) end,
    case when tg_op in ('INSERT','UPDATE') then to_jsonb(new) end
  );
  if tg_op = 'DELETE' then return old; end if;
  return new;
end;
$$;

-- Sensitive tables to audit (BR3): permission changes, member changes, payments,
-- finance, sms sends, deletions/restores (bin). Idempotent re-create.
do $$
declare t text;
begin
  foreach t in array array['admins','members','payments','income','expenses','sms_logs','bin'] loop
    execute format('drop trigger if exists audit_%1$s on public.%1$s', t);
    execute format('create trigger audit_%1$s after insert or update or delete on public.%1$s
                    for each row execute function public.audit_capture()', t);
  end loop;
end $$;

-- =====================================================================
-- T25 hardening sweep: RLS on every remaining table (AC2 — no table is
-- reachable by the anon key without a policy). Counter tables are touched
-- ONLY by security-definer functions (next_receipt_no/next_notice_ref_no),
-- so enabling RLS with no client policy denies all direct access while the
-- functions keep working.
-- =====================================================================
alter table public.receipt_counters enable row level security;  -- no policy: client-deny
alter table public.notice_counters enable row level security;   -- no policy: client-deny

-- birthday_logs: written only by the birthday-cron (service role bypasses RLS);
-- readable for the birthday delivery report with sms_read.
alter table public.birthday_logs enable row level security;
drop policy if exists birthday_logs_perm_read on public.birthday_logs;
create policy birthday_logs_perm_read on public.birthday_logs
  for select using (public.has_permission('sms_read'));

-- Access-control coverage summary (AC2/AC3) — every protected table has RLS:
--   members          admin keyed; members read own via members_self; anon none
--   payments/income/expenses  keyed; members read own payments via payments_self; anon none
--   admins           self-read + super-manage; last-super guard
--   fee_categories/notices/projects/mahfils/committee_members/founding_members/awards/rules
--                    keyed writes; public reads only the safe/published/visible rows
--   sms_templates/sms_logs/birthday_logs   keyed; no public access
--   bin/audit_log/rule_versions            Super-Admin scoped
--   *_counters       function-only (RLS on, no client policy)
-- Safe public surfaces (AC3 — no payment/finance/NID/Birth-Reg/Passport ever returned):
--   members_public (directory), notices/projects/mahfils/committee/founding/awards/rules
--   public reads — none of these views/policies expose a private identity, contact,
--   payment or finance column.
