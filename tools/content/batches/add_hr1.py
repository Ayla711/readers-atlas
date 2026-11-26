"""11-25: Croatia, the books that selection rule v2 adds (tools/selection/hr.md). Croatia opens with this batch.
Seven new books, all in copyright (Ujević's later poems too), so scene notes in our own words; and a Croatian place and
scene for Murder on the Orient Express, whose book entry is already in the Turkey pack (data/tr). Places:
- Zagreb (city-level pin): Cyclops, The Banners, On the Edge of Reason.
- Tin's Tower, Vrgorac (pilgrimage): Ujević's poems name no one place; he was born in the tower (A-24).
- Museum of Peasant Revolts, Gornja Stubica: a key theme of the Ballads is Gubec's revolt of 1573 in Croatian Zagorje.
- Vela Luka, Korčula: Dragojević's poems name no one place; it is his birthplace (A-24).
- Rab town (prototype): the novel's island is unnamed; Novak was bound to Rab all his life.
- Vinkovci: the Orient Express is stopped by snow between Vinkovci and Brod.
Usage: python3 -I tools/content/batches/add_hr1.py <app_dir> tools/content/batches/coords/add_hr1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-25"
b.init(APP, "", "hr", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, year, aliases):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang="hr", public_domain=False, source_url=None, aliases=aliases)

books = [
    BK("kiklop", "Cyclops", "独眼巨人", "Kiklop", "Ranko Marinković", "兰科·马林科维奇", "1965", ["Kiklop", "Melkior Tresić"]),
    BK("zastave", "The Banners", "旗帜", "Zastave", "Miroslav Krleža", "米罗斯拉夫·克尔莱扎", "1976", ["Zastave", "Kamilo Emerički"]),
    BK("ujevic-poems", "Poems", "乌耶维奇诗选", "Pjesme", "Tin Ujević", "蒂恩·乌耶维奇", "1920", ["Lelek sebra", "Kolajna", "Svakidašnja jadikovka"]),
    BK("balade-petrice-kerempuha", "The Ballads of Petrica Kerempuh", "彼特里察·克伦普赫歌谣", "Balade Petrice Kerempuha", "Miroslav Krleža", "米罗斯拉夫·克尔莱扎", "1936",
       ["Balade Petrice Kerempuha", "Petrica Kerempuh"]),
    BK("dragojevic-poems", "Poems", "德拉戈耶维奇诗选", "Pjesme", "Danijel Dragojević", "达尼耶尔·德拉戈耶维奇", "1961", ["Kasno ljeto", "Žamor", "Prirodopis"]),
    BK("mirisi-zlato-i-tamjan", "Gold, Frankincense and Myrrh", "黄金、乳香和没药", "Mirisi, zlato i tamjan", "Slobodan Novak", "斯洛博丹·诺瓦克", "1968",
       ["Mirisi, zlato i tamjan"]),
    BK("na-rubu-pameti", "On the Edge of Reason", "理智的边缘", "Na rubu pameti", "Miroslav Krleža", "米罗斯拉夫·克尔莱扎", "1938", ["Na rubu pameti", "Domaćinski"]),
]

places = [
    b.ORIG("hr-zagreb", "Zagreb", "萨格勒布", *C("hr-zagreb"),
        "The capital of Croatia. Cyclops follows Zagreb's bohemian intellectuals on the eve of the Second World War; The Banners centres on Kamilo Emerički, son of a Zagreb elite family; On the Edge of Reason is the story of a Zagreb lawyer who will not keep quiet",
        "克罗地亚首都。《独眼巨人》写二战前夕萨格勒布的波希米亚知识分子；《旗帜》以萨格勒布上流家庭的儿子卡米洛·埃梅里奇基为中心；《理智的边缘》写一个不肯闭嘴的萨格勒布律师"),
    b.PIL("hr-tinova-kula", "Tin's Tower, Vrgorac", "弗尔戈拉茨的蒂恩塔", *C("hr-tinova-kula"),
        "The largest of the Ottoman towers of Vrgorac, where Tin Ujević was born in 1891. It now hosts cultural events, among them a week of literary events, 'S Tinom u Vrgorcu', around his birthday each July. His poems are not tied to one place, so they are pinned here",
        "弗尔戈拉茨几座奥斯曼时代塔楼中最大的一座，蒂恩·乌耶维奇 1891 年生在这里。如今塔里常办文化活动，每年 7 月他生日前后有为期一周的文学活动“与蒂恩在弗尔戈拉茨”。他的诗不写某一个地方，所以挂在这里",
        ["ujevic-poems"]),
    b.ORIG("hr-peasant-revolts-museum", "Museum of Peasant Revolts, Gornja Stubica", "上斯图比察的农民起义博物馆", *C("hr-peasant-revolts-museum"),
        "The museum of the peasant revolts in Gornja Stubica, in Croatian Zagorje, where the cruelty of Baron Ferenc Tahy towards his serfs set off Matija Gubec's revolt of 1573. Gubec's revolt is one of the key themes of Krleža's Ballads of Petrica Kerempuh",
        "克罗地亚扎戈列地区上斯图比察的农民起义博物馆。正是在扎戈列，塔希男爵对农奴的残暴激起了 1573 年马蒂亚·古贝茨领导的起义。古贝茨起义是克尔莱扎《彼特里察·克伦普赫歌谣》的核心主题之一"),
    b.ORIG("hr-vela-luka", "Vela Luka, Korčula", "科尔丘拉岛的韦拉卢卡", *C("hr-vela-luka"),
        "The harbour town on the island of Korčula where Danijel Dragojević was born in 1934. His poems are not tied to one place, so they are pinned to his birthplace",
        "科尔丘拉岛上的港口小镇，达尼耶尔·德拉戈耶维奇 1934 年生在这里。他的诗不写某一个地方，所以挂在他的出生地"),
    b.PROTO("hr-rab", "Rab", "拉布", *C("hr-rab"),
        "The island of Gold, Frankincense and Myrrh is never named. Slobodan Novak was bound to Rab all his life, felt it to be his island and home, and devoted his best prose to it; the countess of the novel had once owned most of the island",
        "《黄金、乳香和没药》里的岛始终没写名字。斯洛博丹·诺瓦克一生和拉布岛连在一起，把它当作自己的岛和故乡，最好的散文作品都献给了它；小说里的老伯爵夫人从前拥有岛上大部分土地"),
    b.ORIG("hr-vinkovci", "Vinkovci", "温科夫奇", *C("hr-vinkovci"),
        "The railway town in eastern Slavonia beyond which the Orient Express of Agatha Christie's novel is stopped by a snowdrift, between Vinkovci and Brod; the murder and Poirot's investigation take place on the stranded train",
        "斯拉沃尼亚东部的铁路小城。阿加莎·克里斯蒂小说里的东方快车过了温科夫奇，在去布罗德的路上被雪堆挡住；命案和波洛的侦破都发生在这列困在雪里的火车上"),
]

lines = [
    b.S("hr-ki-1", "kiklop", "hr-zagreb", "On the eve of the war", "战争前夕",
        "On the eve of the Second World War the theatre critic Melkior Tresić drifts through the cafés and streets of Zagreb with a crowd of bohemians who drown their fear in drink, affairs and drunken arguments; to escape being called up, he starves himself. The Cyclops of the title is the war itself, the one-eyed giant who rolls a boulder across the mouth of the cave and traps everyone inside. The novel ends with the animals of a zoo shrieking in terror as the first bombs fall on the city.",
        "第二次世界大战前夕，戏剧评论家梅尔基奥尔·特雷西奇和一群波希米亚文人在萨格勒布的咖啡馆和街头游荡，他们靠喝酒、偷情和醉后争吵压住心里的恐惧；为了逃避征兵，他故意让自己挨饿。书名里的独眼巨人就是战争本身，那个推巨石堵住洞口、把所有人困在里面的巨人。小说结尾，第一批炸弹落在城里，动物园里的野兽吓得发疯般嘶叫。",
        ["Zagreb"], ["萨格勒布"], "https://hr.wikipedia.org/wiki/Kiklop_(roman); https://arhiva.nacional.hr/clanak/12956/20-knjiga-koje-bi-trebao-procitati-svaki-hrvat"),
    b.S("hr-za-1", "zastave", "hr-zagreb", "Kamilo's education", "卡米洛的成长",
        "Kamilo Emerički, son of a Zagreb elite family, grows up through the first third of the twentieth century: the bomb affair of 1904, his studies in Pest from 1906, his love for Ana and his engagement to Jolanda, then the war, in which he is badly wounded in a munitions explosion and at the battle of Gródek. Through his quarrels with his father and his friendship with the anarchist Joja Žigman, Krleža follows the national politics of Croatia, Hungary and Serbia, the fall of Austria-Hungary, and Kamilo's slow political awakening.",
        "卡米洛·埃梅里奇基出身萨格勒布的上流家庭，跟着 20 世纪的前三十年长大：1904 年的炸弹案，1906 年起在佩斯求学，对安娜的爱和与约兰达的订婚，接着是战争，他在一次弹药爆炸和格鲁德克战役中两次重伤。克尔莱扎借他和父亲的争执、和无政府主义者约亚·日格曼的友谊，写克罗地亚、匈牙利和塞尔维亚的民族政治、奥匈帝国的崩溃，以及卡米洛一点点成熟的政治觉悟。",
        ["Zagreb"], ["萨格勒布"], "https://hr.wikipedia.org/wiki/Zastave_(roman)"),
    b.S("hr-nr-1", "na-rubu-pameti", "hr-zagreb", "The party", "那场宴会",
        "An unnamed doctor of law in Zagreb has lived a dull, respectable life. At a party among the city's upper class, the director-general Domaćinski tells, as an amusing story, how he shot four men for trespassing on his land. The narrator does not keep quiet: he tells Domaćinski what he thinks of it. Shunned by the society he belonged to, he is taken to court for slander and ends up in prison.",
        "萨格勒布一个没有名字的法学博士，一直过着平淡体面的日子。在一场上流社会的宴会上，总经理多马钦斯基把自己开枪打死四个擅闯他土地的人当作趣事来讲。叙述者没有沉默，当面说出了他对这件事的看法。他被自己原本所属的那个圈子排斥，以诽谤罪被告上法庭，最后进了监狱。",
        ["Zagreb"], ["萨格勒布"], "https://en.wikipedia.org/wiki/On_the_Edge_of_Reason; https://hr.wikipedia.org/wiki/Na_rubu_pameti"),
    b.S("hr-uj-1", "ujevic-poems", "hr-tinova-kula", "Everyday Lament", "日常的哀歌",
        "Tin Ujević was born in 1891 in this tower in Vrgorac and lived here for his first six years, before his family moved to Imotski and then Makarska. In his poems he gave voice to a strong sense of personal tragedy, most famously in 'Svakidašnja jadikovka' (Everyday Lament), wrote of a spiritual, unbodily love in Kolajna, and sang hymns to work and human brotherhood. The poems name no one place, so they are pinned to his birthplace in Vrgorac.",
        "蒂恩·乌耶维奇 1891 年生在弗尔戈拉茨的这座塔里，在这里住到六岁，后来全家搬去伊莫茨基，又搬到马卡尔斯卡。他的诗写出强烈的个人悲剧感，最有名的是《日常的哀歌》；在《项链》里写精神上的、不沾肉身的爱；也写过歌颂劳动和人类兄弟情谊的颂歌。这些诗不写某一个地方，所以挂在他的出生地弗尔戈拉茨。",
        ["Vrgorac"], ["弗尔戈拉茨"], "https://hr.wikipedia.org/wiki/Tin_Ujević; https://hr.wikipedia.org/wiki/Tinova_kula"),
    b.S("hr-bk-1", "balade-petrice-kerempuha", "hr-peasant-revolts-museum", "Gubec's revolt", "古贝茨起义",
        "Krleža's ballads are spoken by Petrica Kerempuh, a folk prophet and cynical commentator on his times, in a Kajkavian idiom that Krleža built from old texts and dialects rather than any one spoken speech. Their key themes are Gubec's peasant revolt of 1573, the Ottoman raids on Croatian lands, and the martyrdom of the common people under their lords, told with the gallows humour of the poor. The revolt rose in Croatian Zagorje; the museum of the peasant revolts stands in Gornja Stubica.",
        "克尔莱扎的这部歌谣集借彼特里察·克伦普赫之口说出，他是民间的先知，也是冷嘲热讽的时事评论者；诗用的卡伊卡夫方言是克尔莱扎从古籍和各地方言里拼出来的，并不是哪一种真正有人说的话。诗集的核心主题是 1573 年古贝茨农民起义、奥斯曼人对克罗地亚的劫掠，以及老百姓在领主手下受的苦难，通篇是穷人的“绞架下的幽默”。起义发生在克罗地亚的扎戈列地区；农民起义博物馆就在上斯图比察。",
        ["Gornja Stubica"], ["上斯图比察"], "https://hr.wikipedia.org/wiki/Balade_Petrice_Kerempuha; https://hr.wikipedia.org/wiki/Petrica_Kerempuh; https://en.wikipedia.org/wiki/Croatian–Slovene_Peasant_Revolt; https://arhiva.nacional.hr/clanak/12956/20-knjiga-koje-bi-trebao-procitati-svaki-hrvat"),
    b.S("hr-dr-1", "dragojevic-poems", "hr-vela-luka", "Poetry of the eye", "眼睛的诗",
        "Danijel Dragojević was born in 1934 in Vela Luka on the island of Korčula, went to school in Dubrovnik and studied art history in Zagreb, where for decades he edited programmes for the Third Programme of Croatian Radio. His quiet poetry of small events and things, sometimes called a poetry of the eye, grew apart from every trend of its time and became a model for younger Croatian poets. The poems name no one place, so they are pinned to his birthplace, Vela Luka.",
        "达尼耶尔·德拉戈耶维奇 1934 年生在科尔丘拉岛的韦拉卢卡，在杜布罗夫尼克读完中学，在萨格勒布学艺术史，后来几十年在克罗地亚广播电台第三套节目当编辑。他的诗安静地写小事和小物件，有人称之为“眼睛的诗”，不随任何潮流，成了年轻一代克罗地亚诗人的榜样。这些诗不写某一个地方，所以挂在他的出生地韦拉卢卡。",
        ["Vela Luka"], ["韦拉卢卡"], "https://hr.wikipedia.org/wiki/Danijel_Dragojević; https://arhiva.nacional.hr/clanak/12956/20-knjiga-koje-bi-trebao-procitati-svaki-hrvat"),
    b.S("hr-mz-1", "mirisi-zlato-i-tamjan", "hr-rab", "Christmas to Epiphany", "从圣诞夜到主显节",
        "From Christmas Eve to Epiphany, on an Adriatic island the novel never names, Mali, a retired intellectual and an invalid of the Second World War, and his wife Draga nurse old Madona, a countess who once owned most of the island. In long monologues Mali settles his accounts with both Communist and Catholic ideology, having lost his faith and every illusion. Slobodan Novak, who wrote it, was bound all his life to the island of Rab.",
        "从圣诞夜到主显节，在小说始终没写名字的一座亚得里亚海岛上，退休的知识分子、二战伤残军人“小个子”和妻子德拉加照料着年迈的玛多娜，她是位伯爵夫人，从前拥有岛上大部分土地。“小个子”在漫长的独白里同共产主义和天主教两种意识形态算账，他已经失去了信仰，也失去了一切幻想。作者斯洛博丹·诺瓦克一生都和拉布岛连在一起。",
        ["Rab"], ["拉布"], "https://hr.wikipedia.org/wiki/Mirisi,_zlato_i_tamjan_(roman); https://www.novilist.hr/?p=1326907"),
    b.S("hr-oe-1", "murder-on-the-orient-express", "hr-vinkovci", "The snowdrift", "雪堆",
        "Beyond Vinkovci the Orient Express runs into a snowdrift and stops. In the night Poirot hears a cry from the next compartment and sees a woman in a scarlet kimono in the corridor. In the morning Bouc tells him that the American Ratchett has been murdered, stabbed twelve times, and that the murderer must still be on board, since no one could have escaped through the snow. With the train stranded between Vinkovci and Brod, Poirot questions the passengers of the Calais coach one by one.",
        "列车过了温科夫奇，撞进雪堆停了下来。夜里，波洛听见隔壁包厢一声叫喊，又看见走廊里有个穿猩红色和服的女人。早上，布克告诉他美国人雷切特被人杀了，身中十二刀，凶手一定还在车上，因为大雪里谁也逃不出去。列车困在温科夫奇和布罗德之间，波洛把加来车厢的乘客一个个叫来问话。",
        ["Vinkovci"], ["温科夫奇"], "https://en.wikipedia.org/wiki/Murder_on_the_Orient_Express"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places}
assert not new_b & all_books, new_b & all_books
assert "murder-on-the-orient-express" in all_books
assert new_p == set(CO), new_p ^ set(CO)
known = new_b | {"murder-on-the-orient-express"}
for l in lines:
    assert l["book_id"] in known and l["place_ids"][0] in new_p, l["id"]
assert {l["book_id"] for l in lines} == known and {l["place_ids"][0] for l in lines} == new_p

HEAD = "// Croatia, hand-written content (tools/content/batches/add_hr1.py, 2026-11-25).\n"
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
