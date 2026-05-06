# 标签分类字典

这些标签值作为标准起点使用。只有现有标签都不适合时，才新增 lowercase kebab-case 格式的新值。

## `tool`

- `opencode`
- `cursor`
- `claude-code`
- `chatgpt`
- `copilot`
- `codex`
- `minmax`
- `internal-agent`
- `office-assistant`
- `search-assistant`
- `unknown`

## `category`

该标签族用于根因问题分类、统计分析和改进规划。每条反馈优先选择一个主分类，可选次分类。

- `model-capability`
- `environment-tooling`
- `business-context-clarity`
- `workflow-process`
- `user-skill-training`
- `data-permission`
- `safety-compliance`
- `unknown`

### 分类定义

- `model-capability`：AI 在推理、规划、上下文管理、指令遵循、代码理解、工具使用决策或错误恢复方面表现不足。
- `environment-tooling`：问题更可能来自本地环境、依赖、IDE/CLI 行为、构建/测试配置、网络、命令可用性或工具集成稳定性。
- `business-context-clarity`：任务缺少清晰的业务目标、产品规则、领域概念、验收标准、边界条件或期望行为。
- `workflow-process`：团队的 AI 辅助研发流程需要改进，例如任务拆分、评审关卡、验证策略、回滚/检查点或交接方式。
- `user-skill-training`：用户可能需要更好的提示词习惯、上下文组织方式、AI 协作模式或结果验证实践。
- `data-permission`：AI 无法访问所需仓库、文件、文档、日志、凭证、私有知识或运行数据。
- `safety-compliance`：涉及隐私、安全、合规、不安全代码变更、生产风险或不可逆操作。
- `unknown`：反馈信息不足，无法负责任地分类。

## `scenario`

- `coding`
- `writing`
- `search`
- `data-analysis`
- `design`
- `office-work`
- `customer-support`
- `meeting`
- `learning`
- `automation`
- `unknown`

## `task`

- `bug-fix`
- `feature-dev`
- `api-change`
- `refactor`
- `test`
- `documentation`
- `code-review`
- `planning`
- `summarization`
- `translation`
- `data-cleaning`
- `report-generation`
- `question-answering`
- `unknown`

## `workflow-stage`

- `requirements`
- `planning`
- `implementation`
- `verification`
- `implementation-and-verification`
- `review`
- `deployment`
- `handoff`
- `unknown`

## `issue`

- `wrong-understanding`
- `hallucination`
- `wrong-file-edit`
- `wrong-tool-use`
- `tool-call-error`
- `repeated-failure`
- `poor-context-use`
- `unclear-business-requirement`
- `missing-acceptance-criteria`
- `missing-domain-context`
- `environment-setup-failure`
- `missing-clarification`
- `ignored-instruction`
- `bad-output-quality`
- `formatting-error`
- `slow-response`
- `excessive-cost`
- `unsafe-action`
- `privacy-risk`
- `permission-error`
- `environment-error`
- `integration-error`
- `unknown`

## `capability`

- `planning`
- `reasoning`
- `coding`
- `context-management`
- `tool-use`
- `instruction-following`
- `memory`
- `communication`
- `retrieval`
- `safety`
- `unknown`

## `severity`

- `low`
- `medium`
- `high`
- `critical`
- `unknown`

## `frequency`

- `once`
- `occasional`
- `frequent`
- `systemic`
- `unknown`

## 建议分派方向

- `产品体验`
- `模型能力`
- `工具集成`
- `环境配置`
- `业务分析`
- `提示词/流程设计`
- `权限/数据访问`
- `文档/培训`
- `安全/合规`
- `unknown`

## 分类示例

使用 `category:model-capability`：Agent 修改了无关文件、反复尝试同一个失败方案、幻觉出不存在的 API、忽略明确指令。

使用 `category:environment-tooling`：依赖缺失导致测试无法运行、工具无法调用终端、IDE 插件断连、命令在本地可用但 Agent 环境不可用。

使用 `category:business-context-clarity`：不知道如何描述业务规则、验收标准不清、AI 实现了技术上可运行但不符合产品预期的逻辑、领域术语没有解释。

使用 `category:workflow-process`：任务过大不适合一次 AI 会话、AI 变更无人评审、没有测试计划、人和 AI 的交接不清。

使用 `category:user-skill-training`：用户不知道该提供哪些上下文、提示词过于模糊、用户没有检查 AI 的关键假设。

使用 `category:data-permission`：AI 需要日志但无法访问、仓库不完整、私有文档不可用、权限或凭证阻塞验证。

使用 `category:safety-compliance`：AI 暴露敏感数据、尝试危险生产操作、输出违反安全或合规要求。

## 严重程度校准

当反馈提到或强烈暗示数据丢失、安全暴露、隐私暴露、生产事故、合规风险、不可逆危险操作或广泛业务影响时，使用 `critical`。

当问题阻塞任务完成、造成大量返工、影响多人，或反复阻碍团队工作流完成时，使用 `high`。

当问题造成明显摩擦、反复人工修正或质量担忧，但用户仍可恢复时，使用 `medium`。

当问题主要是视觉、格式、轻微不便，或有明显绕过方式时，使用 `low`。

当无法从描述中判断影响时，使用 `unknown`。
