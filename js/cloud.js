/* The Reader's Atlas — account (cloud step 1, 11-19): sign in with an emailed link, no password.
   The backend is Supabase for now (js/vendor/supabase.js). The key below is the project's publishable key: it is meant
   to be public, and the database's row-level security decides what it can reach. No secret key belongs in this repo.
   This file owns the account button beside the language toggle and its dialog; app.js does not know about it.
   Signing in is optional: without an account everything keeps working from this browser's storage (js/store.js).
   Exposed as window.RA_CLOUD = { user(), client, onChange(fn) } for the sync step that comes next. */
(function () {
  "use strict";
  const URL_ = "https://silmbyjeyotyngdnwcdf.supabase.co";
  const KEY = "sb_publishable_Ft7WS4ta2Vc4jXqqhyFueA_W84FlSwO";
  const btn = document.getElementById("account-btn");
  const dlg = document.getElementById("account-dialog");
  const RS = window.RA_STORE;
  const T = () => window.RA_I18N[RS.prefs.get("lang", "en") === "zh" ? "zh" : "en"];
  // an emailed link has to come back to a web address: a double-clicked index.html (file://) stays local-only
  const online = /^https?:$/.test(location.protocol) && !!window.supabase;
  if (!btn || !dlg || !online) { if (btn) btn.hidden = true; window.RA_CLOUD = { user: () => null, client: null, onChange: () => () => {} }; return; }

  // ---------- the link coming back ----------
  // The emailed link returns here with the session (or an error) after the #. The app's own router reads the # too
  // and clears what it does not know, so take it now, before app.js runs, and leave a clean address behind.
  let arrived = null;
  if (/^#(.*&)?(access_token|error_description|error_code)=/.test(location.hash)) {
    arrived = new URLSearchParams(location.hash.slice(1));
    history.replaceState(null, "", location.pathname + location.search);
  }

  const client = window.supabase.createClient(URL_, KEY, { auth: { detectSessionInUrl: false, persistSession: true, autoRefreshToken: true } });
  let user = null, view = "form", sentTo = "", message = "";
  const listeners = new Set();
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  function paintButton() {
    const t = T();
    btn.textContent = user ? t.acctButtonIn : t.acctSignIn;
    btn.classList.toggle("is-in", !!user);
    btn.setAttribute("aria-label", user ? t.acctSignedIn(user.email) : t.acctSignIn);
    btn.title = user ? user.email : "";
  }
  function paintDialog() {
    const t = T();
    const note = message ? `<p class="acct-msg" role="alert">${esc(message)}</p>` : "";
    if (user) {
      dlg.innerHTML = `<form method="dialog"><h2>${t.acctTitle}</h2><p class="acct-line">${esc(t.acctSignedIn(user.email))}</p>${note}
        <div class="dialog-actions"><button type="button" class="ghost" data-acct="signout">${t.acctSignOut}</button><button value="close" class="solid">${t.acctClose}</button></div></form>`;
    } else if (view === "sent") {
      dlg.innerHTML = `<form method="dialog"><h2>${t.acctSentTitle}</h2><p class="acct-line">${esc(t.acctSent(sentTo))}</p>
        <div class="dialog-actions"><button type="button" class="ghost" data-acct="again">${t.acctAgain}</button><button value="close" class="solid">${t.acctClose}</button></div></form>`;
    } else {
      dlg.innerHTML = `<form id="account-form"><h2>${t.acctSignIn}</h2><p class="acct-line">${t.acctHint}</p>
        <label><span>${t.acctEmail}</span> <input type="email" name="email" required autocomplete="email" value="${esc(sentTo)}"></label>${note}
        <div class="dialog-actions"><button type="button" class="ghost" data-acct="close">${t.cancel}</button><button class="solid" id="account-send">${t.acctSend}</button></div></form>`;
    }
  }
  function paint() { paintButton(); if (dlg.open) paintDialog(); }
  function setUser(u) {
    const was = user && user.id;
    user = u || null;
    paint();
    if ((user && user.id) !== was) for (const fn of listeners) { try { fn(user); } catch (e) { /* listener error */ } }
  }

  btn.addEventListener("click", () => { view = "form"; message = ""; paintDialog(); dlg.showModal(); });
  dlg.addEventListener("click", async (e) => {
    const act = e.target.dataset && e.target.dataset.acct;
    if (act === "close") dlg.close();
    if (act === "again") { view = "form"; message = ""; paintDialog(); }
    if (act === "signout") {
      e.target.disabled = true;
      await client.auth.signOut({ scope: "local" }); // this browser only; what is saved here stays here
      dlg.close();
    }
  });
  dlg.addEventListener("submit", async (e) => {
    if (e.target.id !== "account-form") return;
    e.preventDefault();
    const t = T(), send = document.getElementById("account-send");
    const email = e.target.email.value.trim();
    if (!email) return;
    send.disabled = true;
    send.textContent = t.acctSending;
    sentTo = email;
    let error = null;
    try {
      // the link returns to this page (without any #/… view: the reader lands on the map they were on)
      ({ error } = await client.auth.signInWithOtp({ email, options: { emailRedirectTo: location.origin + location.pathname } }));
    } catch (err) { error = err; }
    if (error) {
      const limited = error.status === 429 || /rate limit|security purposes/i.test(error.message || "");
      message = limited ? t.acctErrRate : t.acctErrGeneric;
      view = "form";
    } else {
      message = "";
      view = "sent";
    }
    paintDialog();
  });

  client.auth.onAuthStateChange((event, session) => {
    // keep the callback synchronous and light, as supabase-js asks; the session is all it needs
    setUser(session ? session.user : null);
  });
  if (arrived && arrived.get("access_token") && arrived.get("refresh_token")) {
    client.auth.setSession({ access_token: arrived.get("access_token"), refresh_token: arrived.get("refresh_token") }).then(({ error }) => {
      if (error) { message = T().acctErrLink; view = "form"; paintDialog(); dlg.showModal(); }
    });
  } else if (arrived) {
    // an expired or already-used link: say so and offer a new one
    window.addEventListener("load", () => { message = T().acctErrLink; view = "form"; paintDialog(); dlg.showModal(); });
  }

  RS.onChange((what) => { if (what === "prefs:lang") paint(); });
  paintButton();
  window.RA_CLOUD = { user: () => user, client, onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); } };
})();
