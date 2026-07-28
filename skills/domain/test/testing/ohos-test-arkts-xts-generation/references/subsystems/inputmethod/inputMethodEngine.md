# inputMethodEngine 模块测试模式

> **模块信息**
> - 所属：IMEKit / 输入法引擎核心
> - SDK 声明：`@ohos.inputMethodEngine.d.ts`（since 8 dynamic / 23 static）
> - 加载时机：Phase 5 生成 InputMethodAbility/InputClient/KeyboardController/KeyboardDelegate/Panel 测试时
> - 依赖：`extension_ability.md`（ExtensionAbility 个性）、`_common.md`（错误码体系）

---

## 一、InputMethodAbility 事件订阅测试

### 1.1 事件清单（dynamic + static 两套）

| 事件 | dynamic 风格 | static 风格 | since | @throws |
|------|-------------|------------|-------|---------|
| 输入开始 | `on('inputStart', cb)` | `onInputStart(cb)` | 9 | 无 |
| 输入停止 | `on('inputStop', cb)` | `onInputStop(cb)` | 9 | 无 |
| 键盘显示 | `on('keyboardShow', cb)` | `onKeyboardShow(cb)` | 9 | 无 |
| 键盘隐藏 | `on('keyboardHide', cb)` | `onKeyboardHide(cb)` | 9 | 无 |
| 子类型变更 | `on('setSubtype', cb)` | `onSetSubtype(cb)` | 9 | 无 |
| 安全模式 | `on('securityModeChange', cb)` | `onSecurityModeChange(cb)` | 11 | 无 |
| 私有命令 | `on('privateCommand', cb)` | `onPrivateCommand(cb)` | 12 | 12800010 |
| 显示变更 | `on('callingDisplayDidChange', cb)` | `onCallingDisplayDidChange(cb)` | 18 | 801 |
| 丢弃文本 | `on('discardTypingText', cb)` | `onDiscardTypingText(cb)` | 20 | 无 |

### 1.2 测试模式（CROSS_PROCESS / event_subscribe 子场景）

```typescript
// 计数器 + setTimeout 等待
let count = 0;
inputMethodAbility.on('keyboardShow', () => {
  inputMethodAbility.off('keyboardShow');  // 一次性消费
  count += 1;
});
// 触发动作
await keyboardController.hide();
await driver.findComponent(ON.type('TextArea')).click();  // 重新拉起键盘
let t = setTimeout(() => {
  if (count === 1) { commonEventPublishData = { data: "SUCCESS" }; }
  commoneventmanager.publish(resultEvent, commonEventPublishData, ...);
  clearTimeout(t);
}, 2000);
```

### 1.3 其他方法

| 方法 | @throws | 测试要点 |
|------|---------|---------|
| `getSecurityMode()` | 12800004 | 返回 SecurityMode 枚举值验证 |
| `createPanel(ctx, info, cb)` | 401、12800004 | 正向 + null/undefined 反例（见 §5） |
| `destroyPanel(panel, cb)` | 401 | 正向 + null 反例 |

---

## 二、InputClient 文本操作三态覆盖

### 2.1 三态覆盖矩阵

每个方法必须覆盖 **Callback + Promise + Sync** 三种形态：

| 方法 | @throws | 边界值建议 |
|------|---------|-----------|
| `sendKeyFunction(action)` | 401、12800003 | action=0/负数/超大值 |
| `deleteForward(length)` | 401、12800002、12800003 | length=0/负数/超长（>文本长度） |
| `deleteBackward(length)` | 401、12800002、12800003 | 同上 |
| `insertText(text)` | 401、12800002、12800003 | 空字符串/超长(10^6)/特殊字符(Unicode/控制字符) |
| `getForward(length)` | 401、12800003、12800006 | length=0/负数/超大 |
| `getBackward(length)` | 401、12800003、12800006 | 同上 |
| `moveCursor(direction)` | 401、12800003 | direction 四方向(CURSOR_UP/DOWN/LEFT/RIGHT)+无效值 |
| `selectByRange(range)` | 401、12800003 | range.start>range.end/负数/超大 |
| `selectByMovement(movement)` | 401、12800003 | movement.direction 四方向 |
| `getEditorAttribute()` | 12800003 | 返回 14 字段类型验证 |
| `getTextIndexAtCursor()` | 12800003、12800006 | 返回值验证 |
| `sendExtendAction(action)` | 401、12800003、12800006 | SELECT_ALL/CUT/COPY/PASTE 四值+无效值 |
| `sendPrivateCommand(data)` | 401、12800003、12800010 | 空对象/超大 Record |
| `getCallingWindowInfo()` | 12800003、12800012、12800013 | 返回 WindowInfo 验证 |
| `setPreviewText(text, range)` | 401、12800003、12800011 | 空字符串/超长/range 越界 |
| `finishTextPreview()` | 12800003、12800011 | 调用后状态验证 |
| `sendMessage(msgId, param?)` | 401、12800003、12800009、12800014、12800015、12800016 | 空msgId/超大ArrayBuffer |
| `recvMessage(handler?)` | 401 | handler=null/缺 onMessage |

