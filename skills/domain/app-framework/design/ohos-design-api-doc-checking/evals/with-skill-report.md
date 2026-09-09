# With Skill Final Evaluation Report

Skill: `ohos-design-api-doc-checking` (v0.1.0, draft)

Evaluation date: 2026-09-08

Evaluation method: rubric assertion review against `evals/evals.json`。每个用例包含植入缺陷的测试输入（`evals/inputs/`）、预期结果（`expected_output`）与逐条期望（`expectations`）。A case is marked pass only when every expectation in the case is satisfied. This report represents the with-skill run, where the evaluator loads SKILL.md and applies the rule modules under `references/`. Raw run output: `evals/runs/with-skill-output.md`.

## Summary

| Metric | Result |
| --- | --- |
| Total cases | 3 |
| Passed | 3 |
| Failed | 0 |
| Pass rate | **100%** |
| Findings produced | 28 (12 + 7 + 9) |
| Planted defects hit | 16/16 (100% recall) |

## Case Results

| Case | Result | Expectations | Key with-skill behavior |
| --- | --- | --- | --- |
| `api_doc_planted_errors` | **Pass** | 7/7 | 全部命中植入缺陷：`recieve`、`UiAbility`、`$ {` 模板字符串空格(syntax-001)、示例大括号未闭合(syntax-002/003)、"完整示例"名不副实(clarity-001)、queryTasks 缺错误码(completeness-002)；另发现"取消"能力无对应 API、回调 API 返回值误标、`9+` 未用 `<sup>` 导致锚点失效等超出植入集的真实问题 |
| `sdk_consistency_check` | **Pass** | 5/5 | 正确应用映射规则 `js-apis-{name}.md → api/@ohos.{name}.d.ts`；命中起始版本 9+ vs `@since 10` 并按规则标为**严重/Critical**；命中 createTask 缺 801、TaskInfo 缺 `priority` 字段、示例因缺字段无法编译；同时给出 7 个通过/不适用检查点的核对证据 |
| `dev_guide_scope_and_rules` | **Pass** | 6/6 | 明确判定为开发指南并给出依据；按 SKILL.md 范围规则执行必选 8 模块、说明可选 2 模块的执行理由、明确跳过 SDK 一致性检查与 `enabled:false` 规则；命中模糊用词三连(clarity-002)、`$ {` 空格、`recieve`、"高级用法"标题不符(clarity-001/findability-001)、死链 |

## Expectation Detail (grading evidence)

### Case 1: api_doc_planted_errors — 7/7

| # | Expectation | Verdict | Evidence (with-skill-output.md) |
| --- | --- | --- | --- |
| 1 | 逐条结构化记录（类型/行号/原因/建议/级别） | ✅ | 12 行结构化表格，额外含规则 ID 与置信度 |
| 2 | recieve → receive | ✅ | spelling-001, L55, 置信度 95% |
| 3 | UiAbility → UIAbility | ✅ | spelling-002 (glossary AbilityFramework.UIAbility), L55 |
| 4 | `$ {` 模板字符串空格 | ✅ | syntax-001, L46, 置信度 100% |
| 5 | 大括号未闭合 | ✅ | syntax-002/003, L63-70, 严重 |
| 6 | "完整示例"标题与内容不符 | ✅ | clarity-001, L61, 命中 badPattern |
| 7 | queryTasks 缺错误码表 | ✅ | completeness-002, L53-70 |

### Case 2: sdk_consistency_check — 5/5

| # | Expectation | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | 应用文件映射并实际比对 | ✅ | 引用 correctness-rules.json mappingRules，逐检查点比对 |
| 2 | 9+ vs @since 10 且标为 Critical/严重 | ✅ | api-since-version-match, 严重, 置信度 95% |
| 3 | createTask 缺 801 | ✅ | error-code-match, L30-32 |
| 4 | TaskInfo 缺 priority | ✅ | interface-fields-complete, L78-81 |
| 5 | 结构化不一致记录（检查点/位置/文档值 vs SDK 值/级别） | ✅ | 7 项不一致 + 7 项通过检查点证据表 |

### Case 3: dev_guide_scope_and_rules — 6/6

| # | Expectation | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | 判定为开发指南并给依据 | ✅ | 文件名含 guide + 章节结构依据 |
| 2 | 说明跳过 SDK 检查、completeness/capability 为可选 | ✅ | 模块执行范围三张表（必选/可选/跳过） |
| 3 | 命中模糊用词（某些情况下/可能会/大概） | ✅ | clarity-002, L7, 三个模糊词全部点名 |
| 4 | `$ {` 空格 | ✅ | syntax-001, L26 |
| 5 | recieve | ✅ | spelling-001, L32 |
| 6 | "高级用法"标题与内容不符 | ✅ | clarity-001 + findability-001, L34-36 |

## Key Differences Versus Without Skill

- **严重级别校准**：with skill 按规则库将起始版本不一致定为"严重/Critical"；baseline 仅定为"高"，优先级校准依赖规则库而非个人判断。
- **范围治理**：with skill 先做文档类型判定，再按 SKILL.md 决定模块范围（指南跳过 SDK 检查、completeness/capability 可选）；baseline 无范围概念，检查面随评审者经验漂移。
- **可追溯性**：每条发现带规则 ID（syntax-001、clarity-002 等）与置信度，可审计、可回归；baseline 发现无规则映射。
- **覆盖保证**：with skill 对 SDK 10 个检查点逐项给出"命中/通过/不适用"结论（含 param-count、systemapi 等通过项证据）；baseline 只报告发现的问题，无法证明未漏检。
- **深度发现**：with skill 额外命中 `9+` 未用 `<sup>` 上标导致锚点失效（versionPatterns 规则）、"取消"能力在文档与 SDK 中均无实现等 baseline 未系统性覆盖的问题。
- **baseline 的反向亮点**：without skill 发现了 d.ts 缺 `@permission` 声明与文档权限描述不一致的问题，当前规则库未覆盖该检查点，已记入规则扩展建议（见 without-skill-report.md）。

## Conclusion

With-skill run passes **3/3 cases (100%)**, satisfying the entry requirement "with skill 评估必须全部通过".
