# 输入法框架（IMEKit）子系统知识库

> **子系统**: MiscServices / IMEKit
> **@syscap**: `SystemCapability.MiscServices.InputMethodFramework`
> **Kit 入口**: `@kit.IMEKit`
> **适用范围**: 输入法应用开发、自绘编辑框、系统输入法管理
> **语法类型**: 同时支持 dynamic（ets1.1）和 static（ets1.2），static 统一 since 23
> **配置层级**: 本文件为核心配置，子模块配置见同级目录其他 .md 文件
> **extension_ability_type**: InputMethodExtensionAbility
> **extension_ability_config**: extension_ability.md

---

## 一、子系统概述

### 1.1 能力范围

IME Kit 建立编辑框所在应用与输入法应用之间的通信通道，提供三类能力：

| 能力分类 | 面向对象 | 核心模块 |
|----------|---------|---------|
| 输入法服务 API | 输入法应用 | `inputMethodEngine`（`InputMethodAbility`/`KeyboardController`/`KeyboardDelegate`/`Panel`/`InputClient`） |
| 输入法框架 API | 自绘编辑框 | `inputMethod`（`InputMethodController`/`InputMethodSetting`） |
| 系统管理 API | 系统应用 | `inputMethod`（switch/list/enable）、`inputMethodSystemPanelManager` |
| 扩展能力 | 输入法应用进程 | `InputMethodExtensionAbility` + `InputMethodExtensionContext` |

### 1.2 约束限制

- 切换输入法的系统 API（`switchInputMethod`/`switchCurrentInputMethodSubtype`/`switchCurrentInputMethodAndSubtype`）**仅允许当前输入法应用调用**，需申请 `ohos.permission.CONNECT_IME_ABILITY`
- `InputMethodExtensionAbility` 标注 `@stagemodelonly`，仅 Stage 模型支持
- `inputMethodSystemPanelManager` 全部接口为 `@systemapi` + `@stagemodelonly`
- 静态 API（ets1.2）统一 since 23，部分方法返回类型为 `T | null`（动态版返回 `T`）

### 1.3 模块清单（9 个 .d.ts/.ets）

| # | 模块 | 导出方式 | since(dyn) | 核心内容 |
|---|------|---------|-----------|---------|
| 1 | `@ohos.InputMethodExtensionAbility` | `export default class` | 9 | 输入法扩展能力基类（onCreate/onDestroy） |
| 2 | `@ohos.InputMethodExtensionContext` | `export default class extends ExtensionContext` | 9 | 扩展上下文（destroy/startAbility） |
| 3 | `@ohos.InputMethodSubtype` | `export default interface` | 9 | 子类型数据结构 |
| 4 | `@ohos.inputMethodEngine` | `export default namespace` | 8 | 输入法引擎核心（InputMethodAbility/InputClient/KeyboardController/KeyboardDelegate/Panel） |
| 5 | `@ohos.inputMethod` | `export default namespace` | 6 | 输入法管理（InputMethodController/InputMethodSetting） |
| 6 | `@ohos.inputMethod.Panel` | 具名 `export interface/enum` | 11 | PanelInfo/PanelFlag/PanelType 数据定义 |
| 7 | `@ohos.inputMethod.ExtraConfig` | 具名 `export type/interface` | 22 | InputMethodExtraConfig |
| 8 | `@ohos.inputMethodList` | `@CustomDialog struct` + interface | 11 | 输入法列表对话框组件 |
| 9 | `@ohos.inputMethodSystemPanelManager` | `export default namespace` | 26.0.0 | 系统面板管理（@systemapi） |

> **两套 PanelFlag/PanelType 枚举**：文件4（inputMethodEngine）用 `FLG_FIXED`/`FLG_FLOATING` 前缀；文件6（inputMethod.Panel）用 `FLAG_FIXED`/`FLAG_FLOATING` 前缀。生成测试时需注意 import 来源。

---

## 二、ExtensionAbility 测试架构（核心重点）

> **通用模式**：双进程 + 公共事件桥接、module.json5 注册规范、CROSS_PROCESS 测试类型、跨进程 testTemplate 模板、生命周期间接测试、资源清理通用规范，详见 `references/conventions/extension_ability_testing.md`。
> 本节仅描述 IME 子系统的个性化要点，完整个性配置见 `extension_ability.md`。

