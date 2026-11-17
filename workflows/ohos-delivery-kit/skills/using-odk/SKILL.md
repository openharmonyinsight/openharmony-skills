---
name: using-odk
description: "Use when the user mentions ODK, ohos-delivery-kit, `codespec`, or OpenHarmony delivery artifacts (proposal/spec/design/execution-plan/review/validate). Main router: loads phase skills and detects which bridge plugin (Superpowers/OpenSpec/MatrixSpec) is installed."
license: MIT
---

# Using ohos-delivery-kit

You are working in a project that uses **ohos-delivery-kit** — a lightweight delivery artifact specification layer for OpenHarmony.

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

## Phase flow and next step

<!-- ODK:reference contracts/skill-guides/router/phase-flow.md -->
Before phase work, read `contracts/skill-guides/router/phase-flow.md` and apply
its configured pre_hook/post_hook order. At every completion or pause, show
the next pending action and configured hooks; omit the reminder only when
the entire applicable workflow is complete. The coordinator owns this flow.
<!-- /ODK:reference -->

## Activation

### Bridge Mode (session-scoped)

Once the user invokes any `{{CMD_PREFIX}}*` command in the current session, ODK bridge activates for the remainder of the session: Output Redirection Rules (see Phase-Artifact Mapping below) apply to stateless document output paths; OpenSpec retains its native workspace and publishes an ODK projection. Ends when the session ends.

ODK also activates when the user explicitly mentions ODK, ohos-delivery-kit, `codespec`, or ODK artifact names/actions (proposal, spec, api-spec, design, execution-plan, spec-for-validation, threat-model, metadata_tracking, review, validate, submit design docs).

When the user is describing or discussing a requirement, feature idea, or non-trivial change, load `odk-brainstorm` before drafting new artifact decisions; no special trigger phrase is required. Standalone brainstorm and the propose/spec/design inline gates share one interview protocol. An existing `proposal.md`, an initialization stub, or a later phase is not proof that its decisions were explored: reuse confirmed decisions and investigate only new or unresolved branches. **Check escapes first:** ordinary coding, debugging, refactoring or reverts without new feature scope, and self-contained bug fixes with a clear root cause, do not start an artifact interview. Honor explicit requests to skip the interview or go directly to a draft by carrying unresolved choices as assumptions/open questions; do not fabricate confirmations. A fully specified request can close the shared gate from explicit evidence without redundant questions. **Avoid circular loading:** if `odk-brainstorm` is already loaded in this session, reuse it; when brainstorm loads `using-odk`, it only supplements shared context (interaction mode, authorized endpoint, delivery-level contract) and does not re-enter brainstorm. The shared protocol runs once, then returns to the original calling phase.

### Deactivation

ODK bridge does **not** activate when:
- `codespec/` exists but the user has not invoked any `{{CMD_PREFIX}}*` command in this session
- The user is doing ordinary coding, debugging, build, or review tasks
- The user explicitly says "不用ODK" / "skip ODK" / "don't use ODK"

After activation, follow the Context Loading rules below to determine the active change.

### Check for updates first

Before resource self-check, configuration loading or phase routing, follow
[the shared update check](references/update-check.md). Reuse its result and the
user's choice when this activation routes to `odk-init` or `odk-propose` in the
same request. A successful upgrade ends this request with a restart reminder.

### Resource Self-Check

<!-- ODK:reference contracts/skill-guides/router/resource-check.md -->
On first activation, locate and read `contracts/skill-guides/router/resource-check.md` before checking resources. Run this bootstrap with the **absolute path of the SKILL.md actually loaded**, replacing the example argument. It resolves file/directory symlinks first (including flat host skills pointing into source or plugin caches), then probes source/native, neutral and SkillHub layouts. `OHOS_PLUGIN_ROOT` is an optional fallback; no environment variable is required. Use the first existing guide; do not guess relative to the business repository or search unrelated caches.

```sh
python3 - /absolute/path/to/loaded/using-odk/SKILL.md <<'PY'
import os
from pathlib import Path
import sys

loaded = Path(sys.argv[1]).absolute()
suffix = Path('contracts/skill-guides/router/resource-check.md')
roots = [loaded.resolve().parents[2], loaded.parents[2]]
if os.environ.get('OHOS_PLUGIN_ROOT'):
    roots.append(Path(os.environ['OHOS_PLUGIN_ROOT']).expanduser())
candidates = []
for root in roots:
    for base in (root, root / 'runtime/assets', root / 'assets', root / 'core'):
        candidate = base / suffix
        if candidate not in candidates:
            candidates.append(candidate)
for candidate in candidates:
    if candidate.is_file():
        print(candidate.resolve())
        break
else:
    sys.exit('ODK resource guide missing; inspected:\n' + '\n'.join(map(str, candidates)))
PY
```

