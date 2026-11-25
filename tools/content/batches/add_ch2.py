"""11-24: Switzerland, second pack: books that selection rule v2 adds (tools/selection/ch.md). All three are in copyright:
scene notes in our own words.
- The Pledge: Mägendorf is invented ("a small place near Zurich") and the petrol station is unnamed; the frame story begins
  in Chur, where the narrator gives a lecture, and the main places lie along the road from Chur to Zurich. Hung at Chur.
- I'm Not Stiller: Zurich, where the man who calls himself White is held in the remand prison and writes his notebooks.
- Belle du Seigneur: Geneva and the League of Nations, 1935-1936.
Photos: tools/content/batches/add_photos_ch_no_se_1124.py.

Usage: python3 -I tools/content/batches/add_ch2.py <app_dir> tools/content/batches/coords/add_ch2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], (json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else {})
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
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    have = ids_in(b.data("places.js"))
    assert not {p["id"] for p in places} & have and {p["id"] for p in places} == set(CO)
    assert set(old_places) <= have, set(old_places) - have
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    pl = {p["id"] for p in places} | set(old_places)
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in pl, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == pl
b.init(APP, "", "ch", DATE)
books = [
    BK("the-pledge", "The Pledge", "承诺", "Das Versprechen", "Friedrich Dürrenmatt", "迪伦马特", "Friedrich Dürrenmatt", "1958", "de",
       ["Das Versprechen", "Requiem auf den Kriminalroman", "Matthäi", "Kommissar Matthäi", "Gritli Moser", "Mägendorf", "Durrenmatt"]),
    BK("im-not-stiller", "I'm Not Stiller", "我不是施蒂勒", "Stiller", "Max Frisch", "马克斯·弗里施", "Max Frisch", "1954", "de",
       ["Stiller", "Anatol Ludwig Stiller", "James Larkin White", "Julika"]),
    BK("belle-du-seigneur", "Belle du Seigneur", "魂断日内瓦", "Belle du Seigneur", "Albert Cohen", "阿尔贝·科恩", "Albert Cohen", "1968", "fr",
       ["Her Lover", "Solal", "Ariane", "Ariane Deume", "Adrien Deume"]),
]
places = [
    b.ORIG("ch-chur", "Chur", "库尔", *C("ch-chur"),
           "Capital of Graubünden. Friedrich Dürrenmatt's The Pledge (1958) begins here: the narrator, a writer, comes to Chur to lecture on the art of the crime novel, and a former commander of the Zurich cantonal police drives him back to Zurich the next day. The story he tells on the way unfolds along the road between Chur and Zurich",
           "格劳宾登州首府。迪伦马特的《承诺》（1958）从这里开始：叙述者是个作家，来库尔做讲座，讲侦探小说的写法；第二天，苏黎世州警察局的前局长开车送他回苏黎世，路上讲的那个故事，就发生在库尔和苏黎世之间的这条路沿线"),
    b.ORIG("ch-zurich", "Zurich", "苏黎世", *C("ch-zurich"),
           "Switzerland's largest city, Max Frisch's home town. In I'm Not Stiller (1954) a man travelling on an American passport as James Larkin White is held in a Zurich remand prison, accused of being the missing Zurich sculptor Anatol Ludwig Stiller, and writes the notebooks that make up most of the novel",
           "瑞士最大的城市，马克斯·弗里施的家乡。《我不是施蒂勒》（1954）里，一个持美国护照、自称詹姆斯·拉金·怀特的人被关在苏黎世的看守所里，被指认就是失踪的苏黎世雕塑家阿纳托尔·路德维希·施蒂勒；小说的大部分，就是他在狱中写的笔记"),
    b.ORIG("ch-geneva", "Geneva", "日内瓦", *C("ch-geneva"),
           "City at the end of Lake Geneva, seat of the League of Nations between the wars and Albert Cohen's home. Belle du Seigneur (1968) is set here from 1935: Solal, a high official of the League, and Ariane, the Genevan wife of one of his subordinates",
           "日内瓦湖畔的城市，两次大战之间国际联盟的所在地，也是阿尔贝·科恩生活的地方。《魂断日内瓦》（1968）从 1935 年在这里展开：国际联盟的高级官员索拉尔，和他一个下属的妻子、日内瓦姑娘阿丽亚娜"),
]
lines = [
    b.S("ch-pl-1", "the-pledge", "ch-chur", "The frame story", "框架故事",
        "A writer comes to Chur to give a lecture on the art of writing crime novels. Dr H., the former commander of the Zurich cantonal police, who was in the audience, drives him back to Zurich the next day and stops for petrol at a run-down petrol station in Graubünden, where an old man smelling of schnapps sits waiting. On the way H. tells his story: this was Matthäi, his best detective. Just before leaving for a post in Jordan, Matthäi was called to the woods near Mägendorf, a village near Zurich, where the girl Gritli Moser had been murdered, and swore to her mother that he would find the killer. Convinced that the real murderer was still free, he took over a petrol station on the road between Chur and Zurich, the road the killer drove, and waited. The killer never came; Matthäi is still waiting.",
        "一个作家应邀到库尔做讲座，讲侦探小说的写法。苏黎世州警察局前局长 H. 博士也在听众里，第二天开车送他回苏黎世，途中在格劳宾登一个破败的加油站加油——那里坐着一个满身烧酒味、一直在等着什么的老人。一路上 H. 讲起他的故事：这人就是马泰，当年他手下最好的探长。马泰正要动身去约旦赴任时，被叫到苏黎世附近麦根村的树林里——小女孩格丽特丽·莫泽在那里被杀害了。他向孩子的母亲起誓，一定找到凶手。他认定真凶仍逍遥法外，便在库尔到苏黎世的公路边——凶手常开车经过的那条路——盘下一个加油站，守株待兔。凶手始终没有来；马泰至今还在等。",
        ["Chur"], ["库尔"],
        "https://www.Deutschunddeutlich.de/contentLD/GD/GT97uVersprechen.pdf; https://www.getabstract.com/de/zusammenfassung/das-versprechen/4860; https://www.dtv.de/product/57710a88eb9d46ac9765db554b8b3fa9/pdf-download; https://bange-verlag.de/downloads/dl/file/id/100/product/0; https://www.school-scout.de/vorschau/55269/interpretation-zu-duerrenmatt-friedrich-das-versprechen.pdf; https://en.wikipedia.org/wiki/The_Pledge:_Requiem_for_the_Detective_Novel"),
    b.S("ch-st-1", "im-not-stiller", "ch-zurich", "Part one: Stiller's notes in prison", "第一部：施蒂勒的狱中笔记",
        "“I'm not Stiller!” begins the novel. A man travelling on an American passport in the name of James Larkin White is arrested at the Swiss border because he is thought to be Anatol Ludwig Stiller, a Zurich sculptor who disappeared seven years before. Held in a Zurich remand prison, he fills notebooks with wild stories of his adventures as White to prove that he is someone else, while friends, his brother and his wife Julika, who comes from Paris, all recognise him as Stiller. Julika pays bail for an outing, and they walk through Zurich and spend an afternoon on the lake.",
        "“我不是施蒂勒！”小说这样开头。一个持美国护照、名叫詹姆斯·拉金·怀特的人在瑞士边境被捕，因为人们认为他就是七年前失踪的苏黎世雕塑家阿纳托尔·路德维希·施蒂勒。关在苏黎世看守所里，他在一本本笔记里写下自己作为“怀特”的种种离奇冒险，要证明自己是另一个人；可朋友、他的哥哥，还有从巴黎赶来的妻子尤莉卡，都认出他就是施蒂勒。尤莉卡交了保释金带他出去，两人在苏黎世城里散步，又在湖上度过一个下午。",
        ["Zurich"], ["苏黎世"],
        "https://www.perlentaucher.de/buch/max-frisch/stiller.html; https://en.wikipedia.org/wiki/I%27m_Not_Stiller; https://www.ebsco.com/research-starters/literature-and-writing/im-not-stiller-analysis-major-characters; https://www.getabstract.com/de/zusammenfassung/stiller/3415; https://is.muni.cz/th/a04is/Anhang.pdf; https://www.freitag.de/autoren/ralf-klausnitzer/ritt-mit-den-fledermaeusen"),
    b.S("ch-bs-1", "belle-du-seigneur", "ch-geneva", "Part one: 1 May 1935", "第一部：1935 年 5 月 1 日",
        "Geneva, 1935. Solal, a Greek-born Jew of Cephalonia who has risen to be a high official of the League of Nations, has been dazzled at a reception by Ariane, the Genevan wife of Adrien Deume, a lazy, ambitious young Belgian official in his own department. On 1 May he slips into her room disguised as an old Jew and reads her diary, the start of a sudden, consuming passion that slowly falls apart. Around it, Adrien's parents wait all evening for Solal to come to dinner, and he never comes; and the League itself is drawn with satire as war approaches.",
        "1935 年的日内瓦。索拉尔是生在凯法利尼亚岛的希腊犹太人，已经做到国际联盟的高级官员；他在一次招待会上被阿丽亚娜迷住了——她是日内瓦人，嫁给了他部门里一个懒散又一心往上爬的比利时年轻职员阿德里安·德于姆。5 月 1 日，他扮成一个犹太老人溜进她的房间，读了她的日记；一场突如其来、吞噬一切的激情就此开始，又一点点瓦解。故事周围，阿德里安的父母整晚等索拉尔来吃饭，他始终没来；而大战将近时的国际联盟本身，也被写得满是讽刺。",
        ["Geneva"], ["日内瓦"],
        "https://fr-academic.com/dic.nsf/frwiki/200941; https://www.lalibre.be/culture/livres-bd/belle-du-seigneur-51b8ef62e4b0de6db9c78e66; https://www.nybooks.com/articles/1996/07/11/the-book-of-cohen/; https://www.universalis.fr/encyclopedie/belle-du-seigneur/; https://www.schoolmouv.fr/fiches-de-lecture/belle-du-seigneur-albert-cohen/fiche-de-lecture; https://leclaireur.fnac.com/article/cp39553-1-mois-1-classique-belle-du-seigneur-dalbert-cohen/"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_ch2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
