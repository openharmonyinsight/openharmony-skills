# 统一知识库使用规范

本规范适用于需求分析、方案设计、代码生成等所有依赖知识库的 skill。
如各 skill 与本规范冲突，以本规范为准；skill 仅保留"场景特化补充"。

## 1. 数据源降级策略（强制）

所有需要代码/架构信息的 skill 必须按以下优先级逐级降级检索：

| 优先级 | 数据源 | source_type | 说明 |
|--------|--------|-------------|------|
| 🥇 首选 | oh-chromium-knowledge 知识库 | `LOCAL_KB` | Chromium 三仓结构化索引，覆盖 14 个仓库的代码路径和架构信息 |
| 🥇 首选 | oh-ai-full-design 知识库 | `LOCAL_KB` | 鸿蒙全量组件知识库，覆盖 471 仓库、63 子系统、38 万+ API |
| 🥈 次选 | DeepWiki MCP | `DEEPWIKI` | AI 增强的仓库理解，支持精准问答 |
| 🥉 兜底 | 本地文档 | `LOCAL_DOC` | 项目内历史分析文档、references 等 |
| 🏅 最终 | 克隆仓库 | `CODE` | 浅克隆目标仓库，直接搜索源码 |

> **两个 🥇 知识库定位不同、互补使用：**
> - **oh-chromium-knowledge**：聚焦 Chromium 三仓（chromium_src/cef/third_party）的代码路径、模块架构、OHOS 适配层，用于代码定位和技术方案设计
> - **oh-ai-full-design**：聚焦鸿蒙组件体系（子系统/部件/API），用于组件归属、接口查询、依赖关系、SystemCapability 查找
>
> 检索时两个知识库都应尝试，按需求类型选择侧重：涉及 Chromium 内核实现优先 oh-chromium-knowledge，涉及鸿蒙框架层接口优先 oh-ai-full-design。

**降级规则：**
1. 🥇 两个知识库都应尝试检索，未命中或有未覆盖项时降级到 🥈
2. 不允许跳过高级别直接使用低级别数据源
3. DeepWiki 不能单独作为最终结论依据，必须有 KB 证据或代码证据共同支撑
4. 本地文档用于术语解释或背景补充，不用于替代结构化检索
5. 克隆仓库仅在以上方式都无法覆盖需求关键词时使用
6. oh-ai-full-design 为私有仓库，外部用户无权限属正常，跳过即可

## 2. 🥇 oh-chromium-knowledge 检索顺序（强制）

**仓库**: `zhufenghao/oh-chromium-knowledge`（GitCode 公开）
**API**: `GET /api/v5/repos/zhufenghao/oh-chromium-knowledge/contents/{path}`
**认证**: `PRIVATE-TOKEN` header（Token 从环境变量读取（优先 `GITCODE_TOKEN`，回退 `GITLAB_TOKEN`，或从 `.env` 文件加载））

检索步骤（严格按顺序）：
1. `index.json` → 全局路由入口（必须先读）
2. `search/by_feature.json` → 按需求类型定位（35 个功能特性）
3. `search/by_module.json` → 按模块定位（20 个模块）
4. `repos/chromium_src/arkweb_adapter/routing_table.json` → 代码路径映射
5. `repos/{repo}/architecture.md` → 仓库架构文档（1-2 个相关仓库）
6. `repos/{repo}/meta.json` → 仓库元信息（按需）

**兼容旧索引路径（如 by_feature 未命中可尝试）：**
- `search/by_keyword.json` → 按关键词定位
- `search/by_scenario.json` → 场景描述命中时
- `search/by_syscap.json` → 能力词/SystemCapability/SA 命中时
- `search/api_keyword_to_component.json` → API 词命中时
- `subsystems/{subsystem}.json` → 子系统索引
- `components/*/*.json` → 通过 `component_files` 路由打开
- `apis/*/*.json` → 仅在接口细节需要时读取
- `graph/**/*.json` → 仅在依赖/影响分析需要时读取

**路由约束（强制）：**
- 禁止通过 `component_id.split('_')[0]` 推断子系统
- 禁止字符串拼接组件路径
- 必须通过 `subsystems/*.json -> component_files` 路由组件文件
- 禁止跳过 `index.json` 直接读取子文件
- 禁止批量扫描 repos/ 或 search/ 下的所有文件
- 文件路径必须从索引中获取
- `data/api_descriptions.json`（若存在）仅可作为兜底

## 3. 🥇 oh-ai-full-design 检索顺序（强制）

