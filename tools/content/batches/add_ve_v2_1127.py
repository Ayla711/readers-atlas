"""11-27: Venezuela, the new book of the selection re-check (tools/selection/ve.md, rule v2): Doña Bárbara, taken as an
exception (破例收) by the user on 11-27.
The book record goes to the shared South American list (data/sa/books.js). Place:
- The Arauca river for Doña Bárbara: the novel is set in the plains of Apure, on the lands along the Arauca.
Doña Bárbara (1929) is in the US public domain, but no free text of it was found (not on Wikisource or Gutenberg): a scene
note, no quotation.
Usage: python3 -I tools/content/batches/add_ve_v2_1127.py <app_dir> tools/content/batches/coords/add_ve_v2_1127.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "ve", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="dona-barbara", title="Doña Bárbara", title_zh="堂娜芭芭拉", title_orig="Doña Bárbara", author="Rómulo Gallegos",
         author_zh="罗慕洛·加列戈斯", year="1929", orig_lang="es", public_domain=False, source_url=None,
         aliases=["Doña Bárbara", "Santos Luzardo", "Altamira", "El Miedo"]),
]

places = [
    b.ORIG("ve-rio-arauca", "Arauca River", "阿劳卡河", *C("ve-rio-arauca"),
        "The most typical river of the Llanos: it rises in the Colombian Andes, forms the southern border of the Venezuelan state of Apure and flows into the Orinoco; the point here is near its mouth. Rómulo Gallegos travelled to the Llanos in 1927 to research his next novel, and set Doña Bárbara (1929) in the plains of Apure, on the lands along the Arauca",
        "大平原上最典型的河流：发源于哥伦比亚安第斯山，构成委内瑞拉阿普雷州的南界，汇入奥里诺科河；地图上的点在河口附近。罗慕洛·加列戈斯 1927 年专程去大平原为下一部小说搜集素材，把《堂娜芭芭拉》（1929）放在阿普雷平原、阿劳卡河沿岸的土地上"),
]

lines = [
    b.S("ve-barbara-s1", "dona-barbara", "ve-rio-arauca", "The novel as a whole", "全书",
        "Santos Luzardo, a young lawyer from Caracas, comes back to the plains of Apure to save his family's ranch, Altamira, on the Arauca, from Doña Bárbara, the beautiful and ruthless owner of the neighbouring ranch, El Miedo, who has seized land after land by bribery, violence and, it is said, witchcraft. Raped as a girl by the river smugglers she grew up with, she has turned her rage on men; she ruined Lorenzo Barquero, the father of her daughter Marisela, and took his ranch. Luzardo brings the law to the plains and educates the half-wild Marisela, and in the end Doña Bárbara vanishes. The book stages the struggle of civilisation against barbarism, read as a protest against the dictatorship of Juan Vicente Gómez; it is the most popular Venezuelan novel.",
        "年轻的加拉加斯律师桑托斯·卢萨尔多回到阿普雷平原，要从堂娜芭芭拉手里保住家族在阿劳卡河边的庄园阿尔塔米拉。堂娜芭芭拉是邻近庄园“恐惧庄”的女主人，美貌而冷酷，靠贿赂、暴力，据说还有巫术，一块接一块地吞并土地。她少女时被一起长大的河上走私贩强暴，从此把怒火撒向男人；她毁了女儿马里塞拉的父亲洛伦索·巴尔克罗，夺走了他的庄园。卢萨尔多把法律带进平原，教化半野性的马里塞拉，最后堂娜芭芭拉消失了。这本书写的是文明与野蛮的斗争，被读作对胡安·比森特·戈麦斯独裁的抗议；它是委内瑞拉最受欢迎的小说。",
        ["Arauca", "Apure"], ["阿劳卡河", "阿普雷"],
        "https://es.wikipedia.org/wiki/Do%C3%B1a_B%C3%A1rbara_(novela); https://es.wikipedia.org/wiki/R%C3%B3mulo_Gallegos; https://www.bookshare.org/browse/book/3817521"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places
assert not {l["id"] for l in lines} & all_lines
if __name__ == "__main__":
    note = f"11-27 selection re-check, rule v2 ({os.path.basename(__file__)})"
    b.append(SA_BOOKS, books, note)
    b.append(b.data("places.js"), places, note)
    b.append(b.data("lines.js"), lines, note)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
