# Ability 子系统通用配置

> **子系统信息**
> - 名称: Ability（能力框架）
> - Kit包: @kit.AbilityKit
> - 测试路径: C:\Users\10418\Desktop\0202\xts_acts1\ability
> - 版本: 1.6.0
> - 更新日期: 2026-02-08

## 一、子系统通用配置

### 1.1 API Kit 映射

```typescript
// Ability Kit 导入
import ability from '@kit.AbilityKit';
import { UIAbility, AbilityStage } from '@kit.AbilityKit';
```

### 1.2 测试路径规范

- 测试用例目录: `C:\Users\10418\Desktop\0202\xts_acts1\ability\`
- 主要测试套:
  - `ability_runtime/` - Ability 运行时测试
  - `ability_base/` - Ability 基础能力测试

### 1.3 模块映射配置

| 模块名称 | 说明 | API 声明前缀 |
|---------|------|------------|
| ability_runtime | Ability 运行时模块 | @ohos.ability.featureAbility, @ohos.app.ability.* |
| ability_base | Ability 基础能力模块 | @ohos.app.ability.*, @ohos.ability.* |

### 1.4 参考资料

**API 参考文档**：
- 主路径：https://gitcode.com/openharmony/docs/tree/master/zh-cn/application-dev/reference/apis-ability-kit
- 文档路径：https://gitcode.com/openharmony/docs/tree/master/zh-cn/application-dev/reference/apis-ability-kit

**开发指南**：
- 开发指南路径：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/application-models/Readme-CN.md

**特殊参考**（生成用例时必须参考）：
- 通用事件参考：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-basic-services-kit/js-apis-commonEventManager.md

## 二、Ability 子系统强制测试规范

> **重要**: 以下规范为 Ability 子系统的强制要求，生成测试用例时必须遵循

### 2.1 接口调用方式覆盖规范（强制）⭐ 最重要

**强制规则**: 新增用例时，**必须根据接口定义考虑 callback 和 promise 两种调用方式**

**重要性**: ⭐⭐⭐⭐⭐ (最高优先级)

#### 2.1.1 核心原则

**第一条规则**: 当为一个 API 生成测试用例时，首先检查该 API 是否支持 Promise 和 AsyncCallback 两种调用方式

**判断方法**:
1. 查看 `.d.ts` 文件中的 API 定义
2. 如果同时包含以下两个签名，则需要生成两个测试用例：
   - 返回 `Promise<T>` 的签名（Promise 方式）
   - 包含 `callback: AsyncCallback<T>` 参数的签名（Callback 方式）

#### 2.1.2 API 定义识别示例

**示例 1: 同时支持两种方式**
```typescript
// .d.ts 文件定义
export function startAbility(want: Want): Promise<void>;
export function startAbility(want: Want, callback: AsyncCallback<void>): void;
```
**结论**: 需要生成 2 个测试用例（Promise 和 Callback 各一个）

**示例 2: 仅支持 Promise**
```typescript
// .d.ts 文件定义
export function getWant(): Promise<Want>;
```
**结论**: 只需要生成 1 个测试用例（Promise 方式）

**示例 3: 仅支持 Callback**
```typescript
// .d.ts 文件定义
export function on(type: string, callback: Callback): void;
```
**结论**: 只需要生成 1 个测试用例（Callback 方式）

#### 2.1.3 测试用例编号规则

**强制规则**: 使用编号后缀区分 Promise 和 Callback 版本

| 调用方式 | 编号后缀 | 示例编号 |
|---------|---------|----------|
| Promise | `00` | `SUB_Ability_StartAbility_0100` |
| AsyncCallback | `50` | `SUB_Ability_StartAbility_0150` |

**编号分配策略**:
```
0100 - Promise 方式测试
0150 - AsyncCallback 方式测试
0200 - 下一个测试场景的 Promise 方式
0250 - 下一个测试场景的 AsyncCallback 方式
```

**为什么使用 50 作为间隔**:
- 保留了 01-49 的编号空间，便于后续插入其他测试场景
- 明确区分 Promise (00) 和 Callback (50) 版本
- 符合 XTS 测试用例编号规范

#### 2.1.4 标准测试用例模板

**Promise 方式模板**:
```typescript
/**
 * @tc.name   SUB_Ability_StartAbility_0100
 * @tc.number SUB_Ability_StartAbility_0100
 * @tc.desc   Test startAbility with valid parameter (Promise)
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_Ability_StartAbility_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_Ability_StartAbility_0100-------------')
  try {
    let data = await ability.startAbility(validWant)
    hilog.info(0x0000, 'testTag', 'SUB_Ability_StartAbility_0100 success')
    expect(data).assertEqual(expectedValue)
    done()
  } catch (err: BusinessError) {
    hilog.info(0x0000, 'testTag', 'SUB_Ability_StartAbility_0100 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

**AsyncCallback 方式模板**:
```typescript
/**
 * @tc.name   SUB_Ability_StartAbility_0150
 * @tc.number SUB_Ability_StartAbility_0150
 * @tc.desc   Test startAbility with valid parameter (AsyncCallback)
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_Ability_StartAbility_0150', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_Ability_StartAbility_0150-------------')
  try {
    ability.startAbility(validWant, (err: BusinessError, data: void) => {
      try {
        if (err.code) {
          hilog.info(0x0000, 'testTag', 'SUB_Ability_StartAbility_0150 error: ' + JSON.stringify(err))
          expect().assertFail()
        } else {
          hilog.info(0x0000, 'testTag', 'SUB_Ability_StartAbility_0150 success')
          // 验证成功
        }
        done()
      } catch (error) {
        hilog.info(0x0000, 'testTag', 'SUB_Ability_StartAbility_0150 callback error: ' + JSON.stringify(error))
        expect().assertFail()
        done()
      }
    })
  } catch (err) {
    hilog.info(0x0000, 'testTag', 'SUB_Ability_StartAbility_0150 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

#### 2.1.5 实现检查清单

在生成测试用例时，必须检查以下项：

- [ ] 已读取 `.d.ts` 文件，确认 API 支持的调用方式
- [ ] 如果支持 Promise，已生成编号后缀为 `00` 的测试用例
- [ ] 如果支持 AsyncCallback，已生成编号后缀为 `50` 的测试用例
- [ ] 两个测试用例的测试逻辑一致
- [ ] 两个测试用例的期望结果一致
- [ ] @tc.desc 中明确标注调用方式（Promise 或 AsyncCallback）

#### 2.1.6 常见错误

**错误 1: 只生成一种方式的测试用例**
```typescript
// ❌ 错误：只生成了 Promise 方式
it('SUB_Ability_StartAbility_0100', Level.LEVEL0, async (done: Function) => {
  let data = await ability.startAbility(validWant)
  // ...
})

// ✅ 正确：应该同时生成 Callback 方式
it('SUB_Ability_StartAbility_0150', Level.LEVEL0, async (done: Function) => {
  ability.startAbility(validWant, (err, data) => {
    // ...
  })
})
```

**错误 2: 编号不符合规范**
```typescript
// ❌ 错误：Callback 方式使用 0101 编号
it('SUB_Ability_StartAbility_0101', Level.LEVEL0, async (done: Function) => {
  ability.startAbility(validWant, (err, data) => {
    // ...
  })
})

// ✅ 正确：Callback 方式应该使用 0150 编号
it('SUB_Ability_StartAbility_0150', Level.LEVEL0, async (done: Function) => {
  ability.startAbility(validWant, (err, data) => {
    // ...
  })
})
```

**错误 3: @tc.desc 未标注调用方式**
```typescript
// ❌ 错误：未标注调用方式
/**
 * @tc.desc   Test startAbility interface
 */

