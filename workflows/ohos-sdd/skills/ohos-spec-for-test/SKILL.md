---
name: ohos-spec-for-test
description: Use when a developer needs to generate, refresh, or review a Profile-defined spec-for-test.md after spec.md and design.md are Approved, and the matched Profile explicitly declares support for Spec for Test. Do NOT use when the Profile lacks Spec for Test support, or for writing concrete test cases and recording test execution results.
compatibility: Requires the ohos-sdd CLI tool for spec-for-test generation
license: MIT
---

# OHOS Spec for Test

## Overview

为测试人员生成自包含的测试输入规格。旁路不改变 Define → Specify → Design → Plan 主链，也不发明新行为。

**Core principle:** `spec.md` 是行为真相源；`design.md` 只提供测试可观察性和验证约束；`spec-for-test.md` 只承载对外行为和测试侧验证输入，不包含内部实现细节。

## Prerequisites

- Part of the OHOS SDD workflow — see `using-ohos-sdd` for discovery and profile routing
- `manifest.md` tracks feature metadata including `profile` (repo classification)
- `{{ASSET_ROOT}}` is a build-time placeholder for the plugin's shared asset directory
- Requires a Profile that declares `spec_for_test` support; the `ohos-sdd` CLI drives generation

## 核心规则

1. 读取 Approved `spec.md`、`design.md`、`manifest.md`，按 `{{ASSET_ROOT}}/workflow/profile-application.md` 加载命中的 Profile 与子 Profile。
2. 从 Profile 的 `spec_for_test` 配置加载声明式专项分析、可选 adapter/template override 和 playbook；未声明的 Profile 不支持该旁路。
3. 执行 `ohos-sdd spec-for-test generate <change-dir>`；已有产物时使用 `refresh`。
4. 只保留用户可见行为、AC、外部 API 契约、兼容性、用户可观察 NFR 和测试侧验证约束；不得投影开发自验证类型、用例、命令或结果。
5. 生效模板（全局默认或 Profile override）中 `GENERATED:*` 标记的来源投影区域由 CLI 所有：不得摘要、删减、重排或手工改写。发现内部实现信息时，优先修正公共投影规则；仅领域特有内容才修正 Profile adapter，然后重新生成，不能由 Agent 自由改写来源规格。
6. 用户故事必须完整保留角色、目标、价值和所属 AC，不得合并为概述或把多个 US 压缩成一段摘要。
7. 只在 Profile 声明的人工分析区域完成验证追溯与专项分析；若 Profile 模板定义了 2D、NFR、2C 等不同细项格式，必须逐小节按该格式填写，不得合并为统一概览表，也不得保留“待确认”或模板占位符。
8. 不得新增 `spec.md` 中不存在的 AC、规则、API 或行为。发现缺口时回修 spec/design 后重新生成。
9. 将状态更新为 `ReadyForReview`；只有满足 Profile 定义的审批要求后才能改为 `Approved`。
10. 执行 `ohos-sdd spec-for-test check <change-dir>`，检查结果写入 `evidence/checks/check-spec-for-test.md`。

## Verification Checklist

- [ ] Profile 声明了有效的 `spec_for_test` 增量配置和 playbook
- [ ] Spec/Design 均 Approved
- [ ] spec-for-test AC 与 spec AC 一致
- [ ] 每个用户故事的角色、目标、价值和所属 AC 完整保留
- [ ] 所有 `GENERATED:*` 来源投影区域与 CLI fresh render 一致
- [ ] Profile 定义的验证追溯以及 2D/NFR/2C 等专项细项格式完整
- [ ] 无内部实现信息
- [ ] 无开发自验证类型、用例、命令和执行结果
- [ ] 已满足 Profile 定义的审批要求
- [ ] `ohos-sdd spec-for-test check <change-dir>` 通过

## 输出

`spec-for-test.md` + `evidence/checks/check-spec-for-test.md`。具体测试设计仍写入 `test-spec.md` 或测试团队用例系统。
