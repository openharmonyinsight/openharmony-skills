---
name: hmos-multidevice-scenario-entry
description: Entry skill for HarmonyOS multi-device adaptation. Use when the task broadly concerns HarmonyOS multi-device adaptation, or when the correct scenario is still unclear. This skill classifies the request by phase and scenario type, then routes to one or more scenario files for screen and window size, fold state, avoid areas, interaction methods, natural orientation, or hardware access.
---

# 鸿蒙多设备适配总场景入口

## 技能定义

| 字段 | 内容 |
| --- | --- |
| `skill_id` | `harmonyos-multi-device-scenario-entry` |
| `skill_name` | `鸿蒙多设备适配总场景入口` |
| `one_line_purpose` | 先判断当前问题属于哪类多设备适配场景，再把请求引导到对应场景文件。 |
| `device_scope` | `phone / tablet / foldable / tri-fold / pc / wearables / external input or device` |
| `problem_scope` | `多设备布局、折展状态、避让区、交互方式、自然方向、硬件能力差异` |
| `not_in_scope` | `分布式流转、账号体系、网络通信、纯业务功能设计、与多设备无关的常规 UI 微调` |
| `primary_outputs` | `active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`route_reason`、`next_scene_refs` |

## 总入口约束

- 这个 skill 只负责入口分流，不直接展开场景实现细节。
- 先判定阶段，再判定场景类型；不要跳过阶段识别直接选场景。
- 当请求同时命中多个场景时，必须输出主场景和次场景，而不是强行只保留一个。
- 只有在当前问题的根因明确落在某个场景时，才允许单场景处理；否则按复合场景处理。
- `screen-window-size` 是布局类兜底场景，不应吞并折展、避让、方向、交互和硬件问题。
- 进入场景文件后，应优先遵循该场景文件的边界定义和约束，不要让总入口覆盖场景的专有规则。

## 阶段标签

| 标签 | 阶段 | 总入口关注点 |
| --- | --- | --- |
| `REQ` | 需求分析设计 | 问题边界、设备范围、主适配维度 |
| `DEV` | 开发 | 主代码落点在哪个场景，是否需要多个场景联合 |
| `FIX` | 问题修复 | 根因属于哪个适配域，是否存在连带回归域 |
| `VAL` | 功能验证 | 验证矩阵应覆盖哪个场景，是否需要交叉验证 |

## 统一输出字段

- 入口字段：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`route_reason`、`next_scene_refs`
- `REQ`：`problem_frame`、`device_scope_summary`、`routing_focus`
- `DEV`：`primary_code_domain`、`secondary_code_domains`、`integration_edges`
- `FIX`：`suspected_root_domain`、`linked_regression_domains`、`handoff_priority`
- `VAL`：`validation_domains`、`cross_checks`、`evidence_scope`

## 字段释义

- `primary_scene`：当前请求最应该先进入的场景。
- `secondary_scenes`：与主场景联动的次级场景列表，只允许填写 `SCENE-xx` 形式的场景 id，不填写 skill 路径。
- `route_reason`：说明为什么命中当前主场景，而不是其他场景。
- `next_scene_refs`：下一步应该实际打开的场景文件路径列表。
- `primary_scene_ref`：当前场景卡片直接指向的主场景路径，只在场景卡片内部使用。
- `secondary_scene_refs`：当前场景卡片常见的次级场景路径，只在场景卡片内部使用。
- `scene_strategy`：当前场景是 `single` 还是 `composite`。
- `candidate_scenes`：当 `scene_strategy: composite` 时，可作为主次场景的候选 `SCENE-xx` 列表。
- `candidate_scene_refs`：当 `scene_strategy: composite` 时，可进一步展开的候选场景文件路径列表。
- 这个总场景入口不输出 `device_constraints`；`device_constraints` 属于场景文件的 `REQ` 字段，由对应场景在展开分析时产出。

## AI 检索要求

- 先从用户表达判断 `active_phases`：
  - 需求、设计、方案、选型、边界，归入 `REQ`
  - 开发、实现、怎么写、代码接线，归入 `DEV`
  - 修复、bug、异常、错位、崩溃，归入 `FIX`
  - 验证、测试、验收、截图证据、回归，归入 `VAL`
- 再按问题关键词命中主场景，不要一次性读取全部场景文件。
- 命中单一场景时，只打开对应场景文件。
- 命中复合场景时，先确定 `primary_scene`，再从 `secondary_scenes` 里补充 1-2 个次级场景，并汇总为最终的 `next_scene_refs`。
- 若问题只表现为“多设备布局不一致”而未出现更强特征词，默认先走 `SCENE-01`。
- 涉及“旋转后布局未更新、窗口变化未同步”但不涉及自然方向语义、`setPreferredOrientation` 或 `rotation` 值解释时，仍优先走 `SCENE-01`。
- 若请求出现明确系统区域遮挡、折痕、方向语义、输入设备或硬件能力词，则优先使用对应专有场景，不要被布局关键词抢走。

## 场景簇索引

#### `SCENE-01` 布局与窗口尺寸场景

```yaml
scene_id: SCENE-01
scene_name: 布局与窗口尺寸场景
phase_tags: [REQ, DEV, FIX, VAL]
priority: P2
intent_signals:
  - 响应式
  - breakpoint
  - GridRow
  - GridCol
  - 多栏
  - windowSizeChange
  - media query
  - 窗口变化
  - 旋转后布局不同步
