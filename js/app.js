/* The Reader's Atlas — front-end prototype (no backend, no third-party libraries).
   Data: window.RA_WORLD (world outlines), window.RA_COUNTRIES (country list); each country's map and content (data/<code>/) is loaded
   on demand through window.RA_LOAD (js/data.js) and mounted cumulatively; window.RA_I18N (interface text).
   Personal data (wishlist, visited, itinerary, booklist, notes, language) goes through js/store.js. */
(function () {
  "use strict";

  // Countries load on demand (js/data.js) and stay: every map below is cumulative over the countries mounted so far.
  const LOADER = window.RA_LOAD;
  const COUNTRIES = window.RA_COUNTRIES || []; // data/countries.js
  const OPEN = COUNTRIES.filter((c) => c.open);
  const WORLD = window.RA_WORLD || []; // every country's outline; a mounted country hides its own and shows regions instead
  const I18N = window.RA_I18N;
  const SVG_NS = "http://www.w3.org/2000/svg";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- lookups ----------
  const books = new Map(), places = new Map(), regions = new Map();
  const linesByPlace = new Map(), linesByBook = new Map();
  const allLines = [];
  // authors are not a data file of their own: one entry per distinct English name on the book list (the same
  // author in two countries' packs is one author)
  const slug = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const authors = new Map();
  function indexCountry(geo, data) {
    data.lines = data.lines.filter((l) => l.status !== "rejected"); // turned down in review (docs/review-rules.md): not shown
    for (const b of data.books) books.set(b.id, b);
    for (const p of data.places) places.set(p.id, p);
    for (const r of geo.regions) regions.set(r.id, r);
    for (const l of data.lines) {
      allLines.push(l);
      for (const pid of l.place_ids) push(linesByPlace, pid, l);
      push(linesByBook, l.book_id, l);
    }
    for (const b of data.books) {
      const id = slug(b.author);
      if (!authors.has(id)) authors.set(id, { id, name: b.author, name_zh: b.author_zh, orig: b.author_orig || "", books: [] });
      authors.get(id).books.push(b);
    }
  }
  function push(map, key, val) {
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(val);
  }
  const TYPE_KEYS = ["original", "prototype", "pilgrimage", "film_location"];
  // region washes: the country config names one per region; regions it leaves out cycle through the palette so that
  // neighbours in the data order differ
  const WASH_CYCLE = ["--wash-rose", "--wash-sage", "--wash-ochre", "--wash-aqua", "--wash-peach", "--wash-lilac"];
  const WASH = new Map(); // region id -> CSS variable
  const SMALL = new Set(); // regions too small to label at country scale; markers carry them
  const mounted = new Map(); // country code -> { cfg, geo, data } once its files are loaded and drawn
  const regionCountry = new Map(); // region id -> country code
  const OPEN_BY_ISO = new Map(OPEN.map((c) => [c.iso, c]));
  // the country the reader is looking at: set by goCountry, else the one of the open region or place, else the first mounted
  function cur() {
    const code = state.country || (state.region && regionCountry.get(state.region)) || (state.place && places.get(state.place) && places.get(state.place).country);
    return (code && COUNTRIES.find((c) => c.code === code)) || (mounted.size ? mounted.values().next().value.cfg : OPEN[0]);
  }
  const countryLabel = (c = cur()) => (zh() ? c.name_zh : c.name);
  const countryShort = (c = cur()) => (zh() ? c.short_zh || c.name_zh : c.short || c.name);

  // ---------- storage ----------
  // Personal data lives in js/store.js (RA_STORE); app.js reads the live objects and saves through it (R-6, 11-09).
  const RS = window.RA_STORE;
  const store = { get: (key, fallback) => RS.prefs.get(key, fallback), set: (key, val) => RS.prefs.set(key, val) };
  const me = RS.state; // wishlist, visited (Sets of place ids); itinerary (array); shelf, notes (objects); faves (Set)

  // ---------- language ----------
  let lang = store.get("lang", "en") === "zh" ? "zh" : "en";
  const T = () => I18N[lang];
  const zh = () => lang === "zh";
  // data fields in the current language
  const placeName = (p) => (zh() ? p.name_zh : p.name);
  const regionName = (r) => (zh() ? r.name_zh : r.name);
  const bookTitle = (b) => (zh() ? `《${b.title_zh}》` : b.title);
  const bookAuthor = (b) => (zh() ? b.author_zh : b.author);
  const authorName = (a) => (zh() ? a.name_zh : a.name);
  const bookLabel = (b) => (zh() ? `${bookTitle(b)}${bookAuthor(b)}` : `${b.title}, ${b.author}`);
  const lineLocation = (l) => (zh() ? l.location_zh || l.location : l.location);
  const typeLabel = (type) => T().types[type].label;
  const langName = (code) => T().langName[code] || code;

  // ---------- projection (Web Mercator, world = 1000 units wide) ----------
  const W = 1000;
  function project(lon, lat) {
    const phi = Math.max(-85, Math.min(85, lat)) * Math.PI / 180;
    return [
      (lon + 180) / 360 * W,
      W / (2 * Math.PI) * (Math.PI - Math.log(Math.tan(Math.PI / 4 + phi / 2))),
    ];
  }
  function ringPath(ring, close) {
    let d = "";
    for (let i = 0; i < ring.length; i++) {
      const [x, y] = project(ring[i][0], ring[i][1]);
      d += (i ? "L" : "M") + x.toFixed(2) + "," + y.toFixed(2);
    }
    return close ? d + "Z" : d;
  }

  // point in polygon on lon/lat rings (even-odd over all rings of a unit)
  function inRings(lon, lat, rings) {
    let inside = false;
    for (const r of rings) {
      for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
        const [xi, yi] = r[i], [xj, yj] = r[j];
        if ((yi > lat) !== (yj > lat) && lon < (xj - xi) * (lat - yi) / (yj - yi) + xi) inside = !inside;
      }
    }
    return inside;
  }
  function assignRegions(list, geo) {
    for (const p of list) {
      if (p.region && geo.regions.some((r) => r.id === p.region)) continue; // set in the data: a border town the simplified map puts on the wrong side
      const u = geo.units.find((unit) => inRings(p.lon, p.lat, unit.g));
      if (u) { p.region = u.r; continue; }
      // coastal points just outside the simplified coastline (a pier, a harbour wall): take the region
      // of the nearest boundary point — the same rule tools/validate.js uses
      let best = null, bd = Infinity;
      const c = Math.cos(p.lat * Math.PI / 180);
      for (const unit of geo.units) for (const ring of unit.g) for (const [x, y] of ring) {
        const d = ((x - p.lon) * c) ** 2 + (y - p.lat) ** 2;
        if (d < bd) { bd = d; best = unit.r; }
      }
      p.region = best;
    }
  }

  // ---------- DOM refs ----------
  const svg = document.getElementById("map");
  const reader = document.getElementById("reader");
  const crumbs = document.getElementById("crumbs");
  const mapTitle = document.getElementById("map-title");
  const tooltip = document.getElementById("tooltip");
  const legend = document.getElementById("legend");
  const root = el("g", { id: "viewport" });
  const gWorld = el("g", { class: "world" });
  const gUK = el("g", { class: "uk country-regions" }); // the regions of every mounted country (class "uk" kept for the stylesheet)
  const gUnitLabels = el("g", { class: "unit-labels", "aria-hidden": "true" });
  const gLabels = el("g", { class: "labels" });
  const gMarkers = el("g", { class: "markers" });
  root.append(gWorld, gUK, gUnitLabels, gLabels, gMarkers);
  // the vintage street basemap underneath (js/basemap.js); purely visual
  const basemap = window.RA_BASEMAP || null;
  if (basemap) basemap.init(document.getElementById("basemap"), false);
  if (basemap) basemap.onTiles(() => applyView()); // offline the painted regions stay solid
  svg.append(root);

  function el(tag, attrs, parent) {
    const n = document.createElementNS(SVG_NS, tag);
    for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
    if (parent) parent.append(n);
    return n;
  }
  function h(html) {
    const t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content;
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function darken(hex, f) {
    const n = parseInt(hex.slice(1), 16);
    const c = [n >> 16, (n >> 8) & 255, n & 255].map((v) => Math.round(v * f));
    return "rgb(" + c.join(",") + ")";
  }

  // ---------- inland borders: segments shared by two areas are borders, unshared ones are coastline ----------
  const segKey = (a, b) => {
    const A = a[0].toFixed(5) + "," + a[1].toFixed(5), B = b[0].toFixed(5) + "," + b[1].toFixed(5);
    return A < B ? A + "|" + B : B + "|" + A;
  };
  // how many *different* areas use each segment (a coastline repeated inside one area stays coast)
  function countSegments(owners) { // owners: [[ownerId, [[points, closed]]]]
    const m = new Map();
    for (const [owner, lines] of owners) {
      for (const [pts, closed] of lines) {
        const n = pts.length;
        for (let i = 1; i < n + (closed ? 1 : 0); i++) {
          const k = segKey(pts[i - 1], pts[i % n]);
          if (!m.has(k)) m.set(k, new Set());
          m.get(k).add(owner);
        }
      }
    }
    const out = new Map();
    for (const [k, set] of m) out.set(k, set.size);
    return out;
  }
  const regionSegs = new Map(), unitSegs = new Map(); // over all mounted countries
  function addCounts(into, from) { for (const [k, n] of from) into.set(k, (into.get(k) || 0) + n); }
  // path through only the shared runs of the given lines
  function sharedPath(lines, counts) {
    let d = "";
    for (const [pts, closed] of lines) {
      const n = pts.length;
      let open = false;
      for (let i = 1; i < n + (closed ? 1 : 0); i++) {
        const a = pts[i - 1], b = pts[i % n];
        if ((counts.get(segKey(a, b)) || 0) > 1) {
          if (!open) { const [x, y] = project(a[0], a[1]); d += "M" + x.toFixed(2) + "," + y.toFixed(2); open = true; }
          const [x, y] = project(b[0], b[1]); d += "L" + x.toFixed(2) + "," + y.toFixed(2);
        } else open = false;
      }
    }
    return d;
  }
  function innerPath(lines) { return sharedPath(lines, regionSegs); }
  function unitEdges(rid, geo) {
    return sharedPath(geo.units.filter((u) => u.r === rid).flatMap((u) => u.g.map((ring) => [ring, true])), unitSegs);
  }

  // ---------- county / borough names: a finer layer of detail once zoomed in (not clickable) ----------
  const unitLabels = [];
  function addUnitLabel(u) {
    // label the largest ring at its area centroid (projected units)
    let best = null, bestA = 0;
    for (const ring of u.g) {
      const pts = ring.map(([lo, la]) => project(lo, la));
      let a = 0, cx = 0, cy = 0;
      for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
        const f = pts[j][0] * pts[i][1] - pts[i][0] * pts[j][1];
        a += f; cx += (pts[j][0] + pts[i][0]) * f; cy += (pts[j][1] + pts[i][1]) * f;
      }
      if (Math.abs(a) > bestA) {
        bestA = Math.abs(a);
        const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
        best = { x: cx / (3 * a), y: cy / (3 * a), w: Math.max(...xs) - Math.min(...xs), h: Math.max(...ys) - Math.min(...ys) };
      }
    }
    if (!best || !u.n) return;
    const text = el("text", { class: "unit-label", x: best.x, y: best.y }, gUnitLabels);
    text.textContent = u.n.replace(/^(City of |London Borough of |Royal Borough of )/, "");
    unitLabels.push({ node: text, ...best, area: bestA, ll: unproject(best.x, best.y) });
  }
  // greedy placement in screen space, biggest areas first; a name shows only if it fits inside its area
  // screen boxes of the map furniture (title block, legend, buttons, compass, credits), in map coordinates
  function chromeBoxes() {
    const svgR = svg.getBoundingClientRect(), out = [];
    for (const sel of [".titleblock", ".legend", ".map-controls", ".compass", ".attribution"]) {
      const e = document.querySelector(sel);
      if (!e) continue;
      const r = e.getBoundingClientRect();
      if (r.width && r.height) out.push([r.left - svgR.left - 6, r.top - svgR.top - 6, r.right - svgR.left + 6, r.bottom - svgR.top + 6]);
    }
    return out;
  }
  function placeUnitLabels(z) {
    const show = z >= 7.6 && z < 13;
    gUnitLabels.style.display = show ? "" : "none";
    if (!show) return;
    const [w, hgt] = size();
    const fs = 10.5, placed = markerLabelBoxes.slice().concat(markerDotBoxes, chromeBoxes()); // place names, markers and the map furniture win
    const order = unitLabels.slice().sort((a, b) => b.area - a.area);
    for (const L of order) {
      const sx = view.x + view.k * L.x, sy = view.y + view.k * L.y;
      const tw = L.node.textContent.length * fs * 0.72 + 6;
      const fits = L.w * view.k > tw * 0.9 && L.h * view.k > fs * 2.2;
      const onScreen = sx > -tw && sx < w + tw && sy > -20 && sy < hgt + 20;
      const box = [sx - tw / 2, sy - fs, sx + tw / 2, sy + fs * 0.6];
      const clash = placed.some((b) => box[0] < b[2] && box[2] > b[0] && box[1] < b[3] && box[3] > b[1]);
      const ok = fits && onScreen && !clash;
      L.node.style.display = ok ? "" : "none";
      if (ok) {
        placed.push(box);
        L.node.style.fontSize = fs / view.k + "px";
        L.node.style.strokeWidth = 3 / view.k + "px";
      }
    }
  }

  function unproject(x, y) {
    return [(x / W) * 360 - 180, (Math.atan(Math.sinh(Math.PI - (2 * Math.PI * y) / W)) * 180) / Math.PI];
  }
  let markerLabelBoxes = [], markerDotBoxes = [];
  // search highlight (docs/map-layers.md 3.3): places matching the query, and the result under the cursor
  let searchHitIds = null, searchFocusIds = null;
  // tell the basemap where our own names and markers sit, so its labels keep clear (no second "Whitby")
  let blockerTimer = null, blockerSig = "";
  function scheduleBlockers() {
    if (!basemap) return;
    clearTimeout(blockerTimer);
    blockerTimer = setTimeout(() => {
      const feats = [];
      for (const g of markerNodes.values()) {
        if (markerOff(g)) continue;
        const p = places.get(g.dataset.id);
        const label = g.querySelector(".marker-label");
        const shown = label.style.display !== "none" && label.textContent;
        feats.push({ type: "Feature", properties: { kind: shown ? "marker" : "dot", t: shown ? label.textContent : "", side: g.dataset.side || "right" },
          geometry: { type: "Point", coordinates: [p.lon, p.lat] } });
      }
      if (gUnitLabels.style.display !== "none") {
        for (const L of unitLabels) {
          if (L.node.style.display === "none") continue;
          feats.push({ type: "Feature", properties: { kind: "unit", t: L.node.textContent }, geometry: { type: "Point", coordinates: L.ll } });
        }
      }
      const sig = feats.map((f) => f.properties.kind + f.properties.t + (f.properties.side || "") + f.geometry.coordinates.join()).join("|");
      if (sig === blockerSig) return;
      blockerSig = sig;
      basemap.setBlockers({ type: "FeatureCollection", features: feats });
    }, 120);
  }

  // ---------- draw map ----------
  const worldNodes = new Map(); // iso -> outline path
  for (const c of WORLD) {
    const p = el("path", { class: "country", d: c.g.map((r) => ringPath(r, true)).join("") }, gWorld);
    p.dataset.name = c.name;
    p.dataset.nameZh = c.name_zh || c.name;
    p.dataset.iso = c.id;
    if (OPEN_BY_ISO.has(c.id)) p.classList.add("is-open");
    worldNodes.set(c.id, p);
  }
  // the South China Sea dashed line (China view, decision A-22), one path per dash
  for (const l of window.RA_WORLD_LINES || []) el("path", { class: "sea-claim", d: ringPath(l, false) }, gWorld);
  // China's land border as China sees it (tools/cn_admin1.py), shown once the street basemap replaces our outlines,
  // in place of the basemap's own national borders there (js/basemap.js OWN_AREAS)
  for (const o of window.RA_WORLD_OWN || []) el("path", { class: "land-border", d: o.land_border.map((l) => ringPath(l, false)).join("") }, gWorld);
  const regionNodes = new Map();
  const regionLabels = new Map();
  const allUnits = []; // every mounted country's units, for the basemap washes
  function drawCountry(cfg, geo) {
    // region ids are shared across countries (routes, masks, data), so they must be unique: China's carry "CN-" (Hainan vs Hawaii)
    for (const r of geo.regions) if (regionCountry.has(r.id) && regionCountry.get(r.id) !== cfg.code) console.error(`region id ${r.id} of ${cfg.code} is already used by ${regionCountry.get(r.id)}`);
    geo.regions.forEach((r, i) => { WASH.set(r.id, (cfg.wash || {})[r.id] || WASH_CYCLE[i % WASH_CYCLE.length]); regionCountry.set(r.id, cfg.code); });
    for (const id of cfg.small_regions || []) SMALL.add(id);
    addCounts(regionSegs, countSegments(geo.regions.map((r) => [r.id, r.outline.map((l) => [l, false])])));
    addCounts(unitSegs, countSegments(geo.units.map((u, i) => [cfg.code + i, u.g.map((ring) => [ring, true])])));
    for (const r of geo.regions) {
      const g = el("g", { class: "region", "data-id": r.id }, gUK);
      const wash = cssVar(WASH.get(r.id));
      regionNodes.set(r.id, g);
      for (const u of geo.units.filter((x) => x.r === r.id)) {
        el("path", { class: "unit", d: u.g.map((ring) => ringPath(ring, true)).join(""), fill: wash, stroke: wash }, g);
        addUnitLabel(u);
      }
      const outline = r.outline.map((l) => ringPath(l, false)).join("");
      el("path", { class: "region-band", d: outline, stroke: darken(wash, 0.78) }, g);
      el("path", { class: "region-line", d: outline }, g);
      // inland-only versions, used when the street basemap supplies the real coastline
      el("path", { class: "region-band inner", d: innerPath(r.outline.map((l) => [l, false])), stroke: darken(wash, 0.78) }, g);
      el("path", { class: "unit-edges", d: unitEdges(r.id, geo) }, g);
      el("path", { class: "region-line inner", d: innerPath(r.outline.map((l) => [l, false])) }, g);
      const [x, y] = project(...r.centroid); // provisional; layoutRegionLabels() finds the real spot
      const label = el("text", { class: "region-label", x, y }, gLabels);
      if (SMALL.has(r.id)) label.style.display = "none";
      regionLabels.set(r.id, label);
    }
    allUnits.push(...geo.units);
    // region washes for the basemap (drawn under its water so the coast is OpenStreetMap's)
    if (basemap) {
      basemap.setRegions({
        type: "FeatureCollection",
        features: allUnits.map((u) => ({
          type: "Feature",
          properties: { r: u.r, wash: cssVar(WASH.get(u.r)) },
          geometry: { type: "MultiPolygon", coordinates: u.g.map((ring) => [ring.concat([ring[0]])]) },
        })),
      });
    }
    const outline = worldNodes.get(cfg.iso);
    if (outline) outline.style.display = "none"; // the regions stand in for the country's outline from now on
  }

  // ---------- region names: automatic placement (UK scale) ----------
  // Each name tries spots inside its own region, most open first, and keeps clear of other region
  // names, markers, the active place name and the map chrome; long names may wrap onto two lines.
  // A raster mask of the regions answers "which region is this point in?" in constant time.
  const MASK_S = 16; // mask pixels per world unit (≈ 1 px at UK scale)
  const masks = new Map(); // country code -> mask; a point is looked up in each (a few at most)
  function buildRegionMask(geo) {
    try {
      const ids = geo.regions.map((r) => r.id); // region number n (1-based) -> ids[n - 1]
      const regionNo = new Map(ids.map((id, i) => [id, i + 1]));
      const proj = geo.units.map((u) => ({ r: u.r, rings: u.g.map((ring) => ring.map(([lo, la]) => project(lo, la))) }));
      let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      for (const u of proj) for (const ring of u.rings) for (const [x, y] of ring) {
        if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
      }
      x0 -= 0.5; y0 -= 0.5; x1 += 0.5; y1 += 0.5;
      // big countries get a coarser mask so the canvas stays around 1200 px wide (the UK keeps MASK_S)
      const S = Math.min(MASK_S, 1200 / (x1 - x0));
      const w = Math.ceil((x1 - x0) * S), h = Math.ceil((y1 - y0) * S);
      const c = document.createElement("canvas");
      c.width = w; c.height = h;
      const ctx = c.getContext("2d", { willReadFrequently: true });
      // one path per region, so the seams between its own counties are not anti-aliased
      for (const r of geo.regions) {
        ctx.beginPath();
        for (const u of proj) {
          if (u.r !== r.id) continue;
          for (const ring of u.rings) {
            ring.forEach(([x, y], i) => (i ? ctx.lineTo : ctx.moveTo).call(ctx, (x - x0) * S, (y - y0) * S));
            ctx.closePath();
          }
        }
        // region number in steps of 20 on two channels (12 per channel: up to 144 regions); a blended edge pixel
        // lands between the steps and counts as border
        const n = regionNo.get(r.id) - 1;
        ctx.fillStyle = `rgb(${(n % 12 + 1) * 20},${Math.floor(n / 12) * 20},0)`;
        ctx.fill("nonzero");
      }
      const px = ctx.getImageData(0, 0, w, h).data;
      const data = new Uint16Array(w * h);
      for (let i = 0; i < w * h; i++) {
        const v = px[i * 4], g = px[i * 4 + 1], a = px[i * 4 + 3];
        data[i] = a === 255 && v % 20 === 0 && g % 20 === 0 && v > 0 && v <= 240 ? (v / 20 - 1) + 12 * (g / 20) + 1 : 0;
      }
      // chamfer distance (in mask px) to the nearest pixel of another region or the sea
      const INF = 1e9, dist = new Float32Array(w * h);
      for (let i = 0; i < w * h; i++) dist[i] = data[i] ? INF : 0;
      const same = (i, j) => data[i] === data[j];
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const i = y * w + x;
        if (!data[i]) continue;
        let d = dist[i];
        if (x > 0) d = Math.min(d, same(i, i - 1) ? dist[i - 1] + 1 : 1);
        if (y > 0) {
          d = Math.min(d, same(i, i - w) ? dist[i - w] + 1 : 1);
          if (x > 0) d = Math.min(d, same(i, i - w - 1) ? dist[i - w - 1] + 1.414 : 1.414);
          if (x < w - 1) d = Math.min(d, same(i, i - w + 1) ? dist[i - w + 1] + 1.414 : 1.414);
        } else d = Math.min(d, 1);
        if (x === 0 || x === w - 1) d = Math.min(d, 1);
        dist[i] = d;
      }
      for (let y = h - 1; y >= 0; y--) for (let x = w - 1; x >= 0; x--) {
        const i = y * w + x;
        if (!data[i]) continue;
        let d = dist[i];
        if (x < w - 1) d = Math.min(d, same(i, i + 1) ? dist[i + 1] + 1 : 1);
        if (y < h - 1) {
          d = Math.min(d, same(i, i + w) ? dist[i + w] + 1 : 1);
          if (x < w - 1) d = Math.min(d, same(i, i + w + 1) ? dist[i + w + 1] + 1.414 : 1.414);
          if (x > 0) d = Math.min(d, same(i, i + w - 1) ? dist[i + w - 1] + 1.414 : 1.414);
        } else d = Math.min(d, 1);
        dist[i] = d;
      }
      // candidate spots per region: most open first, at least half a world unit apart
      const cands = new Map(), area = new Map();
      const STEP = 4;
      for (let y = 0; y < h; y += STEP) for (let x = 0; x < w; x += STEP) {
        const v = data[y * w + x];
        if (!v) continue;
        if (!cands.has(v)) cands.set(v, []);
        cands.get(v).push({ x: x0 + (x + 0.5) / S, y: y0 + (y + 0.5) / S, d: dist[y * w + x] });
        area.set(v, (area.get(v) || 0) + 1);
      }
      for (const [v, list] of cands) {
        list.sort((a, b) => b.d - a.d);
        const kept = [];
        for (const c of list) {
          if (kept.length >= 80) break;
          if (kept.some((k) => Math.hypot(k.x - c.x, k.y - c.y) < 0.5)) continue;
          kept.push(c);
        }
        cands.set(v, kept);
      }
      // last resort (3.2): spots on the sea just off a region's own coast, nearest the coast first
      const sea = new Map(), R = 12;
      for (let y = 0; y < h; y += STEP) for (let x = 0; x < w; x += STEP) {
        if (data[y * w + x]) continue;
        let best = null;
        for (let dy = -R; dy <= R; dy += 2) for (let dx = -R; dx <= R; dx += 2) {
          const xx = x + dx, yy = y + dy;
          if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue;
          const v = data[yy * w + xx];
          if (!v) continue;
          const dd = Math.hypot(dx, dy);
          if (!best || dd < best.d) best = { v, d: dd };
        }
        if (!best) continue;
        if (!sea.has(best.v)) sea.set(best.v, []);
        sea.get(best.v).push({ x: x0 + (x + 0.5) / S, y: y0 + (y + 0.5) / S, d: best.d });
      }
      for (const [v, list] of sea) {
        list.sort((a, b) => a.d - b.d);
        const kept = [];
        for (const c of list) {
          if (kept.length >= 60) break;
          if (kept.some((k) => Math.hypot(k.x - c.x, k.y - c.y) < 0.4)) continue;
          kept.push(c);
        }
        sea.set(v, kept);
      }
      // keyed by region id from here on
      const byId = (m) => new Map([...m].map(([n, v]) => [ids[n - 1], v]));
      return { x0, y0, w, h, s: S, data, ids, cands: byId(cands), area: byId(area), sea: byId(sea) };
    } catch (e) {
      console.warn("[labels] region mask unavailable:", e);
      return null;
    }
  }
  function regionAtWorld(x, y) {
    for (const mask of masks.values()) {
      const i = Math.floor((x - mask.x0) * mask.s), j = Math.floor((y - mask.y0) * mask.s);
      if (i < 0 || j < 0 || i >= mask.w || j >= mask.h) continue;
      const n = mask.data[j * mask.w + i];
      if (n) return mask.ids[n - 1];
    }
    return null;
  }
  // two balanced lines for multi-word names ("Yorkshire and / the Humber"); null if one word
  function twoLines(name) {
    // Chinese names have no spaces: break around 英格兰 ("东南 / 英格兰", "英格兰 / 东部"), else in the middle
    if (/[\u4e00-\u9fff]/.test(name) && !name.includes("-") && name.length >= 4) {
      const i = name.indexOf("英格兰");
      if (i > 0) return [name.slice(0, i), name.slice(i)];
      if (i === 0) return [name.slice(0, 3), name.slice(3)];
      const h = Math.floor(name.length / 2);
      return [name.slice(0, h), name.slice(h)];
    }
    const parts = name.includes(" ") ? name.split(" ") : name.includes("-") ? name.split(/(?<=-)/) : null;
    if (!parts || parts.length < 2) return null;
    let best = null;
    for (let i = 1; i < parts.length; i++) {
      const a = parts.slice(0, i).join(name.includes(" ") ? " " : ""), b = parts.slice(i).join(name.includes(" ") ? " " : "");
      const score = Math.max(a.length, b.length);
      if (!best || score < best.score) best = { a, b, score };
    }
    return [best.a, best.b];
  }
  function setLabelText(node, x, y, lines) {
    node.setAttribute("x", x);
    node.setAttribute("y", y);
    node.replaceChildren();
    if (lines.length === 1) {
      const t = el("tspan", { x, dy: "0.35em" }, node);
      t.textContent = lines[0];
    } else {
      el("tspan", { x, dy: "-0.25em" }, node).textContent = lines[0];
      el("tspan", { x, dy: "1.2em" }, node).textContent = lines[1];
    }
  }
  const REGION_FS = 11.5; // px on screen
  function setLabelScale(node, scale) {
    node.dataset.scale = scale;
    node.style.fontSize = (REGION_FS * scale) / view.k + "px";
  }
  function measure(node, lines, scale) {
    setLabelScale(node, scale);
    setLabelText(node, 0, 0, lines);
    const b = node.getBBox();
    return [b.width * view.k, b.height * view.k];
  }
  const regionLabelBoxes = [];
  let regionLayoutTimer = null, regionLayoutDone = false;
  function scheduleRegionLayout() {
    if (!regionLayoutDone) return layoutRegionLabels();
    clearTimeout(regionLayoutTimer);
    regionLayoutTimer = setTimeout(layoutRegionLabels, 90);
  }
  function layoutRegionLabels() {
    regionLabelBoxes.length = 0;
    if (gLabels.style.display === "none") return;
    regionLayoutDone = true;
    const k = view.k, [w, h] = size(), right = w - panelOffset();
    const svgR = svg.getBoundingClientRect();
    const obstacles = [];
    for (const sel of [".titleblock", ".legend", ".map-controls", ".compass", ".attribution"]) {
      const e = document.querySelector(sel);
      if (!e) continue;
      const r = e.getBoundingClientRect();
      if (r.width && r.height) obstacles.push([r.left - svgR.left - 6, r.top - svgR.top - 6, r.right - svgR.left + 6, r.bottom - svgR.top + 6]);
    }
    for (const g of markerNodes.values()) {
      if (markerOff(g)) continue;
      const sx = view.x + k * Number(g.dataset.x), sy = view.y + k * Number(g.dataset.y);
      obstacles.push([sx - 8, sy - 8, sx + 8, sy + 8]);
    }
    obstacles.push(...markerLabelBoxes);
    const hit = (b, list) => list.some((o) => b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1]);
    const maskOf = (r) => masks.get(regionCountry.get(r.id)) || null;
    const area = (r) => { const m = maskOf(r); return m ? m.area.get(r.id) || 0 : 0; };
    const order = [...regions.values()].filter((r) => !SMALL.has(r.id) && !farNameCountries.get(regionCountry.get(r.id))).sort((a, b) => area(a) - area(b)); // smallest first
    for (const r of order) {
      const node = regionLabels.get(r.id);
      node.style.display = "";
      const name = regionName(r);
      const one = [name], two = twoLines(name);
      const mask = maskOf(r);
      if (!mask) { const [x, y] = project(...r.centroid); setLabelText(node, x, y, one); continue; }
      const id = r.id;
      const cands = mask.cands.get(id) || [];
      const sized = {};
      const variantsAt = (scale) => sized[scale] || (sized[scale] = [one, two].filter(Boolean).map((lines) => ({ lines, scale, size: measure(node, lines, scale) })));
      let chosen = null;
      // wholly inside its own region comes first, even at a smaller size; only then a name that
      // mostly fits; at each step one line before two
      const TIERS = [[1, 1], [0.85, 1], [0.75, 1], [1, 0.8], [0.85, 0.8], [0.75, 0.8], [0.85, 0.6], [0.75, 0.5], [0.75, 0.3], [0.65, 0.5], [0.65, 0.3], [0.65, 0.2], [0.6, 0.3], [0.6, 0.2], [0.55, 0.3]]; // [0.65, 0.2] and [0.6, 0.3] added 11-05 when new places crowded South East at 1280 px; the last two later on 11-05 after sixteen more writers
      for (const [scale, minInside] of TIERS) {
        for (const v of variantsAt(scale)) {
          const [bw, bh] = v.size;
          for (const c of cands) {
            const sx = view.x + k * c.x, sy = view.y + k * c.y;
            const box = [sx - bw / 2 - 3, sy - bh / 2 - 2, sx + bw / 2 + 3, sy + bh / 2 + 2];
            if (box[0] < 0 || box[1] < 0 || box[2] > right || box[3] > h) continue;
            if (hit(box, regionLabelBoxes) || hit(box, obstacles)) continue;
            let inside = 0, n = 0;
            for (let iy = 0; iy <= 2; iy++) for (let ix = 0; ix <= 4; ix++) {
              const px = box[0] + 3 + ((bw) * ix) / 4, py = box[1] + 2 + ((bh) * iy) / 2;
              n++;
              if (regionAtWorld((px - view.x) / k, (py - view.y) / k) === id) inside++;
            }
            if (inside / n >= minInside) { chosen = { c, v, box }; break; }
          }
          if (chosen) break;
        }
        if (chosen) break;
      }
      // nowhere free inside: try the sea just off its own coast, never over another region (added 11-05)
      if (!chosen) {
        for (const scale of [0.75, 0.65]) {
          for (const v of variantsAt(scale)) {
            const [bw, bh] = v.size;
            for (const c of mask.sea.get(id) || []) {
              const sx = view.x + k * c.x, sy = view.y + k * c.y;
              const box = [sx - bw / 2 - 3, sy - bh / 2 - 2, sx + bw / 2 + 3, sy + bh / 2 + 2];
              if (box[0] < 0 || box[1] < 0 || box[2] > right || box[3] > h) continue;
              if (hit(box, regionLabelBoxes) || hit(box, obstacles)) continue;
              let foreign = false;
              for (let iy = 0; iy <= 2 && !foreign; iy++) for (let ix = 0; ix <= 4; ix++) {
                const px = box[0] + 3 + ((bw) * ix) / 4, py = box[1] + 2 + ((bh) * iy) / 2;
                const r = regionAtWorld((px - view.x) / k, (py - view.y) / k);
                if (r && r !== id) { foreign = true; break; }
              }
              if (!foreign) { chosen = { c, v, box }; break; }
            }
            if (chosen) break;
          }
          if (chosen) break;
        }
      }
      if (chosen) {
        setLabelScale(node, chosen.v.scale);
        setLabelText(node, chosen.c.x, chosen.c.y, chosen.v.lines);
        regionLabelBoxes.push(chosen.box);
      } else {
        node.style.display = "none"; // nowhere free: better absent than overlapping
      }
    }
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { regionLayoutDone = false; scheduleRegionLayout(); });

  // marker shapes in screen pixels; each marker group is counter-scaled on zoom
  function shape(type) {
    if (type === "pilgrimage") {
      const pts = [];
      for (let i = 0; i < 10; i++) {
        const a = -Math.PI / 2 + i * Math.PI / 5, rad = i % 2 ? 3.2 : 7.5;
        pts.push((Math.cos(a) * rad).toFixed(2) + "," + (Math.sin(a) * rad).toFixed(2));
      }
      return el("polygon", { class: "m-shape", points: pts.join(" ") });
    }
    if (type === "film_location") return el("rect", { class: "m-shape", x: -5, y: -5, width: 10, height: 10, rx: 1.5 });
    return el("circle", { class: "m-shape", r: type === "prototype" ? 5 : 5.5 });
  }
  const markerNodes = new Map();
  function addMarkers(list) {
    for (const p of list) {
      const [x, y] = project(p.lon, p.lat);
      const g = el("g", { class: "marker t-" + p.place_type, tabindex: 0, role: "button" }, gMarkers);
      g.dataset.id = p.id;
      if (farCountries.get(p.country)) g.classList.add("is-far");
      g.dataset.x = x;
      g.dataset.y = y;
      el("circle", { class: "m-hit", r: 11 }, g);
      el("circle", { class: "m-ring", r: 10 }, g);
      g.append(shape(p.place_type));
      el("text", { class: "marker-label", x: 10, y: 4 }, g).textContent = placeName(p);
      g.setAttribute("aria-label", placeName(p));
      markerNodes.set(p.id, g);
    }
  }

  // My travels on the map: a small pennant planted at the marker's upper right, coloured by list
  // (green: Places I've been, red: Upcoming trips, ochre: Wishlist). A place on several lists shows one flag,
  // in that order of priority. The art is in design units (staff foot at 0,0, knob at y -100), scaled to about
  // 24 px; strokes don't scale, so the outline stays a fixed hairline. The staff sits behind the marker shape.
  const FLAG_KINDS = ["been", "trip", "wish"];
  const FLAG_SCALE = 0.235;
  const FLAG_ART = {
    body: "M2.5 -95 C16 -99 33 -94 49 -85 C48 -79 47 -73 46 -67 C33 -64 18 -61 2.5 -62Z",
    fold: "M49 -85 C51.5 -88 55 -89.5 58.5 -88 C57 -82 55.5 -76 54 -71 C51 -70 48.5 -68.5 46 -67 C47 -73 48 -79 49 -85Z",
    tail: "M58.5 -88 C64 -85 69 -85 74 -88 C77 -90 80 -91.5 85 -91 C79 -86 73 -79 65 -75.5 C61 -73.5 57 -72 54 -71 C55.5 -76 57 -82 58.5 -88Z",
    ties: "M-3.4 -93.8 L3.6 -91.6 M-3.4 -64.6 L3.6 -62.4",
  };
  function flagNode(kind) {
    const f = el("g", { class: "m-flag k-" + kind, "data-kind": kind, "aria-hidden": "true" });
    const art = el("g", { transform: `translate(3.5 -1) scale(${FLAG_SCALE})` }, f);
    el("rect", { class: "m-flag-pole", x: -2.1, y: -100, width: 4.2, height: 100, rx: 2.1 }, art);
    const cloth = el("g", { class: "m-flag-cloth" }, art);
    el("path", { class: "m-flag-fold", d: FLAG_ART.fold }, cloth);
    el("path", { class: "m-flag-face", d: FLAG_ART.tail }, cloth);
    el("path", { class: "m-flag-face", d: FLAG_ART.body }, cloth);
    el("path", { class: "m-flag-ties", d: FLAG_ART.ties }, cloth);
    el("circle", { class: "m-flag-finial", cx: 0, cy: -100, r: 6.4 }, art);
    return f;
  }
  // planting: the staff grows up from its foot with the knob on top, then the cloth runs up it and fades in.
  // Done by setting SVG attributes each frame (see the note in css/style.css); the clock starts at the first frame,
  // so work done in the same click does not eat the start of the animation.
  const easeOut = (x) => 1 - Math.pow(1 - x, 3);
  function raiseFlag(f) {
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const pole = f.querySelector(".m-flag-pole"), knob = f.querySelector(".m-flag-finial"), cloth = f.querySelector(".m-flag-cloth");
    const POLE = 260, DELAY = 160, CLOTH = 620;
    const draw = (t) => {
      const h = 100 * easeOut(Math.min(1, t / POLE));
      pole.setAttribute("y", -h);
      pole.setAttribute("height", h);
      knob.setAttribute("cy", -h);
      const c = Math.min(1, Math.max(0, (t - DELAY) / CLOTH));
      cloth.setAttribute("transform", `translate(0 ${(60 * (1 - easeOut(c))).toFixed(2)})`);
      cloth.setAttribute("opacity", Math.min(1, c / 0.6).toFixed(3));
    };
    draw(0);
    let t0 = null;
    const step = (now) => {
      if (!f.isConnected) return;
      if (t0 === null) t0 = now;
      const t = now - t0;
      if (t >= DELAY + CLOTH) {
        draw(DELAY + CLOTH);
        cloth.removeAttribute("transform");
        cloth.removeAttribute("opacity");
        return;
      }
      draw(t);
      requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
  const flagsShown = new Set(FLAG_KINDS); // each kind can be switched off in the legend
  function flagKind(id, trips) {
    const on = { been: me.visited.has(id), trip: trips.has(id), wish: me.wishlist.has(id) };
    return FLAG_KINDS.find((k) => on[k] && flagsShown.has(k)) || null;
  }
  // put up, swap or take down flags to match the three lists; `raised` (a place just added to a list) gets the planting animation
  function syncFlags(raised) {
    const trips = new Set(me.itinerary.map((x) => x.place_id));
    for (const [id, g] of markerNodes) {
      const kind = flagKind(id, trips), f = g.querySelector(".m-flag");
      if (f && f.dataset.kind === kind) continue;
      if (f) f.remove();
      g.classList.toggle("has-flag", !!kind);
      if (!kind) continue;
      const n = flagNode(kind);
      g.insertBefore(n, g.querySelector(".m-shape"));
      if (id === raised) raiseFlag(n);
    }
    updateLegendFlags();
  }

  // legend doubles as the filter
  const filters = new Set(TYPE_KEYS);
  const legendItems = new Map();
  for (const type of TYPE_KEYS) {
    const lab = document.createElement("label");
    const box = document.createElement("input");
    box.type = "checkbox";
    box.checked = true;
    box.addEventListener("change", () => {
      box.checked ? filters.add(type) : filters.delete(type);
      updateMarkers();
    });
    const icon = el("svg", { width: 18, height: 18, viewBox: "-9 -9 18 18", class: "marker t-" + type, "aria-hidden": "true" });
    icon.append(shape(type));
    const text = document.createElement("span");
    lab.append(box, icon, text);
    legend.append(lab);
    legendItems.set(type, { lab, text });
  }
  // My travels in the legend: a header that folds out one row per list (in the order of My travels; a row shows
  // once its list has a place). Closed by default; the choice is remembered. The header shows the flags in use.
  const flagGroup = document.createElement("div");
  flagGroup.className = "legend-flags";
  const flagHead = document.createElement("button");
  flagHead.type = "button";
  flagHead.className = "legend-flags-head";
  flagHead.setAttribute("aria-controls", "legend-flag-rows");
  const flagSwatch = el("svg", { class: "legend-flags-swatch", width: 18, height: 18, "aria-hidden": "true" });
  const flagHeadText = document.createElement("span");
  const chevron = el("svg", { class: "legend-flags-chevron", width: 12, height: 12, viewBox: "0 0 12 12", "aria-hidden": "true" });
  el("path", { d: "M2.5 4.5 L6 8 L9.5 4.5" }, chevron);
  flagHead.append(flagSwatch, flagHeadText, chevron);
  const flagBody = document.createElement("div");
  flagBody.className = "legend-flag-rows";
  flagBody.id = "legend-flag-rows";
  const flagInner = document.createElement("div");
  flagBody.append(flagInner);
  flagGroup.append(flagHead, flagBody);
  const flagRows = new Map();
  for (const kind of ["trip", "wish", "been"]) {
    const lab = document.createElement("label");
    const box = document.createElement("input");
    box.type = "checkbox";
    box.checked = true;
    box.addEventListener("change", () => {
      box.checked ? flagsShown.add(kind) : flagsShown.delete(kind);
      syncFlags();
      updateMarkers();
    });
    const icon = el("svg", { width: 18, height: 18, viewBox: "0 -27 26 26", "aria-hidden": "true" });
    icon.append(flagNode(kind));
    const text = document.createElement("span");
    lab.append(box, icon, text);
    flagInner.append(lab);
    flagRows.set(kind, { lab, box, text });
  }
  legend.append(flagGroup);
  let flagsOpen = store.get("legendFlagsOpen", false) === true;
  function setFlagsOpen(open) {
    flagsOpen = open;
    flagGroup.classList.toggle("is-open", open);
    flagHead.setAttribute("aria-expanded", String(open));
    flagBody.inert = !open;
  }
  setFlagsOpen(flagsOpen);
  flagHead.addEventListener("click", () => {
    setFlagsOpen(!flagsOpen);
    store.set("legendFlagsOpen", flagsOpen);
    updateMarkers(); // the legend changed size: place names avoid it
  });
  flagBody.addEventListener("transitionend", (e) => { if (e.target === flagBody) updateMarkers(); });
  function updateLegendFlags() {
    const t = T(), n = { been: me.visited.size, trip: me.itinerary.length, wish: me.wishlist.size };
    for (const [kind, r] of flagRows) {
      r.lab.hidden = !n[kind];
      r.text.textContent = t[kind];
      // a list that empties drops its "off" switch, so the next place added to it shows its flag
      if (!n[kind] && !r.box.checked) {
        r.box.checked = true;
        flagsShown.add(kind);
      }
    }
    flagGroup.hidden = !n.been && !n.trip && !n.wish;
    flagHeadText.textContent = t.tabTravel;
    // the header swatch: the flags of the lists in use as a small bundle, fitted to the 18 px icon column
    const kinds = ["trip", "wish", "been"].filter((k) => n[k]);
    const step = Math.max(0, kinds.length - 1) * 4, w = 26 + step;
    flagSwatch.replaceChildren(...kinds.map((k, i) => {
      const back = (kinds.length - 1 - i) * 4; // the first list stands furthest back, up and to the right
      const g = el("g", { transform: `translate(${back} ${-back})` });
      g.append(flagNode(k));
      return g;
    }));
    flagSwatch.setAttribute("viewBox", `0 ${-27 - step} ${w} ${w}`);
  }

  // all language-dependent text outside the reading panel
  function applyLanguage() {
    const t = T();
    document.documentElement.lang = t.htmlLang;
    document.title = t.pageTitle;
    const str = (v) => (typeof v === "function" ? v(countryShort(), countryLabel(), OPEN.length > 1) : v); // a few strings name the open country (short form, full name)
    for (const n of document.querySelectorAll("[data-i18n]")) n.textContent = str(t[n.dataset.i18n]);
    for (const n of document.querySelectorAll("[data-i18n-placeholder]")) n.placeholder = t[n.dataset.i18nPlaceholder];
    for (const n of document.querySelectorAll("[data-i18n-aria]")) n.setAttribute("aria-label", str(t[n.dataset.i18nAria]));
    for (const n of document.querySelectorAll("[data-i18n-title]")) n.title = str(t[n.dataset.i18nTitle]);
    document.body.classList.toggle("lang-zh", zh());
    // dialogs get their real titles when they open; until then they carry generic ones, so no heading or button is empty
    applyJournalI18n();
    document.getElementById("trip-title").textContent = t.tripDialogGeneric;
    document.getElementById("j-title").textContent = t.jDialogGeneric;
    document.getElementById("ask-yes").textContent = t.yes;
    document.getElementById("ask-no").textContent = t.cancel;
    updateLegendFlags();
    if (basemap) basemap.setLanguage(zh());
    regionLayoutDone = false; // names changed length: place them again
    for (const [id, g] of markerNodes) {
      const name = placeName(places.get(id));
      g.querySelector(".marker-label").textContent = name;
      g.setAttribute("aria-label", name);
    }
    for (const [type, { lab, text }] of legendItems) {
      text.textContent = t.types[type].label;
      lab.title = t.types[type].hint;
    }
    buildSearchIndex();
    renderFocusChip();
  }
  document.getElementById("lang-toggle").addEventListener("click", () => {
    lang = zh() ? "en" : "zh";
    store.set("lang", lang);
    applyLanguage();
    renderCrumbs();
    applyView();
    rerender();
  });

  // ---------- view transform ----------
  const view = { k: 1, x: 0, y: 0 };
  // zoom levels that mean "the whole country", "a region", "a place" were tuned on the UK (about 10° across); for a
  // wider country they come that much earlier. zc is the zoom as if the current country were UK-sized.
  const UK_WIDTH = 10.4;
  const MARKERS_FROM = 4.4; // country-relative zoom from which a country's markers show (the UK about 320 px wide)
  const farCountries = new Map(); // country code -> its markers are hidden for now
  const farNameCountries = new Map(); // country code -> its region names are hidden for now
  // switched off in the legend (display), or its country still too small on screen (is-far; a search hit shows anyway)
  const markerOff = (g) => g.style.display === "none" || (g.classList.contains("is-far") && !g.classList.contains("is-hit"));
  function zCountry(z) { const b = cur().bounds; return z + Math.log2((b[2] - b[0]) / UK_WIDTH); }
  function applyView() {
    root.setAttribute("transform", `translate(${view.x},${view.y}) scale(${view.k})`);
    // zooming in, the painted regions turn into a thin wash so the streets underneath show through
    const z = Math.log2((view.k * W) / 512), zc = zCountry(z);
    // with street tiles: the SVG washes hand over to the basemap's (which follow the real coast)
    const tiles = !!(basemap && basemap.hasTiles());
    const landO = !tiles || z <= 5.8 ? 1 : Math.max(0, 1 - (z - 5.8) / 1.4);
    svg.style.setProperty("--land-o", landO.toFixed(3));
    svg.classList.toggle("is-detail", z >= 6.6);
    svg.classList.toggle("is-tiles", tiles && z >= 6.6);
    if (basemap) { const [bw, bh] = size(); basemap.sync(view, bw, bh); }
    for (const t of regionLabels.values()) {
      t.style.fontSize = (11.5 * (Number(t.dataset.scale) || 1)) / view.k + "px"; // small uppercase serif, as on a vintage map
      t.style.strokeWidth = 3 / view.k + "px"; // the halo must not grow with the map
    }
    // region names give way to place names once zoomed into a region
    const zoomedIn = state.region != null || view.k > 60;
    gLabels.style.display = zoomedIn || zc < 4 ? "none" : ""; // no region names at world scale
    // Markers come on country by country, each once its own country is large enough to hold them (a small country
    // seen from a wide one's view would be a pile of markers); on the world page the countries are the way in.
    let allFar = true;
    for (const { cfg } of mounted.values()) {
      const far = state.world || z + Math.log2((cfg.bounds[2] - cfg.bounds[0]) / UK_WIDTH) < MARKERS_FROM;
      if (!far) allFar = false;
      const farNames = z + Math.log2((cfg.bounds[2] - cfg.bounds[0]) / UK_WIDTH) < 4; // region names likewise, a little earlier
      if (farNameCountries.get(cfg.code) !== farNames) {
        farNameCountries.set(cfg.code, farNames);
        for (const [id, t] of regionLabels) if (regionCountry.get(id) === cfg.code) t.classList.toggle("is-far", farNames);
      }
      if (farCountries.get(cfg.code) === far) continue;
      farCountries.set(cfg.code, far);
      for (const [id, g] of markerNodes) if (places.get(id).country === cfg.code) g.classList.toggle("is-far", far);
    }
    gMarkers.style.display = allFar && !searchHitIds ? "none" : "";
    svg.classList.toggle("is-worldscale", allFar); // search hits stay on (CSS hides the rest)
    spreadMarkers(zoomedIn);
    placeLabels(zoomedIn);
    placeUnitLabels(z);
    if (gLabels.style.display !== "none") scheduleRegionLayout();
    scheduleBlockers();
  }

  // Markers closer than NEAR px on screen (e.g. Baker Street and the Sherlock Holmes Museum, ~100 m apart)
  // are fanned out on a small circle so each one can be clicked. Only small clusters, and only when
  // zoomed into a region: at UK scale London is one dense knot and the region click is the way in.
  const NEAR = 16;
  function spreadMarkers(zoomedIn) {
    const s = 1 / view.k;
    const nodes = [...markerNodes.values()].filter((g) => !markerOff(g));
    for (const g of markerNodes.values()) { g.dataset.dx = 0; g.dataset.dy = 0; }
    if (zoomedIn) {
      const pos = nodes.map((g) => [view.x + view.k * Number(g.dataset.x), view.y + view.k * Number(g.dataset.y)]);
      const parent = nodes.map((_, i) => i);
      const find = (i) => (parent[i] === i ? i : (parent[i] = find(parent[i])));
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          if (Math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]) < NEAR) parent[find(i)] = find(j);
        }
      }
      const groups = new Map();
      nodes.forEach((_, i) => { const r = find(i); if (!groups.has(r)) groups.set(r, []); groups.get(r).push(i); });
      for (const members of groups.values()) {
        if (members.length < 2 || members.length > 4) continue;
        const cx = members.reduce((a, i) => a + pos[i][0], 0) / members.length;
        const cy = members.reduce((a, i) => a + pos[i][1], 0) / members.length;
        const radius = 9 + 2 * members.length;
        // keep each marker on the side it already lies on, so the fan-out reads as a nudge
        const start = Math.atan2(pos[members[0]][1] - cy, pos[members[0]][0] - cx);
        members.forEach((i, n) => {
          const a = start + (n * 2 * Math.PI) / members.length;
          nodes[i].dataset.dx = cx + radius * Math.cos(a) - pos[i][0];
          nodes[i].dataset.dy = cy + radius * Math.sin(a) - pos[i][1];
        });
      }
    }
    for (const g of markerNodes.values()) {
      g.setAttribute("transform", `translate(${g.dataset.x},${g.dataset.y}) scale(${s}) translate(${g.dataset.dx},${g.dataset.dy})`);
    }
  }

  // greedy label placement in screen space: the active place first, then places with
  // more excerpts; a label that would overlap one already placed is hidden
  function placeLabels(zoomedIn) {
    const placed = [];
    markerLabelBoxes = placed;
    // every visible marker (after the fan-out) is an obstacle for the names of the others
    const dots = [...markerNodes.values()].filter((g) => !markerOff(g)).map((g) => {
      const x = view.x + view.k * Number(g.dataset.x) + Number(g.dataset.dx || 0);
      const y = view.y + view.k * Number(g.dataset.y) + Number(g.dataset.dy || 0);
      return { g, box: [x - 7, y - 7, x + 7, y + 7] };
    });
    markerDotBoxes = dots.map((d) => d.box);
    // a flag is two obstacles: the cloth with the knob, and the thin staff below it (a name may sit beside the staff)
    const flags = dots.filter((d) => d.g.classList.contains("has-flag")).flatMap((d) => {
      const x = d.box[0] + 7, y = d.box[1] + 7;
      return [[x + 2, y - 27, x + 24, y - 14], [x + 2, y - 14, x + 5, y - 1]];
    });
    markerDotBoxes.push(...flags);
    const order = [...markerNodes.values()].sort((a, b) => score(b) - score(a));
    const chrome = chromeBoxes(); // title block (with breadcrumbs), legend, buttons, compass, credits
    const charW = zh() ? 13 : 7.2;
    for (const g of order) {
      const label = g.querySelector(".marker-label");
      const visible = !markerOff(g);
      const faded = searchHitIds && !g.classList.contains("is-hit"); // while searching, only results are named
      const named = zoomedIn || g.classList.contains("is-active") || g.classList.contains("is-focus") || g.classList.contains("is-pointed") || (mapFocus && mapFocus.has(g.dataset.id));
      if (!visible || faded || !named) { label.style.display = "none"; continue; }
      const sx = view.x + view.k * Number(g.dataset.x) + Number(g.dataset.dx || 0);
      const sy = view.y + view.k * Number(g.dataset.y) + Number(g.dataset.dy || 0);
      const w = label.textContent.length * charW + 4;
      // a name may not cover another name or another place's marker: try right, left, above, below
      const spots = {
        right: { box: [sx + 8, sy - 10, sx + 12 + w, sy + 8], x: 10, y: 4, anchor: "start" },
        left: { box: [sx - 12 - w, sy - 10, sx - 8, sy + 8], x: -10, y: 4, anchor: "end" },
        above: { box: [sx - w / 2, sy - 26, sx + w / 2, sy - 8], x: 0, y: -12, anchor: "middle" },
        below: { box: [sx - w / 2, sy + 8, sx + w / 2, sy + 26], x: 0, y: 21, anchor: "middle" },
      };
      const free = (box) => !placed.some((b) => hit(box, b)) && !dots.some((d) => d.g !== g && hit(box, d.box)) && !chrome.some((c) => hit(box, c)) && !flags.some((f) => hit(box, f));
      let side = Object.keys(spots).find((k) => free(spots[k].box)) || null;
      // the selected or pointed place always keeps its name (it is placed first, so no other name is in the way):
      // if no side is free, use the one that covers the fewest markers and flags (its own flag included)
      if (!side && (g.classList.contains("is-active") || g.classList.contains("is-pointed") || g.classList.contains("is-focus"))) {
        const cost = (k) => dots.filter((d) => d.g !== g && hit(spots[k].box, d.box)).length + flags.filter((f) => hit(spots[k].box, f)).length;
        side = Object.keys(spots).reduce((a, k) => (cost(k) < cost(a) ? k : a), "right");
      }
      label.style.display = side ? "" : "none";
      g.dataset.side = side || "";
      if (!side) continue;
      label.setAttribute("x", spots[side].x);
      label.setAttribute("y", spots[side].y);
      label.setAttribute("text-anchor", spots[side].anchor);
      placed.push(spots[side].box);
    }
  }
  const hit = (a, b) => a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1];
  function score(g) {
    if (g.classList.contains("is-pointed")) return 3e6;
    if (g.classList.contains("is-focus")) return 2e6;
    if (g.classList.contains("is-active")) return 1e6;
    if (g.classList.contains("is-hit")) return 5e5 + (linesByPlace.get(g.dataset.id) || []).length;
    return (linesByPlace.get(g.dataset.id) || []).length * 10 + (places.get(g.dataset.id).city ? 5 : 0);
  }
  function size() { const r = svg.getBoundingClientRect(); return [r.width, r.height]; }
  // the reading panel covers the right side of the map; keep fitted content clear of it
  function panelOffset() {
    if (window.innerWidth <= 900 || document.body.classList.contains("intro-running") || !panelOpen) return 0;
    return reader.offsetWidth;
  }
  function boundsView(lonMin, latMin, lonMax, latMax, pad) {
    const [x0, y1] = project(lonMin, latMin);
    const [x1, y0] = project(lonMax, latMax);
    const [w0, hgt] = size();
    const w = w0 - panelOffset();
    const P = typeof pad === "number" ? { t: pad, r: pad, b: pad, l: pad } : pad; // a number, or insets per side
    const iw = w - P.l - P.r, ih = hgt - P.t - P.b;
    const k = Math.min(iw / (x1 - x0), ih / (y1 - y0));
    return { k, x: P.l + iw / 2 - k * (x0 + x1) / 2, y: P.t + ih / 2 - k * (y0 + y1) / 2 };
  }
  // room for the map furniture when fitting a set of places: title block (with the focus chip) at the
  // top left, legend at the bottom left, zoom buttons at the bottom right
  function chromeInsets() {
    const svgR = svg.getBoundingClientRect(), hgt = svgR.height;
    const tb = document.querySelector(".titleblock").getBoundingClientRect();
    const lg = document.querySelector(".legend").getBoundingClientRect();
    let t = Math.max(60, tb.bottom - svgR.top + 36), b = Math.max(40, lg.height ? svgR.bottom - lg.top + 24 : 40);
    if (t + b > hgt * 0.6) { const f = (hgt * 0.6) / (t + b); t *= f; b *= f; } // small windows: keep the map usable
    return { t, b, l: 50, r: 90 };
  }
  function fitBounds(lonMin, latMin, lonMax, latMax, pad, animate, dur) {
    tween(boundsView(lonMin, latMin, lonMax, latMax, pad), animate, dur);
  }
  let raf = null;
  function tween(target, animate, dur) {
    cancelAnimationFrame(raf);
    if (!animate || reduceMotion) { Object.assign(view, target); applyView(); return; }
    const from = { ...view }, t0 = performance.now();
    dur = dur || 650;
    // interpolate zoom on a log scale and the centre linearly, so the motion feels even
    const step = (now) => {
      const t = Math.min(1, (now - t0) / dur), e = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      const k = Math.exp(Math.log(from.k) + (Math.log(target.k) - Math.log(from.k)) * e);
      const [w, hgt] = size();
      const cFrom = [(w / 2 - from.x) / from.k, (hgt / 2 - from.y) / from.k];
      const cTo = [(w / 2 - target.x) / target.k, (hgt / 2 - target.y) / target.k];
      const cx = cFrom[0] + (cTo[0] - cFrom[0]) * e, cy = cFrom[1] + (cTo[1] - cFrom[1]) * e;
      view.k = k; view.x = w / 2 - k * cx; view.y = hgt / 2 - k * cy;
      applyView();
      if (t < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
  }
  function zoomBy(f, cx, cy) {
    const [w, hgt] = size();
    cx = cx == null ? w / 2 : cx; cy = cy == null ? hgt / 2 : cy;
    const k = Math.max(1.5, Math.min(60000, view.k * f));
    const r = k / view.k;
    view.x = cx - (cx - view.x) * r;
    view.y = cy - (cy - view.y) * r;
    view.k = k;
    if (coverOn) setCover(false);
    // zoomed in by hand on the world page: once the country at the middle of the view is large enough, it is the
    // country being looked at (its own width decides, not the last country visited)
    const [vw, vh] = size(), [clon, clat] = unproject((vw / 2 - view.x) / k, (vh / 2 - view.y) / k);
    // the country whose box holds the middle of the view, or failing that the nearest one within half a view
    const reach = (vw / k / W) * 180, off = (c) => Math.max(c.bounds[0] - clon, clon - c.bounds[2], c.bounds[1] - clat, clat - c.bounds[3], 0);
    const under = state.world && [...mounted.values()].map((m) => m.cfg).filter((c) => off(c) <= reach).sort((a, b) => off(a) - off(b))[0];
    if (under && Math.log2((k * W) / 512) + Math.log2((under.bounds[2] - under.bounds[0]) / UK_WIDTH) >= 4.6) {
      state.world = false;
      state.country = under.code;
      renderCrumbs();
      if (!routing) history.replaceState(null, "", "#/" + cur().code);
    }
    applyView();
  }
  function zoomCountry(cfg, animate, dur) { fitBounds(...cfg.bounds, 30, animate, dur); }
  const WORLD_BOUNDS = [-170, -58, 180, 78];
  function zoomRegion(rid, animate) {
    const b = regions.get(rid).bbox;
    fitBounds(b[0], b[1], b[2], b[3], 50, animate);
  }
  function zoomPlace(p, animate) {
    // London is dense: zoom closer there than elsewhere
    let d = SMALL.has(p.region) ? 0.09 : 0.5;
    // and closer still where a neighbour is very near, until it is about 60 px away so both names fit
    // (map-layers.md 3); never closer than about 300 m across
    const [px, py] = project(p.lon, p.lat);
    let near = Infinity;
    for (const q of places.values()) {
      if (q === p) continue;
      const [qx, qy] = project(q.lon, q.lat);
      near = Math.min(near, Math.hypot(qx - px, qy - py));
    }
    while (d > 0.004 && boundsView(p.lon - d, p.lat - d / 2, p.lon + d, p.lat + d / 2, 40).k * near < 60) d *= 0.75;
    fitBounds(p.lon - d, p.lat - d / 2, p.lon + d, p.lat + d / 2, 40, animate);
  }

  // drag + wheel
  let drag = null;
  svg.addEventListener("pointerdown", (e) => {
    if (e.button !== 0) return;
    drag = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y, moved: false };
    svg.setPointerCapture(e.pointerId);
  });
  svg.addEventListener("pointermove", (e) => {
    if (!drag) return;
    const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (!drag.moved && Math.hypot(dx, dy) < 4) return;
    drag.moved = true;
    if (coverOn) setCover(false);
    svg.classList.add("is-dragging");
    view.x = drag.vx + dx; view.y = drag.vy + dy;
    applyView();
  });
  svg.addEventListener("pointerup", (e) => {
    const wasDrag = drag && drag.moved;
    drag = null;
    svg.classList.remove("is-dragging");
    if (wasDrag) return;
    // a click: find what is under the pointer (pointer capture retargets the event to the svg)
    svg.releasePointerCapture(e.pointerId);
    handleMapClick(document.elementFromPoint(e.clientX, e.clientY));
  });
  svg.addEventListener("wheel", (e) => {
    e.preventDefault();
    if (Math.abs(e.deltaX) >= 2 * Math.abs(e.deltaY)) return; // a sideways swipe moves the panel, not the zoom
    const r = svg.getBoundingClientRect();
    zoomBy(Math.exp(-e.deltaY * 0.0015), e.clientX - r.left, e.clientY - r.top);
  }, { passive: false });
  document.getElementById("zoom-in").addEventListener("click", () => zoomBy(1.6));
  document.getElementById("zoom-out").addEventListener("click", () => zoomBy(1 / 1.6));
  document.getElementById("zoom-uk").addEventListener("click", () => { forget(); goCountry(cur().code, true); }); // like the country breadcrumb

  function countryName(node) { return zh() ? node.dataset.nameZh : node.dataset.name; }
  function handleMapClick(target) {
    if (!target) return;
    const marker = target.closest(".marker");
    // at world scale the country is a few pixels wide: any click on it opens the country, not one region
    if ((marker || target.closest(".region")) && zCountry(Math.log2((view.k * W) / 512)) < 4) {
      const rid = marker ? places.get(marker.dataset.id).region : target.closest(".region").dataset.id;
      return goCountry(regionCountry.get(rid), true);
    }
    if (marker && marker.dataset.id) { remember(); return openPlace(marker.dataset.id, true); }
    const region = target.closest(".region");
    if (region) { remember(); return openRegion(region.dataset.id, true); }
    if (target.classList.contains("country")) {
      const other = OPEN_BY_ISO.get(target.dataset.iso);
      if (other) { // an open country not yet on the map: load it, then go there
        showTip(T().countryOpening(countryName(target)), lastPointer);
        ensureCountry(other.code).then(() => { hideTip(); goCountry(other.code, true); }, () => showTip(T().countryFailed(countryName(target)), lastPointer));
        return;
      }
      showTip(T().countrySoon(countryName(target)), lastPointer);
    }
  }

  // hover tooltip
  let lastPointer = [0, 0];
  svg.addEventListener("mousemove", (e) => {
    const r = svg.getBoundingClientRect();
    lastPointer = [e.clientX - r.left, e.clientY - r.top];
    if (drag) return hideTip();
    const t = e.target;
    const marker = t.closest(".marker");
    const region = t.closest(".region");
    for (const g of regionNodes.values()) g.classList.toggle("is-hover", g === region && !marker);
    if (basemap) basemap.setHighlight(region && !marker ? region.dataset.id : null, state.region);
    if (marker && marker.dataset.id) {
      const p = places.get(marker.dataset.id);
      const n = (linesByPlace.get(p.id) || []).length;
      showTip((n ? T().tipWithCount(placeName(p), n) : T().tipWithType(placeName(p), typeLabel(p.place_type))) + (me.visited.has(p.id) ? T().tipBeen : "") + (me.itinerary.some((x) => x.place_id === p.id) ? T().tipTrip : "") + (me.wishlist.has(p.id) ? T().tipWish : ""), lastPointer);
    } else if (region) {
      const r0 = regions.get(region.dataset.id);
      showTip(zh() ? `${r0.name_zh} ${r0.name}` : r0.name, lastPointer);
    } else if (t.classList.contains("country")) {
      showTip(countryName(t) + (OPEN_BY_ISO.has(t.dataset.iso) ? "" : T().tipSoon), lastPointer);
    } else hideTip();
  });
  svg.addEventListener("mouseleave", hideTip);
  svg.addEventListener("keydown", (e) => {
    const m = e.target.closest && e.target.closest(".marker");
    if (m && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); remember(); openPlace(m.dataset.id, true); }
  });
  function showTip(text, [x, y]) {
    tooltip.textContent = text;
    tooltip.hidden = false;
    tooltip.style.left = x + 14 + "px";
    tooltip.style.top = y + 14 + "px";
  }
  function hideTip() { tooltip.hidden = true; }

  // ---------- app state ----------
  const state = { country: null, region: null, place: null, book: null, author: null, tab: "map", world: false };

  // ---------- world page, cover title and the sliding panel ----------
  // The home page is the whole world, full-bleed, with the title in the middle (the opening
  // animation's last frame). The panel stays tucked away until the reader asks for it: the tab on
  // the right edge, a two-finger swipe, or clicking the UK, a region, a marker or a search result.
  let panelOpen = false, coverOn = false;
  function setPanel(open) {
    if (panelOpen === open) return;
    panelOpen = open;
    document.body.classList.toggle("panel-closed", !open);
    document.getElementById("panel-open").setAttribute("aria-expanded", String(open));
    regionLayoutDone = false; // the free space for region names changed
    if (gLabels.style.display !== "none") scheduleRegionLayout();
  }
  function setCover(on) {
    coverOn = on;
    document.body.classList.toggle("is-cover", on);
  }
  function showMapTab() {
    if (state.tab === "map") return;
    state.tab = "map";
    for (const b of document.querySelectorAll(".tab")) b.classList.toggle("is-active", b.dataset.view === "map");
  }
  function goWorld(animate) {
    state.world = true;
    showMapTab();
    setPanel(false);
    setCover(true);
    select({ region: null, place: null });
    fitBounds(...WORLD_BOUNDS, 10, animate);
    renderIntro();
  }
  function goCountry(code, animate) {
    const cfg = COUNTRIES.find((c) => c.code === code) || cur();
    state.world = false;
    setCover(false);
    setPanel(true);
    showMapTab();
    select({ country: cfg.code, region: null, place: null });
    zoomCountry(cfg, animate);
    renderIntro();
  }
  // anything that opens content brings the panel out and ends the world page
  function leaveWorld() {
    state.world = false;
    setCover(false);
    setPanel(true);
  }
  function select(next) {
    Object.assign(state, { book: null, author: null }, next);
    // the country the view belongs to, for the breadcrumb and the ⤢ button
    if (state.region) state.country = regionCountry.get(state.region) || state.country;
    else if (state.place && places.get(state.place)) state.country = places.get(state.place).country || state.country;
    else if (state.book || state.author) { const ps = state.book ? bookPlaces(state.book) : authorPlaces(state.author); if (ps[0]) state.country = ps[0].country || state.country; }
    showAllPlaces = false; // every new book or author starts with only its own places on the map
    for (const [id, g] of regionNodes) g.classList.toggle("is-active", id === state.region);
    if (basemap) basemap.setHighlight(null, state.region);
    for (const [id, g] of markerNodes) g.classList.toggle("is-active", id === state.place);
    updateMarkers();
    renderCrumbs();
    applyView();
    syncRoute();
  }

  // ---------- URL routes (spec F5): #/region/TLI · #/place/baker-street · #/book/persuasion · #/travel · #/reading ----------
  const ROUTE_RE = /^#\/([a-z]{2}|region|place|book|author|travel|reading)(?:\/([\w-]+))?$/; // two letters = a country code
  function currentRoute() {
    if (state.tab === "travel") return "#/travel";
    if (state.tab === "reading") return "#/reading";
    if (state.book) return "#/book/" + state.book;
    if (state.author) return "#/author/" + state.author;
    if (state.place) return "#/place/" + state.place;
    if (state.region) return "#/region/" + state.region;
    return state.world ? "" : "#/" + cur().code; // "" is the world page
  }
  let routing = false, freshTrail = false;
  function syncRoute() {
    if (routing) return;
    const next = currentRoute();
    if ((location.hash || "") === next) { freshTrail = false; return; }
    // each history entry notes the view it was opened from, so the panel's back link can use the browser's Back
    // (or, after a breadcrumb, a tab or ⤢, that it starts a fresh trail)
    const from = freshTrail ? { fresh: true } : { from: location.hash || "" };
    freshTrail = false;
    if (next) history.pushState(from, "", next);
    else history.pushState(from, "", location.pathname + location.search);
  }
  const has = (kind, id) => (kind === "region" ? regions : kind === "place" ? places : kind === "book" ? books : authors).has(id);
  async function loadUntilFound(kind, id) {
    for (const c of OPEN) {
      if (mounted.has(c.code)) continue;
      try { await ensureCountry(c.code); } catch (e) { continue; }
      if (has(kind, id)) return true;
    }
    return has(kind, id);
  }
  function applyRoute(hash, animate) {
    const m = ROUTE_RE.exec(hash || "");
    routing = true;
    try {
      if (!m) { goWorld(animate); return true; }
      const [, kind, id] = m;
      if (kind.length === 2) { // a country
        const cfg = OPEN.find((c) => c.code === kind);
        if (!cfg) return false;
        if (mounted.has(kind)) goCountry(kind, animate);
        else ensureCountry(kind).then(() => goCountry(kind, animate), () => { routing = true; goWorld(animate); routing = false; });
      }
      else if (!["travel", "reading"].includes(kind) && !has(kind, id)) {
        // an id from a country not loaded yet: load the open countries until one has it, then come back here
        if (!OPEN.some((c) => !mounted.has(c.code))) return false;
        loadUntilFound(kind, id).then((found) => {
          if (found) applyRoute(hash, animate);
          else { history.replaceState(null, "", location.pathname + location.search); routing = true; goWorld(animate); routing = false; }
        });
      }
      else if (kind === "region" && regions.has(id)) openRegion(id, animate);
      else if (kind === "place" && places.has(id)) openPlace(id, animate);
      else if (kind === "book" && books.has(id)) openBook(id);
      else if (kind === "author" && authors.has(id)) openAuthor(id);
      else if (kind === "travel" || kind === "reading") setTab(kind);
      else return false;
      return true;
    } finally {
      routing = false;
    }
  }
  window.addEventListener("popstate", () => {
    // the browser's Back button and the panel's back link share one trail
    const top = trail[trail.length - 1];
    const back = top && top.route === (location.hash || "");
    if (back) trail.pop(); // before the view renders, so its back link already shows the step before
    // Forward (or a jump in the history list): the back link points to the view this entry was opened from
    const from = history.state && typeof history.state.from === "string" ? history.state.from : null;
    if (!back && from !== null && (!trail.length || trail[trail.length - 1].route !== from)) {
      trail.push({ route: from, scroll: 0 });
      if (trail.length > 30) trail.shift();
    }
    applyRoute(location.hash, true);
    if (back) { restoreScroll(top.scroll); rerender(); }
  });

  // ---------- back link (panel trail) ----------
  // every move to another view remembers the view being left; "‹ <name>" at the top of the panel returns
  // to it with its map focus and scroll position. Breadcrumbs and the top tabs start a fresh trail.
  const trail = [];
  function remember() {
    const route = currentRoute();
    const top = trail[trail.length - 1];
    if (top && top.route === route) { top.scroll = reader.scrollTop; return; }
    trail.push({ route, scroll: reader.scrollTop });
    if (trail.length > 30) trail.shift();
  }
  function forget() { trail.length = 0; freshTrail = true; }
  // clicking the view already on screen (its own marker, the region you are in) remembers that same view: drop it
  function prune() {
    const here = currentRoute();
    while (trail.length && trail[trail.length - 1].route === here) trail.pop();
  }
  function labelFor(route) {
    const t = T(), m = ROUTE_RE.exec(route || "");
    if (!m) return t.worldTitle;
    const [, kind, id] = m;
    if (kind === "travel") return t.tabTravel;
    if (kind === "reading") return t.tabReading;
    if (kind === "book" && books.has(id)) return bookTitle(books.get(id));
    if (kind === "author" && authors.has(id)) return authorName(authors.get(id));
    if (kind === "place" && places.has(id)) return placeName(places.get(id));
    if (kind === "region" && regions.has(id)) return regionName(regions.get(id));
    return countryLabel();
  }
  function restoreScroll(y) { requestAnimationFrame(() => requestAnimationFrame(() => { reader.scrollTop = y; })); }
  function goBack() {
    prune();
    const top = trail[trail.length - 1];
    if (!top) return;
    // the page we came from is the previous history entry: use the browser's Back, so both back buttons are one
    // (popstate below pops the trail and restores the view and scroll), and Forward keeps working
    if (history.state && history.state.from === top.route) return history.back();
    const x = trail.pop();
    if (!applyRoute(x.route, true)) return;
    if (state.tab !== "map" && !/^#\/(travel|reading)$/.test(x.route)) setTab("map");
    syncRoute();
    rerender();
    restoreScroll(x.scroll);
  }
  function backLink() {
    prune();
    const top = trail[trail.length - 1];
    if (!top) return null;
    const b = document.createElement("button");
    b.className = "back-link";
    b.dataset.back = "1";
    b.innerHTML = `<span aria-hidden="true">‹</span> ${esc(labelFor(top.route))}`;
    b.setAttribute("aria-label", T().backTo(labelFor(top.route)));
    return b;
  }
  // with a book or an author open, the map shows only its places (all four kinds); the chip can show all.
  // A search in progress overrides this so its results can be seen wherever they are (map-layers 3.3, 3.4)
  let showAllPlaces = false, mapFocus = null;
  function focusIds() {
    if (showAllPlaces || searchHitIds) return null;
    if (state.book) return new Set(bookPlaces(state.book).map((p) => p.id));
    if (state.author) return new Set(authorPlaces(state.author).map((p) => p.id));
    return null;
  }
  function updateMarkers() {
    mapFocus = focusIds();
    for (const [id, g] of markerNodes) {
      const p = places.get(id);
      g.style.display = filters.has(p.place_type) && (!mapFocus || mapFocus.has(id)) ? "" : "none";
    }
    renderFocusChip();
    const zoomedIn = state.region != null || view.k > 60;
    spreadMarkers(zoomedIn);
    placeLabels(zoomedIn);
    placeUnitLabels(Math.log2((view.k * W) / 512));
    scheduleBlockers();
  }
  // the region the map is showing: the selected one, or, on a book page, the one region all its places share
  function titleRegion() {
    if (state.region) return state.region;
    if (!state.book && !state.author) return null;
    const rs = new Set((state.book ? bookPlaces(state.book) : authorPlaces(state.author)).map((p) => p.region));
    return rs.size === 1 ? [...rs][0] : null;
  }
  function renderCrumbs() {
    const t = T();
    // on the world page the title already says "The World": the line under it describes the atlas
    // instead of repeating it (as on cartogram.earth); breadcrumbs start once you zoom in
    const parts = state.world ? [`<span class="crumb-sub">${t.worldSub}</span>`] : [`<button data-go="world">${t.crumbWorld}</button>`, `<button data-go="uk">${esc(countryLabel())}</button>`];
    if (state.region) parts.push(`<button data-go="region">${esc(regionName(regions.get(state.region)))}</button>`);
    if (state.place) parts.push(`<span>${esc(placeName(places.get(state.place)))}</span>`);
    if (state.book) parts.push(`<span>${esc(bookTitle(books.get(state.book)))}</span>`);
    if (state.author) parts.push(`<span>${esc(authorName(authors.get(state.author)))}</span>`);
    crumbs.innerHTML = parts.join('<span class="sep">›</span>');
    // the map title names the area on screen, like an atlas plate
    mapTitle.textContent = state.world ? t.worldTitle : titleRegion() ? regionName(regions.get(titleRegion())) : countryLabel();
  }
  crumbs.addEventListener("click", (e) => {
    const go = e.target.dataset && e.target.dataset.go;
    if (go) forget();
    if (go === "world") goWorld(true);
    if (go === "uk") goCountry(cur().code, true);
    if (go === "region") openRegion(state.region, true);
  });

  // ---------- reading panel ----------
  function setTab(tab) {
    state.tab = tab;
    if (tab !== "map") setPanel(true);
    for (const b of document.querySelectorAll(".tab")) b.classList.toggle("is-active", b.dataset.view === tab);
    rerender();
    syncRoute();
  }
  function rerender() {
    if (state.tab === "travel") renderTravel();
    else if (state.tab === "reading") renderReading();
    else if (state.book) renderBook(state.book);
    else if (state.author) renderAuthor(state.author);
    else if (state.place) renderPlace(state.place);
    else if (state.region) renderRegion(state.region);
    else renderIntro();
  }
  document.querySelector(".tabs").addEventListener("click", (e) => {
    const b = e.target.closest(".tab");
    if (b) { forget(); setTab(b.dataset.view); }
  });

  function show(fragment, keepScroll) {
    const top = reader.scrollTop;
    reader.replaceChildren(fragment);
    if (window.RA_SHELF) RA_SHELF.fit(reader);
    if (window.RA_BOOKOPEN) RA_BOOKOPEN.hideSpine(reader);
    const back = backLink();
    if (back) reader.prepend(back);
    reader.scrollTop = keepScroll ? top : 0;
  }
  function uniqueLineCount(ps) {
    return new Set(ps.flatMap((p) => (linesByPlace.get(p.id) || []).map((l) => l.id))).size;
  }

  // which nation each ITL1 region belongs to (eyebrow on the region cards)
  // the kicker above a region's name: the country's own grouping if its config has one (England / Wales / …)
  function regionKicker(r) {
    const cfg = COUNTRIES.find((c) => c.code === regionCountry.get(r.id));
    const g = cfg && cfg.groups && cfg.groups[r.id];
    return g ? (T().nations[g] || g) : "";
  }
  function renderIntro() {
    const t = T();
    const shelf = Object.values(me.shelf);
    show(h(`
      <div class="intro">
        <h2>${t.introTitle}</h2>
        <p class="sub">${(() => { const m = mounted.get(cur().code); return m ? t.introSub(countryShort(), m.data.books.length, m.data.lines.length, m.data.places.length) : ""; })()}</p>
        <div class="play-cards">
          <button class="feature-card" data-tab="travel">
            <span class="fc-eyebrow">${t.cardTravelEyebrow}</span>
            <span class="fc-title">${t.tabTravel}</span>
            <span class="fc-sub">${t.cardTravelSub(me.visited.size, me.itinerary.length)}</span>
          </button>
          <button class="feature-card is-blue" data-tab="reading">
            <span class="fc-eyebrow">${t.cardBooksEyebrow}</span>
            <span class="fc-title">${t.tabReading}</span>
            <span class="fc-sub">${t.cardBooksSub(shelf.filter((v) => v === "read").length, shelf.filter((v) => v === "want").length, me.faves.size)}</span>
          </button>
        </div>
        <div class="card">
          <p class="eyebrow">${t.gettingStarted}</p>
          ${t.introSteps.map((s, i) => `<p class="hint${i === t.introSteps.length - 1 ? " dim" : ""}">${esc(s)}</p>`).join("")}
        </div>
        <h3>${t.introRegions(mounted.size > 1 ? 0 : regions.size)}</h3>
        ${[...mounted.values()].sort((a, b) => (b.cfg.code === cur().code) - (a.cfg.code === cur().code)).map(({ cfg, geo }) => `${mounted.size > 1 ? `<h4 class="story-country">${esc(countryLabel(cfg))}</h4>` : ""}
        <ul class="story-list">${geo.regions.map((r) => {
          const ps = [...places.values()].filter((p) => p.region === r.id);
          return `<li><button class="story-link" data-region="${r.id}"><span class="sl-kicker">${esc(regionKicker(r))}</span><span class="sl-title">${esc(regionName(r))}</span><span class="sl-meta">${t.placesAndExcerpts(ps.length, uniqueLineCount(ps))}</span></button></li>`;
        }).join("")}</ul>`).join("")}
      </div>`));
  }

  function openRegion(rid, animate) {
    leaveWorld();
    if (!rid) return;
    select({ region: rid, place: null });
    zoomRegion(rid, animate);
    if (state.tab !== "map") setTab("map"); else renderRegion(rid);
  }
  function renderRegion(rid) {
    const t = T();
    const r = regions.get(rid);
    const ps = [...places.values()].filter((p) => p.region === rid);
    const groups = TYPE_KEYS.map((type) => {
      const items = ps.filter((p) => p.place_type === type);
      if (!items.length) return "";
      return `<h3>${typeLabel(type)}</h3><ul class="place-list">${items.map(placeRow).join("")}</ul>`;
    }).join("");
    show(h(`
      <h2>${esc(regionName(r))}</h2>
      <p class="sub">${t.regionSub(esc(r.name), ps.length, uniqueLineCount(ps))}</p>
      ${groups || `<p class="empty-note">${t.regionEmpty}</p>`}`));
  }
  function placeRow(p) {
    const n = (linesByPlace.get(p.id) || []).length;
    const right = n ? T().excerpts(n) : p.place_type === "film_location" ? esc(p.adaptation.title) : "";
    return `<li><button data-place="${p.id}">${typeIcon(p.place_type)}<span>${esc(placeName(p))}</span><span class="count">${right}</span></button></li>`;
  }
  function typeIcon(type) {
    const tmp = el("svg", { width: 16, height: 16, viewBox: "-9 -9 18 18", class: "marker t-" + type, "aria-hidden": "true" });
    tmp.append(shape(type));
    return tmp.outerHTML;
  }

  function openPlace(pid, animate) {
    leaveWorld();
    const p = places.get(pid);
    select({ region: p.region, place: pid });
    zoomPlace(p, animate);
    if (state.tab !== "map") setTab("map"); else renderPlace(pid);
  }
  function renderPlace(pid, keepScroll) {
    const t = T();
    const p = places.get(pid);
    const r = regions.get(p.region);
    const lines = linesByPlace.get(pid) || [];
    const linked = (p.book_ids || []).map((id) => books.get(id)).filter(Boolean);
    const placeTrips = me.itinerary.map((x, i) => ({ ...x, i })).filter((x) => x.place_id === pid).sort((a, b) => a.date.localeCompare(b.date));
    let context = "";
    const stop = zh() ? "。" : ".";
    if (p.place_type === "prototype") context = `<p>${esc(zh() ? p.prototype_of : p.prototype_of_en)}${stop}</p>`;
    if (p.place_type === "pilgrimage" || (p.place_type === "original" && p.note_en)) context = `<p>${esc(zh() ? p.note : p.note_en)}${stop}</p>`;
    if (p.place_type === "film_location") {
      const a = p.adaptation;
      context = `<p>${esc(t.filmContext(t.adaptationKind[a.kind] || a.kind, a.title, a.year, zh() ? p.scene : p.scene_en))}</p>`;
    }
    // a place shared by many writers (Poets' Corner) lists the writers; other places list the books
    const writers = (p.authors || []).map((n) => authors.get(slug(n))).filter(Boolean);
    const related = writers.length ? `<h3>${t.relatedWriters}</h3><ul class="place-list">${writers.map(authorRow).join("")}</ul>`
      : linked.length ? `<h3>${t.relatedBooks}</h3><ul class="place-list">${linked.map(bookRow).join("")}</ul>` : "";
    const quotes = lines.length
      ? `<h3>${t.linesHere}</h3>${lines.map((l) => quoteHTML(l, "book")).join("")}`
      : (p.place_type === "film_location" || p.place_type === "pilgrimage") ? "" : `<p class="empty-note">${t.noLines}</p>`;
    show(h(`
      <div class="type-badge">${typeIcon(p.place_type)}${typeLabel(p.place_type)}</div>
      <h2>${esc(placeName(p))}</h2>
      <p class="sub">${zh() ? `${esc(p.name)}，` : ""}${esc(r ? regionName(r) : "")}</p>
      ${context}
      ${photoHTML(p)}
      <div class="actions">
        <button class="btn ${me.wishlist.has(pid) ? "is-on" : ""}" data-toggle="wishlist" data-id="${pid}">${me.wishlist.has(pid) ? t.saved : t.save}</button>
        <button class="btn ${placeTrips.length ? "is-on" : ""}" data-trip="${pid}">${placeTrips.length ? t.tripPlanned : t.addTrip}</button>
        <button class="btn ${me.visited.has(pid) ? "is-on" : ""}" data-toggle="visited" data-id="${pid}">${me.visited.has(pid) ? t.visited : t.visit}</button>
      </div>
      ${tripsHere(placeTrips)}
      ${journalSection(pid)}
      ${quotes}
      ${related}`), keepScroll);
    hydratePhotos(reader);
  }
  // a freely licensed photo after the place's introduction; the credit line is a licence requirement
  function photoHTML(p) {
    const ph = p.photo;
    if (!ph) return "";
    const alt = zh() ? ph.alt_zh : ph.alt_en;
    return `<figure class="place-photo">
        <img src="${esc(ph.file)}" alt="${esc(alt)}" width="${ph.width}" height="${ph.height}" decoding="async">
        <figcaption>${T().photoCredit} <a href="${esc(ph.source)}" target="_blank" rel="noopener">${esc(ph.author)}</a> · <a href="${esc(ph.license_url)}" target="_blank" rel="noopener">${esc(ph.license)}</a>${ph.cropped ? ` · ${T().photoCropped}` : ""}</figcaption>
      </figure>`;
  }
  function authorRow(a) {
    return `<li><button data-author="${a.id}"><span>${esc(authorName(a))}</span><span class="count">${T().bookCount(a.books.length)}</span></button></li>`;
  }
  function bookRow(b) {
    const n = (linesByBook.get(b.id) || []).length;
    return `<li><button data-book="${b.id}"><span>${esc(bookLabel(b))}</span><span class="count">${n ? T().excerpts(n) : T().excerptsToCome}</span></button></li>`;
  }

  function highlight(text, terms) {
    let out = esc(text);
    for (const t of (terms || []).filter(Boolean).sort((a, b) => b.length - a.length)) {
      const e = esc(t).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      out = out.replace(new RegExp(e, "g"), "<mark>$&</mark>");
    }
    return out;
  }
  function quoteHTML(l, citeMode) {
    const t = T();
    const b = books.get(l.book_id);
    const hasOrig = l.text_orig && b.orig_lang !== "en";
    const sep = zh() ? "，" : ", ";
    const citeTarget = citeMode === "book"
      ? `<button data-book="${b.id}">${esc(bookTitle(b))}</button>${sep}${esc(bookAuthor(b))}${sep}${esc(b.year)}`
      : l.place_ids.map((id) => `<button data-place="${id}">${esc(placeName(places.get(id)))}</button>`).join(zh() ? "、" : ", ");
    const note = l.translation !== "own" ? ""
      : l.status === "reviewed" ? `<span class="draft is-done" title="${esc(t.ownTranslationDoneLong)}">${t.ownTranslationDone}</span>`
      : `<span class="draft" title="${esc(t.ownTranslationLong)}">${t.ownTranslation}</span>`;
    // a scene note (kind: "scene") is our own summary of a book still in copyright: shown in the page's
    // language, in plain upright type so it never reads as a quotation, and with no tag on the page
    const scene = l.kind === "scene";
    const body = scene
      ? `<blockquote class="is-scene" lang="${zh() ? "zh" : "en"}">${highlight(zh() ? l.text_zh : l.text_en, zh() ? l.highlight_zh : l.highlight_en)}</blockquote>`
      : `<blockquote lang="en">${highlight(l.text_en, l.highlight_en)}</blockquote>`;
    return `
      <figure class="quote" data-line="${l.id}">
        ${body}
        <figcaption class="cite">${citeTarget}${sep}${esc(lineLocation(l))}${note}</figcaption>
        ${hasOrig ? `<button class="orig-toggle" data-orig="${l.id}">${t.showOriginal(langName(b.orig_lang))}</button>` : ""}
      </figure>`;
  }
  let shelfPage = 0; // which page of the favourites shelf is showing
  reader.addEventListener("click", (e) => {
    const bk = e.target.closest("[data-shelf-book]");
    if (bk) return pullBook(bk);
    const t = e.target.closest("button");
    if (!t) return;
    if (t.dataset.shelfPage) { shelfPage += Number(t.dataset.shelfPage); return refresh(); }
    if (t.dataset.back) return goBack();
    if (t.dataset.tab || t.dataset.region || t.dataset.place || t.dataset.book || t.dataset.author) remember();
    if (t.dataset.tab) return setTab(t.dataset.tab);
    if (t.dataset.region) return openRegion(t.dataset.region, true);
    if (t.dataset.place) return openPlace(t.dataset.place, true);
    if (t.dataset.book) return openBook(t.dataset.book);
    if (t.dataset.author) return openAuthor(t.dataset.author);
    if (t.dataset.orig) return toggleOriginal(t);
    if (t.dataset.toggle) {
      const set = me[t.dataset.toggle];
      const n = t.dataset.toggle === "visited" && set.has(t.dataset.id) ? J.count(t.dataset.id) : 0;
      if (n) {
        const id = t.dataset.id;
        ask(T().jUnvisitAsk(n), T().jUnvisitYes).then((yes) => { if (yes) { set.delete(id); RS.save(); syncFlags(); updateMarkers(); refresh(); } });
        return;
      }
      const added = !set.has(t.dataset.id);
      added ? set.add(t.dataset.id) : set.delete(t.dataset.id);
      RS.save();
      syncFlags(added ? t.dataset.id : null);
      updateMarkers();
      return refresh();
    }
    if (t.dataset.fave) {
      if (me.faves.has(t.dataset.fave)) me.faves.delete(t.dataset.fave); else me.faves.add(t.dataset.fave);
      RS.save();
      return refresh();
    }
    if (t.dataset.shelf) {
      const cur = me.shelf[t.dataset.id];
      if (cur === t.dataset.shelf) delete me.shelf[t.dataset.id]; else me.shelf[t.dataset.id] = t.dataset.shelf;
      RS.save();
      return refresh();
    }
    if (t.dataset.trip) return openTripDialog(t.dataset.trip);
    if (t.dataset.removeTrip != null) {
      me.itinerary.splice(Number(t.dataset.removeTrip), 1);
      RS.save();
      syncFlags();
      updateMarkers();
      return refresh();
    }
  });
  // after toggling a button, redraw the same view without jumping to the top
  function refresh() {
    if (state.tab === "travel") renderTravel(true);
    else if (state.tab === "reading") renderReading();
    else if (state.book) renderBook(state.book, true);
    else if (state.author) renderAuthor(state.author, true);
    else if (state.place) renderPlace(state.place, true);
  }
  function toggleOriginal(btn) {
    const t = T();
    const l = allLines.find((x) => x.id === btn.dataset.orig);
    const b = books.get(l.book_id);
    const q = btn.closest(".quote").querySelector("blockquote");
    if (q.getAttribute("lang") !== "en") {
      q.setAttribute("lang", "en");
      q.innerHTML = highlight(l.text_en, l.highlight_en);
      btn.textContent = t.showOriginal(langName(b.orig_lang));
    } else {
      q.setAttribute("lang", b.orig_lang);
      q.innerHTML = highlight(l.text_orig, l.highlight_orig);
      btn.textContent = t.showEnglish;
    }
  }

  function bookPlaces(bid) {
    const ids = new Set((linesByBook.get(bid) || []).flatMap((l) => l.place_ids));
    for (const p of places.values()) if ((p.book_ids || []).includes(bid)) ids.add(p.id);
    return [...ids].map((id) => places.get(id));
  }
  function authorPlaces(aid) {
    const seen = new Map();
    for (const b of authors.get(aid).books) for (const p of bookPlaces(b.id)) seen.set(p.id, p);
    for (const p of places.values()) if ((p.authors || []).some((n) => slug(n) === aid)) seen.set(p.id, p);
    return [...seen.values()];
  }
  function openAuthor(aid) {
    leaveWorld();
    select({ region: null, place: null, author: aid });
    fitPlaces(authorPlaces(aid));
    showMapTab();
    syncRoute();
    renderAuthor(aid);
  }
  function renderAuthor(aid, keepScroll) {
    const t = T();
    const a = authors.get(aid);
    const ps = authorPlaces(aid);
    show(h(`
      <h2>${esc(authorName(a))}</h2>
      <p class="sub">${zh() ? `${esc(a.name)}，` : ""}${t.authorSub(a.books.length, ps.length)}</p>
      <h3>${t.authorBooks}</h3>
      <ul class="place-list">${a.books.map(bookRow).join("")}</ul>
      ${ps.length ? `<h3>${t.placesOnMap}</h3><ul class="place-list">${ps.map(placeRow).join("")}</ul>` : ""}`), keepScroll);
  }
  function openBook(bid) {
    leaveWorld();
    select({ region: null, place: null, book: bid });
    fitPlaces(bookPlaces(bid));
    showMapTab();
    syncRoute();   // select() ran while My books was still the tab, so the address still says #/reading
    renderBook(bid);
  }
  function fitPlaces(ps) {
    if (ps.length) {
      const lons = ps.map((p) => p.lon), lats = ps.map((p) => p.lat);
      // never zoom in further than about a city's width
      const cx = (Math.min(...lons) + Math.max(...lons)) / 2, cy = (Math.min(...lats) + Math.max(...lats)) / 2;
      const dx = Math.max(0.35, (Math.max(...lons) - Math.min(...lons)) / 2 + 0.15);
      const dy = Math.max(0.18, (Math.max(...lats) - Math.min(...lats)) / 2 + 0.08);
      fitBounds(cx - dx, cy - dy, cx + dx, cy + dy, chromeInsets(), true);
    }
  }
  function renderBook(bid, keepScroll) {
    const t = T();
    const b = books.get(bid);
    const lines = linesByBook.get(bid) || [];
    const uniq = bookPlaces(bid);
    const shelf = me.shelf[bid];
    const src = b.source_url ? `<a href="${esc(b.source_url)}" target="_blank" rel="noopener">${t.findText}</a>` : t.noText;
    const who = `<button class="author-link" data-author="${slug(b.author)}">${esc(bookAuthor(b))}</button>`;
    const sub = zh() ? `${esc(b.title)}，${who}，${esc(b.year)}` : `${who}, ${esc(b.year)}`;
    show(h(`
      <h2>${esc(bookTitle(b))}</h2>
      <p class="sub">${sub}</p>
      <p>${src}</p>
      <div class="actions">
        <button class="btn ${shelf === "want" ? "is-on" : ""}" data-shelf="want" data-id="${bid}">${t.want}</button>
        <button class="btn ${shelf === "read" ? "is-on" : ""}" data-shelf="read" data-id="${bid}">${t.read}</button>
        <button class="btn ${me.faves.has(bid) ? "is-on" : ""}" data-fave="${bid}">${me.faves.has(bid) ? t.faved : t.fave}</button>
      </div>
      ${uniq.length ? `<h3>${t.placesOnMap}</h3><ul class="place-list">${uniq.map(placeRow).join("")}</ul>` : ""}
      ${lines.length ? `<h3>${t.bookExcerpts}</h3>${lines.map((l) => quoteHTML(l, "place")).join("")}` : `<p class="empty-note">${t.bookEmpty}</p>`}
      <h3>${t.myNotes}</h3>
      <label class="visually-hidden" for="note-${bid}">${t.notesLabel}</label>
      <textarea class="note-box" id="note-${bid}" data-note="${bid}" placeholder="${esc(t.notesPlaceholder)}">${esc(me.notes[bid] || "")}</textarea>`), keepScroll);
  }
  reader.addEventListener("input", (e) => {
    const id = e.target.dataset && e.target.dataset.note;
    if (!id) return;
    me.notes[id] = e.target.value;
    if (!e.target.value) delete me.notes[id];
    RS.save();
  });

  function renderTravel(keepScroll) {
    const t = T();
    const visited = [...me.visited].map((id) => places.get(id)).filter(Boolean);
    const trips = me.itinerary.map((x, i) => ({ ...x, i })).sort((a, b) => a.date.localeCompare(b.date));
    const wish = [...me.wishlist].map((id) => places.get(id)).filter(Boolean);
    show(h(`
      <h2>${t.travelTitle}</h2>
      <p class="sub">${t.storedLocal}</p>
      <div class="stat-row">
        <div><strong>${visited.length}</strong>${t.statVisited}</div>
        ${[...mounted.values()].map(({ cfg, geo }) => `<div><strong>${new Set(visited.filter((p) => p.country === cfg.code).map((p) => p.region)).size}/${geo.regions.length}</strong>${t.statRegions(countryShort(cfg), zh() ? cfg.region_term.zh : cfg.region_term.en)}</div>`).join("")}
        <div><strong>${trips.length}</strong>${t.statStops}</div>
      </div>
      <h3>${t.trip}</h3>
      <p class="list-sub">${t.tripSub}</p>
      ${trips.length ? `<ul class="trip-list">${trips.map((x) => {
        const p = places.get(x.place_id);
        return `<li><time datetime="${esc(x.date)}">${esc(x.date)}</time><span><button class="link-btn" data-place="${p.id}">${esc(placeName(p))}</button>${x.note ? `<br><span class="empty-note">${esc(x.note)}</span>` : ""}</span><button class="remove" data-remove-trip="${x.i}">${t.remove}</button></li>`;
      }).join("")}</ul>` : `<p class="empty-note">${t.tripEmpty}</p>`}
      <h3>${t.wish}</h3>
      <p class="list-sub">${t.wishSub}</p>
      ${wish.length ? `<ul class="place-list">${wish.map(placeRow).join("")}</ul>` : `<p class="empty-note">${t.wishEmpty}</p>`}
      <h3>${t.been}</h3>
      ${visited.length ? `<ul class="place-list">${visited.map(beenRow).join("")}</ul>` : `<p class="empty-note">${t.beenEmpty}</p>`}
      ${diarySection()}
      <section class="data-tools">
        <h3>${t.dataTitle}</h3>
        <p class="list-sub">${t.dataSub}</p>
        <div class="actions">
          <button class="btn" data-export-data>${t.dataExport}</button>
          <label class="btn file-btn"><input type="file" accept="application/json,.json" data-import-data>${t.dataImport}</label>
        </div>
        <p class="empty-note" id="data-msg" role="status" aria-live="polite"></p>
      </section>`), keepScroll);
    hydratePhotos(reader);
  }
  // R-7: personal data in and out as one JSON file (the shape the cloud backend will sync)
  function exportData() {
    const data = RS.exportData();
    const blob = new Blob([JSON.stringify(data, null, 1)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `readers-atlas-${data.exported_at.slice(0, 10)}.json`;
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }
  async function importDataFile(file) {
    const t = T(), msg = document.getElementById("data-msg");
    try {
      const n = RS.importData(JSON.parse(await file.text()));
      refresh();
      const m = document.getElementById("data-msg"); if (m) m.textContent = t.dataImported(n);
    } catch (e) {
      if (msg) msg.textContent = t.dataImportBad;
    }
  }
  reader.addEventListener("change", (e) => {
    const inp = e.target.closest("[data-import-data]");
    if (inp && inp.files[0]) { importDataFile(inp.files[0]); inp.value = ""; }
  });
  // a place I've been, with its diary cover and entry count
  function beenRow(p) {
    const list = J.forPlace(p.id), cover = list.find((e) => e.photos.length)?.photos[0];
    const right = list.length ? T().jEntries(list.length) : "";
    return `<li><button data-place="${p.id}" class="${cover ? "has-cover" : ""}">${typeIcon(p.place_type)}<span>${esc(placeName(p))}</span>${cover ? `<img class="row-cover" alt="" data-photo="${cover.id}" data-size="thumb">` : ""}<span class="count">${right}</span></button></li>`;
  }
  // a favourite pulled off the shelf opens as a two-page spread (js/bookopen.js)
  function spreadPages(bid) {
    const t = T(), b = books.get(bid), shelf = me.shelf[bid], ps = bookPlaces(bid), n = (linesByBook.get(bid) || []).length;
    const src = b.source_url ? `<a href="${esc(b.source_url)}" target="_blank" rel="noopener">${t.findText}</a>` : t.noText;
    const left = `
      <h2>${esc(bookTitle(b))}</h2>
      ${zh() ? `<p class="ob-orig">${esc(b.title)}</p>` : ""}
      <p class="ob-by"><button class="author-link" data-author="${slug(b.author)}">${esc(bookAuthor(b))}</button>, ${esc(b.year)}</p>
      <div class="actions">
        <button class="btn ${shelf === "want" ? "is-on" : ""}" data-shelf="want" data-id="${bid}">${t.want}</button>
        <button class="btn ${shelf === "read" ? "is-on" : ""}" data-shelf="read" data-id="${bid}">${t.read}</button>
        <button class="btn ${me.faves.has(bid) ? "is-on" : ""}" data-fave="${bid}">${me.faves.has(bid) ? t.faved : t.fave}</button>
      </div>
      <p class="ob-count">${t.obCount(n, ps.length)}</p>
      <p class="ob-src">${src}</p>
      <button class="ghost ob-full" data-ob-full="${bid}">${t.obFull} ›</button>
      ${epigraph(bid)}`;
    const right = `
      <h3>${t.placesOnMap}</h3>
      ${ps.length ? `<ul class="place-list">${ps.map(placeRow).join("")}</ul>` : `<p class="empty-note">${t.obNoPlaces}</p>`}
      <h3>${t.myNotes}</h3>
      <label class="visually-hidden" for="ob-note-${bid}">${t.notesLabel}</label>
      <textarea class="note-box" id="ob-note-${bid}" data-note="${bid}" placeholder="${esc(t.notesPlaceholder)}">${esc(me.notes[bid] || "")}</textarea>`;
    return [left, right];
  }
  // the foot of the left page: the book's first excerpt, cut short, like an epigraph (a scene note stays upright: it is our own words)
  function epigraph(bid) {
    const ls = linesByBook.get(bid) || [];
    const l = ls.find((x) => x.kind !== "scene") || ls[0];
    if (!l) return "";
    const scene = l.kind === "scene", text = scene && zh() ? l.text_zh : l.text_en;
    const max = scene && zh() ? 70 : 170;
    let cut = text.length > max ? text.slice(0, max) : text;
    if (cut.length < text.length) cut = (zh() ? cut : cut.replace(/\s+\S*$/, "")).replace(/[\s,;:.，。；：、]+$/, "") + "…";
    return `<figure class="ob-epigraph${scene ? " is-scene" : ""}"><blockquote lang="${scene && zh() ? "zh" : "en"}">${esc(cut)}</blockquote><figcaption>${esc(lineLocation(l))}</figcaption></figure>`;
  }
  function pullBook(g) {
    if (!window.RA_BOOKOPEN || RA_BOOKOPEN.isOpen()) return;
    const bid = g.dataset.shelfBook, b = books.get(bid), t = T();
    const [left, right] = spreadPages(bid);
    RA_BOOKOPEN.open(g, {
      id: bid, left, right,
      cover: { title: zh() ? b.title_zh : b.title, author: bookAuthor(b) },
      labels: { close: t.obClose, soundOn: t.obSoundOn, soundOff: t.obSoundOff },
      onClick(e, api) {
        const btn = e.target.closest("button");
        if (!btn) return;
        // leaving for another view: put the book down quickly, then go
        const go = btn.dataset.place ? () => openPlace(btn.dataset.place, true) : btn.dataset.author ? () => openAuthor(btn.dataset.author)
          : btn.dataset.obFull ? () => openBook(btn.dataset.obFull) : null;
        if (go) { api.close(true).then(() => { remember(); go(); }); return; }
        if (btn.dataset.fave) { if (me.faves.has(bid)) me.faves.delete(bid); else me.faves.add(bid); }
        else if (btn.dataset.shelf) { if (me.shelf[bid] === btn.dataset.shelf) delete me.shelf[bid]; else me.shelf[bid] = btn.dataset.shelf; }
        else return;
        RS.save();
        api.update(...spreadPages(bid));
        refresh();
      },
      onInput(e) {
        const id = e.target.dataset && e.target.dataset.note;
        if (!id) return;
        me.notes[id] = e.target.value;
        if (!e.target.value) delete me.notes[id];
        RS.save();
      },
      onClose() { if (state.tab === "reading") refresh(); },
    });
  }
  reader.addEventListener("keydown", (e) => {
    const bk = e.target.closest && e.target.closest("[data-shelf-book]");
    if (bk && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); pullBook(bk); }
  });
  // the favourites bookshelf (js/shelf.js); newest favourite first
  function shelfHTML(faves) {
    const items = faves.map((b) => ({ id: b.id, title: zh() ? b.title_zh : b.title, author: b.author }));
    const r = RA_SHELF.html(items, shelfPage);
    shelfPage = r.page;
    const pager = r.pages > 1 ? `<div class="shelf-pager">
        <button class="shelf-pg" data-shelf-page="-1" ${r.page === 0 ? "disabled" : ""} aria-label="${T().shelfPrev}">‹</button>
        <span>${r.page + 1} / ${r.pages}</span>
        <button class="shelf-pg" data-shelf-page="1" ${r.page === r.pages - 1 ? "disabled" : ""} aria-label="${T().shelfNext}">›</button>
      </div>` : "";
    return `<div class="shelf-wrap">${r.svg}${pager}</div>`;
  }
  function renderReading() {
    const t = T();
    const list = (kind) => Object.entries(me.shelf).filter(([, v]) => v === kind).map(([id]) => books.get(id)).filter(Boolean);
    const read = list("read"), want = list("want");
    const faves = [...me.faves].map((id) => books.get(id)).filter(Boolean);
    const noted = Object.keys(me.notes).map((id) => books.get(id)).filter(Boolean);
    show(h(`
      <h2>${t.readingTitle}</h2>
      <p class="sub">${t.storedLocal}</p>
      <h3>${t.faveN(faves.length)}</h3>
      ${shelfHTML(faves)}${faves.length ? "" : `<p class="empty-note shelf-empty-note">${t.faveEmpty}</p>`}
      <h3>${t.readN(read.length)}</h3>
      ${read.length ? `<ul class="place-list">${read.map(bookRow).join("")}</ul>` : `<p class="empty-note">${t.readEmpty}</p>`}
      <h3>${t.wantN(want.length)}</h3>
      ${want.length ? `<ul class="place-list">${want.map(bookRow).join("")}</ul>` : `<p class="empty-note">${t.wantEmpty}</p>`}
      <h3>${t.notedN(noted.length)}</h3>
      ${noted.length ? `<ul class="place-list">${noted.map(bookRow).join("")}</ul>` : `<p class="empty-note">${t.notedEmpty}</p>`}`));
  }

  // ---------- itinerary dialog ----------
  const dialog = document.getElementById("trip-dialog");
  const form = document.getElementById("trip-form");
  let tripPlace = null;
  function openTripDialog(pid) {
    tripPlace = pid;
    document.getElementById("trip-title").textContent = T().tripDialogTitle(placeName(places.get(pid)));
    form.reset();
    const now = new Date(), pad = (n) => String(n).padStart(2, "0");
    form.date.value = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`; // today on the user's own clock, not UTC
    dialog.showModal();
  }
  dialog.addEventListener("close", () => {
    if (dialog.returnValue !== "ok" || !tripPlace) return;
    me.itinerary.push({ place_id: tripPlace, date: form.date.value, note: form.note.value.trim() });
    RS.save();
    syncFlags(tripPlace);
    updateMarkers();
    tripPlace = null;
    refresh(); // the place page shows the new trip under its buttons
  });

  // ---------- travel journal (docs/travel-journal-spec.md; storage in js/journal-store.js) ----------
  const J = window.RA_JOURNAL;
  const jDialog = document.getElementById("journal-dialog");
  const jForm = document.getElementById("journal-form");
  const askDialog = document.getElementById("ask-dialog");
  const lightbox = document.getElementById("lightbox");
  const jOpen = new Set(); // entry ids shown in full
  let jState = null;        // the entry being edited: { id, place_id, photos: [...], dirty }
  let diaryFilter = { year: "", region: "" };

  // visit_date: "" (not recorded), "YYYY", "YYYY-MM" or "YYYY-MM-DD"
  function fmtVisit(d) {
    if (!d) return T().jNoDate;
    const [y, m, day] = d.split("-").map(Number);
    if (!m) return zh() ? `${y} 年` : String(y);
    if (zh()) return day ? `${y} 年 ${m} 月 ${day} 日` : `${y} 年 ${m} 月`;
    const mon = new Date(Date.UTC(y, m - 1, day || 1)).toLocaleDateString("en-GB", { month: "long", timeZone: "UTC" });
    return day ? `${day} ${mon} ${y}` : `${mon} ${y}`;
  }
  function jBooksFor(pid) {
    const p = places.get(pid);
    const ids = new Set([...(linesByPlace.get(pid) || []).map((l) => l.book_id), ...(p.book_ids || [])]);
    for (const id of Object.keys(me.shelf)) ids.add(id);
    for (const id of me.faves) ids.add(id);
    return [...ids].map((id) => books.get(id)).filter(Boolean);
  }
  // one diary entry card; `withPlace` adds the place name (diary list)
  function journalCard(e, withPlace) {
    const t = T(), p = places.get(e.place_id), open = jOpen.has(e.id);
    const cover = e.photos[0];
    const bookChips = e.book_ids.map((id) => books.get(id)).filter(Boolean)
      .map((b) => `<button class="j-book" data-book="${b.id}">${esc(bookTitle(b))}</button>`).join("");
    const photos = open && e.photos.length
      ? `<div class="j-photos">${e.photos.map((ph, i) => `<button class="j-thumb" data-photo-entry="${e.id}" data-photo-i="${i}" aria-label="${esc(ph.caption || t.jPhotoN(i + 1))}"><img alt="${esc(ph.caption)}" data-photo="${ph.id}" data-size="thumb"></button>`).join("")}</div>` : "";
    return `<article class="j-card ${open ? "is-open" : ""}" data-entry="${e.id}">
      ${withPlace && p ? `<button class="j-place" data-place="${p.id}">${typeIcon(p.place_type)}<span>${esc(placeName(p))}</span><span class="j-region">${esc(regionName(regions.get(p.region)))}</span></button>` : ""}
      <button class="j-head" data-journal-open="${e.id}" aria-expanded="${open}">
        ${cover && !open ? `<img class="j-cover" alt="" data-photo="${cover.id}" data-size="thumb">` : ""}
        <span class="j-date">${esc(fmtVisit(e.visit_date))}${e.photos.length ? ` · ${t.jPhotos(e.photos.length)}` : ""}</span>
        ${e.text ? `<span class="j-text">${esc(e.text)}</span>` : ""}
      </button>
      ${photos}
      ${bookChips ? `<div class="j-books"><span>${t.jBooksShort}</span>${bookChips}</div>` : ""}
      ${open ? `<div class="j-tools"><button class="link-btn" data-journal-edit="${e.id}">${t.jEdit}</button><button class="link-btn danger" data-journal-del="${e.id}">${t.jDelete}</button></div>` : ""}
    </article>`;
  }
  // the trips planned for this place, under the buttons, each with its own Remove (same as in My travels)
  function tripsHere(list) {
    if (!list.length) return "";
    const t = T();
    return `<ul class="trip-list place-trips">${list.map((x) => `<li><time datetime="${esc(x.date)}">${esc(x.date)}</time><span>${t.tripHere}${x.note ? `<br><span class="empty-note">${esc(x.note)}</span>` : ""}</span><button class="remove" data-remove-trip="${x.i}">${t.remove}</button></li>`).join("")}</ul>`;
  }
  function journalSection(pid) {
    const t = T(), list = J.forPlace(pid), been = me.visited.has(pid);
    if (!been && !list.length) return "";
    return `<section class="j-section">
      <h3>${t.jTitle}</h3>
      ${list.length ? list.map((e) => journalCard(e, false)).join("") : `<p class="list-sub">${t.jEmptyPlace}</p>`}
      ${been ? `<button class="btn j-new" data-journal-new="${pid}">${t.jWrite}</button>` : `<p class="list-sub">${t.jNotBeen}</p>`}
    </section>`;
  }
  function diarySection() {
    const t = T(), all = J.all();
    if (!all.length) return `<h3>${t.jDiary}</h3><p class="list-sub">${t.jDiarySub}</p><p class="empty-note">${t.jDiaryEmpty}</p>`;
    const years = [...new Set(all.map((e) => e.visit_date.slice(0, 4)).filter(Boolean))].sort().reverse();
    const regs = [...new Set(all.map((e) => places.get(e.place_id)?.region).filter(Boolean))];
    const shown = all.filter((e) => (!diaryFilter.year || e.visit_date.startsWith(diaryFilter.year)) && (!diaryFilter.region || places.get(e.place_id)?.region === diaryFilter.region));
    const opt = (v, label, cur) => `<option value="${v}" ${v === cur ? "selected" : ""}>${esc(label)}</option>`;
    return `<h3 id="diary">${t.jDiary}</h3><p class="list-sub">${t.jDiarySub}</p>
      <div class="j-filters">
        <label><span class="sr-only">${t.jYear}</span><select data-diary="year">${opt("", t.jAllYears, diaryFilter.year)}${years.map((y) => opt(y, y, diaryFilter.year)).join("")}</select></label>
        <label><span class="sr-only">${t.jRegion}</span><select data-diary="region">${opt("", t.jAllRegions, diaryFilter.region)}${regs.map((r) => opt(r, regionName(regions.get(r)), diaryFilter.region)).join("")}</select></label>
      </div>
      ${shown.length ? shown.map((e) => journalCard(e, true)).join("") : `<p class="empty-note">${t.jNoMatch}</p>`}`;
  }
  // fill <img data-photo> once the blobs are read
  function hydratePhotos(root) {
    for (const img of root.querySelectorAll("img[data-photo]:not([src])")) {
      J.photoURL(img.dataset.photo, img.dataset.size || "thumb").then((u) => { if (u) img.src = u; else img.classList.add("is-missing"); }).catch(() => img.classList.add("is-missing"));
    }
  }

  // ----- editor -----
  const jEl = (id) => document.getElementById(id);
  function openJournal(pid, entryId) {
    const t = T(), e = entryId ? J.get(entryId) : null;
    jState = { id: e ? e.id : null, place_id: pid, photos: e ? e.photos.map((p) => ({ ...p })) : [], dirty: false, busy: 0 };
    jEl("j-title").textContent = t.jDialogTitle(placeName(places.get(pid)));
    const d = e ? e.visit_date : "";
    const mode = d.length === 4 ? "year" : d.length === 7 ? "month" : "day";
    jEl("j-date-mode").value = mode;
    setDateMode(mode, d);
    jEl("j-text").value = e ? e.text : "";
    const chosen = new Set(e ? e.book_ids : []);
    const bs = jBooksFor(pid);
    jEl("j-books").innerHTML = bs.length
      ? bs.map((b) => `<label class="j-check"><input type="checkbox" value="${b.id}" ${chosen.has(b.id) ? "checked" : ""}><span>${esc(bookTitle(b))}</span></label>`).join("")
      : `<p class="list-sub">${t.jNoBooks}</p>`;
    jEl("j-error").textContent = "";
    jEl("j-discard").hidden = true;
    renderDraftPhotos();
    applyJournalI18n();
    jDialog.showModal();
    jEl("j-text").focus();
  }
  // the date is optional; switching precision keeps whatever part of it was already filled in
  function setDateMode(mode, value) {
    const inp = jEl("j-date");
    const v = value != null ? value : inp.value;
    const y = v.slice(0, 4), ym = v.slice(0, 7);
    if (mode === "year") {
      inp.type = "number"; inp.min = "1900"; inp.max = String(new Date().getFullYear() + 1); inp.step = "1";
      inp.placeholder = T().jYearPlaceholder; inp.value = y;
    } else {
      inp.removeAttribute("min"); inp.removeAttribute("max"); inp.removeAttribute("step"); inp.placeholder = "";
      inp.type = mode === "month" ? "month" : "date";
      inp.value = mode === "month" ? (ym.length === 7 ? ym : "") : (v.length === 10 ? v : "");
    }
  }
  function renderDraftPhotos() {
    const t = T(), list = jEl("j-photo-list");
    list.innerHTML = jState.photos.map((p, i) => `<li class="j-draft">
      <img alt="" ${p.preview ? `src="${p.preview}"` : `data-photo="${p.id}" data-size="thumb"`}>
      <div class="j-draft-body">
        ${i === 0 ? `<span class="j-cover-tag">${t.jCover}</span>` : ""}
        <input type="text" maxlength="200" data-caption="${i}" value="${esc(p.caption)}" placeholder="${esc(t.jCaption)}" aria-label="${esc(t.jCaption)}">
        <div class="j-draft-tools">
          <button type="button" data-move="${i}" data-dir="-1" ${i === 0 ? "disabled" : ""} aria-label="${esc(t.jMoveUp)}">↑</button>
          <button type="button" data-move="${i}" data-dir="1" ${i === jState.photos.length - 1 ? "disabled" : ""} aria-label="${esc(t.jMoveDown)}">↓</button>
          <button type="button" data-drop="${i}" class="danger">${t.jRemovePhoto}</button>
        </div>
      </div></li>`).join("") + (jState.busy ? `<li class="j-busy">${t.jProcessing(jState.busy)}</li>` : "");
    hydratePhotos(list);
  }
  async function addFiles(files) {
    const t = T(), imgs = [...files].filter((f) => f.type.startsWith("image/") || /\.(heic|heif)$/i.test(f.name));
    const room = 20 - jState.photos.length;
    if (imgs.length > room) jEl("j-error").textContent = t.jTooMany;
    const take = imgs.slice(0, Math.max(0, room));
    if (imgs.length <= room) jEl("j-error").textContent = "";
    jState.busy += take.length;
    renderDraftPhotos();
    const failed = [];
    for (const f of take) {
      try { jState.photos.push(await J.preparePhoto(f)); jState.dirty = true; }
      catch (err) { failed.push(f.name); }
      jState.busy--;
      renderDraftPhotos();
    }
    if (failed.length) jEl("j-error").textContent = t.jBadPhoto(failed.join(", "));
  }
  function applyJournalI18n() {
    const t = T();
    for (const [id, key] of [["j-l-date", "jDate"], ["j-l-mode", "jDateMode"], ["j-o-day", "jExactDate"], ["j-o-month", "jMonthOnly"], ["j-o-year", "jYearOnly"], ["j-l-text", "jText"], ["j-l-photos", "jAddPhotos"], ["j-l-books", "jBooks"], ["j-drop-hint", "jDropHint"], ["j-cancel", "cancel"], ["j-save", "jSave"], ["j-discard-msg", "jDiscardMsg"], ["j-discard-yes", "jDiscardYes"], ["j-discard-no", "jDiscardNo"]]) jEl(id).textContent = t[key];
    jEl("j-text").placeholder = t.jTextPlaceholder;
  }
  function closeJournal(force) {
    if (!force && jState && jState.dirty) { jEl("j-discard").hidden = false; jEl("j-discard-no").focus(); return; }
    for (const p of jState ? jState.photos : []) if (p.preview) URL.revokeObjectURL(p.preview);
    jState = null;
    jDialog.close();
  }
  jForm.addEventListener("input", (e) => {
    if (!jState) return;
    jState.dirty = true;
    if (e.target.id === "j-text" || e.target.id === "j-date") jEl("j-error").textContent = "";
    if (e.target.dataset.caption != null) jState.photos[Number(e.target.dataset.caption)].caption = e.target.value;
  });
  jEl("j-date-mode").addEventListener("change", (e) => setDateMode(e.target.value));
  jEl("j-file").addEventListener("change", (e) => { addFiles(e.target.files); e.target.value = ""; });
  const drop = jEl("j-drop");
  drop.addEventListener("dragover", (e) => { e.preventDefault(); drop.classList.add("is-over"); });
  drop.addEventListener("dragleave", () => drop.classList.remove("is-over"));
  drop.addEventListener("drop", (e) => { e.preventDefault(); drop.classList.remove("is-over"); addFiles(e.dataTransfer.files); });
  jDialog.addEventListener("cancel", (e) => { e.preventDefault(); closeJournal(false); }); // Esc
  jForm.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b || !jState) return;
    if (b.dataset.move != null) {
      const i = Number(b.dataset.move), j = i + Number(b.dataset.dir);
      [jState.photos[i], jState.photos[j]] = [jState.photos[j], jState.photos[i]];
      jState.dirty = true; return renderDraftPhotos();
    }
    if (b.dataset.drop != null) {
      const [p] = jState.photos.splice(Number(b.dataset.drop), 1);
      if (p.preview) URL.revokeObjectURL(p.preview);
      jState.dirty = true; return renderDraftPhotos();
    }
    if (b.id === "j-cancel") return closeJournal(false);
    if (b.id === "j-discard-yes") return closeJournal(true);
    if (b.id === "j-discard-no") { jEl("j-discard").hidden = true; return; }
  });
  jForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const t = T();
    if (!jState || jState.busy) return;
    const text = jEl("j-text").value.trim();
    const date = jEl("j-date").value.trim();
    if (jEl("j-date-mode").value === "year" && date && !(/^\d{4}$/.test(date) && +date >= 1900 && +date <= new Date().getFullYear() + 1)) { jEl("j-error").textContent = t.jBadYear; return; }
    if (!text && !jState.photos.length) { jEl("j-error").textContent = t.jNeedSomething; return; }
    const book_ids = [...jEl("j-books").querySelectorAll("input:checked")].map((i) => i.value);
    jEl("j-save").disabled = true;
    try {
      const saved = await J.save({ id: jState.id, place_id: jState.place_id, visit_date: date, text, book_ids }, jState.photos);
      jOpen.add(saved.id);
      closeJournal(true);
      refresh();
    } catch (err) {
      jEl("j-error").textContent = err && err.message === "storage_full" ? t.jStorageFull : t.jSaveFailed;
    } finally { jEl("j-save").disabled = false; }
  });

  // ----- confirm (in-page, no browser dialogs) -----
  let askResolve = null;
  function ask(message, yesLabel) {
    const t = T();
    document.getElementById("ask-msg").textContent = message;
    document.getElementById("ask-yes").textContent = yesLabel;
    document.getElementById("ask-no").textContent = t.cancel;
    askDialog.showModal();
    return new Promise((r) => { askResolve = r; });
  }
  askDialog.addEventListener("close", () => { if (askResolve) askResolve(askDialog.returnValue === "yes"); askResolve = null; });

  // ----- photo viewer -----
  let lb = null; // { entry, i }
  function openLightbox(entryId, i) {
    const e = J.get(entryId);
    if (!e) return;
    lb = { e, i };
    showLightbox();
    lightbox.showModal();
  }
  function showLightbox() {
    const t = T(), ph = lb.e.photos[lb.i], img = document.getElementById("lb-img");
    img.removeAttribute("src");
    img.alt = ph.caption || t.jPhotoN(lb.i + 1);
    J.photoURL(ph.id, "full").then((u) => { if (u && lb && lb.e.photos[lb.i] === ph) img.src = u; });
    document.getElementById("lb-caption").textContent = ph.caption;
    document.getElementById("lb-count").textContent = `${lb.i + 1} / ${lb.e.photos.length}`;
    document.getElementById("lb-prev").disabled = lb.i === 0;
    document.getElementById("lb-next").disabled = lb.i === lb.e.photos.length - 1;
    document.getElementById("lb-prev").setAttribute("aria-label", t.jPrev);
    document.getElementById("lb-next").setAttribute("aria-label", t.jNext);
    document.getElementById("lb-close").setAttribute("aria-label", t.jClose);
  }
  function lbStep(d) {
    if (!lb) return;
    const j = lb.i + d;
    if (j < 0 || j >= lb.e.photos.length) return;
    lb.i = j; showLightbox();
  }
  lightbox.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (b && b.id === "lb-prev") return lbStep(-1);
    if (b && b.id === "lb-next") return lbStep(1);
    if ((b && b.id === "lb-close") || e.target === lightbox) lightbox.close();
  });
  lightbox.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") lbStep(-1);
    if (e.key === "ArrowRight") lbStep(1);
  });
  let swipeX = null;
  lightbox.addEventListener("pointerdown", (e) => { swipeX = e.clientX; });
  lightbox.addEventListener("pointerup", (e) => {
    if (swipeX == null) return;
    const dx = e.clientX - swipeX; swipeX = null;
    if (Math.abs(dx) > 50) lbStep(dx < 0 ? 1 : -1);
  });
  lightbox.addEventListener("close", () => { lb = null; });

  // ----- clicks and filters in the reading panel -----
  reader.addEventListener("click", async (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    const t = T();
    if (b.hasAttribute("data-export-data")) return exportData();
    if (b.dataset.journalNew) return openJournal(b.dataset.journalNew);
    if (b.dataset.journalOpen) {
      const id = b.dataset.journalOpen;
      jOpen.has(id) ? jOpen.delete(id) : jOpen.add(id);
      return refresh();
    }
    if (b.dataset.journalEdit) { const en = J.get(b.dataset.journalEdit); if (en) openJournal(en.place_id, en.id); return; }
    if (b.dataset.journalDel) {
      const en = J.get(b.dataset.journalDel);
      if (en && await ask(t.jDeleteAsk(en.visit_date ? fmtVisit(en.visit_date) : "", en.photos.length), t.jDelete)) { await J.remove(en.id); jOpen.delete(en.id); refresh(); }
      return;
    }
    if (b.dataset.photoEntry) return openLightbox(b.dataset.photoEntry, Number(b.dataset.photoI));
  });
  reader.addEventListener("change", (e) => {
    const k = e.target.dataset && e.target.dataset.diary;
    if (!k) return;
    diaryFilter[k] = e.target.value;
    refresh();
  });

  // ---------- the map follows the panel (docs/map-layers.md 3.4) ----------
  // a chip under the map title says what the map is limited to, with a switch to show everything
  const chip = document.getElementById("focus-chip");
  function renderFocusChip() {
    const t = T();
    const subject = state.book ? { kind: "book", name: bookTitle(books.get(state.book)), n: bookPlaces(state.book).length }
      : state.author ? { kind: "author", name: authorName(authors.get(state.author)), n: authorPlaces(state.author).length } : null;
    chip.hidden = !subject || !subject.n || state.world;
    if (chip.hidden) return;
    chip.innerHTML = showAllPlaces
      ? `<span>${esc(t.focusAll)}</span><button data-focus="only">${esc(subject.kind === "book" ? t.focusOnlyBook : t.focusOnlyAuthor)}</button>`
      : `<span>${esc(t.focusSome(subject.kind, subject.n, subject.name))}</span><button data-focus="all">${esc(t.focusShowAll)}</button>`;
  }
  chip.addEventListener("click", (e) => {
    const b = e.target.closest("button[data-focus]");
    if (!b) return;
    showAllPlaces = b.dataset.focus === "all";
    regionLayoutDone = false;
    updateMarkers();
    applyView();
  });
  // pointing at a place (or a book) in the panel rings its marker(s) on the map and names them
  let pointed = "";
  function pointAt(ids) {
    const key = ids.join();
    if (key === pointed) return;
    pointed = key;
    for (const [id, g] of markerNodes) {
      const on = ids.includes(id);
      g.classList.toggle("is-pointed", on);
      if (on) gMarkers.append(g); // on top of its neighbours
    }
    regionLayoutDone = false;
    applyView();
  }
  function pointedIds(target) {
    const b = target && target.closest && target.closest("#reader button[data-place], #reader button[data-book], #reader button[data-author]");
    if (!b) return [];
    if (b.dataset.place) return [b.dataset.place];
    if (b.dataset.book) return bookPlaces(b.dataset.book).map((p) => p.id);
    return authorPlaces(b.dataset.author).map((p) => p.id);
  }
  reader.addEventListener("mouseover", (e) => pointAt(pointedIds(e.target)));
  reader.addEventListener("mouseleave", () => pointAt([]));
  reader.addEventListener("focusin", (e) => pointAt(pointedIds(e.target)));
  reader.addEventListener("focusout", () => pointAt([]));
  reader.addEventListener("click", () => pointAt([])); // the view is about to change

  // ---------- search (matches both languages whichever is showing) ----------
  const input = document.getElementById("search-input");
  const results = document.getElementById("search-results");
  let index = [];
  function buildSearchIndex() {
    index = [
      ...[...authors.values()].map((a) => ({ kind: T().kindAuthor, id: a.id, author: true, label: authorName(a), hay: [a.name, a.name_zh, a.orig].join(" ").toLowerCase() })),
      ...[...books.values()].map((b) => ({ kind: T().kindBook, id: b.id, label: bookLabel(b), hay: [b.title, b.title_zh, b.title_orig, b.author, b.author_zh, b.author_orig, ...(b.aliases || [])].join(" ").toLowerCase() })),
      ...[...places.values()].map((p) => ({ kind: typeLabel(p.place_type), id: p.id, place: true, label: placeName(p), hay: [p.name, p.name_zh].join(" ").toLowerCase() })),
    ];
  }
  let hits = [], cursor = -1;
  function runSearch() {
    const q = input.value.trim().toLowerCase();
    if (!q) return hideResults();
    hits = index.filter((x) => x.hay.includes(q)).slice(0, 12);
    cursor = hits.length ? 0 : -1;
    drawHits(q);
    setSearchHighlight(hits, hits[cursor]);
  }
  input.addEventListener("input", runSearch);
  input.addEventListener("focus", () => { if (input.value.trim()) runSearch(); });
  function hideResults() {
    input.setAttribute("aria-expanded", "false"); input.removeAttribute("aria-activedescendant");
    results.hidden = true;
    setSearchHighlight(null);
  }
  // the map follows the list: every result's places are ringed, the one under the cursor pulses and is named
  function placesOf(x) { return x.place ? [x.id] : (x.author ? authorPlaces(x.id) : bookPlaces(x.id)).map((p) => p.id); }
  function setSearchHighlight(list, focus) {
    const next = list && list.length ? new Set(list.flatMap(placesOf)) : null;
    const nextFocus = next && focus ? new Set(placesOf(focus)) : null;
    const key = (s) => (s ? [...s].sort().join() : "");
    if (key(next) === key(searchHitIds) && key(nextFocus) === key(searchFocusIds)) return;
    searchHitIds = next;
    searchFocusIds = nextFocus;
    svg.classList.toggle("is-searching", !!next);
    for (const [id, g] of markerNodes) {
      g.classList.toggle("is-hit", !!next && next.has(id));
      g.classList.toggle("is-focus", !!nextFocus && nextFocus.has(id));
      if (nextFocus && nextFocus.has(id)) gMarkers.append(g); // draw on top of its neighbours
    }
    regionLayoutDone = false; // the focused name may now sit where a region name was
    updateMarkers(); // a search shows every marker; clearing it brings back the open book's focus
    applyView();
  }
  function drawHits(q) {
    results.hidden = false;
    input.setAttribute("aria-expanded", "true");
    results.innerHTML = hits.length
      ? hits.map((x, i) => `<li role="option" id="search-opt-${i}" aria-selected="${i === cursor}" data-i="${i}"><span>${esc(x.label)}</span><span class="kind">${esc(x.kind)}</span></li>`).join("")
      : `<li class="empty" role="option" aria-selected="false">${esc(T().searchEmpty(q))}</li>`;
    if (cursor >= 0 && hits.length) input.setAttribute("aria-activedescendant", `search-opt-${cursor}`); else input.removeAttribute("aria-activedescendant");
  }
  input.addEventListener("keydown", (e) => {
    if (results.hidden || !hits.length) return;
    if (e.key === "ArrowDown") { cursor = (cursor + 1) % hits.length; drawHits(input.value); setSearchHighlight(hits, hits[cursor]); e.preventDefault(); }
    if (e.key === "ArrowUp") { cursor = (cursor - 1 + hits.length) % hits.length; drawHits(input.value); setSearchHighlight(hits, hits[cursor]); e.preventDefault(); }
    if (e.key === "Enter" && cursor >= 0) { choose(hits[cursor]); e.preventDefault(); }
    if (e.key === "Escape") hideResults();
  });
  results.addEventListener("mouseover", (e) => {
    const li = e.target.closest("li[data-i]");
    if (!li || Number(li.dataset.i) === cursor) return;
    cursor = Number(li.dataset.i);
    for (const o of results.querySelectorAll("li[data-i]")) o.setAttribute("aria-selected", String(o === li));
    setSearchHighlight(hits, hits[cursor]);
  });
  results.addEventListener("mousedown", (e) => {
    const li = e.target.closest("li[data-i]");
    if (li) { e.preventDefault(); choose(hits[Number(li.dataset.i)]); }
  });
  input.addEventListener("blur", () => setTimeout(hideResults, 100));
  function choose(x) {
    hideResults();
    input.value = "";
    remember();
    if (x.place) openPlace(x.id, true); else if (x.author) openAuthor(x.id); else openBook(x.id);
  }

  // ---------- start ----------
  window.addEventListener("resize", () => {
    if (document.body.classList.contains("intro-running")) return;
    if (state.world) fitBounds(...WORLD_BOUNDS, 10, false);
    else if (!state.region && !state.place && !state.book) zoomCountry(cur(), false);
  });
  // panel controls: the tab on the right edge, the close button, and a two-finger sideways swipe
  document.getElementById("panel-open").addEventListener("click", () => setPanel(true));
  document.getElementById("panel-close").addEventListener("click", () => setPanel(false));
  let swipe = { sum: 0, t: 0, lock: 0 };
  document.querySelector(".layout").addEventListener("wheel", (e) => {
    if (Math.abs(e.deltaX) < 2 * Math.abs(e.deltaY) || window.innerWidth <= 900) return; // not sideways
    e.preventDefault(); // no browser back / forward on a sideways swipe over the atlas
    const now = performance.now();
    if (now < swipe.lock) return;
    if (now - swipe.t > 250) swipe.sum = 0;
    swipe.t = now;
    swipe.sum += e.deltaX;
    if (swipe.sum > 60 && !panelOpen) { setPanel(true); swipe = { sum: 0, t: now, lock: now + 700 }; }
    else if (swipe.sum < -60 && panelOpen) { setPanel(false); swipe = { sum: 0, t: now, lock: now + 700 }; }
  }, { passive: false });
  // ---------- countries: load on demand, mount once, keep ----------
  function mountCountry(cfg, geo, data) {
    if (mounted.has(cfg.code)) return;
    indexCountry(geo, data);
    assignRegions(data.places, geo);
    drawCountry(cfg, geo);
    const mask = buildRegionMask(geo);
    if (mask) masks.set(cfg.code, mask);
    addMarkers(data.places);
    farCountries.delete(cfg.code); farNameCountries.delete(cfg.code); // the next applyView decides for the new markers and names
    mounted.set(cfg.code, { cfg, geo, data });
    syncFlags();
    buildSearchIndex();
    regionLayoutDone = false;
    if (started) { updateMarkers(); applyView(); if (state.world || state.tab !== "map") renderIntroIfShown(); }
  }
  function ensureCountry(code) {
    if (mounted.has(code)) return Promise.resolve();
    const cfg = OPEN.find((c) => c.code === code);
    if (!cfg) return Promise.reject(new Error("no such country: " + code));
    return LOADER.load(cfg).then(({ geo, data }) => mountCountry(cfg, geo, data));
  }
  function renderIntroIfShown() { if (state.tab === "map" && !state.region && !state.place && !state.book && !state.author) renderIntro(); }
  // after the first country is on screen, fetch the other open ones quietly so that clicking them is instant
  function prefetchOthers() {
    const rest = OPEN.filter((c) => !mounted.has(c.code));
    (function next(i) { if (i < rest.length) ensureCountry(rest[i].code).catch(() => {}).then(() => next(i + 1)); })(0);
  }
  let started = false;
  function start() {
  started = true;
  syncFlags();
  applyLanguage();
  routing = true; // build the initial state without touching the URL a shared link may carry
  select({});
  renderIntro();
  routing = false;

  // The opening animation (js/intro.js) draws on its own canvas and hands over to this map.
  // It needs the same projection and the exact world view it will land on.
  const intro = window.RA_INTRO;
  if (intro && intro.shouldRun()) {
    document.body.classList.add("intro-running");
    gUK.style.opacity = "0";
    const worldView = boundsView(...WORLD_BOUNDS, 10);
    Object.assign(view, worldView);
    applyView();
    state.world = true;
    intro.run({
      project,
      worldView,
      t: () => T(),
      revealRegions() { gUK.style.transition = "opacity 600ms ease-out"; gUK.style.opacity = "1"; },
      // the animation ends on the world page: same view, same title in the same place. A refreshed or shared
      // link then flies on to its own view (11-06).
      finish() {
        gUK.style.opacity = "1";
        document.body.classList.remove("intro-running");
        routing = true;
        goWorld(false);
        routing = false;
        if (ROUTE_RE.test(location.hash)) {
          if (!applyRoute(location.hash, true)) history.replaceState(null, "", location.pathname + location.search);
        }
      },
    });
  } else if (!(ROUTE_RE.test(location.hash) && applyRoute(location.hash, false))) {
    if (location.hash) history.replaceState(null, "", location.pathname + location.search); // unknown link
    routing = true;
    goWorld(false);
    routing = false;
  }
  // no slide-in on first paint; transitions only answer the reader
  requestAnimationFrame(() => requestAnimationFrame(() => document.body.classList.remove("is-loading")));
  setTimeout(prefetchOthers, 1500);
  } // start()

  // the country the page opens on: the one in the URL, else the first open one; it loads before anything is shown,
  // the others follow in the background (see prefetchOthers)
  const startCode = (() => { const m = /^#\/([a-z]{2})(?:\/|$)/.exec(location.hash || ""); return (m && OPEN.some((c) => c.code === m[1])) ? m[1] : OPEN[0] && OPEN[0].code; })();
  if (!startCode) console.error("no open country in data/countries.js");
  else ensureCountry(startCode).then(start, (e) => { console.error(e); start(); });
})();
