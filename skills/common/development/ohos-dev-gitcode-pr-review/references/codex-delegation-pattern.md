# Codex Delegation Pattern for GitCode PR Review

Concrete patterns learned from production use. Reference this file when delegating PR reviews to Codex.

## Prerequisites

- `codex` CLI installed and authenticated (v0.145+)
- `oh-gc` CLI in PATH and authenticated
- Local repo checkout at `/root/work/<repo>`

## Flags

- `--skip-git-repo-check` — always include this. Codex in a repo with dirty state or detached HEAD may refuse to run without it.
- `--dangerously-bypass-approvals-and-sandbox` — required for non-interactive automation (equivalent to `--sandbox danger-full-access --full-auto`).
- `-m <MODEL>` — set the model. Default in config is `gpt-5.6-sol` (flagship). Use `gpt-5.6-terra` for balanced or `gpt-5.6-luna` for cheap. Run `cat ~/.codex/models_cache.json | jq '.models[].slug'` to list all available models.
- `-C <dir>` — set working directory to the repo checkout.
- `-o <file>` — writes a summary file after completion.
- **DO NOT append `2>/dev/null`** — it hides the `apply patch` section in process logs which contains the full report.

## Parallel Launch Command

```bash
cd /root/work/<repo> && codex exec -m gpt-5.6-sol \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  -o /tmp/codex-pr-<NUMBER>-report.md \
  "$(cat <<'PROMPT'
你是 OpenHarmony 代码检视专家。请检视 GitCode PR <NUMBER>。

## 仓库
当前目录就是仓库: <OWNER/REPO>
oh-gc 工具在 PATH 中可用。

## 检视方法论
先读取以下 skill 文件获取检视流程和标准：
1. /root/.hermes/skills/common/development/ohos-dev-gitcode-pr-review/SKILL.md
2. /root/.hermes/skills/common/development/ohos-dev-gitcode-pr-review/references/deep-review-checklist.md
3. /root/.hermes/skills/common/development/ohos-dev-gitcode-pr-review/references/review-rubric.md
4. /root/.hermes/skills/common/development/ohos-dev-security-code-review/SKILL.md
5. /root/.hermes/skills/common/development/ohos-dev-security-code-review/references/permission-authorization.md
6. /root/.hermes/skills/common/development/ohos-dev-security-code-review/references/ipc-input-validation.md
[+ other security refs as needed: system-ability-trust-boundary.md, privacy-logging.md, etc.]

## 执行步骤
1. 使用 oh-gc 收集 PR 上下文:
   - oh-gc pr view <NUMBER> --repo <OWNER/REPO>
   - oh-gc pr diff <NUMBER> --repo <OWNER/REPO>
   - oh-gc pr comments <NUMBER> --repo <OWNER/REPO> --comment-type pr_comment
   - oh-gc pr comments <NUMBER> --repo <OWNER/REPO> --comment-type diff_comment
   - 阅读 PR 描述中自述的「已知问题/已知限制」，检视时逐条实际核实（可能是过期描述或已修复）

2. 按 skill 要求的深度检视流程，对每个变更文件：
   - 读取 diff 中的变更内容
   - 读取本地仓库中对应的完整源文件及上下文
   - 追踪调用者/被调用者
   - [domain-specific focus: e.g. 权限校验逻辑, IPC 安全边界]

3. 对每个变更文件给出检视状态: reviewed / mechanical-low-risk / skipped-with-reason

## 输出要求
- 使用中文
- 按 "严重级别 | 路径:行号 | 问题 | 证据 | 修复建议" 格式输出 findings
- 如果没有发现，说明每个文件的检视状态和已检查的代码路径
- 将完整检视报告写入 /tmp/codex-pr-<NUMBER>-report.md
PROMPT
)"
```

Launch via Hermes: `terminal(background=True, notify_on_complete=True, timeout=600)`

## Post-Codex: Retrieving the Full Report

The `-o` file is often just a summary. Full report is in Codex's process log, specifically in the `apply patch` section.

```bash
# 1. Read the summary file
read_file /tmp/codex-pr-<NUMBER>-report.md

# 2. If it's just a summary, get full report from process logs
process(action="log", session_id="<proc_id>", limit=500, offset=0)
```

**If the process log was truncated (e.g. launch used `| tail -80`) or `-o` was overwritten with the summary, recover the full report from the Codex session JSONL** — see `references/codex-report-recovery.md` for the exact script. The `apply_patch` call that wrote the report file is preserved verbatim in `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`. Verified in production (PR 316).

