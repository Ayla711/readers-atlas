"""11-27: Cyprus, the books the user chose (tools/selection/cy.md): Kyriakos Charalambides's Famagusta Regina (1982), the
one Cypriot book that qualifies by rule v2 (a lyceum set book, one of four, and the Cyprus State Prize for Poetry);
Othello, already in the app (data/it), which qualifies and gets a place in Cyprus; and, as an exception the user chose,
Elif Shafak's The Island of Missing Trees (2021). Ovid's Metamorphoses and Uris's Exodus qualify too; the user left them
out. Cyprus opens with this batch. Places, with the reason for each:
- Famagusta for Famagusta Regina: the book of the poet's lost home town. In copyright: a scene note.
- Othello Castle, Famagusta, for Othello: Acts 2-5 are set in a Cyprus seaport that the play does not name; Othello goes
  "to the Castle" and sends for the ship's master "to the Cittadell". The Famagusta citadel takes its modern name from the
  play (honest note). Quotation from the First Folio (1623) as transcribed on English Wikisource (Project Gutenberg, the
  source of the Venice line, was down for maintenance on 11-27).
  Sources for the castle: https://en.wikipedia.org/wiki/Othello_Castle; https://www.britannica.com/topic/Othellos-Tower;
  https://www.travelweek.ca/?p=19461; https://atlasobscura.com/articles/the-real-life-tragedy-behind-othello-s-tower
- Nicosia for The Island of Missing Trees: Kostas and Defne meet at the Happy Fig, an invented tavern in the city; the
  novel's London half is not on the map. In copyright: a scene note.
The north of the island, Famagusta included, has been under the Turkish Cypriot administration since 1974; the notes say so
plainly. The map of Cyprus (data/cy/geo.js) is the 6 districts of ISO 3166-2:CY over the whole island (user, 11-27), from
geoBoundaries CYP ADM1 (OpenStreetMap via Wambacher, ODbL 1.0; tools/eu-revision/cy_geo_build.py).
Photos: tools/content/batches/add_photos_cy_1127.py.
Usage: python3 -I tools/content/batches/add_cy1.py <app_dir> tools/content/batches/coords/add_cy1.json <wikisource_cache_dir>
(cache/cy holds the English Wikisource page "Shakespeare - First Folio facsimile (1910)/The Tragedie of Othello, the Moore
of Venice/Act 2 Scene 1", fetched with tools/content/wikisource.py)"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-27"
b.init(APP, "", "cy", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="ammochostos-vasilevousa", title="Famagusta Regina (Ammochostos Vasilevousa)", title_zh="女王法马古斯塔",
         title_orig="Αμμόχωστος Βασιλεύουσα", author="Kyriakos Charalambides", author_zh="基里亚科斯·哈拉兰比季斯", year="1982",
         orig_lang="el", public_domain=False, source_url=None, author_orig="Κυριάκος Χαραλαμπίδης",
         aliases=["Αμμόχωστος Βασιλεύουσα", "Ammochostos Vasilevousa", "Famagusta Regina", "Άρδανα"]),
    dict(id="island-of-missing-trees", title="The Island of Missing Trees", title_zh="失落之树岛", title_orig="The Island of Missing Trees",
         author="Elif Shafak", author_zh="艾丽芙·沙法克", year="2021", orig_lang="en", public_domain=False, source_url=None,
         author_orig="Elif Shafak", aliases=["The Happy Fig", "Kostas", "Defne", "Ada Kazantzakis", "Ficus carica"]),
]

places = [
    b.ORIG("cy-famagusta", "Famagusta (Ammochostos / Gazimağusa)", "法马古斯塔", *C("cy-famagusta"),
        "Port town on the east coast of Cyprus, its old town inside the Venetian walls, for centuries the island's chief harbour. Kyriakos Charalambides, born at Achna in 1940, grew up here. Since 1974 Famagusta has been in the north of the island, under the Turkish Cypriot administration, and its Greek Cypriot people became refugees. Famagusta Regina (1982) is his book of the town",
        "塞浦路斯东海岸的港口城市，老城在威尼斯人修的城墙里，几百年来是全岛的主要港口。基里亚科斯·哈拉兰比季斯 1940 年生在阿赫纳，在这里长大。1974 年起，法马古斯塔在岛的北部，归土族塞人当局管辖，城里的希族居民成了难民。《女王法马古斯塔》（1982）是他写这座城的诗集"),
    b.ORIG("cy-othello-castle", "Othello Castle (Othello's Tower), Famagusta", "法马古斯塔 · 奥赛罗城堡（奥赛罗塔）", *C("cy-othello-castle"),
        "The citadel at the harbour of Famagusta's walled town, built by the Lusignan kings in the 14th century and made an artillery fort by the Venetians. From Act 2 on, Othello is set in a seaport in Cyprus that the play does not name; Othello goes up \"to the Castle\" and the ship's master is to be brought \"to the Cittadell\". Famagusta was then the island's chief port, and the citadel takes its modern name from the play. It stands in the north, under the Turkish Cypriot administration, and reopened in 2015 after a restoration under a UNDP programme, with Greek and Turkish Cypriot politicians at the opening",
        "法马古斯塔城墙老城港口边的要塞，14 世纪由吕西尼昂王朝建造，威尼斯人把它改成炮台。《奥赛罗》从第二幕起移到塞浦路斯的一个港口，剧中没有点名；奥赛罗说“到城堡去”，又让人把船长“带到要塞来”。法马古斯塔当时是全岛最大的港口，这座要塞的今名就来自这部戏。它在岛的北部，归土族塞人当局管辖，2015 年在联合国开发计划署的项目下修复后重新开放，希族和土族两边的政界人物都到场"),
    b.ORIG("cy-nicosia", "Nicosia (Lefkosia / Lefkoşa)", "尼科西亚", *C("cy-nicosia"),
        "The capital of Cyprus, its old town ringed by Venetian walls and cut in two since 1974 by the Green Line, the UN buffer zone between the Greek Cypriot south and the Turkish Cypriot north. In The Island of Missing Trees the two lovers meet in a tavern in the city in 1974; the tavern, the Happy Fig, is invented",
        "塞浦路斯首都，老城有威尼斯城墙环绕，1974 年起被“绿线”一分为二——那是希族南部和土族北部之间的联合国缓冲区。《失落之树岛》里，一对恋人 1974 年在城里的一家小酒馆相会；那家“快乐无花果”酒馆是虚构的"),
]

OTH_T = "Shakespeare - First Folio facsimile (1910)/The Tragedie of Othello, the Moore of Venice/Act 2 Scene 1"
OTH = ws.block(WSR, OTH_T, "Come: let vs to the Castle.", "Do's challenge much respect.")
OTH_ZH = ("来，我们到城堡去。\n朋友们，好消息：仗打完了，\n土耳其人都淹死了。\n我在这岛上的老相识们可好？\n"
          "（亲爱的）你在塞浦路斯会很受欢迎，\n我在他们中间得到过深厚的情谊。啊，我的心肝，\n我说话颠三倒四，我太沉醉\n"
          "在自己的快乐里了。好伊阿古，请你\n到海湾去，把我的箱子卸下船；\n把船长带到要塞来，\n他是个好人，他的才干\n值得大家敬重。")
lines = [
    b.S("cy-amm-1", "ammochostos-vasilevousa", "cy-famagusta", "The collection as a whole", "整部诗集",
        "Written in the years after 1974 and published in 1982, the collection is the poet's book of Famagusta, the town he grew up in and could no longer reach. In the first poems he gives the town a face and a voice, charges its people with their share of the blame for what happened, then turns to the town itself and lists its own; other poems go out to the villages around it, such as Ardana. Charalambides called it the geography of the lost homeland, as his next book, Tholos (1989), would be its human side, the missing. It won the Cyprus State Prize for Poetry, and one critic called it the most accomplished Greek book of 1982. Famagusta is the town of the title.",
        "这部诗集写于 1974 年之后，1982 年出版，是诗人写法马古斯塔的书——他长大的城，如今再也回不去。开头几首诗里，他给这座城一张脸、一副嗓子，先数落城里的人对那场灾难应负的责任，再转身面对这座城，一条条数它自己的过失；另一些诗走到城周围的村子，比如阿尔达纳。哈拉兰比季斯说，这本书写的是失去的家乡的地理，下一本《穹顶》（1989）写的是它的人，那些失踪者。诗集获塞浦路斯国家诗歌奖，有评论家称它是 1982 年最完美的希腊语书。书名里的城就是法马古斯塔。",
        ["Famagusta"], ["法马古斯塔"],
        "https://el.wikipedia.org/wiki/Κυριάκος_Χαραλαμπίδης; http://ikee.lib.auth.gr/record/306490/files/GRI-2019-25227.pdf; http://www.elliniki-gnomi.eu/sta-ichni-enos-dramatos/; https://cultural-association.org/βραβείο-λογοτέχνη-για-το-σύνολο-του-έρ/; https://users.sch.gr/ipap/Ellinikos_Politismos/logotexnia/Biografies/charalampidis.htm; https://syntyxanoume.blogspot.com/2012/04/blog-post_24.html"),
    dict(id="cy-oth-1", book_id="othello", place_ids=["cy-othello-castle"], location="Act 2, Scene 1 (First Folio, 1623)", location_zh="第二幕第一场（1623 年第一对开本）",
         text_en=OTH, highlight_en=["Castle", "Cyprus", "Cittadell"], text_zh=OTH_ZH, highlight_zh=["城堡", "塞浦路斯", "要塞"],
         translation="original", status="draft", checked=f"English Wikisource, {OTH_T}, {DATE}"),
    b.S("cy-imt-1", "island-of-missing-trees", "cy-nicosia", "The novel as a whole", "全书",
        "In 1974 Kostas, a Greek Cypriot, and Defne, a Turkish Cypriot, both eighteen, can meet only in secret, at the Happy Fig, a tavern in Nicosia kept by Yiorgos and Yusuf, a Greek Cypriot and a Turkish Cypriot, with a fig tree growing up through a hole in the roof. The fig tree is one of the narrators. Decades later in north London, Kostas buries a fig tree grown from a cutting of it to save it from a winter storm, while his sixteen-year-old daughter Ada, who has never seen the island, tries to learn what her parents went through in the war and the division. Nicosia is the divided city where they met.",
        "1974 年，希族塞人科斯塔斯和土族塞人德芙内都是十八岁，只能偷偷在“快乐无花果”相会——那是尼科西亚城里一家小酒馆，由希族塞人约尔戈斯和土族塞人优素福经营，一棵无花果树从屋顶的洞里长出去。这棵无花果树也是讲故事的人之一。几十年后在伦敦北部，科斯塔斯把一棵用那棵树的插枝种大的无花果树埋进土里，好让它躲过冬天的风暴；他十六岁的女儿艾达从没去过那座岛，想弄明白父母在战争和分裂中经历了什么。尼科西亚就是他们相遇的那座被分开的城。",
        ["Nicosia"], ["尼科西亚"],
        "https://en.wikipedia.org/wiki/The_Island_of_Missing_Trees; https://libraries.dlrcoco.ie/staff-picks/island-missing-trees; https://www.penguin.co.uk/books/316722/the-island-of-missing-trees/9780241434994; https://www.tripfiction.com/review/lead-review-5488/"),
]
for h in ["Castle", "Cyprus", "Cittadell"]:
    assert h in OTH
for h in ["城堡", "塞浦路斯", "要塞"]:
    assert h in OTH_ZH

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
assert not {x["id"] for x in books} & all_books and "othello" in ids_in(os.path.join(APP, "data", "it", "books.js"))
assert {p["id"] for p in places} == set(CO)

HEAD = "// Cyprus, hand-written content (tools/content/batches/add_cy1.py, 2026-11-27).\n"
def write(name, key, entries, extra=""):
    os.makedirs(os.path.dirname(b.data(name)), exist_ok=True)
    with open(b.data(name), "w", encoding="utf-8") as fh:
        fh.write(HEAD + extra + "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA." + key + " = [\n"
                 + ",\n".join("  " + b.obj(e) for e in entries) + "\n];\n")
if __name__ == "__main__":
    for f in ("books.js", "places.js", "lines.js"):
        assert not os.path.exists(b.data(f)), ("already there", f)
    write("books.js", "books", books)
    write("places.js", "places", places, "// Each place's admin-1 region is worked out from its coordinates by app.js.\n")
    write("lines.js", "lines", lines)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
