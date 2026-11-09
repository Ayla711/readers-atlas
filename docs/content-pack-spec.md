# 内容数据包格式（Content Pack）· v1.1

| 项 | 内容 |
|---|---|
| 用途 | 把一个国家（或地区）的书、地点、摘句、照片清单，按固定格式交给 The Reader's Atlas 导入。写内容的人或 AI 只需要按这个格式产出文件，不需要碰网站代码 |
| 提出 | 2026-11-08（用户决定：美国、中国、欧洲的内容可以交给其他 AI 产出，直接导入） |
| 导入工具 | `tools/import_pack.py <pack_dir>`（Week 2 完成）。导入前后自动跑 `tools/validate.js` 和 `tools/check_coverage.js` |
| 关联 | `docs/week1-uk-spec.md` 第 6 节（数据规格）、6.6（审核流程）、`docs/plan-week2-5.md` |
| 样例 | `packs/uk/`：英国数据反向导出的样例包（11-08）。给 Codex 做美国包的任务说明在 `packs/us-brief.md`，选题名单在 `tools/canon-us.json`，已占用的 id 在 `packs/existing-ids.json` |

## 0. 先读这一段：五条硬规则

这五条由导入脚本强制执行，不符合的条目会被整条拒收，并列在导入报告里。这些规则来自英国版踩过的坑，不是形式要求。

1. **公有领域的摘句必须能在原文里逐字找到。** 每条摘句要给出原文来源（古登堡编号或维基文库页面）；脚本会下载原文，逐字比对 `text_en`（或 `text_orig`）。找不到就拒收。**不要凭记忆写引文，不要改写，不要“大意如此”。**
2. **有版权的书只收场景说明，不收任何引文。** 作者去世不满 70 年的书，`public_domain` 为 `false`，摘句一律是 `kind: "scene"`，用自己的话写一两句发生了什么，不得含原文措辞（人名、地名等专名除外）。
3. **每个地点必须有坐标出处。** `coord_checked` 填一个公开网页（维基百科、Geograph、文物登录、官方网站等）的 URL，坐标从那里来。没有出处的坐标拒收。
4. **照片只给维基共享资源（Wikimedia Commons）的文件名，不给图片文件。** 许可只接受 CC0、公有领域、CC BY、CC BY-SA。影视取景地用实地照片，不用剧照。下载、缩放、署名由导入脚本做。
5. **所有文字成对：英文和中文都要有。** 英文字段只写英文（不出现中文、日文），中文字段用中文标点。界面上任何一个字段缺语言版本就显示不出来。

另外：所有导入的摘句和场景说明一律标 `status: "draft"`，由项目负责人审核后才会变成 `reviewed`。不要自己标 `reviewed`。

## 1. 目录结构

```
packs/<country>/            country 用 ISO 3166-1 两位小写代码：us、cn、fr、de、it……
  pack.json                 包的元信息
  books.json                书目（数组）
  places.json               地点（数组）
  lines.json                摘句和场景说明（数组）
  photos.json               照片清单（对象：地点 id → Commons 文件名和说明）
```

欧洲按国家分包（`fr`、`de`、`it`……），不做一个 `eu` 大包：每个国家的一级行政区划分不同，地图数据按国家生成。

文件都是 UTF-8 的 JSON，不是 JS。`id` 全局唯一、小写、用连字符；同一本书、同一个地点在不同包里不能重复出现（比如《东方快车谋杀案》只放在一个包里，地点可以跨国家，见 3.2）。

## 2. `pack.json`

```json
{
  "country": "us",
  "country_name": "United States",
  "country_name_zh": "美国",
  "region_scheme": "state",
  "produced_by": "Claude / <人名>",
  "produced_at": "2026-11-20",
  "notes": "第一批：每个州至少 1 个地点；东海岸为主"
}
```

`region_scheme` 说明一级行政区用什么：美国 `state`（50 州 + DC），中国 `province`（省、自治区、直辖市、特别行政区），法国 `region`，德国 `land`，意大利 `regione`，英国 `itl1`。地点**不填**所属一级区，导入时按坐标判断；坐标落在国外或海上会被标出来。

## 3. 四个数据文件

字段和 `docs/week1-uk-spec.md` 第 6 节一致，这里只写数据包里需要注意的地方。

### 3.1 `books.json`

