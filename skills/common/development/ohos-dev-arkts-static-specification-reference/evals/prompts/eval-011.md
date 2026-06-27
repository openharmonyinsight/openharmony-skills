# Eval 011: 实例方法继承查找优先级

## User Prompt

如果一个 ArkTS 类、它的父类、以及它实现的接口里都有同名实例方法，方法调用时应该按什么优先级查找？当前类、父类、接口谁优先？

## Evaluation Criteria

1. 必须说明当前类成员优先
2. 必须说明父类成员优先于接口成员
3. 必须说明接口成员只在类层级没有合适成员时参与
4. 必须引用 `spec/semantics.md` 和/或 `spec/classes.md`、`spec/interfaces.md`
