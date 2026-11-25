"""11-25: Bosnia and Herzegovina, the 3 books that selection rule v2 adds (tools/selection/ba.md). Bosnia opens with this
batch. All three books are in copyright: scene notes in our own words. Places, with the reason for each:
- The Bridge on the Drina: the Mehmed Paša Sokolović Bridge, Višegrad, which the novel follows for four centuries.
  Coordinates from the Serbian Wikipedia (the English article gives none through the API).
- Death and the Dervish: Sarajevo (city-level pin). The novel does not name its town; the English translation's
  introduction calls it simply the kasaba, the publisher's description places the dervish lodge in Sarajevo.
- Bosnian Chronicle: Travnik, where the French and Austrian consuls of the novel lived from 1807 to 1814.
The language code "sh" (Serbo-Croatian) is added to tools/validate.js and js/i18n.js for Yugoslav-era books.
Usage: python3 -I tools/content/batches/add_ba1.py <app_dir> tools/content/batches/coords/add_ba1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-25"
b.init(APP, "", "ba", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, year, aliases):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang="sh", public_domain=False, source_url=None, aliases=aliases)

books = [
    BK("bridge-on-the-drina", "The Bridge on the Drina", "德里纳河上的桥", "Na Drini ćuprija", "Ivo Andrić", "伊沃·安德里奇", "1945",
       ["Na Drini ćuprija", "На Дрини ћуприја", "Višegrad"]),
    BK("death-and-the-dervish", "Death and the Dervish", "苦修僧与死亡", "Derviš i smrt", "Meša Selimović", "梅沙·塞利莫维奇", "1966",
       ["Derviš i smrt", "Дервиш и смрт"]),
    BK("bosnian-chronicle", "Bosnian Chronicle", "特拉夫尼克纪事", "Travnička hronika", "Ivo Andrić", "伊沃·安德里奇", "1945",
       ["Travnička hronika", "Травничка хроника", "The Days of the Consuls"]),
]

places = [
    b.ORIG("ba-visegrad-bridge", "Mehmed Paša Sokolović Bridge, Višegrad", "维舍格拉德的穆罕默德-帕夏·索科洛维奇桥", *C("ba-visegrad-bridge"),
        "The Ottoman bridge over the Drina at Višegrad, begun in 1566 for the grand vizier Mehmed Paša Sokolović and finished five years later; a UNESCO World Heritage Site. The Bridge on the Drina follows it and the town around it for some four hundred years, from its building to its partial destruction in the First World War",
        "维舍格拉德跨越德里纳河的奥斯曼古桥，1566 年为大维齐尔穆罕默德-帕夏·索科洛维奇动工，五年后建成，是联合国教科文组织世界遗产。《德里纳河上的桥》从造桥写起，写这座桥和桥边小城大约四百年，直到第一次世界大战中桥被炸毁一部分"),
    b.ORIG("ba-sarajevo", "Sarajevo", "萨拉热窝", *C("ba-sarajevo"),
        "Death and the Dervish is set around a dervish lodge in an eighteenth-century Bosnian town that the novel never names; the English translation's introduction calls it simply the kasaba, the market town, and the publisher's description places the lodge in Sarajevo, where the novel was first published in 1966",
        "《苦修僧与死亡》的故事围绕 18 世纪波斯尼亚一座城镇里的苦修院展开，小说始终没写城镇的名字；英译本导言只把它叫作“卡萨巴”（集镇），出版社的简介说苦修院在萨拉热窝。小说 1966 年在萨拉热窝首次出版"),
    b.ORIG("ba-travnik", "Travnik", "特拉夫尼克", *C("ba-travnik"),
        "The seat of the Ottoman vizier of Bosnia in the years of Bosnian Chronicle, whose French and Austrian consuls lived here from 1807 to 1814. The novel opens and closes in Lutva's coffee house, where the town's beys gather",
        "《特拉夫尼克纪事》那些年里，这里是奥斯曼帝国波斯尼亚总督的驻地，小说里的法国和奥地利领事 1807 年至 1814 年住在这里。小说在卢特瓦咖啡馆开头，也在那里结尾，城里的贝伊们常在那儿聚会"),
]

lines = [
    b.S("ba-bd-1", "bridge-on-the-drina", "ba-visegrad-bridge", "The building of the bridge", "造桥",
        "The future grand vizier Mehmed Paša Sokolović was a Serb boy from near Višegrad, taken by the Ottomans in their levy of Christian children. He was ferried across the Drina while his mother followed him, wailing, as far as the river. Haunted by that memory, he orders a bridge built where the two were parted. Work begins in 1566; the serfs forced to build it sabotage the site, and the Ottomans impale the one saboteur they catch. Five years later the bridge is finished, and its wider middle section, the kapija, becomes the town's meeting place for four centuries.",
        "未来的大维齐尔穆罕默德-帕夏·索科洛维奇原是维舍格拉德附近的一个塞尔维亚男孩，在奥斯曼帝国征收基督徒男孩时被带走。他被渡船载过德里纳河，母亲一路哭喊着追到河边，再也追不过去。这段记忆一直缠着他，他下令就在母子分离的地方造一座桥。1566 年动工，被迫干活的农奴暗中破坏工地，奥斯曼人把抓到的那一个破坏者处以穿刺刑。五年后桥建成，桥中间加宽的那一段叫“卡皮亚”，此后四百年成了全城人聚会的地方。",
        ["Višegrad"], ["维舍格拉德"], "https://en.wikipedia.org/wiki/The_Bridge_on_the_Drina"),
    b.S("ba-dd-1", "death-and-the-dervish", "ba-sarajevo", "St George's Day", "圣乔治节",
        "Sheikh Ahmed Nuruddin, the respected head of a dervish lodge in eighteenth-century Bosnia, learns that his brother Harun has been arrested by the Ottoman authorities. It is St George's Day, and everyone is celebrating but him. He goes to the kadi to speak for his brother and refuses Hassan's offer to go to the fortress and help Harun escape; then he learns that Harun was killed in prison three days before. He sets it all down as a kind of long suicide note. The novel never names the town; the publisher's description sets the lodge in Sarajevo.",
        "谢赫艾哈迈德·努鲁丁是 18 世纪波斯尼亚一座苦修院里受人尊敬的长老。他得知弟弟哈伦被奥斯曼官府抓走了。那天是圣乔治节，人人都在过节，只有他没有。他去找卡迪为弟弟说情，又拒绝了哈桑去要塞帮哈伦逃走的提议；后来他才得知，哈伦三天前已经死在牢里。他把这一切写下来，像是一封长长的遗书。小说始终没写城镇的名字，出版社的简介说苦修院在萨拉热窝。",
        ["Sarajevo"], ["萨拉热窝"],
        "https://en.wikipedia.org/wiki/Death_and_the_Dervish; https://mitpressbookstore.mit.edu/book/9780810112971; https://www.knjizara.com/pdf/154148.pdf"),
    b.S("ba-bc-1", "bosnian-chronicle", "ba-travnik", "The consuls arrive", "领事们来了",
        "In 1807 Jean Daville arrives in Travnik as Napoleon's consul, a man from civilised Europe set down in a closed and harsh Bosnian town. He becomes friends with the vizier Mehmed Pasha and distrusts his interpreter d'Avenat. When the Austrian consul von Mitterer arrives, the two diplomats move from rivalry to mutual understanding as the politics of Europe shift. As Napoleon's power declines the French consulate closes and Daville leaves; the people of Travnik, distrustful at first, find that the consuls did not bring what they had most feared.",
        "1807 年，让·达维尔作为拿破仑的领事来到特拉夫尼克，一个来自文明欧洲的人，落进了这座封闭而严酷的波斯尼亚小城。他和总督穆罕默德帕夏交上了朋友，却不信任自己的译员达弗纳。奥地利领事冯·米特雷尔来了以后，随着欧洲政局的变化，两位外交官从对手变成了相互理解的人。拿破仑的势力衰落，法国领事馆关闭，达维尔离开；起初疑虑重重的特拉夫尼克人发现，领事们并没有带来他们最害怕的事。",
        ["Travnik"], ["特拉夫尼克"], "https://en.wikipedia.org/wiki/Bosnian_Chronicle"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places}
assert not new_b & all_books, new_b & all_books
assert new_p == set(CO), new_p ^ set(CO)
for l in lines:
    assert l["book_id"] in new_b and l["place_ids"][0] in new_p, l["id"]
assert {l["book_id"] for l in lines} == new_b and {l["place_ids"][0] for l in lines} == new_p

HEAD = "// Bosnia and Herzegovina, hand-written content (tools/content/batches/add_ba1.py, 2026-11-25).\n"
def write(name, key, entries, extra=""):
    os.makedirs(os.path.dirname(b.data(name)), exist_ok=True)
    with open(b.data(name), "w", encoding="utf-8") as fh:
        fh.write(HEAD + extra + "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA." + key + " = [\n"
                 + ",\n".join("  " + b.obj(e) for e in entries) + "\n];\n")
if __name__ == "__main__":
    for f in ("books.js", "places.js", "lines.js"):
        assert not os.path.exists(b.data(f)), ("already there", f)
    write("books.js", "books", books)
    write("places.js", "places", places, "// Each place's admin-1 region is worked out from its coordinates by app.js.\n")
    write("lines.js", "lines", lines)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
