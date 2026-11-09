/* The Reader's Atlas — front-end prototype (no backend, no third-party libraries).
   Data: window.RA_GEO (map), window.RA_DATA.{books, places, lines}, window.RA_I18N (interface text).
   Personal data (wishlist, visited, itinerary, booklist, notes, language) lives in localStorage. */
(function () {
  "use strict";

  const GEO = window.RA_GEO;
  const DATA = window.RA_DATA;
  const I18N = window.RA_I18N;
  const SVG_NS = "http://www.w3.org/2000/svg";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- lookups ----------
  const books = new Map(DATA.books.map((b) => [b.id, b]));
  const places = new Map(DATA.places.map((p) => [p.id, p]));
  const regions = new Map(GEO.regions.map((r) => [r.id, r]));
  const linesByPlace = new Map();
  const linesByBook = new Map();
  for (const l of DATA.lines) {
    for (const pid of l.place_ids) push(linesByPlace, pid, l);
    push(linesByBook, l.book_id, l);
  }
  function push(map, key, val) {
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(val);
  }
  const TYPE_KEYS = ["original", "prototype", "pilgrimage", "film_location"];
  const WASH = {
    TLC: "--wash-rose", TLD: "--wash-sage", TLE: "--wash-ochre", TLF: "--wash-aqua",
    TLG: "--wash-peach", TLH: "--wash-rose", TLI: "--wash-ochre", TLJ: "--wash-sage",
    TLK: "--wash-lilac", TLL: "--wash-ochre", TLM: "--wash-lilac", TLN: "--wash-aqua",
  };

  // ---------- storage ----------
  const store = {
    get(key, fallback) {
      try {
        const v = localStorage.getItem("ra." + key);
        return v ? JSON.parse(v) : fallback;
      } catch (e) { return fallback; }
    },
    set(key, val) {
      try { localStorage.setItem("ra." + key, JSON.stringify(val)); } catch (e) { /* storage unavailable */ }
    },
  };
  const me = {
    wishlist: new Set(store.get("wishlist", [])),
    visited: new Set(store.get("visited", [])),
    itinerary: store.get("itinerary", []),
    shelf: store.get("shelf", {}), // book_id -> "want" | "read"
    notes: store.get("notes", {}), // book_id -> text
    save() {
      store.set("wishlist", [...this.wishlist]);
      store.set("visited", [...this.visited]);
      store.set("itinerary", this.itinerary);
      store.set("shelf", this.shelf);
      store.set("notes", this.notes);
    },
  };

  // ---------- language ----------
  let lang = store.get("lang", "en") === "zh" ? "zh" : "en";
  const T = () => I18N[lang];
  const zh = () => lang === "zh";
  // data fields in the current language
  const placeName = (p) => (zh() ? p.name_zh : p.name);
  const regionName = (r) => (zh() ? r.name_zh : r.name);
  const bookTitle = (b) => (zh() ? `《${b.title_zh}》` : b.title);
  const bookAuthor = (b) => (zh() ? b.author_zh : b.author);
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
  for (const p of places.values()) {
    const u = GEO.units.find((unit) => inRings(p.lon, p.lat, unit.g));
    if (u) { p.region = u.r; continue; }
    // coastal points just outside the simplified coastline (a pier, a harbour wall): take the region
    // of the nearest boundary point — the same rule tools/validate.js uses
    let best = null, bd = Infinity;
    const c = Math.cos(p.lat * Math.PI / 180);
    for (const unit of GEO.units) for (const ring of unit.g) for (const [x, y] of ring) {
      const d = ((x - p.lon) * c) ** 2 + (y - p.lat) ** 2;
      if (d < bd) { bd = d; best = unit.r; }
    }
    p.region = best;
  }

  // ---------- DOM refs ----------
  const svg = document.getElementById("map");
  const reader = document.getElementById("reader");
  const crumbs = document.getElementById("crumbs");
  const tooltip = document.getElementById("tooltip");
  const legend = document.getElementById("legend");
  const root = el("g", { id: "viewport" });
  const gWorld = el("g", { class: "world" });
  const gUK = el("g", { class: "uk" });
  const gLabels = el("g", { class: "labels" });
  const gMarkers = el("g", { class: "markers" });
  root.append(gWorld, gUK, gLabels, gMarkers);
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

  // ---------- draw map ----------
  for (const c of GEO.world) {
    const p = el("path", { class: "country", d: c.g.map((r) => ringPath(r, true)).join("") }, gWorld);
    p.dataset.name = c.name;
    p.dataset.nameZh = c.name_zh || c.name;
  }
  const regionNodes = new Map();
  for (const r of GEO.regions) {
    const g = el("g", { class: "region", "data-id": r.id }, gUK);
    const wash = cssVar(WASH[r.id]);
    regionNodes.set(r.id, g);
    for (const u of GEO.units.filter((x) => x.r === r.id)) {
      el("path", { class: "unit", d: u.g.map((ring) => ringPath(ring, true)).join(""), fill: wash, stroke: wash }, g);
    }
    const outline = r.outline.map((l) => ringPath(l, false)).join("");
    el("path", { class: "region-band", d: outline, stroke: darken(wash, 0.78) }, g);
    el("path", { class: "region-line", d: outline }, g);
  }
  const regionLabels = new Map();
  // hand-placed label anchors where the area centroid crowds a neighbour's label
  const LABEL_AT = { TLD: [-2.95, 54.55], TLE: [-1.15, 53.85] };
  for (const r of GEO.regions) {
    const [lon, lat] = LABEL_AT[r.id] || r.centroid;
    const [x, y] = project(lon, lat);
    const label = el("text", { class: "region-label", x, y }, gLabels);
    if (r.id === "TLI") label.style.display = "none"; // too small to label at UK scale; markers carry it
    regionLabels.set(r.id, label);
  }

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
  for (const p of places.values()) {
    const [x, y] = project(p.lon, p.lat);
    const g = el("g", { class: "marker t-" + p.place_type, tabindex: 0, role: "button" }, gMarkers);
    g.dataset.id = p.id;
    g.dataset.x = x;
    g.dataset.y = y;
    el("circle", { class: "m-hit", r: 11 }, g);
    g.append(shape(p.place_type));
    el("text", { class: "marker-label", x: 10, y: 4 }, g);
    markerNodes.set(p.id, g);
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

  // all language-dependent text outside the reading panel
  function applyLanguage() {
    const t = T();
    document.documentElement.lang = t.htmlLang;
    document.title = t.pageTitle;
    for (const n of document.querySelectorAll("[data-i18n]")) n.textContent = t[n.dataset.i18n];
    for (const n of document.querySelectorAll("[data-i18n-placeholder]")) n.placeholder = t[n.dataset.i18nPlaceholder];
    for (const n of document.querySelectorAll("[data-i18n-aria]")) n.setAttribute("aria-label", t[n.dataset.i18nAria]);
    document.body.classList.toggle("lang-zh", zh());
    for (const [id, node] of regionLabels) node.textContent = regionName(regions.get(id));
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
  function applyView() {
    root.setAttribute("transform", `translate(${view.x},${view.y}) scale(${view.k})`);
    for (const t of regionLabels.values()) {
      t.style.fontSize = 15 / view.k + "px";
      t.style.strokeWidth = 3 / view.k + "px"; // the halo must not grow with the map
    }
    // region names give way to place names once zoomed into a region
    const zoomedIn = state.region != null || view.k > 60;
    gLabels.style.display = zoomedIn ? "none" : "";
    spreadMarkers(zoomedIn);
    placeLabels(zoomedIn);
  }

  // Markers closer than NEAR px on screen (e.g. Baker Street and the Sherlock Holmes Museum, ~100 m apart)
  // are fanned out on a small circle so each one can be clicked. Only small clusters, and only when
  // zoomed into a region: at UK scale London is one dense knot and the region click is the way in.
  const NEAR = 12;
  function spreadMarkers(zoomedIn) {
    const s = 1 / view.k;
    const nodes = [...markerNodes.values()].filter((g) => g.style.display !== "none");
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
    const order = [...markerNodes.values()].sort((a, b) => score(b) - score(a));
    const charW = zh() ? 13 : 7.2;
    for (const g of order) {
      const label = g.querySelector(".marker-label");
      const visible = g.style.display !== "none";
      if (!visible || (!zoomedIn && !g.classList.contains("is-active"))) { label.style.display = "none"; continue; }
      const sx = view.x + view.k * Number(g.dataset.x) + Number(g.dataset.dx || 0);
      const sy = view.y + view.k * Number(g.dataset.y) + Number(g.dataset.dy || 0);
      const w = label.textContent.length * charW + 4;
      const box = [sx + 8, sy - 10, sx + 12 + w, sy + 8];
      const clash = placed.some((b) => box[0] < b[2] && box[2] > b[0] && box[1] < b[3] && box[3] > b[1]);
      label.style.display = clash ? "none" : "";
      if (!clash) placed.push(box);
    }
  }
  function score(g) {
    if (g.classList.contains("is-active")) return 1e6;
    return (linesByPlace.get(g.dataset.id) || []).length * 10 + (places.get(g.dataset.id).city ? 5 : 0);
  }
  function size() { const r = svg.getBoundingClientRect(); return [r.width, r.height]; }
  // the reading panel covers the right side of the map; keep fitted content clear of it
  function panelOffset() {
    if (window.innerWidth <= 900 || document.body.classList.contains("intro-running")) return 0;
    return reader.offsetWidth;
  }
  function boundsView(lonMin, latMin, lonMax, latMax, pad) {
    const [x0, y1] = project(lonMin, latMin);
    const [x1, y0] = project(lonMax, latMax);
    const [w0, hgt] = size();
    const w = w0 - panelOffset();
    const k = Math.min((w - pad * 2) / (x1 - x0), (hgt - pad * 2) / (y1 - y0));
    return { k, x: w / 2 - k * (x0 + x1) / 2, y: hgt / 2 - k * (y0 + y1) / 2 };
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
    applyView();
  }
  const UK_BOUNDS = [-8.4, 49.9, 2.0, 59.2];
  function zoomUK(animate, dur) { fitBounds(...UK_BOUNDS, 30, animate, dur); }
  const WORLD_BOUNDS = [-170, -58, 180, 78];
  function zoomRegion(rid, animate) {
    const b = regions.get(rid).bbox;
    fitBounds(b[0], b[1], b[2], b[3], 50, animate);
  }
  function zoomPlace(p, animate) {
    // London is dense: zoom closer there than elsewhere
    const d = p.region === "TLI" ? 0.09 : 0.5;
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
    const r = svg.getBoundingClientRect();
    zoomBy(Math.exp(-e.deltaY * 0.0015), e.clientX - r.left, e.clientY - r.top);
  }, { passive: false });
  document.getElementById("zoom-in").addEventListener("click", () => zoomBy(1.6));
  document.getElementById("zoom-out").addEventListener("click", () => zoomBy(1 / 1.6));
  document.getElementById("zoom-uk").addEventListener("click", () => { select({ region: null, place: null }); zoomUK(true); });

  function countryName(node) { return zh() ? node.dataset.nameZh : node.dataset.name; }
  function handleMapClick(target) {
    if (!target) return;
    const marker = target.closest(".marker");
    if (marker && marker.dataset.id) return openPlace(marker.dataset.id, true);
    const region = target.closest(".region");
    if (region) return openRegion(region.dataset.id, true);
    if (target.classList.contains("country")) showTip(T().countrySoon(countryName(target)), lastPointer);
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
    if (marker && marker.dataset.id) {
      const p = places.get(marker.dataset.id);
      const n = (linesByPlace.get(p.id) || []).length;
      showTip(n ? T().tipWithCount(placeName(p), n) : T().tipWithType(placeName(p), typeLabel(p.place_type)), lastPointer);
    } else if (region) {
      const r0 = regions.get(region.dataset.id);
      showTip(zh() ? `${r0.name_zh} ${r0.name}` : r0.name, lastPointer);
    } else if (t.classList.contains("country")) {
      showTip(countryName(t), lastPointer);
    } else hideTip();
  });
  svg.addEventListener("mouseleave", hideTip);
  svg.addEventListener("keydown", (e) => {
    const m = e.target.closest && e.target.closest(".marker");
    if (m && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); openPlace(m.dataset.id, true); }
  });
  function showTip(text, [x, y]) {
    tooltip.textContent = text;
    tooltip.hidden = false;
    tooltip.style.left = x + 14 + "px";
    tooltip.style.top = y + 14 + "px";
  }
  function hideTip() { tooltip.hidden = true; }

  // ---------- app state ----------
  const state = { region: null, place: null, book: null, tab: "map" };
  function select(next) {
    Object.assign(state, { book: null }, next);
    for (const [id, g] of regionNodes) g.classList.toggle("is-active", id === state.region);
    for (const [id, g] of markerNodes) g.classList.toggle("is-active", id === state.place);
    updateMarkers();
    renderCrumbs();
    applyView();
    syncRoute();
  }

  // ---------- URL routes (spec F5): #/region/TLI · #/place/baker-street · #/book/persuasion · #/travel · #/reading ----------
  const ROUTE_RE = /^#\/(region|place|book|travel|reading)(?:\/([\w-]+))?$/;
  function currentRoute() {
    if (state.tab === "travel") return "#/travel";
    if (state.tab === "reading") return "#/reading";
    if (state.book) return "#/book/" + state.book;
    if (state.place) return "#/place/" + state.place;
    if (state.region) return "#/region/" + state.region;
    return "";
  }
  let routing = false;
  function syncRoute() {
    if (routing) return;
    const next = currentRoute();
    if ((location.hash || "") === next) return;
    if (next) history.pushState(null, "", next);
    else history.pushState(null, "", location.pathname + location.search);
  }
  function applyRoute(hash, animate) {
    const m = ROUTE_RE.exec(hash || "");
    routing = true;
    try {
      if (!m) { if (state.tab !== "map") setTab("map"); select({ region: null, place: null }); zoomUK(animate); renderIntro(); return true; }
      const [, kind, id] = m;
      if (kind === "region" && regions.has(id)) openRegion(id, animate);
      else if (kind === "place" && places.has(id)) openPlace(id, animate);
      else if (kind === "book" && books.has(id)) openBook(id);
      else if (kind === "travel" || kind === "reading") setTab(kind);
      else return false;
      return true;
    } finally {
      routing = false;
    }
  }
  window.addEventListener("popstate", () => applyRoute(location.hash, true));
  function updateMarkers() {
    for (const [id, g] of markerNodes) {
      const p = places.get(id);
      g.style.display = filters.has(p.place_type) ? "" : "none";
    }
    const zoomedIn = state.region != null || view.k > 60;
    spreadMarkers(zoomedIn);
    placeLabels(zoomedIn);
  }
  function renderCrumbs() {
    const t = T();
    const parts = [`<button data-go="world">${t.crumbWorld}</button>`, `<button data-go="uk">${t.crumbUK}</button>`];
    if (state.region) parts.push(`<button data-go="region">${esc(regionName(regions.get(state.region)))}</button>`);
    if (state.place) parts.push(`<span>${esc(placeName(places.get(state.place)))}</span>`);
    if (state.book) parts.push(`<span>${esc(bookTitle(books.get(state.book)))}</span>`);
    crumbs.innerHTML = parts.join('<span class="sep">›</span>');
  }
  crumbs.addEventListener("click", (e) => {
    const go = e.target.dataset && e.target.dataset.go;
    if (go === "world") { select({ region: null, place: null }); fitBounds(...WORLD_BOUNDS, 10, true); renderIntro(); }
    if (go === "uk") { select({ region: null, place: null }); zoomUK(true); renderIntro(); }
    if (go === "region") openRegion(state.region, true);
  });

  // ---------- reading panel ----------
  function setTab(tab) {
    state.tab = tab;
    for (const b of document.querySelectorAll(".tab")) b.classList.toggle("is-active", b.dataset.view === tab);
    rerender();
    syncRoute();
  }
  function rerender() {
    if (state.tab === "travel") renderTravel();
    else if (state.tab === "reading") renderReading();
    else if (state.book) renderBook(state.book);
    else if (state.place) renderPlace(state.place);
    else if (state.region) renderRegion(state.region);
    else renderIntro();
  }
  document.querySelector(".tabs").addEventListener("click", (e) => {
    const b = e.target.closest(".tab");
    if (b) setTab(b.dataset.view);
  });

  function show(fragment, keepScroll) {
    const top = reader.scrollTop;
    reader.replaceChildren(fragment);
    reader.scrollTop = keepScroll ? top : 0;
  }
  function uniqueLineCount(ps) {
    return new Set(ps.flatMap((p) => (linesByPlace.get(p.id) || []).map((l) => l.id))).size;
  }

  function renderIntro() {
    const t = T();
    show(h(`
      <div class="intro">
        <h2>${t.introTitle}</h2>
        <p class="sub">${t.introSub(DATA.books.length, DATA.lines.length, places.size)}</p>
        <ol class="steps">${t.introSteps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol>
        <h3>${t.introRegions}</h3>
        <ul class="place-list">${GEO.regions.map((r) => {
          const ps = [...places.values()].filter((p) => p.region === r.id);
          return `<li><button data-region="${r.id}"><span>${esc(regionName(r))}</span><span class="count">${t.placesAndExcerpts(ps.length, uniqueLineCount(ps))}</span></button></li>`;
        }).join("")}</ul>
      </div>`));
  }

  function openRegion(rid, animate) {
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
    let context = "";
    const stop = zh() ? "。" : ".";
    if (p.place_type === "prototype") context = `<p>${esc(zh() ? p.prototype_of : p.prototype_of_en)}${stop}</p>`;
    if (p.place_type === "pilgrimage") context = `<p>${esc(zh() ? p.note : p.note_en)}${stop}</p>`;
    if (p.place_type === "film_location") {
      const a = p.adaptation;
      context = `<p>${esc(t.filmContext(t.adaptationKind[a.kind] || a.kind, a.title, a.year, zh() ? p.scene : p.scene_en))}</p>`;
    }
    const related = linked.length ? `<h3>${t.relatedBooks}</h3><ul class="place-list">${linked.map(bookRow).join("")}</ul>` : "";
    const quotes = lines.length
      ? `<h3>${t.linesHere}</h3>${lines.map((l) => quoteHTML(l, "book")).join("")}`
      : (p.place_type === "film_location" || p.place_type === "pilgrimage") ? "" : `<p class="empty-note">${t.noLines}</p>`;
    show(h(`
      <div class="type-badge">${typeIcon(p.place_type)}${typeLabel(p.place_type)}</div>
      <h2>${esc(placeName(p))}</h2>
      <p class="sub">${zh() ? `${esc(p.name)}，` : ""}${esc(r ? regionName(r) : "")}</p>
      ${context}
      <div class="actions">
        <button class="btn ${me.wishlist.has(pid) ? "is-on" : ""}" data-toggle="wishlist" data-id="${pid}">${me.wishlist.has(pid) ? t.saved : t.save}</button>
        <button class="btn ${me.visited.has(pid) ? "is-on" : ""}" data-toggle="visited" data-id="${pid}">${me.visited.has(pid) ? t.visited : t.visit}</button>
        <button class="btn" data-trip="${pid}">${t.addTrip}</button>
      </div>
      ${quotes}
      ${related}`), keepScroll);
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
    const note = l.translation === "own" ? `<span class="draft">${t.ownTranslation}</span>` : "";
    return `
      <figure class="quote" data-line="${l.id}">
        <blockquote lang="en">${highlight(l.text_en, l.highlight_en)}</blockquote>
        <figcaption class="cite">${citeTarget}${sep}${esc(lineLocation(l))}${note}</figcaption>
        ${hasOrig ? `<button class="orig-toggle" data-orig="${l.id}">${t.showOriginal(langName(b.orig_lang))}</button>` : ""}
      </figure>`;
  }
  reader.addEventListener("click", (e) => {
    const t = e.target.closest("button");
    if (!t) return;
    if (t.dataset.region) return openRegion(t.dataset.region, true);
    if (t.dataset.place) return openPlace(t.dataset.place, true);
    if (t.dataset.book) return openBook(t.dataset.book);
    if (t.dataset.orig) return toggleOriginal(t);
    if (t.dataset.toggle) {
      const set = me[t.dataset.toggle];
      set.has(t.dataset.id) ? set.delete(t.dataset.id) : set.add(t.dataset.id);
      me.save();
      return refresh();
    }
    if (t.dataset.shelf) {
      const cur = me.shelf[t.dataset.id];
      if (cur === t.dataset.shelf) delete me.shelf[t.dataset.id]; else me.shelf[t.dataset.id] = t.dataset.shelf;
      me.save();
      return refresh();
    }
    if (t.dataset.trip) return openTripDialog(t.dataset.trip);
    if (t.dataset.removeTrip != null) {
      me.itinerary.splice(Number(t.dataset.removeTrip), 1);
      me.save();
      return renderTravel();
    }
  });
  // after toggling a button, redraw the same view without jumping to the top
  function refresh() {
    if (state.tab === "travel") renderTravel();
    else if (state.tab === "reading") renderReading();
    else if (state.book) renderBook(state.book, true);
    else if (state.place) renderPlace(state.place, true);
  }
  function toggleOriginal(btn) {
    const t = T();
    const l = DATA.lines.find((x) => x.id === btn.dataset.orig);
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
  function openBook(bid) {
    select({ region: null, place: null, book: bid });
    const ps = bookPlaces(bid);
    if (ps.length) {
      const lons = ps.map((p) => p.lon), lats = ps.map((p) => p.lat);
      // never zoom in further than about a city's width
      const cx = (Math.min(...lons) + Math.max(...lons)) / 2, cy = (Math.min(...lats) + Math.max(...lats)) / 2;
      const dx = Math.max(0.35, (Math.max(...lons) - Math.min(...lons)) / 2 + 0.15);
      const dy = Math.max(0.18, (Math.max(...lats) - Math.min(...lats)) / 2 + 0.08);
      fitBounds(cx - dx, cy - dy, cx + dx, cy + dy, 80, true);
    }
    if (state.tab !== "map") { state.tab = "map"; for (const b of document.querySelectorAll(".tab")) b.classList.toggle("is-active", b.dataset.view === "map"); }
    renderBook(bid);
  }
  function renderBook(bid, keepScroll) {
    const t = T();
    const b = books.get(bid);
    const lines = linesByBook.get(bid) || [];
    const uniq = bookPlaces(bid);
    const shelf = me.shelf[bid];
    const src = b.source_url ? `<a href="${esc(b.source_url)}" target="_blank" rel="noopener">${t.findText}</a>` : t.noText;
    const sub = zh() ? `${esc(b.title)}，${esc(b.author)}，${esc(b.year)}` : `${esc(b.author)}, ${esc(b.year)}`;
    show(h(`
      <h2>${esc(bookTitle(b))}</h2>
      <p class="sub">${sub}</p>
      <p>${src}</p>
      <div class="actions">
        <button class="btn ${shelf === "want" ? "is-on" : ""}" data-shelf="want" data-id="${bid}">${t.want}</button>
        <button class="btn ${shelf === "read" ? "is-on" : ""}" data-shelf="read" data-id="${bid}">${t.read}</button>
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
    me.save();
  });

  function renderTravel() {
    const t = T();
    const visited = [...me.visited].map((id) => places.get(id)).filter(Boolean);
    const regionCount = new Set(visited.map((p) => p.region)).size;
    const trips = me.itinerary.map((x, i) => ({ ...x, i })).sort((a, b) => a.date.localeCompare(b.date));
    const wish = [...me.wishlist].map((id) => places.get(id)).filter(Boolean);
    show(h(`
      <h2>${t.travelTitle}</h2>
      <p class="sub">${t.storedLocal}</p>
      <div class="stat-row">
        <div><strong>${visited.length}</strong>${t.statVisited}</div>
        <div><strong>${regionCount}/12</strong>${t.statRegions}</div>
        <div><strong>${trips.length}</strong>${t.statStops}</div>
      </div>
      <h3>${t.trip}</h3>
      ${trips.length ? `<ul class="trip-list">${trips.map((x) => {
        const p = places.get(x.place_id);
        return `<li><time datetime="${esc(x.date)}">${esc(x.date)}</time><span><button class="link-btn" data-place="${p.id}">${esc(placeName(p))}</button>${x.note ? `<br><span class="empty-note">${esc(x.note)}</span>` : ""}</span><button class="remove" data-remove-trip="${x.i}">${t.remove}</button></li>`;
      }).join("")}</ul>` : `<p class="empty-note">${t.tripEmpty}</p>`}
      <h3>${t.wish}</h3>
      ${wish.length ? `<ul class="place-list">${wish.map(placeRow).join("")}</ul>` : `<p class="empty-note">${t.wishEmpty}</p>`}
      <h3>${t.been}</h3>
      ${visited.length ? `<ul class="place-list">${visited.map(placeRow).join("")}</ul>` : `<p class="empty-note">${t.beenEmpty}</p>`}`));
  }
  function renderReading() {
    const t = T();
    const list = (kind) => Object.entries(me.shelf).filter(([, v]) => v === kind).map(([id]) => books.get(id)).filter(Boolean);
    const read = list("read"), want = list("want");
    const noted = Object.keys(me.notes).map((id) => books.get(id)).filter(Boolean);
    show(h(`
      <h2>${t.readingTitle}</h2>
      <p class="sub">${t.storedLocal}</p>
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
    form.date.value = new Date().toISOString().slice(0, 10);
    dialog.showModal();
  }
  dialog.addEventListener("close", () => {
    if (dialog.returnValue !== "ok" || !tripPlace) return;
    me.itinerary.push({ place_id: tripPlace, date: form.date.value, note: form.note.value.trim() });
    me.save();
    tripPlace = null;
  });

  // ---------- search (matches both languages whichever is showing) ----------
  const input = document.getElementById("search-input");
  const results = document.getElementById("search-results");
  let index = [];
  function buildSearchIndex() {
    index = [
      ...DATA.books.map((b) => ({ kind: T().kindBook, id: b.id, label: bookLabel(b), hay: [b.title, b.title_zh, b.title_orig, b.author, b.author_zh, b.author_orig].join(" ").toLowerCase() })),
      ...[...places.values()].map((p) => ({ kind: typeLabel(p.place_type), id: p.id, place: true, label: placeName(p), hay: [p.name, p.name_zh].join(" ").toLowerCase() })),
    ];
  }
  let hits = [], cursor = -1;
  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    if (!q) { results.hidden = true; return; }
    hits = index.filter((x) => x.hay.includes(q)).slice(0, 12);
    cursor = hits.length ? 0 : -1;
    drawHits(q);
  });
  function drawHits(q) {
    results.hidden = false;
    results.innerHTML = hits.length
      ? hits.map((x, i) => `<li role="option" aria-selected="${i === cursor}" data-i="${i}"><span>${esc(x.label)}</span><span class="kind">${esc(x.kind)}</span></li>`).join("")
      : `<li class="empty">${esc(T().searchEmpty(q))}</li>`;
  }
  input.addEventListener("keydown", (e) => {
    if (results.hidden || !hits.length) return;
    if (e.key === "ArrowDown") { cursor = (cursor + 1) % hits.length; drawHits(input.value); e.preventDefault(); }
    if (e.key === "ArrowUp") { cursor = (cursor - 1 + hits.length) % hits.length; drawHits(input.value); e.preventDefault(); }
    if (e.key === "Enter" && cursor >= 0) { choose(hits[cursor]); e.preventDefault(); }
    if (e.key === "Escape") results.hidden = true;
  });
  results.addEventListener("mousedown", (e) => {
    const li = e.target.closest("li[data-i]");
    if (li) { e.preventDefault(); choose(hits[Number(li.dataset.i)]); }
  });
  input.addEventListener("blur", () => setTimeout(() => (results.hidden = true), 100));
  function choose(x) {
    results.hidden = true;
    input.value = "";
    if (x.place) openPlace(x.id, true); else openBook(x.id);
  }

  // ---------- start ----------
  window.addEventListener("resize", () => {
    if (document.body.classList.contains("intro-running")) return;
    if (!state.region && !state.place && !state.book) zoomUK(false);
  });
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
    intro.run({
      project,
      worldView,
      t: () => T(),
      revealRegions() { gUK.style.transition = "opacity 600ms ease-out"; gUK.style.opacity = "1"; },
      finish(animate) {
        gUK.style.opacity = "1";
        document.body.classList.remove("intro-running");
        zoomUK(animate, 900);
      },
    });
  } else if (!(ROUTE_RE.test(location.hash) && applyRoute(location.hash, false))) {
    if (location.hash) history.replaceState(null, "", location.pathname + location.search); // unknown link
    zoomUK(false);
  }
})();
