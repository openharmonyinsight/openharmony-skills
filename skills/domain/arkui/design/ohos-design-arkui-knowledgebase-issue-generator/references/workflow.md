# Issue KB Generator Workflow Reference

Use this reference for generating, updating, or repairing ArkUI ace_engine issue-type KB pages.

## Step 0: Determine Mode

First, determine the operation mode:

1. Run `python3 docs/kb_search.py <target>` to check whether an issue KB already exists for the target. If the initial search returns no match, also try:
   - `python3 docs/kb_search.py <target> --field name` — search by name only
   - `python3 docs/kb_search.py <target> --field keywords` — search by keywords/aliases
   - If the target looks like an IssueID (PascalCase, no spaces), also try searching by `id` field: `python3 docs/kb_search.py <target> --field id`
   Only conclude "no existing KB" when ALL queries return no match.
2. Based on the result:
   - **No existing KB → CREATE mode**: proceed to Step 1 (gather info) and generate a new KB page.
   - **Existing KB found → UPDATE mode**: if the user wants to add new root causes, cases, or fix outdated information, read the existing KB page and registry entry, then proceed to update in-place (preserving unmodified fields, never duplicating entries).
   - **Existing KB found → REPAIR mode**: if the user wants to fix structural issues, broken links, or invalid registry entries, read the existing KB page and registry entry, identify defects, and repair without altering verified content.

For UPDATE/REPAIR:
- Read the existing KB file and its registry entry in `context_registry.json` before making any changes.
- Preserve fields that the user did not ask to change (e.g. keep existing keywords when updating root causes only).
- Do NOT append duplicate entries to `context_registry.json` — update the existing entry in-place.
- Do NOT create a new KB file alongside the existing one — edit the existing file.

Only when `kb_search.py` returns no match should you enter CREATE mode.

## Step 1: Gather Issue Information from User

**Mode-dependent step applicability**:

| Step | CREATE | UPDATE | REPAIR (registry-only) |
|------|--------|--------|------------------------|
| Step 1 (gather info) | Full — all required fields | Only fields being changed | Skip — no new issue info needed |
| Step 2 (verify) | Full verification | Only verify changed root causes/code paths | Skip — no new claims to verify |
| Step 3 (write KB) | Create new file | Edit existing file | Edit only registry entry |
| Step 4 (register) | Add new entry | Update existing entry | Update existing entry |
| Step 5 (README) | Increment count + add row | Update row if changed | Only fix broken links |
| Step 6 (validate) | Full validation | Full validation | Full validation |

For REPAIR mode that only fixes registry metadata (e.g. adding a missing keyword, correcting a typo), skip Steps 1-2 and Step 3's KB file editing — proceed directly to Step 4 (update registry), then Step 6 (validate).

The user must provide the core issue description. This is NOT optional — the agent cannot invent problem details. Accept input in any of these forms:

- A detailed problem description in natural language (Chinese or English)
- A link to a specific issue/bug report (GitHub, GitCode, Gitee, etc.)
- A reference to a specific PR or commit that fixed a problem
- A verbal description like "Navigation 返回时页面崩溃" or "Flex 布局中子节点反复 Measure"

After receiving the initial input, **always追问** to fill in missing information. Use the best available question mechanism to ask the user until ALL of the following are confirmed:
- If a structured `question` tool is available (OpenCode, Claude Code), use it.
- Otherwise, ask in plain text and end the current turn, waiting for the user's reply. Do NOT continue without answers.

| Required field | 追问 question | Example |
|---------------|-------------|---------|
| 问题现象 | "请描述典型表现/复现步骤" | "界面卡死，布局抖动" |
| 根因类别 | "你知道的根因是什么？如果有多个，请分别说明" | "属性循环依赖 + GeometryTransition 互锁" |
| 结构化关联模块 | "问题表现在哪个组件？根因归属哪个模块？修复落在哪个位置？" | 见下方关联模块结构 |
| 历史案例 | "是否有具体的 PR/Commit/Issue 可以参考？" | "PR #xxxxx, commit abc123" |
| 目标 FuncIDs | "这个问题关联的功能域 FuncID 是什么？如果不确定可以后续推断" | "03-01-01, 04-03-01" |

