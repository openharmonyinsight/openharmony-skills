# Skill Format Optimization

> **Status**: Implemented (P0)
> **Related**: HANDOFF skill slimming backlog; superpowers 6.x / agent-skills / OpenSpec format research
> **Scope**: P0 — skill `description` (tagline) quality + distribution-script hardening + base/bridge trigger disambiguation. Install/uninstall/switch improvements are explicitly **out of scope** here (tracked separately).

## 1. Background — three reference standards

| Standard | Key format requirements |
|---|---|
| Anthropic Agent Skills (`agentskills.io` / `skill-creator`) | frontmatter `name`+`description` required; `name` ≤64 chars, lowercase-hyphen, **must equal parent dir**; `description` ≤1024 chars, must contain **what (3rd person) + when (`Use when…`)**, must **not summarize workflow** (SDO); dir `skills/<name>/SKILL.md`; optional `scripts/`/`references/`/`assets`; cross-skill reference by name, no `@` force-load |
| Claude Code Plugin manifest | `plugin.json` in `.claude-plugin/`, only `name` required; `skills` auto-scanned from `skills/`; skill name = parent dir |
| OpenSpec (reference only) | generates SKILL.md frontmatter `name`+`description`+`license`+`compatibility`+`metadata` from a build step — same build-chain pattern ODK already uses |

## 2. Key architecture constraints (do NOT overturn)

These are intentional ODK design choices. This proposal works **within** them:

1. **dist-only distribution**: `core/skills/*/SKILL.md` is a pure-body source with **no frontmatter**; `distribute-skills.sh` injects frontmatter at generation time, extracting `description` from the body's first non-blank non-heading line (the **tagline**). → We do **not** hand-write frontmatter in `core/`.
2. **Skills are a thin routing layer**: long section definitions / table schemas / contract truth live in `core/{contracts,templates,adapters}/*.yaml`. → We do **not** add `references/`/`scripts/` to skills.
3. **tagline = description source of truth**: editing the core tagline updates the description across all three platforms (claude/codex/opencode) in one place.
4. **`odk-` / `odk-{sp,ops,ms}-` prefixes are intentional layer identifiers**. → We do **not** rename.

## 3. Gap analysis (standard vs. status quo)

### Real gaps (fixed by P0)

| # | Dimension | Standard | ODK status (measured) | Impact |
|---|---|---|---|---|
| G1 | description trigger (SDO) | must contain `Use when…` + what | **23/24 taglines only say what** (`Generate…`/`Bridge…`/`Fuse…`); only `using-odk` starts with `Use when` | undertrigger: "写 spec" won't match `odk-spec` |
| G2 | description pushiness | skill-creator says "be pushy" | neutral phrasing | worsens undertrigger |
| G3 | truncation threshold | description ≤1024 chars | `distribute-skills.sh:150` hard-codes `>120` truncation | `odk-security-threat-model` (148 chars) **already truncated**; 120 too tight for `Use when`+what |
| G4 | version source-of-truth | single | `distribute-skills.sh:50` hard-codes `version: "0.5.0"` | drift; bumping requires editing the script |
| G5 | base/bridge disambiguation | (implicit) | no signal in tagline to pick base vs bridge at trigger time | auto-trigger can't distinguish `odk-spec` from `odk-ms-delta-spec` |

### Architecture trade-offs (NOT changed)

| # | Dimension | Apparent gap | Actually intentional | Disposition |
|---|---|---|---|---|
| G6 | core source has no frontmatter | violates "hand-written frontmatter" | dist-only generation | keep |
| G7 | no references/scripts | violates "optional bundled files" | thin-router design (truth in YAML) | keep |
| G8 | `odk-` project prefix | official repos don't prefix | layer identifier + plugin namespace | keep |
| G9 | mixed H1 line position | inconsistent style | `awk 'NF && !/^#/'` is robust to both | optional unify |

## 4. P0 plan

### 4.1 `distribute-skills.sh` hardening

