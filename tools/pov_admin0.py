"""World outlines from China's point of view (decision 11-10), for build_geo.py (world) and build_intro_geo.py.

Natural Earth publishes its country layer in one version per point of view, but only at 1:10m. The atlas draws the
world from 1:50m (and the opening globe from 1:110m), so this script keeps those files and swaps in the China-view
shape only where the China view differs from Natural Earth's default: countries whose 1:10m default and China-view
shapes differ by more than MIN_DIFF square degrees take the China-view shape; countries the China view does not
have (Taiwan, Kosovo, Northern Cyprus, Somaliland ...) are dropped, their land already part of the country the China
view gives it to; Hong Kong and Macao, which the China view still lists apart as admin-1 regions, join China.
Every other country keeps its 1:50m (or 1:110m) shape untouched.

Usage: python3 -I tools/pov_admin0.py <base: ne_50m or ne_110m admin_0 countries> <ne_10m_admin_0_countries.geojson>
                                       <ne_10m_admin_0_countries_chn.geojson> <out.geojson> [--simplify D] [--min-area A]
  the atlas uses: 1:50m base with --simplify 0.02 --lines <maritime indicator chn>; 1:110m base with --simplify 0.1 --min-area 0.3
Needs shapely.
"""
import argparse
import json

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

ap = argparse.ArgumentParser()
ap.add_argument("base")
ap.add_argument("default10")
ap.add_argument("pov10")
ap.add_argument("out")
ap.add_argument("--simplify", type=float, default=0.0, help="degrees; simplify swapped-in shapes to match a coarser base")
ap.add_argument("--lines", help="ne_10m_admin_0_boundary_lines_maritime_indicator_chn.geojson: the South China Sea dashed line, passed through for the world map")
ap.add_argument("--min-area", type=float, default=0.0, help="square degrees; drop swapped-in islands smaller than this")
A = ap.parse_args()
MIN_DIFF = 0.05
JOIN = {"HKG": "CHN", "MAC": "CHN", "SCR": "CHN"}

load = lambda p: {f["properties"]["ADM0_A3"]: f for f in json.load(open(p, encoding="utf-8"))["features"]}
base, d10, p10 = load(A.base), load(A.default10), load(A.pov10)
swap = {}
for k, f in p10.items():
    if k in JOIN:
        continue
    if k in d10 and shape(f["geometry"]).symmetric_difference(shape(d10[k]["geometry"])).area <= MIN_DIFF:
        continue
    g = shape(f["geometry"])
    if k == "CHN":
        g = unary_union([g] + [shape(p10[j]["geometry"]) for j, to in JOIN.items() if to == k and j in p10])
    if A.min_area:
        parts = [q for q in getattr(g, "geoms", [g]) if q.area >= A.min_area]
        g = unary_union(parts) if parts else g
    swap[k] = g.simplify(A.simplify, preserve_topology=True) if A.simplify else g

out, dropped = [], []
for k, f in base.items():
    if k in JOIN or k not in p10:
        dropped.append(k)
        continue
    if k in swap:
        f = {"type": "Feature", "properties": f["properties"], "geometry": mapping(swap[k])}
    out.append(f)
if A.lines:
    for f in json.load(open(A.lines, encoding="utf-8"))["features"]:
        out.append({"type": "Feature", "properties": {"ra_sea_line": True, "note": f["properties"].get("NOTE")}, "geometry": f["geometry"]})
json.dump({"type": "FeatureCollection", "features": out}, open(A.out, "w", encoding="utf-8"), ensure_ascii=False)
print(f"{len(out)} countries; China-view shape for {', '.join(sorted(k for k in swap if k in base))}; dropped {', '.join(sorted(dropped))}")
