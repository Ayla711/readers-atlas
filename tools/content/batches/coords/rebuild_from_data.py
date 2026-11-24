"""Rebuild a batch's coordinates file from the data it once wrote, when the original file was not kept.
A place record carries everything the file held: lat, lon and coord_checked ("<source> — <url>, <date>").
Usage: python3 -I rebuild_from_data.py <places.js> <out.json> [place id ...]   (no ids: every place in the file)"""
import json, re, sys
src, out, want = sys.argv[1], sys.argv[2], set(sys.argv[3:])
co = {}
for m in re.finditer(r'\{ id: "([^"]+)".*?lat: ([-\d.]+), lon: ([-\d.]+).*?coord_checked: "([^"]*)"', open(src, encoding="utf-8").read()):
    pid, lat, lon, cc = m.groups()
    if want and pid not in want:
        continue
    st, su = re.sub(r", \d{4}-\d\d-\d\d$", "", cc).split(" — ", 1)
    co[pid] = dict(lat=float(lat), lon=float(lon), st=st, su=su)
json.dump(co, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(co), "places")
