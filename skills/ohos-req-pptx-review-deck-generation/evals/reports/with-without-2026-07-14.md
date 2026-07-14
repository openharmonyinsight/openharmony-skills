# with-skill / without-skill 对照评估报告

日期：2026-07-14
对象：`ohos-req-pptx-review-deck-generation` skill（修复 PR #279 评审意见后的版本）
用例来源：`evals/cases.yaml`（3 个 case，对应 `evals/prompts/*.md`）

## 方法

对每个 case，分别用两个独立 Agent 会话生成 PPTX：
- **with skill**：Agent 读取本 skill 的 `SKILL.md` 并按其指引调用 `deckbuilder.Deck`。
- **without skill**：Agent 只拿到与 case 相同的用户 prompt，不知道本 skill 存在，
  用其对 `python-pptx` 的通用知识从零手写。

两组产物均：
1. 跑 `evals/expected/*.md` 的 `must` / `must_not` 逐条核对。
2. 跑 shape 级 overflow 边界检查（`SKILL.md` Verification 一节的脚本）。
3. 额外跑一遍**基于文字测量的溢出检测**（按列宽 × 字号估算每个单元格实际
   需要的行数与高度，比对表格实际行高）——这是本轮修复新增的检查手段，
   用于验证「shape 没溢出 ≠ 文字没被截断」这一评审意见（见下方 case 3）。

## Case 1 — req-review-from-doc（固定 8 页模板）

| | with skill | without skill |
|---|---|---|
| 页数 | 8（与固定模板一致） | 11（自行发挥：封面/议程/概述/范围/AC/模块/拆解/技术方向/风险/讨论/结语） |
| 页序与固定结构 | 完全遵循（封面→价值→设计→背景→影响→交付→兼容→风险） | 不遵循（无模板可依据，自创大纲） |
| 第3页设计方案 | 真实框图（`diagram=` 控制面/数据面分层） | 手绘 pipeline 图（自行摸索坐标） |
| 缺失字段处理 | 全部标注「待评估 / TBD」，未编造（需求编号/SIG纪要/落地版本/设计者/领域PM等9项，逐条列出） | 无标注机制，部分字段被自然略去而非显式标记待评估 |
| 第6页合计行 | `1250` 行 / `2.5` 人月（4个子需求各自"XXX（估算）"，`_num()` 正确解析后求和） | 无固定11列结构 |
| overflow（shape级） | 0 | 0 |
| 结论 | must 项全部满足 | 因无模板依据，`must` 中"固定8页结构"等强约束项不满足——这正是 skill 存在的价值：无 skill 时模型会自创大纲、漏掉必需字段的显式留白 |

## Case 2 — architecture-diagram（框图而非要点列表）

| | with skill | without skill |
|---|---|---|
| 构建方式 | 一次调用 `architecture_slide(nodes, edges)`，库自动布局、画带方向箭头 + 边标签 | 手写 `add_connector` + 操作底层 XML（`headEnd`/`tailEnd`）实现箭头，手工摆放6处坐标 |
| 迭代过程 | 一次成型，0 警告 | 首次生成后跑重叠检测，发现 5 处标签与连线/说明面板重叠，手动调整坐标 3 轮才收敛 |
| overflow（shape级） | 0 | 0（修复重叠后） |
| 结论 | must 项全部满足，且过程无需手动调坐标 | 功能上也能画出框图，但过程验证了评审关注的"手搓 python-pptx 导致版式错乱"——without 路径确实经历了坐标反复调试 |

## Case 3 — wide-table（多列表格自适应、不截断）

| | with skill | without skill |
|---|---|---|
| 构建方式 | `table_slide(headers, rows, col_widths=...)`，行高按实际文字测量自适应（本轮修复新增） | 手动设置每行 `row.height`（0.5in~1.05in），按"估算"分配 |
| table_slide 内容溢出警告 | 0 | N/A（未使用该库） |
| **shape 级 overflow** | 0 | **1（表格实际高度 6.10in，起始 1.45in，底部 7.55in，超出 7.5in 画布 0.05in）** |
| **文字级溢出（本轮新增的测量检查）** | 0（每个单元格测量所需行高 ≤ 实际行高） | **2 处表头单元格（"工作量(人月)""预计代码行数"）文字所需高度 0.57in > 实际行高 0.50in，会被裁剪** |
| 结论 | must 项全部满足 | **实测复现了评审意见 #5 指出的问题类型**：without 路径既产生了 shape 级溢出，也产生了纯 shape 边界检查测不出的文字级截断 |

## 与本 PR 修复的对应关系

- Case 3 的 without-skill 结果**独立验证**了评审意见「overflow 检查测不出文字溢出」
  的必要性——手工分配行高极易导致文字被裁剪且不被简单的 shape 边界检查发现。
  修复后的 `table_slide`（按实际文字测量自适应行高 + 溢出时发 `UserWarning`）在
  with-skill 路径上没有复现这个问题。
- Case 1 验证了 `_rr_lines` / `_num()` 修复后，最小 spec 与部分缺失字段都能正确
  显示「待评估 / TBD」或"已知小计 + 待评估计数"，而不是静默留白或把 unknown
  折算成 0。
- Case 2 验证了 SKILL.md 示例（`flow_slide` / `layered_diagram_slide`）修复
  `takeaway=` 缺失后可正常运行；`architecture_slide` 路径本身在 with/without
  对比中体现出明显的效率与正确性优势（0 轮 vs 3 轮坐标调试）。

## 局限与后续

- 本报告由 Agent 会话生成对比数据，不等价于 `skills-judge` 工具的正式评分
  （该工具不在本仓库内，需要维护者在其评分环境中运行）。建议维护者在此报告
  基础上运行 `skills-judge` 给出正式 B 级及以上评分，并将评分结果附加到本
  报告或单独提交。
- with/without 对比目前基于 3 个 eval case、每 case 各 1 次运行；如需更强的
  统计显著性，可增加每 case 的重复次数。
- 产物文件（`output.pptx`/`build.py`）未随本报告提交到仓库（体积与可重现性
  考虑），如评审需要可另行提供。
