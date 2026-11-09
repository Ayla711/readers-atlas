"""Find candidate photos on Wikimedia Commons for a list of places.
Usage: python3 -I find_photos.py <work_dir> <queries.json> [place_id ...]
queries.json: {"<place id>": ["search phrase", "another phrase", ...], ...}
Keeps only JPEGs ≥ 600 px wide, landscape, licensed CC0 / Public domain / CC BY / CC BY-SA (never NC or ND), and notes
the camera / object location from the file page (handy as a coordinate source). Writes <work_dir>/candidates.json and
<work_dir>/urls.tsv for dl_here.py. Commons rate-limits: expect pauses."""
import html, json, os, re, sys, urllib.parse
WORK, QFILE = sys.argv[1], sys.argv[2]
ONLY = set(sys.argv[3:])
sys.argv = ["x", WORK]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "photo_candidates.py")).read().replace("\nmain()\n", "\n")
exec(src)  # get(), file_info(), thumb_url(), OK_LICENSE
QUERIES = json.load(open(QFILE, encoding="utf-8"))
def where(title):
    page = get("https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))) or ""
    out = {}
    for kind in ("Camera location", "Object location"):
        i = page.find(kind)
        if i < 0:
            continue
        m = re.search(r"params=(-?[\d.]+)_([NS])_(-?[\d.]+)_([EW])", page[i:i + 4000])
        if m:
            la = float(m.group(1)) * (1 if m.group(2) == "N" else -1)
            lo = float(m.group(3)) * (1 if m.group(4) == "E" else -1)
            out[kind] = [round(la, 5), round(lo, 5)]
    return out
os.makedirs(WORK, exist_ok=True)
out_path = f"{WORK}/candidates.json"
out = json.load(open(out_path)) if os.path.exists(out_path) else {}
for pid, qs in QUERIES.items():
    if (ONLY and pid not in ONLY) or (not ONLY and pid in out):
        continue
    titles = []
    for q in qs:
        res = get("https://commons.wikimedia.org/w/index.php?" + urllib.parse.urlencode(
            {"search": q, "title": "Special:Search", "ns6": 1, "fulltext": 1, "limit": 15}))
        for t in re.findall(r'<a href="/wiki/(File:[^"]+)" title="File:[^"]+"', res or ""):
            t = html.unescape(urllib.parse.unquote(t).replace("_", " "))
            if t not in titles and re.search(r"\.jpe?g$", t, re.I):
                titles.append(t)
    cands = []
    for t in titles[:18]:
        i = file_info(t)
        if not i or not OK_LICENSE.search(i["license"]) or re.search(r"\bNC\b|\bND\b", i["license"]):
            continue
        if i["w"] < 600 or i["h"] > i["w"]:
            continue
        i["thumb_url"] = thumb_url(i["original"], 960) if i["w"] > 960 else i["original"]
        i["where"] = where(t)
        cands.append(i)
        if len(cands) == 4:
            break
    out[pid] = {"query": " / ".join(qs), "candidates": cands}
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=1)
    print(pid, len(titles), "found,", len(cands), "usable", flush=True)
with open(f"{WORK}/urls.tsv", "w") as f:
    for pid, d in out.items():
        for n, c in enumerate(d["candidates"]):
            f.write(f"{pid}\t{n}\t{c['thumb_url']}\n")
