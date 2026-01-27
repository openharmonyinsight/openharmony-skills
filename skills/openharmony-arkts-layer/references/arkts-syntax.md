# ArkTS 语法限制

ArkTS 是 TypeScript 的严格子集，以下语法不被支持：

## 对象展开运算符

```typescript
// ❌ 不支持
const newObj = { ...oldObj, key: value }

// ✅ 替代方案
const newObj = Object.assign({}, oldObj, { key: value })
```

## 快速替换

```bash
# 查找：\{\.\.\.(\w+)\}
# 替换为：Object.assign({}, $1)
```

[返回 SKILL.md](../SKILL.md)
