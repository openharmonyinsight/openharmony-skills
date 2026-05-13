# Expected Output: eval-004

## Key Points (必须包含)

1. `.length` 调用会失败。因为没有显式泛型约束时，`T` 默认 `extends Any`。
2. ArkTS `Any` 没有 methods 或 fields，因此 `T` 上无法访问 `.length`。
3. 这与 TypeScript 不同：TypeScript 无约束泛型默认 `extends any`，可以调用任意属性。
4. **修正方案**：添加 `extends string` 或 `extends Object` 约束：
   ```typescript
   class Container<T extends string> {
       value: T
       constructor(value: T) { this.value = value }
       getValue(): T { return this.value }
   }
   ```
5. 依据：`spec/generics.md` — Type Parameter Constraint；`spec/types.md` — Type Any。

## Anti-Pattern (不得出现)

- "可以调用，因为 T 是 string" — 错误，未考虑默认约束
- "和 TypeScript 行为一致" — 错误
- 未解释 Any 的默认约束机制
