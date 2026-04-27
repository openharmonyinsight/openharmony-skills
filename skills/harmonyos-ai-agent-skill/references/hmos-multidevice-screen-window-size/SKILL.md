---
name: hmos-multidevice-screen-window-size
description: Handle HarmonyOS screen and window size adaptation, including breakpoint systems, responsive layouts, GridRow/GridCol usage, window size observation, and multi-device layout changes.
---

# 屏幕窗口尺寸适配

## 技能定义

| 字段 | 内容                                                                                   |
| --- |--------------------------------------------------------------------------------------|
| `skill_id` | `screen-window-size`                                                                 |
| `skill_name` | `屏幕窗口尺寸适配`                                                                           |
| `one_line_purpose` | 为多设备布局提供断点策略、结构切换策略和窗口监听策略。                                                          |
| `device_scope` | `phone / tablet / tv / 2in1`                                                         |
| `problem_scope` | `断点体系、响应式布局、窗口变化监听、媒体查询`                                                             |
| `not_in_scope` | `纯业务逻辑重构、与尺寸无关的视觉微调`                                                                 |
| `primary_outputs` | `primary_scene`、`device_constraints`、`code_touchpoints`、`fix_plan`、`verification_matrix` |

## 核心约束

- 先判断问题属于组件级自适应还是页面级响应式，再选方案。
- 优先复用统一断点体系，不要引入与现有阈值冲突的新断点。
- 涉及结构切换时，优先使用 `GridRow`、`GridCol` 或其他响应式容器，而不是零散条件分支。
- 涉及窗口变化监听时，必须说明监听入口、状态同步和取消监听逻辑。
- 需要横向窗口或特殊比例支持时，必须说明宽度、纵向断点或高宽比谁是主判定条件。
- 未给出不同断点下的结构变化和内容取舍前，不得宣称方案完整。
- `FIX` 阶段必须先保护单屏基线体验，再处理多屏问题；禁止出现“多屏改善但单屏明显退化”。
- 针对图片拉伸问题，优先修复“容器约束与渲染模式”的根因，禁止通过人为拉伸系数制造或掩盖问题。
- 仅修复图片拉伸时，不得通过限制整页主内容宽度制造大面积留白；优先限制目标图片的渲染宽度或容器策略。

## Workflow

### Input
用户描述一个多设备布局需求（如"适配平板"）或布局异常问题（如"折叠屏上布局断裂"）。

### Process
1. **判断问题类型**：需求设计（REQ）/ 开发实现（DEV）/ Bug 修复（FIX）/ 功能验证（VAL）。
2. **读取规格**：先路由到 `SIZE-00`，读取多设备适配规格要求。
3. **场景路由**：根据问题特征路由到 SIZE-01~04：
   - 断点 / 响应式布局 / 窗口监听 → `SIZE-01`
   - 截断 / 留白 / 溢出 / 压缩 → `SIZE-02`
   - 偏移 / 错位 / 对齐异常 / 层级错乱 → `SIZE-03`
   - 堆叠 / 遮挡 / 容器选择错误 → `SIZE-04`
4. **读取场景文档**：根据匹配到的场景和问题类型（阶段），读取该场景「文件读取」中对应的 reference 和 assets 文件。
5. **按阶段交付**：根据匹配的阶段输出对应契约字段（见「阶段输出契约」）。

### Output
按匹配的阶段（REQ/DEV/FIX/VAL）输出对应契约字段。

## 阶段标签

| 标签 | 阶段 | 当前模块关注点 |
| --- | --- | --- |
| `REQ` | 需求分析设计 | 断点边界、设备范围、结构变化原则 |
| `DEV` | 开发 | 断点状态管理、容器选型、监听落点 |
| `FIX` | 问题修复 | 断点错配、布局断裂、状态未同步 |
| `VAL` | 功能验证 | 断点切换证据、窗口变化证据、布局稳定性 |

## 统一输出字段

- 路由字段：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`、`resources_used`
- `REQ`：`device_constraints`、`capability_boundary`、`acceptance_focus`
- `DEV`：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- `FIX`：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- `VAL`：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`

## 字段释义

- `device_constraints`：指由设备形态、窗口状态、输入方式或系统区域带来的适配硬约束。在 `screen-window-size` 中，通常是断点范围、主判定维度和不同尺寸下是否发生结构切换。它不是 API 列表，也不是代码修改点。
- `capability_boundary`：指当前方案支持到哪里、不支持什么、在哪些设备或窗口条件下需要降级或不处理。
- `acceptance_focus`：指需求阶段验收时必须重点确认的现象、证据或边界条件。
- scene 中 `deliverables.REQ` 出现 `device_constraints`，表示“该场景一旦命中，在需求分析阶段必须产出这个字段”，不是对字段再定义一次。

## AI 检索要求

