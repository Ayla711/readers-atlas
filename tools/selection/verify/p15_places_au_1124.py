"""Patch 15 (11-24, night): places checked while adding the 27 Australian books of rule v2 (data: tools/content/batches/
add_au2.py, add_au3.py). Invented towns are hung on the real place tied to them, with an honest note; for five books the
place is the film location (a film location carries no excerpt, so the novel's summary is in the film place's scene text).
Eucalyptus has the weakest tie (Bellingen, where sets were built for a cancelled film). Macquarie Island lies outside the
map's outline of Australia, so Wild Dark Shore is pinned at the Australian Antarctic Division near Hobart.
Only the notes change; decisions come from build.py (rule v2).
Run in tools/selection: python3 -I verify/p15_places_au_1124.py, then make_existing.py and build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
S = specio.load("au")
def upd(t, add, drop=None):
    r = next(x for x in S["rows"] if x[0] == t); n = r[5]
    if drop:
        assert drop in n, (t, drop); n = n.replace(drop, "")
    assert "核地点" not in n, t
    specio.setrow(S, t, note=n + "；核地点：" + add)
upd("Cloudstreet", "云街是虚构的，挂在电视剧放房子的珀斯西利德维尔")
upd("The Slap", "烧烤在诺斯科特赫克托和艾莎家")
upd("Voss", "挂在悉尼（1845 年开篇于邦纳家，劳拉在悉尼等待）")
upd("Oscar and Lucinda", "贝林根，玻璃教堂运去的地方（书中点名）")
upd("A Fortunate Life", "威克平，费西少年打工、1922—1934 年务农的地方，故居在主街")
upd("Breath", "索耶镇是虚构的，挂在 2017 年电影取景地西澳丹麦镇（取景地不挂摘句）")
upd("My Brother Jack", "挂在约翰斯顿童年住的埃尔斯特恩威克")
upd("Eucalyptus", "庄园和小镇都没写地名；按名著规则挂在贝林根（2005 年为电影搭过布景，电影取消），关系最弱，说明里已写明")
upd("The Narrow Road to the Deep North", "塔斯马尼亚的克利夫兰，多里戈长大的小村（书中点名）")
upd("Dirt Music", "怀特角是虚构的，挂在 2019 年电影取景地埃斯佩兰斯（取景地不挂摘句）")
upd("Carpentaria", "挂在诺曼顿（《Overland》书评认为德斯佩兰斯的原型是它）")
upd("Monkey Grip", "菲茨罗伊（合租屋与菲茨罗伊泳池）")
upd("The Tree of Man", "杜里尔盖是虚构的，挂在怀特 1948 年起务农的卡斯尔山")
upd("The Fortunes of Richard Mahony", "巴拉瑞特；公版摘句（英文维基文库，《幸运的澳大利亚》序章）")
upd("True History of the Kelly Gang", "格伦罗万，1880 年最后一战，小说以此开篇")
upd("Boy Swallows Universe", "布里斯班达拉区")
upd("The Dry", "没找到作者说过的原型；挂在 2020 年电影里改名基瓦拉的比尤拉（取景地不挂摘句）", drop="需找作者说过的原型；")
upd("Big Little Lies", "莫里亚蒂说半岛的样子取自悉尼以北的海滩，挂在北部海滩", drop="需找原型；")
upd("Remembering Babylon", "定居点没写名字；挂在原型人物詹姆斯·莫里尔 1863 年回到移民中间的贾维斯菲尔德")
upd("Tomorrow, When the War Began", "维拉威是虚构的，挂在 2010 年电影把国王街改成维拉威主街的雷蒙德台地（取景地不挂摘句）")
upd("Jasper Jones", "科里根是虚构的，挂在 2017 年电影取景地彭伯顿（取景地不挂摘句）")
upd("The Rosie Project", "故事在墨尔本，挂在墨尔本大学（读者通常这样认为，没核实书里点名）")
upd("The Light Between Oceans", "雅努斯岩和帕塔吉斯都是虚构的，挂在 2016 年电影取景地斯坦利（取景地不挂摘句）")
upd("Wild Dark Shore", "剪水鹱岛的原型是麦夸里岛，但它在地图轮廓外约 1500 公里，图钉标在霍巴特附近的澳大利亚南极局")
upd("Looking for Alibrandi", "格利布，乔茜的家")
upd("The Magic Pudding", "故事里没有现实地名，挂在林赛写作此书的福尔肯布里奇家（诺曼·林赛美术馆，朝圣地）", drop="你要收请说；")
upd("A Town Like Alice", "威尔斯敦是虚构的，舒特说原型是伯克敦")
specio.save("au", S)
print("ok")
