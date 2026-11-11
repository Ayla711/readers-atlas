"""Export a country's data back into content-pack form (R-8), the reverse of tools/import_pack.py.

Usage: python3 -I tools/export_pack.py <country> [--app .] [--out packs/<country>] [--by "who"]

data/<country>/{books,places,lines}.js -> <out>/{pack,books,places,lines,photos}.json (docs/content-pack-spec.md).
  lines:  the checked record becomes source (+ translation_source) and is kept verbatim as source.checked, so a
          re-import reproduces it; texts with line breaks get keep_breaks so verse is not reflowed
  places: country and photo are dropped (photo -> photos.json as the Commons file title); an explicit region stays
  photos: a photo that was cropped on import cannot say where: it is listed with "cropped": true and printed
Use it to hand a country to someone else for a further batch, or to check that import_pack.py round-trips the data.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import urllib.parse

ap = argparse.ArgumentParser()
ap.add_argument("country")
ap.add_argument("--app", default=".")
ap.add_argument("--out")
ap.add_argument("--by", default="exported from data/*.js by tools/export_pack.py")
A = ap.parse_args()
APP = os.path.abspath(A.app)
C = A.country
OUT = os.path.abspath(A.out or os.path.join(APP, "packs", C))

code = "global.window={RA_DATA:{}};" + "".join(f"require('./data/{C}/{f}.js');" for f in ("books", "places", "lines")) + \
       "require('./data/countries.js');console.log(JSON.stringify({d:window.RA_DATA,c:window.RA_COUNTRIES}))"
got = json.loads(subprocess.check_output(["node", "-e", code], cwd=APP))
D, cfg = got["d"], next(c for c in got["c"] if c["code"] == C)
notes = []

def source_of(l):
    s = l.get("checked") or ""
    m = re.match(r"Project Gutenberg #(\d+)", s)
    if m:
        src = {"kind": "gutenberg", "id": int(m.group(1)), "checked": s}
        e = re.search(r"; ([^;]*(?:removed|restored|omitted)[^;]*), \d{4}-\d\d-\d\d$", s)
        if e:
            src["edits"] = e.group(1)
        t = re.search(r" and #(\d+)", s)
        return src, ({"kind": "gutenberg", "id": int(t.group(1))} if t else None)
    kind = "wikisource" if s.startswith("Wikisource") else "aozora" if s.startswith("Aozora") else "other"
    return {"kind": kind, "checked": s}, None

lines = []
for l in D["lines"]:
    r = {k: v for k, v in l.items() if k != "checked"}
    if l.get("kind") != "scene":
        r["source"], ts = source_of(l)
        if ts:
            r["translation_source"] = ts
        if "\n" in l["text_en"] or "\n" in (l.get("text_orig") or ""):
            r["keep_breaks"] = True
        if r["source"]["kind"] != "gutenberg":
            notes.append(f"line {l['id']}: source {r['source']['kind']} ({l.get('checked', '')[:50]})")
    lines.append(r)

places, photos = [], {}
for p in D["places"]:
    r = {k: v for k, v in p.items() if k not in ("country", "photo")}
    places.append(r)
    ph = p.get("photo")
    if ph:
        m = re.search(r"commons\.wikimedia\.org/wiki/(.+)$", ph.get("source", ""))
        if not m:
            notes.append(f"photo {p['id']}: not from Commons ({ph.get('source')}), left out")
            continue
        photos[p["id"]] = {"commons_file": urllib.parse.unquote(m.group(1)).replace("_", " "), "alt_en": ph["alt_en"], "alt_zh": ph["alt_zh"], "crop": None}
        if ph.get("cropped"):
            photos[p["id"]]["cropped"] = True
            notes.append(f"photo {p['id']}: was cropped on import; a fresh download would need the crop box again")

meta = {"country": C, "country_name": cfg["name"], "country_name_zh": cfg.get("name_zh", ""), "produced_by": A.by,
        "produced_at": datetime.date.today().isoformat(),
        "notes": "Exported from the site data. source.checked keeps each quotation's original check record; keep_breaks marks texts whose line breaks are kept."}
old = os.path.join(OUT, "pack.json")
if os.path.exists(old):
    prev = json.load(open(old, encoding="utf-8"))
    for k in ("region_scheme",):
        if k in prev:
            meta[k] = prev[k]
os.makedirs(OUT, exist_ok=True)
for name, v in (("pack", meta), ("books", D["books"]), ("places", places), ("lines", lines), ("photos", photos)):
    open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8").write(json.dumps(v, ensure_ascii=False, indent=1) + "\n")
print(f"{os.path.relpath(OUT, APP)}: {len(D['books'])} books, {len(places)} places, {len(lines)} lines, {len(photos)} photos")
for n in notes:
    print("  note:", n)
