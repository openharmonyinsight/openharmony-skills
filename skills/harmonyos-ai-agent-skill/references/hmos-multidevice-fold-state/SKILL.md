---
name: hmos-multidevice-fold-state
description: Validate and route HarmonyOS foldable-device adaptation tasks (including bi-fold, multi-fold, and special-ratio form factors) through a declarative scene and resource index. Use when the task involves FoldStatus, hover layouts, crease avoidance, fold continuity, multi-fold state mapping (for example F/M/G), special-ratio inner/outer screen adaptation, or remediation of existing foldable-page issues.
---

# 设备折展状态适配

## 技能定义

| 字段 | 内容 |
| --- | --- |
| `skill_id` | `device-fold-state` |
| `skill_name` | `设备折展状态适配` |
| `one_line_purpose` | 为折叠屏多形态设备提供悬停适配、折痕避让、开合连续性的统一基线。 |
| `device_scope` | `foldable / multi-fold / special-ratio-foldable` |
| `problem_scope` | `FoldStatus、悬停态、折痕避让、开合连续性、多段折叠形态映射（如 F/M/G）、内外屏比例差异适配、折展问题修复` |
| `not_in_scope` | `普通手机或平板的常规响应式布局、与折展无关的纯视觉调整` |
| `primary_outputs` | `primary_scene`、`device_constraints`、`implementation_notes`、`fix_plan`、`verification_matrix` |

## 核心约束

- 先识别设备形态和当前折叠状态，再决定布局与交互策略。
- 悬停态方向决策遵循“场景结构约束 > foldStatus 或 foldDisplayMode > 折痕几何推断”。
- 对“固定折痕轴”设备（如固定竖折痕），允许用设备约束覆盖单次折痕矩形几何判定；当语义与几何冲突时，优先保证“上展示下操作”等场景语义。
- 同一“折痕轴周期”内只锁定一次方向；当 `foldStatus / foldDisplayMode / 折痕轴` 发生变化时，必须先清锁再重选方向，避免沿用旧方向。
- 折展适配不得改写原有业务显示状态机，不得在折展计算函数里强制写入业务显示态。
- 悬停态与展开态应复用同一套显示判定条件，只调整内容落在哪个分屏。
- 关键内容和核心交互不得落在折痕区域。
- 折痕分屏必须先统一到同一坐标系（全局/页面二选一），再计算分界；禁止直接混用不同坐标系。
- 折痕定位应优先使用“折痕上边界/下边界”作为分区边界；`16 vp / 40 vp` 仅用于内容安全间距，不作为分区锚点。
- 开合后不得引入额外操作步骤，不得出现滚动偏移、输入丢失、图像模糊或播放进度漂移。
- 未给出运行验证证据前，不得判定折展适配完成。

## 三块主线结构

模块主线固定为三块，先按主线归类，再进入场景细分：

| 主线 | 官方条目 | 主场景 | 主资源 |
| --- | --- | --- | --- |
| 悬停适配 | 4.3 | `FOLD-02` | `RSC_FOLD_03` |
| 折痕避让 | 4.4 | `FOLD-03` | `RSC_FOLD_05` |
| 开合连续性 | 4.1 | `FOLD-07` | `RSC_FOLD_17` |

说明：
- `FOLD-01`、`FOLD-04`、`FOLD-05`、`FOLD-06` 属于扩展场景，用于状态入口、多形态/特殊比例和问题修复。
- 三块主线的总览入口是 `RSC_FOLD_16`（`./reference/fold_adaptation_four_blocks.md`）。

## 阶段标签

| 标签 | 阶段 | 当前模块关注点 |
| --- | --- | --- |
| `REQ` | 需求分析设计 | 设备形态、折展状态、方向策略、显示职责 |
| `DEV` | 开发 | 状态监听、分屏布局、折痕计算、开合连续性、生命周期回收 |
| `FIX` | 问题修复 | 折展问题修复、方向偏差、状态不同步、折痕跨越、连续性断档 |
| `VAL` | 功能验证 | foldStatus 证据、方向证据、折痕避让截图、连续性行为回归 |

## 统一输出字段

