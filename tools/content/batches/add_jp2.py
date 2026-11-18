"""11-18: Japan, second pack (works from 1935 on, and the foreign books), plus the writer for both packs.
The Housekeeper and the Professor and Convenience Store Woman were chosen but name no real place, so they wait for book-list-only
support. Usage: python3 -I add_jp2.py <app_dir> <coords_jp.json>"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_jp1 as r
from add_jp1 import BK, ORIG, PROTO, PIL, S, W, b

MISHIMA = ("Yukio Mishima", "三岛由纪夫", "三島由紀夫")
MURAKAMI = ("Haruki Murakami", "村上春树", "村上春樹")
KAWABATA = ("Yasunari Kawabata", "川端康成", "川端康成")
DAZAI = ("Osamu Dazai", "太宰治", "太宰治")
HIGASHINO = ("Keigo Higashino", "东野圭吾", "東野圭吾")
OE = ("Kenzaburo Oe", "大江健三郎", "大江健三郎")

books = [
    BK("makioka-sisters", "The Makioka Sisters", "细雪", "細雪", "Jun'ichiro Tanizaki", "谷崎润一郎", "谷崎潤一郎", "1943–1948", pd=False,
       aliases=["Sasameyuki", "Light Snow", "Yukiko", "Taeko", "雪子", "妙子"]),
    BK("snow-country", "Snow Country", "雪国", "雪国", *KAWABATA, "1935–1948", pd=False, aliases=["Yukiguni", "Komako", "Shimamura", "驹子", "岛村"]),
    BK("setting-sun", "The Setting Sun", "斜阳", "斜陽", *DAZAI, "1947", aliases=["Shayo", "Kazuko", "和子"]),
    BK("no-longer-human", "No Longer Human", "人间失格", "人間失格", *DAZAI, "1948", aliases=["Ningen Shikkaku", "A Shameful Life", "Yozo", "叶藏"]),
    BK("golden-pavilion", "The Temple of the Golden Pavilion", "金阁寺", "金閣寺", *MISHIMA, "1956", pd=False,
       aliases=["Kinkaku-ji", "The Golden Pavilion", "Mizoguchi", "沟口"]),
    BK("woman-in-the-dunes", "The Woman in the Dunes", "砂女", "砂の女", "Kobo Abe", "安部公房", "安部公房", "1962", pd=False,
       aliases=["Suna no Onna", "沙丘之女"]),
    BK("personal-matter", "A Personal Matter", "个人的体验", "個人的な体験", *OE, "1964", pd=False, aliases=["Bird", "鸟"]),
    BK("black-rain", "Black Rain", "黑雨", "黒い雨", "Masuji Ibuse", "井伏鳟二", "井伏鱒二", "1965", pd=False,
       aliases=["Kuroi Ame", "Shigematsu", "Yasuko", "重松", "矢须子"]),
    BK("silence-endo", "Silence", "沉默", "沈黙", "Shusaku Endo", "远藤周作", "遠藤周作", "1966", pd=False,
       aliases=["Chinmoku", "Rodrigues", "Kichijiro", "Ferreira", "罗德里格", "吉次郎", "fumie", "踏绘"]),
    BK("silent-cry", "The Silent Cry", "万延元年的足球", "万延元年のフットボール", *OE, "1967", pd=False,
       aliases=["Football in the First Year of Man'en", "Man'en Gannen no Futtoboru", "Mitsusaburo", "Takashi", "蜜三郎", "鹰四"]),
    BK("grave-of-the-fireflies", "Grave of the Fireflies", "萤火虫之墓", "火垂るの墓", "Akiyuki Nosaka", "野坂昭如", "野坂昭如", "1967", pd=False,
       aliases=["Hotaru no Haka", "Seita", "Setsuko", "清太", "节子"]),
    BK("spring-snow", "Spring Snow", "春雪", "春の雪", *MISHIMA, "1969", pd=False,
       aliases=["Haru no Yuki", "The Sea of Fertility", "丰饶之海", "Kiyoaki", "Satoko", "清显", "聪子"]),
    BK("hard-boiled-wonderland", "Hard-Boiled Wonderland and the End of the World", "世界尽头与冷酷仙境", "世界の終りとハードボイルド・ワンダーランド",
       *MURAKAMI, "1985", pd=False, aliases=["The End of the World", "Calcutec", "世界尽头"]),
    BK("all-she-was-worth", "All She Was Worth", "火车", "火車", "Miyuki Miyabe", "宫部美雪", "宮部みゆき", "1992", pd=False,
       aliases=["Kasha", "Honma", "本间"]),
    BK("wind-up-bird", "The Wind-Up Bird Chronicle", "奇鸟行状录", "ねじまき鳥クロニクル", *MURAKAMI, "1994–1995", pd=False,
       aliases=["Nejimaki-dori Kuronikuru", "Toru Okada", "冈田亨", "拧发条鸟"]),
    BK("journey-under-the-midnight-sun", "Journey Under the Midnight Sun", "白夜行", "白夜行", *HIGASHINO, "1999", pd=False,
       aliases=["Byakuyako", "Yukiho", "Ryoji", "雪穗", "亮司"]),
    BK("suspect-x", "The Devotion of Suspect X", "嫌疑人X的献身", "容疑者Xの献身", *HIGASHINO, "2005", pd=False,
       aliases=["Yogisha X no Kenshin", "Ishigami", "Yukawa", "石神", "汤川"]),
    BK("1q84", "1Q84", "1Q84", "1Q84", *MURAKAMI, "2009–2010", pd=False, aliases=["Aomame", "Tengo", "青豆", "天吾"]),
    BK("shogun", "Shogun", "幕府将军", "Shōgun", "James Clavell", "詹姆斯·克拉维尔", None, "1975", pd=False, lang="en",
       aliases=["Shōgun", "Blackthorne", "Anjin", "Toranaga", "Mariko", "布莱克索恩", "虎长"]),
    BK("hiroshima-hersey", "Hiroshima", "广岛", "Hiroshima", "John Hersey", "约翰·赫西", None, "1946", pd=False, lang="en",
       aliases=["Father Kleinsorge", "Kiyoshi Tanimoto", "谷本清"]),
    BK("memoirs-of-a-geisha", "Memoirs of a Geisha", "艺伎回忆录", "Memoirs of a Geisha", "Arthur Golden", "阿瑟·高顿", None, "1997", pd=False,
       lang="en", aliases=["Sayuri", "Chiyo", "小百合", "千代"]),
    BK("samurais-garden", "The Samurai's Garden", "武士的花园", "The Samurai's Garden", "Gail Tsukiyama", "盖尔·筑山", None, "1994", pd=False,
       lang="en", aliases=["Stephen", "Matsu", "Tarumi"]),
    BK("pachinko", "Pachinko", "柏青哥", "Pachinko", "Min Jin Lee", "李敏金", None, "2017", pd=False, lang="en",
       aliases=["Sunja", "Ikaino", "顺子", "猪饲野"]),
    BK("jacob-de-zoet", "The Thousand Autumns of Jacob de Zoet", "雅各布·德佐特的千秋", "The Thousand Autumns of Jacob de Zoet",
       "David Mitchell", "大卫·米切尔", None, "2010", pd=False, lang="en", aliases=["Dejima", "Orito", "出岛", "织斗"]),
]

places = [
    ORIG("jp-ashiya-river", "Ashiya River", "芦屋川",
         "The short, steep river running from the Rokko mountains through the villa suburb of Ashiya to the sea, lined with pines and fine houses. The Makioka sisters live here in the late 1930s, and in the novel's best-known chapter the great flood of July 1938 pours down from the mountains and traps the youngest sister, Taeko, until a young photographer wades in to save her. Tanizaki's own house of those years is a museum in Kobe",
         "从六甲山流经别墅区芦屋入海的一条短而陡的河，两岸是松树和漂亮的宅邸。20 世纪 30 年代末，莳冈家的姐妹就住在这里。小说最著名的一章里，1938 年 7 月的大水从山上冲下，困住了最小的妹妹妙子，直到一个年轻的摄影师蹚水把她救出。谷崎当年在神户的住宅倚松庵如今是纪念馆",
         book_ids=["makioka-sisters"]),
    PIL("jp-takahan", "Takahan Ryokan, Echigo-Yuzawa", "越后汤泽 · 高半旅馆",
        "An old hot-spring inn on a hill above Echigo-Yuzawa, at the snowy end of the long tunnel through the mountains from Tokyo. Kawabata stayed here from 1934 and wrote Snow Country about a Tokyo dilettante's visits to a hot-spring geisha, Komako; the room he worked in, 'Kasumi-no-ma', is preserved as it was",
        "越后汤泽小山上的一家老温泉旅馆，就在从东京穿山而来的长隧道出口的雪国。川端康成从 1934 年起住在这里，写下《雪国》，讲东京一个无所事事的男人几次来温泉找艺伎驹子的故事。他写作的房间“霞之间”至今保持原样",
        ["snow-country"]),
    PIL("jp-shayokan", "Shayokan, Kanagi", "金木 · 斜阳馆",
        "The huge brick-walled mansion in Kanagi, Aomori, built in 1907 by Dazai's father, a rich landowner, where Dazai was born in 1909 and grew up as one of eleven children. It later became an inn named after The Setting Sun, and is now the Dazai Osamu Memorial Hall. The cold, grand house of No Longer Human, where the boy Yozo plays the clown for his family, draws on it",
        "青森金木一座砖墙环绕的巨大宅邸，1907 年由太宰治身为大地主的父亲建造。1909 年太宰生在这里，在十一个兄弟姐妹中长大。后来它成了以《斜阳》命名的旅馆，如今是太宰治纪念馆。《人间失格》里少年叶藏在家人面前扮小丑的那座冷冰冰的大宅，就取材于此",
        ["no-longer-human", "setting-sun"]),
    ORIG("jp-kinkakuji", "Kinkaku-ji, Kyoto", "京都 · 金阁寺",
         "The gilded three-storey pavilion of Rokuon-ji, reflected in its pond in the northern hills of Kyoto. In 1950 a young acolyte set fire to it and it burned to the ground; Mishima turned the crime into The Temple of the Golden Pavilion, the confession of a stammering monk obsessed by its beauty. The pavilion was rebuilt in 1955 and covered in new gold leaf in 1987",
         "京都北山鹿苑寺的三层金色楼阁，倒映在镜湖池中。1950 年，一个年轻的见习僧放火把它烧成了平地；三岛由纪夫把这桩罪行写成《金阁寺》，一个口吃的僧人对金阁之美着魔的自白。金阁 1955 年重建，1987 年重新贴了金箔",
         book_ids=["golden-pavilion"]),
    PROTO("jp-enshoji-nara", "Ensho-ji, Nara", "奈良 · 圆照寺",
          "A secluded convent of imperial princesses in the hills near Nara, usually closed to visitors. Mishima took it as the model for Gessho-ji in Spring Snow, where the young aristocrat Kiyoaki comes day after day through the snow to see Satoko, who has become a nun, and is turned away each time",
          "奈良附近山中一座由皇女住持的尼寺，平时不对外开放。三岛由纪夫以它为《春雪》中月修寺的原型：年轻的贵族清显冒着大雪一天又一天前来，想见已经出家的聪子，每次都被拒之门外",
          book_ids=["spring-snow"]),
    b.P("jp-hamaoka-dunes", "Hamaoka Dunes, Omaezaki", "御前崎 · 滨冈沙丘", *r.C("jp-hamaoka-dunes"), "film_location",
        adaptation={"title": "Woman in the Dunes (砂の女)", "year": 1964, "kind": "电影"},
        scene="敕使河原宏的电影《砂女》在这片远州滩海岸沙丘拍摄沙中村落的外景",
        scene_en="Hiroshi Teshigahara filmed the sand village of The Woman in the Dunes on these dunes on the Enshu-nada coast",
        book_ids=["woman-in-the-dunes"], fact_source="https://tabi-mag.jp/sz052/"),
    ORIG("jp-genbaku-dome", "Atomic Bomb Dome, Hiroshima", "广岛 · 原爆圆顶",
         "The ruin of the Hiroshima Prefectural Industrial Promotion Hall, left standing almost beneath the explosion of 6 August 1945 and kept as a memorial; it is a World Heritage Site. Ibuse's Black Rain, built from survivors' diaries, follows Shigematsu through the burning city that day, and the black rain that later falls on his niece Yasuko",
         "广岛县产业奖励馆的废墟，1945 年 8 月 6 日原子弹几乎就在它上空爆炸，残骸被保留下来作为纪念，是世界遗产。井伏鳟二根据幸存者日记写成的《黑雨》，跟着重松穿过那天燃烧的城市，也写了后来落在他侄女矢须子身上的黑雨",
         book_ids=["black-rain"]),
    PIL("jp-endo-museum", "Endo Shusaku Literary Museum, Sotome", "外海 · 远藤周作文学馆",
        "A museum on a cliff above the sea at Sotome, north of Nagasaki, in the region of the hidden Christians. Endo modelled Tomogi, the village where the Portuguese priest Rodrigues hides in Silence, on Sotome. Nearby a stone carries his words: 'Lord, man is so sad, and the sea is so blue'",
        "长崎北边外海的海崖上的一座文学馆，这一带是潜伏基督徒的地方。远藤周作以外海为原型，写了《沉默》中葡萄牙神父罗德里格藏身的友木村。附近的石碑上刻着他的话：“人这么悲哀，主啊，海却这么蓝”",
        ["silence-endo"]),
    ORIG("jp-uchiko", "Uchiko, Ehime", "爱媛 · 内子",
         "A town in the forested mountains of Ehime, Shikoku, that now includes Ose, the village in a deep valley where Oe was born in 1935. The village of The Silent Cry, to which the brothers Mitsusaburo and Takashi return and where Takashi stirs the young men to riot as their ancestors rose in 1860, is modelled on it",
         "四国爱媛森林山区的一座小镇，如今包括大濑——1935 年大江健三郎出生的深谷小村。《万延元年的足球》中兄弟蜜三郎和鹰四回到的村子就以它为原型，鹰四在那里煽动年轻人闹事，就像他们的祖先 1860 年起事一样",
         book_ids=["silent-cry"]),
    ORIG("jp-hotaru-monument", "Grave of the Fireflies monument, Nishinomiya", "西宫 · 《萤火虫之墓》诞生地纪念碑",
         "A monument near the Mankechi pond in Nishinomiya, the quiet suburb between Kobe and Osaka where Nosaka lived as a boy in 1945. In Grave of the Fireflies, fourteen-year-old Seita and his little sister Setsuko, burned out of Kobe in the air raids, leave their aunt's house here and live in a dugout shelter by the pond, catching fireflies, until Setsuko starves",
         "西宫满池谷附近的一座纪念碑，这片神户和大阪之间安静的郊区，是 1945 年少年野坂昭如住过的地方。《萤火虫之墓》里，十四岁的清太和年幼的妹妹节子在空袭中失去了神户的家，离开这里的姑妈家，住进池边的防空洞，捉萤火虫，直到节子饿死",
         book_ids=["grave-of-the-fireflies"]),
    PIL("jp-waseda-murakami", "Waseda International House of Literature (Murakami Library)", "早稻田国际文学馆（村上春树图书馆）",
        "Murakami studied drama at Waseda and has given it his manuscripts, letters and huge record collection. The university turned an old building into this library of world literature around them, opened in 2021 with an arching wooden tunnel of bookshelves designed by Kengo Kuma, and a café run by students",
        "村上春树在早稻田大学读戏剧专业，后来把自己的手稿、书信和大量唱片捐给了母校。大学把一座旧楼改建成以这些藏品为核心的世界文学图书馆，2021 年开馆，有隈研吾设计的拱形木质书架隧道，还有学生经营的咖啡馆",
        ["wind-up-bird", "hard-boiled-wonderland", "1q84"]),
    ORIG("jp-sangenjaya", "Sangenjaya and the Shuto Expressway", "三轩茶屋 · 首都高速",
         "A busy crossroads in Setagaya, Tokyo, where the elevated Shuto Expressway No. 3 runs above the old Tamagawa road. 1Q84 begins on that expressway: Aomame, stuck in traffic in a taxi with Janacek's Sinfonietta on the radio, climbs down an emergency stairway near Sangenjaya, and steps into a world with two moons",
         "东京世田谷一个繁忙的路口，高架的首都高速 3 号线在老玉川路上方穿过。《1Q84》从这条高速开始：青豆坐的出租车堵在路上，收音机里放着雅纳切克的《小交响曲》，她从三轩茶屋附近的紧急楼梯爬下去，走进了一个有两个月亮的世界",
         book_ids=["1q84"]),
    ORIG("jp-utsunomiya", "Utsunomiya", "宇都宫",
         "The capital of Tochigi, north of Tokyo. In All She Was Worth, the detective Honma traces his nephew's missing fiancée back here, to the hometown of the real Shoko Sekine, and finds that the woman his nephew knew had stolen the name and life of someone else",
         "东京北边栃木县的首府。《火车》里，刑警本间追查侄子失踪的未婚妻，一路追到这里——真正的关根彰子的家乡，发现侄子认识的那个女人盗用了别人的名字和人生",
         book_ids=["all-she-was-worth"]),
    ORIG("jp-osaka", "Osaka", "大阪",
         "Japan's merchant city on its bay, a sprawl of old shopping streets and new towers. Journey Under the Midnight Sun opens in Osaka in 1973 with the murder of a pawnbroker in an abandoned building, and follows his son Ryoji and the girl Yukiho for the next nineteen years",
         "濒临大阪湾的日本商业都市，老商店街和新高楼连成一片。《白夜行》以 1973 年大阪一栋废弃大楼里的当铺老板被杀开头，此后十九年一直追随他的儿子亮司和少女雪穗",
         book_ids=["journey-under-the-midnight-sun"]),
    ORIG("jp-kiyosu-bridge", "Kiyosu Bridge, Tokyo", "东京 · 清洲桥",
         "A blue suspension bridge of 1928 over the Sumida River, built after the great earthquake and modelled on a bridge in Cologne. In The Devotion of Suspect X, the mathematics teacher Ishigami walks to school every morning along the riverside path here, past the blue tarpaulin shelters of homeless men, which turn out to matter to his perfect alibi",
         "隅田川上一座 1928 年的蓝色吊桥，建于关东大地震之后，仿照科隆的一座桥。《嫌疑人X的献身》里，数学老师石神每天早上沿着这里的河边小道走去学校，经过流浪汉们的蓝色塑料布棚屋——后来才知道，这些棚屋正是他完美诡计的关键",
         book_ids=["suspect-x"]),
    ORIG("jp-tokyo", "Tokyo", "东京",
         "The capital, where A Personal Matter takes place over a few days of 1960s Tokyo: in hospitals, bars and the flat of an old girlfriend, the young crammer teacher Bird tries to escape the decision about his newborn son",
         "首都东京。《个人的体验》就发生在 20 世纪 60 年代东京的几天里：在医院、酒吧和旧情人的公寓之间，年轻的补习班教师“鸟”想逃避如何对待新生儿子的抉择",
         book_ids=["personal-matter"]),
    PROTO("jp-adams-memorial", "Anjinzuka, Yokosuka", "横须贺 · 按针冢",
          "The memorial to William Adams and his Japanese wife on a hilltop park in Yokosuka, near the estate at Hemi given him by Tokugawa Ieyasu. Adams, the first Englishman in Japan, became a samurai and the shogun's adviser; Clavell turned him into Blackthorne, the pilot of Shogun, whom the Japanese call Anjin, 'pilot'",
          "横须贺山顶公园里威廉·亚当斯和他日本妻子的纪念墓，附近就是德川家康赐给他的逸见领地。亚当斯是第一个来到日本的英国人，后来成为武士和将军的顾问；克拉维尔把他写成《幕府将军》里的领航员布莱克索恩，日本人叫他“按针”，即领航员",
          book_ids=["shogun"]),
    ORIG("jp-shukkeien", "Shukkeien Garden, Hiroshima", "广岛 · 缩景园",
         "A landscape garden of 1620 on the Kyobashi River, then called Asano Park after the lords who built it. On 6 August 1945 hundreds of burned survivors fled into it; in Hersey's Hiroshima, the Methodist pastor Kiyoshi Tanimoto ferries the wounded across the river in a punt and Father Kleinsorge carries water to them. The garden was restored after the war",
         "京桥川畔一座 1620 年的回游式庭园，当时以建造它的藩主之名叫浅野泉邸。1945 年 8 月 6 日，数百名被烧伤的幸存者逃进这里；赫西的《广岛》里，卫理公会牧师谷本清用一条小船把伤员渡过河，克莱因佐格神父为他们送水。庭园战后得到修复",
         book_ids=["hiroshima-hersey"]),
    ORIG("jp-gion", "Gion, Kyoto", "京都 · 祇园",
         "Kyoto's old geisha district, with wooden teahouses along the Shirakawa canal and the lanes below Yasaka Shrine. Memoirs of a Geisha follows Chiyo from a fishing village to an okiya here, where she is trained and renamed Sayuri, and where a kind stranger, the Chairman, buys her shaved ice by the Shirakawa stream",
         "京都的老艺伎区，白川沿岸是木结构的茶屋，八坂神社下方是石板小巷。《艺伎回忆录》讲千代从渔村被卖到这里的置屋，受训后取名小百合；就在白川边，一位好心的陌生人“会长”给她买了一碗刨冰",
         book_ids=["memoirs-of-a-geisha"]),
    ORIG("jp-tarumi", "Tarumi, Kobe", "神户 · 垂水",
         "A seaside district of western Kobe, looking across the strait to Awaji Island. In The Samurai's Garden, Stephen, a young Chinese painter recovering from tuberculosis, spends 1937 at his family's beach house in Tarumi, learning silence and patience from the old gardener Matsu while Japan wages war on China",
         "神户西部的海滨地区，隔着海峡遥望淡路岛。《武士的花园》里，患肺结核的年轻中国画家斯蒂芬 1937 年在家里位于垂水的海边别墅养病，跟老园丁松学会了沉默和忍耐，而那时日本正在侵略中国",
         book_ids=["samurais-garden"]),
    ORIG("jp-tsuruhashi", "Tsuruhashi (Ikaino), Osaka", "大阪 · 鹤桥（猪饲野）",
         "The district east of central Osaka, once called Ikaino, home to the largest Korean community in Japan since the colonial era; its market and Korea Town are full of grilled-meat restaurants. In Pachinko, Sunja leaves Busan in 1933 with her new husband and comes to live in the crowded shacks of Ikaino, where she sells kimchi and sweets to survive the war",
         "大阪市中心以东的地区，旧称猪饲野，殖民时代起就是日本最大的朝鲜人聚居区；如今的市场和韩国城里满是烤肉店。《柏青哥》里，顺子 1933 年随新婚丈夫离开釜山，住进猪饲野拥挤的棚屋，靠卖泡菜和糖果熬过了战争",
         book_ids=["pachinko"]),
    ORIG("jp-dejima", "Dejima, Nagasaki", "长崎 · 出岛",
         "The fan-shaped artificial island in Nagasaki harbour where, for two centuries of Japan's isolation, the Dutch East India Company kept its only trading post. The Thousand Autumns of Jacob de Zoet takes place here from 1799, as a young Dutch clerk falls for Orito, a scarred Japanese midwife. Many of the post's buildings have been rebuilt as a museum",
         "长崎港内扇形的人工岛，日本锁国的两百年间，荷兰东印度公司唯一的商馆就设在这里。《雅各布·德佐特的千秋》从 1799 年写起，一个年轻的荷兰文书爱上了脸上有疤的日本助产士织斗。商馆的许多建筑已复原为博物馆",
         book_ids=["jacob-de-zoet"]),
]

lines = [
    S("makioka-s1", "makioka-sisters", "jp-ashiya-river", "Book 2, Chapters 6–9", "中卷第六至九章",
      "In July 1938 days of rain break into a flood that pours down from the Rokko mountains through Ashiya. Sachiko waits at home for news while the youngest sister, Taeko, is trapped at her sewing school as water and boulders fill the streets; the young photographer Itakura wades through the torrent and brings her out, which will tangle her life even further.",
      "1938 年 7 月，连日大雨变成了洪水，从六甲山冲下，穿过芦屋。幸子在家里等消息，而最小的妹妹妙子被困在裁缝学校，街上满是洪水和巨石；年轻的摄影师板仓蹚过激流把她救了出来，这让她的人生更加纠缠不清。",
      ["flood"], ["洪水"], W + "The_Makioka_Sisters"),
    S("snow-s1", "snow-country", "jp-takahan", "Opening and ending", "开头与结尾",
      "The train comes out of the long tunnel into the snow country. Shimamura, a dilettante from Tokyo, returns to the mountain hot spring to see Komako, a young geisha who loves him wholeheartedly though he gives her nothing. On his last night a cocoon warehouse used as a cinema catches fire; Yoko, the girl from the train, falls from its balcony, and as Shimamura looks up, the Milky Way seems to pour down into him.",
      "火车穿过长长的隧道，就是雪国。东京来的闲人岛村又来到山中温泉看驹子——一个全心全意爱着他、而他什么也不给她的年轻艺伎。最后一夜，一座当作电影院的蚕茧仓库着了火，火车上遇见的姑娘叶子从楼上掉下来；岛村抬起头，银河仿佛向他倾泻下来。",
      ["Milky Way"], ["银河"], W + "Snow_Country"),
    S("nlh-s1", "no-longer-human", "jp-shayokan", "The First Notebook", "第一手记",
      "'Mine has been a life of much shame.' So begin the notebooks of Oba Yozo, the son of a rich provincial family, who from childhood cannot understand other people and hides his terror of them by playing the clown, until his act is seen through. Drink, women and a failed double suicide at Kamakura follow, until he is shut away in an asylum, 'disqualified as a human being'.",
      "“我这一生，尽是可耻之事。”大庭叶藏的手记就这样开头。他是外省富家的儿子，从小就无法理解别人，只能靠扮小丑来掩饰对人的恐惧，直到把戏被人看穿。此后是酒、女人和在镰仓的一次殉情未遂，最后他被关进精神病院，“失去了做人的资格”。",
      ["playing the clown"], ["扮小丑"], W + "No_Longer_Human"),
    S("setting-s1", "setting-sun", "jp-shayokan", "Chapters 1–8", "第一至八章",
      "After the war, the aristocrat Kazuko and her frail mother sell their Tokyo house and move to a small villa in Izu, where the mother slowly fades. Her brother Naoji returns from the army addicted to drugs and kills himself, and Kazuko, deciding that 'man was born for love and revolution', sets out to have a child by the dissolute novelist Uehara and raise it alone.",
      "战后，贵族小姐和子和体弱的母亲卖掉东京的房子，搬到伊豆的一座小别墅，母亲在那里慢慢衰弱下去。弟弟直治从军队回来后染上毒瘾，最终自杀；和子认定“人是为了爱和革命而生的”，决心和放荡的小说家上原生一个孩子，独自把他抚养长大。",
      ["love and revolution"], ["爱和革命"], W + "The_Setting_Sun"),
    S("golden-s1", "golden-pavilion", "jp-kinkakuji", "Chapters 1 and 10", "第一章与第十章",
      "Mizoguchi, a stammering priest's son from the Japan Sea coast, has heard all his life that nothing on earth is as beautiful as the Golden Pavilion. As an acolyte there he finds its beauty stands between him and life, even between him and women. One night in 1950 he sets it on fire, means to die in the flames, then runs to the hills, throws away his knife and poison, and decides to live.",
      "沟口是日本海边一个口吃的寺庙之子，从小就听父亲说世上没有比金阁更美的东西。他在金阁寺当了见习僧，却发现金阁的美横在他和生活之间，甚至横在他和女人之间。1950 年的一个夜里，他放火烧了金阁，本想死在火中，却跑上了山，扔掉了刀和毒药，决定活下去。",
      ["sets it on fire"], ["放火烧了金阁"], W + "The_Temple_of_the_Golden_Pavilion"),
    S("spring-s1", "spring-snow", "jp-enshoji-nara", "Chapters 49–54", "第四十九至五十四章",
      "Kiyoaki, the beautiful son of a new noble family, has hidden his love for Satoko until she is engaged to an imperial prince; then they become lovers, and she is sent to take vows at the Gessho-ji convent near Nara. Already ill, he comes from Tokyo and climbs to the gate day after day through the February snow, and is refused each time. He dies in Tokyo at twenty.",
      "清显是新贵族家的美少年，一直把对聪子的爱藏在心里，直到她和一位皇族订婚，两人才成了恋人；后来聪子被送进奈良附近的月修寺出家。已经生病的清显从东京赶来，冒着二月的大雪一天又一天爬到寺门前，每次都被拒绝。他回到东京后死去，年仅二十岁。",
      ["February snow"], ["二月的大雪"], W + "Spring_Snow"),
    S("hb-s1", "hard-boiled-wonderland", "jp-waseda-murakami", "Throughout", "全书",
      "In alternating chapters, a data encoder in a near-future Tokyo is hired by an old scientist who has secretly wired a program into his brain, and pursued through the sewers beneath the city by sinister creatures; and in a walled Town at the End of the World, a newcomer whose shadow has been cut off reads old dreams from unicorn skulls. Slowly the two stories turn out to be one.",
      "小说以单双章交替：在不远的未来的东京，一个“计算士”受雇于一位老科学家，对方暗中在他脑子里装了一段程序，他在城市地下的下水道里被险恶的怪物追赶；在一座有围墙的“世界尽头”小镇里，一个影子被剪掉的新来者从独角兽头骨里读取古老的梦。两个故事渐渐合而为一。",
      ["unicorn skulls"], ["独角兽头骨"], W + "Hard-Boiled_Wonderland_and_the_End_of_the_World"),
    S("kasha-s1", "all-she-was-worth", "jp-utsunomiya", "Throughout", "全书",
      "Honma, a Tokyo police inspector on leave after a shooting, agrees to find his nephew's fiancée, who vanished when a routine credit check revealed she had once gone bankrupt. Tracing her through Utsunomiya, Osaka and Nagoya, he finds that she was someone else: a woman crushed by her family's debts, who had taken over the identity of the real Shoko Sekine and perhaps killed her to do it.",
      "东京刑警本间因枪伤休假，答应帮侄子寻找失踪的未婚妻——一次例行信用调查发现她曾经破产，她随即消失了。他一路追查到宇都宫、大阪和名古屋，发现她其实另有其人：一个被家里的债务压垮的女人，冒用了真正的关根彰子的身份，也许还为此杀了她。",
      ["Shoko Sekine"], ["关根彰子"], W + "All_She_Was_Worth"),
    S("windup-s1", "wind-up-bird", "jp-waseda-murakami", "Book 1–2", "第一至二部",
      "Toru Okada, out of work in a quiet Tokyo suburb, goes looking for his wife's lost cat and meets a string of strange women; then his wife Kumiko disappears too. An old officer tells him how he survived being thrown down a dry well in Mongolia in 1938, and Toru climbs down into the dry well of an abandoned house nearby and sits in the dark for days, searching for a way to her.",
      "冈田亨在东京一个安静的郊区失了业，出门寻找妻子走失的猫，遇见一连串古怪的女人；接着，妻子久美子也失踪了。一位老军官讲起 1938 年他在蒙古被扔进一口枯井、竟活了下来的经历；于是亨爬进附近一座空宅的枯井，在黑暗里坐了好几天，寻找通向妻子的路。",
      ["dry well"], ["枯井"], W + "The_Wind-Up_Bird_Chronicle"),
    S("midnight-s1", "journey-under-the-midnight-sun", "jp-osaka", "Chapter 1", "第一章",
      "In 1973 a pawnbroker is found stabbed in an abandoned building in Osaka. Detective Sasagaki suspects a poor widow who was his customer, but she and her lover die before anything can be proved, and the case goes cold. For the next nineteen years Sasagaki keeps watching two children touched by that day, the pawnbroker's son Ryoji and the widow's daughter Yukiho, as a trail of crimes follows them.",
      "1973 年，大阪一栋废弃大楼里发现一个当铺老板被刺死。刑警笹垣怀疑他的一个顾客——一个穷寡妇，可她和她的情人在任何证据出现前都死了，案子成了悬案。此后十九年，笹垣一直盯着与那天有关的两个孩子：当铺老板的儿子亮司和寡妇的女儿雪穗，一连串罪案总是跟着他们。",
      ["abandoned building"], ["废弃大楼"], W + "Journey_Under_the_Midnight_Sun"),
    S("suspectx-s1", "suspect-x", "jp-kiyosu-bridge", "Chapters 1–2 and ending", "第一至二章与结尾",
      "Ishigami, a brilliant mathematician reduced to teaching high school, walks to work each morning along the Sumida past the homeless men's shelters, and stops every day at the lunch shop where his neighbour Yasuko works. When she and her daughter kill her violent ex-husband, he takes charge, building them an alibi so perfect that only his old university friend, the physicist Yukawa, can see what it cost.",
      "天才数学家石神沦落为高中老师，每天早上沿着隅田川步行上班，经过流浪汉的棚屋，每天都会去邻居靖子工作的便当店。靖子母女杀死了她施暴的前夫，石神接手了一切，为她们编了一个完美的不在场证明，只有他的大学老友、物理学家汤川看得出它付出的代价。",
      ["perfect"], ["完美"], W + "The_Devotion_of_Suspect_X"),
    S("1q84-s1", "1q84", "jp-sangenjaya", "Book 1, Chapter 1", "第一部第一章",
      "Aomame, a fitness instructor who is also a hired killer, is late for an appointment and stuck in a taxi on the jammed Shuto Expressway, with Janacek's Sinfonietta on the radio. The driver tells her there is an emergency stairway down to the street nearby, and warns her that things may look different afterwards. She climbs down in her high heels, and soon notices that there are two moons in the sky.",
      "健身教练青豆同时也是一名受雇的杀手。她赶着赴约，却被困在堵死的首都高速上的出租车里，收音机里放着雅纳切克的《小交响曲》。司机告诉她附近有一道下到地面的紧急楼梯，还提醒她，下去之后，事情可能看上去会不一样。她穿着高跟鞋爬了下去，不久便发现天上有两个月亮。",
      ["two moons"], ["两个月亮"], W + "1Q84"),
    S("pm-s1", "personal-matter", "jp-tokyo", "Throughout", "全书",
      "Bird, a twenty-seven-year-old crammer teacher who dreams of travelling in Africa, learns that his first son has been born with a brain hernia. Over the next days he drinks, hides with an old girlfriend and lets the doctors starve the baby, hoping it will die, until at last he turns back, takes the child from an abortion clinic and agrees to the operation that will save him.",
      "二十七岁的补习班教师“鸟”梦想去非洲旅行，却得知第一个儿子生下来就有脑疝。接下来几天，他酗酒，躲在旧情人那里，任由医生不给婴儿喂奶，盼着孩子死去；最后他终于回头，把孩子从一家堕胎诊所抱回来，同意做那场能救他性命的手术。",
      ["brain hernia"], ["脑疝"], W + "A_Personal_Matter"),
    S("rain-s1", "black-rain", "jp-genbaku-dome", "Throughout", "全书",
      "Years after the war, Shigematsu cannot find a husband for his niece Yasuko, because people say she has radiation sickness. To prove that she was not in the city that day, he copies out her diary and his own of August 1945: the flash, the march through burning streets, the dead in the river. But her diary records that on the way home a black rain fell on her, and she begins to sicken.",
      "战后多年，重松一直给侄女矢须子找不到婆家，因为人们说她得了原子病。为了证明那天她不在市区，他把她和自己 1945 年 8 月的日记抄了一遍：闪光、穿过燃烧街道的跋涉、河里的尸体。可是她的日记里写着，回家路上一场黑雨落在了她身上，而她开始病倒了。",
      ["black rain"], ["黑雨"], W + "Black_Rain_(novel)"),
    S("silence-s1", "silence-endo", "jp-endo-museum", "Chapters 1–8", "第一至八章",
      "In 1639 the young Portuguese Jesuit Rodrigues lands secretly in Japan to find his old teacher Ferreira, said to have renounced the faith. Hidden by poor Christian villagers in Tomogi, then betrayed by the weak Kichijiro, he is made to watch believers drowned and hung in pits, until he is told that if he steps on a bronze image of Christ they will be saved, and he hears a voice telling him to trample.",
      "1639 年，年轻的葡萄牙耶稣会士罗德里格偷偷登上日本，寻找据说已经弃教的老师费雷拉。他先被友木村贫穷的基督徒藏起来，后来被软弱的吉次郎出卖，被迫看着信徒们被溺死、被倒吊在坑里，直到有人告诉他：只要他踩一下铜制的基督像，他们就能得救。这时他听见一个声音叫他踩下去。",
      ["bronze image of Christ"], ["铜制的基督像"], W + "Silence_(Endo_novel)"),
    S("silentcry-s1", "silent-cry", "jp-uchiko", "Throughout", "全书",
      "After a friend's suicide and the birth of a disabled son, Mitsusaburo goes back with his wife and his brother Takashi to the family house in a forest valley in Shikoku. Takashi organises the village youths into a football team and then leads them in looting the supermarket owned by a Korean 'emperor', re-enacting the peasant rising led by their great-grandfather's brother in 1860.",
      "朋友自杀、残障儿子出生之后，蜜三郎和妻子、弟弟鹰四一起回到四国森林山谷里的老家。鹰四把村里的年轻人组织成一支足球队，然后带着他们抢了“超市天皇”——一个朝鲜人老板——的超市，重演了 1860 年他们曾祖父的弟弟领导的农民起义。",
      ["football team"], ["足球队"], W + "The_Silent_Cry"),
    S("fireflies-s1", "grave-of-the-fireflies", "jp-hotaru-monument", "Throughout", "全篇",
      "After their mother dies in the firebombing of Kobe in June 1945, fourteen-year-old Seita takes his four-year-old sister Setsuko to an aunt in Nishinomiya, who soon resents them. They move into a dugout shelter by a pond, light it with fireflies they catch, and live on what Seita can steal, until Setsuko dies of malnutrition; a month later Seita dies at Sannomiya station.",
      "1945 年 6 月，母亲死于神户大空袭，十四岁的清太带着四岁的妹妹节子投奔西宫的姑妈，没多久就遭了嫌弃。他们搬进池塘边的防空洞，用捉来的萤火虫照明，靠清太偷来的东西度日，直到节子营养不良而死；一个月后，清太也死在了三宫车站。",
      ["fireflies"], ["萤火虫"], W + "Grave_of_the_Fireflies_(short_story)"),
    S("shogun-s1", "shogun", "jp-adams-memorial", "Book 1", "第一卷",
      "In 1600 the English pilot John Blackthorne is shipwrecked with his starving crew at the fishing village of Anjiro and thrown into a pit by the local samurai. Brought before the great lord Toranaga, he learns Japanese ways with the help of his Christian interpreter Mariko, becomes a samurai, and is caught up in the struggle that will make Toranaga shogun.",
      "1600 年，英国领航员约翰·布莱克索恩和饥饿的船员在渔村安治劳遇难，被当地武士扔进地坑。他被带到大名虎长面前，在信基督教的翻译真理子帮助下学习日本的规矩，成了武士，卷进了一场将让虎长成为将军的权力斗争。",
      ["shipwrecked"], ["遇难"], W + "Sh%C5%8Dgun_(novel)"),
    S("hiroshima-s1", "hiroshima-hersey", "jp-shukkeien", "'The Fire' and 'Details Are Being Investigated'", "《大火》《细节正在调查》",
      "Hersey follows six survivors through 6 August 1945 and the days after. In the afternoon hundreds of burned and dying people crowd into Asano Park by the river; the Reverend Tanimoto finds a punt and ferries the wounded across, wading with them in the tide, while Father Kleinsorge fetches water in a kettle for those who cannot move.",
      "赫西跟随六名幸存者，写下 1945 年 8 月 6 日和此后的日子。那天下午，数百名烧伤、垂死的人挤进河边的浅野泉邸；谷本牧师找到一条平底船，把伤员渡过河，自己在潮水里蹚着；克莱因佐格神父则用水壶为动不了的人打水。",
      ["Asano Park"], ["浅野泉邸"], W + "Hiroshima_(book)"),
    S("geisha-s1", "memoirs-of-a-geisha", "jp-gion", "Chapters 1–8", "第一至八章",
      "Nine-year-old Chiyo, from the fishing village of Yoroido, is sold to an okiya in Gion and made a maid, bullied by the jealous geisha Hatsumomo. One day, weeping by the Shirakawa stream after a failed escape, she is comforted by a kind gentleman, the Chairman, who buys her a shaved ice and gives her his handkerchief, and she decides to become a geisha so she can meet him again.",
      "九岁的千代来自渔村养老町，被卖到祇园的置屋当女佣，受尽善妒的艺伎初桃欺凌。一天，逃跑失败的她在白川边哭泣，一位好心的绅士——“会长”——安慰了她，给她买了一碗刨冰，还把手帕送给她。她于是决心当上艺伎，好再见到他。",
      ["shaved ice"], ["刨冰"], W + "Memoirs_of_a_Geisha"),
    S("samurai-s1", "samurais-garden", "jp-tarumi", "Throughout", "全书",
      "Stephen, a twenty-year-old Chinese art student ill with tuberculosis, is sent in 1937 to his family's summer house in the seaside village of Tarumi. Cared for by Matsu, the silent old caretaker, he slowly learns his secret: Matsu has for decades loved Sachi, a woman with leprosy who lives in the mountain colony of Yamaguchi, while news comes of Japan's war on China.",
      "二十岁的中国美术学生斯蒂芬患了肺结核，1937 年被送到家里在海边垂水村的避暑别墅。他由沉默的老管家松照顾，慢慢知道了松的秘密：几十年来，松一直爱着住在山里麻风病人村山口的女子佐知；与此同时，日本侵华的消息不断传来。",
      ["Tarumi"], ["垂水"], W + "The_Samurai%27s_Garden"),
    S("pachinko-s1", "pachinko", "jp-tsuruhashi", "Book 1–2", "第一至二部",
      "Sunja, a lodging-house keeper's daughter in Busan, is pregnant by a married fish broker when a sickly young minister, Isak, marries her and takes her to Osaka in 1933. They live among Koreans in the crowded, pig-keeping slum of Ikaino, despised by the Japanese; when Isak is jailed, Sunja and her sister-in-law sell kimchi and sweets on the street to keep the family alive.",
      "釜山客栈老板的女儿顺子怀了一个有妇之夫——鱼贩汉洙——的孩子，体弱的年轻牧师以撒娶了她，1933 年带她到了大阪。他们住在猪饲野拥挤、养猪的贫民窟，和朝鲜人挤在一起，受日本人歧视；以撒入狱后，顺子和妯娌在街头卖泡菜和糖果，养活了一家人。",
      ["Ikaino"], ["猪饲野"], W + "Pachinko_(novel)"),
    S("zoet-s1", "jacob-de-zoet", "jp-dejima", "Parts 1–2", "第一至二部",
      "In 1799 the pious young Dutch clerk Jacob de Zoet arrives at Dejima to root out corruption and make his fortune, and falls for Orito Aibagawa, a Japanese midwife with a burned face who has been allowed to study with the Dutch doctor. When she is taken to a mountain shrine whose monks keep a terrible secret, Jacob, confined to his tiny island, can do nothing to save her.",
      "1799 年，虔诚的年轻荷兰文书雅各布·德佐特来到出岛，打算整肃腐败、发一笔财，却爱上了脸上有烧伤疤痕的日本助产士蓝场川织斗——她获准跟荷兰医生学医。后来她被带进一座山中神社，那里的僧人守着一个可怕的秘密，而被困在小岛上的雅各布无力救她。",
      ["Orito"], ["织斗"], W + "The_Thousand_Autumns_of_Jacob_de_Zoet"),
]

ALL_BOOKS = r.books + books
ALL_PLACES = r.places + places
ALL_LINES = r.lines + lines

HEAD = {"books": "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA.books = [\n",
        "places": "// Each place's admin-1 region is worked out from its coordinates by app.js.\nwindow.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA.places = [\n",
        "lines": "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA.lines = [\n"}

def write(name, entries, marker):
    path = b.data(name + ".js")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = ",\n".join("  " + b.obj(e) for e in entries)
    open(path, "w", encoding="utf-8").write(f"// Japan, hand-written content (tools/content/batches/add_jp1.py + add_jp2.py, {marker}).\n" + HEAD[name] + body + "\n];\n")

if __name__ == "__main__":
    ids = [x["id"] for x in ALL_PLACES]
    assert len(ids) == len(set(ids)), "duplicate place"
    bids = [x["id"] for x in ALL_BOOKS]
    assert len(bids) == len(set(bids)), "duplicate book"
    lids = [x["id"] for x in ALL_LINES]
    assert len(lids) == len(set(lids)), "duplicate line"
    for l in ALL_LINES:
        for p in l["place_ids"]: assert p in ids, (l["id"], p)
        assert l["book_id"] in bids, l["id"]
    for x in ALL_PLACES:
        for bk in x.get("book_ids", []): assert bk in bids, (x["id"], bk)
    film_books = {bk for x in ALL_PLACES if x["place_type"] == "film_location" for bk in x["book_ids"]}
    missing = set(bids) - {l["book_id"] for l in ALL_LINES} - film_books
    assert not missing, missing
    unused = set(ids) - {p for l in ALL_LINES for p in l["place_ids"]}
    print("places without a scene:", sorted(unused))
    write("books", ALL_BOOKS, "2026-11-18")
    write("places", ALL_PLACES, "2026-11-18")
    write("lines", ALL_LINES, "2026-11-18")
    print(len(ALL_BOOKS), "books,", len(ALL_PLACES), "places,", len(ALL_LINES), "lines")
