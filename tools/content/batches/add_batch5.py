"""11-04 afternoon, booklist batch 5: Alice and seven more books published before 1929. Every excerpt is cut out
of the downloaded Project Gutenberg file; every coordinate has a source.
Usage: python3 -I add_batch5.py <app_dir> <pg_texts_dir>"""
import importlib.util
import json
import re
import sys

APP, TX = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("b2", __file__.replace("add_batch5.py", "add_batch2.py"))
b2 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b2)
sys.argv = _argv
prose, norm, flat, append, GAP = b2.prose, b2.norm, b2.flat, b2.append, b2.GAP
D = ", 2026-11-04"
G = "https://www.gutenberg.org/ebooks/"
W = "https://en.wikipedia.org/wiki/"
GBG = "https://www.thegreatbritainguide.com/place/"

def verse_lines(book, start, n):
    """n non-empty lines from the line containing `start`; indentation and the editor's line numbers removed"""
    raw = flat(book)[0].split("\n")
    for i, l in enumerate(raw):
        if start in norm(l):
            out = []
            for l2 in raw[i:]:
                s = re.sub(r"\s+\d+\s*$", "", norm(l2.strip())).strip()
                if s:
                    out.append(s)
                if len(out) == n:
                    return "\n".join(out)
    raise SystemExit(f"not found in {book}: {start}")

def B(id, title, title_zh, author, author_zh, year, pg, pd=True):
    return dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year, orig_lang="en",
                public_domain=pd, source_url=G + str(pg))

books = [
    B("alice-in-wonderland", "Alice's Adventures in Wonderland", "爱丽丝漫游奇境", "Lewis Carroll", "刘易斯·卡罗尔", "1865", 28885),
    B("jane-eyre", "Jane Eyre", "简·爱", "Charlotte Brontë", "夏洛蒂·勃朗特", "1847", 1260),
    B("wind-in-the-willows", "The Wind in the Willows", "柳林风声", "Kenneth Grahame", "肯尼斯·格雷厄姆", "1908", 289),
    B("peter-pan-kensington", "Peter Pan in Kensington Gardens", "肯辛顿公园里的彼得·潘", "J. M. Barrie", "詹姆斯·巴里", "1906", 1332),
    # Eliot died in 1965: in UK copyright until the end of 2035; public domain in the US (1922), hence Gutenberg
    B("the-waste-land", "The Waste Land", "荒原", "T. S. Eliot", "T. S. 艾略特", "1922", 1321, pd=False),
    B("pepys-diary", "The Diary of Samuel Pepys", "佩皮斯日记", "Samuel Pepys", "塞缪尔·佩皮斯", "1660–1669", 4200),
    B("dorian-gray", "The Picture of Dorian Gray", "道林·格雷的画像", "Oscar Wilde", "奥斯卡·王尔德", "1891", 174),
    B("return-of-the-native", "The Return of the Native", "还乡", "Thomas Hardy", "哈代", "1878", 122),
]

def P(id, name, name_zh, lat, lon, st, su, type, **kw):
    d = dict(id=id, name=name, name_zh=name_zh, lat=lat, lon=lon, place_type=type)
    d.update(kw)
    d["coord_checked"] = f"{st} — {su}{D}"
    return d

def ORIG(id, name, name_zh, lat, lon, st, su, en, zh, **kw):
    return P(id, name, name_zh, lat, lon, st, su, "original", note=zh, note_en=en, **kw)

def PROTO(id, name, name_zh, lat, lon, st, su, en, zh, **kw):
    return P(id, name, name_zh, lat, lon, st, su, "prototype", prototype_of=zh, prototype_of_en=en, **kw)

def PIL(id, name, name_zh, lat, lon, st, su, en, zh, book_ids, **kw):
    return P(id, name, name_zh, lat, lon, st, su, "pilgrimage", note=zh, book_ids=book_ids, note_en=en, **kw)