**Critical:** Do not use `2>/dev/null` on the codex exec command. The marketplace `codex` skill recommends appending `2>/dev/null` to suppress thinking tokens in stderr, but this also hides the `apply patch` output that contains the full report. Without `2>/dev/null`, the process log has both thinking tokens (noise) and the full report (signal) — just scroll past the thinking tokens.

**Critical #2: `| tail -N` truncates the report the same way.** When launching via `terminal(background=True)`, do NOT append `2>&1 | tail -80` (or any tail pipe) to the codex exec command. Codex writes the full report to the target file via `apply_patch`, then the final assistant message is only a short summary. If the last Codex action is a `tail`/`cat` of the report file inside the prompt (e.g. "verify the report was written"), the process log's last 80 lines will be that verification, and the earlier `apply_patch` section holding the full report is lost from the visible log. Launch Codex with plain `2>&1` (no pipe) so the whole log is retained.

**Recovery when the report WAS truncated: pull it from the Codex session JSONL.** If the process log lost the full report (tail truncation, log rotation, or you only see the summary), the complete `apply_patch` content still lives in Codex's session transcript:

```bash
# Find the newest rollout JSONL for the session:
ls -t ~/.codex/sessions/$(date +%Y)/$(date +%m)/$(date +%d)/rollout-*.jsonl | head -1
```

The message of interest is a `response_item` with `type: custom_tool_call`, `name: exec`, whose `input` is a JS string like `const patch = "*** Begin Patch\n*** Add File: /tmp/codex-pr-N-report.md\n+...*** End Patch";`. Extract and unescape:

```python
import json, re
msgs = []
with open('<rollout>.jsonl') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try: msgs.append(json.loads(line))
        except: pass
for m in msgs:
    p = m.get('payload', {})
    if m.get('type') == 'response_item' and p.get('type') == 'custom_tool_call' and p.get('name') == 'exec':
        inp = p.get('input')  # JS string: const patch = "*** Begin Patch\n..."
        m2 = re.search(r'\*\*\* Begin Patch\\n(.*?)\\n\*\*\* End Patch', inp, re.S)
        if m2:
            report = m2.group(1).replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
            print(report)  # full report content
```

Note the input is a JS code string (`const patch = "..."`), NOT pure JSON — `json.loads(inp)` fails. Regex for the patch body between `*** Begin Patch` and `*** End Patch` works, then unescape `\n`/`\"`. Verified in production: PR 316 full report (80 lines) recovered this way after `tail -80` had truncated the process log.

## Post-Codex: Submitting Line Comments to GitCode

### Step 1: Get exact diff-side line numbers

If Codex generated context (check for `/tmp/codex-pr-<NUMBER>-context/summary.json`):

```python
import json
with open("/tmp/codex-pr-<NUMBER>-context/summary.json") as f:
    data = json.load(f)
for file_info in data["files"]:
    path = file_info["path"]
    if "<target_substring>" in path:
        print(f"{path}: commentable_lines = {file_info['commentable_lines']}")
        for hunk in file_info["hunks"]:
            print(f"  hunk: {hunk['header']}")
```

If no context dir exists, use Hermes skill's `collect_pr_context.py` to generate one:

```bash
python3 /root/.hermes/skills/common/development/ohos-dev-gitcode-pr-review/scripts/collect_pr_context.py \
  <NUMBER> --repo <OWNER/REPO> --out-dir /tmp/codex-pr-<NUMBER>-context
```

### Step 2: Map Codex findings to exact commentable lines

**Important: Codex line numbering depends on how it accessed the code.**

- **With `-C <dir>` (local repo access):** Codex reads actual files from the working directory and reports **new-file line numbers** directly. No offset calculation needed — use Codex's numbers as-is, then cross-check against `summary.json`.
- **Without `-C` (reading combined diff):** Codex reads `pr diff --color never` output and reports **combined-diff line numbers** — see the offset calculation below.

Default to new-file line numbers when `-C` is used. Verify by checking that the reported line falls within the hunk range in `summary.json`; if it does, it's already a new-file line number. Only reach for offset math when the reported line is far outside known hunk ranges.

**Critical pitfall (legacy mode without `-C`): Codex reports combined-diff line numbers, not new-file line numbers.**

