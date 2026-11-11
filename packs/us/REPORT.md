# 美国内容包 · 第一批修订与知名作品补充

交付日期：2026-11-11。依据内容规范 v1.2、us-brief.md 与 REVIEW-1.md；范围为用户确认的“先修订并补知名作品”，不是累计 100 本的完整第二批。

## 本次交付

45 本书、84 个地点、96 条内容（66 条原文摘句＋30 条原创场景说明）、50 张照片清单。所有内容为 draft，等待导入和人工审核。覆盖 50 州与华盛顿特区。

这是可整体导入的累计包，不是只含新增记录的差量包。没有执行正式导入，没有修改 data/ 或下载图片。旧版快照保存在 tools/us-revision/base/；迁移与移除记录见 ID-MAP.json，审核反馈逐项回应见 REVISION.md。

## 验证结果

- `python3 tools/us-revision/verify.py`：0 错误；66 条引文均为真实下载的 Gutenberg 文件内连续、逐字匹配的片段，保留原文换行及标点；双语高亮、引用关系、版权分流、各书 1–10 条、行 ID 前缀、51 区覆盖与照片比例均通过
- `python3 -I tools/import_pack.py packs/us --dry-run`：0 错误，3 条地理提示；没有未核对或仅宽松匹配的引文。完整输出见 IMPORT.md
- 地理提示：Charleston 位于简化海岸线外约 1 km，导入器归入 SC；Pepin 被简化河界误分到 MN，按本报告归入相距 2.2 km 的 WI；St. Louis 被简化河界分到 IL，按本报告归入相距 1.4 km 的 MO。独立 Census 2024 年 1:500,000 州界检查中，84 个点均落在正确州内；没有为了通过检查移动坐标
- 官方 dry-run 跳过照片下载与许可检查；照片另按 Commons 文件页核对许可和尺寸。13/13 朝圣地均有照片，原著地／原型地 37/71 有照片，超过一半。文件名及双语 alt 见 photos.json；没有影视取景地
- 新增 45 张照片中 44 张宽度至少 1280 px；Eatonville 镇政厅为 1233×669，是已说明的分辨率例外。既有 5 张沿用上次导入许可核验结果。现代实景图仅展示地点，不声称重现历史事件

## 主要州内容数

按每州关联的不同 line ID 计数，同一行不会因关联多个同州地点而重复计算。

| 州 | 内容数 |
|---|---:|
| NY | 5 |
| MA | 7 |
| CA | 5 |
| IL | 5 |
| GA | 5 |
| MS | 5 |
| LA | 6 |
| TX | 5 |
| CT | 5 |
| MO | 5 |

## 引用、版权与选题边界

全部新增引文从实际联网下载的古登堡全文用脚本截取，不由记忆生成；英文为原作，中文为本次自译，仍需人工审译。来源 URL、缓存 SHA-256、片段偏移与锚点保存在 tools/us-revision 各片区 evidence.json，汇总精确比对见 validation.json。

沿用英国作者去世满 70 年的口径；不以美国出版年份替代作者寿命。海明威、福克纳、斯坦贝克、赫斯顿、怀尔德等仍只写原创场景。新增公有领域作者去世年份：霍桑 1864、狄金森 1886、华顿 1937、狄更斯 1870、丽贝卡·哈丁·戴维斯 1910、杰克·伦敦 1916、欧·亨利 1910、凯瑟 1947、米切尔 1949、塔金顿 1946；吐温与缪尔沿用既有核验。各作者传记来源和判断详见片区 evidence.json；既有作者依据保留在 base/REPORT.md。

《飘》使用真实下载的 Gutenberg Australia 全文作为四个场景的依据；当前导入器不能以 .org 数字编号核对这个来源，因此不伪造 Gutenberg 编号、不交引文，也不把公有领域错误标成非公版。狄金森采用 1924 年书信选集中的 1861 年花园来信，Wikisource 为事实来源，同样只交原创场景说明。两者 public_domain 均为 true。

