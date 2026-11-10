// Read current application data without changing it; supports both repository layouts.
const fs = require('fs'), vm = require('vm'), path = require('path');
const root = path.resolve(__dirname, '../../..');
const registry = path.join(root, 'data/countries.js');
let groups;
if (fs.existsSync(registry)) {
  const c = {window: {}}; vm.createContext(c);
  vm.runInContext(fs.readFileSync(registry, 'utf8'), c);
  groups = c.window.RA_COUNTRIES.map(country => country.data.filter(f => /\/(books|places|lines)\.js$/.test(f)));
} else groups = [['data/books.js', 'data/places.js', 'data/lines.js']];
const data = {books: [], places: [], lines: []};
for (const files of groups) {
  const c = {window: {}}; vm.createContext(c);
  for (const f of files) vm.runInContext(fs.readFileSync(path.join(root, f), 'utf8'), c);
  for (const key of Object.keys(data)) data[key].push(...(c.window.RA_DATA?.[key] || []));
}
const out = {books: data.books.map(({id,title,author})=>({id,title,author})),
  authors: [...new Set(data.books.map(b=>b.author))], places: data.places.map(p=>p.id), line_ids: data.lines.map(l=>l.id)};
fs.writeFileSync(path.join(__dirname, 'current-ids.json'), JSON.stringify(out, null, 2)+'\n');
console.log(`Current application: ${out.books.length} books, ${out.places.length} places, ${out.line_ids.length} lines`);
