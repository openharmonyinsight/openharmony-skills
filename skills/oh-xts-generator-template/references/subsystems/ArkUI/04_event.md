# 04. 事件交互接口测试指南

> 四、事件与交互接口（Event & Gesture APIs）- 响应用户操作

---

## 接口说明

事件与交互接口用来**响应用户操作**，包括基础事件、生命周期事件和手势事件。

### 常见接口分类

| 类型 | 示例 |
|------|------|
| 基础事件 | `onClick()`、`onTouch()`、`onHover()`、`onMouse()` |
| 生命周期事件 | `onAppear()`、`onDisAppear()`、`onPageShow()`、`onPageHide()` |
| 焦点事件 | `onFocus()`、`onBlur()` |
| 按键事件 | `onKeyEvent()` |
| 手势接口 | `TapGesture`、`LongPressGesture`、`PanGesture`、`PinchGesture`、`RotationGesture` |

---

## 测试重点

### 1. onClick 点击事件测试

**测试目的**：验证点击事件是否正确触发。

#### 页面侧

```typescript
@Entry
@Component
struct ButtonOnClickTest {
  @State clickCount: number = 0;
  @State buttonText: string = 'Click Me';

  build() {
    Column({ space: 20 }) {
      Button(this.buttonText)
        .id('button_click')
        .onClick(() => {
          this.clickCount++;
          this.buttonText = `Clicked ${this.clickCount} times`;
        })

      Text(`Click count: ${this.clickCount}`)
        .id('text_count')
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

export default function ButtonOnClickTest() {
  describe('ButtonOnClickTest', () => {
    beforeAll(async () => {
      hilog.info(0x0000, 'ButtonOnClickTest', 'beforeAll: start test page');
      await startPage('pages/button/ButtonOnClickTest');
      await sleep(1000);
    });

    /**
     * @tc.name   buttonOnClick_0100
     * @tc.number SUB_ARKUI_BUTTON_ONCLICK_EVENT_0100
     * @tc.desc   测试 Button 的 onClick 事件 - 单次点击
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('buttonOnClick_0100', Level.LEVEL0, async () => {
      // 获取初始状态
      let strJsonBefore: string = getInspectorByKey('text_count');
      let objBefore: Record<string, ESObject> = JSON.parse(strJsonBefore);
      let stateBefore: string = objBefore.$attrs.content as string;
      hilog.info(0x0000, 'ButtonOnClickTest', 'State before: ' + stateBefore);

      // 触发点击事件
      let driver: Driver = await Driver.create();
      let button = await driver.findComponent(ON.id('button_click'));
      await button.click();
      await sleep(500);  // 等待事件处理和 UI 更新

      // 验证状态变化
      let strJsonAfter: string = getInspectorByKey('text_count');
      let objAfter: Record<string, ESObject> = JSON.parse(strJsonAfter);
      let stateAfter: string = objAfter.$attrs.content as string;
      hilog.info(0x0000, 'ButtonOnClickTest', 'State after: ' + stateAfter);

      expect(stateAfter).assertEqual('Click count: 1');
    });

    /**
     * @tc.name   buttonOnClick_0200
     * @tc.number SUB_ARKUI_BUTTON_ONCLICK_EVENT_0200
     * @tc.desc   测试 Button 的 onClick 事件 - 多次点击累加
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL1
     */
    it('buttonOnClick_0200', Level.LEVEL1, async () => {
      let driver: Driver = await Driver.create();
      let button = await driver.findComponent(ON.id('button_click'));

      // 连续点击3次
      for (let i: number = 0; i < 3; i++) {
        await button.click();
        await sleep(300);
      }

      // 验证累加结果
      let strJson: string = getInspectorByKey('text_count');
      let obj: Record<string, ESObject> = JSON.parse(strJson);
      let content: string = obj.$attrs.content as string;
      expect(content).assertEqual('Click count: 3');
    });
  });
}
```

### 2. onTouch 触摸事件测试

**测试目的**：验证触摸事件是否正确触发。

#### 页面侧

