# 03. 状态管理接口测试指南

> 三、状态管理接口（State Management APIs）- 让界面"动起来"

---

## 接口说明

状态管理接口用来**让界面"动起来"**，是 ArkUI 的响应式核心。

### 常见装饰器

| 装饰器 | 用途 | 传递方向 |
|--------|------|---------|
| `@State` | 组件内部状态 | - |
| `@Prop` | 父子组件单向传递 | 父 → 子 |
| `@Link` | 父子组件双向绑定 | 父 ⇄ 子 |
| `@Observed` / `@ObjectLink` | 嵌套对象观测 | 父 → 子（深层） |
| `@Provide` / `@Consume` | 跨层级传递 | 祖先 ⇄ 后代 |
| `@Computed` | 计算属性 | 派生自其他状态 |

---

## 测试重点

### 1. @State 状态变化测试

**测试目的**：验证 `@State` 装饰的变量变化后 UI 是否正确更新。

#### 页面侧

```typescript
@Entry
@Component
struct ButtonStateTest {
  @State counter: number = 0;
  @State buttonText: string = 'Initial';
  @State isEnabled: boolean = true;

  build() {
    Column({ space: 20 }) {
      // 显示当前状态
      Text(`Count: ${this.counter}`)
        .id('text_count')

      Text(`Button: ${this.buttonText}`)
        .id('text_button')

      // 修改状态的按钮
      Button('Increment')
        .id('button_increment')
        .onClick(() => {
          this.counter++;
          this.buttonText = `Clicked ${this.counter} times`;
        })

      // 状态控制的按钮
      Button('Toggle Enabled')
        .id('button_toggle')
        .enabled(this.isEnabled)
        .onClick(() => {
          this.isEnabled = !this.isEnabled;
        })
    }
    .width('100%')
    .height('100%')
    .padding(20)
    .backgroundColor('#F5F5F5')
  }
}
```

#### 测试侧

```typescript
import { describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, Level } from '@ohos/hypium';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { destoryAbility, sleep, startPage } from '../../../uiutils/commonUtils';
import { UiComponent, Driver, ON } from '@ohos.UiTest';

export default function ButtonStateTest() {
  describe('ButtonStateTest', () => {
    beforeAll(async () => {
      hilog.info(0x0000, 'ButtonStateTest', 'beforeAll: start test page');
      await startPage('pages/button/ButtonStateTest');
      await sleep(1000);
    });

    /**
     * @tc.name   buttonStateChange_0100
     * @tc.number SUB_ARKUI_BUTTON_STATE_CHANGE_0100
     * @tc.desc   测试 @State 状态变化 - 点击后计数器增加
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('buttonStateChange_0100', Level.LEVEL0, async () => {
      // 获取初始状态
      let strJsonBefore: string = getInspectorByKey('text_count');
      let objBefore: Record<string, ESObject> = JSON.parse(strJsonBefore);
      let stateBefore: string = objBefore.$attrs.content as string;
      hilog.info(0x0000, 'ButtonStateTest', 'State before: ' + stateBefore);
      expect(stateBefore).assertEqual('Count: 0');

      // 触发状态变化
      let driver: Driver = await Driver.create();
      let button = await driver.findComponent(ON.id('button_increment'));
      await button.click();
      await sleep(500);  // 等待 UI 更新

      // 验证状态变化
      let strJsonAfter: string = getInspectorByKey('text_count');
      let objAfter: Record<string, ESObject> = JSON.parse(strJsonAfter);
      let stateAfter: string = objAfter.$attrs.content as string;
      hilog.info(0x0000, 'ButtonStateTest', 'State after: ' + stateAfter);
      expect(stateAfter).assertEqual('Count: 1');
    });

    /**
     * @tc.name   buttonStateChange_0200
     * @tc.number SUB_ARKUI_BUTTON_STATE_CHANGE_0200
     * @tc.desc   测试 @State 状态变化 - 多次点击计数器累加
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL1
     */
    it('buttonStateChange_0200', Level.LEVEL1, async () => {
      let driver: Driver = await Driver.create();
      let button = await driver.findComponent(ON.id('button_increment'));

      // 连续点击3次
      for (let i: number = 0; i < 3; i++) {
        await button.click();
        await sleep(300);
      }

      // 验证累加结果
      let strJson: string = getInspectorByKey('text_count');
      let obj: Record<string, ESObject> = JSON.parse(strJson);
      let content: string = obj.$attrs.content as string;
      expect(content).assertEqual('Count: 3');
    });
  });
}
```

