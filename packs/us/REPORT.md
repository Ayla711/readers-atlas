# 美国内容包 · 第一批交付报告

日期：2026-11-09。依据 `content-pack-spec.md` v1.1 与 `us-brief.md`。

## 交付范围

- 30 本书，27 位作者，69 个地点，60 条内容：40 条公有领域摘句、20 条原创场景说明。
- 覆盖 51/51 个一级区：50 州和华盛顿特区。州归属不写入地点 JSON，留给导入器按坐标分配。
- 5 张照片清单；所有朝圣地均配 Commons 文件。未收影视取景地；其 20 处目标属于第三批。
- 五个 JSON 均为 UTF-8。全部内容为 `draft`。本次未导入网站，未修改现有 `data/`，未开始第二批。
- 英文摘句以脚本从实际下载的古登堡文本截取，保留原标点与 CRLF 换行，不重排文字。`text_zh` 为本次自译，等待人工审核；`translation: original` 表示英文为原作。

## 自查结果及导入边界

- `node tools/validate.js`：现有英国网站数据通过，0 errors。该工具固定读取英国 `data/*.js` 与英国边界，不能把此结果冒称为美国包通过导入。
- `python3 tools/validate_us_pack.py`：0 errors；检查批次规模、必填字段、全局 ID、引用、高亮、语言、版权分流、原文逐字匹配、照片完整性及州覆盖。机器结果位于 `tools/us-work/shared/validation.json`。
- 独立重新下载 18 份古登堡全文后，40 条摘句全部逐字匹配，未依赖生成脚本自己的判断。下载 URL 与 SHA-256 见 `tools/us-work/shared/fresh-source-check.json`。
- 同时对照 `packs/existing-ids.json` 与实时 `data/*.js` 快照查重。后者有 161 本书、259 个地点、212 条内容，较交付的英国快照新增条目也纳入冲突检查。美国 Oxford 使用 `oxford-mississippi`。
- 英国寿命加 70 年口径采用任务规定的 1955 年去世截止线。海明威、福克纳、斯坦贝克、赫斯顿、怀尔德、弗罗斯特等仍只写场景说明，即使美国古登堡有全文也不引用。规则参考 [英国政府版权期限说明](https://www.gov.uk/copyright/how-long-copyright-lasts)。
- 坐标从公开页面的十进制度数或度分秒换算后保留四位小数；整数末尾的零不影响 JSON 数值精度。城市、河流及山地的代表点用途逐条注明，不伪称精确场景地址。
- 州边界独立检查最终使用 [美国人口普查局 2024 年 1:500,000 州界](https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_state_500k.zip)。69 个地点全部落入其预期州／DC，没有手动落区例外。较粗的初检边界曾漏掉 Nantucket、Sullivan’s Island 和 Honolulu；精细官方边界已全部解决，未为了通过检查移动正确坐标。Honolulu 使用有公开出处的市政厅陆地点作为城市代表，不声称小说场景发生于该楼。
- 阿拉斯加使用 Wrangell 的实际美国地点；没有把加拿大育空或克朗代克写入美国。
- Commons 页面已核对允许许可，照片只交文件标题及双语说明。导入器仍需重新查许可、下载与生成署名。

## 书目、作者与版权依据

“一级／二级”指作者在外部名单中的等级；书不一定本身上榜。书单命中和其余书目的推迟原因见后文。

| 书名 / ID | 作者 | 名单 | 版权处理 | 内容数 |
|---|---|---|---|---|
| 白鲸 / `moby-dick` | Herman Melville | 一级作者 | 公有领域；[去世于 1891](https://en.wikipedia.org/wiki/Herman_Melville) | 2 |
| 瓦尔登湖 / `walden` | Henry David Thoreau | 一级作者 | 公有领域；[去世于 1862](https://en.wikipedia.org/wiki/Henry_David_Thoreau) | 1 |
| 草叶集外集·典型的日子 / `specimen-days` | Walt Whitman | 一级作者 | 公有领域；[去世于 1892](https://en.wikipedia.org/wiki/Walt_Whitman) | 5 |
| 小妇人 / `little-women` | Louisa May Alcott | 一级作者 | 公有领域；[去世于 1888](https://en.wikipedia.org/wiki/Louisa_May_Alcott) | 1 |
| 了不起的盖茨比 / `great-gatsby` | F. Scott Fitzgerald | 一级作者 | 公有领域；[去世于 1940](https://en.wikipedia.org/wiki/F._Scott_Fitzgerald) | 2 |
| 金甲虫 / `gold-bug` | Edgar Allan Poe | 一级作者 | 公有领域；[去世于 1849](https://en.wikipedia.org/wiki/Edgar_Allan_Poe) | 2 |
| 传统的精髓 / `marrow-of-tradition` | Charles W. Chesnutt | 名单外补充 | 公有领域；[去世于 1932](https://en.wikipedia.org/wiki/Charles_W._Chesnutt) | 1 |
| 小城畸人 / `winesburg-ohio` | Sherwood Anderson | 一级作者 | 公有领域；[去世于 1941](https://en.wikipedia.org/wiki/Sherwood_Anderson) | 1 |
| 新罕布什尔 / `new-hampshire` | Robert Frost | 一级作者 | 仅场景说明；[去世于 1963](https://en.wikipedia.org/wiki/Robert_Frost) | 1 |
| 世袭的帽子：帕蒂·坎农的时代 / `entailed-hat` | George Alfred Townsend | 名单外补充 | 公有领域；[去世于 1914](https://en.wikipedia.org/wiki/George_Alfred_Townsend) | 4 |
| 密西西比河上的生活 / `life-on-mississippi` | Mark Twain | 一级作者 | 公有领域；[去世于 1910](https://en.wikipedia.org/wiki/Mark_Twain) | 7 |
| 汤姆叔叔的小屋 / `uncle-toms-cabin` | Harriet Beecher Stowe | 一级作者 | 公有领域；[去世于 1896](https://en.wikipedia.org/wiki/Harriet_Beecher_Stowe) | 1 |
| 嘉莉妹妹 / `sister-carrie` | Theodore Dreiser | 一级作者 | 公有领域；[去世于 1945](https://en.wikipedia.org/wiki/Theodore_Dreiser) | 2 |
| 大森林里的小木屋 / `little-house-in-big-woods` | Laura Ingalls Wilder | 一级作者 | 仅场景说明；[去世于 1957](https://en.wikipedia.org/wiki/Laura_Ingalls_Wilder) | 1 |
| 杀死一只知更鸟 / `to-kill-a-mockingbird` | Harper Lee | 一级作者 | 仅场景说明；[去世于 2016](https://en.wikipedia.org/wiki/Harper_Lee) | 1 |
| 紫色 / `color-purple` | Alice Walker | 二级作者 | 仅场景说明；在世作者 | 1 |
| 喧哗与骚动 / `sound-and-fury` | William Faulkner | 一级作者 | 仅场景说明；[去世于 1962](https://en.wikipedia.org/wiki/William_Faulkner) | 1 |
| 他们眼望上苍 / `their-eyes-were-watching-god` | Zora Neale Hurston | 一级作者 | 仅场景说明；[去世于 1960](https://en.wikipedia.org/wiki/Zora_Neale_Hurston) | 2 |
| 尼克·亚当斯故事集 / `nick-adams-stories` | Ernest Hemingway | 一级作者 | 仅场景说明；[去世于 1961](https://en.wikipedia.org/wiki/Ernest_Hemingway) | 2 |
| 孤鸽镇 / `lonesome-dove` | Larry McMurtry | 二级作者 | 仅场景说明；[去世于 2021](https://en.wikipedia.org/wiki/Larry_McMurtry) | 2 |
| 苦行记 / `roughing-it` | Mark Twain | 一级作者 | 公有领域；[去世于 1910](https://marktwainmuseum.org/learn-with-us/twain-faqs/) | 4 |
| 阿拉斯加游记 / `travels-in-alaska` | John Muir | 名单外补充 | 公有领域；[去世于 1914](https://www.nps.gov/jomu/learn/news/100th-anniversary-of-john-muirs-death.htm) | 3 |
| 弗吉尼亚人 / `virginian` | Owen Wister | 名单外补充 | 公有领域；[去世于 1938](https://www.penguinrandomhouse.com/authors/2049062/owen-wister/) | 1 |
| 我的安东妮亚 / `my-antonia` | Willa Cather | 一级作者 | 公有领域；[去世于 1947](https://www.nps.gov/people/willa-cather.htm) | 1 |
| 啊，拓荒者！ / `o-pioneers` | Willa Cather | 一级作者 | 公有领域；[去世于 1947](https://www.nps.gov/people/willa-cather.htm) | 1 |
| 大路 / `main-travelled-roads` | Hamlin Garland | 名单外补充 | 公有领域；[去世于 1940](https://poets.org/poet/hamlin-garland) | 1 |
| 愤怒的葡萄 / `grapes-of-wrath` | John Steinbeck | 一级作者 | 仅场景说明；[去世于 1968](https://sjsu.edu/steinbeck/resources/biography/index.php) | 3 |
| 在路上 / `on-the-road` | Jack Kerouac | 一级作者 | 仅场景说明；[去世于 1969](https://en.wikipedia.org/wiki/Jack_Kerouac) | 2 |
| 与查理同行 / `travels-with-charley` | John Steinbeck | 一级作者 | 仅场景说明；[去世于 1968](https://sjsu.edu/steinbeck/resources/biography/index.php) | 2 |
| 安息角 / `angle-of-repose` | Wallace Stegner | 二级作者 | 仅场景说明；[去世于 1993](https://en.wikipedia.org/wiki/Wallace_Stegner) | 2 |

## 每州地点数量

| 一级区 | 数量 | 地点 ID |
|---|---:|---|
| Alabama | 1 | `monroeville` |
| Alaska | 1 | `wrangell` |
| Arizona | 1 | `flagstaff` |
| Arkansas | 2 | `helena`、`fort-smith` |
| California | 2 | `weedpatch-camp`、`san-francisco` |
| Colorado | 2 | `denver`、`leadville` |
| Connecticut | 1 | `hartford-stowe-house` |
| Delaware | 3 | `georgetown-entailed-hat`、`laurel-entailed-hat`、`dover-entailed-hat` |
| District of Columbia | 1 | `washington-whitman` |
| Florida | 2 | `eatonville`、`jacksonville` |
| Georgia | 1 | `eatonton` |
| Hawaii | 1 | `honolulu` |
| Idaho | 1 | `kuna` |
| Illinois | 2 | `cairo`、`chicago` |
| Indiana | 1 | `indianapolis` |
| Iowa | 3 | `dubuque`、`burlington`、`davenport` |
| Kansas | 1 | `marysville` |
| Kentucky | 1 | `louisville` |
| Louisiana | 1 | `new-orleans` |
| Maine | 1 | `brunswick-stowe-house` |
| Maryland | 1 | `princess-anne-entailed-hat` |
| Massachusetts | 4 | `new-bedford`、`nantucket-island`、`walden-pond`、`concord-orchard-house` |
| Michigan | 2 | `seney`、`fox-river` |
| Minnesota | 2 | `minneapolis`、`saint-paul` |
| Mississippi | 1 | `oxford-mississippi` |
| Missouri | 1 | `hannibal` |
| Montana | 1 | `billings` |
| Nebraska | 2 | `lincoln-nebraska`、`omaha` |
| Nevada | 1 | `virginia-city` |
| New Hampshire | 1 | `franconia-frost` |
| New Jersey | 1 | `camden-whitman` |
| New Mexico | 1 | `gallup` |
| New York | 2 | `great-neck-west-egg`、`manhattan-plaza-hotel` |
| North Carolina | 1 | `wilmington-wellington` |
| North Dakota | 1 | `fargo` |
| Ohio | 1 | `clyde-winesburg` |
| Oklahoma | 1 | `sallisaw` |
| Oregon | 1 | `mount-hood` |
| Pennsylvania | 1 | `pittsburgh-whitman` |
| Rhode Island | 1 | `providence-athenaeum-poe` |
| South Carolina | 2 | `sullivans-island`、`charleston-gold-bug` |
| South Dakota | 1 | `ordway` |
| Tennessee | 1 | `memphis` |
| Texas | 1 | `san-antonio` |
| Utah | 1 | `salt-lake-city` |
| Vermont | 1 | `shaftsbury-frost-stone-house` |
| Virginia | 1 | `falmouth-whitman` |
| Washington | 2 | `seattle`、`tacoma` |
| West Virginia | 1 | `weirton-panhandle` |
| Wisconsin | 1 | `pepin` |
| Wyoming | 1 | `medicine-bow` |

## 选题调整与名单外依据

- 第一批以全国覆盖为优先约束；以名单中的一级作者为主体，加入确有地方关联的旅行文学。多数故居与其余经典本批暂缓，不视为已完成或永久排除。
- John Muir《Travels in Alaska》补阿拉斯加和太平洋西北；作者有 [NPS John Muir National Historic Site](https://www.nps.gov/jomu/index.htm) 公共纪念地。
- Owen Wister《The Virginian》补怀俄明；[Medicine Bow Museum](https://travelwyoming.com/listing/medicine-bow-museum/735/) 的公开文学纪念资料支持选题。
- Hamlin Garland《Main-Travelled Roads》补南达科他；[美国诗人学会作者介绍](https://poets.org/poet/hamlin-garland) 记录其文学经历与普利策奖。地点摘自作者序言而非虚构短篇正文，已明确标注。
- George Alfred Townsend《The Entailed Hat》补特拉华；[特拉华州档案馆文学研究](https://archivesfiles.delaware.gov/ebooks/GATHs_Literary_Work_and_Folk.pdf) 第 37 页讨论此书的地方文学地位。
- Charles W. Chesnutt《The Marrow of Tradition》补北卡罗来纳；依据 [北卡州文化资源部门作家纪念牌资料](https://www.dncr.nc.gov/blog/2023/12/29/charles-w-chesnutt-1858-1932-i-32)，并核验虚构 Wellington 与 Wilmington 的关系。
- 《飘》《Look Homeward, Angel》本轮未找到满足指定 Gutenberg 下载流程的可用文本，暂缓；不以记忆引文代替。《大地》主要情节在中国，未用美国故居冒充小说发生地。
- 印第安纳 Indianapolis 的摘句是人物说明自己的来处，并非当地正在发生的场景；地点说明已明确。城市规模清单和作者序言属于真实地点提及，但文学展示优先级可在人工审核时降低。

## 外部名单完整去向

名单含 146 位作者、94 处故居、115 条书单来源记录；去重后为 108 部作品。同书被两份书单收录时，下表合并出处。

### 作者

| 作者 | 级别 | 本批处理／暂缓原因 |
|---|---|---|
| Alex Haley | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Carl Sandburg | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Carson McCullers | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| E. B. White | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| E. E. Cummings | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Edgar Allan Poe | 1 | 已收：金甲虫 |
| Edith Wharton | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Edna St. Vincent Millay | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Edward Gorey | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Ellen Glasgow | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Emily Dickinson | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Ernest Hemingway | 1 | 已收：尼克·亚当斯故事集 |
| Eudora Welty | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Eugene O'Neill | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| F. Scott Fitzgerald | 1 | 已收：了不起的盖茨比 |
| Flannery O'Connor | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Frederick Douglass | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Gertrude Stein | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| H. A. Rey | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| H. L. Mencken | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Harper Lee | 1 | 已收：杀死一只知更鸟 |
| Harriet Beecher Stowe | 1 | 已收：汤姆叔叔的小屋 |
| Henry David Thoreau | 1 | 已收：瓦尔登湖 |
| Henry James | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Henry Miller | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Henry Wadsworth Longfellow | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Herman Melville | 1 | 已收：白鲸 |
| Jack Kerouac | 1 | 已收：在路上 |
| Jack London | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| James Baldwin | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| James Dickey | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| James T. Farrell | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| James Thurber | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| James Weldon Johnson | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Joel Chandler Harris | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| John Dos Passos | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| John Kennedy Toole | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| John O'Hara | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| John Steinbeck | 1 | 已收：愤怒的葡萄、与查理同行 |
| John Updike | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Joseph Heller | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Kate Chopin | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Katherine Anne Porter | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Kurt Vonnegut | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Langston Hughes | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Laura Ingalls Wilder | 1 | 已收：大森林里的小木屋 |
| Louisa May Alcott | 1 | 已收：小妇人 |
| Margaret Mitchell | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Marjorie Kinnan Rawlings | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Mark Twain | 1 | 已收：密西西比河上的生活、苦行记 |
| Maya Angelou | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Nathaniel Hawthorne | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Noah Webster | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| O. Henry | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Paul Laurence Dunbar | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Pearl S. Buck | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Rachel Carson | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Ralph Ellison | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Ralph Waldo Emerson | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Richard Wright | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Robert Frost | 1 | 已收：新罕布什尔 |
| Robert Penn Warren | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Robinson Jeffers | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Rudyard Kipling | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Sarah Orne Jewett | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Saul Bellow | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Sherwood Anderson | 1 | 已收：小城畸人 |
| Sinclair Lewis | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Stephen Crane | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Stephen King | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Theodore Dreiser | 1 | 已收：嘉莉妹妹 |
| Theodore Roethke | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Thomas Wolfe | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Thornton Wilder | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Truman Capote | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Upton Sinclair | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Vachel Lindsay | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Virginia Lee Burton | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Vladimir Nabokov | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Walt Whitman | 1 | 已收：草叶集外集·典型的日子 |
| Washington Irving | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Willa Cather | 1 | 已收：我的安东妮亚、啊，拓荒者！ |
| William Carlos Williams | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| William Faulkner | 1 | 已收：喧哗与骚动 |
| Zane Grey | 1 | 暂缓：第一批 30 本及全国覆盖额度；后续须补作品与故居，尚未完成逐条来源核验。 |
| Zora Neale Hurston | 1 | 已收：他们眼望上苍 |
| Alice Sebold | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Alice Walker | 2 | 已收：紫色 |
| Amy Tan | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Andy Weir | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Armistead Maupin | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Arthur Golden | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Ayn Rand | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Betty Smith | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Booth Tarkington | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Colson Whitehead | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Dan Brown | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Dashiell Hammett | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Dave Hunt | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Dean Koontz | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| E. L. Doctorow | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Ernest Cline | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Erskine Caldwell | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Frank E. Peretti | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Frank Herbert | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Gary Paulsen | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| George R. R. Martin | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Gillian Flynn | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Isaac Asimov | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| J. D. Salinger | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| James Jones | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| James M. Cain | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Jason Reynolds | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Jean M. Auel | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| John Cheever | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| John Green | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| John Irving | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| John Knowles | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Junot Díaz | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Kathryn Stockett | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Larry McMurtry | 2 | 已收：孤鸽镇 |
| Lois Lowry | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Marilynne Robinson | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Mario Puzo | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Michael Crichton | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Nathanael West | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Nicholas Sparks | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Norman Mailer | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Paul Bowles | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Philip Roth | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Robert R. McCammon | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Rudolfo Anaya | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| S. E. Hinton | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Sister Souljah | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Stephenie Meyer | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Suzanne Collins | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Tim LaHaye | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Tom Clancy | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Toni Morrison | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| V. C. Andrews | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Walker Percy | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Wallace Stegner | 2 | 已收：安息角 |
| William Kennedy | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| William P. Young | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| William Styron | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |
| Wilson Rawls | 2 | 暂缓：二级候选，第一批优先一级作者与缺州覆盖；等待导入反馈后再选。 |

### 上榜书

| 作品 | 作者 | 出处 | 本批处理／暂缓原因 |
|---|---|---|---|
| The Great Gatsby | F. Scott Fitzgerald | ML #2, GAR | 本批已收。 |
| Lolita | Vladimir Nabokov | ML #4 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Sound and the Fury | William Faulkner | ML #6 | 本批已收。 |
| Catch-22 | Joseph Heller | ML #7, GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Grapes of Wrath | John Steinbeck | ML #10, GAR | 本批已收。 |
| An American Tragedy | Theodore Dreiser | ML #16 | 暂缓：本批已选该作者其他作品或只选部分上榜作品，优先满足 30 本与缺州覆盖。 |
| The Heart Is a Lonely Hunter | Carson McCullers | ML #17 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Slaughterhouse-Five | Kurt Vonnegut | ML #18 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Invisible Man | Ralph Ellison | ML #19, GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Native Son | Richard Wright | ML #20 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Henderson the Rain King | Saul Bellow | ML #21 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Appointment in Samarra | John O'Hara | ML #22 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| U.S.A. | John Dos Passos | ML #23 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Winesburg, Ohio | Sherwood Anderson | ML #24 | 本批已收。 |
| The Wings of the Dove | Henry James | ML #26 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Ambassadors | Henry James | ML #27 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Tender Is the Night | F. Scott Fitzgerald | ML #28 | 暂缓：本批已选该作者其他作品或只选部分上榜作品，优先满足 30 本与缺州覆盖。 |
| The Studs Lonigan Trilogy | James T. Farrell | ML #29 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Golden Bowl | Henry James | ML #32 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Sister Carrie | Theodore Dreiser | ML #33 | 本批已收。 |
| As I Lay Dying | William Faulkner | ML #35 | 暂缓：本批已选该作者其他作品或只选部分上榜作品，优先满足 30 本与缺州覆盖。 |
| All the King's Men | Robert Penn Warren | ML #36 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Bridge of San Luis Rey | Thornton Wilder | ML #37 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Go Tell It on the Mountain | James Baldwin | ML #39 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Deliverance | James Dickey | ML #42 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Sun Also Rises | Ernest Hemingway | ML #45, GAR | 暂缓：本批已选该作者其他作品或只选部分上榜作品，优先满足 30 本与缺州覆盖。 |
| Tropic of Cancer | Henry Miller | ML #50 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Naked and the Dead | Norman Mailer | ML #51 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Portnoy's Complaint | Philip Roth | ML #52 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Pale Fire | Vladimir Nabokov | ML #53 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Light in August | William Faulkner | ML #54 | 暂缓：本批已选该作者其他作品或只选部分上榜作品，优先满足 30 本与缺州覆盖。 |
| On the Road | Jack Kerouac | ML #55 | 本批已收。 |
| The Maltese Falcon | Dashiell Hammett | ML #56 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Age of Innocence | Edith Wharton | ML #58 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Moviegoer | Walker Percy | ML #60 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Death Comes for the Archbishop | Willa Cather | ML #61 | 暂缓：本批已选该作者其他作品或只选部分上榜作品，优先满足 30 本与缺州覆盖。 |
| From Here to Eternity | James Jones | ML #62 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Wapshot Chronicle | John Cheever | ML #63 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Catcher in the Rye | J. D. Salinger | ML #64, GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Main Street | Sinclair Lewis | ML #68 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The House of Mirth | Edith Wharton | ML #69 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Day of the Locust | Nathanael West | ML #73 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| A Farewell to Arms | Ernest Hemingway | ML #74 | 暂缓：本批已选该作者其他作品或只选部分上榜作品，优先满足 30 本与缺州覆盖。 |
| The Adventures of Augie March | Saul Bellow | ML #81 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Angle of Repose | Wallace Stegner | ML #82 | 本批已收。 |
| Ragtime | E. L. Doctorow | ML #86 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Call of the Wild | Jack London | ML #88, GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Tobacco Road | Erskine Caldwell | ML #91 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Ironweed | William Kennedy | ML #92 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Sophie's Choice | William Styron | ML #96 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Sheltering Sky | Paul Bowles | ML #97 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Postman Always Rings Twice | James M. Cain | ML #98 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Magnificent Ambersons | Booth Tarkington | ML #100 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| To Kill a Mockingbird | Harper Lee | GAR #1 | 本批已收。 |
| Gone with the Wind | Margaret Mitchell | GAR #6 | 暂缓：本轮未取得满足指定下载流程的古登堡原文；不是版权判定为否。 |
| Charlotte's Web | E. B. White | GAR #7 | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Little Women | Louisa May Alcott | GAR #8 | 本批已收。 |
| A Confederacy of Dunces | John Kennedy Toole | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| A Prayer for Owen Meany | John Irving | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| A Separate Peace | John Knowles | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| A Tree Grows in Brooklyn | Betty Smith | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Adventures of Tom Sawyer | Mark Twain | GAR | 暂缓：本批已选该作者其他作品或只选部分上榜作品，优先满足 30 本与缺州覆盖。 |
| Another Country | James Baldwin | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Atlas Shrugged | Ayn Rand | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Beloved | Toni Morrison | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Bless Me, Ultima | Rudolfo Anaya | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Brief Wondrous Life of Oscar Wao | Junot Díaz | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Color Purple | Alice Walker | GAR | 本批已收。 |
| Dune | Frank Herbert | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Flowers in the Attic | V. C. Andrews | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Foundation | Isaac Asimov | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| A Game of Thrones | George R. R. Martin | GAR | 英国包已有同书，按全局单书约定不重复新增；以后只扩地点引用。 |
| Ghost | Jason Reynolds | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Gilead | Marilynne Robinson | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Giver | Lois Lowry | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Godfather | Mario Puzo | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Gone Girl | Gillian Flynn | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Hatchet | Gary Paulsen | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Help | Kathryn Stockett | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Hunger Games | Suzanne Collins | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Hunt for Red October | Tom Clancy | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Intuitionist | Colson Whitehead | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Joy Luck Club | Amy Tan | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Jurassic Park | Michael Crichton | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Lonesome Dove | Larry McMurtry | GAR | 本批已收。 |
| Looking for Alaska | John Green | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Lovely Bones | Alice Sebold | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Martian | Andy Weir | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Memoirs of a Geisha | Arthur Golden | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Moby-Dick | Herman Melville | GAR | 本批已收。 |
| The Notebook | Nicholas Sparks | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Outsiders | S. E. Hinton | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Ready Player One | Ernest Cline | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Sirens of Titan | Kurt Vonnegut | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Stand | Stephen King | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Swan Song | Robert R. McCammon | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Tales of the City | Armistead Maupin | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Their Eyes Were Watching God | Zora Neale Hurston | GAR | 本批已收。 |
| Watchers | Dean Koontz | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Where the Red Fern Grows | Wilson Rawls | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Da Vinci Code | Dan Brown | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Clan of the Cave Bear | Jean M. Auel | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Coldest Winter Ever | Sister Souljah | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Left Behind | Tim LaHaye | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| This Present Darkness | Frank E. Peretti | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Twilight Saga | Stephenie Meyer | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| The Shack | William P. Young | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |
| Mind Invaders | Dave Hunt | GAR | 暂缓：本批容量及州覆盖取舍，尚未完成此书地点／原文或场景来源核验。 |

### 故居名单

同一城市的原著地点不等于已收该城的作家故居。例如 Hannibal 城市点不计作 Twain Boyhood Home；Oxford 城市原型不计作 Rowan Oak。

| 名单地点 | 州 | 本批处理／暂缓原因 |
|---|---|---|
| The Scott and Zelda Fitzgerald Museum, Montgomery | AL | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Faulk home site, Monroeville | AL | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Tor House, Carmel | CA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Wolf House and Beauty Ranch (Jack London State Historic Park), Glen Ellen | CA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Tao House, Danville | CA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Upton Sinclair House, Monrovia | CA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Steinbeck House, Salinas | CA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Monte Cristo Cottage, New London | CT | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Mark Twain House, Hartford | CT | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Harriet Beecher Stowe House, Hartford | CT | 已收：`hartford-stowe-house`（pilgrimage） |
| Noah Webster House, West Hartford | CT | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Ernest Hemingway Home, Key West | FL | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Zora Neale Hurston House, Fort Pierce | FL | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Jack Kerouac House, Orlando | FL | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Cross Creek, Cross Creek | FL | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Wren's Nest, Atlanta | GA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Carson McCullers Childhood Home, Columbus | GA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Margaret Mitchell House and Museum, Atlanta | GA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Flannery O'Connor Childhood Home, Savannah | GA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Andalusia, Milledgeville | GA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Ernest Hemingway Birthplace, Oak Park | IL | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Vachel Lindsay House, Springfield | IL | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Carl Sandburg State Historic Site, Galesburg | IL | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Toole-Hecker House, New Orleans | LA | 暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。 |
| Robert Penn Warren House (Twin Oaks), Prairieville | LA | 暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。 |
| Stephen and Tabitha King home, Bangor | ME | 暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。 |
| Sarah Orne Jewett House, South Berwick | ME | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Harriet Beecher Stowe House, Brunswick | ME | 已收：`brunswick-stowe-house`（pilgrimage） |
| Wadsworth-Longfellow House, Portland | ME | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| H. L. Mencken House, Baltimore | MD | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Rachel Carson House, Colesville | MD | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Edgar Allan Poe House and Museum, Baltimore | MD | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| David Bachrach House, Baltimore | MD | 暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。 |
| Virginia Lee Burton Writing Cottage, Gloucester | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| E. E. Cummings House, Cambridge | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Edward Gorey House, Yarmouth Port | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Emily Dickinson Museum, Amherst | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| The Wayside, Concord | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Orchard House, Concord | MA | 已收：`concord-orchard-house`（prototype） |
| Ralph Waldo Emerson House, Concord | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Longfellow House–Washington's Headquarters, Cambridge | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Arrowhead, Pittsfield | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Nathaniel Hawthorne Birthplace, Salem | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| The Wayside, Concord | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Thoreau–Alcott House, Concord | MA | 暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。 |
| The Mount, Lenox | MA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Windemere Cottage, Petoskey | MI | 暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。 |
| Roethke Houses, Saginaw | MI | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| F. Scott Fitzgerald House (Summit Terrace), Saint Paul | MN | 暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。 |
| Sinclair Lewis Boyhood Home, Sauk Centre | MN | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Rowan Oak, Oxford | MS | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Eudora Welty House, Jackson | MS | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Maya Angelou Birthplace, St. Louis | MO | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Kate Chopin House, St. Louis | MO | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Mark Twain Boyhood Home, Hannibal | MO | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Laura Ingalls Wilder House (Rocky Ridge Farm), Mansfield | MO | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Willa Cather Childhood Home, Red Cloud | NE | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Robert Frost Farm, Derry | NH | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| The Frost Place, Franconia | NH | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Curious George Cottage, Waterville Valley | NH | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Arbutus Cottage, Asbury Park | NJ | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Walt Whitman House, Camden | NJ | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| William Carlos Williams House, Rutherford | NJ | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| James Baldwin Residence, New York | NY | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Sunnyside, Tarrytown | NY | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Langston Hughes House, New York | NY | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| James Weldon Johnson Residence, New York | NY | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Herman Melville House, Lansingburgh | NY | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Carson McCullers House, South Nyack | NY | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Steepletop, Austerlitz | NY | 暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。 |
| Edgar Allan Poe Cottage, The Bronx, New York | NY | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Quarry Farm, Elmira | NY | 暂缓：私人／非普通开放场所，需进一步核验访问说明和自由许可实地照片；本批不引导造访。 |
| Walt Whitman Birthplace, West Hills | NY | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Carl Sandburg Home, Flat Rock | NC | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Thomas Wolfe House, Asheville | NC | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Paul Laurence Dunbar House, Dayton | OH | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Harriet Beecher Stowe House, Cincinnati | OH | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Thurber House, Columbus | OH | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Zane Grey Cabin, Rogue River | OR | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Rachel Carson Homestead, Springdale | PA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Pearl S. Buck House (Green Hills Farm), Perkasie | PA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| John Updike Childhood Home, Shillington | PA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Alex Haley House and Museum, Henning | TN | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Katherine Anne Porter House, Kyle | TX | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| O. Henry House, Austin | TX | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Frederick Douglass National Historic Site, Washington | DC | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Langston Hughes House (12th Street), Washington | DC | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Homer Noble Farm, Ripton | VT | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Robert Frost Stone House Museum, Shaftsbury | VT | 已收：`shaftsbury-frost-stone-house`（pilgrimage） |
| Naulakha, Dummerston | VT | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Willa Cather Birthplace, Gore | VA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Willow Shade, Winchester | VA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Ellen Glasgow House, Richmond | VA | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |
| Pearl S. Buck Birthplace, Hillsboro | WV | 暂缓：第一批优先全国真实地点覆盖；此故居的完整史实、坐标与照片核验未纳入本批。 |

## 复现与审核文件

1. 三组 `tools/us-work/{east,central,west}/build.py` 从已下载的文本及截取锚点生成分片；同目录 `evidence.json` 保存原始坐标、版权依据及原文证据，`notes.md` 记录内容判断。
2. `python3 tools/assemble_us_pack.py` 合并五个 JSON。
3. `python3 tools/validate_us_pack.py` 独立校验美国包，并输出逐州机器结果。
4. `python3 tools/report_us_pack.py` 重建本报告。
5. `node tools/validate.js` 检查现有网站数据；正式导入工具准备好后再执行导入和项目负责人的内容审核。

接下来等待第一批的导入与审核反馈，再决定第二批；本交付不宣称已完成名单的全面覆盖。
