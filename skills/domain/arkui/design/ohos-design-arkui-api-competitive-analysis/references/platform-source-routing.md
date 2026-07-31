# Platform Source Routing / 对标平台官方资料路线

本文件只负责选择 Android/iOS 对标对象、Path Check 和官方取证入口。子类型必须覆盖哪些规格由 `analysis-dimensions.md` 定义；本文件提到的符号和字段仅表示去哪里取证，不形成第二套覆盖清单。

> **强制规则**：优先使用 Android Developers 和 Apple Developer 官方文档。官方 API Reference、Guide、Sample 足以支撑结论时，不得用平台源码、第三方博客、聚合文档或模型常识替代。平台源码仅用于补充实现细节，社区资料仅用于定位官方入口。

## 1. 对标对象选择

不要按名称相似度直接选择 API。先根据 Capability Checklist 确认用户能力、作用域、数据模型和生命周期，再标记：

- **Direct equivalent**：层级、行为和生命周期基本一致。
- **Functional equivalent**：达成相同用户能力，但 API 模型不同。
- **Composite equivalent**：需要多个 API 或框架层组合。
- **Fallback**：只能通过降级或替代路径实现。
- **No equivalent found**：完成规定检索后仍未找到直接或功能等价能力。

Compose/SwiftUI 是声明式 API 的优先入口，不是强制答案。若 View/UIKit 更符合目标能力，应作为主对标对象，并说明为什么排除名称相近但语义不同的 API。

## 2. 证据优先级

1. **官方 API Reference**：签名、参数、返回值、availability 和明确行为。
2. **官方 Guide**：概念模型、生命周期、分发流程、限制和推荐用法。
3. **官方 Sample**：组合方式和典型使用路径。
4. **平台源码**：AOSP、AndroidX、Swift SDK 等统一作为 E4 实现佐证，不单独支持公共能力或 availability。
5. **社区资料**：博客和聚合文档统一作为 E5 定位材料，不支持确定性结论。

Fact Ledger 必须填写 Evidence type。只有源码或第三方材料时，不得生成高置信度公共契约结论；继续寻找 Android Developers 或 Apple Developer 的 API Reference、Guide、Sample，找不到则标 `pending`。

声明某平台“缺失/不支持”前，至少完成 API Reference 和 Guide 检索，并在来源表记录检索入口、检索词、版本和结果。

## 3. 按 API 类别路由

| 类别 | Android 官方入口 | iOS 官方入口 | 重点补充资料 |
|---|---|---|---|
| 事件与输入 | Android Developers `develop/ui`、`reference/android/view`、Compose input | Apple Developer SwiftUI input、UIKit event handling | 分发、焦点、设备输入、测试注入 |
| 手势 | Compose gesture、`GestureDetector`、View gesture guides | SwiftUI `Gesture`、UIKit gesture recognizers | 状态机、竞争/并行、取消和阈值 |
| 组件 | Compose component、Views/widgets、Material | SwiftUI views、UIKit controls/views、Human Interface Guidelines | 生命周期、数据更新、可访问性、平台规范 |
| 布局 | Compose layout、ViewGroup/layout guides | SwiftUI layout、Auto Layout、UIKit containers | 约束、测量、窗口和设备形态 |
| 状态与动画 | Compose state/animation、Android animation | SwiftUI state/animation、UIKit/Core Animation | 中断、完成、时间曲线、执行模型 |
| 可访问性 | Android accessibility API 和 guides | Apple accessibility API、UIKit/SwiftUI accessibility | 默认语义、焦点、动作和测试 |
| 工具与测试 | Compose UI test、Espresso、Layout Inspector | XCTest/XCUITest、Accessibility Inspector、Instruments | 注入、回放、可观测性和性能工具 |

检索时从与目标 API 同层级的框架入口开始，再补充另一套框架。不要为了三平台形式对称，把不同层级的 API 压成一个直接等价项。

### 键盘快捷键路径

