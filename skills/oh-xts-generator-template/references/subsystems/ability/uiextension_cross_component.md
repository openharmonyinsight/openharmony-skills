# UIExtension 跨组件调用测试规范

> **文档信息**
> - 创建日期: 2026-02-06
> - 适用场景: UIExtension相关接口的跨进程测试
> - 参考用例: SUB_Ability_AbilityRuntime_UIServiceExtension_0700-2000

## 一、概述

UIExtension跨组件调用测试是一种通过startAbility启动目标Ability，在目标Ability中加载EmbeddedComponent启动EmbeddedUIExtensionAbility，并在onSessionCreate中根据parameters执行指定API调用，最后通过commonEventManager返回测试结果的测试方式。

### 适用场景

- ✅ UIExtension相关接口的跨进程测试
- ✅ 需要在独立进程中测试接口行为
- ✅ 需要通过事件机制验证接口调用结果

### 不适用场景

- ❌ 同进程内的直接API调用测试（使用同步测试即可）
- ❌ 不需要跨进程验证的接口测试

## 二、调用链路

```
Ability.test.ets (测试用例)
    ↓ startAbility()
TestAbility2 (由模块自动加载)
    ↓ loadContent("Index2")
Index2.ets
    ↓ EmbeddedComponent()
ExampleEmbeddedAbility (UIExtAbility1)
    ↓ onSessionCreate()
判断case字段 → 调用对应API → 发布事件
    ↓ commonEventManager.publish()
Ability.test.ets (订阅事件)
    ↓ commonEventManager.subscribe()
验证结果 → done()
```

## 三、完整实现流程

### 步骤1：测试用例启动TestAbility2

**文件位置**: `entry/src/ohosTest/ets/test/Ability.test.ets`

```typescript
it('SUB_Ability_AbilityRuntime_UIServiceExtension_0700', Level.LEVEL0, async (done: Function) => {
  let tag = "SUB_Ability_AbilityRuntime_UIServiceExtension_0700";

  if (isSupportCapability && mpEnable) {
    // 1. 创建事件订阅者
    let commonEventSubscribeInfo: commonEventManager.CommonEventSubscribeInfo = {
      events: [tag]  // 使用测试用例编号作为事件名
    };
    await commonEventManager.createSubscriber(commonEventSubscribeInfo).then((subscriber) => {
      sub = subscriber;
      // 2. 订阅事件
      commonEventManager.subscribe(sub, (err, commonEventData) => {
        try {
          expect(commonEventData.parameters?.result).assertEqual(401);
        } catch {}
        commonEventManager.unsubscribe(subscriber, (err, data) => {
          done();
        });
      });
    });

    // 3. 启动TestAbility2
    testAbilityContext.startAbility({
      bundleName: "com.acts.startuiserviceextensiontest",
      abilityName: "TestAbility2",
      parameters:{
        "case":"startUIService",      // 指定要测试的接口
        "caseName":tag,                // 测试用例标识（用于事件订阅）
        "param":null                   // 接口参数（null/undefined/{})
      }
    },(err, data)=>{
      console.info('====> startAbility result ' + err?.code);
    })
  }
})
```

**关键参数说明**：

| 参数 | 说明 | 示例值 |
|-----|------|--------|
| case | 指定要测试的接口类型 | "startUIService", "connectUIService", "disconnectUIService" |
| caseName | 测试用例标识，用作事件名 | "SUB_Ability_AbilityRuntime_UIServiceExtension_0700" |
| param | 接口参数 | null, undefined, {} |

### 步骤2：Index2页面传递参数到EmbeddedComponent

**文件位置**: `entry/src/ohosTest/ets/testability/pages/Index2.ets`

```typescript
import hilog from '@ohos.hilog';
import common from '@ohos.app.ability.common';
import Want from '@ohos.app.ability.Want';

let testAbilityWant:Want;

@Entry
@Component
struct Index {
  @State message: string = 'Hello World'
  private context:common.UIAbilityContext = getContext(this) as common.UIAbilityContext;

  aboutToAppear() {
    hilog.info(0x0000, 'testTag', '%{public}s', 'TestAbility index aboutToAppear');
    // 从AppStorage获取TestAbility2启动时传递的Want
    testAbilityWant = AppStorage.get<Want>('TestAbilityWant') as Want;
    hilog.info(0x0000, 'testTag', '%{public}s', 'TestAbility index aboutToAppear ' + JSON.stringify(testAbilityWant));
  }

  build() {
    Row() {
      Column() {
        Text(this.message)
          .fontSize(50)
          .fontWeight(FontWeight.Bold)
          // 使用EmbeddedComponent启动UIExtension
          EmbeddedComponent({
            bundleName: "com.acts.startuiserviceextensiontest",
            abilityName: "UIExtAbility1",
            parameters:{
              "case":testAbilityWant?.parameters?.case as string,
              "caseName":testAbilityWant?.parameters?.caseName as string,
              "param":testAbilityWant?.parameters?.param  // ⭐ 关键：传递API参数
            }
          }, EmbeddedType.EMBEDDED_UI_EXTENSION)
          .width('100%')
          .height('90%')
          .onTerminated((info)=>{
            this.message = 'Termination: code = ' + info.code + ', want = ' + JSON.stringify(info.want);
            this.context.terminateSelf()
          })
          .onError((error)=>{
            this.message = 'Error: code = ' + error.code;
          })
      }.width('100%')
    }.height('100%')
  }
}
```

