/* The Reader's Atlas — personal data store (R-6, 11-09).
   Everything a reader owns goes through here: places (wishlist, visited), trips, books (shelf, favourites, notes) and
   preferences (language, sound, legend state). Here the backend is localStorage under "ra.*". Preferences belong to
   this browser. The records belong to a reader: each signed-in reader has their own set of keys ("ra.u.<id>.*"), so
   two people who use the same browser never see each other's; js/cloud.js picks the reader (account) and keeps that
   set in step with their row in the database (snapshot / replaceData / importData are the shape that is synced).
   Exposed as window.RA_STORE. */
(function () {
  "use strict";
  const PREFIX = "ra.";
  // ---------- key/value backend ----------
  const kv = {
    get(key, fallback) {
      try {
        const v = localStorage.getItem(PREFIX + key);
        return v === null ? fallback : JSON.parse(v);
      } catch (e) { return fallback; }
    },
    set(key, val) {
      try { localStorage.setItem(PREFIX + key, JSON.stringify(val)); return true; } catch (e) { return false; }
    },
    remove(key) {
      try { localStorage.removeItem(PREFIX + key); } catch (e) { /* ignore */ }
    },
  };

  // ---------- whose records ----------
  // "" : this browser, no account (the app opened as a file; also where records were kept before accounts existed)
  // "u.<id>." : one signed-in reader
  // null : the site with nobody signed in: nothing is shown and nothing is kept
  let scope = "";
  const mine = {
    get: (key, fallback) => (scope === null ? fallback : kv.get(scope + key, fallback)),
    set: (key, val) => (scope === null ? true : kv.set(scope + key, val)),
    remove(key) { if (scope !== null) kv.remove(scope + key); },
  };
  const RECORDS = ["wishlist", "visited", "itinerary", "shelf", "faves", "notes"];

  // ---------- state ----------
  const load = () => ({
    wishlist: new Set(mine.get("wishlist", [])),
    visited: new Set(mine.get("visited", [])),
    itinerary: mine.get("itinerary", []), // [{ place_id, date, note }]
    shelf: mine.get("shelf", {}), // book_id -> "want" | "read"
    faves: new Set(mine.get("faves", [])), // favourite books, independent of the shelf
    notes: mine.get("notes", {}), // book_id -> text
  });
  const state = load();
  const listeners = new Set();
  const emit = (what) => { for (const fn of listeners) { try { fn(what); } catch (e) { /* listener error */ } } };
  const saveKey = (k) => {
    const v = state[k];
    mine.set(k, v instanceof Set ? [...v] : v);
    emit(k);
  };
  const saveAll = () => { for (const k of RECORDS) saveKey(k); };

  const setOps = (k) => ({
    has: (id) => state[k].has(id),
    add(id) { state[k].add(id); saveKey(k); },
    remove(id) { state[k].delete(id); saveKey(k); },
    toggle(id) { state[k].has(id) ? state[k].delete(id) : state[k].add(id); saveKey(k); return state[k].has(id); },
    list: () => [...state[k]],
    get size() { return state[k].size; },
  });

  const API = {
    kv,
    mine, // the reader's own keys (journal-store.js keeps its entries here)
    state, // the live object: app.js reads state.wishlist etc. each time and calls save() after a change it made itself
    changed: emit, // journal-store.js reports its own saves through here
    /** Switch to another reader's records (an account id), to nobody's (null), or back to this browser's own (""). */
    account(id) {
      scope = id === null ? null : id ? "u." + id + "." : "";
      Object.assign(state, load());
      if (window.RA_JOURNAL) window.RA_JOURNAL.reload();
      emit("account");
    },
    /** True when the current reader has any record at all. */
    hasRecords: () => state.wishlist.size + state.visited.size + state.itinerary.length + state.faves.size + Object.keys(state.shelf).length + Object.keys(state.notes).length + (window.RA_JOURNAL ? window.RA_JOURNAL.raw().length : 0) > 0,
    /** Records this browser kept before accounts existed sit under the bare keys. The reader who signs in here first
        takes them: they are merged into that reader's records and moved aside ("ra.kept.*", a copy nobody reads), so
        the next person to sign in on this browser starts with their own. Returns true when something was taken. */
    takeUnclaimed() {
      if (!scope) return false;
      const keys = RECORDS.concat("journal"), old = {};
      let any = false;
      for (const k of keys) {
        const v = kv.get(k, null);
        if (v === null || typeof v !== "object") continue;
        old[k] = v;
        if (Array.isArray(v) ? v.length : Object.keys(v).length) any = true;
      }
      if (any) {
        const shelf = old.shelf || {}, notes = old.notes || {}, faves = new Set(old.faves || []);
        API.importData({
          app: "readers-atlas",
          user_places: [...(old.wishlist || []).map((id) => ({ place_id: id, kind: "wishlist" })), ...(old.visited || []).map((id) => ({ place_id: id, kind: "visited" }))],
          user_trips: Array.isArray(old.itinerary) ? old.itinerary : [],
          user_books: [...new Set([...Object.keys(shelf), ...faves, ...Object.keys(notes)])].map((bid) => ({ book_id: bid, shelf: shelf[bid] || null, favourite: faves.has(bid), note: notes[bid] || "" })),
          journal_entries: Array.isArray(old.journal) ? old.journal : [],
        });
      }
      for (const k of Object.keys(old)) { if (any) kv.set("kept." + k, old[k]); kv.remove(k); }
      return any;
    },
    save: saveAll,
    saveKey,
    onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); },
    wishlist: setOps("wishlist"),
    visited: setOps("visited"),
    faves: setOps("faves"),
    itinerary: {
      list: () => state.itinerary.slice(),
      add(place_id, date, note) { state.itinerary.push({ place_id, date, note: note || "" }); saveKey("itinerary"); },
      remove(i) { state.itinerary.splice(i, 1); saveKey("itinerary"); },
      forPlace: (pid) => state.itinerary.map((x, i) => ({ ...x, i })).filter((x) => x.place_id === pid),
    },
    shelf: {
      get: (bid) => state.shelf[bid] || null,
      set(bid, v) { if (v) state.shelf[bid] = v; else delete state.shelf[bid]; saveKey("shelf"); },
    },
    notes: {
      get: (bid) => state.notes[bid] || "",
      set(bid, text) { if (text) state.notes[bid] = text; else delete state.notes[bid]; saveKey("notes"); },
    },
    prefs: {
      get: (k, fallback) => kv.get(k, fallback),
      set(k, v) { kv.set(k, v); emit("prefs:" + k); },
    },

    // ---------- export / import (R-7) ----------
    // The file is the future sync payload: one object per table of docs/plan-week2-5.md section 4. Journal entries
    // travel as text; their photos stay in this browser (IndexedDB) and are noted by id only.
    exportData() {
      const journal = window.RA_JOURNAL ? window.RA_JOURNAL.raw() : [];
      return {
        app: "readers-atlas", version: 1, exported_at: new Date().toISOString(),
        user_places: [
          ...[...state.wishlist].map((id) => ({ place_id: id, kind: "wishlist" })),
          ...[...state.visited].map((id) => ({ place_id: id, kind: "visited" })),
        ],
        user_trips: state.itinerary.map((x) => ({ place_id: x.place_id, date: x.date, note: x.note || "" })),
        user_books: [...new Set([...Object.keys(state.shelf), ...state.faves, ...Object.keys(state.notes)])].map((bid) => ({
          book_id: bid, shelf: state.shelf[bid] || null, favourite: state.faves.has(bid), note: state.notes[bid] || "",
        })),
        user_prefs: { lang: kv.get("lang", "en"), sound: kv.get("sound", true) },
        journal_entries: journal.map((e) => ({ ...e, photos: (e.photos || []).map((p) => ({ id: p.id, caption: p.caption || "", width: p.width, height: p.height })) })),
      };
    },
    /** Make the current reader's records exactly what `data` says (the copy kept with their account): what is not in
        it is removed here. Journal photos stay where they are; an entry names its photos by id. */
    replaceData(data) {
      if (!data || data.app !== "readers-atlas" || !Array.isArray(data.user_places)) throw new Error("not a Reader's Atlas record");
      const str = (v) => typeof v === "string";
      state.wishlist = new Set(data.user_places.filter((p) => p.kind === "wishlist" && str(p.place_id)).map((p) => p.place_id));
      state.visited = new Set(data.user_places.filter((p) => p.kind === "visited" && str(p.place_id)).map((p) => p.place_id));
      state.itinerary = (data.user_trips || []).filter((t) => str(t.place_id) && str(t.date)).map((t) => ({ place_id: t.place_id, date: t.date, note: t.note || "" })).sort((a, b) => a.date.localeCompare(b.date));
      state.shelf = {}; state.notes = {}; state.faves = new Set();
      for (const b of data.user_books || []) {
        if (!str(b.book_id)) continue;
        if (b.shelf === "want" || b.shelf === "read") state.shelf[b.book_id] = b.shelf;
        if (b.favourite) state.faves.add(b.book_id);
        if (b.note) state.notes[b.book_id] = String(b.note);
      }
      saveAll();
      if (window.RA_JOURNAL) window.RA_JOURNAL.replaceEntries(Array.isArray(data.journal_entries) ? data.journal_entries : []);
    },
    // Merge: the data adds to what is here; nothing local is removed. Returns counts for the message to the reader.
    importData(data) {
      if (!data || data.app !== "readers-atlas" || !Array.isArray(data.user_places)) throw new Error("not a Reader's Atlas export");
      const n = { places: 0, trips: 0, books: 0, journal: 0 };
      for (const p of data.user_places) {
        const s = p.kind === "visited" ? state.visited : p.kind === "wishlist" ? state.wishlist : null;
        if (s && typeof p.place_id === "string" && !s.has(p.place_id)) { s.add(p.place_id); n.places++; }
      }
      const tripKey = (t) => `${t.place_id}|${t.date}|${t.note || ""}`;
      const have = new Set(state.itinerary.map(tripKey));
      for (const t of data.user_trips || []) {
        if (typeof t.place_id === "string" && typeof t.date === "string" && !have.has(tripKey(t))) { state.itinerary.push({ place_id: t.place_id, date: t.date, note: t.note || "" }); have.add(tripKey(t)); n.trips++; }
      }
      state.itinerary.sort((a, b) => a.date.localeCompare(b.date));
      for (const b of data.user_books || []) {
        if (typeof b.book_id !== "string") continue;
        let changed = false;
        if ((b.shelf === "want" || b.shelf === "read") && !state.shelf[b.book_id]) { state.shelf[b.book_id] = b.shelf; changed = true; }
        if (b.favourite && !state.faves.has(b.book_id)) { state.faves.add(b.book_id); changed = true; }
        if (b.note && !state.notes[b.book_id]) { state.notes[b.book_id] = String(b.note); changed = true; }
        if (changed) n.books++;
      }
      saveAll();
      if (window.RA_JOURNAL && Array.isArray(data.journal_entries)) n.journal = window.RA_JOURNAL.importEntries(data.journal_entries);
      return n;
    },
  };
  window.RA_STORE = API;
})();
