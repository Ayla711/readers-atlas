"""11-24: Netherlands, third pack: the book Out of Mind (Hersenschimmen, J. Bernlef, 1984), held back as "place to be checked".
The novel is set in Gloucester, Massachusetts; its place and scene note are in the US data, added by
tools/content/batches/add_us1.py, which must run after this script.

Usage: python3 -I tools/content/batches/add_nl3.py <app_dir>"""
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
b.init(APP, "", "nl", DATE)
books = [
    BK("hersenschimmen", "Out of Mind", "幻觉", "Hersenschimmen", "J. Bernlef", "J. 伯恩勒夫", "J. Bernlef", "1984", "nl",
       ["Hersenschimmen", "Maarten Klein", "Vera Klein", "Bernlef"]),
]
places, lines = [], []
check(books, places, lines, elsewhere={"hersenschimmen"})
if __name__ == "__main__":
    run(books, places, lines, "add_nl3.py")
