"""China's provincial units, drawn from China's point of view (decision 11-10: the map follows Natural Earth's China
view, the version Natural Earth publishes for each country's own claims).

Natural Earth's admin-1 layer follows de facto control: Taiwan, Hong Kong and Macao are separate countries there,
the Paracels a unit of their own, and the land China claims along the Indian border lies outside every Chinese unit.
This script takes those units and refolds them into China's 34 provincial-level divisions:
  mainland units                    -> their province (ISO 3166-2 code without "CN-"); the Paracels -> Hainan
  Taiwan's 21 units                 -> TW, Hong Kong's 18 -> HK, Macao -> MO
  China-view outline minus all that -> each leftover piece to a named province (RULES below), or, for slivers along
                                       a border, to the province it touches most
Output: a GeoJSON of units with adm0_a3 "CHN" and a field ra_region, read by build_geo.py like any admin-1 file, plus
  - China's land border as China sees it (lines, ra_land_border): once the street basemap is on, the app draws this
    instead of OpenStreetMap's national borders, which follow de facto control
  - the area where OpenStreetMap's national borders are hidden (one polygon, ra_border_area): China plus a margin

Usage: python3 -I tools/cn_admin1.py <ne_10m_admin_1_states_provinces.geojson> <ne_10m_admin_0_countries_chn.geojson> <out.geojson>
Needs shapely (pip install shapely).
"""
import json
import sys

from shapely.geometry import mapping, shape, box
from shapely.ops import linemerge, unary_union

A1, POV, OUT = sys.argv[1:4]
# leftover pieces of the China-view outline, by where they lie: (lon0, lat0, lon1, lat1) -> province
RULES = [
    ((88.5, 26.0, 97.5, 29.6), "XZ", "Zangnan (south of the McMahon Line), administered by China's view as part of Xizang"),
    ((77.5, 29.5, 81.5, 34.0), "XZ", "western and middle sectors of the Indian border, part of Ngari, Xizang in China's view"),
    ((123.0, 25.4, 124.8, 26.0), "TW", "Diaoyu Islands, part of Taiwan in China's view"),
    ((108.0, 3.0, 119.0, 17.5), "HI", "South China Sea islands, part of Hainan (Sansha) in China's view"),
]
MIN_PIECE = 1e-5   # square degrees; smaller leftovers are rounding noise

a1 = json.load(open(A1, encoding="utf-8"))["features"]
pov = next(shape(f["geometry"]) for f in json.load(open(POV, encoding="utf-8"))["features"] if f["properties"]["ADM0_A3"] == "CHN")
pov_extra = [shape(f["geometry"]) for f in json.load(open(POV, encoding="utf-8"))["features"]
             if f["properties"]["ADM0_A3"] in ("HKG", "MAC", "SCR")]   # SCR: Scarborough Shoal, separate in every view
china = unary_union([pov] + pov_extra)

units = []
for f in a1:
    p = f["properties"]
    a3 = p["adm0_a3"]
    if a3 == "CHN":
        rid = "HI" if p["name"] == "Paracel Islands" else p["iso_3166_2"].replace("CN-", "")
    elif a3 in ("TWN", "HKG", "MAC"):
        rid = {"TWN": "TW", "HKG": "HK", "MAC": "MO"}[a3]
    else:
        continue
    units.append({"rid": rid, "name": p["name"], "name_zh": p["name_zh"], "g": shape(f["geometry"])})

covered = unary_union([u["g"] for u in units])
left = china.difference(covered)
pieces = list(getattr(left, "geoms", [left]))
by_region = {}
for u in units:
    by_region.setdefault(u["rid"], []).append(u["g"])
region_shape = {k: unary_union(v) for k, v in by_region.items()}
log, slivers = [], 0
for g in pieces:
    if g.is_empty or g.area < MIN_PIECE:
        continue
    c = g.representative_point()
    rule = next((r for r in RULES if box(*r[0]).contains(c)), None)
    if rule:
        rid, why = rule[1], rule[2]
    elif g.area < 0.01:
        rid = max(region_shape, key=lambda k: region_shape[k].buffer(0.01).intersection(g).area)
        why, slivers = None, slivers + 1
    else:
        raise SystemExit(f"leftover piece of {g.area:.3f} sq deg at {c.x:.2f},{c.y:.2f} has no rule; add one to RULES")
    if why:
        log.append(f"  {rid}  {g.area:7.3f} sq deg at {c.x:.2f},{c.y:.2f}  {why}")
    units.append({"rid": rid, "name": "china-view " + rid, "name_zh": "", "g": g})

feats = [{"type": "Feature", "properties": {"adm0_a3": "CHN", "ra_region": u["rid"], "name": u["name"], "name_zh": u["name_zh"]},
          "geometry": mapping(u["g"])} for u in units]

# land border: the parts of China's outline that touch another country (the rest is coast)
others = unary_union([shape(f["geometry"]) for f in json.load(open(POV, encoding="utf-8"))["features"]
                      if f["properties"]["ADM0_A3"] not in ("CHN", "HKG", "MAC", "SCR")])
near = others.buffer(0.03)
land = linemerge(china.boundary.intersection(near))
land_lines = [l for l in getattr(land, "geoms", [land]) if l.length > 0.05]
feats.append({"type": "Feature", "properties": {"adm0_a3": "CHN", "ra_land_border": True},
              "geometry": mapping(unary_union(land_lines))})
area = china.buffer(0.15).simplify(0.05)
feats.append({"type": "Feature", "properties": {"adm0_a3": "CHN", "ra_border_area": True}, "geometry": mapping(area)})
json.dump({"type": "FeatureCollection", "features": feats}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
print(f"{len(feats)} units in {len({u['rid'] for u in units})} provinces; leftovers assigned by rule:")
print("\n".join(log))
print(f"  plus {slivers} border slivers given to the province they touch")
print(f"land border: {len(land_lines)} lines, {sum(l.length for l in land_lines):.0f} degrees long; basemap-border area: {len(mapping(area)['coordinates'])} polygon(s)")