**结构化关联模块**：问题发生的组件、触发能力、根因所属模块和实际修复位置可能完全不同（例如问题表现在 Navigation，根因位于生命周期管理，修复落在 FrameNode）。用户只需描述问题场景；关联模块和 FuncID 应优先由 Agent 查询 `context_registry.json`、Spec 和源码后派生，然后请用户确认。每个关联条目包含：

| 字段 | 值 |
|------|---|
| kind | `component` / `capability` / `architecture` |
| role | `symptom_surface` / `trigger` / `root_cause_owner` / `fix_location` / `dependency` |
| name | 模块/组件/能力名称 |
| evidence | 对应源码、PR 或用户描述 |
| confidence | `verified` / `inferred` / `user_claimed` / `unknown` |

If the user provides an issue link, fetch the issue content using the best available web-fetching mechanism and extract the above fields from it. If any field is missing or unclear after extraction,追问 the user.
- Prefer `webfetch` if available; otherwise use the runtime's built-in browser or GitCode client integration.
- If no web-fetch capability exists, ask the user to paste the issue content directly.

**Do NOT proceed to step 2 until all required fields are confirmed.** If the user says "不确定" for a field, the agent should propose a reasonable inference based on source code search and ask the user to confirm. If only a single root cause or case can be verified, that is acceptable — proceed with the available information and note the coverage scope in the generated KB.

**Generation readiness criteria**: Before proceeding to step 2, the gathered information should be sufficient for other developers to:
- **Identify the problem**: Problem description includes recognizable trigger conditions, actual results, and impact
- **Understand the cause**: Root cause explanation describes a specific mechanism or causal chain, with corresponding evidence
- **Reuse the solution**: Fix strategy includes key changes, why they work, and verification results
- **Map to code**: Associated modules/classes/functions/tests can be located in the actual source tree

If any of these criteria is not met, continue追问 the user on the insufficient aspect rather than proceeding with a vague KB.

## Step 2: Verify Root Causes and Code Paths

There are two sources for verification:

**Source A: User-provided PR/Commit links**

If the user provided specific PR or commit links in step 1, fetch each one using the best available web-fetching mechanism to extract:
- The changed files and functions
- The fix strategy described in the PR
- Any root cause analysis in the PR description or comments

Then map these to current source code paths. If a referenced path has been renamed or removed since the PR was merged, search the current source tree to find the equivalent location.

**Source B: Agent-driven source code search**

For root cause categories where no PR reference is given, the agent proactively searches the source tree. Use `rg` / `git grep` / `grep` as the **baseline** for all code search; the following MCP/AST tools are optional enhancements when available:
- `codebase-mcp_ast_read` — locate symbol definitions by name (if available)
- `codebase-tool-mcp_GetRemoteCallChain` — trace call chains (if available)
- `codebase-tool-mcp_CodeSemanticSearch` — semantic code search (if available)

If these MCP tools are unavailable (e.g. in Codex runtime), rely entirely on `rg` / `git grep` / `grep` and directory listing. Do NOT require MCP tools as mandatory dependencies.

**After verification, present findings to the user for confirmation** before proceeding to step 3. Show:
- A summary table of each root cause category → verified source path → fix PR (if available)
- Flag any paths that could not be verified or have been relocated

Only proceed to step 3 after the user confirms the verification results.

## Step 3: Write / Update / Repair KB Content

Based on the mode determined in Step 0:

| Action | CREATE | UPDATE | REPAIR |
|--------|--------|--------|--------|
| KB file | Create new at `docs/kb/issues/<category>/<slug>.md` | Edit existing KB file in-place | Edit existing KB file, fix only confirmed defects |
| Registry | Add new entry to `context_registry.json` | Update existing entry in-place (preserve unmodified fields) | Update existing entry, fix only confirmed defects |
| README count | Increment 主题数 | Do NOT increment (topic already counted) | Do NOT increment (no new topic) |
| README table | Add new row to 问题型 KB table | Update existing row if display content changed | Only fix broken links/paths in existing row |
| Duplicate check | New ID by definition | Must NOT append duplicate entry — update existing | Must NOT append duplicate entry — update existing |

**CREATE mode**: Create the file at `docs/kb/issues/<category>/<slug>.md` using the template in [references/template.md](template.md). Fill in all sections with verified information from steps 1 and 2.

**UPDATE mode**: Edit the existing KB file. Preserve sections the user did not ask to change. Add new root cause categories, cases, or fix outdated information only in the specified areas.

