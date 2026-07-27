---
name: ohos-review
description: Use when reviewing an OH change for spec compliance and evidence, before claiming it passes review. Do NOT use before spec is approved — there is no review baseline without an approved spec.
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

1. 读 spec.md + 实现 diff + {{ASSET_ROOT}}/templates/review.md
2. 逐 AC 合规:实现是否精确对应(不多不少不误解)
3. 证据写入 evidence/reviews/spec-compliance.md(逐 AC 结论,Level D 机器真相源)
4. 先符合 spec,再谈代码质量(规范符合性先于代码质量)
5. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
6. 产出:review.md(人读索引)+ evidence/reviews/*

## Rationalizations

| 念头 | 现实 |
|---|---|
| "看起来可以" | 逐 AC 精确对应,不靠看 |
| "AI 自评通过" | 证据写入 evidence/reviews/* |
| "先代码质量" | 先符合 spec,再代码质量 |

## Verification Checklist

- [ ] 每 AC 有合规结论(PASS/FAIL)+ 证据
- [ ] evidence/reviews/spec-compliance.md 非空(Level D)
- [ ] 规范符合性先于代码质量
- [ ] `ohos-sdd validate . --level D` review 边

## 输出

`review.md` + `evidence/reviews/*`。下游:`ohos-validate`(归档就绪)。
