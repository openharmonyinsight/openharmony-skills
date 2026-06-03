# Expected Output: eval-020

## Key Points (必须包含)

1. 必须输出固定边界提示：
   `⚠️ skill 文档未明确说明，待使用者自行确认`
2. 不应根据 JavaScript/TypeScript 动态属性机制推断 ArkTS 静态规范支持该行为。
3. 应说明 ArkTS 静态类型检查不能默认接受“编译后动态追加字段并静态访问”的文档外能力。
4. 如果需要继续判断，应要求提供对应 spec/cookbook 明确章节或运行时插件规范。

## Anti-Pattern (不得出现)

- “可以，因为 JS 对象能动态加字段” — 错误
- “应该支持，ArkTS 基于 TS” — 错误
- 未输出固定边界提示
