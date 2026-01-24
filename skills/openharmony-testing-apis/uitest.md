# @ohos.UiTest

**模块**: UiTest
**API 版本**: 8+
**导入方式**: `import { Driver, ON, Component, UiWindow, MatchPattern } from '@kit.TestKit';`

## 概述

提供在测试期间模拟 UI 交互的 API：点击、双击、长按、滑动、文本输入和组件属性验证。

**重要提示**：
- 只能在 UiTest 上下文中使用
- 不支持并发调用
- API 9+ 使用 **ON/Component/Driver**（推荐）
- API 8 使用 **BY/UiComponent/UiDriver**（已废弃）

## 快速导入

```typescript
// 推荐（API 9+）
import {
  Driver, ON, Component, UiWindow,
  MatchPattern, DisplayRotation, WindowMode
} from '@kit.TestKit';

// 已废弃（API 8）
import { UiDriver, BY, UiComponent } from '@kit.TestKit';
```

## MatchPattern 枚举

定义组件属性的匹配模式。

| 值 | 名称 | 描述 |
|-------|------|-------------|
| 0 | EQUALS | 等于给定值 |
| 1 | CONTAINS | 包含给定值 |
| 2 | STARTS_WITH | 以给定值开头 |
| 3 | ENDS_WITH | 以给定值结尾 |
| 4 | REG_EXP (API 18+) | 正则表达式匹配 |
| 5 | REG_EXP_ICASE (API 18+) | 不区分大小写的正则表达式 |

## Driver (API 9+)

UI 测试的入口类。提供组件匹配/查找、按键注入、坐标操作和截图功能。

### 创建 Driver

```typescript
static create(): Driver
```

**示例**:
```typescript
import { Driver } from '@kit.TestKit';

let driver = Driver.create();
```

### 核心方法

#### find()
```typescript
find(on: On): Promise<Component>
```
查找匹配的组件。

```typescript
let button = await driver.find(ON.id('submitBtn'));
```

#### findComponents()
```typescript
findComponents(on: On): Promise<Component[]>
```
查找所有匹配的组件。

#### pressBack()
```typescript
pressBack(): Promise<void>
```
模拟按下返回按钮。

#### triggerClick()
```typescript
triggerClick(point: Point): Promise<void>
```
在指定坐标处点击。

#### swipe()
```typescript
swipe(start: Point, end: Point, speed?: number): Promise<void>
```
从起点滑动到终点。

#### assertComponentExist()
```typescript
assertComponentExist(on: On): Promise<void>
```
断言组件存在。

#### screenshot()
```typescript
screenshot(): Promise<string>
```
截图并返回保存路径。

## ON (API 9+)

组件特征描述类，用于过滤和匹配组件。

### 静态构造器

```typescript
import { ON } from '@kit.TestKit';

// 链式调用多个属性
let on = ON.text('提交').type('Button').id('btn1');
```

### 属性方法

#### text()
```typescript
text(txt: string, pattern?: MatchPattern): On
```
按组件文本匹配。

```typescript
ON.text('123')                              // 精确匹配
ON.text('提交', MatchPattern.CONTAINS)      // 包含匹配
```

#### id()
```typescript
id(id: string): On              // API 9
id(id: string, pattern: MatchPattern): On  // API 18+
```
按组件 ID 匹配。

```typescript
ON.id('submitBtn')
ON.id('btn.*', MatchPattern.REG_EXP)  // API 18+
```

#### type()
```typescript
type(tp: string): On            // API 9
type(tp: string, pattern: MatchPattern): On  // API 18+
```
按组件类型匹配（Button、Text 等）。

```typescript
ON.type('Button')
ON.type('Text', MatchPattern.EQUALS)
```

#### clickable()
```typescript
clickable(b?: boolean): On
```
按可点击状态匹配。

#### enabled()
```typescript
enabled(b?: boolean): On
```
按启用状态匹配。

#### focused()
```typescript
focused(b?: boolean): On
```
按焦点状态匹配。

#### selected()
```typescript
selected(b?: boolean): On
```
按选中状态匹配。

#### checked()
```typescript
checked(b?: boolean): On
```
按勾选状态匹配。

#### checkable()
```typescript
checkable(b?: boolean): On
```
按可勾选状态匹配。

### 定位方法 (API 9+)

#### isBefore()
```typescript
isBefore(on: On): On
```
组件在另一个组件之前。

```typescript
ON.text('姓名').isBefore(ON.type('TextInput'))
```

#### isAfter()
```typescript
isAfter(on: On): On
```
组件在另一个组件之后。

#### within()
```typescript
within(on: On): On
```
组件在另一个组件内（父组件）。

### 边界方法

#### bounds()
```typescript
bounds(rect: Rect): On
```
按组件边界匹配（left、top、right、bottom）。

```typescript
ON.bounds({ left: 0, top: 0, right: 100, bottom: 100 })
```

## Component (API 9+)

表示具有交互能力的 UI 组件。

### 核心方法

#### click()
```typescript
click(): Promise<void>
```
点击组件。

```typescript
let button = await driver.find(ON.id('submit'));
await button.click();
```

