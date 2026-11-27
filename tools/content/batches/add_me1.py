"""11-27: Montenegro, the one book the user chose (11-27): by the rule no book qualifies (no national list; the curriculum and
the prizes never meet on one book), so, as for Albania, the user takes the recognised national classic as an exception:
Njegoš's The Mountain Wreath (1847). Montenegro opens with this batch.
- Mount Lovćen, Njegoš's Mausoleum on Jezerski vrh: the play opens with the chieftains' assembly on Lovćen on the eve of
  Trinity Day, and Njegoš lies on the mountain. Quotation from Serbian Wikisource (the text of the 1847 Vienna edition,
  in Cyrillic), our own translation.
The map of Montenegro (data/me/geo.js) is geoBoundaries MNE ADM1 (OpenStreetMap via Wambacher, 2017, ODbL 1.0): 23
municipalities with their ISO codes; Tuzi (2018) and Zeta (2022) are still within Podgorica. Natural Earth's 21 units are
coarse on the coast (Kotor town falls in Cetinje municipality, Tivat in the sea). tools/eu-revision/me_geo_build.py.
Usage: python3 -I tools/content/batches/add_me1.py <app_dir> tools/content/batches/coords/add_me1.json <wikisource_cache_dir>
(cache/me holds sr.wikisource "Горски вијенац", fetched with tools/content/wikisource.py)"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-27"
b.init(APP, "", "me", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def Q(id, book, place, loc, loc_zh, source, orig, hl_orig, en, hl_en, zh, hl_zh):
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "[" not in orig and "\xa0" not in orig and "  " not in orig, (id, "page mark or odd space")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"{source}, {DATE}")

books = [dict(id="gorski-vijenac", title="The Mountain Wreath", title_zh="山地花环", title_orig="Горски вијенац (Gorski vijenac)",
              author="Petar II Petrović-Njegoš", author_zh="彼得二世·彼得罗维奇-涅古什", year="1847", orig_lang="sh", public_domain=True,
              source_url="https://sr.wikisource.org/wiki/Горски_вијенац",
              aliases=["Gorski vijenac", "Горски вијенац", "Njegoš", "Његош", "Vladika Danilo", "The Mountain Garland"])]

places = [b.PIL("me-lovcen", "Mount Lovćen and Njegoš's Mausoleum (Jezerski vrh)", "洛夫琴山 · 涅古什陵墓（耶泽尔斯基峰）", *C("me-lovcen"),
    "Njegoš, prince-bishop of Montenegro and its greatest poet, built a chapel on Lovćen in 1845, meaning to be buried there; he was laid in it in 1855. The chapel, damaged in both world wars, was pulled down in 1974 and replaced by a mausoleum to the design of the sculptor Ivan Meštrović, on Jezerski vrh, Lovćen's second peak (1,657 m), in the national park, 21 km by road from Cetinje; the last stretch is a stairway of 461 steps through a tunnel. The Mountain Wreath opens with the chieftains' assembly on Lovćen on the eve of Trinity Day",
    "黑山的亲王兼主教、也是它最伟大的诗人涅古什，1845 年在洛夫琴山上修了一座小教堂，打算死后葬在那里；1855 年他被安葬其中。小教堂在两次世界大战中受损，1974 年被拆除，原址建起雕塑家伊万·梅什特罗维奇设计的陵墓，在洛夫琴山的第二高峰耶泽尔斯基峰（海拔 1657 米），属洛夫琴国家公园，从采蒂涅沿公路 21 公里；最后一段是穿过隧道的 461 级台阶。《山地花环》开场就是圣三一节前夕首领们在洛夫琴山上的集会",
    ["gorski-vijenac"])]

lines = [Q("me-gv-1", "gorski-vijenac", "me-lovcen", "The assembly on Lovćen on the eve of Trinity Day; Serdar Radonja",
           "圣三一节前夕洛夫琴山上的集会；拉多尼亚统领", "Serbian Wikisource, Горски вијенац",
           ws.block(WSR, "Горски вијенац", "Присука сам", "страшнијех громовах;"), ["Ловћен"],
           "I am past fifty years of age;\nI have always spent my summers on Lovćen,\nclimbing up to this summit:\na hundred times I have watched the clouds\ncome in heaps up from the sea\nand cover all this mountain,\nthen push off this way and that\nwith lightning and with a great roar\nand with the crash of fearful thunder;", ["Lovćen"],
           "我已年过五十，\n夏天总在洛夫琴山上度过，\n登上这座山巅：\n上百次我看见云朵\n从海上成堆涌来，\n盖满这整座山，\n又向这边那边推去，\n带着闪电、带着巨大的轰鸣，\n带着可怕的雷声；", ["洛夫琴"])]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO)

HEAD = "// Montenegro, hand-written content (tools/content/batches/add_me1.py, 2026-11-27).\n"
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
