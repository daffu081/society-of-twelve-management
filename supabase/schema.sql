create extension if not exists pgcrypto;
create table if not exists public.members (
 id uuid primary key default gen_random_uuid(), member_id text unique not null, name text not null,
 father_name text, house_name text, village text, mobile text not null, whatsapp text, email text,
 dob date, blood_group text, profession text, fee_category text, monthly_fee numeric(12,2), join_date date,
 active boolean default true, photo_url text, education jsonb, skills text[], interests text[],
 nid_number text, birth_registration_id text, passport_number text, short_bio text,
 show_on_public_directory boolean default false, created_at timestamptz default now(), updated_at timestamptz default now()
);
-- idempotent: add blood_group to members tables that already exist
alter table public.members add column if not exists blood_group text;
-- auto-generate the human-facing SOT#### id server-side (no client race; BR1 never-reused, never-editable)
create sequence if not exists public.members_member_id_seq;
alter table public.members
  alter column member_id set default 'SOT' || lpad(nextval('public.members_member_id_seq')::text, 4, '0');
-- ponytail: roster search/filter runs client-side over a small member base; these
-- indexes only matter if it grows into server-side filtering. Cheap to keep.
create index if not exists members_active_idx on public.members (active);
create index if not exists members_profession_idx on public.members (profession);
create index if not exists members_name_idx on public.members (name);
-- profession/fee tiers (profession-fee feature): admin-editable categories driving member dues.
-- members.fee_category holds the category name; members.monthly_fee is a per-member custom
-- override (null = use the category fee). Payments store their own amount, so editing a fee
-- here never rewrites history (BR4).
create table if not exists public.fee_categories (
 id uuid primary key default gen_random_uuid(), name text unique not null,
 monthly_fee numeric(12,2) not null, created_at timestamptz default now(), updated_at timestamptz default now()
);
-- receipt numbers (payments feature): SOT-YYYYMM-0001, resetting each month (BR5).
-- A per-month counter row updated atomically — no client race, numbers never reused.
-- finance (T08): recorded-by on money movements (BR5)
alter table public.income add column if not exists created_by uuid;
alter table public.expenses add column if not exists created_by uuid;
create table if not exists public.receipt_counters (month text primary key, counter integer not null);
create or replace function public.next_receipt_no() returns text
  language plpgsql volatile security definer set search_path = public as $$
declare m text := to_char(now(), 'YYYYMM'); n integer;
begin
  insert into receipt_counters (month, counter) values (m, 1)
  on conflict (month) do update set counter = receipt_counters.counter + 1
  returning counter into n;
  return 'SOT-' || m || '-' || lpad(n::text, 4, '0');
end;
$$;
alter table public.payments alter column receipt_no set default public.next_receipt_no();
-- notices (T10): meeting fields + archive state + SOT-NOT-YYYYMM-0001 reference numbers
alter table public.notices add column if not exists notice_type text default 'general';
alter table public.notices add column if not exists meeting_date date;
alter table public.notices add column if not exists meeting_time time;
alter table public.notices add column if not exists meeting_venue text;
alter table public.notices add column if not exists archived boolean default false;
create table if not exists public.notice_counters (month text primary key, counter integer not null);
create or replace function public.next_notice_ref_no() returns text
  language plpgsql volatile security definer set search_path = public as $$
declare m text := to_char(now(), 'YYYYMM'); n integer;
begin
  insert into notice_counters (month, counter) values (m, 1)
  on conflict (month) do update set counter = notice_counters.counter + 1
  returning counter into n;
  return 'SOT-NOT-' || m || '-' || lpad(n::text, 4, '0');