places = [
    PROTO("godstow", "Godstow", "戈斯托", 51.7786, -1.2994, "Godstow Abbey (The Great Britain Guide)", GBG + "godstow-abbey/",
          "Not named in the book: Carroll took the Liddell sisters on river trips and picnics to Godstow, and on the boat trip of 4 July 1862 he first told them the story",
          "书中没有点名：卡罗尔常带利德尔姐妹划船到戈斯托野餐，1862 年 7 月 4 日那次泛舟途中，他第一次给她们讲了这个故事"),
    PIL("daresbury", "All Saints' Church, Daresbury", "达斯伯里 · 诸圣堂", 53.3406, -2.6312, "All Saints Church, Daresbury (The Great Britain Guide)", GBG + "all-saints-church-daresbury/",
        "Carroll was born at the vicarage in 1832, when his father was the curate here; the church has a memorial window (1935) and the Lewis Carroll Centre (2012)",
        "卡罗尔 1832 年生在这里的牧师住宅，父亲当时是这座教堂的牧师；教堂里有 1935 年的纪念彩窗和 2012 年开放的刘易斯·卡罗尔中心", ["alice-in-wonderland"]),
    PIL("carroll-grave", "Lewis Carroll's grave, Guildford", "吉尔福德 · 卡罗尔墓", 51.2317, -0.5821, "Lewis Carroll's grave, Mount Cemetery (The Tombstone Tourist)", "https://thetombstonetourist.com/graves/grave-lewis-carroll-mount-cemetery/",
        "Carroll died at his sisters' house, The Chestnuts, in Guildford on 14 January 1898 and is buried in the Mount Cemetery",
        "卡罗尔 1898 年 1 月 14 日在吉尔福德姐姐们的住所“栗树居”去世，葬在山丘公墓", ["alice-in-wonderland"]),
    PROTO("north-lees-hall", "North Lees Hall, Hathersage", "哈瑟塞奇 · 诺斯利斯庄园", 53.3474, -1.6479, "North Lees Hall (The Great Britain Guide)", GBG + "north-lees-hall/",
          "Often named as the model for Thornfield Hall; Charlotte Brontë stayed in Hathersage in 1845",
          "常被认为是桑菲尔德府的原型；夏洛蒂·勃朗特 1845 年在哈瑟塞奇小住过"),
    PROTO("cowan-bridge", "Cowan Bridge", "考恩桥", 54.1834, -2.5615, "Cowan Bridge (Wikipedia), grid ref SD634765", W + "Cowan_Bridge",
          "The Clergy Daughters' School here, where Charlotte and Emily Brontë and their older sisters Maria and Elizabeth were pupils, is the model for Lowood; Maria and Elizabeth died after their time there",
          "这里的牧师女儿学校是罗沃德的原型，夏洛蒂、艾米莉和两个姐姐玛丽亚、伊丽莎白都在这里上过学；玛丽亚和伊丽莎白离校后不久去世"),
    PROTO("quarry-wood", "Quarry Wood, Cookham Dean", "库克姆迪恩 · 采石场林", 51.5574, -0.7227, "Quarry Woods walk (Countryfile), grid ref SU886850", "https://www.countryfile.com/go-outdoors/walks/quarry-woods-berkshire",
          "Taken as the model for the Wild Wood; Grahame grew up and later lived nearby at Cookham Dean, by the Thames",
          "被认为是野树林的原型；格雷厄姆小时候和后来都住在附近泰晤士河边的库克姆迪恩"),
    ORIG("kensington-gardens", "Kensington Gardens", "肯辛顿公园", 51.5072, -0.1803, "Kensington Gardens (The Great Britain Guide)", GBG + "kensington-gardens/",
         "The royal park west of Hyde Park, with the Round Pond and the Long Water, the western arm of the Serpentine",
         "海德公园西边的王家公园，园里有圆池和长湖（九曲湖的西段）"),
    PIL("peter-pan-statue", "Peter Pan statue, Kensington Gardens", "肯辛顿公园 · 彼得·潘雕像", 51.5086, -0.1759, "Peter Pan statue (The Great Britain Guide)", GBG + "peter-pan-statue/",
        "Barrie commissioned the statue from George Frampton and had it put up by the Long Water on 30 April 1912",
        "巴里请乔治·弗兰普顿塑造了这座雕像，1912 年 4 月 30 日把它立在长湖边", ["peter-pan-kensington"]),
    ORIG("london-bridge", "London Bridge", "伦敦桥", 51.5081, -0.0878, "London Bridge (Wikipedia)", W + "London_Bridge",
         "The bridge between the City and Southwark; the present one opened in 1973, on the line of the crossing Eliot's clerks walked over",
         "连接伦敦城和南华克的桥；现在的桥 1973 年启用，位置就是艾略特笔下上班人流走过的那座"),
    ORIG("margate", "Margate Sands", "马盖特海滩", 51.3851, 1.3839, "Margate (Wikipedia), grid ref TR355705", W + "Margate",
         "The Kent seaside town where Eliot recuperated in 1921 and worked on The Waste Land", "肯特郡的海滨小城，艾略特 1921 年在这里休养时写《荒原》", city=True),
    ORIG("pudding-lane", "Pudding Lane and the Monument", "布丁巷与大火纪念碑", 51.5101, -0.0859, "Monument to the Great Fire of London (The Great Britain Guide)", GBG + "monument-to-the-great-fire-of-london/",
         "The Great Fire of 1666 began in Thomas Farriner's bakery in Pudding Lane; the Monument stands 202 feet from the spot",
         "1666 年伦敦大火从布丁巷托马斯·法里纳的面包房烧起；大火纪念碑离起火点 202 英尺"),
    ORIG("covent-garden", "Covent Garden", "科文特花园", 51.5117, -0.1239, "Covent Garden (The Great Britain Guide)", GBG + "covent-garden/",
         "The piazza in the West End, London's main fruit, vegetable and flower market until 1974", "西区的广场，1974 年以前是伦敦主要的果蔬花卉市场"),
    PIL("hardys-cottage", "Hardy's Cottage, Higher Bockhampton", "上博克汉普顿 · 哈代出生的小屋", 50.7309, -2.3863, "Hardy's Cottage (The Great Britain Guide)", GBG + "hardys-cottage/",
        "Hardy was born here in 1840 and wrote Under the Greenwood Tree and Far from the Madding Crowd here; the heath beside it, with Rainbarrow behind, is taken as the heart of Egdon Heath",
        "哈代 1840 年生在这里，在这里写了《绿林荫下》和《远离尘嚣》；小屋旁的荒地和屋后的雨冢，被认为是埃格敦荒原的中心", ["return-of-the-native", "tess"]),
]

