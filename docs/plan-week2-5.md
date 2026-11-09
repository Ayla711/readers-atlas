# Week 2–5 计划（11-09 至 12-08）· v1.0

| 项 | 内容 |
|---|---|
| 状态 | 2026-11-08 晚定稿，用户确认的决定见第 1 节 |
| 前提 | 英国版功能完成（`docs/week1-uk-spec.md` v1.61）；157 本书、251 个地点、201 条摘句和场景说明，其中 57 条草稿待审（T-1 至 T-8） |
| 目标 | 12-08 演示：全世界地图，英国 + 美国 + 中国 + 欧洲若干国家可交互；有登录；个人数据能跨设备；排行榜（示例数据） |

## 1. 11-08 定下的决定

| 编号 | 决定 |
|---|---|
| A-16 | 后端先用 Supabase（登录、Postgres、文件存储），演示那个月升 Pro 避免免费项目一周不用被暂停；12-08 之后换成自己写的后端。数据表结构由我们自己定，不用 Supabase 专有特性，方便搬家 |
| A-17 | 前端托管在 GitHub Pages（公开仓库）。本地双击 `index.html` 仍然能用 |
| A-18 | 美国、中国、欧洲的内容可以由其他 AI 按 `docs/content-pack-spec.md` 产出，用 `tools/import_pack.py` 导入；导入脚本强制核对原文、坐标出处、照片许可 |
| A-19 | 不登录照常能用（数据在本机），登录只增加同步、旅行日志照片的云端保存和排行榜。演示时网络出问题，地图和书照常 |
| A-21 | （11-09 下午改）国家数据按需加载、加载后常驻、同时显示：世界页点一个已开放的国家，`js/data.js` 加载它的数据文件，app.js 把它的大区、地点、索引增量挂载到现有地图上，不卸载已加载的国家；首屏先装 URL 指向的国家（默认英国），1.5 秒后后台预取其余已开放国家。深链接指向未加载国家的 id 时，依次加载已开放国家直到找到。页面不重载。原先“一国一页、切换即重载”的方案已撤回 |
| A-20 | 排行榜先做示例版：界面定型，百分位从一组写死的示例分布算，页面上标“示例数据”；接上后端后换成真实聚合 |
| D-5 | 中国部分的英译方案待定（公有领域英译少）。中国包先收不依赖英译的内容：朝圣地、原型地、有公有领域英译的古典作品。Week 4 做中国包前决定 |
| 规模 | 每个国家先交“最小可演示包”（20–30 本书、每个一级区至少 1 个地点），之后增量加包 |

## 2. 日程（11-09 下午修订，v1.5）

重构比预计快 5 天（R-1 至 R-7 在 11-09 完成），省下的时间给内容线和后端留缓冲。

| 时间 | 主题 | 交付 |
|---|---|---|
| 11-09 | 基础设施 | `git init` + GitHub 私有仓库（用户）；检查脚本和内容工具进仓库（`tools/checks/`、`tools/content/`）；GitHub Pages 开通，拿到公开地址 |
| 11-10 | **Week 2 收尾** | R-8 `import_pack.py` / `export_pack.py`（机器核对：原文逐字、坐标出处、照片许可、id 与作者拼法）；R-11 审核页 `#/review`（草稿逐条通过 / 打回，导出 decisions.json）；R-9 排行榜示例版 |
| 11-11 至 11-14 | **最小后端** | Supabase 项目；邮箱魔法链接登录；8 个本地键 + 旅行日志 + 照片同步；首次登录导入本机数据；在 Pages 地址上跑通 |
| 11-15 至 11-30 | **三个地区** | 美国包（Codex）导入验证流程 → 欧洲（法、德、意各 15–20 本书，每个一级区至少 1 地点）→ 中国（D-5 在 11-15 前定）；每导一个包用户审一轮，审核不卡发布（草稿带标签照常显示） |
| 12-01 至 12-08 | **缓冲与彩排** | 世界视图和懒加载已完成；这一周只修错、补内容、写演示脚本、彩排两次；不加功能 |
| 12-08 之后 | 自己写的后端 | 按第 4 节的接口替换 Supabase；R-10 拆 app.js |

风险与对策：
- 内容是瓶颈，审核更是：审核页（R-11）和导入脚本的机器核对把人工审核压到“这段选得对不对”。
- 中国包的英译（D-5）两个选项：(a) 只收原文 + 场景说明，`text_en` 用我们自己的直译并标“工作译文”；(b) 只收有公有领域英译的古典作品 + 朝圣地。倾向 (a)，11-15 前定。
- 演示第 3 步“点中国”的退路：中国只有朝圣地和古典诗词。
- 美国 `geo.js` 1.2 MB（阿拉斯加海岸线）：Pages 会压缩，上线后看实际加载时间再决定是否简化。

## 3. Week 2 重构任务

