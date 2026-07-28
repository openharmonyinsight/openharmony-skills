# ExtensionAbility 测试通用规范

> **模块信息**
> - 层级：L2_Generation / conventions
> - 适用范围：所有基于 ExtensionAbility 的子系统测试（InputMethod/Service/Form/UI/Share/Action/Driver/EnterpriseAdmin 等）
> - 加载时机：Phase 1（识别 extension_ability_type 标记后）/ Phase 4（设计 CROSS_PROCESS 用例）/ Phase 5（生成跨进程代码）
> - 依赖：conventions/test_conventions.md, conventions/hypium_framework.md

---

## 一、通用测试架构

ExtensionAbility 测试采用**双进程 + 公共事件桥接**模式，这是与普通子系统（同进程 API 调用）最核心的差异：

```
┌─────────────────────────────────┐       ┌──────────────────────────────────────┐
│  TestAbility 进程（UIAbility）   │       │  XxxExtensionAbility 进程（独立进程）  │
│  （.test.ets 用例宿主）           │       │  （被测 API 实际执行处）                │
│                                 │       │                                      │
│  1. subscribe(resultEvent)      │◀──────│  6. 执行被测 API                      │
│  2. publish(triggerEvent,{code})───▶│  5. switch(code) → test_N()          │
│  3. 等待回调                     │       │     → publish(resultEvent,{data})    │
│  4. expect(data).assertEqual    │       │                                      │
│     ("SUCCESS"); done()         │       │                                      │
└─────────────────────────────────┘       └──────────────────────────────────────┘
              ▲                                          ▲
              │                                          │
        Hypium 测试框架                           子系统特定拉起方式
        拉起 TestAbility                          间接触发 onCreate
```

**核心约束**：

| 约束 | 原因 |
|------|------|
| 禁止在 TestAbility 进程直接调用 ExtensionAbility 侧 API | 进程隔离，直接调用会失败或获取 null 对象 |
| 被测 API 必须在 ExtensionAbility 进程执行 | InputClient/KeyboardController/Panel 等对象仅在 ExtensionAbility 侧可用 |
| 断言结果通过 commonEventManager 回传 | 跨进程通信的唯一可靠桥梁 |
| 每个用例必须 done() 必达 | 跨进程异步，未 done() 会触发 60s 超时 |

---

## 二、module.json5 注册规范

ExtensionAbility 必须在 **ohosTest 模块**（非 main 模块）的 module.json5 中注册：

```json5
{
  "module": {
    "extensionAbilities": [
      {
        "name": "testServiceName",          // 必填：与拉起标识一致
        "srcEntry": "./ets/Service/TestService.ts",  // 必填：入口文件
        "type": "inputMethod",              // 必填：ExtensionAbility 类型标识（见 §3 映射表）
        "visible": true,                    // 必填：必须 true 才能被外部拉起
        "description": "测试服务"
      }
    ],
    "requestPermissions": [
      { "name": "ohos.permission.XXX" }     // 按子系统要求申请权限
    ]
  }
}
```

**注册三要素**：
1. `type` — 类型标识（见 §3 映射表）
2. `visible: true` — 可被外部拉起
3. `name` 与拉起标识**完全一致**（如 InputMethod 的 subtype.id = name）

---

## 三、type 映射表（基于有历史用例的类型）

| ExtensionAbility 类 | type 值 | 拉起方式 | 生命周期模型 | 历史用例位置 |
|---------------------|---------|---------|-------------|-------------|
| InputMethodExtensionAbility | `inputMethod` | `switchCurrentInputMethodSubtype(subtype)` | service（onCreate/onDestroy + inputStart/inputStop 事件） | `inputmethod/InputMethodEngine` |
| ServiceExtensionAbility | `service` | `startAbility` / `startServiceExtensionAbility` / `connectServiceExtensionAbility` | service+connect（onCreate/onRequest/onConnect/onDisconnect） | `ability/ability_runtime` |
| FormExtensionAbility | `form` | `FormProvider` 发布卡片 | form（onAddForm/onCastToNormalForm/onUpdateForm/onFormEvent） | `application/formmgr` |
| UIExtensionAbility | `ui` | `startAbility`（UIExtensionComponent） | session（onCreate/onSessionCreate/onSessionDestroy） | `ability/ability_runtime/actsuiextensiontest` |
| ShareExtensionAbility | `share` | `startAbility`（系统分享面板） | session（onCreate/onSessionCreate/onSessionDestroy） | `ability/ability_runtime/shareextensionability` |
| ActionExtensionAbility | `action` | `startAbility`（action 匹配） | service（onCreate/onRequest） | `ability/ability_runtime/actsactionextensionability` |
| DriverExtensionAbility | `driver` | `startAbility` | connect（onCreate/onConnect/onDisconnect） | — |
| EnterpriseAdminExtensionAbility | `enterpriseAdmin` | 系统管理事件触发 | service（onAdminEnabled/onAdminDisabled） | `customization/enterprise_device_management` |