### 2.1 IME 个性化要点

| 项目 | IME 值 |
|------|--------|
| type 值 | `inputMethod` |
| 拉起方式 | `switchCurrentInputMethodSubtype(subtype)`（subtype.id = module.json5 name） |
| 生命周期模型 | service（onCreate/onDestroy + inputStart/inputStop 事件） |
| 会话管理 | inputMethodAbility.on('inputStart') 获取对象，on('inputStop') 触发 destroy |
| 测试通道组织 | 5 套独立 service |
| 被测 API | InputClient/KeyboardController/KeyboardDelegate/Panel |
| 业务错误码 | 128xxxxx 段 |

### 2.2 module.json5 注册示例（IME）

```json5
{
  "module": {
    "extensionAbilities": [
      {
        "name": "inputStageService",                    // 与 subtype.id 一致
        "srcEntrance": "./ets/InputMethodAbility/InputStageService.ts",
        "type": "inputMethod",                          // 关键：类型必须为 inputMethod
        "visible": true,                                // 关键：必须 visible 才能被拉起
        "description": "输入法测试服务"
      }
    ],
    "requestPermissions": [
      { "name": "ohos.permission.CONNECT_IME_ABILITY" } // 必需权限
    ]
  }
}
```

**注册三要素**：
1. `type: "inputMethod"` — 类型标识
2. `visible: true` — 可被外部拉起
3. `name` 与 `switchCurrentInputMethodSubtype` 传入的 `subtype.id` **完全一致**

> **注意**：历史用例**未使用 metadata + input_method_config.json 静态配置子类型**，而是在 beforeAll 中动态构造 subtype 对象调用 `switchCurrentInputMethodSubtype`。这是测试场景的简化做法，官方推荐生产代码用 metadata 静态配置。

### 2.3 ExtensionAbility 启动方式

两种方式拉起 ExtensionAbility：

**方式 A（推荐）：switchCurrentInputMethodSubtype**
```typescript
let testSubtype = {
  id: 'inputStageService',           // = module.json5 中 extensionAbility 的 name
  label: '',
  name: 'com.acts.inputmethodengine.test',  // bundle name
  mode: 'lower',
  locale: '', language: '', icon: '', iconId: 0, extra: {}
};
await inputMethod.switchCurrentInputMethodSubtype(testSubtype);
```

**方式 B：hdc 命令**
```typescript
await delegator.executeShellCommand('ime -e com.acts.inputmethodengine.test -f');  // enable
await delegator.executeShellCommand('ime -s com.acts.inputmethodengine.test');       // set current
```

切换后系统拉起对应 ExtensionAbility，触发 `onCreate(want)`，执行服务初始化逻辑。

### 2.4 服务类封装模式

每个测试通道由 3 层封装：

| 层 | 职责 | 示例文件 |
|----|------|---------|
| ExtensionAbility（Service） | 继承 InputMethodExtensionAbility，实现 onCreate/onDestroy | `InputStageService.ts` |
| Controller/Delegate | 封装 InputMethodAbility/KeyboardDelegate，注册事件 + 公共事件订阅 | `KeyboardDelegate.ts`、`KeyboardController.ts` |
| 测试用例 | 在 TestAbility 进程发起指令、接收结果、断言 | `*.test.ets` |

**服务初始化标准流程**（Controller/Delegate 的 onCreate）：
```typescript
public onCreate(): void {
  this.initWindow();                                    // 创建输入法窗口或 Panel
  inputMethodAbility.on('inputStart', (kbCtrl, client) => {
    this.keyboardController = kbCtrl;                   // 保存供各测试方法使用
    this.inputClient = client;
  });
  inputMethodAbility.on('inputStop', this.onInputStop.bind(this));  // 销毁处理
  // 订阅公共事件，接收测试指令
  commoneventmanager.createSubscriber({ events: ['xxxTest'] })
    .then((subscriber) => {
      commoneventmanager.subscribe(subscriber, (err, data) => {
        // data.code → switch case → 调用对应 test_N() 方法
      });
    });
}
```

### 2.5 生命周期回调

InputMethodExtensionAbility 仅两个生命周期回调（**service 模型，非 session 模型**）：

