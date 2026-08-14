// Daily birthday greetings (birthday feature, AC4).
// Deploy: supabase functions deploy birthday-cron --no-verify-jwt
// Schedule daily (spec BR3 — never manual), e.g. Supabase Dashboard → Edge Functions →
// cron "0 4 * * *", or pg_cron + pg_net invoking this URL.
// Secrets: the same SMS_PROVIDER_URL / SMS_API_KEY / SMS_SENDER_ID as send-sms, plus
// CRON_SECRET — the scheduler must send "Authorization: Bearer <CRON_SECRET>".
//
// Behaviour: finds active members whose dob matches today, skips anyone already
// greeted this year (birthday_logs unique member+year), renders the editable
// birthday_wish template with the member's real name, sends, and records
// sms_logs + birthday_logs. On provider failure/absence nothing is recorded,
// so the next run retries (the documented edge case).
import { createClient } from "npm:@supabase/supabase-js@2";

Deno.serve(async (req) => {
  try {
    // shared-secret gate: this endpoint is called by the scheduler, not a user
    const auth = req.headers.get("Authorization") ?? "";
    if (auth !== `Bearer ${Deno.env.get("CRON_SECRET")}`) {
      return json({ error: "Forbidden" }, 403);
    }

    const providerUrl = Deno.env.get("SMS_PROVIDER_URL");
    if (!providerUrl) return json({ error: "No SMS provider configured — will retry next run" }, 503);

    const service = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    const now = new Date();
    const year = now.getFullYear();
    const mmdd = `${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;

    // the editable template (BR6) — fall back to a sane default if missing
    const { data: tpl } = await service
      .from("sms_templates").select("body").eq("template_key", "birthday_wish").maybeSingle();
    const template = tpl?.body ?? "Society of Twelve: শুভ জন্মদিন {member_name}!";

    const { data: members, error } = await service
      .from("members").select("id, name, mobile, dob").eq("active", true).not("dob", "is", null);
    if (error) throw error;

    const { data: greeted } = await service
      .from("birthday_logs").select("member_id").eq("birthday_year", year);
    const greetedIds = new Set((greeted ?? []).map((g) => g.member_id));

    const birthdays = members.filter((m) =>
      m.dob?.slice(5) === mmdd && !greetedIds.has(m.id) && m.mobile);

    const results: { member: string; status: string }[] = [];
    for (const m of birthdays) {
      const body = template.replaceAll("{member_name}", m.name);
      const res = await fetch(providerUrl, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${Deno.env.get("SMS_API_KEY") ?? ""}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          to: m.mobile,
          message: body,
          sender_id: Deno.env.get("SMS_SENDER_ID") ?? "Society of Twelve",
        }),
      });
      if (!res.ok) {
        console.error(`send failed for ${m.id}:`, await res.text());
        results.push({ member: m.name, status: "failed — will retry next run" });
        continue; // no logs written → retried tomorrow
      }
      let providerMessageId: string | null = null;
      try { providerMessageId = JSON.parse(await res.text())?.message_id ?? null; } catch { /* non-JSON */ }

      const { data: smsLog } = await service.from("sms_logs").insert({
        member_id: m.id,
        template_key: "birthday_wish",
        message_body: body,
        status: "sent",
        provider_message_id: providerMessageId,
        recipient_mobile: m.mobile,
        sent_at: new Date().toISOString(),
      }).select("id").single();

      // yearly dedup (BR5) — unique(member_id, birthday_year) backs this up in the DB
      await service.from("birthday_logs").insert({
        member_id: m.id, birthday_year: year, sms_log_id: smsLog?.id ?? null,
      });
      results.push({ member: m.name, status: "sent" });
    }

    return json({ ok: true, date: mmdd, checked: members.length, sent: results });
  } catch (e) {
    console.error(e);
    return json({ error: "Unexpected error" }, 500);
  }
});

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
