"""11-24: Algeria, second pack: the books that selection rule v2 adds (tools/selection/dz.md), as far as they have a real place.
Memory in the Flesh (Mosteghanemi, 1993) and The Sheltering Sky (Bowles, 1949) are in copyright: scene notes.
The Sheltering Sky hangs at Oran, already in the app for The Plague: the novel opens there and Kit is brought back there at the end.
The Ace (Al-Laz, Wattar) is set in an unnamed village and is not added (tools/selection/verify/p9_houses_1124.py).
No photo yet for Constantine.

Usage: python3 -I tools/content/batches/add_dz2.py <app_dir> tools/content/batches/coords/add_dz2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
b.init(APP, "", "dz", DATE)
OLD_PLACES = ids_in(b.data("places.js"))
def check(books, places, lines):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    assert not {p["id"] for p in places} & OLD_PLACES and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    ok = {p["id"] for p in places} | OLD_PLACES
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in ok, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {p["id"] for p in places} <= {l["place_ids"][0] for l in lines}
books = [
    BK("memory-in-the-flesh", "Memory in the Flesh", "肉体的记忆", "ذاكرة الجسد", "Ahlam Mosteghanemi", "阿赫拉姆·穆斯塔格尼米", "أحلام مستغانمي",
       "1993", "ar", ["The Bridges of Constantine", "Dhakirat al-Jasad", "Khaled", "Hayat", "Mosteghanemi", "Mostaghanemi"]),
    BK("the-sheltering-sky", "The Sheltering Sky", "遮蔽的天空", "The Sheltering Sky", "Paul Bowles", "保罗·鲍尔斯", "Paul Bowles",
       "1949", "en", ["Port Moresby", "Kit Moresby", "Tunner", "Bowles"]),
]
places = [
    b.ORIG("dz-constantine", "Constantine", "君士坦丁", *C("dz-constantine"),
           "City in eastern Algeria built on a rock above the gorge of the Rhumel, crossed by seven bridges, among them the Sidi M'Cid suspension bridge (1912); it is called the City of Bridges. In Memory in the Flesh (1993) the bridges of Constantine are what the exiled painter Khaled paints, again and again, in Paris; the English translation of 2013 is titled The Bridges of Constantine",
           "阿尔及利亚东部的城市，建在鲁迈勒河峡谷上方的岩石上，峡谷上架着七座桥，其中有 1912 年的西迪·姆西德吊桥，所以人称“桥城”。《肉体的记忆》（1993）里，流亡巴黎的画家哈利德一遍又一遍地画的，就是君士坦丁的桥；2013 年的英译本就叫《君士坦丁的桥》"),
]
lines = [
    b.S("dz-mf-1", "memory-in-the-flesh", "dz-constantine", "The novel as a whole", "全书",
        "Khaled, who lost his arm fighting in the Algerian war of independence, has become a painter and lives in exile in Paris, where he paints the bridges of Constantine over and over. There he meets Hayat, now a young woman and a writer, the daughter of Si Taher, his commander in the war, who was killed fighting the French and whom Khaled had known as a child. He falls obsessively in love with her; Ziyad, a Palestinian poet and fighter, comes between them, and in the end she bows to custom and marries a powerful man of the regime. The whole novel is Khaled's monologue.",
        "哈利德在阿尔及利亚独立战争中失去了一条胳膊，后来成了画家，流亡在巴黎，一遍又一遍地画君士坦丁的桥。他在那里遇见了海娅特——他战时的指挥官西·塔希尔的女儿。西·塔希尔死在同法国人的战斗中，哈利德认识她时她还是个孩子，如今已长成年轻女子，也写作。他痴迷地爱上了她；巴勒斯坦诗人、战士齐亚德插在他们之间，最后她顺从习俗，嫁给了政权里一个有权势的人。整部小说是哈利德的独白。",
        ["Constantine"], ["君士坦丁"],
        "https://aljadid.com/node/171; https://www.echoroukonline.com/summer-book-ahlam-mosteghanemi-memory-in-the-flesh/amp; https://en.wikipedia.org/wiki/Memory_in_the_Flesh; https://www.banipal.co.uk/book_reviews/121/the-bridges-of-constantine/"),
    b.S("dz-ss-1", "the-sheltering-sky", "dz-oran", "The arrival, and the end", "到达与结局",
        "Port and Kit Moresby, a married couple from New York, land in Oran after the Second World War with their friend Tunner, meaning to travel without a plan. From Oran they go south into the Sahara, from town to town. Port, who never had himself vaccinated, catches typhoid and dies in a remote French outpost. Kit wanders off into the desert, joins a caravan and is taken into an Arab man's household; at the end she is found and brought back to Oran.",
        "波特和基特·莫尔斯比是一对来自纽约的夫妇，二战结束后同朋友坦纳在奥兰上岸，打算不定计划地走下去。他们从奥兰往南进入撒哈拉，一镇一镇地走。波特从没打过预防针，染上伤寒，死在一个偏远的法国哨所。基特独自走进沙漠，跟上一支驼队，被一个阿拉伯人收进了家里；最后她被人找到，送回了奥兰。",
        ["Oran"], ["奥兰"],
        "https://www.britannica.com/topic/The-Sheltering-Sky-novel-by-Bowles; https://www.ebsco.com/research-starters/literature-and-writing/sheltering-sky-analysis-setting; https://popmatters.com/paul-bowles-70-year-old-existential-masterpiece-continues-to-test-our-limit-2495456293.html"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_dz2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
