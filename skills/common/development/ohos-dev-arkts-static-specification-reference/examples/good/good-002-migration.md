# Good Example 002: 正确处理 TS 到 ArkTS 的迁移问题

## User Question

```typescript
enum Status {
    Active = "ACTIVE",
    Inactive = "INACTIVE",
    Pending = 1,
    Archived = 2
}
```

我需要把这段 TypeScript 代码迁移到 ArkTS，能直接用吗？

## Good Answer

不能直接用。这段代码会导致 **compile-time error**。

**原因**：ArkTS enum 的初始化器类型必须统一，基类型只能是 `int` 或 `string`。上面代码混合使用了字符串（`"ACTIVE"`）和数字（`1`）初始化器，类型不统一。

**修正方案**：

```typescript
// 方案 A：统一使用 string 基类型
enum Status {
    Active = "ACTIVE",
    Inactive = "INACTIVE",
    Pending = "PENDING",
    Archived = "ARCHIVED"
}

// 方案 B：统一使用 int 基类型（自动递增）
enum Status {
    Active,      // 0
    Inactive,    // 1
    Pending,     // 2
    Archived     // 3
}
```

依据：`spec/enums.md` — Initialization of Enumeration Members；`cookbook/cookbook-recipes.md`。

## Why This Is Good

- 先给结论（"不能直接用"）
- 解释了违反的具体规则
- 给出两种可选的修正方案
- 引用了规范文件
