"""Write data/countries.js (what the app needs: code, names, bounds, data files) from tools/countries.json (R-1).
Usage: python3 -I build_countries.py"""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(here, "countries.json"), encoding="utf-8"))["countries"]
pub = [{k: c[k] for k in ["code", "iso", "name", "name_zh", "short", "short_zh", "region_term", "bounds", "small_regions", "wash", "groups", "data", "open"] if k in c} for c in cfg]
with open(os.path.join(here, "..", "data", "countries.js"), "w", encoding="utf-8") as fh:
    fh.write("// Generated from tools/countries.json by tools/build_countries.py. Do not edit by hand.\n")
    fh.write("window.RA_COUNTRIES = " + json.dumps(pub, ensure_ascii=False, indent=1) + ";\n")
print("countries", [c["code"] for c in pub])