Read the returned guide path and resolve subsequent resources from its actual location. If the command fails, report its inspected paths and stop phases that need those resources. Reuse a successful check in this session unless the installation changes.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/workflow.md -->
## Workflow (on activation)

After ODK activates, read `contracts/skill-guides/router/workflow.md` before selecting a phase, archive, or base/bridge command. It defines the unchanged archive layout, phase order, available commands, plugin preference and fallback. Do not load it for ordinary coding or when ODK is disabled.
<!-- /ODK:reference -->
## Configuration

Before configuration-dependent work, run `python3 runtime/executables/lib/odk_repository.py --effective-config` (source checkout: `python3 scripts/lib/odk_repository.py --effective-config`). Use the returned `config` values and `user_config_path`; a config error stops the phase.

<!-- ODK:reference contracts/skill-guides/router/configuration.md -->
Read `contracts/skill-guides/router/configuration.md` for same-directory user overrides, upgrade preservation, precedence and empty-value semantics. Reload at the start of each phase; implementation reuses the commands already confirmed in its execution plan unless the user requests a change.
<!-- /ODK:reference -->

## Key Rules

- **target_release** is the single source of truth for version, stored in `proposal.md` YAML frontmatter
- Traceability chain: `proposal → spec AC → execution-plan Task → code → commit → review`. Any broken link fails validation.
- **Post-implementation**: completed Tasks automatically enter review and validation through the implementation skill's shared handoff. Source PR submission waits for an explicit user trigger after a reminder; confirmed PR results drive local metadata, followed by separate design-docs confirmation. Do not auto-merge or recursively restart the handoff from review/validate.
- **GitCode submission reminder**: when implementation is complete and the user is about to commit, push, or open a GitCode PR, remind them that documents under `codespec/` must be submitted to the separate design-docs repository. Resolve its address using priority order: `codespec/profile.yaml` if present → `odk_config_ext.yaml` → `odk_config.yaml`. Do not warn if `codespec/profile.yaml` is absent. If no address can be resolved, show “待开发者填写” and ask the developer to provide it; never guess a repository or automatically push across repositories. This reminder does not by itself block the business-code submission. When the user explicitly requests design-document submission, invoke `odk-submit-design-docs`: generate `metadata_tracking.yaml`, validate the five-base-file bundle plus required conditional evidence (including the applicable language-specific API metadata files and declaration diffs when `API/SDK=是`), and submit `proposal.md`, `spec.md`, `design.md`, `execution-plan.md`, `metadata_tracking.yaml`, and applicable API evidence together.
- **Phase Gate**: Use the interaction mode below. In interactive mode, artifact approval approves only that document: suggest the next command and wait. Implementation requires an approved execution plan and a user request to implement (natural language or an implement command). In autonomous mode, an explicit end-to-end request authorizes sequential phases within its stated scope: generate and self-check each artifact, summarize decisions, then continue to the authorized next phase. Never infer implementation authorization solely from document approval. TDD remains the default for implementation; untestable Tasks must declare degradation.
- **Session ID 追踪**: 每个生成交付件的 skill（odk-init / odk-propose / odk-spec / odk-design / odk-plan / odk-security-threat-model / odk-spec-for-validation / odk-submit-design-docs）在写入交付件时，必须通过调用 `update-sessions-sidecar.py` 脚本将当前会话 session ID 增量追加到变更目录下的 `.sessions.json` sidecar 文件（权威源），并镜像到交付件的 frontmatter `sessions` 字段和 body `## 会话记录` 表格。判定基准为 session ID 本身：不同 session 调用同一 skill 也必须追加。详见各 skill 的 `## Session ID 追踪` 小节。

## Session ID 追踪契约

### 存储模型

sidecar `.sessions.json` 是权威源；frontmatter 和 body 表格是镜像（可选但推荐）。

| 层 | 位置 | 格式 | 用途 |
|----|------|------|------|
| sidecar（权威源） | 变更目录下 `.sessions.json` | JSON | 原子 read-append-write，不丢数据 |
| frontmatter（镜像） | 交付件 YAML `sessions` 字段 | 逗号分隔标量 `sessions: "ses_aaa,ses_bbb"` | 从 sidecar 镜像，人可读 |
| body 表格（镜像） | 交付件 body 开头 `## 会话记录` | Markdown 表格 | 从 sidecar log 生成，人可读 |

