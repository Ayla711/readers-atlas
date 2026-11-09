"""11-05: Byron and Percy Bysshe Shelley. Four Byron places (Newstead Abbey, Hucknall, Harrow churchyard, Lochnagar),
three Shelley places (University College, Albion House, St Peter's Field) and Shelley's books linked to the existing
Bournemouth grave. Excerpts cut out of the downloaded Project Gutenberg files (#21700 Don Juan, #8861 Byron's early
poems, #4800 Shelley's poems). Facts from Wikipedia, the Coleridge edition of Byron (PG #18762), British Listed
Buildings and the Chilterns AONB page; coordinates from Wikipedia, Geograph or the listing; photos from Commons.
Usage: python3 -I add_batch13.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, re, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch13.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
b5.D = ", 2026-11-05"          # P() reads the date from the module at call time
append, ORIG, PIL, W, G = b5.append, b5.ORIG, b5.PIL, b5.W, b5.G
COM = "https://commons.wikimedia.org/wiki/"

def V(book, start, n, strip_quotes=False):
    """n verse lines from the line containing `start`; editor's footnote markers ([2], [ii]) and line numbers removed"""
    t = b5.verse_lines(book, start, n)
    t = "\n".join(re.sub(r"\s*\[[0-9ivxlc]+\]", "", l).rstrip() for l in t.split("\n"))
    if strip_quotes:
        t = t.strip("'")
    return t

def B(id, title, title_zh, author, author_zh, year, pg, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year, orig_lang="en",
             public_domain=True, source_url=G + str(pg))
    d.update(kw)
    return d
BYRON, SHELLEY = ("Lord Byron", "拜伦"), ("Percy Bysshe Shelley", "珀西·比希·雪莱")
books = [
    B("hours-of-idleness", "Hours of Idleness", "闲暇时光", *BYRON, "1807", 8861, aliases=["Poems Original and Translated"]),
    B("don-juan", "Don Juan", "唐璜", *BYRON, "1819–1824", 21700),
    B("revolt-of-islam", "The Revolt of Islam", "伊斯兰的起义", *SHELLEY, "1818", 4800, aliases=["Laon and Cythna", "莱昂与茜丝娜", "Percy Shelley", "珀西·雪莱"]),
    B("mask-of-anarchy", "The Mask of Anarchy", "暴政的假面游行", *SHELLEY, "1832", 4800, aliases=["The Masque of Anarchy", "Percy Shelley", "珀西·雪莱"]),
]

