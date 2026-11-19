// node tools/world_stats.js <app dir>: totals over every open country (books, excerpts, places), counted the way the
// intro counts one country; a place, excerpt or book that two countries share is counted once. Called by build_countries.py.
const fs = require("fs"), vm = require("vm"), path = require("path");
const app = process.argv[2];
const ctx = { window: {} }; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(app, "data/countries.js"), "utf8"), ctx);
const books = new Set(), lines = new Set(), places = new Set(); let n = 0;
for (const c of ctx.window.RA_COUNTRIES.filter((c) => c.open)) {
  const w = { window: { RA_DATA: {} } }; vm.createContext(w);
  for (const f of c.data || []) if (!f.endsWith("geo.js")) vm.runInContext(fs.readFileSync(path.join(app, f), "utf8"), w);
  const d = w.window.RA_DATA;
  const ls = (d.lines || []).filter((l) => (l.place_ids || []).some((p) => (d.places || []).some((x) => x.id === p && (x.country || c.code) === c.code)));
  const ps = (d.places || []).filter((p) => (p.country || c.code) === c.code);
  n++;
  ls.forEach((l) => { lines.add(l.id); books.add(l.book_id); });
  ps.forEach((p) => { places.add(p.id); (p.book_ids || []).forEach((b) => books.add(b)); });
}
console.log(JSON.stringify({ countries: n, books: books.size, lines: lines.size, places: places.size }));
