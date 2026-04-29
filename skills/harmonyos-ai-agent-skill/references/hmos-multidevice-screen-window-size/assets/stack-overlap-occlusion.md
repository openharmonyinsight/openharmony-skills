# Stack 层叠布局导致组件遮挡案例

## 场景说明

页面包含轮播图和底部通知栏两个区域，预期行为是：
- 轮播图完整显示
- 通知栏显示在轮播图下方

## 正确案例 (goodcase)

### 关键代码

```typescript
build() {
  // Stack (ID=127) → Column 垂直布局，避免遮挡
  Column() {
    // Stack (ID=173) - 轮播图容器
    Stack() {
      Swiper() {
        // ...
      }
      .height(300)
    }
    .height(300)

    // 通知栏
    Stack() {
      // ...
    }
    .height(133)
  }
}
```

### 正确原因

使用 `Column` 垂直布局，子元素按顺序从上到下排列：
- 轮播图占用 0-300 的高度区域
- 通知栏占用 300-433 的高度区域
- 两者互不遮挡

## 错误案例 (badcase)

### 问题代码

```typescript
build() {
  // Stack (ID=127) - 根容器
  Stack({ alignContent: Alignment.BottomStart }) {
    // Stack (ID=173) - 轮播图容器
    Stack() {
      Swiper() {
        // ...
      }
      .height(300)
    }
    .height(300)

    // 通知栏
    Stack() {
      // ...
    }
    .height(133)
  }
}
```

### 错误原因

使用 `Stack` 层叠布局 + `alignContent: Alignment.BottomStart`：
- Stack 的所有子元素默认占用同一块区域（层叠）
- `Alignment.BottomStart` 将通知栏定位在 Stack 底部
- 通知栏高度 133，会覆盖轮播图底部 133 的高度
- 轮播图底部被遮挡，无法完整显示

## 直接修复

将根容器从 `Stack` 改为 `Column`：

```typescript
// 修复前
Stack({ alignContent: Alignment.BottomStart }) {
  // 子元素...
}

// 修复后
Column() {
  // 子元素...
}
```

## 通用结论

- 需要子元素垂直排列、互不遮挡时，使用 `Column`
- 需要子元素层叠显示（如背景图+前景内容）时，使用 `Stack`
- `Stack + Alignment.BottomStart` 常用于底部悬浮场景，但会导致底部内容遮挡下层元素
