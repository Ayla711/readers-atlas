"""11-27: Malta, the books the user chose (tools/selection/mt.md): by selection rule v2 no Maltese book qualifies, and the
user took the poems of Dun Karm Psaila, the national poet, as an exception; of the foreign books that qualify, the user took
Thomas Pynchon's V. (1963) and left out the Odyssey (its Malta link, Calypso's Gozo, is a tradition only). Malta opens with
this batch. Places, with the reason for each:
- Żebbuġ for Dun Karm: he was born there in 1871 and wrote "Lil Ħaż-Żebbuġ, Raħal Twelidi" (To Ħaż-Żebbuġ, my native
  village); the house he was born in still stands and a statue of him is in the town. His poems after 1931 are in copyright
  in the US: a scene note.
- Valletta for V.: chapter 11, "Confessions of Fausto Maijstral" (the city under bombing, 1942-43), chapter 16, "Valletta"
  (1956), and "Epilogue, 1919" (the June 1919 disturbances, the Sette Giugno). In copyright: a scene note.
Sources: https://en.wikipedia.org/wiki/Dun_Karm_Psaila; https://www.guidememalta.com/en/about-town-zebbug-malta;
https://um.edu.mt/library/oar/bitstream/123456789/50712/1/DunKarm_Booklet%5b1%5d.pdf (programme with the poem "Lil Ħaż-Żebbuġ,
Raħal Twelidi"); https://malti.skola.edu.mt/wp-content/uploads/2023/03/Ktejjeb-bit-Risposti-2023-v-2-1.pdf ("L-Ewwel Ward",
1914); https://en.wikipedia.org/wiki/V.; https://v.pynchonwiki.com/wiki; https://www.um.edu.mt/library/oar/handle/123456789/94761;
https://books.openbookpublishers.com/10.11647/obp.0426/ch11.xhtml; https://www.independent.com.mt/articles/2014-04-13/news/thomas-pynchons-v-and-valletta-4606558209/;
https://en.wikipedia.org/wiki/Sette_Giugno
The map of Malta (data/mt/geo.js) is the 6 regions of the 2019 Local Councils Act (in force 2021), merged from the 68 local
councils of geoBoundaries MLT ADM1 (public domain; three labels corrected; tools/eu-revision/mt_geo_build.py).
Photos: tools/content/batches/add_photos_mt_1127.py.
Usage: python3 -I tools/content/batches/add_mt1.py <app_dir> tools/content/batches/coords/add_mt1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "mt", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="dun-karm-poems", title="Poems (Dun Karm)", title_zh="邓·卡姆诗选", title_orig="Poeżiji", author="Dun Karm Psaila",
         author_zh="邓·卡姆·普萨伊拉", year="1912–1961", orig_lang="mt", public_domain=False, source_url=None,
         author_orig="Dun Karm Psaila", aliases=["Dun Karm", "Carmelo Psaila", "L-Innu Malti", "Il-Musbieħ tal-Mużew", "Il-Jien u Lil Hinn Minnu", "Lil Ħaż-Żebbuġ, Raħal Twelidi"]),
    dict(id="v-pynchon", title="V.", title_zh="V.", title_orig="V.", author="Thomas Pynchon", author_zh="托马斯·品钦", year="1963",
         orig_lang="en", public_domain=False, source_url=None, author_orig="Thomas Pynchon",
         aliases=["Herbert Stencil", "Benny Profane", "Fausto Maijstral", "Sette Giugno"]),
]

places = [
    b.ORIG("mt-zebbug", "Ħaż-Żebbuġ, Dun Karm's native town", "泽布季 · 邓·卡姆的家乡", *C("mt-zebbug"),
        "An old inland town of central Malta, the birthplace of Dun Karm Psaila (1871), the national poet, as of the linguist Mikiel Anton Vassalli. The house he was born in still stands in the heart of the town, and a statue of him stands here. He wrote a poem to it, \"Lil Ħaż-Żebbuġ, Raħal Twelidi\" (To Ħaż-Żebbuġ, my native village)",
        "马耳他中部内陆的一座老城，国家诗人邓·卡姆·普萨伊拉 1871 年生在这里，语言学家米基耶尔·安东·瓦萨利也生在这里。他出生的房子至今还在城中心，城里也有他的雕像。他写过一首献给这里的诗《致泽布季，我的故乡》"),
    b.ORIG("mt-valletta", "Valletta", "瓦莱塔", *C("mt-valletta"),
        "The capital of Malta, the walled city built by the Knights of St John after the siege of 1565. Pynchon's V. ends here: Fausto Maijstral's diary of the city under German and Italian bombing in 1942-43, Stencil's arrival with Benny Profane in 1956 as the fleet gathers for Suez, and an epilogue set in the June 1919 disturbances, the Sette Giugno, in which four Maltese were killed by British troops",
        "马耳他首都，1565 年大围城之后由圣约翰骑士团修建的城墙之城。品钦的《V.》在这里收尾：福斯托·迈斯特拉尔记下 1942–43 年德意空袭下这座城的日记；1956 年苏伊士危机前舰队云集时，斯坦西尔带着贝尼·普罗费恩来到这里；尾声回到 1919 年 6 月的骚乱“六月七日”，英军开枪打死了四名马耳他人"),
]

lines = [
    b.S("mt-dk-1", "dun-karm-poems", "mt-zebbug", "The poems, and \"Lil Ħaż-Żebbuġ, Raħal Twelidi\"", "诗作，及《致泽布季，我的故乡》",
        "Dun Karm, a priest who taught at the seminary, wrote only in Italian until 1912, when \"Quddiem Xbieha tal-Madonna\" (Before an Image of Our Lady) appeared in Maltese in the first number of Il-Ħabib; a little book of fifteen of his Maltese poems, L-Ewwel Ward, followed in 1914. His best-known poems include \"Il-Musbieħ tal-Mużew\" (The Museum Lamp, 1920) and the long meditation Il-Jien u Lil Hinn Minnu (The Self and Beyond It); in 1921 he wrote the words of L-Innu Malti, the national anthem, first sung in 1923. His Maltese poems did much to make Maltese a language of literature, and he is called the national poet. He was born at Ħaż-Żebbuġ and wrote a poem to the town.",
        "邓·卡姆是在神学院任教的神父，1912 年以前只用意大利文写诗；那一年，他的第一首马耳他语诗《在圣母像前》登在《朋友》创刊号上，1914 年又出了收十五首马耳他语诗的小册子《初放的玫瑰》。他最有名的诗有《博物馆的灯》（1920）和长篇沉思诗《自我与自我之外》；1921 年他为马耳他国歌《马耳他颂》填词，1923 年首次公开演唱。他的马耳他语诗大大推动了马耳他语成为文学语言，人称“国家诗人”。他生在泽布季，也写过一首献给这座城的诗。",
        ["Ħaż-Żebbuġ"], ["泽布季"],
        "https://en.wikipedia.org/wiki/Dun_Karm_Psaila; https://malti.skola.edu.mt/wp-content/uploads/2023/03/Ktejjeb-bit-Risposti-2023-v-2-1.pdf; https://um.edu.mt/library/oar/bitstream/123456789/50712/1/DunKarm_Booklet%5b1%5d.pdf"),
    b.S("mt-v-1", "v-pynchon", "mt-valletta", "Chapter 11, \"Confessions of Fausto Maijstral\"; Chapter 16, \"Valletta\"; Epilogue, 1919", "第十一章《福斯托·迈斯特拉尔的自白》、第十六章《瓦莱塔》、尾声《1919》",
        "Herbert Stencil hunts across the century for V., a woman who keeps turning up at moments of crisis, and for his father Sidney, a British agent who died in Malta in 1919 while looking into the June disturbances. In chapter 11 the Maltese Fausto Maijstral writes to his daughter Paola of Valletta under the bombs of 1942-43, where children gather round a dying woman pinned under a fallen beam, who may be V. In 1956, as the fleet gathers for Suez, Stencil comes to Valletta with Benny Profane to find Fausto, though he dreads the place where his father died; the epilogue goes back to the Sette Giugno of 1919 and the elder Stencil's last days there. Pynchon said he put 1919 at the end because there was nowhere else to put it, and for irony.",
        "赫伯特·斯坦西尔在整整一个世纪里追寻 V.——一个总在危机关头出现的女人——也在追寻父亲西德尼：这位英国特工 1919 年在马耳他调查六月骚乱时死去。第十一章里，马耳他人福斯托·迈斯特拉尔写信给女儿保拉，讲 1942–43 年轰炸下的瓦莱塔：一群孩子围着一个被倒塌的横梁压住、奄奄一息的女人，她也许就是 V.。1956 年苏伊士危机前舰队云集，斯坦西尔带着贝尼·普罗费恩来到瓦莱塔找福斯托，虽然他害怕这个父亲死去的地方；尾声回到 1919 年的“六月七日”，写老斯坦西尔在这里的最后日子。品钦说，把 1919 放在最后，是因为没别的地方可放，也为了反讽。",
        ["Valletta"], ["瓦莱塔"],
        "https://en.wikipedia.org/wiki/V.; https://v.pynchonwiki.com/wiki; https://www.um.edu.mt/library/oar/handle/123456789/94761; https://books.openbookpublishers.com/10.11647/obp.0426/ch11.xhtml; https://www.independent.com.mt/articles/2014-04-13/news/thomas-pynchons-v-and-valletta-4606558209/; https://en.wikipedia.org/wiki/Sette_Giugno"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO)

HEAD = "// Malta, hand-written content (tools/content/batches/add_mt1.py, 2026-11-27).\n"
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