- ArkUI：公共锚点为 `CommonMethod.keyboardShortcut`。签名和 availability 取 `interface_sdk-js`；焦点与有效作用域继续查锁定版本官方 docs 仓库的 `zh-cn|en/application-dev/reference/apis-arkui/arkui-ts/ts-universal-events-keyboardshortcut.md`，分别记录窗口焦点、组件焦点/可见性/组件树成员、disabled 和重复组合键规则的实际文档结论。InputKit `inputConsumer` 属于另一套输入订阅/热键路径，只能补充比较，不能把 Analysis Brief 的锚点改成它。
- Android：Path Check 必须逐行展示 `Activity.onKeyShortcut`、`View.dispatchKeyShortcutEvent`、`Activity.onProvideKeyboardShortcuts`、menu shortcut 和 Compose key input 的到达/分发或发布路径、角色与有效作用域；明确排除 `ShortcutManager`，因为它管理 launcher/deep-link shortcut。只列符号或只解释最终选中的一个回调都不合格。
- iOS：检查 `UIKeyCommand` availability、创建/注册方式，并解释命令如何经 `UIResponder` responder chain 与 command/menu 路径被发现或分发、作用域落在何处；只写“注册到 keyCommands”不算完成。
- 先用官方 Reference/Guide 建立 Path Check Fact，再分配 direct/functional/composite 等类型。压缩回答也必须先展示 Path Check，不能把解释放在 Comparator Map 之后。

### 显式动画路径

- ArkUI：分别检查 `animateTo`、`AnimateParam`、`keyframeAnimateTo`、curve helpers 和需要控制句柄时的替代 API。
- ArkUI curve helpers 不能合并描述：从 `@ohos.curves.d.ts` 分别记录 `cubicBezierCurve`、`stepsCurve`、`springCurve`、`springMotion`、`responsiveSpringMotion`、`interpolatingSpring` 的签名、参数默认值/单位、`@since` 和废弃状态。
- Android View：将 `ValueAnimator`、`ObjectAnimator`、`AnimatorSet` 分开检查其 keyframe、listener、cancel/end、pause/resume、seek、repeat/reverse 和 availability；Compose 分别检查 `animate*AsState`、`Animatable`、`Transition`、`keyframes`、`repeatable/infiniteRepeatable` 和 spring/velocity。
- iOS：将 `UIView.animate`、`UIViewPropertyAnimator`、`UIView.animateKeyframes`、`CABasicAnimation`、`CAKeyframeAnimation`、`CASpringAnimation`、`CAAnimationGroup` 和 CAMediaTiming 分开检查；不要把某一个 API 的默认值推广到整个平台。
- 对 `analysis-dimensions.md` 要求的每项动画规格，按独立 comparator 路由到官方入口并逐格取证；Version/Fallback Matrix 的输出位置以 `report-template.md` 为准。
- 曲线路由：Android View 使用 `PathInterpolator` 核实 cubic-Bezier，并用 `TimeInterpolator`/keyframe 检查 steps 组合；Compose 分别核实 `CubicBezierEasing` 和 snap/keyframes/custom Easing；UIKit 核实 `UICubicTimingParameters` 与 keyframe discrete mode；Core Animation 核实 `CAMediaTimingFunction` 与 `CAKeyframeAnimation.calculationMode`。
- Compose `tween` 必须继续核对 `DefaultDurationMillis` 的具体值、`durationMillis`/`delayMillis` 的毫秒单位与默认值，以及默认 `FastOutSlowInEasing`；API Reference 仅显示常量名时，用锁定 Compose 版本的 Google Maven official sources artifact 补齐常量值。
- Core Animation 必须打开 `CAMediaTiming.duration` 子页面核对秒单位和默认值，并打开 `CAKeyframeAnimation.calculationMode` 与 Value calculation modes 核对默认 `.linear`/`kCAAnimationLinear` 以及离散 `.discrete`/`kCAAnimationDiscrete`。这些官方子页面可访问或已缓存时不得保留为 `pending`。

### List 无障碍路径

