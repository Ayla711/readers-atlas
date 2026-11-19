"""Write data/countries.js (what the app needs: code, names, bounds, data files) from tools/countries.json (R-1),
plus the totals over every open country that the world page shows (counted by tools/world_stats.js).
Usage: python3 -I build_countries.py"""
import json, os, subprocess
here = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(here, "countries.json"), encoding="utf-8"))["countries"]
pub = [{k: c[k] for k in ["code", "iso", "name", "name_zh", "short", "short_zh", "region_term", "bounds", "small_regions", "wash", "groups", "data", "open"] if k in c} for c in cfg]
out = os.path.join(here, "..", "data", "countries.js")
def write(stats):
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("// Generated from tools/countries.json by tools/build_countries.py. Do not edit by hand.\n")
        fh.write("window.RA_COUNTRIES = " + json.dumps(pub, ensure_ascii=False, indent=1) + ";\n")
        if stats:
            fh.write("// Totals over every open country, for the world page.\n")
            fh.write("window.RA_WORLD_STATS = " + json.dumps(stats) + ";\n")
write(None)  # the country list first: the counter reads it to find the data files
stats = json.loads(subprocess.run(["node", os.path.join(here, "world_stats.js"), os.path.join(here, "..")],
                                  check=True, capture_output=True, text=True).stdout)
write(stats)
print("countries", [c["code"] for c in pub], "world", stats)
