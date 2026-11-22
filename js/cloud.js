/* The Reader's Atlas — account (cloud steps 1 and 2, 11-19/20): sign in with a code sent by email, no password,
   and the reader's records kept with their account.
   The backend is Supabase for now (js/vendor/supabase.js). The key below is the project's publishable key: it is meant
   to be public, and the database's row-level security decides what it can reach. No secret key belongs in this repo.

   Looking is free. Keeping something (a flag, a trip, a shelf mark, a note, a diary entry) needs an account: app.js
   asks RA_CLOUD.require(what, then) at that moment, the dialog opens, and once the reader is in and their records
   have arrived, `then` runs, so the thing they pressed happens without pressing it again. Signed out, nothing in the page chrome asks for an account;
   the My travels and My books tabs carry a sign-in card (promptHTML). Signed in, the reader's portrait
   (js/portrait.js: a small animal they pick; until they do, their account id picks one) sits beside the language toggle and opens the account dialog.

   Records (cloud step 2). Each reader has one row in the table user_data (docs/cloud-sync.sql): their wishlist,
   visited places, trips, shelf, favourites, notes, diary text, chosen portrait and the view they had open last, as one JSON document that only
   they can read or write (row-level security). store.js keeps a working copy per reader in this browser. Signing in
   reads the row; a change here is written back a moment later; coming back to the tab reads it again, so two
   browsers on one account follow each other. Diary photos are not uploaded: they stay in the browser that added them.

   Opened as a local file (file://) there is no account: gated is false and everything stays in this browser.
   Where the reader was. When a reader signs in and their records have arrived, onArrive(fn) listeners get
   { fresh, then }: fresh is true when they have just signed in through the dialog or the emailed link (false for a
   session carried over a reload); then is the action of the control they had pressed, if any. app.js decides from
   that whether to stay on the page or return to the view the account had open last.
   Exposed as window.RA_CLOUD = { gated, user(), client, onChange(fn), onArrive(fn), require(what, then), promptHTML(text), sync(), rank() }. */
