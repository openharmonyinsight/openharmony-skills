# ohos-dev-rtos-migrate evals

5 个评估用例，判据全部来自真实交付数据（SR-05 RTOS迁移助手 自验证说明 + iter09/iter10 测试件：22 条 API 映射表、include 缺陷编译失败证据、fetch 返回值语义坑）与 SKILL.md 速查表，非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `vendor_osal_to_l1_hdf_watchdog` | 厂商 OSAL 驱动 → L1 HDF 完整迁移 | 策略 C 变体判定 + 22 条映射骨架 + WatchdogCntlr/Method 重构 + HCS 三方配对 | SR-05 iter09/iter10：rich_linux_driver.c 真实输入 + hi3516_watchdog_hdf.c 真实产出（交叉编译通过） |
| `atomic_return_value_semantics` | 原子操作返回值语义（新值 vs 旧值） | fetch 旧值 / op-fetch 新值辨析——照抄会反转判断逻辑 | migration-plan.md 映射 #11/#12（increturn/decreturn 返回新值）+ rich_linux_driver.c ot_dog_open 真实独占打开代码 |
| `include_defect_needs_real_compile` | 结构自检盲区 → include 缺陷 | WATCHDOG_START undeclared 真实翻车点 + 真编译必要性 | SR-05 §4.1：iter09 未真编译漏掉 watchdog_if.h include，产出件编译失败 |
| `no_direct_mapping_alternative_not_todo` | 无直接映射 API 的处理 | 组合替代方案 + 置信度标注，不留 TODO 不编造 | iter10 migration-plan.md 映射 #8/#10（⚠️ 中置信度 2 条，0 TODO） |
| `l0_native_api_no_osal` | FreeRTOS → L0 原生 API 映射 | L0 禁 OSAL + 栈单位/Tick 频率换算 | SKILL.md ③ 速查表 20 条核心映射真实数据 |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条布尔判定。全部用例 expectations 全过 = 通过。

**without skill（基线）**：同一 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]`。预期基线弱项：
- `__atomic_fetch_add`（旧值）vs `__atomic_add_fetch`（新值）语义坑——基线常随便选一个
- include 传递包含盲区（基线常认为结构看着对就行）
- 栈 word→字节、Tick 1000Hz→100Hz 换算（基线常原样照抄数值）
- L0/L1 目标 API 集混用（基线可能在 L0 里用 Osal*）
- 无直接映射时留 TODO 或编造假 API（skill 要求组合替代 + 置信度标注）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。
