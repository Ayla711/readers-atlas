"""11-04 afternoon, booklist batch 6: seven books published before 1929 with real place names in the text.
Excerpts are cut out of the Project Gutenberg files (Verne also from the French original, #800); Xu Zhimo's essay
is copied from Wikisource (1926 text, converted to simplified characters by hand, checked character by character).
Usage: python3 -I add_batch6.py <app_dir> <pg_texts_dir>"""
import importlib.util
import sys

APP, TX = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch6.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
prose, append, B, ORIG, PROTO, L, D, W, GBG = b5.prose, b5.append, b5.B, b5.ORIG, b5.PROTO, b5.L, b5.D, b5.W, b5.GBG

books = [
    B("plague-year", "A Journal of the Plague Year", "瘟疫年纪事", "Daniel Defoe", "笛福", "1722", 376),
    B("heart-of-midlothian", "The Heart of Mid-Lothian", "中洛辛郡的心脏", "Walter Scott", "司各特", "1818", 6944),
    B("pilgrims-progress", "The Pilgrim's Progress", "天路历程", "John Bunyan", "约翰·班扬", "1678", 131),
    B("sketch-book", "The Sketch-Book of Geoffrey Crayon", "见闻札记", "Washington Irving", "华盛顿·欧文", "1819–1820", 2048),
    B("people-of-the-abyss", "The People of the Abyss", "深渊里的人们", "Jack London", "杰克·伦敦", "1903", 1688),
    dict(B("around-the-world", "Around the World in Eighty Days", "八十天环游地球", "Jules Verne", "儒勒·凡尔纳", "1872", 103),
         title_orig="Le Tour du monde en quatre-vingts jours", author_orig="Jules Verne", orig_lang="fr"),
    dict(B("cambridge-i-knew", "The Cambridge I Knew", "我所知道的康桥", "Xu Zhimo", "徐志摩", "1926", 0),
         title_orig="我所知道的康桥", author_orig="徐志摩", orig_lang="zh",
         source_url="https://zh.wikisource.org/wiki/%E6%88%91%E6%89%80%E7%9F%A5%E9%81%93%E7%9A%84%E5%BA%B7%E6%A9%8B"),
]

places = [
    ORIG("aldgate", "Aldgate", "阿尔德门", 51.5153, -0.0782, "Aldgate (Wikipedia), grid ref TQ334813", W + "Aldgate",
         "The site of the City's old east gate; St Botolph's church stands just outside it, and Defoe's narrator watches the great plague pit dug in its parish in 1665",
         "伦敦城东面旧城门的所在；圣博托尔夫教堂就在门外，笛福的叙述者看着 1665 年在这个教区挖下的瘟疫大坑"),
    ORIG("old-tolbooth", "The Heart of Midlothian, Royal Mile", "皇家一英里 · 中洛辛郡之心", 55.9494, -3.1917, "Old Tolbooth, Edinburgh (Wikipedia)", W + "Old_Tolbooth,_Edinburgh",
         "A heart in the paving setts marks the entrance of the Old Tolbooth, Edinburgh's prison, demolished in 1817; the prison's nickname gave Scott his title",
         "路面石块拼成的心形标出了老监狱 Tolbooth 的入口位置，这座监狱 1817 年拆除；它的绰号成了司各特这本书的书名"),
    PROTO("bedford-gaol", "Bedford, site of the county gaol", "贝德福德 · 郡监狱旧址", 52.1342, -0.4593, "Bedford (Wikipedia), grid ref TL055495; the gaol plaque is in Silver Street, by the High Street", W + "Bedford",
          "Not named in the book: the 'Den' where the dreamer sleeps is usually read as the Bedfordshire county gaol, where Bunyan was imprisoned for preaching from 1660 to 1672 and began the book",
          "书中没有点名：做梦人躺下睡觉的“洞穴”通常被理解为贝德福德郡监狱；班扬 1660 至 1672 年因传道被关在这里，并在狱中开始写这本书"),
    ORIG("reform-club", "Reform Club, Pall Mall", "蓓尔美尔街 · 改革俱乐部", 51.5067, -0.1333, "Reform Club (The Great Britain Guide)", GBG + "reform-club/",
         "A gentlemen's club on Pall Mall, in its present building since 1841; Phileas Fogg's journey begins and ends here",
         "蓓尔美尔街上的绅士俱乐部，1841 年起使用现在的会所；福格的环球旅行从这里出发，也在这里结束"),
    ORIG("whitechapel", "Whitechapel", "白教堂区", 51.5171, -0.0766, "Whitechapel (Wikipedia), grid ref TQ335815", W + "Whitechapel",
         "A district of the East End; in 1902 Jack London put on ragged clothes and lodged here to write about the East End poor",
         "伦敦东区的一片街区；1902 年杰克·伦敦穿上破衣服住进这里，记录东区穷人的生活"),
]
def T(id, book_id, place, loc, loc_zh, orig, en, hl_orig, hl_en, translation, checked):
    for h in hl_orig:
        assert h in orig, (id, h)
    for h in hl_en:
        assert h in en, (id, h)
    return dict(id=id, book_id=book_id, place_ids=[place], location=loc, location_zh=loc_zh, text_orig=orig, text_en=en,
                highlight_en=hl_en, highlight_orig=hl_orig, translation=translation, status="draft", checked=checked)

