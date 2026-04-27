---
name: hmos-multidevice-avoid-areas
description: Handle HarmonyOS avoid-area adaptation through a declarative scene and resource index. Use when the task involves safe area expansion, status bar or navigation bar avoidance, notch or cutout handling, immersive full-screen layouts, or soft keyboard overlap handling.
---

# 设备避让区适配

## 技能定义

| 字段 | 内容 |
| --- | --- |
| `skill_id` | `device-avoid-areas` |
| `skill_name` | `设备避让区适配` |
| `one_line_purpose` | 为系统栏、挖孔区、软键盘和沉浸式布局提供统一避让策略。 |
| `device_scope` | `phone / tablet / 2in1 / tv` |
| `problem_scope` | `safe area、状态栏和导航栏避让、挖孔区、软键盘、沉浸式布局` |
| `not_in_scope` | `与系统区域无关的普通间距调整、纯业务交互逻辑` |
| `primary_outputs` | `primary_scene`、`device_constraints`、`implementation_notes`、`fix_plan`、`verification_matrix` |

## 核心约束

- 先明确要处理的是哪类避让区域，再决定使用动态检测、安全区扩展还是沉浸式方案。
- 不要硬编码系统栏、挖孔区或键盘尺寸，应优先使用 API 动态获取。
- 涉及沉浸式布局时，必须同时说明背景延伸策略和内容避让策略。
- 涉及软键盘时，必须说明弹出、收起和焦点变化三类时机的布局更新逻辑。
- 关键内容和核心点击区域不得放在挖孔区或不可交互区域。
- 未说明异常场景下的回退策略前，不得宣称避让方案完整。

## 阶段标签

| 标签 | 阶段 | 当前模块关注点 |
| --- | --- | --- |
| `REQ` | 需求分析设计 | 避让区域类型、背景与内容边界、沉浸式适配、安全区扩展 |
| `DEV` | 开发 | 动态获取避让区域API、padding设置、窗口设置、expandSafeArea安全区域设置 |
| `FIX` | 问题修复 | 内容被系统栏区域遮挡、软键盘拉起遮挡内容、沉浸式错位、刘海区/挖孔区内容遮挡或交互失效 |
| `VAL` | 功能验证 | 截图证据、系统区域变化证据、键盘开闭证据 |

## 统一输出字段

- 路由字段：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`resources_used`
- `REQ`：`device_constraints`、`capability_boundary`、`acceptance_focus`
- `DEV`：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- `FIX`：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- `VAL`：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`

## 字段释义

- `device_constraints`：指由状态栏、导航栏、挖孔区、软键盘和沉浸式窗口带来的适配硬约束。在 `device-avoid-areas` 中，通常是哪些系统区域会遮挡内容、背景是否允许延伸、哪些交互区绝不能落入不可点击区域。
- `capability_boundary`：指当前避让方案在哪些窗口模式、系统 UI 状态或设备类型下有效，哪些场景需要回退或额外处理。
- `acceptance_focus`：指需求阶段验收时必须重点确认的遮挡现象、键盘开闭行为和系统区域变化表现。
- scene 中 `deliverables.REQ` 出现 `device_constraints`，表示“该避让场景命中后，需求阶段必须先说明遮挡和边界约束”，不是对字段重复定义。

## AI 检索要求

- 涉及系统区域类型识别和动态获取时，优先命中 `AVOID-01`。
- 涉及背景或者图片延伸但内容仍在安全区内时，优先命中 `AVOID-02`。
- 涉及全屏页面、状态栏透明或沉浸式布局时，优先命中 `AVOID-03`。
- 涉及输入框被键盘遮挡或键盘开闭时页面跳动时，优先命中 `AVOID-04`。

## 场景索引

#### `AVOID-01` 避让区域识别与动态获取

```yaml
scene_id: AVOID-01
scene_name: 避让区域识别与动态获取
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - AvoidAreaType
  - TYPE_SYSTEM
  - TYPE_NAVIGATION_INDICATOR
  - TYPE_CUTOUT
  - TYPE_KEYBOARD
applies_when:
  - 需要动态获取系统栏、挖孔区或键盘区域
  - 当前问题表现为内容被系统区域遮挡
not_applies_when:
  - 只是普通布局间距问题
decisions:
  - 确定需要监听哪些避让区域
  - 决定使用 padding、margin、offset 还是结构切换
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
  - RSC_AVOID_01
  - RSC_AVOID_05
```

#### `AVOID-02` 安全区扩展与背景延伸

```yaml
scene_id: AVOID-02
scene_name: 安全区扩展与背景延伸
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - expandSafeArea
  - SafeAreaType
  - SafeAreaEdge
  - 背景延伸
applies_when:
  - 背景需要铺满系统区域，但内容仍需保持在安全区内
  - 需要明确顶部和底部内容边界
not_applies_when:
  - 页面需要完全沉浸式展示且不保留常规内容边界
decisions:
  - 确定哪些层允许越过安全区，哪些层必须避让
  - 决定安全区扩展后是否还要补额外内边距
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
  - RSC_AVOID_02
```

#### `AVOID-03` 沉浸式全屏布局

```yaml
scene_id: AVOID-03
scene_name: 沉浸式全屏布局
phase_tags: [REQ, DEV, FIX, VAL]
priority: P1
intent_signals:
  - setWindowLayoutFullScreen
  - 全屏
  - 沉浸式
  - 状态栏透明
  - 列表沉浸
applies_when:
  - 页面需要背景或媒体内容铺满边缘
  - 当前问题表现为全屏后内容与系统栏重叠
  - 列表/信息流场景需要上滑隐藏标题栏和导航栏
