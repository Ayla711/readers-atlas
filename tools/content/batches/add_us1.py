"""11-24: United States, a pack for a book from another country: Gloucester, Massachusetts, for J. Bernlef's Out of Mind
(Hersenschimmen, 1984; the book is in the Dutch data, added by tools/content/batches/add_nl3.py, which must run first).
Maarten and Vera Klein, Dutch emigrants, live in Gloucester, north of Boston. A scene note in our own words (in copyright).
Photos: tools/content/batches/add_photos_held_1124.py.

Usage: python3 -I tools/content/batches/add_us1.py <app_dir> tools/content/batches/coords/add_us1.json"""
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
b.init(APP, "", "us", DATE)
books = []
places = [
    b.ORIG("us-gloucester-ma", "Gloucester, Massachusetts", "格洛斯特（马萨诸塞州）", *C("us-gloucester-ma"),
           "Old fishing port on Cape Ann, north of Boston. In J. Bernlef's Out of Mind (Hersenschimmen, 1984), a classic of Dutch literature, it is where Maarten Klein, who came over from the Netherlands with his wife Vera in the 1950s, lives in retirement, and where, one snowy winter, he begins to lose his memory",
           "波士顿以北安妮角上的老渔港。在荷兰文学经典、J. 伯恩勒夫的《幻觉》（1984）里，20 世纪 50 年代和妻子薇拉一起从荷兰移民过来的马尔滕·克莱因退休后住在这里；一个下雪的冬天，他开始失去记忆"),
]
lines = [
    b.S("us-hs-1", "hersenschimmen", "us-gloucester-ma", "The novel as a whole", "全书",
        "Maarten Klein, seventy-one, and his wife Vera have lived for many years in Gloucester, north of Boston, with their dog Robert; they emigrated from the Netherlands in the 1950s. One winter, in the snow, Maarten begins to mix up the days, the past and the present. The novel is told from inside his head as his dementia deepens: he wanders off from home, Vera takes in a young woman, Phil Taylor, to keep an eye on him, and she tries to put his memory in order with the family photo album, in which Maarten no longer recognises himself. His life closes in a circle: at the end he is a child again.",
        "七十一岁的马尔滕·克莱因和妻子薇拉带着狗罗伯特，在波士顿以北的格洛斯特已经住了很多年；他们是 20 世纪 50 年代从荷兰移民来的。一个冬天，下着雪，马尔滕开始把日子、过去和现在搅在一起。小说从他的脑子里往外讲，看着他的失智一天天加深：他从家里走失；薇拉请了一个年轻姑娘菲尔·泰勒住进来照看他；她还想借家里的相册替他把记忆理顺，可马尔滕在照片上已经认不出自己。他的一生画成了一个圆：到最后，他又成了一个孩子。",
        ["Gloucester"], ["格洛斯特"],
        "https://dbnl.org/tekst/anbe001lexi01_01/lvlw00031.php; https://dbnl.org/tekst/_bzz001198901_01/_bzz001198901_01_0087.php; https://dbnl.org/tekst/_bzz001198901_01/_bzz001198901_01_0084.php; https://www.vpro.nl/boeken/artikelen/j-bernlef; https://maken.wikiwijs.nl/bestanden/672676/leesverslag%20havo%205%20hersenschimmen.docx"),
]
check(books, places, lines, ext={"hersenschimmen"})
if __name__ == "__main__":
    run(books, places, lines, "add_us1.py")
