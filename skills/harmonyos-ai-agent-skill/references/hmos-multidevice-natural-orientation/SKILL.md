---
name: hmos-multidevice-natural-orientation
description: Handle HarmonyOS device natural orientation, screen rotation, and window orientation adaptation across multiple device form factors. Use when the task involves setPreferredOrientation, rotation, orientation, natural orientation, tri-fold G-state, follow_desktop, video landscape/portrait switching, short video adaptive rotation, or multi-device orientation strategy.
---

# 设备自然方向与屏幕旋转适配

## 技能定义

| 字段 | 内容 |
| --- | --- |
| `skill_id` | `device-natural-orientation` |
| `skill_name` | `设备自然方向适配` |
| `one_line_purpose` | 为自然竖屏、自然横屏和特殊折叠态提供统一方向判定与更新策略。 |
| `device_scope` | `phone / tablet / pc / 2in1 / tri-fold / foldable` |
| `problem_scope` | `屏幕旋转(rotation)、屏幕方向(display orientation)、窗口方向(window orientation)、自然方向差异、传感器旋转检测、多设备方向映射、三折叠 G 态方向、视频横竖屏切换、短视频自适应旋转` |
| `not_in_scope` | `与方向无关的纯布局问题、web视觉翻转的场景、折叠屏折痕避让（属 device-avoid-areas）、交互输入方式适配（属 interaction-methods）、硬件能力检测（属 hardware-access）` |
| `primary_outputs` | `primary_scene, device_constraints, code_touchpoints, implementation_notes, fix_plan, verification_matrix` |

## 核心约束

1. 先区分屏幕旋转(rotation)、屏幕方向(display orientation)和窗口方向(window orientation)，三者含义和用途不同，不可混用
2. 控制应用显示方向必须通过窗口侧 `setPreferredOrientation()` 设置旋转策略，不能通过屏幕属性设置
3. 涉及多设备适配时，必须明确目标设备的自然方向类型：自然竖屏(rotation=0 为 PORTRAIT)、自然横屏(rotation=0 为 LANDSCAPE)、三折叠 G 态(rotation=0 为 LANDSCAPE_INVERTED)
4. 分屏/悬浮窗/自由窗口场景下 `setPreferredOrientation()` 静默无效，应通过响应式布局适配窗口尺寸
5. 折叠屏设备 `deviceInfo.deviceType` 返回 `'phone'`，不能通过 deviceType 区分折叠屏与直板机，需使用 `display.isFoldable()` + 断点系统
6. 输出方案必须说明方向变化后的 UI 更新逻辑和生命周期管理（保存/恢复方向）

## 三块主线结构

模块主线固定为三块，先按主线归类，再进入场景细分：

| 主线 | 主场景 | 主资源 |
| --- | --- | --- |
| 检测监听 | `ORIENT-01` | `RSC_ORIENT_03` |
| 适配策略 | `ORIENT-02`、`ORIENT-03` | `RSC_ORIENT_02`、`RSC_ORIENT_04` |
| 问题修复 | `ORIENT-04` | `RSC_ORIENT_05` |

说明：
- `RSC_ORIENT_01`（`orientation_concepts.md`）为基础概念资源，非独立场景，由各场景按需引用。
- 三块主线覆盖了方向适配的完整链路：感知变化 → 策略适配 → 问题修复。

## 阶段标签

| 标签 | 阶段 | 当前模块关注点 |
| --- | --- | --- |
| `REQ` | 需求分析设计 | 设备方向差异、自然方向类型、旋转能力边界、验收口径 |
| `DEV` | 开发 | 代码落点、旋转策略选择、断点判断、资源绑定 |
| `FIX` | 问题修复 | 根因分析（概念混淆/检测错误/映射错误）、最小改动路径、回归点 |
| `VAL` | 功能验证 | 设备覆盖矩阵、方向切换证据、通过标准 |

## 统一输出字段

