# 美国累计包 · REVIEW-2 定点修订报告

2026-11-11，依据 docs/content-pack-spec.md v1.3 与 REVIEW-2.md。仅处理点名修改；未开始新批次，没有新增书目、地点或 ID。详细逐项回应见 REVISION-2.md。

## 交付结果

- 45 本书、84 个地点、90 条内容：62 条公有领域摘句、28 条原创场景说明；50 张照片清单
- 删除 6 条，其余 ID 不变；全部内容保持 draft
- 法尔茅斯与迪比克均找到更有地方分量的原文并替换，不再保留原过境／名单片段
- 《喧哗与骚动》从 5 条减为 3 条，密西西比仍有内容；50 州及华盛顿特区的地点覆盖保持
- 完整累计包，可整体导入；本次没有正式导入或修改 data/、images/，没有修改 tools/us-revision/ 以外的工具

## 核验

`python3 -I tools/import_pack.py packs/us --dry-run`：**0 错误、5 条提示**，没有未逐字核对或仅宽松匹配的引文。详见 IMPORT.md。

其中三条沿用既有地图简化提示：Charleston 距简化海岸线约 1 km，归 SC；Pepin 在简化图上落到 MN，距 WI 约 2.2 km，按报告保留 WI；St. Louis 在简化图上落到 IL，距 MO 约 1.4 km，按报告保留 MO。另两条是删除点名摘句后 Lincoln、Omaha 没有行关联；按本次范围保留这两个既有地点，未擅自扩大删除范围。

《啊，拓荒者！》随点名摘句删除后为 0 条；按本次“只做点名修改”限制保留既有书目／地点关联，明确记录这一与通常每书 1–10 条建议的差别。不会用另一条薄弱引文补数。

`python3 tools/us-revision/review2/verify.py`：0 错误。检查修改白名单、无新增或改名 ID、书目未变、精确原文片段、双语高亮、三条 Faulkner 内容、removed 无现存 ID、以及受保护文件哈希未变。新摘句均由实际重新联网下载的 Gutenberg 原文用脚本截取，译文为自译；us-rs-4 的省略号两侧分别连续匹配。仅 New Orleans 高亮按导入器空白规范化核验。

## 事实与照片来源

