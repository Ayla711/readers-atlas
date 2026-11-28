"""11-27: photos for the new Argentine places of add_ar_v2_1127.py: freely licensed Wikimedia Commons photos (CC0, public
domain, CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py).

Usage: python3 -I tools/content/batches/add_photos_ar_v2_1127.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["ar-mar-del-plata", "https://commons.wikimedia.org/wiki/File%3ACasino_Central_de_Mar_del_Plata.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/0b/Casino_Central_de_Mar_del_Plata.jpg", "Mar del Plata Puntonoticias", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "The Casino Central on the seafront at Mar del Plata", "马德普拉塔海滨的中央赌场"],
    ["ar-buenos-aires", "https://commons.wikimedia.org/wiki/File%3ABuenos_Aires-Avenida_de_Mayo_y_Per%C3%BA.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/84/Buenos_Aires-Avenida_de_Mayo_y_Per%C3%BA.jpg", "Roberto Fiadone", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "Avenida de Mayo, Buenos Aires, from the corner of Perú street", "布宜诺斯艾利斯五月大道，从秘鲁街口望去"],
    ["ar-resistencia", "https://commons.wikimedia.org/wiki/File%3ACasadegobiernodelchaco.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1c/Casadegobiernodelchaco.jpg", "Fernando Pascullo", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "The Chaco Government House seen from Plaza 25 de Mayo, Resistencia", "从五月二十五日广场看查科省政府大楼，雷西斯滕西亚"],
    ["ar-colastine", "https://commons.wikimedia.org/wiki/File%3AR%C3%ADo_Colastin%C3%A9_-_San_Jos%C3%A9_del_Rinc%C3%B3n_3.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/fe/R%C3%ADo_Colastin%C3%A9_-_San_Jos%C3%A9_del_Rinc%C3%B3n_3.jpg", "TitiNicola", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Colastiné river at San José del Rincón, Santa Fe", "圣菲省圣何塞德尔林孔附近的科拉斯廷河"],
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
