/* The Reader's Atlas — country data loader (R-5b, 11-09).
   A country's data lives in plain script files (data/<code>/geo.js, books.js, places.js, lines.js) that assign to
   window.RA_GEO and window.RA_DATA, so a double-clicked index.html still works and content packs need no build step.
   load(cfg) injects those files one after another, hands their contents back as one object and clears the globals
   for the next country. Loads are queued, so two countries never write the globals at the same time.
   Exposed as window.RA_LOAD. */
(function () {
  "use strict";
  const V = (document.currentScript && document.currentScript.dataset.v) || ""; // cache-busting version for data files
  let queue = Promise.resolve();
  const pending = new Map(); // code -> promise, so a country asked for twice loads once
  function script(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src + (V ? (src.includes("?") ? "&" : "?") + "v=" + V : "");
      s.onload = () => { s.remove(); resolve(); };
      s.onerror = () => { s.remove(); reject(new Error("failed to load " + src)); };
      document.head.append(s);
    });
  }
  function load(cfg) {
    if (pending.has(cfg.code)) return pending.get(cfg.code);
    const p = queue.then(async () => {
      window.RA_GEO = null;
      window.RA_DATA = {};
      for (const f of cfg.data) await script(f);
      const geo = window.RA_GEO, data = window.RA_DATA;
      window.RA_GEO = null;
      window.RA_DATA = {};
      if (!geo || !data.places) throw new Error(`country ${cfg.code}: data files incomplete`);
      return { cfg, geo, data: { books: data.books || [], places: data.places || [], lines: data.lines || [] } };
    });
    queue = p.catch(() => {}); // a failed country does not block the next
    pending.set(cfg.code, p);
    p.catch(() => pending.delete(cfg.code)); // so it can be retried
    return p;
  }
  // data/index.js (tools/build_index.js): which countries hold a linked place, book, author or region. Fetched once,
  // and only when a link points at something not loaded yet; resolves to { place, book, author, region } maps of
  // id -> [country codes], or to null when the file is missing (the app then looks through the countries in turn).
  let indexP = null;
  function index() {
    if (!indexP) indexP = script("data/index.js").then(() => {
      const raw = window.RA_INDEX; window.RA_INDEX = null;
      if (!raw) return null;
      const out = {};
      for (const kind of Object.keys(raw)) {
        out[kind] = new Map();
        for (const codes of Object.keys(raw[kind])) { const list = codes.split(" "); for (const id of raw[kind][codes].split(" ")) out[kind].set(id, list); }
      }
      return out;
    }).catch(() => null);
    return indexP;
  }
  window.RA_LOAD = { load, index };
})();
