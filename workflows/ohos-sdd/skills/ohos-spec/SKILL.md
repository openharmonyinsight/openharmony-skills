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
2. AC 用 WHEN/THEN 格式,可测试可度量;WHEN 是用户/开发者/上层业务/外部事件可触发输入
3. 每个 AC 声明可观察表面:终端用户或 Public/System/InnerAPI 三层接口的返回值、回调、错误码、事件或查询结果
4. THEN 只写外部可判定结果;禁止内部数据结构、状态机、调用链、类/方法、缓存/队列、锁和算法,越界内容移 design
5. Level C 的 THEN 词法检查只产生 WARN；逐项语义判断后修正文案或移入 design。合法引用被误报时可加 `<!-- ext-ok -->`，但必须在 gate-checklist 记录理由和确认人
6. 验收追溯 ≥1 AC，只维护 Spec 内部的 AC→规则→可观察表面；不复制 Task、验证方式或执行证据。AC→Task 由 execution-plan、测试入口/Red/通过标准由验证映射、实际证据由 Review Evidence 分别维护
7. 验证映射为每个 AC 给出真实测试入口、实现前失败信号(Red 条件)和通过标准;纯规格补录可 N/A 但必须写理由
8. 兼容性声明完整;新增/变更/废弃 API 使用 Public/System/InnerAPI 开放级别,变更/废弃项同时记录当前与目标级别
9. 涉及 API/错误码时先核对源码或已发布声明:已有项记录精确签名/数值、触发条件、外部行为和文件:行/符号;新增项标记 New 并关联 proposal/design/Task 或 AC
10. 禁止用“错误码范围”“返回错误”“某错误码”代替精确错误码;每个错误码关联异常/边界 AC 和验证入口,发现事实冲突先回 proposal/spec 澄清
11. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
12. 提交审查前在本 Skill 内完成运行时自检；机器已覆盖的项目以 validate 结果为准，语义检查只报告结论，不把通用自审清单写入 spec.md
13. 产出:spec.md(+ epic/scenario-library 当需要)

## Rationalizations

| 念头 | 现实 |
|---|---|
| "AC 太细" | WHEN/THEN 可测可度量 |
| "实现细节先写这里" | 归 design,spec 只行为 |
| "测试写出来能过就行" | Red 条件先证明旧行为或缺失能力会真实失败,再允许实现转 Green |
| "跳过验收追溯" | Level C 校 spec→plan AC 覆盖 |
| "先按经验写个错误码" | API/错误码是事实契约,必须核对源码或发布声明;冲突时回上游澄清 |

## Verification Checklist

- [ ] AC 用 WHEN/THEN,可测
- [ ] 每个 AC 有终端用户或 Public/System/InnerAPI 可观察表面
- [ ] THEN 无内部数据结构/状态机/调用链/类方法/锁/算法
- [ ] 验收追溯 ≥1 AC，且只含 AC、关联规则和可观察表面
- [ ] 每个 AC 有测试入口、Red 条件和通过标准
- [ ] 兼容性声明 + API 变更清单;变更/废弃 API 有当前/目标开放级别
- [ ] API/错误码事实表含精确签名/数值、触发条件、外部行为、事实来源和 AC;每个错误码有验证入口
- [ ] 范围边界清晰，无“快速”“稳定”“尽可能”等不可度量表述
- [ ] 规则无重叠冲突，且每条 AC 可独立测试
- [ ] `ohos-sdd validate . --level B` + `ohos-sdd validate . --level C` spec 结构 + AC 边

## 输出

`spec.md`(+ epic/scenario-library)。下游:`ohos-design`。