places = [
    PIL("newstead-abbey", "Newstead Abbey", "纽斯特德修道院", 53.0783, -1.1925, "Newstead Abbey (Wikipedia)", W + "Newstead_Abbey",
        "Byron's family seat. He inherited it with the title in 1798, aged ten, lived here for short spells from 1808, and sold it in 1818 while he was in Italy. The Norman Abbey of Don Juan, Cantos 13 to 16, is drawn from it. It now belongs to Nottingham City Council and is open to visitors, with a Byron museum inside",
        "拜伦家族的祖宅。1798 年他十岁时连同爵位一起继承下来，1808 年起断断续续住过几段时间，1818 年人在意大利时把它卖掉。《唐璜》第十三到十六章里的诺曼修道院就是照它写的。现在归诺丁汉市政府所有，对外开放，里面有拜伦博物馆",
        ["hours-of-idleness", "don-juan"]),
    PIL("byron-hucknall", "Byron's grave, Hucknall", "哈克诺尔 · 拜伦墓", 53.0394, -1.2064,
        "Church of St Mary Magdalene, Hucknall (Wikipedia)", W + "Church_of_St_Mary_Magdalene,_Hucknall",
        "Byron died at Missolonghi in Greece in 1824. Westminster Abbey refused to bury him, and he was laid in the Byron family vault in St Mary Magdalene's. A marble slab given by the King of Greece lies above the grave, and his daughter Ada Lovelace was later buried beside him. Westminster Abbey put up a memorial to him in 1969",
        "拜伦 1824 年死在希腊的迈索隆吉翁。威斯敏斯特教堂拒绝让他入葬，他被葬进这座圣玛利亚·抹大拉教堂里的拜伦家族墓穴。墓上那块大理石板是希腊国王送的，他的女儿艾达·洛芙莱斯后来也葬在他身旁。威斯敏斯特教堂直到 1969 年才为他立了纪念碑",
        ["hours-of-idleness", "don-juan"]),
    ORIG("harrow-peachey", "St Mary's churchyard, Harrow on the Hill", "哈罗山 · 圣玛利亚教堂墓园", 51.5741, -0.3381,
         "The Peachey tomb in St Mary's Churchyard, Harrow on the Hill (Geograph photo by Marathon, Commons object location)",
         COM + "File:The_Peachey_tomb_in_St_Mary%27s_Churchyard,_Harrow_on_the_Hill_-_geograph.org.uk_-_4730479.jpg",
         "As a boy at Harrow School, from 1801 to 1805, Byron liked to sit and daydream by the Peachey Tomb here, his 'favourite tombstone'. The elm of the poem burnt down before 1935; a stone put up in front of the tomb in 1905 carries the poem. His daughter Allegra lies in an unmarked grave by the south porch",
         "拜伦 1801 至 1805 年在哈罗公学读书，常坐在这里的皮奇墓旁发呆，说它是“我最喜欢的墓碑”。诗里那棵榆树 1935 年以前就烧毁了；墓前有一块 1905 年立的石碑，刻着这首诗。他的女儿阿莱格拉葬在教堂南门廊旁，墓上没有标记"),
    ORIG("lochnagar", "Lochnagar", "洛赫纳加山", 56.9547, -3.2403, "Lochnagar (Wikipedia), summit", W + "Lochnagar",
         "A 1,155-metre mountain on the Balmoral estate in the Cairngorms. Byron spent part of his childhood in Aberdeenshire, and in his note to the poem says he lived near it in his early years. The marker is at the summit",
         "凯恩戈姆山区巴尔莫勒尔庄园里的一座山，海拔 1155 米。拜伦童年有一段时间住在阿伯丁郡，他在这首诗的注里说，自己小时候就住在这座山附近。标记放在山顶"),
    PIL("shelley-memorial", "Shelley Memorial, University College, Oxford", "牛津大学学院 · 雪莱纪念像", 51.7526, -1.2524,
        "Shelley Memorial (Wikipedia)", W + "Shelley_Memorial",
        "Shelley came up to University College in 1810 and was expelled on 25 March 1811, with his friend Thomas Jefferson Hogg, over the pamphlet The Necessity of Atheism. The college now honours him: Edward Onslow Ford's marble figure of the drowned poet, first meant for his grave in Rome, has stood in a domed room off the High Street since 1893",
        "雪莱 1810 年进大学学院，1811 年 3 月 25 日因为小册子《无神论的必要性》和朋友霍格一起被开除。现在学院以他为荣：爱德华·昂斯洛·福特雕的溺水诗人大理石像，原本打算放在他罗马的墓地，1893 年起安放在高街边一间带穹顶的小屋里",
        ["revolt-of-islam", "mask-of-anarchy"]),
    PIL("albion-house", "Albion House, Marlow", "马洛 · 阿尔比恩宅", 51.5704, -0.7808,
        "Albion House / Shelley Cottage, Marlow (British Listed Buildings, Grade II)", "https://britishlistedbuildings.co.uk/101217597-albion-houseshelley-cottageshelley-house-marlow",
        "The Shelleys lived at Albion House, 104 West Street, from March 1817 to February 1818. Percy wrote Laon and Cythna, reissued as The Revolt of Islam, in the woods near Marlow, and Mary finished Frankenstein here. The house is now private, as Shelley Cottages, with a plaque outside",
        "雪莱一家 1817 年 3 月到 1818 年 2 月住在西街 104 号的阿尔比恩宅。珀西在马洛附近的树林里写了长诗《莱昂与茜丝娜》（后改名《伊斯兰的起义》），玛丽在这里写完了《弗兰肯斯坦》。房子现在叫雪莱小屋，是私宅，门外有纪念牌",
        ["revolt-of-islam", "frankenstein"]),
    ORIG("peterloo", "St Peter's Field (Peterloo), Manchester", "曼彻斯特 · 圣彼得广场（彼得卢）", 53.4766, -2.2457,
         "Peterloo Memorial (Wikipedia)", W + "Peterloo_Memorial",
         "On 16 August 1819 cavalry charged a crowd of tens of thousands gathered on St Peter's Field to call for parliamentary reform; eighteen people were killed and hundreds injured. Shelley, in Italy, heard the news in September and wrote The Mask of Anarchy, 'written on the occasion of the massacre at Manchester'; it was not published until 1832. The field is now St Peter's Square, and Jeremy Deller's Peterloo Memorial was unveiled beside it in 2019. The marker is at the memorial",
         "1819 年 8 月 16 日，数万人聚集在圣彼得广场要求议会改革，骑兵冲进人群，造成 18 人死亡、数百人受伤。雪莱当时在意大利，9 月才得到消息，写下《暴政的假面游行》，副标题是“为曼彻斯特屠杀而作”，直到 1832 年才出版。这片空地现在是圣彼得广场，2019 年杰里米·德勒设计的彼得卢纪念碑在旁边落成。标记放在纪念碑处"),
]

