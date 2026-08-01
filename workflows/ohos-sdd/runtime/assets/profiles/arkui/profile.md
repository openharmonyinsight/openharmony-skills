---
name: arkui
description: Use when working on ArkUI declarative UI framework (ACE Engine) — components, rendering, state-driven UI, multi-device interaction
repos:
  - arkui_ace_engine
  - arkui_ui_appearance
  - arkui_advanced_components
applies_to:
  - "**/components_ng/**"
subprofiles:
  - component
  - capi
  - sdk-api
  - render
spec_for_validation:
  title: ArkUI 测试设计规格
  adapter: arkui
  template_override: templates/spec-for-validation.md
  playbook: analysis/arkui/spec-for-validation.md
  analysis:
    - id: 2d
      title: 2D 能力特征分析
      items:
        - 新增开放 API
        - 应用兼容性
        - 跨平台
        - IDE 预览
        - 编译工具链
        - 全球化语言
        - 深浅色模式
        - 新材质
        - 无障碍
        - 多设备差异
        - 适老化
        - 资料新增或变更
    - id: 2c
      title: 2C 功能体验分析
      items:
        - UX — 静态 UI 效果
        - UX — 动态 UI 效果（动效）
        - UX — 手势/事件/交互/焦点
        - 用户数据
---

# ArkUI Profile

适用场景：

- UI 框架/组件
- 状态驱动界面
- 多设备形态和交互能力

本 profile 是 ArkUI / ACE Engine 变更的基础 profile。执行时必须先遵循 OHOS_SDD 通用流程，再追加本文档定义的 ArkUI 检查点。若 `manifest.subprofiles` 命中 `component`、`capi`、`sdk-api`、`render` 等子 profile，还必须合并对应子 profile 的补充规则。

重点（按 ODK 对齐的 4 阶段主流程）：

- Define：交互结束判定、合法延迟状态、异常豁免、维测合同、热路径预算；交互、无障碍、国际化、多形态适配
- Specify：规则定义（行为/边界/异常/恢复）、对象覆盖边界、验证映射；当前特性和同 FuncID 前置存量 Feat 必须完成长期归档
- Design：复杂对象关系图、交互事件流程图、状态切换或恢复决策图；组件代码、渲染链路、设计约束；`design.md` 与 `spec.md` 必须交叉一致
- Plan：行为、交互和状态一致性；组件 API、渲染成本、可维护性；Task 与验证路径拆解；开发者可显式触发 Spec for Validation 旁路生成测试输入

## 基本信息

| 项 | 内容 |
|----|------|
| Profile ID | `arkui` |
| 适用对象 | ArkUI / ACE Engine / 声明式 UI 框架、组件、渲染、状态驱动交互 |
| 推荐复杂度 | 标准起步；涉及 Public API、渲染链路、跨设备、多仓或热路径时升级到复杂/关键 |
| 触发条件 | 命中 `repos` 仓名或 `components_ng` 等 ArkUI 路径 |
| 不适用场景 | 与 ArkUI 行为、组件、渲染、API 或交互无关的一般业务逻辑 |

## 阶段补充约束

| 阶段 | 补充要求 |
|------|----------|
| Define | Owner 明确 FuncID/FeatID、Profile/Lineage、影响范围、验证适用性和基线审批；未确认时 Blocked |
| Specify | 先做 FeatID 连续性预检和存量特性归档读取；P0/P1 AC 必须映射验证 |
| Design | `design.md` 与 `spec.md` 交叉一致；API、模块边界、验证映射、热路径预算和 SpecTest 映射不能漂移 |
| Plan | Task 级验证闭环；命中 SpecTest 时记录 case/suite/命令/报告；最终交付前安排长期 `specs/` 回灌 |
| Spec for Validation（旁路） | spec/design Approved 后可生成 `spec-for-validation.md`；完整保留每个 US 的角色/目标/价值和所属 AC，投影对外规则/API/兼容性，再按 ArkUI 模板分别展开 2D、NFR、2C 细项和测试侧验证点；不含内部实现及开发自验证信息；测试输入交付前需双 Owner 审批 |

## 专项检查清单

