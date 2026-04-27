# 交互归一化指南

## 目录

1. [交互归一化概述](#交互归一化概述)
2. [统一事件处理](#统一事件处理)
3. [触摸与鼠标归一](#触摸与鼠标归一)
4. [上下文菜单归一](#上下文菜单归一)
5. [最佳实践](#最佳实践)

---

## 交互归一化概述

HarmonyOS 提供交互归一化能力，让一套代码同时支持触控、鼠标和键盘操作。

### 核心原则

1. **保证触控屏和键鼠体验一致**
2. **统一处理触摸和鼠标事件**
3. **支持多种输入方式的平滑切换**
4. **提供一致的用户体验**

### 输入设备类型

| 输入类型 | 设备示例 | 特点 |
|---------|---------|------|
| 触摸 | 手机、平板 | 直接操作，手势丰富 |
| 鼠标 | PC、平板外接 | 精确点击，悬浮效果 |
| 键盘 | PC、平板外接 | 快捷操作，焦点导航 |
| 触控板 | 笔记本、平板外接 | 类似鼠标+手势 |
| 手写笔 | 平板、三折叠 | 精确绘制，压力感应 |
| 遥控器 | 智慧屏、车机 | 方向键导航 |
| 手柄 | 智慧屏 PC | 快速操作，组合键 |
| 表冠 | 智能穿戴 | 旋转，按压 |

### 设备输入能力映射

| 设备 | 输入设备 |
| --- | --- |
| 直板机 | 触控屏 |
| 折叠屏 | 触控屏 |
| 阔折叠 | 触控屏 |
| 三折叠 | 触控屏、手写笔 |
| 平板 | 触控屏、鼠标、键盘、手写笔 |
| 电脑 | 触控屏、触控板、鼠标、键盘、手柄 |
| 智慧屏 | 灵犀指向遥控、灵犀悬浮触控、走焦类遥控、键盘、鼠标、手柄 |
| 智能穿戴 | 触控屏、表冠 |

---

## 统一事件处理

### 点击事件归一

```typescript
@Entry
@Component
struct UnifiedClickExample {
  build() {
    // onClick 同时处理触摸点击和鼠标点击
    Button('点击我')
      .onClick((event: ClickEvent) => {
        // event.sourceType 可以判断输入来源
        if (event.source === SourceType.TouchScreen) {
          console.log('触摸点击');
        } else if (event.source === SourceType.Mouse) {
          console.log('鼠标点击');
        }
      })
  }
}
```

### 事件来源类型

SourceType为ClickEvent的系统属性，无需也不可自定义，枚举如下：

```typescript
enum SourceType {
  Unknown = 0,        // 未知设备源
  Mouse = 1,          // 鼠标
  TouchScreen = 2,    // 触摸屏
  KEY = 4,            // 按键
  JOYSTICK = 5        // 手柄
}
```

---

## 触摸与鼠标归一

### 长按与右键归一

触摸的长按手势和鼠标的右键点击可以归一为上下文菜单操作。

```typescript
@Entry
@Component
struct ContextMenuExample {
  @State menuVisible: boolean = false;

  build() {
    Column() {
      Text('长按或右键打开菜单')
        .fontSize(16)
        .padding(16)
        .backgroundColor('#F5F5F5')
        .borderRadius(8)
        .bindContextMenu(this.menuBuilder, ResponseType.RightClick)
        .bindContextMenu(this.menuBuilder, ResponseType.LongPress)
    }
  }

  @Builder
  menuBuilder() {
    Menu() {
      MenuItem({ content: '复制' })
        .onClick(() => console.log('复制'))

      MenuItem({ content: '粘贴' })
        .onClick(() => console.log('粘贴'))

      MenuItem({ content: '删除' })
        .onClick(() => console.log('删除'))
    }
  }
}
```

### 拖拽归一

触摸拖拽和鼠标拖拽使用相同的事件接口。

```typescript
interface Position {
  x: number,
  y: number
}

@Entry
@Component
struct DragExample {
  @State itemPosition: Position = { x: 0, y: 0 };

  build() {
    Row() {
      Column() {
        Text('拖拽我')
      }
      .width(100)
      .height(100)
      .backgroundColor('#007AFF')
      .borderRadius(8)
      .position(this.itemPosition)
      .gesture(
        PanGesture()
          .onActionUpdate((event: GestureEvent) => {
            this.itemPosition.x += event.offsetX;
            this.itemPosition.y += event.offsetY;
          })
      )
    }
    .width('100%')
    .height('100%')
  }
}
```

---

## 上下文菜单归一

### 使用 bindContextMenu

```typescript
@Entry
@Component
struct BindContextMenuExample {
  build() {
    List() {
      ForEach([1, 2, 3], (item: number) => {
        ListItem() {
          Text(`项目 ${item}`)
            .width('100%')
            .height(60)
            .padding(16)
            .backgroundColor(Color.White)
            .borderRadius(8)
            .margin({ bottom: 8 })
        }
        .bindContextMenu(this.itemMenuBuilder, ResponseType.RightClick)
        .bindContextMenu(this.itemMenuBuilder, ResponseType.LongPress)
      })
    }
    .padding(16)
  }

  @Builder
  itemMenuBuilder() {
    Menu() {
      MenuItem({ content: '编辑' })
      MenuItem({ content: '删除' })
      MenuItem({ content: '分享' })
    }
  }
}
```

### ResponseType 选项

| ResponseType | 说明 |
|-------------|------|
| LongPress | 长按触发 |
| RightClick | 右键触发 |
| LongPress \| RightClick | 两者都支持 |

---

## 手势功能实现-响应手势事件

```typescript
@Entry
@Component
struct PinchGridSample {
  @State videoGridColumn: string = '1fr 1fr 1fr';

  build() {
    Grid() {
      ForEach([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], (n: number) => {
        GridItem() {
          Row() { Text(`${n}`) }
          .height(72)
          .width(40)
          .justifyContent(FlexAlign.Center)
          .alignItems(VerticalAlign.Center)
          .backgroundColor('#19000000')
        }
      }, (n: number) => n.toString())
    }
    .columnsTemplate(this.videoGridColumn)
    .gesture(PinchGesture({ fingers: 2 }).onActionUpdate((event: GestureEvent) => {
      this.videoGridColumn = event.scale > 1 ? '1fr 1fr 1fr 1fr' : '1fr 1fr 1fr';
    }))
  }
}
```

## 拖拽功能实现-响应拖拽事件
```typescript
import { uniformTypeDescriptor } from '@kit.ArkData';

@Entry
@Component
struct DragDropSample {
  @State targetText: string = 'Drop Here';

  build() {
    Row({ space: 24 }) {
      Text('Drag Source')
        .width(120)
        .height(60)
        .backgroundColor('#19000000')
        .textAlign(TextAlign.Center)
        .onDragStart(() => ({ builder: () => Text('Dragging') }))

      Text(this.targetText)
        .width(160)
        .height(80)
        .backgroundColor('#11000000')
        .textAlign(TextAlign.Center)
        .allowDrop([uniformTypeDescriptor.UniformDataType.TEXT])
        .onDragEnter(() => this.targetText = 'Entered')
        .onDragLeave(() => this.targetText = 'Left')
        .onDrop(() => this.targetText = 'Dropped')
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(VerticalAlign.Center)
  }
}
```
---

## 最佳实践

### 1. 使用统一接口

```typescript
// 使用 onClick 统一处理，鼠标左键点击建议归一到onClick事件中，不要分别处理触摸点击和鼠标左键点击
Button('按钮')
  .onClick(() => {
    // 同时支持触摸和鼠标
  })

// 鼠标右键点击使用onMouse
Button('按钮')
  .onClick(() => { /* 触摸点击&鼠标左键点击 */ })
  .onMouse((event) => {
    if (event.button === MouseButton.Right) { /* 鼠标右键点击 */ }
  })
```

### 2. 添加鼠标悬浮效果

```typescript
// 为可交互组件添加悬浮效果
Button('按钮')
  .hoverEffect(HoverEffect.Highlight)
```

### 3. 支持键盘操作

```typescript
Button('确认')
  .onClick(() => this.confirm())
  .onKeyEvent((event: KeyEvent) => {
    if (event.keyCode === KeyCode.KEYCODE_ENTER) {
      this.confirm();
    }
  })
```

### 4. 检测输入来源

```typescript
.onClick((event: ClickEvent) => {
  switch (event.sourceType) {
    case SourceType.TouchScreen:
      // 触摸操作，提供触觉反馈
      break;
    case SourceType.Mouse:
      // 鼠标操作，可能不需要触觉反馈
      break;
  }
})
```

### 5. 响应式交互设计

```typescript
@State isPointerDevice: boolean = false;

aboutToAppear() {
  // 检测是否有精确指针设备
  this.isPointerDevice = this.hasPointerDevice();
}

build() {
  Column() {
    if (this.isPointerDevice) {
      // 有鼠标时显示悬停效果
      Text('悬停效果')
        .hoverEffect(HoverEffect.Highlight)
    }
  }
}
```
