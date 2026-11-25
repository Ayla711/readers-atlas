"""11-24: photos for the South African places of add_za2.py (5 of 6 places). One freely licensed Wikimedia Commons photo
per place (CC0, public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). None of the 6 is a pilgrimage or film place. Marabastad has none: the only Commons
files in its category are museum exhibits about it (a floor map, display cases), not the place itself.

Usage: python3 -I tools/content/batches/add_photos_za_1124.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""
import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["za-prince-albert", "https://commons.wikimedia.org/wiki/File%3APrince_Albert%2C_Western_Cape_%282009%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1b/Prince_Albert%2C_Western_Cape_%282009%29.jpg", "jonty.fisher", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "Prince Albert below the Swartberg, on the edge of the Karoo", "卡鲁边缘、斯瓦特山下的艾伯特亲王镇"],
    ["za-hector-pieterson", "https://commons.wikimedia.org/wiki/File%3AThe_Hector_Pieterson_Memorial_%284611836835%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/dd/The_Hector_Pieterson_Memorial_%284611836835%29.jpg", "Jorge Láscar from Australia", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "The Hector Pieterson Memorial, Orlando West, Soweto", "索韦托奥兰多西区的赫克托·彼得森纪念碑"],
    ["za-johannesburg", "https://commons.wikimedia.org/wiki/File%3AJohannesburg_skyline_2017.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/95/Johannesburg_skyline_2017.jpg", "Mark Hillary", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "The Johannesburg skyline", "约翰内斯堡天际线"],
    ["za-east-london", "https://commons.wikimedia.org/wiki/File%3ACity_Hall_Oxford_Street.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/66/City_Hall_Oxford_Street.jpg", "Bfluff", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "East London City Hall, where the Truth and Reconciliation Commission's first hearings were held", "东伦敦市政厅——真相与和解委员会第一批听证会在这里举行"],
    ["za-shaka-memorial", "https://commons.wikimedia.org/wiki/File%3AShaka_Zulu_Memorial.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/09/Shaka_Zulu_Memorial.jpg", "JRamatsui", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The memorial to King Shaka at KwaDukuza", "夸杜库扎的沙卡国王纪念碑"],
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
