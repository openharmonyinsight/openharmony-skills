# Expected Output: eval-012

## Key Points (必须包含)

1. 不能把 `static` 方法按实例方法继承规则理解。
2. ArkTS 的静态成员访问需要按 class/static member lookup 规则判断，不能用 JavaScript 原型链直觉推断。
3. 如果规范规则要求 static 只看当前类静态成员，则 `Derived.make()` 不能因为 `Base` 有同名 static 方法就自动可用。
4. 更稳妥的访问方式是通过声明该静态成员的类型访问：`Base.make()`；如果子类需要该静态 API，应在 `Derived` 中显式声明/转发。
5. 依据：`spec/classes.md` — static members；`spec/semantics.md` — member lookup。

## Anti-Pattern (不得出现)

- “static 方法一定像实例方法一样继承” — 错误
- “按 JavaScript 原型链解释 ArkTS static” — 错误
- 未引用依据文件
