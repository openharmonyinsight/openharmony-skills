# inputMethod 模块测试模式（管理侧）

> **模块信息**
> - 所属：IMEKit / 输入法管理（IMM）
> - SDK 声明：`@ohos.inputMethod.d.ts`（since 6 dynamic / 23 static）
> - 加载时机：Phase 5 生成 InputMethodController/InputMethodSetting/系统管理 API 测试时
> - 依赖：`_common.md`（错误码体系）
> - 特点：管理侧 API 在 TestAbility 进程直接调用（无需跨进程桥接），用 PARAM/ERROR/RETURN 类型即可

---

## 一、InputMethodController 测试（自绘编辑框侧）

### 1.1 方法清单

| 方法 | 异步 | @throws | since | 测试类型 |
|------|------|---------|-------|---------|
| `attach(showKeyboard, textConfig, cb)` | callback | 401、12800003、12800008 | 10 | PARAM |
| `attach(showKeyboard, textConfig)` | promise | 401、12800003、12800008 | 10 | PARAM |
| `attach(showKeyboard, textConfig, reason)` | promise | 401、12800003、12800008 | 15 | PARAM |
| `showTextInput(cb)` / `showTextInput()` | cb/promise | 12800003、12800008、12800009 | 10 | RETURN |
| `hideTextInput(cb)` / `hideTextInput()` | cb/promise | 12800003、12800008 | 10 | RETURN |
| `detach(cb)` / `detach()` | cb/promise | 12800003 | 10 | RETURN |
| `updateCursor(cursorInfo, cb)` / `updateCursor(cursorInfo)` | cb/promise | 401、12800003 | 10 | PARAM |
| `changeSelection(textSelection, cb)` / `changeSelection(textSelection)` | cb/promise | 401、12800003 | 10 | PARAM |
| `updateAttribute(attribute, cb)` / `updateAttribute(attribute)` | cb/promise | 401、12800003 | 10 | PARAM |
| `stopInputSession(cb)` / `stopInputSession()` | cb/promise | 12800003 | 10 | RETURN |

### 1.2 测试模式（同进程直接调用）

```typescript
it('Sub_InputMethod_IMC_attach_0100', ..., async (done: Function) => {
  let controller = inputMethod.getController();
  try {
    await controller.attach(true, {
      inputAttribute: { inputPattern: 0, enterKeyType: 0 }
    });
    expect(true).assertTrue();
  } catch (err) {
    expect(err.code).assertEqual(12800003);  // 无编辑框获焦时预期
  }
  done();
});
```

### 1.3 反例场景

| API | 反例输入 | 期望错误码 |
|-----|---------|-----------|
| `attach(true, null)` | textConfig=null | 401 |
| `attach(true, {})` | 缺 inputAttribute | 401 |
| `updateCursor(null)` | cursorInfo=null | 401 |
| `changeSelection(null)` | textSelection=null | 401 |
| `updateAttribute(null)` | attribute=null | 401 |
| `showTextInput()`（无 attach） | 未绑定 | 12800003/12800009 |
| `detach()`（未 attach） | 未绑定 | 12800003 |

---

## 二、InputMethodSetting 事件订阅测试

### 2.1 方法清单

| 方法 | @throws | since | 测试类型 |
|------|---------|-------|---------|
| `on('imeChange', cb)` / `off('imeChange', cb?)` | 无 | 9 | EVENT |
| `on('imeShow', cb)` / `off` (@systemapi) | on: 202 | 10 | EVENT |
| `on('imeHide', cb)` / `off` (@systemapi) | on: 202 | 10 | EVENT |
| `isPanelShown(panelInfo)` (@systemapi) | 202、401、12800008 | 11 | RETURN |
| `listInputMethodSubtype(property, cb)` / `listInputMethodSubtype(property)` | 401、12800001、12800008 | 9 | RETURN |
| `listCurrentInputMethodSubtype(cb)` / `listCurrentInputMethodSubtype()` | 12800001、12800008 | 9 | RETURN |
| `getInputMethods(enable, cb)` / `getInputMethods(enable)` | 401、12800001、12800008 | 9 | RETURN |
| `getInputMethodsSync(enable)` | 401、12800001、12800008 | 11 | RETURN |
| `getAllInputMethods(cb)` / `getAllInputMethods()` | 12800001、12800008 | 11 | RETURN |
| `getAllInputMethodsSync()` | 12800001、12800008 | 11 | RETURN |
| `getInputMethodState()` | 12800004、12800008 | 15 | RETURN |
| `enableInputMethod(bundle, ext, state)` (@systemapi) | 201、202、12800008、12800018、12800019 | 20 | ERROR |

### 2.2 imeChange 事件测试

```typescript
let setting = inputMethod.getSetting();
let count = 0;
setting.on('imeChange', (property, subtype) => {
  setting.off('imeChange');
  count += 1;
});
// 切换输入法触发
await inputMethod.switchCurrentInputMethodSubtype(newSubtype);
setTimeout(() => {
  expect(count).assertEqual(1);
  done();
}, 2000);
```

### 2.3 系统API权限测试

`on('imeShow'/'imeHide')`、`isPanelShown`、`enableInputMethod` 标注 @systemapi：
- 非系统应用调用期望 202
- 系统应用需申请 `ohos.permission.CONNECT_IME_ABILITY`

---

## 三、系统管理 API 测试

### 3.1 方法清单

