// Public front-end configuration. Loaded directly by the browser on every page.
// SAFE to commit: only the project URL and the *anon* (public) key belong here.
// NEVER put the Supabase service-role key or any other secret in this file —
// everything here is visible to every visitor. Row Level Security is what protects data.
window.SOT_CONFIG = {
  SUPABASE_URL: "https://YOUR-PROJECT-ref.supabase.co", // replace with the project URL
  SUPABASE_ANON_KEY: "YOUR-SUPABASE-ANON-KEY",          // anon/public key only — never the service-role key
};