```json
[
  {
    "id": "moby-dick",
    "title": "Moby-Dick",
    "title_zh": "白鲸",
    "author": "Herman Melville",
    "author_zh": "赫尔曼·梅尔维尔",
    "year": "1851",
    "orig_lang": "en",
    "public_domain": true,
    "source_url": "https://www.gutenberg.org/ebooks/2701",
    "aliases": ["Moby Dick", "The Whale"]
  }
]
```

- `public_domain` 按作者去世是否满 70 年判断（以网站所在的英国规则为准，不按美国的出版年规则）。拿不准就填 `false`，宁可只写场景说明。
- 原作不是英文的书，加 `title_orig`、`author_orig`（原文书名和作者名，只用于搜索），`orig_lang` 用 BCP-47（`zh`、`fr`、`de`、`ru`、`it`、`es`、`la`……）。
- 一本书只填一位作者。合著的书，第二位作者放进 `aliases`，这样能搜到。
- 同一位作者的 `author` 拼法在所有包里必须完全一致（比如都写 `Mark Twain`，不要一处 `Samuel Clemens`）。网站按这个字符串聚合作者页。

### 3.2 `places.json`

```json
[
  {
    "id": "new-bedford-seamens-bethel",
    "name": "Seamen's Bethel, New Bedford",
    "name_zh": "新贝德福德 · 海员礼拜堂",
    "lat": 41.6356,
    "lon": -70.9247,
    "place_type": "original",
    "note_en": "The whalemen's chapel Ishmael visits before sailing; the pulpit shaped like a ship's bow was added after the novel made it famous",
    "note": "以实玛利出海前去过的捕鲸人礼拜堂；船头形状的讲坛是小说出名以后才加的",
    "coord_checked": "Seamen's Bethel — https://en.wikipedia.org/wiki/Seamen%27s_Bethel",
    "fact_source": "https://en.wikipedia.org/wiki/Seamen%27s_Bethel"
  }
]
```

- `place_type` 四选一：`original`（书里写到的真实地点）、`prototype`（虚构地点的原型，必填 `prototype_of` / `prototype_of_en`）、`pilgrimage`（作家故居、墓地、纪念碑，必填 `book_ids`，多位作家共用的地方可用 `authors`）、`film_location`（影视取景地，必填 `adaptation: { title, year, kind }`、`scene` / `scene_en`、`book_ids`；`kind` 填 `电影` 或 `电视剧`）。
- `coord_checked` 格式：`<出处名> — <URL>`。导入时脚本补上日期。
- `fact_source`：地点说明里那些事实（谁住过、哪年建的、现在是什么）的出处 URL。和 `coord_checked` 可以是同一个页面。
- 面状地点（一座山、一片荒原、一个城市）取一个有代表性的点，并在 `note` 里说明摘句写的是整体。
- 地点跨国家时（比如一本法国小说写到日内瓦），放在地点所在国家的包里；如果那个国家还没有包，先放在书所在的包里，`notes` 里说明，导入时会按坐标归到正确的国家。

### 3.3 `lines.json`

**公有领域摘句**（必须能逐字核对）：

```json
{
  "id": "md-1",
  "book_id": "moby-dick",
  "place_ids": ["new-bedford-seamens-bethel"],
  "location": "Chapter 7, The Chapel",
  "location_zh": "第 7 章《礼拜堂》",
  "text_en": "In this same New Bedford there stands a Whaleman's Chapel, and few are the moody fishermen, shortly bound for the Indian Ocean or Pacific, who fail to make a Sunday visit to the spot.",
  "highlight_en": ["New Bedford", "Whaleman's Chapel"],
  "translation": "original",
  "source": { "kind": "gutenberg", "id": 2701 },
  "status": "draft"
}
```

- `source.kind` 可以是 `gutenberg`（给编号）、`wikisource`（给页面 URL）、`aozora`（青空文库，给 URL）、`ctext`（中国哲学书电子化计划，给 URL）。 样例包里有 10 条 `kind: "other"`，是英国早期用网页阅读工具核对的旧条目，新包不要用这个值。脚本从这里取原文逐字比对；`…` 表示省略了中间不相邻的部分，省略号前后各自比对。
- `location` 英文用阿拉伯数字（`Chapter 7`、`Book 2, Chapter 3`、`Act 4, Scene 1`），有标题的章写标题。
- 原作不是英文：`text_orig` 填原文，`text_en` 填英译，`translation` 填译本名称和译者（如 `Constance Garnett (1912)`），并加 `translation_source: { kind, id | url }` 指向这个译本的公有领域全文，脚本同样逐字核对译文。**没有公有领域英译的，暂时不收这条**（中国部分的英译方案待定，见 `week1-uk-spec.md` D-5）。
- `highlight_en`（和 `highlight_orig`）里的词必须在对应文本里原样出现。
- 一本书 1–10 条，宁少勿滥。每条都要真的写到那个地点。