- 电影院票数：[Frost Place 诗歌文本，第 5 页](https://frostplace.org/wp-content/uploads/2020/09/New-Hampshire-Poem-Text.pdf#page=5)。只用作场景事实依据，未将 Frost 的文字加入引文
- 费城替换照片：[EDAL-NHS.jpg](https://commons.wikimedia.org/wiki/File:EDAL-NHS.jpg)，公有领域，2048×1536
- Fort Smith 替换照片：[Fort Smith, AR 003.jpg](https://commons.wikimedia.org/wiki/File:Fort_Smith,_AR_003.jpg)，CC BY-SA 4.0，4081×2299

两张均与原有许可类别相同且为横图。现有原照片本来也有大尺寸源文件；500 px 是导入产物的尺寸。导入器可能在请求失败时回退到 500 px，本次不改工具；新文件实际缩略图效果需正式导入后确认。dry-run 跳过照片网络下载／许可核验，不能将其当作新照片已导入的证据；本次另行核对 Commons 文件页。

## 本次书目内容数

书目及版权标记保持不变；新增来源与版权依据不涉及新作者。历史书目依据保存在 tools/us-revision/review2/base/REPORT.md 及既有 evidence.json。

| 书目 ID | 书名 | 内容数 |
|---|---|---:|
| `moby-dick` | 白鲸 | 2 |
| `walden` | 瓦尔登湖 | 1 |
| `specimen-days` | 典型的日子 | 4 |
| `little-women` | 小妇人 | 1 |
| `great-gatsby` | 了不起的盖茨比 | 2 |
| `gold-bug` | 金甲虫 | 2 |
| `marrow-of-tradition` | 传统的精髓 | 1 |
| `winesburg-ohio` | 小城畸人 | 1 |
| `new-hampshire` | 新罕布什尔 | 1 |
| `entailed-hat` | 世袭的帽子：帕蒂·坎农的时代 | 2 |
| `life-on-mississippi` | 密西西比河上的生活 | 9 |
| `uncle-toms-cabin` | 汤姆叔叔的小屋 | 1 |
| `sister-carrie` | 嘉莉妹妹 | 5 |
| `little-house-in-big-woods` | 大森林里的小木屋 | 1 |
| `to-kill-a-mockingbird` | 杀死一只知更鸟 | 1 |
| `color-purple` | 紫色 | 1 |
| `sound-and-fury` | 喧哗与骚动 | 3 |
| `their-eyes-were-watching-god` | 他们眼望上苍 | 2 |
| `lonesome-dove` | 孤鸽镇 | 2 |
| `roughing-it` | 苦行记 | 3 |
| `travels-in-alaska` | 阿拉斯加游记 | 2 |
| `virginian` | 弗吉尼亚人 | 1 |
| `my-antonia` | 我的安东妮亚 | 1 |
| `o-pioneers` | 啊，拓荒者！ | 0 |
| `main-travelled-roads` | 大路 | 1 |
| `grapes-of-wrath` | 愤怒的葡萄 | 3 |
| `on-the-road` | 在路上 | 2 |
| `travels-with-charley` | 与查理同行 | 2 |
| `angle-of-repose` | 安息角 | 2 |
| `scarlet-letter` | 红字 | 2 |
| `age-of-innocence` | 纯真年代 | 3 |
| `american-notes` | 美国札记 | 3 |
| `life-in-iron-mills` | 铁厂的生活 | 1 |
| `letters-emily-dickinson` | 艾米莉·狄金森书信 | 1 |
| `us-call-of-the-wild` | 野性的呼唤 | 2 |
| `us-sea-wolf` | 海狼 | 1 |
| `us-steep-trails` | 险峻的山径 | 1 |
| `us-rolling-stones` | 滚石集 | 4 |
| `us-death-comes-for-the-archbishop` | 死神来迎接大主教 | 1 |
| `us-little-house-on-the-prairie` | 草原上的小木屋 | 1 |
| `usgone-with-wind` | 飘 | 4 |
| `usmagnificent-ambersons` | 伟大的安伯森家族 | 1 |
| `in-our-time` | 在我们的时代 | 2 |
| `ustom-sawyer` | 汤姆·索亚历险记 | 2 |
| `ushuckleberry-finn` | 哈克贝利·费恩历险记 | 2 |

## 各州地点（供导入器核对预期归属）

| 州 | 地点数 | 地点 ID |
|---|---:|---|
| Alabama | 1 | `monroeville` |
| Alaska | 1 | `wrangell` |
| Arizona | 1 | `flagstaff` |
| Arkansas | 1 | `fort-smith` |
| California | 4 | `weedpatch-camp`, `san-francisco`, `us-santa-clara-valley`, `us-wolf-house` |
| Colorado | 2 | `denver`, `leadville` |
| Connecticut | 3 | `hartford-stowe-house`, `us-hartford-dickens`, `us-new-haven-dickens` |
| Delaware | 1 | `georgetown-entailed-hat` |
| District of Columbia | 1 | `washington-whitman` |
| Florida | 2 | `eatonville`, `jacksonville` |
| Georgia | 2 | `eatonton`, `usatlanta` |
| Hawaii | 1 | `honolulu` |
| Idaho | 1 | `kuna` |
| Illinois | 1 | `chicago` |
| Indiana | 1 | `indianapolis` |
| Iowa | 1 | `dubuque` |
| Kansas | 1 | `us-independence-ingalls-site` |
| Kentucky | 1 | `louisville` |
| Louisiana | 3 | `new-orleans`, `usnew-orleans-french-quarter`, `usnew-orleans-west-end` |
| Maine | 1 | `brunswick-stowe-house` |
| Maryland | 2 | `princess-anne-entailed-hat`, `us-baltimore-poe-house` |
| Massachusetts | 8 | `new-bedford`, `nantucket-island`, `walden-pond`, `concord-orchard-house`, `us-boston-scarlet-letter`, `us-salem-custom-house`, `us-amherst-dickinson-museum`, `us-lenox-the-mount` |
| Michigan | 2 | `seney`, `fox-river` |
| Minnesota | 1 | `saint-paul` |
| Mississippi | 1 | `oxford-mississippi` |
| Missouri | 4 | `hannibal`, `usmark-twain-cave`, `usst-louis`, `usmark-twain-boyhood-home` |
| Montana | 1 | `billings` |
| Nebraska | 4 | `lincoln-nebraska`, `omaha`, `us-red-cloud`, `us-cather-childhood-home` |
| Nevada | 1 | `virginia-city` |
| New Hampshire | 1 | `franconia-frost` |
| New Jersey | 1 | `camden-whitman` |
| New Mexico | 1 | `us-santa-fe-cathedral` |
| New York | 4 | `great-neck-west-egg`, `manhattan-plaza-hotel`, `us-ny-academy-of-music`, `us-ny-lower-fifth-avenue` |
| North Carolina | 1 | `wilmington-wellington` |
| North Dakota | 1 | `fargo` |
| Ohio | 1 | `clyde-winesburg` |
| Oklahoma | 1 | `sallisaw` |
| Oregon | 1 | `mount-hood` |
| Pennsylvania | 2 | `pittsburgh-whitman`, `us-philadelphia-poe-house` |
| Rhode Island | 1 | `providence-athenaeum-poe` |
| South Carolina | 2 | `sullivans-island`, `charleston-gold-bug` |
| South Dakota | 1 | `ordway` |
| Tennessee | 1 | `memphis` |
| Texas | 3 | `san-antonio`, `us-austin-land-office`, `us-o-henry-museum` |
| Utah | 1 | `salt-lake-city` |
| Vermont | 1 | `shaftsbury-frost-stone-house` |
| Virginia | 1 | `falmouth-whitman` |
| Washington | 2 | `seattle`, `tacoma` |
| West Virginia | 1 | `us-wheeling-iron-mills` |
| Wisconsin | 1 | `pepin` |
| Wyoming | 1 | `medicine-bow` |

## 复现

本次工具仅在 tools/us-revision/review2/：base/ 保存修改前累计包，build.py 执行定点修改，evidence.json 记录截取与照片事实，verify.py 做范围及文件保护检查，report.py 生成本报告。旧批次 merge.py/verify.py 的 5 条州目标不适用于本次定点删减，不应重跑覆盖本包。
