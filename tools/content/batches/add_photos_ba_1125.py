"""11-25: photos for the 3 Bosnian places of add_ba1.py. One freely licensed Wikimedia Commons photo per place (CC0,
public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). None of the 3 is a pilgrimage or film place. Sarajevo's city-level pin carries
Baščaršija, the old Ottoman market with the Sebilj fountain.

Usage: python3 -I tools/content/batches/add_photos_ba_1125.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["ba-visegrad-bridge", "https://commons.wikimedia.org/wiki/File%3AMehmed_Pa%C5%A1a_Sokolovi%C4%87_Bridge%2C_Vi%C5%A1egrad.JPG", "https://upload.wikimedia.org/wikipedia/commons/c/c9/Mehmed_Pa%C5%A1a_Sokolovi%C4%87_Bridge%2C_Vi%C5%A1egrad.JPG", "Marcin Szala", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Mehmed Paša Sokolović Bridge over the Drina at Višegrad", "维舍格拉德德里纳河上的穆罕默德-帕夏·索科洛维奇桥"],
    ["ba-sarajevo", "https://commons.wikimedia.org/wiki/File%3ABa%C5%A1%C4%8Dar%C5%A1ija_2014.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/41/Ba%C5%A1%C4%8Dar%C5%A1ija_2014.jpg", "Choinowski", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Baščaršija, Sarajevo's old market, with the Sebilj fountain", "萨拉热窝老集市巴什查尔希亚和塞比利喷泉亭"],
    ["ba-travnik", "https://commons.wikimedia.org/wiki/File%3AView_over_Travnik.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/31/View_over_Travnik.jpg", "Kondephy", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "A view over Travnik", "俯瞰特拉夫尼克"],
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
