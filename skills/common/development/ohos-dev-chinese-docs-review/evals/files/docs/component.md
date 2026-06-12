# MyComponent

MyComponent 是一个自定义 UI 组件，用于展示数据列表。

## 使用说明

```typescript
MyComponent({
  data: items,
  onSelected: (index) => {
    console.log(`选中项：${index}`);
  }
})
```

## 属性

| 名称 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| data | Array\<any\> | 是 | 待展示的数据数组 |
| onSelected | function | 否 | 选中项时的回调函数 |

## 事件

| 名称 | 说明 |
| ---- | ---- |
| onSelect | 选中某项时触发 |

## 示例

### 基础用法

```typescript
MyComponent({
  data: [1, 2, 3],
  onSelected: handleSelection
})
```

### 高级配置

```typescript
MyComponent({
  data: largeDataset,
  onSelected: (idx) => processItem(idx),
  pageSize: 20
})
```
