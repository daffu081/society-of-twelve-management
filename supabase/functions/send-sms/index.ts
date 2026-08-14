// Send one queued SMS (sms feature, AC5/AC6).
// Deploy: supabase functions deploy send-sms
// Secrets (provider-agnostic — BR8; swap provider by changing config only):
//   SMS_PROVIDER_URL  — HTTP endpoint of the SMS gateway
//   SMS_API_KEY       — bearer/API key, held server-side only (never in the browser)
//   SMS_SENDER_ID     — sender header, default "Society of Twelve" (BR9)
// Body: { log_id } — a pending sms_logs row. The function resolves the recipient's
// mobile, posts to the provider, and updates the row to sent/failed with the
// provider message id (BR10).
import { createClient } from "npm:@supabase/supabase-js@2";

Deno.serve(async (req) => {
  try {
    const { log_id } = await req.json();
    if (!log_id) return json({ error: "log_id is required" }, 400);

    // Caller must be an admin with the sms_send permission (BR7).
    const authHeader = req.headers.get("Authorization") ?? "";
    const anon = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      { global: { headers: { Authorization: authHeader } } },
    );
    const { data: { user } } = await anon.auth.getUser();
    if (!user) return json({ error: "Not signed in" }, 401);

    const service = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );
    const { data: admin } = await service
      .from("admins").select("id, role, permissions")
      .eq("auth_user_id", user.id).eq("active", true).maybeSingle();
    const canSend = admin && (admin.role === "super_admin" || admin.permissions?.sms_send === true);
    if (!canSend) return json({ error: "Missing sms_send permission" }, 403);

    // Load the pending log row + recipient mobile.
    const { data: log } = await service
      .from("sms_logs").select("id, status, message_body, members(mobile)")
      .eq("id", log_id).maybeSingle();
    if (!log) return json({ error: "Log row not found" }, 404);
    if (log.status !== "pending") return json({ error: `Already ${log.status}` }, 409);
    const mobile = (log.members as unknown as { mobile: string } | null)?.mobile;
    if (!mobile) return json({ error: "Member has no mobile number" }, 422);

    const providerUrl = Deno.env.get("SMS_PROVIDER_URL");
    if (!providerUrl) {
      // No provider contracted yet — leave the row pending, tell the caller plainly.
      return json({ error: "No SMS provider configured (SMS_PROVIDER_URL unset)" }, 503);
    }

    // ponytail: one generic JSON POST covers most Bangladeshi gateways; add a
    // per-provider adapter here only when a contracted provider's API demands it.
    const res = await fetch(providerUrl, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${Deno.env.get("SMS_API_KEY") ?? ""}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        to: mobile,
        message: log.message_body,
        sender_id: Deno.env.get("SMS_SENDER_ID") ?? "Society of Twelve",
      }),
    });
    const providerBody = await res.text();
    let providerMessageId: string | null = null;
    try { providerMessageId = JSON.parse(providerBody)?.message_id ?? null; } catch { /* non-JSON reply */ }

    const status = res.ok ? "sent" : "failed";
    await service.from("sms_logs").update({
      status,
      provider_message_id: providerMessageId,
      recipient_mobile: mobile,
      sent_at: new Date().toISOString(),
    }).eq("id", log_id);

    if (!res.ok) {
      console.error("provider rejected:", providerBody);
      return json({ error: "Provider rejected the message", status }, 502);
    }
    return json({ ok: true, status, sent_to: mobile });
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
