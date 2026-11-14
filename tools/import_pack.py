"""Import a content pack (docs/content-pack-spec.md) into data/<country>/ (R-8).

Usage:
  python3 -I tools/import_pack.py <pack_dir> [--app .] [--date YYYY-MM-DD] [--no-photos] [--dry-run]

What the machine checks (a failure stops the import; nothing is written):
  1. shape: required fields per record, known place types, ids in the pack's own format
  2. ids: unique inside the pack and against every other country's data
  3. references: every line's book and places exist; every pilgrimage place's books exist
  4. text: every quotation is found word for word in its Project Gutenberg source, after the same normalisation the
     app's own batches use (curly quotes, -- as em dash, whitespace); "…" marks a cut and each side is checked on
     its own. A text that only matches after ignoring capitals (Gutenberg sets chapter openings in caps), line
     numbers, footnote marks like [2] and line-end hyphens, or with a short heading or speaker name between two of
     its lines, passes with a note in IMPORT.md; source.edits (a note on
     deliberate editorial changes) turns a remaining mismatch into a note for the reviewer.
     With text_orig, source checks text_orig and translation_source checks text_en. Sources of another
     kind (wikisource, aozora, ctext, other) are listed in IMPORT.md for the reviewer to check by hand.
  5. highlights: every highlighted word occurs in the text it highlights
  6. copyright: a book with public_domain false has scene notes only, except quotations whose source is Project
     Gutenberg (public domain in the US; the UK sample has a few, rechecked before public release, plan R-4)
  7. places: each falls in one of the country's admin-1 regions (or within 8 km of the simplified coast); when the
     pack's REPORT.md has the "每州地点数量" table, the region must match it
  8. authors: an author already present in another country is spelled the same, with the same Chinese name
  9. photos: the Commons file page is read again, the licence must be CC0 / public domain / CC BY / CC BY-SA
A line with "keep_breaks": true keeps its line breaks as written (verse, or a text already in the app's one-line-
per-paragraph form); other texts are reflowed. source.checked, when given, is kept as the line's checked record.
With --no-photos, places keep the photo they already have in data/<country>/places.js. Without it, a photo already
imported from the same Commons file (800 px wide, same crop) is kept and only new or changed photos are downloaded.
What it writes: data/<country>/{books,places,lines}.js (regenerated from the pack), images/places/<id>.jpg,
rows in docs/photo-credits.md, and <pack_dir>/IMPORT.md with every warning. Content stays status "draft".
Gutenberg texts are read from cache/pg/<n>.txt and downloaded there when missing.
"""
import argparse
import datetime
import html
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("pack")
ap.add_argument("--app", default=".")
ap.add_argument("--date", default=datetime.date.today().isoformat())
ap.add_argument("--no-photos", action="store_true")
ap.add_argument("--dry-run", action="store_true")
A = ap.parse_args()
APP = os.path.abspath(A.app)
PACK = os.path.abspath(A.pack)
UA = "ReadersAtlas/1.0 (educational literary atlas; content import, low volume)"
errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

