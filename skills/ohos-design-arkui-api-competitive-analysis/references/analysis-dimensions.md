# Analysis Dimensions / 竞品分析维度框架

本框架使用 **4 组 / 12 维**。12 维用于组织问题和控制深度，不替代来源、版本、作用域和证据门禁。先完成强制基线检查，再按 API 类别选择默认重点；具体能力可以增加或加深维度，但不能因默认重点未列出而跳过已发现的关键风险。

## 1. 强制基线检查

每个 API 都必须记录：

- **分析契约**：目标、目的、作用域层级、API 类别、报告模式和排除项。
- **版本基线**：ArkUI API/分支、Android API Level 与 Compose 版本、iOS/iPadOS 版本、查询日期。
- **公共符号**：ArkUI 精确接口与 `@since`；Android/iOS 精确官方符号与 availability。
- **对标关系**：直接等价、功能等价、组合实现、替代方案或未找到等价能力，并说明选择和排除理由。
- **证据状态**：官方事实、分析推论、冲突和待核事项分开记录。
- **引用关系**：Capability ID、Fact ID、Claim ID 和 Source ID 可相互追溯。

## 2. 类别默认重点与覆盖规则

| API 类别 | 默认重点维度 | 典型关注点 |
|---|---|---|
| 事件类 | 3、4、6、8、11、12 | 事件数据、覆盖范围、分发、运行时频率、注入/测试、使用心智 |
| 手势类 | 3、4、5、6、8、12 | 参数与输出、手势覆盖、状态机、仲裁、运行时语义、组合心智 |
| 组件类 | 4、5、7、8、10、12 | 功能覆盖、生命周期、可访问性、运行时特征、兼容、开发体验 |
| 布局类 | 3、4、8、9、12 | 约束与默认值、布局能力、测量特征、设备形态、迁移心智 |
| 状态/动画类 | 3、4、5、8、10、12 | 参数模型、能力覆盖、状态与中断、执行特征、兼容、编排心智 |

用法：

1. 默认重点表示完整报告中应优先展开的维度，不是固定权重或排除列表。
2. 快速扫描可以压缩非默认维度，但强制基线检查仍全部保留。
3. 用户目标、证据或风险指向其它维度时，立即加入分析。
4. 同一类别的不同子类型使用覆盖规则加深维度，不复制一套新框架。

### 子类型覆盖闭环

识别到下列子类型时，将对应规格逐项加入 Capability Checklist。每项必须标记 `confirmed`、`pending` 或 `not-applicable`，并关联 Fact ID；不得只列出若干示例字段后宣称该子类型已经覆盖。

