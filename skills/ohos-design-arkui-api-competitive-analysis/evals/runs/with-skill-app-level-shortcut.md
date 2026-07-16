# With-skill run: 应用级快捷键 / App-level shortcut keys

> 作用域**锁定在应用级**（按 SKILL.md Initial Checks 第 2 步「勿降级」）。组件级 / 系统级仅在"层级区分"中作为对照提及，不展开。ArkUI 侧 API 以 `interface_sdk-js` / 官方文档为准，不确定处标 `待核`。

## 0. Meta

| 项 | 值 |
|---|---|
| 分析对象 | **应用级**快捷键（app 内全局生效，无论焦点） |
| 作用域层级 | 应用级 / App-level（用户指定，未降级） |
| ArkUI 权威源 | `interface_sdk-js` / 官方文档（`MenuItem`、`UIContext.onKeyEvent`、`ohos.multimodalInput.inputConsumer`） |
| Android 对照 | menu accelerator / `onKeyShortcut` / Activity `onKeyDown` |
| iOS 对照 | **`UIKeyCommand`** + `UIMenu` |
| API 类别 | 事件类·按键（应用级）；高权重维度：2·3·5·10·11 |

## 1. 规格速览（仅应用级）

### ArkUI —— 命令式，窗口级监听（无声明式 app 快捷键注册）
- **应用级实现**：**窗口级 `UIContext.onKeyEvent`**（app 窗口范围按键回调，`待核 @since`，查 interface_sdk-js 确认）。自行匹配 `(keyCode + 修饰键 Ctrl/Alt/Shift)` 来识别快捷键。
- **菜单提示**：`MenuItem.labelInfo`（API 9+）只显示快捷键提示文字（如 "Ctrl+S"），**不响应按键**，需配合窗口监听。
- **组件级（不展开，仅对照）**：`onKeyEvent`（CommonMethod，API 7+），聚焦组件内。
- **系统级（普通应用不可用）**：`ohos.multimodalInput.inputConsumer`（系统快捷键，系统应用接口）。

### Android —— 菜单 accelerator + Activity 级监听
- **应用级实现**：菜单项 accelerator（`MenuItem` 的 `setShortcutAlphabeticModifier`/`Ctrl+` 快捷键，经菜单分发命中）；或 Activity `onKeyDown/onKeyShortcut` 在 Activity 层统一处理。
- **修饰键/键码**：`KeyEvent.keyCode` + `KeyEvent.isCtrlPressed/isAltPressed/...`。
- **声明式程度**：菜单 shortcut 半声明式；纯 app 内全局热键无统一声明式 API，多靠 Activity 监听。

### iOS —— 声明式 `UIKeyCommand`（最贴近"应用级快捷键"心智）
- **应用级实现**：**`UIKeyCommand(input:modifiers:action:)`**，在 `UIResponder`/`UIViewController` 的 `keyCommands` 注册；沿 responder chain 命中，**app 窗口激活时全局生效**（不依赖某组件聚焦）。可配合 `UIMenu` 显示。
- **修饰键/键码**：`UIKeyCommand.input`(字符) + `UIKeyModifierFlags`(.control/.command/.alternate/.shift)。
- **macOS Catalyst / iPadOS 硬键盘**：同 `UIKeyCommand` 体系。

### 用法示例（每平台 1 段，应用级）
```ts
// ArkUI —— 窗口级 onKeyEvent 监听 + 自行匹配修饰键（应用级，命令式）
this.getUIContext().onKeyEvent((event?: KeyEvent) => {   // UIContext.onKeyEvent, 待核 @since
  if (event && event.type === KeyType.Down
      && event.keyCode === KeyCode.KEY_S && event.ctrlKey) {
    save();   // Ctrl+S
  }
})
```
```kotlin
// Android —— Activity 级监听应用级快捷键
override fun onKeyDown(keyCode: Int, e: KeyEvent): Boolean {
  if (keyCode == KeyEvent.KEYCODE_S && e.isCtrlPressed) { save(); return true }
  return super.onKeyDown(keyCode, e)
}
```
```swift
// iOS —— 声明式 UIKeyCommand（应用级，responder chain 命中）
override var keyCommands: [UIKeyCommand]? {
  [UIKeyCommand(input: "s", modifierFlags: .control, action: #selector(save))]
}
```

## 2. 能力对比矩阵（应用级）

| 维度 | ArkUI | Android | iOS |
|---|---|---|---|
| 声明式 app 快捷键注册 | ❌ 命令式（窗口监听+自匹配） | ⚠️ 半声明式（menu shortcut） | ✅ `UIKeyCommand` |
| 默认作用域 | app 窗口 | Activity/Window | responder chain（app-scope） |
| 修饰键+键码表达 | `keyCode`+`ctrlKey/altKey/...` | `keyCode`+`isCtrlPressed/...` | `input`+`UIKeyModifierFlags` |
| 菜单提示联动 | `MenuItem.labelInfo`(仅提示) | `MenuItem` shortcut(提示+命中) | `UIMenu`+`UIKeyCommand` |
| 冲突/优先级 | 自行管理 | 菜单分发 | responder chain + `canPerformAction` |
| 系统级全局热键 | `inputConsumer`(系统应用 only) | 无通用 app 全局 | Carbon `RegisterEventHotKey`(平台特定) |

## 3. 关键差异点
- **声明式 vs 命令式**：ArkUI 应用级快捷键是**命令式**（窗口级监听 + 自建匹配），无 `UIKeyCommand` 式声明式注册；iOS 最声明式；Android 居中。
- **菜单联动**：ArkUI `MenuItem.labelInfo` 仅提示、不响应（易踩坑）；Android/iOS 菜单 shortcut 既提示又命中。
- **系统级**：三平台都不对普通应用开放 OS 全局热键（ArkUI `inputConsumer` 限系统应用）。
- **心智差异大**：从 iOS 迁 ArkUI 需把"声明 UIKeyCommand"改写为"窗口监听 + 手动 keyCode+修饰键匹配 + 维护映射表"。

## 4. 结论与迁移
- **能力覆盖**：应用级快捷键三平台都可实现；ArkUI 缺声明式注册、菜单不联动响应，是主要 gap。
- **对齐建议**：① 文档明确"应用级 = 窗口级 onKeyEvent + 自匹配"，区分组件级/系统级；② 标注 `MenuItem.labelInfo` 仅提示；③ 评估是否补声明式 app 快捷键 API 对齐 iOS/Compose。
- **迁移**：iOS `UIKeyCommand` → ArkUI 窗口级 `onKeyEvent` + 映射表；Android menu shortcut → ArkUI `Menu`+`labelInfo`+窗口监听。

## 5. 附录（来源）
- ArkUI：`interface_sdk-js`（`MenuItem`、`UIContext.onKeyEvent`、`ohos.multimodalInput.inputConsumer`）+ 官方文档 `ts-basic-components-menuitem`、`ts-universal-events-key`
- Android：`android.view.KeyEvent`、`MenuItem` shortcut、`onKeyShortcut`
- iOS：`UIKeyCommand`、`UIMenu`、`UIResponder`
> 注：`UIContext.onKeyEvent` 的 `@since` 与确切签名待在 interface_sdk-js 核实（标注 `待核`，未臆断）。