When Codex reads the full combined diff output (`oh-gc pr diff NUMBER --color never`) — i.e. running without `-C` for local repo access, or the model chooses to read the diff text — it references line numbers from that combined text, NOT from the individual new files. When Codex writes `detailed-cases.md:609`, the `609` is the line in the *combined diff file*, which spans multiple files. The actual new-file line number is different.

**For new files (additions), calculate the offset:**

```
new_file_line = combined_diff_line - hunk_header_line_in_diff + 1
```

Where `hunk_header_line_in_diff` is the line number of the `@@ -0,0 +1,N @@` line in the full diff output. The hunk header line is the line BEFORE the first content line of that file's section. Skip the `diff --git`, `status`, and `---` header lines.

Example from a multi-file diff:

```
Line 415: diff --git a/.../detailed-cases.md b/.../detailed-cases.md
Line 416: status: new file | +245 -0
Line 417: ---
Line 418: @@ -0,0 +1,245 @@   ← hunk_header_line_in_diff = 418
Line 419: +# Detailed Memory Leak Cases   ← new-file line 1
...
Line 609: +    HandleScope handleScope(env);  ← Codex reports "detailed-cases.md:609"
# → new-file line = 609 - 418 + 1 = 192
```

**For existing files with multiple hunks**, each hunk has its own `@@ -old_start,old_count +new_start,new_count @@` header. The new-side start (`new_start`) tells you the mapping. Codex's reported line number is still from the combined diff, so you need to find which hunk it falls in, then:

```
new_file_line = new_start + (combined_diff_line - hunk_header_line_in_diff - 1)
```

**Ground truth is the diff's `+` added lines — NOT `summary.json` `commentable_lines` alone.**

`collect_pr_context.py` writes `commentable_lines` as the ENTIRE hunk range, which includes context lines that GitCode cannot accept comments on. A line can be listed in `commentable_lines` yet be rejected by the API. Verify every target with `verify_diff_lines.py` (from the `cli-agent-delegation` skill):

```bash
python3 /root/.hermes/skills/devops/cli-agent-delegation/scripts/verify_diff_lines.py \
  <pr-diff.txt> "path:line" ["path:line" ...]
```

- `OK` → added line, safe to comment
- `MISSING (added N..M)` → line is context, not commentable; REMAP to the nearest added line in the same hunk and state the real problem line inside the comment body so the author can locate it
- `FILE-NOT-IN-DIFF` → no added lines (pure rename / empty diff); fall back to a file-level comment

Remap worked in production (PR 323): findings at `profiles/README.md:55` and `ohos-spec-for-validation/SKILL.md:5` were listed in `commentable_lines` but were context lines — remapped to added lines `56` and `4` respectively, with the original line number called out in the comment text.

**File-level comment fallback** — when a finding's problem lines sit entirely OUTSIDE any diff hunk (e.g. stale paths in an unchanged section of a file that has other hunks), post a file-level comment by passing `--path` WITHOUT `--line`. Verified working on PR 323: the CLI maps `--line` to the API `position` field, so omitting it yields a file-level comment:

```bash
oh-gc pr comment <NUMBER> --repo <OWNER/REPO> \
  --path "<file_path>" \
  --body "<comment body>"
```

**PR-level fallback — file NOT in the PR changed set at all.** When the finding's target file has NO diff hunks in this PR (e.g. residual references to a deleted skill living in unmodified files like `review-gate`, `value-decision`, `requirement-intake` — verified on PR 324), neither a line comment nor a file-level comment will attach. Detection heuristic: if the target path is absent from `summary.json`'s `files` list, it is unmodified in this PR. Post a PR-level comment with `--body` only (no `--path`):

```bash
oh-gc pr comment <NUMBER> --repo <OWNER/REPO> --body "$(cat /tmp/comment_body.md)"
```

Fallback ladder when a finding cannot attach to a verified added line: (1) nearest added line in same hunk + note real line in body → (2) file-level comment (file IS in changed set) → (3) PR-level comment (file NOT in changed set).

**Never trust Codex's "path:line" number literally for multi-file diffs.** Cross-reference against the hunk ranges, then let `verify_diff_lines.py` decide. If Codex's finding references a code section, pick the nearest verified-added line within that section's hunk.

### Step 3: Verify findings before submitting

**Always verify every finding's path:line before submitting.** Codex can be off by a few lines even when using new-file line numbers. Do this verification:

