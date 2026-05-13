# Eval 003: nullish 类型赋值给 Object

## User Prompt

```typescript
function processValue(): Object {
    let s: string | undefined = getValue()
    return s
}
```

这段 ArkTS 代码能编译通过吗？为什么？

## Evaluation Criteria

1. 必须指出这是 compile-time error
2. 必须解释 `string | undefined`（nullish 类型）不兼容 `Object`
3. 必须引用 spec/types.md Nullish Types 章节
4. 必须给出修正方案
