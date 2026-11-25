"""Patch 17 (11-24, night): places checked while adding the 21 Egyptian books of rule v2 (data: tools/content/batches/
add_eg2.py; The Alchemist is already in the app under ma and gets its Egyptian line there). Invented or unnamed places are
hung on the real place tied to them, with an honest note: the imaginary alleys of Children of the Alley and The Harafish on
the Mahfouz museum in Gamaliya; Zayni Barakat, The Thief and the Dogs and Sharaf on a city-level Cairo pin; Rama and the
Dragon on Alexandria (no source names its setting); Seeds of Corruption on Humaithara (Mount Darhib has no coordinates);
The Call of the Curlew and The Days on Maghagha; War in the Land of Egypt on Tanta.
Only the notes change; decisions come from build.py (rule v2).
Run in tools/selection: python3 -I verify/p17_places_eg_1124.py, then make_existing.py and build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
S = specio.load("eg")
def upd(t, add, drop=None, repl=None):
    r = next(x for x in S["rows"] if x[0] == t); n = r[5]
    if drop:
        assert drop in n, (t, drop); n = n.replace(drop, repl or "")
    assert "核地点" not in n, t
    specio.setrow(S, t, note=n + "；核地点：" + add)
upd("Children of the Alley", "街区是虚构的，马哈福兹的小巷来自他出生的贾马利亚；挂在贾马利亚的马哈福兹博物馆（与《梅达格胡同》同一处）")
upd("The Harafish", "维基百科：书中既没写城市也没写年代；挂在贾马利亚的马哈福兹博物馆，说明里已写明")
upd("The Thief and the Dogs", "在开罗各处走动，结尾在一片没有名字的墓地；挂开罗市中心点")
upd("Zayni Barakat", "写整座马穆鲁克开罗的“城市小说”，没有单一地点；挂开罗市中心点")
upd("Rama and the Dragon", "找不到资料说明小说的具体背景地；挂在作者出生、长大的亚历山大，说明里已写明", drop="亚历山大；")
upd("No One Sleeps in Alexandria", "二战时的亚历山大（市中心点）")
upd("Seeds of Corruption", "故事在东部沙漠靠近苏丹边境的达尔希卜山一带，但达尔希卜山查不到坐标；挂在启发这部小说的东部沙漠之旅经过的胡迈斯拉（沙兹利圣陵，坐标取自维基数据）", drop="地点待查；")
upd("The Heron", "因巴巴的基特卡特街区（图钉标因巴巴）")
upd("The Lamp of Umm Hashim", "赛义达·宰娜卜清真寺")
upd("Return of the Spirit", "主要在开罗的赛义达·宰娜卜区（林恩·林纳版），挂赛义达·宰娜卜清真寺")
upd("The Open Door", "高潮在 1956 年的塞得港，挂塞得港")
upd("Azazeel", "希帕提娅在亚历山大被杀，挂亚历山大")
upd("Woman at Point Zero", "盖纳提尔女子监狱（盖纳提尔监狱建筑群）")
upd("The Call of the Curlew", "阿姆娜的村子贝尼·瓦尔坎没找到位置，小说背景是上埃及乡村；挂马加加（作者家乡村子附近），说明里已写明。塔哈·侯赛因博物馆原本想作朝圣地，但 Commons 上唯一的照片是从公司网站拷来的，没有可用的自由授权照片，没收", drop="上埃及乡村，地点待查；")
upd("The Days (al-Ayyam)", "马加加附近的基卢村，村子没有坐标，挂马加加")
upd("Sunset Oasis", "锡瓦绿洲")
upd("Sharaf (Honor)", "书里的监狱没有名字；挂开罗市中心点", drop="监狱，地点待查；")
upd("War in the Land of Egypt", "村子没有名字，在三角洲城镇坦塔附近；挂坦塔", drop="地点待查；")
upd("The English Patient", "泳者洞，阿尔玛西把凯瑟琳留在那里")
upd("The Alchemist", "书已在摩洛哥数据里（丹吉尔）；埃及这一条挂吉萨大金字塔，圣地亚哥在那里挖掘")
upd("The Egyptian", "底比斯（卢克索）")
specio.save("eg", S)
print("ok")
