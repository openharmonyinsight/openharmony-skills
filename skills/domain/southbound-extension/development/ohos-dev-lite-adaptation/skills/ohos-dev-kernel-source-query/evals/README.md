# ohos-dev-kernel-source-query evals

4 个评估用例，判据全部来自本 skill 自身数据（芯片→数据源映射表 / 路径速记 / Sourcegraph·GitCode 工具链 / 失败兜底表，含真实踩坑记录），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `chip_type_source_routing` | 两颗芯片（有/无 MMU）选数据源 | 映射表命中 + 决策树路由 | 映射表真实条目：AT32F437→NuttX BSP（Fallback Artery SDK）、全志T507→Linux mainline as H616 |
| `compatible_string_content_search` | compatible 反查驱动文件 | Sourcegraph 内容搜索 + literal 精确匹配 | 阶段2/查询工具节真实命令形态 + drivers/watchdog 路径规律 |
| `dts_and_register_definition_lookup` | DTS/寄存器定义查询 | 近似型号映射 + Fallback + 路径规律 | 映射表（STM32F407→as F429 / Fallback CMSIS-SVD）+ 路径速记（STM32 时钟无 st/ 子目录） |
| `gitcode_fallback_when_raw_url_fails` | GitCode raw URL 返回 HTML | 失败兜底 + GitCode API 两步流程 | SKILL.md 真实踩坑注记（raw URL 不可用、API 免认证、Sourcegraph 不索引 GitCode） |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条布尔判定。全部用例 expectations 全过 = 通过。

**without skill（基线）**：同一 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]`。预期基线弱项：
- 近似型号映射（T507 按 H616 查、F407 按 F429 查——基线常直接搜型号无果后放弃）
- GitCode raw URL 坑（基线常反复换路径试 raw URL 而不知要走 contents API + blobs/{sha}）
- STM32 时钟驱动路径特例（基线不知道 st/ 子目录规律差异）
- 免 clone 意识（基线可能建议 clone 仓库）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。
