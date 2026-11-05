---
name: odk-init
description: "Use when starting a new ODK change. Creates the repository-scoped formal or draft skeleton. Run first, before any other odk-* command. Zero plugin dependencies."
license: MIT
---

# ODK Init

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and use the effective
contract. It takes precedence over standard-only artifact lists below; native
OpenSpec schemas remain standard/critical and lite uses the base flow.
<!-- /ODK:reference -->

## Check for updates first

Before collecting inputs or changing any files, follow
[the shared update check](../using-odk/references/update-check.md). Reuse a check
and user choice already made by `using-odk` in this request; direct invocation
must run the check itself. Continue only when the shared procedure says to.

## Input

Ask the user for:
1. **English short slug** — concise description of the requirement (e.g. `arkui-focus`)
2. **目标发布版本 (target_release)** — 填发布版本号（如 `7.0`、`7.1`，可选 `7.1-Beta`），**不填分支名**（`master`/`dev` 不是发布版本）。可按发布惯例做委婉推断（见下），但**不要替用户自动填入**——必须由用户明确给出版本号。
3. **Proposal ID (proposal_id)** (optional) — if not yet available, draft naming is used; link later via `{{CMD_PREFIX}}link-proposal`

> **target_release 委婉推断（参考，不强制）**：OpenHarmony 每年一个大版本（`x.0`）+ 一个小版本（`x.1`）。按今天月份判窗口：7–10 月→小版本，11–12 月及 1–6 月→大版本；按年份查版本（2026：大=7.0、小=7.1）。向用户呈现为「按惯例推断是 X，请明确输入实际目标版本」，**等用户明确答复后再写入 frontmatter**，不替用户自动填入。详见 `oh-metadata-rules.md` R-OH-004。

If arguments are provided, parse both coherent forms:
- `<proposal-id> <slug> <target-release>` when the first argument is a valid proposal ID and the third argument is a target release
- `<slug> <target-release> [proposal-id]` otherwise; the proposal ID remains optional

Validate a supplied proposal_id against `^[0-9]+$`. Formal proposal IDs contain digits only, with no fixed length.
Validate the slug against `^[a-z0-9]+(?:-[a-z0-9]+)*$` and a maximum length of 40. Do this before any directory or `.gitignore` mutation.

## Steps

1. Resolve `<repo-name>` from the Git `origin` URL basename without `.git`; if `origin` is unavailable, use the Git worktree root directory name. Reject a name containing path separators or characters outside `[A-Za-z0-9._-]`.
2. Create directory: `codespec/changes/<repo-name>/<proposal-id>/` (or `codespec/changes/<repo-name>/draft-<yyyymmdd>-<slug>/` if no proposal_id). The formal leaf is exactly the proposal ID and does not retain the slug. If the directory already exists, read its existing proposal and preserve all files. Compare its proposal_id, target_release and stored slug with the request, and check the repo segment against origin. A draft's slug must also match its leaf. For legacy proposals without a slug, use their full requirements body and already-confirmed session decisions to identify the change; a body-less stub without a comparable slug is ambiguous, so report the missing identity and ask before reusing it. A conflicting identity must be resolved explicitly. `--effective-contract` only queries rules and may succeed on a stub; it is not an identity or readiness check.
   - **目录不存在**：创建目录，继续后续步骤（写 stub + sidecar）。
   - **目录已存在**：**不要直接 abort**。先调用 `update-sessions-sidecar.py` 脚本将当前会话记录到 sidecar（action 由脚本自动判定），再镜像到 frontmatter + body 表格，然后告知用户："变更目录已存在，proposal.md 已有内容。如需完善内容请运行 `{{CMD_PREFIX}}propose`。" 不覆盖已有 proposal.md 正文内容，只更新 sidecar + frontmatter `sessions` 字段 + body `## 会话记录` 表格。
3. 获取当前 session ID：从**当前对话**的系统提示提取（"Current conversation session ID: ses_xxx"，格式 `ses_[a-zA-Z0-9_-]+`）。详见 `using-odk` 的 `## Session ID 追踪契约`。