| 回调 | 触发时机 | 典型用途 |
|------|---------|---------|
| `onCreate(want: Want): void` | 服务首次创建（再次启动不触发） | 初始化、注册事件监听、创建 KeyboardController |
| `onDestroy(): void` | 实例销毁前 | 清理资源、注销监听、destroyPanel |

> **历史用例未发现 onSessionCreate/onSessionDestroy 测试** — InputMethodExtensionAbility 当前是 service 模型。会话管理通过 `inputMethodAbility.on('inputStart'/'inputStop')` 事件实现。

### 2.6 会话管理测试（inputStart/inputStop）

- `inputMethodAbility.on('inputStart', (kbController, inputClient) => {})` — 获取核心对象
- `inputMethodAbility.on('inputStop', () => {})` — 触发销毁（`mContext.destroy()`）
- `inputMethodAbility.off('inputStop')` — 测试 off（on 后立即 off 验证不回调）

### 2.7 Panel 创建销毁测试

```typescript
// 正向：createPanel + destroyPanel 配对
let panelInfo = { type: PanelType.SOFT_KEYBOARD, flag: PanelFlag.FLG_FIXED };
inputMethodAbility.createPanel(this.context, panelInfo).then(async (panel) => {
  await panel.setUiContent('pages/Keyboard');
  await panel.show();
  // ... 测试逻辑
  await inputMethodAbility.destroyPanel(panel);
});

// 反例：参数校验（null/undefined → 401）
try {
  inputMethodAbility.createPanel(null, panelInfo, (err, panel) => {});
} catch (err) {
  if (err.code === 401) { /* 预期错误码命中 */ }
}
```

---

## 三、测试组织规范（IME 差异）

> **通用规范**：describe/it 结构、@tc 注解格式、List.test.ets 注册、Test.json 通用结构，详见 `references/conventions/test_conventions.md`。本节仅列 IME 差异。

### 3.1 测试用例命名风格（IME 三种历史风格）

历史用例存在三种命名风格（按年代演进）：

| 风格 | 示例 | 适用 |
|------|------|------|
| 早期数字编号 | `inputMethodEngine_test_028` | 旧 API（inputMethodEngine/inputMethodAbility） |
| SUB_ 全大写 | `SUB_Misc_InputMethod_Manage_Physical_Buttons_0010` | 物理键盘 |
| **Sub_ 推荐** | `Sub_InputMethod_IME_InputClientdeleteForwardSync_0100` | 新 API（New/HotArea） |

**推荐命名规则**：`Sub_InputMethod_IME_<对象><方法><调用方式>_<场景><编号>`
- 调用方式区分：`Callback` / `Promise` / `Sync`
- 编号从 `0100` 开始递增（`0100`/`0200`/`0300`），中间编号预留给补充用例

### 3.2 Test.json 驱动配置（IME 差异值）

```json
{
  "driver": {
    "type": "OHJSUnitTest",
    "test-timeout": "180000",
    "bundle-name": "com.acts.inputmethodengine.test",
    "module-name": "entry_test",
    "testcase-timeout": "60000"
  },
  "kits": [
    { "type": "AppInstallKit", "test-file-name": ["ActsInputMethodEngineTest.hap"], "cleanup-apps": true },
    { "type": "ShellKit", "run-command": ["power-shell wakeup", "uinput -T -m ..."] }
  ]
}
```
- IME 特有：`testcase-timeout: 60000`（跨进程用例需较长超时）、`cleanup-apps: true`（恢复默认输入法）
- ShellKit 中预置 `uinput` 滑屏/点击命令用于唤醒屏幕、模拟手势

---

## 四、断言与异步模式

### 4.1 三种测试形态

#### 形态 A：直接常量断言（同步，不依赖 ExtensionAbility）

适用于枚举值/常量验证：
```typescript
it('test_001', Level.LEVEL1, async (done: Function) => {
  let keyType = inputMethodEngine.ENTER_KEY_TYPE_UNSPECIFIED;
  expect(keyType).assertEqual(0);
  done();
});
```

#### 形态 B：跨进程公共事件桥接（核心模式）

适用于需调用 InputClient/KeyboardController/Panel 等 ExtensionAbility 侧 API 的用例：

