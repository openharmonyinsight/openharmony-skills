# Expected Output: eval-006

## Key Points (必须包含)

1. **不一定成功**。`as` cast 在 ArkTS 中不是纯类型声明，非字面量 cast 会走 **Runtime Checking** 路径。
2. 运行时 `pet` 实际是 `Cat` 实例，转换为 `Dog` 时类型不匹配，会抛出 **`ClassCastError`**。
3. 这与 TypeScript 的 `as` 行为完全不同：TypeScript 的 `as` 是纯编译期类型断言，不做运行时检查。
4. 安全做法是使用 `instanceof` 先检查，或用 try-catch 包裹：
   ```typescript
   if (pet instanceof Dog) {
       let dog: Dog = pet as Dog
       dog.bark()
   }
   ```
5. 依据：`spec/expressions.md` — Cast Expression 和 Runtime Checking in Cast Expression 章节。

## Anti-Pattern (不得出现)

- "as 只是告诉编译器类型，不影响运行时" — 错误
- "这段代码一定能运行" — 错误
- 将 ArkTS `as` 与 TypeScript `as` 等同
