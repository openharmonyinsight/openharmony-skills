---
name: ohos-design
description: Use when writing or updating design.md — architectural decisions and module impact, after spec approved. Do NOT use for simple changes without multi-module, new API, or layering decisions — record a brief technical constraint instead.
license: MIT
---

# OHOS Design

## Overview

确认架构约束 + 关键设计决策 + 模块影响。design 引用 spec AC,不发明行为。

**Core principle:** 设计决策对比有据;design AC ⊆ spec AC(不凭空);分层合规。

## Prerequisites

- Part of the OHOS SDD workflow — see `using-ohos-sdd` for discovery and profile routing
- `manifest.md` tracks feature metadata including `profile` (repo classification)
- `{{ASSET_ROOT}}` is a build-time placeholder for the plugin's shared asset directory

## 核心规则

1. 读 approved proposal.md + spec.md + {{ASSET_ROOT}}/templates/design.md
2. 设计决策对比(备选 vs 选定 + 理由)
3. 模块/分层影响;引用 spec AC(design AC ⊆ spec AC,Level C 边)
4. 分层调用合规(应用→框架→服务→内核);无跨层违规
5. 安全基础检查(条件触发):读 proposal「不涉及项确认」→「安全与权限」;= 是 → 读 {{ASSET_ROOT}}/analysis/security-playbook.md 获取检查项含义和推荐值 → 在 design.md「可选设计扩展」下展开「安全基础检查」(信任边界 + 基础要求 + 敏感数据);命中高风险判据(见 ohos-security-threat-model 触发条件表)→ 在「深度威胁分析(如需)」记录升级决定并链到 threat-model.md;= 否/N/A → 省略,不留空占位
6. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
7. 产出:design.md

## Rationalizations

| 念头 | 现实 |
|---|---|
| "简单变更跳过 design" | 标准及以上必须;简单才记一句约束 |
| "先实现再补 design" | design 先于 plan/code |
| "design 发明新行为" | 行为在 spec,design 只实现路径 |

## Verification Checklist

- [ ] 设计决策有备选对比 + 理由
- [ ] design AC ⊆ spec AC
- [ ] 分层合规,无跨层违规
- [ ] `ohos-sdd validate . --level C` spec→design 边

## 输出

`design.md`。下游:`ohos-plan`。
