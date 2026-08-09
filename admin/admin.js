const { createClient } = window.supabase;

const supabaseClient = createClient(
  window.SOT_CONFIG.SUPABASE_URL,
  window.SOT_CONFIG.SUPABASE_ANON_KEY
);


// ======================================
// MAGIC LINK LOGIN
// ======================================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

  loginForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const email =
      document.getElementById("email").value.trim();

    const button =
      document.getElementById("loginButton");

    const message =
      document.getElementById("message");

    button.disabled = true;
    button.textContent = "Sending...";
    message.textContent = "";

    try {

      const { error } =
        await supabaseClient.auth.signInWithOtp({
          email: email,
          options: {
            emailRedirectTo:
              window.location.origin +
              "/admin/dashboard.html"
          }
        });

      if (error) {
        throw error;
      }

      message.style.color = "#16a34a";

      message.textContent =
        "Login link sent. Please check your email.";

    } catch (error) {

      console.error(error);

      message.style.color = "#dc2626";

      message.textContent =
        error.message || "Unable to send login link.";

    } finally {

      button.disabled = false;
      button.textContent = "Send Login Link";

    }

  });

}


// ======================================
// ADMIN ACCESS CHECK
// ======================================

async function checkAdminAccess() {

  const {
    data: { user }
  } = await supabaseClient.auth.getUser();

  if (!user) {

    window.location.href = "login.html";

    return null;
  }


  const { data: admin, error } =
    await supabaseClient
      .from("admins")
      .select("*")
      .eq("auth_user_id", user.id)
      .eq("active", true)
      .single();


  if (error || !admin) {

    await supabaseClient.auth.signOut();

    alert(
      "This account does not have active admin access."
    );

    window.location.href = "login.html";

    return null;
  }


  return {
    user,
    admin
  };
}


// ======================================
// LOGOUT
// ======================================

async function logoutAdmin() {

  await supabaseClient.auth.signOut();

  sessionStorage.clear();

  window.location.href = "login.html";
}