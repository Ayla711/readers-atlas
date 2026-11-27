"""11-27: the Vatican, the book the user chose (tools/selection/va.md): by selection rule v2 no book qualifies, and the
user took Irving Stone's The Agony and the Ecstasy (1961), the biographical novel of Michelangelo, as an exception. The
Vatican opens with this batch. Place, with the reason:
- the Sistine Chapel: in Book Seven, "The Pope", Michelangelo is set by Julius II to paint its ceiling (1508-12), and in
  Book Ten, "Love", he paints The Last Judgment on its altar wall. In copyright: a scene note.
Sources: https://en.wikipedia.org/wiki/The_Agony_and_the_Ecstasy_(novel); https://en.wikipedia.org/wiki/Sistine_Chapel;
https://en.wikipedia.org/wiki/Sistine_Chapel_ceiling
The map of the Vatican (data/va/geo.js) is the whole state as one region, from geoBoundaries VAT ADM0 (public domain;
tools/eu-revision/va_geo_build.py).
Photos: tools/content/batches/add_photos_luva_1127.py.
Usage: python3 -I tools/content/batches/add_va1.py <app_dir> tools/content/batches/coords/add_va1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "va", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="agony-and-the-ecstasy", title="The Agony and the Ecstasy", title_zh="痛苦与狂喜", title_orig="The Agony and the Ecstasy",
         author="Irving Stone", author_zh="欧文·斯通", year="1961", orig_lang="en", public_domain=False, source_url=None,
         author_orig="Irving Stone", aliases=["Michelangelo", "Michelangelo Buonarroti", "Julius II"]),
]

places = [
    b.ORIG("va-sistine-chapel", "Sistine Chapel", "西斯廷礼拜堂", *C("va-sistine-chapel"),
        "The great chapel of the Apostolic Palace, built for Pope Sixtus IV between 1473 and 1481, where the conclave meets to elect a new pope. Its walls were painted by Botticelli, Ghirlandaio, Perugino and others; Michelangelo painted the ceiling in fresco for Julius II between 1508 and 1512, with nine scenes from Genesis at its centre, The Creation of Adam among them, and came back years later to paint The Last Judgment on the wall behind the altar",
        "使徒宫里的大礼拜堂，1473 至 1481 年为教皇西斯笃四世而建，选举新教皇的秘密会议就在这里举行。墙上的壁画出自波提切利、吉兰达约、佩鲁吉诺等人之手；1508 至 1512 年，米开朗基罗为尤利乌斯二世画了穹顶湿壁画，正中是九幅《创世记》场景，《创造亚当》就在其中；多年后他又回来，在祭坛后的墙上画了《最后的审判》"),
]

lines = [
    b.S("va-agony-1", "agony-and-the-ecstasy", "va-sistine-chapel", "Book Seven, \"The Pope\"; Book Ten, \"Love\"", "第七部《教皇》、第十部《爱》",
        "Stone's biographical novel follows Michelangelo in eleven books, from Ghirlandaio's studio to his death; Stone lived in Italy for years, worked in marble quarries and apprenticed himself to a marble sculptor, and drew above all on Michelangelo's 495 letters. In Book Seven, \"The Pope\", Michelangelo resists the summons of Julius II for as long as he can, and the two hot tempers clash; the tomb he is to carve for the pope is put off again and again, and he is set instead to paint the ceiling of the Sistine Chapel. In Book Ten, \"Love\", he paints The Last Judgment in the same chapel, first for Clement VII and then for Paul III, and in the last book, \"The Dome\", he becomes architect of St Peter's. Part of the novel became the 1965 film, with Charlton Heston as Michelangelo and Rex Harrison as Julius II.",
        "斯通的这部传记小说分十一部，从吉兰达约的画坊一直写到米开朗基罗去世；斯通在意大利住了多年，到大理石采石场干过活，还拜一位大理石雕刻师当学徒，主要依据是米开朗基罗的 495 封书信。第七部《教皇》里，米开朗基罗尽可能拖延尤利乌斯二世的召唤，两个火爆脾气针锋相对；原定为教皇雕的陵墓一拖再拖，他反被派去画西斯廷礼拜堂的穹顶。第十部《爱》里，他在同一座礼拜堂里画《最后的审判》，先为克雷芒七世，后为保罗三世；最后一部《穹顶》里，他成了圣彼得大教堂的建筑师。小说的一部分在 1965 年拍成电影，查尔顿·赫斯顿演米开朗基罗，雷克斯·哈里森演尤利乌斯二世。",
        ["Sistine Chapel"], ["西斯廷礼拜堂"],
        "https://en.wikipedia.org/wiki/The_Agony_and_the_Ecstasy_(novel); https://en.wikipedia.org/wiki/Sistine_Chapel_ceiling"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO)

HEAD = "// Vatican City, hand-written content (tools/content/batches/add_va1.py, 2026-11-27).\n"
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