- 路由字段：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`resources_used`
- `REQ`：`device_constraints`、`capability_boundary`、`acceptance_focus`
- `DEV`：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- `FIX`：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- `VAL`：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`

## 字段释义

- `device_constraints`：指由自然竖屏、自然横屏、rotation 语义、窗口方向和特殊折叠态带来的适配硬约束。在 `device-natural-orientation` 中，通常是需要支持哪些自然方向类型、rotation 如何解释、哪些场景禁止混用屏幕旋转和窗口方向概念。
- `capability_boundary`：指当前方向策略在哪些设备形态和方向模式下成立，哪些场景需要单独降级或绕开。
- `acceptance_focus`：指需求阶段验收时必须确认的方向判定结果、切换一致性和布局更新触发条件。
- scene 中 `deliverables.REQ` 出现 `device_constraints`，表示"该方向场景命中后，需求分析必须先给出设备约束结论"，不是在场景层重新发明字段。

## AI 检索要求

- 涉及旋转角度获取、方向变化监听、传感器检测、调试旋转问题时，优先命中 `ORIENT-01`。
- 涉及多设备方向适配、一多策略、折叠屏方向、三折叠 G 态、module.json5 方向配置、断点判断时，优先命中 `ORIENT-02`。
- 涉及视频横竖屏切换、短视频自适应旋转、adaptive_video 三方库、屏幕锁定时，优先命中 `ORIENT-03`。
- 涉及方向适配 Bug（折叠屏强制竖屏、Tabs 方向锁定、分屏旋转失效、全屏退出未恢复、开合闪烁）时，优先命中 `ORIENT-04`。
- 涉及 rotation/orientation 概念区分、自然方向定义、18 种旋转策略等概念性问题时，先加载 `RSC_ORIENT_01`（`orientation_concepts.md`）作为前置知识。

## Workflow

### Steps

1. 根据 `intent_signals / applies_when` 命中主场景（`primary_scene`）和辅场景（`secondary_scenes`）。
2. 按场景读取 `resource_refs` 与 `skill_to_path`，优先加载 `P0` 官方路径。
3. 概念性问题或修复时概念不清的场景，补加载 `RSC_ORIENT_01`（`orientation_concepts.md`）。
4. 依据"统一输出字段"生成阶段化结果（REQ/DEV/FIX/VAL）。
5. 按"阶段输出契约"补齐必填字段并给出验证证据要求。

### Output

- 路由字段：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`resources_used`。
- 阶段字段：按 `REQ/DEV/FIX/VAL` 契约输出对应结构化结果。

## Checklist

- [ ] 已命中至少一个 `ORIENT-*` 场景，并说明命中依据。
- [ ] 已优先使用 `P0` 官方资源，`P1` 模板资源仅用于加速落地。
- [ ] 概念性问题或根因分析涉及概念混淆时，已加载 `RSC_ORIENT_01`。
- [ ] 已输出当前阶段的所有必填字段（见"阶段输出契约"）。
- [ ] 已包含方向验证证据要求与剩余风险声明。

## 场景索引

#### `ORIENT-01` 屏幕旋转检测与方向变化监听

```yaml
scene_id: ORIENT-01
scene_name: 屏幕旋转检测与方向变化监听
phase_tags: [DEV, FIX, VAL]
priority: P0
intent_signals:
  - "如何获取旋转角度"
  - "传感器检测方向"
  - "重力传感器 atan2"
  - "监听屏幕旋转"
  - "windowSizeChange"
  - "display.on('change')"
  - "hdc 调试旋转"
  - "获取设备握持角度"
  - "旋转180° 不触发"
applies_when:
  - 需要获取连续旋转角度而非离散方向
  - 需要监听方向变化并响应
  - 需要调试旋转相关问题
  - 需要实现自定义旋转检测逻辑
not_applies_when:
  - 只需使用系统旋转策略，不需要自定义检测
  - 概念不清，需先理解基础概念
