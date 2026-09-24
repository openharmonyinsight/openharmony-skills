# ohos-dev-soc-spec-parse evals

5 个评估用例，全部源自 iter09 Part B 真实验证判据（交付件 SR-01 深审数据转换，非编造）。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `l1_full_extraction_from_sdk_sources` | 完整提取（L1 双核 SoC，SDK 源码片段输入） | 从 DTS/autoconf.h/clock 头提取结构化规格 + fieldSources 溯源 | iter09 深审：外设 8/8 全核通过 |
| `ddr_variant_singlepoint_xlsm_query` | 单点查询（DDR 变体 → xlsm） | 不跑完整流程直接查答 + 变体表命中 | AR 详设 §3.2 业务场景实测 |
| `contradiction_detection_ref_vs_sdk` | 数据源矛盾（参考资料 vs SDK 源码） | 以可验证源码证据为准 + crossValidation.discrepancies 记录 | 实测：执行者主动发现 quick-ref 单核@950 vs SDK 双核@1200 矛盾 |
| `l0_wifi_checklist_trim_hi3861` | checklist 两维度裁剪（L0 + WiFi） | 系统级别/功能能力判定 → 裁剪正确性 | SKILL.md 适用规则 + Hi3861 真实参数 |
| `no_irq_peripheral_honesty` | 无中断外设诚实处理 | 不编造中断号，空数组 + 说明 | iter09 深审：I2C0/1/2 无 IRQ 诚实标注实证 |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]` 判定。用于证明 skill 带来的提升——预期基线在以下断言上显著弱于 with skill：
- `fieldSources` 溯源（基线常凭记忆填且无来源标注）
- 矛盾发现用例的 discrepancies 记录（基线常盲信某一方或直接给单值）
- 无中断外设诚实处理（基线可能编造 IRQ）
- checklist 裁剪计数（基线不知道三级 16 项模型）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **溯源率**：with skill 要求 100% 非 null 字段有 fieldSources；基线通常 0 溯源
2. **矛盾处理**：with skill 走 crossValidation.discrepancies + 源码为准；基线二选一不给依据
3. **编造率**：无 IRQ / 查不到字段场景，with skill 空数组+说明；基线倾向编造合理值
4. **结构化程度**：with skill 输出符合 ChipSpecification schema（14 项必选字段）；基线输出自由格式
