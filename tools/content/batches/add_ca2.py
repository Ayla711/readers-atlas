"""11-24: Canada, second pack: the two books of the first pack's list that were left out for having no real place,
A Season in the Life of Emmanuel and Bear. The atlas's rule is that a book worth having is hung on the nearest real
place even when its exact spot cannot be found, so each gets a scene note at the closest place the sources support.

Emmanuel's farm is an unnamed one in rural Quebec; the line hangs at Quebec City, where Marie-Claire Blais was born.
Bear is set in the Algoma District of north-eastern Ontario, on an invented island; the line hangs at the district's own
point as English Wikipedia gives it.

Usage: python3 -I add_ca2.py <app_dir> <coords.json>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
b.init(APP, "", "ca", DATE)

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=lang, public_domain=False, source_url=None, author_orig=author_orig)
    d.update(kw)
    return d

books = [
    BK("season-in-the-life-of-emmanuel", "A Season in the Life of Emmanuel", "埃马纽埃尔生命中的一季", "Une saison dans la vie d’Emmanuel",
       "Marie-Claire Blais", "玛丽-克莱尔·布莱", "Marie-Claire Blais", "1965", "fr",
       aliases=["Une saison dans la vie d'Emmanuel", "Jean-Le Maigre", "Grand-mère Antoinette", "Blais"]),
    BK("bear-engel", "Bear", "熊", "Bear", "Marian Engel", "玛丽安·恩格尔", "Marian Engel", "1976", "en",
       aliases=["Lou", "Cary's Island", "Pennarth", "Algoma", "Engel"]),
]
places = [
    b.ORIG("ca-quebec-city", "Quebec City", "魁北克城", *C("ca-quebec-city"),
           "Capital of the province of Quebec, where Marie-Claire Blais was born in 1939 into a working-class family. A Season in the Life of Emmanuel (1965), which won the Prix Médicis in 1966, is set on a poor farm in rural Quebec that the novel never names, so the book hangs here",
           "魁北克省省会，玛丽-克莱尔·布莱 1939 年生在这里一个工人家庭。《埃马纽埃尔生命中的一季》（1965）1966 年获美第奇奖，故事发生在魁北克乡间一座穷苦的农场，小说没有点出地名，所以这本书挂在这里"),
    b.ORIG("ca-algoma", "Algoma District, Ontario", "阿尔戈马区，安大略省", *C("ca-algoma"),
           "Wooded district of lakes and rivers in north-eastern Ontario, on the Canadian Shield. Marian Engel's Bear (1976), which won the Governor General's Award, is set here, on an invented island estate on a remote lake. The pin is the district's own point, not the island",
           "安大略省东北部、加拿大地盾上一片湖泊河流纵横的林区。玛丽安·恩格尔获总督文学奖的小说《熊》（1976）就设在这里，在一座偏远湖泊中虚构的小岛庄园上。图钉标在这个区的位置，不是那座岛"),
]
lines = [
    b.S("ca-em-1", "season-in-the-life-of-emmanuel", "ca-quebec-city", "The novel as a whole", "全书",
        "A large, poor farm family in rural Quebec, ruled by the grandmother Antoinette, in the season of the birth of Emmanuel, the sixteenth child. The novel follows his teenage brothers and sisters, Jean-Le Maigre, Pomme, Héloïse and the one called Septième, each in some kind of revolt against the family and the church-ruled world around it.",
        "魁北克乡间一个贫穷的农家大家庭，由祖母安托瓦妮特当家，时间是第十六个孩子埃马纽埃尔出生的那一季。小说跟着他十几岁的哥哥姐姐——让-勒迈格尔、波姆、埃卢瓦兹和被叫作“第七”的那一个——他们各自以某种方式反抗着家庭，反抗着由教会主宰的周遭世界。",
        ["Quebec"], ["魁北克"], "https://en.wikipedia.org/wiki/A_Season_in_the_Life_of_Emmanuel; https://www.ebsco.com/research-starters/literature-and-writing/season-life-emmanuel-marie-claire-blais"),
    b.S("ca-be-1", "bear-engel", "ca-algoma", "The novel as a whole", "全书",
        "Lou, a reserved librarian and archivist at a historical institute in Toronto, is sent for a summer to an island estate on a remote lake in northern Ontario, left to the institute with the library of a nineteenth-century colonel, to catalogue the books. The island has one other inhabitant, a bear, and her slow communion with it and with the wild changes her.",
        "露是多伦多一家历史研究所里拘谨的图书管理员兼档案员。研究所继承了安大略北部一座偏远湖泊中的小岛庄园和一位 19 世纪上校的藏书，派她去待一个夏天，给藏书编目。岛上还有另一个住户——一头熊；她与熊、与荒野慢慢的交融，改变了她。",
        ["northern Ontario"], ["安大略北部"], "https://en.wikipedia.org/wiki/Bear_(novel); https://thecanadianencyclopedia.ca/en/article/marian-engel; https://www.indigo.ca/products/bear-kanata-classics-edition"),
]

import re
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
for f, new in (("books.js", books), ("places.js", places), ("lines.js", lines)):
    clash = {e["id"] for e in new} & ids_in(b.data(f))
    assert not clash, (f, clash)
for l in lines:
    assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in {p["id"] for p in places}, l["id"]

if __name__ == "__main__":
    M = "11-24: second pack, the two books left out of the first (tools/content/batches/add_ca2.py)"
    b.append(b.data("books.js"), books, M)
    b.append(b.data("places.js"), places, M)
    b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
