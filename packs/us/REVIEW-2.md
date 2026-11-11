# 美国包 · 第一批修订的导入反馈（REVIEW-2）

2026-11-11。针对 `REVISION.md`（第一批修订＋知名作品补充）。

## 结论

可以导入。官方导入器 0 错误；66 条引文全部逐字对上古登堡原文，没有一条靠宽松比对；3 条地理提示与 REPORT.md 一致。REVIEW-1 的各项都有回应，知名作者补得到位，场景说明明显具体了。下面几处请在下一批里一并处理，不影响这次导入。

## 摘句

1. **地方没有分量（规则：摘句须是“地方有分量”的段落）**
   - `usan-ct3`、`usan-ct4`：哈特福德精神病院里两位病人的轶事，段落里没有地方，高亮是 old lady、window、music。建议删掉，康涅狄格已有 `usan-ct1`、`usan-ct2`、`usan-ct5`。
   - `us-rs-2`：古德尔走进酒馆，段落里没有圣安东尼奥，高亮是人名 Goodall。建议换成《圣安东尼奥之雾》里写城市或河的一段，或删掉（`us-rs-1` 已覆盖这个地方）。
   - 仍是一句带过的：`usmyan-1`（stayed in Lincoln）、`usopion-1`（He settled in Omaha）、`ussd-2`（Left camp at Falmouth）、`uslom-6`（沿途城镇名单里的 Dubuque）。这四条上次已在修订范围内，这次只改了中文。内布拉斯加已有 `us-myan-2`（黑鹰镇夜里下火车），`usmyan-1`、`usopion-1` 可以删；Falmouth、Dubuque 如果找不到更好的段落可以保留，但请标在报告里。
2. **高亮应是地方**：`us-rs-4`（Bexar Scrip No. 2692，换成 Land Office 或删去高亮里的凭证号）、`uslim-1`（smoke、town 可以，因为城市没有点名；保留）、`usts-1`（cave，可以）、`ushf-1`（village，可以）。
3. **格式**：`uslom-8` 的 `highlight_en` 里有 Windows 换行（`New\r\nOrleans`）。导入器会合并空白，网站上没问题，但请在包里写成 `New Orleans`，不要带换行。

## 场景说明

4. `ussaf-s5`：“杰斐逊纪念碑”在中文里容易读成华盛顿的杰斐逊纪念堂。原著里是杰斐逊镇广场上的南军士兵纪念像，请改成“杰斐逊广场上的南军纪念像”。
5. **《喧哗与骚动》占比过大**：密西西比的 5 条全是这本书、全在 `oxford-mississippi` 一个点上（和上次《世袭的帽子》的情况一样）。建议留 2–3 条，其余换成别的作家或别的地方，例如理查德·赖特《黑孩子》（纳奇兹、杰克逊，只写场景）。
6. `usnh-s1`（弗兰科尼亚电影院里观众看到选票数发笑）：请在 `fact_source` 里给出能核对这一细节的出处，审核时我们找不到。

## id

7. 新 id 的前缀写法不一：`us-cw-1` / `uslom-8`，`us-call-of-the-wild` / `usgone-with-wind`，`us-red-cloud` / `usatlanta`。这次不用改（改名会让 ID-MAP 更长）。之后新增的一律用 `us-` 加连字符。

## 照片

8. 50 张全部下载成功，许可都在允许范围内。两张只有 500 px 宽（`us-philadelphia-poe-house`、`fort-smith`），地点卡片按 800 px 显示会有点糊，下一批如果有更大的同许可图片请换掉。
