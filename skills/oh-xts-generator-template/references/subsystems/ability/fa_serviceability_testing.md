# FA模型 ServiceAbility 测试规范

> **文档信息**
> - 版本: 1.0.0
> - 创建日期: 2026-02-08
> - 适用模型: FA (Feature Ability) 模型
> - 适用组件: ServiceAbility
> - 学习范本: `/test/xts/acts/ability/ability_runtime/actsserviceabilityclienttest/`

## 一、测试模式概述

### 1.1 核心思想

FA 模型 ServiceAbility 测试采用**事件驱动模式**，通过以下机制实现接口测试：

1. **测试用例层**：使用 `featureAbility.startAbility()` 启动 ServiceAbility
2. **want.action 标识**：通过 `want.action` 字段传递测试用例标识
3. **ServiceAbility 层**：在 `onCommand()` 回调中根据 `action` 判断当前用例
4. **接口调用**：调用待测试的接口
5. **结果返回**：使用 `commonEvent.publish()` 将测试结果返回给测试用例
6. **结果验证**：测试用例订阅事件，接收并验证结果

### 1.2 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                       测试用例层                              │
│  StServiceAbilityClient.test.js                              │
│                                                              │
│  1. commonEvent.createSubscriber()  - 创建事件订阅者          │
│  2. commonEvent.subscribe()         - 订阅测试结果事件        │
│  3. featureAbility.startAbility()   - 启动ServiceAbility     │
│     want.action = "PageStartService_0100"  ← 用例标识         │
│  4. 接收事件并验证结果                                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    ServiceAbility层                          │
│  ServiceAbility1/service.js                                  │
│                                                              │
│  onCommand(want, restart, startId):                         │
│    1. 读取 want.action                                       │
│    2. switch(action) 判断用例                                 │
│    3. 调用待测试接口                                          │
│    4. commonEvent.publish() 返回结果                         │
└─────────────────────────────────────────────────────────────┘
```

## 二、测试用例实现规范

### 2.1 标准测试用例模板

```javascript
import featureAbility from '@ohos.ability.featureAbility'
import commonEvent from '@ohos.commonEvent'
import { describe, it, expect, Level } from '@ohos/hypium'