- 路由字段：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`resources_used`
- `REQ`：`device_constraints`、`capability_boundary`、`acceptance_focus`
- `DEV`：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- `FIX`：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- `VAL`：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`

## 字段释义

- `device_constraints`：指由设备折叠形态、折展状态、折痕区域和宽折叠特性带来的适配硬约束。在 `device-fold-state` 中，通常是需要支持哪些 fold status、折痕区域禁止承载哪些内容、悬停态是否允许重选方向。
- `capability_boundary`：指当前折展方案适用于哪些设备形态和状态，哪些设备或状态不支持，或只能降级处理。
- `acceptance_focus`：指需求阶段验收时必须确认的折展行为、方向结果、折痕避让和状态切换表现。
- scene 中 `deliverables.REQ` 出现 `device_constraints`，表示“该折展场景命中后，需求分析必须先给出设备约束结论”，不是在场景层重新发明字段。

## AI 检索要求

- 涉及当前是折叠态、展开态还是半折叠态时，优先命中 `FOLD-01`。
- 涉及悬停态上下分屏、上展示下操作时，优先命中 `FOLD-02`。
- 涉及内容跨折痕、点击区落在折痕上时，优先命中 `FOLD-03`。
- 涉及“避让区偏下/偏上、分界线不在中线、状态栏导致整体偏移”时，优先联合命中 `FOLD-03` + `FOLD-06`。
- 涉及折展后步骤增加、滚动偏移、输入丢失、图片模糊、播放进度不一致时，优先命中 `FOLD-07`。
- 涉及多段折叠形态映射（如 F/M/G）或内外屏比例差异适配时，优先命中 `FOLD-04` 或 `FOLD-05`。
- 涉及折展行为偏差且需要通用修复路径时，优先命中 `FOLD-06`。
- 涉及“悬停态黑屏/仅剩 Blank、内容被整屏折痕吞掉”时，优先联合命中 `FOLD-02` + `FOLD-03` + `FOLD-06`。
- 涉及“物理竖折痕但 `creaseRect` 显示为横向宽条（如 `2232x128`）”时，优先联合命中 `FOLD-02` + `FOLD-06`，并启用固定折痕轴判定策略。

## F/M/G 简介

- `F`：可视区较小的折叠形态（常用于保留核心内容）。
- `M`：中间过渡形态（布局通常介于紧凑与扩展之间）。
- `G`：可视区较大的展开形态（适合分栏或提升信息密度）。
- 说明：`F/M/G` 是通用语义标签，最终布局仍以实时窗口尺寸与断点为准。

## Workflow

### Steps

1. 根据 `intent_signals / applies_when` 命中主场景（`primary_scene`）和辅场景（`secondary_scenes`）。
2. 按场景读取 `resource_refs` 与 `skill_to_path`，优先加载 `P0` 官方路径。
3. 依据“统一输出字段”生成阶段化结果（REQ/DEV/FIX/VAL）。
4. 按“阶段输出契约”补齐必填字段并给出验证证据要求。

### Output
- 路由字段：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`resources_used`。
- 阶段字段：按 `REQ/DEV/FIX/VAL` 契约输出对应结构化结果。

## Checklist

- [ ] 已命中至少一个 `FOLD-*` 场景，并说明命中依据。
- [ ] 已优先使用 `P0` 官方资源，`P1` 模板资源仅用于加速落地。
- [ ] 已输出当前阶段的所有必填字段（见“阶段输出契约”）。
- [ ] 已包含折展验证证据要求与剩余风险声明。

## 场景索引

#### `FOLD-01` 折叠状态检测与状态切换响应

```yaml
scene_id: FOLD-01
scene_name: 折叠状态检测与状态切换响应
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - FoldStatus
  - foldStatusChange
  - 展开态
  - 折叠态
  - 半折叠态
applies_when:
  - 需要识别折叠态、展开态、半折叠态
  - 当前问题表现为状态变化后界面未更新
not_applies_when:
  - 问题只涉及常规平板布局，没有折展状态输入
decisions:
  - 选择状态来源、监听点和刷新入口
  - 确定状态变化后的布局刷新和兜底行为
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_FOLD_01
  - RSC_FOLD_02
skill_to_path:
  - skill: 折叠状态检测
    path: ./reference/fold_status_detection.md
```

#### `FOLD-02` 悬停态上下分屏与交互布局

```yaml
scene_id: FOLD-02
scene_name: 悬停态上下分屏与交互布局
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - 悬停态
  - HALF_FOLDED
  - 上下分屏
  - 上展示下操作
