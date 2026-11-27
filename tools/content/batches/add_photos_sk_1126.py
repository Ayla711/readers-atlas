"""11-26: photos for the Slovak places of add_sk1.py: freely licensed Wikimedia Commons photos (CC0, public domain,
CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). The Drienčany church photo is from Wiki Loves Monuments 2016, with GPS in the
village. For Bratislava the square photo whose Commons author field is only a Flickr address was not used; the one used
shows tourists at a distance, no portrait. The bridge photo was taken mid-bridge (GPS 47.7953, 18.7303).

Usage: python3 -I tools/content/batches/add_photos_sk_1126.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["sk-driencany", "https://commons.wikimedia.org/wiki/File%3ADrien%C4%8Dany_-_Evanjelick%C3%BD_kostol.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/4a/Drien%C4%8Dany_-_Evanjelick%C3%BD_kostol.jpg", "Ladislav Luppa", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The walled Lutheran church of Drienčany", "德里恩恰尼带围墙的路德宗教堂"],
    ["sk-bratislava", "https://commons.wikimedia.org/wiki/File%3ABratislava_-_Hlavn%C3%A9_n%C3%A1mestie_%28radnica%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/6e/Bratislava_-_Hlavn%C3%A9_n%C3%A1mestie_%28radnica%29.jpg", "Pudelek (Marcin Szala)", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Old Town Hall on the Main Square, Bratislava", "布拉迪斯拉发老城主广场上的旧市政厅"],
    ["sk-sturovo", "https://commons.wikimedia.org/wiki/File%3AM%C3%A1ria_Val%C3%A9ria_Bridge%2C_halfway_between_Hungary_and_Slovakia_julesvernex2.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/76/M%C3%A1ria_Val%C3%A9ria_Bridge%2C_halfway_between_Hungary_and_Slovakia_julesvernex2.jpg", "Jules Verne Times Two", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "On the Mária Valéria Bridge, halfway between Štúrovo and Esztergom", "玛丽亚·瓦莱里娅桥上，什图罗沃和埃斯泰尔戈姆的正中间"],
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
