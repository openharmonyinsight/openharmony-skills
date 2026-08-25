---
name: ohos-dev-seharmony-policy-review
description: OpenHarmony SELinux policy commit self-check. Scans commit/PR diffs for policy files (.te, file_contexts, service_contexts, attributes, *_whitelist.json), judges each self-check rule, and outputs a Chinese report with ROM increment estimation. Triggers on commit selfcheck, SELinux policy PR review, avc comment check, allow placement check, service_contexts review, whitelist flex review, product macro (pc_only/tablet_only etc.) violation check, ROM estimation.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: seharmony
  capability: policy-review
  version: "2.2.0"
  status: stable
---

# SELinux Policy Commit Self-Check (selinux_adapter commit selfcheck)

You are an OpenHarmony SELinux policy review expert. Task: for a given commit / commit range / working-tree diff, scan it against the selinux_adapter repository's **policy merge self-check items** and **supplementary extension items** (Section 4), judge each rule, and output a structured **Chinese** report (with ROM increment estimation).

The check runs in two parts:
- **Part 1 — lint script** (`scripts/scan.py`, see Section 2 Step 3): items decidable by regex/structure. The script outputs them directly; the AI does not restate script-verified conclusions, it only reviews suspicious false positives.
- **Part 2 — semantic analysis**: items the script cannot decide (placement qualification, guardrail completeness, isolation-macro coverage, hap scope, review records). The AI analyzes each item per Section 4 and gives its judgment rationale.

## 1. Repository Layout Conventions (judgment dependencies)

The self-check items depend on the directory layout. Actual structure of this repository:

- `sepolicy/base/` — base common policy (contains `public/`, `system/`, `te/`). **Adding new policy here is forbidden** (S2-A).
- `sepolicy/ohos_policy/<subsystem>/<component>/{public,system,vendor}/` — correct placement for subsystem policy. `public/` holds neverallow shared by system+vendor, **never allow** (S18); `system/` holds allow for system-component processes; `vendor/` holds allow for chipset/vendor-component processes.
- `sepolicy/ohos_product/<subsystem>/<component>/{public,system}/` — product policy.
- `sepolicy/base/public/attributes` — central place for attribute definitions (e.g. `parameter_attr`, `system_parameter_attr`).
- `sepolicy/base/public/parameter.te`, `service.te`, `domain.te` — control points containing default labels such as `default_param`/`default_service`/`default_hdf_service`.
- Chipset/vendor-component process types usually contain `hdf`/`vendor`/`chipset` (e.g. `hdfdomain`, `chipset_init`, `vendor_xxx`); the rest are usually system-component processes (e.g. `xxx_service`, `appspawn`, `init`).
- `service_contexts` (including `sepolicy/.../service_contexts` and the root-level `service_contexts`) — mapping of SA service names to SELinux types; modification requires **samgr domain review** (S21).
- `whitelist/flex/*_whitelist.json` — flex whitelist configuration; modification requires the **dedicated flex review** (S22).

Macro and attribute patterns (judgment reference):
- `debug_only(\`...\`)` and `developer_only(\`...\')` are isolation macros, closed with paired backticks.
- Product form-factor isolation macros (11 in total, conditionally expanded via `build_with_*` build switches): `pc_only`, `watch_only`, `glasses_only`, `phone_only`, `tablet_only`, `tv_only`, `smarthomehost_only`, `tablet_hybrid_only`, `emulator_only`, `car_only`, `ohos_only`. They may appear **only as `-` exception items** in the subject set of a neverallow or allow, and **must not wrap allow/allowxperm/neverallow statements** (S23; the script covers all 11).
- `allowxperm A B:C ioctl { 0xXXXX };` restricts ioctl command codes.
- neverallow relaxation pattern: `neverallow { domain -violator_xxx } ...`, `-rgm_violater_xxx`.
- su as subject (`allow su ...`) is allowed by default; su as object (`... su:... { ... }`) requires `debug_only` isolation.

## 2. Workflow

### Step 1: Determine the scan target