知名作品优先项已补齐：霍桑／塞勒姆与波士顿、狄金森／阿默斯特、吐温两部小说／汉尼拔与圣路易斯、米切尔／亚特兰大、坡／巴尔的摩与费城、伦敦／湾区与狼屋、凯瑟／红云镇、欧·亨利／奥斯汀、华顿／纽约与蒙特。狼屋、蒙特等朝圣地明确区分作家生平与小说场景。

依据 canon-us.json 的优先作者与书单选题；狄更斯是英国已有作者，用其亲历的康涅狄格描写补足原文；戴维斯《铁厂的生活》是明确的名单外窄幅补充，用持续的工业烟尘描写替换西弗吉尼亚过境句。既有名单外作者保留理由见首批报告。没有扩大到 100 本目标，也不宣称所有州都已有公版摘句。

统一采用 Mark Twain、O. Henry 等通行笔名，跨英国作者拼法由官方导入器复核。In Our Time 替换 1972 年身后汇编，仍只收《大双心河》场景。阿拉斯加仍是 Wrangell，没有误纳加拿大育空。城市、山地和虚构原型均说明代表范围，不伪造精确的故事发生地址。

## 书目与内容数

| 书目 | 作者 | 版权标记 | 内容数 |
|---|---|---|---:|
| 白鲸 / Moby-Dick (`moby-dick`) | Herman Melville | 公有领域 | 2 |
| 瓦尔登湖 / Walden (`walden`) | Henry David Thoreau | 公有领域 | 1 |
| 典型的日子 / Specimen Days (`specimen-days`) | Walt Whitman | 公有领域 | 4 |
| 小妇人 / Little Women (`little-women`) | Louisa May Alcott | 公有领域 | 1 |
| 了不起的盖茨比 / The Great Gatsby (`great-gatsby`) | F. Scott Fitzgerald | 公有领域 | 2 |
| 金甲虫 / The Gold-Bug (`gold-bug`) | Edgar Allan Poe | 公有领域 | 2 |
| 传统的精髓 / The Marrow of Tradition (`marrow-of-tradition`) | Charles W. Chesnutt | 公有领域 | 1 |
| 小城畸人 / Winesburg, Ohio (`winesburg-ohio`) | Sherwood Anderson | 公有领域 | 1 |
| 新罕布什尔 / New Hampshire (`new-hampshire`) | Robert Frost | 仅原创场景 | 1 |
| 世袭的帽子：帕蒂·坎农的时代 / The Entailed Hat; Or, Patty Cannon’s Times (`entailed-hat`) | George Alfred Townsend | 公有领域 | 2 |
| 密西西比河上的生活 / Life on the Mississippi (`life-on-mississippi`) | Mark Twain | 公有领域 | 9 |
| 汤姆叔叔的小屋 / Uncle Tom’s Cabin (`uncle-toms-cabin`) | Harriet Beecher Stowe | 公有领域 | 1 |
| 嘉莉妹妹 / Sister Carrie (`sister-carrie`) | Theodore Dreiser | 公有领域 | 5 |
| 大森林里的小木屋 / Little House in the Big Woods (`little-house-in-big-woods`) | Laura Ingalls Wilder | 仅原创场景 | 1 |
| 杀死一只知更鸟 / To Kill a Mockingbird (`to-kill-a-mockingbird`) | Harper Lee | 仅原创场景 | 1 |
| 紫色 / The Color Purple (`color-purple`) | Alice Walker | 仅原创场景 | 1 |
| 喧哗与骚动 / The Sound and the Fury (`sound-and-fury`) | William Faulkner | 仅原创场景 | 5 |
| 他们眼望上苍 / Their Eyes Were Watching God (`their-eyes-were-watching-god`) | Zora Neale Hurston | 仅原创场景 | 2 |
| 孤鸽镇 / Lonesome Dove (`lonesome-dove`) | Larry McMurtry | 仅原创场景 | 2 |
| 苦行记 / Roughing It (`roughing-it`) | Mark Twain | 公有领域 | 3 |
| 阿拉斯加游记 / Travels in Alaska (`travels-in-alaska`) | John Muir | 公有领域 | 2 |
| 弗吉尼亚人 / The Virginian: A Horseman of the Plains (`virginian`) | Owen Wister | 公有领域 | 1 |
| 我的安东妮亚 / My Ántonia (`my-antonia`) | Willa Cather | 公有领域 | 2 |
| 啊，拓荒者！ / O Pioneers! (`o-pioneers`) | Willa Cather | 公有领域 | 1 |
| 大路 / Main-Travelled Roads (`main-travelled-roads`) | Hamlin Garland | 公有领域 | 1 |
| 愤怒的葡萄 / The Grapes of Wrath (`grapes-of-wrath`) | John Steinbeck | 仅原创场景 | 3 |
| 在路上 / On the Road (`on-the-road`) | Jack Kerouac | 仅原创场景 | 2 |
| 与查理同行 / Travels with Charley: In Search of America (`travels-with-charley`) | John Steinbeck | 仅原创场景 | 2 |
| 安息角 / Angle of Repose (`angle-of-repose`) | Wallace Stegner | 仅原创场景 | 2 |
| 红字 / The Scarlet Letter (`scarlet-letter`) | Nathaniel Hawthorne | 公有领域 | 2 |
| 纯真年代 / The Age of Innocence (`age-of-innocence`) | Edith Wharton | 公有领域 | 3 |
| 美国札记 / American Notes for General Circulation (`american-notes`) | Charles Dickens | 公有领域 | 5 |
| 铁厂的生活 / Life in the Iron-Mills (`life-in-iron-mills`) | Rebecca Harding Davis | 公有领域 | 1 |
| 艾米莉·狄金森书信 / Letters of Emily Dickinson (`letters-emily-dickinson`) | Emily Dickinson | 公有领域 | 1 |
| 野性的呼唤 / The Call of the Wild (`us-call-of-the-wild`) | Jack London | 公有领域 | 2 |
| 海狼 / The Sea-Wolf (`us-sea-wolf`) | Jack London | 公有领域 | 1 |
| 险峻的山径 / Steep Trails (`us-steep-trails`) | John Muir | 公有领域 | 1 |
| 滚石集 / Rolling Stones (`us-rolling-stones`) | O. Henry | 公有领域 | 4 |
| 死神来迎接大主教 / Death Comes for the Archbishop (`us-death-comes-for-the-archbishop`) | Willa Cather | 公有领域 | 1 |
| 草原上的小木屋 / Little House on the Prairie (`us-little-house-on-the-prairie`) | Laura Ingalls Wilder | 仅原创场景 | 1 |
| 飘 / Gone with the Wind (`usgone-with-wind`) | Margaret Mitchell | 公有领域 | 4 |
| 伟大的安伯森家族 / The Magnificent Ambersons (`usmagnificent-ambersons`) | Booth Tarkington | 公有领域 | 1 |
| 在我们的时代 / In Our Time (`in-our-time`) | Ernest Hemingway | 仅原创场景 | 2 |
| 汤姆·索亚历险记 / The Adventures of Tom Sawyer (`ustom-sawyer`) | Mark Twain | 公有领域 | 2 |
| 哈克贝利·费恩历险记 / Adventures of Huckleberry Finn (`ushuckleberry-finn`) | Mark Twain | 公有领域 | 2 |

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

## 复现与交接

`tools/us-revision/merge.py` 从不可变首批快照与 east/west/south/midwest/root 补丁构建累计 JSON；`verify.py` 核对并生成 validation.json；`report.py` 生成本报告。各片区 build.py 与 evidence.json 保留原文截取和事实依据，照片证据分别存于 root/photo-evidence-final.json、south/photo-evidence.json 及 east/west/evidence.json。

请以本目录整体导入并人工审核；ID-MAP.json 提供行 ID 更名、书目更名及移除记录。所有草稿保持 draft；本次未运行正式导入后的站点验证，因为线上 data/us 并未被此交付修改。等待导入／审核反馈后再决定后续扩充。
