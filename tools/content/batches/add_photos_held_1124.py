"""11-24: photos for the nine places added for the famous books held back as "place to be checked" (add_fi3.py, add_ru6.py,
add_us1.py, add_be3.py, add_tr3.py, add_ua3.py; add_nl3.py adds no place). One freely licensed Wikimedia Commons photo per
place (CC0, public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). For Kalender itself no usable photo was found; Yeniköy's pin carries a photo taken at
the Yeniköy ferry pier.

Usage: python3 -I tools/content/batches/add_photos_held_1124.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""
import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["fi-helsinki", "https://commons.wikimedia.org/wiki/File%3AHelsinki_Senate_Square_with_flowers.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/41/Helsinki_Senate_Square_with_flowers.jpg", "JIP", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Senate Square, Helsinki, with the cathedral", "赫尔辛基议会广场与大教堂"],
    ["fi-hameenkyro", "https://commons.wikimedia.org/wiki/File%3AH%C3%A4meenkyr%C3%B6-Kierikkala-N%C3%A4k%C3%B6alakahvila-IMG_6967_69.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/d5/H%C3%A4meenkyr%C3%B6-Kierikkala-N%C3%A4k%C3%B6alakahvila-IMG_6967_69.jpg", "J Hokkanen", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Lake view from the village of Kierikkala, Hämeenkyrö, where Sillanpää was born", "海门屈勒基耶里卡拉村眺望湖面——西兰帕就出生在这个村子"],
    ["ru-petrozavodsk", "https://commons.wikimedia.org/wiki/File%3ALake_Onega._Embankment_in_Petrozavodsk.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/49/Lake_Onega._Embankment_in_Petrozavodsk.jpg", "Antonio Bonanno", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "The shore of Lake Onega at Petrozavodsk", "彼得罗扎沃茨克的奥涅加湖岸"],
    ["us-gloucester-ma", "https://commons.wikimedia.org/wiki/File%3A2012_harbor_in_Gloucester_Massachusetts_USA_8393986457.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/77/2012_harbor_in_Gloucester_Massachusetts_USA_8393986457.jpg", "Doug Kerr", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "Gloucester harbor, Massachusetts", "马萨诸塞州格洛斯特港"],
    ["be-ghent", "https://commons.wikimedia.org/wiki/File%3AGraslei_Ghent.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/59/Graslei_Ghent.jpg", "Martinvl", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Graslei on the Leie, Ghent", "根特莱厄河畔的香草河岸"],
    ["be-borinage", "https://commons.wikimedia.org/wiki/File%3ATerril_de_la_flache%2C_vue_vers_Hornu_-_panoramio.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/aa/Terril_de_la_flache%2C_vue_vers_Hornu_-_panoramio.jpg", "Christophe Gesché", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "The Borinage seen from the Terril de la Flache, towards Hornu", "从拉弗拉什矸石山望博里纳日，远处是奥尔尼"],
    ["tr-ankara", "https://commons.wikimedia.org/wiki/File%3AUlus_Square%2C_Ankara.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/d6/Ulus_Square%2C_Ankara.jpg", "Radosław Botev", "CC BY 3.0 pl", "https://creativecommons.org/licenses/by/3.0/pl/deed.en", "Ulus Square, Ankara", "安卡拉乌卢斯广场"],
    ["tr-yenikoy", "https://commons.wikimedia.org/wiki/File%3AOld_house_on_Bosphorus_shore_-_panoramio.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/94/Old_house_on_Bosphorus_shore_-_panoramio.jpg", "el ui", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "An old house beside the Yeniköy ferry pier on the Bosphorus", "博斯普鲁斯海峡耶尼柯伊码头旁的老房子"],
    ["ua-myrhorod", "https://commons.wikimedia.org/wiki/File%3AMyrhorod_Stadtansicht.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/62/Myrhorod_Stadtansicht.jpg", "AlexanderUA", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Myrhorod from above, looking south", "俯瞰米尔霍罗德，向南望"],
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