1. **Read `summary.json` — confirm the reported line is in `commentable_lines`** for that file.
2. **Read the actual file content** at the target line:
   - If the file exists locally (existing file): `read_file <path> --offset <line-5> --limit 10`
   - If the file is **new in the PR** (status `+N -0`): it won't exist in the local checkout. Use the PR diff text instead: search `pr-diff.txt` for the diff hunk and verify the `+` line content matches what Codex described.
3. **If the line content doesn't match** the finding's description, find the correct line by searching `pr-diff.txt` for the relevant code pattern.
4. **Only submit when the content at the target line is exactly what the finding describes.**

### Step 4: Submit each finding

**Pitfall: shell escapes in `--body`** — The `--body` value is passed as a shell argument. Markdown backticks, brackets, slashes, and special characters get interpreted by bash and cause syntax errors or truncated comments. **Do NOT inline multi-line or markdown-heavy body as a string literal.**

**Correct approach: write the body to a temp file, then read it with `$(cat ...)`:**

```bash
# Write each comment body to a separate file
cat > /tmp/comment_path_line.md <<'CMT'
**[medium] 问题描述**

问题分析 → 证据 → 建议修复

包裹标识符用反引号如 `function_name`
CMT

# Submit using $(cat ...) to avoid shell escaping issues
oh-gc pr comment <NUMBER> --repo <OWNER/REPO> \
  --path "<file_path>" --line <new_side_line> \
  --body "$(cat /tmp/comment_path_line.md)"
```

The `<<'CMT'` heredoc with quoted delimiter prevents shell expansion inside the body text. The `$(cat ...)` ensures the body content is passed as a single argument with all special characters preserved.

**Alternative for short bodies with no special chars:**
```bash
oh-gc pr comment <NUMBER> --repo <OWNER/REPO> \
  --path "<file_path>" --line <new_side_line> \
  --body "简单描述，无反引号和括号"
```

### Comment body format

Follow review-draft-schema.md rules:
- Title: `**[SEVERITY] 简要描述**`
- Body: 问题描述 → 证据 → 建议修复（分隔成短段落或 bullet points）
- Wrap code identifiers in backticks

### `oh-gc pr comment` does NOT accept `--comment-type`

The flag `--comment-type diff_comment` does not exist in `oh-gc pr comment`. Using it causes exit code 2 with "Nonexistent flag: --comment-type". Only `--path` and `--line` are needed for diff-line commenting. Correct syntax:

```bash
oh-gc pr comment <NUMBER> --repo <OWNER/REPO> \
  --path "<file_path>" --line <new_side_line> \
  --body "<comment body>"
```

No `--comment-type`, no `--json` for submission.

## Post-Submission: Re-check PR for New Commits

After submitting all findings, check if the PR has been updated with new commits (the author may have pushed fixes while you were reviewing):

```bash
# 1. Check current state
oh-gc pr view <NUMBER> --repo <OWNER/REPO>

# 2. Check for new/changed files
oh-gc pr diff <NUMBER> --repo <OWNER/REPO> --name-only

# 3. Get the current diff size to detect changes
oh-gc pr diff <NUMBER> --repo <OWNER/REPO> --color never | wc -l

# 4. Compare HEAD SHA to the one Codex reviewed
oh-gc pr view <NUMBER> --json --repo <OWNER/REPO> | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['head']['sha'])"
```

If the diff has grown or the HEAD changed:
- **Re-collect PR context**: `python3 collect_pr_context.py <NUMBER>`
- **Check each submitted finding**: the author may have already fixed some
- **Re-review only unfixed findings**: tell the user what was fixed and what remains
- **Do NOT re-submit findings already addressed** — that creates noise on the PR

### Pitfall: author may have fixed issues before your comments landed
When the author pushes a fix commit while you're still reviewing, some of your findings become stale before they're even posted. After submitting, always check `git log` or `oh-gc pr view` for recent commits. If several findings were already fixed, report that clearly to the user rather than letting them think the PR still has all the issues.

## Known Issues

### Codex tokens
- Small PRs (~50 line diff): ~125K tokens
- Large PRs (~350 line diff): ~480K tokens
- Plan budget accordingly; parallel runs share no token budget.

### `process(action="wait")` clamps timeout to 60s
`process(action="wait", timeout=N)` silently clamps N to the configured 60s limit. Long Codex runs (10+ min) need repeated waits — loop `wait(timeout=60)` (each call returns partial output) or launch with `notify_on_complete=true` and let the notification wake you. Don't expect a single large-timeout wait to block the whole run.

