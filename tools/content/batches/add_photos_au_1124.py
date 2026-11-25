"""11-24: photos for the Australian places of add_au2.py and add_au3.py (25 of 26 places). One freely licensed Wikimedia
Commons photo per place (CC0, public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). Every film location and the pilgrimage place has one; Raymond Terrace's is the
"Wirrawee Cinema" set the film built in King Street. Jarvisfield (prototype) has none: no usable photo of the place was found.
The Australian Antarctic Division's pin (for Macquarie Island) carries a photo of Macquarie Island itself.

Usage: python3 -I tools/content/batches/add_photos_au_1124.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""
import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["au-west-leederville", "https://commons.wikimedia.org/wiki/File%3AWest_Leederville_Primary_School%2C_July_2026_02.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/70/West_Leederville_Primary_School%2C_July_2026_02.jpg", "Calistemon", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "West Leederville Primary School, a state heritage building", "西利德维尔小学，州文物建筑"],
    ["au-northcote", "https://commons.wikimedia.org/wiki/File%3AHigh_Street%2C_Northcote%2C_Victoria.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/3d/High_Street%2C_Northcote%2C_Victoria.jpg", "Unknown photographer", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "High Street, Northcote, in the early twentieth century (old postcard)", "二十世纪初的诺斯科特高街（老明信片）"],
    ["au-sydney", "https://commons.wikimedia.org/wiki/File%3ASydney_ferry_KANGAROO_at_Circular_Quay_and_paddle_steamer.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/0e/Sydney_ferry_KANGAROO_at_Circular_Quay_and_paddle_steamer.jpg", "Unknown photographer", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "Ferries at Circular Quay, Sydney (old photograph)", "悉尼环形码头的渡轮（老照片）"],
    ["au-bellingen", "https://commons.wikimedia.org/wiki/File%3AThe_Bellingen_River_-_Taken_on_Saturday%2C_19th_March_2011_at_1-29pm._-_panoramio.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f0/The_Bellingen_River_-_Taken_on_Saturday%2C_19th_March_2011_at_1-29pm._-_panoramio.jpg", "Christopher Wood", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Bellinger River at Bellingen", "贝林根的贝林格河"],
    ["au-wickepin", "https://commons.wikimedia.org/wiki/File%3AAlbert_Facey_Homestead%2C_October_2020_03.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e0/Albert_Facey_Homestead%2C_October_2020_03.jpg", "Calistemon", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Albert Facey Homestead in Wickepin", "威克平的阿尔伯特·费西故居"],
    ["au-denmark-wa", "https://commons.wikimedia.org/wiki/File%3ARoad_bridge_across_Denmark_River_in_Denmark%2C_Western_Australia%2C_2022.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/af/Road_bridge_across_Denmark_River_in_Denmark%2C_Western_Australia%2C_2022.jpg", "Kgbo", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The road bridge over the Denmark River, Denmark, Western Australia", "西澳丹麦镇丹麦河上的公路桥"],
    ["au-elsternwick", "https://commons.wikimedia.org/wiki/File%3AElsternwick_Hotel.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/fd/Elsternwick_Hotel.jpg", "Donaldtong", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "The Elsternwick Hotel", "埃尔斯特恩威克酒店"],
    ["au-cleveland-tas", "https://commons.wikimedia.org/wiki/File%3ACleveland_Church_and_cemetery_1.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/25/Cleveland_Church_and_cemetery_1.jpg", "Mx. Granger", "CC0", "https://creativecommons.org/publicdomain/zero/1.0/", "The church (1855) and cemetery at Cleveland, Tasmania", "塔斯马尼亚克利夫兰的教堂（1855）与墓地"],
    ["au-esperance", "https://commons.wikimedia.org/wiki/File%3AWest_Beach%2C_Western_Australia%2C_January_2024_02.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/80/West_Beach%2C_Western_Australia%2C_January_2024_02.jpg", "Calistemon", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "West Beach, Esperance", "埃斯佩兰斯的西海滩"],
    ["au-normanton", "https://commons.wikimedia.org/wiki/File%3ANormanton-queensland-australia-gulf-savannah-gulf-of-carpetnaria.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/ab/Normanton-queensland-australia-gulf-savannah-gulf-of-carpetnaria.jpg", "www.gondwananet.com", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The welcome sign at Normanton, in the Gulf Savannah", "海湾草原上诺曼顿镇口的欢迎牌"],
    ["au-fitzroy", "https://commons.wikimedia.org/wiki/File%3AAQUA_PROFONDA_%28Fitzroy_Pool%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/27/AQUA_PROFONDA_%28Fitzroy_Pool%29.jpg", "Ashton 29", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The heritage-listed AQUA PROFONDA sign at the Fitzroy Swimming Pool", "菲茨罗伊泳池列入文物名录的 AQUA PROFONDA 标牌"],
    ["au-castle-hill", "https://commons.wikimedia.org/wiki/File%3ACastle_Hill_Heritage_Park_01.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/d2/Castle_Hill_Heritage_Park_01.jpg", "Collywolly", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Castle Hill Heritage Park", "卡斯尔山遗产公园"],
    ["au-ballarat", "https://commons.wikimedia.org/wiki/File%3ASovereign_hill_D1000053.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/06/Sovereign_hill_D1000053.jpg", "Anne-Marie Steenbergen", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Sovereign Hill, the open-air gold-rush museum at Ballarat", "巴拉瑞特的露天淘金博物馆“君主山”"],
    ["au-glenrowan", "https://commons.wikimedia.org/wiki/File%3AGlenrowan_inn.JPG", "https://upload.wikimedia.org/wikipedia/commons/d/d3/Glenrowan_inn.JPG", "Peterdownunder", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The site of the Glenrowan Inn, where the Kelly Gang made its last stand", "格伦罗万旅店旧址——凯利帮最后一战之地"],
    ["au-darra", "https://commons.wikimedia.org/wiki/File%3ALinh_Son_Buddhist_Temple%2C_89_Rowe_Street%2C_Darra%2C_Brisbane%2C_2023_02.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/74/Linh_Son_Buddhist_Temple%2C_89_Rowe_Street%2C_Darra%2C_Brisbane%2C_2023_02.jpg", "Kerry Raymond", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "Linh Son Buddhist Temple, Darra", "达拉的灵山佛寺"],
    ["au-beulah", "https://commons.wikimedia.org/wiki/File%3ABeulah_Victoria_Hotel.JPG", "https://upload.wikimedia.org/wikipedia/commons/1/1a/Beulah_Victoria_Hotel.JPG", "Peterdownunder", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Victoria Hotel, Beulah", "比尤拉的维多利亚酒店"],
    ["au-northern-beaches", "https://commons.wikimedia.org/wiki/File%3APalm_Beach_Sydney_5.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c1/Palm_Beach_Sydney_5.jpg", "Graeme Churchard", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0", "Palm Beach, on Sydney's Northern Beaches", "悉尼北部海滩的棕榈滩"],
    ["au-raymond-terrace", "https://commons.wikimedia.org/wiki/File%3AWirrawee_Cinema_King_Street%2C_Raymond_Terrace%2C_New_South_Wales%2C_Australia.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/33/Wirrawee_Cinema_King_Street%2C_Raymond_Terrace%2C_New_South_Wales%2C_Australia.jpg", "AussieLegend", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "The 'Wirrawee Cinema' set built in King Street, Raymond Terrace, for the 2010 film", "2010 年电影在雷蒙德台地国王街搭的“维拉威电影院”布景"],
    ["au-pemberton", "https://commons.wikimedia.org/wiki/File%3APemberton_town_vasse_highway.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/ec/Pemberton_town_vasse_highway.jpg", "JAW", "CC BY-SA 3.0", "http://creativecommons.org/licenses/by-sa/3.0/", "Brockman Street, the main street of Pemberton", "彭伯顿的主街布罗克曼街"],
    ["au-unimelb", "https://commons.wikimedia.org/wiki/File%3AThe_natural_philosophy_building_at_the_University_of_Melbourne%2C_Parkville.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/84/The_natural_philosophy_building_at_the_University_of_Melbourne%2C_Parkville.jpg", "Drechmeria-RBGV", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The old Natural Philosophy building at the University of Melbourne, Parkville", "墨尔本大学帕克维尔校区的旧自然哲学楼"],
    ["au-stanley", "https://commons.wikimedia.org/wiki/File%3APark_-_Stanley%2C_Tasmania_%2826183878166%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/ba/Park_-_Stanley%2C_Tasmania_%2826183878166%29.jpg", "Michael Coghlan", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "Stanley, Tasmania, below the Nut", "塔斯马尼亚斯坦利镇，背后是“坚果”岩"],
    ["au-antarctic-division", "https://commons.wikimedia.org/wiki/File%3AMacquarie_station%2C_Macquarie_Island.JPG", "https://upload.wikimedia.org/wikipedia/commons/0/08/Macquarie_station%2C_Macquarie_Island.JPG", "Krudller", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The isthmus and research station on Macquarie Island", "麦夸里岛的地峡与考察站"],
    ["au-glebe", "https://commons.wikimedia.org/wiki/File%3A%281%29Derwent_Street_Glebe_022.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1f/%281%29Derwent_Street_Glebe_022.jpg", "Sardaka", "CC0", "https://creativecommons.org/publicdomain/zero/1.0/", "A corner house in Derwent Street, Glebe", "格利布德温特街的一座街角房子"],
    ["au-norman-lindsay", "https://commons.wikimedia.org/wiki/File%3A%281%29Norman_Lindsay_Gallery_060.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/0d/%281%29Norman_Lindsay_Gallery_060.jpg", "Sardaka", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Norman Lindsay Gallery, Faulconbridge", "福尔肯布里奇的诺曼·林赛美术馆"],
    ["au-burketown", "https://commons.wikimedia.org/wiki/File%3ABurketown-pub-gulf-savannah-queensland-australia.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/ae/Burketown-pub-gulf-savannah-queensland-australia.jpg", "www.gondwananet.com", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Burketown pub", "伯克敦的酒馆"],
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