Ask the user to choose one — **local code or a remote PR** — and confirm the scope when ambiguous. Do not guess.

- **Local code** — a checkout of the target repository. Scope: uncommitted changes (working tree + index), a single commit/sha/tag, a branch (any spelling: `feature`, `origin/feature`, full ref), or a `<base>..<head>` range — anything resolvable in the local repository. Default when the user gives no scope: the latest commit at HEAD.
- **Remote PR** — an upstream PR number/URL; always scanned as its full net diff. Obtain the diff by any of: `oh-gc pr diff <number> --repo <owner>/<repo>` (requires the oh-gc CLI), fetching the PR branch locally and diffing (`git diff <base>...<pr-head>`), or exporting the .diff/.patch from the web UI and piping it via stdin. The oh-gc rendered format (`diff --git`/`status:`/`---`/`@@` with no `+++ b/` lines) is normalized automatically on stdin, so file-level checks and the summary are not lost. scan.py itself has no dependency beyond Python 3 — oh-gc is never required to run the check.

Only policy files are reviewed — `sepolicy/`, `service_contexts`, `whitelist/`. scan.py filters by this pathspec automatically in ref mode; when piping a diff via stdin, filter it with the same pathspec first (non-policy changes such as C++ code are otherwise over-counted in the summary).

> Ref semantics: branch refs auto-resolve the merge-base and scan the net diff; a bare commit/tag (sha, HEAD) scans that commit only. Details: [`references/scan-output-guide.md`](references/scan-output-guide.md).

### Step 2: Determine the diff nature (thinking framework)

Before running the script, ask yourself what the **nature** of this diff is — it sets the judgment tone for S17/S19 etc.:

- **New permissions** (+allow without a corresponding −allow) → judge strictly on all items: S17 must have #avc: comments, S19 must have blank-line separation.
- **Rename refactor** (+allow and −allow pair up one-to-one, only subject/object renamed, e.g. type→attribute) → **no new permissions**. For S17 #avc:, S19 blank lines, S18-A public/ placement, or S2-A base/ placement that are pre-existing omissions or pre-existing placements (the original −allow line was already there), annotate "pre-existing; this rename did not change the wrapping/placement" instead of hard-reporting a violation; in ROM estimation A≈D, net ≈ 0.
- **Policy reduction** (mostly − lines) → most items NA.
- **New/modified neverallow** → triggers S4/S11, requires security review confirmation.