### 2. @Prop 单向传递测试

**测试目的**：验证父组件通过 `@Prop` 向子组件传递数据。

#### 父组件页面侧

```typescript
@Entry
@Component
struct ParentPropTest {
  @State parentText: string = 'Parent Text';

  build() {
    Column({ space: 20 }) {
      Text(`Parent: ${this.parentText}`)
        .id('text_parent')

      // 子组件
      ChildComponent({ childText: this.parentText })
        .id('child_component')

      Button('Update Parent State')
        .id('button_update')
        .onClick(() => {
          this.parentText = 'Updated Text';
        })
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}

@Component
struct ChildComponent {
  @Prop childText: string;

  build() {
    Text(`Child: ${this.childText}`)
      .id('text_child')
  }
}
```

#### 测试侧

```typescript
/**
 * @tc.name   propDataTransfer_0100
 * @tc.number SUB_ARKUI_PROP_DATA_TRANSFER_0100
 * @tc.desc   测试 @Prop 单向数据传递 - 父组件状态更新后子组件同步
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('propDataTransfer_0100', Level.LEVEL0, async () => {
  // 获取初始状态
  let childJsonBefore: string = getInspectorByKey('text_child');
  let childObjBefore: Record<string, ESObject> = JSON.parse(childJsonBefore);
  let childTextBefore: string = childObjBefore.$attrs.content as string;
  expect(childTextBefore).assertEqual('Child: Parent Text');

  // 更新父组件状态
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_update'));
  await button.click();
  await sleep(500);

  // 验证子组件同步更新
  let childJsonAfter: string = getInspectorByKey('text_child');
  let childObjAfter: Record<string, ESObject> = JSON.parse(childJsonAfter);
  let childTextAfter: string = childObjAfter.$attrs.content as string;
  expect(childTextAfter).assertEqual('Child: Updated Text');
});
```

### 3. @Link 双向绑定测试

**测试目的**：验证父组件和子组件通过 `@Link` 实现双向数据绑定。

#### 父组件页面侧

```typescript
@Entry
@Component
struct ParentLinkTest {
  @State sharedValue: number = 0;

  build() {
    Column({ space: 20 }) {
      Text(`Parent Value: ${this.sharedValue}`)
        .id('text_parent_value')

      // 子组件通过 @Link 绑定
      ChildLinkComponent({ sharedValue: $sharedValue })
        .id('child_link_component')
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}

@Component
struct ChildLinkComponent {
  @Link sharedValue: number;

  build() {
    Column({ space: 10 }) {
      Text(`Child Value: ${this.sharedValue}`)
        .id('text_child_value')

      Button('Increment in Child')
        .id('button_child_increment')
        .onClick(() => {
          this.sharedValue++;  // 子组件修改会影响父组件
        })
    }
  }
}
```

#### 测试侧

