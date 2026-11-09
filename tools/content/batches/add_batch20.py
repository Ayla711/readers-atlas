"""11-09 night: the Arthurian legend — a blind spot the coverage canon (authors and book lists) never reached.
Malory's Le Morte d'Arthur, Tennyson's Idylls of the King, Sir Gawain and the Green Knight (Middle English + Weston's
1898 prose), Wace's Roman de Brut (Mason's 1912 translation; stands in for Geoffrey of Monmouth, whose text is not on
Gutenberg), and T. H. White's The Once and Future King (in copyright: scene note only). Every excerpt is cut from the
downloaded Project Gutenberg files.
Usage: python3 -I add_batch20.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, re, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch20.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
b5.D = ", 2026-11-09"
append, prose, PIL, ORIG, PROTO, W, verse_lines, flat, norm = b5.append, b5.prose, b5.PIL, b5.ORIG, b5.PROTO, b5.W, b5.verse_lines, b5.flat, b5.norm
G = "https://www.gutenberg.org/ebooks/"

def me_lines(book, start, end):
    """Middle English verse from the Morris edition (#14568): the editor's line numbers, [A]-style sidenote marks, footnote
    marks and folio notes removed; the file prints yogh as the digit 3, restored to ȝ inside words"""
    raw = flat(book)[0].split("\n")
    out, on = [], False
    for l in raw:
        s = re.sub(r"^\s*\d*\s*(\[[A-Z]\])?\s*", "", l)
        s = re.sub(r"\[\d+\]|\[Fol\.[^\]]*\]", "", s).strip()
        s = re.sub(r"(?<=[A-Za-zþÞ'])3", "ȝ", s)
        s = re.sub(r"3(?=[a-zþ])", "ȝ", s)
        s = norm(s)
        if start in s:
            on = True
        if on and s:
            out.append(s)
        if on and end in s:
            return "\n".join(out)
    raise SystemExit(f"not found in {book}: {start}")

books = [
    dict(id="le-morte-darthur", title="Le Morte d'Arthur", title_zh="亚瑟王之死", author="Thomas Malory", author_zh="托马斯·马洛礼", year="1485", orig_lang="en",
         public_domain=True, source_url=G + "1251", aliases=["Morte d'Arthur", "Le Morte Darthur", "亚瑟王之死", "King Arthur"]),
    dict(id="idylls-of-the-king", title="Idylls of the King", title_zh="国王叙事诗", author="Alfred, Lord Tennyson", author_zh="丁尼生", year="1859–1885", orig_lang="en",
         public_domain=True, source_url=G + "610", aliases=["国王之歌", "国王牧歌", "The Passing of Arthur"]),
    dict(id="sir-gawain-green-knight", title="Sir Gawain and the Green Knight", title_zh="高文爵士与绿骑士", title_orig="Sir Gawayn and þe Grene Knyȝt", author="Anonymous (the Gawain Poet)",
         author_zh="佚名（高文诗人）", year="c. 1375–1400", orig_lang="enm", public_domain=True, source_url=G + "66084", aliases=["Gawain", "the Pearl Poet", "高文与绿骑士", "绿衣骑士"]),
    dict(id="roman-de-brut", title="Roman de Brut", title_zh="布鲁特传奇", title_orig="Roman de Brut", author="Wace", author_zh="瓦斯", author_orig="Wace", year="1155", orig_lang="fr",
         public_domain=True, source_url=G + "10472", aliases=["Brut", "Arthurian Chronicles", "Geste des Bretons", "瓦斯"],
         orig_note="Anglo-Norman French; no public-domain digital edition of the original is available, so the excerpts give Eugene Mason's 1912 translation only"),
    dict(id="once-and-future-king", title="The Once and Future King", title_zh="永恒之王", author="T. H. White", author_zh="T. H. 怀特", year="1958", orig_lang="en",
         public_domain=False, source_url=None, aliases=["The Sword in the Stone", "石中剑", "亚瑟王传奇"]),
]

places = [
    ORIG("tintagel-castle", "Tintagel Castle", "廷塔杰尔城堡", 50.66797, -4.75993, "Tintagel Castle (Wikipedia)", W + "Tintagel_Castle",
         "A headland castle on the north Cornish coast, built in the 1230s by Richard, Earl of Cornwall, on a site the legend had already claimed: Geoffrey of Monmouth (c. 1136) set Arthur's conception here, and Wace, Malory and Tennyson all keep Igraine shut up in Tintagel while Uther lays siege. English Heritage; a footbridge to the island since 2019",
         "康沃尔北岸的海岬城堡，1230 年代由康沃尔伯爵理查所建，但传说早已先占了这块地：蒙茅斯的杰弗里（约 1136 年）把亚瑟的受孕安排在这里，瓦斯、马洛礼、丁尼生都让伊格赖因被困在廷塔杰尔、乌瑟在城外围攻。现由英格兰遗产委员会管理，2019 年起有人行桥通往岛上"),
    ORIG("glastonbury-abbey", "Glastonbury Abbey", "格拉斯顿伯里修道院", 51.14611, -2.71528, "Glastonbury Abbey (Wikipedia)", W + "Glastonbury_Abbey",
         "The ruined abbey where in 1191 the monks announced they had found the grave of Arthur and Guinevere, a hollowed oak with two skeletons and a lead cross, now generally taken as a fund-raising stunt after the fire of 1184. Malory ends his book here: Lancelot, a hermit, buries Guinevere beside Arthur at the hermitage of Glastonbury. A marker in the grass shows the 1278 tomb site",
         "1191 年修士们宣布在这座修道院发现了亚瑟和桂妮薇儿的墓：一截挖空的橡木、两具骸骨和一个铅十字架，现在一般认为是 1184 年大火后为筹款做的噱头。马洛礼的书在这里结束：做了隐士的兰斯洛特把桂妮薇儿葬在格拉斯顿伯里隐修处亚瑟的身边。草地上有标志指出 1278 年迁葬的墓址"),
    ORIG("winchester-great-hall", "The Great Hall, Winchester", "温切斯特 · 大厅", 51.06243, -1.32054, "Winchester Castle (Wikipedia)", W + "Winchester_Castle",
         "All that stands of Winchester Castle: Henry III's hall of 1222–35, with the Round Table hanging on its wall. Tree-ring dating puts the table at 1250–80; Henry VIII had it painted with Arthur and the knights' names. Malory, writing in the 1460s, says plainly that Camelot 'is in English Winchester'",
         "温切斯特城堡只剩这座亨利三世 1222—1235 年建的大厅，墙上挂着那张圆桌。年轮测定圆桌做于 1250—1280 年；亨利八世命人画上亚瑟和骑士们的名字。马洛礼 1460 年代写书时直说卡美洛“用英语说就是温切斯特”"),
    PROTO("cadbury-castle", "Cadbury Castle, Somerset", "萨默塞特 · 卡德伯里城堡", 51.0242, -2.5317, "Cadbury Castle, Somerset (Wikipedia)", W + "Cadbury_Castle,_Somerset",
          "Camelot. Local tradition, first written down by John Leland in 1542, holds that this Iron Age hill fort was Arthur's Camelot; Leslie Alcock's 1966–70 excavations found it refortified around 500 with a great hall 20 metres long and pottery from the eastern Mediterranean — a real stronghold of a post-Roman ruler, whoever he was. The place Tennyson's 'city of shadowy palaces' is most often pinned to",
          "卡美洛。当地传说（1542 年约翰·利兰首次记下）认为这座铁器时代山堡就是亚瑟的卡美洛；1966—1970 年莱斯利·奥尔科克的发掘发现它在公元 500 年前后重新筑防，有一座 20 米长的大厅，还出土了东地中海的陶器——确实是某位后罗马时代统治者的要塞。丁尼生那座“宫殿幢幢如影的城”最常被钉在这里"),
    PROTO("dozmary-pool", "Dozmary Pool, Bodmin Moor", "博德明荒原 · 多兹玛丽池", 50.5423, -4.5502, "Dozmary Pool (Wikipedia)", W + "Dozmary_Pool",
          "The mere into which Excalibur is thrown. A small lake on Bodmin Moor; Cornish tradition says the Lady of the Lake gave Arthur the sword here and that Bedivere returned it here after Camlann. Tennyson's 'great water' beside a broken chapel is a poet's landscape, but this is where Cornwall puts it",
          "投剑的那片水。博德明荒原上的小湖；康沃尔的传说说湖中仙女在这里把剑交给亚瑟，卡姆兰之战后贝德维尔又在这里把剑还回去。丁尼生笔下破礼拜堂旁的“一片大水”是诗人的风景，但康沃尔把它放在这里"),
    PROTO("luds-church", "Lud's Church, Staffordshire", "斯塔福德郡 · 卢德教堂", 53.18778, -2.02056, "Lud's Church (Wikipedia)", W + "Lud%27s_Church",
          "The Green Chapel. A mossy chasm over 100 metres long and 18 deep, opened by a landslip above the River Dane. In 1958 R. W. V. Elliott, working from the poem's north-west Midlands dialect, proposed it as the Green Chapel where Gawain keeps his tryst; the poem's 'old cave, or a crevice of an old crag' fits it well. Nan Tor cave near Wetton Mill is the rival candidate",
          "绿教堂。戴恩河上方一道滑坡裂出的青苔峡谷，长 100 多米、深 18 米。1958 年 R. W. V. 埃利奥特根据诗的西北米德兰方言，提出这里就是高文赴约的绿教堂；诗里“一个老洞，或老岩壁上的一道裂缝”和它很合。韦顿磨坊附近的南托尔洞是另一个候选地"),
    ORIG("caerleon", "Caerleon", "卡利恩", 51.61005, -2.95529, "Caerleon Roman Fortress and Baths (Wikipedia)", W + "Caerleon_Roman_Fortress_and_Baths",
         "The Roman legionary fortress of Isca on the Usk, with its amphitheatre, baths and barracks still visible. Geoffrey of Monmouth, and Wace after him, made it the city where Arthur is crowned at Pentecost; the amphitheatre has long been called Arthur's Round Table. Tennyson lodged at the Hanbury Arms here while working on the Idylls",
         "乌斯克河畔的罗马军团要塞伊斯卡，圆形剧场、浴场和营房都还看得见。蒙茅斯的杰弗里和随后的瓦斯把它写成亚瑟在五旬节加冕的城市；那座圆形剧场长期被叫作亚瑟的圆桌。丁尼生写《国王叙事诗》时曾住在这里的汉伯里纹章旅店"),
    PROTO("slaughterbridge", "Slaughterbridge, on the River Camel", "卡默尔河畔 · 斯劳特桥", 50.638, -4.678, "Slaughterbridge (Wikipedia)", W + "Slaughterbridge",
          "Camlann, Arthur's last battle. Wace places it 'on the Camel, over against the entrance to Cornwall'; since Richard Carew (1602) the spot has been this bridge near Camelford, where a sixth-century inscribed stone on the riverbank is called King Arthur's Stone — it actually commemorates one Latinus, son of Macarus. No battle is proven here; the Arthurian Centre stands beside it",
          "卡姆兰，亚瑟的最后一战。瓦斯说它打在“卡默尔河上，正对康沃尔的入口”；自理查·卡鲁（1602 年）以来，这个地点就被定在卡默尔福德附近的这座桥，河岸上一块 6 世纪的刻字石被叫作亚瑟王石——其实纪念的是马卡鲁斯之子拉提努斯。这里并没有证据打过仗；旁边是亚瑟王中心"),
]

def FL(id, book_id, place, loc, loc_zh, en, hl_en, translation, checked, orig=None, hl_orig=()):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_orig: assert h in orig, (id, h)
    d = dict(id=id, book_id=book_id, place_ids=place if isinstance(place, list) else [place], location=loc, location_zh=loc_zh, text_en=en,
             highlight_en=hl_en, translation=translation or "original", status="draft", checked=checked + b5.D)
    if orig:
        d.update(text_orig=orig, highlight_orig=list(hl_orig))
    return d
def S(id, book_id, place, loc, loc_zh, en, zh, hl_en, hl_zh, src):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book_id, place_ids=[place], location=loc, location_zh=loc_zh, text_en=en, text_zh=zh,
                highlight_en=hl_en, highlight_zh=hl_zh, status="draft", fact_source=src)

PG = "Project Gutenberg #"
lines = [
    FL("mda-1", "le-morte-darthur", "tintagel-castle", "Book I, Chapter 2", "第一卷第 2 章",
       prose(1251, "When the duke had this warning", "the which had many issues and posterns out."), ["Tintagil"], None, PG + "1251"),
    FL("mda-2", "le-morte-darthur", "st-pauls", "Book I, Chapter 5", "第一卷第 5 章",
       prose(1251, "So in the greatest church of London", "rightwise king born of all England."), ["greatest church of London", "Paul's"], None, PG + "1251"),
    FL("mda-3", "le-morte-darthur", "winchester-great-hall", "Book II, Chapter 19", "第二卷第 19 章",
       prose(1251, "Also Merlin let make by his subtilty", "that is in English Winchester."), ["Camelot, that is in English Winchester"], None, PG + "1251"),
    FL("mda-4", "le-morte-darthur", "glastonbury-abbey", "Book XXI, Chapter 11", "第二十一卷第 11 章",
       prose(1252, "Then Sir Launcelot took his eight fellows", "Queen Guenever died but half an hour afore."), ["Glastonbury"], None, PG + "1252"),
    FL("id-1", "idylls-of-the-king", "tintagel-castle", "The Coming of Arthur", "《亚瑟的到来》",
       verse_lines(610, "Sir, for ye know that in King Uther's time", 18), ["Tintagil castle by the Cornish sea", "Tintagil"], None, PG + "610"),
    FL("id-2", "idylls-of-the-king", "dozmary-pool", "The Passing of Arthur", "《亚瑟的逝去》",
       verse_lines(610, "Then quickly rose Sir Bedivere, and ran,", 14), ["the mere"], None, PG + "610"),
    FL("id-3", "idylls-of-the-king", "cadbury-castle", "Gareth and Lynette", "《加雷斯与琳内特》",
       verse_lines(610, "He spake and laughed, then entered with his twain", 11), ["Camelot, a city of shadowy palaces"], None, PG + "610"),
    FL("gk-1", "sir-gawain-green-knight", "luds-church", "Fitt IV, stanzas 8–9 (lines 2168–2188)", "第四部分第 8—9 节（第 2168—2188 行）",
       prose(66084, "Then he drew in his horse and looked around", "he knew not what it might be.") + "\n" + prose(66084, "\"Ah,\" quoth Gawain, \"can this be the Green Chapel?", "say his mattins at midnight!"),
       ["Green Chapel", "an old cave or the crevice of a crag"], "Jessie L. Weston (1898)", PG + "14568 (Middle English, Richard Morris's edition for the Early English Text Society) and #66084 (Weston); editorial line numbers, sidenote marks and footnote marks removed from the Middle English, yogh restored",
       orig=me_lines(14568, "Þenne he houed, & wyth-hylde his hors", "dele his matynnes telle!"), hl_orig=["grene chapelle", "an olde caue"]),
    FL("wb-1", "roman-de-brut", "caerleon", "Arthur's crowning at Caerleon", "亚瑟在卡利恩加冕",
       prose(10472, "Arthur commanded all his lords on their allegiance", "the barns and granges were very rich."), ["Caerleon"], "Eugene Mason (1912)", PG + "10472 (Eugene Mason's translation, 1912)"),
    FL("wb-2", "roman-de-brut", "winchester-great-hall", "The Round Table", "圆桌",
       prose(10472, "Because of these noble lords about his hall", "none was alien at the breaking of Arthur's bread."), ["Round Table"], "Eugene Mason (1912)", PG + "10472 (Eugene Mason's translation, 1912)"),
    FL("wb-3", "roman-de-brut", ["slaughterbridge", "glastonbury-abbey"], "Arthur's last battle", "亚瑟的最后一战",
       prose(10472, "The battle was arrayed on the Camel", "he will return from whence he went and live again."), ["Camel", "Avalon"], "Eugene Mason (1912)", PG + "10472 (Eugene Mason's translation, 1912)"),
    S("ofk-s1", "once-and-future-king", "st-pauls", "Book I, The Sword in the Stone, final chapters", "第一部《石中剑》末尾几章",
      "Sir Ector takes the household to London for the tournament at which Kay is to be knighted. Kay leaves his sword at the inn; the Wart, sent back for it, finds the inn locked and instead pulls a sword from an anvil on a stone in a churchyard — Malory's 'greatest church of London, whether it were Paul's or not'. On the third pull it comes free, and the Wart is king.",
      "埃克托爵士带全家到伦敦参加比武大会，凯要在会上受封骑士。凯把剑忘在客栈，瓦特被打发回去取，客栈却锁着门，他就从教堂墓地里一块石头上的铁砧中拔出了一把剑——马洛礼写的是“伦敦最大的教堂，不知是不是圣保罗”。拔到第三下剑出来了，瓦特成了国王。",
      ["churchyard", "greatest church of London"], ["教堂墓地", "伦敦最大的教堂"], W + "The_Sword_in_the_Stone_(novel)"),
]

PHOTOS = json.load(open(f"{PW}/choice.json", encoding="utf-8"))
cands = json.load(open(f"{PW}/candidates.json")) if PHOTOS else {}
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
    append(f"{APP}/data/books.js", books, "11-09 亚瑟王传奇：马洛礼、丁尼生、《高文爵士与绿骑士》、瓦斯《布鲁特传奇》（英译），T. H. 怀特（有版权，只写场景说明）")
    append(f"{APP}/data/places.js", places, "11-09 亚瑟王传奇（坐标有出处）")
    append(f"{APP}/data/lines.js", lines, "11-09 亚瑟王传奇：古登堡原文逐字截取（草稿，待审核）")
    # Farringford: the Idylls were largely written there
    pp = f"{APP}/data/places.js"
    s = open(pp, encoding="utf-8").read()
    s2 = s.replace('id: "farringford"', 'id: "farringford"', 1)
    m = re.search(r'(\{ id: "farringford".*?book_ids: \[)([^\]]*)(\])', s2)
    assert m and "idylls-of-the-king" not in m.group(2)
    s2 = s2[:m.start(2)] + m.group(2) + ', "idylls-of-the-king"' + s2[m.end(2):]
    open(pp, "w", encoding="utf-8").write(s2)
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places if "photo" in p]
    if rows:
        cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
        open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    for l in lines:
        print(l["id"], "|", l["text_en"][:100].replace("\n", " / "))
        if l.get("text_orig"):
            print("   orig:", l["text_orig"][:100].replace("\n", " / "))