def load(name):
    p = os.path.join(PACK, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

meta = load("pack.json") or {}
C = meta.get("country")
if not C:
    sys.exit("pack.json has no country")
books, places, lines = load("books.json") or [], load("places.json") or [], load("lines.json") or []
# a group of countries can share one book list (South America, 11-13): pack.json "shared_books" points at the group's
# books.json and "books_out" at the one data file every country of the group loads; each country's pack then holds
# only its places and lines, and a book may have places in several countries
SHARED = meta.get("shared_books")
BOOKS_OUT = meta.get("books_out") or f"data/{C}/books.js"
if SHARED:
    books = json.load(open(os.path.join(PACK, SHARED), encoding="utf-8"))
photos = load("photos.json") or {}

# ---------- existing data of the other countries ----------
def node_json(js_files):
    code = "global.window={RA_DATA:{}};" + "".join(f"require({json.dumps(f)});" for f in js_files) + "console.log(JSON.stringify({books:window.RA_DATA.books||[],places:window.RA_DATA.places||[],lines:window.RA_DATA.lines||[],geo:window.RA_GEO||null}))"
    return json.loads(subprocess.check_output(["node", "-e", code], cwd=APP))
countries = json.loads(subprocess.check_output(["node", "-e", "global.window={};require('./data/countries.js');console.log(JSON.stringify(window.RA_COUNTRIES))"], cwd=APP))
cfg = next((c for c in countries if c["code"] == C), None)
if not cfg:
    sys.exit(f"country {C} is not in tools/countries.json / data/countries.js")
others = {"books": [], "places": [], "lines": []}
for c in countries:
    if c["code"] == C:
        continue
    files = [os.path.join(APP, f) for f in c["data"] if os.path.exists(os.path.join(APP, f)) and not f.endswith("geo.js") and f != BOOKS_OUT]
    if files:
        d = node_json(files)
        for k in others:
            others[k] += d[k]
geo = node_json([os.path.join(APP, f"data/{C}/geo.js")])["geo"]

# ---------- 1-3 shape, ids, references ----------
REQ = {
    "book": ["id", "title", "title_zh", "author", "author_zh", "year", "orig_lang", "public_domain"],
    "place": ["id", "name", "name_zh", "lat", "lon", "place_type", "coord_checked"],
    "line": ["id", "book_id", "place_ids", "location", "location_zh", "text_en", "highlight_en", "status"],
}
TYPES = {"original", "prototype", "pilgrimage", "film_location"}
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
def check_records(kind, recs, other):
    seen = set()
    other_ids = {r["id"] for r in other}
    for r in recs:
        for f in REQ[kind]:
            if r.get(f) in (None, "", []):
                err(f"{kind} {r.get('id', '?')}: missing {f}")
        i = r.get("id", "")
        if not ID_RE.match(i):
            err(f"{kind} {i}: id must be lowercase words joined by hyphens")
        if i in seen:
            err(f"{kind} {i}: duplicate id in the pack")
        if i in other_ids:
            err(f"{kind} {i}: id already used by another country")
        seen.add(i)
check_records("book", books, others["books"])
check_records("place", places, others["places"])
check_records("line", lines, others["lines"])
B = {b["id"]: b for b in books}
# places and lines may point at a book another country already has (the app's book list is shared): Dumas's
# Three Musketeers is in the UK data, its opening scene in France
B = {**{b["id"]: b for b in others["books"]}, **B}
P = {p["id"]: p for p in places}
for p in places:
    if p.get("place_type") not in TYPES:
        err(f"place {p['id']}: unknown place_type {p.get('place_type')}")
    if not re.search(r"https?://", p.get("coord_checked", "")):
        err(f"place {p['id']}: coord_checked must name its source with a URL")
    for bid in p.get("book_ids", []):
        if bid not in B:
            err(f"place {p['id']}: book {bid} is not in the pack")
    if p.get("place_type") == "prototype" and not (p.get("prototype_of") and p.get("prototype_of_en")):
        err(f"place {p['id']}: a prototype needs prototype_of and prototype_of_en")
    if p.get("place_type") in ("original", "pilgrimage") and not (p.get("note") and p.get("note_en")):
        warn(f"place {p['id']}: no note / note_en")
for l in lines:
    if l.get("book_id") not in B:
        err(f"line {l['id']}: book {l.get('book_id')} is not in the pack")
    for pid in l.get("place_ids", []):
        if pid not in P:
            err(f"line {l['id']}: place {pid} is not in the pack")
    if l.get("status") not in ("draft", "reviewed", "rejected"):
        err(f"line {l['id']}: status must be draft, reviewed or rejected")
used_places = {pid for l in lines for pid in l.get("place_ids", [])} | {p["id"] for p in places if p.get("place_type") in ("pilgrimage", "film_location")}
for p in places:
    if p["id"] not in used_places:
        warn(f"place {p['id']}: no line points to it")
used_books = {l["book_id"] for l in lines} | {b for p in places for b in p.get("book_ids", [])}
for b in books:
    if b["id"] not in used_books and not SHARED:
        warn(f"book {b['id']}: no line or place refers to it")

# ---------- 4-6 text, highlights, copyright ----------
def norm(s):
    s = s.replace("\r", "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("_", "")
    s = re.sub(r"\s*--\s*", "—", s)
    return s
def flat(s):
    return re.sub(r"\s+", " ", norm(s)).strip()
def reflow(s, english=True):
    """Gutenberg hard wraps -> the app's convention: one line per paragraph, paragraphs joined by a newline.
    English text also gets the app's straight quotes; an original in another language keeps its own punctuation"""
    paras = re.split(r"\n\s*\n", (norm(s) if english else s.replace("\r", "")).strip())
    return "\n".join(re.sub(r"\s+", " ", p).strip() for p in paras if p.strip())
PG_DIR = os.path.join(APP, "cache", "pg")
_pg = {}
def gutenberg(n):
    if n in _pg:
        return _pg[n]
    path = os.path.join(PG_DIR, f"{n}.txt")
    if not os.path.exists(path):
        os.makedirs(PG_DIR, exist_ok=True)
        url = f"https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            data = urllib.request.urlopen(req, timeout=60).read()
            open(path, "wb").write(data)
            time.sleep(1)
        except Exception as e:
            err(f"Gutenberg #{n}: could not download ({e})")
            _pg[n] = None
            return None
    raw = open(path, encoding="utf-8", errors="replace").read()
    _pg[n] = (flat(raw), loose(raw))
    return _pg[n]
def in_order(piece, lenient, gap=120):
    """each line of a multi-line text found in order, with at most `gap` characters between (a heading, a stage
    direction or a speaker's name the quotation leaves out)"""
    parts = [loose(x) for x in piece.split("\n") if loose(x)]
    if len(parts) < 2:
        return False
    i = lenient.find(parts[0])
    while i != -1:
        pos, ok = i + len(parts[0]), True
        for q in parts[1:]:
            j = lenient.find(q, pos)
            if j == -1 or j - pos > gap:
                ok = False
                break
            pos = j + len(q)
        if ok:
            return True
        i = lenient.find(parts[0], i + 1)
    return False
def loose(s):
    s = flat(s).lower().replace("ȝ", "3")
    s = re.sub(r"\[[^\]]{1,12}\]", "", s)                       # footnote and sidenote marks: [2] [ii] [295:2] [D]
    s = re.sub(r"(?<!\S)(\d{1,4}|[xivlc]{1,7}\.)(?!\S)", " ", s)   # line numbers, stanza numbers
    s = re.sub(r"\s*—\s*", "—", s)
    s = re.sub(r"(\w)- (\w)", r"\1-\2", s)                      # hyphen at a line end
    return re.sub(r"\s+", " ", s).strip()
us_pd = set()
SOURCE_KINDS = {"gutenberg", "wikisource", "aozora", "ctext", "other"}
unchecked, loosely = [], []
def check_text(l, field, src):
    kind = src.get("kind")
    if kind not in SOURCE_KINDS:
        err(f"line {l['id']}: {field} needs a source with kind one of {', '.join(sorted(SOURCE_KINDS))}")
        return
    if kind != "gutenberg":
        if not (src.get("url") or src.get("checked") or src.get("note")):
            err(f"line {l['id']}: a {kind} source needs a url")
        unchecked.append(f"`{l['id']}` {field}: {kind} — {src.get('url') or src.get('checked') or src.get('note')}")
        return
    if not src.get("id"):
        err(f"line {l['id']}: a gutenberg source needs its id")
        return
    got = gutenberg(src["id"])
    if got is None:
        return
    strict, lenient = got
    how = "exact"
    for piece in re.split(r"\s*…\s*", l[field]):
        if not flat(piece) or flat(piece) in strict:
            continue
        if loose(piece) in lenient or in_order(piece, lenient):
            how = "loose"
            continue
        if src.get("edits"):
            unchecked.append(f"`{l['id']}` {field}: differs from Gutenberg #{src['id']} by the editing noted in the source — {src['edits']}")
            return
        err(f"line {l['id']}: {field} is not found word for word in Gutenberg #{src['id']}" + (f" (part: {flat(piece)[:50]!r}…)" if "…" in l[field] else ""))
        return
    if how == "loose":
        loosely.append(f"`{l['id']}` {field}")
for l in lines:
    scene = l.get("kind") == "scene"
    b = B.get(l.get("book_id"), {})
    if not scene and b and not b.get("public_domain"):
        if (l.get("source") or {}).get("kind") == "gutenberg":
            us_pd.add(b["id"])
        else:
            err(f"line {l['id']}: quotes from {b['id']}, which is not public domain — only scene notes are allowed")
    if scene:
        if not (l.get("text_zh") and l.get("highlight_zh") is not None):
            err(f"line {l['id']}: a scene note needs text_zh and highlight_zh")
        if not l.get("fact_source"):
            warn(f"line {l['id']}: scene note without fact_source")
    else:
        src = l.get("source") or {}
        if l.get("text_orig"):
            check_text(l, "text_orig", src)
            if l.get("translation_source"):
                check_text(l, "text_en", l["translation_source"])
            elif l.get("translation") == "original":
                check_text(l, "text_en", src)
            else:
                unchecked.append(f"`{l['id']}` text_en: translation {l.get('translation', '?')!r} has no translation_source")
        else:
            check_text(l, "text_en", src)
    for h in l.get("highlight_en", []):
        if flat(h) not in flat(l["text_en"]):
            err(f"line {l['id']}: highlight {h!r} is not in text_en")
    for h in l.get("highlight_orig", []) or []:
        if flat(h) not in flat(l.get("text_orig") or ""):
            err(f"line {l['id']}: highlight {h!r} is not in text_orig")
    if l.get("text_orig") and l.get("kind") != "scene" and not l.get("highlight_orig"):
        warn(f"line {l['id']}: has text_orig but no highlight_orig")
    for h in l.get("highlight_zh", []) or []:
        if h not in (l.get("text_zh") or ""):
            err(f"line {l['id']}: highlight {h!r} is not in text_zh")

if us_pd:
    warn(f"quotations from books marked public_domain false, taken from Project Gutenberg (US public domain; recheck before public release): {', '.join(sorted(us_pd))}")

# ---------- 7 places in regions ----------
def in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside
def region_of(lon, lat):
    for u in geo["units"]:
        n = sum(in_ring(lon, lat, r) for r in u["g"])
        if n % 2:
            return u["r"], 0.0
    import math
    best, reg = 1e9, None
    c = math.cos(math.radians(lat))
    for u in geo["units"]:
        for r in u["g"]:
            for x, y in r:
                d = math.hypot((x - lon) * c, y - lat) * 111.2
                if d < best:
                    best, reg = d, u["r"]
    return reg, best
def dist_to_region(lon, lat, rid):
    import math
    c = math.cos(math.radians(lat))
    return min(math.hypot((x - lon) * c, y - lat) * 111.2 for u in geo["units"] if u["r"] == rid for r in u["g"] for x, y in r)
region_fix = {}
expected = {}
rep = os.path.join(PACK, "REPORT.md")
names = {r["name"]: r["id"] for r in geo["regions"]}
if os.path.exists(rep):
    for m in re.finditer(r"^\| ([A-Z][A-Za-z .]+?) \| \d+ \| (.+?) \|$", open(rep, encoding="utf-8").read(), re.M):
        rid = names.get(m.group(1).strip()) or names.get(m.group(1).strip().replace("Washington, D.C.", "District of Columbia"))
        for pid in re.findall(r"`([a-z0-9-]+)`", m.group(2)):
            expected[pid] = rid or m.group(1).strip()
region_count = {}
for p in places:
    try:
        lat, lon = float(p["lat"]), float(p["lon"])
    except (TypeError, ValueError):
        err(f"place {p['id']}: lat/lon are not numbers")
        continue
    rid, km = region_of(lon, lat)
    if km > 8:
        err(f"place {p['id']}: {lat}, {lon} is {km:.0f} km outside {cfg['name']}")
        continue
    if km > 0:
        warn(f"place {p['id']}: {km:.1f} km off the simplified coastline, counted in {rid}")
    if p.get("region") and p["region"] != rid:
        dist = dist_to_region(lon, lat, p["region"]) if any(r["id"] == p["region"] for r in geo["regions"]) else 1e9
        if dist <= 5:
            region_fix[p["id"]] = p["region"]
            warn(f"place {p['id']}: on the simplified map it falls in {rid}; region field keeps it in {p['region']} ({dist:.1f} km)")
            rid = p["region"]
        else:
            err(f"place {p['id']}: region {p['region']} given, but the point falls in {rid}")
    elif p["id"] in expected and expected[p["id"]] != rid:
        # the simplified border can put a riverbank or lakeshore town on the wrong side: accept the pack's region
        # when the point is within 5 km of it, and store it on the place (the app and validate.js honour it)
        want = expected[p["id"]]
        dist = dist_to_region(lon, lat, want)
        if dist <= 5:
            region_fix[p["id"]] = want
            warn(f"place {p['id']}: on the simplified map it falls in {rid}, {dist:.1f} km from {want}; kept in {want} as REPORT.md says (region field set)")
            rid = want
        else:
            err(f"place {p['id']}: falls in {rid}, REPORT.md says {want} ({dist:.0f} km away)")
    region_count[rid] = region_count.get(rid, 0) + 1
missing_regions = [r["name"] for r in geo["regions"] if r["id"] not in region_count]
if missing_regions:
    warn(f"regions without a place: {', '.join(missing_regions)}")

# ---------- 8 authors ----------
def akey(n):
    return re.sub(r"[^a-z]", "", n.lower())
known = {}
for b in others["books"]:
    known.setdefault(akey(b["author"]), (b["author"], b["author_zh"]))
for b in books:
    k = akey(b["author"])
    if k in known:
        en, zh = known[k]
        if b["author"] != en:
            err(f"book {b['id']}: author spelled {b['author']!r}, another country has {en!r}")
        if b["author_zh"] != zh:
            err(f"book {b['id']}: author_zh {b['author_zh']!r}, another country has {zh!r}")
    if re.search(r"\b[A-Z]\.[A-Z]\.", b["author"]):
        err(f"book {b['id']}: initials need a space after each dot ({b['author']})")

# ---------- 9 photos ----------
OK_LICENSE = re.compile(r"^(CC BY(-SA)? [0-9.]+( [a-z]+)?|CC0|Public domain|PD|Attribution|CC BY(-SA)?)", re.I)
def get(url, binary=False):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                data = r.read()
            time.sleep(1.2)
            return data if binary else data.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429:   # throttled: wait longer each time
                time.sleep(30 * (i + 1))
                continue
            if e.code == 404:
                return None
            time.sleep(3)
        except Exception:
            time.sleep(3)
    return None
def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
def file_info(title):
    page = get("https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")))
    if not page:
        return None
    page = page.replace("&#95;", "_")
    # a file can carry several licences (often GFDL plus a CC one): take the first one we may use
    shorts = [text(x) for x in re.findall(r'class="licensetpl_short"[^>]*>(.*?)</span>', page, re.S)]
    links = [text(x) for x in re.findall(r'class="licensetpl_link"[^>]*>(.*?)</span>', page, re.S)]
    ok = [i for i, x in enumerate(shorts) if OK_LICENSE.search(x) and not re.search(r"\bNC\b|\bND\b", x)]
    k = ok[0] if ok else 0
    class _M:
        def __init__(self, v): self.v = v
        def group(self, n): return self.v
    lic = _M(shorts[k]) if shorts else None
    lic_url = _M(links[k]) if k < len(links) else None
    aut = re.search(r'id="fileinfotpl_aut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', page, re.S)
    orig = re.search(r'<div class="fullImageLink"[^>]*>\s*<a href="(https://upload\.wikimedia\.org/[^"]+)"', page)
    dims = re.search(r'([\d,]+) × ([\d,]+) pixels', page)
    return {"w": int(dims.group(1).replace(",", "")) if dims else 0,"page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
            "license": text(lic.group(1)) if lic else "", "license_url": text(lic_url.group(1)) if lic_url else "",
            "author": text(aut.group(1))[:120] if aut else "", "original": orig.group(1).split("?")[0] if orig else ""}
