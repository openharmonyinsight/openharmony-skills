---
name: ohos-clarify
description: Structured clarification cycle that converges ambiguous requirements into a baselinable scope. Use when an OH requirement's scope, success criteria, or constraints are ambiguous, unclear, or contested — before freezing a baseline. Do NOT use for already-baselined requirements — reopen the baseline in proposal instead.
license: MIT
---

# OHOS Clarify

## Overview

结构化澄清循环:把模糊需求收敛成可基线的明确范围。横切能力(不 own 交付件),产出回写 `proposal.md`。

**Core principle:** 逐项关闭,状态明确(已澄清/N/A);不靠"大概理解"基线。

## Prerequisites

- Part of the OHOS SDD workflow — see `using-ohos-sdd` for discovery and profile routing
- `manifest.md` tracks feature metadata including `profile` (repo classification)
- `{{ASSET_ROOT}}` is a build-time placeholder for the plugin's shared asset directory

## 核心规则

1. 列出待澄清项(范围/AC/约束/不涉及/兼容性/性能...)
2. 逐项:提问 → 等需求方/Owner/SIG 回答 → 记录结论 + 确认来源
3. 每项状态:已澄清 / N/A(附依据)/ 待澄清(阻塞)
4. 全部关闭前不得基线
5. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
6. 产出回写 proposal.md 的澄清记录段

## Rationalizations

| 念头 | 现实 |
|---|---|
| "范围够清楚" | 标准及以上逐项确认 |
| "跳过澄清省时间" | 模糊基线 → 下游全返工 |
| "AI 推断需求方意图" | 必须需求方/Owner/SIG 明确确认 |

## Verification Checklist

- [ ] 每个待澄清项有结论 + 确认来源
- [ ] N/A 项有依据
- [ ] 无"待澄清"遗留(基线前)
- [ ] 结论回写 proposal.md

## 输出

无独立交付件;澄清记录入 `proposal.md`。上游/下游:`ohos-propose`(基线)。
