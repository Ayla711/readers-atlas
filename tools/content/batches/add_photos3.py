"""Photo data for the 11-04 places. The images were resized on the user's computer (800 px wide, no metadata)
straight into images/places/<id>.jpg; this adds the photo field to places.js and the credits to photo-credits.md.
Usage: python3 -I add_photos3.py <app_dir> <candidates_json>"""
import json
import re
import sys
from PIL import Image

APP, CJ = sys.argv[1], sys.argv[2]
cands = json.load(open(CJ))
PICKS = {"lyme-park": 1, "castle-howard": 1, "dark-hedges": 0, "dylan-thomas-boathouse": 0, "abbotsford": 3, "dr-johnsons-house": 0,
         "gloucester-cathedral": 0, "clachaig-gully": 3, "steall-falls": 3, "claremont-square": 0, "millennium-bridge": 0,
         "freshwater-west": 2, "malham-cove": 0, "lavenham": 0}
ALT = {
    "lyme-park": ("The south front of Lyme Park reflected in the lake", "倒映在湖中的莱姆庄园南立面"),
    "castle-howard": ("Castle Howard and its dome", "霍华德城堡和它的穹顶"),
    "dark-hedges": ("The avenue of beech trees on Bregagh Road", "布雷加路两旁的山毛榉林荫道"),
    "dylan-thomas-boathouse": ("The Boathouse above the Taf estuary at Laugharne", "拉恩塔夫河口上方的船屋"),
    "abbotsford": ("The front of Abbotsford House", "阿博茨福德宅第正面"),
    "dr-johnsons-house": ("Gough Square, with Dr Johnson's House", "高夫广场和约翰生博士故居"),
    "gloucester-cathedral": ("The fan-vaulted cloisters of Gloucester Cathedral", "格洛斯特大教堂扇形拱顶的回廊"),
    "clachaig-gully": ("The road from the Clachaig Inn into Glen Coe", "从克拉哈格旅店通往格伦科的路"),
    "steall-falls": ("Steall Falls in upper Glen Nevis", "尼维斯谷上游的斯蒂尔瀑布"),
    "claremont-square": ("The terraced houses of Claremont Square", "克莱蒙特广场的排屋"),
    "millennium-bridge": ("The Millennium Bridge, with St Paul's Cathedral behind", "千禧桥，后面是圣保罗大教堂"),
    "freshwater-west": ("The northern end of Freshwater West beach", "弗雷什沃特西海滩北端"),
    "malham-cove": ("The limestone cliff of Malham Cove", "马勒姆湾的石灰岩崖壁"),
    "lavenham": ("De Vere House, Lavenham", "拉文纳姆的德维尔宅"),
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