**REPAIR mode**: Fix only the confirmed structural defects (broken links, invalid registry entries, missing fields). Do NOT alter verified content that is not defective.

**After writing, present the full KB content to the user for review before committing changes to disk.** The user may want to:
- Adjust wording or phrasing
- Add or remove root cause categories
- Supplement additional cases or PR references
- Modify the problem domain category or file slug

Only write changes to disk after the user confirms the content is satisfactory **AND the information security check passes** (see below).

### Information Security Check (MANDATORY before writing to disk)

Before presenting or writing any KB content, perform an **information security and partner-identifiable feature check**. Issue KBs may extract content from internal bugs, PRs, logs, and user descriptions — this step ensures no sensitive or partner-identifiable information leaks into publicly accessible KB pages.

**Checklist — scan the entire draft for each category:**

| Category | Examples | Action if found |
|----------|----------|-----------------|
| Partner/customer identity | Partner names, customer names, app names, project/product codenames | Rewrite as generic technical condition (e.g. "特定窗口尺寸变化/折叠态切换场景") or remove |
| Internal references | Internal repo URLs, branch names, private Issue/PR URLs, unreleased commit hashes, version plans | Remove or rewrite as generic references |
| Personal data | Names, email addresses, account IDs, device IDs, username paths | Remove entirely |
| Credentials | Tokens, cookies, API keys, passwords, secrets | Remove entirely and flag as security incident |
| Full business text / screenshots / log payloads | Detailed business logic, raw log dumps, screenshot content | Abstract into technical symptom description |
| Indirectly identifiable combinations | Device model + business name + version that can re-identify a partner | Abstract into generic conditions |

**Output a security classification:**
- **public-safe**: No sensitive or partner-identifiable information found. Proceed to write.
- **internal-only**: Contains internal references that cannot be removed. Since the skill's output location is a **public Git repository** (`docs/kb/issues/`) with no access control mechanism, `internal-only` content **must NOT be written to disk** — it would be publicly accessible. The user must either sanitize the content to reach `public-safe`, or store the KB in a separate private repository with access controls.
- **blocked**: Contains credentials, unredacted personal data, or information that cannot be anonymized. **Must NOT write to disk.** Report findings to the user and request sanitized input.

## Step 4: Register / Update in context_registry.json

Based on the mode:

- **CREATE**: Before adding the entry, confirm the following fields with the user:
  - **IssueID**: Is the proposed ID appropriate? (e.g. `MeasureInfiniteLoop` — PascalCase, concise, descriptive)
  - **name_cn**: Is the Chinese name accurate and natural?
  - **keywords**: Are the keywords sufficient for search? Any missing or redundant ones?

  Use the best available question mechanism to ask the user to confirm these three fields. After confirmation, add the new entry to the `contexts` array with the `kind: "issue"` shape (see [references/template.md](template.md) for the entry shape).

- **UPDATE/REPAIR**: Update the existing entry in-place in `context_registry.json`. Do NOT append a new entry. Preserve fields that the user did not ask to change.

## Step 5: Update README

Based on the mode:

- **CREATE**: Update `docs/kb/README.md` — increment the 主题数 count, and add the new issue KB to the **"### 问题型 KB"** subsection table (NOT the 知识型 KB table).
- **UPDATE**: Update `docs/kb/README.md` — update the existing row in the 问题型 KB table if display content changed. Do NOT increment 主题数.
- **REPAIR**: Update `docs/kb/README.md` — only fix broken links or paths in the existing row. Do NOT increment 主题数 or add new rows.

## Step 6: Validate

Run the existing validation tool:

```bash
python3 docs/validate_context.py
python3 docs/kb_search.py "<IssueID>"
```

**Note**: Issue KBs do NOT have `### API 入口`, `### 测试入口`, `## 常见问题定位`, or `## 调试入口` sections, so `validate_context.py` will report WARNINGS for these missing sections. These WARNINGS are **expected and acceptable** for issue-type KBs. Only ERROR-level findings need to be fixed. Issue KB entries use `kind: "issue"` which is natively supported by `validate_context.py` — the validator exempts `kind: "issue"` entries from `spec_status` and standard KB section validation.

Also verify the KB file is reachable:

```bash
ls docs/kb/issues/<category>/<slug>.md
```
