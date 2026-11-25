"""11-24: New Zealand, the 13 books that selection rule v2 adds (tools/selection/nz.md).
Scene notes in our own words (all in copyright). Places, with the reason for each:
- Plumb: the trilogy is largely set in Henderson, West Auckland, where Gee grew up (Wikipedia, Oxford Companion); the
  family's house there is Peacehaven; the trilogy's Loomis corresponds to Henderson (New Zealand Books) (prototype).
- An Autobiography (Janet Frame): line on the existing nz-oamaru (56 Eden Street, Oamaru).
- Once Were Warriors: Pine Block is "a fictionalised version of Fordlands in Rotorua" (Te Ara); Duff: "Fordlands, as it's
  known now, was Pine Block in the novel" (Rotorua Daily Post, 2014) (prototype).
- Potiki: "a coastal community resembling Hongoeka, Grace's hometown" (Wikipedia) (prototype).
- Can You Tolerate This?: Te Kūiti, where Young grew up; the essay "The Te Kūiti Underground".
- Smith's Dream: Smith lives alone on an island off the Coromandel (Sunday Star-Times, 2021); the pin is the peninsula.
- Other Halves and The 10pm Question share a city-level pin on Christchurch, each with an honest note:
  Other Halves: a reader's review says the novel opens with Liz phoning an institution in 1970s Christchurch (not checked
  against the text; the 1984 film moved the story to Auckland). The 10pm Question: the city is never named; De Goldi
  "sets all her novels" in Christchurch, where she grew up (Christchurch City Libraries, WORD Christchurch 2022).
- Pounamu Pounamu: Waituhi; Ihimaera's stories are set in a fictional recreation of it (Wikipedia) (prototype).
- Tu: Wellington, where the family moves (city-level pin).
- Season of the Jew: Matawhero, Poverty Bay, attacked by Te Kooti on 10 November 1868, where the narrative begins.
  Matawhero has no English Wikipedia article and the Māori one has no coordinates, so the pin uses Wikidata Q25660807.
- Under the Mountain: Lake Pupuke, where the twins stay.
- The Changeover: Gardendale is Mahy's name for Bishopdale, Christchurch (Wikipedia) (prototype).
Photos: tools/content/batches/add_photos_nz_1124.py.

Usage: python3 -I tools/content/batches/add_nz2.py <app_dir> tools/content/batches/coords/add_nz2.json"""
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
    """every book has a line; every new place and every listed old place has a line"""
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
    M = f"11-24: New Zealand, books that selection rule v2 adds (tools/content/batches/{script})"
    for name, xs in (("books.js", books), ("places.js", places), ("lines.js", lines)):
        if xs: b.append(b.data(name), xs, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
b.init(APP, "", "nz", DATE)
books = [
    BK("plumb", "Plumb", "普拉姆", "Plumb", "Maurice Gee", "莫里斯·吉", "Maurice Gee", "1978", "en",
       ["George Plumb", "Plumb trilogy", "Peacehaven", "Loomis"]),
    BK("frame-autobiography", "An Autobiography", "珍妮特·弗雷姆自传", "An Autobiography", "Janet Frame", "珍妮特·弗雷姆", "Janet Frame",
       "1982–1985", "en", ["To the Is-Land", "An Angel at My Table", "The Envoy from Mirror City", "Eden Street"]),
    BK("once-were-warriors", "Once Were Warriors", "昔日勇士", "Once Were Warriors", "Alan Duff", "艾伦·达夫", "Alan Duff", "1990", "en",
       ["Beth Heke", "Jake Heke", "Jake the Muss", "Pine Block", "Two Lakes"]),
    BK("potiki", "Potiki", "波提基", "Potiki", "Patricia Grace", "帕特里夏·格雷斯", "Patricia Grace", "1986", "en",
       ["Toko", "Roimata", "Hemi"]),
    BK("can-you-tolerate-this", "Can You Tolerate This?", "你能忍受这个吗？", "Can You Tolerate This?", "Ashleigh Young", "阿什莉·扬",
       "Ashleigh Young", "2016", "en", ["Can You Tolerate This", "The Te Kūiti Underground", "Big Red"]),
    BK("smiths-dream", "Smith's Dream", "史密斯的梦", "Smith's Dream", "C. K. Stead", "C. K. 斯特德", "C. K. Stead", "1971", "en",
       ["Smith", "Volkner", "Sleeping Dogs"]),
    BK("other-halves", "Other Halves", "另一半", "Other Halves", "Sue McCauley", "休·麦考利", "Sue McCauley", "1982", "en",
       ["Liz", "Tug"]),
    BK("the-10pm-question", "The 10pm Question", "晚上十点的问题", "The 10pm Question", "Kate De Goldi", "凯特·德戈尔迪", "Kate De Goldi",
       "2008", "en", ["The 10 P.M. Question", "Frankie Parsons", "Sydney", "Gigs"]),
    BK("pounamu-pounamu", "Pounamu Pounamu", "绿玉，绿玉", "Pounamu Pounamu", "Witi Ihimaera", "威蒂·伊希马埃拉", "Witi Ihimaera", "1972", "en",
       ["Pounamu, Pounamu", "A Game of Cards", "Waituhi"]),
    BK("tu-grace", "Tu", "图", "Tu", "Patricia Grace", "帕特里夏·格雷斯", "Patricia Grace", "2004", "en",
       ["Te Hokowhitu-a-Tu", "Pita", "Rangi", "Maori Battalion", "Māori Battalion"]),
    BK("season-of-the-jew", "Season of the Jew", "犹太人的季节", "Season of the Jew", "Maurice Shadbolt", "莫里斯·沙德博尔特",
       "Maurice Shadbolt", "1987", "en", ["George Fairweather", "Te Kooti", "Kooti", "Poverty Bay"]),
    BK("under-the-mountain", "Under the Mountain", "山下", "Under the Mountain", "Maurice Gee", "莫里斯·吉", "Maurice Gee", "1979", "en",
       ["Rachel Matheson", "Theo Matheson", "the Wilberforces", "Mr Jones"]),
    BK("the-changeover", "The Changeover", "蜕变", "The Changeover: A Supernatural Romance", "Margaret Mahy", "玛格丽特·马希",
       "Margaret Mahy", "1984", "en", ["Laura Chant", "Carmody Braque", "Sorensen Carlisle", "Gardendale", "Jacko"]),
]
places = [
    b.PROTO("nz-henderson", "Henderson, Auckland", "亨德森，奥克兰", *C("nz-henderson"),
            "the West Auckland town where Maurice Gee grew up, on which his Plumb trilogy (1978–1983) is largely set. In Plumb the old minister George Plumb moves his family north to this quiet country town and makes a home in a house called Peacehaven; in the trilogy the town appears as Loomis",
            "西奥克兰的小镇，莫里斯·吉在这里长大，他的“普拉姆三部曲”（1978–1983）大部分就以这里为背景。在《普拉姆》里，年迈的牧师乔治·普拉姆把一家人迁到北边这个安静的乡下小镇，在一座叫“和平居”的房子里安了家；三部曲里，这个小镇叫“卢米斯”"),
    b.PROTO("nz-fordlands", "Fordlands, Rotorua", "福德兰兹，罗托鲁阿", *C("nz-fordlands"),
            "the state-housing suburb of Rotorua, once called Ford Block, that Alan Duff turned into Pine Block, the bleak subdivision of Once Were Warriors (1990), on the edge of the town of Two Lakes (Rotorua means 'two lakes'). Duff has said he did not grow up there but knew it from relatives' homes; Lee Tamahori's 1994 film moved the story to South Auckland",
            "罗托鲁阿的国宅区，旧称“福德街区”。艾伦·达夫把它写成了《昔日勇士》（1990）里那片荒凉的“松林街区”，在“双湖镇”的边上（罗托鲁阿在毛利语里就是“两个湖”）。达夫说他不是在那里长大的，但常去亲戚家，很清楚那里的日子；李·塔玛霍里 1994 年的电影把故事搬到了南奥克兰"),
    b.PROTO("nz-hongoeka", "Hongoeka Bay", "洪戈埃卡湾", *C("nz-hongoeka"),
            "the Māori coastal settlement near Plimmerton, north of Wellington, where Patricia Grace's home marae stands; she lives close by on ancestral land. Her novel Potiki (1986) is set in a coastal community resembling Hongoeka",
            "惠灵顿以北、普利默顿附近的毛利海边聚落，帕特里夏·格雷斯所属的会堂就在这里，她本人就住在附近祖传的土地上。她的小说《波提基》（1986）写的海边社区，就像洪戈埃卡"),
    b.ORIG("nz-te-kuiti", "Te Kūiti", "蒂库伊蒂", *C("nz-te-kuiti"),
           "King Country town where Ashleigh Young was born in 1983 and grew up. Her essay collection Can You Tolerate This? (2016), which won her a Windham-Campbell Prize, keeps going back to it, above all in 'The Te Kūiti Underground', about a shy teenager among the town's grey hills",
           "国王乡的小镇，阿什莉·扬 1983 年生在这里，也在这里长大。她获温德姆-坎贝尔奖的散文集《你能忍受这个吗？》（2016）一次次回到这里，最集中的是《蒂库伊蒂地下》——写一个害羞的少女和小镇灰蒙蒙的山"),
    b.ORIG("nz-coromandel", "Coromandel Peninsula", "科罗曼德尔半岛", *C("nz-coromandel"),
           "Peninsula across the Hauraki Gulf from Auckland. In C. K. Stead's Smith's Dream (1971), Smith leaves his broken marriage for a life alone on a small island off the Coromandel, and is pulled from there into a war between a dictatorship and guerrillas. The novel was filmed as Sleeping Dogs (1977). The pin is the peninsula's point",
           "隔着豪拉基湾与奥克兰相望的半岛。C. K. 斯特德的《史密斯的梦》（1971）里，史密斯婚姻破裂，躲到科罗曼德尔外海的一个小岛上独自过活，却从那里被卷进独裁政权和游击队之间的战争。这部小说被拍成了电影《沉睡的狗》（1977）。图钉标在半岛的中心点"),
    b.ORIG("nz-christchurch", "Christchurch", "克赖斯特彻奇", *C("nz-christchurch"),
           "South Island city, pinned here for two novels. Kate De Goldi, who grew up in Christchurch, has said she sets all her novels in it, though in The 10pm Question (2008) the city is never named. In Sue McCauley's Other Halves (1982), by a reader's account, Liz's story opens with a phone call to an institution in 1970s Christchurch; we could not check this against the text, and the 1984 film set the story in Auckland. The pin is the city's point",
           "南岛的城市，这里为两部小说标了图钉。在克赖斯特彻奇长大的凯特·德戈尔迪说，她所有的小说都设在这座城市，虽然《晚上十点的问题》（2008）里从没提过城市的名字。休·麦考利的《另一半》（1982），据一位读者的书评，开篇就是莉兹给 20 世纪 70 年代克赖斯特彻奇的一家机构打电话；我们没能对照原文核实，1984 年的电影则把故事放在了奥克兰。图钉标在市中心点"),
    b.PROTO("nz-waituhi", "Waituhi", "怀图希", *C("nz-waituhi"),
            "the small Māori settlement west of Gisborne where Witi Ihimaera grew up and where his family marae, Te Rongopai, stands. Many of his stories, from his first book, Pounamu Pounamu (1972), on, are set in an imagined recreation of it",
            "吉斯本以西的毛利小聚落，威蒂·伊希马埃拉在这里长大，他家族的会堂“特隆戈派”也在这里。从第一本书《绿玉，绿玉》（1972）起，他的许多故事都设在一个按想象重建的怀图希"),
    b.ORIG("nz-wellington", "Wellington", "惠灵顿", *C("nz-wellington"),
           "New Zealand's capital. In Patricia Grace's Tu (2004), the three Māori brothers Pita, Rangi and Tu move here with their mother and sisters after their father's death; the novel moves between their life in early-1940s Wellington and the 28th (Māori) Battalion in Italy. The pin is the city's point",
           "新西兰的首都。帕特里夏·格雷斯的《图》（2004）里，毛利三兄弟皮塔、兰吉和图在父亲去世后，跟着母亲和姐妹搬到这里；小说在 20 世纪 40 年代初的惠灵顿生活与意大利战场上的第 28（毛利）营之间来回切换。图钉标在市中心点"),
    b.ORIG("nz-matawhero", "Matawhero, Poverty Bay", "马塔怀罗，贫穷湾", *C("nz-matawhero"),
           "Farming district just west of Gisborne. On 10 November 1868 Te Kooti's forces fell on the settlers here, the start of the year of war through which Maurice Shadbolt's Season of the Jew (1987) follows Captain George Fairweather. Matawhero has no English Wikipedia article, so the pin uses Wikidata's coordinates for the locality",
           "吉斯本西边的农业区。1868 年 11 月 10 日，特库蒂的人马在这里袭击了移民，莫里斯·沙德博尔特《犹太人的季节》（1987）跟着乔治·费尔韦瑟上尉走过的那一年战争，就从这一天开始。马塔怀罗没有英文维基百科条目，图钉用的是维基数据给这个地方的坐标"),
    b.ORIG("nz-lake-pupuke", "Lake Pupuke", "普普克湖", *C("nz-lake-pupuke"),
           "Freshwater lake in a volcanic explosion crater beside Takapuna, on Auckland's North Shore. In Maurice Gee's Under the Mountain (1979) the red-haired twins Rachel and Theo Matheson spend the summer at their relatives' house on the lake; across the water live the Wilberforces",
           "奥克兰北岸塔卡普纳旁边、火山爆发口里的淡水湖。莫里斯·吉的《山下》（1979）里，红头发的双胞胎蕾切尔和西奥·马西森在亲戚家湖边的房子里过暑假；湖对岸住着威尔伯福斯一家"),
    b.PROTO("nz-bishopdale", "Bishopdale, Christchurch", "毕晓普代尔，克赖斯特彻奇", *C("nz-bishopdale"),
            "the suburb in the north of Christchurch that Margaret Mahy renamed Gardendale for The Changeover (1984), her Carnegie Medal-winning supernatural romance. The 2017 film moved the story to the post-earthquake city; one of its makers spent his early teens in Bishopdale",
            "克赖斯特彻奇北部的郊区，玛格丽特·马希在获卡内基奖的超自然爱情小说《蜕变》（1984）里把它改名为“花园谷”。2017 年的电影把故事搬到了地震后的城市；影片的主创之一少年时就住在毕晓普代尔"),
]
lines = [
    b.S("nz-plumb-1", "plumb", "nz-henderson", "Peacehaven", "和平居",
        "George Plumb, now about eighty, looks back over his life, not in order but as the memories come, from the 1890s to the 1940s: a Presbyterian minister thrown out of his church for heresy, jailed for sedition during the First World War, husband of Edie and father of twelve, who followed his conscience wherever it led, whatever it cost the people he loved. Later the family moves north to a quiet country town outside Auckland, Henderson, where Gee grew up and which the trilogy calls Loomis, and makes its home in a house named Peacehaven; the children grow up and leave, and Edie dies. Gee based George Plumb on his own grandfather, the minister James Chapple.",
        "年近八十的乔治·普拉姆回顾自己的一生——不按时间顺序，而是想到哪里写到哪里，从 19 世纪 90 年代一直到 20 世纪 40 年代：他是长老会牧师，因为异端被教会赶了出来，一战期间又因煽动罪坐了牢；他是伊迪的丈夫、十二个孩子的父亲，一辈子跟着自己的良心走，不管这让他爱的人付出什么代价。后来一家人北迁到奥克兰城外一个安静的乡下小镇——亨德森，吉就在那里长大，三部曲里它叫“卢米斯”——在一座名叫“和平居”的房子里安了家；孩子们长大离家，伊迪去世了。吉笔下的乔治·普拉姆，原型就是他自己的外祖父、牧师詹姆斯·查普尔。",
        ["Henderson"], ["亨德森"],
        "https://en.wikipedia.org/wiki/Plumb_(novel_series); https://www.britannica.com/topic/Plumb; https://www.librarything.com/work/187470; https://nzetc.victoria.ac.nz/tm/scholarly/tei-Salient42011979-t1-body-d32.html; https://nzbooks.org.nz/2008/literature/containing-multitudes-hamish-clayton/; https://en.wikipedia.org/wiki/Maurice_Gee"),
    b.S("nz-fa-1", "frame-autobiography", "nz-oamaru", "Fifty-six Eden Street", "伊登街五十六号",
        "In three volumes, To the Is-Land (1982), An Angel at My Table (1984) and The Envoy from Mirror City (1985), Janet Frame tells her own life. The first follows a poor railway family through small towns of Otago and Southland, Outram and Wyndham among them, until they settle at 56 Eden Street, Oamaru, the house that gives a chapter its name. The second takes her to teachers' training college in Dunedin, to a breakdown, a misdiagnosis of schizophrenia and eight years in and out of psychiatric hospitals, Seacliff among them, until the prize won by her first book of stories saves her from a scheduled lobotomy. The third follows her as a writer to England and Spain and home again. Jane Campion filmed it as An Angel at My Table (1990).",
        "珍妮特·弗雷姆用三卷书讲述自己的一生：《到岛上去》（1982）、《我桌旁的天使》（1984）和《来自镜城的使者》（1985）。第一卷跟着一个贫穷的铁路工人家庭辗转奥塔哥和南地的小镇，奥特拉姆、温德姆都在其中，最后在奥马鲁伊登街五十六号落脚——书里有一章就以这座房子命名。第二卷写她去达尼丁读师范学院，精神崩溃，被误诊为精神分裂症，此后八年反复进出精神病院，锡克利夫医院是其中之一，直到她的第一本短篇集得了奖，才让她逃过一场脑叶切除手术。第三卷跟着成了作家的她去英国、西班牙，又回到新西兰。简·坎皮恩把它拍成了电影《伏案天使》（1990）。",
        ["Oamaru"], ["奥马鲁"],
        "https://medhum.med.nyu.edu/view/11908; https://www.ebsco.com/research-starters/biography/autobiography-janet-frame; https://en.wikipedia.org/wiki/Janet_Frame; https://ci.nii.ac.jp/ncid/BB07121310?l=en; https://www.lrb.co.uk/the-paper/v47/n08/lucie-elven/wouldn-t-you-like-to-be-normal"),
    b.S("nz-oww-1", "once-were-warriors", "nz-fordlands", "Pine Block", "松林街区",
        "Beth Heke left her small town and married Jake 'the Muss' Heke against her parents' wishes; eighteen years later they live in Pine Block, a state-housing area on the edge of Two Lakes, with six children. Jake, out of work, drinks at the pub, rules by his fists and turns on Beth in front of their friends at his own parties. Their eldest son Nig joins a gang; Boogie is sent to a borstal, where he learns about his Māori heritage; and thirteen-year-old Grace, who writes stories to escape, keeps the household going until she is raped in her own bed and takes her own life. Jake leaves home; Beth starts a Māori culture group to bring the community back to life. (Pine Block is Duff's version of Fordlands in Rotorua.)",
        "贝丝·赫克离开家乡小镇，不顾父母反对嫁给了“肌肉”杰克·赫克；十八年后，他们带着六个孩子住在双湖镇边上的国宅区“松林街区”。杰克没有工作，整天在酒吧喝酒，用拳头说话，在自家的聚会上当着朋友的面对贝丝动手。大儿子尼格加入了街头帮派；布吉被送进少年感化院，在那里认识了自己的毛利传统；十三岁的格蕾丝靠写故事躲开家里的暴力，一手撑着这个家，直到她在自己的床上被强暴，结束了自己的生命。杰克离开了家；贝丝办起毛利文化小组，想让这个社区重新活过来。（松林街区是达夫笔下的罗托鲁阿福德兰兹。）",
        ["Fordlands"], ["福德兰兹"],
        "https://en.wikipedia.org/wiki/Once_Were_Warriors; https://teara.govt.nz/mi/node/16412; https://teara.govt.nz/en/node/223081; https://www.nzherald.co.nz/rotorua-daily-post/news/once-were-warriors-alan-duff-in-his-own-words/Y6QK3D3H45HNBZWJPHREFYG5XQ; https://www.encyclopedia.com/education/news-wires-white-papers-and-books/duff-alan"),
    b.S("nz-pot-1", "potiki", "nz-hongoeka", "The meeting house", "会堂",
        "After the local freezing works closes, a small Māori community on a stretch of coast north of Wellington turns back to its land and the sea. Roimata and her husband Hemi bring up their children together with Toko, a physically disabled boy who has visions of the conflict to come. Developers want the land for a road to a beach resort, a road that would destroy the community's cemetery and meeting house; when the people refuse, the developers burn the marae, and the violence Toko foresaw follows. Toko is killed in the final conflict. The novel closes as the community rebuilds, and with the revelation that Toko has been telling the story as a spirit from within the new meeting house. (The community resembles Hongoeka, Grace's home.)",
        "当地的冷冻肉厂关门以后，惠灵顿以北海边一个小小的毛利社区重新回到土地和大海。罗伊玛塔和丈夫赫米把自己的孩子和托科一起带大——托科身有残疾，能在幻象里看见将要到来的冲突。开发商想要这片地，修一条通往海滨度假村的路，而这条路会毁掉社区的墓地和会堂；人们拒绝了，开发商就烧了会堂，托科预见的暴力随之而来。托科死在了最后的冲突里。小说结尾，社区开始重建，读者这才知道，一直在讲故事的托科，是从新会堂里说话的灵魂。（这个社区就像格雷斯的家乡洪戈埃卡。）",
        ["Hongoeka"], ["洪戈埃卡"],
        "https://en.wikipedia.org/wiki/Potiki; https://www.thenile.co.nz/books/patricia-grace/tu/9780143019206"),
    b.S("nz-cyt-1", "can-you-tolerate-this", "nz-te-kuiti", "“The Te Kūiti Underground”", "《蒂库伊蒂地下》",
        "Twenty-one personal essays, candid and often very funny, about growing up in a small New Zealand town and finding a way out into the wider world. Several go back to Te Kūiti in the 1990s: to a family of a father, a mother and two older brothers, to the Hamilton music scene, to the long essay 'Big Red', and to 'The Te Kūiti Underground', in which a shy fourteen-year-old walks up above the town, looks down over its paddocks and little airport under the grey sky, and wishes for someone who could make the place feel like the setting of a story. The collection won the 2017 Ockham award for general non-fiction, and Young a Windham-Campbell Prize.",
        "二十一篇个人散文，坦率，常常好笑，写一个在新西兰小镇长大的女孩怎样一步步走进更大的世界。好几篇回到 20 世纪 90 年代的蒂库伊蒂：父亲、母亲和两个哥哥组成的家，汉密尔顿的音乐圈，长篇散文《大红》，还有《蒂库伊蒂地下》——一个害羞的十四岁女孩爬到镇子上方，在灰色的天空下俯看牧场和小小的机场，盼着能有个人出现，让这个地方像故事里的场景一样。这部集子获得 2017 年奥克姆图书奖的非虚构类奖，扬本人也因此获得温德姆-坎贝尔奖。",
        ["Te Kūiti"], ["蒂库伊蒂"],
        "https://thespinoff.co.nz/culture/11-08-2016/book-of-the-week-confirming-the-amazing-talent-of-ashleigh-young; https://nzbooks.org.nz/2016/non-fiction/something-that-rises-ingrid-horrocks; https://sydneyreviewofbooks.com/essay/the-te-kuiti-underground; https://en.wikipedia.org/wiki/Ashleigh_Young; https://www.readings.com.au/product/9781925336443/9781925336443"),
    b.S("nz-sd-1", "smiths-dream", "nz-coromandel", "The island", "小岛",
        "In a New Zealand of the near future, a man named Volkner has seized power in a right-wing coup and keeps it with the army and a special police force, while a war much like the Vietnam War spreads through the country. Smith, whose marriage has fallen apart, has retreated to a small island off the Coromandel to live alone. The world will not leave him there: arrested as a guerrilla, he is caught between the special police and a growing resistance and drawn, unwilling, into the fighting. Stead, then active against the Vietnam War, made the ending harsher for the revised edition of 1973; the novel was filmed as Sleeping Dogs (1977), starring Sam Neill.",
        "近未来的新西兰，一个叫沃尔克纳的人通过右翼政变夺取了政权，靠军队和特别警察维持统治，一场很像越南战争的战事在全国蔓延。婚姻破裂的史密斯躲到科罗曼德尔外海的一个小岛上，想一个人过日子。可世界不肯放过他：他被当作游击队员抓了起来，夹在特别警察和日益壮大的抵抗力量之间，身不由己地卷进了战斗。当时正投身反越战运动的斯特德，在 1973 年的修订版里把结局改得更加冷酷；小说后来被拍成由萨姆·尼尔主演的电影《沉睡的狗》（1977）。",
        ["Coromandel"], ["科罗曼德尔"],
        "https://www.pressreader.com/new-zealand/sunday-star-times/20210509/281891596150291; https://nzherald.co.nz/entertainment/top-five-favourite-nz-novels-named/QK7Q3XIPHOH7CDCKXPFSIU6ACA; https://journalhosting.ucalgary.ca/index.php/ariel/article/view/32072/26133; https://sf-encyclopedia.com/entry/stead_c_k; https://www.britannica.com/topic/Smiths-Dream; https://teara.govt.nz/en/node/212253"),
    b.S("nz-oh-1", "other-halves", "nz-christchurch", "The hospital", "医院",
        "Liz, a Pākehā woman in her thirties whose marriage is failing, feels she is going mad and has herself admitted to a psychiatric hospital. There she meets Tug, a sixteen-year-old Māori street kid, angry, funny and in his own way suffering, and they become friends over games of poker. Outside, the friendship grows into a love that breaks almost every rule around them, and the two try to make a life together. The novel is semi-autobiographical, drawn from McCauley's own relationship, and won both the Wattie Book of the Year and the New Zealand Book Award for Fiction. (A reader's review says the book opens with Liz phoning an institution in 1970s Christchurch; we have not checked this against the text, and the 1984 film set the story in Auckland.)",
        "莉兹是个三十多岁的白人女子，婚姻正在破裂，她觉得自己要疯了，于是主动住进了精神病院。在那里，她认识了图格——一个十六岁的毛利街头少年，满腔怒火，很会逗乐，也有他自己的痛苦；两人在打扑克中成了朋友。出院以后，这份友谊变成了一场几乎打破身边一切规矩的爱情，两人试着一起过日子。这部小说带有半自传性质，取材于麦考利自己的感情经历，同时获得瓦蒂年度图书奖和新西兰图书奖小说奖。（据一位读者的书评，小说开篇是莉兹给 20 世纪 70 年代克赖斯特彻奇的一家机构打电话；我们没有对照原文核实，1984 年的电影则把故事放在了奥克兰。）",
        ["Christchurch"], ["克赖斯特彻奇"],
        "https://www.kirkusreviews.com/book-reviews/sue-mccauley/other-halves/; https://www.nzherald.co.nz/the-listener/culture/author-sue-mccauley-doesnt-stick-to-convention-in-her-new-novel/36UUPU3L55AYLEGFKLNV7Z5MZ4; https://en.wikipedia.org/wiki/Sue_McCauley; https://www.everand.com/book/902960490/Other-Halves; https://www.allmovie.com/movie/other-halves-v118611; https://www.wikiwand.com/en/articles/Other_Halves"),
    b.S("nz-10pm-1", "the-10pm-question", "nz-christchurch", "Frankie's ten o'clock questions", "十点钟的问题",
        "Twelve-year-old Frankie Parsons is a talented, anxious boy in a warm, eccentric family: a father everyone calls Uncle, an older brother and sister, great-aunts and a very fat cat, and Gigs, the best friend with whom he shares a private language. Every night at ten he goes to his mother's room with his latest worry, a rash, the smoke alarm, the school camp, and she answers it. Then Sydney arrives at his school, a loud, fearless girl who has been to twenty-two schools, and her questions start to unravel his carefully kept world, above all the one Frankie has never let himself ask: why his mother has not left the house in nine years. (The city is never named; De Goldi, who grew up in Christchurch, sets her novels there.)",
        "十二岁的弗兰基·帕森斯有才华，也特别爱担心。他生活在一个温暖又古怪的大家庭里：大家都叫“叔叔”的爸爸，一个哥哥一个姐姐，几位姑婆，一只特别胖的猫，还有和他共用一套秘密语言的好朋友吉格斯。每天晚上十点，他都要去妈妈房间，问出当天最新的担心——身上的疹子，烟雾报警器，学校的露营——妈妈一一回答。后来学校里来了悉尼，一个嗓门大、什么都不怕、已经转过二十二所学校的女孩；她的问题一点点拆开了弗兰基小心维持的世界，尤其是那个他从不让自己问出口的问题：为什么妈妈九年没有出过家门。（书里从没提过城市的名字；在克赖斯特彻奇长大的德戈尔迪，把她的小说都设在那里。）",
        ["Christchurch"], ["克赖斯特彻奇"],
        "https://www.rnz.co.nz/collections/not-for-children/the-10pm-question; https://www.schoollibraryjournal.com/review/the-10-pm-question; https://bookpage.com/reviews/6704-kate-de-goldi-mysteries-family-friendship-ya/; https://nzherald.co.nz/entertainment/the-detail-of-a-butterflys-wing/5BRCVVXS35RAHITL3TAJSG7I6Y; https://excerpts.cdn.overdrive.com/FormatType-410/1486-1/1BD/369/BE/10PMQuestion9781848774728.epub; https://my.christchurchcitylibraries.com/blogs/post/kate-de-goldi-earthquakes-and-cathedrals-word-christchurch-2022/"),
    b.S("nz-pp-1", "pounamu-pounamu", "nz-waituhi", "“A Game of Cards”", "《打牌》",
        "The first collection of short stories published by a Māori writer: ten stories, most of them of family and community life in a small East Coast settlement, with Māori words woven through the English. In the opening story, 'A Game of Cards', a young man comes home by train to find his grandmother ill; she always cheated at cards, and from her bed she asks for one more game, so the old women gather round and play. Death is the theme of four of the ten stories, and 'Fire on Greenstone' takes up where 'A Game of Cards' leaves off. Ihimaera said the book fulfilled a childhood vow to write about Māori from his own self and home place. (The settlement is his recreation of Waituhi, where he grew up.)",
        "这是第一部由毛利作家出版的短篇小说集：十个故事，大多写东海岸一个小聚落里的家庭与社群生活，英语叙述里织进了毛利语。开篇的《打牌》里，一个年轻人坐火车回家，发现奶奶病了；奶奶打牌一向爱耍赖，躺在床上还要再玩一局，于是几位老太太围坐在床边打起牌来。十个故事里有四个以死亡为主题，《绿玉上的火》接着《打牌》往下讲。伊希马埃拉说，这本书兑现了他儿时的誓愿：用自己和家乡来写毛利人。（这个聚落是他按想象重建的怀图希，他就在那里长大。）",
        ["Waituhi"], ["怀图希"],
        "https://en.wikipedia.org/wiki/Witi_Ihimaera; https://dynamic-rsnz.natlib.govt.nz/periodicals/TAH197311.2.27.2; https://ojs.victoria.ac.nz/kotare/article/download/734/544/639; https://books.apple.com/au/book/pounamu-pounamu/id6443281578; https://cdn2.penguin.com.au/content/resources/pounamupounamu-teachersnotes.pdf; https://journals.lib.unb.ca/index.php/IFR/article/download/13129/14212/17837"),
    b.S("nz-tu-1", "tu-grace", "nz-wellington", "From Wellington to Cassino", "从惠灵顿到卡西诺",
        "Tu is proud of his name, which belongs to Tūmatauenga, the god of war. He and his older brothers Pita and Rangi grew up in the shadow of Mount Taranaki, where their father came back from the First World War a broken man given to fits of rage; after his death the family moved to Wellington, where Pita and Rangi found labouring jobs and the family slowly made its place. Rangi and then Pita join the 28th (Māori) Battalion, and Tu, who was meant to stay home with his mother and sisters, follows them; the three fight in the mud and rubble of Cassino and on through Italy. Only Tu comes home. Some twenty years later he writes to Pita's and Rangi's children and gives them his war journal, and with it the truth of what happened to the brothers.",
        "图为自己的名字骄傲——它属于战神图马陶恩加。他和两个哥哥皮塔、兰吉在塔拉纳基山下长大，他们的父亲从一战回来，成了一个时常暴怒的废人；父亲死后，一家人搬到惠灵顿，皮塔和兰吉找了体力活，一家人慢慢站稳了脚。兰吉和皮塔先后加入第 28（毛利）营，本该留在家里陪母亲和姐妹的图也跟了去；三兄弟在卡西诺的泥泞与废墟中作战，一路打过意大利。只有图活着回了家。大约二十年后，他给皮塔和兰吉的孩子写信，把自己的战地日记交给他们，也把兄弟们真正的遭遇交给了他们。",
        ["Wellington"], ["惠灵顿"],
        "https://teara.govt.nz/en/document/42294/patricia-graces-tu; https://nzherald.co.nz/lifestyle/ipatricia-gracei-tu-a-novel/P2LPENF3FSCQXXI62T7MHJMKUQ; https://nzbooks.org.nz/2004/literature/for-god-king-and-country-chris-else/; https://books.apple.com/gb/book/tu/id1456703492; https://books.apple.com/ca/book/tu/id1456703492; https://www.goodreads.com/book/show/1295361"),
    b.S("nz-sotj-1", "season-of-the-jew", "nz-matawhero", "Poverty Bay, November 1868", "1868 年 11 月，贫穷湾",
        "George Fairweather, a former British officer and amateur watercolourist who has tired of killing Māori for land-hungry colonists, comes to Poverty Bay in 1867 to paint and to find again Meriana Smith, a woman of mixed descent. He urges negotiation and keeps his distance from the settlers. Then Kooti, a mission-educated trader turned prophet who has escaped with his followers from exile on the Chatham Islands, falls on the settlement at Matawhero in November 1868, killing settlers and Māori, women and children, and Fairweather is drawn into the long pursuit of him through Te Urewera, and into a reckoning with himself. The narrative covers the year that begins on 10 November 1868; Te Kooti himself is glimpsed only twice.",
        "乔治·费尔韦瑟曾是英国军官，也是个业余水彩画家，他厌倦了替贪地的殖民者杀毛利人，1867 年来到贫穷湾，想画画，也想再见到混血女子梅丽亚娜·史密斯。他主张谈判，同移民们保持距离。后来，受过教会教育、由商人变成先知的科提带着追随者从查塔姆群岛的流放地逃回，1868 年 11 月袭击了马塔怀罗的定居点，移民和毛利人、妇女和孩子都死在刀下；费尔韦瑟被卷进穿越特乌雷韦拉山区、对科提旷日持久的追捕，也被迫面对他自己。小说讲的是从 1868 年 11 月 10 日开始的那一年；特库蒂本人在书里只露过两次面。",
        ["Matawhero"], ["马塔怀罗"],
        "https://en.wikipedia.org/wiki/Season_of_the_Jew; https://www.kirkusreviews.com/book-reviews/a/maurice-shadbolt-5/season-of-the-jew/; https://www.abebooks.com/9780393024319/Season-Jew-Novel-Shadbolt-Maurice-0393024318/plp; https://www.librarything.es/work/451287; https://www.goodreads.com/book/show/1505538; https://nzbooks.org.nz/2005/literature/tickling-history-jane-stafford/; https://wolfgangsperlich.blogspot.com/2026/05/"),
    b.S("nz-utm-1", "under-the-mountain", "nz-lake-pupuke", "The house across the lake", "湖对岸的房子",
        "The red-haired twins Rachel and Theo Matheson, from Nelson, come to spend the summer holidays with their uncle, aunt and cousin Ricky in a house on Lake Pupuke, a deep lake in an old explosion crater within sight of Rangitoto. Across the lake live the Wilberforces, whose strange smell and stares make the twins' skin crawl. A mysterious old man, Mr Jones, tells them the truth: the Wilberforces are slug-like creatures from another world, held for thousands of years in a spellbound sleep beneath Auckland's volcanoes and now waking, and only red-haired twins can wield the weapon that will destroy them before they destroy the Earth.",
        "红头发的双胞胎蕾切尔和西奥·马西森从纳尔逊来，到叔叔、婶婶和表弟里基家过暑假，房子就在普普克湖边——那是一个古老火山爆发口里的深湖，望得见朗伊托托岛。湖对岸住着威尔伯福斯一家，他们身上的怪味和盯人的目光让双胞胎浑身发毛。一位神秘的老人琼斯先生告诉了他们真相：威尔伯福斯一家是来自另一个世界、像巨型鼻涕虫一样的生物，被咒语困在奥克兰的火山底下沉睡了几千年，如今正在醒来；只有红头发的双胞胎能使用那件武器，在它们毁掉地球之前消灭它们。",
        ["Lake Pupuke"], ["普普克湖"],
        "https://www.blackgate.com/?p=10703; https://www.wcl.govt.nz/blogs/kids/?p=192; https://en.wikipedia.org/wiki/Under_the_Mountain_(novel); https://www.librarything.com/work/16399; https://teara.govt.nz/mi/node/224360; https://weneedtotalkaboutbooks.com/2025/03/18/under-the-mountain-by-maurice-gee-a-review/"),
    b.S("nz-co-1", "the-changeover", "nz-bishopdale", "Gardendale", "花园谷",
        "Fourteen-year-old Laura Chant lives in Gardendale, a fairly new suburb of Christchurch, with her mother Kate, who manages a bookshop in the Gardendale Mall, and her three-year-old brother Jacko. One day they go into a strange new antique shop, where the proprietor, Carmody Braque, stamps Jacko's hand with an image of his own face; it will not wash off, and Jacko begins to sicken as Braque, an ancient being who lives on others' lives, drains him. To save him, Laura turns to Sorensen Carlisle, a prefect at her school and a secret witch, and his family of witches, and goes through the dangerous changeover into a witch herself, a spirit journey through a dark forest that is also Gardendale. (Gardendale is Mahy's name for Bishopdale.)",
        "十四岁的劳拉·钱特住在克赖斯特彻奇一个新建不久的郊区“花园谷”，和她一起生活的是在花园谷商场管一家书店的母亲凯特，还有三岁的弟弟杰科。一天，姐弟俩走进一家新开的古怪古董店，店主卡莫迪·布拉克在杰科手上盖了个印章，印的是他自己的脸；那印怎么也洗不掉，杰科一天天病下去——布拉克是个靠吸食别人生命活着的古老怪物。为了救弟弟，劳拉去找学校的级长、暗地里是个巫师的索伦森·卡莱尔和他那一家女巫，冒险经历“蜕变”，自己也变成女巫——那是一场穿过黑暗森林的灵魂之旅，而那片森林同时也是花园谷。（花园谷是马希给毕晓普代尔起的名字。）",
        ["Bishopdale"], ["毕晓普代尔"],
        "https://en.wikipedia.org/wiki/The_Changeover; https://thespinoff.co.nz/culture/26-10-2024/the-changeover-by-margaret-mahy-is-the-greatest-young-adult-novel-ever; https://www.librarything.com/work/26674; https://my.christchurchcitylibraries.com/blogs/post/book-to-film-the-changeover/; https://www.penguin.com.au/books/the-changeover-9798217345045"),
]
check(books, places, lines, old_places=["nz-oamaru"])
if __name__ == "__main__":
    run(books, places, lines, "add_nz2.py")
