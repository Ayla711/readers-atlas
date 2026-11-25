"""11-24: Ukraine, third pack: Do the Oxen Low When the Manger Is Full? (Panas Myrny with Ivan Bilyk, 1880), held back as
"place to be checked". The novel's village, Pisky, is not identified (there are several villages of that name in Poltava
region); under the rule for famous books it is hung at Myrhorod, where Myrny was born in 1849 and later worked (place type
prototype, honest note). The novel is in the public domain, but no passage names a real place to highlight, so it gets a
scene note in our own words. Photos: tools/content/batches/add_photos_held_1124.py.

Usage: python3 -I tools/content/batches/add_ua3.py <app_dir> tools/content/batches/coords/add_ua3.json"""
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
b.init(APP, "", "ua", DATE)
books = [
    BK("do-the-oxen-low", "Do the Oxen Low When the Manger Is Full?", "牛满槽还会叫吗", "Хіба ревуть воли, як ясла повні?",
       "Panas Myrny", "帕纳斯·米尔尼", "Панас Мирний", "1880", "uk",
       ["Khiba revut voly, yak yasla povni?", "Do Oxen Low When Mangers are Full?", "Do the Oxen Bellow, When Their Mangers Are Full?",
        "Propashcha syla", "Chipka", "Chipka Varenychenko", "Ivan Bilyk"], pd=True,
       src="https://uk.wikisource.org/wiki/%D0%A5%D1%96%D0%B1%D0%B0_%D1%80%D0%B5%D0%B2%D1%83%D1%82%D1%8C_%D0%B2%D0%BE%D0%BB%D0%B8,_%D1%8F%D0%BA_%D1%8F%D1%81%D0%BB%D0%B0_%D0%BF%D0%BE%D0%B2%D0%BD%D1%96%3F"),
]
places = [
    b.PROTO("ua-myrhorod", "Myrhorod", "米尔霍罗德", *C("ua-myrhorod"),
            "the Poltava country of Panas Myrny's Do the Oxen Low When the Manger Is Full? (1880). The novel's village, Pisky, has not been identified, as there are several villages of that name in Poltava region; Myrny was born in Myrhorod in 1849 and later worked there as a treasury clerk, and the book is hung at Myrhorod as the nearest real place",
            "帕纳斯·米尔尼《牛满槽还会叫吗》（1880）里的波尔塔瓦乡间。小说里的村子叫皮斯基，但波尔塔瓦州有好几个皮斯基，是哪一个没能确定；米尔尼 1849 年生在米尔霍罗德，后来又在那里的县金库当过会计，这本书就近挂在米尔霍罗德"),
]
lines = [
    b.S("ua-ox-1", "do-the-oxen-low", "ua-myrhorod", "The novel as a whole", "全书",
        "The village of Pisky, in the Poltava country of central Ukraine, over about a century, from the end of the Zaporozhian Sich in 1775 to the abolition of serfdom in 1861. Nikifor Varenychenko, called Chipka, a poor, illegitimate village boy, grows up hating a world divided into masters and servants. When the plot of land his family has won is handed to someone else, he goes to law, and is met with a clerk who wants a bribe and a petition-writer who steals his mother's savings. Drink and three bad companions lead him into theft; he rises for a while to a seat on the zemstvo, but his past is used to throw him out, and he goes back to crime, down to murder. His beloved Halya hangs herself, and Chipka is sent to hard labour in Siberia. The title asks the novel's question: would oxen bellow if their mangers were full? (Pisky is not identified; Myrny was born in Myrhorod.)",
        "乌克兰中部波尔塔瓦乡间的皮斯基村，前后大约一百年：从 1775 年扎波罗热营地被取消，到 1861 年废除农奴制。尼基福尔·瓦列尼琴科，外号奇普卡，是村里一个贫穷的私生子，从小就恨这个把人分成老爷和仆人的世界。家里好不容易得到的一块地被判给了别人，他去打官司，碰上的是索贿的书吏，和偷走他母亲积蓄的代写状子的人。酒和三个坏伙伴把他引上了偷盗的路；他一度当上了地方自治会的议员，可别人拿他的过去把他赶了下来，他又回去作恶，直到杀人。他爱的哈利娅上吊自尽，奇普卡被送到西伯利亚服苦役。书名问的就是小说的问题：牛槽要是满的，牛还会叫吗？（皮斯基未能确定；米尔尼生在米尔霍罗德。）",
        ["Myrhorod"], ["米尔霍罗德"],
        "https://en.wikipedia.org/wiki/Do_Oxen_Low_When_Mangers_are_Full%3F; https://en.wikipedia.org/wiki/Panas_Myrny; https://www.encyclopediaofukraine.com/pages%5CM%5CY%5CMyrnyPanas.htm; https://www.britannica.com/biography/Panas-Myrny"),
]
check(books, places, lines)
if __name__ == "__main__":
    run(books, places, lines, "add_ua3.py")
