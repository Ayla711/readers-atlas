/* The Reader's Atlas — personal data store (R-6, 11-09).
   Everything a reader owns goes through here: places (wishlist, visited), trips, books (shelf, favourites, notes) and
   preferences (language, sound, legend state). Today the backend is localStorage under "ra.*"; when the cloud backend
   arrives, only this file and journal-store.js change. The export/import format (R-7) is the shape that will be synced.
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

  // ---------- state ----------
  const state = {
    wishlist: new Set(kv.get("wishlist", [])),
    visited: new Set(kv.get("visited", [])),
    itinerary: kv.get("itinerary", []), // [{ place_id, date, note }]
    shelf: kv.get("shelf", {}), // book_id -> "want" | "read"
    faves: new Set(kv.get("faves", [])), // favourite books, independent of the shelf
    notes: kv.get("notes", {}), // book_id -> text
  };
  const listeners = new Set();
  const emit = (what) => { for (const fn of listeners) { try { fn(what); } catch (e) { /* listener error */ } } };
  const saveKey = (k) => {
    const v = state[k];
    kv.set(k, v instanceof Set ? [...v] : v);
    emit(k);
  };
  const saveAll = () => { for (const k of Object.keys(state)) saveKey(k); };

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
    state, // the live objects: app.js reads these directly and calls save() after a change it made itself
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
      const journal = window.RA_JOURNAL ? window.RA_JOURNAL.list() : [];
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
    // Merge: the file adds to what is here; nothing local is removed. Returns counts for the message to the reader.
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
