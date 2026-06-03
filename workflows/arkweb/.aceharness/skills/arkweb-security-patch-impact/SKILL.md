---
name: arkweb-security-patch-impact
description: Determine whether ArkWeb M144 or configured baseline is affected by an upstream Chromium vulnerability.
metadata:
  descriptionZH: ArkWeb 影响判定技能。基于 ArkWeb/Chromium 基线、源码路径和修复版本判断是否受影响。
  tags: [ArkWeb, security, impact, Chromium]
---

# ArkWeb Impact Analysis

用于 `arkweb-security-patch-impact-decider`。

## When to use this skill

Use this skill after issue analysis and patch fetch are complete. It maps upstream fix facts to the configured ArkWeb baseline and produces the final affected/unaffected/unknown decision, ownership routing, feature impact, risk and test recommendations.

## 输入

- `.ace-outputs/{runId}/{issue_id}/01_issue_analysis.md`
- `.ace-outputs/{runId}/{issue_id}/01_issue_analysis.json`
- `.ace-outputs/{runId}/{issue_id}/02_patch_fetch.md`
- `.ace-outputs/{runId}/{issue_id}/02_patch_fetch.json`
- 可选 ArkWeb 本地仓库路径：仅当当前 workflow context 中的 `context.automation.repoPath`、`context.codebase` 或 `context.projectRoot` 任一字段显式配置时使用，按该顺序选择第一个非空有效路径。
- 默认责任田配置：[references/team_definition.yaml](references/team_definition.yaml)
- 默认特性树配置：[references/feature_tree_list.txt](references/feature_tree_list.txt)
- 如果 `context.requirements` 指定了项目专属责任田或特性树配置，优先使用用户指定配置；否则使用上述默认 references。
- 影响分析字段模板以内置 skill 说明为准，不依赖外部参考目录。

## 分析入口

影响分析必须从三块证据入手，并按顺序收敛结论：

1. Issue 证据：读取 `01_issue_analysis.*` 中从本地 HTML/MHTML 提取的 issue 字段、标签、评论时间线、Milestone、FoundIn、Merge-Request、Merge-Approved、Merged、FixedIn、修复线索和安全属性，用于判断上游问题背景、版本信号和信息缺口。
2. PR/CL 证据：读取 `02_patch_fetch.*` 中确认的 selected fix、Gerrit/Gitiles/PR/commit、patch、modified_files，并核验修复实际落在哪些分支；这里决定主线修复、cherry-pick、release branch、branch-head、requested/approved/merged 等状态。
3. 项目根目录代码证据：基于当前 workflow context 中的 `context.codebase` 检查当前工程代码，确认对应文件、符号、调用链、编译开关、平台裁剪或等价实现是否存在；这里决定当前 ArkWeb 工程是否受影响。

最终报告必须把结论依据写成这三块证据链：`Issue -> PR/CL -> context.codebase 源码核验 -> ArkWeb 影响结论`。

## 输出

写入同一个 issue 目录：

- `.ace-outputs/{runId}/{issue_id}/03_impact_decision.md`
- `.ace-outputs/{runId}/{issue_id}/03_impact_decision.json`

根目录不得写任何文件；不得生成 `03_impact_decision.index.md/json` 或根级 `03_impact_decision.md/json`。

Detailed output structure is in [references/impact-output.md](references/impact-output.md).

必须覆盖：

1. Chromium 上游影响版本结论：明确列出该漏洞/修复影响哪些 Chromium milestone、分支或版本范围，无法精确到版本时必须说明 `unknown`。
2. Chromium 版本结论依据：引用 issue 元数据、merge/milestone 标签、修复 CL/commit、branch-head、release note、提交时间或 patch 所在分支等证据，区分事实、推断和缺口。
   - `Milestone` / `M-*` / `Target-*` 表示目标修复里程碑或希望解决的版本，不能单独等同于“已影响版本”或“已修复版本”。
   - `Labels` 是标签集合，必须按具体标签含义拆解；`Type-*`、`Security_Severity-*`、组件标签不能直接推出版本影响结论。
   - `FoundIn-*` 表示已确认受影响的 milestone；存在多个时，最早的 `FoundIn-*` 是受影响起点的重要证据。
   - `Merge-Request-*` / `Request-*` 只表示请求回合到对应 milestone 分支，不表示已批准或已落地。
   - `Merge-Approved-*` / `Approved-*` 表示回合请求已批准，不表示 cherry-pick 已提交到分支。
   - `Merged-*`、branch-head 上的 cherry-pick commit、或修复 CL 在对应 release branch 的提交记录，才可作为“该分支已修复”的强证据。
   - `FixedIn-*` 只能作为辅助信号，必须结合修复 CL/PR 实际合入分支、commit message、cherry-pick 来源或 branch-head 证据交叉验证。