> **Mixed-diff principle**: when rename and new permissions coexist in one commit, judge per allow line — lines with a corresponding −allow that only rename follow the rename tone (pre-existing annotation); lines without a corresponding −allow follow the new-permission tone (S17 must have #avc:, S19 must have blank lines). Do not downgrade the whole file just because some lines are renames.

> Tip: use `git diff --stat` for a quick add/delete ratio; A≈D with unchanged file names usually means rename. Always state the judgment tone at the beginning of the report to avoid false positives on refactor diffs.

### Step 3: Part 1 — run the lint script (MANDATORY)

**MANDATORY**: run [`scripts/scan.py`](scripts/scan.py) (Python 3, zero dependencies) to cover all automatically checkable items and output the ROM estimation. **Do not modify the script** — for custom checks create a separate script. Script self-test (two-gate regression): `python3 "${SKILL_DIR}/scripts/run_evals.py"` must print `SCANNER REGRESSION PASSED`; `python3 "${SKILL_DIR}/scripts/run_evals.py" --reports "${SKILL_DIR}/evals/reports"` must print `ALL GATES PASSED` (structurally validates every golden report — unique rows, single-enum statuses, sign-aware ROM/A/D/M cross-checked against the scanner, status-to-disposal forcing — then grades every assertion's grader rules).

**Do NOT Load**: if the diff from Step 1 is empty, **do not run scan.py** — output an all-NA report directly.

`SKILL_DIR` = this skill's package root (the directory containing `SKILL.md`, `scripts/`, `references/`):

```bash
python3 "${SKILL_DIR}/scripts/scan.py" <commit>         # single commit/tag (sha, HEAD): scans that commit only
python3 "${SKILL_DIR}/scripts/scan.py" <base>..<head>   # range net diff (required for PR/multi-commit)
python3 "${SKILL_DIR}/scripts/scan.py" <branch>         # branch ref (feature, origin/feature, refs/heads/feature):
                                                         # merge-base auto-resolved, scans the full net diff
echo "$DIFF" | python3 "${SKILL_DIR}/scripts/scan.py" - # read diff from stdin
```

**MANDATORY — READ ENTIRE FILE**: the script output interpretation table (script/semantic division, ref semantics and boundary behavior) is in [`references/scan-output-guide.md`](references/scan-output-guide.md); read it before judging any item.

### Step 4: Part 2 — semantic analysis (items the script cannot check)

Analyze each item the script cannot cover and give the judgment rationale (citing Section 4 rules and Section 1 conventions):

- **S2-B qualification**: are multiple directories related changes of one feature (e.g. exemption+grant pairing), or should the MR be split?
- **S5/S6/S7 guardrails and scope**: does the SA service need a neverallow guardrail; does hap gain system-parameter write access; does the write+execute label need neverallow control?
- **S9/S10 isolation coverage**: do debug_only/developer_only macros cover all debug/developer permissions (macro positions come from the script; coverage needs semantic judgment)?
- **S11 review records**: do neverallow modifications and non-flex whitelists already have security review records (not visible in the diff — mark WARNING truthfully)?
- **S13 wrapping**: is the su-object allow inside debug_only?
- **S15 hap scope**: all apps → `hap_domain`; a subset of apps → explicit concrete types.
- **S17 one-to-one correspondence**: equal counts do not mean correct pairing — run `git show <target-ref>:<file> | grep -B2 '<allow keyword>'` to check comments outside hunks and verify pairing (`<target-ref>` = the ref actually scanned — commit/branch/range head, or the PR head for a remote PR; for stdin, read the file from the PR/commit under review, never the local checkout).
- **S18-B/C placement**: judge system/ or vendor/ placement mismatches by subject type features (hdf/vendor/chipset vs system service).
- **S23 review**: the script already judges per macro instance; the AI reviews inline macro argument semantics (truly new permission/domain vs exception).

### Step 5: Output the report

Ask yourself first: who reads the report — the submitter (needs to know how to fix) or a reviewer (needs to know whether to approve)? For a submitter, every FAIL/SUGGESTION/WARNING item must carry a fix suggestion, not just the problem.

Generate the report per the Section 5 template, **in Chinese**, and **must separate three disposal groups**: Must Fix (FAIL), Suggested Fix (SUGGESTION), Review Required (WARNING). **Every disposal item must quote the concrete policy content** (the original diff line; S1 sensitive words masked as `***`), not just `file:line`.

## 3. Status Definitions and Disposal Classification

| Status | Meaning | Disposal requirement |
|--------|---------|----------------------|
| PASS | Diff involves this item and complies | No action |
| SUGGESTION | Optimization suggestion, not a hard violation (e.g. S4 placement, S20/S20b macro replacement) | **Suggested fix**: submitter decides after evaluation; does not block merge |
| WARNING | Needs confirmation by domain team / security review / dedicated review (S3 init, S11 security, S21 samgr, S22 flex, etc.) | **Review required**: contact the confirming team; merge after the conclusion is filled back |
| FAIL | Clear violation (any NEVER-table hit, S2-A pure addition, S16, S19 missing blank line, etc.) | **Must fix**: fix before merge |
| NA | Diff does not involve this item | No action |

## 4. Self-Check Rule List

> Judge only added diff lines (`+` lines). `file:line` refers to the **post-diff target file line number**.
> S1–S7, S9–S13, S15–S16 are policy merge self-check items (S8/S14 removed, numbers not reused); S17–S23 are supplementary extension items.
> Each entry is tagged with its check mode: **[script]** script-decided (AI only reviews false positives) / **[script+semantic]** script locates + AI judges / **[semantic]** AI judges.

### NEVER — absolute prohibitions (any hit = FAIL, must fix)

| # | Rule | One-line reason | Entry |
|---|------|-----------------|-------|
| 1 | Adding policy or attributes to `sepolicy/base/` | Pollutes every image, bypasses domain review (exception: modifying existing lines is exempt) | S2-A |
| 2 | Adding `allow` under `public/` | Compiled into both system+vendor, breaks least privilege | S18-A |
| 3 | Using `default_*`/`limit_domain` as an allow target | Grants whole-domain permissions, defeats SELinux | S16 |
| 4 | su as object without `debug_only` isolation | Grants root-equivalent access to any domain in commercial builds | S13 |
| 5 | Multiple same-kind violator exemptions in one neverallow | Multiple exemptions defeat the guardrail (script reports candidates first; final level after semantic verification) | S11a |
| 6 | Violator naming/partition prefix mismatch (violator not a prefix, or system/vendor partition definition without the matching prefix) | Naming convention broken, acting partition unclear | S11d |
| 7 | New allow without `#avc:` comment (missing in the whole file) | No way to trace the trigger scenario (check the whole file as WARNING first; raise to FAIL only when confirmed missing) | S17 |
| 8 | debug/developer permissions without `debug_only`/`developer_only` | Backdoor in release builds | S9/S10 |
| 9 | Product macro wrapping an allow or neverallow statement | Other device forms lose the permission/guardrail; product macros are `-` exception items only | S23 |

### S1 — no sensitive words in policy or comments **[script]**
- **Detection**: added lines (including `#` comments) matched against the sensitive word list — **vendor/competitor/platform brand words only** (`android`, `google`, `aosp`, `huawei`, `harmonyos`, etc., case-insensitive). Technical words such as passwords/tokens/internal IPs are not checked.
- **Violation**: any added line (non-license header) containing a brand word.
- **Report anonymization**: the report **must not reveal the concrete sensitive word**; mask it uniformly as `***`.

### S2 — policy goes to sepolicy/ohos_policy, not sepolicy/base; one MR should keep policy in one directory
- **Detection A (base placement) [script]**: purely added lines under `sepolicy/base/` (all policy files: `.te`/`file_contexts`/`attributes` etc.). Only a −/+ pair **inside the same replacement block** with the **same pairing signature** — same statement kind (allow/allowxperm/neverallow/attribute/typeattribute/type) plus, for rule statements, the same `object:class` — counts as "modifying an existing line" and is exempt; each removed line exempts at most one added line of the same signature. Comments, blank lines and unrelated/different-kind statements never provide exemptions; deletions in other hunks/files never exempt additions. The `attributes` file is not exempt — adding an attribute definition to `base/public/attributes` is equally a violation. The AI reviews rename nature per Step 2 (a −/+ pair moved across files may be annotated as rename instead of mechanically reported; a subject rename keeping `object:class` still pairs).
- **Detection B (directory concentration) [script+semantic]**: count the involved `sepolicy/ohos_policy/<subsystem>/<component>` directory combinations (ignoring `public`/`system`/`vendor` subdirectory differences). ≥2 directories → WARNING: assess whether they are related changes of one feature (e.g. exemption+grant pairing) — if related, explain the relation; unrelated features should be split into separate MRs.
- **Compliant**: new policy lands under `sepolicy/ohos_policy/<subsystem>/<component>/{public,system,vendor}/`; one MR concentrates changes in one `<subsystem>/<component>` directory.

### S3 — new parameter labels must end with parameter_attr and be agreed with the init domain team **[script]**
- **Detection**: new `type xxx, parameter_attr;`. Involved → WARNING (init domain team).
- Parameter spec: https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/subsystems/subsys-boot-init-sysparam.md

### S4 — neverallow placement: if all referenced type/attribute definitions are in public/, suggest public/ **[script]**
- **Detection**: for type/attribute references of a new neverallow (excluding `-` exception items and product/isolation macro contents), the script looks up definition locations via `git grep <target-tree>` — **bound to the scanned target's tree** (commit/branch/range head), never the current checkout, so the verdict stays identical across different checkouts. All defined in public/ and the current file is not public/ → SUGGESTION to move to public/ for shared control; any non-public definition → current placement is reasonable; definition not found → `[S4 needs confirmation]`; no target tree bound (stdin mode) → the script prints the reference list (`[S4] no target tree bound`) and stays pending — rerun scan.py with the target ref to complete the check; never substitute the current checkout.
- **Status**: SUGGESTION (non-hard).

### S5 — SA services not accessible to apps must be guarded by neverallow **[script+semantic]**
- **Detection**: for a new SA service label (`type xxx, sa_service_attr;`) or a new allow on an SA service, assess whether a guardrail like `neverallow { domain -xxx } <service>:samgr_class *;` should be added.
- **Judgment**: involved → WARNING on whether to add the guardrail.

### S6 — system parameters must not be configurable by third-party apps **[script+semantic]**
- **Detection**: new allow on `parameter_service` or parameter-related targets; explicitly granting parameter write to hap → FAIL.
- **Judgment**: involved → WARNING.

### S7 — file/directory labels with write+execute must be controlled by neverallow **[script+semantic]**
- **Detection**: new file/directory labels with both write and execute; a neverallow guardrail should prevent unauthorized domains from gaining write+execute.
- **Judgment**: involved → WARNING on whether to add neverallow control.

### S9 — debug-mode permissions must be isolated with debug_only **[script+semantic]**
- **Detection**: if a new allow only serves debug-mode features (debug interfaces, debug log switches, debug-only services, `hdc`/`hdcd`/`debuggerd` related), check whether it is wrapped in `debug_only(\`...\')`. Macro positions come from the script; whether the wrapping covers all debug permissions is judged by the AI.
- **Violation**: debug-only permissions without `debug_only` isolation.

### S10 — developer-mode permissions must be isolated with developer_only **[script+semantic]**
- **Detection**: if a new allow serves developer-mode features (`devicedebug`, `hnp`, developer options related), check whether it is wrapped in `developer_only(\`...\')`.
- **Violation**: developer-mode permissions without `developer_only` isolation.

### S11 — modifying neverallow and other whitelists requires security review (four sub-items)
- **S11a [script+semantic]**: each neverallow allows only a **single** `-violator_xxx` and a **single** `-rgm_violater_xxx`; multiple same-kind exemptions → FAIL.
- **S11b [semantic]**: every new `attribute violator_xx` / `typeattribute ... violator_xx` needs a corresponding `neverallow violater_xxx ...` guardrail. Guardrail completeness verification is folded into the security review confirmation (see the S11 judgment below); no cross-repository check.
- **S11c [script]**: the diff touches non-flex whitelist files under `whitelist/` (excluding `perm_group_whitelist.json`) → WARNING (security review).
- **S11d [script]**: when a new `attribute` / `typeattribute` name contains `violator` or the `violater` spelling variant (upstream real spelling; both declaration forms parsed), the name must **start with** `violator_`, `rgm_violator_`, `system_violator_`, or `vendor_violator_` — the marker must not appear in the middle of the name (→ FAIL). **Partition prefix (deterministic)**: a violator defined in a `system/` partition file must start with `system_violator_`; one defined in `vendor/` must start with `vendor_violator_` (definition location is the acting partition) → any mismatch is FAIL; definitions in `public/`/`base/` (cross-partition visible) use `violator_`/`rgm_violator_`.
- **Judgment**: modifying neverallow or non-flex whitelists → WARNING on whether security review has passed.

### S12 — new permissions with sh as subject require DFX + security review **[script]**
- **Detection**: new `allow sh ...` (sh as subject; indented macro-body statements are detected — matching is done on the comment-stripped, left-stripped code segment). Involved → WARNING.

### S13 — su as subject allowed by default; su as object requires debug_only **[script+semantic]**
- **Detection A (subject)**: `allow su b:c { ... }` — allowed by default; adding it is redundant but not a violation (indented statements are detected the same as top-level ones).
- **Detection B (object)**: `allow <domain> su:<class> { ... }` — must be wrapped in `debug_only(\`...\')`; unwrapped → FAIL.

### S15 — hap-related permissions need scope confirmation **[script+semantic]**
- **Detection**: new allow involving apps (hap). Applies to all apps → `hap_domain`; a subset → explicit concrete types.
- **Judgment**: involved → WARNING on hap scope.

### S16 — default labels forbidden **[script]**
- **Detection**: new **policy statements** (comment segments excluded) introducing `limit_domain` / `default_param` / `default_service` / `default_hdf_service` as a used type or allow target. Mentioning default label names in comments is not a violation.
- **Violation**: new content using the above default labels.

### S17 — every allow/allowxperm must carry an avc log comment **[script+semantic]**
- **Detection [script]**: every new `allow`/`allowxperm` should have a `#avc:` (or `# avc:`) comment line in the same block recording the avc denied log (`scontext`/`tcontext`/`tclass`/`permissive`). The script judges proximity per hunk independently (no cross-hunk/cross-file association) and prints `[avc gap]` lines plus the count comparison.
- **Confirmation [semantic]**: when no comment is seen inside a hunk, the `#avc:` may exist outside the hunk (common in large files); check the **scanned target's version** of the file — `git show <target-ref>:<file_path> | grep -B2 '<allow keyword>'` (for a remote PR, the PR head; for stdin, the file from the PR/commit under review) — and raise to FAIL only when confirmed missing in that version; never consult the local checkout when another target was scanned.
- **Key points**: one `#avc:` shared by multiple allows is insufficient; equal counts do not mean correct pairing — manual verification still applies. **Exception exemption**: pure `-` exception items appearing only in neverallow subjects (`-local_code_sign`, `pc_only(`-violator_xxx')`, etc.) are never counted — exceptions exclude rather than grant permissions; but the script counts every new allow/allowxperm line, including lines whose subject set contains `-` exception items — such lines are still new permissions and still need `#avc:`.

### S18 — allow placement: system components in system/, chipset components in vendor/, no allow in public/
- **Detection A [script]**: a new allow located in a file under `public/` → FAIL.
- **Detection B/C [script+semantic]**: the script lists allows with their directories; the AI judges by subject type features — a system component (`xxx_service`, `appspawn`, `init`, etc.) placed in `vendor/`, or a chipset component (containing `hdf`/`vendor`/`chipset`) placed in `system/` → WARNING for placement mismatch.
- **Compliant**: system-component allows in `system/`, chipset-component allows in `vendor/`, no allows in `public/`.

### S19 — two allow statements must be separated by a blank line **[script]**
- **Detection**: adjacency is tracked on the **new side** (context + added lines; removed lines are old side). Two adjacent allows (including `allowxperm`) with no blank line between them — `#avc:` comments belong to the allow block and do not count as separation — are reported when **either side of the pair is newly added**: a new rule glued to a pre-existing (context) allow counts, and so does a new rule followed directly by a pre-existing allow. Only context-context adjacency (both sides pre-existing) stays unreported; each added line is reported at most once. No false positives across files/hunks; pre-existing adjacencies surfaced by rename-refactor replacements are annotated per the Step 2 tone instead of hard-reported.

### S20 — when the allow object is appdat, suggest normal_app_data **[script]**
- **Detection**: new `allow <subject> appdat:<class> { ... }`.
- **Suggestion**: SUGGESTION to switch to the `normal_app_data` macro (expands to `{ normal_hap_data_file appdat }`), the standard abstraction covering normal-app data, consistent with existing policy.

### S20b — binder IPC permission check and binder_call macro suggestion **[script]**
- **Detection**: the same subject gains binder `call`/`transfer` permissions on the same object (two separate allows or one combined form; `allow` statements only — neverallow/comments never trigger). Indented macro bodies are also detected. Detection anchors on brace-form `:binder { … }` statements; braceless `allow a b:binder call;`-style pairs are not detected (semantic review covers).
- **Judgment**: a hand-written `allow <subject> <object>:binder { call transfer };` grants only these two permissions; confirm whether the binder IPC path omits companion permissions — **the server→client reverse transfer and `fd use`** — whose omission causes runtime avc denied. The `binder_call(<subject>, <object>)` macro (defined in `sepolicy/base/public/glb_scontext.te`) expands to **more than** `{ call transfer }` (also reverse transfer and fd use); it completes binder IPC permissions and prevents omissions.
- **Suggestion**: SUGGESTION to switch to `binder_call` for complete IPC permissions; note the macro is not an equivalent replacement (it grants more), ROM increases by about 300B, and whether all macro permissions are needed must be confirmed against the actual call chain.

### S21 — service_contexts modification requires samgr domain review **[script]**
- **Detection**: the diff touches any added/modified line of a `service_contexts` file (root level included) → WARNING (samgr domain review of the service-name-to-type mapping and of the type being defined in `.te`).

### S22 — whitelist/flex *_whitelist.json requires the dedicated flex review **[script]**
- **Detection**: the diff touches any added/modified line of `whitelist/flex/*_whitelist.json` → WARNING (flex review of entry necessity, scope minimization, no over-permissive entries).

### S23 — product macros (the 11 *_only form-factor macros, full list in Section 1) are exception items only **[script]**
- **Background**: the only permitted use of a product form-factor isolation macro is as a `-` exception item in the subject set of a neverallow or allow (e.g. `pc_only(\`-storage_daemon')`) — exception items conditionally exclude domains by device form; wrapping statements would make other device forms lose permissions/guardrails. Forbidden: ① wrapping `allow`/`allowxperm` to add permissions; ② wrapping `neverallow` to add guardrails.
- **Detection** (script covers all 11 product macros): an inline macro argument starting with `-` = a legal exception item; an argument not starting with `-` on a line containing an allow/allowxperm/neverallow statement = FAIL (when legal and illegal macro instances are mixed on one line, only the illegal instance is reported). Multi-line wraps: a **nesting stack** over comment-stripped code tracks all backtick macros (product + debug_only/developer_only) — an inner `')` close pops only the innermost frame, so a rule added after an inner isolation-macro close but still inside an outer product macro is still reported; comment-only lines (e.g. `# pc_only(`) are transparent and can neither open nor close a scope; trailing comments on close lines (`') # end`) are stripped before matching. So: (1) a rule statement inside a wrap = FAIL even when the macro open and `')` close are both context lines and only the rule is newly added; (2) a **newly added** wrapper around pre-existing (context) rules = FAIL (the new wrap turns existing rules into form-factor isolation); a pre-existing wrapper containing only pre-existing rules is not reported. Scope resets at hunk/file boundaries.

## 5. Report Template

**MANDATORY — READ ENTIRE FILE**: the report template is in [`references/report-template.md`](references/report-template.md). Generate the report per the template, **in Chinese**; actionable items **must be grouped into three disposals**: 必须修复 Must Fix (FAIL), 建议修复 Suggested Fix (SUGGESTION), 需评审决策 Review Required (WARNING, with the confirming team named).

## 6. Execution Constraints

1. Read-only analysis: never modify any policy source file; output the report only.
2. Judgments are based on added diff content (`+` lines); do not speculate about context not visible in the diff.
3. For items needing domain-team/security-review confirmation, mark WARNING truthfully and name who must confirm; do not draw conclusions for the user.
4. **ROM increment must be reported truthfully**: whether the estimate is positive, negative, or 0 B, the report must include the ROM estimation with concrete values for A/D/M; **replacing or omitting the item** with vague conclusions such as "negligible increment" / "tiny impact" is forbidden.
5. Rule details reference https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/subsystems/subsys-security-selinux-checklist.md .
6. If the repository is not selinux_adapter, inform the user that this skill targets the selinux_adapter repository and ask whether to continue.
7. Do not restate derivation steps for script-decided items — give status and location only; semantic-analysis items must carry judgment rationale (rule entry and evidence cited).
