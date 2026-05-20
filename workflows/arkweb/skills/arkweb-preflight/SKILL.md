---
name: arkweb-preflight
description: ArkWeb SDD 工作流环境预检。在启动主流程前检查外部依赖、数据源、工具链是否就绪，自动修复可修复项，输出环境状态报告。触发词：环境检查、preflight、检查配置、开始前检查。
---

# ArkWeb SDD Preflight — 环境预检

## 定位

**可选的 Phase 0**。在主流程（Phase 1-9）启动前，用户可主动触发此 skill 检查当前工作环境是否满足要求。不在主流程中，不阻塞任何阶段。

**使用场景：**
- 首次使用 arkweb-sdd 时
- 切换到新机器/新项目时
- 工作流执行中遇到数据源不可用时
- 想确认当前环境能力等级时

## 检查流程

### Step 0: 确定项目根目录

```
1. 确认当前工作目录（cwd）
2. 检查 skills/arkweb-architect/SKILL.md 是否存在
   - 存在 → 当前目录即为项目根（SKILL_HOME）
   - 不存在 → 提示用户指定项目根目录，或 clone arkweb-sdd
```

### Step 1: 必须项检查（不满足则无法启动主流程）

| # | 检查项 | 检测方式 | 自动修复 | 修复失败时 |
|---|--------|---------|---------|-----------|
| P-1 | Skill 文件完整 | 检查 `skills/` 下 11 个核心 SKILL.md 是否存在 | 提示用户从 arkweb-sdd 复制缺失文件 | 列出缺失 skill，主流程可能部分不可用 |
| P-2 | 产出物目录可写 | `mkdir -p docs/features/test && rm -rf docs/features/test` | 自动创建 `docs/features/`、`analysis/` | 提示用户检查目录权限 |
| P-3 | 模板文件存在 | 检查 `assets/templates/` 下 6 个模板 | 提示从 arkweb-sdd 复制 | 列出缺失模板，设计文档阶段可能缺少模板引导 |
| P-4 | AI Agent 能力探测 | 检测 `sessions_spawn` 是否可用 | 不可用则切换到**模式 B（串行）** | 告知用户将使用串行模式，专家团无法并行 |

### Step 2: 增强项检查（不满足可降级，不影响启动）

| # | 检查项 | 检测方式 | 降级方案 |
|---|--------|---------|---------|
| E-1 | GitCode API Token | 读取环境变量（优先 `GITCODE_TOKEN`，回退 `GITLAB_TOKEN`）或 `.env` 文件 | 提示用户配置，Phase 9（提交 PR）需手动处理 |
| E-2 | oh-chromium-knowledge 知识库 | `curl -s -H "PRIVATE-TOKEN: $TOKEN" "https://gitcode.com/api/v5/repos/zhufenghao/oh-chromium-knowledge/contents/index.json"` 检查 HTTP 200 | code-analysis 降级为 DeepWiki 优先 |
| E-3 | oh-ai-full-design 知识库 | 同上方式检查 `openharmony-ai-design/oh-ai-full-design` | 无权限属正常，code-analysis 跳过此数据源 |
| E-4 | DeepWiki MCP | 尝试调用 MCP 工具，或检查常见 MCP 配置文件（opencode.json / claude_desktop_config.json / cursor mcp.json 等） | 降级为 agent-browser 方式或跳过 DeepWiki |
| E-5 | agent-browser skill | 检查 skill 文件是否存在 | DeepWiki 降级为不可用，code-analysis 依赖本地文档 |
| E-6 | 参考文档 | 检查 `references/` 下文件 | 各 skill 引用参考文档时自动跳过，不影响主流程 |

### Step 3: 环境能力评级

根据检查结果，输出当前环境的能力等级：

| 等级 | 条件 | 能力 |
|------|------|------|
| 🟢 **完整** | 所有必须项 + 3 个以上增强项通过 | 完整 subagent 编排 + 知识库 + MCP + PR 自动化 |
| 🟡 **标准** | 所有必须项通过 + 部分增强项 | subagent 编排 + 部分数据源，部分阶段需手动 |
| 🟠 **基础** | 必须项通过 + 无增强项 | 串行模式 + 本地文档，无知识库增强 |
| 🔴 **不可用** | 必须项未通过 | 需修复后重试 |

