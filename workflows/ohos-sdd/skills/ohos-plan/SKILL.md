---
name: ohos-plan
description: Use when writing execution-plan.md or decomposing work into tasks, after design approved (standard+ complexity). For simple changes, use after spec approved — design may be skipped.
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

1. 读 approved proposal/spec + {{ASSET_ROOT}}/templates/execution-plan.md
   - 标准及以上复杂度:还需读 approved design
   - 简单变更(design 跳过):直接基于 spec 拆 Task,在 plan 开头记录一句技术约束替代 design
2. AC→Task 追溯(spec 每 AC 在 plan 覆盖,Level C 边)
3. 受影响文件全量清单(声明文件范围,不扩范围)
4. 生成文件(bridge/IDL/CAPI/cpptoc)声明生成源 + 生成命令
5. 若 `.codespec/changes/<id>/threat-model.md` 在场,其 P0/P1 缓解措施必须落到 Task(可执行),并在 `test-spec.md`「安全与权限」场景里对应验证
6. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
7. 产出:execution-plan.md(+ tasks/<id>.md / bugfix / regression-test / test-spec)
   - 简单变更:可仅产 task.md(1-2 Tasks),跳过 execution-plan.md

## Rationalizations

| 念头 | 现实 |
|---|---|
| "Task 粒度随意" | 每个 Task 独立可验证闭环 |
| "生成文件手改" | 声明生成源,手改只临时验证 |
| "AC 覆盖以后再说" | Level C 校 spec→plan AC 覆盖 |

## Verification Checklist

- [ ] spec 每 AC 在 plan 覆盖
- [ ] 受影响文件清单完整
- [ ] 生成文件声明生成源
- [ ] `ohos-sdd validate . --level C` spec→execution-plan 边

## 输出

`execution-plan.md`(+ tasks/...)。下游:code 实现 + `ohos-review`/`ohos-validate`。
