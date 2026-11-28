"""11-27: photos for the new Peruvian places of add_pe_v2_1127.py: freely licensed Wikimedia Commons photos (CC0, public
domain, CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py).

Usage: python3 -I tools/content/batches/add_photos_pe_v2_1127.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["pe-country-club-lima", "https://commons.wikimedia.org/wiki/File%3AHotel_Country_Club_de_Lima_3gg.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/ba/Hotel_Country_Club_de_Lima_3gg.jpg", "Rdrg109", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Country Club Lima Hotel at night, seen across its lawn", "夜色中隔着草坪看利马乡村俱乐部酒店"],
    ["pe-huamachuco", "https://commons.wikimedia.org/wiki/File%3AHuamachuco-_Plaza_de_Armas_%26_Gallardete.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9d/Huamachuco-_Plaza_de_Armas_%26_Gallardete.jpg", "David Almeida from Lima, Peru", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "The Plaza de Armas of Huamachuco with its flagpole", "瓦马丘科的武器广场和旗杆"],
    ["pe-abancay", "https://commons.wikimedia.org/wiki/File%3APlaza_de_Armas_de_Abancay.JPG", "https://upload.wikimedia.org/wikipedia/commons/6/61/Plaza_de_Armas_de_Abancay.JPG", "Vcardenas", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The main square of Abancay", "阿班凯的中心广场"],
    ["pe-huaca-pucllana", "https://commons.wikimedia.org/wiki/File%3AHuaca_Pucllana-nX-28.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f0/Huaca_Pucllana-nX-28.jpg", "PsamatheM", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The stepped adobe walls of Huaca Pucllana, Miraflores", "米拉弗洛雷斯普克亚纳神庙的阶梯状土坯墙"],
    ["pe-plaza-san-martin", "https://commons.wikimedia.org/wiki/File%3APlaza_San_Mart%C3%ADn%2C_Lima_Peru.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/06/Plaza_San_Mart%C3%ADn%2C_Lima_Peru.jpg", "Ministerio de Defensa del Perú", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "The Plaza San Martín, Lima, from the air", "鸟瞰利马圣马丁广场"],
    ["pe-hotel-paracas", "https://commons.wikimedia.org/wiki/File%3AParacas_bay_-_Peru.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/3e/Paracas_bay_-_Peru.jpg", "Inti Runa", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "Fishing boats on the bay of Paracas, below the desert cliffs", "帕拉卡斯湾的渔船和沙漠悬崖"],
    ["pe-huancayo", "https://commons.wikimedia.org/wiki/File%3APlaza_de_armas_de_Huancayo_-_panoramio.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/50/Plaza_de_armas_de_Huancayo_-_panoramio.jpg", "Heiner Amado Cadillo", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Plaza de Armas and cathedral of Huancayo", "万卡约的武器广场和主教座堂"],
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