end;
$$;
alter table public.notices alter column ref_no set default public.next_notice_ref_no();
-- projects (T11): full detail + finance fields; images are URLs until the storage split (T25)
alter table public.projects add column if not exists image_urls text[];
alter table public.projects add column if not exists start_date date;
alter table public.projects add column if not exists end_date date;
alter table public.projects add column if not exists budget numeric(12,2);
alter table public.projects add column if not exists amount_spent numeric(12,2);
-- mahfil (T12): full event fields + publication state
alter table public.mahfils add column if not exists event_date date;
alter table public.mahfils add column if not exists event_time time;
alter table public.mahfils add column if not exists venue text;
alter table public.mahfils add column if not exists published boolean default false;
create table if not exists public.payments (
 id uuid primary key default gen_random_uuid(), receipt_no text unique not null, member_id uuid references public.members(id),
 amount numeric(12,2) not null, purpose text not null, payment_method text not null, payment_date timestamptz default now(), notes text, created_by uuid, created_at timestamptz default now()
);
create table if not exists public.notices (
 id uuid primary key default gen_random_uuid(), ref_no text unique not null, title text not null, body text not null,
 published boolean default false, running boolean default false, published_at timestamptz, created_at timestamptz default now(), updated_at timestamptz default now()
);
create table if not exists public.projects (id uuid primary key default gen_random_uuid(),title text not null,description text,status text default 'running',cover_url text,created_at timestamptz default now(),updated_at timestamptz default now());
create table if not exists public.mahfils (id uuid primary key default gen_random_uuid(),title text not null,description text,status text default 'running',cover_url text,created_at timestamptz default now(),updated_at timestamptz default now());
create table if not exists public.admins (id uuid primary key default gen_random_uuid(),auth_user_id uuid unique,name text not null,email text,role text default 'executive_admin',active boolean default true,permissions jsonb default '{}'::jsonb,created_at timestamptz default now());
create table if not exists public.sms_templates (id uuid primary key default gen_random_uuid(),template_key text unique not null,template_name text not null,body text not null,active boolean default true,updated_at timestamptz default now());
create table if not exists public.sms_logs (id uuid primary key default gen_random_uuid(),member_id uuid references public.members(id),template_key text,message_body text not null,status text default 'pending',provider_message_id text,sent_by uuid,sent_at timestamptz,created_at timestamptz default now());
create table if not exists public.birthday_logs (id uuid primary key default gen_random_uuid(),member_id uuid references public.members(id) not null,birthday_year integer not null,sms_log_id uuid references public.sms_logs(id),created_at timestamptz default now(),unique(member_id,birthday_year));
create table if not exists public.income (id uuid primary key default gen_random_uuid(),source text not null,amount numeric(12,2) not null,income_date date default current_date,payment_id uuid references public.payments(id),notes text,created_at timestamptz default now());
create table if not exists public.expenses (id uuid primary key default gen_random_uuid(),category text not null,amount numeric(12,2) not null,expense_date date default current_date,notes text,created_at timestamptz default now());
create table if not exists public.bin (id uuid primary key default gen_random_uuid(),entity_type text not null,entity_id uuid not null,deleted_by uuid,deleted_at timestamptz default now(),expires_at timestamptz default (now()+interval '30 days'),snapshot jsonb not null);
-- executive committee (T13): public roster in a configured order
create table if not exists public.committee_members (
 id uuid primary key default gen_random_uuid(), name text not null, position text not null,
 year text, short_bio text, photo_url text, display_order integer default 0,
 visible boolean default true, created_at timestamptz default now(), updated_at timestamptz default now()
);
-- founding members (T14): public historical recognition
create table if not exists public.founding_members (
 id uuid primary key default gen_random_uuid(), name text not null, historical_role text,
 short_bio text, photo_url text, display_order integer default 0,
 created_at timestamptz default now(), updated_at timestamptz default now()
);
-- awards (T16): achievements, optional member link, admin-controlled visibility
create table if not exists public.awards (
 id uuid primary key default gen_random_uuid(), title text not null, member_id uuid references public.members(id),
 recipient_name text, description text, award_date date, image_url text,
 visible boolean default false, created_at timestamptz default now(), updated_at timestamptz default now()
);
-- rules & regulations (T17): super-admin-managed, versioned
create table if not exists public.rules (
 id uuid primary key default gen_random_uuid(), title text not null, body text not null,
 status text default 'draft', -- draft | published | archived
 version integer default 1, display_order integer default 0,
 created_at timestamptz default now(), updated_at timestamptz default now()
);
create table if not exists public.rule_versions (
 id uuid primary key default gen_random_uuid(), rule_id uuid references public.rules(id) not null,
 version integer not null, title text not null, body text not null, status text,
 archived_at timestamptz default now()
);
-- sms (T19): recipient snapshot for the log (BR10) — member mobile at send time
alter table public.sms_logs add column if not exists recipient_mobile text;
