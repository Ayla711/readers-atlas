"""11-24: Nigeria, the 5 books that selection rule v2 adds (tools/selection/ng.md). Scene notes in our own words (all in
copyright). Places, with the reason for each:
- The Famished Road: the unnamed city is most likely a Nigerian one; Azaro's ghetto is taken to be based on the Lagos slum
  where Okri grew up (honest note); line on the existing ng-lagos.
- Americanah: Lagos, where Ifemelu and Obinze fall in love at school and to which she returns as an "Americanah" (the
  word is Lagos slang for those newly back from America); line on the existing ng-lagos.
- The Palm-Wine Drinkard: the drinkard's bush is mythical; Tutuola was born in Abeokuta (village of Wasinmi nearby), so
  the line hangs on the existing Aké, Abeokuta pin (honest note).
- Arrow of God: Umuaro and Okperi are fictional; Achebe based the novel on an incident in Umuchu, recorded in Simon
  Nnolim's History of Umuchu, where a priest named Ezeagu refused a chieftaincy in 1913 and was imprisoned (prototype).
- The Joys of Motherhood: Ibuza (Ibusa, Igbuzo), Nnu Ego's and Emecheta's family hometown, where Nnu Ego dies.
Photos: tools/content/batches/add_photos_ng_1124.py.

Usage: python3 -I tools/content/batches/add_ng2.py <app_dir> tools/content/batches/coords/add_ng2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP = sys.argv[1]
CO = json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines, old_places=()):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    bk = {x["id"] for x in books}
    assert not bk & allb, bk & allb
    have = ids_in(b.data("places.js"))
    assert not {p["id"] for p in places} & have and {p["id"] for p in places} == set(CO)
    assert set(old_places) <= have, set(old_places) - have
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    pl = {p["id"] for p in places} | set(old_places)
    for l in lines:
        assert l["book_id"] in bk and l["place_ids"][0] in pl, l["id"]
    assert {l["book_id"] for l in lines} == bk
    assert {l["place_ids"][0] for l in lines} == pl
def run(books, places, lines, script):
    M = f"11-24: Nigeria, books that selection rule v2 adds (tools/content/batches/{script})"
    for name, xs in (("books.js", books), ("places.js", places), ("lines.js", lines)):
        if xs: b.append(b.data(name), xs, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
b.init(APP, "", "ng", DATE)
books = [
    BK("the-famished-road", "The Famished Road", "饥饿的路", "The Famished Road", "Ben Okri", "本·奥克里", "Ben Okri", "1991", "en",
       ["Azaro", "Madame Koto", "abiku"]),
    BK("arrow-of-god", "Arrow of God", "神箭", "Arrow of God", "Chinua Achebe", "钦努阿·阿契贝", "Chinua Achebe", "1964", "en",
       ["Ezeulu", "Ulu", "Umuaro", "Okperi", "Winterbottom"]),
    BK("americanah", "Americanah", "美国佬", "Americanah", "Chimamanda Ngozi Adichie", "奇玛曼达·恩戈兹·阿迪契", "Chimamanda Ngozi Adichie", "2013", "en",
       ["Ifemelu", "Obinze", "Raceteenth"]),
    BK("palm-wine-drinkard", "The Palm-Wine Drinkard", "棕榈酒鬼", "The Palm-Wine Drinkard", "Amos Tutuola", "阿莫斯·图图奥拉", "Amos Tutuola",
       "1952", "en", ["The Palm-Wine Drinkard and His Dead Palm-Wine Tapster in the Deads' Town", "Deads' Town", "Complete Gentleman"]),
    BK("joys-of-motherhood", "The Joys of Motherhood", "为母之乐", "The Joys of Motherhood", "Buchi Emecheta", "布奇·埃梅切塔", "Buchi Emecheta",
       "1979", "en", ["Nnu Ego", "Nnaife", "Ibuza", "Ibusa"]),
]
places = [
    b.PROTO("ng-umuchu", "Umuchu, Anambra", "乌穆丘，阿南布拉州", *C("ng-umuchu"),
            "the Igbo town whose history gave Chinua Achebe the story of Arrow of God (1964). According to Simon Nnolim's History of Umuchu, a priest named Ezeagu refused a chieftaincy offered by the British in 1913, was imprisoned, and afterwards refused to roast the sacred yams for the months he had missed; the novel's Umuaro and Okperi are fictional",
            "这座伊博小镇的历史给了钦努阿·阿契贝《神箭》（1964）的故事。据西蒙·恩诺利姆的《乌穆丘史》记载，1913 年，一位名叫埃泽阿古的祭司拒绝了英国人给他的酋长职位，被关进牢里，出狱后又拒绝为他错过的那几个月烤食圣薯；小说里的乌穆阿罗和奥克佩里都是虚构的"),
    b.ORIG("ng-ibusa", "Ibuza (Ibusa), Delta State", "伊布扎（伊布萨），三角洲州", *C("ng-ibusa"),
           "Igbo town west of the Niger, the family hometown of Buchi Emecheta and of Nnu Ego, the heroine of The Joys of Motherhood (1979). Nnu Ego is born here, the daughter of the chief Agbadi, leaves for Lagos after a childless first marriage, and comes back at the end of her life to die here alone",
           "尼日尔河西岸的伊博小镇，布奇·埃梅切塔的家族故乡，也是《为母之乐》（1979）的主人公努·埃戈的家乡。努·埃戈生在这里，是酋长阿格巴迪的女儿；第一段婚姻没有孩子，她便去了拉各斯，晚年又回到这里，孤零零地死去"),
]
lines = [
    b.S("ng-fr-1", "the-famished-road", "ng-lagos", "Madame Koto's bar", "科托夫人的酒吧",
        "Azaro is an abiku, a spirit child who is meant to die young and return again and again to the spirit world, but who decides, for his mother's sake, to stay among the living. He lives with his parents in a ghetto compound by a road in an unnamed African city, most likely Nigerian, in the years around independence: his father a labourer and boxer who dreams of politics, his mother a hawker, their rent always owed. Spirits keep trying to call him back, and the forest around the settlement is being cut down. At the centre of it all is the bar of Madame Koto, who thinks Azaro brings her luck, and who grows rich and powerful as the parties of the rich and the poor fight their elections. The novel won the Booker Prize in 1991. (The city is unnamed; the ghetto is taken to be based on the Lagos slum where Okri grew up.)",
        "阿扎罗是个“阿比库”——注定早夭、一次次回到灵界的精灵孩子，可他为了母亲，决定留在人间。独立前后的那些年，他和父母住在一座无名非洲城市（多半是尼日利亚）里一条路边的贫民区大杂院里：父亲是搬运工，也是拳手，梦想着搞政治；母亲沿街叫卖，房租永远欠着。精灵们不停地想把他叫回去，定居点周围的森林正被一片片砍掉。这一切的中心是科托夫人的酒吧——她认为阿扎罗会给她带来好运，而在富人党和穷人党争夺选举的过程中，她越来越有钱有势。这部小说获得 1991 年布克奖。（城市没有名字；人们认为这片贫民区取材于奥克里长大的拉各斯贫民窟。）",
        ["Lagos"], ["拉各斯"],
        "https://en.wikipedia.org/wiki/The_Famished_Road; https://omc.obta.al.uw.edu.pl/myth-survey/item/784; https://www.ebsco.com/research-starters/literature-and-writing/famished-road-and-songs-enchantment-ben-okri; https://www.themodernnovel.org/?p=5552; https://www.encyclopedia.com/arts/culture-magazines/famished-road; https://wiki.angl-am.uni-oldenburg.de/index.php/Ben_Okri,_The_Famished_Road_(1991)"),
    b.S("ng-am-1", "americanah", "ng-lagos", "The Americanah comes home", "“美国佬”回国",
        "As teenagers at a Lagos secondary school under military rule, Ifemelu and Obinze fall in love. When strikes close the university at Nsukka, Ifemelu leaves for America on a scholarship; Obinze, refused a visa after 9/11, goes to London and ends up an undocumented immigrant. In America Ifemelu discovers what it means to be black there and becomes known for her blog, Raceteenth. Years later, with a Princeton fellowship and an American boyfriend behind her, she goes home to Lagos, where her friends tease her as an 'Americanah', Lagos slang for those newly back from the States; she works for a women's magazine, starts a new blog about life in Lagos, and finds Obinze, now a rich property developer with a wife and daughter.",
        "军政府统治下，伊菲麦露和奥宾仔在拉各斯的一所中学里相爱。恩苏卡的大学因罢课停摆，伊菲麦露拿着奖学金去了美国；奥宾仔在“9·11”之后拿不到美国签证，去了伦敦，最后成了非法移民。在美国，伊菲麦露才明白在那里做一个黑人意味着什么，并因博客“种族十年”出了名。多年后，她放下普林斯顿的研究员职位和美国男友，回到拉各斯，朋友们笑她是“美国佬”——拉各斯人对刚从美国回来的人的叫法；她在一家女性杂志工作，又开了一个写拉各斯生活的新博客，也重新找到了奥宾仔，如今他已是有妻有女的富有地产商。",
        ["Lagos"], ["拉各斯"],
        "https://en.wikipedia.org/wiki/Americanah; https://www.penguinrandomhouse.com/books/878/americanah-by-chimamanda-ngozi-adichie/readers-guide/; https://www.litcharts.com/lit/americanah/summary; https://www.supersummary.com/americanah/summary/; https://www.barnesandnoble.com/blog/americanah/; https://www.npr.org/2013/05/15/182313317/coming-to-americanah-two-tales-of-immigrant-experience"),
    b.S("ng-pwd-1", "palm-wine-drinkard", "ng-ake", "The Complete Gentleman", "“完美绅士”",
        "The narrator, a man who has done nothing since boyhood but drink palm wine, loses his expert tapster when the man falls from a palm tree and dies; with no wine, his friends stop coming, and he sets out to find the tapster in the Deads' Town. On the way, through bush and town, he meets a long series of creatures out of Yoruba folktale. In the most famous episode, a beautiful girl who has refused every suitor follows a 'complete gentleman' from the market into the endless forest, where he returns his borrowed limbs and skin to their owners until he is only a skull; the drinkard rescues her and marries her. At last he reaches the Deads' Town, but the tapster cannot return with him and gives him a magic egg instead. (The drinkard's bush is mythical; Tutuola was born in Abeokuta, where this pin stands.)",
        "叙述者从小到大什么都不干，只喝棕榈酒；他那手艺高超的割酒人从棕榈树上摔下来死了，没了酒，朋友们也不再上门，他便出发去“亡者镇”寻找割酒人。一路穿过丛林和城镇，他遇到了一连串来自约鲁巴民间故事的怪物。最有名的一段里，一个拒绝了所有求婚者的美丽姑娘，跟着集市上的一位“完美绅士”走进无边的森林，他一路把借来的四肢和皮肤还给原主，最后只剩下一颗头骨；酒鬼救出姑娘，娶了她。他终于到了亡者镇，可割酒人不能跟他回去，只送了他一枚神奇的蛋。（酒鬼走过的丛林是神话里的；图图奥拉生在阿贝奥库塔，图钉就标在这里。）",
        ["Abeokuta"], ["阿贝奥库塔"],
        "https://en.wikipedia.org/wiki/The_Palm-Wine_Drinkard; https://www.ebsco.com/research-starters/literature-and-writing/palm-wine-drinkard-amos-tutuola; https://www.ebsco.com/research-starters/literature-and-writing/palm-wine-drinkard-analysis-setting; https://journals.lib.unb.ca/index.php/IFR/article/download/13280/14363/17988; https://en.wikipedia.org/wiki/Amos_Tutuola; https://www.britannica.com/biography/Amos-Tutuola"),
    b.S("ng-aog-1", "arrow-of-god", "ng-umuchu", "The sacred yams", "圣薯",
        "Igboland in the 1920s. Ezeulu, chief priest of Ulu, the god of the six villages of Umuaro, bears witness against his own people in a land dispute with neighbouring Okperi, because he will tell the truth to the British district officer, Captain Winterbottom. When Winterbottom, ordered to rule through native chiefs, summons him to make him a warrant chief, Ezeulu refuses and is held for two months at Okperi. Back in Umuaro, he will not name the day of the New Yam Festival until he has eaten the sacred yams for the months he missed, and the harvest rots in the fields while his people go hungry. Many turn to the Christian mission, whose harvest offering lets them gather their yams. (Umuaro and Okperi are fictional; the story comes from Umuchu, where a priest refused a chieftaincy in 1913.)",
        "20 世纪 20 年代的伊博兰。乌卢神是乌穆阿罗六个村子共同供奉的神，乌卢的大祭司埃泽乌卢在乌穆阿罗与邻村奥克佩里的土地纠纷中作证，站在了自己族人的对立面，因为他要对英国区长温特博特姆上尉说真话。温特博特姆奉命通过本地酋长实行统治，召他去当“委任酋长”，埃泽乌卢拒绝了，在奥克佩里被扣押了两个月。回到乌穆阿罗后，他坚持要先把错过那几个月的圣薯吃完，才肯宣布新薯节的日子，于是庄稼烂在地里，族人挨饿。许多人转向了基督教会——教会的丰收献祭让他们可以收获自己的山药。（乌穆阿罗和奥克佩里是虚构的；故事来自乌穆丘，1913 年那里有位祭司拒绝了酋长之职。）",
        ["Umuchu"], ["乌穆丘"],
        "https://en.wikipedia.org/wiki/Arrow_of_God; https://www.ebsco.com/research-starters/literature-and-writing/arrow-god-chinua-achebe; https://www.ebsco.com/research-starters/literature-and-writing/arrow-god-analysis-major-characters; https://cambridge.org/core/books/chinua-achebe/religion-and-power-in-africa-arrow-of-god/403261F8A985C214DDC60156C5E50151; https://www.shmoop.com/study-guides/literature/arrow-of-god/summary; https://www.cse.iitk.ac.in/users/amit/books/achebe-1964-arrow-of-god.html"),
    b.S("ng-jom-1", "joys-of-motherhood", "ng-ibusa", "Nnu Ego's return", "努·埃戈的归来",
        "Nnu Ego, daughter of the great chief Agbadi of Ibuza, is sent back to her father when her first marriage brings no child, and is married off to Nnaife, a servant to a British couple in Lagos, whom she cannot respect. In the city, from the 1930s through the war, she bears child after child, loses some, and wears herself out in poverty to feed and school the sons on whom, she believes, a mother's joy and old age depend; her husband takes a second wife, goes to war and later to prison. In the end her children scatter, her eldest son to America, and she goes home to Ibuza, where one night she lies down by the roadside and dies alone. Her children give her a lavish funeral and build her a shrine; women pray to her for children, but she never answers.",
        "努·埃戈是伊布扎大酋长阿格巴迪的女儿，第一段婚姻没有孩子，她被送回了父亲家，后来又被许配给在拉各斯给一对英国夫妇当用人的纳伊费，一个她看不起的男人。从 20 世纪 30 年代一直到战争年代，她在城里一个接一个地生孩子，有的夭折了，她在贫困中耗尽自己，养活儿子们、供他们上学——她相信，一个母亲的快乐和晚年都系在儿子身上；丈夫娶了第二个妻子，后来上了战场，又进了监狱。最后孩子们各奔东西，长子去了美国，她回到伊布扎，一天夜里躺在路边，孤零零地死去。孩子们为她办了隆重的葬礼，给她修了神龛；女人们向她祈求子嗣，她却从不应答。",
        ["Ibuza"], ["伊布扎"],
        "https://www.supersummary.com/the-joys-of-motherhood/summary; https://www.supersummary.com/the-joys-of-motherhood/chapters-16-18-summary; https://www.shmoop.com/study-guides/joys-of-motherhood/plot-analysis.html; https://www.encyclopedia.com/arts/culture-magazines/joys-motherhood; https://www.encyclopedia.com/social-sciences/encyclopedias-almanacs-transcripts-and-maps/emecheta-buchi-title-commentary; https://ebooks.inflibnet.ac.in/engp06/chapter/buchi-emecheta-the-joys-of-motherhood/"),
]
check(books, places, lines, old_places=["ng-lagos", "ng-ake"])
if __name__ == "__main__":
    run(books, places, lines, "add_ng2.py")
