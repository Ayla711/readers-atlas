"""11-28: photos for the places of add_ca_v2_1128_1.py (Canada, batch 1): freely licensed Wikimedia Commons photos (CC0, public
domain, CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py, plus a Commons geosearch around New Waterford). No usable photo of New Waterford itself is
on Commons (only 1917 disaster pictures with crowds); the place shows the Low Point lighthouse at New Victoria, on the coast next
to the town, and the alt text says so. Trinity shows the Lester-Garland Premises on the harbour.

Usage: python3 -I tools/content/batches/add_photos_ca_v2_1128_1.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["ca-new-waterford", "https://commons.wikimedia.org/wiki/File:20161001_Low_Point_Lighthouse_Aerial_2.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/11/20161001_Low_Point_Lighthouse_Aerial_2.jpg", "Ken Heaton", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Low Point lighthouse at New Victoria, on the Cape Breton coast next to New Waterford, from the air", "从空中看新沃特福德旁边海岸上的洛波因特灯塔（新维多利亚）"],
    ["ca-scots-bay", "https://commons.wikimedia.org/wiki/File:Scots_Bay,_Nova_Scotia.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/2a/Scots_Bay%2C_Nova_Scotia.jpg", "Quintin Soloviev", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "Scots Bay on the Bay of Fundy from the air: farms, a white church and the shore", "从空中看芬迪湾边的斯科茨湾：农田、白色教堂和海岸"],
    ["ca-st-johns", "https://commons.wikimedia.org/wiki/File:City_of_St._John%27s.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/04/City_of_St._John%27s.jpg", "Jcmurphy", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "St. John's harbour and the city from Signal Hill", "从信号山望圣约翰斯港和城区"],
    ["ca-trinity", "https://commons.wikimedia.org/wiki/File:Lester-Garland_Premises_and_the_Rising_Tide_Theatre_(Trinity,_Trinity_Bight,_Newfoundland_and_Labrador,_Canada).jpg", "https://upload.wikimedia.org/wikipedia/commons/5/51/Lester-Garland_Premises_and_the_Rising_Tide_Theatre_%28Trinity%2C_Trinity_Bight%2C_Newfoundland_and_Labrador%2C_Canada%29.jpg", "Wikidedia11001", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The red Lester-Garland Premises and the Rising Tide Theatre on the harbour at Trinity", "三一镇港边红色的莱斯特-加兰商栈和涨潮剧院"],
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
