# Eval 019: 字面量 cast 与非字面量 cast

## User Prompt

ArkTS 中下面两类 cast 行为一样吗？

```typescript
let a: int = 1 as int

let x: Object = getObject()
let s: string = x as string
```

字面量 cast 和变量/对象 cast 都只是在编译期改类型吗？

## Evaluation Criteria

1. 必须区分字面量 cast 和非字面量 cast
2. 必须说明非字面量 cast 可能走 Runtime Checking
3. 必须说明类型不匹配可能抛 `ClassCastError`
4. 必须引用 `spec/expressions.md`
