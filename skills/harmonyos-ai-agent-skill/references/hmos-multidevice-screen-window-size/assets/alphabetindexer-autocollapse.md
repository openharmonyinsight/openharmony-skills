# AlphabetIndexer 自动折叠与高度不足挤压案例

## 场景说明

页面右侧使用 `AlphabetIndexer` 作为字母索引导航，配合左侧 `List` 实现联系人快速跳转。

预期行为：

- 高度充足时，索引条完整显示所有字母
- 高度较小时，索引条自动折叠部分字母，保持索引项之间有合理间距

## 正确案例

### 关键代码

```typescript
AlphabetIndexer({ arrayValue: this.alphabets, selected: this.selectedIndex })
  .autoCollapse(true)
  .selected(this.selectedIndex)
  .selectedColor(0xFFFFFF)
  .selectedBackgroundColor(0xCCCCCC)
  .itemSize(20)
  .usingPopup(false)
  .selectedFont({ size: this.getResponsiveConfig().fontSize, weight: FontWeight.Bolder })
  .alignStyle(IndexerAlign.Left)
  .itemBorderRadius(this.getResponsiveConfig().borderRadius)
  .onSelect((index: number) => {
    this.selectedIndex = index;
    this.scroller.scrollToIndex(index);
  })
```

### 正确原因

`.autoCollapse(true)` 允许 `AlphabetIndexer` 在可用高度不足时自动折叠部分索引项。

结果是：

- 高度充足时，索引条完整展示
- 高度较小时，索引条自动折叠低频或非关键索引项
- 索引项之间保持合理间距，视觉上不会拥挤

## 错误案例

### 问题代码

```typescript
AlphabetIndexer({ arrayValue: this.alphabets, selected: this.selectedIndex })
  .autoCollapse(false)
  // ... 其余属性相同
```

### 错误原因

`.autoCollapse(false)` 强制索引条在所有高度下都完整展示所有索引项。

当高度不足时：

- 所有索引项被迫挤在有限空间内
- 索引项间距过小，变得非常紧凑
- 视觉上不美观，且影响触摸操作的准确性

## 最小根因

`AlphabetIndexer` 的 `.autoCollapse(false)` 阻止了索引条在高度不足时自动折叠索引项，导致所有字母挤在有限垂直空间内。

## 直接修复

将：

```typescript
.autoCollapse(false)
```

改为：

```typescript
.autoCollapse(true)
```

## 通用结论

- `AlphabetIndexer` 在可用高度可能不足的场景下，应默认启用 `.autoCollapse(true)`
- 只有在明确保证索引条始终有充足高度的场景下，才考虑使用 `.autoCollapse(false)`
- 当右侧索引条出现挤压、紧凑的问题时，优先检查 `.autoCollapse()` 是否为 `false`