| 子类型 | 必须闭环的规格 |
|---|---|
| 原始触摸、指针或高刷新事件 | 坐标空间、单位、废弃字段及公共替代字段，报告中必须显式写 ArkUI `vp`、Android `px`、iOS `pt`；事件级与触点级字段归属，逐项核对 `source`、`sourceTool`、`tiltX`、`tiltY`、pressure 和 hand；归一化值与原始值；当前、变化、历史、合并与预测采样；命中、传播、取消和 responder/dispatch 链；注入与回放。禁止无 accepted advantage Claim 的“最细/最完整/领先”表述 |
| 键盘快捷键 | ArkUI 锚点固定为 `CommonMethod.keyboardShortcut`，核对签名、availability、修饰键、按键表达和绑定模型；必须从锁定版本的官方渲染文档 `ts-universal-events-keyboardshortcut.md` 逐项确认窗口是否需获焦、组件自身焦点/可见性/组件树成员条件、disabled 行为和重复组合键的命中规则，不预写结果；`onKeyEvent` 与 InputKit `inputConsumer` 作为不同层级路径单列，不得替代锚点；Android/iOS 按规定 Path Check 后映射 |
| 连续手势 | 配置、输入和输出的全部公共字段及其默认值、单位、范围与 availability；平移类特别核对 fingers、distance、direction、distanceMap、offset、velocity 和 angle；开始、更新、结束、取消和失败状态；阈值、多指、方向；优先、并行、互斥和 failure dependency；iOS 必须核对 `UIGestureRecognizerDelegate.gestureRecognizer(_:shouldRecognizeSimultaneouslyWith:)` 等 simultaneous-recognition 机制；位移的累计、增量、方向与重置语义；声明式与命令式路径 |
| 长列表或虚拟化集合 | 必须将 `List`、`ListItem`、`ListItemGroup`、通用 `Scroller`、`ListScroller`、`lanes`、`cachedCount`、`sticky`、`chainAnimation`、已废弃 `editMode` 和当前编辑路径逐项关联独立 Fact ID，并分别写 introduction/deprecation availability；同类控制器或属性不能互相代替。建立“能力 × 框架”矩阵，以 ArkUI、RecyclerView、Compose lazy list、UITableView、SwiftUI List 为独立列，逐行填写分组、多列、sticky、lazy、刷新、数据源、稳定身份、更新通知/局部更新、复用、缓存、nested scrolling、大数据模型、选择/重排；任何一行缺证据都写 `pending/not-applicable`，不得只在 checklist 提问。另建“框架 × 工具”矩阵，分别记录自动化定位/滚动/动作注入、无障碍检查、布局检查和性能分析的官方路径与状态；一个框架的能力、测试或 inspector 不得替代其它框架。继续逐框架覆盖默认无障碍语义、集合信息、焦点和动作，以及直接或组合的 refresh、accessibility 与 testing/tooling 路径 |
| Flex 类布局 | 主轴/交叉轴、方向与 reverse、wrap、justify、align/alignContent/alignSelf、grow、shrink、basis（含百分比）、order、spacing 的默认值和 availability；通用 Flex 与 Row/Column/stack 路径的边界；测量与约束；窗口尺寸、方向、折叠屏和平板适配 |
| 显式动画与复杂编排 | 核心入口、参数对象和 keyframe；ArkUI 必须点名核对 `cubicBezierCurve`、`stepsCurve`、`springCurve`、`springMotion`、`responsiveSpringMotion`、`interpolatingSpring` 等公共 curve helpers 的参数、默认值/单位和 availability，不得只写 Curve/ICurve；duration、delay、repeat、reverse、Bezier、steps、spring、keyframe；完成、中断、取消、暂停、恢复、scrub 和 velocity；声明式状态驱动与命令式起止模型；AnimatorSet/Transition/UIView keyframes/CAAnimationGroup 等编排路径；核心与每个可选能力分别记录引入版本、废弃、替代和低版本 fallback。时间默认值引用命名常量时必须追到常量值；离散/steps 能力引用枚举时必须追到精确 Swift/Kotlin/Java/Objective-C 符号。无官方 fallback 时明确写“无文档化 fallback”，不要留空 |
| 对话框、弹窗、模态组件 | 创建/展示/关闭生命周期；焦点陷阱、默认动作和屏幕阅读；窗口尺寸、方向、多窗口和设备形态 |
| 输入控件 | 数据约束、编辑状态、焦点与输入法交互、默认无障碍语义、替代输入和自动化测试 |

“全部公共字段”指从入口签名递归跟踪到的公开类型，不表示复制平台内部字段。只比较同一能力层级；某平台没有对应概念时记录 `not-applicable` 或经双向检索后的 `pending/no-equivalent-found`，不要借用另一平台字段补齐表格。

涉及多个 comparator（例如 RecyclerView、Compose lazy list、UITableView、SwiftUI List）时，建立“必查规格 × comparator”二维核对表。某一框架的空白不能由同平台另一框架代替；未确认也必须写明 `pending`、已检查来源和下一步。

动画不得使用“Android View/Compose”或“UIKit/Core Animation”合并单元格。至少将 `ValueAnimator`、`ObjectAnimator`、Compose animation、`UIView.animate`/`UIViewPropertyAnimator` 和 Core Animation 分成独立 comparator；每个 comparator 都要逐项覆盖必查规格和编排路径。

曲线能力不能以“支持自定义插值器”概括。逐 comparator 明确核对 cubic-Bezier 和 steps/discrete：Android View 检查 `PathInterpolator` 与 `TimeInterpolator`/keyframe 组合，Compose 检查 `CubicBezierEasing` 与 snap/keyframes/custom Easing，UIKit 检查 `UICubicTimingParameters` 与 keyframe discrete mode，Core Animation 检查 `CAMediaTimingFunction` 与 `CAKeyframeAnimation.calculationMode`。没有专用 steps API 时说明组合路径或 `pending`，不能留空。

## 3. 能力拆解

在套用 12 维前，先从 ArkUI 公共面拆成原子能力：

1. 入口、签名和调用模型。
2. 参数、返回值、默认值、单位、空值和错误语义。
3. 数据模型、状态机、生命周期和作用域。
4. 分发、仲裁、组合、限制和降级路径。
5. 版本演进、设备约束、可访问性和测试接口。

将每项写成待回答问题并分配 `C-01`、`C-02` 等 Capability ID。不要从 Android/iOS API 结构反推 ArkUI 的能力拆解。

## A. Scope & Contract / 范围与契约

### 1. Scope and Comparator Mapping / 作用域与对标映射

