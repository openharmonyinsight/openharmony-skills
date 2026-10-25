# ohos-test-docs-pr-diff-review 评估结果

设计评分：**100/120，B 级**。详细证据见 [skills-judge.json](skills-judge.json)。

with skill：**4/4**；without skill：**4/4**。

| 用例 | with skill | without skill | 原始输出 |
|---|---|---|---|
| 0：multi-hunk | 通过 | 通过 | [with](results/with_skill/case-0/output.md) / [without](results/without_skill/case-0/output.md) |
| 1：deletion | 通过 | 通过 | [with](results/with_skill/case-1/output.md) / [without](results/without_skill/case-1/output.md) |
| 2：missing-patch | 通过 | 通过 | [with](results/with_skill/case-2/output.md) / [without](results/without_skill/case-2/output.md) |
| 3：rename-json5 | 通过 | 通过 | [with](results/with_skill/case-3/output.md) / [without](results/without_skill/case-3/output.md) |

## 逐条差异


两组在本组核心用例通过数上持平，不能据此宣称缺陷发现能力获得提升。

## 运行边界

每个用例/条件均为全新 CLI 对话；预期断言未提供给生成会话。判分由另一个会话对随机 A/B 标签逐条完成，映射及原始评分输出保留在 results/。

仅评估合成输入与只读行为，每个条件运行一次；没有执行真实 SDK 编译、设备操作或远端写操作。使用同一 CLI 默认配置但未显式锁定模型版本。设计评分、行为判分均为模型评估，最终准入由维护者审核。

完整断言、证据、工具动作与限制见 [report.json](report.json)，评估步骤见 [README.md](README.md)。

## 补充验证

- standalone_pr_fallback：passed，见 [results/standalone-case-3](results/standalone-case-3)。不计入配对用例总数。

## release 目录适配

上述模型结果来自迁移前同名技能。迁入 release 仅改变目录、治理元数据及展示资料；触发描述、执行正文和参考规则逐字节相同，未重跑模型评估。原会话哈希保留为历史证据，等价性及新入口哈希见 [release-packaging.json](release-packaging.json)。


## Review 分类调整

当前技能为 `ohos-dev-docs-pr-diff-review`，位于 `skills/common/development/`。本文既有结果及 release-packaging.json 描述迁移前版本；历史名称、会话、哈希和断言原样保留。此次仅调整分类、名称及配套引用，未重跑模型评估，映射与新哈希见 [review-migration.json](review-migration.json)。
