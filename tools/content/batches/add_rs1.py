"""11-25: Serbia, the 5 books that selection rule v2 adds (tools/selection/rs.md). Serbia opens with this batch. All
five books are in copyright: scene notes in our own words. Places, with the reason for each:
- Roots: Prerovo, the novel's village, is fictional. Studies of Dobrica Ćosić trace many motifs and prototypes in his
  novels to his Morava homeland, so the book is pinned to his birthplace, Velika Drenova on the West Morava (A-24).
- Dictionary of the Khazars: the novel has no scene in Serbia (the Khazar kaghanate, seventeenth-century Constantinople,
  scholars in 1982). Following A-24 it is pinned to the monument to Milorad Pavić in Tašmajdan Park, Belgrade (2011).
- The Use of Man: Novi Sad, on the eve of the Second World War and under occupation.
- My Family's Role in the World Revolution, At the Lucky Hand: Belgrade (one city-level pin for both).
Under China's standard map (decision A-22) Kosovo is a region of Serbia (tools/countries.json, pov_units).
Usage: python3 -I tools/content/batches/add_rs1.py <app_dir> tools/content/batches/coords/add_rs1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-25"
b.init(APP, "", "rs", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, year, aliases):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang="sh", public_domain=False, source_url=None, aliases=aliases)

books = [
    BK("koreni", "Roots", "根", "Koreni", "Dobrica Ćosić", "多布里察·乔西奇", "1954", ["Koreni", "Корени"]),
    BK("dictionary-of-the-khazars", "Dictionary of the Khazars", "哈扎尔辞典", "Hazarski rečnik", "Milorad Pavić", "米洛拉德·帕维奇", "1984",
       ["Hazarski rečnik", "Хазарски речник"]),
    BK("the-use-of-man", "The Use of Man", "人的用途", "Upotreba čoveka", "Aleksandar Tišma", "亚历山大·蒂什马", "1976",
       ["Upotreba čoveka", "Употреба човека"]),
    BK("my-familys-role-in-the-world-revolution", "My Family's Role in the World Revolution", "我家在世界革命中的角色",
       "Uloga moje porodice u svetskoj revoluciji", "Bora Ćosić", "博拉·乔西奇", "1969",
       ["Uloga moje porodice u svetskoj revoluciji", "Улога моје породице у светској револуцији"]),
    BK("at-the-lucky-hand", "At the Lucky Hand", "“好运手”杂货铺", "Sitničarnica „Kod srećne ruke”", "Goran Petrović", "戈兰·彼得罗维奇", "2000",
       ["Sitničarnica kod srećne ruke", "Ситничарница „Код срећне руке”", "Sixty-Nine Drawers"]),
]

places = [
    b.ORIG("rs-velika-drenova", "Velika Drenova", "大德雷诺瓦", *C("rs-velika-drenova"),
        "Dobrica Ćosić's birthplace, a village of vine growers on the West Morava near Trstenik. Prerovo, the village of Roots, is fictional: in the novel a deserter reaches it by crossing the Morava, and studies of Ćosić trace many motifs and prototypes in his novels to this Morava homeland, so the book is pinned here",
        "多布里察·乔西奇的出生地，特尔斯泰尼克附近西摩拉瓦河边一个以培育葡萄苗出名的村子。《根》里的普雷罗沃村是虚构的：小说里一个逃兵渡过摩拉瓦河来到村里；研究乔西奇的文章说，他小说里的许多题材和原型出自这片摩拉瓦河谷家乡，所以把这本书挂在这里"),
    b.PIL("rs-pavic-monument", "Monument to Milorad Pavić, Tašmajdan Park", "塔什马伊丹公园的帕维奇纪念碑", *C("rs-pavic-monument"),
        "A three-metre bronze monument to Milorad Pavić in Tašmajdan Park, Belgrade, unveiled on 8 June 2011, by the Baku sculptor Natig Aliyev. Pavić was born and died in Belgrade. His Dictionary of the Khazars has no scene set in Serbia, so the book is pinned here",
        "贝尔格莱德塔什马伊丹公园里米洛拉德·帕维奇的青铜纪念碑，高三米，2011 年 6 月 8 日揭幕，作者是巴库的雕塑家纳蒂格·阿利耶夫。帕维奇生于贝尔格莱德，也死在这里。他的《哈扎尔辞典》没有写塞尔维亚的场景，所以把这本书挂在这里",
        ["dictionary-of-the-khazars"]),
    b.ORIG("rs-novi-sad", "Novi Sad", "诺维萨德", *C("rs-novi-sad"),
        "The city on the Danube where The Use of Man is set, on the eve of the Second World War and through the occupation",
        "多瑙河边的城市，《人的用途》的故事发生在这里，从二战前夕一直写到占领时期"),
    b.ORIG("rs-belgrade", "Belgrade", "贝尔格莱德", *C("rs-belgrade"),
        "The capital, where the Sava meets the Danube. My Family's Role in the World Revolution is set here during the German occupation and after the war; At the Lucky Hand follows a Belgrade student, Adam",
        "塞尔维亚首都，萨瓦河在这里汇入多瑙河。《我家在世界革命中的角色》写的是德国占领时期和战后的贝尔格莱德；《“好运手”杂货铺》的主人公亚当是贝尔格莱德的大学生"),
]

lines = [
    b.S("rs-ko-1", "koreni", "rs-velika-drenova", "Christmas Eve, 1899", "1899 年的圣诞夜",
        "On Christmas Eve 1899 Vukašin Katić comes home to Prerovo after studying in Paris and three years' work in Belgrade, with the news that he will marry Olga Tošić, daughter of his father's fiercest political rival, a Liberal. Aćim Katić, Radical leader of the village, disowns him and makes his elder son Đorđe pay Vukašin his share of the inheritance, five hundred ducats; Đorđe, bitter that the money he worked for goes to his father's favourite, hands over only three hundred. Childless, Đorđe blames his wife Simka, and the question of who fathers the Katić heir runs through the rest of the novel.",
        "1899 年的圣诞夜，武卡辛·卡蒂奇在巴黎读完书、又在贝尔格莱德工作了三年，回到普雷罗沃，带回的消息是他要娶奥尔加·托希奇，她父亲是武卡辛父亲最大的政敌、自由党人。村里的激进党首领阿奇姆·卡蒂奇不认这个儿子，逼大儿子焦尔杰把五百杜卡特的家产分给武卡辛；焦尔杰气不过自己辛苦挣的钱给了父亲偏爱的弟弟，只给了三百。焦尔杰没有孩子，怪罪妻子西姆卡；卡蒂奇家的继承人究竟是谁的孩子，成了后面整部小说的心结。",
        ["Prerovo"], ["普雷罗沃"], "https://sr.wikipedia.org/wiki/Корени_(роман)"),
    b.S("rs-dk-1", "dictionary-of-the-khazars", "rs-pavic-monument", "The Khazar polemic", "哈扎尔论辩",
        "The Khazar kaghan has a dream and summons three sages, a Christian, a Muslim and a Jew, to interpret it: the Khazars will take the faith of whoever explains it best. Pavić tells the debate three times, in a red Christian, a green Islamic and a yellow Hebrew book, as dictionary entries the reader may take in any order, and threads through them the seventeenth-century compilers of an earlier Khazar dictionary and three scholars whose paths cross in 1982. The novel has no scene in Serbia; it is pinned to the monument to Pavić in Belgrade, the city where he was born and died.",
        "哈扎尔可汗做了一个梦，召来三位智者——一个基督徒、一个穆斯林、一个犹太人——为他解梦：谁解得最好，哈扎尔人就皈依谁的宗教。帕维奇把这场论辩讲了三遍，分成红色的基督教之书、绿色的伊斯兰教之书和黄色的希伯来之书，写成可以按任意顺序读的辞典条目，其间穿插 17 世纪编过一部哈扎尔辞典的三个人，以及 1982 年命运交错的三位学者。小说里没有塞尔维亚的场景；这里挂在贝尔格莱德的帕维奇纪念碑上，他生在这座城市，也死在这里。",
        ["Belgrade"], ["贝尔格莱德"], "https://en.wikipedia.org/wiki/Dictionary_of_the_Khazars; https://sr.wikipedia.org/wiki/Хазарски_речник; https://sr.wikipedia.org/wiki/Споменик_Милораду_Павићу_у_Београду"),
    b.S("rs-um-1", "the-use-of-man", "rs-novi-sad", "Fräulein's diary", "“小姐”的日记",
        "In 1940 Ana Drentvešek, a German teacher her pupils call Fräulein, dies in hospital after a gall-bladder operation, in her forty-first year. Before she dies she asks her pupil Vera to go to her flat and burn her diary. The novel follows three young people from her German lessons in Novi Sad: Vera Kroner, of Jewish and German descent; her boyfriend Milinko Božić, a poor Serbian boy who collects encyclopaedias; and Sredoje Lazukić, a rich man's son who gambles away his father's money. Then the war comes, with the persecution of the Jews and the crimes of the Hungarian occupiers.",
        "1940 年，学生们叫她“小姐”的德语老师安娜·德伦特韦舍克做完胆囊手术后死在医院，那年她四十一岁。临死前，她托学生薇拉去她家把日记烧掉。小说跟着在诺维萨德上过她德语课的三个年轻人往下写：有犹太和德国血统的薇拉·克罗纳；薇拉的男朋友、爱买百科全书的穷苦塞尔维亚少年米林科·博日奇；还有挥霍父亲钱财、爱赌博的富家子斯雷多耶·拉祖基奇。接着战争来了，犹太人遭到迫害，匈牙利占领者犯下罪行。",
        ["Novi Sad"], ["诺维萨德"], "https://sr.wikipedia.org/wiki/Употреба_човека"),
    b.S("rs-fr-1", "my-familys-role-in-the-world-revolution", "rs-belgrade", "Occupied Belgrade", "被占领的贝尔格莱德",
        "A small boy tells the story of his family in Belgrade under German occupation: a mother forever predicting disaster, a father who is never sober, two young aunts in love with Hollywood stars and an uncle who chases women, all looking for any work they can do from home. When the war ends the same household tries, comically and not very well, to turn into good Communists in Tito's new order.",
        "一个小男孩讲他家在德国占领下的贝尔格莱德怎么过日子：总在预言大祸临头的母亲，从来没清醒过的父亲，迷恋好莱坞明星的两个年轻姨妈，还有一个到处追女人的舅舅，一家人到处找能在家里做的活计。战争结束，这一家人又手忙脚乱、滑稽地想在铁托的新秩序里变成合格的共产党人。",
        ["Belgrade"], ["贝尔格莱德"], "https://suhrkamp.de/rights/book/bora-cosic-my-family-s-role-in-the-world-revolution-fr-9783518399224; https://en.wikipedia.org/wiki/Bora_Ćosić; https://www.kirkusreviews.com/book-reviews/a/bora-osi/my-familys-role-in-the-world-revolution-and-oth"),
    b.S("rs-lh-1", "at-the-lucky-hand", "rs-belgrade", "Reading as a door", "读书是一扇门",
        "Adam, a student in Belgrade, is offered an odd job: to revise a book that came out ten years earlier. As he reads it, he finds himself inside the novel, where he meets other readers with the same gift of stepping into the story, and not all of them are there with innocent intentions.",
        "贝尔格莱德的大学生亚当接到一份怪差事：修订一本十年前出版的书。读着读着，他发现自己走进了小说里，在那儿遇到了别的读者，他们也有走进故事的本事，而且并不都怀着单纯的心思。",
        ["Belgrade"], ["贝尔格莱德"], "https://database.traduki.eu/publications/sitnicarnica-kod-srecne-ruke-2/"),
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

HEAD = "// Serbia, hand-written content (tools/content/batches/add_rs1.py, 2026-11-25).\n"
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
