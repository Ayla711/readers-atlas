#!/usr/bin/env node
/* Data checks for The Reader's Atlas (spec 6.4). Run after every data change:
     node tools/validate.js
   Exits with code 1 if any error is found. Warnings do not fail the run. */
"use strict";
const path = require("path");
const fs = require("fs");
const vm = require("vm");

const root = path.join(__dirname, "..");
const sandbox = { window: {} };
vm.createContext(sandbox);
// one country per run (R-3/R-4): node tools/validate.js [country code]; default uk
const COUNTRY_CODE = process.argv[2] || "uk";
vm.runInContext(fs.readFileSync(path.join(root, "data/countries.js"), "utf8"), sandbox, { filename: "data/countries.js" });
const COUNTRY = sandbox.window.RA_COUNTRIES.find((c) => c.code === COUNTRY_CODE);
if (!COUNTRY) { console.error(`no country ${COUNTRY_CODE} in data/countries.js`); process.exit(2); }
for (const f of COUNTRY.data) {
  vm.runInContext(fs.readFileSync(path.join(root, f), "utf8"), sandbox, { filename: f });
}
const GEO = sandbox.window.RA_GEO;
if (GEO.country !== COUNTRY_CODE) console.error(`geo.js says country ${GEO.country}, expected ${COUNTRY_CODE}`);
const { books, places } = sandbox.window.RA_DATA;
let { lines } = sandbox.window.RA_DATA;

const errors = [], warnings = [];
const err = (m) => errors.push(m), warn = (m) => warnings.push(m);
const TYPES = ["original", "prototype", "pilgrimage", "film_location"];
const LANGS = ["en", "enm", "sco", "zh", "ja", "fr", "de", "it", "ru", "la", "cy", "es", "pt", "qu"];
const ID_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;

function checkIds(list, kind) {
  const seen = new Set();
  for (const x of list) {
    if (!x.id) { err(`${kind}: entry without id`); continue; }
    if (!ID_RE.test(x.id)) err(`${kind} ${x.id}: id must be lower-case words joined by hyphens`);
    if (seen.has(x.id)) err(`${kind} ${x.id}: duplicate id`);
    seen.add(x.id);
  }
  return seen;
}
function need(obj, fields, label) {
  for (const f of fields) {
    const v = obj[f];
    if (v === undefined || v === null || (typeof v === "string" && !v.trim())) err(`${label}: missing ${f}`);
  }
}

// ---------- books ----------
const bookIds = checkIds(books, "book");
// places and lines may point at a book another country already has (the app's book list is shared)
const otherBooks = [];
for (const c of sandbox.window.RA_COUNTRIES) {
  if (c.code === COUNTRY_CODE) continue;
  for (const f of c.data.filter((f) => f.endsWith("books.js") && !COUNTRY.data.includes(f))) {
    const sb = { window: {} }; vm.createContext(sb);
    try { vm.runInContext(fs.readFileSync(path.join(root, f), "utf8"), sb, { filename: f }); } catch (e) { continue; }
    otherBooks.push(...(((sb.window.RA_DATA || {}).books) || []));
  }
}
const refBookIds = new Set([...bookIds, ...otherBooks.map((b) => b.id)]);
for (const b of books) {
  const label = `book ${b.id}`;
  need(b, ["title", "title_zh", "author", "author_zh", "year", "orig_lang"], label);
  if (!LANGS.includes(b.orig_lang)) err(`${label}: unknown orig_lang "${b.orig_lang}"`);
  if (typeof b.public_domain !== "boolean") err(`${label}: public_domain must be true or false`);
}