目标：代码和数据从“英国专用”变成“国家可配置”，同时把个人数据的读写收口，为后端做准备。每项做完都要过现有的全部检查（`validate.js`、标签、圆点、旗标、中文字符），英国的行为不能变。

| 编号 | 任务 | 涉及 | 验收 |
|---|---|---|---|
| R-1 ✅ 11-09 | 国家配置表 `data/countries.js`：代码、中英文名、一级区划名称（state / province / region…）、默认视图范围、数据文件路径 | 新文件 | 英国是第一条记录 |
| R-2 ✅ 11-09 | `build_geo.py` 按国家配置：输入 Natural Earth 一级行政区 + 国家代码 + 可选的合并规则（英国 232 单元 → 12 区是合并规则的一个实例；美国 50 州不合并），输出 `data/<country>/geo.js` | `tools/build_geo.py` | 重新生成英国 geo.js 后和现在逐字节一致，或只有可解释的差异 |
| R-3 ✅ 11-09（含懒加载）| 数据按国家拆目录：`data/uk/{books,places,lines,geo}.js`；`index.html` 只加载世界轮廓 + 国家列表，进入某国时再加载该国数据（动态插入 `<script>`，仍然双击可用） | `index.html`、`app.js` 加载部分 | 首屏不加载任何国家数据；进入英国时加载并缓存 |
| R-4 ✅ 11-09 | 地点加 `country` 字段（导入时按坐标填，校验时核对）；`validate.js` 的“落在 12 个大区之一”改成“落在所属国家的某个一级区” | `data/*/places.js`、`tools/validate.js` | 英国 251 个地点全部 `country: "uk"`，0 错误 |
| R-5 ✅ 11-09 | 路由和界面去英国化：`#/uk` → `#/{country}`；`goUK`、`gUK`、面包屑 “United Kingdom”、左上角标题、`zoom-uk` 按钮、世界首页点国家的逻辑（有数据的国家进入，没有的提示“开放时间”）全部读国家配置 | `app.js`、`i18n.js` | 英国所有旧链接仍然可用（`#/uk` 保留） |
| R-6 ✅ 11-09 | 个人数据收口：新建 `js/store.js`，提供 `get/set` 之外的领域方法（`wishlist.add`、`visited.toggle`、`shelf.set`、`faves.toggle`、`notes.set`、`itinerary.add/remove`、`prefs`），`app.js` 不再直接碰 localStorage；`journal-store.js` 保持接口，内部并入同一套“本地 / 云端”切换 | `app.js`、新 `store.js` | `grep localStorage js/app.js` 为 0；行为不变 |
| R-7 ✅ 11-09 | 导出 / 导入个人数据（JSON 文件，R-5 风险项）：侧栏“我的旅行”底部一个入口；导出的 JSON 形状就是将来同步到后端的形状 | `store.js`、`app.js`、`i18n.js` | 导出再导入后数据一致 |
| R-8 | `tools/import_pack.py` 和 `tools/export_pack.py`：按 `content-pack-spec.md` 校验、核对原文、查照片许可、并入 `data/<country>/`；先用英国反向导出的包做回归（导出 → 导入 → 和现在一致） | 新脚本 | 英国包往返一致 |
| R-9 | 排行榜示例版：“我的旅行”统计区加“你超过了 X% 的读者”，指标是去过的文学地点数和走过的一级区数；示例分布写在 `data/leaderboard-sample.js`，页面标“示例数据” | `app.js`、`i18n.js`、`css` | 中英文都有；数字随本机数据变 |
| R-11 | 审核页 `#/review`：列出所有 `status: "draft"` 的摘句和场景说明，逐条看原文与地点、一键通过 / 打回并写备注；结果导出 `decisions.json`，`tools/apply_review.py` 写回数据文件 | `app.js`、`i18n.js`、新脚本 | 审完的条目 status 变 reviewed，打回的进待办 |
| R-10 | `app.js` 拆分（演示后）：至少把地图渲染、侧栏页面、路由、个人数据分成四个文件 | `js/` | 不改行为 |

顺序建议：R-6、R-7 先做（独立、风险低、后端直接依赖）→ R-1、R-2、R-3、R-4 一起做（数据层）→ R-5（界面层）→ R-8 → R-9 → R-10。

## 4. 后端接口（Supabase 阶段就按这个建表，以后自己写后端沿用）

表都带 `user_id`，行级安全：只能读写自己的行。所有时间用 UTC ISO 字符串。

