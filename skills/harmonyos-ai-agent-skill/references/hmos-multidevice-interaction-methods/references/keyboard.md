# 键盘适配指南

## 目录

1. [焦点导航](#焦点导航)
2. [键盘快捷键](#键盘快捷键)
3. [最佳实践](#最佳实践)

---

## 焦点导航

焦点导航是使用键盘、智慧屏遥控器或或表冠等非指向性输入设备与应用程序进行间接交互的关键机制。

### Tab导航

#### 基本Tab导航

```typescript
@Entry
@Component
struct TabNavExample {
  build() {
    Column() {
      // 按 tabIndex 顺序导航
      TextInput({ placeholder: '姓名' })
        .tabIndex(1)

      TextInput({ placeholder: '邮箱' })
        .tabIndex(2)

      Row() {
        Button('取消')
          .tabIndex(4)

        Button('提交')
          .tabIndex(3)
      }
    }
  }
}
```

#### tabIndex 规则

- **正数**: 按 1, 2, 3... 顺序导航
- **0**: 默认值，按DOM顺序
- **-1**: 可通过程序获焦，但不在Tab序列中

#### 焦点属性

```typescript
// 可获焦
.focusable(true)

// Tab顺序
.tabIndex(1)

// 默认焦点（页面加载时）
.defaultFocus(true)

// 组内默认焦点
.groupDefaultFocus(true)

// Tab键是否停留
.tabStop(true)
```
---

### 方向键导航

#### 使用 nextFocus

```typescript
@Entry
@Component
struct ArrowNavExample {
  build() {
    Column() {
      Row() {
        Button('左上')
          .id('topLeft')
          .nextFocus({ right: 'topRight', down: 'bottomLeft' })

        Button('右上')
          .id('topRight')
          .nextFocus({ left: 'topLeft', down: 'bottomRight' })
      }

      Row() {
        Button('左下')
          .id('bottomLeft')
          .nextFocus({ up: 'topLeft', right: 'bottomRight' })

        Button('右下')
          .id('bottomRight')
          .nextFocus({ up: 'topRight', left: 'bottomLeft' })
      }
    }
  }
}
```

#### nextFocus 参数

| 参数 | 值 | 说明 |
|-----|---|------|
| forward | 组件id | tab键走焦目标 |
| backward | 组件id | shift+tab键走焦目标 |
| up | 组件id | 方向键上键走焦目标 |
| down | 组件id | 方向键下键走焦目标 |
| left | 组件id | 方向键左键走焦目标 |
| right | 组件id | 方向键右键走焦目标 |


#### 网格导航示例

```typescript
@Entry
@Component
struct GridNavExample {
  private items: string[] = [];

  aboutToAppear() {
    for (let i = 0; i < 9; i++) {
      this.items.push(`项目${i + 1}`);
    }
  }

  build() {
    Grid() {
      ForEach(this.items, (item: string, index: number) => {
        GridItem() {
          Text(item)
            .width('100%')
            .height('100%')
            .textAlign(TextAlign.Center)
            .id(`item_${index + 1}`)
            .backgroundColor(Color.Blue)
            .focusable(true)
            .nextFocus({
              forward: `item_${(index + 2) % 9}`,
              backward: `item_${(index) % 9}`,
              up: `item_${(index - 2) % 9}`,
              down: `item_${(index + 4) % 9}`,
              left: `item_${index % 9}`,
              right: `item_${(index + 2) % 9}`
            })
        }
      })
    }
    .columnsTemplate('1fr 1fr 1fr')
    .rowsTemplate('1fr 1fr 1fr')
    .width(300)
    .height(300)
  }
}
```

---

### 焦点样式

#### 焦点事件

```typescript
@Entry
@Component
struct FocusEventsExample {
  @State isFocused: boolean = false;

  build() {
    Column() {
      Text(this.isFocused ? '已获焦' : '未获焦')
        .focusable(true)
        .onFocus(() => {
          this.isFocused = true;
          console.log('获焦');
        })
        .onBlur(() => {
          this.isFocused = false;
          console.log('失焦');
        })

      Text('其他焦点组件')
        .focusable(true)
    }
    .width(200)
    .height(100)
    .backgroundColor(this.isFocused ? '#E3F2FD' : '#F5F5F5')
    .border({
      width: this.isFocused ? 2 : 1,
      color: this.isFocused ? '#007AFF' : '#E8E8E8'
    })
  }
}
```

#### 焦点样式最佳实践

```typescript
@Entry
@Component
struct FocusableCard {
  @State isFocused: boolean = false;

  build() {
    Column() {
      Text('卡片内容')
        .focusable(true)
        .border(this.isFocused ? { width: 2, color: '#007AFF' } : { width: 1, color: '#E8E8E8' })
        .shadow(this.isFocused ? { radius: 4, color: '#007AFF33', offsetX: 0, offsetY: 0 } : { radius: 0 })
        .onFocus(() => this.isFocused = true)
        .onBlur(() => this.isFocused = false)

      Text('其它焦点组件')
        .focusable(true)
    }
    .width(200)
    .height(100)
    
  }
}
```

---

## 键盘快捷键

### 常用快捷键示例

```typescript
import { KeyCode } from '@kit.InputKit';

@Entry
@Component
struct ShortcutsExample {
  @State text: string = '';


  build() {
    Column() {
      Text(this.text)
        .fontSize(24)

      TextInput({ placeholder: '输入' })
    }
    .width('100%')
    .height('100%')
    .onKeyEvent((event: KeyEvent) => {
      if (event.type === KeyType.Down) {
        // Ctrl + S 保存
        if (event.keyCode === KeyCode.KEYCODE_S) {
          try {
            const hasCtrl = event?.getModifierKeyState?.(['Ctrl']);
            if (hasCtrl) {
              this.save();
              event.stopPropagation();
            }
          } catch (error) {
            // TODO: Implement error handling.
          }
        }

        // Escape 取消
        if (event.keyCode === KeyCode.KEYCODE_ESCAPE) {
          this.cancel();
          event.stopPropagation();
        }

        // Enter 确认
        if (event.keyCode === KeyCode.KEYCODE_ENTER) {
          this.confirm();
          event.stopPropagation();
        }
      }
    })
  }

  save() {
    console.log('保存');
  }

  cancel() {
    console.log('取消');
  }

  confirm() {
    console.log('确认');
  }
}
```

### 键盘输入最佳实践

对于需要稳定支持键盘输入的页面，不要只依赖 `event.keyText` 或单一路径。推荐统一按以下顺序处理：

1. 功能键优先走固定 `keyCode`
   - 如 `Enter`、`Esc`、`Del`
2. 再处理 `keyText`
   - 适合直接字符输入，如 `+`、`*`、`.`、`/`
3. 再处理组合键回退
   - 如 US 键盘上的 `Shift + 8 -> *`、`Shift + = -> +`
4. 最后处理主键盘数字和小键盘数字
   - 如 `KEYCODE_0-9`、`KEYCODE_NUMPAD_0-9`

`KeyEvent` 通过getModifierKeyState查看 'Ctrl' | 'Alt' | 'Shift'的按压状态，从而判断组合键，注意当前只能监听这三个键的按压。

```typescript
const hasAlt = event?.getModifierKeyState?.(['Alt']);
```

### 常用键码

| 键码 | 说明 |
|-----|------|
| KEYCODE_SPACE | 空格 |
| KEYCODE_ENTER | 回车 |
| KEYCODE_ESCAPE | ESC |
| KEYCODE_TAB | Tab |
| KEYCODE_BACK | 返回 |
| KEYCODE_DEL | 删除 |
| KEYCODE_CTRL_LEFT/RIGHT | Ctrl |
| KEYCODE_SHIFT_LEFT/RIGHT | Shift |
| KEYCODE_ALT_LEFT/RIGHT | Alt |
| KEYCODE_DPAD_UP/DOWN/LEFT/RIGHT | 方向键 |

---

## 最佳实践

### 1. 设置默认焦点

```typescript
Column() {
  TextInput()
    .defaultFocus(true) // 页面加载时自动获焦
}
```

### 2. 确保焦点可见

```typescript
// 焦点样式要足够明显
.onFocus(() => {
  this.isFocused = true;
})
.border({ width: this.isFocused ? 2 : 1, color: this.isFocused ? '#007AFF' : '#E8E8E8' })
```

### 3. 合理设置 tabIndex

```typescript
// 按照视觉阅读顺序设置
TextInput().tabIndex(1)
TextInput().tabIndex(2)
Button().tabIndex(3)
```

### 4. 处理焦点循环

```typescript
// 最后一个元素按Tab跳到第一个
Button('最后一个')
  .tabIndex(3)
  .nextFocus({ forward: 'first' })

Button('第一个')
  .id('first')
  .tabIndex(1)
```

### 5. 跳过不可用元素

```typescript
Button('禁用按钮')
  .enabled(false)
  .focusable(false) // 禁用时不可获焦
```

### 6. 提供键盘快捷键

```typescript
// 常用快捷键
Ctrl+S  保存
Ctrl+C  复制
Ctrl+V  粘贴
Ctrl+Z  撤销
Escape  取消/关闭
Enter   确认/提交
```

### 7. 消费按键事件

```typescript
.onKeyEvent((event: KeyEvent) => {
  if (event.type === KeyType.Down && event.keyCode === KeyCode.KEYCODE_ENTER) {
    this.confirm();
    return true; // 消费事件，阻止冒泡
  }
  return false;
})
```