- **所有窗口尺寸适配场景都必须先命中 `SIZE-00`**，读取规格要求。
- 涉及断点命名、阈值统一、断点错配、GridRow/GridCol、响应式布局、窗口变化监听时，优先命中 `SIZE-01`。
- 涉及组件截断、留白、尺寸溢出或压缩时，优先命中 `SIZE-02`。
- 涉及组件偏移、错位、对齐异常或层级错乱时，优先命中 `SIZE-03`。
- 涉及组件堆叠、遮挡、截断或布局容器选择错误时，优先命中 `SIZE-04`。
- 当请求同时包含"怎么改"和"怎么验"时，设置 `active_phases: [DEV, VAL]`。
- 出现以下信号时，必须主命中 `SIZE-02`，并联动 `VAL`：
  - 首图/轮播图/横幅在单屏正常，多屏拉伸或聚焦异常
  - `ImageFit.Cover`、容器高度、宽屏放大导致内容缺失或裁切
  - `component_stretch`、图片四周被拉开、中心聚焦失真

## 资源索引

#### `SIZE-00` 多设备窗口适配规格

**阶段**：REQ | **优先级**：P0

**适用场景**
- 所有涉及屏幕窗口尺寸适配的需求，必须先进入此场景读取规格要求
- 需要了解 HarmonyOS 多设备适配的标准规范、设计原则和约束条件

**不适用场景**
- 已完成规格分析，直接进入开发或修复阶段（跳过此场景，直接进入 SIZE-01 至 SIZE-04）
- 纯业务逻辑重构，不涉及窗口尺寸适配

**文件读取**

**REQ 阶段**（读取 reference）
- `./reference/adaptation-specification.md` - 多设备适配规格要求

**DEV 阶段**（按最佳实践读取 assets）
- `./assets/PipWindow.ets` ⭐ 推荐方案 - SPEC-05 画中画能力完整示例（PipManager + CustomNodeController + 页面集成）



#### `SIZE-01` 多设备适配窗口尺寸布局

**阶段**：REQ / DEV / FIX | **优先级**：P0

**适用场景**
- 涉及断点系统设计、阈值定义
- 使用 GridRow/GridCol 实现响应式布局
- 需要监听窗口尺寸变化（旋转、折叠、拖拽）
- 问题：断点不一致、布局未随尺寸变化更新

**不适用场景**
- 仅与安全区、键盘、折痕相关
- 静态布局，不依赖运行时尺寸变化

**关键决策**
- 系统断点 vs 自定义断点
- 宽度/纵向断点/高宽比谁是主判定条件
- 页面骨架和容器类型（GridRow、Stack、Flex）
- 窗口监听方式：windowSizeChange / media query
- 同步粒度和防抖策略

**文件读取**

**REQ 阶段**（读取 reference）
- `./reference/breakpoint_system.md` - 断点系统设计原理
- `./reference/responsive_layout.md` - 四种响应式布局（重复布局、分栏布局、挪移布局、缩进布局）
- `./reference/adaptive_layout.md` - 七种自适应能力（拉伸、缩放、隐藏、占比、折行、均分、延伸）
- `./reference/window_size_detection.md` - 窗口监听机制

**DEV 阶段**（按最佳实践读取 assets）

**断点系统**
- `./assets/SystemBreakpointExample.ets` ⭐ 推荐方案 - 系统断点枚举
- `./assets/BreakpointConstants.ets` - 备选方案 - 自定义断点常量
- `./assets/BreakpointType.ets` - 简化条件渲染
- `./assets/BreakpointObserver.ets` - 断点观察器

**响应式布局**
- `./assets/GridRowBreakpoints.ets` - GridRow 内置断点
- `./assets/GridRowExample.ets` - 栅格布局示例
- `./assets/GridColOffset.ets` - 栅格偏移配置

**窗口监听**
- `./assets/WindowSizeChangeListener.ets` ⭐ 推荐方案 - 直接监听窗口尺寸变化
- `./assets/MediaQueryManager.ets` - 媒体查询管理器
- `./assets/MediaQueryExample.ets` - 媒体查询示例

**FIX 阶段**（读取 reference）
- `./reference/breakpoint_system.md` - 断点系统设计原理
- `./reference/adaptive_layout.md` - 七种自适应能力（拉伸、缩放、隐藏、占比、折行、均分、延伸）
- `./reference/window_size_detection.md` - 窗口监听机制



#### `SIZE-02` 尺寸异常修复

**阶段**：DEV / FIX | **优先级**：P1

**适用场景**
- 组件宽度/高度在多设备上不适配
- 问题：截断、留白、溢出、压缩、内容被切掉

**不适用场景**
- 仅位置偏移（见 SIZE-03）
- 布局容器选择错误（见 SIZE-04）

**关键决策**
- 问题类型：固定尺寸 / 断点缺失 / 空间竞争
- 需要调整的尺寸属性和断点分支

**图片拉伸专项规则（component_stretch）**

**根因判断（必须先判断再改）**
- 若“单屏正常、多屏异常拉伸”，优先判定为：大宽度下图片容器与渲染策略不匹配，而非业务主动调节拉伸值。
- 若出现“内容缺失”，优先判定为：`ImageFit.Cover` 与容器高度过低导致裁切，而非图片资源问题。

