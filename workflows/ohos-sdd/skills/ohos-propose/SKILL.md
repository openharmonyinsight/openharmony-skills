---
name: ohos-propose
description: Use when drafting, refreshing, or baselining a proposal.md, or when a new OH requirement or change enters the workflow. Do NOT use to make requirement changes without revising the baseline — always reopen the clarification and baseline cycle for post-spec changes.
license: MIT
---

# OHOS Propose

## Overview

起草/刷新 `proposal.md` 并冻结需求基线。proposal 是交付件依赖图的**根**(spec/design/plan 的上游),基线不稳则下游全摇晃。

**Core principle:** 先澄清再基线;基线需需求方/Owner/SIG 明确确认,不是 AI 自评。

## Prerequisites

- Part of the OHOS SDD workflow — see `using-ohos-sdd` for discovery and profile routing
- `manifest.md` tracks feature metadata including `profile` (repo classification)
- `{{ASSET_ROOT}}` is a build-time placeholder for the plugin's shared asset directory
- Slash commands: `/ohos-intake` (new requirement), `/ohos-baseline` (freeze baseline)

## 核心规则

1. 读 {{ASSET_ROOT}}/templates/proposal.md + manifest.md + {{ASSET_ROOT}}/workflow/workflow.md 依赖图
2. target_release 写 proposal frontmatter(不在 manifest,P2 已迁)
3. 先定义"不涉及项"(N/A 维度),避免实现期扩写
4. 标准及以上复杂度:逐项澄清(可 invoke ohos-clarify)
5. 基线结论 = 通过/条件通过/不通过;需需求方/Owner/SIG 确认证据
6. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
7. 产出:proposal.md(+ manifest.md 元数据)

## Rationalizations

| 念头 | 现实 |
|---|---|
| "需求很清楚不用澄清" | 标准及以上必须逐项澄清 |
| "先写 spec 再补 proposal" | proposal 是根,先基线 |
| "target_release 写 manifest" | P2 已迁 proposal frontmatter |
| "AI 自评基线通过" | 需求方/Owner/SIG 确认证据 |

## Verification Checklist

- [ ] target_release 在 proposal frontmatter(id+status)
- [ ] 不涉及项已显式 N/A
- [ ] 标准及以上:澄清逐项关闭
- [ ] 基线结论有需求方/Owner/SIG 确认
- [ ] `ohos-sdd validate . --level A` proposal(required)存在

## 输出

`proposal.md`(+ `manifest.md`)。下游:`ohos-spec`(见 `{{ASSET_ROOT}}/workflow/workflow.md` 依赖图)。