```typescript
@Entry
@Component
struct TouchEventTest {
  @State touchType: string = 'None';
  @State touchX: string = '0';
  @State touchY: string = '0';

  build() {
    Column({ space: 20 }) {
      Text(`Touch Type: ${this.touchType}`)
        .id('text_touch_type')

      Text(`Position: (${this.touchX}, ${this.touchY})`)
        .id('text_touch_pos')

      Column()
        .width('200vp')
        .height('100vp')
        .backgroundColor('#FF0000')
        .id('column_touch_area')
        .onTouch((event: TouchEvent) => {
          if (event.type === TouchType.Down) {
            this.touchType = 'Down';
            this.touchX = event.touches[0].x.toString();
            this.touchY = event.touches[0].y.toString();
          } else if (event.type === TouchType.Up) {
            this.touchType = 'Up';
          } else if (event.type === TouchType.Move) {
            this.touchType = 'Move';
          }
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
/**
 * @tc.name   onTouchEvent_0100
 * @tc.number SUB_ARKUI_TOUCH_EVENT_0100
 * @tc.desc   测试 onTouch 事件 - 触摸触发
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('onTouchEvent_0100', Level.LEVEL0, async () => {
  let driver: Driver = await Driver.create();
  let touchArea = await driver.findComponent(ON.id('column_touch_area'));

  // 执行点击操作（包含按下和抬起）
  await touchArea.click();
  await sleep(500);

  // 验证触摸类型被记录
  let typeJson: string = getInspectorByKey('text_touch_type');
  let typeObj: Record<string, ESObject> = JSON.parse(typeJson);
  let typeContent: string = typeObj.$attrs.content as string;
  // 验证触摸事件触发
  expect(typeContent).assertNotEqual('Touch Type: None');
});
```

### 3. onAppear/onDisAppear 生命周期事件测试

**测试目的**：验证组件显示/隐藏事件。

#### 页面侧

```typescript
@Entry
@Component
struct LifecycleEventTest {
  @State appearCount: number = 0;
  @State disappearCount: number = 0;
  @State showComponent: boolean = true;

  build() {
    Column({ space: 20 }) {
      Button('Toggle Component')
        .id('button_toggle')
        .onClick(() => {
          this.showComponent = !this.showComponent;
        })

      if (this.showComponent) {
        Text('Lifecycle Component')
          .id('text_lifecycle')
          .onAppear(() => {
            this.appearCount++;
          })
          .onDisAppear(() => {
            this.disappearCount++;
          })
      }

      Text(`Appear: ${this.appearCount}, Disappear: ${this.disappearCount}`)
        .id('text_count')
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
/**
 * @tc.name   onAppearEvent_0100
 * @tc.number SUB_ARKUI_ONAPPEAR_EVENT_0100
 * @tc.desc   测试 onAppear 生命周期事件
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('onAppearEvent_0100', Level.LEVEL0, async () => {
  // 初始状态下组件已出现
  let strJson: string = getInspectorByKey('text_count');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  let content: string = obj.$attrs.content as string;
  expect(content).assertEqual('Appear: 1, Disappear: 0');
});

/**
 * @tc.name   onDisAppearEvent_0100
 * @tc.number SUB_ARKUI_ONDISAPPEAR_EVENT_0100
 * @tc.desc   测试 onDisAppear 生命周期事件
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('onDisAppearEvent_0100', Level.LEVEL0, async () => {
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_toggle'));

  // 隐藏组件
  await button.click();
  await sleep(500);

  let strJson: string = getInspectorByKey('text_count');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  let content: string = obj.$attrs.content as string;
  expect(content).assertEqual('Appear: 1, Disappear: 1');
});
```

### 4. 手势事件测试

**测试目的**：验证各种手势事件的触发。

#### 页面侧（长按手势）

```typescript
@Entry
@Component
struct LongPressGestureTest {
  @State gestureResult: string = 'No Gesture';

  build() {
    Column({ space: 20 }) {
      Text(`Gesture: ${this.gestureResult}`)
        .id('text_gesture_result')

      Column()
        .width('200vp')
        .height('100vp')
        .backgroundColor('#00FF00')
        .id('column_gesture_area')
        .gesture(
          LongPressGesture({ repeat: false })
            .onAction(() => {
              this.gestureResult = 'Long Pressed';
            })
        )
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
/**
 * @tc.name   longPressGesture_0100
 * @tc.number SUB_ARKUI_LONGPRESS_GESTURE_0100
 * @tc.desc   测试长按手势事件
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL1
 */
it('longPressGesture_0100', Level.LEVEL1, async () => {
  let driver: Driver = await Driver.create();
  let gestureArea = await driver.findComponent(ON.id('column_gesture_area'));

  // 执行长按操作
  await gestureArea.longPress();
  await sleep(1000);  // 长按需要更长等待时间

  // 验证手势结果
  let resultJson: string = getInspectorByKey('text_gesture_result');
  let resultObj: Record<string, ESObject> = JSON.parse(resultJson);
  let resultContent: string = resultObj.$attrs.content as string;
  expect(resultContent).assertEqual('Gesture: Long Pressed');
});
```

