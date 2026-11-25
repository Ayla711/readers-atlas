"""11-24: Turkey, third pack: the two famous books held back as "place to be checked", hung on the nearest real place under
the rule for famous books (honest notes):
- The Disconnected (Tutunamayanlar, Oğuz Atay, 1972; in copyright, a scene note): Turgut Özben goes to Ankara to find
  Selim Işık's friends Süleyman Kargı and Metin. Place: Ankara.
- Aşk-ı Memnu (Halit Ziya Uşaklıgil, 1900; public domain): the novel opens as Firdevs Hanım and her daughters row home from
  an outing at Kalender, on the Bosphorus (the edition's own footnote: "İstanbul Boğaziçi'nde bir semt"). Kalender, the cove
  between Yeniköy and Tarabya, has no coordinates in any Wikipedia; the pin is at Yeniköy, which the chapter also names.
  A quotation from Turkish Wikisource, Aşk-ı Memnu/Bölüm 1 (the opening sentence; the footnote mark is left out).
  Sources for Kalender: https://archnet.org/sites/20749; https://turkeyfromtheinside.com/?p=3880;
  https://en.wikipedia.org/wiki/Tarabya (Kalender among its neighbourhoods).
Photos: tools/content/batches/add_photos_held_1124.py.

Usage: python3 -I tools/content/batches/add_tr3.py <app_dir> tools/content/batches/coords/add_tr3.json <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP = sys.argv[1]
CO = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 and sys.argv[2].endswith(".json") else {}
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines, ext=(), elsewhere=()):
    """ext: books already in the app (another country's books.js) that get a line here;
    elsewhere: books added here whose line goes into another country's data (another batch script)"""
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    new = {x["id"] for x in books}
    assert not new & allb, new & allb
    assert set(ext) <= allb, set(ext) - allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    bk = new | set(ext)
    for l in lines:
        assert l["book_id"] in bk and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} | set(elsewhere) == bk
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
def run(books, places, lines, script):
    M = f"11-24: famous books hung on their nearest real place (tools/content/batches/{script})"
    for name, xs in (("books.js", books), ("places.js", places), ("lines.js", lines)):
        if xs: b.append(b.data(name), xs, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
import wikisource as ws
WSR = sys.argv[3]
WS = "https://tr.wikisource.org/wiki/"
def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh):
    assert "[" not in orig and "\xa0" not in orig and "\n" not in orig, id
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls: assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_orig=orig, highlight_orig=hl_orig,
                text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own", status="draft",
                checked=f"Turkish Wikisource, {title}, {DATE}")
