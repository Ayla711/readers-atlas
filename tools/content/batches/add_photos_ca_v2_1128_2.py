"""11-28: photos for the new places of add_ca_v2_1128_2.py (Canada, batch 2: Quebec): freely licensed Wikimedia Commons photos
(CC0, public domain, CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). Saint-Henri shows rue Notre-Dame in an early twentieth-century photograph from the
Quebec national archives (BAnQ), public domain. The Montreal place keeps its photo.

Usage: python3 -I tools/content/batches/add_photos_ca_v2_1128_2.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["ca-saint-laurent", "https://commons.wikimedia.org/wiki/File:Boulevard_Saint-Laurent_et_rue_Sainte-Catherine_Ouest.JPG", "https://upload.wikimedia.org/wikipedia/commons/2/2b/Boulevard_Saint-Laurent_et_rue_Sainte-Catherine_Ouest.JPG", "Jeangagnon", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The corner of Saint-Laurent Boulevard and Saint Catherine Street in Montreal", "蒙特利尔圣洛朗大道和圣凯瑟琳街的路口"],
    ["ca-saint-henri", "https://commons.wikimedia.org/wiki/File:Saint-Henri,_Montreal_-_La_rue_Notre-Dame.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b7/Saint-Henri%2C_Montreal_-_La_rue_Notre-Dame.jpg", "BAnQ Vieux-Montréal archives", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "Rue Notre-Dame in Saint-Henri, Montreal, in an early twentieth-century photograph", "二十世纪初照片里蒙特利尔圣亨利区的圣母街"],
    ["ca-knowlton", "https://commons.wikimedia.org/wiki/File:%E2%81%A8Knowlton%E2%81%A9,_%E2%81%A8Quebec%E2%81%A9,_%E2%81%A8Canada%E2%81%A9.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1f/%E2%81%A8Knowlton%E2%81%A9%2C_%E2%81%A8Quebec%E2%81%A9%2C_%E2%81%A8Canada%E2%81%A9.jpg", "Hayden Soloviev", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "Knowlton village and Brome Lake from the air", "从空中看诺尔顿村和布罗姆湖"],
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
