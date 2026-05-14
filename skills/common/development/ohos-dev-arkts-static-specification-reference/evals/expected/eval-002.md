# Expected Output: eval-002

## Key Points (必须包含)

1. 输出是 **3**，不是 3.5。
2. ArkTS 中 `int` 类型的除法是**整数除法**，会截断小数部分。
3. 这与 TypeScript 不同：TypeScript 中 `7/2=3.5`（浮点除法），但 ArkTS 整数除法 `int(7)/int(2)=3`。
4. ArkTS 有独立数值体系（byte/short/int/long/float/double），除法行为取决于操作数类型。
5. 依据：`spec/expressions.md` — Division 章节。

## Anti-Pattern (不得出现)

- "输出 3.5" — 错误
- "和 TypeScript 一样" — 错误
- 未区分整数除法与浮点除法
