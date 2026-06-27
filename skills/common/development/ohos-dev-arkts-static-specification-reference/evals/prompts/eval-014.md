# Eval 014: main 函数限制

## User Prompt

在一个 ArkTS 模块里，我能不能写多个 `main` 函数做重载？如果模块级出现多个 `main`，应该怎么判断？

## Evaluation Criteria

1. 必须说明 `main` 入口函数不能按普通函数重载处理
2. 必须指出模块级多个 `main` 应触发 compile-time error 或入口冲突诊断
3. 必须说明不能为了测试方便重复声明多个 main
4. 必须引用 `spec/modules.md`、`spec/semantics.md` 或相关入口规则文件