// ✅ 正确：明确标注调用方式
/**
 * @tc.desc   Test startAbility interface (Promise)
 */
// 或
/**
 * @tc.desc   Test startAbility interface (AsyncCallback)
 */
```

### 2.2 测试用例编号规范

**强制规则**: 用例编号每次增加100是必须遵循的规范

```
格式: SUB_Ability_[模块]_[接口所属包名]_[API]_[序号]

说明：
- SUB_Ability_：固定前缀，表示 Ability 子系统
- [模块]：ability_runtime 或 ability_base
- [接口所属包名]：接口所在的包名/模块名，例如 FeatureAbility、AppManager、UIAbility、UIAbilityContext 等
- [API]：接口名称，例如 GetWant、On、StartAbility 等
- [序号]：4位数字，**每次递增100**，例如 0100、0200、0300

示例：
SUB_Ability_AbilityRuntime_FeatureAbility_GetWant_0100
SUB_Ability_AbilityRuntime_FeatureAbility_GetWant_0200
SUB_Ability_AbilityRuntime_FeatureAbility_GetWant_0300
SUB_Ability_AbilityBase_AppManager_On_Null_0100
SUB_Ability_AbilityBase_AppManager_On_Undefined_0200
SUB_Ability_AbilityBase_UIAbilityContext_StartAbility_0100
```

**重要性**: 此规范确保用例编号的唯一性和可扩展性，允许后续在两个用例之间插入新的测试用例（例如在0100和0200之间可插入0110-0190）。

**包名映射表**：

| 模块 | 接口所属包名 | 说明 |
|------|-------------|------|
| ability_runtime | FeatureAbility | @ohos.ability.featureAbility |
| ability_runtime | UIAbility | @ohos.app.ability.UIAbility |
| ability_runtime | UIAbilityContext | @ohos.app.ability.UIAbilityContext |
| ability_runtime | AbilityStage | @ohos.app.ability.AbilityStage |
| ability_base | AppManager | @ohos.app.ability.appManager |
| ability_base | WantAgent | @ohos.app.ability.wantAgent |
| ability_base | ApplicationContext | @ohos.app.ability.AbilityStageContext |

### 2.2 异常断言规范（强制）

**强制规则**: callback或者promise中断言需要使用try-catch{}

**说明**:
- 所有包含异步操作的测试用例，必须使用try-catch包裹
- **不允许同时使用try-catch和Promise.catch**（违反"单一职责"原则）
- 确保异常能被正确捕获和处理

**正确示例 - Promise方式**:
```typescript
it('SUB_Ability_GetBundleName_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_Ability_GetBundleName_0100-------------')
  try {
    expect(typeof (wantAgent)).assertEqual("object");
    let data = await wantAgent.getBundleName(validAgent)
    hilog.info(0x0000, 'testTag', 'SUB_Ability_GetBundleName_0100 success: ' + JSON.stringify(data))
    expect(typeof data).assertEqual('string')
    done()
  } catch (err: BusinessError) {
    hilog.info(0x0000, 'testTag', 'SUB_Ability_GetBundleName_0100 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

**正确示例 - AsyncCallback方式**:
```typescript
it('SUB_Ability_GetBundleName_0200', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', '------------start SUB_Ability_GetBundleName_0200-------------')
  try {
    expect(typeof (wantAgent)).assertEqual("object");
    wantAgent.getBundleName(validAgent, (err: BusinessError, data: string) => {
      try {
        if (err.code) {
          hilog.info(0x0000, 'testTag', 'SUB_Ability_GetBundleName_0200 error: ' + JSON.stringify(err))
          expect().assertFail()
        } else {
          hilog.info(0x0000, 'testTag', 'SUB_Ability_GetBundleName_0200 success: ' + JSON.stringify(data))
          expect(typeof data).assertEqual('string')
        }
        done()
      } catch (error) {
        hilog.info(0x0000, 'testTag', 'SUB_Ability_GetBundleName_0200 callback error: ' + JSON.stringify(error))
        expect().assertFail()
        done()
      }
    })
  } catch (err) {
    hilog.info(0x0000, 'testTag', 'SUB_Ability_GetBundleName_0200 error: ' + JSON.stringify(err))
    expect().assertFail()
    done()
  }
})
```

**错误示例 - 违反单一职责原则**:
```typescript
// ❌ 错误：同时使用了try-catch和Promise.catch
it('SUB_Ability_GetBundleName_0100', Level.LEVEL0, async (done: Function) => {
  try {
    expect(typeof (wantAgent)).assertEqual("object");
    wantAgent.getBundleName(validAgent)
      .then((data) => {
        expect(typeof data).assertEqual('string')
        done()
      })
      .catch((err: BusinessError) => {  // ❌ 错误：与外层try-catch重复
        hilog.info(0x0000, 'testTag', 'error: ' + JSON.stringify(err))
        expect().assertFail()
        done()
      });
  } catch (err) {
    expect().assertFail()
    done()
  }
})
```

### 2.3 接口测试覆盖规范（强制）

**强制规则**: 接口补充用例时，需要考虑callback和promise两种调用方式

**说明**:
- 如果API同时支持Promise和AsyncCallback两种调用方式，必须分别为两种方式生成测试用例
- 确保两种调用方式的功能一致性
- 测试用例编号应明确区分Promise和Callback版本

**实现策略**:
```
1. 解析.d.ts文件，识别API是否支持两种调用方式
2. 为Promise方式生成测试用例（编号后缀00）
3. 为AsyncCallback方式生成测试用例（编号后缀50）
4. 确保两种方式的测试逻辑和期望结果一致
```

**示例**:
```typescript
// Promise方式测试
it('SUB_Ability_GetBundleName_0100', Level.LEVEL0, async (done: Function) => {
  try {
    let data = await wantAgent.getBundleName(validAgent)
    expect(typeof data).assertEqual('string')
    done()
  } catch (err: BusinessError) {
    expect().assertFail()
    done()
  }
})

// AsyncCallback方式测试
it('SUB_Ability_GetBundleName_0150', Level.LEVEL0, async (done: Function) => {
  try {
    wantAgent.getBundleName(validAgent, (err: BusinessError, data: string) => {
      try {
        if (err.code) {
          expect().assertFail()
        } else {
          expect(typeof data).assertEqual('string')
        }
        done()
      } catch (error) {
        expect().assertFail()
        done()
      }
    })
  } catch (err) {
    expect().assertFail()
    done()
  }
})
```

### 2.4 错误码断言规范（强制）⭐ NEW

**强制规则**: 错误码断言必须使用 `assertEqual(-1)`，禁止使用 `code !== undefined`

**说明**:
- 当捕获到错误时，必须明确断言错误码的具体值（通常为 -1）
- **禁止**使用 `expect(err.code !== undefined).assertTrue()` 这种模糊判断
- 此规范确保测试用例精确验证错误码，提高测试可靠性

**正确示例**:
```typescript
// ✅ 正确：明确断言错误码等于 -1
it('SUB_Ability_GetBundleName_0200', Level.LEVEL0, async (done: Function) => {
  try {
    await wantAgent.getBundleName("")
    expect().assertFail()
    done()
  } catch (err: BusinessError) {
    expect(err.code).assertEqual(-1)  // ✅ 正确
    done()
  }
})
```

**错误示例**:
```typescript
// ❌ 错误：使用模糊的 !== undefined 判断
it('SUB_Ability_GetBundleName_0200', Level.LEVEL0, async (done: Function) => {
  try {
    await wantAgent.getBundleName("")
    expect().assertFail()
    done()
  } catch (err: BusinessError) {
    expect(err.code !== undefined).assertTrue()  // ❌ 错误：不规范
    done()
  }
})
```

**对比说明**:

| 断言方式 | 规范性 | 问题 |
|---------|--------|------|
| `expect(err.code !== undefined).assertTrue()` | ❌ 不规范 | 仅验证错误码存在，未验证具体值 |
| `expect(err.code).assertEqual(-1)` | ✅ 规范 | 明确验证错误码等于 -1 |
| `expect(err.code).assertEqual(401)` | ✅ 规范 | 明确验证错误码等于 401 |

**应用场景**:
- 参数异常测试：错误码通常为 `401`（参数错误）
- 权限异常测试：错误码通常为 `201`（权限拒绝）
- 通用异常测试：错误码通常为 `-1`（通用错误）
- 根据实际 API 的 `@throws` 标签确定具体错误码

### 2.5 参数异常测试规范（强制）

**强制规则**: 补充参数异常用例时，不考虑callback是null/undefined

**说明**:
- 当生成参数错误测试用例时，不需要测试callback参数为null或undefined的情况
- callback为null/undefined通常会导致同步抛出异常，而不是401参数错误
- 重点关注业务参数的边界测试：""、undefined、null、空数组

**不需要测试的参数**:
- callback: AsyncCallback<T> - 不测试null/undefined
- 可选的callback参数（如trigger的callback）- 不测试null/undefined

**需要测试的参数**:
- 所有业务参数：uri、bundleName、methodName、valuesBucket等
- 测试值：""、undefined、null、空数组[]

**示例 - 需要测试的参数**:
```typescript
// ✅ 正确：测试业务参数为空字符串
it('SUB_Ability_GetBundleName_0200', Level.LEVEL0, async (done: Function) => {
  try {
    await wantAgent.getBundleName("")  // 测试agent为""
    expect().assertFail()
    done()
  } catch (err: BusinessError) {
    expect(err.code).assertEqual(-1)  // ✅ 使用 assertEqual
    done()
  }
})

// ✅ 正确：测试业务参数为undefined
it('SUB_Ability_GetBundleName_0300', Level.LEVEL0, async (done: Function) => {
  try {
    await wantAgent.getBundleName(undefined)  // 测试agent为undefined
    expect().assertFail()
    done()
  } catch (err: BusinessError) {
    expect(err.code).assertEqual(-1)  // ✅ 使用 assertEqual
    done()
  }
})

// ✅ 正确：测试业务参数为null
it('SUB_Ability_GetBundleName_0400', Level.LEVEL0, async (done: Function) => {
  try {
    await wantAgent.getBundleName(null)  // 测试agent为null
    expect().assertFail()
    done()
  } catch (err: BusinessError) {
    expect(err.code).assertEqual(-1)  // ✅ 使用 assertEqual
    done()
  }
})

// ❌ 错误：不需要测试callback为null
// it('SUB_Ability_GetBundleName_0500', Level.LEVEL0, async (done: Function) => {
//   wantAgent.getBundleName(validAgent, null);  // 不需要测试
// })
```

### 2.5 Ability 相关测试规则

1. **FA 模型（Feature Ability）测试**
   - 使用 `@ohos.ability.featureAbility` 模块
   - 主要 API：getWant(), startAbility(), terminateSelf() 等
   - 测试时需要模拟 FA 模型环境

2. **Stage 模型测试**
   - 使用 `@kit.AbilityKit` 模块
   - 主要类：UIAbility, AbilityStage, UIAbilityContext
   - 测试时需要验证生命周期回调

3. **Context 测试规则**
   - AbilityContext: 验证上下文相关接口
   - 需要注意同步和异步 API 的测试方式
   - 回调函数和 Promise 两种方式都要测试

### 2.3 事件相关测试规则

**重要**：生成用例时必须参考 `js-apis-commonEventManager.md`

- CommonEventManager: 通用事件管理
- CommonEvent: 通用事件数据
- 测试事件发布和订阅功能
- 验证事件参数传递

## 三、已知问题和注意事项

### 3.1 FA 模型与 Stage 模型差异

- FA 模型和 Stage 模型的 API 不同
- 需要根据模型类型选择对应的测试方法
- 测试套要明确区分两种模型

### 3.2 生命周期测试注意事项

- UIAbility 生命周期：onCreate(), onDestroy(), onForeground(), onBackground()
- AbilityStage 生命周期：onCreate(), onAcceptWant(), onForeground()
- 测试时需要验证回调顺序和参数

### 3.3 权限要求

某些 Ability API 需要特定权限，测试时需要：
- 在 config.json 中声明权限
- 使用 grantPermission 工具授予权限
- 验证权限相关错误码

## 四、通用代码模板

### 4.1 FA 模型 API 测试模板

```typescript
import { describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, Level } from '@ohos/hypium'
import featureAbility from '@ohos.ability.featureAbility'
import { BusinessError } from '@ohos.base'
import hilog from '@ohos.hilog'

export default function FeatureAbilityTest() {
  describe('FeatureAbilityTest', () => {

    it('SUB_AA_FeatureAbility_GetWant_0100', Level.LEVEL0, async (done: Function) => {
      hilog.info(0x0000, 'testTag', '------------start SUB_AA_FeatureAbility_GetWant_0100-------------')
      try {
        const want = await featureAbility.getWant()
        hilog.info(0x0000, 'testTag', 'SUB_AA_FeatureAbility_GetWant_0100 getWant successful')
        expect(want?.bundleName).assertEqual('com.example.test')
        done()
      } catch (err: BusinessError) {
        hilog.info(0x0000, 'testTag', 'SUB_AA_FeatureAbility_GetWant_0100 error: ' + JSON.stringify(err))
        expect().assertFail()
        done()
      }
    })

  })
}
```

### 4.2 Stage 模型 UIAbility 测试模板

```typescript
import { UIAbility } from '@kit.AbilityKit'
import { BusinessError } from '@ohos.base'
import window from '@ohos.window'

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, 'testTag', 'EntryAbility onCreate')
  }

  onDestroy(): void {
    hilog.info(0x0000, 'testTag', 'EntryAbility onDestroy')
  }

  onForeground(): void {
    hilog.info(0x0000, 'testTag', 'EntryAbility onForeground')
  }

  onBackground(): void {
    hilog.info(0x0000, 'testTag', 'EntryAbility onBackground')
  }
}
```

### 4.3 错误处理模板

```typescript
try {
  await featureAbility.startAbility({ want: {} })
  expect().assertFail()
  done()
} catch (err: BusinessError) {
  hilog.info(0x0000, 'testTag', 'Expected error: ' + JSON.stringify(err))
  expect(err.code).assertEqual(-1)  // ✅ 使用 assertEqual 明确断言错误码
  done()
}
```

## 五、UIExtension跨组件调用测试

> **重要**: UIExtension相关接口的跨进程测试必须遵循此规范

### 5.1 适用场景

- ✅ UIExtension相关接口的跨进程测试
- ✅ 需要在独立进程中测试接口行为
- ✅ 需要通过事件机制验证接口调用结果

**详细规范**: 请查看 [`uiextension_cross_component.md`](./uiextension_cross_component.md)

该文档包含：
- 完整的调用链路说明
- 四步实现流程详解
- 参数传递链路图
- 支持的测试场景列表
- 关键注意事项和常见问题

## 六、FA模型 ServiceAbility 测试规范

> **重要**: FA 模型 ServiceAbility 相关接口的测试必须遵循此规范

### 6.1 适用场景

- ✅ ServiceAbility 启动测试（startAbility）
- ✅ ServiceAbility 连接测试（connectAbility/disconnectAbility）
- ✅ ServiceAbility 生命周期测试（onStart/onStop/onCommand/onConnect/onDisconnect）
- ✅ 跨进程接口测试
- ✅ 需要通过事件机制验证接口调用结果

### 6.2 测试模式概述

FA 模型 ServiceAbility 测试采用**事件驱动模式**：

1. **测试用例层**：使用 `featureAbility.startAbility()` 启动 ServiceAbility 或 `connectAbility()` 连接
2. **want.action 标识**：通过 `want.action` 字段传递测试用例标识（可选）
3. **ServiceAbility 层**：在生命周期回调（`onCommand`/`onConnect`/`onDisconnect`）中执行测试
4. **事件发送**：使用 `commonEvent.publish()` 将生命周期事件发送给测试用例
5. **结果验证**：测试用例订阅事件，接收并验证结果

### 6.3 生命周期事件流测试规范

**参考范本**: `/test/xts/acts/ability/ability_runtime/faapicover/faapicoverhaptest/entry/src/ohosTest/ets/test/VerificationTest.ets`
- **用例编号**: `SUB_AA_OpenHarmony_Test_ServiceAbility_0200` (行369-450)
- **测试场景**: ServiceAbility 连接/断开生命周期测试

#### 6.3.1 Connect/Disconnect 生命周期事件流

```javascript
/**
 * 测试流程：
 * 1. 订阅 ServiceAbility 的生命周期事件（onConnect, onDisconnect）
 * 2. 调用 featureAbility.connectAbility() 连接 Service
 * 3. ServiceAbility.onConnect() 触发，发送事件到测试用例
 * 4. 测试用例收到 onConnect 事件，调用 disconnectAbility()
 * 5. ServiceAbility.onDisconnect() 触发，发送事件到测试用例
 * 6. 测试用例收到 onDisconnect 事件，验证生命周期完成
 */
```

#### 6.3.2 标准连接测试用例模板

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
  TAG = 'SUB_AA_OpenHarmony_Test_ServiceAbility_0200 ==>';

  try {
    // 生命周期事件追踪列表
    let lifecycleList: string[] = []
    let lifecycleListCheck = ["onConnect", "onDisconnect"]

    // 连接状态标志
    let flagOnConnect = false
    let flagOnDisconnect = false
    let flagOnFailed = false

    let subscriber: commonEvent.CommonEventSubscriber | undefined = undefined;
    let subscribeInfo: commonEvent.CommonEventSubscribeInfo = {
      events: [
        "Fa_Auxiliary_ServiceAbility2_onConnect",
        "Fa_Auxiliary_ServiceAbility2_onDisconnect"
      ]
    }

    // 事件订阅回调
    let SubscribeInfoCallback = async (err: BusinessError, data: commonEvent.CommonEventData) => {
      console.info(TAG + "===SubscribeInfoCallback===" + JSON.stringify(data))

      // 收到 onConnect 事件
      if (data.event == "Fa_Auxiliary_ServiceAbility2_onConnect") {
        lifecycleList.push("onConnect")

        // 步骤：触发断开连接
        await ability_featureAbility.disconnectAbility(connectionId).then((data) => {
          console.info(TAG + "disconnectAbility data = " + JSON.stringify(data));
        }).catch((err: BusinessError) => {
          console.info(TAG + "disconnectAbility err = " + JSON.stringify(err));
          expect().assertFail();
          done();
        });
      }

      // 收到 onDisconnect 事件
      if (data.event == "Fa_Auxiliary_ServiceAbility2_onDisconnect") {
        lifecycleList.push("onDisconnect")

        setTimeout(() => {
          // 验证生命周期事件顺序
          expect(JSON.stringify(lifecycleList)).assertEqual(JSON.stringify(lifecycleListCheck));

          // 验证连接状态
          expect(flagOnConnect).assertTrue();      // onConnect 被调用
          expect(flagOnDisconnect).assertTrue();   // onDisconnect 被调用
          expect(flagOnFailed).assertFalse();      // onFailed 未被调用

          commonEvent.unsubscribe(subscriber, UnSubscribeInfoCallback);
        }, 1000)
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

    // 步骤：连接 ServiceAbility
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

#### 6.3.3 ServiceAbility 生命周期事件发送规范

```javascript
// ServiceAbility2/service.js
import commonEvent from '@ohos.commonEvent'

export default {
  onConnect(want) {
    console.info('ServiceAbility onConnect: ' + JSON.stringify(want));

    // 发送 onConnect 事件到测试用例
    commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onConnect', (err) => {
      console.info('Fa_Auxiliary_ServiceAbility2_onConnect publish: ' + JSON.stringify(err));
    });

    // 返回 RemoteObject
    return new RemoteObject('test');
  },

  onDisconnect(elementName) {
    console.info('ServiceAbility onDisconnect: ' + JSON.stringify(elementName));

    // 发送 onDisconnect 事件到测试用例
    commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onDisconnect', (err) => {
      console.info('Fa_Auxiliary_ServiceAbility2_onDisconnect publish: ' + JSON.stringify(err));
    });
  },

  onCommand(want, restart, startId) {
    console.info('ServiceAbility onCommand: ' + JSON.stringify(want));

    // 发送 onCommand 事件到测试用例
    commonEvent.publish('Fa_Auxiliary_ServiceAbility_onCommand', (err) => {
      console.info('Fa_Auxiliary_ServiceAbility_onCommand publish: ' + JSON.stringify(err));
    });
  }
}
```

### 6.4 命名规范

#### 6.4.1 事件名称规范

**测试事件名称格式**: `[测试模块]_[组件名]_[生命周期]`

**示例**:
- `Fa_Auxiliary_ServiceAbility_onCommand`
- `Fa_Auxiliary_ServiceAbility2_onConnect`
- `Fa_Auxiliary_ServiceAbility2_onDisconnect`
- `Fa_Auxiliary_MainAbility_onCreate`
- `Fa_Auxiliary_MainAbility_onDestroy`

**命名要素**:
- **测试模块**: `Fa_Auxiliary_` - FA 模型辅助测试模块标识
- **组件名**: `ServiceAbility`, `ServiceAbility2`, `MainAbility` 等
- **生命周期**: `onStart`, `onStop`, `onCommand`, `onConnect`, `onDisconnect`, `onCreate`, `onDestroy`

#### 6.4.2 action 标识规范（可选）

**action 格式**: `[调用方][接口]_[用例编号]`

**示例**:
- `PageStartService_0100` - Page调用startAbility接口
- `ServiceStartService_0900` - Service调用startAbility接口
- `PageConnectService_0500` - Page调用connectAbility接口

> **注**: action 标识主要用于在 onCommand 回调中区分不同的测试用例，对于 connectAbility 测试通常不需要。

### 6.5 StartAbility 生命周期测试规范

**参考范本**: `/test/xts/acts/ability/ability_runtime/faapicover/faapicoverhaptest/entry/src/ohosTest/ets/test/VerificationTest.ets`
- **用例编号**: `SUB_AA_OpenHarmony_Test_ServiceAbility_0100` (行318-367)

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
  TAG = 'SUB_AA_OpenHarmony_Test_ServiceAbility_0100 ==>';

  try {
    let subscriber: commonEvent.CommonEventSubscriber | undefined = undefined;
    let subscribeInfo: commonEvent.CommonEventSubscribeInfo = {
      events: ["Fa_Auxiliary_ServiceAbility_onCommand"]
    }

    let SubscribeInfoCallback = (err: BusinessError, data: commonEvent.CommonEventData) => {
      console.info(TAG + "===SubscribeInfoCallback===" + JSON.stringify(data))

      if (data.event == "Fa_Auxiliary_ServiceAbility_onCommand") {
        // 收到 onCommand 事件，验证生命周期回调被调用
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

### 6.6 测试用例实现要点

#### 6.6.1 生命周期事件追踪

使用列表追踪生命周期事件顺序：

```typescript
// 定义预期的事件顺序
let lifecycleList: string[] = []
let lifecycleListCheck = ["onConnect", "onDisconnect"]

// 在事件回调中记录
if (data.event == "Fa_Auxiliary_ServiceAbility2_onConnect") {
  lifecycleList.push("onConnect")
}
if (data.event == "Fa_Auxiliary_ServiceAbility2_onDisconnect") {
  lifecycleList.push("onDisconnect")
}

// 最终验证顺序
expect(JSON.stringify(lifecycleList)).assertEqual(JSON.stringify(lifecycleListCheck));
```

#### 6.6.2 连接状态验证

使用标志位验证回调状态：

```typescript
let flagOnConnect = false      // onConnect 是否被调用
let flagOnDisconnect = false   // onDisconnect 是否被调用
let flagOnFailed = false       // onFailed 是否被调用

// 在回调中设置标志
onConnect: (elementName, proxy) => {
  flagOnConnect = true
  // ...
}

// 最终验证
expect(flagOnConnect).assertTrue();
expect(flagOnDisconnect).assertTrue();
expect(flagOnFailed).assertFalse();  // 失败回调不应被调用
```

#### 6.6.3 事件订阅和取消订阅

```typescript
// 1. 创建订阅者
commonEvent.createSubscriber(subscribeInfo, (err, data) => {
  subscriber = data

  // 2. 订阅事件
  commonEvent.subscribe(subscriber, SubscribeInfoCallback)
})

// 3. 在测试完成后取消订阅
commonEvent.unsubscribe(subscriber, UnSubscribeInfoCallback);
```

#### 6.6.4 延迟验证

由于事件发送是异步的，需要使用 setTimeout 延迟验证：

```typescript
setTimeout(() => {
  expect(JSON.stringify(lifecycleList)).assertEqual(JSON.stringify(lifecycleListCheck));
  expect(flagOnConnect).assertTrue();
  expect(flagOnDisconnect).assertTrue();
  commonEvent.unsubscribe(subscriber, UnSubscribeInfoCallback);
  done();
}, 1000)  // 延迟 1 秒
```

### 6.7 ServiceAbility 实现规范

```javascript
// ServiceAbility.js
import commonEvent from '@ohos.commonEvent'

export default {
  onStart(want) {
    console.info('ServiceAbility onStart: ' + JSON.stringify(want));
    commonEvent.publish('Fa_Auxiliary_ServiceAbility_onStart', (err) => {
      console.info('Fa_Auxiliary_ServiceAbility_onStart published');
    });
  },

  onStop() {
    console.info('ServiceAbility onStop');
    commonEvent.publish('Fa_Auxiliary_ServiceAbility_onStop', (err) => {
      console.info('Fa_Auxiliary_ServiceAbility_onStop published');
    });
  },

  onCommand(want, restart, startId) {
    console.info('ServiceAbility onCommand: ' + JSON.stringify(want));

    // 发布 onCommand 事件
    commonEvent.publish('Fa_Auxiliary_ServiceAbility_onCommand', {
      parameters: {
        want: want,
        restart: restart,
        startId: startId
      }
    }, (err) => {
      if (!err.code) {
        console.info('Fa_Auxiliary_ServiceAbility_onCommand published successfully');
      }
    });
  },

  onConnect(want) {
    console.info('ServiceAbility onConnect: ' + JSON.stringify(want));

    // 发布 onConnect 事件
    commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onConnect', (err) => {
      if (!err.code) {
        console.info('Fa_Auxiliary_ServiceAbility2_onConnect published successfully');
      }
    });

    // 返回 RemoteObject
    return new RemoteObject('test');
  },

  onDisconnect(elementName) {
    console.info('ServiceAbility onDisconnect: ' + JSON.stringify(elementName));

    // 发布 onDisconnect 事件
    commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onDisconnect', (err) => {
      if (!err.code) {
        console.info('Fa_Auxiliary_ServiceAbility2_onDisconnect published successfully');
      }
    });
  }
}
```

### 6.8 最佳实践

#### 6.8.1 事件命名一致性

确保测试用例中订阅的事件名与 ServiceAbility 中发布的事件名完全一致：

```typescript
// 测试用例中
events: ["Fa_Auxiliary_ServiceAbility2_onConnect", "Fa_Auxiliary_ServiceAbility2_onDisconnect"]

// ServiceAbility 中
commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onConnect', ...)
commonEvent.publish('Fa_Auxiliary_ServiceAbility2_onDisconnect', ...)
```

#### 6.8.2 错误处理

```typescript
// 在事件回调中处理错误
let SubscribeInfoCallback = async (err: BusinessError, data: commonEvent.CommonEventData) => {
  if (err.code) {
    console.info(TAG + "SubscribeInfoCallback error: " + JSON.stringify(err));
    expect().assertFail();
    done();
    return;
  }
  // 正常处理逻辑...
}
```

#### 6.8.3 日志输出

```typescript
// 使用 TAG 标识当前用例
let TAG = 'SUB_AA_OpenHarmony_Test_ServiceAbility_0200 ==>';

console.info(TAG + "===SubscribeInfoCallback===" + JSON.stringify(data));
```

**详细规范**: 请查看 [`fa_serviceability_testing.md`](./fa_serviceability_testing.md)

该文档包含：
- 完整的架构图和流程说明
- 多步骤测试用例实现方法
- 使用 action 标识的高级测试场景
- 最佳实践和常见问题解决方案

## 七、通用生命周期测试规范

> **重要**: 所有 Ability 组件的生命周期测试必须遵循此规范

### 7.1 生命周期测试核心流程

**测试流程**：

```
步骤1: 确定要测试的组件
   ↓
步骤2: 梳理组件的生命周期回调
   ↓
步骤3: 根据要测试的生命周期选择对应的启动接口
   ↓
步骤4: 在测试用例中使用接口启动组件
   ↓
步骤5: 组件生命周期回调后，发送事件到测试用例
   ↓
步骤6: 在测试用例中统一判断生命周期回调是否正确
```

### 7.2 常见 Ability 组件及其生命周期

#### 7.2.1 ServiceExtensionAbility (ServiceExtension/AppServiceExtension)

**生命周期回调**:
- `onCreate(want: Want)` - 服务创建时调用
- `onRequest(want: Want, startId: number)` - 服务请求时调用
- `onConnect(want: Want): RemoteObject` - 连接时调用
- `onDisconnect(want: Want)` - 断开连接时调用
- `onDestroy()` - 服务销毁时调用

**对应的测试接口**:
| 生命周期 | 测试接口 | 说明 |
|---------|---------|------|
| onCreate | `startAppServiceExtensionAbility(want)` | 启动服务后触发 onCreate |
| onRequest | `startAppServiceExtensionAbility(want)` | 启动服务后触发 onRequest |
| onConnect | `connectAppServiceExtensionAbility(want, options)` | 连接服务时触发 onConnect |
| onDisconnect | `disconnectAppServiceExtensionAbility(connId)` | 断开连接时触发 onDisconnect |
| onDestroy | `AppServiceExtensionContext.terminateSelf()` 或 `stopAppServiceExtensionAbility(want)` | 销毁服务时触发 onDestroy |

#### 7.2.2 UIAbility

**生命周期回调**:
- `onCreate(want: Want, launchParam: AbilityConstant.LaunchParam)` - Ability 创建时调用
- `onForeground()` - Ability 切换到前台时调用
- `onBackground()` - Ability 切换到后台时调用
- `onDestroy()` - Ability 销毁时调用
- `onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam)` - Ability 重新启动时调用
- `onContinue(wantParam: Want)` - Ability 迁移时调用
- `onConfigurationUpdate(newConfig: Configuration)` - 配置更新时调用

**对应的测试接口**:
| 生命周期 | 测试接口 | 说明 |
|---------|---------|------|
| onCreate | `startAbility()` | 首次启动时触发 |
| onForeground | `startAbility()` / `onBackground()` 后切换回前台 | 切换到前台时触发 |
| onBackground | `moveAbilityToBackground()` | 切换到后台时触发 |
| onDestroy | `terminateSelf()` | 自我销毁时触发 |
| onNewWant | `startAbility()` (已存在实例) | 热启动时触发 |

#### 7.2.3 UIExtensionAbility

**生命周期回调**:
- `onCreate(want: Want, launchType: string)` - 创建时调用
- `onForeground()` - 切换到前台时调用
- `onBackground()` - 切换到后台时调用
- `onDestroy()` - 销毁时调用
- `onReady()` - 准备完成时调用

#### 7.2.4 DataAbility (数据扩展)

**生命周期回调**:
- `onCreate(want: Want)` - 创建时调用
- `insert(uri: string, valueBucket: rdb.ValuesBucket)` - 插入数据
- `query(uri: string, columns: Array<string>, predicates: dataSharePredicates.DataSharePredicates)` - 查询数据
- `update(uri: string, valueBucket: rdb.ValuesBucket, predicates: dataSharePredicates.DataSharePredicates)` - 更新数据
- `delete(uri: string, predicates: dataSharePredicates.DataSharePredicates)` - 删除数据
- `onDestroy()` - 销毁时调用

### 7.3 生命周期测试用例模板

#### 7.3.1 onCreate 生命周期测试模板

**测试思路**: 调用 start 接口启动组件，在组件的 onCreate 回调中发送事件，测试用例验证事件

```typescript
/**
 * @tc.name   SUB_AA_ServiceExtension_onCreate_0100
 * @tc.number SUB_AA_ServiceExtension_onCreate_0100
 * @tc.desc   Test ServiceExtension onCreate lifecycle
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_AA_ServiceExtension_onCreate_0100', Level.LEVEL0, async (done: Function) => {
  const tcNumber = 'SUB_AA_ServiceExtension_onCreate_0100';
  hilog.info(0x0000, 'testTag', `${tcNumber} Begin`);

  let subscriber: commonEventManager.CommonEventSubscriber | undefined = undefined;

  // 订阅 onCreate 事件
  let subscribeInfo: commonEventManager.CommonEventSubscribeInfo = {
    events: ['ServiceExtension_onCreate']
  };

  await commonEventManager.createSubscriber(subscribeInfo).then((data) => {
    subscriber = data;

    commonEventManager.subscribe(subscriber, (err, commonEventData) => {
      hilog.info(0x0000, 'testTag', `${tcNumber} subscribe callback: ${JSON.stringify(commonEventData)}`);

      // 验证 onCreate 事件被触发
      expect(commonEventData.event).assertEqual('ServiceExtension_onCreate');
      expect(commonEventData.parameters?.lifecycle).assertEqual('onCreate');

      commonEventManager.unsubscribe(subscriber);
      done();
    });
  });

  // 调用 startAppServiceExtensionAbility 启动服务，触发 onCreate
  try {
    await context.startAppServiceExtensionAbility({
      bundleName: 'com.example.test',
      abilityName: 'ServiceExtAbility',
      parameters: {
        'case': 'onCreate_0100'  // 可选：传递测试用例标识
      }
    }).then(() => {
      hilog.info(0x0000, 'testTag', `${tcNumber} startAppServiceExtensionAbility succeed`);
    }).catch((err: BusinessError) => {
      hilog.info(0x0000, 'testTag', `${tcNumber} startAppServiceExtensionAbility error: ${JSON.stringify(err)}`);
      expect().assertFail();
      done();
    });
  } catch (err) {
    hilog.info(0x0000, 'testTag', `${tcNumber} error: ${JSON.stringify(err)}`);
    expect().assertFail();
    done();
  }
})
```

**ServiceExtAbility 实现端**:
```typescript
import { ServiceExtensionAbility, Want } from '@kit.AbilityKit';
import { commonEventManager } from '@kit.BasicServicesKit';
import { hilog } from '@kit.PerformanceAnalysisKit';

const TAG: string = 'testTag';

export default class ServiceExtAbility extends ServiceExtensionAbility {
  onCreate(want: Want): void {
    hilog.info(0x0000, TAG, `ServiceExtAbility onCreate, want: ${JSON.stringify(want)}`);

    // 发送 onCreate 事件到测试用例
    commonEventManager.publish('ServiceExtension_onCreate', {
      parameters: {
        lifecycle: 'onCreate',
        want: want
      }
    }).then(() => {
      hilog.info(0x0000, TAG, 'ServiceExtension_onCreate event published');
    });
  }

  // 其他生命周期...
  onRequest(want: Want, startId: number): void {}
  onConnect(want: Want): rpc.RemoteObject { return null; }
  onDisconnect(want: Want): void {}
  onDestroy(): void {}
}
```

#### 7.3.2 onConnect/onDisconnect 生命周期测试模板

**测试思路**: 调用 connect 接口连接组件，验证 onConnect，然后调用 disconnect 验证 onDisconnect

```typescript
/**
 * @tc.name   SUB_AA_ServiceExtension_onConnect_0100
 * @tc.number SUB_AA_ServiceExtension_onConnect_0100
 * @tc.desc   Test ServiceExtension onConnect and onDisconnect lifecycle
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_AA_ServiceExtension_onConnect_0100', Level.LEVEL0, async (done: Function) => {
  const tcNumber = 'SUB_AA_ServiceExtension_onConnect_0100';
  hilog.info(0x0000, 'testTag', `${tcNumber} Begin`);

  let lifecycleList: string[] = [];
  let lifecycleCheck = ['onConnect', 'onDisconnect'];

  let subscriber: commonEventManager.CommonEventSubscriber | undefined = undefined;

  // 订阅 onConnect 和 onDisconnect 事件
  let subscribeInfo: commonEventManager.CommonEventSubscribeInfo = {
    events: ['ServiceExtension_onConnect', 'ServiceExtension_onDisconnect']
  };

  await commonEventManager.createSubscriber(subscribeInfo).then((data) => {
    subscriber = data;

    commonEventManager.subscribe(subscriber, (err, commonEventData) => {
      hilog.info(0x0000, 'testTag', `${tcNumber} subscribe callback: ${JSON.stringify(commonEventData)}`);

      if (commonEventData.event === 'ServiceExtension_onConnect') {
        lifecycleList.push('onConnect');

        // 收到 onConnect 事件后，调用 disconnect 触发 onDisconnect
        context.disconnectAppServiceExtensionAbility(connectionId).then(() => {
          hilog.info(0x0000, 'testTag', `${tcNumber} disconnectAppServiceExtensionAbility succeed`);
        }).catch((err: BusinessError) => {
          hilog.info(0x0000, 'testTag', `${tcNumber} disconnectAppServiceExtensionAbility error: ${JSON.stringify(err)}`);
          expect().assertFail();
          done();
        });
      }

      if (commonEventData.event === 'ServiceExtension_onDisconnect') {
        lifecycleList.push('onDisconnect');

        // 验证生命周期顺序
        expect(JSON.stringify(lifecycleList)).assertEqual(JSON.stringify(lifecycleCheck));

        commonEventManager.unsubscribe(subscriber);
        done();
      }
    });
  });

  // 调用 connectAppServiceExtensionAbility 连接服务，触发 onConnect
  let connectionId: number;
  try {
    connectionId = context.connectAppServiceExtensionAbility(
      {
        bundleName: 'com.example.test',
        abilityName: 'ServiceExtAbility'
      },
      {
        onConnect(elementName, remote) {
          hilog.info(0x0000, 'testTag', `${tcNumber} onConnect elementName: ${JSON.stringify(elementName)}`);
        },
        onDisconnect(elementName) {
          hilog.info(0x0000, 'testTag', `${tcNumber} onDisconnect elementName: ${JSON.stringify(elementName)}`);
        },
        onFailed(code) {
          hilog.info(0x0000, 'testTag', `${tcNumber} onFailed code: ${code}`);
          expect().assertFail();
          done();
        }
      }
    );
  } catch (err) {
    hilog.info(0x0000, 'testTag', `${tcNumber} error: ${JSON.stringify(err)}`);
    expect().assertFail();
    done();
  }
})
```

**ServiceExtAbility 实现端**:
```typescript
onConnect(want: Want): rpc.RemoteObject {
  hilog.info(0x0000, TAG, `ServiceExtAbility onConnect, want: ${JSON.stringify(want)}`);

  // 发送 onConnect 事件到测试用例
  commonEventManager.publish('ServiceExtension_onConnect', {
    parameters: {
      lifecycle: 'onConnect',
      want: want
    }
  }).then(() => {
    hilog.info(0x0000, TAG, 'ServiceExtension_onConnect event published');
  });

  return new StubTest('test');
}

onDisconnect(want: Want): void {
  hilog.info(0x0000, TAG, `ServiceExtAbility onDisconnect, want: ${JSON.stringify(want)}`);

  // 发送 onDisconnect 事件到测试用例
  commonEventManager.publish('ServiceExtension_onDisconnect', {
    parameters: {
      lifecycle: 'onDisconnect',
      want: want
    }
  }).then(() => {
    hilog.info(0x0000, TAG, 'ServiceExtension_onDisconnect event published');
  });
}
```

#### 7.3.3 onDestroy 生命周期测试模板

**测试思路**: 启动组件后，调用 terminateSelf 或 stop 接口，触发 onDestroy

```typescript
/**
 * @tc.name   SUB_AA_ServiceExtension_onDestroy_0100
 * @tc.number SUB_AA_ServiceExtension_onDestroy_0100
 * @tc.desc   Test ServiceExtension onDestroy lifecycle
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL0
 */
it('SUB_AA_ServiceExtension_onDestroy_0100', Level.LEVEL0, async (done: Function) => {
  const tcNumber = 'SUB_AA_ServiceExtension_onDestroy_0100';
  hilog.info(0x0000, 'testTag', `${tcNumber} Begin`);

  let subscriber: commonEventManager.CommonEventSubscriber | undefined = undefined;

  // 订阅 onCreate 和 onDestroy 事件
  let subscribeInfo: commonEventManager.CommonEventSubscribeInfo = {
    events: ['ServiceExtension_onCreate', 'ServiceExtension_onDestroy']
  };

  await commonEventManager.createSubscriber(subscribeInfo).then((data) => {
    subscriber = data;

    let lifecycleList: string[] = [];

    commonEventManager.subscribe(subscriber, (err, commonEventData) => {
      hilog.info(0x0000, 'testTag', `${tcNumber} subscribe callback: ${JSON.stringify(commonEventData)}`);

      if (commonEventData.event === 'ServiceExtension_onCreate') {
        lifecycleList.push('onCreate');

        // onCreate 后调用 stopAppServiceExtensionAbility 触发 onDestroy
        context.stopAppServiceExtensionAbility({
          bundleName: 'com.example.test',
          abilityName: 'ServiceExtAbility'
        }).then(() => {
          hilog.info(0x0000, 'testTag', `${tcNumber} stopAppServiceExtensionAbility succeed`);
        }).catch((err: BusinessError) => {
          hilog.info(0x0000, 'testTag', `${tcNumber} stopAppServiceExtensionAbility error: ${JSON.stringify(err)}`);
          expect().assertFail();
          done();
        });
      }

      if (commonEventData.event === 'ServiceExtension_onDestroy') {
        lifecycleList.push('onDestroy');

        // 验证生命周期顺序：onCreate -> onDestroy
        expect(lifecycleList[0]).assertEqual('onCreate');
        expect(lifecycleList[1]).assertEqual('onDestroy');

        commonEventManager.unsubscribe(subscriber);
        done();
      }
    });
  });

  // 调用 startAppServiceExtensionAbility 启动服务，触发 onCreate
  try {
    await context.startAppServiceExtensionAbility({
      bundleName: 'com.example.test',
      abilityName: 'ServiceExtAbility'
    }).then(() => {
      hilog.info(0x0000, 'testTag', `${tcNumber} startAppServiceExtensionAbility succeed`);
    }).catch((err: BusinessError) => {
      hilog.info(0x0000, 'testTag', `${tcNumber} startAppServiceExtensionAbility error: ${JSON.stringify(err)}`);
      expect().assertFail();
      done();
    });
  } catch (err) {
    hilog.info(0x0000, 'testTag', `${tcNumber} error: ${JSON.stringify(err)}`);
    expect().assertFail();
    done();
  }
})
```

**ServiceExtAbility 实现端**:
```typescript
onDestroy(): void {
  hilog.info(0x0000, TAG, 'ServiceExtAbility onDestroy');

  // 发送 onDestroy 事件到测试用例
  commonEventManager.publish('ServiceExtension_onDestroy', {
    parameters: {
      lifecycle: 'onDestroy'
    }
  }).then(() => {
    hilog.info(0x0000, TAG, 'ServiceExtension_onDestroy event published');
  });
}
```

### 7.4 生命周期测试要点

#### 7.4.1 选择正确的启动接口

| 生命周期 | 启动接口 | 示例 |
|---------|---------|------|
| onCreate | startAppServiceExtensionAbility | `context.startAppServiceExtensionAbility(want)` |
| onConnect | connectAppServiceExtensionAbility | `context.connectAppServiceExtensionAbility(want, options)` |
| onDestroy | stopAppServiceExtensionAbility | `context.stopAppServiceExtensionAbility(want)` |

#### 7.4.2 事件命名规范

**事件名称格式**: `[组件名]_[生命周期]`

**示例**:
- `ServiceExtension_onCreate`
- `ServiceExtension_onConnect`
- `ServiceExtension_onDisconnect`
- `ServiceExtension_onDestroy`
- `UIAbility_onCreate`
- `UIAbility_onForeground`

#### 7.4.3 生命周期顺序验证

对于多个生命周期回调的测试，使用数组追踪顺序：

```typescript
let lifecycleList: string[] = [];
let lifecycleCheck = ['onCreate', 'onRequest', 'onDestroy'];

// 在事件回调中记录
if (commonEventData.event === 'ServiceExtension_onCreate') {
  lifecycleList.push('onCreate');
}

// 最终验证顺序
expect(JSON.stringify(lifecycleList)).assertEqual(JSON.stringify(lifecycleCheck));
```

#### 7.4.4 使用 Common Event 传递结果

```typescript
// ServiceExtension 端：发送事件
commonEventManager.publish('ServiceExtension_onCreate', {
  parameters: {
    lifecycle: 'onCreate',
    want: want,
    result: 'success'
  }
});

// 测试用例端：接收事件并验证
commonEventManager.subscribe(subscriber, (err, commonEventData) => {
  expect(commonEventData.parameters?.lifecycle).assertEqual('onCreate');
  expect(commonEventData.parameters?.result).assertEqual('success');
});
```

### 7.5 完整示例参考

**参考文件**:
- `/test/xts/acts/ability/ability_runtime/actsaappserviceextensioncontexttest/actsaappserviceextensioncon/entry/src/ohosTest/ets/test/Ability.test.ets`
- `/test/xts/acts/ability/ability_runtime/actsaappserviceextensioncontexttest/actsaappserviceextensioncon/entry/src/ohosTest/ets/testability/ServiceExtension/ServiceExtAbility.ets`

**关键用例**:
- `SUB_AA_ABILITY_NewRule_AppServiceExtension_0100` - connectAppServiceExtensionAbility 和 disconnectAppServiceExtensionAbility 测试（onConnect/onDisconnect）
- `SUB_AA_ABILITY_NewRule_AppServiceExtension_0300` - startAppServiceExtensionAbility 和 stopAppServiceExtensionAbility 测试（onCreate/onDestroy）
- `SUB_AA_ABILITY_NewRule_AppServiceExtension_0600` - AppServiceExtensionContext connectServiceExtensionAbility 测试

## 八、参考示例

参考已有的测试用例：
- `C:\Users\10418\Desktop\0202\xts_acts1\ability\ability_runtime\`
- `C:\Users\10418\Desktop\0202\xts_acts1\ability\ability_base\`

## 九、版本历史

- **v1.6.0** (2026-02-08): 新增通用生命周期测试规范（重要更新）⭐
  - **新增第七章**: 通用生命周期测试规范
  - 定义生命周期测试核心流程（6步）
  - 梳理常见 Ability 组件及其生命周期映射表
    - ServiceExtensionAbility 生命周期映射
    - UIAbility 生命周期映射
    - UIExtensionAbility 生命周期映射
    - DataAbility 生命周期映射
  - 提供3个完整的生命周期测试模板
    - onCreate 生命周期测试模板
    - onConnect/onDisconnect 生命周期测试模板
    - onDestroy 生命周期测试模板
  - 说明生命周期测试要点（4个方面）
    - 选择正确的启动接口
    - 事件命名规范
    - 生命周期顺序验证
    - 使用 Common Event 传递结果
  - 包含完整的 ServiceExtAbility 实现端代码示例
  - 提供完整的参考示例路径和关键用例说明
- **v1.5.0** (2026-02-08): 强化接口调用方式覆盖规范
  - **将"接口调用方式覆盖规范"提升为 2.1 节（最重要规则）** ⭐
  - 新增详细的 API 定义识别方法和判断示例
  - 新增标准测试用例模板（Promise 和 AsyncCallback）
  - 新增实现检查清单（6项检查项）
  - 新增常见错误示例和正确做法对比
  - 明确测试用例编号规则：Promise (00) / AsyncCallback (50)
  - 强调新增用例时必须优先考虑 callback 和 promise 两种方式
- **v1.4.0** (2026-02-08): 新增FA模型ServiceAbility测试规范
  - 新增 `fa_serviceability_testing.md` 文档
  - 提供完整的事件驱动测试模式说明
  - 包含标准测试用例模板和ServiceAbility实现规范
  - 说明want.action标识机制和命名规范
  - 包含ConnectAbility测试规范和最佳实践
- **v1.3.0** (2026-02-06): 新增UIExtension跨组件调用测试规范
  - 新增 `uiextension_cross_component.md` 文档
  - 提供完整的跨组件调用流程说明
  - 包含参数传递链路和注意事项
- **v1.2.0** (2026-02-06): 新增错误码断言规范（强制）
  - **错误码断言规范**: 必须使用 `assertEqual(-1)`，禁止使用 `code !== undefined`（强制）
  - 更新所有相关代码示例和模板
- **v1.1.0** (2026-02-04): 新增4项强制测试规范
  - **用例编号规范**: 每次递增100（强制）
  - **异常断言规范**: callback/promise必须使用try-catch{}（强制）
  - **接口测试覆盖规范**: 必须考虑callback和promise两种调用方式（强制）
  - **参数异常测试规范**: 不考虑callback是null/undefined（强制）
- **v1.0.0** (2026-02-03): 初始版本，定义Ability子系统通用配置

## 八、通用配置继承

- **v1.2.0** (2026-02-06): 新增错误码断言规范（强制）
  - **错误码断言规范**: 必须使用 `assertEqual(-1)`，禁止使用 `code !== undefined`（强制）
  - 更新所有相关代码示例和模板
- **v1.1.0** (2026-02-04): 新增4项强制测试规范
  - **用例编号规范**: 每次递增100（强制）
  - **异常断言规范**: callback/promise必须使用try-catch{}（强制）
  - **接口测试覆盖规范**: 必须考虑callback和promise两种调用方式（强制）
  - **参数异常测试规范**: 不考虑callback是null/undefined（强制）
- **v1.0.0** (2026-02-03): 初始版本，定义Ability子系统通用配置

## 七、通用配置继承

本 Ability 子系统配置继承自全局通用配置 (`references/subsystems/_common.md`):

- **测试用例命名规范**: 见 `_common.md` 第 1.1 节
- **测试级别定义**: 见 `_common.md` 第 1.2 节
- **测试类型定义**: 见 `_common.md` 第 1.3 节
- **通用代码模板**: 见 `_common.md` 第 2 节
