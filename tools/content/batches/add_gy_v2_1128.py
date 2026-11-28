"""11-28: Guyana, one more book after the 11-27 re-check left the country empty (tools/selection/gy.md, rule v2: thegreatestbooks
rank 449 and 30,095 Goodreads ratings; the user agreed on 11-27/28). The book record goes to the shared South American list
(data/sa/books.js), as for the other foreign books set in South America; no other country's files change. Place:
- St Ignatius, Rupununi, for A Handful of Dust: Tony Last and Dr Messinger land at Demerara and go upriver into Macushi
  country, and Mr Todd is "a British Guianan"; the novel never says on which side of the Brazilian border Todd's clearing
  lies (commentators often call it the Brazilian jungle). Waugh's own journey ran through the Rupununi, and he stayed twice
  at the Jesuit mission of St Ignatius in 1933, reading the Superior's Dickens there; the note says all this.
In copyright: a scene note, no quotation.
gy's places.js and lines.js are empty after the 11-27 deletion, so the first entry is written without a leading comma.
Usage: python3 -I tools/content/batches/add_gy_v2_1128.py <app_dir> tools/content/batches/coords/add_gy_v2_1128.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-28"
b.init(APP, "", "gy", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

def append(path, entries, marker):
    s = open(path, encoding="utf-8").read()
    i = s.rstrip().rfind("];")
    head = s[:i].rstrip()
    sep = "\n" if head.endswith("[") else ",\n"
    s = head.rstrip(",") + sep + "  // —— " + marker + " ——\n" + ",\n".join("  " + b.obj(e) for e in entries) + "\n];\n"
    open(path, "w", encoding="utf-8").write(s)

books = [
    dict(id="a-handful-of-dust", title="A Handful of Dust", title_zh="一抔尘土", title_orig="A Handful of Dust", author="Evelyn Waugh",
         author_zh="伊夫林·沃", year="1934", orig_lang="en", public_domain=False, source_url=None,
         aliases=["A Handful of Dust", "Mr Todd", "The Man Who Liked Dickens", "Tony Last"]),
]

places = [
    b.ORIG("gy-st-ignatius", "St Ignatius, Rupununi", "鲁普努尼 · 圣伊格内修斯", *C("gy-st-ignatius"),
        "An Amerindian village of the central Rupununi savannah, near Lethem and the Brazilian border, founded as a Jesuit mission; the area was settled by Macushi and Wapishana people. Evelyn Waugh stayed at the mission twice in 1933, in January and again from late February to early March, and there rediscovered the pleasure of reading with the Superior Fr Mather's Dickens; on the same journey he met the eccentric settler Christie. Out of the journey came the short story \"The Man Who Liked Dickens\" and the ending of A Handful of Dust (1934), in which Tony Last, lost in the interior, is held captive by Mr Todd and made to read Dickens aloud for ever",
        "鲁普努尼草原中部的一个印第安村庄，靠近莱瑟姆和巴西边界，最初是耶稣会建的传教站；这一带原是马库西人和瓦皮沙纳人的地方。伊夫林·沃 1933 年两度住在这里，一次在 1 月，一次从 2 月底到 3 月初，在那里读着传教站负责人马瑟神父的狄更斯，重新找回了读书的乐趣；同一趟旅途中他还结识了古怪的定居者克里斯蒂。这趟旅途后来化成了短篇《喜欢狄更斯的人》，也就是《一抔尘土》（1934）的结尾：托尼·拉斯特迷失在内陆，被托德先生扣住，被迫一遍遍给他朗读狄更斯"),
]

lines = [
    b.S("gy-dust-s1", "a-handful-of-dust", "gy-st-ignatius", "Chapters 5 and 6, “In Search of a City” and “Du Côté de Chez Todd”", "第五、六章《寻找一座城》《托德家那边》",
        "Tony Last, a contented country squire, loses everything at once: his wife Brenda has an affair with the social climber John Beaver, their son John Andrew is killed in a hunting accident, and Brenda asks for a divorce. To escape, Tony joins the explorer Dr Messinger in search of a lost city in the Amazon. They land at Demerara in British Guiana and go upriver into the country of the Macushi, who are reluctant to go on into the territory of the dreaded Pie-Wie. The guides desert, Messinger is swept over a waterfall, and the feverish Tony is found by Mr Todd, a British Guianan settler who rules a clearing in the forest. Todd cannot read but owns the complete Dickens; he nurses Tony back to health and has him read it aloud, and will not let him go; when a search party comes, Todd drugs Tony and sends them home with his watch. Waugh drew Todd from a settler named Christie he met in 1933 on his own journey through the Rupununi, when he stayed at the St Ignatius mission; the novel does not say on which side of the Brazilian border Todd's clearing lies.",
        "托尼·拉斯特是个心满意足的乡绅，却一下子失去了一切：妻子布伦达和一心往上爬的约翰·比弗有了私情，儿子约翰·安德鲁在一次狩猎事故中丧生，布伦达提出离婚。为了逃开，托尼跟着探险家梅辛杰博士去亚马孙寻找一座失落的城。他们在英属圭亚那的德梅拉拉上岸，溯河而上进入马库西人的地界，马库西人却不愿再往前进入令人畏惧的皮维人的领地。向导们跑了，梅辛杰被冲下瀑布，高烧中的托尼被托德先生发现：一个在林中空地上称王的英属圭亚那定居者。托德不识字，却有一套狄更斯全集，他把托尼照料好，让他念给自己听，却不肯放他走；搜救队来时，托德给托尼下了药，把他的手表交给他们带回英国。沃笔下的托德取材于他 1933 年自己穿越鲁普努尼时遇到的定居者克里斯蒂，那趟旅途中他住在圣伊格内修斯传教站；小说没有说明托德的空地在巴西边界的哪一边。",
        ["British Guiana", "Demerara", "Rupununi"], ["英属圭亚那", "德梅拉拉", "鲁普努尼"],
        "https://en.wikipedia.org/wiki/A_Handful_of_Dust; https://www.litcharts.com/lit/a-handful-of-dust/chapter-5-in-search-of-a-city; https://www.jesuitarchives.co.uk/post/evelyn-waugh-in-guyana; https://www.connotations.de/wp-content/uploads/2017/07/lobb01312.pdf; https://en.wikipedia.org/wiki/St._Ignatius,_Guyana"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places
assert not {l["id"] for l in lines} & all_lines
if __name__ == "__main__":
    note = "11-28 Guyana, one more book (add_gy_v2_1128.py)"
    append(SA_BOOKS, books, note)
    append(b.data("places.js"), places, note)
    append(b.data("lines.js"), lines, note)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