**禁止方案（命中任一即判高风险）**
- 通过调整“人为拉伸倍率”来制造或抵消拉伸现象，缺乏真实工程约束依据。
- 为了避免拉伸而限制整页主内容宽度，导致明显留白和交互区域浪费。
- 仅验证多屏，不验证单屏；或仅凭截图主观判断，不提供布局边界证据。

**推荐方案（按顺序执行）**
1. 先锁定单屏基线观感：保持首图在单屏全宽可见，不出现明显瘦条化。
2. 再抑制大屏过度放大：优先限制目标图片渲染宽度或设置合理容器高度上限，而非限制整页宽度。
3. 最后处理裁切：在不引入拉伸的前提下，提升首图容器可视高度，减少底部内容丢失。

**验收门禁（未全部满足不得宣称 GoodCase）**
- 单屏门禁：修复后单屏首图不得比修复前明显变小；若单屏观感退化，必须回滚并重做。
- 多屏门禁：双屏/三屏不出现继续放大导致的“拉伸感增强”。
- 证据门禁：必须同时提供截图与布局 dump 的 `Image bounds` 对比证据。

**文件读取**

**DEV 阶段**（读取 assets）
- `./assets/small-square-screen-collapse.md` - 小方形屏底部栏折叠
- `./assets/scroll-page-content-clipped-by-full-height.md` - 滚动内容裁剪
- `./assets/alphabetindexer-autocollapse.md` - 索引器自动折叠

**FIX 阶段**（读取 reference）
- `./reference/size-anomaly.md` - 问题分类和根因分析



#### `SIZE-03` 位置异常修复

**阶段**：DEV / FIX | **优先级**：P1

**适用场景**
- 组件相对位置或绝对位置在多设备上不适配
- 问题：偏移、错位、对齐异常、层级错乱、组件跑到屏幕外

**不适用场景**
- 仅尺寸截断（见 SIZE-02）
- 布局容器选择错误（见 SIZE-04）

**关键决策**
- 问题类型：绝对定位 / 锚点适配 / 对齐方式 / 边距累加
- 定位方式的修复策略

**文件读取**

**DEV 阶段**（读取 assets）
暂无内容

**FIX 阶段**（读取 reference）
- `./reference/position-anomaly.md` - 位置异常分类和根因



#### `SIZE-04` 布局异常修复

**阶段**：DEV / FIX | **优先级**：P1

**适用场景**
- 布局容器选择或配置不当
- 问题：堆叠、遮挡、截断、布局错乱、GridRow 不降列

**不适用场景**
- 仅组件尺寸问题（见 SIZE-02）
- 仅组件位置问题（见 SIZE-03）

**关键决策**
- 问题类型：容器选择 / 断点参考系 / 滚动缺失 / 嵌套结构
- 布局容器的替换或配置修复方案

**文件读取**

**DEV 阶段**（读取 assets）
- `./assets/gridrow-breakpoints.md` - GridRow 断点问题修复
- `./assets/stack-overlap-occlusion.md` - Stack 堆叠遮挡修复
- `./assets/row-displaypriority-truncation.ets` - Row/Column 组件截断优先级
- `./assets/SplitScreenExample.ets` - 分屏模式下截断问题修复

**FIX 阶段**（读取 reference）
- `./reference/layout-anomaly.md` - 布局异常分类和根因

## 阶段输出契约

### `REQ`

- 必须输出：`active_phases`、`primary_phase`、`primary_scene`、`secondary_scenes`
- 必须输出：`device_constraints`、`capability_boundary`、`acceptance_focus`
- 额外要求：说明最小支持断点集合，以及每个断点下是否发生结构变化

### `DEV`

- 必须输出：`code_touchpoints`、`reuse_resources`、`implementation_notes`、`integration_risks`
- 额外要求：明确断点状态由谁维护，窗口变化由谁监听，布局由哪个容器承接

### `FIX`

- 必须输出：`problem_profile`、`root_cause_hypothesis`、`fix_plan`、`regression_watchlist`
- 额外要求：
1.明确问题属于断点边界错误、容器配置错误还是监听同步错误
2.必须显式给出 `single_screen_guard`（单屏不退化策略）和 `multi_screen_guard`（多屏不拉伸策略）
3.`fix_plan` 必须包含“先单屏基线、后多屏抑制、再裁切优化”的执行顺序

### `VAL`

- 必须输出：`verification_matrix`、`evidence_requirements`、`pass_criteria`、`residual_risks`
- 额外要求：
1.至少覆盖 `small / medium / large` 或项目等价断点，并提供截图、布局 dump 或窗口尺寸证据
2.图片拉伸类问题必须覆盖单屏/双屏/三屏三个窗口宽度层级（项目等价值如 `1008 / 2048 / 3184`）
3.`pass_criteria` 必须包含以下客观项：
  - 页面路径正确（目标 GoodCase 页面）
  - 三屏 `Image bounds` 可对比且无异常拉伸趋势
  - 单屏首图可视高度不低于修复前基线
