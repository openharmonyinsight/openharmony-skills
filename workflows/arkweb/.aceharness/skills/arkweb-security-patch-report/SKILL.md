---
name: arkweb-security-patch-report
description: Produce final ArkWeb archive or auto merge report from workflow outputs.
metadata:
  descriptionZH: ArkWeb 最终报告技能。区分集成工作流中的分析归档状态和结果归档状态。
  tags: [ArkWeb, report, archive]
---

# ArkWeb Final Report

用于 `arkweb-security-patch-report-writer`。

## When to use this skill

Use this skill in either report state of:

- `ArkWeb 本地 Issue 分析归档与上游安全补丁自动合入`

## 输入

本技能支持同一集成工作流里的两种报告模式，必须先根据当前状态任务或已有产物判断报告模式，不能混用要求。

### 模式 A：分析归档状态

只汇总本地 issue 解析、patch 抓取、影响判定和归档产物：

- 需求描述中给出的输入 issue 归档目录
- 当前 issue 目录里的 `01_issue_analysis.*`、`02_patch_fetch.*`、`03_impact_decision.*`、`04_final_archive.md/json`、`summary.*` 和 `patches/`

本模式尚未包含自动合入、冲突解决、代码审查、编译验证、编译修复、风险评估、提交上库或 GitCode PR。报告中不得把“未自动合入”“未编译测试”“未提交上库”写成最终未完成项、失败原因、风险或缺口；这些属于本工作流后续状态。

### 模式 B：结果归档状态

汇总既有归档输入和后续合入/验证/提交产物：

- 输入归档目录里的 `01_issue_analysis.*`、`02_patch_fetch.*`、`03_impact_decision.*`、`04_final_archive.md/json` 和 `patches/`
- 当前运行产物 `06_merge_result.md`、`07_conflict_resolution.md`、`08_code_review.md`、`09_build_verification.md`、`10_build_fix.md`、`11_risk_assessment.md`、`12_submit_result.md`
- 批量模式额外汇总 `00_batch_plan.md/json`、`batch_status.md/json`、`issues/{issue_id}/06_merge_result.md`、`issues/{issue_id}/09_build_verification.md`、`issues/{issue_id}/11_risk_assessment.md`、`issues/{issue_id}/12_submit_result.md`

## 输出

模式 A 写入每个 issue 目录：

- `.ace-outputs/{runId}/{issue_id}/04_final_archive.md`
- `.ace-outputs/{runId}/{issue_id}/04_final_archive.json`
- `.ace-outputs/{runId}/{issue_id}/summary.md`
- `.ace-outputs/{runId}/{issue_id}/summary.json`

模式 A 可先使用内置汇总脚本收集现有产物，避免运行时生成临时汇总脚本：

```bash
python3 skills/arkweb-security-patch-report/scripts/collect_archive_summary.py \
  --project-root <context.codebase> \
  --output-root <context.projectRoot>/.ace-outputs/<runId>
```

该脚本只读取 `01/02/03` 阶段已有 JSON 并向 stdout 输出汇总，不向运行根目录写文件，不重新生成漏洞事实、patch 文件列表或影响结论；agent 仍需基于汇总和各 issue 目录产物写出每个 issue 的 `04_final_archive.*` 与 `summary.*`。

也可使用已验证的归档生成脚本直接为每个 issue 写最终报告：

```bash
python3 skills/arkweb-security-patch-report/scripts/generate_final_archive.py \
  --project-root <context.codebase> \
  --output-root <context.projectRoot>/.ace-outputs/<runId> \
  --issue-archive-root <local_issue_archive_dir>
```

该脚本只写 `<context.projectRoot>/.ace-outputs/<runId>/{issue_id}` 子目录下的 `04_final_archive.md/json` 与 `summary.md/json`，不得写运行根目录文件，也不得写到 `~/.aceharness/runs/<runId>/outputs/.ace-outputs`；源码根使用 `context.codebase`。

模式 B 写入运行根目录：

- `.ace-outputs/{runId}/13_final_report.md`
- 可选 `.ace-outputs/{runId}/13_final_report.json`

批量模式还必须写入：

- `.ace-outputs/{runId}/issues/{issue_id}/13_final_report.md`
- 可选 `.ace-outputs/{runId}/13_batch_summary.json`

必须包含：

模式 A 必须包含：

1. 本地 issue 归档目录、实际处理的 HTML/MHTML 文件、issue id 和标题。
2. 漏洞/缺陷摘要、可信度、上游修复 PR/CL。
3. patch 抓取结果、patch 文件有效性、修改文件列表和缺失工件。
4. Chromium 上游影响版本结论与依据。
5. 当前 `context.codebase` 工程影响结论、源码证据、责任田、影响特性、五性/RAM/ROM、是否建议保留、是否需要测试。
6. 安全相关 issue 的安全专项影响摘要。
7. 人工核查建议和后续工作建议。只能写“如需合入/编译/提交，请进入自动合入工作流”，不得写成本工作流失败或未完成。
8. JSON 摘要块。

模式 B 必须包含：

1. 输入归档目录、issue id、上游修复 PR/CL、patch 文件和允许修改文件列表。
2. 自动合入结果、冲突解决结果、最终变更文件。
3. 代码审查结论。
4. 编译验证和编译修复结果。
5. 风险评估摘要。
6. 提交 / 上库结果、commit id、fork 分支、GitCode PR 链接或失败原因。
7. 未解决问题、后续建议、回滚建议。
8. JSON 摘要块。

模式 B 批量输入时还必须包含：

1. 批量输入 run 目录、总 issue 数、ready/blocked/submitted/failed 统计。
2. 每个 issue 一行汇总：issue_id、CVE、影响判定、目标子仓、duplicate_files/overlap、commit、fork 分支、GitCode Issue、PR、start build 评论结果、最终状态。
3. duplicate_files/overlap 文件清单；必须列出每个重复文件组的关联 issue、winner_issue_id 和 loser issue。winner issue 按正常 active batch 结果归档；涉及重复文件而未进入 active batch 的 loser issue 必须列为“遗留 issue”，说明重复文件、关联 issue、winner_issue_id、未自动合入原因和后续人工处理建议；如果存在 `blocked_overlap_conflict`，列为人工处理项。
4. 每个 issue 独立 commit/PR 的确认；不得把多个 issue 的提交结果合并成一个“批量提交”描述。
5. 成功 issue 与失败 issue 分开列；失败 issue 必须保留失败阶段、失败原因、下一步建议。

字段归属边界：

- 本阶段只聚合和归档，不重新生成漏洞事实、patch 文件列表或影响结论。
- 必须忠实引用当前工作流已有产物，不得伪造未执行结果。
- 模式 A 不得要求或总结自动合入、编译验证、提交上库结果；这些属于本集成工作流的后续状态。
- 模式 B 必须引用前序合入、编译、风险、提交产物；缺失时按自动合入工作流缺失项处理。
- 模式 B 批量输入时，根报告是总览，不得替代每个 issue 的独立报告；每个 issue 的 GitCode 提交、PR 和门禁状态必须独立呈现。
- 不得重新生成本地 issue 分析归档产物；不得写 `01_issue_analysis.*`、`02_patch_fetch.*`、`03_impact_decision.*`、`04_final_archive.*`、`summary.*` 或 `patches/`。
- 若输入归档目录缺少某阶段产物或 patch 文件，在最终报告中列明缺失项。
