# Expected Output: eval-009

## Key Points (必须包含)

1. **不能构成合法重载**。只返回类型不同、参数列表相同的函数不是有效重载。
2. 这两个 `parse(x: string)` 的可调用签名等价，应视为冲突并产生 compile-time error。
3. 重载选择主要依据调用参数，不能依赖返回类型来消除这种歧义。
4. 修正方案：改名，或让参数类型/参数数量不同。
5. 依据：`spec/semantics.md` — overload signature / equivalent signature 相关规则。

## Anti-Pattern (不得出现)

- “返回类型不同就可以重载” — 错误
- “根据赋值目标类型自动选择返回类型” — 错误
- 未说明这是 compile-time error
