# Expected Output: eval-016

## Key Points (必须包含)

1. **不一样**。ArkTS annotations 不能按 TypeScript decorators 的语义解释。
2. ArkTS annotations 有独立规范，重点是声明、可用位置、元注解和编译期处理。
3. 不能默认认为 ArkTS annotation 会像 TypeScript decorator 一样执行运行时包装、替换或元编程逻辑。
4. 若文档未明确说明某种 decorator 风格行为，应输出边界提示，不应自行推断。
5. 依据：`spec/annotations.md`。

## Anti-Pattern (不得出现)

- “annotation 就是 TS decorator” — 错误
- “可以按 JS 运行时装饰器机制理解” — 错误
- 未引用 `spec/annotations.md`