applies_when:
  - 主要问题是断点、结构切换或窗口尺寸变化
  - 问题可以不依赖折叠态、系统避让区、方向语义、输入设备或硬件能力来解释
not_applies_when:
  - 存在折痕、悬停态、Pura X、键盘遮挡、状态栏遮挡、自然方向语义、`setPreferredOrientation`、`rotation` 值解释、mouse、canIUse 等更强信号
scene_strategy: single
primary_scene_ref: ./references/hmos-multidevice-screen-window-size/SKILL.md
secondary_scenes:
  - SCENE-02
  - SCENE-03
secondary_scene_refs:
  - ./references/hmos-multidevice-fold-state/SKILL.md
  - ./references/hmos-multidevice-avoid-areas/SKILL.md
```

#### `SCENE-02` 折展状态与折痕场景

```yaml
scene_id: SCENE-02
scene_name: 折展状态与折痕场景
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - foldStatus
  - 折叠
  - 展开
  - 悬停态
  - 折痕
  - tri-fold
  - G态
  - Pura X
applies_when:
  - 主要问题依赖设备折叠状态、折痕几何或宽折叠形态
  - 页面在手机和平板正常，但在折叠设备上出现结构或行为异常
not_applies_when:
  - 问题只与普通横竖屏变化或普通窗口断点有关
scene_strategy: single
primary_scene_ref: ./references/hmos-multidevice-fold-state/SKILL.md
secondary_scenes:
  - SCENE-01
  - SCENE-05
secondary_scene_refs:
  - ./references/hmos-multidevice-screen-window-size/SKILL.md
  - ./references/hmos-multidevice-natural-orientation/SKILL.md
```

#### `SCENE-03` 系统区域与键盘避让场景

```yaml
scene_id: SCENE-03
scene_name: 系统区域与键盘避让场景
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - safe area
  - 状态栏
  - 导航栏
  - 挖孔
  - 刘海
  - 沉浸式
  - 键盘遮挡
  - 输入法
applies_when:
  - 主要问题是内容被系统区域、挖孔区或软键盘遮挡
  - 需要处理背景延伸和内容避让边界
not_applies_when:
  - 问题只是普通 margin 或栅格调整
scene_strategy: single
primary_scene_ref: ./references/hmos-multidevice-avoid-areas/SKILL.md
secondary_scenes:
  - SCENE-01
  - SCENE-02
secondary_scene_refs:
  - ./references/hmos-multidevice-screen-window-size/SKILL.md
  - ./references/hmos-multidevice-fold-state/SKILL.md
```

#### `SCENE-04` 多输入与焦点交互场景

```yaml
scene_id: SCENE-04
scene_name: 多输入与焦点交互场景
phase_tags: [REQ, DEV, FIX, VAL]
priority: P1
intent_signals:
  - 鼠标
  - hover
  - 右键
  - 键盘焦点
  - shortcut
  - 手写笔
  - 拖拽
  - 外接键鼠
