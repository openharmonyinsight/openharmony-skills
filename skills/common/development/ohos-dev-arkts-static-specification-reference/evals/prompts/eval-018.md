# Eval 018: nullish 联合类型成员访问

## User Prompt

```typescript
function printLength(s: string | undefined): void {
    console.log(s.length)
}
```

这段代码在 ArkTS 静态类型检查下可以直接访问 `s.length` 吗？为什么？

## Evaluation Criteria

1. 必须指出不能直接访问
2. 必须说明 `s` 可能是 `undefined`，访问成员前需要类型收窄
3. 必须给出修正方案
4. 必须引用 `spec/types.md` 和/或 `spec/semantics.md`
