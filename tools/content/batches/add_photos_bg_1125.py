"""11-25: photos for the 6 Bulgarian places of add_bg1.py. One freely licensed Wikimedia Commons photo per place (CC0,
public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). None of the 6 is a pilgrimage or film place. Plovdiv's pin carries the 1932 aerial
photo of the tobacco district; Sofia's city-level pin carries Alexander Nevsky Cathedral.

Usage: python3 -I tools/content/batches/add_photos_bg_1125.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["bg-sopot", "https://commons.wikimedia.org/wiki/File%3AHouse-Museum_of_Ivan_Vazov_18.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/48/House-Museum_of_Ivan_Vazov_18.jpg", "vislupus", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The house where Ivan Vazov was born, now a museum, in Sopot", "索波特的伊万·伐佐夫故居博物馆"],
    ["bg-chepino", "https://commons.wikimedia.org/wiki/File%3AVelingrad_cloudy.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/2d/Velingrad_cloudy.jpg", "Klearchos Kapoutsis", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "Velingrad, of which Chepino is now a quarter, in the western Rhodopes", "西罗多彼山区的韦林格勒，切皮诺今天是它的一个区"],
    ["bg-plovdiv", "https://commons.wikimedia.org/wiki/File%3ATobacco_district_in_Plovdiv_1932.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/d0/Tobacco_district_in_Plovdiv_1932.jpg", "Unknown", "Public domain", "https://creativecommons.org/publicdomain/mark/1.0/", "Plovdiv's tobacco district from the air, 1932", "1932 年航拍的普罗夫迪夫烟草区"],
    ["bg-kazanlak", "https://commons.wikimedia.org/wiki/File%3AKazanlak_Center.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/16/Kazanlak_Center.jpg", "stealman", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The centre of Kazanlak", "卡赞勒克市中心"],
    ["bg-sofia", "https://commons.wikimedia.org/wiki/File%3AAlexander_Nevsky_Cathedral%2C_Sofia_%28by_Pudelek%29.JPG", "https://upload.wikimedia.org/wikipedia/commons/0/04/Alexander_Nevsky_Cathedral%2C_Sofia_%28by_Pudelek%29.JPG", "Marcin Szala", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Alexander Nevsky Cathedral, Sofia", "索非亚的亚历山大·涅夫斯基大教堂"],
    ["bg-ndk", "https://commons.wikimedia.org/wiki/File%3ANational_Palace_of_Culture%2C_Sofia_1.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/5d/National_Palace_of_Culture%2C_Sofia_1.jpg", "Ivano Giambattista", "CC0", "http://creativecommons.org/publicdomain/zero/1.0", "The National Palace of Culture, Sofia, at dusk", "黄昏时的索非亚国家文化宫"],
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
