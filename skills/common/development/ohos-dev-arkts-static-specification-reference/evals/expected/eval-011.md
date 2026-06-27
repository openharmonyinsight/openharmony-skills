# Expected Output: eval-011

## Key Points (必须包含)

1. 实例方法查找应优先考虑 **当前类** 的成员。
2. 当前类没有合适成员时，再考虑 **父类** 继承成员。
3. 接口成员的优先级低于类层级成员，通常在类和父类没有合适实例方法时才作为候选。
4. 如果存在同名不同签名，还要结合 overload resolution 判断最终可调用签名。
5. 依据：`spec/semantics.md` — method call / overload candidate rules；`spec/classes.md`、`spec/interfaces.md`。

## Anti-Pattern (不得出现)

- “接口优先于当前类方法” — 错误
- “父类和接口顺序无关，随便选” — 错误
- 未说明当前类优先