```
TestAbility 侧（.test.ets）             ExtensionAbility 侧（Controller.ts）
─────────────────────────────          ────────────────────────────────
1. createSubscriber([eventName])
2. subscribe(subscriber, cb)  ◀──────────────────────────────────────
3. setTimeout(500ms) ─────────┐
4. publish(triggerEvent, {code}) ────▶ switch(data.code) { case N: test_N(); }
                                   test_N() {
                                     await InputClient.xxx(...)
                                     publish(eventName, {data:"SUCCESS/FAILED"})
                                   } ────▶
5. cb 触发: data.data="SUCCESS" ◀────────────────────────────────
6. expect(data.data).assertEqual("SUCCESS")
7. unsubscribe → setTimeout(500ms) → done()
```

**推荐提炼为公共模板**（历史用例提供了 `testTemplate` 但未广泛使用）：
```typescript
let testTemplate = async (testName, code, done, beforePublish?, afterPublish?) => {
  let subscriberCallback = (err, data) => {
    commoneventmanager.unsubscribe(subscriber, unSubscriberCallback);
    let t = setTimeout(() => {
      try { expect(data.data).assertEqual("SUCCESS"); done(); }
      catch (err) { done(); }
      clearTimeout(t);
    }, 500);
  };
  commoneventmanager.createSubscriber({ events: [testName] }).then(async (data) => {
    subscriber = data;
    commoneventmanager.subscribe(subscriber, subscriberCallback);
    await beforePublish?.();
    commoneventmanager.publish('inputMethodEngineTest', { code }, publishCallback);
    afterPublish?.();
  });
};
```

#### 形态 C：UI 自动化 + 公共事件

适用于热区/Panel 调整等需 UI 交互的场景：
```typescript
let touch = async () => {
  textArea = await driver.findComponent(ON.type('TextArea'));
  await textArea.click();              // 获焦触发 inputStart
  await driver.delayMs(1000);
  text1 = await driver.findComponent(ON.id('text1'));
  await text1.click();                 // 触发 insertText('1')
};
```

### 4.2 异步处理要点

- **必用 `done: Function`**：所有 `it` 为 `async (done: Function) => {...}`，必须在断言或异常分支末尾调用 `done()`
- **`setTimeout` 节流**：publish 前 500ms（等订阅就绪）；回调内 500ms~2000ms（等 ExtensionAbility 处理）；复杂场景 8000ms
- **try/catch 包裹 expect**：保证断言失败也能 `done()`：
  ```typescript
  try { expect(data.data).assertEqual("SUCCESS"); done(); }
  catch (err) { done(); }
  ```
- **Promise 形态 API**：ExtensionAbility 侧用 `await this.inputClient.xxx()`

### 4.3 错误码断言方式

错误码断言发生在 **ExtensionAbility 侧**，catch 到 err.code 转化为 `data:"SUCCESS"` 回传：
```typescript
try {
  await this.keyboardController.exitCurrentInputType();
  commonEventPublishData = { data: 'FAILED' };     // 不应成功
} catch (err) {
  if (err.code === 12800010) {                     // 期望错误码命中
    commonEventPublishData = { data: 'SUCCESS' };
  }
}
```

**断言规范**：
- 使用 `assertEqual` 精确匹配错误码（R002: number 字面量）
- 禁止用 `==`/`!=`（R022），禁止 `Number()` 强转（R023）
- 每个 catch 块必须有断言（R024），禁止空 catch 或仅 console.log（R026）

### 4.4 事件监听测试模式

采用**计数器 + setTimeout 等待**模式：
```typescript
let count = 0;
inputMethodAbility.on('keyboardShow', () => {
  inputMethodAbility.off('keyboardShow');    // 一次性消费避免重复
  count += 1;
});
// 触发动作（hideKeyboard/insertText 等）
let t = setTimeout(() => {
  if (count === 1) { commonEventPublishData = { data: "SUCCESS" }; }
  commoneventmanager.publish(...);
  clearTimeout(t);
}, 2000);
```

### 4.5 异步三态覆盖

历史用例对每个 InputClient API 系统性覆盖 **Callback + Promise + Sync** 三种形态：
- `deleteForward(callback)` / `deleteForward(): Promise` / `deleteForwardSync()`
- 生成新 API 用例时应延续此三态覆盖模式

---

## 五、测试隔离与资源清理

### 5.1 beforeAll（每文件一次）