**有版权的书：场景说明**

```json
{
  "id": "gatsby-s1",
  "kind": "scene",
  "book_id": "great-gatsby",
  "place_ids": ["great-neck"],
  "location": "Chapter 1",
  "location_zh": "第 1 章",
  "text_en": "Nick rents a small house in West Egg, next door to Gatsby's mansion, and looks across the bay to the green light at the end of Daisy's dock.",
  "text_zh": "尼克在西卵租了一座小房子，隔壁就是盖茨比的豪宅；他隔着海湾望见黛西家码头尽头的绿灯。",
  "highlight_en": ["West Egg"],
  "highlight_zh": ["西卵"],
  "status": "draft",
  "fact_source": "https://en.wikipedia.org/wiki/The_Great_Gatsby"
}
```

- 用自己的话，一两句，说这一处发生了什么。不要引原文，不要模仿原文的句式。
- `fact_source` 写情节依据（维基百科、书评、梗概页面），方便审核时核对章节和情节。

### 3.4 `photos.json`

```json
{
  "new-bedford-seamens-bethel": {
    "commons_file": "File:Seamen's Bethel, New Bedford MA.jpg",
    "alt_en": "The Seamen's Bethel on Johnny Cake Hill, New Bedford",
    "alt_zh": "新贝德福德约翰尼蛋糕山上的海员礼拜堂",
    "crop": null
  }
}
```

- 只给 Commons 的文件名。脚本会查许可（只接受 CC0、公有领域、CC BY、CC BY-SA）、下载、缩到 800 px 宽、去掉元数据、把作者和许可写进 `docs/photo-credits.md`。许可不符会拒收，并在报告里列出，可以换一张再导。
- 横图优先；竖图可以给 `crop: [x0, y0, x1, y1]`（0–1 的比例）裁成横图。
- 哪些地点要照片：作家朝圣地和影视取景地都要；原著地点和原型地有好照片就给。
- 不要给谷歌地图截图、不要给电影剧照、不要给来源不明的图。

## 4. 产出前的自查清单

交付前请逐条过一遍。导入脚本也会查，但自查能少来回一轮。

- [ ] 每本书：`public_domain` 判断有依据；有版权的书在 `lines.json` 里只有 `kind: "scene"`。
- [ ] 每条摘句：有 `source`；`text_en` 是从原文复制的，没有改动一个标点；`highlight_en` 里的词在 `text_en` 里原样出现。
- [ ] 每个地点：`coord_checked` 有 URL；`lat` / `lon` 小数点后 4 位；`place_type` 对应的必填字段齐全。
- [ ] 每个一级行政区至少有 1 个地点（这是“最小可演示包”的底线；后续的包可以只补某几个区）。
- [ ] 中英文成对；英文字段里没有中文。
- [ ] `id` 没有和已有的英国数据重复（现有 id 见 `data/*.js`）。
- [ ] 所有 `status` 都是 `draft`。

## 5. 导入后会发生什么

1. 脚本校验格式、核对原文、查照片许可，生成报告：收了多少、拒了多少、为什么。
2. 通过的条目并入 `data/<country>/books.js`、`places.js`、`lines.js`，照片进 `images/places/`，署名进 `docs/photo-credits.md`。
3. 跑 `validate.js`（引用、坐标落区、必填字段）和 `check_coverage.js`（对照这个国家的外部名单）。
4. 项目负责人审核草稿，改成 `reviewed`。

## 6. 规模建议

每个国家先交一个**最小可演示包**：20–30 本书、每个一级行政区至少 1 个地点、总共 50–80 个地点、50 条左右摘句和场景说明。导入是增量的，之后可以再交第二批、第三批，不用一次到位。

选书依据和英国一致（`week1-uk-spec.md` A-3）：有权威性的经典，加上长期畅销、有成型朝圣地的大众作品。先用 `tools/build_canon.py` 为这个国家生成外部名单（作家故居名单、国家级文学奖、公认的百大书单），从名单的缺口里选，不要从“我记得哪本书写到哪里”出发。

## 7. 变更记录

| 日期 | 版本 | 内容 |
|---|---|---|
| 2026-11-08 | v1.0 | 首版 |
| 2026-11-08 | v1.1 | 加样例包 `packs/uk/`、美国任务说明和名单的指引 |
