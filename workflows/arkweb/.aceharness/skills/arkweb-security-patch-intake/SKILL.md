---
name: arkweb-security-patch-intake
description: Parse ArkWeb security issue inputs such as CVE, Chromium bug, Gerrit CL, PR, and advisory links into an auditable vulnerability intelligence report.
metadata:
  descriptionZH: ArkWeb 漏洞情报解析技能。把 CVE、Chromium issue、Gerrit CL、PR、安全公告解析成结构化漏洞情报报告。
  tags: [ArkWeb, security, vulnerability, Chromium]
---

# ArkWeb Vulnerability Intake

用于 `arkweb-security-patch-issue-analyzer`。

## When to use this skill

Use this skill to parse local Chromium issue HTML/MHTML archives, issue links, CVE/security advisory text, Gerrit CLs, PRs, or commit messages into auditable issue analysis artifacts.

## 输入

- `context.requirements` 中的 issue / CVE / Chromium bug / Gerrit CL / PR / 安全公告链接。
- 已有 `.ace-outputs/{runId}` 报告或 `.ace-outputs/{runId}/{issue_id}/` 目录。
- 本地 issue HTML/MHTML 归档目录，由 `context.requirements` 指定；未指定时可使用当前工作流给出的默认输入目录。

## 输出

写入每个 issue 独立目录：

- `.ace-outputs/{runId}/{issue_id}/01_issue_analysis.md`
- `.ace-outputs/{runId}/{issue_id}/01_issue_analysis.json`

如果一次处理多个 issue，必须从本阶段开始就拆成多个 `{issue_id}` 目录。根目录不得写任何文件；不得生成 `01_issue_analysis.index.md/json`，也不得生成根级 `01_issue_analysis.md/json`。

Detailed output structure is in [references/issue-analysis-output.md](references/issue-analysis-output.md).

字段归属边界：

- 本阶段必须填：Issue 基础字段、原始描述、上游修复 PR/CL 链接、修复事件审计、初步问题/修复摘要。
- 本阶段不得填最终值：修改文件列表、patch 本地路径、ArkWeb affected/unaffected 结论、责任田、特性树影响、是否建议保留。

## Fix link extraction

Use semantic review of issue comments. Do not just regex all URLs. The extraction and deduplication rules are in [references/fix-link-extraction.md](references/fix-link-extraction.md).

## Scripts

优先使用内置脚本解析本地 HTML/MHTML 归档，不要在运行时重新生成临时 Python 脚本：

```bash
python3 skills/arkweb-security-patch-intake/scripts/parse_local_issue_archive.py \
  --archive-dir <local_issue_archive_dir> \
  --project-root <context.codebase> \
  --output-root <context.projectRoot>/.ace-outputs/<runId>
```

脚本能力：

- 只读扫描 `.html`、`.htm`、`.mhtml`、`.mht`，并可读取 `issue.zip` 里的同类文件到输出目录临时区；
- 强制输出目录只能是 `<context.projectRoot>/.ace-outputs/<runId>`，不能写到 `~/.aceharness/runs/<runId>/outputs/.ace-outputs`；`context.projectRoot` 是工作流输出根，真实 ArkWeb 源码根使用 `context.codebase`；
- 从 MHTML 中提取 HTML 正文，生成每个 issue 独立目录下的 `01_issue_analysis.md/json`；
- 按 fix-link 规则审计代码链接，区分 accepted fix、bug-introducing candidate 和普通 noise 链接；
- 只向 `{issue_id}` 子目录写产物，stdout 输出批量摘要，便于 agent 再做人工复核和补充。

如果脚本输出的 `upstream_fix_prs[]` 为空或 `decision=review` 较多，agent 再基于原始归档和审计表做语义复核；不要把脚本当成最终判断的唯一来源。

## 规则

- 不要臆造 CVE、commit 或文件路径。
- 对每个关键结论标注来源链接或来源文本。
- 无法访问外网时，明确写出阻塞原因和建议人工补充项。
- 本地 HTML/MHTML 原始文件只读，不要修改归档目录。
- 责任田和特性树只在本阶段读取作背景，不在本阶段做最终归属判定。
