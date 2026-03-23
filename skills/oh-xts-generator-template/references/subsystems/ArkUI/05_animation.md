# 05. 动画转场接口测试指南

> 五、动画与转场接口（Animation APIs）- 做动效和过渡

---

## 接口说明

动画与转场接口用来**做动效和过渡**，包括显式动画、隐式动画和页面转场。

### 常见接口分类

| 类型 | 示例 |
|------|------|
| 显式动画 | `animateTo()`、`animateToImmediately()` |
| 隐式动画 | `animation()` |
| 属性动画 | `scale()`、`rotate()`、`translate()` |
| 转场动画 | `transition()`、`PageTransition()` |
| 动画曲线 | `Curve`、`SpringCurve`、`ICurve` |
| 动画效果 | `motionBlur()`、`geometryTransition()` |

---

## 测试重点

### 1. animateTo 显式动画测试

**测试目的**：验证 `animateTo` 显式动画执行后组件的最终状态。

#### 页面侧

```typescript
@Entry
@Component
struct AnimateToTest {
  @State scale: number = 1;
  @State rotation: number = 0;
  @State translateX: number = 0;

  build() {
    Column({ space: 20 }) {
      Text('Animate Test')
        .id('text_animate')
        .width(100)
        .height(50)
        .backgroundColor('#FF0000')
        .scale({ x: this.scale, y: this.scale })
        .rotate({ angle: this.rotation })
        .translate({ x: this.translateX })

      Button('Start Animate')
        .id('button_animate')
        .onClick(() => {
          animateTo({ duration: 300, curve: Curve.EaseInOut }, () => {
            this.scale = 2;
            this.rotation = 180;
            this.translateX = 50;
          });
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

export default function AnimateToTest() {
  describe('AnimateToTest', () => {
    beforeAll(async () => {
      hilog.info(0x0000, 'AnimateToTest', 'beforeAll: start test page');
      await startPage('pages/animate/AnimateToTest');
      await sleep(1000);
    });

    /**
     * @tc.name   animateTo_0100
     * @tc.number SUB_ARKUI_ANIMATETO_0100
     * @tc.desc   测试 animateTo 显式动画 - 验证动画后最终状态
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL1
     */
    it('animateTo_0100', Level.LEVEL1, async () => {
      // 获取初始状态
      let strJsonBefore: string = getInspectorByKey('text_animate');
      let objBefore: Record<string, ESObject> = JSON.parse(strJsonBefore);
      hilog.info(0x0000, 'AnimateToTest', 'Scale before: ' + objBefore.$attrs.scale);

      // 触发动画
      let driver: Driver = await Driver.create();
      let button = await driver.findComponent(ON.id('button_animate'));
      await button.click();
      await sleep(500);  // 等待动画完成（duration: 300ms）

      // 验证动画后的最终状态
      let strJsonAfter: string = getInspectorByKey('text_animate');
      let objAfter: Record<string, ESObject> = JSON.parse(strJsonAfter);

      // 验证缩放状态
      let scale: string = objAfter.$attrs.scale as string;
      hilog.info(0x0000, 'AnimateToTest', 'Scale after: ' + scale);
      expect(scale).assertEqual('2.00');

      // 验证旋转状态
      let rotation: string = objAfter.$attrs.rotation as string;
      hilog.info(0x0000, 'AnimateToTest', 'Rotation after: ' + rotation);
      expect(rotation).assertEqual('180.00');
    });

    /**
     * @tc.name   animateTo_0200
     * @tc.number SUB_ARKUI_ANIMATETO_0200
     * @tc.desc   测试 animateTo 显式动画 - 不同动画曲线
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL2
     */
    it('animateTo_0200', Level.LEVEL2, async () => {
      // 测试不同动画曲线的动画效果
      // 验证动画最终状态与曲线参数无关
      let driver: Driver = await Driver.create();
      let button = await driver.findComponent(ON.id('button_animate'));
      await button.click();
      await sleep(500);

      let strJson: string = getInspectorByKey('text_animate');
      let obj: Record<string, ESObject> = JSON.parse(strJson);
      let scale: string = obj.$attrs.scale as string;
      expect(scale).assertEqual('2.00');
    });
  });
}
```

### 2. animation 隐式动画测试

**测试目的**：验证 `animation` 隐式动画在属性变化时的效果。

#### 页面侧