export default function ActsServiceAbilityTest() {
  describe('ActsServiceAbilityTest', function () {

    // 定义事件订阅信息
    let subscriber0100;
    let CommonEventSubscribeInfo0100 = {
      events: ["ACTS_ServiceAbility_onCommand_PageStartService_0100"],
    };

    /**
     * @tc.name   ACTS_JsServiceAbility_0100
     * @tc.number ACTS_JsServiceAbility_0100
     * @tc.desc   Test ServiceAbility interface (by Promise)
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('ACTS_JsServiceAbility_0100', Level.LEVEL0, async function (done) {
      console.info('ACTS_JsServiceAbility_0100====<begin');

      try {
        // 步骤1: 创建事件订阅者
        await commonEvent.createSubscriber(CommonEventSubscribeInfo0100).then((data) => {
          console.info("createSubscriber success: " + JSON.stringify(data));
          subscriber0100 = data;

          // 步骤2: 订阅事件
          commonEvent.subscribe(subscriber0100, (err, data) => {
            console.info("subscribe callback: " + JSON.stringify(data));

            // 步骤5: 验证事件结果
            expect("ACTS_ServiceAbility_onCommand_PageStartService_0100")
              .assertEqual(data.event);

            // 步骤6: 取消订阅
            commonEvent.unsubscribe(subscriber0100, (err) => {
              console.info("unsubscribe success");
            });

            console.info('ACTS_JsServiceAbility_0100====<end');
            done();
          });
        });

        // 步骤3: 启动ServiceAbility，通过action标识用例
        featureAbility.startAbility({
          want: {
            bundleName: "com.example.test",
            abilityName: "ServiceAbility1",
            action: "PageStartService_0100",  // ← 用例标识
          },
        }).then(data => {
          console.info("startAbility success: " + JSON.stringify(data));
        }).catch(err => {
          console.info('startAbility failed: ' + JSON.stringify(err));
          expect().assertFail();
          done();
        });

      } catch (err) {
        expect().assertFail();
        console.info('ACTS_JsServiceAbility_0100==== err: ' + JSON.stringify(err));
        done();
      }
    })
  })
}
```

### 2.2 命名规范

#### 2.2.1 事件名称规范

**事件名称格式**: `ACTS_[组件]_[生命周期]_[调用方]_[接口]_[用例编号]`

**示例**:
- `ACTS_ServiceAbility_onCommand_PageStartService_0100`
  - `ACTS_`: 固定前缀
  - `ServiceAbility`: 组件名称
  - `onCommand`: 生命周期回调
  - `PageStartService`: 调用方（Page表示从Ability调用）
  - `0100`: 用例编号

#### 2.2.2 action 标识规范

**action 格式**: `[调用方][接口]_[用例编号]`

**常见调用方标识**:
- `Page`: 从 Page Ability 调用
- `Service`: 从 Service Ability 调用

**示例**:
- `PageStartService_0100` - Page调用startAbility接口
- `ServiceStartService_0900` - Service调用startAbility接口
- `PageConnectService_0500` - Page调用connectAbility接口

### 2.3 多步骤测试用例

某些测试用例需要多次启动ServiceAbility来验证不同场景：

```javascript
it('ACTS_JsServiceAbility_0300', Level.LEVEL0, async function (done) {
  console.info('ACTS_JsServiceAbility_0300====<begin');

  // 订阅多个事件
  let CommonEventSubscribeInfo0300 = {
    events: [
      "ACTS_ServiceAbility_onCommand_PageStartService_0300",
      "ACTS_ServiceAbility_onCommand_PageStartService_0301",
    ],
  };

  await commonEvent.createSubscriber(CommonEventSubscribeInfo0300).then((data) => {
    subscriber0300 = data;

    commonEvent.subscribe(subscriber0300, (err, data) => {
      // 根据事件名称判断当前是第几步
      if (data.event == "ACTS_ServiceAbility_onCommand_PageStartService_0300") {
        // 第一步完成，启动第二步
        featureAbility.startAbility({
          want: {
            bundleName: bundleName,
            abilityName: abilityName,
            action: "PageStartService_0301",  // 第二步的action
          },
        });
      } else {
        // 第二步完成，验证结果
        expect("ACTS_ServiceAbility_onCommand_PageStartService_0301")
          .assertEqual(data.event);
        commonEvent.unsubscribe(subscriber0300);
        done();
      }
    });
  });

  // 启动第一步
  featureAbility.startAbility({
    want: {
      bundleName: bundleName,
      abilityName: abilityName,
      action: "PageStartService_0300",  // 第一步的action
    },
  });
})
```

## 三、ServiceAbility 实现规范

### 3.1 onCommand 回调实现模板

```javascript
// ServiceAbility1/service.js
import commonEvent from '@ohos.commonEvent'
import particleAbility from '@ohos.ability.particleAbility'

export default {
  onStart(want) {
    console.info('ServiceAbility onStart: ' + JSON.stringify(want));
    commonEvent.publish('ACTS_ServiceAbility_onStart', (err) => {});
  },

  onStop() {
    console.info('ServiceAbility onStop');
    commonEvent.publish('ACTS_ServiceAbility_onStop', (err) => {});
  },

  onCommand(want, restart, startId) {
    console.info('ServiceAbility onCommand: ' + JSON.stringify(want));

    // 根据 action 判断用例
    if (want.action === 'PageStartService_0100') {
      // 用例 0100: 测试某个接口
      try {
        // 调用待测试的接口
        let result = particleAbility.someInterface();

        // 发布成功事件
        commonEvent.publish('ACTS_ServiceAbility_onCommand_PageStartService_0100', {
          parameters: {
            result: 'success',
            data: result
          }
        }, (err) => {
          console.info('publish event success');
        });
      } catch (err) {
        // 发布失败事件
        commonEvent.publish('ACTS_ServiceAbility_onCommand_PageStartService_0100', {
          parameters: {
            result: 'fail',
            error: err.code
          }
        });
      }
    } else if (want.action === 'PageStartService_0200') {
      // 用例 0200: 测试另一个接口
      // ...
    } else {
      // 默认处理：发布事件
      commonEvent.publish('ACTS_ServiceAbility_onCommand_' + want.action, (err) => {
        if (!err.code) {
          console.info('publish event: ' + want.action);
        }
      });
    }
  },

  onConnect(want) {
    console.info('ServiceAbility onConnect: ' + JSON.stringify(want));
    // 连接相关测试
  },

  onDisconnect(elementName) {
    console.info('ServiceAbility onDisconnect: ' + JSON.stringify(elementName));
    // 断开连接相关测试
  },
}
```

### 3.2 switch-case 模式（推荐）

对于多个测试用例，推荐使用 switch-case 结构：

```javascript
onCommand(want, restart, startId) {
  console.info('ServiceAbility onCommand action: ' + want.action);

  let action = want.action;
  let eventName = 'ACTS_ServiceAbility_onCommand_' + action;

  try {
    switch(action) {
      case 'PageStartService_0100':
        // 测试接口1 - Promise方式
        particleAbility.startAbility({
          want: {
            bundleName: 'com.example.test',
            abilityName: 'ServiceAbility2',
          }
        });
        break;

      case 'PageStartService_0200':
        // 测试接口2 - Callback方式
        particleAbility.startAbility({
          want: {
            bundleName: 'com.example.test',
            abilityName: 'ServiceAbility2',
          }
        }, (err, data) => {
          console.info('callback result: ' + JSON.stringify(data));
        });
        break;

      case 'PageStartService_0300':
        // 测试接口3 - 带参数
        let value = particleAbility.acquireDataAbilityHelper(
          'dataability:///com.example.DataAbility'
        );
        commonEvent.publish(eventName, {
          parameters: { result: value }
        });
        break;

      default:
        // 默认处理
        console.info('Unknown action: ' + action);
        break;
    }

    // 发布事件通知测试用例
    if (action !== 'default') {
      commonEvent.publish(eventName, (err) => {
        if (!err.code) {
          console.info('Event published: ' + eventName);
        }
      });
    }
  } catch (err) {
    console.error('onCommand error: ' + err.code);
    commonEvent.publish(eventName, {
      parameters: { error: err.code }
    });
  }
}
```

## 四、ConnectAbility 测试规范

### 4.1 测试用例模板

```javascript
it('ACTS_JsServiceAbility_0500', Level.LEVEL0, async function (done) {
  console.info('ACTS_JsServiceAbility_0500====<begin');

  // 定义三个事件：连接、断开、回调
  let CommonEventSubscribeInfo0500 = {
    events: [
      "ACTS_ServiceAbility_onConnect_PageConnectService_0500",
      "ACTS_ServiceAbility_onDisconnect_PageConnectService_0500",
      "ACTS_ServiceAbility_onConnectCallback_PageConnectService_0500"
    ],
  };

  await commonEvent.createSubscriber(CommonEventSubscribeInfo0500).then((data) => {
    subscriber0500 = data;

    commonEvent.subscribe(subscriber0500, (err, data) => {
      console.info("subscribe: " + data.event);

      if (data.event == "ACTS_ServiceAbility_onConnect_PageConnectService_0500") {
        // 连接成功，断开连接
        featureAbility.disconnectAbility(connectionId);
      } else if (data.event == "ACTS_ServiceAbility_onDisconnect_PageConnectService_0500") {
        // 断开成功，完成测试
        expect("ACTS_ServiceAbility_onDisconnect_PageConnectService_0500")
          .assertEqual(data.event);
        commonEvent.unsubscribe(subscriber0500);
        done();
      }
    });
  });

  // 连接 ServiceAbility
  let connectionId = featureAbility.connectAbility({
    bundleName: "com.example.test",
    abilityName: "ServiceAbility1",
    action: "PageConnectService_0500",
  }, {
    onConnect: (elementName, proxy) => {
      console.info('onConnect: ' + JSON.stringify(elementName));
    },
    onDisconnect: (elementName) => {
      console.info('onDisconnect: ' + JSON.stringify(elementName));
    },
    onFailed: (code) => {
      console.info('onFailed: ' + code);
    }
  });
})
```

### 4.2 ServiceAbility 连接处理

```javascript
onConnect(want) {
  console.info('onConnect: ' + JSON.stringify(want));
  let action = want.action;

  // 返回 RemoteObject
  return new StubTest('remoteObject');
}

onDisconnect(elementName) {
  console.info('onDisconnect: ' + JSON.stringify(elementName));

  // 发布断开连接事件
  commonEvent.publish('ACTS_ServiceAbility_onDisconnect_' +
    this.currentAction, (err) => {});
}
```

## 五、最佳实践

### 5.1 事件管理

```javascript
// 辅助函数：取消订阅
function unsubscribe(caller, subscriber) {
  commonEvent.unsubscribe(subscriber, (err, data) => {
    console.info(caller + " unsubscribe: " +
      JSON.stringify(data));
  });
}

// 使用
commonEvent.subscribe(subscriber, (err, data) => {
  expect("ExpectedEvent").assertEqual(data.event);
  unsubscribe("TestName_0100", subscriber);
  done();
});
```

### 5.2 延迟处理

```javascript
// ServiceAbility 中可能需要延迟
function sleep(delay) {
  let start = new Date().getTime();
  while (true) {
    if (new Date().getTime() - start > delay) {
      break;
    }
  }
}

onCommand(want, restart, startId) {
  if (want.action === 'ServiceStartService_0900') {
    particleAbility.startAbility({ /* ... */ });
    sleep(600);  // 等待启动完成
  }
}
```

### 5.3 afterEach 清理

```javascript
describe('ActsServiceAbilityTest', function () {
  let gSetTimeout = 2000;

  afterEach(async (done) => {
    setTimeout(function () {
      done();
    }, gSetTimeout);
  });

  // 测试用例...
})
```

## 六、常见问题

### 6.1 事件未收到

**问题**: 测试用例一直等待，收不到事件

**可能原因**:
1. 事件名称不匹配
2. ServiceAbility 未启动
3. action 标识错误

**解决方案**:
```javascript
// 检查事件名称是否一致
let testName = "PageStartService_0100";
let event1 = "ACTS_ServiceAbility_onCommand_" + testName;
let event2 = "ACTS_ServiceAbility_onCommand_" + want.action;  // 在ServiceAbility中

