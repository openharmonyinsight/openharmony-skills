# ohos-test-lite-ut-gen evals

5 个评估用例，判据全部来自真实交付件数据（SR-10 自验证说明 + iter09/iter12 真实生成物），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `l0_gpio_hctest_five_scenario_generation` | L0 GPIO 五类场景生成（HCTest+iCunit + BUILD.gn） | 框架选择 / 五类覆盖 / 断言判别力 / ISR 真 callback / 不硬编码引脚 | iter12 端到端真产物 `iot_gpio_test_27.c`（27 用例板子 27/27 PASS） |
| `l1_watchdog_hwtest_gtest_generation` | L1-Linux watchdog HWTest/gtest 生成 | L1 框架选择 + 不混用 L0 宏 + L1 不硬凑 ISR/CMSIS | iter09 测试1：`watchdog_hal_test.cpp` 17 用例编进 ARM .bin（ninja 退出码 0） |
| `anti_pattern_vacuous_boundary_assertion_review` | 反模式审查：边界断言退化恒真 | `TEST_ASSERT_UINT32_WITHIN(1,0,ret)` 对 {0,1} 返回值恒真 → 修为具体值断言 | iter09 测试2 真实翻车点（deep-review 判定），iter10/iter12 修复 |
| `isr_null_callback_and_cmsis_case_presence` | ISR NULL callback 假红 + CMSIS 用例必要性 | ISR 用例传真 callback / CMSIS 兼容用例不可省 | iter12 v1→v2：v1 NULL callback 烧板 HardFault，v2 修复后 27/27 PASS |
| `board_test_not_running_gc_sections_triage` | 烧板测试不跑 / 注册时 HardFault | gc-sections 丢 zinitcall 段判定 + KEEP 修法 + nm 三条编后验证 | iter12 最大坑（已回填 skill commit b1e9eb7，Step 5.5 / Step 7 §抗 gc-sections） |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]` 判定。预期基线在以下断言上显著弱于 with skill：

- `l0` 用例的断言宏名精确性（基线常写 `ICUNIT_ASSERT_EQ` 这类不存在的宏）、BUILD.gn include 路径下划线（`iot_hardware`）
- `anti_pattern` 用例：基线常不识别 WITHIN(1,0,ret) 退化恒真，认为"能编译就行"
- `isr_null_callback` 用例：基线可能认可 NULL callback 简化写法（iter09 首版真实翻车点）
- `gc_sections` 用例：基线倾向怪驱动/烧录，不知道 zinitcall KEEP 机制

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **框架纯度**：with skill L0 零 C++ 混入 / L1 零 iCunit 混入；基线常混用
2. **断言判别力**：with skill 断言具体预期值（IOT_SUCCESS/IOT_FAILURE）；基线倾向 WITHIN/恒真断言（iter09 首版实证）
3. **ISR 写法**：with skill 传真 callback；基线倾向 NULL 简化（烧板 HardFault 实证）
4. **烧板不跑归因**：with skill 直指 gc-sections/zinitcall KEEP + nm 验证；基线无从下手
