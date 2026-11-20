/* The Reader's Atlas — account (cloud step 1, 11-19): sign in with a code sent by email, no password.
   The backend is Supabase for now (js/vendor/supabase.js). The key below is the project's publishable key: it is meant
   to be public, and the database's row-level security decides what it can reach. No secret key belongs in this repo.

   Looking is free. Keeping something (a flag, a trip, a shelf mark, a note, a diary entry) needs an account: app.js
   asks RA_CLOUD.require(what, then) at that moment, the dialog opens, and once the reader is in, `then` runs, so the
   thing they pressed happens without pressing it again. Signed out, nothing in the page chrome asks for an account;
   the My travels and My books tabs carry a sign-in card (promptHTML). Signed in, the reader's portrait
   (js/portrait.js: a small animal they pick; until they do, their account id picks one) sits beside the language toggle and opens the account dialog.

   Opened as a local file (file://) there is no account: gated is false and everything stays in this browser.
   Exposed as window.RA_CLOUD = { gated, user(), client, onChange(fn), require(what, then), promptHTML(text) }. */
(function () {
  "use strict";
  const URL_ = "https://silmbyjeyotyngdnwcdf.supabase.co";
  const KEY = "sb_publishable_Ft7WS4ta2Vc4jXqqhyFueA_W84FlSwO";
  const dlg = document.getElementById("account-dialog");
  const btn = document.getElementById("account-btn");
  const RS = window.RA_STORE;
  const T = () => window.RA_I18N[RS.prefs.get("lang", "en") === "zh" ? "zh" : "en"];
  const online = /^https?:$/.test(location.protocol) && !!window.supabase && !!dlg;
  if (!online) { window.RA_CLOUD = { gated: false, user: () => null, client: null, onChange: () => () => {}, require: (w, then) => then && then(), promptHTML: () => "" }; return; }

  // ---------- a sign-in link coming back ----------
  // The email carries a code; if it also carries a link (the default template), the link returns here with the
  // session, or an error, after the #. The app's router reads the # too and clears what it does not know, so take it
  // now, before app.js runs, and leave a clean address behind.
  let arrived = null;
  if (/^#(.*&)?(access_token|error_description|error_code)=/.test(location.hash)) {
    arrived = new URLSearchParams(location.hash.slice(1));
    history.replaceState(null, "", location.pathname + location.search);
  }

  const client = window.supabase.createClient(URL_, KEY, { auth: { detectSessionInUrl: false, persistSession: true, autoRefreshToken: true } });
  let user = null;
  let view = "email", email = "", message = "", what = "", pending = null;
  const listeners = new Set();
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // the portrait: the animal the reader picked, else one chosen by their account id
  const P = window.RA_PORTRAIT;
  const picks = () => RS.prefs.get("portrait", {}) || {};
  const mine = () => { const k = user && picks()[user.id]; return P.keys.includes(k) ? k : P.pick(user ? user.id : ""); };
  const zh = () => RS.prefs.get("lang", "en") === "zh";
  function paintButton() {
    if (!btn) return;
    btn.hidden = !user;
    if (!user) { btn.innerHTML = ""; return; }
    btn.innerHTML = P(mine(), 28);
    btn.setAttribute("aria-label", T().acctTitle);
    btn.title = T().acctTitle;
  }
  function paint() {
    const t = T();
    const note = message ? `<p class="acct-msg" role="alert">${esc(message)}</p>` : "";
    if (view === "account" && user) {
      dlg.innerHTML = `<form method="dialog"><h2>${t.acctTitle}</h2>
        <div class="acct-portrait">${P(mine(), 104)}</div>
        <p class="acct-line acct-email">${esc(user.email)}</p>
        <p class="acct-label">${t.acctChoose}</p>
        <div class="acct-choices" role="radiogroup" aria-label="${t.acctChoose}">${P.keys.map((k) => `<button type="button" role="radio" aria-checked="${k === mine()}" aria-label="${P.label(k, zh())}" title="${P.label(k, zh())}" data-pick="${k}">${P(k, 38)}</button>`).join("")}</div>
        <div class="dialog-actions"><button type="button" class="ghost" data-acct="out">${t.acctSignOut}</button><button value="close" class="dark">${t.acctClose}</button></div></form>`;
      return;
    }
    if (view === "code") {
      dlg.innerHTML = `<form id="account-code"><h2>${t.acctCodeTitle}</h2><p class="acct-line">${esc(t.acctSent(email))}</p>
        <label><span>${t.acctCode}</span> <input type="text" name="code" required inputmode="numeric" autocomplete="one-time-code" pattern="[0-9 ]{6,12}" maxlength="12" class="acct-code"></label>${note}
        <div class="dialog-actions"><button type="button" class="ghost" data-acct="back">${t.acctAgain}</button><button class="solid" id="account-go">${t.acctVerify}</button></div></form>`;
    } else {
      dlg.innerHTML = `<form id="account-email"><h2>${t.acctSignIn}</h2><p class="acct-line">${what ? esc(t.acctFor(what)) + " " : ""}${t.acctHint}</p>
        <label><span>${t.acctEmail}</span> <input type="email" name="email" required autocomplete="email" value="${esc(email)}"></label>${note}
        <div class="dialog-actions"><button type="button" class="ghost" data-acct="close">${t.cancel}</button><button class="solid" id="account-go">${t.acctSend}</button></div></form>`;
    }
    const first = dlg.querySelector("input");
    if (first && dlg.open) first.focus();
  }
  function open(forWhat, then) {
    what = forWhat || "";
    pending = then || null;
    view = "email";
    message = "";
    paint();
    if (!dlg.open) dlg.showModal();
  }
  function setUser(u) {
    const was = user && user.id;
    user = u || null;
    paintButton();
    if ((user && user.id) === was) return;
    for (const fn of listeners) { try { fn(user); } catch (e) { /* listener error */ } }
    if (user) {
      if (dlg.open) dlg.close("in");
      // the page has just been redrawn for the signed-in reader: now do what they had asked for
      const then = pending;
      pending = null;
      if (then) setTimeout(then, 0);
    }
  }
  const failure = (error, t) => (error.status === 429 || /rate limit|security purposes/i.test(error.message || "") ? t.acctErrRate : null);

  dlg.addEventListener("close", () => { if (dlg.returnValue !== "in") pending = null; });
  dlg.addEventListener("click", async (e) => {
    const act = e.target.dataset && e.target.dataset.acct;
    if (act === "close") dlg.close();
    if (act === "back") { view = "email"; message = ""; paint(); }
    const pickBtn = e.target.closest && e.target.closest("[data-pick]");
    if (pickBtn && user) { const n = picks(); n[user.id] = pickBtn.dataset.pick; RS.prefs.set("portrait", n); paint(); paintButton(); const again = dlg.querySelector(`[data-pick="${pickBtn.dataset.pick}"]`); if (again) again.focus(); }
    if (act === "out") { e.target.disabled = true; await client.auth.signOut({ scope: "local" }); dlg.close(); } // this browser only
  });
  if (btn) btn.addEventListener("click", () => { view = "account"; message = ""; pending = null; paint(); dlg.showModal(); });
  dlg.addEventListener("submit", async (e) => {
    e.preventDefault();
    const t = T(), go = document.getElementById("account-go");
    go.disabled = true;
    let error = null;
    if (e.target.id !== "account-email" && e.target.id !== "account-code") return;
    if (e.target.id === "account-email") {
      email = e.target.email.value.trim();
      go.textContent = t.acctSending;
      try { ({ error } = await client.auth.signInWithOtp({ email, options: { emailRedirectTo: location.origin + location.pathname } })); } catch (err) { error = err; }
      message = error ? failure(error, t) || t.acctErrGeneric : "";
      if (!error) view = "code";
      paint();
    } else {
      const token = e.target.code.value.replace(/\s+/g, "");
      go.textContent = t.acctVerifying;
      try { ({ error } = await client.auth.verifyOtp({ email, token, type: "email" })); } catch (err) { error = err; }
      if (error) { message = failure(error, t) || t.acctErrCode; paint(); }
      // success: onAuthStateChange closes the dialog and runs what was pending
    }
  });

  client.auth.onAuthStateChange((event, session) => { setUser(session ? session.user : null); });
  if (arrived && arrived.get("access_token") && arrived.get("refresh_token")) {
    client.auth.setSession({ access_token: arrived.get("access_token"), refresh_token: arrived.get("refresh_token") }).then(({ error }) => {
      if (error) { open(""); message = T().acctErrLink; paint(); }
    });
  } else if (arrived) {
    window.addEventListener("load", () => { open(""); message = T().acctErrLink; paint(); });
  }

  // the sign-in card and the footer live inside the reading panel, which app.js redraws: listen from the document
  document.addEventListener("click", (e) => {
    const b = e.target.closest && e.target.closest("[data-acct-open]");
    if (b) open("");
  });
  RS.onChange((k) => { if (k === "prefs:lang") { paintButton(); if (dlg.open) paint(); } });

  window.RA_CLOUD = {
    gated: true,
    client,
    user: () => user,
    onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); },
    require(forWhat, then) { if (user) { if (then) then(); return; } open(forWhat, then); },
    promptHTML: (text) => `<div class="card acct-card"><p>${esc(text)}</p><div class="actions"><button class="btn" data-acct-open>${T().acctSignIn}</button></div></div>`,
  };
})();
