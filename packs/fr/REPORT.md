# 法国内容包 · 第二批累计交付报告

日期：2026-11-13。依据 `docs/content-pack-spec.md` v1.3、`packs/eu-brief.md` 和 `packs/fr/REVIEW-1.md`。只做法国。

## 规模与本批变化

累计 **23 本书、51 个地点、50 条摘句、40 张照片**。较首批新增 8 本书、12 个地点、10 条摘句、16 张照片。所有 50 条内容均为 `draft`。首批 15 本书和 40 条摘句原样保留，所有旧 ID 保留，新增 ID 均为 `fr-` 加连字符。`ID-MAP.json` 的 `removed` 为空。

巴黎由 2 条增加到 **7 条，占 14%**，低于四分之一上限。仍覆盖全部 13 个本土大区。亨利·詹姆斯《法国小游记》仍为 **7 条**，没有新增或改动。

## 审核意见逐项落实

| REVIEW-1 要求 | 本批结果 |
|---|---|
| 巴黎 6–8 条 | 7 条：原有两条雨果，加《高老头》两条、《妇女乐园》一条、《恶之花》一条、《悲惨世界》一条 |
| 伏盖公寓 | `fr-fg-1` 写公寓所在街区；定位真实的图尔讷福街（原新圣热纳维埃芙街），不指认某栋现存建筑就是虚构公寓 |
| 拉雪兹神父公墓 | `fr-fg-2` 写拉斯蒂涅葬礼后俯瞰巴黎、向城市挑战的结尾 |
| 左拉 | `fr-lp-1` 写《妇女乐园》街角橱窗开门前的布置，使用1895年 Vizetelly 版 |
| 波德莱尔 | `fr-fe-1` 采用《恶之花》〈天鹅〉开篇三节，写新卡鲁塞尔广场与消失的旧巴黎；原文和英译保留诗行 |
| 雨果故居内容关联 | 明确关联《悲惨世界》在故居动笔的写作史；新增 `fr-lm-3` 的卢森堡公园相遇。故居仍是朝圣地，公园是小说地点，未把公园段落误标到故居 |
| 《基督山伯爵》 | `fr-mc-1` 马赛老港的迎船人群，`fr-mc-2` 唐泰斯第一次望见伊夫堡；作者写法 `Alexandre Dumas` / `大仲马` |
| 《磨坊书简》 | `fr-wm-1` 叙述者门前的松林、阿尔皮耶山、短笛与骡铃；方特维耶都德磨坊标为朝圣地，明确作者并未在该建筑居住 |
| 《最后一课》 | 归在《星期一故事》书目下；`fr-mt-1` 选写字课上“法国，阿尔萨斯”字帖如旗帜的具体场景。故事未指定村名，标阿尔萨斯整体，不虚构学校坐标 |
| 凡尔纳 | 新增亚眠故居，关联《征服者罗比尔》，见下文跨国引用限制 |
| 莫泊桑的埃特雷塔 | 新增吉耶特别墅，关联已有《皮埃尔与让》；该书卷首文章署“吉耶特别墅，埃特雷塔，1887年9月” |
| 普鲁斯特的卡堡 | 新增大饭店原型点及《在少女们身旁》书目；`fr-bg-1` 写餐厅如水族箱、外面的人隔着玻璃观看 |
| 补照片 | 12 个新增地点全部配图，另补勒阿弗尔、南特、波尔多、第戎公爵宫 |

保留奥肖内西现有三条游记，没有删除已经通过审核的内容；阿尔萨斯本批由《最后一课》增加第二位作家，而非继续增加冷门游记。

## 原文、英译与版权

共 37 条法语原著摘句，其中 **36 条配古登堡旧英译、1 条经用户授权自译英文**；另外 13 条为首批保留的英语原创游记。古登堡法文原作与旧英译均由脚本下载并截取，中文直接从法文翻译。`SOURCE-AUDIT.json` 保存 86 段引用的原始文件 SHA-256 和解码字符偏移；诗行只去缩进，散文只合并硬换行，未改引用词句。

**自译英文仅 `fr-wm-1`，占全部内容 2%。** 古登堡 #30442 明确标注 Harmelin / Adams 的2009年版权译本，未采用。用户在本轮明确允许少量自译英文，因此从 #11770 法文自行译出英文和中文。导入器把这一条英文列为人工核对项，这是预期行为，不是漏配来源。

本批新译者：Ellen Marriage（1946年去世）、Ernest Alfred Vizetelly（1922）、F. P. Sturm（1942）、J. Berg Esenwein（1946）、C. K. Scott Moncrieff（1930），均满足去世满70年的要求。译者信息取古登堡目录及所用版本的署名、目录和扉页。#68291 明写〈The Last Class〉由本书编者译，编者是 Esenwein；只截取其连续正文，不带教学边注或段落编号。