not_applies_when:
  - 页面保持普通安全区布局即可
decisions:
  - 明确背景延伸和内容避让的分层策略
  - 决定窗口级设置和页面级布局如何配合
  - 识别是否命中 best practice 场景, 命中时必须逐条对照
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
  - RSC_AVOID_03
  - RSC_AVOID_06
  - RSC_AVOID_05
```

#### `AVOID-04` 软键盘避让与输入区稳定性

```yaml
scene_id: AVOID-04
scene_name: 软键盘避让与输入区稳定性
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - keyboardAvoidMode
  - avoidAreaChange
  - 输入框被遮挡
  - 键盘弹出
applies_when:
  - 输入框、按钮或底部操作栏会被软键盘遮挡
  - 当前问题表现为键盘开闭导致内容跳动或错位
not_applies_when:
  - 页面没有输入交互
decisions:
  - 选择滚动、平移或重排哪种键盘避让方式
  - 决定键盘弹出、收起、焦点切换时的同步策略
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
  - RSC_AVOID_01
  - RSC_AVOID_04
  - RSC_AVOID_05
```

## 资源索引

#### `RSC_AVOID_01` 避让区域类型参考

```yaml
resource_id: RSC_AVOID_01
resource_type: reference
path: ./reference/avoid_area_types.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 识别系统栏、导航栏、挖孔区和键盘区域类型
  - 设计动态获取与监听策略
load_when:
  - 命中 AVOID-01 或 AVOID-04
avoid_when:
  - 当前不涉及系统区域和键盘区域
supports_scenes:
  - AVOID-01
  - AVOID-04
output_fields:
  - device_constraints
  - capability_boundary
  - implementation_notes
  - root_cause_hypothesis
  - verification_matrix
```

#### `RSC_AVOID_02` 安全区扩展参考

```yaml
resource_id: RSC_AVOID_02
resource_type: reference
path: ./reference/safe_area_api.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 定义安全区扩展和背景延伸的边界
  - 判断内容层与背景层的职责划分
load_when:
  - 命中 AVOID-02
avoid_when:
  - 页面不使用安全区扩展
supports_scenes:
  - AVOID-02
output_fields:
  - device_constraints
  - capability_boundary
  - implementation_notes
  - fix_plan
  - pass_criteria
```

#### `RSC_AVOID_03` 沉浸式布局参考

```yaml
resource_id: RSC_AVOID_03
resource_type: reference
path: ./reference/immersive_layout.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 定义窗口级全屏和页面级避让的配合方式
  - 排查沉浸式布局中的内容遮挡问题
load_when:
  - 命中 AVOID-03
avoid_when:
  - 页面不需要沉浸式展示
supports_scenes:
  - AVOID-03
output_fields:
  - device_constraints
  - implementation_notes
  - root_cause_hypothesis
  - verification_matrix
  - residual_risks
```

#### `RSC_AVOID_04` 键盘避让参考

```yaml
resource_id: RSC_AVOID_04
resource_type: reference
path: ./reference/keyboard_handling.md
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
used_for:
  - 设计键盘弹出、收起和焦点切换时的避让逻辑
  - 排查输入区跳动、按钮被遮挡等问题
load_when:
  - 命中 AVOID-04
avoid_when:
  - 页面没有输入交互
supports_scenes:
  - AVOID-04
output_fields:
  - acceptance_focus
  - implementation_notes
  - fix_plan
  - verification_matrix
  - evidence_requirements
```

#### `RSC_AVOID_05` 问题修复案例集

```yaml
resource_id: RSC_AVOID_05
resource_type: reference
path: ./reference/bug-fix-cases.md
phase_tags: [FIX]
priority: P1
used_for:
  - 排查状态栏遮挡、挖孔区遮挡、沉浸式布局错位、键盘避让异常等常见问题
load_when:
  - 命中 AVOID-01 或 AVOID-03 或 AVOID-04 且处于 FIX 阶段
avoid_when:
  - 当前不涉及问题修复
supports_scenes:
  - AVOID-01
  - AVOID-03
  - AVOID-04
output_fields:
  - problem_profile
  - root_cause_hypothesis
  - fix_plan
  - regression_watchlist
```

#### `RSC_AVOID_06` 开发场景方案集

```yaml
resource_id: RSC_AVOID_06
resource_type: reference
path: ./reference/scenario-development-cases.md
phase_tags: [REQ, DEV, VAL]
priority: P0
used_for:
  - 提供沉浸式布局等场景的完整开发方案与分步实现
load_when:
  - 命中 AVOID-03 且处于 REQ 或 DEV 阶段
avoid_when:
  - 当前处于 FIX 阶段（应走 RSC_AVOID_05）
supports_scenes:
  - AVOID-03
output_fields:
  - acceptance_focus
  - implementation_notes
  - code_touchpoints
  - verification_matrix
```

## 阶段输出契约

### `REQ`

- 必须输出：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`
- 必须输出：`device_constraints`、`capability_boundary`、`acceptance_focus`
- 额外要求：明确背景层、内容层、输入层各自是否允许越过系统区域

### `DEV`

- 必须输出：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- 额外要求：明确动态获取 API、布局更新入口和窗口级设置落点

### `FIX`

- 必须输出：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- 额外要求：明确遮挡来源是系统栏、挖孔区、软键盘还是沉浸式窗口设置

### `VAL`

- 必须输出：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`
- 额外要求：至少提供系统栏变化、键盘开闭或挖孔方向变化下的截图或录屏证据
