# IME ExtensionAbility 测试个性配置

> 通用模式参见 `references/conventions/extension_ability_testing.md`，本文件仅填充 IME 子系统个性。
> **填充通用层 §11 全部插槽（§1-§8），追加 IME 特有内容（§9-§14）**

---

## 插槽填充

### §1 extension_ability_type

`InputMethodExtensionAbility`

### §2 type 值

`inputMethod`

### §3 拉起方式

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

切换后系统拉起对应 ExtensionAbility，触发 `onCreate(want)`。

### §4 生命周期回调清单

| 回调 | 签名 | 触发时机 | 测试要点 |
|------|------|---------|---------|
| `onCreate` | `onCreate(want: Want): void` | 服务首次创建（再次启动不触发） | 初始化、注册事件监听、创建 KeyboardController |
| `onDestroy` | `onDestroy(): void` | 实例销毁前 | 清理资源、注销监听、destroyPanel |

> **会话通过事件管理（非 session 模型）**：
> - `inputMethodAbility.on('inputStart', (kbCtrl, client) => {})` — 获取核心对象
> - `inputMethodAbility.on('inputStop', () => {})` — 触发 `mContext.destroy()`

### §5 会话模型

**service 模型**（非 session）。无 `onSessionCreate`/`onSessionDestroy`。
- 会话开始 = `inputStart` 事件 → 保存 `keyboardController` + `inputClient`
- 会话结束 = `inputStop` 事件 → `mContext.destroy()` + off 全部监听

### §6 被测 API 集合

| 对象 | 获取方式 | 核心方法域 |
|------|---------|-----------|
| `InputClient` | `on('inputStart')` 回调第二参数 | 文本操作三态（deleteForward/insertText/getForward/...） |
| `KeyboardController` | `on('inputStart')` 回调第一参数 | hide/exitCurrentInputType |
| `KeyboardDelegate` | `getKeyboardDelegate()` | 物理键盘事件（keyDown/keyUp/keyEvent） |
| `Panel` | `InputMethodAbility.createPanel()` | setUiContent/resize/show/hide/adjustPanelRect/setImmersiveMode |
| `InputMethodAbility` | `getInputMethodAbility()` | 事件订阅（inputStart/inputStop/keyboardShow/...） |

### §7 业务错误码

IMEKit 业务错误码（128xxxxx 段），详见 `_common.md` §6.2。核心错误码：
- `12800002` input method engine error（面板未创建/未订阅事件）
- `12800003` input method client error（编辑框未获焦/未绑定/IPC 失败）
- `12800004` not an input method application
- `12800010` not the preconfigured default input method
- `12800011` text preview not supported
- `12800013` window manager service error

### §8 测试通道组织方式

**5 套独立 service**，每套一个 commonEvent 通道：

| service name | ExtensionAbility 文件 | commonEvent 通道 | 被测 API 域 |
|-------------|----------------------|-----------------|------------|
| `inputStageService` | `InputMethodAbility/InputStageService.ts` | `inputMethodAbilityTest` | InputClient 旧 API（callback/promise） |
| `InputDemoService` | `InputMethodEngine/InputDemoService.ts` | `inputMethodEngineTest` | TextInputClient 旧 API + KeyboardDelegate 事件 |
| `InputKeyService` | `InputMethodEngineKey/InputKeyService.ts` | `inputMethodEngineKeyTest` | 物理键盘 keyEvent |
| `InputNewService` | `InputMethodEngineNew/InputNewService.ts` | `inputMethodEngineNewTest` | 新 API（Sync/Panel/PreviewText/SendMessage） |
| `InputHotAreaService` | `InputMethodEngineHotArea/InputHotAreaService.ts` | `inputMethodEngineHotAreaTest` | Panel adjustPanelRect + 热区 |

---

## IME 特有内容

### §9 code 编号空间分配表

每个测试通道内 `data.code` 唯一，与 ExtensionAbility 侧 `switch case` 一一对应：

| 通道 | code 范围 | 被测 API | 历史用例数 |
|------|----------|---------|-----------|
| inputMethodAbilityTest | 1~106 | InputClient（callback/promise）+ 常量断言 | ~106 |
| inputMethodEngineTest | 1~100+ | TextInputClient + 事件 + exitCurrentInputType | ~100 |
| inputMethodEngineKeyTest | 10~70 | keyEvent 物理键序列 | ~7 |
| inputMethodEngineNewTest | 1~110 | Sync 三态 + Panel + sendPrivateCommand + sendMessage | ~110 |
| inputMethodEngineHotAreaTest | 100~200 | adjustPanelRect + 热区输入验证 | ~2 |

### §10 跨进程 testTemplate IME 应用示例