applies_when:
  - 页面在悬停态需要将展示区和操作区拆到上下分屏
  - 当前问题表现为悬停态布局职责混乱
not_applies_when:
  - 页面没有悬停态交互设计
decisions:
  - 明确上半屏和下半屏的职责分配
  - 明确方向锁定策略和退出悬停后的恢复策略
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_FOLD_03
  - RSC_FOLD_04
skill_to_path:
  - skill: 悬停态上下分屏与交互
    path: ./reference/hover_state_interaction.md
```

#### `FOLD-03` 折痕区域避让

```yaml
scene_id: FOLD-03
scene_name: 折痕区域避让
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - 折痕
  - CreaseRegion
  - getFoldCreaseRegion
  - 内容被劈开
  - 避让区偏下
  - 分界线不在中线
  - 状态栏偏移
applies_when:
  - 关键内容或交互可能落在折痕区域
  - 状态变化后需要重新计算折痕避让范围
not_applies_when:
  - 设备没有折痕区域输入
decisions:
  - 确定折痕区域获取方式和重算时机
  - 决定哪些内容必须远离折痕
  - 先映射折痕矩形到页面坐标，再计算分界线，禁止未映射直接参与布局
  - 上分区下边界锚定折痕上边界，下分区上边界锚定折痕下边界
  - `16 vp / 40 vp` 仅作为分区内部内容安全间距，不替代边界定位
  - 若页面根节点有 `globalPosition` 偏移，必须在同单位下扣减后再分区
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_FOLD_05
  - RSC_FOLD_06
skill_to_path:
  - skill: 折痕区域避让
    path: ./reference/crease_avoidance.md
```

#### `FOLD-07` 开合连续性保障

```yaml
scene_id: FOLD-07
scene_name: 开合连续性保障
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - 开合连续性
  - 操作步骤增加
  - 页面滚动位置偏移
  - 输入内容丢失
  - 图片模糊
  - 播放进度不一致
applies_when:
  - 折叠/展开后出现状态断档，导致操作路径变长或体验降级
  - 需要保证滚动、输入、图像和媒体时间轴在折展后的连续性
not_applies_when:
  - 问题仅为静态布局差异，不涉及状态连续
decisions:
  - 明确哪些状态必须跨折展保持（滚动锚点、输入草稿、媒体时间轴）
  - 明确恢复链路触发时机，禁止基于过期视口恢复
  - 明确降级策略回收点，避免质量衰减累积
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_FOLD_17
  - RSC_FOLD_01
skill_to_path:
  - skill: 开合连续性
    path: ./reference/fold_continuity.md
  - skill: 折叠状态检测
    path: ./reference/fold_status_detection.md
```

#### `FOLD-04` 多段折叠形态状态适配

```yaml
scene_id: FOLD-04
scene_name: 多段折叠形态状态适配
phase_tags: [REQ, DEV, FIX, VAL]
priority: P1
intent_signals:
  - 多段折叠
  - 多形态折展
  - F/M/G
  - 形态映射
applies_when:
  - 目标设备存在多段折叠形态差异（可映射为 F/M/G 等）
  - 当前问题表现为某一形态下方向或结构判断错误
not_applies_when:
  - 设备仅存在单一折展形态，无需形态映射
decisions:
  - 形态映射基线：可将不同设备形态抽象为“小可视区/中间态/大可视区”等统一语义（如 F/M/G）
  - 确定不同折叠组合下的布局和方向策略
  - 形态标签只作为语义入口，真实布局空间仍以运行时窗口尺寸和断点判定
  - 明确“大可视区形态”下的方向和信息密度策略
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_FOLD_07
  - RSC_FOLD_01
skill_to_path:
  - skill: 多段折叠形态状态适配
    path: ./reference/multi_fold_states.md
  - skill: 折叠状态检测
    path: ./reference/fold_status_detection.md
```

#### `FOLD-05` 特殊比例折叠屏适配（内外屏差异）

```yaml
scene_id: FOLD-05
scene_name: 特殊比例折叠屏适配（内外屏差异）
phase_tags: [REQ, DEV, FIX, VAL]
priority: P1
intent_signals:
  - 特殊比例折叠屏
  - 1:1 外屏
  - 16:10 内屏
  - 内外屏比例差异
