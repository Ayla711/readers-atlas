"""11-27: photos for the places of add_si1.py (four in data/si, the Hippodrome in data/tr): freely licensed Wikimedia
Commons photos (CC0, public domain, CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact
sheets of candidates (tools/content/photos/find_photos.py). The Muljava photo shows Jurčič's bust, small, on the lawn: a
monument, not a portrait photo. The Bainsizza photo is an Austro-Hungarian army press photo of 1917 (public domain, Austrian
National Library). The Hippodrome photo is a 1967 slide; of the Hippodrome photos found it is the one without a crowd.

Usage: python3 -I tools/content/batches/add_photos_si_1127.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["si-jurcic-muljava", "https://commons.wikimedia.org/wiki/File%3AJur%C4%8Di%C4%8Deva_doma%C4%8Dija_%28Muljava%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/d1/Jur%C4%8Di%C4%8Deva_doma%C4%8Dija_%28Muljava%29.jpg", "Petar Milošević", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Jurčič's birth house at Muljava, now a museum", "穆利亚瓦的尤尔奇奇故居，如今是博物馆"],
    ["si-visoko", "https://commons.wikimedia.org/wiki/File%3ADvorec_Visoko.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f7/Dvorec_Visoko.jpg", "Domen Rant", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Visoko Manor in winter", "冬天的维索科庄园"],
    ["si-strmol", "https://commons.wikimedia.org/wiki/File%3AGrad_Strmol_02.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f7/Grad_Strmol_02.jpg", "Mihael Grmek", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Strmol Castle below the wooded hill", "林木覆盖的山坡下的斯特莫尔城堡"],
    ["si-banjsice", "https://commons.wikimedia.org/wiki/File%3ABainsizza_Plateau._%28BildID_15599835%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/88/Bainsizza_Plateau._%28BildID_15599835%29.jpg", "K.u.k. Kriegspressequartier, Lichtbildstelle Wien", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "The Bainsizza plateau in 1917", "1917 年的贝因西扎高原"],
    ["tr-hippodrome", "https://commons.wikimedia.org/wiki/File%3AIstanbul_-_Hippodrome_%283494147224%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/64/Istanbul_-_Hippodrome_%283494147224%29.jpg", "Roger W", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "The site of the Hippodrome with the Obelisk of Theodosius, 1967", "赛马场旧址和狄奥多西方尖碑，1967 年"],
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
