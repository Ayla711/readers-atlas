"""Build data/intro-geo.js: light world outlines for the opening animation.
Natural Earth 1:110m countries (public domain), Antarctica dropped, long edges densified
so they curve properly on the globe.
Usage: python3 -I build_intro_geo.py <ne_110m_admin_0_countries.geojson> <out.js>"""
import json
import math
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
STEP = 0.05      # degrees, coordinate quantization
MAX_SEG = 2.0    # degrees, longest edge allowed after densifying

d = json.load(open(SRC))
countries = []
points = 0
for f in d["features"]:
    p = f["properties"]
    iso = p.get("ADM0_A3")
    if iso == "ATA":
        continue
    g = f["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    rings = []
    for poly in polys:
        ring = poly[0]
        out = []
        for i in range(len(ring) - 1):
            (x1, y1), (x2, y2) = ring[i], ring[i + 1]
            n = max(1, math.ceil(max(abs(x2 - x1), abs(y2 - y1)) / MAX_SEG))
            for k in range(n):
                x = x1 + (x2 - x1) * k / n
                y = y1 + (y2 - y1) * k / n
                pt = [round(round(x / STEP) * STEP, 2), round(round(y / STEP) * STEP, 2)]
                if not out or out[-1] != pt:
                    out.append(pt)
        if len(out) >= 3:
            rings.append(out)
            points += len(out)
    if rings:
        countries.append({"id": iso, "uk": iso == "GBR", "g": rings})

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("// Generated from Natural Earth 1:110m (public domain) for the opening animation. Do not edit by hand.\n")
    fh.write("window.RA_INTRO_GEO = ")
    json.dump(countries, fh, separators=(",", ":"))
    fh.write(";\n")
print("countries", len(countries), "points", points)
