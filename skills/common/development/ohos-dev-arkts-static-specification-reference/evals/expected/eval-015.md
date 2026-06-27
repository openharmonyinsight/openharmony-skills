# Expected Output: eval-015

## Key Points (必须包含)

1. 不建议也不应在 ArkTS 静态代码中保留 CommonJS `require`。
2. ArkTS 静态模块应使用 ES module 风格的 `import` / `export`。
3. `require(path)` 这种动态路径加载不符合静态模块解析和类型检查要求。
4. 修正示例：
   ```typescript
   import fs from "fs"
   ```
   或根据实际模块导出改为命名导入。
5. 依据：`cookbook/cookbook-recipes.md` — require 迁移规则；`spec/modules.md` — module import/export。

## Anti-Pattern (不得出现)

- “直接保留 require 即可” — 错误
- “动态 require 在静态 ArkTS 中和 TS 一样可用” — 错误
- 未给出 ES module 改写方向