4. 调用脚本更新 sidecar（**禁止手动操作 JSON**）：

   ```sh
   python3 "runtime/executables/update-sessions-sidecar.py" \
     "<变更目录绝对路径>" "proposal.md" "<当前session ID>" "odk-init" "<action>"
   ```

   - `<action>`：**由脚本自动判定**。log 为空（首次）→ `"生成"`，log 非空（后续）→ `"更新"`。
   - 脚本输出 `---MIRROR---` 段包含 `sessions: "..."` 和 `## 会话记录` 表格。

5. 根据 step 2 的分支处理 proposal.md（使用 step 4 脚本输出的镜像数据）。Only create the stub when proposal.md does not exist; an existing proposal is read and preserved, including its full body.

   **A. 目录不存在（新建）**：创建 `proposal.md` frontmatter-only stub（无章节骨架，不读模板）：


   ```yaml
   ---
   target_release: <user-provided value>
   proposal_id: "<proposal_id or empty>"
   slug: "<validated English short slug>"
   author: ""
   date: ""
   status: Draft
   sessions: "<脚本输出的 sessions 字段>"
   delivery_level: standard
   ---

   <脚本输出的 ## 会话记录 表格>

   <!-- ODK proposal stub: run `{{CMD_PREFIX}}propose` to generate requirements content. -->
   ```

   **B. 目录已存在（追加 session 记录）**：**不覆盖 proposal.md 正文**，只更新 frontmatter `sessions` 字段和 body 开头的 `## 会话记录` 表格（用脚本输出的镜像数据替换）。告知用户："变更目录已存在，已记录当前会话。如需完善内容请运行 `{{CMD_PREFIX}}propose`。"

6. Do **not** create `spec.md`, `design.md`, or `execution-plan.md` here — each is generated on first run by its own command (`{{CMD_PREFIX}}spec` / `{{CMD_PREFIX}}design` / `{{CMD_PREFIX}}plan`), which reads and revises an existing target, or creates a missing target from its effective contract. Pre-building empty skeletons would only be read back and overwritten (wasted context).
7. Do not create `reviews/` or `gates/` by default. They are optional process evidence directories, not part of the minimal archive contract.
8. Ensure the repo `.gitignore` ignores redirected workspaces and `codespec/`. OpenSpec retains its native workspace: do not add or remove an `openspec/` ignore entry; its tracking policy belongs to the project:
   - Entries to ensure, **idempotently** (append only missing ones; never overwrite or remove existing content): `codespec/`, `docs/superpowers/`, `matspec/`, `.matspec-cli/`
   - If `.gitignore` does not exist, create it with a short `# ODK bridge workspaces` header followed by the entries.
   - **Do NOT add adapter install dirs** (`.claude/`, `.codex/`, `.opencode/`, `opencode.json`, etc.) — committing those is a team choice, not ODK's to decide.

## Session ID 追踪

odk-init 的 session ID 追踪逻辑已集成在 step 3-5 中（调用脚本 + 镜像到 proposal.md）。详见 `using-odk` 的 `## Session ID 追踪契约`。

**关键**：目录已存在时不再 abort，而是调用脚本追加当前会话记录。脚本自动判定 action（首次=生成，后续=更新）。

## Output

```
codespec/changes/arkui/12345/   (or codespec/changes/arkui/draft-20260522-arkui-focus/)
└── proposal.md      (frontmatter-only stub — full body generated by {{CMD_PREFIX}}propose)
```

`spec.md`, `design.md`, and `execution-plan.md` are **not** created by init — each appears when its command first runs. (Repo-root `.gitignore` bridge-workspace entries are ensured separately.)

After creating the stub:
- Report the `.gitignore` state (created / already had the bridge-workspace entries / appended missing ones), and remind: `codespec/` goes to the developer-configured `design_docs_repository` on GitCode, redirected bridge workspaces are ignored; OpenSpec tracking follows project policy, and adapter install dirs are the team's choice. `odk-submit-design-docs` generates `metadata_tracking.yaml` and validates the five-base-file bundle plus required conditional evidence before submission. If the address is absent, display “待开发者填写”; do not guess it. Run the configuration command defined in `using-odk` and show its `user_config_path`, in the installation’s `assets/config/` directory beside the active `odk_config.yaml`. Users customize this sibling file; keys automatically override defaults without rewriting them. The installer must preserve it while replacing default assets; do not move it to a separate global directory. Report config errors before proceeding.
- Suggest: "Next: run `{{CMD_PREFIX}}propose` to generate the requirements proposal."

Confirm with the user that the structure is correct before proceeding.
