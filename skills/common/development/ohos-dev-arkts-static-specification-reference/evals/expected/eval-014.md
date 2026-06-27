# Expected Output: eval-014

## Key Points (必须包含)

1. `main` 是程序入口相关声明，不能简单按普通函数重载来处理。
2. 模块级多个 `main` 会造成入口歧义，应视为 compile-time error 或等价入口冲突诊断。
3. 生成测试用例时不能通过多个 `main` 来覆盖多场景；应拆分文件或在一个 `main` 内调用不同辅助函数。
4. 依据：`spec/modules.md` 或 `spec/semantics.md` 中入口/声明冲突/函数声明相关规则。

## Anti-Pattern (不得出现)

- “main 可以正常重载” — 错误
- “模块级多个 main 没问题” — 错误
- 未说明入口歧义
