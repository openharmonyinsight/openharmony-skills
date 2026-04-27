---
name: hmos-multidevice-interaction-methods
description: HarmonyOS应用多设备交互适配开发方案skill，提供触摸、鼠标、键盘、手写笔等多输入方式的交互方案和统一策略。当涉及触摸、鼠标、键盘、手写笔等设备的交互以及实现交互归一化、悬停效果、右键菜单、焦点导航、手写板输入和压感等功能时调用。
---

# 交互方式适配

## 技能概述
HarmonyOS应用交互方式适配skill，为触摸、鼠标、键盘、手写笔等多输入方式提供交互方案和统一交互策略
适用设备(device types)： phone / tablet / 2in1 / tv
适用范围：交互归一化、鼠标悬浮、右键菜单、焦点导航、键盘快捷键、手写笔输入` 
不适用范围： 纯视觉动画微调、与输入方式无关的业务流程改造

## 核心约束

- 先明确当前页面的主输入方式和兼容输入方式，再决定交互模型。
- 优先采用交互归一化方案，避免为不同输入方式维护完全独立的主流程。
- 涉及鼠标或触控板时，必须补充悬浮、右键和拖拽反馈。
- 涉及键盘时，必须明确焦点顺序、方向键行为和快捷键行为。
- 涉及手写笔时，必须区分触碰和按压。
- 多输入并存时必须给出优先级策略。

## 阶段标签

| 标签 | 阶段 | 当前模块关注点 |
| --- | --- | --- |
| `REQ` | 需求分析设计 | 主输入方式、兼容输入方式、交互边界 |
| `DEV` | 开发 | 事件接线、焦点链路、悬浮和快捷键实现 |
| `FIX` | 问题修复 | 焦点断裂、鼠标无反馈、快捷键冲突、手写笔异常 |
| `VAL` | 功能验证 | 输入矩阵、焦点路径、悬浮效果验证、快捷键验证 |

## 统一输出字段

- 路由字段：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`resources_used`
- `REQ`：`device_constraints`、`capability_boundary`、`acceptance_focus`
- `DEV`：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- `FIX`：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- `VAL`：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`

## 字段释义

- `device_constraints`：指由触摸、鼠标、键盘、手写笔或外接输入设备差异带来的交互硬约束。在 `interaction-methods` 中，通常是哪些输入方式必须支持、是否必须有 hover 或 focus、快捷键是否是必选能力。
- `capability_boundary`：指当前交互方案覆盖哪些输入方式，哪些输入路径可以降级，哪些行为只在特定设备上生效。
- `acceptance_focus`：指需求阶段验收时必须确认的焦点链路、悬浮反馈、快捷键行为和多输入回退策略。
- scene 中 `deliverables.REQ` 出现 `device_constraints`，表示“该交互场景命中后，需求阶段必须先明确输入适配边界”，不是对字段重新命名。

## 场景决策树

```
开始
  │
  ├─→ 步骤1: 分析是否涉及鼠标交互(右键菜单，鼠标悬浮)
  │     └─→ 涉及 → 命中 `INPUT-01` -> 步骤2
  │     └─→ 不涉及 → 步骤3
  │
  ├─→ 步骤2: 分析是否涉及交互归一化，即一套组件同时支持触摸和鼠标
  │     └─→ 涉及 → 命中 `INPUT-02` -> 步骤3
  │     └─→ 不涉及 → 步骤3
  │
  ├─→ 步骤3: 分析是否涉及键盘交互（焦点导航、样式或键盘快捷键）
  │     └─→ 涉及 → 命中 `INPUT-03` -> 步骤4
  │     └─→ 不涉及 → 步骤4
  │
  └─→ 步骤4: 分析是否涉及手写笔交互（手写笔交互，压感）
        └─→ 涉及 → 命中 `INPUT-04` -> 结束
        └─→ 不涉及 → 结束
```
---

## 场景索引

### `INPUT-01` 鼠标设备交互（点击，悬浮，右键菜单）

**阶段：** REQ, DEV, FIX

#### 适用场景
  - 页面需要面向 PC 或平板外接鼠标
  - 当前问题表现为鼠标悬浮无反馈或右键无菜单

#### 不适用场景
  - 页面只面向纯触摸设备

#### 关键决策
  - 明确悬浮态反馈、右键菜单和拖拽手势的交互层级
  - 决定是否为桌面设备提供额外快捷操作