b.init(APP, "", "tr", DATE)
T_AM = "Aşk-ı Memnu/Bölüm 1"
AM = ws.cut(os.path.join(WSR, "tr"), T_AM, "Maun sandalla", "fark etmemiş göründüler.")
books = [
    BK("tutunamayanlar", "The Disconnected", "不合群的人", "Tutunamayanlar", "Oğuz Atay", "奥乌兹·阿塔伊", "Oğuz Atay", "1972", "tr",
       ["Tutunamayanlar", "Selim Işık", "Turgut Özben", "Süleyman Kargı", "Olric"]),
    BK("ask-i-memnu", "Forbidden Love", "禁忌之恋", "Aşk-ı Memnu", "Halit Ziya Uşaklıgil", "哈立德·齐亚·乌沙克勒吉尔",
       "Halit Ziya Uşaklıgil", "1900", "tr", ["Aşk-ı Memnu", "Ask-i Memnu", "Bihter", "Adnan Bey", "Firdevs Hanım", "Behlül", "Nihal"],
       pd=True, src=WS + "A%C5%9Fk-%C4%B1_Memnu"),
]
places = [
    b.ORIG("tr-ankara", "Ankara", "安卡拉", *C("tr-ankara"),
           "Capital of Turkey. In Oğuz Atay's The Disconnected (Tutunamayanlar, 1972), the engineer Turgut Özben comes to Ankara after his friend Selim Işık's suicide, to find Selim's friends Süleyman Kargı and Metin and learn from them who Selim was",
           "土耳其首都。奥乌兹·阿塔伊的《不合群的人》（1972）里，工程师图尔古特·厄兹本在朋友塞利姆·厄申自杀后来到安卡拉，找塞利姆的朋友苏莱曼·卡尔格和梅廷，想从他们那里弄明白塞利姆是个什么样的人"),
    b.ORIG("tr-yenikoy", "Kalender and Yeniköy, Bosphorus", "卡伦德尔与耶尼柯伊，博斯普鲁斯海峡", *C("tr-yenikoy"),
           "Yeniköy is an old village on the European shore of the Bosphorus; just north of it, towards Tarabya, lies the small cove of Kalender, once a pleasure ground with an Ottoman pavilion. Halit Ziya Uşaklıgil's Aşk-ı Memnu (1900) opens as Firdevs Hanım and her daughters row home from an outing at Kalender, and Adnan Bey's mahogany boat skims past them. Kalender has no coordinates of its own in any Wikipedia, so the pin is at Yeniköy, which the first chapter also names",
           "耶尼柯伊是博斯普鲁斯海峡欧洲岸的一个老村子；它北边、往塔拉布亚方向，有个叫卡伦德尔的小海湾，从前是游乐的地方，还有一座奥斯曼时代的亭阁。哈立德·齐亚·乌沙克勒吉尔的《禁忌之恋》（1900）开篇，菲尔黛芙丝夫人带着女儿们从卡伦德尔游玩后划船回家，阿德南先生的桃花心木小艇从她们身边擦过。卡伦德尔在各语种维基百科里都没有坐标，所以图钉标在第一章里同样点了名的耶尼柯伊"),
]
lines = [
    b.S("tr-tu-1", "tutunamayanlar", "tr-ankara", "The search for Selim", "寻找塞利姆",
        "Turgut Özben, a young engineer with a comfortable middle-class life in Istanbul, learns from the newspapers that his friend Selim Işık has shot himself. Feeling he has neglected him, he sets out to find out why. In Ankara, Selim's friend Süleyman Kargı gives him a long poem Selim wrote about himself and a pile of his papers, and Metin, another friend, tells him what he remembers; later Turgut meets Günseli, with whom Selim had had a relationship. The better Turgut comes to understand Selim, the less he can bear his own orderly life; in the end he leaves everything behind and disappears, jumping from train to train.",
        "图尔古特·厄兹本是个年轻工程师，在伊斯坦布尔过着舒适的小资生活。他从报纸上得知，朋友塞利姆·厄申开枪打死了自己。他觉得自己冷落了这个朋友，决心弄明白他为什么这样做。在安卡拉，塞利姆的朋友苏莱曼·卡尔格交给他一首塞利姆写自己的长诗和一大堆文稿，另一个朋友梅廷讲了他记得的事；后来图尔古特又见到了和塞利姆有过一段感情的京塞莉。他越懂塞利姆，就越受不了自己那循规蹈矩的生活；最后他抛下一切，消失了，从一列火车跳上另一列火车。",
        ["Ankara"], ["安卡拉"],
        "https://dergipark.org.tr/en/download/article-file/374716; https://www.turkedebiyati.org/?p=18980; https://www.themodernnovel.org/asia/other-asia/turkey/oguz-atay%20/the-disconnected/"),
    Q("tr-am-1", "ask-i-memnu", "tr-yenikoy", "Chapter 1, the opening: rowing home from Kalender", "第一章开头：从卡伦德尔划船回来", T_AM,
      AM, ["Kalender"],
      "They had grown so used to these encounters with the mahogany boat, which were almost like collisions, that today, coming back from Kalender, they seemed not to notice it once again skimming past them so close that it all but struck them.",
      ["Kalender"],
      "她们对那条桃花心木小艇这种近乎相撞的相遇早已习以为常，所以今天从卡伦德尔回来时，它又一次差点撞上似的贴着她们擦身而过，她们看上去也像没有察觉。",
      ["卡伦德尔"]),
]
check(books, places, lines)
if __name__ == "__main__":
    run(books, places, lines, "add_tr3.py")