def thumb(orig, width=960):  # Commons serves only its standard thumbnail widths; 960 is one of them
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+)$", orig)
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/{m.group(3)}/{width}px-{m.group(3)}" if m else orig
photo_out, credit_rows, kept_photos = {}, [], 0
old_photo = {}
if os.path.exists(os.path.join(APP, f"data/{C}/places.js")):
    old_photo = {p["id"]: p["photo"] for p in node_json([os.path.join(APP, f"data/{C}/places.js")])["places"] if p.get("photo")}
for pid, ph in photos.items():
    if pid not in P:
        err(f"photo {pid}: no such place in the pack")
        continue
    if A.no_photos or A.dry_run or errors:
        continue
    # a photo already imported from the same Commons file, at full card width and with the same crop, is kept as it
    # is (only its alt text follows the pack): Commons throttles downloads, so only new or changed photos are fetched
    was = old_photo.get(pid)
    same_page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(ph["commons_file"].replace(" ", "_"))
    if was and was.get("source") == same_page and was.get("width", 0) >= 800 and was.get("crop") == (list(ph["crop"]) if ph.get("crop") else None) \
            and os.path.exists(os.path.join(APP, was["file"])):
        photo_out[pid] = (None, {**was, "alt_en": ph["alt_en"], "alt_zh": ph["alt_zh"]})
        kept_photos += 1
        continue
    info = file_info(ph["commons_file"])
    if not info:
        err(f"photo {pid}: Commons page {ph['commons_file']} not found")
        continue
    if not OK_LICENSE.search(info["license"]) or re.search(r"\bNC\b|\bND\b", info["license"]):
        err(f"photo {pid}: licence {info['license']!r} is not allowed")
        continue
    # Commons asks bots to fetch standard thumbnail widths rather than originals: 960 first, then 500 (upscaling is
    # avoided: a 500 px image stays 500 px and is flagged)
    # a cropped photo starts from the next standard width up, so that what is left still fills the 800 px card
    widths = ([1920] if ph.get("crop") and info["w"] >= 1920 else []) + [960, 500]
    data = None
    for w in widths:
        data = get(thumb(info["original"], w), binary=True)
        if data:
            break
    if not data:
        err(f"photo {pid}: could not download the image")
        continue
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGB")
    if ph.get("crop"):
        x0, y0, x1, y1 = ph["crop"]
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    if im.width < 800:
        warn(f"photo {pid}: only {im.width} px wide (the place card shows 800); a larger file would look sharper")
    if im.height > im.width:
        warn(f"photo {pid}: portrait image ({im.width}×{im.height}); the place card is designed for landscape")
    if not info["license_url"] and re.match(r"(Public domain|PD)", info["license"], re.I):
        info["license_url"] = "https://creativecommons.org/publicdomain/mark/1.0/"  # Commons gives no link for plain PD
    rel = f"images/places/{pid}.jpg"
    photo_out[pid] = (im, {"file": rel, "width": im.width, "height": im.height, "author": info["author"] or "Unknown author",
                           "license": info["license"], "license_url": info["license_url"], "source": info["page"],
                           "alt_en": ph["alt_en"], "alt_zh": ph["alt_zh"], **({"cropped": True, "crop": list(ph["crop"])} if ph.get("crop") else {})})
    credit_rows.append(f"| {P[pid]['name']} | {info['author'] or 'Unknown author'} | [{info['license']}]({info['license_url']}) | [Commons]({info['page']}) |")