```typescript
@Entry
@Component
struct AnimationTest {
  @State width: number = 100;
  @State height: number = 50;

  build() {
    Column({ space: 20 }) {
      Column()
        .id('column_animated')
        .width(this.width)
        .height(this.height)
        .backgroundColor('#00FF00')
        .animation({
          duration: 300,
          curve: Curve.EaseInOut,
          iterations: 1
        })

      Button('Change Size')
        .id('button_change_size')
        .onClick(() => {
          this.width = 200;
          this.height = 100;
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
 * @tc.name   animation_0100
 * @tc.number SUB_ARKUI_ANIMATION_0100
 * @tc.desc   测试 animation 隐式动画 - 属性变化后的最终状态
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL1
 */
it('animation_0100', Level.LEVEL1, async () => {
  // 获取初始状态
  let strJsonBefore: string = getInspectorByKey('column_animated');
  let objBefore: Record<string, ESObject> = JSON.parse(strJsonBefore);
  expect(objBefore.$attrs.width).assertEqual('100.00vp');

  // 触发属性变化
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_change_size'));
  await button.click();
  await sleep(500);  // 等待动画完成

  // 验证最终状态
  let strJsonAfter: string = getInspectorByKey('column_animated');
  let objAfter: Record<string, ESObject> = JSON.parse(strJsonAfter);
  expect(objAfter.$attrs.width).assertEqual('200.00vp');
  expect(objAfter.$attrs.height).assertEqual('100.00vp');
});
```

### 3. 属性动画测试（scale、rotate、translate）

**测试目的**：验证组件的变换属性动画效果。

#### 页面侧

```typescript
@Entry
@Component
struct TransformAnimationTest {
  @State scaleValue: number = 1;
  @State rotateValue: number = 0;
  @State translateX: number = 0;
  @State translateY: number = 0;

  build() {
    Column({ space: 20 }) {
      // 缩放动画测试
      Text('Scale Test')
        .id('text_scale')
        .scale({ x: this.scaleValue, y: this.scaleValue })

      // 旋转动画测试
      Text('Rotate Test')
        .id('text_rotate')
        .rotate({ angle: this.rotateValue })

      // 平移动画测试
      Text('Translate Test')
        .id('text_translate')
        .translate({ x: this.translateX, y: this.translateY })

      Button('Start Transform')
        .id('button_transform')
        .onClick(() => {
          this.scaleValue = 1.5;
          this.rotateValue = 90;
          this.translateX = 30;
          this.translateY = 20;
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
 * @tc.name   scaleAnimation_0100
 * @tc.number SUB_ARKUI_SCALE_ANIMATION_0100
 * @tc.desc   测试 scale 缩放动画效果
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL1
 */
it('scaleAnimation_0100', Level.LEVEL1, async () => {
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_transform'));
  await button.click();
  await sleep(500);

  let strJson: string = getInspectorByKey('text_scale');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  let scale: string = obj.$attrs.scale as string;
  expect(scale).assertEqual('1.50');
});

/**
 * @tc.name   rotateAnimation_0100
 * @tc.number SUB_ARKUI_ROTATE_ANIMATION_0100
 * @tc.desc   测试 rotate 旋转动画效果
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL1
 */
it('rotateAnimation_0100', Level.LEVEL1, async () => {
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_transform'));
  await button.click();
  await sleep(500);

  let strJson: string = getInspectorByKey('text_rotate');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  let rotation: string = obj.$attrs.rotation as string;
  expect(rotation).assertEqual('90.00');
});

/**
 * @tc.name   translateAnimation_0100
 * @tc.number SUB_ARKUI_TRANSLATE_ANIMATION_0100
 * @tc.desc   测试 translate 平移动画效果
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL1
 */
it('translateAnimation_0100', Level.LEVEL1, async () => {
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_transform'));
  await button.click();
  await sleep(500);

  let strJson: string = getInspectorByKey('text_translate');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  let translate: string = obj.$attrs.translate as string;
  // translate 返回格式可能为 "x,y" 或对象形式
  expect(translate).assertContain('30');
  expect(translate).assertContain('20');
});
```

### 4. transition 转场动画测试

**测试目的**：验证组件的转场动画效果。

#### 页面侧

```typescript
@Entry
@Component
struct TransitionTest {
  @State show: boolean = true;

  build() {
    Column({ space: 20 }) {
      Button('Toggle Transition')
        .id('button_toggle')
        .onClick(() => {
          this.show = !this.show;
        })

      if (this.show) {
        Text('Transition Content')
          .id('text_transition')
          .width(200)
          .height(100)
          .backgroundColor('#FF0000')
          .transition({ type: TransitionType.All, opacity: 0, translate: { x: -100 } })
      }
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
 * @tc.name   transition_0100
 * @tc.number SUB_ARKUI_TRANSITION_0100
 * @tc.desc   测试 transition 转场动画 - 组件消失
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL1
 */
it('transition_0100', Level.LEVEL1, async () => {
  // 验证初始状态组件存在
  let strJsonBefore: string = getInspectorByKey('text_transition');
  expect(strJsonBefore).not.assertEqual('');

  // 触发转场
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_toggle'));
  await button.click();
  await sleep(500);  // 等待转场完成

  // 验证组件已消失（可能抛出异常或返回空）
  try {
    let strJsonAfter: string = getInspectorByKey('text_transition');
    // 如果能获取到，验证 opacity 等属性
  } catch (e) {
    // 组件已消失，符合预期
  }
});
```

