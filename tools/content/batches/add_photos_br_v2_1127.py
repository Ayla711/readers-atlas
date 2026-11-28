"""11-27: photos for the new Brazilian places of add_br_v2_1127.py: freely licensed Wikimedia Commons photos (CC0, public
domain, CC BY, CC BY-SA; never NC or ND, never ported licences), chosen by eye from contact sheets of candidates
(tools/content/photos/find_photos.py). No photo of the Espaço Pasárgada house itself is on Commons;
its place shows the Capibaribe and Rua da Aurora in the same Boa Vista quarter, about 450 m away, and the alt text says so.

Usage: python3 -I tools/content/batches/add_photos_br_v2_1127.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""

import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["br-rio-de-janeiro", "https://commons.wikimedia.org/wiki/File:Copacabana,_Rio_de_Janeiro,_Brazil.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/8e/Copacabana%2C_Rio_de_Janeiro%2C_Brazil.jpg", "Wilfredor", "CC0", "https://creativecommons.org/publicdomain/zero/1.0/", "Copacabana beach, Rio de Janeiro, from the hills above", "从山上俯瞰里约热内卢的科帕卡巴纳海滩"],
    ["br-pindorama", "https://commons.wikimedia.org/wiki/File%3ACidade_de_Pindorama_vista_da_rodovia_vicinal_de_acesso_a_Usina_Catanduva_e_Palmares_Paulista_-_panoramio.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/de/Cidade_de_Pindorama_vista_da_rodovia_vicinal_de_acesso_a_Usina_Catanduva_e_Palmares_Paulista_-_panoramio.jpg", "MARCO AURÉLIO ESPARZ…", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Pindorama seen across the farmland from a country road", "从乡间公路远望农田那头的平多拉马"],
    ["br-itabira", "https://commons.wikimedia.org/wiki/File:Vista_Panoramica_da_cidade_de_Itabira.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/46/Vista_Panoramica_da_cidade_de_Itabira.jpg", "MateusItabira", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "A view over Itabira and the Minas Gerais hills", "俯瞰伊塔比拉和米纳斯吉拉斯的群山"],
    ["br-espaco-pasargada", "https://commons.wikimedia.org/wiki/File:Vue_sur_le_Rio_Capibaribe_(en_arri%C3%A8re-plan_Rua_da_Aurora,_Boa_Vista).jpg", "https://upload.wikimedia.org/wikipedia/commons/0/02/Vue_sur_le_Rio_Capibaribe_%28en_arri%C3%A8re-plan_Rua_da_Aurora%2C_Boa_Vista%29.jpg", "Antoine Guillas", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Capibaribe river and Rua da Aurora in Boa Vista, Recife, a few hundred metres from the house", "累西腓博阿维斯塔区的卡皮巴里比河和奥罗拉街，离这座老宅几百米"],
    ["br-belo-horizonte", "https://commons.wikimedia.org/wiki/File:Pra%C3%A7a_da_Liberdade,_Belo_Horizonte,_Minas_Gerais,_Brasil,_Brazil_2022.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/ec/Pra%C3%A7a_da_Liberdade%2C_Belo_Horizonte%2C_Minas_Gerais%2C_Brasil%2C_Brazil_2022.jpg", "Tet", "CC0", "https://creativecommons.org/publicdomain/zero/1.0/", "Praça da Liberdade, Belo Horizonte", "贝洛奥里藏特的自由广场"],
    ["br-rio-japura", "https://commons.wikimedia.org/wiki/File:Japur%C3%A1_River.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f5/Japur%C3%A1_River.jpg", "The original uploader was בן הטבע at Hebrew Wikipedia.", "CC BY-SA 2.5", "https://creativecommons.org/licenses/by-sa/2.5", "The Japurá river with flooded forest on its banks", "雅普拉河，岸边是被水淹没的森林"],
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