3. PR/CL 分支合入核验：基于 `02_patch_fetch.json` 中的 selected fix、Gerrit/Gitiles/PR/commit 链接和 patch 元数据，确认主线提交、cherry-pick 提交、目标 branch-head 或 release branch；不得只凭 issue 标签下最终版本结论。
4. 当前 ArkWeb 基线与上游修复版本的相对关系。
5. 基于当前 workflow context 中的 `context.codebase` 做本地工程源码核验，检查 `02_patch_fetch.json.modified_files[]` 对应的文件、符号、调用链、编译开关、平台裁剪或等价实现是否存在。
6. 明确 ArkWeb 当前工程结论：`affected`、`unaffected`、`unknown` 三选一，并说明它与 Chromium 版本影响范围之间的关系。
7. 每个关键结论都必须写出依据链：`Issue 证据 -> PR/CL 实际合入分支或缺口 -> 当前 ArkWeb 源码核验证据 -> 结论`。
8. 受影响模块、产品面、安全、兼容性、稳定性、性能、RAM、ROM、业务逻辑正确性风险。
9. 责任田归属：团队名必须从可用责任田配置的合法团队名中原样复制。
10. 影响的特性：必须从可用特性树配置中原样复制完整行，格式为 `团队名 > 一级业务特性 > 二级业务特性 > 三级业务特性`，禁止自造路径。
11. 修复优先级、修复复杂度、是否建议保留、是否需要测试和测试建议。
12. 若 issue 安全相关，必须输出安全专项影响分析：漏洞类别、攻击面、触发条件、可利用性、权限/沙箱/隐私/证书等安全边界、未修复后果、风险等级依据和安全测试建议。
13. 若判定不受影响，必须给出可审计证据；安全相关 issue 还必须说明安全链路为何不可达、对应代码为何不存在或平台为何不暴露。

Team and feature routing rules are in [references/team-feature-routing.md](references/team-feature-routing.md).
Use [references/team_definition.yaml](references/team_definition.yaml) and [references/feature_tree_list.txt](references/feature_tree_list.txt) as the default routing data.

## Scripts

可优先使用本次归档 workflow 已验证逻辑沉淀出的脚本生成 `03_impact_decision.md/json`，不要在运行时重新生成临时 Python 脚本：

```bash
python3 skills/arkweb-security-patch-impact/scripts/generate_impact_decision.py \
  --project-root <context.codebase> \
  --output-root <context.projectRoot>/.ace-outputs/<runId> \
  --feature-tree skills/arkweb-security-patch-impact/references/feature_tree_list.txt
```

脚本会读取 `<context.projectRoot>/.ace-outputs/<runId>/{issue_id}` 中的 `01_issue_analysis.json` 和 `02_patch_fetch.json`，写回同目录 `03_impact_decision.md/json`。脚本输出目录使用 `context.projectRoot`，源码核验使用 `context.codebase`；脚本只做路径命中、版本证据整理、责任田/特性树初判和安全专项骨架，agent 必须继续复核版本分支、源码语义和安全影响，不能把脚本输出当作免审最终结论。

字段归属边界：

- 本阶段必须先给出 Chromium 上游影响版本范围和依据，再结合 `context.codebase` 的当前工程源码给出 ArkWeb 影响结论。
- 本阶段必须复核前两步产物中已经定位的 PR/CL/commit 实际合入分支；允许补充验证分支、commit 和 cherry-pick 关系，但不得重新选择另一个主修复 patch。
- 本阶段必须填：ArkWeb 影响结论、五性/RAM/ROM/业务正确性判断、责任田、特性树、风险级别、保留建议、测试建议。
- 本阶段只读取前两步产物作为事实依据，不重抓 patch，不重写 patch 文件列表。

## 注意

- 必须从 Web 页面需求描述 `context.requirements` 中解析“是否强制合入：是/否”。如果解析为“是”，仍要如实写出真实 `arkweb_impact` 和证据链，但必须在 `03_impact_decision.json` 中写入 `merge_policy.force_merge=true`、`merge_policy.impact_mode=force_affected`、`merge_policy.source=requirements` 和原因；如果解析为“否”，必须写入 `merge_policy.force_merge=false`。
- 不要只凭版本号下结论；需要结合文件路径、编译开关、ArkWeb 适配层差异。
- 不要只凭 `Milestone`、`Merge-Request-*`、`Merge-Approved-*`、`FixedIn-*` 单项信息下版本结论；必须结合 PR/CL 实际合入分支和当前工程源码证据。
- 不得把 `context.automation.repoPath` 为空单独等同于未配置本地仓库路径；必须继续检查 `context.codebase`。
- 未显式配置 ArkWeb 本地仓库路径时，不得访问、引用或猜测任何固定本机 ArkWeb 路径；涉及本地代码存在性、patch apply/reverse-check 的结论应标记为 `unknown` 或待验证。
- 安全相关 issue 不能只写“安全性相关：是/否”，必须结合 ArkWeb 暴露面、补丁修改路径和运行时边界给出专项分析。
- `归属团队` 必须精确匹配可用责任田配置中的合法团队名。
- `影响的特性` 必须从可用特性树配置中原文复制完整行。