applies_when:
  - 目标设备存在明显的外屏和内屏比例差异
  - 需要处理宽折叠内容密度或导航形式变化
not_applies_when:
  - 设备不具备宽折叠屏幕特征
decisions:
  - 定义外屏与内屏的布局差异
  - 决定哪些内容在外屏裁剪、隐藏或延后展示
deliverables:
  REQ:
    - device_constraints
    - capability_boundary
    - acceptance_focus
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_FOLD_08
  - RSC_FOLD_03
  - RSC_FOLD_09
  - RSC_FOLD_10
  - RSC_FOLD_11
  - RSC_FOLD_12
skill_to_path:
  - skill: 特殊比例折叠屏适配
    path: ./reference/special_form_factor_foldable_adaptation.md
  - skill: 悬停态上下分屏与交互
    path: ./reference/hover_state_interaction.md
```

#### `FOLD-06` 折展问题通用修复路径

```yaml
scene_id: FOLD-06
scene_name: 折展问题通用修复路径
phase_tags: [DEV, FIX, VAL]
priority: P0
intent_signals:
  - 折展问题修复
  - 悬停态错乱
  - 方向偏差
  - 折痕跨越
  - 连续性断档
  - 生命周期回收
applies_when:
  - 已有页面在折展态出现行为偏差，需要修复但不重构页面架构
  - 需要按“问题描述-根因分析-通用修复方案”输出修复路径
not_applies_when:
  - 当前任务是新页面从零设计
decisions:
  - 先归类问题类型，再选对应通用修复模板，避免按页面类型定制
  - 修复顺序统一为：监听入口 -> 几何/状态 -> 布局/交互 -> 生命周期回收 -> 回归验证
  - 方向与分界线优先基于真实折痕几何，不使用经验比例硬编码
  - 出现“避让区偏下/偏上”时，先排查坐标系混用与“中线 + 固定偏移”策略，再排查布局容器约束
  - 禁止在折展修复中改写业务状态机语义
deliverables:
  DEV:
    - code_touchpoints
    - reuse_resources
    - implementation_notes
    - integration_risks
  FIX:
    - problem_profile
    - root_cause_hypothesis
    - fix_plan
    - regression_watchlist
  VAL:
    - verification_matrix
    - evidence_requirements
    - pass_criteria
    - residual_risks
resource_refs:
  - RSC_FOLD_01
  - RSC_FOLD_03
  - RSC_FOLD_05
  - RSC_FOLD_13
skill_to_path:
  - skill: 折叠状态检测
    path: ./reference/fold_status_detection.md
  - skill: 悬停态上下分屏与交互
    path: ./reference/hover_state_interaction.md
  - skill: 折痕区域避让
    path: ./reference/crease_avoidance.md
  - skill: 折展问题修复场景库
    path: ./reference/bug-fix-cases.md
```

## 资源索引

完整资源卡片已下沉至 [`./reference/resource-index.md`](./reference/resource-index.md)，主文件仅保留检索入口与输出契约。

使用顺序：
- 优先读取 `P0` 官方路径作为主方案。
- `P1` 工程模板资源仅作补充，不能替代官方基线。

资源分组：
- 官方主路径：`RSC_FOLD_01`、`RSC_FOLD_03`、`RSC_FOLD_05`、`RSC_FOLD_07`、`RSC_FOLD_08`、`RSC_FOLD_16`、`RSC_FOLD_17`
- 官方 API 模板与问题修复资源：`RSC_FOLD_02`、`RSC_FOLD_04`、`RSC_FOLD_06`、`RSC_FOLD_09` 到 `RSC_FOLD_13`

## 阶段输出契约

### `REQ`

- 必须输出：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`
- 必须输出：`device_constraints`、`capability_boundary`、`acceptance_focus`
- 额外要求：明确当前设备形态、当前 fold 状态、方向策略和上下分屏职责

### `DEV`

- 必须输出：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- 额外要求：明确状态监听入口、折痕计算入口、分屏组件落点和生命周期回收点

### `FIX`

- 必须输出：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- 额外要求：明确问题是状态监听缺失、方向锁定错误、折痕映射错误还是旧状态机被破坏

### `VAL`

- 必须输出：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`
- 额外要求：至少包含 `foldStatus` 结果、方向信息、窗口几何或截图证据，并验证原有显示逻辑未被破坏
