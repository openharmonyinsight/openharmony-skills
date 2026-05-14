# Expected Output: eval-001

## Key Points (必须包含)

1. **不同**。ArkTS `Any` 与 TypeScript `any` 是完全不同的概念。
2. ArkTS `Any` 是预定义的 **nullish 类型**，是所有类型的超类型（包括 `void`/`undefined` 和 `null`）。
3. ArkTS `Any` **没有方法和字段**，不能像 TypeScript `any` 那样随意调用任何属性。
4. TypeScript `any` 是类型系统的逃生舱，允许任意操作；ArkTS `Any` 是类型层级顶端，但不提供任何访问能力。
5. 依据：`spec/types.md` — Type Any 和 Nullish Types 章节。

## Anti-Pattern (不得出现)

- "Any 和 any 基本一样" — 错误
- "Any 可以调用任意方法" — 错误
- 未引用依据文件