### Step 4: 自动修复（对可修复项执行）

以下项可以由 AI 直接修复，修复前向用户确认：

| 修复项 | 操作 |
|--------|------|
| 创建缺失目录 | `mkdir -p docs/features/ analysis/ references/ assets/templates/` |
| 生成 .env 模板 | 创建 `.env` 文件（`GITCODE_TOKEN=你的Token`），提示用户填入 |
| 生成 MCP 配置模板 | 根据用户使用的 AI 工具（OpenClaw / Cursor / Claude Desktop / opencode 等）生成对应的 MCP 配置，提示用户确认 |
| 检测运行模式 | 自动设置模式 A 或模式 B |

### Step 5: 输出环境报告

```markdown
# 🔍 ArkWeb SDD 环境预检报告

**项目根目录**: /path/to/project
**检查时间**: YYYY-MM-DD HH:MM
**环境等级**: 🟢 完整 / 🟡 标准 / 🟠 基础

## 必须项（P-1 ~ P-4）
| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| P-1 | Skill 文件 | ✅/❌ | 11/11 完整 / 缺少: xxx |
| P-2 | 产出物目录 | ✅/❌ | 自动创建完成 |
| P-3 | 模板文件 | ✅/❌ | 6/6 完整 / 缺少: xxx |
| P-4 | Agent 能力 | ✅ 模式A / ⚠️ 模式B | subagent 可用 / 串行模式 |

## 增强项（E-1 ~ E-6）
| # | 检查项 | 状态 | 降级方案 |
|---|--------|------|---------|
| E-1 | GitCode Token | ✅/⚠️ | 已配置 / Phase 9 需手动 |
| E-2 | chromium-knowledge | ✅/⚠️/❌ | 可访问 / 无Token / 降级DeepWiki |
| E-3 | oh-ai-full-design | ✅/⚠️ | 可访问 / 无权限（正常） |
| E-4 | DeepWiki MCP | ✅/⚠️ | 可用 / 降级浏览器或跳过 |
| E-5 | agent-browser | ✅/⚠️ | 可用 / 跳过DeepWiki浏览器方式 |
| E-6 | 参考文档 | ✅/⚠️ | 文件完整 / 部分缺失 |

## 自动修复记录
- [x] 创建 docs/features/ 目录
- [x] 创建 analysis/ 目录
- [ ] .env 模板已生成，请填入 GITCODE_TOKEN 或 GITLAB_TOKEN

## 数据源优先级（基于当前环境）
code-analysis 将使用：🥇 xxx → 🥈 xxx → 🥉 xxx

## 建议
- （如果环境不是 🟢 完整，列出改进建议）
```

## 在主流程中的位置

```
Phase 0 (可选) ─ preflight 环境检查
     │ 用户主动触发，非必须
     ▼
Phase 1 ─ proposal（需求录入）
     │ 主流程开始
     ▼
  ... Phase 2-9 ...
```

**触发方式：**
- 用户说"检查环境"/"preflight"/"帮我检查配置"
- AI 在主流程 Phase 1 开始前主动询问"是否需要检查环境？"

**不触发的情况：**
- 用户直接说"开始需求分析"→ 跳过 Phase 0，直接 Phase 1
- 用户明确说"跳过检查"→ 忽略

## 与 architect 的集成

在 `arkweb-architect/SKILL.md` 的 Phase 1 之前，可选添加：

```
### Phase 0（可选）: 环境预检

当用户首次使用、切换环境、或主动要求时，读取 `.skills/arkweb-preflight/SKILL.md` 执行环境检查。

主 Session:
  1. 询问用户"是否需要检查工作环境？"
  2. 用户确认 → 读取 preflight skill 并执行检查
  3. 用户跳过 → 直接进入 Phase 1
```

## 注意事项

- **不修改任何已有 skill 的流程**，仅作为可选前置
- 检查结果**不作为门禁**，用户可以忽略警告直接启动主流程
- 自动修复操作需要**用户确认**后才执行
- 环境报告保存在项目根目录 `preflight-report.md`（可选）