sidecar 格式（session ID 跨平台格式见下文「Session ID 获取」）：

```json
{
  "proposal.md": {
    "sessions": ["ses_aaa", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"],
    "log": [
      {"session": "ses_aaa", "skill": "odk-init", "time": "2026-10-16T10:00:00Z", "action": "生成"},
      {"session": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "skill": "odk-propose", "time": "2026-10-16T11:00:00Z", "action": "更新"}
    ]
  }
}
```

- `sessions` 数组：去重（按 session ID），追加顺序保留。
- `log` 数组：不去重，每次调用追加一条。

### Session ID 获取（多平台）

各宿主平台的会话标识格式不同，由平台适配层注入系统提示。脚本接受以下格式：

| 平台 | 格式 | 示例 | 获取来源 |
|------|------|------|----------|
| opencode | `ses_<字母数字>` | `ses_abc123` | OpenCode 插件注入的系统提示 |
| codex | `<uuid>` | `11111111-2222-3333-4444-555555555555` | Codex hook 注入的系统提示 |
| claude | `<uuid>` | `aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee` | Claude hook 注入的系统提示 |

**规则**：
1. 优先从当前对话的系统提示中提取会话标识（形如 "Current conversation session ID: xxx"）。
2. **必须用当前对话自己的 ID**，不得复用历史会话或编造 ID。
3. **宿主未暴露会话标识时**：传入字面量 `unavailable` 调用脚本（脚本会跳过 sidecar 更新并提示用户），**禁止编造或留空**。明确告知用户本次交付件未记录会话追踪。

### 增量追加规则（使用脚本，禁止手动操作 JSON）

**所有 skill 必须通过调用 `update-sessions-sidecar.py` 脚本来更新 sidecar，禁止手动读/写 JSON。** 脚本对整个 read-modify-write 加排他锁并通过临时文件 + `os.replace()` 原子发布，不会丢失已有 log 条目，不会因并发覆写丢数据，不会复制错误的 session ID。

1. **获取当前 session ID**：按上文「Session ID 获取」从当前对话提取；获取不到则用 `unavailable`。⚠️ 必须用当前对话自己的 ID。
2. **调用脚本**：

   ```sh
   python3 "runtime/executables/update-sessions-sidecar.py" \
     "<变更目录绝对路径>" "<交付件文件名>" "<当前session ID>" "<skill名>" "<action>"
   ```

   - `<action>`：**由脚本自动判定，传入任意值都会被覆盖**。log 为空（首次）→ `"生成"`，log 非空（后续）→ `"更新"`。
   - 脚本会原子性地：加锁 → 读取已有 sidecar → 追加 session（`sessions` 去重，`log` 不去重）→ 临时文件写入 → `os.replace()` 原子发布 → 解锁。
   - 脚本是 fail-open 的，出错时 exit(0) 不阻塞。
3. **从脚本输出提取镜像数据**：脚本输出中的 `---MIRROR---` 段包含：
   - `sessions: "ses_aaa,aaaaaaaa-..."` → 写入交付件 frontmatter `sessions` 字段。
   - `## 会话记录` 表格（所有行） → 写入交付件 **body 开头**（frontmatter 之后、正文 `#` 标题之前）。
4. **写入交付件**：将 frontmatter `sessions` 字段和 body `## 会话记录` 表格写入交付件。镜像丢失不影响数据完整性——**sidecar 是权威源**。

### 追加时序

skill 准备好新增内容或增量补丁**之后**、通过受保护命令写入交付件**之前**执行：
- 调用 `update-sessions-sidecar.py` 脚本更新 sidecar（脚本内部完成 read-append-write）
- 从脚本输出提取 `---MIRROR---` 段，将 `sessions` 字段和 `## 会话记录` 表格写入交付件
- 写入交付件

**关键**：sidecar `.sessions.json` 只保存会话调用历史；镜像缺失时可据此恢复会话记录，但它不备份交付件正文，也不证明阶段完成。阶段与 hook 的成功结果、证据和恢复位置必须按 `contracts/skill-guides/router/workflow-state.md` 写入 `.workflow.json`。

## Effective contract and delivery level

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and use the validator's
`--effective-contract` JSON before selecting required artifacts or phases.
<!-- /ODK:reference -->

## Interaction Mode