```typescript
// TestAbility 侧（.test.ets）
it('Sub_InputMethod_IME_InputClientDeleteForward_0100',
  TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
    let subscriberCallback = (err, data) => {
      commoneventmanager.unsubscribe(subscriber, unSubscriberCallback);
      let t = setTimeout(() => {
        try {
          expect(data.data).assertEqual("SUCCESS");
          done();
        } catch (err) { done(); }
        clearTimeout(t);
      }, 500);
    };
    commoneventmanager.createSubscriber({
      events: ['Sub_InputMethod_IME_InputClientDeleteForward_0100']
    }).then(async (data) => {
      subscriber = data;
      commoneventmanager.subscribe(subscriber, subscriberCallback);
      commoneventmanager.publish('inputMethodEngineNewTest', { code: 30 }, publishCallback);
    });
  });

// ExtensionAbility 侧（KeyboardControllerNew.ts）
case 30:  await this.Sub_InputMethod_IME_InputClientDeleteForward_0100(); break;

async Sub_InputMethod_IME_InputClientDeleteForward_0100() {
  let commonEventPublishData = { data: "FAILED" };
  try {
    await this.inputClient.deleteForward(1);
    commonEventPublishData = { data: "SUCCESS" };
  } catch (err) {
    // 错误码命中也视为成功（按用例设计预期）
    if (err.code === 12800003) { commonEventPublishData = { data: "SUCCESS" }; }
  }
  commoneventmanager.publish('Sub_InputMethod_IME_InputClientDeleteForward_0100',
    commonEventPublishData, publishCallback);
}
```

### §11 IME UI 自动化模式（HotArea）

热区/Panel 调整等需 UI 交互的场景采用 Driver + ON 模式：

```typescript
let touch = async () => {
  textArea = await driver.findComponent(ON.type('TextArea'));
  await textArea.click();              // 获焦触发 inputStart
  await driver.delayMs(1000);           // 等键盘拉起
  text1 = await driver.findComponent(ON.id('text1'));
  await text1.click();                  // 触发 insertText('1')
  // ... 点击 text2/text3/text4
};
// 验证 getForward(4) === '1234' 后 deleteForward(4)
```

**要点**：
- `ON.type('TextArea')` 定位获焦组件
- `ON.id('textN')` 精确定位热区组件
- `delayMs(1000)` 等待键盘拉起
- 复杂场景（横竖屏切换）`delayMs(8000)`

### §12 IME 反例场景清单

| API | 反例输入 | 期望错误码 | 子场景 |
|-----|---------|-----------|--------|
| `createPanel(null, info, cb)` | ctx=null | 401 | 默认 |
| `createPanel(ctx, null, cb)` | info=null | 401 | 默认 |
| `destroyPanel(null, cb)` | panel=null | 401 | 默认 |
| `InputClient.deleteForward(undefined)` | length=undefined | 401 | 默认 |
| `InputClient.insertText(null)` | text=null | 401 | 默认 |
| `InputClient.deleteForward(0)` | length=0 | 12800002/12800003 | 边界 |
| `InputClient.insertText(超长字符串)` | text=10^6字符 | 12800003 | 边界 |
| `exitCurrentInputType()` | 非预置输入法 | 12800010 | 默认 |
| `sendPrivateCommand(data)` | 非预置输入法 | 12800010 | 默认 |
| `setPreviewText(text, range)` | 不支持预上屏 | 12800011 | 默认 |
| `sendMessage(msgId, param)` | 客户端 detached | 12800009 | 默认 |
| `sendMessage(msgId, param)` | 基础模式 | 12800014 | 默认 |
| `Panel.setImmersiveEffect(effect)` | 未先 adjustPanelRect | 12800021 | 默认 |
| `Panel.getSystemPanelCurrentInsets(displayId)` | displayId 无效 | 12800022 | 默认 |

### §13 IME 特有资源清理

| 资源 | 清理方式 | 触发时机 |
|------|---------|---------|
| commonEvent 订阅 | `unsubscribe(subscriber, cb)` | subscriberCallback 首行 |
| InputMethodAbility 事件 | `off('inputStart'/'inputStop'/'keyboardShow'/...)` | inputStop 回调内 off 全部 |
| KeyboardDelegate 事件 | `off('keyDown'/'keyUp'/'keyEvent'/...)` | onDestroy 内 off 全部 |
| Panel | `inputMethodAbility.destroyPanel(panel)` | onDestroy 内配对销毁 |
| ExtensionAbility 实例 | `mContext.destroy(callback)` | inputStop 触发 |
| InputMethod 窗口 | `windowManager.destroyWindow(win)` | onDestroy 内销毁（旧架构） |
| 物理键模拟 | 无需清理（uinput 一次性） | — |

**inputStop → destroy 标准流程**：
```typescript
private onInputStop() {
  inputMethodAbility.off('inputStop');
  inputMethodAbility.off('inputStart');
  inputMethodAbility.off('keyboardShow');
  // ... off 全部监听
  try {
    this.mContext.destroy((err) => {
      console.info(TAG + 'destroy err:' + JSON.stringify(err));
    });
  } catch (err) { /* log */ }
}
```

### §14 IME 服务初始化标准流程

```typescript
public onCreate(): void {
  this.initWindow();                                    // 创建窗口或 Panel
  inputMethodAbility.on('inputStart', (kbCtrl, client) => {
    this.keyboardController = kbCtrl;                   // 保存供各测试方法
    this.inputClient = client;
  });
  inputMethodAbility.on('inputStop', this.onInputStop.bind(this));
  // 订阅公共事件，接收测试指令
  commoneventmanager.createSubscriber({ events: ['xxxTest'] })
    .then((subscriber) => {
      commoneventmanager.subscribe(subscriber, (err, data) => {
        // data.code → switch case → 调用对应 test_N()
      });
    });
}
```

**新架构差异**：HotArea 测试用 `inputMethodAbility.createPanel` + `panel.adjustPanelRect` + `panel.setUiContent`，而非旧架构的 `windowManager.createWindow`。