// ---------- places ----------
const placeIds = checkIds(places, "place");
function inRings(lon, lat, rings) {
  let inside = false;
  for (const r of rings) for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
    const [xi, yi] = r[i], [xj, yj] = r[j];
    if ((yi > lat) !== (yj > lat) && lon < (xj - xi) * (lat - yi) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}
// nearest unit vertex: distance in km and its region (good enough for "within 2 km of the coast")
function nearest(lon, lat) {
  let best = Infinity, region = null;
  for (const u of GEO.units) for (const r of u.g) for (const [x, y] of r) {
    const dx = (x - lon) * 111.32 * Math.cos(lat * Math.PI / 180), dy = (y - lat) * 110.57;
    const d = Math.hypot(dx, dy);
    if (d < best) { best = d; region = u.r; }
  }
  return { km: best, region };
}
// photos (spec 6.2): free licences only, file present, credit complete
const PHOTO_LICENSE = /^(CC BY(-SA)? [0-9.]+|CC0|Public domain)$/;
let photos = 0;
for (const p of places) {
  if (!p.photo) continue;
  photos++;
  const ph = p.photo, label = `place ${p.id} photo`;
  need(ph, ["file", "author", "license", "license_url", "source", "alt_en", "alt_zh"], label);
  if (ph.license && !PHOTO_LICENSE.test(ph.license)) err(`${label}: licence "${ph.license}" is not on the allowed list`);
  if (ph.file && !fs.existsSync(path.join(__dirname, "..", ph.file))) err(`${label}: file ${ph.file} is missing`);
}
const placeRegion = {};
for (const p of places) {
  const label = `place ${p.id}`;
  need(p, ["name", "name_zh", "place_type"], label);
  if (!TYPES.includes(p.place_type)) err(`${label}: unknown place_type "${p.place_type}"`);
  if (typeof p.lat !== "number" || typeof p.lon !== "number") { err(`${label}: lat/lon must be numbers`); continue; }
  if (p.country !== COUNTRY_CODE) err(`place ${p.id}: country is ${JSON.stringify(p.country)}, expected "${COUNTRY_CODE}"`);
  const unit = GEO.units.find((u) => inRings(p.lon, p.lat, u.g));
  if (p.region) {
    // a region given in the data: only for a border town the simplified map puts on the wrong side
    if (!GEO.regions.some((r) => r.id === p.region)) err(`${label}: region ${p.region} does not exist`);
    else {
      let best = Infinity;
      const c = Math.cos((p.lat * Math.PI) / 180);
      for (const u of GEO.units) if (u.r === p.region) for (const ring of u.g) for (const [x, y] of ring) best = Math.min(best, Math.hypot((x - p.lon) * c, y - p.lat) * 111.2);
      if (unit && unit.r === p.region) warn(`${label}: region ${p.region} is set but the coordinates already fall there; the field can go`);
      else if (best > 5) err(`${label}: region ${p.region} is set but the point is ${best.toFixed(1)} km from it`);
      placeRegion[p.id] = p.region;
    }
  }
  else if (unit) placeRegion[p.id] = unit.r;
  else {
    const { km, region } = nearest(p.lon, p.lat);
    // islands Natural Earth leaves out (e.g. Holy Island) are flagged in the data and may sit up to 6 km off
    // mainland places on a coast that the simplified line cuts short (flag rough_coast) may sit up to 4 km off
    const limit = p.offshore_island ? 6 : p.rough_coast ? 4 : 2;
    if (km > limit) err(`${label}: ${p.lat}, ${p.lon} is ${km.toFixed(1)} km outside ${COUNTRY.name}`);
    else { placeRegion[p.id] = region; if (!p.offshore_island) warn(`${label}: just off the simplified coastline (${km.toFixed(1)} km), counted in ${region}`); }
  }
  if (p.place_type === "prototype") need(p, ["prototype_of", "prototype_of_en"], label);
  if (p.place_type === "pilgrimage") need(p, ["note", "note_en", "book_ids"], label);
  if (p.place_type === "original") need(p, ["note", "note_en"], label);
  if (p.place_type === "film_location") {
    need(p, ["adaptation", "scene", "scene_en", "book_ids"], label);
    if (p.adaptation) need(p.adaptation, ["title", "year", "kind"], `${label} adaptation`);
  }
  for (const bid of p.book_ids || []) if (!refBookIds.has(bid)) err(`${label}: book_ids points to missing book "${bid}"`);
  if (p.authors !== undefined) {
    if (p.place_type !== "pilgrimage") err(`${label}: authors is only for pilgrimage places`);
    if (!Array.isArray(p.authors) || !p.authors.length) err(`${label}: authors must be a non-empty list`);
    for (const a of p.authors || []) if (!books.some((b) => b.author === a)) err(`${label}: authors names "${a}", who has no book`);
  }
}

// ---------- lines ----------
checkIds(lines, "line");
const filmPlaces = new Set(places.filter((p) => p.place_type === "film_location").map((p) => p.id));
const bookById = Object.fromEntries([...otherBooks, ...books].map((b) => [b.id, b]));
for (const l of lines) {
  const label = `line ${l.id}`;
  // kind: "scene" = our own-words summary of a book still in copyright (spec 6.3): both languages, no source check
  const scene = l.kind === "scene";
  if (l.kind && !scene) err(`${label}: unknown kind "${l.kind}"`);
  need(l, scene ? ["book_id", "location", "location_zh", "text_en", "text_zh", "status"] : ["book_id", "location", "location_zh", "text_en", "translation", "status"], label);
  if (scene && (l.text_orig || l.checked)) err(`${label}: a scene note has no original text and no source check`);
  for (const term of (scene && l.highlight_zh) || []) if (!(l.text_zh || "").includes(term)) err(`${label}: highlight_zh "${term}" not found in text_zh`);
  if (!refBookIds.has(l.book_id)) err(`${label}: book_id points to missing book "${l.book_id}"`);
  if (!Array.isArray(l.place_ids) || !l.place_ids.length) err(`${label}: needs at least one place_id`);
  for (const pid of l.place_ids || []) {
    if (!placeIds.has(pid)) err(`${label}: place_ids points to missing place "${pid}"`);
    if (filmPlaces.has(pid)) err(`${label}: excerpts cannot point to a film location ("${pid}")`);
  }
  const b = bookById[l.book_id];
  if (b && !scene && b.orig_lang !== "en" && !b.orig_note && !l.text_orig) err(`${label}: ${b.orig_lang} original needs text_orig`);
  for (const term of l.highlight_en || []) if (!(l.text_en || "").includes(term)) err(`${label}: highlight_en "${term}" not found in text_en`);
  for (const term of l.highlight_orig || []) if (!(l.text_orig || "").includes(term)) err(`${label}: highlight_orig "${term}" not found in text_orig`);
  if (!["draft", "reviewed", "rejected"].includes(l.status)) err(`${label}: status must be draft, reviewed or rejected`);
}

// ---------- summary against the Week 1 content targets (spec 6.5) ----------
// targets count quotations only; scene notes are reported on their own line
const scenes = lines.filter((l) => l.kind === "scene");
lines = lines.filter((l) => l.kind !== "scene");
const lineCountByRegion = {};
for (const r of GEO.regions) lineCountByRegion[r.id] = new Set();
for (const l of lines) for (const pid of l.place_ids || []) if (placeRegion[pid]) lineCountByRegion[placeRegion[pid]].add(l.id);
const booksWithLines = new Set(lines.map((l) => l.book_id)).size;
const reviewed = lines.filter((l) => l.status === "reviewed").length;
const checked = lines.filter((l) => l.checked).length;
const emptyRegions = GEO.regions.filter((r) => lineCountByRegion[r.id].size === 0).map((r) => r.name);

const coordsChecked = places.filter((p) => typeof p.coord_checked === "string" && p.coord_checked.trim()).length;
console.log(`books ${books.length} (with excerpts ${booksWithLines}/25) · excerpts ${lines.length}/75 · checked against source ${checked} · reviewed ${reviewed}/50 · places ${places.length}/60 · coordinates checked ${coordsChecked}/${places.length}`);
// excerpts per region (spec 6.5: every region at least 5)
const perRegion = {};
for (const l of lines) for (const pid of l.place_ids) if (placeRegion[pid]) (perRegion[placeRegion[pid]] ||= new Set()).add(l.id);
const thin = GEO.regions.filter((r) => (perRegion[r.id] || new Set()).size < 5).map((r) => `${r.name} ${(perRegion[r.id] || new Set()).size}`);
console.log(`regions under 5 excerpts: ${thin.length ? thin.join(", ") : "none"}`);
const withPhoto = (types) => `${places.filter((p) => types.includes(p.place_type) && p.photo).length}/${places.filter((p) => types.includes(p.place_type)).length}`;
console.log(`photos ${photos} (pilgrimage and film places ${withPhoto(["pilgrimage", "film_location"])} · real-life models ${withPhoto(["prototype"])})`);
console.log(`scene notes (own words, books in copyright): ${scenes.length} for ${new Set(scenes.map((l) => l.book_id)).size} books`);
console.log(`regions without excerpts: ${emptyRegions.length ? emptyRegions.join(", ") : "none"}`);
for (const w of warnings) console.log("warning: " + w);
for (const e of errors) console.log("ERROR: " + e);
console.log(errors.length ? `\n${errors.length} error(s)` : "\nno errors");
process.exit(errors.length ? 1 : 0);
