"""11-24: remove the books that still had zero evidence after the second check (selection rule v2, docs/selection-rubric.md;
the user agreed on 11-24: 复核完确定 0 分的可以删掉). The list comes from tools/selection/<cc>.json, rows whose decision starts
with 删除. For each book: its record, all its lines (in any country), and the places that only it used; a place another book
still uses stays, a pilgrimage place keeps its other book_ids. Photos of removed places are moved to _to_delete/ (this machine
cannot delete files) and their rows taken out of docs/photo-credits.md.

Usage (repo root): python3 -I tools/content/batches/del_v2_1124.py .            dry run: prints what would go
                   python3 -I tools/content/batches/del_v2_1124.py . --apply    writes; then run tools/build_countries.py and validate"""
import glob, json, os, re, shutil, sys

APP = sys.argv[1]
APPLY = "--apply" in sys.argv
SEL = os.path.join(APP, "tools", "selection")
CC = "au nz eg za ng dz ma ke fi hu is tr ua ro nl be ch dk no se".split()

drop = {}
for cc in CC:
    for r in json.load(open(os.path.join(SEL, cc + ".json"), encoding="utf-8"))["rows"]:
        if r["decision"].startswith("删除") and r["in_app"]:
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
missing = set(drop) - found_books
assert not missing, ("books not found in data", missing)
gone_places = {p for p, users in place_users.items() if users and users <= set(drop)}

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
    dest = os.path.join(APP, "_to_delete", "photos_del_v2_1124"); os.makedirs(dest, exist_ok=True)
    for _, fn, _ in out["photos"]:
        if fn and os.path.exists(os.path.join(APP, fn)): shutil.move(os.path.join(APP, fn), os.path.join(dest, os.path.basename(fn)))
print(json.dumps({"apply": APPLY, "books_to_drop": len(drop), **{k: (len(v) if isinstance(v, list) else v) for k, v in out.items()}}, ensure_ascii=False))
for k in ("books", "places", "pil_trimmed"): print(k, out[k])
print("photos", [(p, f) for p, f, _ in out["photos"]])
