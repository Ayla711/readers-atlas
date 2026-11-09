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
AUTHOR_FIX = {"leadenhall-market": "Diego Delso", "sherlock-museum": "Jordan 1972", "glenfinnan": "Nicolas17"}
LICENSE_URL_FALLBACK = {"Public domain": "https://en.wikipedia.org/wiki/Public_domain", "CC0": "https://creativecommons.org/publicdomain/zero/1.0/"}
ALT = {
    "bronte-parsonage": ("The Brontë Parsonage in Haworth", "霍沃斯的勃朗特故居"),
    "poets-corner": ("Monuments in Poets' Corner, Westminster Abbey", "威斯敏斯特教堂诗人角的纪念碑"),
    "shakespeare-birthplace": ("Shakespeare's Birthplace on Henley Street, Stratford-upon-Avon", "埃文河畔斯特拉特福亨利街的莎士比亚故居"),
    "dove-cottage": ("Dove Cottage, Grasmere", "格拉斯米尔的鸽舍"),
    "keats-house": ("Keats House, Hampstead", "汉普斯特德的济慈故居"),
    "chawton": ("Jane Austen's House, Chawton", "乔顿的简·奥斯汀故居"),
    "dickens-museum": ("The Charles Dickens Museum on Doughty Street", "道蒂街的狄更斯博物馆"),
    "sherlock-museum": ("The Sherlock Holmes Museum at 221B Baker Street", "贝克街 221B 的福尔摩斯博物馆"),
    "xu-zhimo-stone": ("The Xu Zhimo poem stone at King's College, Cambridge", "剑桥国王学院的徐志摩诗碑"),
    "lao-she-plaque": ("Lao She's blue plaque", "老舍故居的蓝色纪念牌"),
    "torquay": ("Torquay harbour", "托基港"),
    "greenway": ("Greenway House above the River Dart", "达特河畔的格林威庄园"),
    "cholsey-church": ("St Mary's Church, Cholsey", "乔尔西圣玛丽教堂"),
    "st-martins-theatre": ("St Martin's Theatre at night, with the sign for The Mousetrap", "夜晚的圣马丁剧院和《捕鼠器》招牌"),
    "cuckmere-cottages": ("The Coastguard Cottages at Cuckmere Haven, with the Seven Sisters cliffs", "卡克米尔港的海岸警卫小屋和七姐妹白崖"),
    "leadenhall-market": ("Leadenhall Market", "利德贺市场"),
    "christ-church": ("The Grand Staircase at Christ Church, Oxford", "牛津基督堂学院的大楼梯"),
    "alnwick-castle": ("Alnwick Castle", "阿尼克城堡"),
    "glenfinnan": ("A steam train crossing the Glenfinnan Viaduct", "蒸汽火车驶过格伦芬南高架桥"),
    "dyrham-park": ("The west front of Dyrham House", "德汉姆庄园西立面"),
    "chalcot-crescent": ("Chalcot Crescent, Primrose Hill", "樱草山的查尔科特新月街"),
    "doune-castle": ("Doune Castle", "杜恩城堡"),
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
