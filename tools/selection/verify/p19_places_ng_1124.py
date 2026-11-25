"""Patch 19 (11-24, night): places checked while adding the 5 Nigerian books of rule v2 (data: tools/content/batches/
add_ng2.py). The Famished Road (unnamed city, taken to be based on the Lagos slum where Okri grew up) and Americanah on the
existing Lagos pin; The Palm-Wine Drinkard on the existing Aké, Abeokuta pin (Tutuola's birthplace); Arrow of God on Umuchu,
whose 1913 incident Achebe drew on (prototype); The Joys of Motherhood on Ibuza (Ibusa).
Only the notes change; decisions come from build.py (rule v2).
Run in tools/selection: python3 -I verify/p19_places_ng_1124.py, then make_existing.py and build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
S = specio.load("ng")
def upd(t, add):
    r = next(x for x in S["rows"] if x[0] == t); n = r[5]
    assert "核地点" not in n, t
    specio.setrow(S, t, note=n + "；核地点：" + add)
upd("The Famished Road", "城市没写名字，一般认为取材于奥克里长大的拉各斯贫民窟；挂已有的拉各斯，说明里已写明")
upd("Arrow of God", "乌穆阿罗、奥克佩里是虚构的；阿契贝取材于乌穆丘 1913 年祭司拒任酋长被关押的事，挂乌穆丘（原型）")
upd("Americanah", "伊菲麦露在拉各斯长大、回国后住在拉各斯，挂已有的拉各斯")
upd("The Palm-Wine Drinkard", "神话丛林；作者生在阿贝奥库塔，挂已有的阿凯（阿贝奥库塔），说明里已写明")
upd("The Joys of Motherhood", "伊布扎（伊布萨），努·埃戈的家乡，她最后死在那里")
specio.save("ng", S)
print("ok")
