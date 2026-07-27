---
name: ohos-spec
description: Use when writing or updating spec.md — acceptance criteria, coverage, compatibility, before design. Do NOT use before proposal is baselined (run ohos-propose first), or for implementation details (that belongs in design).
license: MIT
---

# OHOS Spec

## Overview

固化用户可见行为 + 验收标准。spec 是 design/plan 的上游真相源。

**Core principle:** 只写"用户可见行为 + AC + 兼容性";实现细节归 design。

## Prerequisites

- Part of the OHOS SDD workflow — see `using-ohos-sdd` for discovery and profile routing
- `manifest.md` tracks feature metadata including `profile` (repo classification)
- `{{ASSET_ROOT}}` is a build-time placeholder for the plugin's shared asset directory

## 核心规则

1. 读 approved proposal.md + {{ASSET_ROOT}}/templates/spec.md + {{ASSET_ROOT}}/workflow/workflow.md
2. AC 用 WHEN/THEN 格式,可测试可度量
3. 验收追溯 ≥1 AC(追溯 proposal 成功标准,Level C 边)
4. 不写实现流程/中间件链路/框架类名(归 design)
5. 兼容性声明完整;API 变更项清单(与 design 共享锚点)
6. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
7. 产出:spec.md(+ epic/scenario-library 当需要)

## Rationalizations

| 念头 | 现实 |
|---|---|
| "AC 太细" | WHEN/THEN 可测可度量 |
| "实现细节先写这里" | 归 design,spec 只行为 |
| "跳过验收追溯" | Level C 校 spec→plan AC 覆盖 |

## Verification Checklist

- [ ] AC 用 WHEN/THEN,可测
- [ ] 验收追溯 ≥1 AC
- [ ] 无实现细节(归 design)
- [ ] 兼容性声明 + API 变更清单
- [ ] `ohos-sdd validate . --level B` + `ohos-sdd validate . --level C` spec 结构 + AC 边

## 输出

`spec.md`(+ epic/scenario-library)。下游:`ohos-design`。