decisions:
  - 优先使用系统旋转策略（setPreferredOrientation），仅当系统策略不满足时才自定义传感器检测
  - display.on('change') 回调中必须通过 Display 实例获取信息，不能通过 Window 实例（有时序问题）
  - windowSizeChange 在旋转 180° 时不触发，需结合 display.on('change') 补充
  - 传感器数据需防抖和平滑处理，回调必须使用命名引用以便取消
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
  VAL:
    - verification_matrix
    - evidence_requirements
resource_refs:
  - RSC_ORIENT_03
  - RSC_ORIENT_08
  - RSC_ORIENT_06
  - RSC_ORIENT_07
skill_to_path:
  - skill: 旋转检测与方向监听
    path: ./references/rotation_detection.md
```

#### `ORIENT-02` 多设备方向适配（一多策略）

```yaml
scene_id: ORIENT-02
scene_name: 多设备方向适配（一多策略）
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - "多设备方向适配"
  - "折叠屏方向"
  - "三折叠 G 态"
  - "follow_desktop"
  - "348vp 阈值"
  - "一多方向策略"
  - "module.json5 orientation"
  - "AUTO_ROTATION_RESTRICTED"
  - "断点判断方向"
  - "WidthBreakpoint"
  - "折叠屏展开态方向"
applies_when:
  - 同一应用需适配多种设备形态的方向策略
  - 需要配置 module.json5 方向
  - 需要选择设备方向映射策略
  - 需要理解三折叠 G 态特殊性
not_applies_when:
  - 纯概念理解不涉及适配实现
  - 只涉及视频横竖屏切换（应命中 ORIENT-03）
  - 只涉及传感器检测不涉及多设备策略选择
decisions:
  - 一多推荐策略：module.json5 配置 follow_desktop + 运行时基于断点动态切换
  - 优先使用系统断点 API（WidthBreakpoint/HeightBreakpoint）判断设备形态，而非 deviceInfo.deviceType
  - 三折叠 G 态 rotation=0 对应 LANDSCAPE_INVERTED，窗口方向不能通过 rotation 推断
  - 折叠屏 deviceInfo.deviceType 返回 'phone'，需用 display.isFoldable() + 断点系统区分
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
  - RSC_ORIENT_02
  - RSC_ORIENT_01
  - RSC_ORIENT_09
  - RSC_ORIENT_10
skill_to_path:
  - skill: 多设备方向适配
    path: ./references/orientation_adaptation.md
  - skill: 方向概念与API速查
    path: ./references/orientation_concepts.md
```

#### `ORIENT-03` 视频应用横竖屏切换与自适应旋转

```yaml
scene_id: ORIENT-03
scene_name: 视频应用横竖屏切换与自适应旋转
phase_tags: [DEV, FIX, VAL]
priority: P0
intent_signals:
  - "视频横竖屏切换"
  - "USER_ROTATION_LANDSCAPE"
  - "短视频自适应旋转"
  - "adaptive_video"
  - "视频全屏"
  - "屏幕锁定"
  - "横竖屏性能优化"
  - "视频全屏退出恢复"
applies_when:
  - 视频播放页需要横竖屏切换
  - 短视频页面需要自适应旋转
  - 视频全屏退出后方向未恢复
  - 需要使用 adaptive_video 三方库
not_applies_when:
  - 非视频类应用的方向适配
  - 不涉及视频播放的方向问题
decisions:
  - 视频全屏用 USER_ROTATION_LANDSCAPE，退出时恢复之前保存的方向
  - 进入时保存方向、退出时恢复，必须成对调用 setPreferredOrientation()
  - 折叠屏展开态视频全屏时不旋转，直接调整播窗大小
  - Navigation 场景用 onShown/onHidden 处理方向切换
  - Tabs 场景方向控制放 Tabs.onChange，不放子组件生命周期
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
resource_refs:
  - RSC_ORIENT_04
  - RSC_ORIENT_01
skill_to_path:
  - skill: 视频横竖屏切换
    path: ./references/video_rotation.md
