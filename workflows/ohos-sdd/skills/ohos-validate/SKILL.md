---
name: ohos-validate
description: Use when about to claim any OH change is complete, passing, or ready to merge — before commit, PR, or archiving. Always run without exception — never skip validate.
compatibility: Requires the ohos-sdd CLI tool for validation checks
license: MIT
---

# OHOS Validate

## Overview

**声称完成前必跑**的守门:调 CLI validate,解读 broken_edges,按 rework_capability 路由回对应能力修复。

**Core principle:** Evidence before claims —— 没跑 validate 就不能声称完成/通过/可合入。

## Prerequisites

- Part of the OHOS SDD workflow — see `using-ohos-sdd` for discovery and profile routing
- `manifest.md` tracks feature metadata including `profile` (repo classification)
- `{{ASSET_ROOT}}` is a build-time placeholder for the plugin's shared asset directory
- Requires the `ohos-sdd` CLI for `validate . --level all` and broken-edge routing

## 核心规则(Iron Law)

```
NO COMPLETION CLAIMS WITHOUT `ohos-sdd validate . --level all` FRESH OUTPUT
```

1. 跑 ohos-sdd validate . --level all(在 change 目录)
2. 读 broken_edges:每条含 level/artifact/issue/rework_capability
3. 有 broken → 按 rework_capability 回对应能力 skill 修复(不在本 skill 内修)
4. 全绿(0 broken)→ 方可声称完成,声明附 validate 输出
5. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
6. evidence/checks/check-*.md 记录验证证据

## Rationalizations

| 念头 | 现实 |
|---|---|
| "应该没问题" | RUN validate |
| "手动测过了" | validate 是机器一致性,手动不等 |
| "下次再 validate" | 声称完成前必跑,无例外 |
| "我很有信心" | 信心 ≠ 证据 |

## Red Flags - STOP

- 即将说"完成/通过/可合入"但没跑 validate
- 用"应该/大概/看起来"
- 信任 agent 自报成功
- 部分校验代替全 level

**任一出现:先跑 `ohos-sdd validate . --level all`。**

## Verification Checklist

- [ ] 跑了 `ohos-sdd validate . --level all`
- [ ] 读了 broken_edges(0 broken 或已路由修复)
- [ ] 完成声明附 validate 输出证据

## 输出

产 `evidence/checks/check-*.md` 验证证据(owns `gate_checklist`,其运行产物)+ 验证结论(回注 rework_capability 到 broken_edges)。回退路由:所有能力 skill(按 rework_capability)。