// 确保一致
console.info("Event1: " + event1);
console.info("Event2: " + event2);
```

### 6.2 多个用例互相干扰

**问题**: 前一个用例的事件影响后一个用例

**解决方案**:
- 每个用例使用唯一的订阅者
- afterEach 中设置足够的延迟
- 每个用例取消订阅

```javascript
afterEach(async (done) => {
  setTimeout(function () {
    done();
  }, 2000);  // 给予足够时间清理
})
```

### 6.3 action 大小写问题

**问题**: action 匹配失败

**解决方案**:
```javascript
// 统一使用 PascalCase 或 camelCase
// 测试用例中
action: "PageStartService_0100"

// ServiceAbility 中
if (want.action === 'PageStartService_0100') {  // 注意大小写
  // ...
}
```

## 七、生命周期测试补充规范（基于 SUB_AA_OpenHarmony_Test_ServiceAbility_0200）

> **参考范本**: `/test/xts/acts/ability/ability_runtime/faapicover/faapicoverhaptest/entry/src/ohosTest/ets/test/VerificationTest.ets`
> **行数**: 369-450
> **测试场景**: ServiceAbility 连接/断开生命周期完整测试

### 7.1 核心测试模式

**不使用 action 标识的生命周期测试模式**：

1. **测试用例层**：
   - 订阅 ServiceAbility 的生命周期事件（onConnect, onDisconnect）
   - 调用 `connectAbility()` 连接 Service
   - 在 `onConnect` 事件回调中调用 `disconnectAbility()`
   - 在 `onDisconnect` 事件回调中验证测试结果

2. **ServiceAbility 层**：
   - 在 `onConnect()` 回调中发送事件
   - 在 `onDisconnect()` 回调中发送事件
   - 无需判断 action，直接发送固定事件名

3. **测试验证**：
   - 验证生命周期事件顺序（先 onConnect，后 onDisconnect）
   - 验证连接回调状态（onConnect 成功，onFailed 未触发）

### 7.2 Connect/Disconnect 生命周期测试模板

```typescript
/**
 * @tc.name   SUB_AA_OpenHarmony_Test_ServiceAbility_0200
 * @tc.number SUB_AA_OpenHarmony_Test_ServiceAbility_0200
 * @tc.desc   Test ServiceAbility connect/disconnect lifecycle
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_AA_OpenHarmony_Test_ServiceAbility_0200', Level.LEVEL0, async (done: Function) => {
  const TAG = 'SUB_AA_OpenHarmony_Test_ServiceAbility_0200 ==>';
  console.info(TAG + 'start');

  try {
    // 1. 定义生命周期追踪变量
    let lifecycleList: string[] = [];
    let lifecycleListCheck = ["onConnect", "onDisconnect"];

    let flagOnConnect = false;
    let flagOnDisconnect = false;
    let flagOnFailed = false;

    // 2. 定义事件订阅信息
    let subscriber: commonEvent.CommonEventSubscriber | undefined = undefined;
    let subscribeInfo: commonEvent.CommonEventSubscribeInfo = {
      events: [
        "Fa_Auxiliary_ServiceAbility2_onConnect",
        "Fa_Auxiliary_ServiceAbility2_onDisconnect"
      ]
    };

    // 3. 定义事件订阅回调
    let SubscribeInfoCallback = async (err: BusinessError, data: commonEvent.CommonEventData) => {
      console.info(TAG + "===SubscribeInfoCallback===" + JSON.stringify(data))

      if (data.event == "Fa_Auxiliary_ServiceAbility2_onConnect") {
        // 4. 记录 onConnect 事件
        lifecycleList.push("onConnect");

        // 5. 触发断开连接
        await ability_featureAbility.disconnectAbility(connectionId).then((data) => {
          console.info(TAG + "disconnectAbility data = " + JSON.stringify(data));
        }).catch((err: BusinessError) => {
          console.info(TAG + "disconnectAbility err = " + JSON.stringify(err));
          expect().assertFail();
          done();
        });
      }

      if (data.event == "Fa_Auxiliary_ServiceAbility2_onDisconnect") {
        // 6. 记录 onDisconnect 事件
        lifecycleList.push("onDisconnect");

        // 7. 延迟验证（等待异步操作完成）
        setTimeout(() => {
          // 8. 验证生命周期事件顺序
          expect(JSON.stringify(lifecycleList)).assertEqual(JSON.stringify(lifecycleListCheck));

          // 9. 验证连接状态
          expect(flagOnConnect).assertTrue();      // onConnect 被调用
          expect(flagOnDisconnect).assertTrue();   // onDisconnect 被调用
          expect(flagOnFailed).assertFalse();      // onFailed 未被调用

          // 10. 取消订阅并完成测试
          commonEvent.unsubscribe(subscriber, UnSubscribeInfoCallback);
        }, 1000)
      }
    }

    let UnSubscribeInfoCallback = () => {
      console.info(TAG + "===UnSubscribeInfoCallback===")
      done()
    }

    // 11. 创建订阅者并订阅事件
    commonEvent.createSubscriber(subscribeInfo, (err, data) => {
      console.info(TAG + "===CreateSubscriberCallback===")
      subscriber = data
      commonEvent.subscribe(subscriber, SubscribeInfoCallback)
    })

    // 12. 连接 ServiceAbility
    let connectionId = ability_featureAbility.connectAbility(
      {
        bundleName: 'com.example.faapicoverhaptest',
        abilityName: 'com.example.faapicoverhaptest.ServiceAbility2'
      },
      {
        onConnect: (elementName, proxy) => {
          flagOnConnect = true
          console.info(TAG + 'Ext onConnect SUCCESS, elementName = ' + JSON.stringify(elementName));
          if (proxy == null) {
            console.info(TAG + 'Ext proxy == null');
            return;
          }
        },
        onDisconnect: (elementName) => {
          flagOnDisconnect = true
          console.info(TAG + 'Ext onDisconnect, elementName = ' + JSON.stringify(elementName));
        },
        onFailed: (number) => {
          flagOnFailed = true
          console.info(TAG + 'Ext onFailed, number = ' + number);
        }
      }
    )
  } catch (err) {
    console.info(TAG + "catch err = " + JSON.stringify(err));
    expect().assertFail();
    done();
  }
})
```

### 7.3 ServiceAbility 端实现规范

```javascript
// ServiceAbility2/service.js
import commonEvent from '@ohos.commonEvent'

export default {
  onConnect(want) {
    console.info('ServiceAbility onConnect: ' + JSON.stringify(want));

    // 发送 onConnect 事件到测试用例
    commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onConnect', (err) => {
      if (!err.code) {
        console.info('Fa_Auxiliary_ServiceAbility2_onConnect published successfully');
      } else {
        console.error('Fa_Auxiliary_ServiceAbility2_onConnect publish failed: ' + JSON.stringify(err));
      }
    });

    // 返回 RemoteObject
    return new RemoteObject('test');
  },

  onDisconnect(elementName) {
    console.info('ServiceAbility onDisconnect: ' + JSON.stringify(elementName));

    // 发送 onDisconnect 事件到测试用例
    commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onDisconnect', (err) => {
      if (!err.code) {
        console.info('Fa_Auxiliary_ServiceAbility2_onDisconnect published successfully');
      } else {
        console.error('Fa_Auxiliary_ServiceAbility2_onDisconnect publish failed: ' + JSON.stringify(err));
      }
    });
  }
}
```

### 7.4 关键实现要点

#### 7.4.1 生命周期事件顺序验证

使用数组追踪事件顺序：

```typescript
// 定义预期顺序
let lifecycleListCheck = ["onConnect", "onDisconnect"];

// 追踪实际发生的事件
let lifecycleList: string[] = [];

// 在事件回调中记录
if (data.event == "Fa_Auxiliary_ServiceAbility2_onConnect") {
  lifecycleList.push("onConnect")
}
if (data.event == "Fa_Auxiliary_ServiceAbility2_onDisconnect") {
  lifecycleList.push("onDisconnect")
}

// 验证顺序
expect(JSON.stringify(lifecycleList)).assertEqual(JSON.stringify(lifecycleListCheck));
```

#### 7.4.2 连接状态标志验证

```typescript
// 定义连接状态标志
let flagOnConnect = false;      // onConnect 是否被调用
let flagOnDisconnect = false;   // onDisconnect 是否被调用
let flagOnFailed = false;       // onFailed 是否被调用

// 在 connectAbility 回调中设置
let connectionId = ability_featureAbility.connectAbility(
  { /* want */ },
  {
    onConnect: (elementName, proxy) => {
      flagOnConnect = true
      // ...
    },
    onDisconnect: (elementName) => {
      flagOnDisconnect = true
      // ...
    },
    onFailed: (number) => {
      flagOnFailed = true
      // ...
    }
  }
)

