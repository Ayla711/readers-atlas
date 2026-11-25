"""11-24: Russia, sixth pack: Petrozavodsk, for The Unknown Soldier (Väinö Linna, 1954; the book is in the Finnish data,
added by tools/content/batches/add_fi3.py, which must run first). The novel's main places (Petrozavodsk, the Svir, the
Karelian Isthmus) are in Russia today; under the rule for famous books it is hung at Petrozavodsk, which the Finns held as
Äänislinna in 1941–1944 and which is central to the novel's account of the 1941 advance (Kauhanen, "Äänislinna-noir").
A scene note in our own words (in copyright). Photos: tools/content/batches/add_photos_held_1124.py.

Usage: python3 -I tools/content/batches/add_ru6.py <app_dir> tools/content/batches/coords/add_ru6.json"""
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
b.init(APP, "", "ru", DATE)
books = []
places = [
    b.ORIG("ru-petrozavodsk", "Petrozavodsk (Äänislinna)", "彼得罗扎沃茨克", *C("ru-petrozavodsk"),
           "Capital of the Republic of Karelia, on Lake Onega. Finnish troops took the city in 1941, in the Continuation War, and held it until 1944 under the name Äänislinna. In Väinö Linna's The Unknown Soldier (1954), the most famous Finnish war novel, the city is central to the account of the 1941 advance into East Karelia",
           "卡累利阿共和国首府，在奥涅加湖畔。1941 年继续战争中芬兰军队攻占了这座城市，改名“Äänislinna”，一直占到 1944 年。在芬兰最著名的战争小说、韦伊诺·林纳的《无名战士》（1954）里，这座城市是 1941 年向东卡累利阿进攻那一部分的中心"),
]
lines = [
    b.S("ru-us-1", "unknown-soldier", "ru-petrozavodsk", "The advance of 1941", "1941 年的进攻",
        "A Finnish machine-gun company goes to war in the summer of 1941, at the start of the Continuation War: the laconic Karelian Rokka, the quiet officer Koskela, good-natured Hietanen, the shirker Rahikainen and the rest of a crew of ordinary men from all over Finland, who mock their officers, grumble, and fight. In the attack phase their road leads east across Karelia to Petrozavodsk, which the Finns rename Äänislinna; then come the long years of trench war and the retreat of 1944. Linna, who had served as a machine-gunner himself, showed the war from the ranks, with fear and rebellion as well as courage.",
        "1941 年夏天，继续战争开始，一个芬兰机枪连开赴前线：寡言的卡累利阿人罗卡、沉静的军官科斯凯拉、好脾气的希耶塔宁、偷懒耍滑的拉希凯宁，还有一群来自芬兰各地的普通人——他们挖苦军官、发牢骚，也打仗。进攻阶段，他们一路向东穿过卡累利阿，打到彼得罗扎沃茨克，芬兰人把它改名“Äänislinna”；接下来是漫长的堑壕战和 1944 年的撤退。林纳自己当过机枪手，他从士兵的角度写这场战争，写他们的恐惧和反抗，也写勇气。",
        ["Petrozavodsk", "Äänislinna"], ["彼得罗扎沃茨克", "Äänislinna"],
        "https://www.utupub.fi/handle/11111/41788 (Riku Kauhanen, Äänislinna-noir – Miehitetty Petroskoi suomalaisessa kirjallisuudessa); https://caponeu.ffzg.unizg.hr/cdp/novels/tuntematon-sotilas; https://en.wikipedia.org/wiki/The_Unknown_Soldier_(novel)"),
]
check(books, places, lines, ext={"unknown-soldier"})
if __name__ == "__main__":
    run(books, places, lines, "add_ru6.py")