- Truncation threshold `120 → 300` (still far below the 1024 cap; room for `Use when…` + what + keywords).
- `version` read from `packaging/claude/.claude-plugin/plugin.json` (single source, **fail-fast** on read error — no silent `0.0.0` fallback that would mask a broken manifest).
- `description` emitted as a **YAML double-quoted scalar** with `\` and `"` escaped, so taglines containing `: ` (e.g. "Base layer: …", "Main router: …") or quotes don't break frontmatter parsing. Plain scalars split on `: ` and silently drop **all** frontmatter at runtime — discovered by `claude plugin validate` after the first P0 pass.
- `claude plugin validate` failure now exits the script non-zero (was swallowed by `|| echo "Warning"`); previously a broken frontmatter could ship with exit 0.

### 4.2 Version bump (cache-key coupling)

`plugin.json` `version` is Claude Code's plugin cache key. P0 bumps `0.5.0 → 0.6.0` in `packaging/claude` and `packaging/codex` so existing users pick up the new taglines on reinstall/update.

### 4.3 24 tagline rewrites (disambiguation convention)

**Convention (base vs bridge must be mutually exclusive at trigger time):**

```
base  → "... Default template-driven, zero plugin dependencies — use unless a bridge plugin is requested."
bridge → "Use when <Plugin> is installed AND the user wants <native concept> ... Falls back to <base> if unavailable."
```

Decision axis: **does the user want a bridge plugin's process discipline** + **is that plugin in `available_skills`**. Both true → bridge; otherwise → base.

Full rewrite table is in §5 below (authoritative). Outline by layer:

