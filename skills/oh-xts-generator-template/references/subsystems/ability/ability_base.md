# Ability Base 模块配置

> **模块信息**
> - 所属子系统: Ability
> - 模块名称: Ability Base（Ability 基础能力）
> - API 类型: 基础能力接口
> - 版本: 1.0.0
> - 更新日期: 2026-02-03

## 一、模块特有配置

### 1.1 模块概述

Ability Base 模块包含 Ability 的基础能力相关 API，主要涵盖：
- Context 相关：AbilityContext、AbilityStageContext、UIAbilityContext
- Want 相关：Want、WantAgent
- 错误码：Ability 相关的错误码定义
- 常量：Ability 相关常量定义

### 1.2 API 声明文件

**Context 相关**：
- `@ohos.app.ability.AbilityStageContext.d.ts`
- `@ohos.app.ability.UIAbilityContext.d.ts`
- `@ohos.app.ability.Context.d.ts`
- `@ohos.application.AbilityContext.d.ts`

**Want 相关**：
- `@ohos.app.ability.Want.d.ts`
- `@ohos.app.ability.WantAgent.d.ts`
- `@ohos.ability.wantConstant.d.ts`

**错误码**：
- `@ohos.ability.errorCode.d.ts`

### 1.3 通用配置继承

本模块继承 Ability 子系统通用配置：
- **测试路径规范**：见 `ability/_common.md` 第 1.2 节
- **通用测试规则**：见 `ability/_common.md` 第 2 节
- **代码模板**：见 `ability/_common.md` 第 4 节

## 二、模块特有 API 列表

### 2.1 Want 相关 API

| API名称 | 说明 | 优先级 |
|---------|------|--------|
| Want.bundleName | 应用包名 | LEVEL0 |
| Want.abilityName | Ability 名称 | LEVEL0 |
| Want.moduleName | 模块名称 | LEVEL0 |
| Want.deviceId | 设备 ID | LEVEL1 |
| Want.action | 动作 | LEVEL1 |
| Want.entities | 实体数组 | LEVEL1 |
| Want.uri | URI | LEVEL1 |
| Want.type | MIME 类型 | LEVEL1 |
| Want.flags | 标志位 | LEVEL2 |
| Want.parameters | 参数对象 | LEVEL0 |

### 2.2 WantAgent 相关 API

| API名称 | 说明 | 优先级 |
|---------|------|--------|
| getWantAgent | 获取 WantAgent 对象 | LEVEL0 |
| triggerWantAgent | 触发 WantAgent | LEVEL0 |
| cancelWantAgent | 取消 WantAgent | LEVEL1 |
| getWantAgentInfo | 获取 WantAgent 信息 | LEVEL2 |

### 2.3 Context 相关 API

**UIAbilityContext**：
| API名称 | 说明 | 优先级 |
|---------|------|--------|
| startAbility | 启动 Ability | LEVEL0 |
| startAbilityForResult | 启动 Ability 并获取结果 | LEVEL0 |
| terminateSelf | 终止当前 Ability | LEVEL0 |
| getBundleName | 获取应用包名 | LEVEL0 |
| getModuleName | 获取模块名 | LEVEL0 |
| getAbilityInfo | 获取 Ability 信息 | LEVEL1 |
| getWindow | 获取窗口对象 | LEVEL1 |

**AbilityStageContext**：
| API名称 | 说明 | 优先级 |
|---------|------|--------|
| getBundleName | 获取应用包名 | LEVEL0 |
| getModuleName | 获取模块名 | LEVEL0 |
| createModuleContext | 创建模块上下文 | LEVEL1 |

### 2.4 常量和错误码

**WantConstant**：
| 常量名称 | 说明 | 优先级 |
|---------|------|--------|
| Flags | Want 标志位常量 | LEVEL1 |
| Params | Want 参数常量 | LEVEL1 |

**Ability 错误码**：
| 错误码 | 说明 | 优先级 |
|-------|------|--------|
| 16000001 | 内部错误 | LEVEL1 |
| 16000002 | Ability 不存在 | LEVEL1 |
| 16000003 | Ability 启动失败 | LEVEL1 |
| 16000004 | Ability 连接失败 | LEVEL1 |

## 三、模块特有测试规则

### 3.1 Want 测试规则

1. **Want 对象构造测试**
   - 验证必需字段：bundleName、abilityName
   - 验证可选字段的正确性
   - 测试边界值和异常值

2. **Want 参数测试**
   - parameters 支持基本类型
   - parameters 支持复杂对象
   - 参数序列化和反序列化

### 3.2 WantAgent 测试规则

1. **WantAgent 构造测试**
   - 验证 WantAgentInfo 参数
   - 测试不同的 OperationType
   - 验证 flags 设置

2. **WantAgent 触发测试**
   - 验证同步触发
   - 验证异步触发
   - 测试触发结果

### 3.3 Context 测试规则

1. **Context 获取测试**
   - 验证 Context 的获取方法
   - 测试 Context 的生命周期
   - 验证 Context 的权限检查

