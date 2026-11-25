"""11-24: photos for the New Zealand places of add_nz2.py (8 of 11 places). One freely licensed Wikimedia Commons photo per
place (CC0, public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). None of the 11 is a pilgrimage or film place. Fordlands, Waituhi and Matawhero
(prototype, prototype, original) have none: Commons has no photo of any of them (searches for Fordlands return English
places of the same name; Waituhi's only file is a different Waituhi; Matawhero returns pictures of Mars).

Usage: python3 -I tools/content/batches/add_photos_nz_1124.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""
import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["nz-henderson", "https://commons.wikimedia.org/wiki/File%3AHenderson%27s_Mill_20250411_122230.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7c/Henderson%27s_Mill_20250411_122230.jpg", "Prosperosity", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "Henderson's Mill on the Ōpanuku Stream, Henderson", "亨德森奥帕努库溪边的亨德森磨坊"],
    ["nz-hongoeka", "https://commons.wikimedia.org/wiki/File%3AHongoeka_Bay.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/10/Hongoeka_Bay.jpg", "AxonsArachnida", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The rocky shore of Hongoeka Bay", "洪戈埃卡湾的礁石海岸"],
    ["nz-te-kuiti", "https://commons.wikimedia.org/wiki/File%3ATe_Kuiti%2C_Rora_Street%2C_New_Zealand.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/22/Te_Kuiti%2C_Rora_Street%2C_New_Zealand.jpg", "Ulrich Lange, Bochum, Germany", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Rora Street, the main street of Te Kūiti", "蒂库伊蒂的主街罗拉街"],
    ["nz-coromandel", "https://commons.wikimedia.org/wiki/File%3A00_23_1006_Coromandel_Peninsula%2C_NZ_-_Coromandel%2C_McGregor_Bay.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e9/00_23_1006_Coromandel_Peninsula%2C_NZ_-_Coromandel%2C_McGregor_Bay.jpg", "W. Bulach", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Coromandel town, McGregor Bay and Whanganui Island, Coromandel Peninsula", "科罗曼德尔半岛：科罗曼德尔镇、麦格雷戈湾和旺阿努伊岛"],
    ["nz-christchurch", "https://commons.wikimedia.org/wiki/File%3AAvon_River%2C_Christchurch%2C_New_Zealand_01.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/6b/Avon_River%2C_Christchurch%2C_New_Zealand_01.jpg", "Michal Klajban", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Avon River in central Christchurch", "克赖斯特彻奇市中心的埃文河"],
    ["nz-wellington", "https://commons.wikimedia.org/wiki/File%3AWellington_Harbour_from_Te_Ara_Tupua.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/4f/Wellington_Harbour_from_Te_Ara_Tupua.jpg", "Wainuiomartian", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "Wellington city across the harbour", "隔着海港望惠灵顿城"],
    ["nz-lake-pupuke", "https://commons.wikimedia.org/wiki/File%3ABay_in_Lake_Pupuke_facing_Rangitoto_Channel.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/51/Bay_in_Lake_Pupuke_facing_Rangitoto_Channel.jpg", "Bjankuloski06", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "Lake Pupuke, with the Rangitoto Channel beyond", "普普克湖，远处是朗伊托托海峡"],
    ["nz-bishopdale", "https://commons.wikimedia.org/wiki/File%3ABishopdale_Seventh-day_Adventist_Church%2C_Christchurch%2C_New_Zealand_02.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/ad/Bishopdale_Seventh-day_Adventist_Church%2C_Christchurch%2C_New_Zealand_02.jpg", "Michal Klajban", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "A church among the trees in Bishopdale, Christchurch", "克赖斯特彻奇毕晓普代尔绿树间的一座教堂"],
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
