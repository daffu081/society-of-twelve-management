-- Initial fee tiers (spec §8 / profession-fee BR1). Idempotent: existing rows keep
-- their admin-edited amounts. "Special Fee" is not a category — it is the per-member
-- custom override in members.monthly_fee.
insert into public.fee_categories (name, monthly_fee) values
  ('Business', 200.00),
  ('Jobholder', 100.00),
  ('Student', 50.00),
  ('High Ranking Officer', 200.00) -- admin-configurable; edit in admin/settings.html
on conflict (name) do nothing;
