"""Patch 18 (11-24, night): places checked while adding the 6 South African books of rule v2 (data: tools/content/batches/
add_za2.py). Life & Times of Michael K: Prince Albert. A Dry White Season: the Hector Pieterson Museum, Soweto (the novel
begins with the uprising of 16 June 1976). Burger's Daughter: Johannesburg (city-level; the prison is not named). Country
of My Skull: East London, where the TRC's first hearings were held (city-level). Down Second Avenue: Marabastad. Chaka:
the Shaka Memorial, KwaDukuza (Shaka's grave, visited by Mofolo in 1909).
Only the notes change; decisions come from build.py (rule v2).
Run in tools/selection: python3 -I verify/p18_places_za_1124.py, then make_existing.py and build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
S = specio.load("za")
def upd(t, add):
    r = next(x for x in S["rows"] if x[0] == t); n = r[5]
    assert "核地点" not in n, t
    specio.setrow(S, t, note=n + "；核地点：" + add)
upd("Life & Times of Michael K", "艾伯特亲王镇，迈克尔·K把母亲的骨灰埋在那里的废弃农场")
upd("A Dry White Season", "小说从 1976 年 6 月 16 日索韦托起义开始，挂索韦托的赫克托·彼得森博物馆（标的是那一天，说明里已写明）")
upd("Burger's Daughter", "约翰内斯堡市中心点；开篇的监狱没写名字")
upd("Country of My Skull", "真相与和解委员会 1996 年 4 月在东伦敦市政厅举行第一批听证会，克罗格特别写了诺蒙德·卡拉塔在那里的证词；挂东伦敦市中心点")
upd("Down Second Avenue", "比勒陀利亚马拉巴斯塔德，第二大道所在")
upd("Chaka", "夸杜库扎的沙卡纪念地（沙卡墓，莫福洛 1909 年去过）")
specio.save("za", S)
print("ok")
