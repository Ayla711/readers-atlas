"""11-25: photos for the Estonian places of add_ee1.py: freely licensed Wikimedia Commons photos (CC0, public domain,
CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). No usable photo was found for Võisiku manor (only CC BY-SA 3.0 EE). Tallinn,
a city-level pin for a book that names no place, has none.

Usage: python3 -I tools/content/batches/add_photos_ee_1125.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["ee-open-air-museum", "https://commons.wikimedia.org/wiki/File%3AEstonian_Open_Air_Museum%2C_2006_%2802%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/30/Estonian_Open_Air_Museum%2C_2006_%2802%29.jpg", "Bahnfrend", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Harvest work at the Estonian Open Air Museum, 2006", "2006 年爱沙尼亚露天博物馆里的收割场景"],
    ["ee-vargamae", "https://commons.wikimedia.org/wiki/File%3AA._H._Tammsaare_museum_in_Vargam%C3%A4e_2007.JPG", "https://upload.wikimedia.org/wikipedia/commons/5/53/A._H._Tammsaare_museum_in_Vargam%C3%A4e_2007.JPG", "Ivo Kruusamägi from Estonian Wikipedia", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Farmhands' houses at the A. H. Tammsaare Museum, Vargamäe, 2007", "2007 年瓦尔加梅塔姆萨雷博物馆的雇工住房"],
    ["ee-palamuse", "https://commons.wikimedia.org/wiki/File%3APalamuse_parv_2024.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/54/Palamuse_parv_2024.jpg", "Minnekon", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "A raft built on the Palamuse millpond, inspired by Spring, 2024", "2024 年帕拉穆塞水塘上仿照《春天》造的木筏"],
    ["ee-kaali", "https://commons.wikimedia.org/wiki/File%3AKaali_kraater_2006.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/2e/Kaali_kraater_2006.jpg", "ansik", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "The main Kaali crater, Saaremaa", "萨雷马岛的卡利主陨石坑"],
    ["ee-iru-amm", "https://commons.wikimedia.org/wiki/File%3AIru_linnam%C3%A4gi_2013_%281%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c2/Iru_linnam%C3%A4gi_2013_%281%29.jpg", "Rein Urm", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Iru hill (the Iru hillfort), 2013", "2013 年的伊鲁山（伊鲁古堡遗址）"],
    ["ee-tanassilma", "https://commons.wikimedia.org/wiki/File%3AT%C3%A4nassilma_j%C3%B5gi_Oiu.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/48/T%C3%A4nassilma_j%C3%B5gi_Oiu.jpg", "Oktoober", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Tänassilma River at Oiu", "奥尤附近的塔纳西尔马河"],
    ["ee-tartu", "https://commons.wikimedia.org/wiki/File%3ATartu_Town_Hall_2015.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/61/Tartu_Town_Hall_2015.jpg", "Cayambe", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Tartu Town Hall, 2015", "2015 年的塔尔图市政厅"],
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
