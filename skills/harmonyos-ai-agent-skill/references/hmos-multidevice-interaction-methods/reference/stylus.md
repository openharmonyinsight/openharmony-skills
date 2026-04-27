# 手写笔输入指南

## 目录

1. [手写笔概述](#手写笔概述)
2. [手写笔事件](#手写笔事件)
3. [压力感应](#压力感应)
4. [最佳实践](#best-practices)

---

## 手写笔概述

手写笔 (Stylus/Pen) 提供比触摸更精确的输入方式，适用于绘图、笔记等场景。

### 支持设备

| 设备 | 手写笔支持 |
|-----|----------|
| 平板 (MatePad) | ✓ |
| 三折叠 (Mate XTs) | ✓ |
| 手机 | ✗ |
| PC | 外接数位板 |

### 手写笔特点

- **精确输入**: 比手指更精确
- **压力感应**: 检测按压力度
- **悬浮检测**: 检测笔尖悬浮
- **倾斜检测**: 检测笔身倾斜角度
- **按键**: 部分手写笔有物理按键

---

## 手写笔事件

### 基本事件

```typescript
@Entry
@Component
struct StylusEventExample {
  context: CanvasRenderingContext2D | DrawingRenderingContext | undefined;

  build() {
    Column() {
      Canvas(this.context)
        .width('100%')
        .height('100%')
        .onReady(() => {
          // Canvas 准备就绪
        })
        .onTouch((event: TouchEvent) => {
          // 检测是否为手写笔触摸
          if (event.sourceTool === SourceTool.Pen) {
            const touch = event.touches[0];
            console.log(`手写笔位置: x=${touch.x}, y=${touch.y}`);
          }
        })
    }
  }
}
```

### 区分触摸和手写笔

```typescript
.onTouch((event: TouchEvent) => {
  switch (event.sourceTool) {
    case SourceTool.Finger:
      console.log('手指触摸');
      break;
    case SourceTool.Pen:
      console.log('手写笔触摸');
      break;
    case SourceTool.MOUSE:
      console.log('鼠标');
      break;
  }
})
```

### 手写笔事件类型

该类型与手指触摸类型一致

| 事件 | 说明 |
|-----|------|
| TouchType.Down | 手写笔按下 |
| TouchType.Move | 手写笔移动 |
| TouchType.Up | 手写笔抬起 |

---

## 压力感应

### 获取压力值

```typescript
@Entry
@Component
struct PressureExample {
  @State pressure: number | undefined = undefined;
  @State lineWidth: number = 1;
  context: CanvasRenderingContext2D | DrawingRenderingContext | undefined;

  build() {
    Column() {
      Text(`压力: ${this.pressure}`)
      Text(`当前线宽: ${this.lineWidth}`)

      Canvas(this.context)
        .width('100%')
        .height(900)
        .onTouch((event: TouchEvent) => {
          if (event.sourceTool === SourceTool.Pen) {
            const touch = event.touches[0];
            this.pressure = touch.pressure; // 压力值 [0,1)
            console.log(`压力值： ${this.pressure}`)

            // 根据压力调整线宽
            if (this.pressure) {
              this.lineWidth = 1 + this.pressure * 10;
            }
          }
        })
    }
  }
}
```

### 压力应用

```typescript
// 根据压力调整画笔粗细
private drawWithPressure(x: number, y: number, pressure: number) {
  const lineWidth = this.baseLineWidth * (1 + pressure * 2);

  this.context.lineWidth = lineWidth;
  this.context.lineTo(x, y);
  this.context.stroke();
}
```

### 手写笔支持判断

如需开发手写笔特有功能和界面，需要先判断设备是否支持手写笔设备

```typescript
@Entry
@Component
struct HandwriteExample {
  @State penWidth: number = 5;
  @State ballpointPenWidth: number = 3;

  build() {
    Column() {
      if (canIUse('SystemCapability.Stylus.Handwrite')) {
        Text('当前设备支持手写笔')
          .fontSize(16)
          .fontColor('#999999')
      } else {
        Text('当前设备不支持手写笔')
          .fontSize(16)
          .fontColor('#999999')
      }
    }
    .width('100%')
    .height('100%')
    .padding(16)
  }
}
```
---

## 最佳实践

### 1. 区分触摸和手写笔输入

```typescript
.onTouch((event: TouchEvent) => {
  if (event.sourceTool === SourceTool.Pen) {
    // 手写笔模式：精确绘制
    this.drawWithStylus(event);
  } else {
    // 其它模式：其它操作
    this.handleGesture(event);
  }
})
```

### 2. 利用压力感应

```typescript
// 根据压力调整笔触效果
const lineWidth = baseWidth * (1 + touch.force * 2);
const opacity = 0.5 + touch.pressure * 0.5;
```