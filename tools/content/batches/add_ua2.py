"""11-24: Ukraine, second pack: books that selection rule v2 adds (tools/selection/ua.md), as far as their places are found.
Four are in the public domain and get quotations cut from Ukrainian Wikisource (tools/content/wikisource.py); English and
Chinese are our own drafts:
- The City (Pidmohylny, d. 1937; first published 1928): the opening, Stepan on the steamer coming up the Dnieper to Kyiv.
  Pin: Kyiv river port on Podil, where the boat comes in.
- Shadows of Forgotten Ancestors (Kotsiubynsky, 1911): the second paragraph, the roar of the Cheremosh. The village is not
  named; Kotsiubynsky gathered the material in Kryvorivnia in 1910 and 1911 and wrote the novella after he came back
  (Ukrainian Wikipedia, Криворівня), so the pin is Kryvorivnia, place type prototype.
- Zakhar Berkut (Franko, 1883): the opening of chapter II, the old village of Tukhlia.
- The Black Council (Kulish, 1857): the opening of chapter XVI, Briukhovetsky feasting in Nizhyn; edition of 1943.
Two are in copyright and get scene notes: The Enchanted Desna (Dovzhenko, d. 1956) at Sosnytsia, and The Shipmaster
(Yanovsky, 1928), whose text is not on Wikisource, at the Odesa Film Studio.
Not yet added: Do the Oxen Low When the Manger Is Full? (Myrny): its village is Pisky in the Poltava region, on the road to
Romodan, but which of several villages called Pisky it is has not been confirmed. No photos yet.

Usage: python3 -I tools/content/batches/add_ua2.py <app_dir> tools/content/batches/coords/add_ua2.json <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
WS = "https://uk.wikisource.org/wiki/"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
def raw(title, start, end):
    t = ws.text(os.path.join(WSR, "uk"), title)
    i = t.find(start); assert i >= 0, (title, start)
    j = t.find(end, i); assert j >= 0, (title, end)
    return t[i:j + len(end)].replace("\xa0", " ")
def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    assert "[" not in orig and "\xa0" not in orig and "\n" not in orig, id
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls: assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_orig=orig, highlight_orig=hl_orig,
                text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own", status="draft",
                checked=f"Ukrainian Wikisource, {title}{note}, {DATE}")
b.init(APP, "", "ua", DATE)
T_MI, T_TI = "Місто/1/I", "Твори (Коцюбинський, 1955)/2/Тіні забутих предків"
T_ZB, T_CR = "Твори (Франко, 1956–1962)/13/Захар Беркут/II", "Чорна рада (1943)/XVI"
books = [
    BK("misto", "The City", "城市", "Місто", "Valerian Pidmohylny", "瓦列里扬·皮德莫希尔内", "Валер'ян Підмогильний", "1928", "uk",
       ["Misto", "Stepan Radchenko", "Nadiika", "Pidmohylny", "Pidmohylnyi"], pd=True, src=WS + "Місто"),
    BK("shadows-of-forgotten-ancestors", "Shadows of Forgotten Ancestors", "被遗忘的祖先的影子", "Тіні забутих предків", "Mykhailo Kotsiubynsky",
       "米哈伊洛·科秋宾斯基", "Михайло Коцюбинський", "1911", "uk", ["Tini zabutykh predkiv", "Ivan Paliichuk", "Marichka", "Palagna", "Hutsul", "Kotsiubynsky"],
       pd=True, src=WS + T_TI.replace(" ", "_")),
    BK("zakhar-berkut", "Zakhar Berkut", "扎哈尔·别尔库特", "Захар Беркут", "Ivan Franko", "伊万·弗兰科", "Іван Франко", "1883", "uk",
       ["Zakhar Berkut", "Maksym Berkut", "Myroslava", "Tuhar Vovk", "Tukhlia", "Franko"], pd=True, src=WS + "Захар_Беркут"),
    BK("chorna-rada", "The Black Council", "黑色议会", "Чорна рада", "Panteleimon Kulish", "潘捷列伊蒙·库利什", "Пантелеймон Куліш", "1857", "uk",
       ["Chorna rada", "Black Rada", "Shram", "Petro Shramenko", "Somko", "Briukhovetsky", "Kulish"], pd=True, src=WS + "Чорна_рада_(1943)"),
    BK("enchanted-desna", "The Enchanted Desna", "着魔的杰斯纳河", "Зачарована Десна", "Oleksandr Dovzhenko", "亚历山大·杜甫仁科", "Олександр Довженко",
       "1955", "uk", ["Zacharovana Desna", "Sashko", "Dovzhenko", "Desna"]),
    BK("the-shipmaster", "The Shipmaster", "船长", "Майстер корабля", "Yuri Yanovsky", "尤里·亚诺夫斯基", "Юрій Яновський", "1928", "uk",
       ["Maister korablia", "Master of the Ship", "To-Ma-Ki", "Sev", "Taiakh", "Yanovsky", "Ianovskyi"]),
]
places = [
    b.ORIG("ua-kyiv-river-port", "Kyiv river port, Podil", "基辅河港，波迪尔", *C("ua-kyiv-river-port"),
           "The Dnieper landing stage below Podil, the old merchant quarter of Kyiv. Pidmohylny's The City (1928) opens on a steamer coming up the river, with the village youth Stepan Radchenko on deck watching for Kyiv, where he is going to study; he lands at the pier on Podil",
           "基辅老商业区波迪尔下面的第聂伯河码头。皮德莫希尔内的《城市》（1928）开篇在一艘逆流而上的轮船上：乡下青年斯捷潘·拉琴科站在甲板上眺望基辅，他要去那里上学；他在波迪尔的码头上了岸"),
    b.PROTO("ua-kryvorivnia", "Kryvorivnia, Hutsul region", "克里沃里夫尼亚，胡楚尔地区", *C("ua-kryvorivnia"),
            "the Hutsul mountain village of Shadows of Forgotten Ancestors (1911), on the Cheremosh, where Ivan and Marichka grow up. The story does not name the village. Kotsiubynsky came to Kryvorivnia in July 1910 and again the next year, gathered material on Hutsul life here, and wrote the novella after he came back from the Carpathians",
            "《被遗忘的祖先的影子》（1911）里切列莫什河边那个胡楚尔山村，伊万和玛丽奇卡在那里长大。小说没有说出村名。科秋宾斯基 1910 年 7 月来到克里沃里夫尼亚，第二年又来了一次，在这里收集胡楚尔人生活的材料，从喀尔巴阡山回去后写成了这部中篇"),
    b.ORIG("ua-tukhlia", "Tukhlia, Lviv region", "图赫利亚，利沃夫州", *C("ua-tukhlia"),
           "Village in the Carpathians on the upper Opir. Franko's Zakhar Berkut (1883) tells of its mountain community in the thirteenth century, under its elder Zakhar Berkut, standing against the Mongol invasion; the story puts old Tukhlia higher up in a valley now overgrown with forest",
           "喀尔巴阡山中、奥皮尔河上游的村子。弗兰科的《扎哈尔·别尔库特》（1883）写十三世纪这里的山民公社，在长老扎哈尔·别尔库特带领下抵抗蒙古入侵；小说说，古时的图赫利亚在更高处一条如今长满森林的山谷里"),
    b.ORIG("ua-nizhyn", "Nizhyn", "尼任", *C("ua-nizhyn"),
           "Town in the Chernihiv region. On its outskirts in June 1663 the Black Council of the Cossacks elected Ivan Briukhovetsky hetman of the Left Bank over Yakym Somko, who was soon executed. Kulish's historical novel The Black Council (1857) leads up to it",
           "切尔尼戈夫州的城市。1663 年 6 月，哥萨克的“黑色议会”在城郊召开，选伊万·布留霍韦茨基为左岸盖特曼，压过了雅基姆·索姆科——后者不久就被处死。库利什的历史小说《黑色议会》（1857）一路写到的就是这场议会"),
    b.ORIG("ua-sosnytsia", "Sosnytsia, on the Desna", "索斯尼齐亚，杰斯纳河畔", *C("ua-sosnytsia"),
           "Small town in the Chernihiv region where Oleksandr Dovzhenko was born in 1894. The Enchanted Desna, the autobiographical “film story” he wrote at the end of his life, is his childhood here on the banks of the Desna",
           "切尔尼戈夫州的小镇，亚历山大·杜甫仁科 1894 年生在这里。《着魔的杰斯纳河》是他晚年写的自传体“电影小说”，写的就是他在杰斯纳河岸边度过的童年"),
    b.ORIG("ua-odesa-film-studio", "Odesa Film Studio", "敖德萨电影制片厂", *C("ua-odesa-film-studio"),
           "The film studio by the sea in Odesa. Yuri Yanovsky worked at the Odesa film factory as art editor from the spring of 1926 to the autumn of 1927 and began The Shipmaster (1928) in Odesa; the novel is about the film factory, the city and the sea",
           "敖德萨海边的电影制片厂。尤里·亚诺夫斯基 1926 年春到 1927 年秋在敖德萨电影厂当艺术编辑，并在敖德萨动笔写《船长》（1928）；这部小说写的就是电影厂、这座城市和大海"),
]
lines = [
    Q("ua-mi-1", "misto", "ua-kyiv-river-port", "Part one, chapter I: the steamer nears Kyiv", "第一部第一章：轮船驶近基辅", T_MI,
      raw(T_MI, "Київ! Це те велике місто", "Невже Київ справді близько?"), ["Київ"],
      "Kyiv! That great city where he was going to study and to live. That new thing he had to enter to reach the dream he had cherished so long. Was Kyiv really close?",
      ["Kyiv"],
      "基辅！就是那座大城市，他要到那里去上学、去生活。就是那新的天地，他必须走进去，才能实现他久久怀抱的梦想。难道基辅真的近了？",
      ["基辅"]),
    Q("ua-ti-1", "shadows-of-forgotten-ancestors", "ua-kryvorivnia", "The opening: Ivan's childhood", "开篇：伊万的童年", T_TI,
      raw(T_TI, "Не знати, — чи то вічний шум Черемоша".replace(" — ", "\xa0— ", 1), "на своє бішеня."), ["Черемоша"],
      "Who can tell whether it was the endless roar of the Cheremosh and the laments of the mountain streams that filled the lonely house on the high bare hilltop, or the gloom of the black spruce forests, that frightened the child, but Ivan cried all the time, screamed at night, grew poorly and looked at his mother with such a deep, old and knowing gaze that she turned her eyes away from him in alarm. More than once she even thought with dread that the child was not hers. The midwife had not kept watch at the birth, had not smoked out the house somewhere, had not lit a candle, and a sly she-devil had managed to swap her child for its own devil's brat.",
      ["Cheremosh"],
      "谁也说不清，是切列莫什河永不停息的喧响和山涧的哀诉——它们灌满了高高的光秃山顶上那座孤零零的屋子——还是黑沉沉的云杉林的愁郁，吓着了这孩子；反正伊万总是哭，夜里尖叫，长得不好，看母亲的目光那么深沉、那么老成，叫母亲心慌得避开他的眼睛。她不止一次害怕地想，这孩子不是她的。接生婆生产时没有“守着”，哪儿没有熏一熏屋子，没有点上蜡烛——狡猾的女鬼就趁机把她的孩子换成了自己的小鬼崽。",
      ["切列莫什河"], note=" (no-break spaces before dashes printed as plain spaces)"),
    Q("ua-zb-1", "zakhar-berkut", "ua-tukhlia", "Chapter II, opening", "第二章开头", T_ZB,
      raw(T_ZB, "Стародавнє село Тухля", "годувала своїх жильців достатнім хлібом."), ["Тухля"],
      "The ancient village of Tukhlia was a large mountain settlement with two or three sizeable hamlets, some fifteen hundred souls in all. The village and its hamlets did not lie where Tukhlia lies today, but far higher up among the mountains, in a broad, long valley that is now overgrown with forest and is called the Sunken Valley. In those old times, when our story takes place, the Sunken Valley was not overgrown with forest; on the contrary, it was tilled and fed its people with bread enough.",
      ["Tukhlia"],
      "古老的图赫利亚村是一座很大的山村，带着两三个不小的小村落，一共约有一千五百口人。村子和那些小村落并不在今天图赫利亚所在的地方，而是在高得多的山里，在一条宽阔狭长的山谷中——这山谷如今长满了树林，叫作“塌谷”。在我们这个故事发生的古时候，塌谷并没有长满树林，恰恰相反，它被开垦耕种，叫住在这里的人吃得饱饱的。",
      ["图赫利亚"]),
    Q("ua-cr-1", "chorna-rada", "ua-nizhyn", "Chapter XVI, opening", "第十六章开头", T_CR,
      raw(T_CR, "А Брюховецький тимчасом бенкетував у Ніжені.", "а де горілку п'ють”."), ["Ніжені"],
      "Meanwhile Briukhovetsky was feasting in Nizhyn. In that unhappy hour it truly came about as Halka had said: “Where they shout, there they sing; where they shed blood, there they drink horilka.”",
      ["Nizhyn"],
      "这时候，布留霍韦茨基正在尼任大摆筵席。在那个不幸的时刻，真应了加尔卡的话：“这边在喊，那边在唱；这边流血，那边喝酒。”",
      ["尼任"]),
    b.S("ua-ed-1", "enchanted-desna", "ua-sosnytsia", "The book as a whole", "全书",
        "An autobiographical “film story” that Oleksandr Dovzhenko, born in Sosnytsia in 1894, wrote at the end of his life; it was first printed in 1956, the year he died. It goes back to his childhood in the village by the Desna: the grandfather who liked to sleep on top of the cellar, the house and garden, the meadows and the river, seen with a child's wonder.",
        "这是 1894 年生在索斯尼齐亚的亚历山大·杜甫仁科晚年写的一部自传体“电影小说”，1956 年——他去世的那一年——才第一次刊出。它回到他在杰斯纳河边乡村度过的童年：爱睡在地窖顶上的爷爷，房子和园子，草地和河流，一切都带着孩子的惊奇。",
        ["Sosnytsia"], ["索斯尼齐亚"],
        "https://www.encyclopediaofukraine.com/pages%5CD%5CO%5CDovzhenkoOleksander.htm; https://tarnawsky.artsci.utoronto.ca/elul/English/Dovzhenko/Enchanted-Desna.pdf; https://is.muni.cz/el/phil/podzim2022/UJS302b/um/Dovzenko.pdf?lang=en; https://en.wikipedia.org/wiki/The_Enchanted_Desna"),
    b.S("ua-sm-1", "the-shipmaster", "ua-odesa-film-studio", "The novel as a whole", "全书",
        "Told by To-Ma-Ki, “Comrade Master of Cinema”, a seventy-year-old film man looking back on his youth as an editor and scriptwriter at the Odesa film factory, a portrait of Yanovsky himself. With his friends Sev, a director, and Bohdan, a sailor, he works on a film for which a sailing ship is built; he and Sev compete for the ballerina Taiakh. The carved figurehead of the ship, the shipmaster, stands for the cheerful people building a new culture.",
        "讲述者是“电影大师同志”托-玛-基——一位七十岁的电影人，回忆自己年轻时在敖德萨电影厂当编辑和编剧的日子，原型就是亚诺夫斯基本人。他和朋友——导演谢夫、水手博赫丹——一起拍一部电影，为此造了一艘帆船；他和谢夫都在追求芭蕾舞演员塔亚赫。船头那尊木雕像，就是书名里的“船长”，象征着正在创造新文化的快活的人民。",
        ["Odesa"], ["敖德萨"],
        "https://osvita.ua/test/training/skorocheni-tvory/82516/; https://osvita.ua/test/training/skorocheni-tvory/82517/; https://osvita.ua/school/literature/ya/65156/list-19.html"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_ua2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
