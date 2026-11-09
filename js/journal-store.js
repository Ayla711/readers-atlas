/* The Reader's Atlas — travel journal storage (front-end stand-in).
   Spec: docs/travel-journal-spec.md. Until the back end exists, entries live in this browser:
   the text in localStorage ("ra.journal"), the photos as JPEG blobs in IndexedDB ("ra-journal").
   The app only uses the functions below, so the back end can replace this file without touching the screens.
   Photos are re-encoded through a canvas before they are stored, which drops EXIF data (GPS included). */
(function () {
  "use strict";
  const KEY = "journal"; // "ra.journal" through the shared key/value backend in store.js
  const kv = window.RA_STORE ? window.RA_STORE.kv : {
    get(k, f) { try { const v = localStorage.getItem("ra." + k); return v === null ? f : JSON.parse(v); } catch (e) { return f; } },
    set(k, v) { try { localStorage.setItem("ra." + k, JSON.stringify(v)); return true; } catch (e) { return false; } },
  };
  const LONG_EDGE = 2048, THUMB_EDGE = 480;
  let entries = kv.get(KEY, []);
  if (!Array.isArray(entries)) entries = [];
  const persist = () => kv.set(KEY, entries);
  const newId = (p) => p + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

  // ---------- photo blobs (IndexedDB) ----------
  let dbp = null;
  function idb() {
    if (!dbp) dbp = new Promise((resolve, reject) => {
      if (!window.indexedDB) return reject(new Error("no indexedDB"));
      const r = indexedDB.open("ra-journal", 1);
      r.onupgradeneeded = () => r.result.createObjectStore("photos");
      r.onsuccess = () => resolve(r.result);
      r.onerror = () => reject(r.error);
    });
    return dbp;
  }
  async function tx(mode, fn) {
    const db = await idb();
    return new Promise((resolve, reject) => {
      const t = db.transaction("photos", mode);
      const out = fn(t.objectStore("photos"));
      t.oncomplete = () => resolve(out && "result" in out ? out.result : undefined);
      t.onerror = () => reject(t.error);
      t.onabort = () => reject(t.error);
    });
  }
  const urlCache = new Map(); // "<photo id>:<full|thumb>" -> object URL
  async function photoURL(id, size) {
    const k = id + ":" + size;
    if (urlCache.has(k)) return urlCache.get(k);
    const blob = await tx("readonly", (s) => s.get(k));
    if (!blob) return null;
    const u = URL.createObjectURL(blob);
    urlCache.set(k, u);
    return u;
  }

  // ---------- photo preparation ----------
  async function decode(file) {
    if (window.createImageBitmap) {
      try { return await createImageBitmap(file, { imageOrientation: "from-image" }); } catch (e) { /* fall through */ }
    }
    const url = URL.createObjectURL(file);
    try {
      const img = new Image();
      img.src = url;
      await img.decode();
      return img;
    } finally { URL.revokeObjectURL(url); }
  }
  function encode(src, edge) {
    const w0 = src.width, h0 = src.height, k = Math.min(1, edge / Math.max(w0, h0));
    const c = document.createElement("canvas");
    c.width = Math.round(w0 * k); c.height = Math.round(h0 * k);
    c.getContext("2d").drawImage(src, 0, 0, c.width, c.height);
    return new Promise((resolve, reject) => c.toBlob((b) => (b ? resolve({ blob: b, width: c.width, height: c.height }) : reject(new Error("encode"))), "image/jpeg", 0.85));
  }
  /** Read a picked file into a draft photo: resized, re-encoded (no EXIF), with a preview URL. Rejects for unreadable formats. */
  async function preparePhoto(file) {
    const src = await decode(file);
    const full = await encode(src, LONG_EDGE), thumb = await encode(src, THUMB_EDGE);
    if (src.close) src.close();
    return { id: newId("p_"), width: full.width, height: full.height, caption: "", full: full.blob, thumb: thumb.blob, preview: URL.createObjectURL(thumb.blob), isNew: true };
  }

  // ---------- entries ----------
  const byDate = (a, b) => (b.visit_date || "").localeCompare(a.visit_date || "") || (b.created_at || "").localeCompare(a.created_at || "");
  const clone = (e) => JSON.parse(JSON.stringify(e));
  const API = {
    all: () => entries.slice().sort(byDate).map(clone),
    list: () => entries.slice().sort(byDate).map(clone),
    /** Import entries from an export file (R-7): adds entries whose id is new; photos are kept only when this browser
        already holds them, otherwise the entry comes in without them. Returns the number added. */
    importEntries(list) {
      let n = 0;
      const have = new Set(entries.map((e) => e.id));
      for (const e of list) {
        if (!e || typeof e.id !== "string" || typeof e.place_id !== "string" || have.has(e.id)) continue;
        entries.push({ id: e.id, place_id: e.place_id, visit_date: e.visit_date || "", text: e.text || "", book_ids: Array.isArray(e.book_ids) ? e.book_ids : [],
          photos: [], created_at: e.created_at || new Date().toISOString(), updated_at: e.updated_at || new Date().toISOString() });
        have.add(e.id); n++;
      }
      if (n) persist();
      return n;
    },
    forPlace: (pid) => entries.filter((e) => e.place_id === pid).sort(byDate).map(clone),
    count: (pid) => entries.filter((e) => e.place_id === pid).length,
    get: (id) => { const e = entries.find((x) => x.id === id); return e ? clone(e) : null; },
    preparePhoto,
    photoURL,
    /** Save an entry. `photos` is the full ordered list: kept ones ({id, caption, width, height}) and new drafts from preparePhoto. */
    async save(entry, photos) {
      const now = new Date().toISOString();
      const old = entry.id ? entries.find((x) => x.id === entry.id) : null;
      for (const p of photos.filter((p) => p.isNew)) {
        await tx("readwrite", (s) => { s.put(p.full, p.id + ":full"); s.put(p.thumb, p.id + ":thumb"); });
      }
      const keep = new Set(photos.map((p) => p.id));
      const dropped = old ? old.photos.filter((p) => !keep.has(p.id)) : [];
      const rec = {
        id: old ? old.id : newId("j_"),
        place_id: entry.place_id,
        visit_date: entry.visit_date,
        text: entry.text || "",
        book_ids: entry.book_ids || [],
        photos: photos.map((p) => ({ id: p.id, caption: p.caption || "", width: p.width, height: p.height })),
        created_at: old ? old.created_at : now,
        updated_at: now,
      };
      if (old) entries[entries.indexOf(old)] = rec; else entries.push(rec);
      if (!persist()) throw new Error("storage_full");
      for (const p of dropped) await API._dropPhoto(p.id);
      return clone(rec);
    },
    async remove(id) {
      const e = entries.find((x) => x.id === id);
      if (!e) return;
      entries = entries.filter((x) => x !== e);
      persist();
      for (const p of e.photos) await API._dropPhoto(p.id);
    },
    async _dropPhoto(pid) {
      for (const size of ["full", "thumb"]) {
        const k = pid + ":" + size;
        if (urlCache.has(k)) { URL.revokeObjectURL(urlCache.get(k)); urlCache.delete(k); }
      }
      try { await tx("readwrite", (s) => { s.delete(pid + ":full"); s.delete(pid + ":thumb"); }); } catch (e) { /* storage gone */ }
    },
  };
  window.RA_JOURNAL = API;
})();
