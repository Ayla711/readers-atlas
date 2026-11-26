"""11-26: photos for the Latvian places of add_lv1.py: freely licensed Wikimedia Commons photos (CC0, public domain,
CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). The Liezēre film location shows the parish church; the farm where the series was
filmed has no free photo. Sakstagals shows the farmhouse of the Francis Trasuns museum there.

Usage: python3 -I tools/content/batches/add_photos_lv_1126.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["lv-saulrieti", "https://commons.wikimedia.org/wiki/File%3AVecpiebalga%2C_K._Skalbes_muzejs_%22Saulrieti%22_2000-05-27.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/2a/Vecpiebalga%2C_K._Skalbes_muzejs_%22Saulrieti%22_2000-05-27.jpg", "J. Sedols", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "Saulrieti, Kārlis Skalbe's memorial museum, Vecpiebalga, 2000", "2000 年韦茨皮耶巴尔加的卡尔利斯·斯卡尔贝纪念馆“绍尔列蒂”"],
    ["lv-ragaciems", "https://commons.wikimedia.org/wiki/File%3AImanta_Ziedo%C5%86a_un_Ausmas_Ziedones-Kant%C4%81nes_kapavieta.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/98/Imanta_Ziedo%C5%86a_un_Ausmas_Ziedones-Kant%C4%81nes_kapavieta.jpg", "Treisijs", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The grave of Imants Ziedonis and Ausma Ziedone-Kantāne, Ragaciems", "拉加齐姆斯的伊曼茨·齐耶多尼斯与奥斯玛·齐耶多内-坎塔内之墓"],
    ["lv-lozmetejkalns", "https://commons.wikimedia.org/wiki/File%3ALo%C5%BEmet%C4%93jkalns_Piemi%C5%86as_akmens.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/77/Lo%C5%BEmet%C4%93jkalns_Piemi%C5%86as_akmens.jpg", "Evita wiki", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Christmas Battles memorial stone at Ložmetējkalns", "机枪山的圣诞战役纪念石"],
    ["lv-grizinkalns", "https://commons.wikimedia.org/wiki/File%3AGr%C4%ABzi%C5%86kalns_-_d%C4%81rznieka_m%C4%81ja_%281%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/90/Gr%C4%ABzi%C5%86kalns_-_d%C4%81rznieka_m%C4%81ja_%281%29.jpg", "Mārtiņš Bruņenieks", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The gardener's house in Grīziņkalns Park, Riga", "里加格里津卡尔恩斯公园的园丁小屋"],
    ["lv-sakstagals", "https://commons.wikimedia.org/wiki/File%3AKolnas%C4%81ta_-_F._Trasuna_muzejs_Sakstagal%C4%81._2002-09-14.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/83/Kolnas%C4%81ta_-_F._Trasuna_muzejs_Sakstagal%C4%81._2002-09-14.jpg", "J. Sedols", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "Kolnasāta, the Francis Trasuns museum in Sakstagals, 2002", "2002 年萨克斯塔加尔斯的弗朗齐斯·特拉苏恩斯博物馆“科尔纳萨塔”"],
    ["lv-liezere", "https://commons.wikimedia.org/wiki/File%3ALiezeres_bazn%C4%ABca_2001-08-25.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/6b/Liezeres_bazn%C4%ABca_2001-08-25.jpg", "J. Sedols", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "The Lutheran church of Liezēre, 2001", "2001 年的列泽雷路德宗教堂"],
    ["lv-lejasciems", "https://commons.wikimedia.org/wiki/File%3AAnna_Sakse_monument_Lejasciems.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/4a/Anna_Sakse_monument_Lejasciems.jpg", "Semigallen", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "The monument to Anna Sakse in Lejasciems", "莱亚斯齐姆斯的安娜·萨克塞纪念碑"],
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