```

#### `ORIENT-04` 方向适配问题修复

```yaml
scene_id: ORIENT-04
scene_name: 方向适配问题修复
phase_tags: [DEV, FIX, VAL]
priority: P0
intent_signals:
  - "方向锁定异常"
  - "折叠屏被强制竖屏"
  - "Tabs 方向 Bug"
  - "分屏旋转失效"
  - "全屏退出方向未恢复"
  - "折叠屏开合闪烁"
  - "方向适配Bug"
  - "Swiper 方向锁定"
  - "aboutToAppear 方向不恢复"
  - "Navigation 方向异常"
applies_when:
  - 遇到方向适配 Bug（强制竖屏、锁定失效、闪烁等）
  - 折叠屏展开态方向异常
  - Tabs/Swiper 方向锁定问题
  - 分屏/悬浮窗下旋转不生效
  - 折叠屏开合布局闪烁
not_applies_when:
  - 新需求设计，不涉及 Bug 修复
  - 纯概念理解，不涉及实际修复
decisions:
  - Bug 修复优先尊重开发者原有适配方式，在其方案基础上修复，不强制切换方案
  - 先归类问题类型（概念混淆/检测错误/映射错误），再选对应修复方案
  - 修复顺序统一为：监听入口 → 几何/状态 → 布局/交互 → 生命周期回收 → 回归验证
  - 概念不清时先加载 RSC_ORIENT_01 确认概念是否被混淆
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
  - RSC_ORIENT_05
  - RSC_ORIENT_02
  - RSC_ORIENT_01
skill_to_path:
  - skill: 方向适配问题修复场景库
    path: ./references/bug-fix-cases.md
  - skill: 多设备方向适配
    path: ./references/orientation_adaptation.md
```

## 资源索引

完整资源卡片已下沉至 [`./references/resource-index.md`](./references/resource-index.md)，主文件仅保留检索入口与输出契约。

使用顺序：
- 优先读取 `P0` 官方路径作为主方案。
- `P1` 工程模板资源仅作补充，不能替代官方基线。

资源分组：
- 基础概念：`RSC_ORIENT_01`
- 检测监听：`RSC_ORIENT_03`、`RSC_ORIENT_06`、`RSC_ORIENT_07`、`RSC_ORIENT_08`
- 适配策略：`RSC_ORIENT_02`、`RSC_ORIENT_04`、`RSC_ORIENT_09`、`RSC_ORIENT_10`
- 问题修复：`RSC_ORIENT_05`

## 阶段输出契约

### `REQ`

- 必须输出：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`
- 必须输出：`device_constraints`、`capability_boundary`、`acceptance_focus`
- 额外要求：明确当前设备形态、自然方向类型、旋转策略和方向适配目标

### `DEV`

- 必须输出：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- 额外要求：明确旋转策略选择理由、断点判断逻辑、生命周期管理（保存/恢复方向）

### `FIX`

- 必须输出：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- 额外要求：明确问题是概念混淆、检测错误还是映射错误；优先在原方案基础上修复

### `VAL`

- 必须输出：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`
- 额外要求：至少包含各设备形态的方向行为证据、hdc 日志（rotation/orientation 值），并验证方向恢复正确

## 方向速查

| 设备 | 自然方向 | rotation=0 含义 | 默认是否支持旋转 |
|------|---------|---------------|----------------|
| 直板手机 | 竖屏 | PORTRAIT | 否 |
| 折叠屏折叠态 | 竖屏 | PORTRAIT | 否 |
| 折叠屏展开态 | 竖屏 | PORTRAIT | 否（但桌面可旋转） |
| 三折叠 F/M 态 | 竖屏 | PORTRAIT | 否 |
| 三折叠 G 态 | 横屏 | LANDSCAPE_INVERTED | 是 |
| 平板 | 竖屏 | PORTRAIT | 是 |
| PC/2in1 | 横屏 | LANDSCAPE | 不支持旋转策略 |