2. **Context 功能测试**
   - 验证启动 Ability 功能
   - 测试信息获取功能
   - 验证资源访问功能

### 3.4 事件相关测试（重要）

**必须参考文档**：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-basic-services-kit/js-apis-commonEventManager.md

**CommonEventManager 测试规则**：
- 测试事件发布功能
- 测试事件订阅功能
- 验证事件参数传递
- 测试事件取消订阅
- 验证事件权限管理

## 四、模块特有代码模板

### 4.1 Want 对象验证模板

```typescript
it('SUB_AA_Want_Verification_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_AA_Want_Verification_0100-------------')
  try {
    const want: Want = {
      bundleName: 'com.example.test',
      abilityName: '.MainAbility',
      moduleName: 'entry',
      deviceId: '',
      action: 'action.system.home',
      entities: ['entity.system.home'],
      parameters: {
        key: 'value'
      }
    }

    // 验证 Want 对象属性
    expect(want?.bundleName).assertEqual('com.example.test')
    expect(want?.abilityName).assertEqual('.MainAbility')
    expect(want?.moduleName).assertEqual('entry')
    expect(want?.parameters?.key).assertEqual('value')

    hilog.info(0x0000, 'testTag', 'SUB_AA_Want_Verification_0100 Want verification successful')
    done()
  } catch (err: BusinessError) {
    hilog.info(0x0000, 'testTag', 'SUB_AA_Want_Verification_0100 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

### 4.2 WantAgent 测试模板

```typescript
import wantAgent from '@ohos.app.ability.wantAgent'

it('SUB_AA_WantAgent_GetWantAgent_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_AA_WantAgent_GetWantAgent_0100-------------')
  try {
    const wantAgentInfo: wantAgent.WantAgentInfo = {
      wants: [
        {
          bundleName: 'com.example.test',
          abilityName: '.MainAbility',
          moduleName: 'entry'
        } as Want
      ],
      operationType: wantAgent.OperationType.START_ABILITY,
      requestCode: 0,
      wantAgentFlags: [wantAgent.WantAgentFlags.UPDATE_PRESENT_FLAG]
    }

    const wantAgentObj = await wantAgent.getWantAgent(wantAgentInfo)
    hilog.info(0x0000, 'testTag', 'SUB_AA_WantAgent_GetWantAgent_0100 getWantAgent successful')

    expect(wantAgentObj !== null && wantAgentObj !== undefined).assertTrue()
    done()
  } catch (err: BusinessError) {
    hilog.info(0x0000, 'testTag', 'SUB_AA_WantAgent_GetWantAgent_0100 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

### 4.3 Context 测试模板

```typescript
it('SUB_AA_Context_GetBundleName_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_AA_Context_GetBundleName_0100-------------')
  try {
    const context = getContext(this) as common.UIAbilityContext
    const bundleName = context.bundleName

    hilog.info(0x0000, 'testTag', 'SUB_AA_Context_GetBundleName_0100 bundleName: ' + bundleName)
    expect(bundleName).assertEqual('com.example.test')

    done()
  } catch (err: BusinessError) {
    hilog.info(0x0000, 'testTag', 'SUB_AA_Context_GetBundleName_0100 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

### 4.4 CommonEvent 测试模板（参考 js-apis-commonEventManager.md）

```typescript
import commonEventManager from '@ohos.commonEventManager'

it('SUB_AA_CommonEvent_Publish_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_AA_CommonEvent_Publish_0100-------------')
  try {
    const eventData = {
      code: 1,
      data: 'test event'
    }

    await commonEventManager.publish('customEvent', eventData)
    hilog.info(0x0000, 'testTag', 'SUB_AA_CommonEvent_Publish_0100 publish event successful')

    expect(true).assertTrue()
    done()
  } catch (err: BusinessError) {
    hilog.info(0x0000, 'testTag', 'SUB_AA_CommonEvent_Publish_0100 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

## 五、测试注意事项

### 5.1 Want 测试注意事项

- Want 对象的字段顺序不影响功能
- parameters 支持序列化和反序列化
- deviceId 为空字符串表示本地设备

### 5.2 WantAgent 测试注意事项

- WantAgent 需要正确的权限配置
- 触发 WantAgent 需要合适的场景
- 取消 WantAgent 需要匹配原有的 requestCode

### 5.3 Context 测试注意事项

- Context 的生命周期与 Ability 绑定
- 不同类型的 Context 功能有差异
- 需要注意 Context 的线程安全

### 5.4 事件测试注意事项（重要）

**生成用例时必须参考 js-apis-commonEventManager.md**：
- 事件名需要符合规范
- 事件数据需要正确序列化
- 订阅和取消订阅需要配对
- 注意事件的权限管理

### 5.5 错误码测试注意事项

- 需要覆盖所有常见错误码
- 验证错误码的准确性
- 测试错误处理逻辑
- 验证错误信息的完整性