- ArkUI 公共符号先完成独立 availability 表：`List`、`ListItem`、`ListItemGroup`、`Scroller`、`ListScroller`、`lanes`、`cachedCount`、`sticky`、`chainAnimation`、`editMode` 与当前编辑路径逐项记录 introduction/deprecation、Fact ID 和定义位置；不得用 `ListScroller` 替代 `Scroller`，也不得用组件 availability 推断其属性 availability。
- 对 `analysis-dimensions.md` 定义的五框架能力矩阵逐列取证；nested scrolling 重点查公开入口/组合路径、方向或父子协调语义，未闭环时保留已检查入口并标 `pending`。
- ArkUI：核对 List/ListItem 的默认语义是否由公共定义明确给出，并补充通用 accessibility/focus/action API；未明确的默认值标 pending。
- RecyclerView 与 Compose：分别核对 CollectionInfo/item info、focus、scroll/select/custom action 和测试语义。
- UITableView 与 SwiftUI List：分别核对默认 cell/collection 语义、`allowsFocus`/focus 行为、标准或自定义 accessibility actions；使用 `UITableView`、Focus API、`UIAccessibilityCustomAction` 和 SwiftUI accessibility 官方入口。即使默认行为待核，也必须逐框架列出 focus/actions 状态和来源。
- 测试与工具不得只写一个框架：为 ArkUI、RecyclerView、Compose lazy list、UITableView、SwiftUI List 分别核对官方自动化测试中的节点/标识定位、滚动与动作注入，无障碍检查工具，以及布局/性能诊断入口。未找到精确 List 专项入口时列出已检查的通用官方工具并标 `pending`，不能省略该框架。

## 4. 官方站点与版本记录

- Android：`developer.android.com/reference`、`developer.android.com/develop/ui`、`developer.android.com/jetpack/androidx/releases/compose`。
- iOS/iPadOS：`developer.apple.com/documentation`，按 SwiftUI、UIKit、Core Animation、Accessibility、XCTest 等框架进入。

每个对标接口记录：精确符号、框架、API Level/系统 availability、Compose 或 SDK 版本、查询日期和文档章节。不得混用预览、未发布或不同版本接口。

官方网页无法通过交互浏览器读取时，在任务缓存目录使用可审计的 HTTP 回退，不要直接转向博客：

```bash
mkdir -p "${TASK_CACHE}"
curl -L --retry 2 -A "Mozilla/5.0" "<ANDROID_DEVELOPERS_URL>?hl=en" -o "${TASK_CACHE}/android-page.html"
curl -L --retry 2 -A "Mozilla/5.0" "https://developer.apple.com/tutorials/data/documentation/<DOCC_PATH>.json" -o "${TASK_CACHE}/apple-doc.json"
```

```powershell
$taskCache = '<TASK_CACHE>'
New-Item -ItemType Directory -Force -Path $taskCache | Out-Null
$headers = @{ 'User-Agent' = 'Mozilla/5.0' }
Invoke-WebRequest -UseBasicParsing -Headers $headers -Uri '<ANDROID_DEVELOPERS_URL>?hl=en' -OutFile (Join-Path $taskCache 'android-page.html')
Invoke-WebRequest -UseBasicParsing -Headers $headers -Uri 'https://developer.apple.com/tutorials/data/documentation/<DOCC_PATH>.json' -OutFile (Join-Path $taskCache 'apple-doc.json')
```

- Android 优先请求具体 API Reference 或 Guide 页面，不从站点首页判断可访问性。
- Apple API Reference 页面为 JavaScript 外壳时，使用同一 `developer.apple.com` 域名下的 DocC JSON；它仍是 Apple 官方文档证据。
- 缓存文件只用于当前任务取证，不复制进 Skill 或用户项目。
- 页面与结构化入口均失败时，记录 URL、HTTP/网络错误和尝试时间，再将事实标 `待核`。

## 5. 交叉检索清单

- [ ] 在平台 API Reference 检索对应符号、同义词和相关类型。
- [ ] 在平台 Guide 检索相关行为、生命周期和限制。
- [ ] 检索过功能等价、组合实现和替代路径。
- [ ] 记录排除的名称相似 API及其层级或语义不匹配原因。
- [ ] 区分“官方明确无此能力”和“当前版本官方资料中未找到”。
- [ ] 记录检索词、入口、版本、结果和 Comparator Map 类型。
- [ ] 官方页面读取失败时尝试具体页面 HTTP 缓存或 Apple DocC JSON，并记录结果。

## 6. 独立取证规则

分别完成 Android 和 iOS Fact Ledger 后再填能力矩阵。取证记录只写平台事实，不提前使用“比 ArkUI 更强/更弱”等比较级措辞。官方资料冲突时保留双方来源并转入待核，不静默选择其中一个版本。