```typescript
/**
 * @tc.name   linkTwoWayBinding_0100
 * @tc.number SUB_ARKUI_LINK_TWO_WAY_BINDING_0100
 * @tc.desc   测试 @Link 双向数据绑定 - 子组件修改影响父组件
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('linkTwoWayBinding_0100', Level.LEVEL0, async () => {
  // 获取初始状态
  let parentJsonBefore: string = getInspectorByKey('text_parent_value');
  let parentObjBefore: Record<string, ESObject> = JSON.parse(parentJsonBefore);
  expect(parentObjBefore.$attrs.content).assertEqual('Parent Value: 0');

  // 在子组件中修改值
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_child_increment'));
  await button.click();
  await sleep(500);

  // 验证父组件同步更新
  let parentJsonAfter: string = getInspectorByKey('text_parent_value');
  let parentObjAfter: Record<string, ESObject> = JSON.parse(parentJsonAfter);
  expect(parentObjAfter.$attrs.content).assertEqual('Parent Value: 1');

  // 验证子组件也更新
  let childJsonAfter: string = getInspectorByKey('text_child_value');
  let childObjAfter: Record<string, ESObject> = JSON.parse(childJsonAfter);
  expect(childObjAfter.$attrs.content).assertEqual('Child Value: 1');
});
```

### 4. @Observed / @ObjectLink 嵌套对象测试

**测试目的**：验证嵌套对象的深层观测。

#### 页面侧

```typescript
@Observed
class NestedObject {
  public id: number;
  public name: string;

  constructor(id: number, name: string) {
    this.id = id;
    this.name = name;
  }
}

@Entry
@Component
struct ObservedTest {
  @State nestedData: NestedObject = new NestedObject(1, 'Initial');

  build() {
    Column({ space: 20 }) {
      Text(`ID: ${this.nestedData.id}`)
        .id('text_id')

      Text(`Name: ${this.nestedData.name}`)
        .id('text_name')

      Button('Update Nested Object')
        .id('button_update')
        .onClick(() => {
          this.nestedData.id = 2;
          this.nestedData.name = 'Updated';
        })
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}
```

#### 测试侧

```typescript
/**
 * @tc.name   observedObjectUpdate_0100
 * @tc.number SUB_ARKUI_OBSERVED_OBJECT_UPDATE_0100
 * @tc.desc   测试 @Observed 嵌套对象更新
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('observedObjectUpdate_0100', Level.LEVEL0, async () => {
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_update'));
  await button.click();
  await sleep(500);

  let idJson: string = getInspectorByKey('text_id');
  let idObj: Record<string, ESObject> = JSON.parse(idJson);
  expect(idObj.$attrs.content).assertEqual('ID: 2');

  let nameJson: string = getInspectorByKey('text_name');
  let nameObj: Record<string, ESObject> = JSON.parse(nameJson);
  expect(nameObj.$attrs.content).assertEqual('Name: Updated');
});
```

---

## 测试注意事项

> **说明**：本节列出状态管理接口测试的特定注意事项。通用测试规范请参考 [_common.md](./_common.md)。

### 1. UI 更新等待时间

状态变化后需要等待 UI 更新完成：

```typescript
// ✅ 正确：等待 UI 更新
await button.click();
await sleep(500);  // 给 UI 渲染时间

// 验证状态
let obj = JSON.parse(getInspectorByKey('text_count'));
```

### 2. 状态验证方式

- 通过组件属性验证状态，而非直接访问状态变量
- 使用文本内容、显示/隐藏等 UI 属性验证

```typescript
// ✅ 正确：通过 UI 验证
let obj = JSON.parse(getInspectorByKey('text_count'));
expect(obj.$attrs.content).assertEqual('Count: 1');

// ❌ 错误：直接访问状态变量（测试侧无法访问）
expect(component.counter).assertEqual(1);
```

### 3. 双向绑定测试要点

- 测试父组件修改是否影响子组件
- 测试子组件修改是否影响父组件
- 测试多层嵌套的绑定传递

### 4. 嵌套对象测试要点

- 确保使用 `@Observed` 装饰对象类
- 测试对象属性的深层修改
- 验证对象引用变化时的 UI 更新

---

## 参考文档

- ArkUI 子系统通用配置：[_common.md](./_common.md)
- ArkUI 接口分类概览：[arkui.md](./arkui.md)