# ---------- report ----------
lines_md = [f"# 导入报告 · {meta.get('country_name', C)} · {A.date}", "",
            f"包：{len(books)} 本书、{len(places)} 个地点、{len(lines)} 条摘句和场景说明、{len(photos)} 张照片。", "",
            f"## 错误（{len(errors)}）", ""] + [f"- {e}" for e in errors] + ["", f"## 提示（{len(warnings)}）", ""] + [f"- {w}" for w in warnings] + \
           ["", f"## 脚本没有逐字核对的文本（{len(unchecked)}，审核时人工核对）", ""] + [f"- {u}" for u in unchecked] + \
           ["", f"## 忽略大小写、行号、注码后才对上的文本（{len(loosely)}）", ""] + [f"- {u}" for u in loosely] + \
           ["", "## 每个一级区的地点数", "", "| 区 | 地点 |", "|---|---:|"] + \
           [f"| {r['name']} | {region_count.get(r['id'], 0)} |" for r in geo["regions"]]
open(os.path.join(PACK, "IMPORT.md"), "w", encoding="utf-8").write("\n".join(lines_md) + "\n")
print(f"errors {len(errors)}, warnings {len(warnings)} (details in {os.path.relpath(os.path.join(PACK, 'IMPORT.md'), APP)})")
for e in errors[:40]:
    print("  ERROR", e)
