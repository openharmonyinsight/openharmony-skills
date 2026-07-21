# Platform Source Routing / 对标平台官方资料路线

取 Android / iOS 对标接口时，按本路线检索，保证**同口径、同版本**与**声明缺失前的双向交叉检索**。

## 证据优先级（高→低）
1. **官方 API Reference**（接口签名、参数、availability/`@since`）——最高权威。
2. **官方指南（Guide）**（行为、生命周期、分发流程）。
3. **官方示例 / Sample**。
4. **平台源码**（AOSP / Swift SDK）——仅佐证实现，不作 availability 结论。
5. 社区/博客——**不作**能力有无或规格结论的依据。

> 规则：声明某平台"缺失/不支持"前，必须完成 1→2 的双向检索（API Reference + Guide），并在来源表记录检索过的入口与版本。

## 输入事件类：Android 入口
- **Compose（首选）**：`developer.android.com/jetpack/androidx/compose` → Pointer/Key input：`PointerInputScope`/`detectTapGestures`/`detectDragGestures`、`Modifier.onKeyEvent`/`onPreviewKeyEvent`、`PointerEvent`/`PointerType`。记录 Compose BOM 版本。
- **framework Reference（必要时）**：`developer.android.com/reference` → `android.view.MotionEvent`、`android.view.KeyEvent`、`View.onTouchEvent/onKeyDown/onKeyShortcut`、`View.onProvideKeyboardShortcuts`、`android.content.pm.ShortcutManager`（**注意：launcher 启动快捷方式，非键盘**）、Menu `alphabeticShortcut`+modifier。
- **Guide**：`developer.android.com/develop/ui` → Touch/Input、Keyboard shortcuts、Gestures。

## 输入事件类：iOS 入口
- **SwiftUI（首选）**：`developer.apple.com/documentation/swiftui` → `.onTapGesture`、`DragGesture`/`MagnificationGesture`、`.onKeyPress`（iOS 17+）、`Gesture` 优先级（`simultaneously`/`highPriority`）。
- **UIKit（必要时）**：`developer.apple.com/documentation/uikit` → `UIResponder`（`touchesBegan/Moved/Ended/Cancelled`、`pressesBegan/pressesEnded`）、`UITouch`（`phase`/`location(in:)`/`force`/`tapCount`/`altitudeAngle`/`azimuthAngle`）、`UIEvent`（**`coalescedTouches(for:)`/`predictedTouches(for:)`**）、`UIKeyCommand` + `UIMenu`（应用级键盘快捷键）、`UIGestureRecognizer` 体系。
- **Guide**：`developer.apple.com/documentation/uikit` → Touches/Presses/Gestures。

## 版本记录
每个对标接口在来源表记录：availability（`@since`/API Level/iOS 版本）、查询日期、章节。不得混用未发布/不同版本接口。

## 交叉检索清单（声明"缺失/独有"前）
- [ ] 在该平台 API Reference 检索过对应符号/能力（记录检索词与版本）。
- [ ] 在该平台 Guide 检索过相关行为章节。
- [ ] 检索过等价替代路径（若无直接对应）。
- [ ] 结论区分"官方明确无此能力" vs "未在当前版本检索到（待核）"。
