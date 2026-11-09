"""Photo data for the 11-04 places. The images were resized on the user's computer (800 px wide, no metadata)
straight into images/places/<id>.jpg; this adds the photo field to places.js and the credits to photo-credits.md.
Usage: python3 -I add_photos3.py <app_dir> <candidates_json>"""
import json
import re
import sys
from PIL import Image

APP, CJ = sys.argv[1], sys.argv[2]
cands = json.load(open(CJ))
PICKS = {"bedford-gaol": 0}
ALT = {"bedford-gaol": ("The plaque in Silver Street marking the site of the Bedford County Gaol", "银街上标出贝德福德郡监狱旧址的纪念牌")}
s = open(f"{APP}/data/places.js", encoding="utf-8").read()
rows = []
for pid, n in PICKS.items():
    c = cands[pid]["candidates"][n]
    rel = f"images/places/{pid}.jpg"
    im = Image.open(f"{APP}/{rel}")
    assert im.width <= 800, (pid, im.size)
    photo = {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip(), "license": c["license"].strip(),
             "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": ALT[pid][0], "alt_zh": ALT[pid][1]}
    m = re.search(r'^  \{ id: "' + re.escape(pid) + r'",.*\}(?=,?\n)', s, re.M)
    assert m and "photo:" not in m.group(0), pid
    line = m.group(0)[:-2] + ", photo: " + json.dumps(photo, ensure_ascii=False) + " }"
    s = s[:m.start()] + line + s[m.end():]
    name = re.search(r'name: "([^"]+)"', line).group(1)
    rows.append(f"| {name} | {photo['author']} | [{photo['license']}]({photo['license_url']}) | [Commons]({photo['source']}) |")
open(f"{APP}/data/places.js", "w", encoding="utf-8").write(s)
cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
print("\n".join(rows))