applies_when:
  - 主要问题是交互模型会随输入方式变化
  - 需要同时兼容触摸、鼠标、键盘或手写笔
not_applies_when:
  - 问题只表现为布局变化，没有交互行为变化
scene_strategy: single
primary_scene_ref: ./references/hmos-multidevice-interaction-methods/SKILL.md
secondary_scenes:
  - SCENE-01
secondary_scene_refs:
  - ./references/hmos-multidevice-screen-window-size/SKILL.md
```

#### `SCENE-05` 自然方向与旋转语义场景

```yaml
scene_id: SCENE-05
scene_name: 自然方向与旋转语义场景
phase_tags: [REQ, DEV, FIX, VAL]
priority: P1
intent_signals:
  - rotation 值
  - orientation
  - 自然竖屏
  - 自然横屏
  - setPreferredOrientation
  - 传感器方向
  - 横竖屏误判
applies_when:
  - 主要问题是方向语义、rotation 值或自然方向类型
  - 需要区分屏幕旋转、窗口方向和自然方向
not_applies_when:
  - 只是宽度断点变化或窗口尺寸同步导致的布局切换
scene_strategy: single
primary_scene_ref: ./references/hmos-multidevice-natural-orientation/SKILL.md
secondary_scenes:
  - SCENE-02
  - SCENE-01
secondary_scene_refs:
  - ./references/hmos-multidevice-fold-state/SKILL.md
  - ./references/hmos-multidevice-screen-window-size/SKILL.md
```

#### `SCENE-06` 硬件能力与外设场景

```yaml
scene_id: SCENE-06
scene_name: 硬件能力与外设场景
phase_tags: [REQ, DEV, FIX, VAL]
priority: P0
intent_signals:
  - canIUse
  - SysCap
  - 相机
  - camera
  - 传感器
  - GPS
  - NFC
  - 蓝牙
  - 外接设备
  - 热插拔
applies_when:
  - 主要问题是硬件能力存在设备差异，或调用前必须先检测能力
  - 行为异常与设备枚举、权限声明、连接切换或降级策略直接相关
not_applies_when:
  - 问题是纯 UI 布局、方向或避让，不涉及硬件能力差异
scene_strategy: single
primary_scene_ref: ./references/hmos-multidevice-hardware-access/SKILL.md
secondary_scenes:
  - SCENE-04
secondary_scene_refs:
  - ./references/hmos-multidevice-interaction-methods/SKILL.md
```

#### `SCENE-07` 复合问题联合场景

```yaml
scene_id: SCENE-07
scene_name: 复合问题联合场景
phase_tags: [REQ, DEV, FIX, VAL]
priority: P1
intent_signals:
  - 同时出现折叠、键盘、窗口、方向、输入或硬件中的多个信号
  - 需要解释主问题和连带问题
  - 单一场景不足以完整覆盖
applies_when:
  - 问题必须同时依赖两个以上场景才能解释
  - 需要先选主场景，再合并次场景
not_applies_when:
  - 单一场景已经足够解释问题
scene_strategy: composite
candidate_scenes:
  - SCENE-01
  - SCENE-02
  - SCENE-03
  - SCENE-04
  - SCENE-05
  - SCENE-06
candidate_scene_refs:
  - ./references/hmos-multidevice-screen-window-size/SKILL.md
  - ./references/hmos-multidevice-fold-state/SKILL.md
  - ./references/hmos-multidevice-avoid-areas/SKILL.md
  - ./references/hmos-multidevice-interaction-methods/SKILL.md
  - ./references/hmos-multidevice-natural-orientation/SKILL.md
  - ./references/hmos-multidevice-hardware-access/SKILL.md
```

## 输出约定

- 先输出结构化场景判断，再进入对应场景文件。
- 如果必须联合多个场景，优先输出 `SCENE-07` 的组合策略。
- 不要把场景和实现混在一起；入口负责定位，场景文件负责展开。
- 最终输出应尽量保持字段稳定，不要因表达习惯改变字段名。
