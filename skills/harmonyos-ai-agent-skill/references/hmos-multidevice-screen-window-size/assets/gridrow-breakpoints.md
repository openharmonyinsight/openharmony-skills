# GridRow 组件宽度断点与窗口宽度断点对照案例

## 场景说明

场景是一个可拖拽缩窄的局部面板，内部使用 `GridRow` 展示图标栅格。预期行为是：

- 宽度较大时，每行显示 8 个图标
- 宽度变小时，每行自动切换为 4 个图标

## 正确案例

### 关键代码

```typescript
GridRow({
  columns: { xs: 12, sm: 12, md: 12, lg: 24 },
  gutter: { x: 0, y: 0 },
  breakpoints: { reference: BreakpointsReference.ComponentSize }
}) {
  GridCol({ span: { xs: 3, sm: 3, md: 3, lg: 3 } }) {
    ItemView()
  }
}
```

### 正确原因

这里使用 `BreakpointsReference.ComponentSize`，断点依据是当前组件自身宽度。

因此当局部面板宽度缩小时，`GridRow` 会跟随组件宽度切换断点：

- `lg: 24` 且 `span: 3`，每行 8 个
- `xs: 12` 且 `span: 3`，每行 4 个

## 错误案例

### 问题代码

```typescript
GridRow({
  columns: { xs: 12, sm: 12, md: 12, lg: 24 },
  gutter: { x: 0, y: 0 },
  breakpoints: { reference: BreakpointsReference.WindowSize }
}) {
  GridCol({ span: { xs: 3, sm: 3, md: 3, lg: 3 } }) {
    ItemView()
  }
}
```

### 错误原因

这里使用 `BreakpointsReference.WindowSize`，断点依据是应用窗口宽度。

但在这个场景里，变化的是局部面板宽度，不是窗口宽度，所以：

- 断点不会切换
- 每行列数不会减少
- 面板变窄后仍保持 8 列
- 子项内容会被挤压、重叠或堆叠

## 直接修复

将：

```typescript
breakpoints: { reference: BreakpointsReference.WindowSize }
```

改为：

```typescript
breakpoints: { reference: BreakpointsReference.ComponentSize }
```

## 通用结论

- 页面整体随窗口变化时，用 `BreakpointsReference.WindowSize`
- 局部容器随自身尺寸变化时，用 `BreakpointsReference.ComponentSize`
