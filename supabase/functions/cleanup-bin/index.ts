// Scheduled bin cleanup (bin feature, AC2).
// Deploy: supabase functions deploy cleanup-bin (JWT verification disabled — it
// authenticates via CRON_SECRET). Schedule daily, e.g. "0 3 * * *".
// Secret: CRON_SECRET — the scheduler must send "Authorization: Bearer <CRON_SECRET>".
//
// Permanently removes bin rows whose expires_at (deleted_at + 30 days) has passed.
// The snapshot is discarded with the row, so recovery is no longer possible — which
// is the intended 30-day window (BR2/BR4). Source-table rows were already removed at
// soft-delete time, so this only purges the bin snapshots.
import { createClient } from "npm:@supabase/supabase-js@2";

Deno.serve(async (req) => {
  try {
    const auth = req.headers.get("Authorization") ?? "";
    if (auth !== `Bearer ${Deno.env.get("CRON_SECRET")}`) {
      return json({ error: "Forbidden" }, 403);
    }

    const service = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    // delete expired rows, returning what was purged for the run summary
    const { data, error } = await service
      .from("bin")
      .delete()
      .lt("expires_at", new Date().toISOString())
      .select("id, entity_type");
    if (error) throw error;

    return json({ ok: true, purged: data?.length ?? 0, at: new Date().toISOString() });
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
