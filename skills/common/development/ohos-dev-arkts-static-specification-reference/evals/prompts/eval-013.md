# Eval 013: 构造函数重载与 unnamed constructor

## User Prompt

ArkTS 类里可以写多个 unnamed constructor 吗？构造函数重载和普通方法重载有什么限制？

## Evaluation Criteria

1. 必须说明 constructor/unnamed constructor 不能无限制重复声明
2. 必须说明构造函数重载需要满足签名区分和等价签名检查
3. 必须指出只返回类型不同对 constructor 无意义
4. 必须引用 `spec/classes.md` 和/或 `spec/semantics.md`
