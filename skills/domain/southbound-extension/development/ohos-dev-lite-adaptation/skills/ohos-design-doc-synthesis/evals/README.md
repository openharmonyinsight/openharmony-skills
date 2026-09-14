# ohos-design-doc-synthesis evals

3 个评估用例，判据来自真实合成产物（SR-07 `Hi3516CV610_L1_适配指南.md`：9 章结构/变量来自上游/术语一致）+ skill 自身模板与禁止操作规则，非编造。

> **2026-08-27 C-6 修订**：全部用例 prompt 已去内嵌脚手架——上游数据改为中性事实清单（不再内嵌"L1 精简版 HDF + HCS"等正确措辞，驱动条目只说"配置走 HCS"）、删去"只输出文档框架"提示与意图预排除词、缺失数据处理改为开放式提问；expectations 同步调整（术语须执行者自取、缺失章节保留显式占位）。判据来源（source_example）不变。重跑记录见 `evals-reports/{with,without}/ohos-design-doc-synthesis.md` 的重跑小节。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `l1_adaptation_guide_fill_from_upstream_outputs` | 读上游产出填 9 章适配指南 | 结构完整 / 变量来自上游非编造 / 术语一致（小型系统、精简版 HDF） | SR-07 真实合成产物（9 章 + 实测 XTS/编译数据填充） |
| `deliverable_template_selection_by_intent` | 按意图选三种 deliverable 模板 | 移植指南 vs 适配手册 vs API 参考的意图路由 | SKILL.md Step 0 决策树 |
| `missing_upstream_data_marked_not_fabricated` | 上游数据缺失 | 标 WIP 不编造，不把"没跑"写成"应该支持" | SKILL.md 禁止操作表 + Step 3 填充规则 |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent。预期基线在以下断言上显著弱于 with skill：

- `l1_adaptation_guide`：基线章节结构随意（无固定 9 章模板）、规格值常凭记忆补全（编主频/外设）、术语混用（"轻量 HDF"/"Mini System"直译）
- `missing_upstream_data`：基线倾向编合理的 XTS 数字或写"各外设均支持"填满矩阵（不标 WIP）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **结构化程度**：with skill 输出严格 9 章（或 7 章移植指南）模板；基线自由发挥
2. **数据溯源**：with skill 全部数值来自给定上游 + 头部数据来源块；基线常见无出处补全
3. **缺失诚实度**：with skill 缺失标 WIP；基线倾向编造填充
4. **术语一致**：with skill 全文统一（小型系统/精简版 HDF/LiteOS-A）；基线混用