| 操作 | 说明 |
|------|------|
| 保存当前输入法 | 切换前记录原始输入法（可选） |
| switchCurrentInputMethodSubtype | 切换到测试 ExtensionAbility |
| findComponent + click | 点击 TextArea 获焦触发 inputStart |
| 等待 2000ms | 等 ExtensionAbility 启动完成 |

### 5.2 afterAll

历史用例统一为空实现，**未恢复原始输入法**，依赖 `cleanup-apps: true`。

> **改进建议**：新用例应在 afterAll 中恢复原始输入法：
> ```typescript
> afterAll(async (done) => {
>   await inputMethod.switchInputMethod(originalInputMethod);
>   done();
> });
> ```

### 5.3 用例内资源释放

- subscriberCallback 首行执行 `unsubscribe`
- 事件型用例：on 后立即 off（一次性消费）
- ExtensionAbility 侧：inputStop 触发 `mContext.destroy()` + off 所有监听

---

## 六、错误码体系

### 6.1 公共错误码（独立于 @throws，动态模式下应生成测试）

| 错误码 | 含义 | 触发条件 | 出现位置 |
|--------|------|---------|---------|
| **401** | Parameter error | 必填参数未指定/参数类型错误/参数校验失败 | 几乎所有带参数方法 |
| **201** | 权限不足 | 调用需权限接口但权限不足 | switchInputMethod、setPrivacyMode、enableInputMethod、connectSystemChannel 等 |
| **202** | 非系统应用 | 非系统应用调用系统 API | on('imeShow'/'imeHide')、isPanelShown、inputMethodSystemPanelManager 全部接口、setShadow 等 |
| **801** | 能力不支持 | 设备/能力不支持 | on('callingDisplayDidChange')、startMoving、getAttachOptions、setImmersiveEffect 等 |

> **801 全局防护**：@throws 含 801 的 API，其所有用例（PARAM/RETURN/BOUNDARY/EVENT）都必须包裹 801 防护（try 正常逻辑，catch 判断 801→通过，其他→assertFail）。详见 `error_test.md` 第七章。

### 6.2 IMEKit 业务错误码（128xxxxx）

| 错误码 | 含义 | 主要出现位置 |
|--------|------|-------------|
| 12800001 | bundle manager error | listInputMethodSubtype、getInputMethods、getAllInputMethods |
| 12800002 | input method engine error（面板未创建/未订阅事件） | InputClient 文本操作、Panel.startMoving、setImmersiveMode |
| 12800003 | input method client error（编辑框未获焦/未绑定/IPC 失败） | KeyboardController.hide、InputClient 几乎所有方法、InputMethodController.attach 等 |
| 12800004 | not an input method application | getSecurityMode、createPanel、getInputMethodState |
| 12800005 | configuration persistence error | switchInputMethod 系列 |
| 12800006 | input method controller error | getController、InputClient.getForward/Backward、getTextIndexAtCursor |
| 12800007 | input method setter error | getSetting |
| 12800008 | input method manager service error | 大量接口的系统错误 |
| 12800009 | input method client detached | showTextInput/hideTextInput/detach 后调用、sendMessage |
| 12800010 | not the preconfigured default input method | on('privateCommand')、exitCurrentInputType、sendPrivateCommand |
| 12800011 | text preview not supported | setPreviewText/finishTextPreview |
| 12800012 | the input method panel does not exist | getCallingWindowInfo |
| 12800013 | window manager service error | Panel 调整/移动、getCallingWindowInfo、setShadow |
| 12800014 | the input method is in basic mode | sendMessage |
| 12800015 | the other side does not accept the request | sendMessage、discardTypingText |
| 12800016 | input method client is not editable | sendMessage |
| 12800017 | invalid panel type or panel flag | Panel 调整/移动相关 |
| 12800018 | input method is not found | enableInputMethod |
| 12800019 | 不可应用于预置默认输入法 | enableInputMethod |
| 12800020 | invalid immersive effect | setImmersiveEffect |
| 12800021 | 需先调用 adjustPanelRect 或 resize | setImmersiveEffect |
| 12800022 | invalid displayId | getSystemPanelCurrentInsets |
| 12800023 | the specified user does not exist | 带 userId 的系统 API |
| 12800024 | the specified user is not in the foreground | 同上 |
| 12800025 | cross-user operation denied（仅 user 0） | 同上 |
| 12800026 | input method system panel error | inputMethodSystemPanelManager |