### Codex may or may not generate context
Codex sometimes runs `collect_pr_context.py` on its own, sometimes doesn't. If it didn't, Hermes should run it after Codex finishes to get `summary.json` for line number mapping.

### `-o` file is often just a summary
The `-o` target file may contain only a short summary. The full detailed report is in Codex's stdout captured by the process log — look for the `apply patch` section. Read both:
1. `read_file /tmp/codex-pr-<NUMBER>-report.md` — check if this is the full report or just a summary
2. `process(action="log", session_id="<proc_id>", limit=500, offset=0)` — full report is here

### Prompt length
The heredoc prompt can be long. Wrap it in `$(cat <<'PROMPT' ... PROMPT)` to pass as a single argument to `codex exec`. The single quotes around `PROMPT` prevent shell expansion.

### `oh-gc pr comments --json` may timeout
The JSON mode for reading PR comments can silently hang or timeout when the comment count is high or the API response is large. Workaround: pipe to a file first using text mode, then read the file:
```bash
oh-gc pr comments <NUMBER> --repo <OWNER/REPO> --comment-type pr_comment > /tmp/comments.txt
oh-gc pr comments <NUMBER> --repo <OWNER/REPO> --comment-type diff_comment > /tmp/diff_comments.txt
```
Then grep/cat the files for specific comment IDs or author names.

## Re-review (Second Round) Pattern

After PR author makes changes based on initial findings, launch Codex again with a modified prompt that:

