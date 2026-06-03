# Expected Output: eval-019

## Key Points (必须包含)

1. 两类 cast 不能简单视为完全相同。
2. 字面量 cast 可以按字面量转换/检查规则处理。
3. 对变量、对象引用等非字面量表达式的 cast 可能进入 Runtime Checking 路径。
4. 如果运行时实际类型与目标类型不匹配，可能抛出 `ClassCastError`。
5. 依据：`spec/expressions.md` — Cast Expression / Runtime Checking in Cast Expression。

## Anti-Pattern (不得出现)

- “所有 as 都只是编译期类型声明” — 错误
- “非字面量 cast 一定成功” — 错误
- 混同 ArkTS `as` 与 TypeScript `as`
