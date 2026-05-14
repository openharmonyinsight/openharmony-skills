# Expected Output: eval-003

## Key Points (必须包含)

1. **不能编译通过**，这是 compile-time error。
2. `string | undefined` 是 nullish 类型，nullish 类型**不兼容 `Object`**。
3. `Object` 的子类型不包括 `undefined` 和 `null`，因此 nullish 联合类型不能赋值给 `Object`。
4. 依据：`spec/types.md` — Nullish Types 章节；`spec/types.md` — Type Object 章节。
5. **修正方案**：将返回类型改为 `string | undefined`，或在赋值前做 null 检查：
   ```typescript
   function processValue(): string | undefined {
       let s: string | undefined = getValue()
       return s
   }
   ```

## Anti-Pattern (不得出现)

- "可以编译通过" — 错误
- "undefined 可以自动转为 Object" — 错误
- 未给出修正方案