def L(id, book_id, place, loc, loc_zh, text, hl, pg):
    for h in hl:
        assert h in text, (id, h)
    return dict(id=id, book_id=book_id, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text,
                highlight_en=hl, translation="original", status="draft", checked=f"Project Gutenberg #{pg}{D}")

lines = [
    L("alice-1", "alice-in-wonderland", "godstow", "Prefatory poem", "卷首诗", verse_lines(28885, "All in the golden afternoon", 6), ["golden afternoon"], 28885),
    L("alice-2", "alice-in-wonderland", "london", "Chapter 2, The Pool of Tears", "第 2 章《眼泪池》",
      prose(28885, "London is the capital of Paris", "that's all wrong, I'm certain!"), ["London"], 28885),
    L("je-1", "jane-eyre", "north-lees-hall", "Chapter 11", "第 11 章",
      prose(1260, "It was three storeys high", "gave it a picturesque look."), ["three storeys high", "battlements"], 1260),
    L("je-2", "jane-eyre", "cowan-bridge", "Chapter 9", "第 9 章",
      prose(1260, "That forest-dell, where Lowood lay", "into an hospital."), ["Lowood"], 1260),
    L("wiw-1", "wind-in-the-willows", "quarry-wood", "Chapter 3, The Wild Wood", "第 3 章《野树林》",
      prose(289, "with great cheerfulness of spirit he pushed on", "some still southern sea."), ["Wild Wood"], 289),
    L("ppk-1", "peter-pan-kensington", "kensington-gardens", "Peter Pan", "《彼得·潘》一章",
      prose(1332, "Standing on the ledge he could see trees far away", "right over the houses to the Gardens."), ["Kensington Gardens"], 1332),
    L("ppk-2", "peter-pan-kensington", "kensington-gardens", "Peter Pan", "《彼得·潘》一章",
      prose(1332, "He alighted gaily on the open sward", "lie on his back and kick."), ["Serpentine"], 1332),
    L("wl-1", "the-waste-land", "london-bridge", "I. The Burial of the Dead", "第一章《死者葬仪》", verse_lines(1321, "Unreal City,", 4), ["London Bridge"], 1321),
    L("wl-2", "the-waste-land", "margate", "III. The Fire Sermon", "第三章《火诫》", verse_lines(1321, "On Margate Sands.", 3).lstrip('"'), ["Margate Sands"], 1321),
    L("pepys-1", "pepys-diary", "pudding-lane", "2 September 1666", "1666 年 9 月 2 日",
      prose(4200, "So down, with my heart full of trouble, to the Lieutenant of the Tower", "most part of Fish-street already."), ["Pudding-lane"], 4200),
    L("dg-1", "dorian-gray", "covent-garden", "Chapter 7", "第 7 章",
      prose(174, "As the dawn was just breaking, he found himself close to Covent Garden.", "down the polished empty street."), ["Covent Garden"], 174),
    L("ron-1", "return-of-the-native", "hardys-cottage", "Book 1, Chapter 1", "第一部第 1 章",
      prose(122, "A Saturday afternoon in November was approaching the time of twilight", "embrowned itself moment by moment."), ["Egdon Heath"], 122),
]

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-04 下午 书单第 5 批：《爱丽丝》等 8 本 1929 年前出版的书（古登堡原文）")
    append(f"{APP}/data/places.js", places, "11-04 下午 书单第 5 批（坐标均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-04 下午 书单第 5 批：古登堡原文摘句")
    print(len(books), "books,", len(places), "places,", len(lines), "excerpts")
    for l in lines:
        print(f"{l['id']:8}", l["text_en"].replace("\n", " / ")[:170])
