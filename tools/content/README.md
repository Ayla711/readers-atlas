# tools/content — 内容制作工具（人工批次与照片）

内容现在有两条路：
1. **内容包**（美国、欧洲、中国）：按 `docs/content-pack-spec.md` 产出 JSON，用 `tools/import_pack.py` 导入（R-8）。
2. **手写批次**（英国历史批次，以及以后的小修补）：Python 脚本调用 `batchlib.py`，每条摘句都从古登堡原文文件里切出来，坐标都带出处。

## batchlib.py
```python
import sys; sys.path.insert(0, "tools/content")
import batchlib as b
b.init(app_dir=".", tx_dir="cache/pg", country="uk", date="2026-11-09")
b.prose(1342, "起始句", "结束句")          # 一段之内，从起始句到结束句（含），逐字
b.paras(1342, ("a", "b"), ("c", "d"))     # 相邻几段，用换行连接
b.verse_lines(610, "起始行", 14)          # 诗：从含起始行的那行起 14 个非空行
b.B(...)  b.ORIG(...)  b.PROTO(...)  b.PIL(...)  b.L(...)  b.S(...)   # 书、地点（三种）、摘句、场景说明
b.append(b.data("places.js"), [..], "批次说明")   # 追加到 data/<country>/<file>
```
古登堡原文：`https://www.gutenberg.org/cache/epub/<n>/pg<n>.txt` 存为 `cache/pg/<n>.txt`（`cache/` 不进 git）。

`batches/` 是英国各批次的脚本原件（11-03 至 11-09），保留作记录；它们引用的是旧路径 `data/places.js`，如需重跑请改成 `data/uk/`。

## photos/ 照片流水线（只用自由许可：CC0 / 公有领域 / CC BY / CC BY-SA）
1. `find_photos.py <工作目录> <queries.json>` — 在 Commons 搜候选，过滤许可、尺寸、横图，记下文件页上的拍摄/对象坐标，写 `candidates.json` 和 `urls.tsv`。
2. `dl_here.py <工作目录>` — 下载候选缩略图到 `dl/`（Commons 限速，会慢）。
3. `contact_sheet.py <工作目录> <每张几处>` — 拼预览图挑选（每处最多 4 张候选，标序号和许可）。
4. 写 `choice.json`：`{"地点id": [候选序号, "英文替代文字", "中文替代文字", null], ...}`
5. `attach_photos.py <仓库目录> <国家> <工作目录>` — 缩到 800 px、写进 places.js、署名追加到 `docs/photo-credits.md`。
然后 `node tools/validate.js <国家>`。