(function () {
  "use strict";
  const URL_ = "https://silmbyjeyotyngdnwcdf.supabase.co";
  const KEY = "sb_publishable_Ft7WS4ta2Vc4jXqqhyFueA_W84FlSwO";
  const dlg = document.getElementById("account-dialog");
  const btn = document.getElementById("account-btn");
  const RS = window.RA_STORE;
  const T = () => window.RA_I18N[RS.prefs.get("lang", "en") === "zh" ? "zh" : "en"];
  const online = /^https?:$/.test(location.protocol) && !!window.supabase && !!dlg;
  if (!online) { window.RA_CLOUD = { gated: false, user: () => null, client: null, onChange: () => () => {}, onArrive: () => () => {}, require: (w, then) => then && then(), promptHTML: () => "", sync: () => "off", rank: async () => null }; return; }
  RS.account(null); // on the site, records belong to an account: nobody is signed in yet

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
  let justSignedIn = false; // set while a sign-in through the dialog or the emailed link is under way
  const listeners = new Set(), arrivals = new Set();
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
        <p class="acct-sync" role="status">${syncLine()}</p>
        <p class="acct-label">${t.acctChoose}</p>
        <div class="acct-choices" role="radiogroup" aria-label="${t.acctChoose}">${P.keys.map((k) => `<button type="button" role="radio" aria-checked="${k === mine()}" aria-label="${P.label(k, zh())}" title="${P.label(k, zh())}" data-pick="${k}">${P(k, 38)}</button>`).join("")}</div>
        <div class="dialog-actions"><button type="button" class="ghost" data-acct="out">${t.acctSignOut}</button><button type="button" class="dark" data-acct="close">${t.acctClose}</button></div></form>`;
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
    if ((user && user.id) === was) { paintButton(); return; }
    // another reader, or nobody: their records, not the last reader's
    clearTimeout(timer);
    rev = 0; moved = 0; status = user ? "busy" : "off";
    RS.account(user ? user.id : null);
    if (user && RS.takeUnclaimed()) mark();
    paintButton();
    tell();
    if (user) {
      if (dlg.open) dlg.close("in");
      // once their records are here and the page shows them: do what they had asked for, in the place app.js picks
      const then = pending, uid = user.id, fresh = justSignedIn;
      pending = null; justSignedIn = false;
      pull().then(() => setTimeout(() => {
        if (!user || user.id !== uid) return;
        if (!arrivals.size) { if (then) then(); return; }
        for (const fn of arrivals) { try { fn({ fresh, then }); } catch (e) { /* listener error */ } }
      }, 0));
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
    if (act === "out") { e.target.disabled = true; clearTimeout(timer); if (note().dirty || moved) await push(); await client.auth.signOut({ scope: "local" }); dlg.close(); } // this browser only; unsaved changes go first
  });
  if (btn) btn.addEventListener("click", () => { view = "account"; message = ""; pending = null; paint(); dlg.showModal(); });
  dlg.addEventListener("submit", async (e) => {
    // only the two sign-in forms are handled here; the account card has nothing to submit
    if (e.target.id !== "account-email" && e.target.id !== "account-code") return;
    e.preventDefault();
    const t = T(), go = document.getElementById("account-go");
    go.disabled = true;
    let error = null;
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
      justSignedIn = true;
      try { ({ error } = await client.auth.verifyOtp({ email, token, type: "email" })); } catch (err) { error = err; }
      if (error) justSignedIn = false;
      if (error) { message = failure(error, t) || t.acctErrCode; paint(); }
      // success: onAuthStateChange closes the dialog and runs what was pending
    }
  });

  // ---------- the reader's records, kept with the account ----------
  const TABLE = "user_data";
  let status = "off"; // off | busy | saved | failed
  let rev = 0, timer = null, applying = false, lastPull = 0;
  let moved = 0; // the reader has moved to another view since the last save (kept apart from `dirty`: it is not a change to their records)
  const tell = () => { for (const fn of listeners) { try { fn(user); } catch (e) { /* listener error */ } } };
  const note = () => RS.mine.get("sync", {}) || {}; // { at: the row's time when this browser last matched it, dirty: changes not yet written }
  const mark = () => { rev++; RS.mine.set("sync", { ...note(), dirty: true }); };
  const setStatus = (v) => { status = v; const line = dlg.querySelector(".acct-sync"); if (line) line.textContent = syncLine(); };
  function syncLine() { const t = T(); return status === "saved" ? t.acctSaved : status === "failed" ? t.acctSaveFailed : status === "busy" ? t.acctSaving : ""; }
  const usable = (d) => !!d && d.app === "readers-atlas" && Array.isArray(d.user_places);
  function doc() {
    const d = RS.exportData();
    delete d.user_prefs; delete d.exported_at; // language and sound belong to the browser
    d.portrait = picks()[user.id] || null;
    return d;
  }
  // put what the account holds into this browser; `merge` keeps what is only here as well
  function take(d, merge) {
    applying = true;
    const here = moved ? RS.where.get() : null; // where this browser is now is newer than where the account says
    try {
      if (merge) RS.importData(d); else RS.replaceData(d);
      if (here !== null) RS.where.set(here);
      if (P.keys.includes(d.portrait) && !(merge && picks()[user.id])) { const n = picks(); n[user.id] = d.portrait; RS.prefs.set("portrait", n); }
    } finally { applying = false; }
  }
  async function push() {
    if (!user) return false;
    const uid = user.id, mine = rev, was = moved, at = new Date().toISOString();
    setStatus("busy");
    let error = null;
    try { ({ error } = await client.from(TABLE).upsert({ user_id: uid, data: doc(), updated_at: at })); } catch (err) { error = err; }
    if (!user || user.id !== uid) return false;
    if (error) { setStatus("failed"); clearTimeout(timer); timer = setTimeout(push, 20000); return false; }
    RS.mine.set("sync", { at, dirty: rev !== mine });
    if (moved === was) moved = 0;
    setStatus(rev !== mine ? "busy" : "saved");
    return true;
  }
  async function pull() {
    if (!user) return;
    const uid = user.id;
    lastPull = Date.now();
    let row = null, error = null;
    try { ({ data: row, error } = await client.from(TABLE).select("data, updated_at").eq("user_id", uid).maybeSingle()); } catch (err) { error = err; }
    if (!user || user.id !== uid) return;
    if (error) { setStatus("failed"); return; }
    const n = note(), unsaved = n.dirty || (!n.at && RS.hasRecords());
    if (!row || !usable(row.data)) { await push(); return; } // nothing kept with the account yet
    if (unsaved) { take(row.data, true); paintButton(); tell(); await push(); return; } // both sides have something: keep both
    if (row.updated_at !== n.at) { take(row.data, false); RS.mine.set("sync", { at: row.updated_at, dirty: false }); paintButton(); if (dlg.open && view === "account") paint(); tell(); }
    if (moved) { await push(); return; }
    setStatus("saved");
  }
  RS.onChange((k) => {
    if (!user || applying || k === "account" || (k.startsWith("prefs:") && k !== "prefs:portrait")) return;
    // moving to another view is saved too, but quietly and less often, and it never counts as an unsaved record
    if (k === "last") { moved++; clearTimeout(timer); timer = setTimeout(push, note().dirty ? 1200 : 4000); return; }
    mark();
    setStatus("busy");
    clearTimeout(timer);
    timer = setTimeout(push, 1200);
  });
  // Where this reader stands among readers (docs/cloud-sync.sql, reader_rank): the database counts from the row
  // saved with the account, so unsaved changes are written first. Resolves to the numbers, or null when there is
  // no answer (signed out, offline, or the function has not been added to the database yet).
  async function rank() {
    if (!user) return null;
    const uid = user.id;
    if (note().dirty) { clearTimeout(timer); if (!(await push())) return null; }
    let data = null, error = null;
    try { ({ data, error } = await client.rpc("reader_rank")); } catch (err) { error = err; }
    if (error || !data || !user || user.id !== uid) return null;
    return data;
  }
  // back on this tab: another browser may have changed the records meanwhile
  const refresh = () => { if (user && !document.hidden && Date.now() - lastPull > 4000) pull(); };
  document.addEventListener("visibilitychange", refresh);
  window.addEventListener("focus", refresh);

  client.auth.onAuthStateChange((event, session) => { setTimeout(() => setUser(session ? session.user : null), 0); });
  if (arrived && arrived.get("access_token") && arrived.get("refresh_token")) {
    justSignedIn = true;
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
    sync: () => status,
    rank,
    onArrive(fn) { arrivals.add(fn); return () => arrivals.delete(fn); },
    promptHTML: (text) => `<div class="card acct-card"><p>${esc(text)}</p><div class="actions"><button class="btn" data-acct-open>${T().acctSignIn}</button></div></div>`,
  };
})();
