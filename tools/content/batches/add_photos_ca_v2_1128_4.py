"""11-28: photos for the new places of add_ca_v2_1128_4.py (Canada, batch 4: Ontario): freely licensed Wikimedia Commons photos
(CC0, public domain, CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). Orillia shows Stephen Leacock's summer house, now the Leacock Museum; Essex County a
county road between fields, from a photographer in Leamington who titled it "The sky over Essex County". The Wingham and Moose
Factory places keep their photos.

Usage: python3 -I tools/content/batches/add_photos_ca_v2_1128_4.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["ca-orillia", "https://commons.wikimedia.org/wiki/File:Stephen_Leacock_House_Orillia.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f9/Stephen_Leacock_House_Orillia.jpg", "Jcart1534", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Stephen Leacock's summer house in Orillia, now the Leacock Museum", "奥里利亚的斯蒂芬·里柯克夏日别墅，如今是里柯克博物馆"],
    ["ca-parliament-hill", "https://commons.wikimedia.org/wiki/File:Centre_Block,_Ottawa,_Southeast_view_20170422_1.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/94/Centre_Block%2C_Ottawa%2C_Southeast_view_20170422_1.jpg", "DXR", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Centre Block and Peace Tower on Parliament Hill, Ottawa", "渥太华国会山上的中央大楼和和平塔"],
    ["ca-sainte-marie", "https://commons.wikimedia.org/wiki/File:Sainte-Marie_among_the_Hurons_native_section.JPG", "https://upload.wikimedia.org/wikipedia/commons/5/53/Sainte-Marie_among_the_Hurons_native_section.JPG", "Pjposullivan", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Reconstructed longhouse and wigwam in the Indigenous section of Sainte-Marie among the Hurons", "休伦人中的圣玛丽原住民区里复建的长屋和棚屋"],
    ["ca-essex-county", "https://commons.wikimedia.org/wiki/File:The_sky_over_Essex_County_today_(3629337607).jpg", "https://upload.wikimedia.org/wikipedia/commons/0/04/The_sky_over_Essex_County_today_%283629337607%29.jpg", "Andrea_44", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "A straight county road between flat fields under a summer sky in Essex County, Ontario", "安大略埃塞克斯县平坦田野间一条笔直的乡道，头上是夏日的天空"],
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
