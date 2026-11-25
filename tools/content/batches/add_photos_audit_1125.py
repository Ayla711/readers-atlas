"""11-25 audit: photos for 14 of the 19 pilgrimage and film places that had none, and the Pujiu Temple photo taken out.
One freely licensed Wikimedia Commons photo per place (CC0, public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye
from contact sheets of candidates (tools/content/photos/find_photos.py, then Commons file and category searches).
Where Commons has no photo of the spot itself the nearest honest one is used and the alt text says what it shows:
Green Hedges (demolished) by the replica at Bekonscot Model Village; the Saint-Exupéry monument in Lyon (no freedom of
panorama in France, so no free photo of it) by Place Bellecour; Gljúfrasteinn by Mosfellsdalur, the valley it stands in;
the Felder Museum by Felder's birthplace in Schoppernau. Hamaoka Dunes 1 is dual-licensed GFDL / CC BY-SA 3.0: CC BY-SA 3.0
is used. No usable photo: Virginia Park (Ann Arbor), Lin Haiyin's residence, Xijiang village (Commons only has the film
studio on the White Deer Plain), Wang Xiaobo's grave, the Mandelstam monument in Vladivostok.
Pujiu Temple: Commons has one photo, uploaded by someone other than its author with "hwcmsb@126" as author and a LOFTER
blog as source; the licence cannot be checked at the source, so the photo and its credit line are taken out (as with the
Taha Hussein Museum) and the place keeps no photo.

Usage: python3 -I tools/content/batches/add_photos_audit_1125.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["green-hedges", "https://commons.wikimedia.org/wiki/File%3AGreen_Hedges_replica_at_Bekonscot_Model_Village_%28geograph_6389287%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f5/Green_Hedges_replica_at_Bekonscot_Model_Village_%28geograph_6389287%29.jpg", "David Hillas", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "The replica of Green Hedges at Bekonscot Model Village, Beaconsfield", "比肯斯菲尔德贝肯斯科特模型村里的“绿篱”复制模型"],
    ["cn-haiyan", "https://commons.wikimedia.org/wiki/File%3AHaiyan%2C_Jiaxing%2C_Zhejiang%2C_China_-_panoramio_%288%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/28/Haiyan%2C_Jiaxing%2C_Zhejiang%2C_China_-_panoramio_%288%29.jpg", "song songroov", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "A river among the hills of Haiyan County, Zhejiang", "浙江海盐县境内的河流与山丘"],
    ["cn-jiangan-drama-school", "https://commons.wikimedia.org/wiki/File%3ASite_of_the_National_Drama_School_in_Jiang%27an_%2820250117104750%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/75/Site_of_the_National_Drama_School_in_Jiang%27an_%2820250117104750%29.jpg", "N509FZ", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The site of the National Drama School in Jiang'an", "江安国立剧专旧址"],
    ["fr-little-prince-lyon", "https://commons.wikimedia.org/wiki/File%3APlace_Bellecour_Lyon_3.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7d/Place_Bellecour_Lyon_3.jpg", "Chabe01", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Place Bellecour, Lyon, with Fourvière on the hill beyond", "里昂贝勒库尔广场，远处山上是富维耶圣母院"],
    ["ru-arsenyev", "https://commons.wikimedia.org/wiki/File%3ASvetlanskaya_Street_20%2C_Vladivostok_%28October_2024%29-0.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7c/Svetlanskaya_Street_20%2C_Vladivostok_%28October_2024%29-0.jpg", "Vyacheslav Bukharov", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The main building of the Arsenyev Museum, Svetlanskaya Street 20, Vladivostok", "符拉迪沃斯托克斯韦特兰斯卡亚街 20 号，阿尔谢尼耶夫博物馆主楼"],
    ["jp-hamaoka-dunes", "https://commons.wikimedia.org/wiki/File:Hamaoka_Dunes_1.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/87/Hamaoka_Dunes_1.jpg", "Qurren", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Hamaoka Dunes, Omaezaki", "御前崎的浜冈沙丘"],
    ["br-academia-brasileira", "https://commons.wikimedia.org/wiki/File%3AAcademia_brasileira_de_letras_1.JPG", "https://upload.wikimedia.org/wikipedia/commons/2/21/Academia_brasileira_de_letras_1.JPG", "Wolfhardt", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Petit Trianon, seat of the Academia Brasileira de Letras", "巴西文学院所在的小特里亚农宫"],
    ["br-guimaraes-rosa-museum", "https://commons.wikimedia.org/wiki/File%3AMuseu_Casa_Guimar%C3%A3es_Rosa_-_panoramio.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e9/Museu_Casa_Guimar%C3%A3es_Rosa_-_panoramio.jpg", "Tiago Macedo", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Museu Casa Guimarães Rosa, Cordisburgo", "科迪斯堡的吉马良斯·罗萨故居博物馆"],
    ["br-clarice-statue", "https://commons.wikimedia.org/wiki/File%3AEstatuaClarice.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9b/EstatuaClarice.jpg", "Fernando Frazão/Agência Brasil", "CC BY 3.0 br", "https://creativecommons.org/licenses/by/3.0/br", "The statue of Clarice Lispector and her dog on the seafront at Leme", "莱米海边克拉丽丝·李斯佩克朵和她的狗的雕像"],
    ["cl-isla-negra", "https://commons.wikimedia.org/wiki/File%3ACasa_de_Isla_Negra_-_El_Quisco_-_2009_-_01.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/55/Casa_de_Isla_Negra_-_El_Quisco_-_2009_-_01.jpg", "José Joaquín Cortes", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Neruda's house at Isla Negra", "黑岛的聂鲁达故居"],
    ["at-krieglach", "https://commons.wikimedia.org/wiki/File%3AWiki_kri_004.JPG", "https://upload.wikimedia.org/wikipedia/commons/2/27/Wiki_kri_004.JPG", "Michael Zangl", "CC BY-SA 3.0 at", "https://creativecommons.org/licenses/by-sa/3.0/at", "Rosegger's house in Krieglach, where he lived and died", "罗泽格在克里格拉赫的住所，他在这里去世"],
    ["at-schoppernau", "https://commons.wikimedia.org/wiki/File%3AOberdorf_55%2C_Schoppernau_3.JPG", "https://upload.wikimedia.org/wikipedia/commons/6/6d/Oberdorf_55%2C_Schoppernau_3.JPG", "Friedrich Böhringer", "CC BY-SA 2.5", "https://creativecommons.org/licenses/by-sa/2.5", "Franz Michael Felder's birthplace, Oberdorf 55, Schoppernau", "施奥珀瑙上村 55 号，费尔德的出生地"],
    ["is-gljufrasteinn", "https://commons.wikimedia.org/wiki/File%3AMosfellsdalur.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/05/Mosfellsdalur.jpg", "Stig Nygaard", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "Mosfellsdalur, the valley where Gljúfrasteinn stands", "格柳夫拉斯泰因所在的莫斯费德斯谷"],
    ["za-plaatje-house", "https://commons.wikimedia.org/wiki/File%3ASol_Plaatje_Museum.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e8/Sol_Plaatje_Museum.jpg", "TwinMosia", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Sol Plaatje Museum and Library, 32 Angel Street, Kimberley", "金伯利安琪儿街 32 号的索尔·普拉杰博物馆和图书馆"],
]
REMOVE = ["cn-pujiu-temple"]
FOLDER = {"green-hedges": "uk"}  # ids without a country prefix

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
    pp = os.path.join(APP, "data", FOLDER.get(pid, pid.split("-")[0]), "places.js")
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
cred = os.path.join(APP, "docs", "photo-credits.md")
credits = open(cred, encoding="utf-8").read()
for pid in REMOVE:
    pp = os.path.join(APP, "data", pid.split("-")[0], "places.js")
    s = files.get(pp) or open(pp, encoding="utf-8").read()
    m = re.search(r'\{ id: "' + re.escape(pid) + r'"[^\n]*?(, photo: (\{[^{}]*\}))', s)
    assert m, pid
    page = json.loads(m.group(2))["source"]
    files[pp] = s[:m.start(1)] + s[m.end(1):]
    lines = [l for l in credits.split("\n") if page in l]
    assert len(lines) == 1, pid
    credits = credits.replace(lines[0] + "\n", "")
    print("photo taken out:", pid, "(delete", json.loads(m.group(2))["file"], "by hand)")
for pp, s in files.items():
    if pp != "credits": write(pp, s)
write(cred, credits.rstrip("\n") + "\n" + "\n".join(files["credits"]) + "\n")
print(len(files["credits"]), "photos attached")