if errors or A.dry_run:
    sys.exit(1 if errors else 0)

# ---------- write ----------
D = ", " + A.date
def js(v):
    return json.dumps(v, ensure_ascii=False)
def obj(d):
    return "{ " + ", ".join(f"{k}: {js(v)}" for k, v in d.items()) + " }"
def write(name, header, var, recs):
    with open(os.path.join(APP, name if "/" in name else os.path.join("data", C, name)), "w", encoding="utf-8") as fh:
        fh.write(header)
        fh.write(f"window.RA_DATA = window.RA_DATA || {{}};\nwindow.RA_DATA.{var} = [\n")
        fh.write(",\n".join("  " + obj(r) for r in recs))
        fh.write("\n];\n")
src_note = f"// Imported from packs/{os.path.basename(PACK)} ({meta.get('produced_by', '?')}, {meta.get('produced_at', '?')}) by tools/import_pack.py on {A.date}. Edit the pack and re-import rather than editing this file.\n"
out_books = []
for b in books:
    d = {k: b[k] for k in ["id", "title", "title_zh", "title_orig", "author", "author_zh", "author_orig", "year", "orig_lang", "public_domain", "source_url", "aliases", "orig_note"] if k in b and (b[k] is not None or k == "source_url")}
    out_books.append(d)
