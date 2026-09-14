# ohos-design-ref-retrieval evals

5 个评估用例：4 个源自 SR-07「适配文档检索」交付件自验证的真实判据（iter09/iter10 live 产出 + 深审抽样 + §4.6 适配文档路径验证，非编造），1 个 L1-Linux 术语正例源自内置 target profile（hi3516cv610-linux-l1）与 R2 检视修复。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `intent_routing_porting_guide_l1_linux` | 意图识别（查移植指南，L1-Linux 路径） | 7 类意图路由 + 主路径选择正确 + L0/L1 接口区分 | SR-07 TC-07-01 实测（iter09 ✅）+ iter10 recommended-refs.md |
| `retrieval_source_and_version_traceability` | 检索推荐带来源与版本 | 检索日期/数据来源标注 + 跨 skill references 覆盖 + claim 可溯源 | SR-07 TC-07-03 + §3.3 深审方法（5 抽样核 claim 真实性） |
| `terminology_consistency_check` | 术语一致性检查 | terminology.md 标准术语（L0/L1/内核名/驱动框架/L2 禁用词）+ 三档状态标注 | SR-07 TC-07-06 实测（iter10 ✅） |
| `adaptation_doc_generation_template_fill` | 生成适配文档路径 | L1 模板选择 + chip_spec.json 变量填充（不编造）+ 头部元数据 | SR-07 §4.6 实测（变量 100% 来自 chip_spec.json） |
| `l1_linux_terminology_positive` | L1-Linux 路线术语正例 | 按 kernel_family 判定：DTS/ext4/Kernel Panic/HWTEST_F 不禁用、不把 L1 一刀切为 LiteOS-A/HCS | 内置 target profile hi3516cv610-linux-l1 + R2 F004 检视修复 |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]` 判定。预期基线在以下断言上显著弱于 with skill：
- 意图路由（基线不知道 7 类意图分类树，L1-Linux vs LiteOS-A 路径区分常缺失）
- 溯源（基线推荐常无来源路径/检索日期，凭记忆编条目）
- 术语（基线常混用 Mini/Small System、iot_gpio.h 用于 L1、'应该支持'式模糊标注）
- 变量填充（基线倾向凭记忆填 RAM/主频等数值）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **意图命中率**：with skill 按 7 类分类树路由并先判 L0/L1 + 内核路径；基线常给通用资料不分路径
2. **溯源率**：with skill 100% 条目带来源 + 头部检索日期；基线通常 0 溯源
3. **术语错误率**：with skill 全文符合 terminology.md（无 L2 禁用词、三档状态）；基线常见混用
4. **编造率**：规格类变量 with skill 只从 chip_spec.json 取、缺则 TODO；基线倾向编合理值