- [ ] Define gate 未通过前，不创建 `spec.md`、`design.md` 或后续 gate 证据。
- [ ] FuncID、FeatID、功能域名称、影响范围、Profile/Lineage、验证适用性必须有 Owner 输入确认。
- [ ] 存量 FeatID 连续性和历史 spec/design 读取记录写入 `evidence/checks/check-spec.md`。
- [ ] `design.md` 中关键代码路径、API、类名和行为结论有源码核验路径和行号。
- [ ] 适用的 Host Preview / SpecTest / 设备补验路径已映射到 AC 和 Task。
- [ ] 不适用项有 N/A 理由和替代验证方式。
- [ ] 最终交付前 `.codespec` 短期产物、长期 `specs`、manifest、registry 和 review 证据状态一致。
- [ ] 触发 Spec for Validation 时，`spec-for-validation.md` 的来源 hash、AC 集合、2C/2D 和验证点通过 `ohos-sdd spec-for-validation check`。

## ArkUI 最小加载路径

默认只读下面这些：

1. 当前 `profile.md`
2. 命中的子 profile
3. 仅在需要更多背景、验证路径或 gate 执行细则时，再读 ArkUI analysis 文档

路径说明：

- 源仓路径：`openharmony/context-engine/analysis/arkui/`
- 运行时路径：`{{ASSET_ROOT}}/analysis/arkui/`

按任务的最小上下文参考：

- 新需求/澄清：`profile.md` -> `analysis/arkui/asset-model.md`
- 写 `spec.md`：`profile.md` -> 命中的子 profile
- 写 `design.md` / `execution-plan.md`：`profile.md` -> 命中的子 profile -> `analysis/arkui/validation-playbook.md`
- 执行 ArkUI gate 或写 `evidence/checks/*`：`profile.md` -> `analysis/arkui/gate-playbook.md`
- 做验证/评审：`profile.md` -> `analysis/arkui/validation-playbook.md`；需要核对 gate 证据时再读 `analysis/arkui/gate-playbook.md`
- 生成测试输入：`profile.md` -> `profiles/arkui/templates/spec-for-validation.md`（ArkUI override）-> `analysis/arkui/spec-for-validation.md`；公共 `templates/spec-for-validation.md` 仅作为未覆盖 Profile 的默认格式

## ArkUI-SDD 执行资产

ArkUI 变更的流程实例写入 `.codespec/`，长期功能规格沉淀到 `specs/`。详细资产关系见 `analysis/arkui/asset-model.md`（源仓对应 `openharmony/context-engine/analysis/arkui/asset-model.md`）。

最低映射关系：

| 资产 | 目录 | 用途 |
|---|---|---|
| 流程实例 | `.codespec/changes/*` | 单次需求从 Define 到 Plan 的主流程产物，加上后续实现与验证证据 |
| 长期功能规格 | `specs/<func-domain>/Feat-XX-*-spec.md` | FuncID/FeatID 的长期行为事实 |
| 长期功能设计 | `specs/<func-domain>/design.md` | 功能域统一设计、架构约束和 ADR |
| Host Preview 用例 | `examples/SpecTest/entry/src/main/ets/spec_cases/*` | 可 Inspector 断言的 Host Preview 规格测试 |

`.codespec/changes/*/manifest.md` 建议记录以下 ArkUI 增强字段：

- `func_id`: 功能域 ID，例如 `04-03-01`
- `feat_id`: 功能域内特性编号，例如 `Feat-03`
- `profile`: `arkui`（主 profile，不含斜杠）
- `subprofiles`: 实际命中的子 profile 列表（block seq 格式，每项一行 `- <name>`，如 `- component` 或 `- capi` + `- sdk-api`）
- `lineage`: `new`、`legacy`、`migrated`、`new-on-legacy` 或 `bugfix-on-feature`
- `long_term_spec_path`: 对应长期 spec 路径
- `long_term_design_path`: 对应长期 design 路径
- `spectest_feature_path`: 如适用，对应 SpecTest feature 用例目录

## 信息检索与 Gate 执行细则

Base profile 只保留默认必读摘要和 gate 插槽定义。

- 不确定该读哪些 ArkUI 上下文、或需要检索策略时，读取 `analysis/arkui/context-loading.md`（源仓对应 `openharmony/context-engine/analysis/arkui/context-loading.md`）。
- 实际执行 ArkUI gate、编写 `evidence/checks/*` 或 review gate 证据时，读取 `analysis/arkui/gate-playbook.md`（源仓对应 `openharmony/context-engine/analysis/arkui/gate-playbook.md`）。
- 默认不要为了“更全面”读取全部 analysis。

## Profile Gate 定义

