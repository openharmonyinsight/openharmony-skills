## 仓颉测试执行（run-cangjie-tests 技能）

**⚠️ 触发关键词：**
运行测试 | HLT/LLT测试 | testsuite | testlist | 测试失败 | 回归测试

**⚠️ 硬规则：必须设置 CANGJIE_HOME 环境变量，否则测试无法运行。**

测试类型：HLT（编译+运行）| LLT（单元测试）| cjcov（覆盖率）| LSP

常用参数：`-j`并行数 | `--timeout`超时 | `-pFAIL`只显失败 | `--retry`重试

详细命令和配置路径，见 `skills/run-cangjie-tests/SKILL.md`