out_places = []
for p in places:
    d = {"id": p["id"], "country": C}
    p = {k: v for k, v in p.items() if k != "region"}
    d.update({k: v for k, v in p.items() if k not in ("id", "country") and v not in (None, [])})
    for k in ("note", "note_en", "prototype_of", "prototype_of_en", "scene", "scene_en"):
        if isinstance(d.get(k), str):
            d[k] = re.sub(r"[.。]$", "", d[k].strip())  # the app adds the full stop itself
    if p["id"] in region_fix:
        d["region"] = region_fix[p["id"]]
    if p["id"] in photo_out:
        d["photo"] = photo_out[p["id"]][1]
    elif A.no_photos and p["id"] in photos and p["id"] in old_photo:
        d["photo"] = old_photo[p["id"]]
    out_places.append(d)
out_lines = []
for l in lines:
    d = {k: v for k, v in l.items() if k not in ("source", "translation_source", "keep_breaks")}
    if l.get("kind") != "scene":
        if l.get("keep_breaks"):
            d["text_en"] = norm(l["text_en"]).strip()
            if l.get("text_orig"):
                d["text_orig"] = l["text_orig"].replace("\r", "").strip()
        else:
            d["text_en"] = reflow(l["text_en"])
            if l.get("text_orig"):
                d["text_orig"] = reflow(l["text_orig"], english=False)
        d["highlight_en"] = [flat(h) for h in l["highlight_en"]]
        d.setdefault("translation", "original")
        src, ts = l["source"], l.get("translation_source") or {}
        if src.get("checked"):
            d["checked"] = src["checked"]
        elif src["kind"] == "gutenberg":
            d["checked"] = f"Project Gutenberg #{src['id']}" + (f" and #{ts['id']}" if ts.get("kind") == "gutenberg" else "") + D
        else:
            d["checked"] = f"{src['kind'].capitalize()} {src.get('url') or src.get('note')}{D}"
    else:
        d["text_en"] = flat(l["text_en"])
        d["highlight_en"] = [flat(h) for h in l["highlight_en"]]
    out_lines.append(d)