#### 文件读取
  **REQ阶段**
  - 读取文档: [鼠标适配指南](./reference/mouse.md)
  
  **DEV阶段**
  - 读取文档: [鼠标适配指南](./reference/mouse.md)
  - 读取代码：[悬浮反馈示例](./assets/HoverEffectExample.ets)

  **FIX阶段**
  - 读取文档: [鼠标适配指南](./reference/mouse.md)
  - 读取代码：[悬浮反馈示例](./assets/HoverEffectExample.ets)
---

### `INPUT-02` 交互归一化

**阶段：** REQ, DEV, FIX

#### 适用场景
  - 同一组件需要兼容触摸和鼠标
  - 当前问题表现为不同输入方式走了不同主流程

#### 不适用场景
  - 当前页面只支持单一输入方式

#### 关键决策
  - 选择统一事件入口和差异化反馈出口
  - 决定长按、右键、拖拽之间的优先级

#### 文件读取
  **REQ阶段**
  - 读取文档: [交互归一化指南](./reference/interaction_normalization.md)
  
  **DEV阶段**
  - 读取文档: [交互归一化指南](./reference/interaction_normalization.md)
  - 读取代码：[交互归一化实现示例1](./assets/VideoPlayPauseAdapter.ets)
  - 读取代码：[交互归一化实现示例2](./assets/AdaptiveNavigation.ets)

  **FIX阶段**
  - 读取文档: [交互归一化指南](./reference/interaction_normalization.md)
  - 读取代码：[交互归一化实现示例1](./assets/VideoPlayPauseAdapter.ets)
  - 读取代码：[交互归一化实现示例2](./assets/AdaptiveNavigation.ets)
---

### `INPUT-03` 键盘焦点导航与快捷键

**阶段：** REQ, DEV, FIX

#### 适用场景
  - 页面需要焦点导航、方向键切换焦点、键盘快捷键时
  - 当前问题表现为焦点顺序错乱或快捷键冲突

#### 不适用场景
  - 页面完全不支持键盘输入

#### 关键决策
  - 定义焦点顺序、方向键映射和快捷键命名空间
  - 决定自动导航和手动导航的边界

#### 文件读取
  **REQ阶段**
  - 读取文档: [键盘适配指南](./reference/keyboard.md)
  
  **DEV阶段**
  - 读取文档: [键盘适配指南](./reference/keyboard.md)
  - 读取代码：[焦点导航示例](./assets/FocusNavigationExample.ets)
  - 读取代码：[键盘快捷键示例](./assets/KeyboardShortcutsExample.ets)

  **FIX阶段**
  - 读取文档: [键盘适配指南](./reference/keyboard.md)
  - 读取代码：[焦点导航示例](./assets/FocusNavigationExample.ets)
  - 读取代码：[键盘快捷键示例](./assets/KeyboardShortcutsExample.ets)
---

### `INPUT-04` 手写笔输入与笔态交互

**阶段：** REQ, DEV, FIX

#### 适用场景
  - 页面需要支持手写笔触碰、按压或悬浮
  - 当前问题表现为笔输入和手指输入混淆

#### 不适用场景
  - 目标设备不支持手写笔

#### 关键决策
  - 区分笔触输入与普通触摸输入
  - 决定悬浮、按压、笔迹预览的反馈方式

#### 文件读取
  **REQ阶段**
  - 读取文档: [手写笔输入指南](./reference/stylus.md)
  
  **DEV阶段**
  - 读取文档: [手写笔输入指南](./reference/stylus.md)

  **FIX阶段**
  - 读取文档: [手写笔输入指南](./reference/stylus.md)
---

## 阶段输出契约

### `REQ`

- 必须输出：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`
- 必须输出：`device_constraints`、`capability_boundary`、`acceptance_focus`
- 额外要求：明确主输入方式、兼容输入方式，以及是否存在输入优先级

### `DEV`

- 必须输出：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- 额外要求：明确事件入口、焦点管理入口和快捷键触发逻辑

### `FIX`

- 必须输出：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- 额外要求：明确问题属于事件归一化缺失、焦点链路错误、悬浮反馈缺失还是笔输入分流错误

### `VAL`

- 必须输出：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`
- 额外要求：至少覆盖触摸、鼠标或触控板、键盘三类输入中的适用组合；如命中 `INPUT-04`，还要进行手写笔验证