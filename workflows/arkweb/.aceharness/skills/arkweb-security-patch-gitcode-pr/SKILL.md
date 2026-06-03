---
name: arkweb-security-patch-gitcode-pr
description: "Submit ArkWeb Chromium security patches to GitCode with oh-gc: commit only intended patch files, push to a personal fork branch, create or confirm a GitCode Issue, create a PR to the configured upstream repo, and verify the PR is linked to the GitCode Issue. Use for ArkWeb security patch upstream submission after merge/apply analysis."
descriptionZH: ArkWeb GitCode PR 提交技能。用于 ArkWeb/Chromium 安全补丁上库：只提交目标 patch 文件，推送到个人 fork 分支，先创建或确认 GitCode Issue，再用 oh-gc 创建并关联上游 PR。
tags: [ArkWeb, GitCode, PR, Chromium]
---

# ArkWeb GitCode PR

用于 `arkweb-security-patch-submitter`。路径、目标仓库、目标分支必须来自工作流上下文或前序合入结果，不得在 skill 中写死个人本地路径。

## 必读引用

- 归档输入和符号链接处理：[references/archive-input-contract.md](references/archive-input-contract.md)
- 当前 issue 可提交文件集合：[references/submit-scope-contract.md](references/submit-scope-contract.md)
- GitCode Issue/commit/PR 流程：[references/pr-flow.md](references/pr-flow.md)
- 公开文本脱敏边界：[references/public-text-redaction.md](references/public-text-redaction.md)
- HTTP 413 / 大 pack 诊断：[references/http-413-diagnosis.md](references/http-413-diagnosis.md)
- 文案模板：
  - [references/gitcode-issue-template.md](references/gitcode-issue-template.md)
  - [references/commit-message-template.md](references/commit-message-template.md)
  - [references/pr-body-template.md](references/pr-body-template.md)

## 本 skill 脚本

所有脚本都在本 skill 的 `scripts/` 目录内，不跨 skill 调用：

```bash
node skills/arkweb-security-patch-gitcode-pr/scripts/resolve_archive_dir.mjs <archive-dir>
node skills/arkweb-security-patch-gitcode-pr/scripts/compute_submit_scope.mjs --merge-result <06_merge_result.json> --build-fix <10_build_fix.json>
node skills/arkweb-security-patch-gitcode-pr/scripts/preflight_commit_scope.mjs --repo <target-git-repo> --scope <submit_scope.json>
node skills/arkweb-security-patch-gitcode-pr/scripts/create_isolated_issue_commit.mjs --repo <target-git-repo> --scope <submit_scope.json> --base-ref <manifest_remote>/<targetBranch> --branch <fork-branch> --message-file <commit-message-file>
node skills/arkweb-security-patch-gitcode-pr/scripts/scan_existing_submit_targets.mjs --run-dir <.ace-outputs/runId> --repo <target-git-repo> --upstream-repo <owner/project> --fork-remote <fork-remote>
node skills/arkweb-security-patch-gitcode-pr/scripts/validate_public_text.mjs <commit_msg> <issue_body> <pr_body>
```

提交阶段禁止临时生成大段 shell/Python/Node 脚本替代上述脚本。若现有脚本缺能力，先补充本 skill 的
`scripts/`，再执行上库。

## 输入来源

优先读取当前 issue 的前序产物：

- `01_issue_analysis.*`
- `02_patch_fetch.*`
- `03_impact_decision.*`
- `04_final_archive.*`
- `issues/{issue_id}/06_merge_result.*`
- `issues/{issue_id}/09_build_verification.*`
- `issues/{issue_id}/10_build_fix.*`
- `issues/{issue_id}/11_risk_assessment.*`
- 当前目标 git 子仓中属于该 issue 的 diff

批量模式可读取 `00_batch_plan.*` 和 `batch_status.*` 只用于本地提交队列判断；不得把批量总览、其它 issue 信息、overlap 汇总写进当前 issue 的 GitCode Issue、commit message 或 PR body。

`deferred_for_archive` / overlap 非 winner issue 不属于提交队列；不得创建 commit、分支、GitCode Issue 或 PR。

## 目标仓库规则

- 提交仓库：前序合入结果中的目标 git 子仓。
- 上游仓库：优先使用 manifest project/remote 推导出的 `<owner>/<project>`。
- 常见映射：`src -> chromium_src`，`src/v8 -> chromium_v8`，`src/arkweb -> chromium_arkweb`。
- 目标分支：使用 `context.automation.gitcode.targetBranch`，未配置时才使用 `master`。
- PR 方式：个人 fork 分支到上游目标分支。
- 待推送范围基线：必须使用 manifest/upstream remote 的目标分支
  `<manifest_remote>/<targetBranch>`，例如 `tpc/master`；个人 fork remote
  只作为 push 目的地，不得用 `personal/master..HEAD` 作为最小提交范围判定。

## 硬规则

1. 每个 Chromium issue 对应一个 GitCode Issue、一个 commit、一个 fork 分支、一个 PR。
2. 禁止 `git add -A`、`git add .`、`git add -u`、`git commit -a`。
3. 禁止提交 SDK、toolchain、构建产物、压缩包、临时 patch、`.ace-outputs`、`src/out` 或无关脏改。
4. 无关脏改只能记录为忽略，不得清理、回滚、暂存或提交。
5. token 不得写入仓库文件、remote URL、commit message、PR body、Issue body 或报告正文。
6. GitCode Issue、commit message、PR title/body、`12_submit_result.md` 不得泄露本机路径、运行目录、本地归档文件名、临时目录、token 或完整工作流报告。
7. 提交到 GitCode 的公开材料优先中文，英文只作为字段名、上游链接或必要补充。
8. 必须写漏洞详细描述，不能只写一行 “Apply upstream Chromium security fix”。
9. Chromium issue 是漏洞来源；GitCode Issue 是上库流程 issue，不能混用编号。
10. GitCode Issue、commit message、PR title/body 中的上游 Chromium issue 必须写完整链接
    `https://issues.chromium.org/issues/<issue_id>`；不得只写裸 issue id。