---

## UiTest API 规范

### 1. Driver 创建

```typescript
import { UiComponent, Driver, ON } from '@ohos.UiTest';

// 在测试用例中创建 Driver
let driver: Driver = await Driver.create();
```

### 2. 组件查找

```typescript
// 通过 ID 查找
let button = await driver.findComponent(ON.id('button_click'));

// 通过文本查找
let textComponent = await driver.findComponent(ON.text('Click Me'));

// 通过其他属性查找
let component = await driver.findComponent(ON.type('Button'));
```

### 3. 组件操作

```typescript
// 点击
await button.click();

// 长按
await component.longPress();

// 滑动
await component.swipe(Direction.DOWN);

// 输入文本（对于 TextInput）
await textInput.setText('Hello');
```

---

## 测试注意事项

### 事件交互接口特定注意事项

#### 1. 事件触发后等待时间

事件触发后需要等待足够时间让 UI 更新：

```typescript
await button.click();
await sleep(500);  // 等待事件处理和 UI 更新
```

#### 2. 手势测试注意事项

- 手势测试属于 LEVEL1 或更高级别
- 长按、滑动等手势需要更长的等待时间
- 不同手势可能需要特定的测试场景

### 通用规范引用

| 规范项 | 说明 | 参考文档 |
|--------|------|---------|
| 状态验证方式 | 通过 UI 属性验证，而非直接访问状态变量 | [_common.md](./_common.md) |
| 一个用例只验证一个测试点 | 避免用例职责过重 | [_common.md](./_common.md) |

---

## 事件测试模板

### 页面侧模板

```typescript
@Entry
@Component
struct {Component}{Event}Test {
  @State {eventState}: string = '{InitialValue}';

  build() {
    Column({ space: 20 }) {
      {Component}('{Component} {Event} Test')
        .id('{component}_{event}')
        .{event}(() => {
          this.{eventState} = '{TriggeredValue}';
        })

      Text(`State: ${this.{eventState}}`)
        .id('text_{event_state}')
    }
    .width('100%')
    .height('100%')
    .padding(20)
    .backgroundColor('#F5F5F5')
  }
}
```

### 测试侧模板

```typescript
import { describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, Level } from '@ohos/hypium';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { destoryAbility, sleep, startPage } from '../../../uiutils/commonUtils';
import { UiComponent, Driver, ON } from '@ohos.UiTest';

export default function {Component}{Event}Test() {
  describe('{Component}{Event}Test', () => {
    beforeAll(async () => {
      hilog.info(0x0000, '{Component}{Event}Test', 'beforeAll: start test page');
      await startPage('pages/{component}/{Component}{Event}');
      await sleep(1000);
    });

    /**
     * @tc.name   {component}{event}_0100
     * @tc.number SUB_ARKUI_{COMPONENT}_{EVENT}_EVENT_0100
     * @tc.desc   测试 {Component} 的 {event} 事件
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('{component}{event}_0100', Level.LEVEL0, async () => {
      // 获取初始状态
      let strJsonBefore: string = getInspectorByKey('text_{event_state}');
      let objBefore: Record<string, ESObject> = JSON.parse(strJsonBefore);
      let stateBefore: string = objBefore.$attrs.content as string;

      // 触发事件
      let driver: Driver = await Driver.create();
      let component = await driver.findComponent(ON.id('{component}_{event}'));
      await component.click();
      await sleep(500);

      // 验证状态变化
      let strJsonAfter: string = getInspectorByKey('text_{event_state}');
      let objAfter: Record<string, ESObject> = JSON.parse(strJsonAfter);
      let stateAfter: string = objAfter.$attrs.content as string;
      expect(stateAfter).assertNotEqual(stateBefore);
    });
  });
}
```

---

## 参考文档

- ArkUI 子系统通用配置：[_common.md](./_common.md)
- ArkUI 接口分类概览：[arkui.md](./arkui.md)