write(BOOKS_OUT if SHARED else "books.js", src_note.replace(f"packs/{os.path.basename(PACK)}", f"packs/{os.path.basename(PACK)}/{SHARED}") if SHARED else src_note, "books", out_books)
write("places.js", src_note + "// Each place's admin-1 region is worked out from its coordinates by app.js.\n", "places", out_places)
write("lines.js", src_note + "// Gutenberg quotations were checked word for word on import (other sources by hand: see the pack's IMPORT.md); status changes only through review (tools/apply_review.py).\n", "lines", out_lines)
for pid, (im, ph) in photo_out.items():
    if im is not None:   # None: kept as it was
        im.save(os.path.join(APP, ph["file"]), "JPEG", quality=82, optimize=True, progressive=True)
if credit_rows:
    cp = os.path.join(APP, "docs", "photo-credits.md")
    s = open(cp, encoding="utf-8").read()
    rows = [r for r in credit_rows if r.split(" | [Commons](")[1] not in s]
    if rows:
        open(cp, "a", encoding="utf-8").write("\n".join(rows) + "\n")
print(f"written: {BOOKS_OUT} ({len(out_books)}), places.js ({len(out_places)}), lines.js ({len(out_lines)}), {len(photo_out)} photos ({kept_photos} kept as they were)")
