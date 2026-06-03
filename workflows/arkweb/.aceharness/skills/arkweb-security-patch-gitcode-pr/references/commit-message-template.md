# Commit Message Template

用途：进入 git 历史并显示在 GitCode commit 页面。commit 页面只展示 git commit message、commit hash 和 diff，不等同于 PR body。

## 字段要求

| 字段 | 要求 |
|------|------|
| GitCode Issue 编号 | 可写在 `Issue:`，但不能替代 Chromium issue/CVE |
| Chromium 漏洞 issue | 必须写完整链接 `https://issues.chromium.org/issues/<issue_id>`，不能只写裸 issue id |
| CVE | 如果存在，必须写完整 `CVE-YYYY-NNNN...` |
| 修复 PR/CL/commit | 必须写 |
| 引入 bug PR/CL | 不作为 `Upstream` 修复来源 |
| 漏洞详细描述 | 必须中文优先写清楚触发点、漏洞成因、攻击或绕过方式、修复方式 |
| 安全专项分析 | 简要提炼影响分析中的漏洞类别、攻击面、触发条件、安全边界影响和未修复后果 |
| 影响版本/分支 | 写摘要和依据，至少包含 FoundIn/Milestone/修复 CL 或 commit 证据 |
| ArkWeb 当前工程结论 | 写 affected/unaffected/unknown、判定原因和相对源码依据 |
| 责任田/特性树 | 必须写责任田、归属理由和影响特性树；优先来自 `03_impact_decision.*` |
| Signed-off-by | 必须由 `git commit -s` 自动追加；name/email 必须来自当前提交仓库的 `git config user.name` 和 `git config user.email` |
| Co-Authored-By | 必须固定写 `Co-Authored-By: Agent` |
| PR `IssueNo`/评审模板字段 | 不在 commit 中承载 |
| 本机路径/`.ace-outputs`/`run-*`/本地归档文件名/token | 禁止 |
| 完整工作流报告 | 禁止 |
| 批量处理信息 | 禁止；commit message 只写当前 Chromium issue 的公开摘要 |

## 批量模式边界

如果输入来自批量归档目录，每个 issue 仍然必须生成独立分支、独立提交和独立 PR。当前 commit message 只能来自当前 issue 的材料。

- 不得引用 `00_batch_plan`、`batch_status`、根目录批量总结或其它 issue 目录。
- 不得写批量统计、批量失败清单、批量处理顺序、其它 issue 的 CVE/commit/PR、overlap 总览或跨 issue 合并建议。
- 引入 bug PR/CL 只能作为当前 issue 的根因/版本证据，不得作为当前提交的上游修复来源。

## 模板

```text
[ArkWeb][安全] 修复 <CVE-or-Chromium-issue> <中文漏洞摘要>

GitCode Issue: #<gitcode-issue-number>
Chromium Issue: https://issues.chromium.org/issues/<chromium-issue-id>
CVE: <CVE-YYYY-NNNN or N/A>
上游修复: <chromium-cl-or-commit>
Change-Id: <upstream-change-id-if-any>

漏洞详细描述:
- 触发点/受影响功能: <例如 WebUI webview executeScript/addContentScripts 文件脚本加载>
- 漏洞成因: <说明缺失的校验、错误的信任边界或绕过条件>
- 安全影响: <说明可能导致的跨源读取、脚本注入、权限绕过等公开影响>
- 修复方式: <说明上游修复增加了什么校验或限制>
- 安全专项结论: <漏洞类别、攻击面、触发条件和未修复后果的简要公开摘要>

影响分析:
- Chromium 影响范围: <受影响 milestone/branch 结论和 issue/PR 依据>
- ArkWeb 当前工程结论: <affected|unaffected|unknown，附源码路径/符号级简要依据，只写相对路径>
- 责任田: <ownership team>
- 责任田归属理由: <why this team owns the issue>
- 影响特性树: <feature-tree paths>
- 五性/RAM/ROM: <stability/security/performance/compatibility/business logic/RAM/ROM summary>
- 测试建议: <security regression, compatibility regression, automation suggestions>

上游修复判定:
- 修复 CL/commit: <why the selected Chromium CL/commit is the fixing change>
- 非引入 bug PR/CL 依据: <如有引入 bug PR/CL，说明它只作为根因/版本证据>

ArkWeb 适配:
- 修改范围: <relative changed files>
- 适配摘要: <short summary of local code changes>

Co-Authored-By: Agent
```

提交时使用：

```bash
git commit -s -F "$commit_msg"
```

`Signed-off-by: <git config user.name> <git config user.email>` 由 `git commit -s` 自动追加，不要在 `$commit_msg` 中手工写入。

## 校验

提交前必须从当前提交仓库读取签名信息，缺失则停止：

```bash
SIGNOFF_NAME=$(git config user.name)
SIGNOFF_EMAIL=$(git config user.email)
test -n "$SIGNOFF_NAME" -a -n "$SIGNOFF_EMAIL"
```

必须检查 DCO：

```bash
git log -1 --format=%B | grep -Eq '^Signed-off-by: .+ <.+>$'
```

必须检查固定协作者行：

```bash
git log -1 --format=%B | grep -Fxq 'Co-Authored-By: Agent'
```

如果前序材料存在 CVE，必须检查 CVE：

```bash
git log -1 --format=%B | grep -Eq 'CVE-[0-9]{4}-[0-9]+'
```

必须检查上游 Chromium issue 是完整链接：

```bash
git log -1 --format=%B | grep -Eq 'https://issues\.chromium\.org/issues/[0-9]+'
```

脱敏检查：

```bash
git log -1 --format=%B | grep -E '(^|[[:space:]])/(home|tmp|var|mnt)/|\.ace-outputs|run-[0-9]{12,}|00_batch_plan|batch_status|13_batch_summary|批量统计|批量失败|批量处理顺序|overlap 总览|blocked_overlap_conflict|03_impact_decision\.md|04_final_archive\.md|13_final_report\.md|12_submit_result\.md|Source archive file|Input issue archive directory|Workflow execution facts|target subrepo|GITCODE_TOKEN|gitcode-askpass'
```

命中即停止，修正 commit message 后再 push。
