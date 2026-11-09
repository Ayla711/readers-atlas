"""11-05: pilgrimage places for authors who had none — Burns, Stevenson (with Scott and Burns), Gaskell, Lawrence,
George Eliot, Wilde, Tolkien, C. S. Lewis, Blake / Defoe / Bunyan, Pepys, Mary Shelley. Facts from Wikipedia;
coordinates from Geograph subject locations, Commons camera locations or Wikipedia; photos from Commons.
Usage: python3 -I add_batch12.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch12.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
append, PIL, W = b5.append, b5.PIL, b5.W
GEO = "https://www.geograph.org.uk/photo/"
COM = "https://commons.wikimedia.org/wiki/"
def G(n, what): return (f"{what} (Geograph photo {n}, subject location)", GEO + str(n))

STEVENSON = ["edinburgh-notes", "kidnapped", "treasure-island", "jekyll-and-hyde"]
places = [
    PIL("burns-cottage", "Burns Cottage, Alloway", "阿洛韦 · 彭斯故居", 55.4328, -4.6334, *G(428032, "Burns Cottage, Alloway"),
        "The thatched cottage Burns's father built in 1757. Robert was born here on 25 January 1759 and lived here until he was about seven; it is now part of the Robert Burns Birthplace Museum, run by the National Trust for Scotland",
        "彭斯的父亲 1757 年盖的茅草屋。罗伯特 1759 年 1 月 25 日生在这里，住到七岁左右；现在是苏格兰国民信托管理的罗伯特·彭斯出生地博物馆的一部分",
        ["burns-highlands"]),
    PIL("writers-museum", "The Writers' Museum, Lady Stair's House", "爱丁堡 · 作家博物馆（莱迪·斯泰尔宅）", 55.9496, -3.1946, *G(2140534, "Lady Stair's House"),
        "A museum in Lady Stair's House, in a close off the Lawnmarket at the top of the Royal Mile, given to the lives of Scotland's three great writers: Robert Burns, Walter Scott and Robert Louis Stevenson",
        "皇家一英里上端劳恩市场旁小巷里的莱迪·斯泰尔宅，现在是作家博物馆，专门介绍苏格兰三位大作家彭斯、司各特和史蒂文森的生平",
        STEVENSON + ["burns-highlands", "marmion", "lady-of-the-lake", "heart-of-midlothian", "ivanhoe"]),
    PIL("gaskell-house", "Elizabeth Gaskell's House, Manchester", "曼彻斯特 · 盖斯凯尔故居", 53.4636, -2.2212, *G(720377, "Elizabeth Gaskell's House, Plymouth Grove"),
        "The Gaskells moved into 84 Plymouth Grove in 1850, and Elizabeth wrote all her later books here, Cranford and North and South among them; Charlotte Brontë stayed three times and Dickens called. Restored and opened to visitors in 2014",
        "盖斯凯尔一家 1850 年搬进普利茅斯林荫路 84 号，她后来的书，包括《克兰福德》和《南方与北方》，都是在这里写的；夏洛蒂·勃朗特来住过三次，狄更斯也来拜访过。2014 年修复后对外开放",
        ["north-and-south", "cranford", "sylvias-lovers", "mary-barton"]),
    PIL("lawrence-birthplace", "D. H. Lawrence Birthplace Museum, Eastwood", "伊斯特伍德 · D. H. 劳伦斯出生地博物馆", 53.0186, -1.3071, *G(7641153, "D H Lawrence Birthplace Museum, Eastwood"),
        "The miner's house at 8a Victoria Street where Lawrence was born in 1885, kept as it is thought to have been when the family lived there; his original gravestone is on show",
        "维多利亚街 8a 号的矿工住宅，劳伦斯 1885 年生在这里；屋子按当年一家人住时的样子布置，还陈列着他最初的墓碑",
        ["sons-and-lovers", "the-rainbow"]),
    PIL("eliot-grave", "George Eliot's grave, Highgate Cemetery", "海格特公墓 · 乔治·艾略特墓", 51.5664, -0.1443, *G(5876589, "The grave of George Eliot in Highgate Cemetery"),
        "The headstone gives her pen name and her married name, Mary Ann Cross; she lies next to George Henry Lewes, her partner",
        "墓碑上刻着她的笔名，以及婚后的名字玛丽·安·克罗斯；她葬在伴侣乔治·亨利·刘易斯的旁边",
        ["mill-on-the-floss", "middlemarch"]),
    PIL("reading-gaol", "Reading Gaol", "雷丁监狱", 51.4569, -0.9645, *G(5320123, "Reading Prison"),
        "Oscar Wilde was held here from 1895 to 1897; an execution at the prison in 1896 lies behind The Ballad of Reading Gaol. The prison closed in 2014",
        "王尔德 1895 至 1897 年被关在这里；1896 年狱中的一次绞刑，后来写成了《雷丁监狱之歌》。监狱 2014 年关闭",
        ["dorian-gray"]),
    PIL("tolkien-grave", "J. R. R. Tolkien's grave, Wolvercote Cemetery", "牛津沃尔弗科特公墓 · 托尔金墓", 51.7914, -1.2749,
        "Grave of Edith and J.R.R. Tolkien (Commons photo, camera location at the grave)", COM + "File:Grave_of_Edith_and_J.R.R._Tolkien_in_the_Wolvercote_Cemetery,_Oxonmoot_1979.jpg",
        "Tolkien, who died in 1973, is buried with his wife Edith; the stone gives them the names of the lovers in his legends, Beren and Lúthien",
        "托尔金 1973 年去世，和妻子伊迪丝合葬；墓碑上还刻着他传说里那对恋人的名字：贝伦和露西恩",
        ["the-hobbit"]),
    PIL("the-kilns", "The Kilns, Headington", "牛津黑丁顿 · 窑屋", 51.7567, -1.1899, *G(7925307, "The Kilns, home of C.S. Lewis"),
        "Lewis bought the house in 1930 with his brother Warren and Janie Moore, and lived here for the rest of his life, writing the Narnia books here; it is now a study centre run by the C. S. Lewis Foundation",
        "刘易斯 1930 年和哥哥沃伦、简妮·摩尔一起买下这座房子，此后一直住在这里，纳尼亚系列也是在这里写的；现在是 C. S. 刘易斯基金会的研究中心",
        ["lion-witch-wardrobe"]),
    PIL("bunhill-fields", "Bunhill Fields", "邦希尔墓园", 51.5238, -0.0885, *G(3710090, "Defoe and Blake memorials, Bunhill Fields"),
        "A burial ground for nonconformists from 1665 to 1854, now a public garden. William Blake, Daniel Defoe and John Bunyan lie here: Defoe's obelisk went up in 1870, Bunyan's tomb carries his effigy, and a stone marking Blake's grave was unveiled in 2018",
        "1665 至 1854 年间不信国教者的墓地，现在是公共花园。布莱克、笛福和班扬都葬在这里：笛福的方尖碑立于 1870 年，班扬的墓上有他的卧像，标出布莱克墓穴位置的石碑 2018 年揭幕",
        ["blake-songs", "plague-year", "robinson-crusoe", "pilgrims-progress"]),
    PIL("st-olaves", "St Olave's Church, Hart Street", "哈特街 · 圣奥拉夫教堂", 51.5106, -0.0792, *G(1085120, "St Olave, Hart Street"),
        "Pepys's parish church, 'our own church' in the diary. He had a gallery built here reached from the Navy Office, put up a bust of his wife Elizabeth after her death in 1669, and was buried beside her in 1703",
        "佩皮斯所属的教区教堂，日记里称它“我们自己的教堂”。他在这里修了一条从海军部直通的楼廊，1669 年妻子伊丽莎白去世后在这里立了她的胸像，1703 年葬在她身旁",
        ["pepys-diary"]),
    PIL("mary-shelley-grave", "Mary Shelley's grave, Bournemouth", "伯恩茅斯 · 玛丽·雪莱墓", 50.7204, -1.8750, *G(1861397, "Grave of Mary Wollstonecraft Shelley"),
        "Mary Shelley lies in St Peter's churchyard, reputedly with the heart of Percy Bysshe Shelley; her son had her parents, Mary Wollstonecraft and William Godwin, reburied here beside her",
        "玛丽·雪莱葬在圣彼得教堂的墓园，据说和珀西·比希·雪莱的心脏葬在一起；她的儿子把她的父母玛丽·沃斯通克拉夫特和威廉·葛德文也迁葬到这里",
        ["frankenstein"]),
]
PHOTOS = {
    "burns-cottage": (1, "Burns Cottage, the long thatched cottage in Alloway", "阿洛韦那座长长的茅草屋彭斯故居"),
    "writers-museum": (0, "Lady Stair's House in Lady Stair's Close, Edinburgh", "爱丁堡莱迪·斯泰尔小巷里的莱迪·斯泰尔宅"),
    "gaskell-house": (0, "The front of Elizabeth Gaskell's House on Plymouth Grove", "普利茅斯林荫路上盖斯凯尔故居的正面"),
    "lawrence-birthplace": (0, "The D. H. Lawrence Birthplace Museum on Victoria Street, Eastwood", "伊斯特伍德维多利亚街上的劳伦斯出生地博物馆"),
    "eliot-grave": (1, "George Eliot's headstone, inscribed George Eliot and Mary Ann Cross", "刻着“乔治·艾略特”和“玛丽·安·克罗斯”的墓碑"),
    "reading-gaol": (0, "The red-brick buildings of Reading Prison", "雷丁监狱的红砖建筑"),
    "tolkien-grave": (2, "The Tolkiens' grave in Wolvercote Cemetery", "沃尔弗科特公墓里托尔金夫妇的墓"),
    "the-kilns": (0, "The Kilns, C. S. Lewis's house in Headington", "黑丁顿的窑屋，刘易斯的住所"),
    "bunhill-fields": (0, "Defoe's obelisk, with Blake's memorial beyond, in Bunhill Fields", "邦希尔墓园里笛福的方尖碑，后面是布莱克的纪念碑"),
    "st-olaves": (0, "St Olave's Church, Hart Street", "哈特街的圣奥拉夫教堂"),
    "mary-shelley-grave": (0, "The Shelley tomb in St Peter's churchyard, Bournemouth", "伯恩茅斯圣彼得教堂墓园里的雪莱家族墓"),
}
cands = json.load(open(f"{PW}/candidates.json"))
for p in places:
    n, en, zh = PHOTOS[p["id"]]
    c = cands[p["id"]]["candidates"][n]
    im = Image.open(f"{PW}/dl/{p['id']}__{n}.jpg").convert("RGB")
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, p["id"]
    rel = f"images/places/{p['id']}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)
    p["photo"] = {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip(), "license": c["license"].strip(),
                  "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}
if __name__ == "__main__":
    append(f"{APP}/data/places.js", places, "11-05 作家朝圣地补齐：彭斯、史蒂文森、盖斯凯尔、劳伦斯、乔治·艾略特、王尔德、托尔金、刘易斯、布莱克 / 笛福 / 班扬、佩皮斯、玛丽·雪莱")
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places]
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    print(len(places), "places")
