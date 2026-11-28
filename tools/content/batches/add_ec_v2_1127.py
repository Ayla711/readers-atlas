"""11-27: Ecuador, the new book of the selection re-check (tools/selection/ec.md, rule v2; the user took it on 11-27). The book
is by the Chilean Luis Sepúlveda; it was moved from the Chilean table to Ecuador's because it is set in the Ecuadorian Amazon.
The book record goes to the shared South American list (data/sa/books.js). Place:
- The Nangaritza river for Un viejo que leía novelas de amor: El Idilio, the old man's village, is on the Nangaritza, his hut
  facing the river.
In copyright: a scene note, no quotation.
Usage: python3 -I tools/content/batches/add_ec_v2_1127.py <app_dir> tools/content/batches/coords/add_ec_v2_1127.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "ec", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="the-old-man-who-read-love-stories", title="The Old Man Who Read Love Stories", title_zh="读爱情故事的老人",
         title_orig="Un viejo que leía novelas de amor", author="Luis Sepúlveda", author_zh="路易斯·塞普尔维达", year="1989",
         orig_lang="es", public_domain=False, source_url=None, aliases=["Un viejo que leía novelas de amor", "El Idilio"]),
]

places = [
    b.ORIG("ec-rio-nangaritza", "Nangaritza River", "南加里察河", *C("ec-rio-nangaritza"),
        "A river of the Ecuadorian Amazon in Zamora Chinchipe province, the largest tributary of the Zamora, in one of the most biodiverse valleys on earth. Luis Sepúlveda, who had lived among the Shuar, set Un viejo que leía novelas de amor (1989) in El Idilio, a village on the Nangaritza, drawing on stories told him by Miguel Tzenke, a Shuar leader of Sumbi on the upper Nangaritza",
        "厄瓜多尔亚马孙地区萨莫拉-钦奇佩省的一条河，是萨莫拉河最大的支流，流经地球上生物最多样的河谷之一。曾和舒阿尔人一起生活的路易斯·塞普尔维达，把《读爱情故事的老人》（1989）放在南加里察河边的小村埃尔伊迪利奥，书中借用了上游松比村舒阿尔族首领米格尔·曾克讲给他的故事"),
]

lines = [
    b.S("ec-viejo-s1", "the-old-man-who-read-love-stories", "ec-rio-nangaritza", "The novel as a whole", "全书",
        "Antonio José Bolívar Proaño lives alone in a hut facing the Nangaritza at El Idilio, a remote settlement in the Ecuadorian Amazon. He came as a settler, lost his wife there, and learned the forest from the Shuar, who taught him their ways. Discovering that he can read, he has Rubicundo Loachamín, the travelling dentist who comes up the river on the boat Sucre, bring him love stories for his old age. When a female jaguar, maddened, it seems, by the loss of her cubs, starts killing men, the mayor makes the old man join the hunt. The novel sold some 18 million copies in 60 languages.",
        "安东尼奥·何塞·玻利瓦尔·普罗阿尼奥独自住在厄瓜多尔亚马孙偏远村落埃尔伊迪利奥一间面朝南加里察河的小屋里。他当年作为垦荒者来到这里，妻子死在了这里，后来跟舒阿尔人学会了森林里的生存之道。发现自己识字后，他托乘“苏克雷号”沿河而来的流动牙医鲁比昆多·洛阿查明给他带爱情小说，打发晚年。一头母美洲豹似乎因失去幼崽而发狂，开始伤人，镇长让老人加入猎杀它的队伍。这部小说译成 60 种语言，卖出约 1800 万册。",
        ["Nangaritza"], ["南加里察河"],
        "https://es.wikipedia.org/wiki/Un_viejo_que_le%C3%ADa_novelas_de_amor; https://es.wikipedia.org/wiki/Luis_Sep%C3%BAlveda; https://revistas.tec.ac.cr/index.php/comunicacion/article/download/1273/1176/4117; https://www.tripfiction.com/books/the-old-man-who-read-love-stories/; https://www.pulzo.com/opinion/resena-un-viejo-que-leia-novelas-amor-luis-sepulveda-PP953386; https://es.wikipedia.org/wiki/R%C3%ADo_Nangaritza"),
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
