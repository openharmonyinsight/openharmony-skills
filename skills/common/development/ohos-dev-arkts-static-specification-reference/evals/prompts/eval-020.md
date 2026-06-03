# Eval 020: 规范未明确说明的边界

## User Prompt

ArkTS 静态规范有没有说明：某个自定义运行时插件可以在编译后动态给任意类追加字段，并且这些字段能通过静态类型检查直接访问？

请直接按 skill 文档回答，不要猜。

## Evaluation Criteria

1. 如果 skill 文档没有明确规则，必须输出固定边界提示
2. 不得根据 TypeScript 或 JavaScript 动态对象经验补全规则
3. 必须说明不能把文档外行为当成 ArkTS 规范
4. 必须符合 `SKILL.md` 的边界回答要求
