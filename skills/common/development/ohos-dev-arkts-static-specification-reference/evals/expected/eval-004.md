# Expected Output: eval-004

## Key Points (必须包含)

1. **不能编译通过**。`this.value.length` 访问会失败。
2. 没有显式泛型约束时，`T` 默认 `extends Any`。
3. ArkTS `Any` 没有 methods 或 fields，因此在泛型类体内不能把 `T` 当作有 `length` 字段/属性的类型使用。
4. 这与 TypeScript 的 `any` 直觉不同；不能假设无约束泛型参数可以访问任意属性。
5. **修正方案**：添加能提供 `length` 的显式约束，例如 `extends string`：
   ```typescript
   class Container<T extends string> {
       value: T
       constructor(value: T) { this.value = value }
       getLength(): int { return this.value.length }
   }
   ```
6. 依据：`spec/generics.md` — Type Parameter Constraint；`spec/types.md` — Type Any。

## Anti-Pattern (不得出现)

- "可以调用，因为 T 已经是 string" — 错误，本用例是在泛型类体内访问 `T` 成员
- "和 TypeScript 行为一致" — 错误
- 未解释 Any 的默认约束机制
- 只建议显式写 `new Container<string>`，但不修正类体内 `T` 的约束 — 错误
