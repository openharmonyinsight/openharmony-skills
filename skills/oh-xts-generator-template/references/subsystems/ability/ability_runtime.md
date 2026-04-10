# Ability Runtime 模块配置

> **模块信息**
> - 所属子系统: Ability
> - 模块名称: Ability Runtime（Ability 运行时）
> - API 类型: FA 模型 + Stage 模型
> - 版本: 1.0.0
> - 更新日期: 2026-02-03

## 一、模块特有配置

### 1.1 模块概述

Ability Runtime 模块包含 Ability 运行时相关的 API，主要涵盖：
- FA 模型（Feature Ability）：@ohos.ability.featureAbility
- Stage 模型：@kit.AbilityKit 中的 UIAbility、AbilityStage 等
- AbilityContext：Ability 上下文相关接口

### 1.2 API 声明文件

**FA 模型声明文件**：
- `@ohos.ability.featureAbility.d.ts`
- `@ohos.ability.errorCode.d.ts`

**Stage 模型声明文件**：
- `@ohos.app.ability.UIAbility.d.ts`
- `@ohos.app.ability.AbilityStage.d.ts`
- `@ohos.app.ability.UIAbilityContext.d.ts`

### 1.3 通用配置继承

本模块继承 Ability 子系统通用配置：
- **测试路径规范**：见 `ability/_common.md` 第 1.2 节
- **通用测试规则**：见 `ability/_common.md` 第 2 节
- **代码模板**：见 `ability/_common.md` 第 4 节

## 二、模块特有 API 列表

### 2.1 FA 模型 API（@ohos.ability.featureAbility）

| API名称 | 说明 | 优先级 |
|---------|------|--------|
| getWant | 获取 Ability 启动的 Want 参数 | LEVEL0 |
| startAbility | 启动 Ability | LEVEL0 |
| terminateSelf | 终止当前 Ability | LEVEL0 |
| terminateSelfWithResult | 终止 Ability 并返回结果 | LEVEL1 |
| startAbilityForResult | 启动 Ability 并获取结果 | LEVEL1 |
| hasWindowFocus | 检查是否有窗口焦点 | LEVEL2 |
| getWindow | 获取窗口对象 | LEVEL2 |

### 2.2 Stage 模型 API（@kit.AbilityKit）

**UIAbility 类**：
| API名称 | 说明 | 优先级 |
|---------|------|--------|
| onCreate | Ability 创建生命周期回调 | LEVEL0 |
| onDestroy | Ability 销毁生命周期回调 | LEVEL0 |
| onForeground | Ability 前台生命周期回调 | LEVEL0 |
| onBackground | Ability 后台生命周期回调 | LEVEL0 |
| onNewWant | 新 Want 请求回调 | LEVEL1 |
| onConfigurationUpdate | 配置更新回调 | LEVEL2 |

**AbilityStage 类**：
| API名称 | 说明 | 优先级 |
|---------|------|--------|
| onCreate | AbilityStage 创建回调 | LEVEL0 |
| onAcceptWant | 接受 Want 请求回调 | LEVEL0 |
| onConfigurationUpdate | 配置更新回调 | LEVEL2 |

**UIAbilityContext 类**：
| API名称 | 说明 | 优先级 |
|---------|------|--------|
| startAbility | 启动 Ability | LEVEL0 |
| startAbilityForResult | 启动 Ability 并获取结果 | LEVEL0 |
| terminateSelf | 终止当前 Ability | LEVEL0 |
| requestModalUIExtensionPresentation | 请求模态扩展UI | LEVEL2 |

## 三、模块特有测试规则

### 3.1 FA 模型测试规则

1. **异步 API 测试**
   - 支持回调函数和 Promise 两种方式
   - 必须测试两种调用方式
   - 验证返回值的完整性

2. **Want 参数测试**
   - 验证 bundleName、abilityName、moduleName
   - 验证 parameters 参数传递
   - 验证 action、entities 等字段

3. **结果测试**
   - terminateSelfWithResult 需要验证 AbilityResult
   - startAbilityForResult 需要验证返回结果
   - 结果码（resultCode）验证

### 3.2 Stage 模型测试规则

1. **生命周期测试**
   - 按顺序验证生命周期回调
   - 验证回调参数的正确性
   - 测试异常场景下的生命周期

2. **Context 测试**
   - 验证 Context 的功能完整性
   - 测试跨 Ability 的 Context 使用
   - 验证 Context 权限检查

### 3.3 错误码测试

需要测试的常见错误码：
- 201：权限不足
- 202：参数错误
- 401：参数检查失败
- 16000001：内部错误
- 16000002：Ability 不存在
- 16000003：Ability 启动失败
- 16000004：Ability 连接失败
- 16000005：Ability 断开连接失败
- 16000006：Ability 未连接
- 16000007：Worker 已存在
- 16000008：Worker 不存在

## 四、模块特有代码模板

### 4.1 getWant 测试模板

