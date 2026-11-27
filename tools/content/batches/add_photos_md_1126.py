"""11-26: photos for the Moldovan places of add_md1.py: freely licensed Wikimedia Commons photos (CC0, public domain,
CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). Mana and Mălăiești have none: the Mălăiești photos found show the Mălăiești of
Rîșcani district or the fortress of Mălăiești in Romania, and the photos of Mana show its cemeteries or Goma's portrait on
a memorial plaque. Horodiște's church was checked by its heritage code (MD-DN, Dondușeni), as another Horodiște lies in
Rîșcani district. The Codreanca photo's author signs "Ion Chibzii from Chisinau"; the credit gives the name.

Usage: python3 -I tools/content/batches/add_photos_md_1126.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["md-untesti", "https://commons.wikimedia.org/wiki/File%3ABiserica_%E2%80%9ETo%C8%9Bi_Sfin%C8%9Bii%E2%80%9D_din_sat._Un%C8%9Be%C8%99ti_01.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/da/Biserica_%E2%80%9ETo%C8%9Bi_Sfin%C8%9Bii%E2%80%9D_din_sat._Un%C8%9Be%C8%99ti_01.jpg", "Vladikh", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "A street in Unțești with the Church of All Saints", "温采什蒂村的街道和诸圣教堂"],
    ["md-horodiste", "https://commons.wikimedia.org/wiki/File%3ABiserica_%E2%80%9ESf._Treime%E2%80%9D_din_Horodi%C8%99te.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b0/Biserica_%E2%80%9ESf._Treime%E2%80%9D_din_Horodi%C8%99te.jpg", "Tatiana Beghiu", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The wooden Church of the Holy Trinity, Horodiște", "霍罗迪什泰的木结构圣三一教堂"],
    ["md-codreanca", "https://commons.wikimedia.org/wiki/File%3AThe_surroundings_of_the_Codreanca_village_%281980%29._%2824503778619%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7a/The_surroundings_of_the_Codreanca_village_%281980%29._%2824503778619%29.jpg", "Ion Chibzii", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "The country around Codreanca, 1980", "1980 年科德良卡村周围的田野"],
]

def thumb(u):
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+)$", u)
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/{m.group(3)}/960px-{m.group(3)}" if m else u

def image(pid, url):
    if CACHE and os.path.exists(os.path.join(CACHE, pid + ".jpg")):
        return Image.open(os.path.join(CACHE, pid + ".jpg"))
    f = os.path.join(APP, "images", "places", pid + ".download")
    for u in (thumb(url), url):
        try:
            open(f, "wb").write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()); break
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(60)
    time.sleep(4)
    im = Image.open(f); im.load(); os.replace(f, f + ".done"); return im

def write(path, s):
    open(path + ".new", "w", encoding="utf-8").write(s); os.replace(path + ".new", path)

assert len({p[0] for p in PHOTOS}) == len(PHOTOS)
files = {}
for pid, page, url, author, lic, lic_url, alt_en, alt_zh in PHOTOS:
    pp = os.path.join(APP, "data", pid.split("-")[0], "places.js")
    s = files.get(pp) or open(pp, encoding="utf-8").read()
    m = re.search(r'(\{ id: "' + re.escape(pid) + r'".*?)( \},?\n)', s)
    assert m, pid
    assert "photo:" not in m.group(1), pid + ": already has a photo"
    im = image(pid, url).convert("RGB")
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, pid
    rel = f"images/places/{pid}.jpg"
    im.save(os.path.join(APP, rel), "JPEG", quality=82, optimize=True, progressive=True)  # no EXIF carried over
    photo = {"file": rel, "width": im.width, "height": im.height, "author": author, "license": lic, "license_url": lic_url,
             "source": page, "alt_en": alt_en, "alt_zh": alt_zh}
    files[pp] = s[:m.end(1)] + ", photo: " + json.dumps(photo, ensure_ascii=False) + s[m.end(1):]
    name = re.search(r'name: "([^"]*)"', m.group(1)).group(1)
    files.setdefault("credits", []).append(f"| {name} | {author} | [{lic}]({lic_url}) | [Commons]({page}) |")
for pp, s in files.items():
    if pp != "credits": write(pp, s)
cred = os.path.join(APP, "docs", "photo-credits.md")
write(cred, open(cred, encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(files["credits"]) + "\n")
print(len(files["credits"]), "photos attached")
