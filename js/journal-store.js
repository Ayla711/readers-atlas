/* The Reader's Atlas — travel journal storage.
   Spec: docs/travel-journal-spec.md. The text of the entries is one of the reader's records (store.js keeps it under
   the reader's own keys, cloud.js keeps it with their account). The photos are JPEG blobs in IndexedDB
   ("ra-journal") and stay in the browser where they were added: an entry names its photos by id, and a browser that
   does not hold a photo leaves it out of what it shows without forgetting it.
   Photos are re-encoded through a canvas before they are stored, which drops EXIF data (GPS included). */
(function () {
  "use strict";
  const KEY = "journal"; // among the reader's own keys in store.js
  const RS = window.RA_STORE;
  const kv = RS ? RS.mine : {
    get(k, f) { try { const v = localStorage.getItem("ra." + k); return v === null ? f : JSON.parse(v); } catch (e) { return f; } },
    set(k, v) { try { localStorage.setItem("ra." + k, JSON.stringify(v)); return true; } catch (e) { return false; } },
  };
  const LONG_EDGE = 2048, THUMB_EDGE = 480;
  const read = () => { const v = kv.get(KEY, []); return Array.isArray(v) ? v : []; };
  let entries = read();
  const persist = () => { const ok = kv.set(KEY, entries); if (RS && RS.changed) RS.changed("journal"); return ok; };
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
  // the photos this browser holds; null until the list has been read (until then every photo is assumed to be here)
  let here = null;
  idb().then((db) => new Promise((resolve) => {
    const r = db.transaction("photos", "readonly").objectStore("photos").getAllKeys();
    r.onsuccess = () => { here = new Set(r.result.filter((k) => String(k).endsWith(":thumb")).map((k) => String(k).slice(0, -6))); resolve(); };
    r.onerror = () => resolve();
  })).catch(() => { /* no IndexedDB: nothing to list */ });
  const isHere = (p) => !here || here.has(p.id);
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
  // what the screens get: the entry with the photos this browser can show
  const view = (e) => { const c = clone(e); c.photos = (c.photos || []).filter(isHere); return c; };
  const clean = (e) => ({ id: e.id, place_id: e.place_id, visit_date: e.visit_date || "", text: e.text || "", book_ids: Array.isArray(e.book_ids) ? e.book_ids.filter((b) => typeof b === "string") : [],
    photos: (Array.isArray(e.photos) ? e.photos : []).filter((p) => p && typeof p.id === "string").map((p) => ({ id: p.id, caption: p.caption || "", width: p.width, height: p.height })),
    created_at: e.created_at || new Date().toISOString(), updated_at: e.updated_at || new Date().toISOString() });
  const valid = (e) => e && typeof e.id === "string" && typeof e.place_id === "string";
  const API = {
    all: () => entries.slice().sort(byDate).map(view),
    list: () => entries.slice().sort(byDate).map(view),
    /** Every entry as stored, with all its photo ids: what is kept with the account. */
    raw: () => entries.slice().sort(byDate).map(clone),
    /** Read the entries again: store.js calls this when the reader changes. */
    reload() { entries = read(); },
    /** Make the entries exactly this list (the copy kept with the account). */
    replaceEntries(list) { entries = list.filter(valid).map(clean); persist(); },
    /** Merge entries in: an entry whose id is new is added; one that is already here is replaced when the incoming
        copy was edited later. Returns the number added. */
    importEntries(list) {
      let n = 0, touched = false;
      const at = new Map(entries.map((e, i) => [e.id, i]));
      for (const e of list) {
        if (!valid(e)) continue;
        if (!at.has(e.id)) { entries.push(clean(e)); at.set(e.id, entries.length - 1); n++; touched = true; }
        else if ((e.updated_at || "") > (entries[at.get(e.id)].updated_at || "")) { entries[at.get(e.id)] = clean(e); touched = true; }
      }
      if (touched) persist();
      return n;
    },
    forPlace: (pid) => entries.filter((e) => e.place_id === pid).sort(byDate).map(view),
    count: (pid) => entries.filter((e) => e.place_id === pid).length,
    get: (id) => { const e = entries.find((x) => x.id === id); return e ? view(e) : null; },
    preparePhoto,
    photoURL,
    /** Save an entry. `photos` is the full ordered list: kept ones ({id, caption, width, height}) and new drafts from preparePhoto. */
    async save(entry, photos) {
      const now = new Date().toISOString();
      const old = entry.id ? entries.find((x) => x.id === entry.id) : null;
      for (const p of photos.filter((p) => p.isNew)) {
        await tx("readwrite", (s) => { s.put(p.full, p.id + ":full"); s.put(p.thumb, p.id + ":thumb"); });
        if (here) here.add(p.id);
      }
      const keep = new Set(photos.map((p) => p.id));
      // photos held in another browser were not on the screen, so they were not the reader's to remove here
      const elsewhere = old ? old.photos.filter((p) => !isHere(p) && !keep.has(p.id)) : [];
      const dropped = old ? old.photos.filter((p) => isHere(p) && !keep.has(p.id)) : [];
      const rec = {
        id: old ? old.id : newId("j_"),
        place_id: entry.place_id,
        visit_date: entry.visit_date,
        text: entry.text || "",
        book_ids: entry.book_ids || [],
        photos: photos.map((p) => ({ id: p.id, caption: p.caption || "", width: p.width, height: p.height })).concat(elsewhere),
        created_at: old ? old.created_at : now,
        updated_at: now,
      };
      if (old) entries[entries.indexOf(old)] = rec; else entries.push(rec);
      if (!persist()) throw new Error("storage_full");
      for (const p of dropped) await API._dropPhoto(p.id);
      return view(rec);
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
      if (here) here.delete(pid);
      try { await tx("readwrite", (s) => { s.delete(pid + ":full"); s.delete(pid + ":thumb"); }); } catch (e) { /* storage gone */ }
    },
  };
  window.RA_JOURNAL = API;
})();
