# Bad Example 002: 错误推广 TypeScript 除法语义

## User Question

```typescript
let a: int = 7
let b: int = 2
let result = a / b
```

输出什么？

## Bad Answer

输出 3.5。因为 ArkTS 是基于 TypeScript 的，除法行为和 TypeScript 一样，都是浮点数除法。

## Why This Is Bad

1. **核心错误**：输出是 3，不是 3.5。ArkTS `int` 类型的除法是整数除法。
2. **违反 NEVER 规则**："NEVER 将 TS 的 `1/2 = 0.5` 推广到 ArkTS"。
3. **按 TypeScript 习惯补全**，违反 Rules 第 2 条。
4. **未引用依据文件**。

## Correct Version

参见 `evals/expected/eval-002.md`。
