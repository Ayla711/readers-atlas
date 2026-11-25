"""11-24: photos for the places of the ch, no and se second packs (add_ch2.py, add_no2.py, add_se2.py); the dk third pack adds
no place. One freely licensed Wikimedia Commons photo per place (CC0, public domain, CC BY, CC BY-SA; never NC or ND), chosen
by eye from contact sheets of candidates (tools/content/photos/find_photos.py). Trysil is a film location and must have a
photo: an old public-domain photograph of Innbygda from the National Library of Norway (photographer not known).

Usage: python3 -I tools/content/batches/add_photos_ch_no_se_1124.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""
import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["ch-chur", "https://commons.wikimedia.org/wiki/File%3AChur_in_Graub%C3%BCnden_%28Zwitserland%29_035.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/a3/Chur_in_Graub%C3%BCnden_%28Zwitserland%29_035.jpg", "Agnes Monkelbaan", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "A street in the old town of Chur", "库尔老城的一条街"],
    ["ch-zurich", "https://commons.wikimedia.org/wiki/File%3AGrossm%C3%BCnster_and_Limmat_River%2C_Zurich%2C_20250330_1239_7931.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c2/Grossm%C3%BCnster_and_Limmat_River%2C_Zurich%2C_20250330_1239_7931.jpg", "Jakub Hałun", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "The Grossmünster above the Limmat, Zurich", "利马特河畔的苏黎世大教堂"],
    ["ch-geneva", "https://commons.wikimedia.org/wiki/File%3AGeneva_Lac_Leman.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/95/Geneva_Lac_Leman.jpg", "Markus Bernet", "CC BY-SA 2.5", "https://creativecommons.org/licenses/by-sa/2.5", "Lake Geneva at Geneva, with the Jet d'Eau and a paddle steamer", "日内瓦湖上的大喷泉和明轮船"],
    ["no-lillesand", "https://commons.wikimedia.org/wiki/File%3ALillesandskyline12.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/8a/Lillesandskyline12.jpg", "Espen Franck-Nielsen", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Lillesand seen from the water", "从海上望利勒桑"],
    ["no-tromso", "https://commons.wikimedia.org/wiki/File%3ATroms%C3%B8_sentrum_01.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/5f/Troms%C3%B8_sentrum_01.jpg", "Snurre86", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Central Tromsø below the mountains", "群山脚下的特罗姆瑟市中心"],
    ["no-royal-palace", "https://commons.wikimedia.org/wiki/File%3ARoyal_Palace%2C_Oslo_%282015%29.JPG", "https://upload.wikimedia.org/wikipedia/commons/6/65/Royal_Palace%2C_Oslo_%282015%29.JPG", "Beata May", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Royal Palace, Oslo", "奥斯陆王宫"],
    ["no-trysil", "https://commons.wikimedia.org/wiki/File%3AInnbygda%2C_Trysil_-_no-nb_digifoto_20150313_00117_NB_MIT_FNR_00694.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/94/Innbygda%2C_Trysil_-_no-nb_digifoto_20150313_00117_NB_MIT_FNR_00694.jpg", "Unknown photographer (National Library of Norway)", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "Innbygda in Trysil, with the church and the bridge over the river (old photograph)", "特吕西尔的因比格达：教堂和河上的桥（老照片）"],
    ["no-myre", "https://commons.wikimedia.org/wiki/File%3AMyre_-_%C3%98ksnes%2C_Norway_2023-07-13_%2807%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9f/Myre_-_%C3%98ksnes%2C_Norway_2023-07-13_%2807%29.jpg", "Ryan Hodnett", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Myre in Vesterålen", "韦斯特罗伦的米勒"],
    ["se-norra-stationsgatan", "https://commons.wikimedia.org/wiki/File%3ANorra_Stationsgatan_49-53.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/a7/Norra_Stationsgatan_49-53.jpg", "I99pema", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Buildings on Norra Stationsgatan, Stockholm", "斯德哥尔摩北车站街上的楼房"],
    ["se-sunne", "https://commons.wikimedia.org/wiki/File%3ASunnesundet.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/01/Sunnesundet.jpg", "Gräsmark", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "The Sunne strait, with Sunne church", "松讷海峡与松讷教堂"],
    ["se-jamshog", "https://commons.wikimedia.org/wiki/File%3AKirche_in_J%C3%A4msh%C3%B6g%2C_Blekinge%2C_Schweden.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/40/Kirche_in_J%C3%A4msh%C3%B6g%2C_Blekinge%2C_Schweden.jpg", "Berliner Kartenspieler", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Jämshög church", "耶姆舍格教堂"],
    ["se-sodermalm", "https://commons.wikimedia.org/wiki/File%3AS%C3%B6dermalm.JPG", "https://upload.wikimedia.org/wikipedia/commons/c/c5/S%C3%B6dermalm.JPG", "Batintherain", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "Södermalm seen across the water", "隔水望南岛"],
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
