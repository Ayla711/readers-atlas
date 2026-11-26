"""11-26: photos for the Lithuanian places of add_lt1.py, and for its two places abroad (Stutthof in data/pl, 34th
Street in data/us): freely licensed Wikimedia Commons photos (CC0, public domain, CC BY, CC BY-SA; never NC or ND, never
ported licences), chosen by eye from contact sheets of candidates (tools/content/photos/find_photos.py). Pilotiškės shows
the hill Aušrakalnis named in the novel; Lieporiai shows its gymnasium, as no free photo shows the blocks of Lieporiai.

Usage: python3 -I tools/content/batches/add_photos_lt_1126.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["lt-rasos", "https://commons.wikimedia.org/wiki/File%3ARasos_entrance.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/2c/Rasos_entrance.jpg", "arz", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "The gate of Rasos Cemetery, Vilnius", "维尔纽斯拉索斯公墓大门"],
    ["lt-antakalnis", "https://commons.wikimedia.org/wiki/File%3AAntakalnio_kap_by_Augustas_Didzgalvis.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/88/Antakalnio_kap_by_Augustas_Didzgalvis.jpg", "Augustas Didžgalvis", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "A path in Antakalnis Cemetery, Vilnius", "维尔纽斯安塔卡尔尼斯公墓里的小路"],
    ["lt-sv-mykolo", "https://commons.wikimedia.org/wiki/File%3AChurch_of_St_Michael%2C_Vilnius%2C_Lithuania.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/26/Church_of_St_Michael%2C_Vilnius%2C_Lithuania.jpg", "John Samuel", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "St Michael's Church, Vilnius", "维尔纽斯圣米迦勒教堂"],
    ["lt-sv-jurgio", "https://commons.wikimedia.org/wiki/File%3ASide-view_of_the_Church_of_St._George_in_Vilnius%2C_Lithuania_in_2023.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b3/Side-view_of_the_Church_of_St._George_in_Vilnius%2C_Lithuania_in_2023.jpg", "Pofka", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "St George's Church, Vilnius, from the side", "维尔纽斯圣乔治教堂侧影"],
    ["lt-uzupis", "https://commons.wikimedia.org/wiki/File%3APrie_Men%C5%B3_inkubatoriaus.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7f/Prie_Men%C5%B3_inkubatoriaus.jpg", "Stela", "CC0", "http://creativecommons.org/publicdomain/zero/1.0/deed.en", "The Vilnia bank by the Užupis Art Incubator", "乌茹皮斯艺术孵化器旁的维尔尼亚河岸"],
    ["lt-pilotiskes", "https://commons.wikimedia.org/wiki/File%3AAu%C5%A1rakalnis.JPG", "https://upload.wikimedia.org/wikipedia/commons/0/07/Au%C5%A1rakalnis.JPG", "VytautasDegutis at Lithuanian Wikipedia", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "Aušrakalnis, Pilotiškės", "皮洛蒂什凯斯的曙光山"],
    ["lt-lieporiai", "https://commons.wikimedia.org/wiki/File%3ASiauliu_Lieporiu_gimnazija.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/12/Siauliu_Lieporiu_gimnazija.jpg", "Mind lt", "CC0", "http://creativecommons.org/publicdomain/zero/1.0/deed.en", "The Lieporiai gymnasium, Šiauliai", "希奥利艾的利埃波里艾中学"],
    ["lt-mikytai", "https://commons.wikimedia.org/wiki/File%3AWolfskinder-Denkmal_in_Mikytai%2C_1995.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/95/Wolfskinder-Denkmal_in_Mikytai%2C_1995.jpg", "Ruth Leiserowitz", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The wolf children memorial at Mikytai, 1995", "1995 年米基泰的“狼孩”纪念碑"],
    ["pl-stutthof", "https://commons.wikimedia.org/wiki/File%3AStutthof_concentration_camp_2016.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c8/Stutthof_concentration_camp_2016.jpg", "kallerna", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The gate of the former Stutthof camp, 2016", "2016 年施图特霍夫集中营旧址大门"],
    ["us-ny-34th-street", "https://commons.wikimedia.org/wiki/File%3A34th_St_9th_Av_td_%282018-08-16%29_11.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/33/34th_St_9th_Av_td_%282018-08-16%29_11.jpg", "Tdorante10", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "34th Street at Ninth Avenue, Manhattan, 2018", "2018 年曼哈顿 34 街与第九大道路口"],
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