### 2.2 三态测试模板

```typescript
// Callback 形态
async testDeleteForwardCallback() {
  let result = await new Promise(resolve => {
    this.inputClient.deleteForward(1, (err, value) => resolve(value));
  });
  // publish result
}

// Promise 形态
async testDeleteForwardPromise() {
  let result = await this.inputClient.deleteForward(1);
  // publish result
}

// Sync 形态（since 10）
testDeleteForwardSync() {
  this.inputClient.deleteForwardSync(1);  // 无返回值，不抛错即成功
  // publish "SUCCESS"
}
```

### 2.3 EditorAttribute 14 字段验证

```typescript
let attr = await this.inputClient.getEditorAttribute();
// 验证字段类型
expect(typeof attr.enterKeyType).assertEqual('number');
expect(typeof attr.inputPattern).assertEqual('number');
expect(typeof attr.isTextPreviewSupported).assertEqual('boolean');
// 可选字段（since 14+）
if (attr.bundleName) expect(typeof attr.bundleName).assertEqual('string');
if (attr.immersiveMode) expect(typeof attr.immersiveMode).assertEqual('number');
// ... windowId/displayId/placeholder/abilityName/capitalizeMode/gradientMode/extraConfig
```

---

## 三、KeyboardController 测试

| 方法 | 异步 | @throws | 测试要点 |
|------|------|---------|---------|
| `hide(callback)` / `hide()` | callback/promise | 12800003 | 隐藏键盘后验证 keyboardHide 事件触发 |
| `exitCurrentInputType(callback)` / `exitCurrentInputType()` | callback/promise | 12800008、12800010 | 非预置输入法场景期望 12800010 |
| `hideKeyboard(cb)` / `hideKeyboard()` | callback/promise | 无（已废弃） | @deprecated since 9，仅兼容测试 |

---

## 四、KeyboardDelegate 事件订阅测试

### 4.1 事件清单

| 事件 | dynamic 风格 | static 风格 | since |
|------|-------------|------------|-------|
| 物理键按下 | `on('keyDown', cb)` | `onKeyDown(cb)` | 8 |
| 物理键抬起 | `on('keyUp', cb)` | `onKeyUp(cb)` | 8 |
| 物理键事件 | `on('keyEvent', cb)` | `onKeyEvent(cb)` | 10 |
| 光标上下文变更 | `on('cursorContextChange', cb)` | `onCursorContextChange(cb)` | 8 |
| 选区变更 | `on('selectionChange', cb)` | `onSelectionChange(cb)` | 8 |
| 文本变更 | `on('textChange', cb)` | `onTextChange(cb)` | 8 |
| 编辑属性变更 | `on('editorAttributeChanged', cb)` | `onEditorAttributeChanged(cb)` | 10 |

> KeyboardDelegate 所有方法 **@throws 均无错误码声明**。

### 4.2 物理键模拟模式（uinput）

```typescript
// 通过 hdc 模拟物理键
await delegator.executeShellCommand('uinput -K -d 2000 -u 2000');  // 按下并抬起 keyCode=2000

// 验证事件序列
inputKeyboardDelegate.on('keyDown', (keyEvent) => {
  inputKeyboardDelegate.off('keyDown');
  if (keyEvent.keyCode === 2000 && keyEvent.keyAction === 2) { count += 1; }
  return true;
});
```

### 4.3 文本/选区事件触发模式

```typescript
// 通过 insertText 制造 textChange 事件流
inputKeyboardDelegate.on('textChange', (text) => {
  if (text === 'expected') { count += 1; }
});
await this.inputClient.insertText('expected');  // 触发
```

---

## 五、Panel 生命周期与操作测试

### 5.1 Panel 方法清单（42 个方法）