> **生命周期模型说明**：
> - **service 模型**：onCreate/onDestroy，可能配合事件（如 inputStart/inputStop）
> - **connect 模型**：onConnect/onDisconnect，返回 rpc.RemoteObject 供 IPC
> - **session 模型**：onCreate/onSessionCreate/onSessionDestroy，每个 UI 会话独立
> - **form 模型**：onAddForm/onUpdateForm/onCastToNormalForm 等卡片专属回调

> 其余 ExtensionAbility 类型（AutoFill/Wallpaper/WorkScheduler/Window/StaticSubscriber 等）按需补充。

---

## 四、CROSS_PROCESS 测试类型定义

### 4.1 类型定义

新增测试类型 `CROSS_PROCESS`，`@tc.type` 标注为 `CROSS_PROCESS`：

```typescript
/**
 * @tc.number SUB_XXX_XXX_0100
 * @tc.type CROSS_PROCESS
 * @tc.level LEVEL0
 */
it('testName', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => { ... });
```

**适用条件**：`metadata.extension_ability = true`（Phase 1 识别子系统 _common.md 元信息头 `extension_ability_type` 标记后设置）。

### 4.2 三个子场景

| 子场景 | 适用 | 自动化判断规则 |
|--------|------|--------------|
| **默认（跨进程调用）** | 需调用 ExtensionAbility 侧 API 的用例（InputClient/Panel 等） | API 所属对象在 ExtensionAbility 进程获取（如 inputStart 回调参数） |
| **lifecycle** | 生命周期回调间接测试（onCreate/onDestroy） | 回调名匹配 `onCreate`/`onDestroy`/`onSessionCreate` 等生命周期方法 |
| **event_subscribe** | 事件订阅+计数器模式（on/off + 触发动作） | API 为 `on(type, cb)` / `onXxx(cb)` 订阅方法 |

### 4.3 子场景在设计文档中的标注

```markdown
| @tc.number | @tc.type | 子场景 | code | 事件名 |
|-----------|---------|--------|------|--------|
| Sub_XXX_InputClientDelete_0100 | CROSS_PROCESS | — | 10 | xxx_test_028 |
| Sub_XXX_Lifecycle_onCreate_0100 | CROSS_PROCESS | lifecycle | — | — |
| Sub_XXX_keyboardShow_0100 | CROSS_PROCESS | event_subscribe | 70 | xxx_test_070 |
```

---

## 五、跨进程测试模板

### 5.1 testTemplate 高阶函数

```typescript
let testTemplate: (testName: string, code: number, done: Function,
  beforePublish?: () => Promise<void>, afterPublish?: () => void) => void =
  async (testName, code, done, beforePublish, afterPublish) => {
    let subscriberCallback = (err, data) => {
      commoneventmanager.unsubscribe(subscriber, unSubscriberCallback);
      let t = setTimeout(() => {
        try {
          expect(data.data).assertEqual("SUCCESS");
          done();
        } catch (err) {
          done();  // 断言失败也必须 done()
        }
        clearTimeout(t);
      }, 500);
    };
    commoneventmanager.createSubscriber({ events: [testName] }).then(async (data) => {
      subscriber = data;
      commoneventmanager.subscribe(subscriber, subscriberCallback);
      await beforePublish?.();
      commoneventmanager.publish('triggerEvent', { code }, publishCallback);
      afterPublish?.();
    });
  };
```

### 5.2 code 编号空间管理

- 每个测试通道内 `data.code` 必须**唯一**，与 ExtensionAbility 侧 `switch case` 一一对应
- 建议用 `10/20/30...` 间隔预留扩展空间，避免插入新用例时重排
- code 编号在设计文档"ExtensionAbility 配置"章节登记

### 5.3 setTimeout 节流档位

| 档位 | 延时 | 用途 |
|------|------|------|
| 订阅就绪 | 500ms | publish 前等订阅完成 |
| 处理等待 | 500ms~2000ms | 回调内等 ExtensionAbility 处理完成 |
| 复杂场景 | 8000ms | 横竖屏切换、多步 UI 交互 |

### 5.4 try/catch 包裹规范

```typescript
let t = setTimeout(() => {
  try {
    expect(data.data).assertEqual("SUCCESS");
    done();
  } catch (err) {
    done();  // 必须 done()，否则用例挂起至 60s 超时
  }
  clearTimeout(t);
}, 500);
```

---

## 六、生命周期间接测试思路

ExtensionAbility 的生命周期回调（onCreate/onDestroy/onSessionCreate 等）**不直接断言**，采用间接测试：

