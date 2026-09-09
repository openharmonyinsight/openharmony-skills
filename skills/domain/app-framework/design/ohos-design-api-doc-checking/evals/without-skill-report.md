# Without Skill Final Evaluation Report (Baseline)

Skill: `ohos-design-api-doc-checking` — baseline run WITHOUT the skill

Evaluation date: 2026-09-08

Evaluation method: rubric assertion review against `evals/evals.json`, using **the same prompts and the same expectations** as the with-skill run. The baseline reviewer is an experienced OpenHarmony documentation reviewer working from general knowledge only — no SKILL.md, no `references/` rule files, no module scoping. Raw run output: `evals/runs/without-skill-output.md`.

## Summary

| Metric | Result |
| --- | --- |
| Total cases | 3 |
| Passed | 0 |
| Failed | 3 |
| Pass rate | **0%** |
| Findings produced | 29 (11 + 8 + 10) |
| Planted defects hit | 13/16 (81% recall, but expectation-level failures below) |

## Case Results

| Case | Result | Expectations | Failure reasons |
| --- | --- | --- | --- |
| `api_doc_planted_errors` | **Fail** | 6/7 | 未命中期望 6："完整示例"标题与不完整代码不符。baseline 在 L61 仅报"章节标签不一致"（与 createTask 的"示例"标签不统一），未识别标题宣称"完整"而代码被截断的标题-内容矛盾（clarity-001 语义）。其余 6 条期望（结构化记录、recieve、UiAbility、`$ {` 空格、大括号未闭合、queryTasks 缺错误码）均命中 |
| `sdk_consistency_check` | **Fail** | 4/5 | 未满足期望 2 的严重级别要求：命中文档 `9+` 与 d.ts `@since 10` 不一致，但标为"高"而非 Critical/严重，未按 api-since-version-match 检查点的优先级定义校准。其余 4 条期望（实际比对、缺 801、缺 priority、结构化记录）均命中 |
| `dev_guide_scope_and_rules` | **Fail** | 4/6 | 未命中期望 1 与 2：baseline 没有文档类型判定环节（未区分开发指南 vs API 文档），也没有规则模块范围概念（未说明跳过 SDK 一致性检查、completeness/capability 为可选模块）。其余 4 条期望（模糊用词、`$ {` 空格、recieve、"高级用法"标题不符）均命中 |

## Expectation Detail (grading evidence)

### Case 1: api_doc_planted_errors — 6/7

| # | Expectation | Verdict | Evidence (without-skill-output.md) |
| --- | --- | --- | --- |
| 1 | 逐条结构化记录 | ✅ | 11 行结构化表格（类型/行号/原因/建议/级别） |
| 2 | recieve → receive | ✅ | L55 |
| 3 | UiAbility → UIAbility | ✅ | L55 |
| 4 | `$ {` 模板字符串空格 | ✅ | L46 |
| 5 | 大括号未闭合 | ✅ | L66-70 |
| 6 | "完整示例"标题与内容不符 | ❌ | L61 仅报"章节标签不一致"，未识别标题-内容矛盾 |
| 7 | queryTasks 缺错误码表 | ✅ | L53-59 |

### Case 2: sdk_consistency_check — 4/5

| # | Expectation | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | 实际比对文档与 d.ts | ✅ | 逐项引用 d.ts 行号 |
| 2 | 版本不一致且标为 Critical/严重 | ❌ | 命中不一致但严重级别为"高" |
| 3 | createTask 缺 801 | ✅ | L28-32 |
| 4 | TaskInfo 缺 priority | ✅ | L78-81 |
| 5 | 结构化不一致记录 | ✅ | 8 行表格 + 一致性通过项说明 |

### Case 3: dev_guide_scope_and_rules — 4/6

| # | Expectation | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | 判定为开发指南并给依据 | ❌ | 无文档类型判定环节 |
| 2 | 说明 SDK 检查跳过与可选模块 | ❌ | 无规则模块范围概念 |
| 3 | 命中模糊用词 | ✅ | L7（"大概"、"某些情况下"） |
| 4 | `$ {` 空格 | ✅ | L26 |
| 5 | recieve | ✅ | L32 |
| 6 | "高级用法"标题与内容不符 | ✅ | L34-36 |

## Key Differences Versus With Skill

| 维度 | With skill | Without skill (baseline) |
| --- | --- | --- |
| 用例通过率 | 3/3 (100%) | 0/3 (0%) |
| 植入缺陷召回 | 16/16，全部按规则语义命中 | 13/16，3 处期望级失败（标题-内容矛盾、严重级别校准、范围治理） |
| 严重级别校准 | 规则库驱动（版本不一致=严重/Critical） | 经验驱动，同一问题降级为"高" |
| 文档类型/模块范围 | 显式判定 + 必选/可选/跳过三张表 | 无，检查面不可复现 |
| 可追溯性 | 每条发现带规则 ID + 置信度 | 无规则映射、无置信度 |
| 覆盖证明 | SDK 10 检查点逐项"命中/通过/不适用" | 仅列发现的问题，无法证明未漏检 |
| 输出稳定性 | 由 SKILL.md 流程约束，跨评审者一致 | 依赖评审者个人经验，波动大 |

### Baseline 的反向发现（规则扩展输入）

baseline 在 Case 2 发现一项 with-skill 未报告的真实问题：文档声明 `ohos.permission.RUNNING_TASKS`，而 d.ts 无任何 `@permission` 注释（权限声明不一致）。当前 `correctness-rules.json` 的 10 个 SDK 检查点未覆盖 permission 比对，建议按 `references/rule-extensions.md` 新增检查点 `permission-mark-match`。这是本次 with/without 对比产生的直接改进项。

## Conclusion

Baseline 具备可用的通用文档评审能力（发现数 29 与 with-skill 的 28 相当），但在**期望级判定上 0/3 通过**：无法保证标题-内容矛盾类语义检查、严重级别校准、文档类型范围治理和规则级可追溯性。对比证明 Skill 相对基线的效果提升主要体现在**一致性、可审计性与覆盖保证**，而非单纯发现数量。
