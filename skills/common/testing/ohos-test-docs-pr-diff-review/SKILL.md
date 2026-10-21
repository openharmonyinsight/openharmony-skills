---
name: ohos-test-docs-pr-diff-review
description: 在用户要求仅评审 OpenHarmony/HarmonyOS 文档 PR 的改动点、diff 或补丁时使用。接收 GitCode/GitHub PR、本地提交范围或 unified diff，排除未改动行的既有问题。
metadata:
  author: openharmony
  source: SkillCreateBykingqaquuu/skills/hdq-pr-diff
  source-revision: e4061b33471a45c181778e8272396ba9d028781a
  scope: common
  stage: testing
  domain: docs
  capability: pr-diff-review
  version: 0.1.0
  status: draft
  original-author: kingqaquu
  tags:
  - docs
  - quality-review
  related-skills:
  - ohos-test-docs-writing-compliance-review
  - ohos-test-docs-api-reference-review
  - ohos-test-docs-dev-guide-review
  - ohos-test-docs-code-correctness-review
---

# 文档 PR 改动检视

独立完成取 diff、范围定位、专项检视和报告。默认在回复中输出，不依赖原主技能、报告或 Excel 技能，不自动发布评论或改写文档。

## 获取完整变更

- 原始 unified diff：直接读取，说明缺少哪些原文件/版本信息。
- 本地明确 `base..head`：按用户给出的两端使用 `git diff base head`；用户要求 PR 视角时解析 `git merge-base base head` 后比较 merge-base 与 head，披露实际 SHA，不能静默混淆两种语义。先取所有文件清单，再筛选 `.md`/`.markdown` 及相关 `.json5`，不要预先丢掉配置。
- GitCode PR：发现当前可用的 GitCode MCP/CLI，读取 PR 元信息、head/base SHA 和所有分页文件变更。patch 缺失、截断或仅有统计时，使用已配置的 GitCode API/CLI 或在独立临时目录取得对应提交后生成 diff；不能假定 GitHub 的 `gh` 能访问 GitCode。仍取不到完整内容时明确报告未覆盖文件，不把空 patch 当无改动。
- GitHub PR：使用可用的 `gh pr diff` / API 等取得 diff 和 head/base。无认证或工具时，可继续评审已给补丁，列出缺口；仅在缺口阻止工作时请求补丁或本地范围。

不切换、暂存、重置用户工作区。完整文件和 SDK 用于理解上下文，检视范围仍限改动引入的问题。

## 确定行号与侧别

读取 [diff 定位规则](references/diff-contract.md)，按 hunk 跟踪 old/new 行号及文件路径。`+` 是新侧可报告行，`-` 是删除证据，context 仅供理解。删除起始版本、权限、错误码或前置约束且没有等价替换时可报告删除缺陷；纯删除冗余内容不报。重命名时分别保留 old_path/new_path；纯重命名无内容变化不触发全文评审。

## 按内容选择检视规则

只读取对应 skill 的 SKILL.md 及所需引用，不依赖特定平台的 Skill 调用工具：

| 内容 | 随仓配套技能 |
|---|---|
| 代码、版本、截图，相关 JSON5 | `ohos-test-docs-code-correctness-review` |
| ArkTS/JS/C/REST API 参考 | `ohos-test-docs-api-reference-review` |
| 开发指南、教程、最佳实践 | `ohos-test-docs-dev-guide-review` |
| 文档通用写作与排版 | `ohos-test-docs-writing-compliance-review` |

单独安装本技能而未安装配套技能时，继续按本节最低检查执行，并明确专项 checklist 未覆盖；完整专项覆盖需要上述四项。最低检查：参数/签名/版本内部矛盾、删除重要约束、调用缺少已给出的前提、断开的操作步骤、损坏的链接/代码块语法。没有匹配 SDK 时不可声称接口核验通过。配套技能从当前仓库同级目录或当前环境技能列表解析，不使用个人绝对路径。

类别可组合：含示例的API文档采用API+代码规则，指南含JSON5配置采用指南+代码规则；只有文字修订时不加载无关语言代码规则。写作规则只处理叙述/展示，不重新判定SDK签名；相同签名缺陷以代码或API规则为主，合并依据。规则属于迁入的用户检视体系，项目明确约定优先，缺少同版本证据不得套用另一版本或将风格阈值当语法门禁。

向专项检视传递：文件类型、目标版本、完整可用上下文、新增行集合、删除行及旧侧位置、仅报告改动引入问题的约束。过滤既有缺陷；同一根因按文件、侧别、位置去重，合并规则依据，不把不同缺陷仅因同行而合并。

## 输出

列出 PR/范围及 SHA、已覆盖与未覆盖文件、变更统计、验证限制；未知统计标未知。按文件 → hunk → 位置给出严重度、new/old 侧别、原文、规则、证据、修改建议及预期效果；删除问题不得编造新文件行号。给总数与严重度统计。无缺陷时说明“在已检查改动范围内未发现问题”；未取全或未验证时不输出无条件通过。默认不生成 Excel；用户另行要求导出时按指定格式处理。

严重度按实际影响：高为已有证据支持的错误调用、不兼容或任务无法完成；中为必要约束/关键说明缺失；低为风格和阅读体验。参考规则不预置高/中颜色，缺少验证条件单列未验证，不当作高严重度问题凑数。
