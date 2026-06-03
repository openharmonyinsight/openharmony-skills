---
name: arkweb-security-patch-fetch
description: Fetch and normalize the exact upstream Chromium security patch for ArkWeb integration.
metadata:
  descriptionZH: ArkWeb 上游补丁抓取技能。只抓取明确目标修复 commit/CL，不补抓依赖 patch，不混入无关 PR。
  tags: [ArkWeb, patch, Chromium, Gerrit]
---

# ArkWeb Patch Fetch

用于 `arkweb-security-patch-fetcher`。

## When to use this skill

Use this skill after vulnerability intake has selected upstream fix PRs/CLs. It fetches or locates the exact patch files and modified file list used by later ArkWeb impact and merge stages.

## 输入

- `.ace-outputs/{runId}/{issue_id}/01_issue_analysis.md`
- `.ace-outputs/{runId}/{issue_id}/01_issue_analysis.json`
- 其中 `upstream_fix_prs[]` 是唯一可信入口；不要重新从相似标题或相同目录扩展抓取范围。

## 输出

写入同一个 issue 目录：

- `.ace-outputs/{runId}/{issue_id}/02_patch_fetch.md`
- `.ace-outputs/{runId}/{issue_id}/02_patch_fetch.json`
- patch 文件归档到 `.ace-outputs/{runId}/{issue_id}/patches/`

根目录不得写任何文件；不得生成 `02_patch_fetch.index.md/json` 或 `.ace-outputs/{runId}/patches/`。

Detailed output structure is in [references/patch-fetch-output.md](references/patch-fetch-output.md).

## Scripts

优先使用内置脚本抓取和校验 patch，不要在运行时重新生成临时 Python 脚本：

```bash
python3 skills/arkweb-security-patch-fetch/scripts/fetch_chromium_patch.py \
  --project-root <context.codebase> \
  --output-root <context.projectRoot>/.ace-outputs/<runId>
```

可选参数：

- `--issue-id <issue_id>`：只处理单个 issue；
- `--offline`：不联网，只根据 `upstream_fix_prs[]` 生成可复现抓取命令和阻塞说明。

脚本能力：

- 扫描 `{issue_id}/01_issue_analysis.json`；
- 强制输出目录只能是 `<context.projectRoot>/.ace-outputs/<runId>`，不能写到 ACEHarness run 日志目录；真实 ArkWeb 源码根使用 `context.codebase`；
- 只使用 `upstream_fix_prs[]` 的第一个主修复候选，后续候选写入 `excluded_candidates[]`；
- 支持 Chromium Gerrit CL 和 Gitiles commit patch URL；
- 将 patch 写入 `{issue_id}/patches/`，并生成 `02_patch_fetch.md/json`；
- 对 patch 内容做标准 diff 签名校验，避免 HTML、JSON metadata 或错误页被当成 patch。

裁决阶段可用独立校验脚本复查已有 `patch_files[]`：

```bash
python3 skills/arkweb-security-patch-fetch/scripts/validate_patch_files.py \
  --project-root <context.codebase> \
  --output-root <context.projectRoot>/.ace-outputs/<runId>
```

字段归属边界：

- 本阶段必须填：确认的主修复 PR/CL、修改文件列表、本地 patch 文件、抓取命令、候选排除理由。
- 本阶段不得重写：Issue 基础字段、上游修复 PR/CL 的语义审计结论。
- 本阶段不得填最终值：ArkWeb affected/unaffected、责任田、特性树影响、是否建议保留。

## 规则

- 优先直接获取 issue、upstream CL 或 PR 中明确指定的那个主修复。
- 不要补抓任何依赖 patch，哪怕它们在上游里被提及；只保留当前主修复本体。
- 不要把相似标题、同组件、同目录、同作者的其他 CL / PR 当成修复 patch。
- 不要把没有被主修复显式引用的候选 patch 混进结果里，哪怕它们看起来相关。
- 必须区分修复 PR/CL 和引入 bug 的 PR/CL；`culprit`、`bisect`、`introduced by`、`caused by`、`regression range`、`first bad` 等语义指向的 PR/CL 只能作为根因或版本范围证据，不得作为 patch 抓取对象。
- 如果 `upstream_fix_prs[]` 中的候选看起来是 bug-introducing PR/CL 而不是修复 PR/CL，必须在 excluded_candidates[] 记录并阻塞抓取，不得下载其 patch 当作修复。
- 如果当前主修复无法单独确认或无法直接获取，就明确失败，不要用其他 patch 补齐。
- 无法联网时，记录失败命令和需要人工提供的精确 patch 链接。
- 不要把不确定的 CL 当成修复 patch。
- 如果网络可用，Gerrit CL 可优先尝试 `https://chromium-review.googlesource.com/changes/{project}~{cl}/revisions/current/files` 获取文件列表，patch 可尝试 `.../revisions/current/patch?download` 或 Gerrit 下载链接；失败时记录 HTTP 状态和命令。
- patch 文件下载后必须做内容校验，不能只看 HTTP 命令返回、文件存在或文件大小：
  - 有效 `.patch/.diff` 必须包含标准 diff 信号之一：`diff --git`、`Index:`、`--- a/` + `+++ b/`、或 mbox patch 的 `From <hash>` + `Subject:` + diff hunks；
  - 如果内容是 HTML 错误页、`<!DOCTYPE html>`、`<html`、HTTP 错误文本、Gerrit/Gitiles 错误页、`)]}'` JSON metadata，必须标记为 invalid patch；
  - metadata JSON 只能作为 commit/file-list 辅助产物，不能填作可用 patch；
  - 只有通过内容校验的 patch/diff 文件才能在 `02_patch_fetch.md/json` 中写为“patch 已归档/可进入后续阶段”。
