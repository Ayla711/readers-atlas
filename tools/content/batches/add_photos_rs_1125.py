"""11-25: photos for the 4 Serbian places of add_rs1.py. One freely licensed Wikimedia Commons photo per place (CC0,
public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). The monument to Milorad Pavić is a pilgrimage place: its only clear Commons photo
without people (File:Milorad Pavić1.JPG) is upright, so it carries a landscape photo from the Azerbaijani presidential
press service (CC BY 4.0, 23 November 2022) showing the monument with a Serbian honour guard. Belgrade's city-level pin
carries Kalemegdan fortress; Novi Sad's carries Freedom Square and the City Hall.

Usage: python3 -I tools/content/batches/add_photos_rs_1125.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["rs-velika-drenova", "https://commons.wikimedia.org/wiki/File%3AVelika_Drenova_-Crkva.JPG", "https://upload.wikimedia.org/wikipedia/commons/a/a5/Velika_Drenova_-Crkva.JPG", "Sonjabgd", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The church in Velika Drenova, Dobrica Ćosić's native village", "多布里察·乔西奇的家乡大德雷诺瓦村的教堂"],
    ["rs-pavic-monument", "https://commons.wikimedia.org/wiki/File%3AIlham_Aliyev_visited_monuments_to_national_leader_Heydar_Aliyev_and_Milorad_Pavic_in_Tasmajdan_park%2C_Belgrade_07.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/40/Ilham_Aliyev_visited_monuments_to_national_leader_Heydar_Aliyev_and_Milorad_Pavic_in_Tasmajdan_park%2C_Belgrade_07.jpg", "Press Service of the President of the Republic of Azerbaijan", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "The monument to Milorad Pavić in Tašmajdan Park, Belgrade, with an honour guard, November 2022", "2022 年 11 月，贝尔格莱德塔什马伊丹公园的帕维奇纪念碑和仪仗队"],
    ["rs-novi-sad", "https://commons.wikimedia.org/wiki/File%3AWiki.Vojvodina_II_Freedom_Square_%28Novi_Sad%29_058.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/d5/Wiki.Vojvodina_II_Freedom_Square_%28Novi_Sad%29_058.jpg", "Ванилица", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Freedom Square and the City Hall, Novi Sad", "诺维萨德的自由广场和市政厅"],
    ["rs-belgrade", "https://commons.wikimedia.org/wiki/File%3AKalemegdan%2C_a04.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/6f/Kalemegdan%2C_a04.jpg", "Mickey Mystique", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Old cannons on the walls of Kalemegdan, Belgrade Fortress", "贝尔格莱德卡莱梅格丹要塞城墙边的旧炮"],
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
