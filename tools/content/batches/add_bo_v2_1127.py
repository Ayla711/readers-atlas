"""11-27: Bolivia, the new books of the selection re-check (tools/selection/bo.md, rule v2; on 11-27 the user took these three).
The book records go to the shared South American list (data/sa/books.js). Places, with the reason for each:
- La Coronilla, Cochabamba, for Juan de la Rosa: the novel's account of the women who stood on the Coronilla hill on 27 May
  1812 shaped Cochabamba's memory of them.
- Copacabana for Raza de bronce: the Aymara community and the Pantoja hacienda, Kohahuyo, are on the shore of Lake Titicaca,
  at no named point; Copacabana is the lake's best-known town on the Bolivian shore (A-24, said in the note).
- Cotagaita for La Chaskañawi: the novel is set in San Javier de Chirca, a hamlet of Cotagaita.
Juan de la Rosa (1885) and Raza de bronce (1919) are in the US public domain, but no free text of either was found on
Wikisource or Gutenberg: scene notes, no quotation, as for La Chaskañawi (1947, in copyright).
Usage: python3 -I tools/content/batches/add_bo_v2_1127.py <app_dir> tools/content/batches/coords/add_bo_v2_1127.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "bo", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="juan-de-la-rosa", title="Juan de la Rosa: Memoirs of the Last Soldier of the Independence Movement", title_zh="胡安·德拉罗萨",
         title_orig="Juan de la Rosa. Memorias del último soldado de la independencia", author="Nataniel Aguirre", author_zh="纳塔尼埃尔·阿吉雷",
         year="1885", orig_lang="es", public_domain=False, source_url=None, aliases=["Juan de la Rosa", "Juanito"]),
    dict(id="raza-de-bronce", title="Race of Bronze", title_zh="青铜的种族", title_orig="Raza de bronce", author="Alcides Arguedas",
         author_zh="阿尔西德斯·阿格达斯", year="1919", orig_lang="es", public_domain=False, source_url=None,
         aliases=["Raza de bronce", "Wata-Wara"]),
    dict(id="la-chaskanawi", title="La Chaskañawi", title_zh="星眸姑娘", title_orig="La Chaskañawi", author="Carlos Medinaceli",
         author_zh="卡洛斯·梅迪纳塞利", year="1947", orig_lang="es", public_domain=False, source_url=None,
         aliases=["La Chaskañawi", "La chaskañawi", "Claudina"]),
]

places = [
    b.ORIG("bo-la-coronilla", "La Coronilla, Cochabamba", "科恰班巴 · 科罗尼利亚山", *C("bo-la-coronilla"),
        "The top of the hill of San Sebastián, about 1.4 km from the old centre of Cochabamba, now inside the city. On 27 May 1812, with the patriot army beaten at Pocona, women of Cochabamba dug in here against the royalist general Goyeneche and were overrun; since 1927 the day has been Mother's Day in Bolivia. Nataniel Aguirre's novel Juan de la Rosa (1885) gave the city its account of the heroines of the Coronilla, which later historians repeated and others have since questioned",
        "圣塞瓦斯蒂安山的山顶，离科恰班巴老城中心约 1.4 公里，如今已在城里。1812 年 5 月 27 日，爱国军在波科纳战败后，科恰班巴的妇女在这里筑垒抵抗保王派将军戈耶内切，最终被攻破；1927 年起，这一天成了玻利维亚的母亲节。纳塔尼埃尔·阿吉雷的小说《胡安·德拉罗萨》（1885）为这座城市讲述了“科罗尼利亚女英雄”的故事，后来的史家沿用了这个说法，也有人提出质疑"),
    b.ORIG("bo-copacabana", "Copacabana, Lake Titicaca", "的的喀喀湖 · 科帕卡巴纳", *C("bo-copacabana"),
        "A pilgrimage town on a peninsula of Lake Titicaca, the best known on the lake's Bolivian shore. Alcides Arguedas's Raza de bronce (1919), the founding novel of Bolivian indigenismo, is set among an Aymara community and a hacienda on the shore of the lake, at no named point; it is hung here",
        "的的喀喀湖一个半岛上的朝圣小城，是湖的玻利维亚一侧最有名的地方。阿尔西德斯·阿格达斯的《青铜的种族》（1919）是玻利维亚原住民主义文学的开山之作，写湖边一个艾马拉村社和一座庄园，没有点明具体地点；这里把它放在科帕卡巴纳"),
    b.ORIG("bo-cotagaita", "Cotagaita", "科塔盖塔", *C("bo-cotagaita"),
        "A town in the valleys of southern Potosí, where colonial families, the Medinacelis among them, settled for its mild climate. Carlos Medinaceli set his novel La Chaskañawi (1947) in San Javier de Chirca, a hamlet of Cotagaita; some say he was born in Cotagaita, others in Sucre",
        "玻利维亚波托西省南部河谷里的小城，殖民时期不少世家（梅迪纳塞利家族也在其中）因为气候温和而定居于此。卡洛斯·梅迪纳塞利把小说《星眸姑娘》（1947）放在科塔盖塔的小村圣哈维尔-德奇尔卡；有人说他生在科塔盖塔，也有人说生在苏克雷"),
]

lines = [
    b.S("bo-rosa-s1", "juan-de-la-rosa", "bo-la-coronilla", "The novel as a whole", "全书",
        "Written as the memoirs of Juan de la Rosa, an old colonel and the last soldier of the War of Independence, the novel goes back to his boyhood in Cochabamba between 1809 and 1812: Juanito, the orphaned son of Rosita, grows up among the patriots, with his uncle Fray Justo and the insurgent Esteban Arze, through the death of his mother, the risings and the Spanish repression under General Goyeneche. Its account of the women of Cochabamba who faced Goyeneche on the hill of San Sebastián on 27 May 1812 became the city's memory of the heroines of the Coronilla. Serialised in 1884 and printed in 1885 under the name of Juan de la Rosa, it heads Bolivia's 2009 official list of the ten most representative novels.",
        "小说写成一位老上校、独立战争最后一名老兵胡安·德拉罗萨的回忆录，回到他 1809 到 1812 年在科恰班巴的少年时代：罗西塔的孤儿胡安尼托在爱国者中间长大，身边有舅舅胡斯托修士和起义者埃斯特万·阿尔塞，经历了母亲之死、一次次起义和戈耶内切将军治下的西班牙镇压。书中写 1812 年 5 月 27 日科恰班巴妇女在圣塞瓦斯蒂安山上迎战戈耶内切的一段，成了这座城市对“科罗尼利亚女英雄”的记忆。它 1884 年连载、1885 年成书，署名胡安·德拉罗萨；2009 年玻利维亚官方评选十部最具代表性的小说，它名列第一。",
        ["Cochabamba"], ["科恰班巴"],
        "https://es.wikipedia.org/wiki/Juan_de_la_Rosa; https://en.wikipedia.org/wiki/Nataniel_Aguirre; https://www.lostiempos.com/node/497389; https://www.lostiempos.com/node/57269; https://www.abebooks.co.uk/Juan-Rosa-Paperback-Nataniel-Aguirre-Linkgua/32048744965/bd; https://es.wikipedia.org/wiki/Hero%C3%ADnas_de_la_Coronilla"),
    b.S("bo-raza-s1", "raza-de-bronce", "bo-copacabana", "The novel as a whole", "全书",
        "Wata-Wara, a shepherdess, and Agiali, a fisherman, are young Aymara of a community on the shore of Lake Titicaca who serve the hacienda of the landowner Pablo Pantoja. In the first part, \"The valley\", Agiali and three other colonos make the brutal journey down to the valleys to buy seed for the hacienda, and one of them, Manuno, is swept away by a flooded river. In the second, \"The barren land\", on the altiplano, the administrator rapes Wata-Wara, and in the end Pantoja and his friends kill her as they try to rape her; the community, urged on by the old sage Choquehuanka, rises and sets the hacienda alight. Arguedas grew it from his short novel Wata-Wara (1904), a story he was told on a trip to the lake; it is counted the first Bolivian indigenista novel.",
        "牧羊女瓦塔-瓦拉和渔夫阿希亚利是的的喀喀湖边一个艾马拉村社的年轻人，给庄园主巴勃罗·潘托哈的庄园当差。第一部《河谷》里，阿希亚利和另外三个佃农被派下山谷为庄园买种子，一路艰险，其中的马努诺被涨水的河冲走。第二部《荒原》发生在高原上：庄园管家强暴了瓦塔-瓦拉，最后潘托哈和他的朋友们企图强暴她时把她杀死；村社在老智者乔克万卡的鼓动下起来，放火烧了庄园。阿格达斯由 1904 年的中篇《瓦塔-瓦拉》发展出这部小说，故事是他去湖边旅行时听人讲的；它被看作玻利维亚第一部原住民主义小说。",
        ["Lake Titicaca"], ["的的喀喀湖"],
        "https://es.wikipedia.org/wiki/Raza_de_bronce; https://revistaliteratura.uchile.cl/index.php/RCL/article/download/41426/42967/; https://nrfh.colmex.mx/index.php/nrfh/article/download/648/648; https://ojs.umsa.bo/index.php/estudiosbolivianos/article/download/1525/1177/3253; https://www.themodernnovel.org/americas/latin-america/bolivia/arguedas/raza/"),
    b.S("bo-chaska-s1", "la-chaskanawi", "bo-cotagaita", "The novel as a whole", "全书",
        "Adolfo Reyes, a young gentleman of the landowning oligarchy, comes back from his studies in Sucre to the family estate at San Javier de Chirca to keep his newly widowed mother company. Torn between Julia Valdez, the proper match expected of him, and his passion for Claudina, the chola they call La Chaskañawi, \"star eyes\" in Quechua, he runs off with Claudina, against a background of the 1920s feud between the parties of Saavedra and Montes. His choice reads as a break with the old social order and a figure of mestizaje, the \"encholamiento\" that was a great theme of the indigenista novel. It was Medinaceli's last novel, published in 1947.",
        "阿道夫·雷耶斯是地主寡头家族的少爷，在苏克雷读完书，回到圣哈维尔-德奇尔卡的家族庄园陪伴新寡的母亲。他在家里期待的门当户对的胡利娅·巴尔德斯和他热恋的混血姑娘克劳迪娜之间摇摆，克劳迪娜外号“恰斯卡尼亚维”，盖丘亚语意为“星星般的眼睛”；最后他带着克劳迪娜私奔，背景是 1920 年代萨韦德拉派和蒙特斯派的争斗。他的选择被读作与旧社会秩序的决裂、种族混融的象征，也就是原住民主义小说的一大主题“混血化”。这是梅迪纳塞利的最后一部小说，1947 年出版。",
        ["San Javier de Chirca"], ["圣哈维尔-德奇尔卡"],
        "https://es.wikipedia.org/wiki/La_chaska%C3%B1awi; https://es.wikipedia.org/wiki/Carlos_Medinaceli_Quintana_(escritor); https://es.wikipedia.org/wiki/Santiago_de_Cotagaita"),
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
