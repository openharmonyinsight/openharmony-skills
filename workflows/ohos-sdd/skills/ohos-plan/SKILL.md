---
name: ohos-plan
description: Use when writing execution-plan.md or decomposing work into tasks, after proposal/spec/design are approved. All complexities keep execution-plan.md; simple changes use a concise 1-2 Task plan.
license: MIT
---

# OHOS Plan

## Overview

把 design 落成可执行 Task 拆分 + AC→Task 追溯 + 受影响文件清单。

**Core principle:** spec 每个 AC 在 plan 覆盖(Level C 边);Task 粒度独立可验证;生成文件声明生成源。

## Prerequisites

- Part of the OHOS SDD workflow — see `using-ohos-sdd` for discovery and profile routing
- `manifest.md` tracks feature metadata including `profile` (repo classification)
- `{{ASSET_ROOT}}` is a build-time placeholder for the plugin's shared asset directory

## 核心规则

1. 读 approved proposal/spec/design + {{ASSET_ROOT}}/templates/execution-plan.md
   - 所有复杂度都消费 design.md；简单变更的 design 可只记录关键约束或明确 N/A
   - 所有复杂度都产出 execution-plan.md；简单变更压缩为 1-2 个 Task
2. `execution-plan.md` 的“AC 到 Task 追溯”是 AC→Task 的单一事实源；建立 AC→Task→Code→Commit→Review 追溯，计划阶段先填 AC/Task/计划文件，实施后回填实际文件、Commit 和 Review Evidence
3. 若 design 定义 STATE-*/INV-*,每个不变量必须落到对应 Task 的 AC 映射、状态生命周期、Anti-Fake Completion 和 Verification
4. 每个 Task 明确 Produces/Consumes，跨 Task 的签名、错误码和数据结构必须一致
5. Task 的 Spec/Design 上下文只写已存在的 AC/R/ADR/STATE/INV 编号和文档章节锚点，禁止复制上游正文；简单变更引用 design.md 中的简写约束或 N/A 章节
6. 新增或修改状态时明确 owner、key/index、创建、读取、更新和清理生命周期，并与 design 的 STATE-* 一致
7. 每个验证项同时定义 Expected Result 和 Actual Result，并填写 Anti-Fake Completion 证据
8. 受影响文件全量清单(声明计划文件范围)，并在代码范围映射中回填实际范围和偏差
9. 生成文件(bridge/IDL/CAPI/cpptoc)声明生成源 + 生成命令
10. 若 `.codespec/changes/<id>/threat-model.md` 在场,其 P0/P1 缓解措施必须落到 Task(可执行),并在 `test-spec.md`「安全与权限」场景里对应验证
11. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
12. 提交审查前在本 Skill 内完成运行时自检；机器已覆盖的项目以 validate 结果为准，语义检查只报告结论，不把通用自审清单写入 execution-plan.md
13. 产出:execution-plan.md(+ tasks/<id>.md / bugfix / regression-test / test-spec)；task.md 始终是可选拆分件，不能替代 execution-plan.md

## Rationalizations

| 念头 | 现实 |
|---|---|
| "Task 粒度随意" | 每个 Task 独立可验证闭环 |
| "生成文件手改" | 声明生成源,手改只临时验证 |
| "AC 覆盖以后再说" | Level C 校 spec→plan AC 覆盖 |

## Verification Checklist

- [ ] spec 每 AC 在 plan 覆盖，且 AC→Task 映射只在 execution-plan 维护
- [ ] 受影响文件清单完整
- [ ] Produces/Consumes 和状态生命周期完整
- [ ] 每个 Task 的 Spec/Design References 只使用有效编号和锚点，无正文复制
- [ ] design 的 STATE-*/INV-* 已完整映射到 Task 和验证
- [ ] Expected/Actual、Anti-Fake Completion 和代码范围映射完整
- [ ] 生成文件声明生成源
- [ ] Task 粒度形成独立能力闭环，交接信息自包含且未要求执行 Agent 自行寻找未列上下文
- [ ] 超 3000 行阈值的 Task 已拆分或给出可审查的不拆分理由
- [ ] `ohos-sdd validate . --level C` spec→execution-plan 边

## 输出

`execution-plan.md`(+ tasks/...)。下游:code 实现 + `ohos-review`/`ohos-validate`。
