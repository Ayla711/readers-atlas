"""Build the map geometry for The Reader's Atlas (R-2: one run per country, configured in tools/countries.json).

Inputs (Natural Earth, public domain):
  ne_10m_admin_1_states_provinces.geojson  -> a country's admin-1 units, folded into regions per the config
  ne_50m_admin_0_countries.geojson         -> world outlines (all countries; the app hides the one it is showing)
Usage:
  python3 -I build_geo.py <admin1.geojson> <admin0.geojson> <country code> <out.js>   -> window.RA_GEO = {regions, units}
  python3 -I build_geo.py <admin1.geojson> <admin0.geojson> world <out.js>            -> window.RA_WORLD = [...]
"""
import json
import os
import sys
from collections import Counter, defaultdict

ADMIN1, ADMIN0, WHICH, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
CONFIG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "countries.json"), encoding="utf-8"))["countries"]


def q(v, step):
    return round(round(v / step) * step, 4)


def polygons(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon":
        return geom["coordinates"]
    return []


def clean_ring(ring, step):
    out = []
    for x, y in ring:
        p = (q(x, step), q(y, step))
        if not out or out[-1] != p:
            out.append(p)
    if len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out if len(out) >= 3 else None


def ring_area(r):
    a = 0.0
    for i in range(len(r)):
        x1, y1 = r[i]
        x2, y2 = r[(i + 1) % len(r)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2


def dp(points, eps):
    """Douglas-Peucker on an open polyline."""
    if len(points) < 3:
        return points
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        s, e = stack.pop()
        (x1, y1), (x2, y2) = points[s], points[e]
        dx, dy = x2 - x1, y2 - y1
        norm = (dx * dx + dy * dy) ** 0.5 or 1e-12
        best, idx = 0.0, None
        for i in range(s + 1, e):
            x0, y0 = points[i]
            d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
            if d > best:
                best, idx = d, i
        if idx is not None and best > eps:
            keep[idx] = True
            stack.append((s, idx))
            stack.append((idx, e))
    return [p for p, k in zip(points, keep) if k]


def dp_any(points, eps):
    """Douglas-Peucker that also handles closed lines (first point == last)."""
    if len(points) >= 4 and points[0] == points[-1]:
        x0, y0 = points[0]
        far = max(range(1, len(points) - 1),
                  key=lambda i: (points[i][0] - x0) ** 2 + (points[i][1] - y0) ** 2)
        return dp(points[: far + 1], eps)[:-1] + dp(points[far:], eps)
    return dp(points, eps)


def chain(segments):
    """Join undirected segments into polylines."""
    adj = defaultdict(list)
    for a, b in segments:
        adj[a].append(b)
        adj[b].append(a)
    used = set()
    lines = []

    def key(a, b):
        return (a, b) if a <= b else (b, a)

    starts = [p for p in adj if len(adj[p]) != 2] + list(adj.keys())
    for s in starts:
        for n in adj[s]:
            if key(s, n) in used:
                continue
            line = [s, n]
            used.add(key(s, n))
            cur, prev = n, s
            while True:
                nxt = [m for m in adj[cur] if key(cur, m) not in used]
                if not nxt or len(adj[cur]) != 2:
                    break
                m = nxt[0]
                used.add(key(cur, m))
                line.append(m)
                prev, cur = cur, m
                if cur == s:
                    break
            lines.append(line)
    return lines



def build_world():
    STEP_W = 0.03
    a0 = json.load(open(ADMIN0))
    world, sea_lines = [], []
    for f in a0["features"]:
        p = f["properties"]
        if p.get("ra_sea_line"):   # the South China Sea dashed line (tools/pov_admin0.py --lines), one feature per dash
            sea_lines.append([[round(x, 3), round(y, 3)] for x, y in f["geometry"]["coordinates"]])
            continue
        iso = p.get("ADM0_A3")
        if iso == "ATA":
            continue
        rings_out = []
        for poly in polygons(f["geometry"]):
            r = clean_ring(poly[0], STEP_W)
            if not r or ring_area(r) < 0.02:
                continue
            r = dp_any(r + [r[0]], STEP_W * 0.7)[:-1]
            if len(r) >= 3:
                rings_out.append([list(pt) for pt in r])
        if rings_out:
            world.append({"id": iso, "name": p.get("NAME"), "name_zh": p.get("NAME_ZH"), "g": rings_out})
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("// Generated from Natural Earth (public domain) by tools/build_geo.py. Do not edit by hand.\n")
        fh.write("window.RA_WORLD = ")
        json.dump(world, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write(";\n")
        own = own_borders()
        if own:
            fh.write("window.RA_WORLD_OWN = ")
            json.dump(own, fh, separators=(",", ":"))
            fh.write(";\n")
        if sea_lines:
            fh.write("window.RA_WORLD_LINES = ")
            json.dump(sea_lines, fh, separators=(",", ":"))
            fh.write(";\n")
    print("world countries", len(world), "sea lines", len(sea_lines))


def own_borders():
    """A country drawn from its own point of view (tools/cn_admin1.py, given here as the admin-1 file) supplies its
    land border as it sees it and the area where the basemap's de facto national borders give way to it."""
    out = []
    try:
        a1 = json.load(open(ADMIN1))
    except (OSError, ValueError):
        return out
    for f in a1["features"]:
        p = f["properties"]
        if p.get("ra_land_border"):
            step, lines = 0.02, []
            for line in ([f["geometry"]["coordinates"]] if f["geometry"]["type"] == "LineString" else f["geometry"]["coordinates"]):
                pts = []
                for x, y in line:
                    pt = [q(x, step), q(y, step)]
                    if not pts or pts[-1] != pt:
                        pts.append(pt)
                if len(pts) >= 2:
                    lines.append(pts)
            out.append({"iso": p["adm0_a3"], "land_border": lines})
    for f in a1["features"]:
        p = f["properties"]
        if p.get("ra_border_area"):
            area = [[[[round(x, 2), round(y, 2)] for x, y in ring] for ring in poly] for poly in polygons(f["geometry"])]
            for o in out:
                if o["iso"] == p["adm0_a3"]:
                    o["border_area"] = area
    return out


def region_of(p, cfg):
    rc = cfg["regions"]
    if rc["mode"] == "merge":
        for rule in rc["by"]:
            rid = rule["map"].get(p.get(rule["field"]))
            if rid:
                return rid
        return None
    rid = p.get(rc["id_field"]) or ""
    return rid[len(rc.get("id_strip", "")):] if rid.startswith(rc.get("id_strip", "")) else rid


def build_country(cfg):
    step = cfg.get("step", 0.004)
    a1 = json.load(open(ADMIN1))
    units = []
    edges = defaultdict(Counter)
    names = {}
    if cfg["regions"]["mode"] == "merge":
        names = {k: tuple(v) for k, v in cfg["regions"]["names"].items()}
    bbox = defaultdict(lambda: [180, 90, -180, -90])
    area_sum = defaultdict(float)
    cent = defaultdict(lambda: [0.0, 0.0])
    for f in a1["features"]:
        p = f["properties"]
        if p.get("adm0_a3") != cfg["iso"]:
            continue
        if p.get("ra_land_border") or p.get("ra_border_area"):   # go to data/world-geo.js (build_world)
            continue
        rid = region_of(p, cfg)
        if not rid:
            raise SystemExit(f"unmapped unit: {p.get('name')}")
        if cfg["regions"]["mode"] == "units":
            names[rid] = (p.get(cfg["regions"]["name_field"]), p.get(cfg["regions"].get("name_zh_field", "")) or p.get(cfg["regions"]["name_field"]))
        rings_out = []
        for poly in polygons(f["geometry"]):
            # islands across the antimeridian (the western Aleutians) would stretch the country over the whole map
            if "drop_rings_lon_gt" in cfg and any(x > cfg["drop_rings_lon_gt"] for x, _ in poly[0]):
                continue
            for k, ring in enumerate(poly):
                r = clean_ring(ring, step)
                if not r:
                    continue
                for i in range(len(r)):
                    a, b = r[i], r[(i + 1) % len(r)]
                    edges[rid][(a, b) if a <= b else (b, a)] += 1
                if k == 0:
                    ar = ring_area(r)
                    area_sum[rid] += ar
                    cx = sum(x for x, _ in r) / len(r)
                    cy = sum(y for _, y in r) / len(r)
                    cent[rid][0] += cx * ar
                    cent[rid][1] += cy * ar
                    bb = bbox[rid]
                    for x, y in r:
                        bb[0], bb[1] = min(bb[0], x), min(bb[1], y)
                        bb[2], bb[3] = max(bb[2], x), max(bb[3], y)
                rings_out.append([list(pt) for pt in r])
        rings_out = [r for r in rings_out if len(r) >= 3]
        units.append({"r": rid, "n": p.get("name"), "g": rings_out})

    regions = []
    order = list(cfg["regions"]["names"].keys()) if cfg["regions"]["mode"] == "merge" else sorted(names)
    for rid in order:
        en, zh = names[rid]
        segs = [e for e, c in edges[rid].items() if c == 1]
        lines = chain(segs)
        lines = [[list(pt) for pt in l] for l in lines if len(l) >= 2]
        a = area_sum[rid] or 1
        regions.append({
            "id": rid, "name": en, "name_zh": zh,
            "outline": lines,
            "centroid": [round(cent[rid][0] / a, 3), round(cent[rid][1] / a, 3)],
            "bbox": [round(v, 3) for v in bbox[rid]],
        })
    out = {"country": cfg["code"], "regions": regions, "units": units}
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("// Generated from Natural Earth (public domain) by tools/build_geo.py. Do not edit by hand.\n")
        fh.write("window.RA_GEO = ")
        json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write(";\n")
    print(cfg["code"], "units", len(units), "regions", len(regions))
    for r in regions:
        print(" ", r["id"], r["name"], "outline lines", len(r["outline"]), "pts", sum(len(l) for l in r["outline"]), r["centroid"])


if WHICH == "world":
    build_world()
else:
    cfg = next((c for c in CONFIG if c["code"] == WHICH), None)
    if not cfg:
        raise SystemExit(f"no country {WHICH} in tools/countries.json")
    build_country(cfg)
