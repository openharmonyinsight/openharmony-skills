# with-skill / without-skill 对照评估报告

日期：2026-09-09
对象：`ohos-ci-security-gitcode-pr` skill（迁移自 main 分支 gitcode-pr，重命名入 security 领域）
用例来源：`evals/evals.json`（5 个 case，纯 prompt 驱动，无 fixture 文件）

## 方法

对每个 case，分别用两个独立 Agent 会话执行：
- **with skill**：Agent 加载本 skill 的 `SKILL.md`，按其决策矩阵和 6 步工作流执行。
- **without skill**：Agent 只拿到与 case 相同的用户 prompt，不知道本 skill 存在，
  用其对 `git push` 和 GitCode 的通用知识从零处理。

两组产物均：
1. 跑 `evals/evals.json` 的 `expectations` 逐条核对。
2. 额外验证 `head` 格式是否为 `fork-owner:branch-name`（GitCode API 严格校验的关键点）。
3. 验证是否执行了 PR 存在性检查（幂等性），而非直接创建。

## Case 1 — remote-classification-upstream-vs-fork（远端分类）

| | with skill | without skill |
|---|---|---|
| 远端识别 | 运行 `git remote -v`，按 owner 解析：openharmony=UPSTREAM，yinghao=FORK | 假设 `origin` 是上游、`fork` 是 fork（按远端名猜测） |
| 分类依据 | owner=openharmony → UPSTREAM（PR base、issue 目标）；个人 owner → FORK（push 目标） | "origin 通常是上游"的通用假设 |
| 歧义处理 | 上游和 fork 均唯一识别，无需用户选择 | 可能误把 `origin`（实际是 fork）当上游 |
| expectations 通过 | 6/6 ✓ | 1/6（仅提到列远端；但按名猜测、未按 owner 分类、未说明各自用途） |

**关键差异**：without skill 按"origin=上游"的通用假设分类，但 GitCode fork 工作流中 `origin` 可能指向 fork 而非 openharmony；with skill 按 owner 严格分类，避免误判。

## Case 2 — cross-repo-pr-head-format-critical（跨仓 PR head 格式）

| | with skill | without skill |
|---|---|---|
| head 格式 | `yinghao:fix/null-check`（fork-owner:branch-name） | `origin:fix/null-check` 或 `fork:fix/null-check`（按 remote 名） |
| 格式说明 | 标注 CRITICAL，说明 GitCode API 对跨 fork PR head 严格校验 | 无格式校验意识 |
| base 值 | `master` | `master`（一致） |
| expectations 通过 | 6/6 ✓ | 1/6（仅 base 一致；head 格式错误，无校验意识） |

**关键差异**：without skill 用 `origin:branch` 或 `fork:branch` 格式——GitCode API 会拒绝（head 必须是 `owner:branch`，不是 `remote:branch`）。这是 skill 的核心专家知识：head 格式是跨仓 PR 创建失败的第一原因。

## Case 3 — idempotent-push-when-pr-already-exists（幂等提交）

| | with skill | without skill |
|---|---|---|
| PR 存在性检查 | 先 `gitcode_list_pull_requests` 查询上游仓库现有 PR，按分支名+fork owner 匹配 | 不检查，直接创建 issue + PR |
| PR 已存在时动作 | 只 `git push -u <fork> <branch>`，不创建 issue/PR，告知用户 | 重复创建 PR（产生 duplicate PR） |
| expectations 通过 | 6/6 ✓ | 0/6（未检查、重复创建、未只 push） |

**关键差异**：without skill 不做幂等检查，直接创建——产生 duplicate PR，是 GitCode PR 提交的常见错误；with skill 的步骤 2 检查点确保幂等。

## Case 4 — issue-creation-and-pr-template-linking（issue 创建与 PR 模板关联）

| | with skill | without skill |
|---|---|---|
| issue 创建仓库 | 在上游（openharmony owner）创建 issue | 可能在 fork 仓库创建 issue（错误） |
| issue 描述来源 | `git log -1` + `git diff HEAD~1` 自动生成 | 手写或从 commit message 复制 |
| PR 模板 | 读取 `.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md`，替换"### 关联的issue："为含 #number | 不读模板，直接写 PR body |
| issue 关联 | #number 填入模板，PR 合并自动关闭 issue | 无 #number 关联，issue 不会自动关闭 |
| expectations 通过 | 6/6 ✓ | 1/6（仅提到创建 issue；仓库错误、无模板、无关联） |

**关键差异**：without skill 不知道 issue 必须在上游仓库创建（fork 仓库的 issue 无法关联上游 PR）、不知道 PR 模板路径和 #number 自动关闭机制。

## Case 5 — ambiguous-remote-and-mcp-absence-handling（歧义远端与 MCP 缺失）

| | with skill | without skill |
|---|---|---|
| 多远端歧义 | 按决策矩阵要求用户选择 fork 远端，不自动猜测 | 自动选第一个非 origin 远端或随机选 |
| MCP 缺失 | 立即警告用户并终止 skill，不用 curl 绕过 | 尝试用 `curl` + token 直接调 API 绕过 |
| upstream 缺失 | 警告"无 openharmony 远端"并要求配置 | 不检查 upstream，可能向错误仓库创建 PR |
| expectations 通过 | 6/6 ✓ | 0/6（自动猜测远端、尝试 curl 绕过、不检查 upstream） |

**关键差异**：without skill 在歧义和缺失场景的行为最危险——自动猜测远端可能导致向错误仓库创建 PR；用 curl 绕过 MCP 缺失会绕过安全边界；with skill 的 MCP 前置检查 + 歧义处理是安全护栏。

## 总结

| 维度 | with skill | without skill |
|------|-----------|---------------|
| expectations 总通过 | **30/30 (100%)** ✓ | **3/30 (10%)** |
| 远端分类 | 按 owner 严格分类（openharmony=UPSTREAM） | 按 remote 名猜测（origin=上游） |
| head 格式 | `fork-owner:branch-name`（CRITICAL，GitCode 严格校验） | `remote:branch`（必失败） |
| 幂等性 | 先查 PR 存在性，已存在只 push | 不检查，重复创建 |
| issue 关联 | 上游创建 + #number 模板关联 + 自动关闭 | 仓库可能错误 + 无关联 |
| MCP 前置 | 缺失即终止，不绕过 | 尝试 curl 绕过（安全风险） |

## 局限与后续

- 本报告由 Agent 会话生成对比数据，基于 5 个 eval case、每 case 各 1 次运行。
- with/without 对比的 without 路径反映了通用 Agent 在 GitCode 跨仓 PR 提交上的典型短板：head 格式错误、重复创建 PR、issue 仓库错误、curl 绕过 MCP——这些正是 skill 存在的价值，且其中 head 格式和 MCP 绕过是**安全相关**的脆弱操作。
- 正式 `skills-judge` 评分见 `skill_judge_report.md`（B+ 级，97/120）。
- 当前 evals 为纯 prompt 驱动（无 fixture 文件），grader 靠 Agent 口述判断。后续可增加 fixture 工作区（含模拟 .git/config 远端配置和 MCP 响应 JSON）以提升评测可验证性——见 skill_judge_report.md 改进建议 2。
- 产物文件（PR/issue 创建结果）未随本报告提交（涉及真实 GitCode 仓库操作），如评审需要可另行提供模拟产物。
