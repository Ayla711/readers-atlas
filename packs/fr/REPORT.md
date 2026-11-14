# 法国累计包 · 审核补充核验报告

日期：2026-11-14。依据内容规范 v1.3、欧洲任务说明及当前 REVIEW-1。

## 当前包与本轮范围

磁盘上的累计包已由另一轮工作扩充至 **31 本本地书目、62 个地点、62 条内容、50 张照片**；另有一条引用英国已有书目 `three-musketeers`。本轮保留这些成果，没有新增或删除任何书、地点或行 ID。旧报告的 23 / 51 / 50 / 40 数字已失效，不应再用于当前包。

本轮只实质修订已有的 `fr-lm-4`、`fr-lm-5`、`fr-lm-6` 及其三个地点的出处/坐标，并补齐审计与统计。全部 62 条为 draft。`ID-MAP.json` 的 removed 为空，latest_revision 单列本轮变更；added_* 重新按第一批基线计算，以免遗漏继承的新 ID。

## REVIEW-1 四处《悲惨世界》场景

| 要求 | 当前条目与处理 |
|---|---|
| 卢森堡公园 | 保留 `fr-lm-3`：春日长椅前马吕斯与珂赛特目光相遇 |
| 缪尚咖啡馆 | `fr-lm-4` 改为后厅的长走廊、窗户、暗梯和墙上旧地图，取第三部第四卷第 1 章 |
| 科林斯酒馆与街垒 | `fr-lm-5` 改为街口宽、尽头窄、酒馆形成瓶颈及可防守方向，取第四部第十二卷第 3 章；酒馆、街垒仍共用 `fr-corinthe-barricade` |
| 巴黎下水道 | `fr-lm-6` 改为冉阿让适应黑暗、看见湿墙、重新扛起马吕斯出发，取第五部第三卷第 1 章 |

所有三段法文、Hapgood 英译均从下载文本脚本截取，中文直接从法文译出。原文编号分别为 **17494、17518、17519**；17489 只有第一部，不能用来标这三处。英译沿用 #135、Isabel F. Hapgood（1887，1928年去世）。

