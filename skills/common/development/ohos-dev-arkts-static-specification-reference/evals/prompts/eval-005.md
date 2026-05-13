# Eval 005: TypeScript enum 迁移到 ArkTS

## User Prompt

我有一段 TypeScript 代码要迁移到 ArkTS：

```typescript
enum Direction {
    Up = "UP",
    Down = "DOWN",
    Left = 1,
    Right = 2
}
```

能直接用吗？有什么要注意的？

## Evaluation Criteria

1. 必须指出 ArkTS enum 基类型只能是 int 或 string，不能混合
2. 必须指出混合初始化器类型会导致 compile-time error
3. 必须给出修正方案（统一基类型）
4. 必须引用 spec/enums.md 和/或 cookbook/cookbook-recipes.md
