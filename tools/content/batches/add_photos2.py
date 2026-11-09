"""Add one freely licensed photo to each pilgrimage and film-location place.
Images: resized to 800 px wide, metadata stripped, saved to images/places/<id>.jpg.
Data: places.js gets photo: {file, author, license, license_url, source, alt_en, alt_zh}.
Usage: python3 -I add_photos.py <app_dir> <picks_json>"""
import json
import os
import re
import sys
from PIL import Image

APP, PJ = sys.argv[1], sys.argv[2]
picks = json.load(open(PJ))
AUTHOR_FIX = {"top-withens": "Dave Dunford"}
LICENSE_URL_FALLBACK = {"Public domain": "https://en.wikipedia.org/wiki/Public_domain", "CC0": "https://creativecommons.org/publicdomain/zero/1.0/"}
ALT = {
    "stoke-poges": ("St Giles' Church, Stoke Poges", "斯托克波吉斯的圣贾尔斯教堂"),
    "top-withens": ("The ruins of Top Withens on Haworth Moor", "霍沃斯荒原上的托普威森斯废墟"),
    "glencoyne-bay": ("Ullswater from Glencoyne Bay", "从格伦科因湾望阿尔斯沃特湖"),
    "chatsworth": ("Chatsworth House", "查茨沃斯庄园"),
    "preston": ("The Harris Museum, Preston", "普雷斯顿的哈里斯博物馆"),
    "cooling-church": ("St James' Church, Cooling", "库林的圣詹姆斯教堂"),
    "knutsford": ("King Street, Knutsford", "纳茨福德的国王街"),
    "gainsborough": ("The River Trent at Gainsborough", "盖恩斯伯勒的特伦特河"),
    "eastwood": ("The D. H. Lawrence Birthplace Museum, Eastwood", "伊斯特伍德的劳伦斯出生地博物馆"),
    "burslem": ("The Royal Doulton factory, Burslem", "伯斯勒姆的皇家道尔顿陶瓷厂"),
    "whitby": ("Whitby harbour, with the abbey on the cliff above", "惠特比港，崖上是修道院"),
    "scarborough": ("Scarborough's South Bay at night", "夜晚的斯卡伯勒南湾"),
    "clava-cairns": ("A cairn and standing stone at Clava", "克拉瓦的石冢和立石"),
    "burgh-island": ("Burgh Island and its hotel, seen from the mainland", "从岸上望伯格岛和岛上的酒店"),
}

os.makedirs(f"{APP}/images/places", exist_ok=True)
s = open(f"{APP}/data/places.js", encoding="utf-8").read()
for pid, c in picks.items():
    im = Image.open(c["thumb"]).convert("RGB")
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    rel = f"images/places/{pid}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)  # no EXIF carried over
    photo = {
        "file": rel, "width": im.width, "height": im.height,
        "author": AUTHOR_FIX.get(pid, c["author"]).strip(),
        "license": c["license"].strip(),
        "license_url": c["license_url"].strip() or LICENSE_URL_FALLBACK.get(c["license"].strip(), c["page"]),
        "source": c["page"],
        "alt_en": ALT[pid][0], "alt_zh": ALT[pid][1],
    }
    m = re.search(r'^  \{ id: "' + re.escape(pid) + r'",.*\}(?=,?\n)', s, re.M)
    assert m, pid
    line = m.group(0)
    assert "photo:" not in line, pid
    line = line[:-2] + ", photo: " + json.dumps(photo, ensure_ascii=False) + " }"
    s = s[:m.start()] + line + s[m.end():]
    print(f"{pid:22} {im.width}x{im.height} {os.path.getsize(f'{APP}/{rel}') // 1024} KB")
open(f"{APP}/data/places.js", "w", encoding="utf-8").write(s)