// 最终验证
expect(flagOnConnect).assertTrue();      // 应该被调用
expect(flagOnDisconnect).assertTrue();   // 应该被调用
expect(flagOnFailed).assertFalse();      // 不应该被调用
```

#### 7.4.3 在 onConnect 事件中触发断开连接

```typescript
if (data.event == "Fa_Auxiliary_ServiceAbility2_onConnect") {
  lifecycleList.push("onConnect");

  // 收到 onConnect 事件后，立即触发断开连接
  await ability_featureAbility.disconnectAbility(connectionId).then((data) => {
    console.info(TAG + "disconnectAbility data = " + JSON.stringify(data));
  }).catch((err: BusinessError) => {
    console.info(TAG + "disconnectAbility err = " + JSON.stringify(err));
    expect().assertFail();
    done();
  });
}
```

#### 7.4.4 使用延迟验证

由于事件发送和接收都是异步操作，需要使用 setTimeout 延迟验证：

```typescript
if (data.event == "Fa_Auxiliary_ServiceAbility2_onDisconnect") {
  lifecycleList.push("onDisconnect");

  setTimeout(() => {
    // 验证所有断言
    expect(JSON.stringify(lifecycleList)).assertEqual(JSON.stringify(lifecycleListCheck));
    expect(flagOnConnect).assertTrue();
    expect(flagOnDisconnect).assertTrue();
    expect(flagOnFailed).assertFalse();

    // 取消订阅
    commonEvent.unsubscribe(subscriber, UnSubscribeInfoCallback);
  }, 1000)  // 延迟 1 秒
}
```

### 7.5 与 action 标识模式的对比

| 特性 | action 标识模式 | 生命周期事件模式 |
|------|----------------|------------------|
| **适用场景** | 需要在 onCommand 中测试不同接口 | 验证生命周期回调顺序和状态 |
| **事件命名** | `ACTS_ServiceAbility_onCommand_PageStartService_0100` | `Fa_Auxiliary_ServiceAbility2_onConnect` |
| **action 使用** | 必须设置 want.action | 不需要 action |
| **测试逻辑位置** | ServiceAbility 的 onCommand 中 | 测试用例的事件回调中 |
| **参考用例** | SUB_AA_OpenHarmony_Test_ServiceAbility_0100 | SUB_AA_OpenHarmony_Test_ServiceAbility_0200 |

### 7.6 StartAbility 生命周期测试

**参考范本**: `/test/xts/acts/ability/ability_runtime/faapicover/faapicoverhaptest/entry/src/ohosTest/ets/test/VerificationTest.ets`
**行数**: 318-367

```typescript
/**
 * @tc.name   SUB_AA_OpenHarmony_Test_ServiceAbility_0100
 * @tc.number SUB_AA_OpenHarmony_Test_ServiceAbility_0100
 * @tc.desc   Test ServiceAbility startAbility lifecycle (onCommand)
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_AA_OpenHarmony_Test_ServiceAbility_0100', Level.LEVEL0, async (done: Function) => {
  const TAG = 'SUB_AA_OpenHarmony_Test_ServiceAbility_0100 ==>';

  try {
    let subscriber: commonEvent.CommonEventSubscriber | undefined = undefined;
    let subscribeInfo: commonEvent.CommonEventSubscribeInfo = {
      events: ["Fa_Auxiliary_ServiceAbility_onCommand"]
    }

    let SubscribeInfoCallback = (err: BusinessError, data: commonEvent.CommonEventData) => {
      console.info(TAG + "===SubscribeInfoCallback===" + JSON.stringify(data))

      if (data.event == "Fa_Auxiliary_ServiceAbility_onCommand") {
        // 验证 onCommand 事件被触发
        commonEvent.unsubscribe(subscriber, UnSubscribeInfoCallback);
      }
    }

    let UnSubscribeInfoCallback = () => {
      console.info(TAG + "===UnSubscribeInfoCallback===")
      done()
    }

    // 创建订阅者并订阅事件
    commonEvent.createSubscriber(subscribeInfo, (err, data) => {
      console.info(TAG + "===CreateSubscriberCallback===")
      subscriber = data
      commonEvent.subscribe(subscriber, SubscribeInfoCallback)
    })

    // 启动 ServiceAbility
    await ability_featureAbility.startAbility({
      want: {
        bundleName: 'com.example.faapicoverhaptest',
        abilityName: 'com.example.faapicoverhaptest.ServiceAbility'
      }
    }).then((data) => {
      console.info(TAG + "startAbility data = " + JSON.stringify(data));
    }).catch((err: BusinessError) => {
      console.info(TAG + "startAbility err = " + JSON.stringify(err));
      expect().assertFail();
      done();
    });
  } catch (err) {
    console.info(TAG + "catch err = " + JSON.stringify(err));
    expect().assertFail();
    done();
  }
})
```

### 7.7 事件命名规范

#### 7.7.1 生命周期事件命名格式

**格式**: `[测试模块]_[组件名]_[生命周期]`

**示例**:
- `Fa_Auxiliary_ServiceAbility_onCommand`
- `Fa_Auxiliary_ServiceAbility2_onConnect`
- `Fa_Auxiliary_ServiceAbility2_onDisconnect`
- `Fa_Auxiliary_MainAbility_HasWindowFocus`
- `Fa_Auxiliary_MainAbility_onDestroy`
- `Fa_Auxiliary_MainAbility4_onCreate`

**命名要素**:
- **测试模块**: `Fa_Auxiliary_` - FA 模型辅助测试模块
- **组件名**: 具体的 Ability 名称，如 `ServiceAbility`, `ServiceAbility2`, `MainAbility`, `MainAbility4`
- **生命周期**: 回调方法名，如 `onStart`, `onStop`, `onCommand`, `onConnect`, `onDisconnect`, `onCreate`, `onDestroy`, `HasWindowFocus`

#### 7.7.2 命名一致性

测试用例中的事件订阅和 ServiceAbility 中的事件发布必须使用完全相同的名称：

```typescript
// 测试用例中订阅
let subscribeInfo: commonEvent.CommonEventSubscribeInfo = {
  events: ["Fa_Auxiliary_ServiceAbility2_onConnect", "Fa_Auxiliary_ServiceAbility2_onDisconnect"]
}
```

```javascript
// ServiceAbility 中发布
commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onConnect', ...)
commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onDisconnect', ...)
```

### 7.8 最佳实践总结

#### 7.8.1 事件驱动测试流程

```
1. 测试用例创建事件订阅者
   ↓
2. 订阅 ServiceAbility 的生命周期事件
   ↓
3. 调用 connectAbility() 连接 Service
   ↓
4. ServiceAbility.onConnect() 被触发，发送事件
   ↓
5. 测试用例收到 onConnect 事件
   ↓
6. 测试用例调用 disconnectAbility()
   ↓
7. ServiceAbility.onDisconnect() 被触发，发送事件
   ↓
8. 测试用例收到 onDisconnect 事件
   ↓
9. 验证生命周期顺序和状态
   ↓
10. 取消订阅，完成测试
```

#### 7.8.2 错误处理

```typescript
// 在每个异步操作中添加错误处理
try {
  // 主要测试逻辑
} catch (err) {
  console.info(TAG + "catch err = " + JSON.stringify(err));
  expect().assertFail();
  done();
}

// 在 disconnectAbility 中添加错误处理
await ability_featureAbility.disconnectAbility(connectionId).then((data) => {
  console.info(TAG + "disconnectAbility data = " + JSON.stringify(data));
}).catch((err: BusinessError) => {
  console.info(TAG + "disconnectAbility err = " + JSON.stringify(err));
  expect().assertFail();
  done();
});
```

#### 7.8.3 日志输出规范

```typescript
// 使用 TAG 标识当前用例
const TAG = 'SUB_AA_OpenHarmony_Test_ServiceAbility_0200 ==>';

// 使用统一的前缀输出关键步骤
console.info(TAG + "===CreateSubscriberCallback===")
console.info(TAG + "===SubscribeInfoCallback===" + JSON.stringify(data))
console.info(TAG + "===UnSubscribeInfoCallback===")
```

## 八、完整示例

参考文件:
- 测试用例: `/test/xts/acts/ability/ability_runtime/faapicover/faapicoverhaptest/entry/src/ohosTest/ets/test/VerificationTest.ets`
  - SUB_AA_OpenHarmony_Test_ServiceAbility_0100 (行318-367) - StartAbility 生命周期测试
  - SUB_AA_OpenHarmony_Test_ServiceAbility_0200 (行369-450) - Connect/Disconnect 生命周期测试

ServiceAbility 实现:
- `/test/xts/acts/ability/ability_runtime/faapicover/faapicoverhaptest/entry/src/main/js/ServiceAbility/service.js`
- `/test/xts/acts/ability/ability_runtime/faapicover/faapicoverhaptest/entry/src/main/js/ServiceAbility2/service.js`

## 九、版本历史

- **v1.1.0** (2026-02-08): 新增生命周期测试补充规范
  - 添加 SUB_AA_OpenHarmony_Test_ServiceAbility_0200 参考范本
  - 补充 Connect/Disconnect 生命周期事件流测试规范
  - 提供完整的测试用例模板和实现规范
  - 说明生命周期事件顺序验证方法
  - 添加与 action 标识模式的对比说明
  - 补充 StartAbility 生命周期测试模板
  - 统一事件命名规范
  - 总结最佳实践
- **v1.0.0** (2026-02-08): 初始版本
  - 定义 FA 模型 ServiceAbility 测试规范
  - 提供完整的测试用例模板
  - 说明事件驱动机制的实现流程
  - 包含最佳实践和常见问题解决方案
