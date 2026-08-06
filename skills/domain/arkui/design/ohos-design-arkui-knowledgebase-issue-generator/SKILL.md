---
name: ohos-design-arkui-knowledgebase-issue-generator
description: >-
  Generate, update, or repair ArkUI ace_engine issue-type knowledge-base documents under docs/kb/issues/. Use when the user says "生成问题KB", "补充问题知识库", "问题经验沉淀", "典型问题KB", "issue KB", "troubleshooting KB", "问题排查KB", or mentions adding historical/typical issue experience to the knowledge base. Covers analyzing issue patterns from bug reports, PR fixes, or user descriptions, producing a structured issue KB page, and registering it in context_registry.json.
metadata:
  author: openharmony
  scope: domain
  stage: design
  domain: arkui
  capability: knowledgebase-issue-generator
  version: 0.1.0
  status: trial
  tags:
    - arkui
    - ace-engine
    - knowledge-base
    - kb
    - issue
    - troubleshooting
    - root-cause-analysis
  related-skills:
    - ohos-design-arkui-knowledgebase-generator
---

# ArkUI Issue KB Generator

## Scope

This skill generates **issue-type knowledge-base pages** under `docs/kb/issues/` in the ace_engine repository. Issue KBs capture typical problem patterns, root cause analysis, and troubleshooting guidance — complementing the existing code-based KBs that provide source/API routing.

## Directory Layout

Issue KBs live alongside existing KB categories:

```text
docs/kb/
├── components/      # 对外 UI 组件 (code-based KB)
├── capabilities/    # 通用能力 (code-based KB)
├── architecture/    # 引擎架构 (code-based KB)
├── api/             # SDK、C API (code-based KB)
├── syntax/          # ArkTS 语法 (code-based KB)
├── issues/          # ★ 历史典型问题 (issue-based KB, NEW)
└── _generated/      # 可再生成索引页
```

Within `issues/`, subdirectories group by problem domain:

```text
docs/kb/issues/
├── layout/                  # 布局类问题
├── rendering/               # 渲染类问题
├── interaction/             # 交互类问题
├── state-management/        # 状态管理类问题
├── navigation/              # 导航类问题
├── lifecycle/               # 生命周期类问题
├── performance/             # 性能类问题
└── compatibility/           # 兼容性类问题
```

File naming: lowercase English slugs with hyphens, e.g. `measure-infinite-loop.md`.

## Workflow

**MANDATORY — READ ENTIRE FILE**: Before creating, updating, or repairing any issue KB, read [references/workflow.md](references/workflow.md) completely. It defines the mode determination (CREATE/UPDATE/REPAIR), information gathering, verification, information security check, registry updates, and validation.

## Issue KB Page Template

**MANDATORY — READ ENTIRE FILE**: Before writing any KB content, read [references/template.md](references/template.md) completely. It defines the page structure, context_registry.json entry shape, schema compatibility note, and change relationship taxonomy.

### Before Writing Any KB Content, Ask Yourself

- **Security**: Does this content contain partner-identifiable information, credentials, or internal references? Run the Information Security Check in workflow.md before writing to disk.
- **Coverage**: Is the coverage scope explicitly noted when only a single root cause or case is available? Do NOT fabricate additional content to meet an ideal count.
- **Verification**: Did I confirm code paths and function names against the current source tree, or am I echoing unverified claims?
- **Causality**: Are PR/Issue references labeled with explicit relationship values (introduced/fixed/related/unknown) rather than a flat "关联 PR / Issue"? See the change relationship taxonomy in template.md.

## Subdirectory Categories

Standard categories for `docs/kb/issues/`:

| 目录 | 类别 | 说明 | 典型问题举例 |
|------|------|------|-------------|
| `layout/` | 布局 | 布局算法、约束、测量、放置 | 测量死循环、布局未触发、安全区避让失败 |
| `rendering/` | 渲染 | 绘制、渲染上下文、图形 | 内容不显示、滚动模糊、闪烁 |
| `interaction/` | 交互 | 手势、事件、焦点 | 手势冲突、事件不响应 |
| `state-management/` | 状态管理 | V1/V2 状态、装饰器 | 状态更新不反映、V1V2 混用崩溃 |
| `navigation/` | 导航 | Navigation、路由 | 返回崩溃、转场闪烁 |
| `lifecycle/` | 生命周期 | 页面/组件生命周期 | onShow 不触发、自定义组件销毁泄漏 |
| `performance/` | 性能 | VSync、内存、帧率 | 卡顿、内存泄漏 |
| `compatibility/` | 兼容性 | API 版本、SDK 迁移 | API 行为变更、废弃迁移 |

If the user's issue doesn't fit these categories, create a new subdirectory with a lowercase English slug.

## Notes

- Issue KBs focus on **problem patterns** (not individual bugs). A single issue KB should cover a class of similar problems.
- Each issue KB should ideally have 2 or more root cause categories and 2 or more associated cases for richer coverage. However, a single verified root cause and a single verified case are sufficient to generate an initial KB — mark the coverage scope explicitly (e.g. "当前仅覆盖根因类别 A，后续补充 B/C"). Do NOT fabricate additional root causes or cases to meet the ideal count.
- Code paths and function names must be verified against the current source tree before writing.
- The `func_ids` array in context_registry.json links the issue KB to one or more FuncIDs for cross-referencing with spec and code KBs.
- Do not duplicate information already covered by a code-based KB; reference it via "相关主题" instead.
- Keep the KB concise — it's a navigation and pattern-recognition aid, not a full troubleshooting manual.
- Filter out commercial product names from issue scenarios — abstract into OpenHarmony-specific technical conditions only (e.g. "特定窗口尺寸变化/折叠态切换场景" instead of "XX伙伴 MatePad Pro 折叠态切换"). See the Information Security Check in workflow.md for the full checklist.

## Key Paths

| What | Path |
|------|------|
| Issue KB root | `docs/kb/issues/` |
| Registry | `docs/context_registry.json` |
| KB README | `docs/kb/README.md` |
| Search script | `docs/kb_search.py` |
| Validator | `docs/validate_context.py` |
