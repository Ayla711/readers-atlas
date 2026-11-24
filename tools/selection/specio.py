"""Load / save spec_<cc>.py files (used by patch scripts in verify/)."""
import importlib.util, json
def load(cc):
    s = importlib.util.spec_from_file_location("s_"+cc, f"spec_{cc}.py"); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m.SPEC
def save(cc, S):
    r = lambda x: json.dumps(x, ensure_ascii=False)
    L = ["SPEC=dict(cc=%s," % r(S["cc"])]
    if S.get("existing_alias"): L.append("existing_alias=%s," % r(S["existing_alias"]))
    L.append("name=%s,date=%s," % (r(S["name"]), r(S["date"])))
    L.append("sources={")
    for k, v in S["sources"].items(): L.append("%s:%s," % (r(k), r(v)))
    L.append("},")
    L.append("size_note=%s," % r(S["size_note"]))
    L.append("rows=[")
    for row in S["rows"]: L.append("(%s)," % ",".join(r(x) for x in row))
    L.append("])")
    open(f"spec_{cc}.py", "w", encoding="utf-8").write("\n".join(L) + "\n")
def setrow(S, title, pts=None, add=None, note=None, dec=None):
    for i, row in enumerate(S["rows"]):
        if row[0] == title:
            t, a, k, p, d, n = row
            if pts is not None: p = pts
            if add: p = {**p, **add}
            if note is not None: n = note
            if dec is not None: d = dec
            S["rows"][i] = (t, a, k, p, d, n); return
    raise KeyError(title)