### 5. 动画曲线测试

**测试目的**：验证不同动画曲线的效果。

#### 常见动画曲线

| 曲线 | 说明 |
|------|------|
| `Curve.Linear` | 线性曲线 |
| `Curve.EaseIn` | 缓入曲线 |
| `Curve.EaseOut` | 缓出曲线 |
| `Curve.EaseInOut` | 缓入缓出曲线 |
| `Curve.FastOutSlowIn` | 快出慢入曲线 |
| `Curve.SpringMotion` | 弹簧曲线 |

#### 测试策略

动画曲线主要影响动画过程，**测试重点验证最终状态**，曲线参数对最终状态无影响：

```typescript
/**
 * @tc.name   animationCurve_0100
 * @tc.number SUB_ARKUI_ANIMATION_CURVE_0100
 * @tc.desc   测试不同动画曲线的最终状态一致
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL2
 */
it('animationCurve_0100', Level.LEVEL2, async () => {
  // 不同曲线参数不应影响最终状态
  // 验证动画完成后，组件状态与目标值一致
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_animate'));
  await button.click();
  await sleep(1000);  // 等待足够时间

  // 验证最终状态
  let strJson: string = getInspectorByKey('text_animate');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  expect(obj.$attrs.scale).assertEqual('2.00');
});
```

---

## 测试注意事项

> **说明**：本节列出动画转场接口测试的特定注意事项。通用测试规范请参考 [_common.md](./_common.md)。

### 1. 动画等待时间

动画测试需要足够长的等待时间：

```typescript
// 等待时间应大于动画 duration
await button.click();
await sleep(500);  // duration: 300ms，等待 500ms
```

### 2. 验证最终状态

动画测试应验证**最终状态**，而非动画过程：

```typescript
// ✅ 正确：验证最终状态
let obj = JSON.parse(getInspectorByKey('text_animate'));
expect(obj.$attrs.scale).assertEqual('2.00');

// ❌ 错误：尝试验证动画过程（难以实现）
// 动画过程中的中间状态难以捕获和验证
```

### 3. 测试级别

动画测试通常属于 LEVEL1 或更高级别：

```typescript
it('animation_test', Level.LEVEL1, async () => {
  // 动画测试通常为 LEVEL1
});
```

### 4. 转场动画特殊性

转场动画可能涉及组件的创建和销毁：

```typescript
// 组件消失后可能无法通过 getInspectorByKey 获取
try {
  let strJson: string = getInspectorByKey('text_transition');
  // 处理存在的情况
} catch (e) {
  // 组件已消失，符合预期
}
```

### 5. 属性返回格式

变换属性在组件树中的返回格式：

| 属性 | 返回格式示例 |
|------|-------------|
| `scale` | `'2.00'` 或 `'x,y'` |
| `rotate` | `'90.00'` (角度) |
| `translate` | `'30.00,20.00'` (x,y) |

---

## 动画测试模板

### 页面侧模板

```typescript
@Entry
@Component
struct {Component}AnimationTest {
  @State {animState}: number = {InitialValue};

  build() {
    Column({ space: 20 }) {
      {Component}('Animation Test')
        .id('{component}_animated')
        .{animProperty}({this.{animState}})

      Button('Start Animation')
        .id('button_animate')
        .onClick(() => {
          animateTo({ duration: 300, curve: Curve.EaseInOut }, () => {
            this.{animState} = {TargetValue};
          });
        })
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

export default function {Component}AnimationTest() {
  describe('{Component}AnimationTest', () => {
    beforeAll(async () => {
      hilog.info(0x0000, '{Component}AnimationTest', 'beforeAll: start test page');
      await startPage('pages/{component}/{Component}AnimationTest');
      await sleep(1000);
    });

    /**
     * @tc.name   {component}Animation_0100
     * @tc.number SUB_ARKUI_{COMPONENT}_ANIMATION_0100
     * @tc.desc   测试 {Component} 的动画效果 - 验证最终状态
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL1
     */
    it('{component}Animation_0100', Level.LEVEL1, async () => {
      // 获取初始状态
      let strJsonBefore: string = getInspectorByKey('{component}_animated');
      let objBefore: Record<string, ESObject> = JSON.parse(strJsonBefore);

      // 触发动画
      let driver: Driver = await Driver.create();
      let button = await driver.findComponent(ON.id('button_animate'));
      await button.click();
      await sleep(500);  // 等待动画完成

      // 验证最终状态
      let strJsonAfter: string = getInspectorByKey('{component}_animated');
      let objAfter: Record<string, ESObject> = JSON.parse(strJsonAfter);
      let {animProperty}: string = objAfter.$attrs.{animProperty} as string;
      expect({animProperty}).assertEqual('{ExpectedValue}');
    });
  });
}
```

---

## 参考文档

- ArkUI 子系统通用配置：[_common.md](./_common.md)
- ArkUI 接口分类概览：[arkui.md](./arkui.md)