Default to **interactive** mode. If the user asks to automate, use recommended options, or run through the workflow ("自动", "全选推荐", "跑完"), use **autonomous** mode within the requested endpoint. Record the mode, authorized endpoint and assumptions at the start; summarize artifact changes, selected recommendations and validation results at every phase, then invoke the next phase without requiring another slash command. "全选推荐" changes how choices are made; it authorizes code changes only when the task also includes implementation. A request to finish design stops at design; an explicit request to implement and deliver may continue through plan, implementation, review and validation.

Self-check every updated/new artifact and run the packaged validator with the current `--phase define|specify|design|plan` after each artifact phase; future artifacts are outside that check. Fix issues in available artifacts before continuing. Stop for missing essential facts, conflicting requirements, failures that cannot be resolved, or a material scope expansion. Previously granted authorization stays effective; neither mode authorizes new publication destinations, merging, destructive operations or separate design-docs submission. Follow the shared delivery handoff for those steps and honor any source-PR submission already requested by the user.


## Context Loading

For actual design-document submission, `odk-submit-design-docs` resolves and confirms the destination first: for an exact `gitcode.com` business origin retain configured `design_docs_repository` or offer `https://gitcode.com/OpenHarmonyAI/design-docs`; other/missing origins require the user to supply the address for this submission, not silently reuse a profile. No answer is not consent; the reminder alone never authorizes cross-repository writes. Confirmation of the document PR authorizes commit/push/PR creation, not merging.

- If `codespec/` does not exist, the project is not yet initialized — guide the user to run `odk-init`
- Resolve the current `<repo-name>` and inspect only `codespec/changes/<repo-name>/`
- If that repository directory has exactly one change directory, treat it as the active change
- If it has multiple change directories, ask the user which one to operate on before proceeding
- Once determined, read `target_release` from the active change's `proposal.md` frontmatter
- Do not load full documents into context — use summaries (≤15 lines) when passing between phases
- Existing targets: read full frontmatter and body before revising; preserve confirmed decisions, stable IDs, custom sections, progress and evidence. Templates fill missing structure. See the document-updates guide above.
- Upstream context: read the relevant sections in full; summaries (≤15 lines) are for handoff only.
- When spawning subagents (e.g. via bridge commands), run them in isolated contexts — never fork the main session history; the main session only dispatches tasks and receives summaries
- Pass evidence by file path, not by content — artifacts land on disk once (`evidence/`, `pr-diff.txt`, `findings.json`); later references pass the path, not the full text
- Cap parallel fan-out at ≤4 subagents per layer; batch or narrow task scope if more are needed
- The fixed three-seat Task review in `contracts/skill-guides/delivery/task-review.md`, executed by `odk-task-review` (arch/scope/security), is the only sanctioned exception; do not treat it as permission to widen fan-out elsewhere, and reviewers never dispatch further reviewers
- Template files are located at `templates/` (installed with the plugin)

<!-- ODK:reference contracts/skill-guides/router/profiles.md -->
## Profile Detection

When generating ODK artifacts for a module, read `contracts/skill-guides/router/profiles.md` before applying profile overrides; resolve its relative paths from that guide's directory. It defines profile selection, phase mappings, fragment composition and conflict precedence. Routing-only requests do not need this reference.
<!-- /ODK:reference -->
## Bypass Documents (Design Phase)

ODK supports bypass documents that supplement main artifacts for complex scenarios:

| Bypass Document | Trigger Condition | Relation to Main Artifact | Production Skill |
|----------------|-------------------|---------------------------|-------------------|
| `threat-model.md` | High-risk security/privacy/compliance (see `odk-security-threat-model` trigger conditions) | `design.md` 基础检查 → 深度分析独立存档 | `odk-security-threat-model` |
| `spec-for-validation.md` | Integration/system scenarios needed for validation | Derived from `spec.md`; parallel bypass, does not block main flow | `odk-spec-for-validation` |

**Drift direction rule**: When upstream proposal/spec content changes, re-run the bypass skill to sync (e.g., `threat-model.md` security triggers expand → re-run `odk-security-threat-model` to refresh analysis).

When using bridge commands, `using-odk-bridge` is loaded automatically and provides output mode selection and redirection rules.

## Template Reference

- AI artifact templates: `templates/ai/` (proposal, spec, design, execution-plan, spec-for-validation, threat-model)
- Review templates: `templates/review/` (spec-compliance, code-quality, verification)
- API metadata templates: `templates/api/arkts-api-spec.yaml`, `templates/api/c-api-spec.yaml`
- Design-docs submission metadata: `templates/metadata_tracking.yaml`
