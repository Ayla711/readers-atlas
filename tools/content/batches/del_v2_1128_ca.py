"""11-28: Canada (selection rule v2, docs/selection-rubric.md, tools/selection/ca.md): remove 6 books from the app.
- 2 with zero evidence (Barometer Rising, I Heard the Owl Call My Name): user 11-28 「三本都删」; the third, Songs of a
  Sourdough, is kept as an exception (破例收) because the Robert Service Cabin in Dawson must carry it (user 11-28 「算了都留着吧」);
- 3 with one class of evidence whose authors have stronger books (Dance of the Happy Shades, St. Urbain's Horseman,
  The Manticore): user 11-28, reviewing the ten one-class books one by one;
- Life of Pi, judged not a Canadian setting (only the Toronto interludes of Part 1), like Do Not Say We Have Nothing: user 11-28.
Same method as del_v2_1127_sa.py: rows of tools/selection/ca.json whose decision starts with 删除 or 用户定不收, or is 不算加拿大,
and that are in the app. For each book: its record, all its lines (in any country), and the places only it used; a place another
book still uses stays, a pilgrimage place keeps its other book_ids. Photos of removed places go to _to_delete/ and their rows
leave docs/photo-credits.md.
KEEP: places that would be left without a book but are reused in this same batch by a new book (ca-wingham: Lives of Girls and
Women, whose Jubilee is drawn from Wingham), so they and their photos stay.

Usage (repo root): python3 -I tools/content/batches/del_v2_1128_ca.py .            dry run
                   python3 -I tools/content/batches/del_v2_1128_ca.py . --apply    writes; then build_countries.py and validate"""
import glob, json, os, re, shutil, sys

APP = sys.argv[1]
APPLY = "--apply" in sys.argv
SEL = os.path.join(APP, "tools", "selection")
CC = ["ca"]

drop = {}
for cc in CC:
    for r in json.load(open(os.path.join(SEL, cc + ".json"), encoding="utf-8"))["rows"]:
        if (r["decision"].startswith(("删除", "用户定不收")) or r["decision"] == "不算加拿大") and r["in_app"]:
            for bid in r["in_app"].split(", "):
                drop.setdefault(bid, []).append(cc)

RID = re.compile(r'^\s*\{ id: "([^"]+)"')
def field(line, name):
    m = re.search(r'\b%s: "([^"]*)"' % name, line)
    return m.group(1) if m else None
def idlist(line, name):
    m = re.search(r'\b%s: \[([^\]]*)\]' % name, line)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []

files = {}
for f in sorted(glob.glob(os.path.join(APP, "data", "*", "*.js"))):
    if os.path.basename(f) in ("books.js", "lines.js", "places.js"):
        files[f] = open(f, encoding="utf-8").read().split("\n")

found_books = set(); gone_lines = []; place_users = {}; pil = {}
for f, rows in files.items():
    kind = os.path.basename(f)
    for line in rows:
        m = RID.match(line)
        if not m: continue
        if kind == "books.js" and m.group(1) in drop: found_books.add(m.group(1))
        if kind == "lines.js":
            b = field(line, "book_id")
            for p in idlist(line, "place_ids"):
                place_users.setdefault(p, set()).add(b)
            if b in drop: gone_lines.append((f, m.group(1), b))
        if kind == "places.js":
            bids = idlist(line, "book_ids")
            if bids: pil[m.group(1)] = bids
for p, bids in pil.items():
    place_users.setdefault(p, set()).update(bids)
kept_elsewhere = set()
for cc in CC:
    for r in json.load(open(os.path.join(SEL, cc + ".json"), encoding="utf-8"))["rows"]:
        if r["in_app"] and not r["decision"].startswith("删除") and r["decision"].startswith(("保留", "破例收")):
            kept_elsewhere.update(set(r["in_app"].split(", ")) & set(drop))
assert not kept_elsewhere, ("marked 删除 in one table but kept in another", kept_elsewhere)
missing = set(drop) - found_books
assert not missing, ("books not found in data", missing)
KEEP = {"ca-wingham"}
gone_places = {p for p, users in place_users.items() if users and users <= set(drop)} - KEEP

out = {"books": [], "lines": [], "places": [], "photos": [], "pil_trimmed": []}
for f, rows in files.items():
    kind = os.path.basename(f); keep = []
    for line in rows:
        m = RID.match(line)
        if m:
            i = m.group(1)
            if kind == "books.js" and i in drop: out["books"].append(i); continue
            if kind == "lines.js" and field(line, "book_id") in drop: out["lines"].append(i); continue
            if kind == "places.js" and i in gone_places:
                out["places"].append(i)
                ph = re.search(r'photo: (\{.*?\})(, |\s*\})', line)
                if ph:
                    d = json.loads(ph.group(1)); out["photos"].append((i, d.get("file"), d.get("source")))
                continue
            if kind == "places.js" and i in pil and set(pil[i]) & set(drop):
                left = [b for b in pil[i] if b not in drop]
                line = re.sub(r'\bbook_ids: \[[^\]]*\]', "book_ids: " + json.dumps(left, ensure_ascii=False), line)
                out["pil_trimmed"].append((i, left))
        keep.append(line)
    if APPLY and keep != rows:
        open(f + ".new", "w", encoding="utf-8").write("\n".join(keep)); os.replace(f + ".new", f)

cred = os.path.join(APP, "docs", "photo-credits.md")
srcs = [s for _, _, s in out["photos"] if s]
cl = open(cred, encoding="utf-8").read().split("\n")
ck = [l for l in cl if not any(s in l for s in srcs)]
out["credit_rows_removed"] = len(cl) - len(ck)
if APPLY:
    if ck != cl:
        open(cred + ".new", "w", encoding="utf-8").write("\n".join(ck)); os.replace(cred + ".new", cred)
    dest = os.path.join(APP, "_to_delete", "photos_del_v2_1128_ca"); os.makedirs(dest, exist_ok=True)
    for _, fn, _ in out["photos"]:
        if fn and os.path.exists(os.path.join(APP, fn)): shutil.move(os.path.join(APP, fn), os.path.join(dest, os.path.basename(fn)))
print(json.dumps({"apply": APPLY, "books_to_drop": len(drop), **{k: (len(v) if isinstance(v, list) else v) for k, v in out.items()}}, ensure_ascii=False))
for k in ("books", "places", "pil_trimmed"): print(k, out[k])
print("photos", [(p, f) for p, f, _ in out["photos"]])