**关键点**：
- 从AppStorage获取TestAbility2的Want对象
- 将Want中的parameters完整传递给EmbeddedComponent
- **必须传递param参数**，否则EmbeddedUIExtAbility无法获取API参数

### 步骤3：EmbeddedUIExtAbility接收参数并调用API

**文件位置**: `entry/src/ohosTest/ets/embedded/EmbeddedUIExtAbility.ets`

```typescript
import { EmbeddedUIExtensionAbility, UIExtensionContentSession, Want } from '@kit.AbilityKit';
import { commonEventManager } from '@kit.BasicServicesKit';
import hilog from '@ohos.hilog';
import { BusinessError } from '@ohos.base';
import common from '@ohos.app.ability.common';

const TAG: string = '[ExampleEmbeddedAbility]'

export default class ExampleEmbeddedAbility extends EmbeddedUIExtensionAbility {
  onCreate() {
    console.log(TAG, `onCreate`);
  }

  onSessionCreate(want: Want, session: UIExtensionContentSession) {
    console.log(TAG, `onSessionCreate, want: ${JSON.stringify(want)}`);
    let param: Record<string, UIExtensionContentSession> = {
      'session': session
    };
    let tag = want?.parameters?.caseName as string;
    hilog.info(0x0000, TAG, '%{public}s', `onSessionCreate tag: ${tag}`);

    let storage: LocalStorage = new LocalStorage(param);

    // 根据case字段判断要测试的接口
    if(want?.parameters?.case == 'startUIService'){
      hilog.info(0x0000, tag, '%{public}s', `startUIService with param: ${JSON.stringify(want?.parameters?.param)}`);
      try{
        let param = want?.parameters?.param;
        this.context.startUIServiceExtensionAbility(param).then((data)=>{
          hilog.info(0x0000, tag, '%{public}s', `startUIServiceExtensionAbility success: ${JSON.stringify(data)}`);
        }).catch((err:BusinessError)=>{
          hilog.info(0x0000, tag, '%{public}s', `startUIServiceExtensionAbility failed: ${JSON.stringify(err)}`);
        })
      }catch(err){
        hilog.error(0x0000, tag, '%{public}s', `startUIServiceExtensionAbility catch failed, code is ${JSON.stringify(err)}`);
        // 发布事件，将错误码传递给测试用例
        let commonEventData: commonEventManager.CommonEventPublishData = {
          parameters: {
            'result': err?.code,
          }
        }
        commonEventManager.publish(tag, commonEventData, (result) => {
          hilog.info(0x0000, tag, '%{public}s', `publish event result: ${JSON.stringify(result)}`);
          this.context.terminateSelf()
        });
      }

    }else if(want?.parameters?.case == 'connectUIService'){
      hilog.info(0x0000, tag, '%{public}s', `connectUIService with param: ${JSON.stringify(want?.parameters?.param)}`);
      try{
        let param = want?.parameters?.param;
        let dataCallBack : common.UIServiceExtensionConnectCallback = {
          onData: (data: Record<string, Object>) => {
            hilog.info(0x0000, tag, '%{public}s', `dataCallBack received data: ${JSON.stringify(data)}`);
          },
          onDisconnect: () => {
            hilog.info(0x0000, tag, '%{public}s', `dataCallBack onDisconnect`);
          }
        }
        this.context.connectUIServiceExtensionAbility(param, dataCallBack).then((proxy: common.UIServiceProxy)=>{
          hilog.info(0x0000, tag, '%{public}s', `connectUIServiceExtensionAbility success: ${JSON.stringify(proxy)}`);
        }).catch((err:BusinessError)=>{
          hilog.info(0x0000, tag, '%{public}s', `connectUIServiceExtensionAbility failed: ${JSON.stringify(err)}`);
        })
      }catch(err){
        hilog.error(0x0000, tag, '%{public}s', `connectUIServiceExtensionAbility catch failed, code is ${JSON.stringify(err)}`);
        let commonEventData: commonEventManager.CommonEventPublishData = {
          parameters: {
            'result': err?.code,
          }
        }
        commonEventManager.publish(tag, commonEventData, (result) => {
          hilog.info(0x0000, tag, '%{public}s', `publish event result: ${JSON.stringify(result)}`);
          this.context.terminateSelf()
        });
      }

    }else if(want?.parameters?.case == 'disconnectUIService'){
      hilog.info(0x0000, tag, '%{public}s', `disconnectUIService with param: ${JSON.stringify(want?.parameters?.param)}`);
      try{
        let param = want?.parameters?.param;
        this.context.disconnectUIServiceExtensionAbility(param)
        .then(() => {
          hilog.info(0x0000, tag, '%{public}s', `disconnectUIServiceExtensionAbility succeed`);
        }).catch((err: BusinessError) => {
          hilog.error(0x0000, tag, '%{public}s', `disconnectUIServiceExtensionAbility failed: ${JSON.stringify(err)}`);
        });
      }catch(err){
        hilog.error(0x0000, tag, '%{public}s', `disconnectUIServiceExtensionAbility catch failed, code is ${JSON.stringify(err)}`);
        let commonEventData: commonEventManager.CommonEventPublishData = {
          parameters: {
            'result': err?.code,
          }
        }
        commonEventManager.publish(tag, commonEventData, (result) => {
          hilog.info(0x0000, tag, '%{public}s', `publish event result: ${JSON.stringify(result)}`);
          this.context.terminateSelf()
        });
      }
    }

    session.loadContent('testability/pages/Index', storage);
  }

  onSessionDestroy(session: UIExtensionContentSession) {
    console.log(TAG, `onSessionDestroy`);
  }
}
```