**仓库**: `openharmony-ai-design/oh-ai-full-design`（GitCode 私有）
**API**: `GET /api/v5/repos/openharmony-ai-design/oh-ai-full-design/contents/{path}`
**认证**: `PRIVATE-TOKEN` header（Token 从环境变量读取（优先 `GITCODE_TOKEN`，回退 `GITLAB_TOKEN`，或从 `.env` 文件加载））
**覆盖**: 471 仓库、63 子系统、385 部件、19,346 Public API + 6,526 System API + 358,220 Inner API

检索步骤（严格按顺序）：
1. `index.json` → 全局路由入口（必须先读，获取子系统列表和统计信息）
2. `search/by_keyword.json` → 按关键词定位组件
3. 场景描述命中时：`search/by_scenario.json`
4. 能力词/SystemCapability/SA 命中时：`search/by_syscap.json`
5. API 词命中时：`search/api_keyword_to_component.json`
6. `subsystems/{subsystem}.json` → 子系统索引（获取 component_files 列表）
7. 通过 `component_files` 路由打开 `components/*/*.json`
8. 仅在接口细节需要时读取 `apis/*/*.json`
9. 仅在依赖/影响分析需要时读取 `graph/**/*.json`

**路由约束（强制）：**
- 禁止通过 `component_id.split('_')[0]` 推断子系统
- 禁止字符串拼接组件路径（如 `components/{subsystem}/{component}.json`）
- 必须通过 `subsystems/*.json -> component_files` 路由组件文件
- 禁止跳过 `index.json` 直接读取子文件
- 禁止批量扫描所有子系统/组件文件
- 文件路径必须从索引中获取
- `data/api_descriptions.json`（若存在）仅可作为兜底

**权限说明**：此仓库为 OpenHarmony AI Design 团队私有仓库。有权限时正常使用，无权限时跳过此知识库（不影响主流程）。

## 4. 🥈 DeepWiki MCP 检索规范

**MCP 配置：**
```json
{ "mcp": { "deepwiki": { "type": "remote", "url": "https://mcp.deepwiki.com/mcp" } } }
```

**覆盖仓库：**
| 仓库 | repoName |
|------|----------|
| OpenHarmony ACE Engine | `openharmony/arkui_ace_engine` |
| OpenHarmony WebWebView | `openharmony/web_webview` |
| OpenHarmony Chromium 适配 | `OpenHarmony-TPC/chromium_src` |
| OpenHarmony CEF 适配 | `OpenHarmony-TPC/chromium_cef` |

**调用策略：**
1. `read_wiki_structure` → 获取仓库主题概览
2. `read_wiki_contents` → 读取相关模块文档
3. `ask_question` → 精准搜索代码问题（类定义、方法签名、调用链路）

**MCP 不可用时降级为本地文档。**

## 5. 🥉 本地文档检索

| 类型 | 路径 | 说明 |
|------|------|------|
| 分析文档 | `{DOCS_REPO}/analysis/*.md` | 历史代码分析缓存 |
| 参考资料 | `{DOCS_REPO}/references/*.md` | 架构参考、竞品分析等 |

## 6. 🏅 克隆仓库（最终兜底）

当前面三级数据源都无法覆盖时：
```bash
git clone --depth=1 https://gitcode.com/{owner}/{repo}.git {DOCS_REPO}/tmp/{repo}
```
克隆后使用 `grep`/`find` 搜索关键词，提取代码信息。

## 7. 证据规范（强制）

所有输出（分析报告/设计文档/实现报告）必须包含"知识证据清单"，每条至少包含：

| 字段 | 值域 | 说明 |
|------|------|------|
| `source_type` | `LOCAL_KB` / `DEEPWIKI` / `LOCAL_DOC` / `CODE` | 数据源级别 |
| `object_type` | `subsystem` / `component` / `api` / `file` / `class` | 对象类型 |
| `object_id` | 自由文本 | 对象标识 |
| `evidence_path_or_url` | 路径或 URL | 证据来源 |
| `hit_reason` | 关键词/场景/syscap/API词 | 命中原因 |
| `confidence` | 高/中/低 | 置信度 |

## 8. 深度检索与重排规则（建议）

- 先本地检索后在线补充：先得到 LOCAL_KB 候选，再用 DeepWiki 做背景补全。
- 混合重排：LOCAL_KB 命中优先，DeepWiki 证据仅加分不单独排首位。
- 低质量页降权：对纯 wrapper、自动生成索引页设置低权重。

## 9. 失败与降级策略

- 离线 KB 缺失：明确标注"证据不足（离线）"，禁止给出确定性结论。
- DeepWiki 不可用：流程不中断，回退到离线 KB + 代码证据。
- 证据冲突：保留冲突项，输出"待代码落点验证"。

## 10. 输出口径

- 结论必须可追溯到证据，不允许"仅凭经验"结论。
- 所有推断项必须显式标注"推断项"。
- 同一对象跨阶段（分析/设计/实现）的名称与归属口径保持一致。
- 证据冲突时保留冲突项，输出"待代码落点验证"。