| 表 | 字段 | 对应本地键 |
|---|---|---|
| `user_places` | `user_id, place_id, kind ('wishlist'\|'visited'), created_at` | `ra.wishlist`、`ra.visited` |
| `user_trips` | `user_id, id, place_id, date, note, created_at` | `ra.itinerary` |
| `user_books` | `user_id, book_id, shelf ('want'\|'read'\|null), favourite bool, note text, updated_at` | `ra.shelf`、`ra.faves`、`ra.notes` |
| `user_prefs` | `user_id, lang, sound, updated_at` | `ra.lang`、`ra.sound` |
| `journal_entries` | `user_id, id, place_id, visit_date, title, text, book_ids, created_at, updated_at` | `ra.journal`（`travel-journal-spec.md` 第 6 节） |
| `journal_photos` | `user_id, id, entry_id, path, thumb_path, width, height, caption, taken_at, sort` | IndexedDB `ra-journal` |
| `leaderboard_stats`（视图） | `user_id, places_visited, regions_visited` | 由 `user_places` 聚合；排行榜百分位从这里算 |

同步规则：
- 游客模式只写本地。登录后首次：本地有、云端没有的条目上传；两边都有的以 `updated_at` 新者为准；之后每次改动先写本地再写云端，失败时记一个待同步标记，下次打开重试。
- 照片走文件存储，路径 `journal/<user_id>/<photo_id>.jpg` 和 `_thumb.jpg`；浏览器里缩图的逻辑不变。
- 删除日志同时删照片；删除账号删全部（`travel-journal-spec.md` 第 5 节）。

前端只有 `store.js` 和 `journal-store.js` 知道后端的存在；换成自己写的后端时，这两个文件里的 Supabase 调用换成 fetch。

## 5. 演示（12-08）要能走通的路线

1. 打开 GitHub Pages 地址，开场动画，世界地图。
2. 点英国 → 大区 → 地点 → 摘句、原文、照片；搜索一本书。
3. 点美国 → 州 → 地点；点一个欧洲国家；点中国。
4. 游客身份收藏几处、收藏一本书，书架抽书。
5. 登录 → 数据跟过来 → 换一个浏览器登录，数据还在。
6. 写一篇带照片的旅行日志。
7. 我的旅行：统计、排行榜（示例数据标注）。

每一步都要有离线或断网时的退路：1–4、7 不需要网络；5、6 需要。

## 6. 变更记录

| 日期 | 版本 | 内容 |
|---|---|---|
| 2026-11-08 | v1.0 | 首版 |
| 2026-11-09 | v1.5 | 整体复盘后重排日程：后端提前到 11-11；Pages 11-09 上线；内容线 11-15 至 11-30；12 月第一周改为缓冲与彩排。新增 R-11 审核页；R-10 推到演示后。检查脚本与内容工具入库（`tools/checks/`、`tools/content/`），仓库加 `.gitignore`、README 加版本控制与上线一节。欧洲最小包缩为每国 15–20 本书 |
| 2026-11-09 | v1.4 | 按用户要求撤回“切换国家即重载”：改为按需加载 + 增量挂载 + 同时显示（A-21 改写）。新 `js/data.js`（RA_LOAD）；`js/boot.js` 删除；app.js 的查找表、大区、标记、标签掩膜、搜索索引全部改成累计式 `mountCountry()`；掩膜编码扩到 144 个区、大国自动降分辨率；“国家尺度”的缩放阈值按国家宽度折算（`zCountry`）；首页区列表按国家分组，“我的旅行”按国家统计。用 Natural Earth 生成了 `data/us/geo.js`（51 州，无内容，`open: false`）做双国测试：加载、并存、深链接、标签布局（51 州 19 ms）全部通过；英国 8 个视图逐像素不变 |
| 2026-11-09 | v1.3 | R-3 收尾、R-5 完成：路由 `#/<国家代码>`（`#/uk` 照旧）；面包屑、地图标题、封面提示、⤢ 按钮、统计文案、aria 标签都读国家配置（`short`/`name`）；大区颜色和“太小不标名”的区（伦敦）进配置（`wash`、`small_regions`）；世界页已开放的国家涂色可点（进入即重载到该国），未开放的国家悬停显示“暂未开放”；`#/xx` 指向未开放国家时回世界页。英国 6 个视图逐像素不变。决定 A-21 |
| 2026-11-09 | v1.2 | R-1、R-2、R-4 完成，R-3 完成一半：`tools/countries.json` → `data/countries.js`；`build_geo.py` 按国家出 `data/<code>/geo.js`（英国 regions、units 与旧文件逐字节一致）和 `data/world-geo.js`（205 国，含英国，应用隐藏当前国家）；数据搬到 `data/uk/`；`js/boot.js` 按 URL 选国家、加载它的数据文件再启动 app.js。还差的一半：世界页不加载任何国家数据、进入某国时再加载，要等 R-5 让 app.js 能在运行中切换国家。`validate.js` 按国家校验，地点必须带 `country` |
| 2026-11-09 | v1.1 | R-6、R-7 完成：`js/store.js`（RA_STORE：kv 后端、领域方法、onChange、exportData / importData）；`journal-store.js` 改走同一 kv 后端并加 importEntries；`app.js`、`bookopen.js` 不再直接碰 localStorage。导出 JSON 的表结构即第 4 节；导入为追加合并，日志照片不随文件走 |
