# 行为评估

`evals.json` 包含可直接复现的输入及逐项预期，覆盖正例、反例和缺少条件的边界。输入中的 API/schema 是合成夹具，不是官方 SDK 声明。

## 执行方法

对每个用例建立两个全新、互不共享对话的运行环境，模型、工具权限、输入和运行配置保持一致：

1. `with_skill`：提供本技能及可发现的必要引用。文档 PR 技能的完整组合运行同时提供四个配套检视技能；额外检查仅安装 PR 技能时的降级行为，并记录实际安装集合。
2. `without_skill`：只提供原始任务及夹具，不提供本技能、预期断言、迁移说明或此前运行结果；不在当前已读取技能的上下文中模拟基线。
3. 测试只允许读取给出的夹具和在隔离临时目录操作。Git 工作流用例明确只要方案/草稿，不应连接真实远端进行写操作。
4. 保存原始输出、工具动作、模型/配置、技能版本、耗时和运行限制，再按每条 expectations 人工或独立判分（通过/失败及证据）。一个用例的全部断言满足才算通过。
5. 分别汇总全部用例结果和通过率，对比关键差异；不能预设 with skill 一定优于 baseline。with skill 未全通过须修订并重新运行受影响用例。

设计质量另按仓库要求运行 skills-judge，保存真实工具版本、评分和证据，达到 B 或以上才满足该项准入条件。结构校验不能替代行为评估或正式评分。

本轮已完成评分及独立配对评估，汇总见 [评估报告](report.md)，机器可读结果见 [report.json](report.json)，设计证据见 [skills-judge.json](skills-judge.json)。原始输入、输出、工具事件、匿名判分及首轮失败记录均在 results/；与基线持平时不宣称已证明增益。

## 来源与复核

评分规则的固定版本、来源链接及 SHA-256 见 [skills-judge.json](skills-judge.json) 的 rubric 字段。原始评分输入包含该规则的副本，对应 [MIT 许可证](results/skill-judge-LICENSE.txt) 随结果保留。

复核时根据各条件 metadata.json 的 provided_skills 准备独立资料目录，仅复制对应 SKILL.md 和 references，按 input.txt 在全新会话执行；不得将预期断言或其它条件输出交给生成会话。生成会话的 CLI 参数、session ID、资料哈希和工具事件均已记录。判分规则、随机标签映射及原始结果保留在 results/behavior-grader/；首次低分及修订证据见 results/initial-evaluation.json。
