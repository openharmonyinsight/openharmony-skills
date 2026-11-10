# ohos-dev-docs-writing-compliance-review 行为评估用例

[evals.json](evals.json) 保留4个可复用用例，包含 prompt、expected_output 和逐项 expectations。输入中的 API、SDK 声明及 schema 是合成夹具，不代表官方 SDK。

## 执行方法

1. 每个用例分别在两个全新会话执行，保持模型、工具权限和输入一致。with skill 提供本技能及必要引用；without skill 仅提供 prompt 和夹具，不提供技能、预期断言或既有结果。
2. PR diff 完整模式提供四个配套文档技能；单独安装时另验降级覆盖说明。其它技能仅按实际引用提供资料。
3. 生成阶段不提供 expectations。另由人工或独立会话按逐项断言判分，记录证据；全部断言满足才算该用例通过。记录实际模型、技能版本、权限和未验证项，不预设技能优于基线。
4. 仅在隔离环境读取夹具，除非用例明确要求且获得授权，不进行远端写操作；不能将合成夹具检查称为真实 SDK 编译或设备验证。

本目录保留用例和方法；运行输出、日志、评分及迁移过程记录不随技能包发布。既有评估报告见 [PR !373 评论区](https://gitcode.com/openharmonyinsight/openharmony-skills/merge_requests/373)。
