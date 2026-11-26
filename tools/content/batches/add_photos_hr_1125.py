"""11-25: photos for 5 of the 6 Croatian places of add_hr1.py. One freely licensed Wikimedia Commons photo per place
(CC0, public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). Tin's Tower in Vrgorac (a pilgrimage place) has no photo: the only Commons
photo of the tower (File:Vrgorac - kula Tina Ujevića.jpg) is 500 x 667, upright and too small, and the other Vrgorac
photos do not show it. The Museum of Peasant Revolts carries the Oršić Castle courtyard (the museum's Wikidata image).

Usage: python3 -I tools/content/batches/add_photos_hr_1125.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["hr-zagreb", "https://commons.wikimedia.org/wiki/File%3ATrg_bana_Jela%C4%8Di%C4%87a_%282021%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/ff/Trg_bana_Jela%C4%8Di%C4%87a_%282021%29.jpg", "Vojtěch Dočkal", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Ban Jelačić Square, Zagreb", "萨格勒布的耶拉契奇总督广场"],
    ["hr-peasant-revolts-museum", "https://commons.wikimedia.org/wiki/File%3ADvorac_Or%C5%A1i%C4%87%2C_Gornja_Stubica_-_dvori%C5%A1te.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/59/Dvorac_Or%C5%A1i%C4%87%2C_Gornja_Stubica_-_dvori%C5%A1te.jpg", "Silverije", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The courtyard of Oršić Castle in Gornja Stubica, home of the Museum of Peasant Revolts", "上斯图比察奥尔希奇城堡的庭院，农民起义博物馆就设在城堡里"],
    ["hr-vela-luka", "https://commons.wikimedia.org/wiki/File%3AVela_Luka_ferryport_20260720.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/4b/Vela_Luka_ferryport_20260720.jpg", "Argo Navis", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The ferry port of Vela Luka, Korčula", "科尔丘拉岛韦拉卢卡的渡轮码头"],
    ["hr-rab", "https://commons.wikimedia.org/wiki/File%3A20140505_Rab_old_town_1.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/3a/20140505_Rab_old_town_1.jpg", "Isiwal", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The old town of Rab from the sea, with its bell towers and walls", "从海上看拉布老城的钟楼和城墙"],
    ["hr-vinkovci", "https://commons.wikimedia.org/wiki/File%3A%C5%BDeljezni%C4%8Dki_kolodvor_Vinkovci_-_%D0%96%D0%B5%D0%BB%D0%B5%D0%B7%D0%BD%D0%B8%D1%87%D0%BA%D0%B0_%D1%81%D1%82%D0%B0%D0%BD%D0%B8%D1%86%D0%B0_%D0%92%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D1%86%D0%B8.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7e/%C5%BDeljezni%C4%8Dki_kolodvor_Vinkovci_-_%D0%96%D0%B5%D0%BB%D0%B5%D0%B7%D0%BD%D0%B8%D1%87%D0%BA%D0%B0_%D1%81%D1%82%D0%B0%D0%BD%D0%B8%D1%86%D0%B0_%D0%92%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D1%86%D0%B8.jpg", "MirkoS18", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "Vinkovci railway station", "温科夫奇火车站"],
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
