// Email a payment receipt to the member (receipts feature, AC3).
// Deploy: supabase functions deploy send-receipt-email
// Secrets: RESEND_API_KEY (email provider), plus the standard SUPABASE_* env
// injected automatically. Receipts are emailed only — never sent over SMS (BR5).
import { createClient } from "npm:@supabase/supabase-js@2";

Deno.serve(async (req) => {
  try {
    const { receipt_no } = await req.json();
    if (!receipt_no) return json({ error: "receipt_no is required" }, 400);

    // Caller must be an active admin: verify their JWT against the admins table.
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
      .from("admins").select("id")
      .eq("auth_user_id", user.id).eq("active", true).maybeSingle();
    if (!admin) return json({ error: "Not an active admin" }, 403);

    // Load the receipt + the member's email.
    const { data: p, error } = await service
      .from("payments")
      .select("receipt_no, amount, purpose, payment_method, payment_date, members(name, member_id, house_name, email)")
      .eq("receipt_no", receipt_no).maybeSingle();
    if (error || !p) return json({ error: "Receipt not found" }, 404);
    const member = p.members as unknown as {
      name: string; member_id: string; house_name: string | null; email: string | null;
    };
    if (!member?.email) return json({ error: "Member has no email on file" }, 422);

    const html = `
      <div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;border:1px solid #e5e7eb;border-radius:12px;padding:32px">
        <h1 style="margin:0">Society of Twelve</h1>
        <p style="color:#64748b;margin:4px 0 24px">Payment receipt</p>
        <table style="width:100%;border-collapse:collapse">
          ${[
            ["Receipt no", p.receipt_no],
            ["Date", new Date(p.payment_date).toLocaleString()],
            ["Member", member.name],
            ["Member ID", member.member_id],
            ["House", member.house_name ?? "—"],
            ["Purpose", p.purpose],
            ["Method", p.payment_method],
            ["Amount", `BDT ${p.amount}`],
          ].map(([k, v]) =>
            `<tr><td style="color:#64748b;padding:8px 0;border-bottom:1px solid #eef1f4">${k}</td>
                 <td style="padding:8px 0;border-bottom:1px solid #eef1f4">${v}</td></tr>`).join("")}
        </table>
        <p style="color:#64748b;font-size:12px;margin-top:24px">This is a system-generated receipt.</p>
      </div>`;

    const resend = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${Deno.env.get("RESEND_API_KEY")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: "Society of Twelve <receipts@societyoftwelve.org>",
        to: [member.email],
        subject: `Payment receipt ${p.receipt_no}`,
        html,
      }),
    });
    if (!resend.ok) {
      const detail = await resend.text();
      console.error("resend failed:", detail);
      return json({ error: "Email provider rejected the message" }, 502);
    }

    return json({ ok: true, sent_to: member.email });
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