def L(id, book, place, loc, loc_zh, text, hl, pg):
    for h in hl:
        assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl,
                translation="original", status="draft", checked=f"Project Gutenberg #{pg}{b5.D}")
lines = [
    L("dj-1", "don-juan", "newstead-abbey", "Canto 13, stanza 55", "第十三章第 55 节",
      V(21700, "To Norman Abbey whirl'd the noble pair", 8), ["Norman Abbey"], 21700),
    L("hoi-1", "hours-of-idleness", "newstead-abbey", "On Leaving Newstead Abbey, stanza 1", "《离别纽斯特德修道院》第 1 节",
      V(8861, "Through thy battlements, Newstead", 4), ["Newstead"], 8861),
    L("hoi-2", "hours-of-idleness", "harrow-peachey", "Lines Written beneath an Elm in the Churchyard of Harrow (added in the 1808 edition)",
      "《哈罗墓园榆树下》（1808 年版增补）", V(8861, "Spot of my youth! whose hoary branches sigh", 10), ["Spot of my youth", "Thou drooping Elm"], 8861),
    L("hoi-3", "hours-of-idleness", "lochnagar", "Lachin y Gair, stanza 5", "《洛赫纳加》第 5 节",
      V(8861, "Years have roll'd on, Loch na Garr, since I left you", 8), ["Loch na Garr"], 8861),
    L("ma-1", "mask-of-anarchy", "peterloo", "Stanza 38 (repeated as the last stanza, 91)", "第 38 节（全诗最后一节第 91 节重复了这一节）",
      V(4800, "'Rise like Lions after slumber", 5, strip_quotes=True), ["Ye are many—they are few"], 4800),
]

PHOTOS = json.load(open(f"{PW}/choice.json"))   # {place_id: [candidate_no, alt_en, alt_zh, cropped?]}
cands = json.load(open(f"{PW}/candidates.json"))
for p in places:
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
    p["photo"] = {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip(), "license": c["license"].strip(),
                  "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}
    if crop:
        p["photo"]["cropped"] = True

def link_bournemouth():
    path = f"{APP}/data/places.js"
    s = open(path, encoding="utf-8").read()
    old = '"mary-shelley-grave"'
    i = s.index("{ id: " + old)
    j = s.index('book_ids: ["frankenstein"]', i)
    assert j - i < 600, "book_ids not where expected"
    s = s[:j] + 'book_ids: ["frankenstein", "revolt-of-islam", "mask-of-anarchy"]' + s[j + len('book_ids: ["frankenstein"]'):]
    open(path, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-05 拜伦与珀西·雪莱（古登堡原文）")
    append(f"{APP}/data/places.js", places, "11-05 拜伦与珀西·雪莱（坐标和照片均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-05 拜伦与珀西·雪莱：古登堡原文摘句（草稿，待审核）")
    link_bournemouth()
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places]
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    for l in lines:
        print(f"{l['id']:6}", l["text_en"].replace("\n", " / "))