- **Router (2)**: `using-odk` (already `Use when`; add "main router + plugin detection" role), `using-odk-bridge` (passive, loaded by bridge skills — no `Use when`).
- **Base (11)**: each `Use when <artifact/phase>. Default … zero plugin dependencies.` `odk-implement` adds "no TDD/subagent cycles" to disambiguate from `odk-sp-implement`.
- **Bridge SP (4)**: `Use when Superpowers is installed AND …`. `odk-sp-brainstorm` notes "one-session proposal+spec+design" (3 artifacts, vs base's 1).
- **Bridge OPS (2)**: `Use when OpenSpec is installed AND …`. `odk-ops-propose` notes "all 4 artifacts in one pass".
- **Bridge MS (5)**: `Use when MatrixSpec is installed AND …`. delta-* note "ADDED/MODIFIED/REMOVED delta".

### 4.4 `using-odk` routing decision tree (P1, but tightly coupled to trigger disambiguation — done with P0)

Insert a `## Base vs Bridge Selection` section before `## Phase Skills` that turns the router into the first disambiguation layer: detect execution plugins from the available skill list → suggest the matching layer.

## 5. Authoritative P0 rewrite table

### 5.1 Router layer

| skill | new tagline (→ description) |
|---|---|
| `using-odk` | `Use when the user mentions ODK, ohos-delivery-kit, .codespec, or OpenHarmony delivery artifacts (proposal/spec/design/execution-plan/review/validate). Main router: loads phase skills and detects which bridge plugin (Superpowers/OpenSpec/MatrixSpec) is installed.` |
| `using-odk-bridge` | `Loaded automatically by odk-sp-*/odk-ops-*/odk-ms-* bridge commands — not invoked directly. Provides output redirection (strict/passthrough/merge), phase-artifact mapping, and design state-ownership rules.` |

### 5.2 Base layer (zero plugin dependencies)

| skill | new tagline |
|---|---|
| `odk-init` | `Use when starting a new ODK change. Creates the .codespec/changes/<id>/ skeleton. Run first, before any other odk-* command. Zero plugin dependencies.` |
| `odk-link-issue` | `Use when binding a GitCode/issue ID to an existing draft change directory (links to issue-<number>-<slug>). Zero plugin dependencies.` |
| `odk-propose` | `Use when writing ODK proposal.md (requirements, 8-dim N/A triage, success criteria, target_release). Default template-driven, zero plugin dependencies — use unless a bridge plugin is requested.` |
| `odk-spec` | `Use when writing ODK spec.md (WHEN/THEN acceptance criteria, error codes, verification mapping). Default template-driven, zero plugin dependencies. Use after proposal.md is approved.` |
| `odk-design` | `Use when writing ODK design.md (architecture, decisions, Mermaid, spec-AC references, conditional security check). Default template-driven, zero plugin dependencies. Use after spec.md.` |
| `odk-plan` | `Use when writing ODK execution-plan.md (AC-to-Task traceability, file-level scope, anti-fake checks). Default template-driven, zero plugin dependencies. Use after design.md.` |
| `odk-implement` | `Use when implementing an approved execution-plan.md Task-by-Task and backfilling code scope. Base layer: AI-assisted, zero plugin dependencies (no TDD/subagent cycles). Use after execution-plan.md approval.` |
| `odk-review` | `Use when generating ODK review evidence (spec-compliance, code-quality, verification) from templates after implementation. Default standalone, zero plugin dependencies.` |
| `odk-validate` | `Use when checking a change against the ODK delivery contract (Level A/B/C/D readiness) before archiving. Final gate. Zero plugin dependencies.` |
| `odk-spec-for-validation` | `Use when deriving spec-for-validation.md (integration/system scenarios, SC→AC trace) from spec.md. Parallel bypass, does not block main flow. Zero plugin dependencies.` |
| `odk-security-threat-model` | `Use when a change touches security/privacy/compliance and needs threat-model.md (STRIDE + regulatory checks). Bypass skill, triggered by proposal's security/permission dimension. Zero plugin dependencies.` |

### 5.3 Bridge layer — Superpowers

| skill | new tagline | artifacts / fallback |
|---|---|---|
| `odk-sp-brainstorm` | `Use when Superpowers is installed AND the user wants one-session proposal+spec+design via Superpowers brainstorming. Output redirected to ODK archive. Falls back to odk-propose+odk-spec+odk-design if unavailable.` | 3 artifacts (proposal/spec/design) |
| `odk-sp-plan` | `Use when Superpowers is installed AND the user wants writing-plans discipline for execution-plan.md (task decomposition, file-level boundaries, AC-Task trace). Falls back to odk-plan if unavailable.` | execution-plan → odk-plan |
| `odk-sp-implement` | `Use when Superpowers is installed AND the user wants TDD + subagent-driven execution of an approved execution-plan.md. ODK keeps traceability; Superpowers runs red/green cycles. Falls back to odk-implement if unavailable.` | code → odk-implement |
| `odk-sp-review` | `Use when Superpowers is installed AND the user wants requesting-code-review + verification-before-completion to produce ODK review evidence under evidence/reviews/. Falls back to odk-review if unavailable.` | evidence → odk-review |

### 5.4 Bridge layer — OpenSpec

| skill | new tagline | artifacts / fallback |
|---|---|---|
| `odk-ops-propose` | `Use when OpenSpec is installed AND the user wants /opsx:propose to generate all 4 artifacts (proposal+spec+design+execution-plan) in one pass, split into ODK format. Falls back to base commands if unavailable.` | 4 artifacts → base chain |
| `odk-ops-apply` | `Use when OpenSpec is installed AND the user wants /opsx:apply to implement tasks and backfill execution-plan code scope. Falls back to odk-implement if unavailable.` | code → odk-implement |

### 5.5 Bridge layer — MatrixSpec

| skill | new tagline | artifacts / fallback |
|---|---|---|
| `odk-ms-proposal` | `Use when MatrixSpec is installed AND the user wants /matspec.proposal to drive proposal.md. Falls back to odk-propose if unavailable.` | proposal → odk-propose |
| `odk-ms-delta-spec` | `Use when MatrixSpec is installed AND the user wants /matspec.delta-spec (ADDED/MODIFIED/REMOVED delta) for spec.md. Falls back to odk-spec if unavailable.` | delta spec → odk-spec |
| `odk-ms-delta-design` | `Use when MatrixSpec is installed AND the user wants /matspec.delta-design (delta format) for design.md. Falls back to odk-design if unavailable.` | delta design → odk-design |
| `odk-ms-tasks` | `Use when MatrixSpec is installed AND the user wants /matspec.tasks to drive execution-plan.md. Falls back to odk-plan if unavailable.` | execution-plan → odk-plan |
| `odk-ms-validation` | `Use when MatrixSpec is installed AND the user wants /matspec.validation to produce ODK review evidence. Falls back to odk-review if unavailable.` | evidence → odk-review |

## 6. Trigger routing (how base/bridge disambiguate after P0)

```
User input
  │
  ▼
[Layer 1] using-odk (main gate) — "Use when … ODK/.codespec/OH artifacts"
  │  on match → reads body → detects available execution plugins → suggests layer
  │
  ▼
[Layer 2] phase skill — each description carries its own precondition
  ├─ no bridge plugin requested → odk-spec / odk-propose / … (base, "zero plugin deps")
  ├─ Superpowers present        → odk-sp-*   ("Superpowers is installed AND…")
  ├─ OpenSpec present           → odk-ops-*  ("OpenSpec is installed AND…")
  └─ MatrixSpec present         → odk-ms-*   ("MatrixSpec is installed AND…")
  │
  │  if a bridge fires but the plugin is actually absent
  ▼
[Backstop] bridge body fallback → degrade to base (already exists, retained)
```

## 7. Compliance verification (post-P0)

Judged against the **dist artifact Claude actually loads** (not the core source):

| Agent Skills hard constraint | Post-P0 | Verdict |
|---|---|---|
| frontmatter `name`+`description` | generated by script | ✅ |
| `name` ≤64, equals parent dir | `name: $skill` (basename) | ✅ |
| `description` ≤1024 chars | longest ~230 | ✅ |
| description what + when | all 24 `Use when…`+what (P0) | ✅ |
| no workflow summary (SDO) | trigger + artifact only | ✅ |
| 3rd person, no first person | none | ✅ |
| `skills/<name>/SKILL.md`, kebab-case | yes | ✅ |
| cross-skill by name, no `@` | yes | ✅ |
| `license`/`metadata` optional | present | ✅ |
| `compatibility` optional | unused (bridge needs expressed in description) | ⚠️ optional optimization |

**Plugin layer**: `plugin.json` compliant; local-path install works; marketplace distribution not supported (HANDOFF P2, out of scope here).

**Final proof = runtime test**: `claude plugin validate dist/claude` + an actual install/trigger test. Recommended to wire into `validate-distribution.sh` later.

## 8. Install / uninstall / switch audit (summary — out of P0 scope)

Documented here so it is not lost; **handled in a separate pass** per maintainer decision.

| Action | Claude | Codex |
|---|---|---|
| Install | ⚠️ `claude plugin install dist/claude` (path form) is **not** the official contract; use `claude --plugin-dir` (session) or copy to `~/.claude/skills/<name>/` (persist) or a corrected local marketplace | ❌ CLI path installs the #53 empty shell (no skills); manual fallback copies `dist/codex` to `$TARGET/.codex/` but bypasses Codex's plugin system |
| Switch | ✅ `claude plugin enable/disable` | ❌ no `codex plugin enable/disable` CLI (TUI/config.toml only); manual path can't switch |
| Uninstall | ✅ clean, hooks side-effect-free | ⚠️ `codex plugin remove` won't clean manual copy; **no uninstall script** |

Minimal follow-ups (not done in P0): fix Claude install instructions; add `scripts/uninstall-codex.sh`; root-cause is HANDOFF P2's `ohos-marketplace` release repo.

## 9. Out of scope (explicitly not changed)

- No hand-written frontmatter in `core/`.
- No rename of `odk-` prefixes.
- No forced `references/`/`scripts/` per skill.
- No root `.claude-plugin/marketplace.json` (dist-only local install is the current model).
- No install/uninstall/switch changes (separate pass).

## 10. Validation steps (run after implementing P0)

1. `./scripts/distribute-skills.sh` regenerates `dist/` — now exits non-zero if `claude plugin validate` fails.
2. `claude plugin validate dist/claude` passes (authoritative frontmatter/structure check).
3. YAML roundtrip: parse every `dist/claude/skills/*/SKILL.md` frontmatter; `description` must equal the core tagline (escape is lossless), and `name` must equal the parent dir.
4. Length check: longest (`using-odk` ≈ 264) < 300.
5. Disambiguation self-check (grep, case-insensitive — some taglines use sentence-initial "Zero"):
   - base taglines contain "zero plugin dependencies".
   - bridge taglines contain "is installed AND" and "Falls back to".
6. Run existing validators (`validate-superpowers-bridge.sh`, `validate-distribution.sh`) to confirm nothing else broke.
