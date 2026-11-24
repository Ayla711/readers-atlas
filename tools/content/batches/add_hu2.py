"""11-24: Hungary, second pack: books that selection rule v2 adds (tools/selection/hu.md), as far as their places are found.
All five are scene notes in our own words. Anna Édes (Kosztolányi, d. 1936) is in the public domain, but the only full text
found (Hungarian Electronic Library) is a PDF the tools here cannot read reliably; a quotation can replace the note later.
- Abigail: the town of Árkod is invented; the Matula is modelled on the Dóczy girls' school in Debrecen (place type prototype).
- The Door: Pasarét, Budapest. Fatelessness: Budapest, where it begins and ends (the camps are outside Hungary).
- Anna Édes: Attila utca in Krisztinaváros. Celestial Harmonies: Eszterháza, the family's great palace.
Not added, no real place: Embers (the castle is unnamed) and The Tót Family (Mátraszentanna is invented). No photos yet.

Usage: python3 -I tools/content/batches/add_hu2.py <app_dir> tools/content/batches/coords/add_hu2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
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
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
b.init(APP, "", "hu", DATE)
books = [
    BK("abigel", "Abigail", "阿比盖尔", "Abigél", "Magda Szabó", "萨博·玛格达", "Szabó Magda", "1970", "hu",
       ["Abigél", "Gina Vitay", "Matula", "Árkod", "Mici Horn", "Szabo Magda"]),
    BK("the-door", "The Door", "鸽子女人", "Az ajtó", "Magda Szabó", "萨博·玛格达", "Szabó Magda", "1987", "hu",
       ["Az ajtó", "Emerence", "Emerence Szeredás", "Szabo Magda"]),
    BK("fatelessness", "Fatelessness", "无命运的人生", "Sorstalanság", "Imre Kertész", "凯尔泰斯·伊姆雷", "Kertész Imre", "1975", "hu",
       ["Sorstalanság", "Fateless", "György Köves", "Gyuri Köves", "Kertesz"]),
    BK("anna-edes", "Anna Édes", "家奴安娜", "Édes Anna", "Dezső Kosztolányi", "科斯托拉尼·德若", "Kosztolányi Dezső", "1926", "hu",
       ["Édes Anna", "Vizy", "Kornél Vizy", "Angéla Vizy", "Kosztolanyi"], pd=True),
    BK("celestial-harmonies", "Celestial Harmonies", "天堂的和谐", "Harmonia Caelestis", "Péter Esterházy", "艾斯特哈兹·彼得", "Esterházy Péter",
       "2000", "hu", ["Harmonia Caelestis", "Harmonia cælestis", "Esterházy family", "Esterhazy"]),
]
places = [
    b.PROTO("hu-doczy", "Dóczy Gimnázium, Debrecen", "多齐中学，德布勒森", *C("hu-doczy"),
            "the Matula, the strict Calvinist girls' boarding school in the invented town of Árkod in Magda Szabó's Abigail (1970). Its closed, puritan world is modelled on the Dóczy Institute for Girls in Debrecen, where Szabó was a pupil for twelve years; a memorial house and an Abigail exhibition have opened in the school",
            "萨博·玛格达《阿比盖尔》（1970）里虚构的阿尔科德镇上那所严格的加尔文宗女子寄宿学校马图拉。它那封闭、清教式的世界，以德布勒森的多齐女子学校为原型——萨博在那里读了十二年书；如今学校里开了纪念馆和《阿比盖尔》展览"),
    b.ORIG("hu-pasaret", "Pasarét, Budapest", "帕沙雷特，布达佩斯", *C("hu-pasaret"),
           "Green villa quarter in the Buda hills. Magda Szabó's The Door (1987) is set here: the writer Magda and her husband move into a new flat, and for twenty years the housekeeper Emerence, who lets no one through her own door, comes to work for them",
           "布达山间绿树成荫的别墅区。萨博·玛格达的《鸽子女人》（1987）就发生在这里：女作家玛格达和丈夫搬进一套新公寓，此后二十年，从不让任何人跨进自己家门的女管家艾米伦斯来给他们干活"),
    b.ORIG("hu-budapest", "Budapest", "布达佩斯", *C("hu-budapest"),
           "Imre Kertész's Fatelessness (1975) begins and ends here: in 1944 the fourteen-year-old György Köves is taken off a bus on his way to work outside the city and deported, and after the camps he comes home to Budapest",
           "凯尔泰斯·伊姆雷的《无命运的人生》（1975）从这里开始，也在这里结束：1944 年，十四岁的科韦什·久尔吉在去城外上工的公共汽车上被拉下来，遭到驱逐；熬过集中营之后，他又回到布达佩斯"),
    b.ORIG("hu-attila-ut", "Attila út, Krisztinaváros, Budapest", "阿提拉大街，克里斯蒂娜城，布达佩斯", *C("hu-attila-ut"),
           "Street along the foot of Castle Hill in Krisztinaváros, the quiet Buda quarter where Kosztolányi lived. In Anna Édes (1926) the Vizys live at 238 Attila utca, and almost every important event of the novel happens in the Krisztina quarter; Kosztolányi's own green-fenced house appears at the end",
           "城堡山脚下、克里斯蒂娜城里的一条街——科斯托拉尼就住在这个安静的布达街区。《家奴安娜》（1926）里，维齐夫妇住在阿提拉街 238 号，小说几乎所有重要的事都发生在克里斯蒂娜城；结尾还出现了科斯托拉尼自己那座绿篱笆的房子"),
    b.ORIG("hu-eszterhaza", "Eszterháza, Fertőd", "埃斯特哈泽宫，费尔特德", *C("hu-eszterhaza"),
           "The palace that Prince Nikolaus Esterházy built at Fertőd in the 1760s, the “Hungarian Versailles”, where Haydn lived and worked with his orchestra from 1766 to 1790. Péter Esterházy's Celestial Harmonies (2000) is a vast, part-autobiographical history of his family",
           "尼古拉·埃斯特哈兹亲王 1760 年代在费尔特德建造的宫殿，号称“匈牙利的凡尔赛”，海顿 1766 年到 1790 年和他的乐团就在这里生活、工作。艾斯特哈兹·彼得的《天堂的和谐》（2000）是一部卷帙浩繁、半自传的家族史"),
]
lines = [
    b.S("hu-ab-1", "abigel", "hu-doczy", "The novel as a whole", "全书",
        "Hungary, 1943. Gina Vitay, a general's daughter from Budapest, is sent by her father without explanation to the Matula, a strict religious boarding school in the provincial town of Árkod; he is hiding her there to keep her safe from the consequences of his own secret conspiracy. Unhappy and shut in, she is helped by a mysterious protector who signs as Abigail, after the statue of a girl in the school garden. As the war reaches the Matula, the former pupil Mici Horn, now a war widow, helps Gina escape from Árkod.",
        "1943 年的匈牙利。将军的女儿、布达佩斯姑娘维泰·吉娜被父亲不加解释地送进外省小城阿尔科德一所严格的教会寄宿学校马图拉——父亲在秘密策划一件大事，要把她藏起来，免得她受牵连。孤独压抑的吉娜得到一位神秘保护人的帮助，那人署名“阿比盖尔”，用的是校园里一尊少女雕像的名字。战火烧到马图拉时，学校的老校友、战争寡妇霍恩·米奇帮吉娜逃出了阿尔科德。",
        ["Árkod"], ["阿尔科德"],
        "https://en.wikipedia.org/wiki/Abigail_(novel); https://www.pressreader.com/uk/the-daily-telegraph-review/20200222/282020444320020; https://magyar.fazekas.hu/wp-content/uploads/2024/09/Abigel_jegyzet.pdf; https://epa.hu/04600/04620/00040/pdf/EPA04620_debreceni_szemle_2017_04_439-444.pdf; https://welovebudapest.com/2017/10/16/egy-kicsit-mi-is-matulasok-lehetunk-megnyilt-az-abigel-kiallitas/"),
    b.S("hu-dr-1", "the-door", "hu-pasaret", "The novel as a whole", "全书",
        "The novel opens with the narrator's recurring dream of a door that will not open. Magda, a writer whose work had been politically frozen, and her husband look for help in their new home in Budapest and take on Emerence Szeredás, an old woman who chooses her employers rather than the other way round and lets no one into her own flat. Over twenty years the two women, the educated writer and the proud, unbending housekeeper, become bound to each other in a struggle of love and power.",
        "小说开篇是叙述者反复做的一个梦：一扇怎么也打不开的门。作家玛格达的创作曾在政治上被“冻结”，她和丈夫在布达佩斯的新家需要帮手，雇来了塞雷达什·艾米伦斯——这位老妇人只挑她看得上的雇主，也从不让任何人进她自己的屋子。二十年间，这两个女人，一个有学问的作家，一个骄傲倔强的女管家，在爱与较劲之中彼此缠在了一起。",
        ["Budapest"], ["布达佩斯"],
        "https://www.lrb.co.uk/v27/n24/liam-mcilvanney/that-time; https://books.apple.com/gb/book/the-door/id489833146; https://bookmarkedplaces.com/the-door-by-magda-szabo/; https://europeanconservative.com/?p=39354"),
    b.S("hu-fl-1", "fatelessness", "hu-budapest", "The opening and the return", "开头与归来",
        "Budapest, 1944. Fourteen-year-old György Köves gets a day off school to see his father sign the family timber business over to the bookkeeper before leaving for labour service. Gyuri is himself assigned to work outside the city, and one day the police stop his bus and take off the Jewish workers. He is sent to Auschwitz, then to Buchenwald and Zeitz, which he tells in a calm, unknowing voice; liberated, he comes back to Budapest.",
        "1944 年的布达佩斯。十四岁的科韦什·久尔吉请了一天假不上学，看父亲去劳役营之前把家里的木材生意转给账房。久尔吉自己也被派到城外做工，一天，警察拦下他的公共汽车，把车上的犹太工人带了下来。他被送到奥斯维辛，又到布痕瓦尔德和蔡茨——他用平静而懵懂的口吻讲述这一切；获得解放后，他回到了布达佩斯。",
        ["Budapest"], ["布达佩斯"],
        "https://en.wikipedia.org/wiki/Fatelessness; https://blackwells.co.uk/bookshop/product/Fateless-by-Imre-Kertsz/9780099502524; https://caponeu.eu/cdp/novels/sorstalansag; https://www.ebsco.com/research-starters/literature-and-writing/fateless-imre-kertesz"),
    b.S("hu-ea-1", "anna-edes", "hu-attila-ut", "The novel as a whole", "全书",
        "Budapest, 1919. The novel opens as Béla Kun flies out of the country and the Soviet Republic falls. In their flat at 238 Attila utca in Krisztinaváros the civil servant Kornél Vizy and his wife Angéla, who has never kept a maid more than six months, take on Anna Édes, a maid from the country who seems the perfect servant. In the end Anna kills her mistress and master. The last chapter is a conversation in front of a green-fenced house.",
        "1919 年的布达佩斯。小说开篇，库恩·贝拉坐飞机出逃，苏维埃共和国垮台。在克里斯蒂娜城阿提拉街 238 号的公寓里，公务员维齐·科尔内尔和他那从没留住过哪个女仆半年以上的太太安吉拉，雇来了乡下来的女仆安娜——看上去是个完美的仆人。最后，安娜杀死了女主人和男主人。最后一章，是在一座绿篱笆房子前的一场对话。",
        ["Attila utca"], ["阿提拉街"],
        "https://www.complete-review.com/reviews/magyar/kosztod1.htm; https://www.mek.oszk.hu/15500/15577/fulszoveg.html; https://welovebudapest.com/cikk/2023/02/10/akarsz-e-jatszani-bejartuk-kosztolanyi-dezso-budapestjet/; https://caponeu.ffzg.unizg.hr/cdp/novels/edes-anna"),
    b.S("hu-hc-1", "celestial-harmonies", "hu-eszterhaza", "The novel as a whole", "全书",
        "A vast, part-autobiographical family history covering some seven centuries of the Esterházys, the princely family whose great palace is Eszterháza. Book one is made of numbered sentences from the life of the family; book two turns to the author's own family in the twentieth century, which in 1951 was deported to the village of Hort.",
        "一部卷帙浩繁、半自传的家族史，横跨埃斯特哈兹家族约七百年——这个亲王家族的大宫殿就是埃斯特哈泽宫。第一部由一条条编了号的句子组成，讲家族的生平；第二部转向作者自己家在二十世纪的遭遇，1951 年全家被流放到霍尔特村。",
        ["Eszterháza"], ["埃斯特哈泽宫"],
        "https://www.britannica.com/topic/Celestial-Harmonies; https://lesejury.de/media/samples/876/9783446255876_leseprobe.pdf; https://www.goodreads.com/book/show/441142; https://mandadb.hu/cikk/1256753/Majk_where_silence_lived_once; https://bookmarkedplaces.com/celestial-harmonies-by-peter-esterhazy/"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_hu2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
