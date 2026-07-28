# 阶段1：需求解析骨架

> 本文件内容将填入SKILL.md统一Prompt模板。详细执行规则见 `rules/phase1_rules.md`，知识库匹配规则见 `rules/knowledge_usage_guide.md`，编排器交互流程见 `rules/phase1_clarify_rules.md`。

## 任务
分析需求文档，生成requirement_analysis.md + knowledge_match.md（创建骨架+§1.1交付推断结果+§1.2条目匹配详情）。

## NEVER约束
- NEVER 输出推导性内容——只输出文档明确描述的黑盒可验证行为
- NEVER 内部接口/内部变量——严格执行inner接口过滤
- NEVER 应用测试设计方法——属于phase2职责
- NEVER 跳过正交判定——每个主单元必须判定正交/非正交

## 核心约束（必须理解）
- IBO原则：仅提取外部可触发且可验证的行为
- 零推导原则：仅输出原文档明确描述
- 正交判定：每个主单元判定正交/非正交并采用对应格式
- 跨US场景重叠检测：多个US涉及相同被测对象时标注"场景重叠"
- ID角色边界：内部追溯ID仅出现在追溯引用位置

## 输入
- Spec文档路径：{requirement_docs_path}
- 领域名称：{domain}
- 知识库模式：{knowledge_mode}（mcp/local/none）

## 输出
- {output_dir}/requirement_analysis.md
- {output_dir}/knowledge_match.md（创建骨架 + §1.1交付推断结果 + §1.2条目匹配详情，供Phase2/Phase4追加）

## 知识库调用（辅助理解 + 交付推断 + 创建knowledge_match.md）

**详细执行规则**：详见 `rules/knowledge_usage_guide.md`（§2层级发现与读取流程、§3调用方式含MCP工具调用语法和本地模式流程、§4层级隔离规则、§6 knowledge_match.md格式、§11交付推断规则）。

**Phase1专属规则**：仅读取domain-knowledge目录，禁止读取test-experience或case-refinement。

**交付推断（Phase1强制执行）**：区分测试对象（spec标注变更内容的主单元）与回归对象（DK条目提取的已交付功能），写入knowledge_match.md§1.1交付推断结果表。详见 `rules/knowledge_usage_guide.md` §11。

## 返回摘要
- 拆分策略 / 主单元总数 / 输入条件总数（直接参数X个 + 上下文条件Y个） / 被测场景总数
- 正交判定结果：主单元1(正交/非正交) + 主单元2(正交/非正交) + ...
- 交付推断结果：测试对象主单元X个（{主单元ID列表}） + 回归对象领域Y个（{领域名称列表}）
- SDK API总数（public）/ 可测试性手段总数（类型分布）
- 验证映射总数 / 非功能需求数 / 待确认项数（缺口类型分布）
- 删除的inner接口数 / 零推导验证 / 自检结果：X/X项通过
