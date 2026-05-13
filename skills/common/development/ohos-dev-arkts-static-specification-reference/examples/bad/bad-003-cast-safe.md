# Bad Example 003: 错误声称 as cast 一定成功

## User Question

```typescript
class Animal {}
class Dog extends Animal { bark(): void {} }
let pet: Animal = new Cat()
let dog: Dog = pet as Dog
```

这段代码安全吗？

## Bad Answer

安全。`as` 只是类型断言，告诉编译器这个值的类型，不会做运行时检查，和 TypeScript 的 `as` 一样。代码能正常运行。

## Why This Is Bad

1. **核心错误**：ArkTS 的 `as` cast 对非字面量走 Runtime Checking 路径，类型不匹配时抛出 `ClassCastError`。
2. **违反 NEVER 规则**："NEVER 假设 `as` cast 一定成功"。
3. **将 ArkTS `as` 与 TypeScript `as` 等同**。
4. **未引用依据文件**。

## Correct Version

参见 `examples/good/good-003-cast-runtime.md`。