11. PR body 和 GitCode Issue body 必须包含当前 issue 的影响分析摘要、责任田、责任田归属理由、
    影响特性树、五性/RAM/ROM 和测试建议；这些字段优先来自 `03_impact_decision.*`，缺失时才从
    `04_final_archive.*` 的 `ownership_and_quality` 补齐。缺字段不能直接省略，必须写“待确认”并说明证据缺口。
12. commit message 必须包含 `Signed-off-by:` 和固定行 `Co-Authored-By: Agent`；签名来自当前提交仓库的 `git config user.name/user.email`。
13. Cross-repo PR 的 `--head` 必须是 `forkOwner:branch`。
14. PR 创建并确认关联 GitCode Issue 后，必须评论 `start build` 并确认评论存在。
13. `upstream_patch_applied_exactly=false` 不直接失败；只要 `semantic_landed=true`、blockers 为空且本地适配记录完整，可以提交适配后的文件。
14. HTTP 413 或远端大 pack 拒绝时，按本 skill 的 HTTP 413 引用诊断，禁止重复盲推。
15. 不得因为 fork 目标分支落后或 `personal/master..HEAD` 很大而整批失败；只有
    manifest/upstream range、暂存区 scope、文件体积或实际 push 返回证明范围异常时，才阻塞对应 issue。
16. 批量工作树已包含多个 issue 的未提交总 diff，或当前 HEAD 已有其它 issue 提交时，必须使用
    `create_isolated_issue_commit.mjs` 从 manifest/upstream baseline 和当前 issue 白名单文件构造独立 commit；
    不得在污染分支上直接 `git commit`，不得切换/清理当前工作树，不得使用 git worktree。
17. 如果 push 被 Git LFS pre-push hook 报 `Unable to find source for object`，且当前 issue
    submit scope 没有 LFS 跟踪文件，必须用 `GIT_LFS_SKIP_PUSH=1` 对同一分支重试一次；这属于 fork/baseline
    LFS hook 问题，不得直接把整批标记为无法上库。
18. 如果 `personal/master..HEAD` 很大或与 manifest/upstream 无 merge-base，先确保个人 fork
    上存在指向 manifest/upstream baseline SHA 的临时基线分支（例如
    `aceharness-upstream-master-YYYYMMDD`）。可使用 `oh-gc branch create <base-branch>
    --repo <forkOwner>/<project> --ref <manifest_base_sha>`；基线分支创建成功后再 push issue 分支。
19. 批量模式必须逐 issue 推进。单个 issue push、Issue 或 PR 失败，只能标记该 issue
    `submit_failed` 并继续后续 ready issue；只有认证失效、网络不可达、配置缺失等会让所有 issue
    必然失败的共享基础设施问题，才允许停止整批。
20. push 前必须先执行 `scan_existing_submit_targets.mjs` 做远端幂等扫描，并把结果写入或引用到
    `12_submit_result.md`。扫描发现同一 issue 已有 open PR 时，必须直接复用，不得重新生成 commit、
    分支、GitCode Issue 或 PR。
21. 如果 fork 分支已经存在且指向本 issue isolated commit，不能重复停在 push；必须继续创建或复用
    GitCode Issue，并创建 PR、评论 `start build`。如果同名 fork 分支已存在但 commit 不一致，禁止盲目
    `git push`、禁止自动加 `-r2/-r3` 新分支、禁止强推；必须先查询是否已有 PR。无 PR 时标记
    `submit_failed(branch_exists_commit_mismatch)` 并记录远端 SHA、本地 isolated commit 和人工决策需求。
22. 批量恢复提交必须先做远端幂等扫描：按 issue id 查询已有 fork 分支和已有 PR。只要该 issue
    已存在 open PR 指向 `ringking0:<arkweb-security-{issue_id}-...>`，必须复用该 PR 并标记
    `submitted`，不得再生成新 commit、新分支、新 GitCode Issue 或新 PR。
23. 若已有 fork 分支但 PR 缺失，只能复用该分支创建 PR；不得为同一 issue 再创建第二个分支，除非原分支
    commit 与当前 issue scope 明确不一致并在结果文件中记录废弃原因。
24. 使用 `create_isolated_issue_commit.mjs` 时，当前工作树中的范围外脏改、未跟踪文件、SDK/toolchain
    删除或构建产物只作为 ignored_worktree_state 记录，不得阻塞当前 issue 提交；真正的提交对象只能由
    submit scope 白名单文件和 manifest/upstream baseline 构造。只有 submit scope 本身包含禁用路径时才阻塞。

## 输出

写入 `.ace-outputs/{runId}/12_submit_result.md`；批量模式还必须写入每个 issue 的 `issues/{issue_id}/12_submit_result.md`。

每个 issue 至少记录：目标 git 子仓、上游仓、目标分支、提交文件、commit id、fork 分支、GitCode Issue、PR、`start build` 评论结果、被忽略的无关脏改、失败原因或人工后续动作。