```typescript
it('SUB_Ability_AbilityRuntime_FeatureAbility_GetWant_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_Ability_AbilityRuntime_FeatureAbility_GetWant_0100-------------')
  try {
    const want = await featureAbility.getWant()
    hilog.info(0x0000, 'testTag', 'SUB_Ability_AbilityRuntime_FeatureAbility_GetWant_0100 getWant successful, want: ' + JSON.stringify(want))

    // 验证 Want 对象的具体值
    expect(want?.bundleName).assertEqual('com.example.faapicoverhaptest')
    expect(want?.abilityName).assertEqual('.TestAbility')
    expect(want?.moduleName).assertEqual('entry_test')
    expect(want?.action).assertEqual('action.system.home')
    expect(want?.entities?.[0]).assertEqual('entity.system.home')

    done()
  } catch (err: BusinessError) {
    hilog.info(0x0000, 'testTag', 'SUB_Ability_AbilityRuntime_FeatureAbility_GetWant_0100 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

### 4.2 startAbility 测试模板

```typescript
it('SUB_Ability_AbilityRuntime_FeatureAbility_StartAbility_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_Ability_AbilityRuntime_FeatureAbility_StartAbility_0100-------------')
  try {
    await featureAbility.startAbility({
      want: {
        bundleName: 'com.example.test',
        abilityName: '.MainAbility',
        moduleName: 'entry'
      }
    })
    hilog.info(0x0000, 'testTag', 'SUB_Ability_AbilityRuntime_FeatureAbility_StartAbility_0100 startAbility successful')
    expect(true).assertTrue()
    done()
  } catch (err: BusinessError) {
    hilog.info(0x0000, 'testTag', 'SUB_Ability_AbilityRuntime_FeatureAbility_StartAbility_0100 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

### 4.3 terminateSelfWithResult 测试模板

```typescript
it('SUB_Ability_AbilityRuntime_FeatureAbility_TerminateSelfWithResult_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_Ability_AbilityRuntime_FeatureAbility_TerminateSelfWithResult_0100-------------')
  try {
    await featureAbility.terminateSelfWithResult({
      resultCode: 1,
      want: {
        bundleName: 'com.example.test',
        abilityName: '.MainAbility'
      }
    })
    hilog.info(0x0000, 'testTag', 'SUB_Ability_AbilityRuntime_FeatureAbility_TerminateSelfWithResult_0100 successful')
    expect(true).assertTrue()
    done()
  } catch (err: BusinessError) {
    hilog.info(0x0000, 'testTag', 'SUB_Ability_AbilityRuntime_FeatureAbility_TerminateSelfWithResult_0100 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

## 五、UIExtension 跨组件测试模式

### 5.1 模式概述

**UIExtension 跨组件测试模式** 是用于测试 UIExtensionContentSession API 的专用测试架构，通过路由跳转、页面组件、Provider 和公共事件通信实现跨 Ability 的测试执行和结果验证。

#### 适用场景

- 测试 UIExtensionContentSession 的各种 API
  - `loadContent()` / `loadContentByName()`
  - `terminateSelf()` / `terminateSelfWithResult()`
  - `setWindowPrivacyMode()`
  - `startAbilityByType()`
- 测试边界参数（null, undefined）的错误码验证
- 需要在 Provider 端执行逻辑并通过公共事件返回结果的场景

#### 架构流程图

```
┌─────────────────────────────────────────────────────────────┐
│  1. 测试文件 (.test.ets)                                     │
│     - 创建公共事件订阅者                                        │
│     - 注册事件监听回调                                           │
│     - router.pushUrl() 跳转到测试页面                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  2. 页面组件 (UIExtensionPage.ets)                            │
│     - 接收路由参数（测试用例名称）                              │
│     - EmbeddedComponent 启动 UIExtensionProvider                │
│     - 传递 action 参数（用例标识）                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Provider (UIExtensionProvider.ts)                         │
│     - onSessionCreate() 接收 action 参数                       │
│     - 根据用例标识执行对应的测试逻辑                            │
│     - 调用目标 API 并捕获异常                                   │
│     - 通过 commonEventManager.publish() 返回测试结果            │
│     - terminateSelf() 终止 Provider                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  4. 测试文件 (回调处理)                                       │
│     - 接收公共事件                                             │
│     - 验证错误码或结果                                          │
│     - 取消订阅                                                 │
│     - done() 结束测试                                          │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 测试文件实现模板

```typescript
import { describe, beforeAll, it, Level, expect } from '@ohos/hypium';
import { commonEventManager, systemParameterEnhance } from '@kit.BasicServicesKit';
import { router } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';

// 公共事件订阅信息
let ACTS_EVENT: commonEventManager.CommonEventSubscribeInfo = {
  events: ['ACTS_TEST_DESTROY']
};

let subscriber: commonEventManager.CommonEventSubscriber;
let context = getContext(this) as common.UIAbilityContext;
let mpEnable: string;

// 路由参数类
class MyRouterParam {
  constructor(from: string) {
    this.fromPage = from;
  }
  fromPage: string = "";
}

export default function UIExtensionContentSessionTest() {
  describe('UIExtensionContentSessionTest', () => {
    beforeAll(() => {
      context = globalThis.context;
      // 获取多进程模式配置
      try {
        mpEnable = systemParameterEnhance.getSync('persist.sys.abilityms.multi_process_model');
      } catch (err) {
        console.error(`Get system parameter error: ${JSON.stringify(err)}`);
        mpEnable = 'fail';
      }
    })

    it('Sub_UIExtensionContentSession_errorCode_0600', Level.LEVEL0, (done: Function) => {
      let tag: string = `Sub_UIExtensionContentSession_errorCode_0600`;

      // 步骤1: 创建公共事件订阅者
      commonEventManager.createSubscriber(ACTS_EVENT)
        .then(async (commonEventSubscriber) => {
          subscriber = commonEventSubscriber;

          // 步骤2: 定义事件订阅回调
          let subscribeCallBack = async (err: base.BusinessError,
            data: commonEventManager.CommonEventData) => {
            console.log("subscribeCallBack success");

            // 步骤6: 监听测试完成事件并验证结果
            if (data.event == 'ACTS_TEST_DESTROY') {
              expect(data?.parameters?.result).assertEqual(401);
              console.log("subscribeCallBack ACTS_TEST_DESTROY");

              // 步骤7: 取消订阅
              setTimeout(() => {
                commonEventManager.unsubscribe(subscriber, unSubscribeCallback);
              }, 500);
            }
          }

          let unSubscribeCallback = () => {
            setTimeout(async () => {
              console.info(`====>${tag} unSubscribeCallback`);
              done();
            }, 1000);
          }

          // 步骤3: 注册事件监听
          commonEventManager.subscribe(subscriber, subscribeCallBack);

          // 步骤4: 通过路由跳转启动测试页面
          if (mpEnable == 'true') {
            try {
              router.pushUrl({
                url: 'testability/pages/UIExtensionContentSession/UIExtensionPage',
                params: new MyRouterParam(tag)
              });
              console.info(tag, 'push page UIExtensionPage success');
            } catch (err) {
              console.info(tag, 'push page err,err is :', err);
            }
          } else if (mpEnable == 'false') {
            commonEventManager.unsubscribe(subscriber, unSubscribeCallback);
          }
        })
    })
  })
}
```

### 5.3 页面组件实现模板

```typescript
import { router } from '@kit.ArkUI';

class MyRouterParam {
  constructor(from: string) {
    this.fromPage = from;
  }
  public fromPage: string = "";
}

@Entry
@Component
struct UIExtensionPage {
  @State message: string = 'UIExtension User';
  private myProxy: UIExtensionProxy | undefined = undefined;
  public params: string = '';

  aboutToAppear(): void {
    // 接收路由参数（测试用例标识）
    this.params = (router.getParams() as MyRouterParam).fromPage;
  }

  build() {
    Row() {
      Column() {
        Text(this.message)
          .fontSize(30)
          .textAlign(TextAlign.Center)

        // 通过 EmbeddedComponent 启动 UIExtensionProvider
        EmbeddedComponent(
          {
            bundleName: 'com.test.actsabilityerrcodequerytest',
            abilityName: 'UIExtensionProvider',
            moduleName: 'entry_test',
            action: this.params,  // 传递测试用例标识
          },
          EmbeddedType.EMBEDDED_UI_EXTENSION
        )
          .focusable(true)
          .size({ width: 300, height: 300 })
          .border({ width: 5, color: 0x317AF7, radius: 10 })
      }
      .width('100%')
    }
    .height('100%')
  }
}
```

### 5.4 Provider 实现模板

```typescript
import { Want, UIExtensionAbility, UIExtensionContentSession }
  from '@kit.AbilityKit';
import { BusinessError, commonEventManager } from '@kit.BasicServicesKit';

let TAG: string = 'UIExtensionContentSession UIExtAbility';
let caseTag: string = '';

export default class UIExtensionProvider extends UIExtensionAbility {
  onCreate() {
    console.log(TAG, `onCreate`);
  }

  onDestroy() {
    console.log(TAG, `onDestroy`);
  }

  onSessionCreate(want: Want, session: UIExtensionContentSession) {
    // 接收测试用例标识
    caseTag = want.action;
    TAG = caseTag;
    console.log(`${caseTag} onSessionCreate, want: ${JSON.stringify(want)}`);

    let storage: LocalStorage = new LocalStorage();
    storage.setOrCreate('session', session);

    // 根据用例标识执行对应测试逻辑
    if (want.action == 'Sub_UIExtensionContentSession_errorCode_0600') {
      try {
        // 调用目标 API（callback 模式）
        session.setWindowPrivacyMode(undefined, (err: BusinessError) => {
          if (err) {
            console.error(`Failed to set window to privacy mode, code: ${err.code}`);
            return;
          }
          console.info(`Successed in setting window to privacy mode.`);
          commonEventManager.publish('ACTS_TEST_DESTROY');
        });
      } catch (error) {
        // 捕获同步抛出的异常（参数错误在调用时抛出）
        console.error(`session.setWindowPrivacyMode fail, error: ${JSON.stringify(error)}`);

        if (error.code == 401) {
          globalThis.errCode = error.code;

          // 通过公共事件返回错误码
          commonEventManager.publish('ACTS_TEST_DESTROY', {
            parameters: {
              'result': error?.code,
            }
          }, function () {
            console.info(`${caseTag} publish ACTS_TEST_DESTROY`);

            // 终止 UIExtensionProvider
            setTimeout(() => {
              session?.terminateSelf((err: BusinessError) => {
                if (err) {
                  console.error(`Failed to terminate self, code: ${err.code}`);
                  return;
                }
                console.info(`Successed in terminating self.`);
              });
            }, 500);
          });
        }
      }
    }
  }
}
```

### 5.5 关键技术点

#### 5.5.1 路由传参

```typescript
// 发送端（测试文件）
router.pushUrl({
  url: 'testability/pages/UIExtensionContentSession/UIExtensionPage',
  params: new MyRouterParam('Sub_UIExtensionContentSession_errorCode_0600')
})

// 接收端（页面组件）
aboutToAppear(): void {
  this.params = (router.getParams() as MyRouterParam).fromPage;
}
```

#### 5.5.2 EmbeddedComponent 组件

用于嵌入 UIExtension 能力，通过 `action` 参数传递业务数据（测试用例标识）。

#### 5.5.3 公共事件通信

```typescript
// 发布端（Provider）
commonEventManager.publish('ACTS_TEST_DESTROY', {
  parameters: {
    'result': error.code
  }
})

// 订阅端（测试文件）
commonEventManager.createSubscriber(ACTS_EVENT)
  .then((subscriber) => {
    commonEventManager.subscribe(subscriber, (err, data) => {
      if (data.event == 'ACTS_TEST_DESTROY') {
        expect(data?.parameters?.result).assertEqual(401);
      }
    });
  })
```

#### 5.5.4 异步错误处理

- **同步异常**：参数错误在调用时立即抛出，通过 try-catch 捕获
- **异步错误**：API 执行过程中的错误通过 callback 的 err 参数返回

### 5.6 测试用例命名规范

- 测试用例标识：`Sub_UIExtensionContentSession_errorCode_XXXX`
- 公共事件名称：`ACTS_TEST_DESTROY`, `ACTS_TEST_LOADCONTENT` 等
- Provider 类名：`UIExtensionProvider`
- 页面组件名：`UIExtensionPage`

### 5.7 Promise 模式变体

对于 Promise 模式的 API，使用以下模板：

```typescript
if (want.action == 'Sub_UIExtensionContentSession_errorCode_0500') {
  try {
    session.setWindowPrivacyMode(undefined)
      .then(() => {
        // 成功分支（不应发生）
        console.error(`Test case execution results do not match expected outcomes.`);
        commonEventManager.publish('ACTS_TEST_DESTROY');
      })
      .catch((err: BusinessError) => {
        // Promise catch 错误处理
        console.error(`Failed to set window to privacy mode, code: ${err.code}`);
      });
  } catch (error) {
    // 同步异常处理
    if (error.code == 401) {
      commonEventManager.publish('ACTS_TEST_DESTROY', {
        parameters: { 'result': error?.code }
      });
    }
  }
}
```

### 5.8 参考实例

完整的实现示例位于：
- 测试文件：`ability_runtime/actsabilityerrcodequery/actsabilityerrcodequerytest/entry/src/ohosTest/ets/test/UIExtensionContentSession.test.ets`
- 页面组件：`ability_runtime/actsabilityerrcodequery/actsabilityerrcodequerytest/entry/src/ohosTest/ets/testability/pages/UIExtensionContentSession/UIExtensionPage.ets`
- Provider：`ability_runtime/actsabilityerrcodequery/actsabilityerrcodequerytest/entry/src/ohosTest/ets/test/UIExtensionContentSession/UIExtensionContentSession.ts`

## 六、测试注意事项

### 6.1 FA 模型注意事项

- FA 模型主要基于 API 8-9
- 测试时需要配置 config.json
- 使用 featureAbility 模块进行测试

### 6.2 Stage 模型注意事项

- Stage 模型主要基于 API 9+
- 测试时需要配置 module.json5
- 使用 AbilityKit 进行测试
- 需要验证生命周期回调顺序

### 6.3 UIExtension 测试注意事项

- 需要确保多进程模式配置正确
- Provider 和测试页面必须在不同的模块
- 公共事件名称要保持一致
- 注意 Provider 的生命周期管理
- 测试完成后必须调用 terminateSelf() 终止 Provider
- 注意路由跳转的时序，确保订阅创建在跳转之前

### 6.4 兼容性测试

- 需要同时测试 FA 模型和 Stage 模型
- 验证两种模型的 API 差异
- 确保迁移路径的兼容性

## 七、AppServiceExtensionAbility 启动规范

### 7.1 模式概述

**AppServiceExtensionAbility 启动模式** 是用于测试 AppServiceExtensionAbility 各种启动和连接方式的专用测试架构。与 UIExtension 不同，AppServiceExtensionAbility 专注于后台服务能力，支持启动和连接两种交互方式。

#### 适用场景

- 测试 AppServiceExtensionContext API
  - `startAppServiceExtensionAbility()` - 启动后台服务
  - `connectAppServiceExtensionAbility()` - 连接后台服务
  - `stopAppServiceExtensionAbility()` - 停止后台服务
  - `disconnectAppServiceExtensionAbility()` - 断开连接
- 测试 AppServiceExtensionAbility 生命周期
  - `onCreate()` - 服务创建
  - `onRequest()` - 服务启动请求
  - `onConnect()` - 连接建立
  - `onDisconnect()` - 连接断开
  - `onDestroy()` - 服务销毁
- 测试跨应用的服务调用和权限控制
- 测试 appIdentifierAllowList 权限验证

#### 启动方式对比

| 启动方式 | 接口方法 | 生命周期回调 | 返回值 | 适用场景 |
|---------|---------|------------|--------|---------|
| **启动方式** | `startAppServiceExtensionAbility()` | onCreate → onRequest | Promise<void> | 一次性任务、后台服务 |
| **连接方式** | `connectAppServiceExtensionAbility()` | onCreate → onConnect | Promise<AppServiceProxy> | 持续通信、RPC调用 |

#### 运作机制

```
┌─────────────────────────────────────────────────────────────────┐
│  客户端操作          │  服务端状态    │  客户端是否可信  │  结果说明   │
├─────────────────────────────────────────────────────────────────┤
│  startAppService   │  未启动       │  是             │  成功，通过  │
│  ExtensionAbility  │              │                 │  start方式   │
│                    │              │                 │  启动服务    │
├─────────────────────────────────────────────────────────────────┤
│  startAppService   │  未启动       │  否             │  失败，不在  │
│  ExtensionAbility  │              │                 │  允许列表中  │
├─────────────────────────────────────────────────────────────────┤
│  connectAppService │  未启动       │  是             │  成功，通过  │
│  ExtensionAbility  │              │                 │  connect方式  │
│                    │              │                 │  启动并连接  │
├─────────────────────────────────────────────────────────────────┤
│  connectAppService │  已启动       │  是或否         │  成功，直接  │
│  ExtensionAbility  │              │                 │  建立连接    │
└─────────────────────────────────────────────────────────────────┘
```

#### 架构流程图

**启动方式流程**：

```
┌─────────────────────────────────────────────────────────────┐
│  1. 测试文件 (.test.ets)                                     │
│     - 创建公共事件订阅者                                        │
│     - 准备 Want 参数                                          │
│     - 调用 context.startAppServiceExtensionAbility(want)      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  2. AppServiceExtensionAbility (服务端)                       │
│     - onCreate(want) 初始化服务                                │
│     - onRequest(want, startId) 处理启动请求                    │
│     - 执行后台任务                                             │
│     - 通过 commonEventManager.publish() 返回结果              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. 测试文件 (回调处理)                                       │
│     - 接收公共事件验证结果                                      │
│     - 调用 context.stopAppServiceExtensionAbility() 停止服务   │
│     - 取消订阅                                                 │
│     - done() 结束测试                                          │
└─────────────────────────────────────────────────────────────┘
```

**连接方式流程**：

```
┌─────────────────────────────────────────────────────────────┐
│  1. 测试文件 (.test.ets)                                     │
│     - 定义 AppServiceExtensionConnectionCallback              │
│     - 调用 context.connectAppServiceExtensionAbility()        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  2. AppServiceExtensionAbility (服务端)                       │
│     - onCreate(want) 初始化（如果首次启动）                     │
│     - onConnect(want) 返回 RemoteObject                       │
│     - 建立 IPC 通信通道                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. 测试文件 (连接成功)                                       │
│     - 接收 AppServiceProxy                                    │
│     - 通过 proxy 发送消息                                      │
│     - 测试完成后调用 disconnectAppServiceExtensionAbility()   │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 启动方式测试模板

#### 7.2.1 测试文件实现模板

```typescript
import { describe, beforeAll, it, Level, expect } from '@ohos/hypium';
import { commonEventManager, BusinessError } from '@kit.BasicServicesKit';
import { common, Want } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';

let context: common.UIAbilityContext;
let subscriber: commonEventManager.CommonEventSubscriber;

export default function AppServiceExtensionTest() {
  describe('AppServiceExtensionAbility_Start', () => {
    beforeAll(() => {
      context = AppStorage.get<common.UIAbilityContext>('abilityContext') as common.UIAbilityContext;
    })

    /**
     * @tc.name   SUB_AA_AppServiceExtension_Start_0100
     * @tc.desc   Test startAppServiceExtensionAbility with valid Want
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_AA_AppServiceExtension_Start_0100', Level.LEVEL0, async (done: Function) => {
      const tcNumber = 'SUB_AA_AppServiceExtension_Start_0100';
      hilog.info(0x0000, 'testTag', `${tcNumber} Begin`);

      // 步骤1: 准备 Want 参数
      let want: Want = {
        bundleName: 'com.example.appserviceextension',
        abilityName: 'MyAppServiceExtAbility',
        parameters: {
          TestFlag: 'startAppServiceDefault'
        }
      };

      // 步骤2: 创建公共事件订阅者
      let commonEventSubscribeInfo: commonEventManager.CommonEventSubscribeInfo = {
        events: ['AppServiceExtension_Start_0100']
      };

      await commonEventManager.createSubscriber(commonEventSubscribeInfo)
        .then((commonEventSubscriber) => {
          subscriber = commonEventSubscriber;
          hilog.info(0x0000, 'testTag', `${tcNumber} createSubscriber succeed`);

          // 步骤3: 定义事件订阅回调
          commonEventManager.subscribe(subscriber, (err, commonEventData) => {
            hilog.info(0x0000, 'testTag',
              `${tcNumber} subscribe callback result:${JSON.stringify(err)}`);

            // 步骤6: 验证服务端返回的结果
            expect(commonEventData.parameters?.result).assertEqual(200);

            // 步骤7: 取消订阅
            commonEventManager.unsubscribe(subscriber);
            done();
          });

          // 步骤4: 调用 startAppServiceExtensionAbility 启动服务
          try {
            context.startAppServiceExtensionAbility(want)
              .then(() => {
                hilog.info(0x0000, 'testTag',
                  `${tcNumber} startAppServiceExtensionAbility succeed`);
              })
              .catch((err: BusinessError) => {
                hilog.info(0x0000, 'testTag',
                  `${tcNumber} startAppServiceExtensionAbility error:${JSON.stringify(err)}`);

                // 步骤5: 处理启动失败情况
                if (err.code !== 801) {
                  expect().assertFail();
                }
                done();
              });
          } catch (err) {
            hilog.info(0x0000, 'testTag',
              `${tcNumber} startAppServiceExtensionAbility failed: ${JSON.stringify(err)}`);
            expect().assertFail();
            done();
          }
        })
    })

    /**
     * @tc.name   SUB_AA_AppServiceExtension_Start_0200
     * @tc.desc   Test startAppServiceExtensionAbility with invalid bundleName
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_AA_AppServiceExtension_Start_0200', Level.LEVEL0, async (done: Function) => {
      const tcNumber = 'SUB_AA_AppServiceExtension_Start_0200';
      hilog.info(0x0000, 'testTag', `${tcNumber} Begin`);

      // 测试错误包名
      let want: Want = {
        bundleName: 'com.example.invalidbundle',
        abilityName: 'MyAppServiceExtAbility',
        parameters: {
          TestFlag: 'startAppServiceErrorBundleName'
        }
      };

      let commonEventSubscribeInfo: commonEventManager.CommonEventSubscribeInfo = {
        events: ['AppServiceExtension_Start_0200']
      };

      await commonEventManager.createSubscriber(commonEventSubscribeInfo)
        .then((commonEventSubscriber) => {
          subscriber = commonEventSubscriber;
          commonEventManager.subscribe(subscriber, (err, commonEventData) => {
            // 验证错误码
            expect(commonEventData.parameters?.result).assertEqual(16000001);
            commonEventManager.unsubscribe(subscriber);
            done();
          });

          try {
            context.startAppServiceExtensionAbility(want)
              .then(() => {
                hilog.info(0x0000, 'testTag',
                  `${tcNumber} startAppServiceExtensionAbility succeed`);
              })
              .catch((err: BusinessError) => {
                if (err.code !== 801) {
                  expect().assertFail();
                }
                done();
              });
          } catch (err) {
            hilog.info(0x0000, 'testTag',
              `${tcNumber} startAppServiceExtensionAbility failed: ${JSON.stringify(err)}`);
            expect().assertFail();
            done();
          }
        })
    })
  })
}
```

#### 7.2.2 服务端实现模板

```typescript
import { AppServiceExtensionAbility, Want } from '@kit.AbilityKit';
import { rpc } from '@kit.IPCKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { commonEventManager } from '@kit.BasicServicesKit';

const TAG: string = '[MyAppServiceExtAbility]';
const DOMAIN_NUMBER: number = 0xFF00;

// 实现 RPC RemoteObject
class StubTest extends rpc.RemoteObject {
  constructor(des: string) {
    super(des);
  }

  onRemoteMessageRequest(code: number,
    data: rpc.MessageSequence,
    reply: rpc.MessageSequence,
    options: rpc.MessageOption): boolean | Promise<boolean> {
    hilog.info(DOMAIN_NUMBER, TAG, `onRemoteMessageRequest, code: ${code}`);
    // 处理客户端发送的消息
    return true;
  }
}

export default class MyAppServiceExtAbility extends AppServiceExtensionAbility {
  onCreate(want: Want): void {
    hilog.info(DOMAIN_NUMBER, TAG, `onCreate, want: ${JSON.stringify(want)}`);
    // 服务创建时的初始化逻辑
  }

  onRequest(want: Want, startId: number): void {
    hilog.info(DOMAIN_NUMBER, TAG,
      `onRequest, want: ${JSON.stringify(want)}, startId: ${startId}`);

    // 根据参数执行不同的测试逻辑
    if (want.parameters?.TestFlag === 'startAppServiceDefault') {
      // 成功场景
      hilog.info(DOMAIN_NUMBER, TAG, 'Start AppService default success');

      // 通过公共事件返回成功结果
      commonEventManager.publish('AppServiceExtension_Start_0100', {
        parameters: {
          'result': 200  // 成功
        }
      }, () => {
        hilog.info(DOMAIN_NUMBER, TAG, 'Publish success event');
      });
    } else if (want.parameters?.TestFlag === 'startAppServiceErrorBundleName') {
      // 错误场景
      hilog.error(DOMAIN_NUMBER, TAG, 'Invalid bundle name');

      // 通过公共事件返回错误码
      commonEventManager.publish('AppServiceExtension_Start_0200', {
        parameters: {
          'result': 16000001  // bundle name 错误
        }
      }, () => {
        hilog.info(DOMAIN_NUMBER, TAG, 'Publish error event');
      });
    }
  }

  onConnect(want: Want): rpc.RemoteObject {
    hilog.info(DOMAIN_NUMBER, TAG, `onConnect, want: ${JSON.stringify(want)}`);
    // 返回 RemoteObject 用于 IPC 通信
    return new StubTest('test');
  }

  onDisconnect(want: Want): void {
    hilog.info(DOMAIN_NUMBER, TAG, `onDisconnect, want: ${JSON.stringify(want)}`);
  }

  onDestroy(): void {
    hilog.info(DOMAIN_NUMBER, TAG, 'onDestroy');
    // 服务销毁时的清理逻辑
  }
};
```

#### 7.2.3 module.json5 配置模板

```json5
{
  "module": {
    "name": "entry",
    "type": "entry",
    "extensionAbilities": [
      {
        "name": "MyAppServiceExtAbility",
        "description": "AppService Extension",
        "type": "appService",
        "exported": true,
        "srcEntry": "./ets/appserviceextability/MyAppServiceExtAbility.ets",
        "appIdentifierAllowList": [
          // 配置允许启动该服务的客户端应用 appIdentifier
          "com.example.clientapp"
        ]
      }
    ]
  }
}
```

### 7.3 连接方式测试模板

#### 7.3.1 连接测试文件模板

```typescript
import { describe, beforeAll, it, Level, expect } from '@ohos/hypium';
import { common, Want } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { BusinessError } from '@kit.BasicServicesKit';

let context: common.UIAbilityContext;
let proxy: common.AppServiceProxy | undefined;

export default function AppServiceExtensionConnectTest() {
  describe('AppServiceExtensionAbility_Connect', () => {
    beforeAll(() => {
      context = AppStorage.get<common.UIAbilityContext>('abilityContext') as common.UIAbilityContext;
    })

    /**
     * @tc.name   SUB_AA_AppServiceExtension_Connect_0100
     * @tc.desc   Test connectAppServiceExtensionAbility with valid Want
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_AA_AppServiceExtension_Connect_0100', Level.LEVEL0, async (done: Function) => {
      const tcNumber = 'SUB_AA_AppServiceExtension_Connect_0100';
      hilog.info(0x0000, 'testTag', `${tcNumber} Begin`);

      // 步骤1: 准备 Want 参数
      let want: Want = {
        bundleName: 'com.example.appserviceextension',
        abilityName: 'MyAppServiceExtAbility'
      };

      // 步骤2: 定义连接回调
      let connectCallback: common.AppServiceExtensionConnectionCallback = {
        onConnect: (elementName: common.ElementName, proxy: common.AppServiceProxy) => {
          hilog.info(0x0000, 'testTag', `${tcNumber} onConnect success`);
          expect(elementName.bundleName).assertEqual('com.example.appserviceextension');

          // 保存 proxy 用于后续通信
          proxy = proxy;

          // 步骤5: 测试完成后断开连接
          setTimeout(() => {
            context.disconnectAppServiceExtensionAbility(proxy);
            done();
          }, 1000);
        },
        onDisconnect: (elementName: common.ElementName) => {
          hilog.info(0x0000, 'testTag', `${tcNumber} onDisconnect`);
        },
        onFailed: (code: number) => {
          hilog.error(0x0000, 'testTag', `${tcNumber} onFailed, code: ${code}`);
          expect().assertFail();
          done();
        }
      };

      // 步骤3: 调用 connectAppServiceExtensionAbility 连接服务
      try {
        context.connectAppServiceExtensionAbility(want, connectCallback)
          .then(() => {
            hilog.info(0x0000, 'testTag',
              `${tcNumber} connectAppServiceExtensionAbility succeed`);
          })
          .catch((err: BusinessError) => {
            // 步骤4: 处理连接失败情况
            hilog.error(0x0000, 'testTag',
              `${tcNumber} connectAppServiceExtensionAbility error: ${JSON.stringify(err)}`);

            if (err.code !== 801) {
              expect().assertFail();
            }
            done();
          });
      } catch (err) {
        hilog.error(0x0000, 'testTag',
          `${tcNumber} connectAppServiceExtensionAbility failed: ${JSON.stringify(err)}`);
        expect().assertFail();
        done();
      }
    })
  })
}
```

#### 7.3.2 RPC 通信示例

```typescript
// 在服务端的 StubTest 中实现消息处理
class StubTest extends rpc.RemoteObject {
  constructor(des: string) {
    super(des);
  }

  onRemoteMessageRequest(code: number,
    data: rpc.MessageSequence,
    reply: rpc.MessageSequence,
    options: rpc.MessageOption): boolean | Promise<boolean> {

    hilog.info(DOMAIN_NUMBER, TAG, `onRemoteMessageRequest, code: ${code}`);

    // 读取客户端发送的数据
    let inputStr: string = data.readString();
    hilog.info(DOMAIN_NUMBER, TAG, `Received from client: ${inputStr}`);

    // 处理业务逻辑
    let result: string = `Server processed: ${inputStr}`;

    // 写入返回数据
    reply.writeString(result);

    return true;
  }
}

// 在客户端通过 proxy 发送消息
let option: rpc.MessageOption = new rpc.MessageOption();
let data: rpc.MessageSequence = new rpc.MessageSequence();
let reply: rpc.MessageSequence = new rpc.MessageSequence();

data.writeString('Hello from client');

proxy?.sendMessageRequest(1, data, reply, option)
  .then((result) => {
    hilog.info(0x0000, 'testTag', `sendMessageRequest succeed, result: ${result}`);

    // 读取服务端返回的数据
    let response: string = reply.readString();
    hilog.info(0x0000, 'testTag', `Received from server: ${response}`);

    expect(response).assertEqual('Server processed: Hello from client');
    done();
  })
  .catch((err: BusinessError) => {
    hilog.error(0x0000, 'testTag', `sendMessageRequest failed: ${JSON.stringify(err)}`);
    expect().assertFail();
    done();
  });
```

### 7.4 错误码测试规范

#### 7.4.1 常见错误码

| 错误码 | 说明 | 测试场景 |
|-------|------|---------|
| 201 | 权限不足 | 未申请 ACL 权限时调用 |
| 401 | 参数错误 | 传递 null、undefined、错误类型的参数 |
| 16000001 | 内部错误 | bundleName 不存在 |
| 16000002 | Ability 不存在 | abilityName 错误 |
| 16000019 | 参数校验失败 | abilityName 为 undefined |
| 16000004 | 连接失败 | 网络异常、服务端崩溃 |
| 16000005 | 断开连接失败 | 未连接时断开 |
| 16000050 | 参数数量错误 | 参数数量不匹配 |

#### 7.4.2 错误码测试模板

```typescript
/**
 * @tc.name   SUB_AA_AppServiceExtension_Error_401_0100
 * @tc.desc   Test startAppServiceExtensionAbility with null Want
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_AA_AppServiceExtension_Error_401_0100', Level.LEVEL0, async (done: Function) => {
  const tcNumber = 'SUB_AA_AppServiceExtension_Error_401_0100';

  try {
    // 测试 null 参数
    await context.startAppServiceExtensionAbility(null);
    expect().assertFail();
    done();
  } catch (err) {
    // 验证错误码
    expect(err.code).assertEqual(401);
    done();
  }
})

/**
 * @tc.name   SUB_AA_AppServiceExtension_Error_16000001_0100
 * @tc.desc   Test startAppServiceExtensionAbility with invalid bundleName
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_AA_AppServiceExtension_Error_16000001_0100', Level.LEVEL0, async (done: Function) => {
  const tcNumber = 'SUB_AA_AppServiceExtension_Error_16000001_0100';

  let want: Want = {
    bundleName: 'com.example.nonexistent',
    abilityName: 'MyAppServiceExtAbility'
  };

  let commonEventSubscribeInfo: commonEventManager.CommonEventSubscribeInfo = {
    events: ['AppServiceExtension_Error_16000001']
  };

  await commonEventManager.createSubscriber(commonEventSubscribeInfo)
    .then((subscriber) => {
      commonEventManager.subscribe(subscriber, (err, data) => {
        // 验证错误码
        expect(data.parameters?.result).assertEqual(16000001);
        commonEventManager.unsubscribe(subscriber);
        done();
      });

      context.startAppServiceExtensionAbility(want)
        .then(() => {
          expect().assertFail();
        })
        .catch((err: BusinessError) => {
          if (err.code !== 801) {
            expect().assertFail();
          }
        });
    })
})
```

### 7.5 生命周期测试规范

#### 7.5.1 生命周期测试模板

```typescript
/**
 * @tc.name   SUB_AA_AppServiceExtension_Lifecycle_0100
 * @tc.desc   Test AppServiceExtensionAbility lifecycle callbacks
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_AA_AppServiceExtension_Lifecycle_0100', Level.LEVEL0, async (done: Function) => {
  const tcNumber = 'SUB_AA_AppServiceExtension_Lifecycle_0100';

  let want: Want = {
    bundleName: 'com.example.appserviceextension',
    abilityName: 'MyAppServiceExtAbility',
    parameters: {
      TestFlag: 'testLifecycle'
    }
  };

  let events: string[] = [];
  let commonEventSubscribeInfo: commonEventManager.CommonEventSubscribeInfo = {
    events: ['AppServiceExtension_Lifecycle_Create',
             'AppServiceExtension_Lifecycle_Request',
             'AppServiceExtension_Lifecycle_Destroy']
  };

  await commonEventManager.createSubscriber(commonEventSubscribeInfo)
    .then((subscriber) => {
      commonEventManager.subscribe(subscriber, (err, data) => {
        events.push(data.event);

        // 验证生命周期顺序
        if (events.length === 3) {
          expect(events[0]).assertEqual('AppServiceExtension_Lifecycle_Create');
          expect(events[1]).assertEqual('AppServiceExtension_Lifecycle_Request');
          expect(events[2]).assertEqual('AppServiceExtension_Lifecycle_Destroy');

          commonEventManager.unsubscribe(subscriber);
          done();
        }
      });

      // 启动服务
      context.startAppServiceExtensionAbility(want)
        .then(() => {
          hilog.info(0x0000, 'testTag', `${tcNumber} start succeed`);

          // 停止服务
          setTimeout(() => {
            context.stopAppServiceExtensionAbility(want);
          }, 1000);
        })
        .catch((err: BusinessError) => {
          if (err.code !== 801) {
            expect().assertFail();
          }
          done();
        });
    })
})
```

#### 7.5.2 服务端生命周期事件发布

```typescript
export default class MyAppServiceExtAbility extends AppServiceExtensionAbility {
  onCreate(want: Want): void {
    hilog.info(DOMAIN_NUMBER, TAG, `onCreate, want: ${JSON.stringify(want)}`);

    // 发布创建事件
    commonEventManager.publish('AppServiceExtension_Lifecycle_Create');
  }

  onRequest(want: Want, startId: number): void {
    hilog.info(DOMAIN_NUMBER, TAG,
      `onRequest, want: ${JSON.stringify(want)}, startId: ${startId}`);

    // 发布请求事件
    commonEventManager.publish('AppServiceExtension_Lifecycle_Request');
  }

  onDestroy(): void {
    hilog.info(DOMAIN_NUMBER, TAG, 'onDestroy');

    // 发布销毁事件
    commonEventManager.publish('AppServiceExtension_Lifecycle_Destroy');
  }
};
```

### 7.6 多实例和进程模型测试

#### 7.6.1 多实例测试

```typescript
/**
 * @tc.name   SUB_AA_AppServiceExtension_MultiInstance_0100
 * @tc.desc   Test multiple AppServiceExtensionAbility instances
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL2
 */
it('SUB_AA_AppServiceExtension_MultiInstance_0100', Level.LEVEL2, async (done: Function) => {
  const tcNumber = 'SUB_AA_AppServiceExtension_MultiInstance_0100';

  let want1: Want = {
    bundleName: 'com.example.appserviceextension',
    abilityName: 'MyAppServiceExtAbility',
    parameters: {
      instanceId: 'instance1'
    }
  };

  let want2: Want = {
    bundleName: 'com.example.appserviceextension',
    abilityName: 'MyAppServiceExtAbility',
    parameters: {
      instanceId: 'instance2'
    }
  };

  // 启动第一个实例
  context.startAppServiceExtensionAbility(want1)
    .then(() => {
      hilog.info(0x0000, 'testTag', `${tcNumber} start instance1 succeed`);

      // 启动第二个实例
      return context.startAppServiceExtensionAbility(want2);
    })
    .then(() => {
      hilog.info(0x0000, 'testTag', `${tcNumber} start instance2 succeed`);
      expect(true).assertTrue();
      done();
    })
    .catch((err: BusinessError) => {
      hilog.error(0x0000, 'testTag', `${tcNumber} error: ${JSON.stringify(err)}`);
      expect().assertFail();
      done();
    });
})
```

### 7.7 与 UIExtension 的关键区别

| 特性 | UIExtension | AppServiceExtension |
|-----|-------------|-------------------|
| **启动方式** | UIExtensionComponent / startAbility | startAppServiceExtensionAbility / connectAppServiceExtensionAbility |
| **界面支持** | 有界面，支持嵌入式显示 | 无界面，纯后台服务 |
| **通信方式** | UIExtensionContentSession | RPC (RemoteObject) |
| **生命周期** | onCreate → onSessionCreate → onForeground → onBackground → onDestroy | onCreate → onRequest/onConnect → onDisconnect → onDestroy |
| **使用场景** | 弹窗、状态栏、嵌入式UI | 后台任务、数据处理、长连接服务 |
| **进程隔离** | 支持多进程模型 | 独立进程运行 |
| **权限控制** | exported + type 控制 | appIdentifierAllowList 控制 |
| **适用设备** | 多种设备 | 仅 2in1 设备 |

### 7.8 测试注意事项

#### 7.8.1 权限和配置

1. **ACL 权限**：
   - 必须申请 `ohos.permission.SUPPORT_APP_SERVICE_EXTENSION`
   - 该权限仅对企业普通应用开放
   - 测试时需要在 module.json5 中配置请求权限

2. **appIdentifierAllowList 配置**：
   - 只有在允许列表中的应用才能启动服务
   - 测试时需要确保测试应用在允许列表中
   - 跨应用调用需要配置正确的 appIdentifier

3. **设备限制**：
   - 仅支持 2in1 设备
   - 测试前需要确认设备类型
   - 可通过系统参数判断设备能力

#### 7.8.2 公共事件使用

1. **事件命名规范**：
   - 使用统一的命名前缀，如 `AppServiceExtension_*`
   - 包含测试用例标识，如 `AppServiceExtension_Start_0100`
   - 避免事件名冲突

2. **订阅生命周期**：
   - 订阅必须在启动服务之前创建
   - 测试完成后必须取消订阅
   - 使用 timeout 防止订阅泄漏

3. **参数传递**：
   - 通过 `parameters` 字段传递测试数据
   - 使用公共事件返回测试结果
   - 参数类型保持一致

#### 7.8.3 异步处理

1. **Promise 和 Callback**：
   - 支持两种异步模式
   - 必须同时测试两种方式
   - 注意错误处理的差异

2. **时序控制**：
   - 使用 setTimeout 确保事件顺序
   - 合理设置超时时间
   - 避免竞态条件

3. **资源清理**：
   - 测试完成后停止服务
   - 断开连接释放资源
   - 取消公共事件订阅

#### 7.8.4 编码规范

1. **Want 参数构建**：
   ```typescript
   // ✅ 正确：明确指定字段
   let want: Want = {
     bundleName: 'com.example.app',
     abilityName: 'MyAppServiceExtAbility',
     parameters: {
       key: 'value'
     }
   };

   // ❌ 错误：缺少必需字段
   let want: Want = {
     bundleName: 'com.example.app'
     // 缺少 abilityName
   };
   ```

2. **错误处理**：
   ```typescript
   // ✅ 正确：完整的错误处理
   try {
     await context.startAppServiceExtensionAbility(want);
     expect(true).assertTrue();
   } catch (err) {
     if (err.code !== 801) {
       expect().assertFail();
     }
   }

   // ❌ 错误：缺少错误处理
   await context.startAppServiceExtensionAbility(want);
   ```

3. **生命周期验证**：
   ```typescript
   // ✅ 正确：验证生命周期顺序
   let events: string[] = [];
   // ... 启动服务
   expect(events[0]).assertEqual('onCreate');
   expect(events[1]).assertEqual('onRequest');

   // ❌ 错误：不验证顺序
   expect(events).toContain('onCreate');
   ```

### 7.9 参考实例

完整的实现示例位于：
- 启动测试：`ability_runtime/actsaappserviceextensioncontexttest/`
- 连接测试：`ability_runtime/actsaappserviceextensioncontexttest/`
- 服务端实现：`ability_runtime/actsaappserviceextensioncontexttest/actsactsaappserviceextensionrely/entry/src/main/ets/AppServiceExtension/`
- 配置文件：`ability_runtime/actsaappserviceextensioncontexttest/actsactsaappserviceextensionrely/entry/src/main/module.json5`

### 7.10 API 版本说明

- **API 20+**：AppServiceExtensionAbility 从 API 20 开始支持
- **仅 Stage 模型**：不支持 FA 模型
- **Kit 导入**：使用 `import { AppServiceExtensionAbility } from '@kit.AbilityKit';`
- **上下文**：通过 `this.context` 获取 AppServiceExtensionContext
