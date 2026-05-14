# Eval 002: ArkTS 整数除法行为

## User Prompt

```typescript
let a: int = 7
let b: int = 2
let result = a / b
console.log(result)
```

上面这段 ArkTS 代码会输出什么？是 3.5 还是 3？

## Evaluation Criteria

1. 必须明确输出是 3（整数除法，截断小数部分）
2. 必须指出 ArkTS 有独立数值体系，整数除法与 TypeScript 的浮点除法不同
3. 必须引用 spec/expressions.md
4. 不得将 TypeScript 的 `7/2=3.5` 推广到 ArkTS
