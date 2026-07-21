# Eval: 应用级快捷键 / App-level shortcut keys

## Prompt（测试输入）

> 分析 ArkUI **应用级快捷键**的实现，对标 Android 和 iOS 的应用级快捷键能力。

跑两遍：**with skill**（加载本 skill）与 **without skill**（不加载），对比产出。

## 预期关键发现 / Expected findings（with skill 必须命中）

- [ ] **锁定作用域 = 应用级**：报告标题、规格、结论显式围绕"应用级 / app-scope 全局热键"，**未降级**为通用或组件级快捷键。
- [ ] **应用级实现三平台都覆盖**：
  - ArkUI：窗口级 / 菜单级（`MenuItem.labelInfo` 仅提示）；**不是**只讲组件 `onKeyEvent`。
  - Android（**键盘**快捷键）：`Activity.onKeyShortcut` / `onProvideKeyboardShortcuts` / Menu keyboard shortcuts（`alphabeticShortcut`+modifier）/ `dispatchKeyShortcutEvent` / Compose key input。
  - iOS：**`UIKeyCommand`**（responder/command chain 注册，app 级生效）。
- [ ] **勿混淆**：`ShortcutManager` 是 launcher **启动快捷方式**（长按图标），**不是**键盘 accelerator，不作为键盘快捷键对标。
- [ ] **区分层级**：明确区分应用级 vs 组件级（`onKeyEvent`/`onKeyDown`/`pressesBegan`）vs 系统级（OS 全局热键），并说明本次只分析应用级。
- [ ] **规格精度**：修饰键（Ctrl/Alt/Shift/Cmd）与键码表达、`@since` 版本、各平台差异。
- [ ] **格式**：每平台规格用结构化列表（不压单行）；附每平台 1 段最小用法示例代码。
- [ ] **来源**：ArkUI 侧以 `interface_sdk-js` 为准；具体 API 名若不确定标注"待核"，不臆造。
- [ ] **迁移/结论**：给出从 Android/iOS 应用级快捷键迁到 ArkUI（或反向）的路径与缺口。

## 通过标准 / Pass criteria

- with skill：上述清单全部命中，**尤其"未降级 + 三平台应用级实现都覆盖"两条**。
- without skill 对比：典型会降级成"组件级 key event / 普通快捷键"，漏掉 `UIKeyCommand` / `ShortcutManager` / ArkUI 窗口级，证明 skill 的价值。

## 备注 / Notes

- 与 `onTouch.md`（触摸事件类）互补，验证 skill 在**带作用域层级**能力上的可靠性。
- 若需进一步验证层级纪律，可改 Prompt 为"**组件级**快捷键"，确认报告转而只覆盖组件级、不混入应用级。