XU = "Wikisource, 我所知道的康橋 (1926; simplified characters)" + D
lines = [
    L("ply-1", "plague-year", "aldgate", "The great pit at Aldgate", "阿尔德门的大坑",
      prose(376, "they dug the great pit in the churchyard of our", "about nine feet deep;").replace("deep;", "deep"), ["Aldgate"], 376),
    L("hm-1", "heart-of-midlothian", "old-tolbooth", "Introductory chapter", "引言章",
      prose(6944, "\"Then the Tolbooth of Edinburgh is called the Heart of Mid-Lothian?\"", "said I.") + "\n" + prose(6944, "\"So termed and reputed, I assure you.\"", "I assure you.\""),
      ["Tolbooth of Edinburgh", "Heart of Mid-Lothian"], 6944),
    L("pil-1", "pilgrims-progress", "bedford-gaol", "The First Part, opening", "第一部开篇",
      prose(131, "As I walked through the wilderness of this world", "I dreamed a dream."), ["a Den"], 131),
    L("si-1", "sketch-book", "shakespeare-birthplace", "Stratford-on-Avon", "《埃文河畔斯特拉特福》",
      prose(2048, "I had come to Stratford on a poetical pilgrimage.", "hatching its offspring in by-corners."), ["Stratford", "the house where Shakespeare was born"], 2048),
    L("si-2", "sketch-book", "poets-corner", "Westminster Abbey", "《威斯敏斯特教堂》",
      prose(2048, "I passed some time in Poet's Corner", "mere inscriptions."), ["Poet's Corner"], 2048),
    L("poa-1", "people-of-the-abyss", "whitechapel", "Chapter 1, The Descent", "第 1 章《下沉》",
      prose(1688, "What I wish to do is to go down into the East End", "I am going to live there myself."), ["East End"], 1688),
    T("atw-1", "around-the-world", "reform-club", "Chapter 3", "第 3 章",
      prose(800, "Phileas Fogg avait quitté sa maison de Saville-row", "trois millions à bâtir."),
      prose(103, "Phileas Fogg, having shut the door of his house", "could not have cost less than three millions."),
      ["Reform-Club", "Pall-Mall"], ["Reform Club", "Pall Mall"], "George M. Towle (1873)", "Project Gutenberg #800 (French) and #103 (Towle)" + D),
    T("cik-1", "cambridge-i-knew", "river-cam", "Part 3", "第三节",
      "康桥的灵性全在一条河上；康河，我敢说，是全世界最秀丽的一条水。",
      "The spirit of Cambridge lies wholly in one river; the Cam, I dare say, is the loveliest water in all the world.",
      ["康河"], ["Cam"], "own", XU),
    T("cik-2", "cambridge-i-knew", "grantchester", "Part 3", "第三节",
      "上游是有名的拜伦潭——“Byron's Pool”——当年拜伦常在那里玩的；有一个老村子叫格兰骞斯德，有一个果子园，你可以躺在累累的桃李树荫下吃茶，花果会吊入你的茶杯，小雀子会到你桌上来啄食，那真是别有一番天地。",
      "Upstream is the famous Byron's Pool, where Byron used to play in his day; there is an old village called Grantchester, with an orchard where you can lie under the laden peach and plum trees and take tea, the blossom and fruit drop into your teacup and the little sparrows come to peck at your table: it is truly a world of its own.",
      ["拜伦潭", "格兰骞斯德"], ["Byron's Pool", "Grantchester"], "own", XU),
]

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-04 下午 书单第 6 批：7 本 1929 年前出版的书")
    append(f"{APP}/data/places.js", places, "11-04 下午 书单第 6 批（坐标均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-04 下午 书单第 6 批：古登堡原文摘句；凡尔纳附法文原文，徐志摩为自译")
    print(len(books), "books,", len(places), "places,", len(lines), "excerpts")
    for l in lines:
        print(f"{l['id']:7}", l["text_en"].replace("\n", " / ")[:200])
        if "text_orig" in l:
            print("        ", l["text_orig"][:200])
