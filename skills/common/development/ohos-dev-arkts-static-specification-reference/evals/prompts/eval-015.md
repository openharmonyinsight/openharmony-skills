# Eval 015: require 迁移

## User Prompt

TypeScript 里有这样的代码：

```typescript
const fs = require("fs")
const mod = require(path)
```

迁移到 ArkTS 静态语言时可以保留 `require` 吗？应该怎么改？

## Evaluation Criteria

1. 必须指出 ArkTS 静态代码不应使用 CommonJS `require`
2. 必须建议使用 ES module `import`
3. 必须说明动态路径 require 不符合静态模块解析
4. 必须引用 `cookbook/cookbook-recipes.md` 和/或 `spec/modules.md`
