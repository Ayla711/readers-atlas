"""11-24: Denmark, third pack: Winter's Tales (Karen Blixen, 1942), the last book that selection rule v2 adds for Denmark.
In copyright: a scene note in our own words. The manor of its best-known tale, "Sorrow-Acre", is unnamed and the folk
tale behind it has not been traced to a place, so by the rule for famous books (hang them on the nearest real place) the
book is hung at Rungstedlund, where Blixen was born, and lived, and where she lived when she wrote the collection during the German occupation; the
place is already in the app (pilgrimage, with Out of Africa) and gets the book in its book_ids. No new place, no new photo.

Usage: python3 -I tools/content/batches/add_dk3.py <app_dir>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], (json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else {})
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines, old_places=()):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    have = ids_in(b.data("places.js"))
    assert not {p["id"] for p in places} & have and {p["id"] for p in places} == set(CO)
    assert set(old_places) <= have, set(old_places) - have
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    pl = {p["id"] for p in places} | set(old_places)
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in pl, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == pl
b.init(APP, "", "dk", DATE)
books = [
    BK("winters-tales", "Winter's Tales", "冬天的故事", "Winter's Tales", "Karen Blixen", "凯伦·布里克森", "Karen Blixen", "1942", "en",
       ["Vinter-Eventyr", "Vintereventyr", "Sorrow-Acre", "Sorg-Agre", "Isak Dinesen", "Anne-Marie"]),
]
places = []
lines = [
    b.S("dk-wt-1", "winters-tales", "dk-rungstedlund", "“Sorrow-Acre”", "《悲伤田》",
        "Written during the German occupation, while Blixen lived at Rungstedlund, and smuggled out of Denmark through Sweden, the eleven tales draw their themes and places from Blixen's Danish childhood. The best known, “Sorrow-Acre”, is set on a manor in late eighteenth-century Denmark, on the first day of the harvest. A barn has burned, and Goske Piil, a widow's son, is accused. His mother Anne-Marie protests his innocence, and the old lord promises to set him free if she mows a whole field of rye by herself. She does it, and dies. The peasants named the field Sorrow-Acre.",
        "这部集子写于德国占领期间，那时布里克森住在伦斯泰德隆德；书稿经瑞典偷偷带出丹麦；十一篇故事的题材和地方，都来自她在丹麦的童年。最有名的一篇《悲伤田》发生在十八世纪末丹麦的一座庄园里，正值收获的头一天。一座谷仓被烧了，寡妇的儿子戈斯克·皮尔被指为纵火者。他的母亲安妮-玛丽坚称儿子无辜，老领主便许诺：只要她一个人割完一整块黑麦田，就放了她儿子。她割完了，随即死去。农民们从此把那块地叫作“悲伤田”。",
        ["Rungstedlund"], ["伦斯泰德隆德"],
        "https://www.penguin.co.uk/books/57324/winters-tales-by-dinesen-isak/9780141185880; https://www.newworldencyclopedia.org/entry/Karen_Blixen; https://ebsco.com/research-starters/history/isak-dinesen; https://www.ebsco.com/research-starters/literature-and-writing/sorrow-acre-isak-dinesen; https://www.encyclopedia.com/education/news-wires-white-papers-and-books/sorrow-acre; https://encyclopedia.com/arts/encyclopedias-almanacs-transcripts-and-maps/sorrow-acre-sorg-agre-isak-dinesen-1940; https://www.kb.dk/en/inspiration/karen-blixen-behind-scenes"),
]
check(books, places, lines, old_places=["dk-rungstedlund"])
def add_book_to_place(pid, book_id):
    p = b.data("places.js"); s = open(p, encoding="utf-8").read()
    m = re.search(r'(\{ id: "' + re.escape(pid) + r'".*?book_ids: \[)([^\]]*)(\])', s)
    assert m and f'"{book_id}"' not in m.group(2), pid
    s = s[:m.end(2)] + f', "{book_id}"' + s[m.end(2):]
    open(p + ".new", "w", encoding="utf-8").write(s); os.replace(p + ".new", p)
if __name__ == "__main__":
    M = "11-24: third pack, books added under selection rule v2 (tools/content/batches/add_dk3.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("lines.js"), lines, M)
    add_book_to_place("dk-rungstedlund", "winters-tales")
    print(len(books), "books,", len(lines), "lines; dk-rungstedlund gets winters-tales")
