# Expected Output: eval-018

## Key Points (必须包含)

1. 不能直接访问 `s.length`，因为 `s` 的类型是 `string | undefined`。
2. `undefined` 没有 `length` 成员，访问前必须通过判空或控制流收窄为 `string`。
3. 修正示例：
   ```typescript
   function printLength(s: string | undefined): void {
       if (s !== undefined) {
           console.log(s.length)
       }
   }
   ```
4. 依据：`spec/types.md` — Nullish Types；`spec/semantics.md` — type checking / assignability / member access。

## Anti-Pattern (不得出现)

- “可以直接访问，undefined 会自动跳过” — 错误
- “ArkTS 会把 undefined 当成空字符串” — 错误
- 未给出类型收窄方案
