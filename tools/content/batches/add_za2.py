"""11-24: South Africa, the 6 books that selection rule v2 adds (tools/selection/za.md). Scene notes in our own words.
Places, with the reason for each:
- Life & Times of Michael K: Prince Albert, the Karoo town of K's mother's birthplace, where he buries her ashes on a
  deserted farm.
- A Dry White Season: the novel begins with the Soweto uprising of 16 June 1976, in which Gordon Ngubene's son Jonathan
  disappears; pinned at the Hector Pieterson Museum in Orlando West, Soweto, which marks that day.
- Burger's Daughter: Johannesburg (city-level pin); the prison where the novel opens is not named.
- Country of My Skull: East London, where the Truth and Reconciliation Commission held its first public hearings in April
  1996 (City Hall) and Nomonde Calata gave the testimony to which Krog gives particular attention (city-level pin).
- Down Second Avenue: Marabastad, Pretoria, the location of Second Avenue.
- Chaka: the Shaka Memorial at KwaDukuza, Shaka's grave near the place where he was assassinated, which Mofolo visited in
  1909 while gathering material for the novel. The Sesotho original (1925) is out of copyright, but no transcription was
  found, so the line is a scene note.
Also: tools/validate.js and js/i18n.js gain the language codes "af" (Afrikaans) and "st" (Sesotho).
Photos: tools/content/batches/add_photos_za_1124.py.

Usage: python3 -I tools/content/batches/add_za2.py <app_dir> tools/content/batches/coords/add_za2.json"""
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
def check(books, places, lines):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    bk = {x["id"] for x in books}
    assert not bk & allb, bk & allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    for l in lines:
        assert l["book_id"] in bk and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} == bk
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
def run(books, places, lines, script):
    M = f"11-24: South Africa, books that selection rule v2 adds (tools/content/batches/{script})"
    for name, xs in (("books.js", books), ("places.js", places), ("lines.js", lines)):
        if xs: b.append(b.data(name), xs, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
b.init(APP, "", "za", DATE)
books = [
    BK("life-and-times-of-michael-k", "Life & Times of Michael K", "迈克尔·K的生活和时代", "Life & Times of Michael K", "J. M. Coetzee",
       "J. M. 库切", "J. M. Coetzee", "1983", "en", ["Life and Times of Michael K", "Michael K", "Anna K", "Prince Albert"]),
    BK("a-dry-white-season", "A Dry White Season", "干旱的白色季节", "’n Droë wit seisoen", "André Brink", "安德烈·布林克", "André Brink",
       "1979", "af", ["n Droe wit seisoen", "Ben du Toit", "Gordon Ngubene", "Jonathan Ngubene"]),
    BK("burgers-daughter", "Burger's Daughter", "伯格的女儿", "Burger's Daughter", "Nadine Gordimer", "纳丁·戈迪默", "Nadine Gordimer", "1979", "en",
       ["Rosa Burger", "Lionel Burger", "Bram Fischer"]),
    BK("country-of-my-skull", "Country of My Skull", "我的头骨之国", "Country of My Skull", "Antjie Krog", "安特耶·克罗格", "Antjie Krog", "1998", "en",
       ["Antjie Samuel", "Truth and Reconciliation Commission", "TRC", "Nomonde Calata"]),
    BK("down-second-avenue", "Down Second Avenue", "第二大道", "Down Second Avenue", "Es'kia Mphahlele", "埃斯基亚·姆帕赫莱莱", "Es'kia Mphahlele",
       "1959", "en", ["Ezekiel Mphahlele", "Marabastad", "Maupaneng"]),
    BK("chaka-mofolo", "Chaka", "恰卡", "Chaka", "Thomas Mofolo", "托马斯·莫福洛", "Thomas Mofolo", "1925", "st",
       ["Shaka", "Chaka Senzangakhona", "Isanusi", "Noliwa", "Nandi"], pd=True),
]
places = [
    b.ORIG("za-prince-albert", "Prince Albert", "艾伯特亲王镇", *C("za-prince-albert"),
           "Small town at the foot of the Swartberg on the edge of the Great Karoo. In J. M. Coetzee's Life & Times of Michael K (1983), which won the Booker Prize, Michael K sets out from Cape Town in a time of civil war to take his dying mother to her birthplace on a farm in the district of Prince Albert; he arrives alone with her ashes and settles on a deserted farm to grow pumpkins",
           "大卡鲁边缘、斯瓦特山脚下的小镇。J. M. 库切获布克奖的《迈克尔·K的生活和时代》（1983）里，内战时期，迈克尔·K从开普敦出发，要把垂死的母亲送回她出生的地方——艾伯特亲王镇地区的一座农场；最后他独自带着母亲的骨灰来到这里，在一座废弃的农场住下，种起了南瓜"),
    b.ORIG("za-hector-pieterson", "Hector Pieterson Museum, Soweto", "赫克托·彼得森博物馆，索韦托", *C("za-hector-pieterson"),
           "Museum in Orlando West, Soweto, two blocks from where the schoolboy Hector Pieterson was shot dead on 16 June 1976, the first day of the Soweto uprising. André Brink's A Dry White Season (1979) begins with that uprising, in which Jonathan, the son of the school cleaner Gordon Ngubene, disappears; the pin marks the day rather than a place named in the novel",
           "索韦托奥兰多西区的博物馆，离学生赫克托·彼得森 1976 年 6 月 16 日——索韦托起义第一天——中弹身亡的地方只隔两个街区。安德烈·布林克的《干旱的白色季节》（1979）就从这场起义开始：学校清洁工戈登·恩古贝内的儿子乔纳森在起义中失踪了；这个图钉标的是那一天，而不是小说里点名的某个地点"),
    b.ORIG("za-johannesburg", "Johannesburg", "约翰内斯堡", *C("za-johannesburg"),
           "South Africa's largest city. Nadine Gordimer's Burger's Daughter (1979) begins here in 1974: Rosa Burger, whose Afrikaner communist father Lionel, modelled on Bram Fischer, has just died in prison, tries to find a life of her own; the novel opens with Rosa at fourteen outside a prison, waiting to visit her detained mother. The prison is not named; the pin is the city's point",
           "南非最大的城市。纳丁·戈迪默的《伯格的女儿》（1979）从 1974 年的这里开始：罗莎·伯格的父亲莱昂内尔——一个以布拉姆·费希尔为原型的阿非利卡共产党人——刚刚死在狱中，她想过上属于自己的生活；小说开篇是十四岁的罗莎站在监狱外，等着探望被关押的母亲。书里没写是哪座监狱；图钉标在市中心点"),
    b.ORIG("za-east-london", "East London (City Hall hearings)", "东伦敦（市政厅听证会）", *C("za-east-london"),
           "Port city on the coast of the Eastern Cape, where the Truth and Reconciliation Commission held its first public hearings, in the City Hall, in April 1996. On the second day Nomonde Calata, widow of Fort Calata, one of the Cradock Four, broke down in a wail that became one of the defining sounds of the Commission; Antjie Krog, who covered the hearings for SABC radio, gives her testimony particular attention in Country of My Skull (1998). The pin is the city's point",
           "东开普省海边的港口城市，1996 年 4 月，真相与和解委员会在这里的市政厅举行了第一批公开听证会。第二天，“克拉多克四人”之一福特·卡拉塔的遗孀诺蒙德·卡拉塔失声痛哭，那一声哭喊成了真相与和解委员会最鲜明的声音之一；为南非广播公司电台报道听证会的安特耶·克罗格在《我的头骨之国》（1998）里特别关注了她的证词。图钉标在市中心点"),
    b.ORIG("za-marabastad", "Marabastad, Pretoria", "马拉巴斯塔德，比勒陀利亚", *C("za-marabastad"),
           "Old location on the western edge of central Pretoria where Es'kia Mphahlele was born in 1919 and grew up from the age of twelve, at his grandmother's house on Second Avenue. His autobiography Down Second Avenue (1959), banned in South Africa, takes its title from that street",
           "比勒陀利亚市中心西边的老黑人居住区，埃斯基亚·姆帕赫莱莱 1919 年生在这里，十二岁起在第二大道外祖母家长大。他在南非遭禁的自传《第二大道》（1959）就以这条街为名"),
    b.ORIG("za-shaka-memorial", "Shaka Memorial, KwaDukuza", "沙卡纪念地，夸杜库扎", *C("za-shaka-memorial"),
           "Provincial heritage site at KwaDukuza that marks the grave of the Zulu king Shaka, near the place at his capital Dukuza where he was assassinated in 1828 by his half-brothers Dingane and Mhlangana. Thomas Mofolo visited the grave in 1909 while gathering material for Chaka, his Sesotho novel of Shaka's rise and fall, published in 1925",
           "夸杜库扎的省级文物地，标记祖鲁国王沙卡的坟墓，旁边就是他 1828 年在都城杜库扎被同父异母的兄弟丁冈和姆赫兰加纳刺杀的地方。托马斯·莫福洛 1909 年为写《恰卡》搜集材料时到过这座坟墓；这部写沙卡兴衰的塞索托语小说出版于 1925 年"),
]
lines = [
    b.S("za-mk-1", "life-and-times-of-michael-k", "za-prince-albert", "The farm near Prince Albert", "艾伯特亲王镇附近的农场",
        "In a South Africa torn by civil war, Michael K, a municipal gardener in Cape Town born with a harelip and brought up in an institution, leaves his job to take his sick mother Anna, a domestic servant in Sea Point, back to the farm in the district of Prince Albert where she was born. Without the permits to travel, he pushes her in a barrow he has built; she dies in a hospital in Stellenbosch, and he goes on carrying her ashes in a box. After a spell of forced labour on the railway he reaches Prince Albert, finds what may be the farm, buries her ashes and begins to grow pumpkins, living off the land, until soldiers and camps take hold of him again.",
        "南非内战正酣。迈克尔·K天生兔唇，在收容机构里长大，是开普敦市政局的园丁。他的母亲安娜在海角区给人当女佣，病得很重；他辞了工作，要把母亲送回她出生的地方——艾伯特亲王镇地区的那座农场。没有通行证，他就推着自己做的手推车载着她上路；母亲死在斯泰伦博斯的医院里，他便把她的骨灰装在盒子里继续往前走。在铁路上被强迫劳动了一阵之后，他到了艾伯特亲王镇，找到了也许就是那座农场的地方，埋下骨灰，种起南瓜，靠土地过活，直到士兵和营地又一次抓住了他。",
        ["Prince Albert"], ["艾伯特亲王镇"],
        "https://en.wikipedia.org/wiki/Life_%26_Times_of_Michael_K; https://www.ebsco.com/research-starters/literature-and-writing/life-and-times-michael-k-j-m-coetzee; https://medhum.med.nyu.edu/view/17373; https://www.encyclopedia.com/arts/culture-magazines/coetzee-john-michael; https://www.gradesaver.com/life-and-times-of-michael-k/study-guide/summary; https://www.themodernnovel.org/?p=6023"),
    b.S("za-dws-1", "a-dry-white-season", "za-hector-pieterson", "Soweto, 16 June 1976", "1976 年 6 月 16 日，索韦托",
        "Ben du Toit, an Afrikaner who teaches history and geography at a Johannesburg school, has never questioned the state and has never set foot in Soweto. Then Jonathan, the son of the school's black cleaner Gordon Ngubene, whose fees Ben has paid, disappears in the Soweto uprising of June 1976 and dies in the hands of the security police. Gordon cannot accept the official story and asks Ben for help; he is arrested in turn and dies in custody, and the police say he hanged himself. Ben begins to investigate the Special Branch himself, loses his family, his friends and his standing, and is killed, apparently by the security police. His story is told by a writer friend from the papers Ben left. The novel was banned soon after it appeared.",
        "本·杜托伊是个阿非利卡人，在约翰内斯堡一所学校教历史和地理，从没怀疑过国家，也从没踏进过索韦托一步。后来，学校的黑人清洁工戈登·恩古贝内的儿子乔纳森——本替他交过学费——在 1976 年 6 月的索韦托起义中失踪，死在了安全警察手里。戈登不肯接受官方的说法，请本帮忙；他随后也被捕，死在羁押中，警方说他是上吊自杀。本开始自己调查特别处，因此失去了家庭、朋友和地位，最后被杀，看来是安全警察下的手。他的故事由一位作家朋友根据他留下的文件讲出来。小说出版后不久就被禁了。",
        ["Soweto"], ["索韦托"],
        "https://www.goodreads.com/book/show/65249; https://www.librarything.com/work/27399; https://www.librarycat.org/lib/allibrary/item/195305575; https://proof.csmonitor.com/1980/0310/031052.html; https://www.supersummary.com/a-dry-white-season/summary; https://www.encyclopedia.com/arts/culture-magazines/dry-white-season-1; https://en.wikipedia.org/wiki/A_Dry_White_Season_(novel)"),
    b.S("za-bd-1", "burgers-daughter", "za-johannesburg", "Outside the prison", "监狱外",
        "The novel opens with Rosa Burger at fourteen, waiting outside a prison to visit her detained mother. In 1974 Rosa is twenty-six, and her father, Lionel Burger, an Afrikaner doctor and communist, has died in prison three years into a life sentence for treason. Her whole life has been defined by her parents' struggle, and she tries to find a self of her own: she leaves South Africa for the south of France, to stay in Nice with Katya, her father's first wife, and then London. But she comes home, works in Soweto, and after the uprising of 1976 is detained herself. Gordimer called the book 'a coded homage' to Bram Fischer. (The novel is set in Johannesburg; the prison is not named.)",
        "小说开篇，十四岁的罗莎·伯格站在监狱外，等着探望被关押的母亲。到 1974 年，罗莎二十六岁，她的父亲莱昂内尔·伯格——一位阿非利卡医生、共产党人——因叛国罪被判终身监禁，服刑三年后死在狱中。她的一生都被父母的斗争所界定，她想找到自己：她离开南非去了法国南部，在尼斯投靠父亲的前妻卡佳，后来又去了伦敦。可她还是回了国，在索韦托工作，1976 年起义之后，她自己也被拘押了。戈迪默称这本书是献给布拉姆·费希尔的“一份加密的致敬”。（小说的背景是约翰内斯堡；书里没写是哪座监狱。）",
        ["Johannesburg"], ["约翰内斯堡"],
        "https://en.wikipedia.org/wiki/Burger%27s_Daughter; https://www.gradesaver.com/burgers-daughter/wikipedia/introduction; https://supersummary.com/burger-s-daughter/summary; https://encyclopedia.com/arts/culture-magazines/burgers-daughter; https://www.ebsco.com/research-starters/literature-and-writing/burgers-daughter-analysis-major-characters"),
    b.S("za-coms-1", "country-of-my-skull", "za-east-london", "The first hearings", "第一批听证会",
        "From 1996 to 1998 Antjie Krog, an Afrikaans poet working as a radio reporter under her married name Antjie Samuel, led the SABC team covering the Truth and Reconciliation Commission, travelling across the country from city halls to backwater community centres to hear victims tell of the killings and torture of the apartheid years, and perpetrators ask for amnesty. Her book weaves verbatim testimony together with reporting, poetry and memoir, and with her own struggle, as a white Afrikaner, with guilt, language and belonging. Among the testimonies she dwells on is that of Nomonde Calata, whose cry at the first hearings in East London, in April 1996, came to stand for the Commission itself. It was Krog's first book in English.",
        "1996 年至 1998 年，阿非利卡语诗人安特耶·克罗格以婚后的名字“安特耶·塞缪尔”当电台记者，带领南非广播公司的团队报道真相与和解委员会。她跑遍全国，从气派的市政厅到偏僻的社区中心，听受害者讲述种族隔离年代的杀戮和酷刑，听施害者请求特赦。她的书把证词原文和报道、诗歌、回忆交织在一起，也写下她作为一个白人阿非利卡人，在罪责、语言和归属上的挣扎。她着墨较多的证词之一来自诺蒙德·卡拉塔——1996 年 4 月东伦敦第一批听证会上，她的那一声哭喊后来成了真相与和解委员会本身的象征。这是克罗格的第一部英文作品。",
        ["East London"], ["东伦敦"],
        "https://en.wikipedia.org/wiki/Country_of_My_Skull; https://en.wikipedia.org/wiki/Antjie_Krog; https://www.opendemocracy.net/en/krog-3434jsp/; https://supersummary.com/country-of-my-skull/part-2; https://www.dailymaverick.co.za/?p=135280; https://sabctrc.saha.org.za/export/hearingtext.php?id=55192; https://www.inkl.com/news/justice-denied-why-families-of-apartheid-victims-are-still-searching-for-answers"),
    b.S("za-dsa-1", "down-second-avenue", "za-marabastad", "Second Avenue", "第二大道",
        "In the autumn of 1924, five-year-old Ezekiel Mphahlele, his brother and his sister are sent from Marabastad, where their parents work, to live with their stern paternal grandmother in Maupaneng, a village near Pietersburg. At twelve he comes back to Marabastad, to his grandmother's house on Second Avenue, and grows up in the location among three strong women, his mother Eva, his grandmother and his aunt Dora, amid poverty, police raids and his parents' broken marriage. Clever at school, he goes on to St Peter's in Johannesburg and Adams College in Natal and becomes a teacher, only to meet one setback after another in his career. The book, punctuated by five intensely personal interludes, ends with his leaving South Africa for exile in 1957.",
        "1924 年秋天，五岁的伊齐基尔·姆帕赫莱莱和哥哥、姐姐被从父母做工的马拉巴斯塔德送到彼得斯堡附近的毛帕能村，跟严厉的祖母一起生活。十二岁那年，他回到马拉巴斯塔德第二大道上外祖母的家，在这片黑人居住区里，在三个坚强的女人——母亲伊娃、外祖母和姨妈多拉——身边长大，周围是贫穷、警察的突袭，还有父母破裂的婚姻。他在学校成绩出众，先后进了约翰内斯堡的圣彼得学校和纳塔尔的亚当斯学院，成了教师，却在教书生涯里屡遭挫折。全书穿插着五段极其私人的独白，最后以他 1957 年离开南非、流亡海外结束。",
        ["Marabastad"], ["马拉巴斯塔德"],
        "https://en.wikipedia.org/wiki/Down_Second_Avenue; https://en.wikipedia.org/wiki/Es%27kia_Mphahlele; https://www.supersummary.com/down-second-avenue-ezekiel-mphahlele/summary; https://ebsco.com/research-starters/biography/ezekiel-mphahlele; https://www.goodreads.com/book/show/1379959; https://www.dailymaverick.co.za/opinionista/2023-10-23-down-second-avenue-second-time-around-re-reading-eskia-mphahlele-today/; https://www.unisa.ac.za/sites/corporate/default/Unisa-History-and-Memory-Project/Personalities/All-personalities/Es%27kia-Mphahlele"),
    b.S("za-ch-1", "chaka-mofolo", "za-shaka-memorial", "The death of Chaka", "恰卡之死",
        "Mofolo tells the life of Shaka not as history but as a tale. Chaka is born to the Zulu chief Senzangakhona and Nandi, whose pregnancy before marriage brings shame on them both; rejected by his father and hounded as a boy, he flees, and meets Isanusi, a sorcerer whose medicines and followers help him in war. He rises in the service of Dingiswayo, succeeds him and falls in love with Noliwa, Dingiswayo's sister; told by Isanusi that he can be a great king and marry her, or a truly great king and kill her, he chooses to kill her, and from then on his rule is drowned in ever more blood. At last, at his capital Dukuza, he is killed by his half-brothers Dingane and Mhlangana. (Mofolo visited Shaka's grave at KwaDukuza in 1909.)",
        "莫福洛讲沙卡的一生，不是当作历史，而是当作一个传说。恰卡是祖鲁酋长森赞加科纳和南迪的儿子，南迪婚前怀孕，让两人都蒙了羞；他遭父亲嫌弃，从小受人追杀，只好出逃，遇见了巫师伊萨努西，伊萨努西的药和手下帮他打仗。他在丁吉斯瓦约麾下崛起，继承了他的位置，又爱上了丁吉斯瓦约的妹妹诺莉瓦；伊萨努西告诉他，他可以做一个伟大的国王娶她，也可以做一个真正伟大的国王杀了她，他选择了杀她，从此他的统治淹没在越来越多的血里。最后，在都城杜库扎，他被同父异母的兄弟丁冈和姆赫兰加纳杀死。（莫福洛 1909 年到夸杜库扎拜谒过沙卡的坟墓。）",
        ["KwaDukuza"], ["夸杜库扎"],
        "https://en.wikipedia.org/wiki/Chaka_(novel); https://www.themodernnovel.org/?p=4952; https://www.ebsco.com/research-starters/literature-and-writing/chaka-thomas-mofolo; https://www.encyclopedia.com/reference/encyclopedias-almanacs-transcripts-and-maps/chaka; https://d.lib.msu.edu/juz/492/OBJ/download; https://en.wikipedia.org/wiki/Shaka_Memorial"),
]
check(books, places, lines)
if __name__ == "__main__":
    run(books, places, lines, "add_za2.py")