《基督山伯爵》#1184 **未署译者姓名**。按19世纪匿名英译的出版期限处理，不冒填 William Robson 或任何去世年份；译本栏明确标 Anonymous，未声称与1846年首译的每个词都一致。匿名作品期限依据见[英国知识产权局的期限说明](https://www.gov.uk/government/publications/copyright-notice-duration-of-copyright-term/copyright-notice-duration-of-copyright-term)及[英国版权法第12条](https://www.legislation.gov.uk/ukpga/1988/48/section/12)。版本沿革见[小说的英译版本说明](https://en.wikipedia.org/wiki/The_Count_of_Monte_Cristo#Translations_and_notable_editions)。原作合作者 Auguste Maquet（1888年去世）列入别名，显示作者仍为大仲马。

《高老头》Marriage 译本年代1896见[电子版的版本说明](https://next.manifoldapp.org/read/father-goriot/section/1a13798d-deb3-4fe3-8c7f-9ecec9d1ee3f)。波德莱尔所标1919、普鲁斯特1924、都德英译1918均指本次引用的版本；《恶之花》〈天鹅〉属于1861年扩充版内容，不误称1857年初版已含此诗。

## 累计书目

| ID | 书 / 作者 | 内容条数 | 原作 PG | 英译 / 引用版本 |
|---|---|---:|---:|---|
| `fr-les-miserables` | 《悲惨世界》 / Victor Hugo | 3 | 17489 | Isabel F. Hapgood (1887) |
| `fr-notre-dame-de-paris` | 《巴黎圣母院》 / Victor Hugo | 2 | 19657 | Isabel F. Hapgood (1888) |
| `fr-madame-bovary` | 《包法利夫人》 / Gustave Flaubert | 3 | 14155 | Eleanor Marx-Aveling (1886) |
| `fr-eugenie-grandet` | 《欧也妮·葛朗台》 / Honoré de Balzac | 2 | 11049 | Katharine Prescott Wormeley (1886) |
| `fr-lost-illusions` | 《幻灭》 / Honoré de Balzac | 2 | 54723 | Ellen Marriage (1897) |
| `fr-swanns-way` | 《在斯万家那边》 / Marcel Proust | 2 | 2650 | C. K. Scott Moncrieff (1922) |
| `fr-colomba` | 《科隆巴》 / Prosper Mérimée | 2 | 16239 | Lady Mary Loyd (1902) |
| `fr-germinal` | 《萌芽》 / Émile Zola | 2 | 5711 | Havelock Ellis (1894) |
| `fr-the-devils-pool` | 《魔沼》 / George Sand | 2 | 23582 | George B. Ives (1901) |
| `fr-red-and-black` | 《红与黑》 / Stendhal | 2 | 798 | Horace B. Samuel (1916) |
| `fr-pierre-and-jean` | 《皮埃尔与让》 / Guy de Maupassant | 3 | 11131 | Clara Bell (1890) |
| `fr-memoirs-beyond-grave` | 《墓畔回忆录》 / François-René de Chateaubriand | 3 | 18864 | Alexander Teixeira de Mattos (1902) |
| `fr-little-tour-france` | 《法国小游记》 / Henry James | 7 | 28004 | original |
| `fr-travels-donkey` | 《骑驴漫游记》 / Robert Louis Stevenson | 3 | 535 | original |
| `fr-alsace-rust-gold` | 《阿尔萨斯：锈色与金色》 / Edith O’Shaughnessy | 3 | 75745 | original |
| `fr-father-goriot` | 《高老头》 / Honoré de Balzac | 2 | 55860 | Ellen Marriage (1896) |
| `fr-ladies-paradise` | 《妇女乐园》 / Émile Zola | 1 | 16852 | Ernest Alfred Vizetelly (1895) |
| `fr-flowers-of-evil` | 《恶之花》 / Charles Baudelaire | 1 | 6099 | F. P. Sturm (1919) |
| `fr-count-monte-cristo` | 《基督山伯爵》 / Alexandre Dumas | 2 | 17989 | Anonymous nineteenth-century translation (Project Gutenberg #1184) |
| `fr-letters-my-windmill` | 《磨坊书简》 / Alphonse Daudet | 1 | 11770 | own |
| `fr-monday-tales` | 《星期一故事》 / Alphonse Daudet | 1 | 50154 | J. Berg Esenwein (1918) |
| `fr-within-budding-grove` | 《在少女们身旁》 / Marcel Proust | 1 | 2999 | C. K. Scott Moncrieff (1924) |
| `fr-robur-conqueror` | 《征服者罗比尔》 / Jules Verne | 0 | 5126 | 只作故居关联，未引文 |

《征服者罗比尔》只作凡尔纳故居关联，尚未收摘句。原因：英国已有 `around-the-world`，但现行导入器一方面禁止重复别国书 ID，另一方面要求 `book_ids` 必须存在于当前包，故不能直接跨国关联。未复制、改名或移动《八十天环游地球》，也未修改导入器；改收1886年、在凡尔纳居住亚眠故居期间出版的《征服者罗比尔》。这是本批唯一没有摘句的书，故居关联可正常导入。

## 大区覆盖

| 大区 | 地点 | 内容 | 有内容的书 | 照片 |
|---|---:|---:|---:|---:|
| FR-ARA · Auvergne-Rhône-Alpes | 2 | 1 | 1 | 2 |
| FR-BFC · Bourgogne-Franche-Comté | 2 | 3 | 2 | 2 |
| FR-BRE · Brittany | 3 | 3 | 1 | 1 |
| FR-CVL · Centre-Val de Loire | 6 | 4 | 2 | 6 |
| FR-COR · Corsica | 1 | 2 | 1 | 1 |
| FR-GES · Grand Est | 4 | 4 | 2 | 1 |
| FR-HDF · Hauts-de-France | 3 | 3 | 2 | 1 |
| FR-IDF · Île-de-France | 8 | 7 | 5 | 8 |
| FR-NOR · Normandy | 8 | 7 | 3 | 6 |
| FR-NAQ · Nouvelle-Aquitaine | 2 | 3 | 2 | 1 |
| FR-OCC · Occitanie | 4 | 4 | 2 | 3 |
| FR-PDL · Pays de la Loire | 3 | 4 | 2 | 3 |
| FR-PAC · Provence-Alpes-Côte d’Azur | 5 | 5 | 4 | 5 |

## 地点证据与照片

坐标来自缓存的公开页面，并保留 `coord_checked` URL；不为适应简化地图而移动坐标。文学定位、纪念地和原型区别写在地点说明中。

- 雨果故居与1845年《苦难》写作的关系：[巴黎雨果研究资料](https://victorhugoressources.paris.fr/sites/default/files/documents/2023-01/08-10-24Molinari.pdf)，[博物馆沿革](https://www.maisonsvictorhugo.paris.fr/paris/musee/histoire-du-musee)。
- 莫泊桑故居：[法国文化部建筑登记](https://pop.culture.gouv.fr/notice/merimee/PA76000101)，作品卷首署地：[古登堡 #11131](https://www.gutenberg.org/ebooks/11131)。
- 卡堡原型：[诺曼底旅游局](https://www.normandie-tourisme.fr/madeleine-proust-cabourg/)与[卡堡市历史保护研究](https://www.cabourg.fr/wp-content/uploads/2024/06/02.Document-de-synthese-SPR-Cabourg.pdf)。
- 都德磨坊不是作者住所：[建筑资料](https://fr.wikipedia.org/wiki/Moulin_d%27Alphonse_Daudet)。

40张照片中，朝圣地 **9/9** 配图，其余地点 **31/42（73.8%）** 配图。新增16张均核对 Commons 许可、作者、原图尺寸，并下载960 px宽预览逐张看图；只交付文件名，不把图片文件放进包。原图均至少1200 px宽，已有24张照片保持原样。许可记录和实际下载尺寸见 `PHOTO-AUDIT.json`。

吉耶特别墅目前采用1888年莫泊桑与友人在园中的公版历史照片，明确标注历史照片；它不是今日建筑外观图。都德磨坊、凡尔纳故居、米绍迪耶尔街和这张历史照片为竖图，保留全幅，没有为凑横图裁掉主体。阿尔萨斯配塞尔奈和平原的地域风景，不暗示已找到《最后一课》的具体村庄。

## 验证与限制

执行：

```sh
python3 -I tools/import_pack.py packs/fr --dry-run
python3 -I tools/eu-revision/fr/batch2/verify_pack.py
```

官方 dry-run：**0 错误，4 条地图提示**；86段来源引用无需宽松匹配，1条自译英文待人工核对。照片许可由本批独立审计核实；官方 dry-run 本身跳过照片下载，未用其结果冒称照片许可已由导入器验证。

地图提示为：阿雅克肖距简化岸线0.4公里；勒阿弗尔拉埃夫角1.1公里；阿维尼翁边界偏差0.2公里、沿用已认可的 `FR-PAC`；新增伊夫堡离简化大陆岸线2.8公里，实际在近海岛上，归 `FR-PAC`。前三条延续首批，第四条不是坐标估算错误。

独立检查包括：旧书目与摘句完整保留、ID唯一与占用表不冲突、三语高亮、法英原文文件哈希及偏移、作者与译者版权依据、照片许可和尺寸、巴黎比例、13大区覆盖、亨利·詹姆斯条数不增。未正式导入，未开始其他国家。

### 并发文案同步

本任务只写 `packs/fr/` 和 `tools/eu-revision/`。核验途中，`data/us/places.js`、`data/uk/places.js`、`data/fr/places.js` 在同一时刻被另一写入更新，导致原始文件哈希基线变化；未回滚这些文件。其余671个受保护文件与开工时一致，无新增受保护文件。工作目录的 `concurrent-changes.json` 保存三个文件的前后哈希与时间。

法国网站中34个已有地点的新版中英文说明已同步入累计包，避免之后整体导入恢复旧文案；这是保留工作区最新文案，并非重写旧摘句。同步 ID 列在 `ID-MAP.json` 的 `inherited_latest_note_ids`。雨果故居保留最新说明中《悲惨世界》在此动笔的关联，并补有本批核查的写作史出处。首批15本书、40条摘句、24张照片及所有旧 ID 均保持不变。