**关键点**：
- 使用hilog记录日志，tag作为domain便于追踪
- 在try-catch中捕获异常，通过commonEventManager.publish发布错误码
- 使用tag（测试用例编号）作为事件名
- 完成后调用terminateSelf()结束进程

### 步骤4：配置module.json5

**文件位置**: `entry/src/ohosTest/module.json5`

```json5
{
  "module": {
    "name": "entry",
    "type": "feature",
    "extensionAbilities": [
      {
        "name": "UIExtAbility1",
        "srcEntry": "./ets/embedded/EmbeddedUIExtAbility.ets",
        "description": "$string:TestAbility_desc",
        "label": "$string:TestAbility_label",
        "type": "ui"
      }
    ]
  }
}
```

**关键配置**：
- name: EmbeddedComponent的abilityName参数
- srcEntry: EmbeddedUIExtAbility文件的相对路径
- type: 必须设置为"ui"

## 四、参数传递链路

```
Ability.test.ets
  ↓ startAbility parameters
  ├─ case: "startUIService"
  ├─ caseName: "SUB_Ability_AbilityRuntime_UIServiceExtension_0700"
  └─ param: null

TestAbility2 (AppStorage)
  ↓ testAbilityWant = AppStorage.get<Want>('TestAbilityWant')

Index2.ets
  ↓ EmbeddedComponent parameters
  ├─ case: testAbilityWant?.parameters?.case
  ├─ caseName: testAbilityWant?.parameters?.caseName
  └─ param: testAbilityWant?.parameters?.param  ⭐ 必须传递

ExampleEmbeddedAbility (onSessionCreate want)
  ↓ want.parameters
  ├─ case: "startUIService"
  ├─ caseName: "SUB_Ability_AbilityRuntime_UIServiceExtension_0700"
  └─ param: null  ⭐ 获取并使用

API调用
  ↓ startUIServiceExtensionAbility(null)
  catch(err: BusinessError)
  ↓ commonEventManager.publish(
    event: "SUB_Ability_AbilityRuntime_UIServiceExtension_0700",
    data: { result: 401 }
  )

Ability.test.ets
  ↓ commonEventManager.subscribe(event: "SUB_Ability_AbilityRuntime_UIServiceExtension_0700")
  expect(commonEventData.parameters?.result).assertEqual(401)
  done()
```

## 五、支持的测试场景

### 5.1 startUIServiceExtensionAbility

| case值 | 测试参数 | 用例编号 | 预期错误码 |
|--------|---------|---------|-----------|
| "startUIService" | null | 0700 | 401 |
| "startUIService" | undefined | 1500 | 401 |
| "startUIService" | {} | 1600 | 16000001 |

### 5.2 connectUIServiceExtensionAbility

| case值 | 测试参数 | 用例编号 | 预期错误码 |
|--------|---------|---------|-----------|
| "connectUIService" | null | 0800 | 401 |
| "connectUIService" | undefined | 1700 | 401 |
| "connectUIService" | {} | 1800 | 16000001 |

