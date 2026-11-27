"""11-26: photos for the Belarusian places of add_by1.py: freely licensed Wikimedia Commons photos (CC0, public domain,
CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py); the Byčki photo was taken by hand from the Commons category "Museum of Vasil
Bykaŭ, Byčki", which the search did not reach. Karanioŭka has no free photo (those found show Hlinišča), so it has none.
The Lastok photographer signs as "Валацуга" with a link to a web site; the credit gives the name only.

Usage: python3 -I tools/content/batches/add_photos_by_1126.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["by-orsha-karatkievich", "https://commons.wikimedia.org/wiki/File%3ALenina_street_26_in_Orsha_-_002.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/66/Lenina_street_26_in_Orsha_-_002.jpg", "Mikra72", "CC0", "http://creativecommons.org/publicdomain/zero/1.0/deed.en", "The Uladzimir Karatkievič Museum, 26 Lenin Street, Orsha", "奥尔沙列宁街 26 号的乌拉济米尔·卡拉特克维奇博物馆"],
    ["by-bychki", "https://commons.wikimedia.org/wiki/File:By%C4%8Dki_siadziba_V._Bykava_1.JPG", "https://upload.wikimedia.org/wikipedia/commons/7/7c/By%C4%8Dki_siadziba_V._Bykava_1.JPG?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original", "Sergei", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Vasil Bykaŭ museum-estate in Byčki", "贝奇基的瓦西里·贝科夫故居博物馆"],
    ["by-lastok", "https://commons.wikimedia.org/wiki/File%3A%C5%81astok._%D0%9B%D0%B0%D1%81%D1%82%D0%BE%D0%BA._%D0%A1%D1%8F%D0%B4%D0%B7%D1%96%D0%B1%D0%B0_%D0%AF%D0%BA%D1%83%D0%B1%D0%B0_%D0%9A%D0%BE%D0%BB%D0%B0%D1%81%D0%B0_%281885%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/a9/%C5%81astok._%D0%9B%D0%B0%D1%81%D1%82%D0%BE%D0%BA._%D0%A1%D1%8F%D0%B4%D0%B7%D1%96%D0%B1%D0%B0_%D0%AF%D0%BA%D1%83%D0%B1%D0%B0_%D0%9A%D0%BE%D0%BB%D0%B0%D1%81%D0%B0_%281885%29.jpg", "Валацуга", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The forester's lodge at Lastok, a memorial estate of Jakub Kolas", "拉斯托克的护林人小屋，雅库布·科拉斯纪念庄园"],
    ["by-belavezha", "https://commons.wikimedia.org/wiki/File%3ABelovezhskaya_Pushcha_N.P.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/95/Belovezhskaya_Pushcha_N.P.jpg", "Metselaar, J.", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Woodland in Belavezha Forest National Park", "别洛韦日森林国家公园的林地"],
    ["by-polotsk", "https://commons.wikimedia.org/wiki/File%3ABELARUS_-_POLOTSK_%28%D0%9F%D0%BE%D0%BB%D0%B0%D1%86%D0%BA%29._St_Sophia_cathedral..jpg", "https://upload.wikimedia.org/wikipedia/commons/a/a1/BELARUS_-_POLOTSK_%28%D0%9F%D0%BE%D0%BB%D0%B0%D1%86%D0%BA%29._St_Sophia_cathedral..jpg", "Jurasikt", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "St Sophia Cathedral above the Dvina, Polotsk", "道加瓦河岸上的波洛茨克圣索菲亚大教堂"],
    ["by-slutsk", "https://commons.wikimedia.org/wiki/File%3ABLR_Slutsk_Administrative_Building.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9e/BLR_Slutsk_Administrative_Building.jpg", "Pulkassa, Flickr", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "The centre of Slutsk", "斯卢茨克市中心"],
    ["by-kusliany", "https://commons.wikimedia.org/wiki/File%3ABelarus-Kushlany.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c9/Belarus-Kushlany.jpg", "Viktar Palstsiuk", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Bahuševič house at Kušlany", "库什利亚内的博古舍维奇故居"],
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
