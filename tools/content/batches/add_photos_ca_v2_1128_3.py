"""11-28: photos for the new places of add_ca_v2_1128_3.py (Canada, batch 3: Toronto): freely licensed Wikimedia Commons photos
(CC0, public domain, CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). The Toronto Islands place shows a cottage on Ward's Island; High Park shows Grenadier
Pond. The existing Toronto place keeps its photo.

Usage: python3 -I tools/content/batches/add_photos_ca_v2_1128_3.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["ca-bloor-viaduct", "https://commons.wikimedia.org/wiki/File:Prince_Edward_Viaduct.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e2/Prince_Edward_Viaduct.jpg", "Paul dexxus", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "The steel arches of the Prince Edward Viaduct over the Don Valley, in autumn", "秋天当河谷上爱德华王子高架桥的钢拱"],
    ["ca-high-park", "https://commons.wikimedia.org/wiki/File:Grenadier_Pond_(61904034).jpg", "https://upload.wikimedia.org/wikipedia/commons/b/bd/Grenadier_Pond_%2861904034%29.jpg", "Diego Torres Silvestre", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "Autumn trees over Grenadier Pond in High Park, Toronto", "多伦多海伊公园掷弹兵池边的秋树"],
    ["ca-elgin-theatre", "https://commons.wikimedia.org/wiki/File:Front_Facade_for_the_Elgin_and_Winter_Gardens_theatres,_Yonge_Street,_Toronto_-e.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c7/Front_Facade_for_the_Elgin_and_Winter_Gardens_theatres%2C_Yonge_Street%2C_Toronto_-e.jpg", "Geo Swan", "CC0", "https://creativecommons.org/publicdomain/zero/1.0/", "The front of the Elgin and Winter Garden Theatres on Yonge Street, Toronto", "多伦多央街上埃尔金与冬园剧院的正门"],
    ["ca-toronto-islands", "https://commons.wikimedia.org/wiki/File:A_lovely_cottage_on_Ward%27s_Island_(27864695136).jpg", "https://upload.wikimedia.org/wikipedia/commons/7/79/A_lovely_cottage_on_Ward%27s_Island_%2827864695136%29.jpg", "shankar s.", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "A cottage among the trees on Ward's Island, one of the Toronto Islands", "多伦多群岛沃兹岛上树丛间的一座小屋"],
    ["ca-erindale", "https://commons.wikimedia.org/wiki/File:University_of_Toronto_at_Mississauga.JPG", "https://upload.wikimedia.org/wikipedia/commons/a/ab/University_of_Toronto_at_Mississauga.JPG", "Siqbal at English Wikipedia", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "A building on the University of Toronto Mississauga campus, the former Erindale College", "多伦多大学密西沙加校区（原伊林代尔学院）的一座楼"],
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
