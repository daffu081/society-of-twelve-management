// Member portal client. Separate from the admin client — members authenticate
// with their own email (Supabase magic link) and only ever touch their own row
// through RLS (members_self view + members_self_update policy).
const { createClient } = window.supabase;

const memberClient = createClient(
  window.SOT_CONFIG.SUPABASE_URL,
  window.SOT_CONFIG.SUPABASE_ANON_KEY
);

// Returns the logged-in member's own profile (private identity fields excluded
// by the members_self view), or redirects to login. Null on no session.
async function loadMemberSelf() {
  const { data: { user } } = await memberClient.auth.getUser();
  if (!user) {
    window.location.href = "login.html";
    return null;
  }
  const { data, error } = await memberClient
    .from("members_self")
    .select("*")
    .maybeSingle();
  if (error) {
    console.error(error);
    return null;
  }
  return { user, member: data };
}

async function logoutMember() {
  await memberClient.auth.signOut();
  window.location.href = "login.html";
}
