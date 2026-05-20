---
name: arkweb-code-analysis
description: ArkWeb 代码仓库分析与索引生成。可作为独立 subagent 运行。支持 DeepWiki 在线索引增强。输出结构化索引文档供后续 design-doc 和 spec-review 调用。触发词：分析代码仓库、生成代码索引、理解仓库结构。
---

# ArkWeb 代码仓库分析与索引

**Announce at start:** "我正在使用 arkweb-code-analysis skill 分析代码仓库。"

## 运行模式

### 模式 A：Subagent 模式（推荐）

作为独立 subagent 被 `arkweb-architect` 调用时，从 task 描述中获取需求关键词和知识库证据包，结合 DeepWiki 在线索引 + 本地分析文档，输出结构化代码索引。

**输入格式（从 task 描述中解析）：**
```
## 需求关键词
{从需求中提取的技术关键词}

## 分析范围
- ace_engine: Web 组件相关代码
- web_webview: NWeb API 相关代码
- chromium_src: 内核相关代码（如涉及）

## 知识库证据包（主 Session 已在 Phase 2 Step 2.0 检索完成）
{知识库检索结果，可直接引用}
```

**输出：** 分析文档 → 保存到指定路径 → 回复关键发现

### 模式 B：交互模式

在主 session 中直接调用，用户指定仓库和分析目标。

---

## 分析数据源

> 通用降级策略、仓库信息、认证方式详见 `_shared/KB_RULES.md`。以下仅列出本 skill 的检索流程。

### 🥇 oh-chromium-knowledge 知识库

**读取流程（严格按顺序）：**
1. `index.json` → 全局路由入口（14 个仓库索引）
2. `search/by_feature.json` → 按需求类型定位（35 个功能特性）
3. `search/by_module.json` → 按模块定位（20 个模块）
4. `repos/chromium_src/arkweb_adapter/routing_table.json` → 代码路径映射（29 个需求类型）
5. `repos/chromium_src/modules/components.json` → 组件索引（17 个核心组件）
6. `repos/chromium_src/arkweb_adapter/ohos_dirs.json` → OHOS 适配目录（43 个）
7. `repos/chromium_src/arkweb_adapter/nweb_service.json` → NWeb 接口映射
8. `repos/{repo}/architecture.md` → 各仓库架构文档

**禁止事项：**
- ❌ 不要一次性读取所有 repos/ 下的文件
- ❌ 不要跳过 Step 1（必须先读 index.json）
- ❌ 不要把知识库当源码——知识库仅提供索引，具体实现需查看实际代码仓库

**调用策略：**
1. 先读 `index.json` 了解全局结构
2. 根据需求关键词在 `search/by_feature.json` 中匹配相关功能特性
3. 从匹配到的 `files` 列表中读取 1-2 个关键文件
4. 用定位到的代码路径指导 DeepWiki 查询（更精准的关键词）
5. 如涉及 OHOS 适配，额外读取 `ohos_dirs.json` 和 `skills/ohos-adapter-guide.md`

**覆盖范围：**
- chromium_src / chromium_cef / chromium_third_party / chromium_chrome / chromium_v8 / chromium_third_party_skia（Tier 1）
- ffmpeg / angle / devtools_frontend / webrtc / blink_webtests / dawn / pdfium（Tier 2）
- chromium_arkweb（Tier 3）
- 详见知识库 SKILL.md：`skills/oh-chromium-knowledge/SKILL.md`

### 🥇 oh-ai-full-design 知识库

**仓库**: `openharmony-ai-design/oh-ai-full-design`（GitCode 私有）
**用途**: 鸿蒙组件体系检索（子系统/部件/API/SystemCapability），与 oh-chromium-knowledge 互补

**读取流程：**
1. `index.json` → 全局路由入口
2. `search/by_keyword.json` → 按关键词定位组件
3. `subsystems/{subsystem}.json` → 子系统索引
4. `components/*/*.json` → 部件详情
5. `apis/*/*.json` → 接口详情（按需）

**注意**: 私有仓库，无权限时跳过。详见 `_shared/KB_RULES.md` 第 3 节。

### 🥈 DeepWiki MCP（在线索引增强）

通过 OpenCode MCP 直接调用 DeepWiki API，获取 AI 增强的仓库代码理解（架构、类关系、调用链路等）。无需浏览器渲染，速度快、结构化输出。

**MCP 配置（opencode.json）：**
```json
{
  "mcp": {
    "deepwiki": {
      "type": "remote",
      "url": "https://mcp.deepwiki.com/mcp"
    }
  }
}
```

**MCP 工具（3 个）：**

| 工具 | 功能 | 参数 | 适用场景 |
|------|------|------|---------|
| `read_wiki_structure` | 获取仓库文档主题列表 | `repoName`: GitHub 仓库路径 | 快速了解仓库覆盖范围，确定搜索方向 |
| `read_wiki_contents` | 查看仓库文档内容 | `repoName` + `topic` | 深入了解模块/类/API 的详细文档 |
| `ask_question` | AI 问答（基于仓库上下文） | `repoName` + `question` | 精准搜索代码问题，获取 AI 增强分析 |

**覆盖仓库：**

| 仓库 | repoName | DeepWiki URL |
|------|----------|-------------|
| OpenHarmony ACE Engine | `openharmony/arkui_ace_engine` | https://deepwiki.com/openharmony/arkui_ace_engine |
| OpenHarmony WebWebView | `openharmony/web_webview` | https://deepwiki.com/openharmony/web_webview |
| OpenHarmony Chromium 适配 | `OpenHarmony-TPC/chromium_src` | https://deepwiki.com/OpenHarmony-TPC/chromium_src |
| OpenHarmony CEF 适配 | `OpenHarmony-TPC/chromium_cef` | https://deepwiki.com/OpenHarmony-TPC/chromium_cef |
| OpenHarmony Chromium 第三方库 | `OpenHarmony-TPC/chromium_third_party` | https://deepwiki.com/OpenHarmony-TPC/chromium_third_party |