1. **References previous findings** — tells Codex what was found before so it can check each one.
2. **Uses `--limit 100`** on oh-gc pr comments — reads all PR discussion including author replies to your previous comments.
3. **Asks per-finding status** — each prior finding gets ✅ 已修复 / ❌ 未修复 / 🔄 部分修复 / ✅ 合理拒绝 (author's rejection, verified).
4. **Writes to a separate report file** — use `-r2` suffix to avoid overwriting the first report.
5. **Inspect the fix commit BEFORE launching.** Fetch the PR head (`git fetch <fork-url> <branch>:prNNN-head`) and `git show` the newest commit(s) to see whether the author targeted prior findings. Use that to give Codex exact 核实点 per finding. Worked on PR 291 R2: the fix commit `f83f8b3` rewrote the deprecated-detection section and added `files` fields to evals — each became a concrete verification point in the prompt, and Codex confirmed 3/4 fixed, 1 partially.
5. **Write per-finding 核实点 (verification points)** — for each prior finding add a concrete "核实点：..." line stating exactly what to check in the new code (field present? value correct? version pinned? shortcut removed?). This turns "check if fixed" into verifiable assertions and yields precise verdicts. Verified in production (PR 291 R2): 3 ✅ 已修复 + 1 🔄 部分修复 + 3 new medium findings, with the 🔄 verdict backed by concrete evidence (e.g. `files` field added but still empty arrays — structure fixed, reproducibility not closed).

### Re-review prompt template

```bash
cd /root/work/<repo> && codex exec -m gpt-5.6-sol \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  -o /tmp/codex-pr-<NUMBER>-r2-report.md \
  "$(cat <<'PROMPT'
你是 OpenHarmony 代码检视专家。请**重新检视** GitCode PR <NUMBER>。

这是第二次检视，PR 作者已经根据第一次检视的 findings 做了修改。

## 仓库
OWNER/REPO: <OWNER/REPO>
oh-gc 工具在 PATH 中可用。

## 第一次检视的 findings（参考用）
之前的检视发现以下 <N> 个问题，请重点检查这些是否已解决：
1. <severity>: <brief description>
2. ...

## 执行步骤
1. 使用 oh-gc 收集 PR 上下文:
   - oh-gc pr view <NUMBER> --repo <OWNER/REPO>
   - oh-gc pr diff <NUMBER> --repo <OWNER/REPO>
   - oh-gc pr comments <NUMBER> --repo <OWNER/REPO> --comment-type pr_comment --limit 100
   - oh-gc pr comments <NUMBER> --repo <OWNER/REPO> --comment-type diff_comment --limit 100
   - **特别关注**：读取 PR 上的评论（上次检视提交的评论），检查作者是否已回复或修改

2. 对比第一次检视的 findings，确认修复情况。
3. 按 skill 要求的深度检视流程，对每个变更文件进行完整检视。

## 输出要求
- 对每个之前的问题标注：✅ 已修复 / ❌ 未修复 / 🔄 部分修复 / ✅ 合理拒绝
- 若作者对某 finding 答复"不修改/不修复"，**必须核实其拒绝理由**（引用的规范章节原文、plugin.yaml 依赖闭包、同类插件先例、适用范围），理由成立才标 ✅ 合理拒绝，不成立标 ❌ 未修复并给出反驳证据
- 按 "严重级别 | 路径:行号 | 问题 | 证据 | 修复建议" 格式输出新的 findings
- 检查新提交是否引入回归（路径替换指向真实文件、删除字段无固定键消费者、provenance 对账一致）
- 不要在检视报告中提"命令无法验证"或"官方文档链接缺失"这类问题
- 如果没有新的发现，说明每个文件的检视状态
- 将完整检视报告写入 /tmp/codex-pr-<NUMBER>-r2-report.md
PROMPT
)"
```

Launch identically: `terminal(background=True, notify_on_complete=True, timeout=600)`

### Pre-flight: verify the author pushed, then inspect the new commit before launching Codex

Before starting an R2 (or any re-review), confirm the PR head actually moved and learn what the new commit changed — this decides whether the round is a real re-review and shapes the 核实点 lines. Verified in production (PR 291 R2):

1. **Check `updated_at` vs your last submission time**: `oh-gc pr view <N> --repo <OWNER/REPO> --json` → if `updated_at` is AFTER the timestamp of your previous review's comments, the author pushed fixes since.
2. **`oh-gc pr commits <N> --json` quirk**: it returns only SHAs (no messages, no dates — the fields come back empty). To see commit messages/dates, fetch the branch locally:
   ```bash
   git fetch https://gitcode.com/<AUTHOR>/<repo>.git <branch>:pr<N>-head
   git log --oneline -5 pr<N>-head
   git show <new-sha> --stat          # which files the fix touched
   ```
3. **Map the new commit's files to your prior findings** — if the fix commit touches exactly the files your findings referenced (e.g. the 3 `evals.json` + `workflow.md` for 4 findings), it is a targeted fix round: state that explicitly in the prompt and write per-finding 核实点 verifying the *substance* of the fix (e.g. "author added `files` — is it a non-empty fixture with pinned provenance, or just `[]`?"), not just its presence. This catches "structure fixed, behavior not closed" outcomes (PR 291 R2 finding 1: `files: []` added → 🔄 not ✅).

### Submitting only unfixed findings after re-review

After Codex re-review completes, submit line comments ONLY for findings marked ❌ (unfixed) or 🔄 (partially fixed):

1. Read the report to get each finding's status.
2. For each ❌/🔄 finding, collect PR context with `collect_pr_context.py` to get exact commentable lines.
3. Write each comment body to a temp file and submit via `oh-gc pr comment`.
4. **Do NOT re-submit findings already marked ✅** — they've been addressed.
5. **Always post a PR-level summary reply (user expectation, verified on PR 325 R2)** — in addition to the ❌/🔄 line comments, submit one PR-level comment (`--body` only, no `--path`) that lists ALL prior findings with their re-review status, explicitly calling out the ❌ 未修复 and 🔄 部分修复 items with a short evidence summary. Use a `## 未修复` / `## 部分修复` structure. This is what the user means by "再提交一个独立回复说明没有改或者没改完的问题" — without it, the author only sees scattered line comments and no consolidated verdict.
5. **🔄 follow-up comments go on the line the author CHANGED, not the original finding line.** For partially-fixed findings, the original line may no longer be an added line (the fix commit rewrote it into a context line). Remap to a line the fix commit touched, and mark the comment as a follow-up: `**[medium] 🔄 部分修复跟进：<what's still open>**`. Worked on PR 291 R2: finding 1 (evals missing `files`) was only structurally fixed (`files: []` everywhere but still empty, no fixture/pin) — the follow-up landed on `spec-generator/evals/evals.json:9` (the newly-added `files` line) and explicitly stated the reproducibility gap remains.

### Replying to author comments on PR

After re-review, if the author has replied disputing a finding:

1. Read the author's comment text to understand their reasoning.
2. If they are incorrect (e.g., confusing two code paths or files), write a new PR-level comment addressing the specific confusion with code-level evidence — do not repeat the original finding verbatim.
3. Use `oh-gc pr comment NUMBER --repo OWNER/REPO --body "$(cat /tmp/reply_body.md)"` — there is no oh-gc reply-to-thread command; post as a fresh pr_comment with context.
4. In the reply, reference the exact file path, line number, and function/class name so the author can locate the code.

**Pitfall: "no fix needed" may be about the wrong file.** When the author claims a finding doesn't need changes, verify they are looking at the correct function. In one session, the author said `_find_profiles_dir()` was already fixed because `ohos_sdd_engine.py` worked, but the finding was about `ohos_sdd_spec_for_test.py` — a different function with the same name in a different file. Always cross-reference the exact file:line from your finding before closing.

**✅ 合理拒绝 — how to adjudicate author rejections (not just "no fix needed" but "won't fix").** When the author rejects a finding with reasoning (policy, spec, precedent), do NOT accept the rejection at face value and do NOT blindly re-argue. Instruct Codex to verify the rejection grounds against actual repo artifacts before labeling it ✅ 合理拒绝 (accepted) or ❌ 未修复 (rejection invalid):

1. **Cited spec/document actually says what the author claims** — read the cited section (e.g. placement spec §9.2 marking `related-skills` as optional) and confirm the text supports the author.
2. **The dependency/requirement is genuinely satisfied elsewhere** — e.g. author says "`plugin.yaml` include already declares the dependency closure, so per-skill `related-skills` is redundant": verify the plugin.yaml include list actually covers every skill the router invokes, with no missing/duplicate/dangling entries.
3. **Repo precedent exists** — author cites sibling workflows (e.g. `workflows/ohos-delivery-kit/` skills lacking `related-skills`): verify at least the named precedent exists and matches the claim; a quick count (e.g. "all 34 workflow-embedded skills have zero `metadata` blocks") is strong evidence.
4. **Applicability scope** — author claims the norm doesn't apply to this file's location (e.g. placement spec only governs `skills/common/<stage>/` and `skills/domain/<domain>/`, not `workflows/<plugin>/skills/`): verify the spec's scope definition and the file's actual location.

Verified in production (PR 323 R2): author rejected two findings citing (a) placement spec §9.2 marks `metadata.related-skills` optional, (b) plugin.yaml include closure covers all 9 invoked skills, (c) ODK sibling precedent, (d) placement spec scope excludes `workflows/<plugin>/skills/`. Codex verified all four claims against the actual spec text, plugin.yaml, and the 34 workflow-embedded skills (zero with `metadata`), and correctly marked both ✅ 合理拒绝. The findings are then CLOSED — do not re-submit them, and report them as resolved in the round summary.

### Default: always submit findings as line comments

When the user asks Codex to review a PR, the default expectation is that findings are submitted as GitCode line comments — not just reported in a markdown file. The workflow is:

1. Run Codex (first round or re-review).
2. Collect PR context with `collect_pr_context.py`.
3. Cross-reference each finding's reported line number against `summary.json` commentable_lines.
4. Write each comment body to a temp file with `cat > /tmp/comment_* <<'CMT'` (quoted delimiter to prevent shell expansion).
5. Submit each with `oh-gc pr comment --repo OWNER/REPO --path "<file>" --line <N> --body "$(cat /tmp/comment_*)`.

## Full Regression Check (Rounds 4+)

After several rounds when all previous findings appear fixed, launch a full regression check instead of a narrow re-review. This is distinct from R2/R3 which focus only on unfixed items.

### When to use
- All prior findings from all rounds are marked ✅
- Author has made at least one more commit since the last clean round
- Need to confirm no new commits introduced regressions

### Prompt structure

```
你是 OpenHarmony 代码检视专家。请第<N>次检视 GitCode PR <NUMBER>。

确认前几轮的遗留问题是否已全部修复。第<N-1>轮结论是全部通过，请检查是否因新提交出现了回归。

## 仓库
OWNER/REPO: <OWNER/REPO>

## 第<N-1>轮结论
[list each finding from all prior rounds with status]

## 执行步骤
1. oh-gc pr view/diff/comments <NUMBER> --repo <OWNER/REPO>
2. 读取所有评论和作者回复
3. 检查是否有新增提交导致回归
4. 输出结论

## 输出要求
- 使用中文
- 写入 /tmp/codex-pr-<NUMBER>-r<N>-report.md
- 不提"命令无法验证"或"官方文档链接缺失"
```

### After Codex completes

If report confirms all clean: inform the user the PR is ready to merge.
If regressions found: submit line comments only for the regression findings.
Do NOT re-submit comments for findings that remain fixed.