本 Profile 定义以下追加 Gate，按阶段和执行位置组织。此表只定义 gate-checklist 的机械插槽、入口/出口位置和通过标准摘要；逐项执行规则、Blocked 条件和证据格式见 `analysis/arkui/gate-playbook.md`。

### Define 阶段

| Gate ID | 位置 | 门禁内容 | 通过标准 |
|---------|------|----------|----------|
| arkui-define-entry | 入口 | 功能树、Lineage、Profile 定位与影响面矩阵 | FuncID/FeatID 唯一，`.codespec` 目录、profile、lineage、`.codespec/registry.md` 与 `specs/index.md` 注册完整；前端/API/依赖/跨平台/热路径/无障碍/国际化等维度已评估 |
| arkui-define-exit | 出口 | 基线审批 + 信息来源记录 | Owner 已批准基线；gate 证据包含检索手段、来源链路、源码核验 path:line 和确认来源；未核验项不得标记为通过 |

### Specify 阶段

| Gate ID | 位置 | 门禁内容 | 通过标准 |
|---------|------|----------|----------|
| arkui-specify-entry | 入口 | 存量特性归档与 FeatID 连续性 | FeatID 编号连续，同 FuncID 下历史 Feat 已注册并归档，存量 spec 已读取作为规格说明参考 |
| arkui-specify-exit | 出口 | 短期规格产物完整 + 信息来源记录 + 短期/长期分离 | `.codespec/changes/` 下 spec.md 已创建且内容完整；长期 `specs/` 下当前 Feat 文件状态正确；P0/P1 AC 已映射验证 |

### Design 阶段

| Gate ID | 位置 | 门禁内容 | 通过标准 |
|---------|------|----------|----------|
| arkui-design-entry | 入口 | 设计约束、对象关系和交叉一致性 | design.md 已建立对象关系、渲染链路、设计约束；与 spec.md 交叉一致；关键来源已核验 |
| arkui-design-exit | 出口 | 设计基线通过 | `evidence/checks/check-design.md` 记录交叉一致性、来源链路和设计结论；未核验项不得标记为通过 |

### Plan 阶段

| Gate ID | 位置 | 门禁内容 | 通过标准 |
|---------|------|----------|----------|
| arkui-plan | 入口/出口 | Task 级 Host TDD 闭环 + SpecTest Host Preview 闭环 + 长期资产回灌计划 | 每个 Task 有 fresh RED/GREEN/验证证据；适用范围内 `run_feature.sh` 目标范围 `failed_cases=0` 且日志无关键错误；`evidence/checks/check-execution-plan.md` 记录长期归档迁移计划、设备最小矩阵与差异摘要 |

## SpecTest Host Preview 与 Build/Test 入口

SpecTest 适用性、常用命令、Build/Test 入口不再内嵌在 base profile。需要这些信息时，读取 `analysis/arkui/validation-playbook.md`（源仓对应 `openharmony/context-engine/analysis/arkui/validation-playbook.md`）。

## Spec for Validation 旁路

仅 ArkUI Profile 支持。`spec.md`、`design.md` Approved 后，开发者执行：

```bash
ohos-sdd spec-for-validation generate .codespec/changes/<id>
```

生成 Agent 按 `analysis/arkui/spec-for-validation.md` 完成 AC 验证点以及 2D、NFR、2C 的逐项分析，只允许编辑 `TEST-ANALYSIS` 区域，不得改写 CLI 生成的来源投影，再执行 `ohos-sdd spec-for-validation check`。具体测试用例仍写入 `test-spec.md` 或测试团队用例系统。

## Profile 选择

ArkUI base profile 适用于所有 ArkUI / ACE Engine 变更。若能进一步判定模块类型，使用子 profile：

| 子 profile | manifest.subprofiles 值 | 适用场景 |
|-----------|--------------------------|---------|
| component | `component` | NG 组件 pattern、组件交互、组件状态机 |
| capi | `capi` | C API / NDK 接口 |
| sdk-api | `sdk-api` | ArkTS SDK API、`.d.ets`、Modifier |
| render | `render` | 渲染、布局算法、绘制管线 |

当需求跨多个 ArkUI 模块类型时，`manifest.profile` 填 `arkui`，`manifest.subprofiles` 列出全部命中子 profile；`execution-plan.md` 和 Task Card 必须在 Task 维度记录实际命中的子 profile 与验证命令。
