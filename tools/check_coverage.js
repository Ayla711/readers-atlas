#!/usr/bin/env node
/* Coverage check for The Reader's Atlas (spec 6.5). Run before choosing a new batch and after adding one:
     node tools/check_coverage.js            report
     node tools/check_coverage.js --brief    counts only
   It compares the database with an outside checklist (tools/canon.json, built from published lists of
   writers' houses, Poets' Corner and the BBC Big Read), so gaps show up even for writers the database has
   never heard of. Decisions to leave something out go in tools/coverage-decisions.json with a reason.
   Exits with code 1 while a tier-1 gap is neither filled nor decided. */
"use strict";
const path = require("path");
const fs = require("fs");
const vm = require("vm");

const root = path.join(__dirname, "..");
const sandbox = { window: {} };
vm.createContext(sandbox);
for (const f of ["data/uk/books.js", "data/uk/places.js", "data/uk/lines.js"]) {
  vm.runInContext(fs.readFileSync(path.join(root, f), "utf8"), sandbox, { filename: f });
}
const { books, places, lines } = sandbox.window.RA_DATA;
const canon = JSON.parse(fs.readFileSync(path.join(__dirname, "canon.json"), "utf8"));
const decFile = path.join(__dirname, "coverage-decisions.json");
const decisions = fs.existsSync(decFile) ? JSON.parse(fs.readFileSync(decFile, "utf8")).decisions || [] : [];
const decided = (kind, name) => decisions.find((d) => d.kind === kind && d.name === name);
const brief = process.argv.includes("--brief");

const norm = (s) => (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
const byAuthor = {};
for (const b of books) (byAuthor[b.author] = byAuthor[b.author] || []).push(b);
const bookById = Object.fromEntries(books.map((b) => [b.id, b]));
const titles = new Set(books.flatMap((b) => [b.title, ...(b.aliases || [])].map(norm)));

const out = { gaps1: [], gaps2: [], decided: [] };
function report(tier, kind, name, msg) {
  const d = decided(kind, name);
  if (d) out.decided.push(`${kind} ${name}: ${d.decision} (${d.reason})`);
  else (tier === 1 ? out.gaps1 : out.gaps2).push(`${kind.padEnd(7)} ${msg}`);
}

// 1. writers on the checklist who have no book at all
for (const a of canon.authors) {
  if (!byAuthor[a.name]) report(a.tier, "author", a.name, `${a.name}: no book in the database`);
}

// 2. writers' houses, graves and memorials: is the place there, and is it linked to every listed writer we have?
for (const s of canon.sites) {
  let hits = places.filter((p) => s.ids.includes(p.id));
  if (!hits.length && s.names.length) {
    hits = places.filter((p) => p.place_type === "pilgrimage" && s.names.some((n) => norm(p.name).includes(norm(n))));
  }
  if (!hits.length) {
    const have = s.authors.filter((a) => byAuthor[a]);
    report(s.tier, "site", s.name, `${s.name}: no place${have.length ? "" : " (writer not in the database either)"}`);
    continue;
  }
  for (const p of hits) {
    // linked through the place's book list, its writer list, or a line or scene placed there
    const ids = [...(p.book_ids || []), ...lines.filter((l) => l.place_ids.includes(p.id)).map((l) => l.book_id)];
    const linked = new Set([...ids.map((id) => bookById[id] && bookById[id].author), ...(p.authors || [])]);
    const missing = s.authors.filter((a) => byAuthor[a] && !linked.has(a));
    if (missing.length) report(s.tier, "link", `${p.id}`, `${p.id}: not linked to ${missing.join(", ")}`);
  }
}

// 3. BBC Big Read titles with a UK setting or model
for (const r of canon.big_read) {
  if (![r.title, ...r.also].some((t) => titles.has(norm(t)))) report(r.tier, "book", r.title, `${r.rank ? "#" + r.rank + " " : ""}${r.title} (${r.author}): not in the database`);
}

// 4. a pilgrimage place linked to some of a writer's books but not the others
for (const p of places.filter((x) => x.place_type === "pilgrimage")) {
  const ids = p.book_ids || [];
  const authors = new Set(ids.map((id) => bookById[id] && bookById[id].author));
  const missing = books.filter((b) => authors.has(b.author) && !ids.includes(b.id)).map((b) => b.id);
  if (missing.length) report(2, "books", p.id, `${p.id}: also by the same writer, not linked: ${missing.join(", ")}`);
}

// 5. books that never show up as a line or scene
const withLines = new Set(lines.map((l) => l.book_id));
const silent = books.filter((b) => !withLines.has(b.id)).map((b) => b.id);

console.log(`checklist ${canon.checked}: ${canon.authors.length} writers, ${canon.sites.length} places, ${canon.big_read.length} Big Read titles`);
console.log(`tier-1 gaps ${out.gaps1.length} · tier-2 gaps ${out.gaps2.length} · decided ${out.decided.length} · books without a line or scene ${silent.length}`);
if (!brief) {
  if (out.gaps1.length) console.log("\nTIER 1 (must fix or decide):\n  " + out.gaps1.join("\n  "));
  if (out.gaps2.length) console.log("\nTIER 2:\n  " + out.gaps2.join("\n  "));
  if (out.decided.length) console.log("\nDECIDED:\n  " + out.decided.join("\n  "));
  if (silent.length) console.log("\nBOOKS WITHOUT A LINE OR SCENE:\n  " + silent.join(", "));
}
process.exit(out.gaps1.length ? 1 : 0);
