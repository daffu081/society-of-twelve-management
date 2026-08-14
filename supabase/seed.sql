-- Initial fee tiers (spec §8 / profession-fee BR1). Idempotent: existing rows keep
-- their admin-edited amounts. "Special Fee" is not a category — it is the per-member
-- custom override in members.monthly_fee.
insert into public.fee_categories (name, monthly_fee) values
  ('Business', 200.00),
  ('Jobholder', 100.00),
  ('Student', 50.00),
  ('High Ranking Officer', 200.00) -- admin-configurable; edit in admin/settings.html
on conflict (name) do nothing;

-- The six initial Bangla SMS templates (spec §12 / sms BR5-BR6). Idempotent:
-- admin-edited wording survives re-runs. Placeholders resolve before sending.
insert into public.sms_templates (template_key, template_name, body) values
  ('payment_success', 'Payment Success', 'Society of Twelve: প্রিয় {member_name}, আপনার {amount} টাকা পেমেন্ট সফল হয়েছে। রসিদ নং {receipt_no}। ধন্যবাদ।'),
  ('due_reminder', 'Due Payment Reminder', 'Society of Twelve: প্রিয় {member_name}, আপনার {due_amount} টাকা মাসিক ফি বকেয়া আছে। অনুগ্রহ করে পরিশোধ করুন।'),
  ('meeting_notice', 'Meeting Notice', 'Society of Twelve: {notice_text} — {date} {time}, {venue}।'),
  ('birthday_wish', 'Birthday Wish', 'Society of Twelve: শুভ জন্মদিন {member_name}! আপনার জীবন সুন্দর ও সাফল্যময় হোক।'),
  ('general_notice', 'General Notice', 'Society of Twelve: {notice_text}'),
  ('payment_thank_you', 'Payment Thank You', 'Society of Twelve: প্রিয় {member_name}, নিয়মিত ফি পরিশোধের জন্য আপনাকে আন্তরিক ধন্যবাদ।')
on conflict (template_key) do nothing;