保留 `fr-cafe-musain` 当前的老圣米歇尔广场定位：小说说“先贤祠附近”，对应今日埃德蒙-罗斯丹广场，而不是塞纳河边后来建成的同名喷泉广场。[广场沿革](https://fr.wikipedia.org/wiki/Place_Edmond-Rostand) 已补入 fact_source。

科林斯坐标细化为 **48.8625, 2.3480**。[巴黎市历史委员会报告](https://cdn.paris.fr/paris/2019/07/24/93bb6132691fdd80e007396945d2a1e0.pdf) 印刷页33–35确认朗布托街102号／蒙代图尔街2号，坐标取[法国国家地址库该门牌](https://api-adresse.data.gouv.fr/search/?q=102%20rue%20Rambuteau%2075001%20Paris&limit=1)。原街道已消失的说明保留。下水道地点仍用现有博物馆点，补入[博物馆官方来源](https://musee-egouts.paris.fr/en/)与第五部原文。

蒙费梅属于可选项，本轮未增加。亨利·詹姆斯仍为7条。

## 核验结果与限制

- 官方 `python3 -I tools/import_pack.py packs/fr --dry-run`：**0 错误、5 条地图提示**。
- 独立逐字检查 **97 段**原文／旧英译，均与缓存原文的 SHA-256 及字符偏移吻合；只规范化空白。官方宽松匹配项为0。
- 56条摘句、6条场景说明；42条含法文原文；自译英文仍只有已获授权的 `fr-wm-1`，官方将其列为唯一人工英文核对项。
- 50张照片的许可与尺寸均有 PHOTO-AUDIT 记录。本轮补核验此前缺记录的10张，均为 CC BY 或 CC BY-SA，原图宽度至少1600像素，缓存缩略图均达960像素。照片文件名未改，未向 images/ 写文件。
- 巴黎现有 **15/62条（24.2%）**，低于四分之一上限。13个本土大区均有地点；原著/原型地照片覆盖及朝圣照片按当前清单统计。
- 本轮开始时记录的 **853个 data/、images/ 和其他 tools/ 文件哈希全部保持不变**。没有正式导入。

**仍须审核的继承项：`fr-hn-1`《空心岩柱》仅有 #4017 英译，没有法文 text_orig。** 本轮查古登堡目录只找到英文文本及英文音频，未取得符合任务要求的古登堡法文。该条能通过导入器，但不满足欧洲任务说明的双源要求；保留另一轮已有内容，不擅自删除，也不把它称为完全合规。中文是否从法文译出亦无法从现有证据确认。不能因为 dry-run 为0错误，就忽略此项。

本轮并未重新做另一轮新增的六条版权场景的情节审核；它们原样保留。原 SOURCE-AUDIT 的逐本版权表覆盖原23本；新加的8本书需结合其书目来源复审，不能将原表误读成覆盖全部31本。两部新增公版书目录署名为 Gaston Leroux（1927年去世）、Maurice Leblanc（1941），英译均为 Alexander Teixeira de Mattos（1921）；其余新增书保持非公版场景或朝圣关联，没有新增引文。

五条地图提示分别为阿雅克肖0.4公里、勒阿弗尔岬1.1公里、阿维尼翁跨简化边界0.2公里（保留 FR-PAC）、伊夫堡离简化大陆海岸2.8公里、埃特雷塔岩柱0.8公里。详情见 IMPORT.md。

## 当前书目与内容数

| ID | 书名 | 作者 | 内容数 |
|---|---|---|---:|
| `fr-les-miserables` | 悲惨世界 | Victor Hugo | 6 |
| `fr-notre-dame-de-paris` | 巴黎圣母院 | Victor Hugo | 2 |
| `fr-madame-bovary` | 包法利夫人 | Gustave Flaubert | 3 |
| `fr-eugenie-grandet` | 欧也妮·葛朗台 | Honoré de Balzac | 2 |
| `fr-lost-illusions` | 幻灭 | Honoré de Balzac | 2 |
| `fr-swanns-way` | 在斯万家那边 | Marcel Proust | 2 |
| `fr-colomba` | 科隆巴 | Prosper Mérimée | 2 |
| `fr-germinal` | 萌芽 | Émile Zola | 2 |
| `fr-the-devils-pool` | 魔沼 | George Sand | 2 |
| `fr-red-and-black` | 红与黑 | Stendhal | 2 |
| `fr-pierre-and-jean` | 皮埃尔与让 | Guy de Maupassant | 3 |
| `fr-memoirs-beyond-grave` | 墓畔回忆录 | François-René de Chateaubriand | 3 |
| `fr-little-tour-france` | 法国小游记 | Henry James | 7 |
| `fr-travels-donkey` | 骑驴漫游记 | Robert Louis Stevenson | 3 |
| `fr-alsace-rust-gold` | 阿尔萨斯：锈色与金色 | Edith O’Shaughnessy | 3 |
| `fr-father-goriot` | 高老头 | Honoré de Balzac | 2 |
| `fr-ladies-paradise` | 妇女乐园 | Émile Zola | 1 |
| `fr-flowers-of-evil` | 恶之花 | Charles Baudelaire | 1 |
| `fr-count-monte-cristo` | 基督山伯爵 | Alexandre Dumas | 2 |
| `fr-letters-my-windmill` | 磨坊书简 | Alphonse Daudet | 1 |
| `fr-monday-tales` | 星期一故事 | Alphonse Daudet | 1 |
| `fr-within-budding-grove` | 在少女们身旁 | Marcel Proust | 1 |
| `fr-robur-conqueror` | 征服者罗比尔 | Jules Verne | 0 |
| `fr-phantom-of-the-opera` | 歌剧魅影 | Gaston Leroux | 1 |
| `fr-hollow-needle` | 空心岩柱 | Maurice Leblanc | 1 |
| `fr-little-prince` | 小王子 | Antoine de Saint-Exupéry | 0 |
| `fr-da-vinci-code` | 达·芬奇密码 | Dan Brown | 2 |
| `fr-perfume` | 香水 | Patrick Süskind | 1 |
| `fr-moveable-feast` | 流动的盛宴 | Ernest Hemingway | 1 |
| `fr-all-the-light` | 所有我们看不见的光 | Anthony Doerr | 1 |
| `fr-year-in-provence` | 普罗旺斯的一年 | Peter Mayle | 1 |
| `three-musketeers`（英国已有） | 三个火枪手 | Alexandre Dumas | 1 |

《征服者罗比尔》《小王子》等零摘句书目作为已有朝圣点关联保留；本轮没有增加空书目。

## 大区覆盖

| 大区 | 地点 | 内容 | 照片 |
|---|---:|---:|---:|
| FR-ARA | 3 | 1 | 2 |
| FR-BFC | 2 | 3 | 2 |
| FR-BRE | 3 | 4 | 1 |
| FR-CVL | 7 | 5 | 7 |
| FR-COR | 1 | 2 | 1 |
| FR-GES | 4 | 4 | 1 |
| FR-HDF | 3 | 3 | 1 |
| FR-IDF | 15 | 15 | 15 |
| FR-NOR | 9 | 8 | 7 |
| FR-NAQ | 2 | 3 | 1 |
| FR-OCC | 4 | 4 | 3 |
| FR-PDL | 3 | 4 | 3 |
| FR-PAC | 6 | 6 | 6 |

## 复核文件

`IMPORT.md` 为官方预检；`SOURCE-AUDIT.json` 保存逐段证据；`PHOTO-AUDIT.json` 保存50张照片许可与尺寸；`CHECKS.json` 为最新统计与未解决项。工作脚本和本轮开始时的完整包快照位于 `tools/eu-revision/fr/batch3/`。最终仍交付累计 `packs/fr/`，不交局部替换包。
