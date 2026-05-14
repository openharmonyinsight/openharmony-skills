# Expected Output: eval-005

## Key Points (必须包含)

1. **不能直接用**，会导致 compile-time error。
2. ArkTS enum 的基类型只能是 `int` 或 `string`，**不能混合不同类型的初始化器**。
3. 上面代码中 `Up`/`Down` 用字符串初始化，`Left`/`Right` 用数字初始化，类型混合不合法。
4. **修正方案**：统一使用同一基类型：
   ```typescript
   // 方案 A：全部使用 string
   enum Direction {
       Up = "UP",
       Down = "DOWN",
       Left = "LEFT",
       Right = "RIGHT"
   }

   // 方案 B：全部使用 int（自动递增）
   enum Direction {
       Up,      // 0
       Down,    // 1
       Left,    // 2
       Right    // 3
   }
   ```
5. 依据：`spec/enums.md` — Initialization of Enumeration Members；`cookbook/cookbook-recipes.md` — enum 迁移规则。

## Anti-Pattern (不得出现)

- "可以直接用" — 错误
- "enum 底层是 number，所以混用没问题" — 错误，ArkTS enum 基类型是 int
- 未给出修正方案
