"""Photo data for the 11-04 places. The images were resized on the user's computer (800 px wide, no metadata)
straight into images/places/<id>.jpg; this adds the photo field to places.js and the credits to photo-credits.md.
Usage: python3 -I add_photos3.py <app_dir> <candidates_json>"""
import json
import re
import sys
from PIL import Image

APP, CJ = sys.argv[1], sys.argv[2]
cands = json.load(open(CJ))
PICKS = {"godstow": 1, "daresbury": 2, "carroll-grave": 0, "north-lees-hall": 3, "cowan-bridge": 3, "quarry-wood": 0, "peter-pan-statue": 0, "hardys-cottage": 2}
ALT = {
    "godstow": ("The ruins of Godstow Abbey by the Thames", "泰晤士河边的戈斯托修道院遗址"),
    "daresbury": ("All Saints' Church, Daresbury, and its churchyard", "达斯伯里诸圣堂和墓园"),
    "carroll-grave": ("The Dodgson family graves in the Mount Cemetery, Guildford", "吉尔福德山丘公墓里的道奇森家族墓"),
    "north-lees-hall": ("North Lees Hall, a stone tower house above Hathersage", "哈瑟塞奇山坡上的石砌塔楼诺斯利斯庄园"),
    "cowan-bridge": ("The former Clergy Daughters' School building at Cowan Bridge", "考恩桥牧师女儿学校的旧校舍"),
    "quarry-wood": ("A path climbing through Quarry Wood, Cookham Dean", "穿过库克姆迪恩采石场林的上坡小路"),
    "peter-pan-statue": ("George Frampton's Peter Pan statue in Kensington Gardens", "肯辛顿公园里乔治·弗兰普顿塑造的彼得·潘雕像"),
    "hardys-cottage": ("Hardy's Cottage, the thatched house where he was born", "哈代出生的茅草顶小屋"),
}
s = open(f"{APP}/data/places.js", encoding="utf-8").read()
rows = []
for pid, n in PICKS.items():
    c = cands[pid]["candidates"][n]
    rel = f"images/places/{pid}.jpg"
    im = Image.open(f"{APP}/{rel}")
    assert im.width == 800, (pid, im.size)
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