| 方法 | @throws | since | 权限 |
|------|---------|-------|------|
| `getSetting()` | 12800007 | 9 | — |
| `getController()` | 12800006 | 9 | — |
| `getCurrentInputMethod()` | 无 | 9 | — |
| `getCurrentInputMethodSubtype()` | 无 | 9 | — |
| `getDefaultInputMethod()` | 12800008 | 11 | — |
| `switchInputMethod(target, cb)` / `switchInputMethod(target)` | 201、401、12800005、12800008 | 9 | CONNECT_IME_ABILITY |
| `switchCurrentInputMethodSubtype(target, cb)` / `switchCurrentInputMethodSubtype(target)` | 201、401、12800005、12800008 | 9 | 同上 |
| `switchCurrentInputMethodAndSubtype(prop, subtype, cb)` / `...(prop, subtype)` | 201、401、12800005、12800008 | 9 | 同上 |
| `switchInputMethod(bundleName, subtypeId?)` | 201、202、401、12800005、12800008 | 11 | 同上(@systemapi) |
| `setSimpleKeyboardEnabled(enable)` | 无 | 20 | — |
| `onAttachmentDidFail(cb)` / `offAttachmentDidFail(cb?)` | 无 | 22 | — |

### 3.2 权限测试模式

```typescript
// 201 权限不足反例（撤销权限后调用）
it('Sub_InputMethod_switchInputMethod_noPermission_0100', ..., async (done) => {
  // 确保未授权 CONNECT_IME_ABILITY 的环境
  try {
    await inputMethod.switchInputMethod(targetProperty);
    expect().assertFail();  // 不应成功
  } catch (err) {
    expect(err.code).assertEqual(201);
  }
  done();
});
```

### 3.3 switchCurrentInputMethodSubtype 测试（ExtensionAbility 拉起）

此方法用于拉起测试用 ExtensionAbility（详见 `extension_ability.md` §3）：

```typescript
let testSubtype = {
  id: 'inputStageService',
  label: '', name: 'com.acts.inputmethodengine.test',
  mode: 'lower', locale: '', language: '', icon: '', iconId: 0, extra: {}
};
let result = await inputMethod.switchCurrentInputMethodSubtype(testSubtype);
expect(result).assertTrue();  // 切换成功返回 true
```

---

## 四、InputMethodSubtype 数据结构测试

### 4.1 属性清单

| 属性 | 类型 | 必填 | since |
|------|------|------|-------|
| `label` | string | 可选 | 9 |
| `labelId` | double | 可选 | 10 |
| `name` | string | 必填 | 9 |
| `id` | string | 必填 | 9 |
| `mode` | 'upper'\|'lower' | 可选 | 9 |
| `locale` | string | 必填（ICU Locale 如 'zh-CN'） | 9 |
| `language` | string | 必填（如 'zh'/'en'） | 9 |
| `icon` | string | 可选 | 9 |
| `iconId` | double | 可选 | 9 |
| `extra` | object | 可选 | 9 |

### 4.2 测试模式

```typescript
// 从 getCurrentInputMethodSubtype 获取实例验证属性类型
let subtype = inputMethod.getCurrentInputMethodSubtype();
expect(typeof subtype.name).assertEqual('string');
expect(typeof subtype.id).assertEqual('string');
expect(typeof subtype.locale).assertEqual('string');
expect(typeof subtype.language).assertEqual('string');
```

### 4.3 动态构造 vs 静态配置

- **动态构造**（历史用例方式）：在 beforeAll 中构造 subtype 对象调用 switchCurrentInputMethodSubtype
- **静态配置**（官方推荐）：module.json5 metadata + input_method_config.json 配置 subtypes 数组

---

## 五、inputMethodListDialog 组件测试

### 5.1 组件信息

- 模块：`@ohos.inputMethodList`（since 11）
- 类型：`@CustomDialog` 声明式组件
- 构造：`InputMethodListDialog({controller, patternOptions?})`

### 5.2 测试模式

```typescript
let dialogController = new CustomDialogController({
  builder: InputMethodListDialog({
    patternOptions: {
      defaultSelected: 0,
      patterns: [
        { icon: $r('app.media.icon1'), selectedIcon: $r('app.media.icon1_s') },
        { icon: $r('app.media.icon2'), selectedIcon: $r('app.media.icon2_s') }
      ],
      action: (index: number) => { /* 切换回调 */ }
    }
  })
});
dialogController.open();
// 验证对话框显示
```

---

## 六、inputMethodSystemPanelManager 测试

### 6.1 模块信息

- 模块：`@ohos.inputMethodSystemPanelManager`（since 26.0.0）
- 注解：`@systemapi` + `@stagemodelonly`（全部接口）
- 权限：`connectSystemChannel` 需 `ohos.permission.CONNECT_IME_ABILITY`

### 6.2 方法清单

| 方法 | @throws | 测试类型 |
|------|---------|---------|
| `onSystemPrivateCommand(cb)` / `offSystemPrivateCommand(cb?)` | 202 | EVENT |
| `onSystemPanelStatusChange(cb)` / `offSystemPanelStatusChange(cb?)` | 202 | EVENT |
| `sendPrivateCommand(data)` | 202、12800026 | ERROR |
| `connectSystemChannel()` | 201、202、12800008、12800026 | RETURN |

### 6.3 测试要点

- 全部接口 @systemapi，非系统应用期望 202
- `connectSystemChannel` 需 CONNECT_IME_ABILITY 权限，无权限期望 201
- `sendPrivateCommand` 在系统面板未连接时期望 12800026

---

## 七、ExtraConfig 测试

- 模块：`@ohos.inputMethod.ExtraConfig`（since 22）
- 接口：`InputMethodExtraConfig`（`customSettings: Record<string, CustomValueType>`）
- 类型：`CustomValueType = int | string | boolean`
- 测试：通过 EditorAttribute.extraConfig 获取实例验证属性