1. **拉起** → 隐式触发 onCreate
2. **各用例能正常收到 commonEvent 回执** → 证明 onCreate 中的订阅链已建立
3. **停止事件触发** → 隐式触发 onDestroy（如 inputStop → mContext.destroy()）

> 直接断言生命周期回调被调用不可行——回调在 ExtensionAbility 进程，TestAbility 无法直接观测。通过功能可用性反证是唯一可靠方式。

---

## 七、事件订阅测试模式

针对 `on(type, cb)` / `onXxx(cb)` 订阅方法，采用**计数器 + setTimeout 等待**模式：

```typescript
let count = 0;
xxxAbility.on('eventName', () => {
  xxxAbility.off('eventName');  // 一次性消费避免重复触发
  count += 1;
});
// 触发动作（hideKeyboard/insertText 等）
let t = setTimeout(() => {
  if (count === 1) {
    commonEventPublishData = { data: "SUCCESS" };
  }
  commoneventmanager.publish(resultEvent, commonEventPublishData, ...);
  clearTimeout(t);
}, 2000);
```

**要点**：
- on 后立即 off（一次性消费）
- setTimeout 等待事件触发（1000~2000ms）
- 计数器验证回调确实被执行

---

## 八、资源清理通用规范

| 资源类型 | 清理方式 | 时机 |
|---------|---------|------|
| commonEvent 订阅 | `commoneventmanager.unsubscribe(subscriber, cb)` | subscriberCallback 首行 |
| 事件订阅 | `xxxAbility.off('event')` / `offXxx(cb)` | on 后配对 off（一次性消费）或在 afterEach |
| Panel | `inputMethodAbility.destroyPanel(panel)` | createPanel 后配对 |
| ExtensionAbility 实例 | `mContext.destroy()` | inputStop/等价停止事件触发 |
| 原始状态 | 恢复原始输入法/配置 | afterAll |

**afterAll 改进建议**：
```typescript
afterAll(async (done: Function) => {
  await xxx.switchOriginalMethod();  // 恢复原始状态
  done();
});
```

---

## 九、设计文档扩展模板

当 `metadata.extension_ability = true` 时，设计文档新增"ExtensionAbility 配置"章节：

```markdown
## ExtensionAbility 配置

| 字段 | 值 |
|------|---|
| ExtensionAbility 类型 | {extension_ability_type} |
| type 值 | {type} |
| 拉起方式 | {launch_method} |
| 测试通道 | {service_name} |
| code 编号空间 | {code_list} |
| 跨进程事件名 | {event_names} |
```

用例表新增两列：

```markdown
| @tc.number | @tc.type | 子场景 | code | 事件名 | 测试步骤 | 预期结果 |
```

---

## 十、错误码断言方式

错误码断言发生在 **ExtensionAbility 侧**，catch 到 err.code 转化为 `data:"SUCCESS"` 回传：

```typescript
// ExtensionAbility 侧（Controller.ts）
try {
  await this.inputClient.someMethod(invalidParam);
  commonEventPublishData = { data: 'FAILED' };  // 不应成功
} catch (err) {
  if (err.code === 12800003) {                  // 期望错误码命中
    commonEventPublishData = { data: 'SUCCESS' };
  }
}
```

**规范**：
- 使用 `assertEqual` 精确匹配错误码（R002: number 字面量）
- 禁止 `==`/`!=`（R022），禁止 `Number()` 强转（R023）
- 每个 catch 块必须有断言（R024）
- **禁止在 TestAbility 侧断言错误码**（进程隔离无法捕获 ExtensionAbility 侧异常）

---

## 十一、插槽声明（子系统层必须填充）

子系统层 `extension_ability.md` 必须提供以下字段（供通用层引用）：

| # | 插槽名 | 说明 | 示例 |
|---|--------|------|------|
| 1 | `extension_ability_type` | ExtensionAbility 类名 | InputMethodExtensionAbility |
| 2 | `type 值` | module.json5 中的 type | inputMethod |
| 3 | `拉起方式` | 具体 API 或 hdc 命令 | switchCurrentInputMethodSubtype(subtype) |
| 4 | `生命周期回调清单` | 全部回调签名 | onCreate(want)/onDestroy() |
| 5 | `会话模型` | service/connect/session/form | service |
| 6 | `被测 API 集合` | 核心对象清单 | InputClient/KeyboardController/Panel |
| 7 | `业务错误码` | 子系统专属错误码段 | 128xxxxx |
| 8 | `测试通道组织方式` | 多 service 还是单 service | 5 套独立 service |

子系统层首行引用本文件：
```markdown
> 通用模式参见 `references/conventions/extension_ability_testing.md`，本文件仅填充子系统个性。
```