#### doubleClick()
```typescript
doubleClick(): Promise<void>
```
双击组件。

#### longClick()
```typescript
longClick(): Promise<void>
```
长按组件。

#### clickText()
```typescript
clickText(text: string, pattern?: MatchPattern): Promise<void>
```
点击组件内的文本。

#### inputText()
```typescript
inputText(text: string): Promise<void>
```
向文本组件输入文本。

```typescript
let input = await driver.find(ON.type('TextInput'));
await input.inputText('你好世界');
```

#### clear()
```typescript
clear(): Promise<void>
```
清空文本输入。

#### scrollWidth()
```typescript
scrollTo(targetOn: On, direction?: UiDirection): Promise<boolean>
```
滚动以查找目标组件。

```typescript
let list = await driver.find(ON.type('List'));
await list.scrollTo(ON.text('目标项'), UiDirection.DOWN);
```

#### pinchOut()
```typescript
pinchOut(scale?: number): Promise<void>
```
捏合手势（放大）。

#### pinchIn()
```typescript
pinchIn(scale?: number): Promise<void>
```
捏合手势（缩小）。

#### getAttribute()
```typescript
getAttribute(key: string): Promise<string>
```
获取组件属性值。

```typescript
let button = await driver.find(ON.id('btn'));
let id = await button.getAttribute('id');
let text = await button.getAttribute('text');
```

#### getBounds()
```typescript
getBounds(): Promise<Rect>
```
获取组件边界。

#### isEnabled()
```typescript
isEnabled(): Promise<boolean>
```
检查组件是否启用。

#### isCheckable()
```typescript
isCheckable(): Promise<boolean>
```
检查组件是否可勾选。

#### isChecked()
```typescript
isChecked(): Promise<boolean>
```
检查组件是否已勾选。

### 组件列表方法

#### getChildren()
```typescript
getChildren(): Promise<Component[]>
```
获取子组件。

#### sibling()
```typescript
sibling(on: On): Promise<Component>
```
获取兄弟组件。

## UiWindow (API 9+)

窗口操作的入口类。

### 创建 UiWindow

```typescript
static create(): UiWindow
```

### 核心方法

#### getProperties()
```typescript
getProperties(): Promise<WindowProperties>
```
获取窗口属性（边界、模式、旋转等）。

#### drag()
```typescript
drag(start: Point, end: Point): Promise<void>
```
拖动窗口。

#### resize()
```typescript
resize(direction: ResizeDirection, amount: number): Promise<void>
```
按指定方向调整窗口大小。

```typescript
let window = UiWindow.create();
await window.resize(ResizeDirection.RIGHT_DOWN, 100);
```

#### move()
```typescript
move(to: Point): Promise<void>
```
移动窗口。

## 完整示例

```typescript
import { Driver, ON, MatchPattern, UiDirection } from '@kit.TestKit';

async function testLoginForm() {
  // 创建 driver
  let driver = Driver.create();

  // 查找用户名输入框并输入文本
  let usernameInput = await driver.find(ON.id('username'));
  await usernameInput.inputText('testuser@example.com');

  // 查找密码输入框并输入文本
  let passwordInput = await driver.find(ON.id('password'));
  await passwordInput.inputText('password123');

  // 查找并点击提交按钮
  let submitBtn = await driver.find(
    ON.text('提交')
      .type('Button')
      .enabled(true)
  );
  await submitBtn.click();

  // 等待结果
  await driver.wait(ON.text('欢迎'), 5000);

  // 截图
  let screenshotPath = await driver.screenshot();
  console.info(`截图已保存到: ${screenshotPath}`);
}
```

## 数据类型

### Point
```typescript
interface Point {
  x: number;          // 水平坐标
  y: number;          // 垂直坐标
  displayId?: number; // 显示器 ID（API 20+）
}
```

### Rect
```typescript
interface Rect {
  left: number;
  top: number;
  right: number;
  bottom: number;
  displayId?: number;  // API 20+
}
```

### WindowMode (API 9+)
- `FULLSCREEN` (0) - 全屏模式
- `PRIMARY` (1) - 主窗口模式
- `SECONDARY` (2) - 次窗口模式
- `FLOATING` (3) - 浮窗模式

### DisplayRotation (API 9+)
- `ROTATION_0` (0) - 无旋转（竖屏）
- `ROTATION_90` (1) - 顺时针 90°（横屏）
- `ROTATION_180` (2) - 顺时针 180°（反向竖屏）
- `ROTATION_270` (3) - 顺时针 270°（反向横屏）

### UiDirection (API 10+)
- `LEFT` (0), `RIGHT` (1), `UP` (2), `DOWN` (3)

### MouseButton (API 10+)
- `MOUSE_BUTTON_LEFT` (0) - 鼠标左键
- `MOUSE_BUTTON_RIGHT` (1) - 鼠标右键
- `MOUSE_BUTTON_MIDDLE` (2) - 鼠标中键

## 已废弃的类 (API 8)

请改用 API 9+ 类：

| 已废弃（API 8） | 改用（API 9+） |
|-------------------|---------------------|
| `BY` | `ON` |
| `UiComponent` | `Component` |
| `UiDriver` | `Driver` |
