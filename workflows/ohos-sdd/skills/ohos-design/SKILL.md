---
name: ohos-design
description: Use when writing or updating design.md — architectural decisions and module impact, after spec approved. Always keep design.md; simple changes may record only a brief technical constraint or explicit N/A rationale.
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

1. 读 approved proposal.md + spec.md + {{ASSET_ROOT}}/templates/design.md；所有复杂度都产出 design.md，简单变更只需简写关键约束或明确 N/A
2. 设计决策对比(备选 vs 选定 + 理由)
3. 模块/分层影响;引用 spec AC(design AC ⊆ spec AC,Level C 边)
4. 分层调用合规(应用→框架→服务→内核);无跨层违规
5. 代码事实基线(条件触发):涉及已有实现时,用 `文件:行/符号 → 已验证事实 → 架构规则 → 设计约束` 固化现状;二手资料或推测不能进入 Approved 基线
6. 既有模式复用(条件触发):检索相邻能力的接口、错误处理、资源/并发和测试模式;有 prior art 则声明复用与偏差,无则记录检索范围和 no prior art found
7. 类图(条件触发):继承/接口实现层级、IPC proxy/stub/impl 或跨模块组合关系变化时,冻结关键类关系并关联 ADR/Task
8. 状态归属与不变量(条件触发):统一定义 STATE-* 的唯一 Owner、完整生命周期、恢复和并发模型;每个 INV-* 必须关联 spec AC、后续 Task、验证方式和通过标准,并被状态机/资源/并发设计引用
9. 安全基础检查(条件触发):读 proposal「不涉及项确认」→「安全与权限」;= 是 → 读 {{ASSET_ROOT}}/analysis/security-playbook.md 获取检查项含义和推荐值 → 在 design.md「可选设计扩展」下展开「安全基础检查」(信任边界 + 基础要求 + 敏感数据);命中高风险判据(见 ohos-security-threat-model 触发条件表)→ 在「深度威胁分析(如需)」记录升级决定并链到 threat-model.md;= 否/N/A → 省略,不留空占位
10. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
11. 产出:design.md

## Rationalizations

| 念头 | 现实 |
|---|---|
| "简单变更不需要 design 文件" | 四件套固定存在；简单变更在 design.md 记一句约束或明确 N/A |
| "先实现再补 design" | design 先于 plan/code |
| "design 发明新行为" | 行为在 spec,design 只实现路径 |

## Verification Checklist

- [ ] 设计决策有备选对比 + 理由
- [ ] design AC ⊆ spec AC
- [ ] 分层合规,无跨层违规
- [ ] 命中条件时,代码事实均有文件:行/符号引用且形成设计约束
- [ ] 既有模式复用或 no prior art 检索结论明确
- [ ] 类图与代码事实、ADR、Task 一致
- [ ] 每个 INV-* 关联 AC、Task、验证方式并被状态/资源/并发设计引用
- [ ] `ohos-sdd validate . --level C` spec→design 边

## 输出

`design.md`。下游:`ohos-plan`。