## 11. 证据包持久化（强制）

**问题**：知识库检索过程中，证据包仅存在于 LLM 上下文，不落盘。一旦上下文被截断或 subagent 超时，检索结果全部丢失，需要重新检索，浪费 token 和时间。

**强制要求**：每次完成知识库检索后，必须将完整的证据包 **Write 到 `{DOCS_REPO}/tmp/` 目录**。

**输出路径规范**：
- 文件名格式：`{DOCS_REPO}/tmp/arkweb_kb_evidence_{YYYYMMDD_HHmmss}_{feature}.md`
- `feature` 为需求英文标识（kebab-case），如 `page-control`、`webgpu-context`
- 时间戳精确到秒，确保多轮检索不覆盖

**文件内容结构（强制）**：
```markdown
# 知识库证据包

- 需求标识：{feature-name}
- 生成时间：{YYYY-MM-DD HH:mm:ss}
- 触发来源：{skill-name} / {phase-name}

## 🥇 oh-chromium-knowledge
- 匹配的功能类型: {type}（来自 search/by_feature.json）
- 相关代码路径: {paths}（来自 routing_table.json）
- 架构约束: {summary}（来自 architecture.md）
- 未覆盖项: {items}
- 原始检索内容（保留完整 JSON/文本）:
  {raw_kb_content}

## 🥇 oh-ai-full-design
- 匹配的子系统/部件: {subsystem/component}（来自 index.json → subsystems/ → components/）
- 相关 API: {apis}（来自 apis/）
- SystemCapability: {syscap}（来自 search/by_syscap.json）
- 未覆盖项: {items}
- 原始检索内容（保留完整 JSON/文本）:
  {raw_ohai_content}

## 🥈 DeepWiki 补充
- 仓库: {repo} → 搜索 "{keyword}" → {发现摘要}
- 原始响应（保留完整内容）:
  {raw_deepwiki_content}
- 未覆盖项: {items}

## 🥉 本地文档补充
- 文档: {path} → {发现摘要}
- 原始命中片段（保留原文）:
  {raw_local_doc_content}
- 未覆盖项: {items}

## 🏅 克隆仓库（如有）
- 仓库: {repo} → 搜索 "{keyword}" → {发现摘要}
- 原始搜索结果（保留完整内容）:
  {raw_clone_content}

## 证据汇总表
| # | source_type | object_type | object_id | evidence_path_or_url | hit_reason | confidence |
|---|-------------|-------------|-----------|---------------------|------------|------------|
| 1 | LOCAL_KB    | ...         | ...       | ...                 | ...        | ...        |
```

**关键原则**：
1. **保留原始内容**：每个数据源的原始检索结果（JSON、文本、代码片段）必须完整保留，不允许仅保存摘要
2. **先写后用**：证据包必须先 Write 到 `{DOCS_REPO}/tmp/`，然后再注入 subagent 或用于后续分析
3. **失败可恢复**：如果 subagent 超时或上下文丢失，可以直接从 `{DOCS_REPO}/tmp/` 读取证据包，无需重新检索
4. **跨阶段复用**：同一需求的证据包在整个流程中复用，后续 phase 优先从 `{DOCS_REPO}/tmp/` 读取已有证据包
5. **多条目追加**：同一需求多轮检索时，使用不同时间戳文件名，不覆盖已有证据包

## 13. Chromium 文档搜索（chromium-docs skill）

基于 chromium_agents 的 chromium_docs.py，自动索引 Chromium 源码仓库中的官方文档。

**使用场景**：当需要理解 Chromium 架构、编程模式、开发规范时，优先使用 chromium-docs 搜索文档。

**触发条件**：
- 需要理解某个 Chromium 子系统的架构或设计
- 需要查阅 Chromium 的编程规范或最佳实践
- 需要了解构建系统、测试框架的使用方法

**使用方式**：
```bash
# 构建索引（首次使用）
python skills/chromium-docs/scripts/chromium_docs.py --build-index

# 搜索
python skills/chromium-docs/scripts/chromium_docs.py "threading model"
```

**与 oh-chromium-knowledge 的关系**：
- chromium-docs → 索引**文档**（理解架构/模式/规范）
- oh-chromium-knowledge → 索引**代码路径**（定位具体文件）

两者互补：先通过 chromium-docs 理解架构，再通过 oh-chromium-knowledge 定位代码。

## 14. 任务导航（knowledge_base.md）

`skills/_shared/knowledge_base.md` 提供了任务→文档的映射关系，AI Agent 在处理 Chromium 相关任务时应参考此文件确定需要查阅哪些文档。