### 6.3 Ability 框架错误码（16xxxxxxx，仅 InputMethodExtensionContext.startAbility）

`16000001`/`16000002`/`16000004`/`16000005`/`16000006`/`16000008`/`16000009`/`16000010`/`16000011`/`16000012`/`16000013`/`16000019`/`16000050`/`16000053`/`16000055`/`16000061`/`16000069`/`16000070`/`16200001`

> 这些是 Ability 框架通用错误码，触发条件需对照 Ability 框架文档。

---

## 七、核心 API 速查（索引）

> 详细测试模式见模块级配置文件，本节仅提供快速定位索引。

### 7.1 对象获取速查

| 获取方式 | 返回 | since | 说明 | 详细模式见 |
|---------|------|-------|------|-----------|
| `inputMethodEngine.getInputMethodAbility()` | `InputMethodAbility` | 9 | 输入法应用核心能力对象 | `inputMethodEngine.md` §1 |
| `inputMethodEngine.getKeyboardDelegate()` | `KeyboardDelegate` | 9 | 物理键盘事件代理 | `inputMethodEngine.md` §4 |
| `inputMethod.getController()` | `InputMethodController` | 9 | 输入法控制器（自绘编辑框侧） | `inputMethod.md` §1 |
| `inputMethod.getSetting()` | `InputMethodSetting` | 9 | 输入法设置 | `inputMethod.md` §2 |

### 7.2 模块文件指引表

| API 域 | 核心对象 | 详细测试模式 |
|--------|---------|-------------|
| 引擎核心（事件订阅/文本操作/键盘/Panel） | InputMethodAbility/InputClient/KeyboardController/KeyboardDelegate/Panel | `inputMethodEngine.md` |
| 管理侧（控制器/设置/系统管理/子类型/对话框/系统面板） | InputMethodController/InputMethodSetting/InputMethodSubtype/InputMethodListDialog/inputMethodSystemPanelManager | `inputMethod.md` |
| ExtensionAbility 个性 | InputMethodExtensionAbility/InputMethodExtensionContext | `extension_ability.md` |

---

## 八、测试设计建议

### 8.1 ExtensionAbility 测试必备清单

生成 ExtensionAbility 相关测试时，必须包含以下工程结构：

| 文件 | 用途 | 必需 |
|------|------|------|
| `ohosTest/module.json5` | 注册 extensionAbilities（type:inputMethod, visible:true） | ✅ |
| `ohosTest/ets/{Service}/{Controller}.ts` | ExtensionAbility 服务实现 + 事件订阅 | ✅ |
| `ohosTest/ets/testability/TestAbility.ets` | UIAbility 测试宿主 | ✅ |
| `ohosTest/ets/test/List.test.ets` | 测试套件注册 | ✅ |
| `ohosTest/ets/testrunner/OpenHarmonyTestRunner.ts` | 测试运行器 | ✅ |
| `Test.json` | 驱动配置（OHJSUnitTest） | ✅ |
| `main/ets/pages/*.ets` | TextArea 等获焦组件页面 | ✅ |

### 8.2 code 编号空间管理

每个测试通道内 `data.code` 必须唯一，与 `switch case` 一一对应。建议用 10/20/30... 间隔预留扩展空间。

### 8.3 边界值与异常场景覆盖建议

历史用例的覆盖缺口（建议补充）：

| API | 缺失场景 | 建议用例 |
|-----|---------|---------|
| InputClient 文本操作 | 超长字符串 insertText（10^6 字符） | BOUNDARY |
| InputClient deleteForward/Backward | length=0、负数、超大值 | BOUNDARY |
| Panel.resize | width/height=0、负数、超大值 | BOUNDARY |
| Panel.adjustPanelRect | rect 越界、负数 | BOUNDARY |
| switchInputMethod | target=null/undefined/空对象 | ERROR_401 |
| InputMethodController.attach | textConfig 缺字段/类型错误 | ERROR_401 |
| InputClient.sendMessage | msgId 空字符串/超长/msgParam 超大 ArrayBuffer | BOUNDARY |
| createPanel | context=null、info.type 无效值 | ERROR_401 |

### 8.4 未覆盖能力扩展点

历史用例未覆盖的能力（建议补充）：