### 5.3 disconnectUIServiceExtensionAbility

| case值 | 测试参数 | 用例编号 | 预期错误码 |
|--------|---------|---------|-----------|
| "disconnectUIService" | null | 0900 | 401 |
| "disconnectUIService" | null | 1400 | 401 |
| "disconnectUIService" | undefined | 1900 | 401 |
| "disconnectUIService" | {} | 2000 | 401 |

## 六、关键注意事项

### 6.1 参数传递完整性

⭐ **最重要**: Index2.ets必须将所有参数完整传递给EmbeddedComponent

```typescript
// ✅ 正确：完整传递所有参数
EmbeddedComponent({
  bundleName: "com.acts.startuiserviceextensiontest",
  abilityName: "UIExtAbility1",
  parameters:{
    "case":testAbilityWant?.parameters?.case as string,
    "caseName":testAbilityWant?.parameters?.caseName as string,
    "param":testAbilityWant?.parameters?.param  // ⭐ 必须传递
  }
}, EmbeddedType.EMBEDDED_UI_EXTENSION)

// ❌ 错误：缺少param参数
EmbeddedComponent({
  bundleName: "com.acts.startuiserviceextensiontest",
  abilityName: "UIExtAbility1",
  parameters:{
    "case":testAbilityWant?.parameters?.case as string,
    "caseName":testAbilityWant?.parameters?.caseName as string
    // 缺少param，EmbeddedUIExtAbility无法获取API参数
  }
}, EmbeddedType.EMBEDDED_UI_EXTENSION)
```

### 6.2 日志记录规范

- 使用hilog而不是console.log
- 使用tag（测试用例编号）作为domain，便于日志过滤
- 使用%{public}s格式化输出

```typescript
// ✅ 正确
hilog.info(0x0000, tag, '%{public}s', `startUIService with param: ${JSON.stringify(param)}`);
hilog.error(0x0000, tag, '%{public}s', `API failed: ${JSON.stringify(err)}`);

// ❌ 错误
console.log('startUIService with param:' + JSON.stringify(param));
```

### 6.3 事件发布规范

- 使用tag（测试用例编号）作为事件名
- 错误码通过parameters.result传递

```typescript
// ✅ 正确
let commonEventData: commonEventManager.CommonEventPublishData = {
  parameters: {
    'result': err?.code,
  }
}
commonEventManager.publish(tag, commonEventData, (result) => {
  hilog.info(0x0000, tag, '%{public}s', `publish event result: ${JSON.stringify(result)}`);
  this.context.terminateSelf()
});

// ❌ 错误：事件名不匹配
commonEventManager.publish("someEventName", commonEventData, ...);
```

### 6.4 功能开关检查

跨组件测试通常需要检查功能开关：

```typescript
let isSupportCapability = systemParameterEnhance.getSync('const.abilityms.enable_uiservice') == 'true';
let mpEnable = systemParameterEnhance.getSync('persist.sys.abilityms.multi_process_model') == 'true';

if (isSupportCapability && mpEnable) {
  // 执行跨组件测试
} else if ((isSupportCapability == false) && (mpEnable == false)) {
  console.log(`${tag} function not enable.`);
  expect(true).assertTrue();
  done();
} else {
  console.log(`${tag} wrong param`);
  expect(true).assertTrue();
  done();
}
```

## 七、常见问题

### Q1: 事件订阅收不到结果

**原因**:
1. Index2.ets没有传递param参数
2. EmbeddedUIExtAbility没有使用tag作为事件名
3. commonEventManager.publish没有正确调用

**解决**: 检查参数传递链路的完整性

### Q2: 测试用例超时

**原因**:
1. TestAbility2没有正确加载Index2页面
2. EmbeddedUIExtAbility没有调用terminateSelf()
3. 事件订阅没有正确unsubscribe

**解决**:
1. 检查module.json5配置
2. 确保在catch中调用terminateSelf()
3. 在事件回调中调用unsubscribe

### Q3: 日志查看混乱

**原因**: 没有使用tag作为domain

**解决**: 所有hilog调用使用tag作为domain
```typescript
hilog.info(0x0000, tag, '%{public}s', `message`);
```

## 八、参考示例

完整的参考示例请查看：
- 测试用例: `actsstartuiserviceextensiontest/.../Ability.test.ets` (0700-2000)
- 页面文件: `actsstartuiserviceextensiontest/.../Index2.ets`
- Extension: `actsstartuiserviceextensiontest/.../EmbeddedUIExtAbility.ets`
- 配置文件: `actsstartuiserviceextensiontest/.../module.json5`
