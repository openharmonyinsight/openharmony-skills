# Expected Output: eval-010

## Key Points (必须包含)

1. 接口继承方法集合不能无序合并。当前接口 `Child` 自己声明的 `run(x: int)` 应优先进入候选集合。
2. 父接口成员在当前接口成员之后参与；多个父接口按 `extends ParentA, ParentB` 的文本顺序参与。
3. 如果当前接口或父接口链上出现同名等价签名，需要按规范做去重或冲突检查，不能重复加入成两个不可区分候选。
4. 如果同名但参数签名不同，则可形成可区分的方法集合，后续调用还要按 method call / overload resolution 规则选择。
5. 依据：`spec/interfaces.md` — interface inheritance / members；`spec/semantics.md` — method candidate / overload resolution。

## Anti-Pattern (不得出现)

- “父接口方法一定优先于当前接口方法” — 错误
- “多个父接口顺序无关” — 错误
- “同名等价签名可以重复保留为多个候选” — 错误
