# Eval: 应用级键盘快捷键 / App-level keyboard shortcut

> ArkUI 锚点是 `keyboardShortcut`（声明式组件绑定），**不是**菜单 accelerator、**不是**窗口 `onKeyEvent`。

## Prompt（测试输入）

> 分析 ArkUI **应用级键盘快捷键**的实现，对标 Android 和 iOS 的应用级键盘快捷键能力。

跑两遍：**with skill** 与 **without skill**，对比产出。

## 预期关键发现 / Expected findings（with skill 必须命中）

ArkUI 侧以 `interface_sdk-js` / 官方文档为准，不确定标 `待核`。

- [ ] **锁定到键盘快捷键**：以 ArkUI `keyboardShortcut` 为锚点，**不**混入菜单 accelerator / 窗口 `onKeyEvent`。
- [ ] **ArkUI**：`keyboardShortcut(value: string | FunctionKey, keys: Array<ModifierKey>, action?: () => void): T`（API 10+，原子化 11+）；**声明式组件绑定**；组件未获焦/未展示时，只要挂在获焦窗口组件树上就响应（window/app-scope）。
- [ ] **Android（键盘快捷键）**：`Activity.onKeyShortcut` / `onProvideKeyboardShortcuts` / Menu keyboard shortcuts（`MenuItem` `alphabeticShortcut`+modifier）/ `dispatchKeyShortcutEvent` / Compose key input；**无** ArkUI 那种"声明式组件绑定·未获焦也响应"的直接等价。
- [ ] **iOS**：**`UIKeyCommand`**（声明式·responder/command chain·app 级生效）——与 `keyboardShortcut` 心智最接近。
- [ ] **勿混淆**：`ShortcutManager` 是 launcher **启动快捷方式**（长按图标），**不是**键盘 accelerator，不作为键盘快捷键对标。
- [ ] **区分层级**：应用级（`keyboardShortcut`/`UIKeyCommand`/`onKeyShortcut`）vs 组件级（`onKeyEvent`/`onKeyDown`/`pressesBegan`）vs 系统级（`inputConsumer`/Carbon）。
- [ ] **规格精度**：修饰键（Ctrl/Shift/Alt/Cmd）+ 键码表达、`@since`/availability、各平台差异。
- [ ] **格式**：每平台规格结构化列表 + 每平台 1 段用法代码；断言带来源编号；锁定版本基线。
- [ ] **结论**：`keyboardShortcut`（声明式·window-scope）≈ iOS `UIKeyCommand`；Android 缺直接等价（用 menu shortcut/Activity 监听近似）。

## 通过标准 / Pass criteria

- with skill：上述清单全中，**尤其"以 keyboardShortcut 为锚 + 三平台键盘快捷键覆盖 + ShortcutManager 排除"**。
- without skill 对比：典型会把 ArkUI 侧错写成"窗口 onKeyEvent / 菜单 accelerator"，或把 `ShortcutManager` 当键盘快捷键；证明 skill 价值。

## 备注

- 与 `onTouch.md`（触摸）互补，验证 skill 在**带作用域层级 + 声明式 vs 命令式**能力上的可靠性。
