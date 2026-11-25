"""11-24: Egypt, the 21 books that selection rule v2 adds (tools/selection/eg.md); The Alchemist is already in the app
(data/ma, Tangier) and gets its Egyptian line here. Scene notes in our own words (all in copyright). Places, with the reason
for each:
- Zayni Barakat, The Thief and the Dogs, Sharaf: a city-level pin on Cairo. Zayni Barakat is a "city novel" of Mamluk Cairo
  with no single site; The Thief and the Dogs moves through Cairo and ends in an unnamed cemetery; Sharaf's prison is not
  named (each with an honest note).
- Children of the Alley, The Harafish: their alleys are imaginary (Wikipedia: The Harafish names neither place nor time);
  Mahfouz's alleys come from Gamaliya, his childhood quarter (NYRB, The Nation), so both hang on the existing Naguib
  Mahfouz Museum in Gamaliya, as Midaq Alley already does.
- Return of the Spirit (al-Sayyida Zaynab, Cairo, 1918-19; Lynne Rienner edition) and The Lamp of Umm Hashim: the Mosque
  of Sayyida Zaynab.
- Azazeel (Hypatia's killing), No One Sleeps in Alexandria, Rama and the Dragon: the existing city pin on Alexandria.
  For Rama and the Dragon no source names the city; it is pinned at Alexandria, al-Kharrat's birthplace (honest note).
- Woman at Point Zero: Qanatir women's prison (Qanater Prison Complex).
- The Heron: Kit Kat, Imbaba (pin: Imbaba).
- The Open Door: Port Said, the centre of the action in 1956.
- Seeds of Corruption: set around Mount Darhib in the Eastern Desert near the Sudanese border; Darhib has no coordinates in
  Wikipedia or Wikidata, so the book is pinned at Humaithara (shrine of Abu al-Hasan al-Shadhili), which lay on the
  journey through the Eastern Desert, with the Ababda and the mining companies, that Moussa says inspired the novel
  (Wikidata coordinates; honest note).
- The Days: the village of al-Kilo (Izbet el Kilo) near Maghagha, Minya; the village has no coordinates, so the pin is
  Maghagha (Arabic Wikipedia: "the village of al-Kilo near Maghagha").
- The Call of the Curlew: Amna's village, Beni Warkan, could not be placed; the novel is set in the Upper Egyptian
  countryside, so it shares the Maghagha pin with The Days, near Taha Hussein's own village (honest note). The Taha
  Hussein Museum in Giza was considered as a pilgrimage place, but Commons has no freely licensed photo of it (its only
  file was copied from a company website), and pilgrimage places must have one.
- Sunset Oasis: Siwa Oasis.
- War in the Land of Egypt: the village is unnamed, near the Delta town of Tanta (Daily News Egypt); pin: Tanta.
- The English Patient: the Cave of Swimmers, where Almásy leaves Katharine.
- The Alchemist: the existing Great Pyramid of Giza, where Santiago digs.
- The Egyptian: Thebes, where Sinuhe grows up and where the last battle is fought.
Photos: tools/content/batches/add_photos_eg_1124.py.

Usage: python3 -I tools/content/batches/add_eg2.py <app_dir> tools/content/batches/coords/add_eg2.json"""
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
def check(books, places, lines, ext=(), old_places=()):
    """ext: books already in the app (another country's books.js) that get a line here; old_places: existing places
    that get lines here. Every book has a line; every new place has a line."""
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    new = {x["id"] for x in books}
    assert not new & allb, new & allb
    assert set(ext) <= allb, set(ext) - allb
    have = ids_in(b.data("places.js"))
    assert not {p["id"] for p in places} & have and {p["id"] for p in places} == set(CO)
    assert set(old_places) <= have, set(old_places) - have
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    bk, pl = new | set(ext), {p["id"] for p in places} | set(old_places)
    for l in lines:
        assert l["book_id"] in bk and l["place_ids"][0] in pl, l["id"]
    assert {l["book_id"] for l in lines} == bk
    assert {l["place_ids"][0] for l in lines} == pl
    for p in places:
        for x in p.get("book_ids") or []: assert x in bk | allb, (p["id"], x)
