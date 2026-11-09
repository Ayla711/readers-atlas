"""11-09: foreign writers on Britain — the five most famous works chosen by the user: The Three Musketeers (Dumas), Around the
World in Eighty Days (Verne; already in, gets two more places), Caesar's Gallic War books 4–5, Hugo's The Man Who Laughs, and
the manga Black Butler (in copyright: scene notes only). Originals and public-domain English translations both cut from the
downloaded Project Gutenberg files; the Latin from #218 (books I–IV) and #18837 (books V–VIII).
Usage: python3 -I add_batch19.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, re, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch19.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
b5.D = ", 2026-11-09"
append, prose, PIL, ORIG, W = b5.append, b5.prose, b5.PIL, b5.ORIG, b5.W
G = "https://www.gutenberg.org/ebooks/"

def paras(book, *pairs):
    """adjacent paragraphs, each cut with prose(), joined with a newline (the convention in 6.6)"""
    return "\n".join(prose(book, a, b) for a, b in pairs)

books = [
    dict(id="three-musketeers", title="The Three Musketeers", title_zh="三个火枪手", title_orig="Les Trois Mousquetaires", author="Alexandre Dumas", author_zh="大仲马",
         author_orig="Alexandre Dumas", year="1844", orig_lang="fr", public_domain=True, source_url=G + "1257", aliases=["三剑客", "The Three Musketeers"]),
    dict(id="gallic-war", title="Commentaries on the Gallic War", title_zh="高卢战记", title_orig="Commentarii de Bello Gallico", author="Julius Caesar", author_zh="恺撒",
         author_orig="C. Iulius Caesar", year="c. 50 BC", orig_lang="la", public_domain=True, source_url=G + "10657", aliases=["De Bello Gallico", "The Gallic Wars", "凯撒", "高卢战纪"]),
    dict(id="man-who-laughs", title="The Man Who Laughs", title_zh="笑面人", title_orig="L'Homme qui rit", author="Victor Hugo", author_zh="雨果",
         author_orig="Victor Hugo", year="1869", orig_lang="fr", public_domain=True, source_url=G + "12587", aliases=["By Order of the King"]),
    dict(id="black-butler", title="Black Butler", title_zh="黑执事", title_orig="黒執事", author="Yana Toboso", author_zh="枢梁", author_orig="枢やな",
         year="2006–", orig_lang="ja", public_domain=False, source_url=None, aliases=["Kuroshitsuji", "黒執事"]),
]

places = [
    ORIG("buckingham-house-portsmouth", "Buckingham House, Old Portsmouth", "老朴茨茅斯 · 白金汉府", 50.7915, -1.1008,
         "Buckingham House, 10½–11 High Street (British Listed Buildings, Grade II*)", "https://britishlistedbuildings.co.uk/101104356-buckingham-house-st-thomas-ward",
         "The house at 11 High Street where the Duke of Buckingham was stabbed by John Felton on 23 August 1628, the event Dumas rewrites at the end of The Three Musketeers. A 16th-century timber-framed house, later an inn, now offices and flats; a plaque on the wall records the assassination",
         "高街 11 号，1628 年 8 月 23 日白金汉公爵在这里被约翰·费尔顿刺死，大仲马在《三个火枪手》结尾重写了这件事。房子建于 16 世纪，木结构，后来做过客栈，现在是办公室和公寓，墙上有纪念牌"),
    ORIG("savile-row", "Savile Row", "萨维尔街", 0, 0, "", "",
         "The tailors' street in Mayfair. Verne gave Phileas Fogg a house at No. 7, from which he sets out on his wager",
         "梅费尔的裁缝街。凡尔纳让菲利亚斯·福格住在 7 号，他就是从这里出发去打那个赌的"),
    ORIG("liverpool", "Liverpool", "利物浦", 53.4072, -2.9917, "Liverpool (Wikipedia)", W + "Liverpool",
         "The great transatlantic port of the 19th century. Fogg lands here from America six hours short of London, and is arrested on the quay",
         "19 世纪横渡大西洋的大港。福格从美洲回来在这里上岸，离伦敦只差六个小时，却在码头上被捕", city=True),
    ORIG("walmer-beach", "Walmer beach, near Deal", "迪尔附近 · 沃尔默海滩", 51.21113, 1.40292, "Caesar's first invasion plaque, Walmer (Historical Marker Database)", "https://www.hmdb.org/m.asp?m=24553",
         "Caesar names no beach, only an open, level shore a few miles on from the cliffs. The traditional landing place of 55 BC is the shingle between Walmer and Deal, marked by a plaque on the seafront; archaeology since 2017 points to Pegwell Bay, further north, for the 54 BC landing",
         "恺撒没有写出登陆的地名，只说离开悬崖几英里后是一片开阔平坦的海岸。传统上认为公元前 55 年的登陆地是沃尔默和迪尔之间的卵石滩，海滨有一块纪念牌；2017 年以来的考古发现则把公元前 54 年的登陆地指向更北的佩格韦尔湾"),
    ORIG("brentford-monument", "Brentford Monument", "布伦特福德纪念柱", 51.48412, -0.30401, "List of public art in the London Borough of Hounslow (Wikipedia)", W + "List_of_public_art_in_the_London_Borough_of_Hounslow",
         "A granite column of 1909 on Brentford High Street recording four events, the first being Caesar's crossing of the Thames in 54 BC against Cassivellaunus at the ancient ford here. Caesar himself names only the river; Brentford is the traditional identification of his one fordable place",
         "布伦特福德高街上 1909 年立的花岗岩柱，刻着四件史事，第一件是公元前 54 年恺撒在这里的古渡口渡过泰晤士河、击退卡西维拉努斯。恺撒本人只写了河名；布伦特福德是传统上对那个唯一可涉水之处的考订"),
    ORIG("isle-of-portland", "Isle of Portland", "波特兰岛", 50.55, -2.44, "Isle of Portland (Wikipedia)", W + "Isle_of_Portland",
         "A limestone peninsula off Weymouth, tied to the mainland by Chesil Beach. The Man Who Laughs opens here on a January night in 1690, when the child Gwynplaine is abandoned on the shore",
         "韦茅斯外海的石灰岩半岛，靠切瑟尔海滩和大陆相连。《笑面人》就从 1690 年 1 月的一个夜晚、小格温普兰被丢在这片海岸上开始"),
    ORIG("southwark", "Southwark", "南华克", 51.4989, -0.0925, "Southwark (Wikipedia, OS grid TQ325795)", W + "Southwark",
         "The borough south of London Bridge, for centuries the city's playground of inns, theatres and bear-gardens. Hugo sets Ursus's Green Box and the Tadcaster Inn on Tarrinzeau Field, a fairground he places here",
         "伦敦桥南岸的区，几百年来是伦敦人寻欢的地方，客栈、剧院、斗熊场都在这里。雨果把于尔絮斯的“绿箱子”和塔德卡斯特客栈安排在他虚构于此的塔林佐场"),
    ORIG("southampton", "Southampton", "南安普敦", 50.9025, -1.40417, "Southampton (Wikipedia)", W + "Southampton",
         "The great liner port on the south coast, where the Titanic sailed from in 1912. In Black Butler the Campania leaves from here for America",
         "英国南岸的大邮轮港，1912 年泰坦尼克号从这里出发。《黑执事》里的坎帕尼亚号也是从这里开往美洲", city=True),
]
SRC = {
    "savile-row": W + "Savile_Row", "walmer-beach": W + "Julius_Caesar%27s_invasions_of_Britain", "brentford-monument": "https://londonremembers.com/memorials/brentford-monument",
    "isle-of-portland": W + "Isle_of_Portland", "southwark": W + "Southwark", "southampton": "https://kuroshitsuji.fandom.com/wiki/Luxury_Liner_Arc", "liverpool": W + "Liverpool",
    "buckingham-house-portsmouth": "https://britishlistedbuildings.co.uk/101104356-buckingham-house-st-thomas-ward",
}
for p in places:
    p["fact_source"] = SRC[p["id"]]

def FL(id, book_id, place, loc, loc_zh, en, orig, hl_en, hl_orig, translation, checked):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_orig: assert h in orig, (id, h)
    return dict(id=id, book_id=book_id, place_ids=[place], location=loc, location_zh=loc_zh, text_en=en, text_orig=orig,
                highlight_en=hl_en, highlight_orig=hl_orig, translation=translation, status="draft", checked=checked + b5.D)
def S(id, book_id, place, loc, loc_zh, en, zh, hl_en, hl_zh, src):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book_id, place_ids=[place], location=loc, location_zh=loc_zh, text_en=en, text_zh=zh,
                highlight_en=hl_en, highlight_zh=hl_zh, status="draft", fact_source=src)

TM = "anonymous English translation (Project Gutenberg #1257)"
MWL = "anonymous English translation of 1888 (Project Gutenberg #12587)"
CAE = "W. A. McDevitte and W. S. Bohn (1869)"
TOWLE = "George M. Towle (1873)"
lines = [
    FL("tm-1", "three-musketeers", "dover", "Volume 1, Chapter 20, The Journey", "第一卷第 20 章《旅程》",
       prose(1257, "On the morrow, at break of day", "crying, \"Here I am at last!\""),
       paras(13951, ("Le lendemain, au point du jour", "l'on avait peu marché."), ("À dix heures, le bâtiment", "le port de Douvres."),
             ("À dix heures et demie, d'Artagnan", "d'Angleterre, en s'écriant:"), ("«Enfin, m'y voilà!»", "«Enfin, m'y voilà!»")),
       ["Dover"], ["Douvres"], TM, "Project Gutenberg #13951 (French) and #1257"),
    FL("tm-2", "three-musketeers", "buckingham-house-portsmouth", "Volume 2, Chapter 59, What Took Place at Portsmouth, August 23, 1628", "第二卷第 59 章《1628 年 8 月 23 日朴茨茅斯发生的事》",
       paras(1257, ("Felton took advantage of this moment", "up to the handle."), ("\"Ah, traitor,\" cried Buckingham", "you have killed me!\""), ("\"Murder!\" screamed Patrick.", "\"Murder!\" screamed Patrick.")),
       paras(13951, ("Felton profita du moment", "jusqu'au manche."), ("«Ah! traître! cria Buckingham", "tu m'as tué…"), ("— Au meurtre!» hurla Patrick.", "— Au meurtre!» hurla Patrick.")),
       ["Felton", "Buckingham"], ["Felton", "Buckingham"], TM, "Project Gutenberg #13951 (French) and #1257"),
    FL("atw-2", "around-the-world", "savile-row", "Chapter 1", "第 1 章",
       prose(103, "Mr. Phileas Fogg lived, in 1872", "growing old."),
       prose(800, "En l'année 1872, la maison portant", "attirer l'attention."),
       ["Saville Row", "Burlington Gardens"], ["Saville-row", "Burlington Gardens"], TOWLE, "Project Gutenberg #800 (French) and #103 (Towle)"),
    FL("atw-3", "around-the-world", "liverpool", "Chapter 33", "第 33 章",
       paras(103, ("Phileas Fogg at last disembarked", "distant from London."), ("But at this moment Fix came up", "\"You are really Phileas Fogg?\""), ("\"I am.\"", "\"I am.\""), ("\"I arrest you in the Queen's name!\"", "\"I arrest you in the Queen's name!\"")),
       paras(800, ("À midi moins vingt, le 21 décembre", "six heures de Londres."), ("Mais à ce moment, Fix s'approcha", "exhibant son mandat:"), ("«Vous êtes le sieur Phileas Fogg?", "dit-il."), ("—Oui, monsieur.", "—Oui, monsieur."), ("—Au nom de la reine, je vous arrête!»", "—Au nom de la reine, je vous arrête!»")),
       ["Liverpool quay"], ["quai de Liverpool"], TOWLE, "Project Gutenberg #800 (French) and #103 (Towle)"),
    FL("gw-1", "gallic-war", "dover", "Book 4, Chapter 23", "第四卷第 23 章",
       prose(10657, "he himself reached Britain with the first squadron", "for the other ships to arrive there."),
       prose(218, "ipse hora diei circiter IIII.", "in ancoris expectavit."),
       ["Britain", "the sea was confined by mountains"], ["Britanniam", "montibus"], CAE, "Project Gutenberg #218 (Latin, books I–IV) and #10657 (McDevitte and Bohn)"),
    FL("gw-2", "gallic-war", "walmer-beach", "Book 4, Chapter 25", "第四卷第 25 章",
       prose(10657, "And while our men were hesitating", "all leaped from the ship."),
       prose(218, "Atque nostris militibus cunctantibus", "universi ex navi desiluerunt."),
       ["eagle of the tenth legion"], ["X legionis aquilam"], CAE, "Project Gutenberg #218 (Latin, books I–IV) and #10657 (McDevitte and Bohn)"),
    FL("gw-3", "gallic-war", "brentford-monument", "Book 5, Chapter 18", "第五卷第 18 章",
       prose(10657, "Caesar, discovering their design, leads his army", "committed themselves to flight."),
       prose(18837, "Caesar cognito consilio eorum ad flumen Tamesim", "se fugae mandarent."),
       ["Thames"], ["Tamesim"], CAE, "Project Gutenberg #18837 (Latin, books V–VIII) and #10657 (McDevitte and Bohn)"),
    FL("mwl-1", "man-who-laughs", "isle-of-portland", "Part 1, Book 1, Chapter 1, Portland Bill", "第一部第一卷第 1 章《波特兰角》",
       prose(12587, "One evening, towards the close of one of the most bitter days", "not daring to re-enter."),
       prose(5423, "Un soir, vers la fin d'une des plus glaciales journées", "n'osant rentrer."),
       ["bay of Portland"], ["golfe de Portland"], MWL, "Project Gutenberg #5423 (French) and #12587"),
    FL("mwl-2", "man-who-laughs", "southwark", "Part 2, Book 3, Chapter 1, The Tadcaster Inn", "第二部第三卷第 1 章《塔德卡斯特客栈》",
       paras(12587, ("The bowling-green of Southwark was called Tarrinzeau Field", "parochial property."), ("Tarrinzeau Field was a kind of permanent fair ground", "means to go to the play.")),
       paras(5423, ("Le bowling-green de Southwark s'appelait Tarrinzeau-field", "propriété paroissiale."), ("Le Tarrinzeau-field était une sorte de champ de foire permanent", "c'est aller au spectacle.")),
       ["Southwark", "Tarrinzeau Field"], ["Southwark", "Tarrinzeau-field"], MWL, "Project Gutenberg #5423 (French) and #12587"),
    S("bb-s1", "black-butler", "whitechapel", "Volume 2, the Jack the Ripper case", "第 2 卷，开膛手杰克篇",
      "Prostitutes are being murdered in Whitechapel and the Queen sends her Watchdog to find the killer. Ciel Phantomhive and his butler Sebastian work the case with Ciel's aunt Madam Red and the Undertaker, and the trail leads somewhere very close to home.",
      "白教堂区接连有妓女被杀，女王派她的“看门狗”去查凶手。夏尔·凡多姆海恩和管家塞巴斯蒂安同姨妈红夫人、葬仪屋一起追查，线索最后指向离他们极近的人。",
      ["Whitechapel"], ["白教堂区"], "https://otakuusamagazine.com/black-butler-vol-2/"),
    S("bb-s2", "black-butler", "southampton", "Volume 12, Chapter 51, the luxury liner Campania", "第 12 卷第 51 话，豪华客轮坎帕尼亚号",
      "On 17 April the liner Campania sails from Southampton for America with Ciel, Sebastian and Snake aboard, following the Aurora Society and its promise to raise the dead; the voyage ends in a shipwreck.",
      "4 月 17 日，豪华客轮坎帕尼亚号从南安普敦启航前往美洲，夏尔、塞巴斯蒂安和斯内克也在船上，为的是追查宣称能让死者复活的曙光会；这趟航行以沉船收场。",
      ["Southampton"], ["南安普敦"], "https://kuroshitsuji.fandom.com/wiki/Luxury_Liner_Arc"),
]

COORDS = json.load(open(f"{PW}/coords.json", encoding="utf-8"))
for p in places:
    if p["id"] in COORDS:
        la, lo, st, su = COORDS[p["id"]]
        p["lat"], p["lon"], p["coord_checked"] = la, lo, f"{st} — {su}{b5.D}"
    assert p["lat"] and p["coord_checked"].split(" — ")[1].startswith("http"), p["id"]

PHOTOS = json.load(open(f"{PW}/choice.json", encoding="utf-8"))
cands = json.load(open(f"{PW}/candidates.json"))
for p in places:
    if p["id"] not in PHOTOS:
        continue
    n, en, zh, crop = PHOTOS[p["id"]]
    c = cands[p["id"]]["candidates"][n]
    im = Image.open(f"{PW}/dl/{p['id']}__{n}.jpg").convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, p["id"]
    rel = f"images/places/{p['id']}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)
    p["photo"] = {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip() or "Unknown author", "license": c["license"].strip(),
                  "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}
    if crop:
        p["photo"]["cropped"] = True

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-09 外国作家写英国：大仲马、恺撒、雨果（原文 + 公有领域英译），《黑执事》（有版权，只写场景说明）")
    append(f"{APP}/data/places.js", places, "11-09 外国作家写英国（坐标和照片均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-09 外国作家写英国：古登堡原文 + 公有领域英译逐字截取；《黑执事》两条场景说明（草稿，待审核）")
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places if "photo" in p]
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    for l in lines:
        print(l["id"], "|", l["text_en"][:90].replace("\n", " / "))