- `inputMethodAbility.on('privateCommand')` 正向测试
- `InputMethodController.attach` 自绘编辑框场景
- 非聚焦窗口 `shiftAppWindowFocus` 场景
- `panel.setImmersiveMode`/`getImmersiveMode` 正向测试
- `getSystemPanelCurrentInsets` 偏移区域
- metadata + `input_method_config.json` 静态子类型配置
- `inputMethodSystemPanelManager`（since 26.0.0，全部 @systemapi）
- `InputMethodListDialog`（@CustomDialog 组件）
- `InputMethodExtraConfig`（since 22）

### 8.5 静态项目（ArkTS-Sta）注意事项

- ets1.2 统一 since 23，部分方法返回类型为 `T | null`（如 `getInputMethodAbility(): InputMethodAbility | null`）
- **不生成 ERROR_401 测试**（编译时已拦截类型错误）
- hypium 导入用相对路径 `from "../../../hypium/index"`
- 事件订阅用命名方法式（`onInputStart(cb)` 而非 `on('inputStart', cb)`）
- 非重赋值变量用 `const`
- 禁止 `as any`（ESE0143）

### 8.6 关键文件路径速查

| 用途 | 路径 |
|------|------|
| ohosTest module 注册 | `entry/src/ohosTest/module.json5` |
| 测试入口 | `entry/src/ohosTest/ets/testability/TestAbility.ets` |
| 测试套件注册 | `entry/src/ohosTest/ets/test/List.test.ets` |
| 驱动配置 | `Test.json` |
| InputClient 旧 API 通道 | `entry/src/ohosTest/ets/InputMethodAbility/KeyboardDelegate.ts` |
| TextInputClient 通道 | `entry/src/ohosTest/ets/InputMethodEngine/KeyboardController.ts` |
| keyEvent 通道 | `entry/src/ohosTest/ets/InputMethodEngineKey/KeyboardController.ts` |
| 新 API 通道 | `entry/src/ohosTest/ets/InputMethodEngineNew/KeyboardControllerNew.ts` |
| HotArea 通道 | `entry/src/ohosTest/ets/InputMethodEngineHotArea/KeyboardControllerNew.ts` |
| 测试用例 | `entry/src/ohosTest/ets/test/*.test.ets` |
| SDK 声明（中文版） | `/home/chen/ohos/interface/sdk-js/zh-cn/api/@ohos.inputMethod*.d.ts` |
| 官方文档 | `/home/chen/ohos/docs/zh-cn/application-dev/inputmethod/` |
| 历史用例根目录 | `/home/chen/ohos/test/xts/acts/inputmethod/` |

---

## 九、子模块索引

| 子模块 | 内容 | 加载时机 |
|--------|------|---------|
| `_common.md`（本文件） | 子系统总览、ExtensionAbility 个性要点、测试规范差异、错误码体系、API 速查索引 | Phase 1/4/5 必读 |
| `extension_ability.md` | ExtensionAbility 插槽填充 + IME 个性（5 套通道配置、testTemplate 示例、HotArea 模式、反例场景、资源清理） | 生成 ExtensionAbility 测试时 |
| `inputMethodEngine.md` | InputMethodAbility/InputClient/KeyboardController/KeyboardDelegate/Panel 详细测试模式 + 历史用例清单 | 生成引擎 API 测试时 |
| `inputMethod.md` | InputMethodController/InputMethodSetting/系统管理 API/InputMethodSubtype/InputMethodListDialog/inputMethodSystemPanelManager 测试模式 | 生成管理 API 测试时 |

---

## 十、参考来源

| 来源 | 路径/版本 |
|------|----------|
| SDK 声明（9 个文件） | `/home/chen/ohos/interface/sdk-js/zh-cn/api/@ohos.inputMethod*.d.ts` |
| Kit 入口 | `/home/chen/ohos/interface/sdk-js/kits/@kit.IMEKit.d.ts` |
| 官方文档 | `/home/chen/ohos/docs/zh-cn/application-dev/inputmethod/` |
| 历史用例 | `/home/chen/ohos/test/xts/acts/inputmethod/InputMethodEngine/` |
| 完整 API 解析 | 子代理输出（92KB，含全部方法签名/@throws/枚举） |

> **生成测试时的权威依据**：API 签名以 `.d.ts` 声明为最高优先级；测试模式以历史用例为参考；错误码以 `@throws` 注解 + 公共错误码集合为准。
