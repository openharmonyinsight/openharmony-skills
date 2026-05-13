# Bad Example 001: 混淆 ArkTS Any 与 TypeScript any

## User Question

ArkTS 中 `Any` 类型和 TypeScript 的 `any` 有什么区别？

## Bad Answer

ArkTS 的 `Any` 和 TypeScript 的 `any` 基本是一样的，都是表示任意类型。你可以用 `Any` 来代替 TypeScript 中的 `any`，功能上没有太大差别。

```typescript
let x: Any = "hello"
x.toUpperCase()  // 应该能用
```

## Why This Is Bad

1. **核心错误**：将 ArkTS `Any` 等同于 TypeScript `any`。实际上 `Any` 是 nullish 类型，没有方法和字段。
2. **`x.toUpperCase()` 会 compile-time error**：`Any` 不提供任何属性访问。
3. **违反 NEVER 规则**："NEVER 将 ArkTS `Any` 与 TypeScript `any` 混淆"。
4. **未引用依据文件**。
5. **按 TypeScript 习惯补全 ArkTS 语义**，违反 Skill Rules 第 2 条。

## Correct Version

参见 `examples/good/good-001-type-inference.md`。
