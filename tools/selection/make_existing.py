"""Write tools/selection/existing.json: for each country, every book the app shows there -- the books its own books.js holds,
and the books its lines and its places (book_ids of writers' houses) point to. 11-24: the first version counted only books
with a line in the country, and so missed books shown only at a writer's house or a pilgrimage place.
"via" says how the country uses the book: "line" (it has a line or scene there), "house" (a writer's house or memorial names it), "book" (record kept in this country's books.js).
Usage (repo root): python3 -I tools/selection/make_existing.py"""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID = re.compile(r'^\s*\{ id: "([^"]+)"')
def field(l, n):
    m = re.search(r'\b%s: "((?:[^"\\]|\\.)*)"' % n, l); return m.group(1) if m else None
def ids(l, n):
    m = re.search(r'\b%s: \[([^\]]*)\]' % n, l); return re.findall(r'"([^"]+)"', m.group(1)) if m else []
books, home = {}, {}
for f in sorted(glob.glob(os.path.join(ROOT, "data", "*", "books.js"))):
    cc = os.path.basename(os.path.dirname(f))
    for l in open(f, encoding="utf-8"):
        m = ID.match(l)
        if m and m.group(1) not in books:
            books[m.group(1)] = (field(l, "title"), field(l, "author")); home[m.group(1)] = cc
out = {}
for d in sorted(glob.glob(os.path.join(ROOT, "data", "*"))):
    cc = os.path.basename(d); used = []; via = {}
    for name in ("books.js", "lines.js", "places.js"):
        p = os.path.join(d, name)
        if not os.path.exists(p): continue
        for l in open(p, encoding="utf-8"):
            m = ID.match(l)
            if not m: continue
            got = [m.group(1)] if name == "books.js" else ([field(l, "book_id")] if name == "lines.js" else ids(l, "book_ids"))
            for b in got:
                if b and b not in used: used.append(b)
                if b: via.setdefault(b, set()).add({"books.js": "book", "lines.js": "line", "places.js": "house"}[name])
    if used:
        out[cc] = [dict(id=b, title=books.get(b, (None, None))[0], author=books.get(b, (None, None))[1], home=home.get(b), via=sorted(via[b])) for b in used]
json.dump(out, open(os.path.join(ROOT, "tools", "selection", "existing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in out.items()})