**调用策略：**
1. 先调用 `read_wiki_structure` 获取仓库主题概览，确定相关模块
2. 调用 `read_wiki_contents` 读取相关模块的详细文档
3. 调用 `ask_question` 精准搜索具体代码问题（类定义、方法签名、调用链路等）
4. 对多个关键词分别调用 `ask_question`，合并结果
5. 对于 chromium_src，优先搜 Blink 命名空间的类（如 `blink::HTMLInputElement`）

**降级策略：** 见 `_shared/KB_RULES.md`

### 🥉 本地分析文档（复用）

| 文档 | 路径 | 内容 |
|------|------|------|
| ACE Engine 分析 | `analysis/arkweb-ace-engine-analysis.md` | Web 组件完整索引 |
| WebWebView 分析 | `analysis/web-webview-analysis.md` | NWeb API 索引 |
| Chromium ArkWeb | `analysis/chromium-arkweb-analysis.md` | 内核分析 |
| CEF 分析 | `analysis/chromium-cef-analysis.md` | CEF 层分析 |

**使用方式：** `grep -n -i "{keyword}" {project_root}/analysis/*.md`

### 🏅 克隆仓库（兜底）

当 DeepWiki 和本地文档都无法覆盖时：
```bash
git clone --depth=1 https://gitcode.com/{owner}/{repo}.git {DOCS_REPO}/tmp/{repo}
```

---

## 流程

### Step 1: oh-chromium-knowledge 知识库检索

1. 读取 `index.json` 获取全局结构
2. 根据需求关键词在 `search/by_feature.json` 中匹配相关功能特性
3. 从匹配结果中获取推荐的文件列表
4. 读取 `routing_table.json` 中对应需求类型的代码路径映射
5. 如涉及 OHOS 适配，读取 `ohos_dirs.json` 和 `nweb_service.json`
6. 如涉及特定组件，读取 `components.json` 中对应条目

### Step 2: DeepWiki MCP 查询

1. 根据分析范围确定要查询的仓库（参见上方覆盖仓库表）
2. 调用 `read_wiki_structure` 获取仓库文档主题概览
3. 调用 `read_wiki_contents` 读取相关模块文档
4. 调用 `ask_question` 精准搜索代码问题：
   - 类定义和继承关系
   - 方法签名和参数
   - 调用链路
   - 架构关系
   - 文件路径（如 `third_party/blink/renderer/core/html/...`）
5. 对多个关键词重复查询，合并结果

**MCP 不可用时，降级为浏览器方式：**
1. 使用 agent-browser skill 打开 DeepWiki 页面
2. 获取快照后搜索关键词，提取代码信息

### Step 3: 本地文档补充

1. 在已有分析文档中搜索关键词
2. 补充 DeepWiki 未覆盖的细节（如文件路径、行号）

### Step 4: 合并分析

将知识库索引 + DeepWiki 发现 + 本地文档信息合并为统一的分析结果。

### Step 5: 证据包持久化（强制）

**【强制持久化】** 证据包 Write 到 `{DOCS_REPO}/tmp/`，详见 `_shared/KB_RULES.md` 第 10 节。

证据包文件必须包含：
- 每个数据源的**原始检索结果**（完整 JSON、文本、代码片段），不允许仅保存摘要
- 🥇 知识库索引的完整 JSON 响应
- 🥈 DeepWiki 的完整回答内容
- 🥉 本地文档的完整命中片段
- 🏅 克隆仓库的完整搜索输出

### Step 6: 生成分析文档

```markdown
# {feature-name} 代码分析

## 数据源
- 知识库: oh-chromium-knowledge（{匹配的需求类型}, {读取的索引文件}）
- DeepWiki: {使用的仓库 URL，搜索的关键词及结果摘要}
  - {仓库1}: {URL} → 搜索 "{keyword1}", "{keyword2}" → {发现摘要}
  - {仓库2}: {URL} → 搜索 "{keyword3}" → {发现摘要}
- 本地文档: {参考的分析文件}

## 相关文件清单
| 文件 | 路径 | 职责 | 与本需求的关系 |
|------|------|------|--------------|

## 关键类和接口
| 类/结构 | 文件 | 方法/字段 | 说明 |
|---------|------|----------|------|

## 调用链路
{描述相关代码的调用关系}

## 现有相关逻辑
{描述现有代码中与本需求相关的已有实现}

## 技术可行性评估
| 方案 | 涉及的现有代码 | 可行性 | 风险点 |
|------|--------------|--------|--------|
```

### Step 7: 输出

#### Subagent 模式
保存文档并回复关键发现摘要。

#### 交互模式
输出分析结果，供用户参考。

## 产出物

- **路径**：`{DOCS_REPO}/analysis/YYYY-MM-DD-{feature}-analysis.md`

## Subagent 回复格式

```
✅ code-analysis 完成
📄 文档：{file_path}
🔍 数据源：oh-chromium-knowledge + oh-ai-full-design ({N} 个索引) + DeepWiki ({N} 个仓库, {N} 个关键词) + 本地文档 ({N} 个)
📊 关键发现：
- 相关文件 {N} 个，核心类 {N} 个
- 关键接口：{interface_1}, {interface_2}
- 调用链路：{简要描述}
- ⚠️ 注意：{潜在风险或需关注的点}
```
