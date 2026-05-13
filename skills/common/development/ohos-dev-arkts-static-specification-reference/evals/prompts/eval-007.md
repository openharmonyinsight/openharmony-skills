# Eval 007: FixedArray 与 ResizableArray

## User Prompt

```typescript
let fixed: FixedArray<int> = [1, 2, 3]
let resizable: Array<int> = [4, 5, 6]
fixed = resizable   // 可以吗？
resizable = fixed   // 可以吗？
```

这两种赋值在 ArkTS 中合法吗？

## Evaluation Criteria

1. 必须指出两者不可互赋值（not assignable to each other）
2. 必须说明 FixedArray 无方法
3. 必须引用 spec/types.md
4. 不得说 "数组类型兼容可以互相赋值"