- **Definition**：能力所在层级、用户目标、比较边界及对标对象关系。
- **What to look for**：组件/窗口/应用/系统层级；主对标与补充对标；直接、功能、组合、替代或未找到等价能力。
- **How to check**：先完成 Analysis Brief 和 Comparator Map，记录选择与排除理由，禁止按名称相似度直接映射。

### 2. API Shape and Signature / API 形态与签名

- **Definition**：命名、参数、返回值、回调、声明式/命令式、Builder/Modifier/链式模型和类型表达。
- **What to look for**：调用入口、重载、泛型、可选参数、同步/异步、错误通道以及静态/动态接口差异。
- **How to check**：逐项核对三平台官方 API Reference，并把语法相似与行为等价分开。

### 3. Data Model and Specification Precision / 数据模型与规格精度

- **Definition**：数据结构、字段归属、单位、范围、默认值、枚举、空值和错误语义。
- **What to look for**：对象层级、标识稳定性、坐标/时间等量纲、约束、钳制、默认行为和废弃字段。
- **How to check**：建立字段级 Normalized Spec，保留各平台原生单位和语义，不强行换算为等价。

## B. Capability & Behavior / 能力与行为

### 4. Capability Coverage / 能力覆盖

- **Definition**：目标用户能力和子能力是否完整覆盖。
- **What to look for**：核心能力、可选能力、组合路径、降级方案和未找到的等价能力。
- **How to check**：按 Capability Checklist 逐项比较；负面或独有结论执行双向检索。

### 5. State and Lifecycle / 状态与生命周期

- **Definition**：创建、激活、更新、中断、完成、销毁及数据更新时序。
- **What to look for**：状态机、回调时机、所有权、副作用、恢复策略和生命周期边界。
- **How to check**：结合官方 API Reference 与 Guide 建立时序或状态表；无法对齐时标记语义不同。

### 6. Dispatch and Interaction / 分发与交互

- **Definition**：事件传递、命中测试、焦点、仲裁、优先级、嵌套协作和交互反馈。
- **What to look for**：传播链、拦截/取消、冲突处理、注册与命中范围、组合规则。
- **How to check**：比较官方分发流程和可控制节点，不根据单个方法名推断完整交互模型。

## C. Quality Attributes / 质量属性

### 7. Accessibility / 可访问性

- **Definition**：语义、焦点、屏幕阅读、可操作性、替代输入和系统辅助能力。
- **What to look for**：默认语义、可覆盖属性、焦点顺序、无障碍动作、动态字体和状态通知。
- **How to check**：检索各平台官方 Accessibility API Reference、Guide 和组件规范，区分框架默认能力与开发者责任。

### 8. Runtime and Performance Characteristics / 运行时与性能特征

- **Definition**：执行线程、调用频率、批处理、缓存、测量/布局、渲染提交和资源开销语义。
- **What to look for**：是否主线程、是否合并或节流、懒加载/复用、同步边界、中断与背压。
- **How to check**：只陈述官方文档或实测支持的特征；没有同条件数据时不得输出性能优越性结论。

### 9. Device and Form-Factor Consistency / 设备与形态一致性

- **Definition**：手机、平板、折叠屏、穿戴、桌面、车机、多窗口和多屏下的支持与行为。
- **What to look for**：SystemCapability、设备限制、方向/尺寸变化、窗口模式和输入设备差异。
- **How to check**：核对 availability、设备指南和限制说明，不以单一手机场景代表全平台。

## D. Evolution & Adoption / 演进与采用

### 10. Version and Compatibility / 版本与兼容

- **Definition**：引入、废弃、替代、行为变更及向前/向后兼容策略。
- **What to look for**：`@since`、API Level、availability、deprecated/obsoleted、迁移路径和降级方案。
- **How to check**：按锁定版本核对符号和行为，不混用当前、预览和未发布接口。

### 11. Interoperability, Tooling and Testability / 互操作、工具与可测试性

- **Definition**：与其它框架/标准的协作，以及调试、检查、注入、回放和自动化测试能力。
- **What to look for**：跨层桥接、序列化/标识、测试钩子、调试工具、可观测性和模拟输入。
- **How to check**：检索官方工具、测试和互操作文档；源码能力不得直接当作公共测试契约。

### 12. Developer Experience, Mental Model and Migration / 开发体验、心智与迁移

- **Definition**：学习成本、默认行为、组合方式、错误暴露、迁移适配和维护复杂度。
- **What to look for**：声明式/命令式差异、样板代码、隐式状态、调试难度、跨平台适配点和文档清晰度。
- **How to check**：从已确认的 API 与行为差异推导影响；没有用户研究时不做总体易用性排名。
