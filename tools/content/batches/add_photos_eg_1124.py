"""11-24: photos for the Egyptian places of add_eg2.py (10 of 11 places). One freely licensed Wikimedia Commons photo per
place (CC0, public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). None of the 11 is a pilgrimage or film place. Maghagha has none: Commons has only
maps and a football ground for it. The Qanatir prison pin carries a photo of the town of al-Qanatir al-Khayriyya (no free
photo of the prison itself); the Cave of Swimmers photo (Roland Unger) is dual-licensed GFDL / CC BY-SA 3.0 and is used
under CC BY-SA 3.0.

Usage: python3 -I tools/content/batches/add_photos_eg_1124.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""
import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["eg-sayyida-zaynab", "https://commons.wikimedia.org/wiki/File%3AMosque_of_Sayeda_Zainab%2C_Cairo.JPG", "https://upload.wikimedia.org/wikipedia/commons/2/2c/Mosque_of_Sayeda_Zainab%2C_Cairo.JPG", "لا روسا", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Mosque of Sayyida Zaynab, Cairo", "开罗赛义达·宰娜卜清真寺"],
    ["eg-cairo", "https://commons.wikimedia.org/wiki/File%3ACairo_skyline%2C_Nile_River%2C_Egypt.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/54/Cairo_skyline%2C_Nile_River%2C_Egypt.jpg", "Vyacheslav Argenberg", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "The Cairo skyline across the Nile", "隔着尼罗河看开罗天际线"],
    ["eg-qanater-prison", "https://commons.wikimedia.org/wiki/File%3AEl_Qanater_El_Khayreya_%2C_photo_by_Hatem_Moushir_40.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9d/El_Qanater_El_Khayreya_%2C_photo_by_Hatem_Moushir_40.jpg", "Hatem Moushir", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Nile at al-Qanatir al-Khayriyya, the town where the prison stands", "盖纳提尔·海里耶的尼罗河——监狱就在这座小镇"],
    ["eg-imbaba", "https://commons.wikimedia.org/wiki/File%3AImbaba_Bridge_%28271400956%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c9/Imbaba_Bridge_%28271400956%29.jpg", "Hossam el-Hamalawy", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "Imbaba Bridge over the Nile", "尼罗河上的因巴巴桥"],
    ["eg-port-said", "https://commons.wikimedia.org/wiki/File%3APort_Said_1930s_01.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/14/Port_Said_1930s_01.jpg", "Unknown photographer", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "The lighthouse and harbour of Port Said in the 1930s (old photograph)", "20 世纪 30 年代塞得港的灯塔和港口（老照片）"],
    ["eg-humaithara", "https://commons.wikimedia.org/wiki/File%3ATombeau_de_Sheikh_Shazly_-_panoramio.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e8/Tombeau_de_Sheikh_Shazly_-_panoramio.jpg", "youssef_alam", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "The tomb of Abu al-Hasan al-Shadhili at Humaithara", "胡迈斯拉的阿布·哈桑·沙兹利陵墓"],
    ["eg-siwa", "https://commons.wikimedia.org/wiki/File%3ASiwa_Oasis%2C_Sahara_Desert%2C_Egypt.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/63/Siwa_Oasis%2C_Sahara_Desert%2C_Egypt.jpg", "Vyacheslav Argenberg", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "Siwa town and its palm groves, with the desert beyond", "锡瓦镇和棕榈林，远处是沙漠"],
    ["eg-tanta", "https://commons.wikimedia.org/wiki/File%3AEl-Sayed_el-Badawy_Mosque_-_Tanta_-_Egypt2.JPG", "https://upload.wikimedia.org/wikipedia/commons/2/29/El-Sayed_el-Badawy_Mosque_-_Tanta_-_Egypt2.JPG", "Ashashyou", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Mosque of al-Sayyid al-Badawi, Tanta", "坦塔的赛义德·巴达维清真寺"],
    ["eg-thebes", "https://commons.wikimedia.org/wiki/File%3AKarnak_temple_complex_12.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/aa/Karnak_temple_complex_12.jpg", "Hamerani", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The avenue of sphinxes at Karnak, Luxor (ancient Thebes)", "卢克索（古底比斯）卡纳克神庙的狮身羊首像大道"],
    ["eg-cave-of-swimmers", "https://commons.wikimedia.org/wiki/File%3AWadiSuraSwimmers.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/dc/WadiSuraSwimmers.jpg", "Roland Unger", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The 'swimmers' painted in the Cave of Swimmers, Wadi Sura", "苏拉谷泳者洞里画着的“游泳的人”"],
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