| 方法域 | 方法 | @throws |
|--------|------|---------|
| UI 内容 | `setUiContent(path)` / `setUiContent(path, storage)` | 401 |
| 尺寸/位置 | `resize(w,h)` / `moveTo(x,y)` | 401 |
| 显示控制 | `show()` / `hide()` | 无 |
| 事件订阅 | `on('show'/'hide'/'sizeChange'/'sizeUpdate')` / `off` | off: 401 |
| 标志变更 | `changeFlag(flag)` | 401 |
| 隐私模式 | `setPrivacyMode(bool)` | 201、401 |
| 热区调整 | `adjustPanelRect(flag, rect)` / `adjustPanelRect(flag, enhancedRect)` | 401、12800013、12800017 |
| 沉浸模式 | `setImmersiveMode(mode)` / `getImmersiveMode()` | 401、12800002、12800013 |
| 沉浸效果 | `setImmersiveEffect(effect)` | 801、12800002、12800013、12800020、12800021 |
| 屏幕常亮 | `setKeepScreenOn(bool)` | 12800013 |
| 系统面板偏移 | `getSystemPanelCurrentInsets(displayId)` | 12800013、12800017、12800022 |
| 阴影 | `setShadow(radius, color, offsetX, offsetY)` | 202、12800013、12800017 |
| 区域更新 | `updatePanelRect(flag, rect)` / `updatePanelRectSync(flag, rect)` | 12800013、12800017 |

### 5.2 createPanel/destroyPanel 配对测试

```typescript
// 正向配对
let panelInfo = { type: PanelType.SOFT_KEYBOARD, flag: PanelFlag.FLG_FIXED };
inputMethodAbility.createPanel(this.context, panelInfo).then(async (panel) => {
  await panel.setUiContent('pages/Keyboard');
  await panel.show();
  // ... 测试逻辑
  await inputMethodAbility.destroyPanel(panel);
});

// 反例：参数校验
try { inputMethodAbility.createPanel(null, panelInfo, cb); }
catch (err) { if (err.code === 401) { /* 预期 */ } }
```

### 5.3 adjustPanelRect 热区测试（HotArea 模式）

```typescript
let panelInfo = { type: PanelType.SOFT_KEYBOARD, flag: PanelFlag.FLG_FIXED };
inputMethodAbility.createPanel(this.mContext, panelInfo).then(async (panel) => {
  await panel.adjustPanelRect(PanelFlag.FLG_FIXED, panelRect);
  await panel.setUiContent('testability/pages/HotArea');
  await panel.show();
});
```

### 5.4 Panel 事件测试（event_subscribe 子场景）

```typescript
let count = 0;
panel.on('show', () => {
  panel.off('show');
  count += 1;
});
await panel.show();
let t = setTimeout(() => {
  if (count === 1) { commonEventPublishData = { data: "SUCCESS" }; }
  publish(...);
  clearTimeout(t);
}, 1000);
```

---

## 六、历史用例测试点清单

| 测试文件 | 通道 | 被测 API | code 范围 | 断言模式 |
|---------|------|---------|----------|---------|
| `inputMethodAbility.test.ets` | inputMethodAbilityTest | InputClient(callback/promise) + 常量断言 + 事件 | 1~106 | data.data=="SUCCESS" / 常量 assertEqual |
| `inputMethodEngine.test.ets` | inputMethodEngineTest | TextInputClient(旧) + 事件 + exitCurrentInputType | 1~100+ | data.data=="SUCCESS" |
| `inputMethodEngineKey.test.ets` | inputMethodEngineKeyTest | keyEvent 物理键序列 | 10~70 | data.data=="SUCCESS"（uinput 模拟） |
| `InputMethodEngineNew.test.ets` | inputMethodEngineNewTest | Sync三态 + Panel + sendPrivateCommand + sendMessage + setPreviewText | 1~110 | 主要 401 错误码验证 |
| `InputMethodEngineHotArea.test.ets` | inputMethodEngineHotAreaTest | adjustPanelRect + getForward/deleteForward 验证 | 100~200 | data.data=="SUCCESS"（Driver+ON.id） |

### 历史用例覆盖缺口

| API | 缺失场景 | 建议 |
|-----|---------|------|
| insertText | 超长字符串(10^6) | BOUNDARY |
| deleteForward/Backward | length=0/负数 | BOUNDARY |
| Panel.resize | width/height=0/负数 | BOUNDARY |
| Panel.adjustPanelRect | rect 越界/负数 | BOUNDARY |
| setImmersiveMode | 正向测试 | 缺失 |
| getSystemPanelCurrentInsets | 正向测试 | 缺失 |
| on('privateCommand') | 正向测试 | 缺失 |
| on('callingDisplayDidChange') | 正向测试（含 801 防护） | 缺失 |
| on('discardTypingText') | 正向测试 | 缺失 |
