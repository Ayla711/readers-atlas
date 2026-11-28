"""11-27: photos for the new Colombian places of add_co_v2_1127.py: freely licensed Wikimedia Commons photos (CC0, public
domain, CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py).

Usage: python3 -I tools/content/batches/add_photos_co_v2_1127.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["co-orocue", "https://commons.wikimedia.org/wiki/File%3ALos_llanos_in_Orocue.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/21/Los_llanos_in_Orocue.jpg", "ednamortagui from Bogotá", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "Grassland of the Llanos at Orocué under a rainbow", "奥罗奎的大平原草地和彩虹"],
    ["co-cienaga", "https://commons.wikimedia.org/wiki/File%3APalacioAzul-Ci%C3%A9naga%2C_Magdalena-20251206.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/51/PalacioAzul-Ci%C3%A9naga%2C_Magdalena-20251206.jpg", "Jdvillalobos", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Palacio Azul, an old house on a street corner in Ciénaga", "谢纳加街角的老宅“蓝宫”"],
    ["co-medellin", "https://commons.wikimedia.org/wiki/File:Colombia_Medellin.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/61/Colombia_Medellin.jpg", "Mussi Katz", "CC0", "http://creativecommons.org/publicdomain/zero/1.0/deed.en", "Tower blocks of Medellín against the green slopes of the Aburrá valley", "阿布拉谷绿色山坡下麦德林的高楼"],
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