def run(books, places, lines, script):
    M = f"11-24: Egypt, books that selection rule v2 adds (tools/content/batches/{script})"
    for name, xs in (("books.js", books), ("places.js", places), ("lines.js", lines)):
        if xs: b.append(b.data(name), xs, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
b.init(APP, "", "eg", DATE)
books = [
    BK("zayni-barakat", "Zayni Barakat", "宰尼·巴拉卡特", "الزيني بركات", "Gamal al-Ghitani", "杰马勒·黑托尼", "جمال الغيطاني", "1974", "ar",
       ["al-Zini Barakat", "Zayni Barakat ibn Musa", "Zakariya bin Radi", "Ghitani"]),
    BK("children-of-the-alley", "Children of the Alley", "我们街区的孩子们", "أولاد حارتنا", "Naguib Mahfouz", "纳吉布·马哈福兹", "نجيب محفوظ",
       "1959", "ar", ["Children of Gebelawi", "Awlad Haretna", "Gebelawi", "Gabalawi", "Adham"]),
    BK("return-of-the-spirit", "Return of the Spirit", "灵魂归来", "عودة الروح", "Tawfiq al-Hakim", "陶菲格·哈基姆", "توفيق الحكيم", "1933", "ar",
       ["The Return of the Spirit", "Awdat al-Ruh", "Muhsin", "Saniya"]),
    BK("azazeel", "Azazeel", "阿撒兹勒", "عزازيل", "Youssef Ziedan", "优素福·齐丹", "يوسف زيدان", "2008", "ar",
       ["Azazel", "Hypa", "Hypatia"]),
    BK("woman-at-point-zero", "Woman at Point Zero", "零点女人", "امرأة عند نقطة الصفر", "Nawal El Saadawi", "纳瓦勒·赛阿达维", "نوال السعداوي",
       "1975", "ar", ["Firdaus", "Qanatir"]),
    BK("rama-and-the-dragon", "Rama and the Dragon", "拉玛与龙", "رامة والتنين", "Edwar al-Kharrat", "爱德华·哈拉特", "إدوار الخراط", "1980", "ar",
       ["Rama", "Mikhail"]),
    BK("no-one-sleeps-in-alexandria", "No One Sleeps in Alexandria", "亚历山大无人入眠", "لا أحد ينام في الإسكندرية", "Ibrahim Abdel Meguid",
       "易卜拉欣·阿卜杜勒-迈吉德", "إبراهيم عبد المجيد", "1996", "ar", ["Magd al-Din", "Dimyan", "Alexandria Trilogy"]),
    BK("seeds-of-corruption", "Seeds of Corruption", "地方的腐败", "فساد الأمكنة", "Sabri Moussa", "萨布里·穆萨", "صبري موسى", "1973", "ar",
       ["Fasad al-Amkina", "Nicola", "Darhib", "Dorhib"]),
    BK("the-heron", "The Heron", "苍鹭", "مالك الحزين", "Ibrahim Aslan", "易卜拉欣·阿斯兰", "إبراهيم أصلان", "1983", "ar",
       ["Malik al-Hazin", "Kit Kat", "Sheikh Hosni", "Yusuf al-Naggar"]),
    BK("lamp-of-umm-hashim", "The Lamp of Umm Hashim", "乌姆·哈希姆的灯", "قنديل أم هاشم", "Yahya Haqqi", "叶海亚·哈基", "يحيى حقي", "1944", "ar",
       ["Qindil Umm Hashim", "Ismail", "Fatima", "Yahya Hakki"]),
    BK("the-open-door", "The Open Door", "敞开的门", "الباب المفتوح", "Latifa al-Zayyat", "拉蒂法·扎亚特", "لطيفة الزيات", "1960", "ar",
       ["al-Bab al-Maftuh", "Layla", "Husayn"]),
    BK("call-of-the-curlew", "The Call of the Curlew", "鹬鸟的呼唤", "دعاء الكروان", "Taha Hussein", "塔哈·侯赛因", "طه حسين", "1934", "ar",
       ["Doaa al-Karawan", "The Nightingale's Prayer", "Amna", "Hanadi"]),
    BK("the-harafish", "The Harafish", "平民史诗", "ملحمة الحرافيش", "Naguib Mahfouz", "纳吉布·马哈福兹", "نجيب محفوظ", "1977", "ar",
       ["Malhamat al-Harafish", "Ashur al-Nagi", "harafish"]),
    BK("thief-and-the-dogs", "The Thief and the Dogs", "小偷与狗", "اللص والكلاب", "Naguib Mahfouz", "纳吉布·马哈福兹", "نجيب محفوظ", "1961", "ar",
       ["al-Liss wal-Kilab", "Said Mahran", "Rauf Ilwan", "Nur"]),
    BK("the-days-taha-hussein", "The Days", "日子", "الأيام", "Taha Hussein", "塔哈·侯赛因", "طه حسين", "1926–1967", "ar",
       ["al-Ayyam", "An Egyptian Childhood", "The Stream of Days", "A Passage to France", "Izbet el Kilo"]),
    BK("sunset-oasis", "Sunset Oasis", "日落绿洲", "واحة الغروب", "Bahaa Taher", "巴哈·塔希尔", "بهاء طاهر", "2007", "ar",
       ["Wahat al-Ghurub", "Mahmoud Abd el Zahir", "Catherine", "Siwa"]),
    BK("sharaf-ibrahim", "Sharaf", "沙拉夫", "شرف", "Sonallah Ibrahim", "松阿拉·易卜拉欣", "صنع الله إبراهيم", "1997", "ar",
       ["Honor", "Ashraf Abdel Aziz Suleiman", "Ramzi"]),
    BK("war-in-the-land-of-egypt", "War in the Land of Egypt", "埃及大地上的战争", "الحرب في بر مصر", "Yusuf al-Qa'id", "优素福·盖伊德",
       "يوسف القعيد", "1978", "ar", ["al-Harb fi Barr Misr", "Masri", "The Egyptian Citizen", "umda"]),
    BK("the-english-patient", "The English Patient", "英国病人", "The English Patient", "Michael Ondaatje", "迈克尔·翁达杰", "Michael Ondaatje",
       "1992", "en", ["Almásy", "Almasy", "Katharine Clifton", "Hana", "Kip", "Cave of Swimmers"]),
    BK("the-egyptian-waltari", "The Egyptian", "埃及人辛努赫", "Sinuhe egyptiläinen", "Mika Waltari", "米卡·瓦尔塔里", "Mika Waltari", "1945", "fi",
       ["Sinuhe the Egyptian", "Sinuhe", "Akhenaten", "Horemheb"]),
]
places = [
    b.ORIG("eg-sayyida-zaynab", "Mosque of Sayyida Zaynab, Cairo", "赛义达·宰娜卜清真寺，开罗", *C("eg-sayyida-zaynab"),
           "Mosque and shrine of Sayyida Zaynab, the Prophet's granddaughter, known to Cairenes as Umm Hashim, at the heart of the popular quarter that bears her name. In Yahya Haqqi's The Lamp of Umm Hashim (1944) the oil of the shrine's lamp, believed to heal the eyes, is at the centre of the story; Tawfiq al-Hakim's Return of the Spirit (1933) is set largely in the same quarter, in 1918–19",
           "赛义达·宰娜卜清真寺与圣陵，供奉先知的外孙女宰娜卜，开罗人称她“乌姆·哈希姆”，就在以她命名的平民街区中心。叶海亚·哈基的《乌姆·哈希姆的灯》（1944）里，圣陵油灯的灯油据说能治眼病，是整个故事的中心；陶菲格·哈基姆的《灵魂归来》（1933）大部分也发生在这个街区，时间是 1918 至 1919 年"),
    b.ORIG("eg-cairo", "Cairo", "开罗", *C("eg-cairo"),
           "Egypt's capital, pinned here for three novels that move through the city without one place to stand for them: Gamal al-Ghitani's Zayni Barakat (1974), a portrait of Mamluk Cairo on the eve of the Ottoman conquest of 1517; Naguib Mahfouz's The Thief and the Dogs (1961), which follows a thief just out of prison across the city to an unnamed cemetery; and Sonallah Ibrahim's Sharaf (1997), whose prison is not named. The pin is the city's point",
           "埃及首都。这里为三部在城中四处走动、找不到某一个地点能代表它们的小说标了图钉：杰马勒·黑托尼的《宰尼·巴拉卡特》（1974），写 1517 年奥斯曼征服前夕的马穆鲁克开罗；纳吉布·马哈福兹的《小偷与狗》（1961），跟着一个刚出狱的小偷穿过全城，一直走到一片没有名字的墓地；松阿拉·易卜拉欣的《沙拉夫》（1997），书里的监狱没有名字。图钉标在市中心点"),
    b.ORIG("eg-qanater-prison", "Qanatir Women's Prison", "盖纳提尔女子监狱", *C("eg-qanater-prison"),
           "Prison complex at al-Qanatir al-Khayriyya, north of Cairo, which includes a women's prison. In the autumn of 1974 the psychiatrist Nawal El Saadawi met here a woman condemned to death for killing a man, the Firdaus of Woman at Point Zero (1975); in 1981 El Saadawi was herself imprisoned here for political offences",
           "开罗以北盖纳提尔·海里耶的监狱建筑群，其中有一座女子监狱。1974 年秋，精神科医生纳瓦勒·赛阿达维在这里见到一个因杀人被判死刑的女人——她就是《零点女人》（1975）里的菲尔道斯；1981 年，赛阿达维本人也因政治罪名被关进了这里"),
    b.ORIG("eg-imbaba", "Kit Kat, Imbaba", "基特卡特，因巴巴", *C("eg-imbaba"),
           "Popular quarter on the west bank of the Nile in Giza, where Ibrahim Aslan's family settled when he was a boy and which became the setting of his fiction. His novel The Heron (1983) takes place over one long winter night in the Kit Kat neighbourhood of Imbaba, on the eve of the bread riots of January 1977; Daoud Abdel Sayed filmed it as Kit Kat (1991). The pin is Imbaba",
           "吉萨省尼罗河西岸的平民街区。易卜拉欣·阿斯兰小时候全家搬到这里，此后这里成了他小说的舞台。他的长篇《苍鹭》（1983）写的是 1977 年 1 月面包暴动前夕，因巴巴基特卡特街区一个漫长的冬夜；达乌德·阿卜杜勒-赛义德把它拍成了电影《基特卡特》（1991）。图钉标在因巴巴"),
    b.ORIG("eg-port-said", "Port Said", "塞得港", *C("eg-port-said"),
           "City at the Mediterranean mouth of the Suez Canal. In Latifa al-Zayyat's The Open Door (1960), Layla escapes an engagement by taking a teaching post here, and Port Said under the British, French and Israeli attack of 1956 becomes the centre of the novel's climax",
           "苏伊士运河地中海入口处的城市。拉蒂法·扎亚特的《敞开的门》（1960）里，莱拉为了逃开一桩婚约，申请调到这里教书；1956 年英、法、以色列进攻下的塞得港，成了小说高潮的中心"),
    b.PROTO("eg-humaithara", "Humaithara, Eastern Desert (for Mount Darhib)", "胡迈斯拉，东部沙漠（代达尔希卜山）", *C("eg-humaithara"),
            "the Eastern Desert where Sabri Moussa set Seeds of Corruption (1973), around Mount Darhib near the Sudanese border. Moussa spent a night at Darhib in 1963 and returned for years; the journey that inspired the novel, through the desert with the Ababda and the mining companies, took him to Darhib and to the shrine of Abu al-Hasan al-Shadhili at Humaithara. Darhib has no published coordinates, so the book is pinned at Humaithara, using Wikidata's coordinates",
            "萨布里·穆萨把《地方的腐败》（1973）放在东部沙漠里、靠近苏丹边境的达尔希卜山一带。穆萨 1963 年在达尔希卜山过了一夜，此后几年一再回去；启发这部小说的那趟旅程，跟着阿巴卜达人和矿业公司穿越沙漠，到过达尔希卜山，也到过胡迈斯拉的阿布·哈桑·沙兹利圣陵。达尔希卜山查不到公开的坐标，所以这本书标在胡迈斯拉，坐标取自维基数据"),
    b.ORIG("eg-maghagha", "Maghagha (for Izbet el Kilo)", "马加加（代基卢村）", *C("eg-maghagha"),
           "Town in Minya Governorate, Upper Egypt. Taha Hussein was born in 1889 in the village of al-Kilo (Izbet el Kilo) near Maghagha, blinded in early childhood, and taught to read and recite the Quran at the village kuttab; the first volume of The Days (1926–1967) is his childhood there. The village has no published coordinates, so the pin is Maghagha. His novel The Call of the Curlew (1934), set in an Upper Egyptian village that could not be placed, is pinned here too",
           "上埃及明亚省的小镇。塔哈·侯赛因 1889 年生在马加加附近的基卢村（伊兹贝特·基卢），幼年失明，在村里的私塾学会认字、背诵《古兰经》；《日子》（1926–1967）的第一卷写的就是他在那里的童年。这个村子查不到公开的坐标，所以图钉标在马加加。他的小说《鹬鸟的呼唤》（1934）发生在一个没能找到确切位置的上埃及村子，也标在这里"),
    b.ORIG("eg-siwa", "Siwa Oasis", "锡瓦绿洲", *C("eg-siwa"),
           "Oasis in Egypt's Western Desert, home in antiquity to the oracle of Amun that greeted Alexander the Great as the god's son. In Bahaa Taher's Sunset Oasis (2007), winner of the first International Prize for Arabic Fiction, the disgraced officer Mahmoud Abd el Zahir is sent here as district commissioner in the late 1890s, with his Irish wife Catherine, who is searching for the tomb of Alexander",
           "埃及西部沙漠中的绿洲，古代阿蒙神谕所在地，亚历山大大帝曾在这里被神谕称为神之子。巴哈·塔希尔获首届阿拉伯小说国际奖的《日落绿洲》（2007）里，失势的军官马哈茂德·阿卜杜勒-扎希尔在 19 世纪 90 年代末被派到这里当地区长官，同行的爱尔兰妻子凯瑟琳一心寻找亚历山大的陵墓"),
    b.ORIG("eg-tanta", "Tanta", "坦塔", *C("eg-tanta"),
           "Delta town. Yusuf al-Qa'id's War in the Land of Egypt (1978) is set in a village near Tanta on the eve of the October War of 1973, where the umda (village mayor) sends the night watchman's son to the army in place of his own. The village is unnamed; the pin is Tanta",
           "尼罗河三角洲的城镇。优素福·盖伊德的《埃及大地上的战争》（1978）发生在 1973 年十月战争前夕坦塔附近的一个村子：村长让守夜人的儿子顶替自己的儿子去当兵。村子没有名字，图钉标在坦塔"),
    b.ORIG("eg-thebes", "Thebes (Luxor)", "底比斯（卢克索）", *C("eg-thebes"),
           "Capital of Egypt in the New Kingdom, on the site of today's Luxor. In Mika Waltari's The Egyptian (1945), the physician Sinuhe, found as a baby in a reed boat on the Nile, grows up in the poor quarter of Thebes and lives through the reign of Akhenaten; the novel's final battle is fought here",
           "新王国时期的埃及都城，就在今天的卢克索。米卡·瓦尔塔里的《埃及人辛努赫》（1945）里，医生辛努赫婴儿时被人在尼罗河上一只芦苇小船里发现，在底比斯的穷人区长大，亲历了阿肯那顿的统治；小说最后一战也发生在这里"),
    b.ORIG("eg-cave-of-swimmers", "Cave of Swimmers, Gilf Kebir", "泳者洞，吉尔夫凯比尔", *C("eg-cave-of-swimmers"),
           "Cave in Wadi Sura, on the Gilf Kebir plateau in Egypt's far south-western desert, painted with prehistoric figures that seem to swim. In Michael Ondaatje's The English Patient (1992), which won the Booker Prize, Almásy leaves the injured Katharine Clifton here and sets out for help; when he returns, years later, she has long been dead",
           "埃及西南部沙漠深处吉尔夫凯比尔高原上苏拉谷的一个山洞，洞壁上有史前人物岩画，看上去像在游泳。迈克尔·翁达杰获布克奖的《英国病人》（1992）里，阿尔玛西把受了重伤的凯瑟琳·克利夫顿留在这里，自己去求救；等他多年后回来，她早已死去"),
]
lines = [
    b.S("eg-zb-1", "zayni-barakat", "eg-cairo", "The muhtasib's Cairo", "市场总监的开罗",
        "Cairo in 1516–17, in the last days of the Mamluks. Zayni Barakat ibn Musa, puritanical and enigmatic, rises to become muhtasib, the powerful inspector of the city's markets and morals, and rules the corrupt city through a web of spies and informers, alongside Zakariya bin Radi, whose story the novel tells together with his. The story is told by many voices, a Venetian traveller among them, in diary entries, police reports, decrees and proclamations, until the Mamluks fall to the Ottomans. Al-Ghitani saw in that age a parallel to the mass arrests and surveillance of Egypt in the late 1960s, and Edward Said read Zayni as a figure for Nasser. (A city novel with no single site; the pin is Cairo.)",
        "1516 至 1517 年，马穆鲁克王朝最后的日子里的开罗。清教徒般严苛、深不可测的宰尼·巴拉卡特·伊本·穆萨升任“穆赫塔西卜”——掌管全城市场与风化的权势人物，靠一张由密探和告密者织成的网统治这座腐败的城市，小说同时讲述的另一个人物是扎卡里亚·本·拉迪。故事由许多声音讲述，其中有一位威尼斯旅行者，形式有日记、警方报告、敕令和公告，一直讲到马穆鲁克败于奥斯曼人之手。黑托尼在那个时代里看到了 20 世纪 60 年代末埃及大逮捕和监视的影子，爱德华·萨义德也把宰尼读作纳赛尔的化身。（这是一部写整座城市的小说，没有某一个地点，图钉标在开罗。）",
        ["Cairo"], ["开罗"],
        "https://en.wikipedia.org/wiki/Al-Zini_Barakat; https://complete-review.com/reviews/egypt/ghitani.htm; https://www.arabbritishcentre.org.uk/resources/library/books/zayni-barakat/; https://www.target.com/p/zayni-barakat-by-gamal-al-ghitani-paperback/-/A-1002769075; https://core.ac.uk/download/492998122.pdf; https://www.egyptindependent.com/?p=2459670"),
    b.S("eg-cota-1", "children-of-the-alley", "eg-mahfouz-museum", "The alley and the Big House", "街区与大宅",
        "At the top of an alley somewhere between the old city and the desert stands the Big House of Gebelawi, the stern patriarch who is never seen. He throws out his son Idris for defying him, and then Adham for trying to read his will; generation after generation, the alley falls under the rule of bullies, and one hero after another, Gabal, Rifaa, Qassem, rises to lead the poor and oppressed, before the alley forgets and the bullies return; last comes Arafa, a magician of the modern age. The allegory of the three monotheistic faiths and of science was banned in Egypt for decades. (The alley is imaginary; Mahfouz's alleys come from Gamaliya, where he was born, and where his museum now stands.)",
        "在老城与沙漠之间的某处，一条街区的顶端立着杰巴拉维的大宅——这位严厉的家长从不露面。他先是把违抗他的儿子伊德里斯赶了出去，后来又赶走了想偷看他遗嘱的阿德哈姆；一代又一代，街区落入恶霸的统治，一个又一个英雄——贾巴勒、里法阿、卡西姆——站出来带领穷苦受压迫的人，可街区随后又会忘记，恶霸又会回来；最后出场的是阿拉法，一个现代的魔术师。这部关于三大一神教与科学的寓言，在埃及被禁了几十年。（街区是虚构的；马哈福兹笔下的小巷都来自他出生的贾马利亚区，他的博物馆如今就在那里。）",
        ["Gamaliya"], ["贾马利亚"],
        "https://en.wikipedia.org/wiki/Children_of_Gebelawi; https://www.kirkusreviews.com/book-reviews/naguib-mahfouz/children-of-the-alley/print; https://supersummary.com/children-of-gebelawi/summary; https://www.themodernnovel.org/?p=2770; https://core.ac.uk/download/268163561.pdf; https://www.nybooks.com/?p=19972"),
    b.S("eg-rots-1", "return-of-the-spirit", "eg-sayyida-zaynab", "The flat in al-Sayyida Zaynab", "赛义达·宰娜卜区的公寓",
        "Cairo, from the influenza epidemic of 1918 to the revolution of March 1919. Muhsin, a schoolboy from a wealthy rural family near Damanhur, lives in a crowded flat in the quarter of al-Sayyida Zaynab with his uncles and his aunt, a household of bachelors who all, one by one, fall for their beautiful neighbour Saniya, while Saniya falls for someone else. Their rivalries and quarrels give way when the revolution against British rule breaks out and they join it together, a picture, for al-Hakim, of the Egyptian spirit's awakening. Al-Hakim wrote the novel in Paris in 1927; after reading it, the young Nasser became a great admirer of its author.",
        "开罗，从 1918 年的流感大流行一直到 1919 年 3 月的革命。来自达曼胡尔附近富裕乡绅家庭的中学生穆赫辛，和几个叔叔、一个姑姑挤住在赛义达·宰娜卜区的一套公寓里——这一屋子单身汉一个接一个爱上了美丽的女邻居萨尼娅，而萨尼娅爱上的却是另一个人。反抗英国统治的革命爆发了，他们之间的争风吃醋随之退场，一家人一起投身革命——在哈基姆看来，这正是埃及精神的苏醒。哈基姆 1927 年在巴黎写成此书；年轻的纳赛尔读过之后，成了作者的忠实崇拜者。",
        ["al-Sayyida Zaynab"], ["赛义达·宰娜卜"],
        "https://www.rienner.com/uploads/4fce7d55764d5.pdf; https://en.wikipedia.org/wiki/The_Return_of_the_Spirit_(novel); https://qantara.de/en/article/book-review-tawfiq-al-hakim’s-return-spirit-awaiting-day-resurrection; https://greatwarreading.blogspot.com/2016/04/the-retrun-of-spirit.html; https://lithub.com/the-writer-and-the-dictator-a-love-hate-story/; https://www.cambridge.org/core/product/AFDC06DF1B7D099440F4B8E0C0295BD5/core-reader"),
    b.S("eg-az-1", "azazeel", "eg-alexandria", "The death of Hypatia", "希帕提娅之死",
        "Hypa, a Coptic monk and physician from Upper Egypt, writes his life on parchment scrolls in a monastery north of Aleppo in AD 431, urged on by Azazeel, the devil within him. As a boy near Akhmim he had seen his father lynched by Christians; as a young man he goes to Alexandria to study medicine, is warned not to wear his monk's habit in the troubled city, and there sees the philosopher Hypatia, whose name he will take, dragged through the streets by a mob of Christians and killed. Fleeing to Jerusalem and Syria, he is drawn into the church quarrels of the age and into temptations of his own. The novel won the International Prize for Arabic Fiction in 2009 and was fiercely condemned by many Copts.",
        "科普特僧侣兼医生希帕来自上埃及。公元 431 年，他在阿勒颇以北的一座修道院里，在他心中的魔鬼阿撒兹勒的催促下，把自己的一生写在羊皮纸卷上。少年时，他在艾赫米姆附近看见父亲被基督徒私刑处死；年轻时他去亚历山大学医，有人提醒他在这座动荡的城市里别穿僧袍，而正是在那里，他看见哲学家希帕提娅——他后来用了她的名字——被一群基督徒拖过街道、活活杀死。他逃到耶路撒冷和叙利亚，卷进那个时代教会的纷争，也卷进自己的诱惑。这部小说获得 2009 年阿拉伯小说国际奖，也遭到许多科普特人的强烈谴责。",
        ["Alexandria"], ["亚历山大"],
        "https://www.bidoun.org/articles/azazeel-beelzebub; https://www.themodernnovel.org/asia/arab/egypt/youssef-ziedan/azazeel/; https://www.banipal.co.uk/book_reviews/95/azazeel/; https://www.egyptindependent.com/?p=1704; https://www.irishtimes.com/culture/books/azazeel-by-youssef-ziedan-1.1436623; https://www.irishexaminer.com/lifestyle/arid-20192062.html"),
    b.S("eg-wpz-1", "woman-at-point-zero", "eg-qanater-prison", "The cell", "牢房",
        "In Qanatir Prison a psychiatrist researching women prisoners asks to meet Firdaus, a woman who has killed a man and is to be hanged, who has refused to appeal and refuses to see anyone. At last Firdaus agrees, and in the hours before her execution she tells her life: a childhood of poverty in a village, a youth of abuse at the hands of the men around her, a marriage she flees, the streets of Cairo, a life as a prostitute in which she learns that her body has a price, and the man, a pimp, whom she kills. She goes to her death unafraid. El Saadawi based the book on the woman she met in Qanatir in 1974, and finished it in a week.",
        "在盖纳提尔监狱，一位正在研究女囚的精神科医生请求见见菲尔道斯——她杀了一个男人，即将被绞死，她拒绝上诉，也拒绝见任何人。菲尔道斯终于答应了，在行刑前的几个小时里讲出自己的一生：乡下贫穷的童年，少女时代遭身边男人的欺凌，一场她逃离的婚姻，开罗的街头，一段让她明白自己的身体是有价钱的卖淫生涯，还有她杀死的那个男人——一个皮条客。她毫无畏惧地走向死亡。赛阿达维根据 1974 年在盖纳提尔见到的那个女人写成此书，只用了一个星期。",
        ["Qanatir"], ["盖纳提尔"],
        "https://en.wikipedia.org/wiki/Woman_at_Point_Zero; https://britannica.com/topic/Woman-at-Point-Zero; https://litcharts.com/lit/woman-at-point-zero/summary; https://www.sparknotes.com/lit/pointzero/context/; https://www.librarything.com/work/124574"),
    b.S("eg-rd-1", "rama-and-the-dragon", "eg-alexandria", "The novel as a whole", "全书",
        "A love story of unrequited passion between Mikhail, a Coptic intellectual, and Rama, a Muslim woman, told as a long dialogue between them in which past and present run together: the Egypt of the 1960s and 1970s, with memories reaching back to the 1940s, and threads of Pharaonic, Greek, Coptic and Islamic myth, the dragon among them. Their relationship stands not only for man and woman but for Copt and Muslim and for Upper and Lower Egypt. The novel won the Naguib Mahfouz Medal for Literature. (No source names a single setting for the novel; the pin is Alexandria, where al-Kharrat was born, raised and educated.)",
        "一个单恋的爱情故事：科普特知识分子米哈伊尔和穆斯林女子拉玛，全书是两人之间的一场长长的对话，过去和现在交织在一起——20 世纪 60、70 年代的埃及，回忆一直伸到 40 年代，其间穿插着法老时代、希腊、科普特和伊斯兰的神话线索，那条龙也在其中。他们的关系不只是男人和女人，也是科普特人和穆斯林、上埃及和下埃及。这部小说获得了纳吉布·马哈福兹文学奖。（找不到任何资料说明小说的具体背景地；图钉标在亚历山大——哈拉特在那里出生、长大、受教育。）",
        ["Alexandria"], ["亚历山大"],
        "https://en.wikipedia.org/wiki/Rama_and_the_Dragon; https://www.storytel.com/in/books/rama-and-the-dragon-1403963; https://www.everand.com/book/382877050/Rama-and-the-Dragon; https://abjjad.com/book/15445969; https://en.wikipedia.org/wiki/Edwar_al-Kharrat"),
    b.S("eg-nosia-1", "no-one-sleeps-in-alexandria", "eg-alexandria", "Alexandria under the sirens", "警报声中的亚历山大",
        "Alexandria during the Second World War. Sheikh Magd al-Din, a devout Muslim peasant driven out of his village in the north of Egypt, comes to the city with his wife Zahra and finds a friend as close as a brother in Dimyan, a Copt with roots in the south. Around their friendship the novel gathers the lives of an assortment of Egyptians, Muslims and Copts, northerners and southerners, men and women, settling in the city, while the war comes nearer: air-raid sirens send the neighbours running in the dark, and some of the characters' stories reach out to the desert battlefields at the edge of the war.",
        "二战期间的亚历山大。虔诚的穆斯林农民谢赫马吉德丁被逐出埃及北部的家乡村庄，带着妻子扎赫拉来到这座城市，在来自南方的科普特人迪米扬身上找到了一个亲如兄弟的朋友。围绕这份友谊，小说聚拢起一群在这座城市安家的埃及人的生活——穆斯林和科普特人，北方人和南方人，男人和女人——而战争正一步步逼近：防空警报一响，邻居们就在黑暗中奔逃，一些人物的故事一直延伸到战争边缘的沙漠战场。",
        ["Alexandria"], ["亚历山大"],
        "https://www.everand.com/book/382877133/No-One-Sleeps-in-Alexandria; https://storytel.com/in/books/no-one-sleeps-in-alexandria-1404273; https://www.arabbritishcentre.org.uk/?p=23052; https://www.cede.ch/it/books/?id=2373377; https://bingebooks.com/book/the-anchor-book-of-modern-arabic-fiction; https://biblioteca.izt.uam.mx/vufind/Record/JSTOR_ocn873141404/Details"),
    b.S("eg-soc-1", "seeds-of-corruption", "eg-humaithara", "Mount Darhib", "达尔希卜山",
        "Nicola, a mining engineer of European background, a man without a country, comes to the Eastern Desert near the Red Sea in the years before 1952, is struck with wonder at it, and settles around Mount Darhib among the Bedouin, finding gold and digging the mountain for other metals until what he has found and how to trade in it fill his mind. Into this remote place come the corruptions of the age, the dissolute king and his court and foreign interests among them, and they ruin the people and the place alike. Nicola ends his days as a hermit on the mountain, punishing himself for his sins, and dies there alone. It was among the first Egyptian novels set wholly in the desert. (The pin is Humaithara, on the journey that inspired the novel; Darhib has no published coordinates.)",
        "尼古拉是个有欧洲背景、没有祖国的矿业工程师。1952 年以前，他来到红海边的东部沙漠，被这片沙漠迷住，在贝都因人中间、达尔希卜山一带住了下来；他找到了黄金，又在山里挖掘别的金属，直到满脑子都是自己找到的东西和怎么拿它做买卖。那个时代的种种腐败也来到了这片偏远之地——其中有荒淫的国王和他的宫廷，还有外国势力——毁掉了这里的人，也毁掉了这个地方。尼古拉最后在山上当了隐士，折磨自己来赎罪，孤零零地死在那里。这是最早一批完全以沙漠为背景的埃及小说之一。（图钉标在启发这部小说的那趟旅程经过的胡迈斯拉；达尔希卜山查不到公开坐标。）",
        ["Humaithara"], ["胡迈斯拉"],
        "https://muse.jhu.edu/article/203341; https://arablit.org/2018/03/03/corruptions-of-places-between-the-cracks-of-wisdom-and-overwhelming-tragedy/; https://bookmate.com/books/BOmuC1W4; https://en.wikipedia.org/wiki/Seeds_of_Corruption; https://www.safahat.org/books/74840315/121/; https://www.goodreads.com/book/show/7130935; https://www.goodreads.com/book/show/17452953"),
    b.S("eg-her-1", "the-heron", "eg-imbaba", "Sheikh Hosni's bicycle", "谢赫胡斯尼的自行车",
        "One long winter night in the Kit Kat neighbourhood of Imbaba, on the eve of the bread riots of January 1977. Yusuf al-Naggar, a writer, watches the men and women of the quarter, waiting like herons on the bank of the Nile while their chances swim past, and wants to turn them into the characters of a novel. Among them is the blind, long-winded Sheikh Hosni, who rides a bicycle all the way from Kit Kat, and, to the crowd's delight and horror, sails straight on across the street and into the river. Daoud Abdel Sayed filmed the novel as Kit Kat (1991).",
        "1977 年 1 月面包暴动前夕，因巴巴基特卡特街区一个漫长的冬夜。作家优素福·纳贾尔看着街区里的男男女女——他们像尼罗河岸边的苍鹭一样等待着，眼看机会从面前游过——想把他们写进一部小说。其中有个瞎眼、话多的谢赫胡斯尼，他从基特卡特一路骑着自行车过来，在众人又惊又乐的围观下，径直冲过街道，连人带车冲进了河里。达乌德·阿卜杜勒-赛义德把小说拍成了电影《基特卡特》（1991）。",
        ["Kit Kat"], ["基特卡特"],
        "https://www.barnesandnoble.com/w/heron-ibrahim-aslan/1102393597; https://www.jadaliyya.com/Details/25106; https://www.banipal.co.uk/book_reviews/22/zuzana-kratka-reviews-two-novels-by-ibrahim-aslan/; https://en.wikipedia.org/wiki/Ibrahim_Aslan; https://www.jadaliyya.com/Author/3043"),
    b.S("eg-loh-1", "lamp-of-umm-hashim", "eg-sayyida-zaynab", "The lamp of the shrine", "圣陵的油灯",
        "Ismail grows up in the precincts of the shrine of Sayyida Zaynab, Umm Hashim, among people who trust in her blessing. Sent to England, he spends seven years studying ophthalmology and comes home a modern doctor. He finds his cousin Fatima, his promised bride, with trachoma growing worse, and his family treating her eyes with oil from the lamp of Umm Hashim, given them by the imam of the mosque. Enraged at what he sees as superstition, he turns on the lamp and on the faith of the quarter, and his scientific treatment fails. Only when he returns to the people of the quarter and joins his science to their faith does he heal Fatima, and he goes on to practise among the poor of the district.",
        "伊斯梅尔在赛义达·宰娜卜——乌姆·哈希姆——的圣陵周边长大，身边的人都相信她的赐福。他被送到英国，学了七年眼科，回来时成了一名现代医生。他发现自己的未婚妻、表妹法蒂玛的沙眼越来越重，家里人却在用清真寺伊玛目给的乌姆·哈希姆圣灯的灯油给她治眼睛。他认定这是迷信，勃然大怒，矛头指向那盏灯，也指向整个街区的信仰，而他的科学疗法却失败了。直到他重新回到街区的人们中间，把科学同他们的信仰结合起来，才治好了法蒂玛，此后便留在这个区为穷人行医。",
        ["Sayyida Zaynab"], ["赛义达·宰娜卜"],
        "https://complete-review.com/reviews/egypt/hakkiy.htm; https://www.everand.com/book/382877037/The-Lamp-of-Umm-Hashim-And-Other-Stories; https://edizionicafoscari.it/media/pdf/books/978-88-6969-599-5/978-88-6969-599-5-ch-03.pdf; https://edizionicafoscari.it/media/pdf/books/978-88-6969-599-5/978-88-6969-599-5-ch-01.pdf; https://mol7saat.blogspot.com/2025/08/the-lamp-of-umm-hashim-by-yahya-haqqi.html"),
    b.S("eg-od-1", "the-open-door", "eg-port-said", "Port Said, 1956", "1956 年的塞得港",
        "The novel opens on 21 February 1946, a day of mass demonstrations against the British, and follows Layla, a girl of a middle-class Cairo family, through ten years of political and personal coming of age, from student protests that set her against her conservative father to an engagement with a cold, correct professor, Dr Ramzi, which she does not dare to break. She gets herself transferred to a teaching post in Port Said; when Nasser nationalises the Suez Canal and Britain, France and Israel attack in 1956, the city becomes the centre of the action. There, in the resistance, she takes off her engagement ring, takes up arms, and opens herself to love with Husayn, her brother Mahmud's friend.",
        "小说开篇是 1946 年 2 月 21 日，那天爆发了反英大示威。故事跟着开罗中产家庭的女孩莱拉，走过十年政治上和个人的成长：学生抗议让她和守旧的父亲起了冲突；后来她和一位冷淡刻板的教授拉姆齐博士订了婚，却不敢解除婚约。她设法调到塞得港去教书；1956 年纳赛尔把苏伊士运河收归国有，英、法、以色列随即进攻，这座城市成了全书的中心。就在那里，在抵抗运动中，她摘下了订婚戒指，拿起了枪，也向哥哥马哈茂德的朋友侯赛因敞开了心扉。",
        ["Port Said"], ["塞得港"],
        "https://www.cse.iitk.ac.in/users/amit/books/al-zayyat-2002-open-door-albab.html; https://www.powells.com/book/open-door-9789774246982; https://rebeccamakkai.substack.com/p/the-feminist-egyptian-novel-that; https://u.osu.edu/arabic2241/?p=253; https://en.wikipedia.org/wiki/The_Open_Door_(al-Zayyat_novel); https://www.kirkusreviews.com/book-reviews/latifa-al-zayyat/the-open-door-2/print"),
    b.S("eg-cotc-1", "call-of-the-curlew", "eg-maghagha", "The curlew's cry", "鹬鸟的叫声",
        "Amna, a girl from the Upper Egyptian village of Beni Warkan, tells her own story. Driven from the village by the shame her father brought on the family, she, her sister Hanadi and their mother Zahra find work as servants in town, Hanadi in the house of a young irrigation engineer, who seduces her. On the road home their uncle stops in the dark and kills Hanadi to 'restore the family's honour', and as Amna watches her sister die she hears the cry of a curlew overhead. She vows revenge on the engineer, the real killer, and enters his house as a servant; but the hunter comes to love her prey, and when he asks to marry her, the curlew calls again. (Beni Warkan could not be placed; the pin is Maghagha, in the Upper Egyptian countryside near Taha Hussein's own village.)",
        "故事由阿姆娜自己讲述，她来自上埃及的贝尼·瓦尔坎村。父亲给家里招来了耻辱，她和姐姐哈娜迪、母亲扎赫拉被赶出村子，到镇上给人当用人，哈娜迪进了一位年轻水利工程师的家，被他诱骗。在回乡的路上，舅舅在黑暗中停下来，以“挽回家族名誉”为由杀了哈娜迪；阿姆娜看着姐姐死去，听见头顶传来一声鹬鸟的叫声。她发誓要向真正的凶手——那位工程师——复仇，扮作用人进了他的家；可复仇者却爱上了她要报复的人，当他向她求婚时，鹬鸟又叫了起来。（贝尼·瓦尔坎村没能找到确切位置；图钉标在马加加——上埃及乡间，塔哈·侯赛因自己的村子附近。）",
        ["Maghagha"], ["马加加"],
        "https://en.wikipedia.org/wiki/Doaa_al-Karawan_(novel); https://www.themodernnovel.org/?p=24478; https://arablit.org/2016/03/04/friday-films-a-nightingales-prayer/; https://enterpriseam.com/egypt/?p=660187; https://www.readfy.com/en/ebooks/665305-the-call-of-the-curlew/"),
    b.S("eg-har-1", "the-harafish", "eg-mahfouz-museum", "Ashur al-Nagi", "阿舒尔·纳吉",
        "The epic of a family of the harafish, the common people of an alley, across a dozen generations. It begins with Ashur al-Nagi, a foundling who grows into a strong and just leader of the alley; when plague strikes he flees with his wife Fulla to the caves of the foothills, and returns to rule with fairness, until one day he vanishes. His descendants follow him as clan chiefs, some benefactors of the poor and others tyrants, and the alley swings between justice and corruption, until at last a descendant of the same name restores Ashur's way. Neither the alley's city nor the time is ever named. (The pin is the Mahfouz museum in Gamaliya, the quarter whose alleys run through his fiction.)",
        "一个“平民”（哈拉菲什）家族跨越十几代人的史诗。故事从阿舒尔·纳吉开始：这个弃儿长大后成了街区强壮而公正的头领；瘟疫来袭时，他带着妻子富拉逃到山脚下的洞穴里，回来后公正地治理街区，直到有一天他消失了。他的后代一个接一个当上帮派头领，有的造福穷人，有的成了暴君，街区就在公正和腐败之间来回摇摆，直到最后，一个同名的后代恢复了阿舒尔的做法。书里从没写明街区在哪座城市，也没写明年代。（图钉标在贾马利亚区的马哈福兹博物馆——这片老城区的小巷贯穿了他的小说。）",
        ["Gamaliya"], ["贾马利亚"],
        "https://en.wikipedia.org/wiki/The_Harafish; https://www.lrb.co.uk/v16/n14/amit-chaudhuri/on-holiday; https://www.nybooks.com/?p=19972; https://www.thenation.com/article/archive/naguib-mahfouz-world/tnamp/"),
    b.S("eg-tad-1", "thief-and-the-dogs", "eg-cairo", "Among the graves", "坟墓之间",
        "After four years in prison, the thief Said Mahran walks out into a Cairo that has changed, bent on revenge. His wife Nabawiyya has married his former henchman Ilish, who betrayed him to the police; his little daughter Sana will not even shake his hand; and his mentor Rauf Ilwan, who once taught him that robbing the rich was a war on behalf of the poor, is now a rich and powerful journalist in a grand house. Said's attempts at vengeance go wrong and kill innocent men instead, and the newspapers make him a hunted celebrity. Sheltered by Nur, a prostitute who loves him, in a small flat by a cemetery, and by a Sufi sheikh, he is at last cornered among the graves, and the dogs of the title become real police dogs.",
        "在牢里关了四年之后，小偷赛义德·迈赫兰走进一个已经变了样的开罗，一心复仇。他的妻子纳巴维娅嫁给了出卖他、向警察告密的从前的手下伊利什；年幼的女儿萨娜连手都不肯跟他握；而他的导师拉乌夫·伊勒万——当年曾教他抢劫富人就是替穷人打仗——如今住在豪宅里，成了有钱有势的记者。赛义德的复仇一次次失手，打死的反倒是无辜的人，报纸把他捧成了被追捕的名人。爱他的妓女努尔把他藏在墓地旁的小公寓里，一位苏菲派长老也收留过他，最后他在坟墓之间被围堵，书名里的“狗”变成了真正的警犬。",
        ["Cairo"], ["开罗"],
        "https://www.bibalex.org/libraries/bigread/sec/ThiefAndDogs_en.aspx; https://www.supersummary.com/the-thief-and-the-dogs/summary; https://www.gradesaver.com/the-thief-and-the-dogs/study-guide/summary; https://www.gradesaver.com/the-thief-and-the-dogs/wikipedia/introduction; https://www.supersummary.com/the-thief-and-the-dogs/chapters-14-18-summary; https://www.publishersweekly.com/9780385264617"),
    b.S("eg-days-1", "the-days-taha-hussein", "eg-maghagha", "An Egyptian Childhood", "埃及的童年",
        "Told in the third person about 'our friend', the first volume follows a boy in a small village in Upper Egypt in the 1890s who has lost his sight in early childhood through an ignorant remedy, and who learns to know the world by touch and sound: the fence at the end of the yard, the canal, the village kuttab where he learns the Quran by heart. Clever and proud, he wins a place at al-Azhar, and at thirteen sets out for Cairo; the second volume is his rebellion against the teachers and traditions of al-Azhar, the third his years at the new Cairo University and in France. (The village is al-Kilo, near Maghagha; the pin is Maghagha.)",
        "全书用第三人称讲“我们的朋友”。第一卷写 19 世纪 90 年代上埃及一个小村子里的男孩：他幼年因为庸医的土方失明，靠触摸和声音认识世界——院子尽头的篱笆，水渠，还有他背会《古兰经》的村塾。他聪明又骄傲，考进了爱资哈尔，十三岁那年动身去开罗；第二卷写他对爱资哈尔的老师和传统的反叛，第三卷写他在新办的开罗大学和在法国的岁月。（村子是马加加附近的基卢村；图钉标在马加加。）",
        ["Maghagha"], ["马加加"],
        "https://en.wikipedia.org/wiki/The_Days_(book); https://www.encyclopedia.com/arts/culture-magazines/egyptian-childhood; https://en.wikipedia.org/wiki/Taha_Hussein; https://ar.wikipedia.org/wiki/طه_حسين; https://www.barnesandnoble.com/w/the-days-taha-hussein/1147698971; https://www.universalis.fr/encyclopedie/le-livre-des-jours/"),
    b.S("eg-so-1", "sunset-oasis", "eg-siwa", "Siwa, the late 1890s", "19 世纪 90 年代末的锡瓦",
        "In the late 1890s, Mahmoud Abd el Zahir, an Egyptian police officer disgraced for his sympathy with the revolt of Ahmed Urabi, is sent as district commissioner to the remote oasis of Siwa, knowing that two of his predecessors were murdered. His Irish wife Catherine insists on coming, obsessed with finding the tomb of Alexander the Great, the conqueror whom the oracle of Amun at Siwa once named the son of the god. In the oasis Mahmoud is caught between two warring factions, while Catherine, digging among its ruins, alienates the whole community. One chapter is told by Alexander himself. The novel won the first International Prize for Arabic Fiction, in 2008.",
        "19 世纪 90 年代末，埃及警官马哈茂德·阿卜杜勒-扎希尔因同情艾哈迈德·奥拉比起义而失势，被派到偏远的锡瓦绿洲当地区长官——他知道自己的两任前任都被人杀了。他的爱尔兰妻子凯瑟琳执意同行，她一心想找到亚历山大大帝的陵墓——当年锡瓦的阿蒙神谕曾称这位征服者为神之子。在绿洲里，马哈茂德夹在两个敌对的派系之间，而凯瑟琳在废墟中四处挖掘，得罪了整个社群。书里有一章由亚历山大本人讲述。这部小说获得 2008 年首届阿拉伯小说国际奖。",
        ["Siwa"], ["锡瓦"],
        "https://www.omanobserver.om/article/1140936/opinion/oman/sunset-oasis-is-a-brilliantly-imagined-tale; https://wob.com/de-ch/buecher/bahaa-taher/sunset-oasis/9780340998601; https://www.fantasticfiction.com/t/bahaa-taher/sunset-oasis.htm; https://dailynewsegypt.com/2008/03/20/arabic-booker-winner-paints-an-oasis-of-memories/; https://www.hachette.co.uk/titles/bahaa-taher/sunset-oasis/9780340924884/; https://www.abebooks.com/9780340998601/Sunset-Oasis-0340998601/plp"),
    b.S("eg-sha-1", "sharaf-ibrahim", "eg-cairo", "Inside the prison", "监狱里",
        "Ashraf, called Sharaf ('honour') by his mother, is a young man in his early twenties from a middle-class family, his life bent out of shape by the economic opening of the Sadat and Mubarak years. Wandering an expensive shopping centre and then an expensive cinema, he meets a foreigner who tries to take advantage of him, and kills him; he says it was self-defence, but he is pressed into a confession and sent to prison. There he learns a new world with laws of its own and tries to rise in its hierarchy, while other prisoners' stories, among them that of Dr Ramzi, open out into the history of Egypt from Nasser to Mubarak. The novel ends without an ending. (The prison is not named; the pin is Cairo.)",
        "阿什拉夫，母亲叫他“沙拉夫”（意为“荣誉”），二十出头，出身中产家庭，萨达特和穆巴拉克时代的经济开放把他的生活扭曲变了形。他先在一家高档商场闲逛，又走进一家高档影院，在那里遇到一个想占他便宜的外国人，杀了对方；他说那是自卫，却被逼着认了罪，送进监狱。他在狱中认识了一个自有一套法则的新世界，想在其中往上爬，而其他囚犯——其中有拉姆齐博士——的故事，则铺展成从纳赛尔到穆巴拉克的埃及历史。小说没有结局。（书里的监狱没有名字；图钉标在开罗。）",
        ["Cairo"], ["开罗"],
        "https://en.wikipedia.org/wiki/Sharaf_(novel); https://www.wikipedia.com/wiki/Sharaf_(novel); https://forage-86j.pages.dev/book/438592; https://stream.sooner.de/en/id/1972094000109239129/sharaf; https://cambridge.org/core/books/sonallah-ibrahim/prison-of-dishonour-sharaf-1997/A17AD7D2C7B71C537FD5323D112D0D84"),
    b.S("eg-wle-1", "war-in-the-land-of-egypt", "eg-tanta", "The village near Tanta", "坦塔附近的村子",
        "On the eve of the October War of 1973, in a village near the Delta town of Tanta, the umda, the wealthy and corrupt village mayor who owns the land and, as one character says, everyone who lives on it, learns that his youngest son has been drafted. He persuades his poor night watchman to send his own son, Masri, a brilliant young peasant whose name means 'Egyptian', to the army in his son's place under his son's name. The impersonation goes wrong in a tragicomedy of corruption and bureaucracy: Masri is killed in the war, and an investigator tries to make sense of the crime. The story is told in turn by six voices, from the umda to the investigator. The novel was banned in Egypt until 1985.",
        "1973 年十月战争前夕，在三角洲城镇坦塔附近的一个村子里，村长——这个富有而腐败的人拥有这里的土地，用书中一个人物的话说，也拥有住在这片土地上、在上面干活的每一个人——得知自己最小的儿子被征召入伍。他说服家里贫穷的守夜人，让守夜人的儿子马斯里——一个聪明的年轻农民，名字的意思就是“埃及人”——冒用他儿子的名字去当兵。冒名顶替在一出腐败与官僚主义的悲喜剧中出了差错：马斯里死在了战场上，一位调查员试图弄清这桩罪行。故事由六个声音轮流讲述，从村长一直到调查员。这部小说在埃及被禁，直到 1985 年才解禁。",
        ["Tanta"], ["坦塔"],
        "https://www.dailynewsegypt.com/?p=109026; https://www.egyptindependent.com/?p=502328; https://dergipark.org.tr/en/download/article-file/2569630; https://www.kirkusreviews.com/book-reviews/a/yusuf-al-qaid-2/war-in-the-land-of-egypt-2; https://www.barnesandnoble.com/w/war-in-the-land-of-egypt-ysuf-al-qaid/1013448461; https://en.wikipedia.org/wiki/War_in_the_Land_of_Egypt"),
    b.S("eg-ep-1", "the-english-patient", "eg-cave-of-swimmers", "The Cave of Swimmers", "泳者洞",
        "In an Italian villa at the end of the Second World War, a nurse, Hana, cares for a patient burned beyond recognition, who remembers the desert. He is Almásy, a Hungarian explorer, who in the 1930s joined a British expedition in the Libyan desert and fell in love with Katharine Clifton as she read Herodotus aloud by the fire. When her husband Geoffrey learns of their affair, he flies a plane with Katharine aboard into Almásy's camp; Geoffrey is killed and Katharine badly hurt. Almásy carries her to the Cave of Swimmers, leaves her there, and walks for help to the British post at El Tag, where the British will not listen to him. When he comes back years later she is long dead; he flies her body out, and the plane catches fire. The novel won the Booker Prize in 1992.",
        "二战结束时的一座意大利别墅里，护士汉娜照料着一个烧得面目全非、心里只记得沙漠的病人。他是匈牙利探险家阿尔玛西：20 世纪 30 年代，他加入英国人在利比亚沙漠的考察队，在篝火边听凯瑟琳·克利夫顿朗读希罗多德，爱上了她。她的丈夫杰弗里得知两人的私情，驾着载有凯瑟琳的飞机撞向阿尔玛西的营地；杰弗里当场身亡，凯瑟琳身受重伤。阿尔玛西把她抱进泳者洞，留在那里，徒步到英国人驻扎的塔格求救，英国人却不理睬他。多年后他回来时，她早已死去；他驾机运走她的遗体，飞机却起了火。这部小说获得 1992 年布克奖。",
        ["Cave of Swimmers"], ["泳者洞"],
        "https://en.wikipedia.org/wiki/The_English_Patient; https://en.wikipedia.org/wiki/Cave_of_Swimmers"),
    b.S("eg-alc-1", "the-alchemist", "eg-great-pyramid", "Digging at the pyramids", "在金字塔下挖掘",
        "Santiago, an Andalusian shepherd, follows a recurring dream of treasure buried near the Egyptian pyramids. He crosses the Sahara with a caravan, falls in love with Fatima at an oasis, and learns from an alchemist to listen to his heart and to the Soul of the World. At last he reaches the pyramids and begins to dig; thieves beat and rob him, and when he tells them of his dream, their leader laughs and describes a dream of his own, of treasure under a sycamore in a ruined church in Spain, the very place where Santiago's journey began. He goes home, finds the treasure there, and returns to Fatima.",
        "安达卢西亚的牧羊少年圣地亚哥一再梦见埃及金字塔旁埋着宝藏，便追随这个梦出发。他跟着商队穿越撒哈拉，在一处绿洲爱上了法蒂玛，又跟一位炼金术士学会倾听自己的心和“世界之魂”。他终于来到金字塔下，开始挖掘；一伙盗贼把他打了一顿，抢走了他的东西。他说起自己的梦，盗贼头子笑了，讲起自己做过的梦：宝藏埋在西班牙一座破教堂里的一棵无花果树下——那正是圣地亚哥出发的地方。他回到家乡，在那里找到了宝藏，又回到法蒂玛身边。",
        ["pyramids"], ["金字塔"],
        "https://en.wikipedia.org/wiki/The_Alchemist_(novel)"),
    b.S("eg-egy-1", "the-egyptian-waltari", "eg-thebes", "The poor quarter of Thebes", "底比斯的穷人区",
        "Sinuhe, physician to Pharaoh, writes his life in exile after the fall and death of Akhenaten. Found as a baby in a reed boat on the Nile, he grows up in the poor quarter of Thebes, the son of a humble doctor, studies medicine in the House of Life, and becomes royal physician. His travels take him through Syria, Mitanni, Babylon, Minoan Crete and the land of the Hittites; he follows Akhenaten, the pharaoh of the one god Aten, from Thebes to his new capital, Akhetaten, and fights for him to the end in the final battle, in Thebes. Waltari's novel, published in 1945, is known for its historical accuracy and for its pessimism about human nature; Hollywood filmed it in 1954.",
        "法老的御医辛努赫在阿肯那顿倒台、死去之后，在流放中写下自己的一生。他婴儿时被人在尼罗河上的一只芦苇小船里发现，在底比斯的穷人区长大，是一位卑微医生的养子，后来在“生命之屋”学医，成了御医。他的足迹遍及叙利亚、米坦尼、巴比伦、米诺斯时代的克里特和赫梯人的土地；他追随信奉唯一神阿顿的法老阿肯那顿，从底比斯迁往新都阿赫塔顿，并在底比斯的最后一战中为他战斗到底。瓦尔塔里这部 1945 年出版的小说以历史细节的准确和对人性的悲观著称；好莱坞在 1954 年把它拍成了电影。",
        ["Thebes"], ["底比斯"],
        "https://en.wikipedia.org/wiki/The_Egyptian; https://www.britannica.com/topic/The-Egyptian; https://en.wikipedia.org/wiki/Mika_Waltari"),
]
check(books, places, lines, ext=["the-alchemist"], old_places=["eg-alexandria", "eg-mahfouz-museum", "eg-great-pyramid"])
if __name__ == "__main__":
    run(books, places, lines, "add_eg2.py")
