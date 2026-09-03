---
name: ohos-review
description: Use when reviewing an OH change for spec compliance and evidence, before claiming it passes review. Required when actual scope contains code; optional for docs-only changes but strict once enabled. Do NOT use before spec is approved.
license: MIT
---

# OHOS Review

## Overview

逐 AC 规格符合性审查 + 证据要求。先符合 spec,再谈代码质量。

**Core principle:** 不多、不少、不误解 —— 实现与 spec 精确对应;证据先于声明。

## Prerequisites

- Part of the OHOS SDD workflow — see `using-ohos-sdd` for discovery and profile routing
- `manifest.md` tracks feature metadata including `profile` (repo classification)
- `{{ASSET_ROOT}}` is a build-time placeholder for the plugin's shared asset directory

## 核心规则

1. 读 spec.md + design.md + execution-plan.md + 实现 diff + {{ASSET_ROOT}}/templates/review.md，并先检查 execution-plan「代码范围映射」的实际范围
   - 三份独立证据分别使用 `templates/review/spec-compliance.md`、`code-quality.md`、`verification.md`
   - 实际范围含代码文件/符号：三份 Evidence 必须生成且 Approved
   - 实际范围仅文档类文件或 `N/A：理由`：Evidence 可选；一旦生成任一份，仍须三份齐全且 Approved
2. 逐 AC 合规:实现是否精确对应(不多不少不误解)
3. 证据写入 evidence/reviews/spec-compliance.md(逐 AC 结论,Level D 机器真相源)
4. 先符合 spec,再谈代码质量(规范符合性先于代码质量)
5. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
6. 产出（状态触发）:代码变更产出 review.md(仅 GA/GB/GC 汇总、Evidence 索引、开放问题和最终决策)+ evidence/reviews/spec-compliance.md + code-quality.md + verification.md；纯文档变更可不产出，启用时产物相同
7. 详细 AC 结论、finding、质量维度、执行记录和独立 Verdict 只写入对应 Evidence；review.md 不复制这些明细，也不能替代任一 Evidence
8. 若 AC→Task→Code→Commit→Review 追溯断裂、Actual Result 缺失或 Anti-Fake Completion 不通过,退回 execution-plan 修订,不得给出通过结论

## Rationalizations

| 念头 | 现实 |
|---|---|
| "看起来可以" | 逐 AC 精确对应,不靠看 |
| "AI 自评通过" | 证据写入 evidence/reviews/* |
| "先代码质量" | 先符合 spec,再代码质量 |

## Verification Checklist

- [ ] 每 AC 有合规结论(PASS/FAIL)+ 证据
- [ ] Evidence 是否必需只由 execution-plan 实际范围决定，未按 complexity 放宽
- [ ] review.md 仅汇总和索引，未复制 Evidence 的详细 finding/verdict
- [ ] evidence/reviews/spec-compliance.md 非空(Level D)
- [ ] evidence/reviews/code-quality.md 与 verification.md 非空且结论有真实证据
- [ ] 规范符合性先于代码质量
- [ ] `ohos-sdd validate . --level D` review 边

## 输出

代码实际范围存在时输出 `review.md` + `evidence/reviews/*`；纯文档变更可选（存在即严校验）。下游:`ohos-validate`(归档就绪)。
