# Expected Output: eval-013

## Key Points (必须包含)

1. 不能把多个 unnamed constructor 当成普通函数随意重复声明。
2. 构造函数重载必须通过参数数量或参数类型形成可区分签名，并接受等价签名检查。
3. constructor 没有普通返回类型，不能通过“返回类型不同”构成重载。
4. 如果多个 constructor 的参数签名等价，应产生 compile-time error。
5. 依据：`spec/classes.md` — constructors；`spec/semantics.md` — overload / equivalent signature。

## Anti-Pattern (不得出现)

- “可以写任意多个无参数 constructor” — 错误
- “constructor 可以靠返回类型重载” — 错误
- 未提等价签名检查
