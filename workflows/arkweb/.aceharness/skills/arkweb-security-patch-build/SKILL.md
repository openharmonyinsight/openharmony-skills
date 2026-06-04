---
name: arkweb-security-patch-build
description: This skill should be used when the user asks to "编译 ArkWeb", "build ArkWeb", "执行 ArkWeb 编译", "验证 ArkWeb 构建", "排查 ArkWeb build.log", "分析 ArkWeb 编译失败", or mentions build_arkweb.sh, src/out/product/build.log, ArkWeb native or browser build targets, or incremental ArkWeb build verification. Handles command selection, incremental build execution, success verification, and build.log-first failure diagnosis for ArkWeb projects.
metadata:
  version: 0.1.3
  author: ringking0
---

# ArkWeb Build Skill

This skill supports building ArkWeb projects through `build_arkweb.sh`, verifying the result, and diagnosing failures from `src/out/<product>/build.log`.

Requires a Linux build host with GNU coreutils and `/proc` available.

For the slim ArkWeb patch workflow, load this skill's own references instead of referencing another skill:

- [references/batch-build-contract.md](references/batch-build-contract.md)
- [references/compile-adaptation-contract.md](references/compile-adaptation-contract.md)

## When to use this skill

Use it when the user wants to:

- run an ArkWeb build
- choose the right ArkWeb build target
- verify whether a build actually succeeded
- diagnose a failed ArkWeb build from logs
- continue an incremental ArkWeb build without cleaning the tree

## Project root rules

ArkWeb wrapper roots usually look like `arkweb_*` directories in the current workspace and contain:

- `build_arkweb.sh`
- `src/arkweb/build/build.sh`

Build commands must run from the wrapper root, not from `src/`.

Use this helper to find the root from anywhere inside the tree:

```bash
find_arkweb_root() {
  local dir="${1:-$PWD}"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/build_arkweb.sh" && -f "$dir/src/arkweb/build/build.sh" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  echo "ArkWeb root not found" >&2
  return 1
}
```

For git status and diff, use the real git repository under `src/`:

```bash
git -C "$(find_arkweb_root)/src" status --short
```

Note: `src` and `src/arkweb` are different git repositories. The `arkweb` repo lives under `src/`, but change diagnosis must inspect the two repos separately.

## Batch in-place verification

For `ArkWeb 本地 Issue 分析归档与上游安全补丁自动合入` batch mode, the active batch is applied directly into the current ArkWeb project git repository. Do not create git worktrees for build verification.

Rules:

- Do not apply or replay extra patches for build verification; verify the current in-place active batch as it exists.
- If the workflow asks for batch verification, first confirm `active_batch`, `duplicate_files`, and each issue's `target_subrepo` from `issues/{issue_id}/06_merge_result.md` or `batch_status.json`.
- Issues marked `deferred_for_archive` because they are duplicate/overlap non-winners are not part of the active batch; do not compile, repair, or submit them in this run. They are only summarized in the final report. Duplicate/overlap winner issues are part of the active batch and must be compiled, repaired, and submitted normally.
- If a local build is actually executed for the active batch and exits successfully, mark all active issues `ready_for_next`.
- In build verification, any completed non-zero build exit must route to build repair, even if the first useful root cause looks unrelated to the current patch. Build repair is the second-stage diagnosis gate that either performs a minimal patch-related fix, or proves the completed failure is unrelated and then marks the issue `ready_for_next` with a non-blocking build risk. Do not go directly from build verification to risk assessment on a compile failure.
- A build interruption is not an unrelated build failure. During build verification, poll the main `build_arkweb.sh` process, child `ninja` / `autoninja` processes, and `build.log` until the command returns a real exit code. If those processes disappear but `build.log` does not show a trustworthy success or failure ending and no real exit code was captured, record `build_completed=false` and `build_status=interrupted|incomplete`, then rerun the configured build once before making the stage verdict. The rerun may lower parallelism when resource pressure is suspected, but must not clean or reset the tree.
- If the first build attempt disappears before completion, the build-verification step must perform the retry immediately in the same step. It must not output `pass`, must not advance to risk assessment, and must not rely on risk assessment to notice missing `09_build_verification.md/json`.
- Only build repair may classify a completed build command with a real non-zero exit code as an unrelated non-blocking build risk. If the rerun still does not produce a trustworthy completed build result, do not mark `ready_for_next`; route to build repair for interruption diagnosis, and if no complete result can be obtained there, mark `submit_eligible=false` and block submission for that batch.
- If the build exits non-zero and the first useful root cause is related to a current patch issue, build verification must return `verdict=fail` and route to build repair. This is not final archive failure; it means the workflow must execute the build-repair state before risk assessment.
- Unrelated build failures include historical dirty changes, environment/resource pressure, LFS/SDK/toolchain problems, existing main-tree errors, another issue in the active batch, or files outside the current patch `modified_files[]` and final diff.
- Build commands normally run from the ArkWeb wrapper root. Use the configured `context.codebase` command once for the active batch; `context.projectRoot` is only the workflow output root.
- When a build fix is attributed to an issue, all diagnostics, git diff checks, and allowed fixes must stay within that issue's `modified_files[]` / `final_changed_files`.
- Build repair must first attempt a minimal fix for failures that are related to the current patch. Do not return final `fail` for a patch-related build error before attempting the minimal in-scope repair. For interrupted or incomplete builds, build repair must first attempt a controlled rerun and record whether a complete exit code was obtained. Build repair must show verifiable progress: a repair diff, changed root cause, changed next build error location, a concrete retry basis, a completed rerun with a trustworthy exit code, or clear evidence that the completed failure is unrelated to the current patch and should be `conditional_pass`. Mark only that issue `terminal_failed` after an attempted repair/rerun cannot continue, the fix would require files outside the allowed patch scope, or one repair round has no diff change, no root-cause change, no retry basis, and no unrelated-failure evidence; it must not prevent the current stage from advancing once all pending_current_stage issues are resolved. If build repair produced an in-scope fix or changed root cause, the top-level build-repair verdict must be `pass,next_state=编译验证` so the workflow reruns build verification. If pending_current_stage is empty and at least one ready_for_next issue remains, the top-level build-repair verdict must be `conditional_pass,next_state=风险评估`. Build repair must not return `conditional_pass,next_state=编译修复`, because the YAML transition for conditional_pass leaves the build-repair state. Top-level `fail` is allowed only when no ready_for_next issue remains, the whole batch has an unrecoverable infrastructure failure, or repeated interruption means no trustworthy completed build result exists.
- Batch output must be per issue: write `.ace-outputs/{runId}/issues/{issue_id}/09_build_verification.md` summaries and a root `.ace-outputs/{runId}/09_build_verification.md` summary. Active issues, including duplicate/overlap winners, must carry `stage_status=ready_for_next|pending_current_stage|terminal_failed`; overlap non-winners may remain `deferred_for_archive` and are excluded from build verdict aggregation. Top-level verdict must keep ready_for_next issues waiting while any pending_current_stage issue remains. Build verification routes completed non-zero exits to build repair. Build repair either returns to build verification after an in-scope repair, or advances all ready_for_next issues together once pending is clear.
- Build verification may output `verdict=pass,next_state=风险评估` only after root `09_build_verification.md` and `09_build_verification.json` both exist and the JSON records `build_completed=true`, `build_status=success`, `exit_code=0`, and `submit_eligible=true`. Missing root build-verification artifacts are a build-verification failure, not a risk-assessment input.

## Workflow final reply contract

For workflow state-machine steps, the final assistant reply must be easy for the runner to parse:

- Output exactly one JSON code block at the end of the reply.
- That JSON must contain `verdict`, `next_state`, `issues`, and `summary`.
- Do not output a second JSON block such as `remaining_issues`.
- Do not output `<step-conclusion>` or any XML/HTML-style conclusion tag.
- Do not include "下一步建议", "下一步所需上下文", "涉及对象", or "验证状态" sections in the final reply. Put those details into `09_build_verification.md` or `10_build_fix.md` instead.
- For build verification, a completed non-zero build exit must use:

```json
{
  "verdict": "fail",
  "next_state": "编译修复",
  "issues": [
    {
      "type": "implementation",
      "severity": "major",
      "description": "编译命令完整退出且返回非零，需要进入编译修复。"
    }
  ],
  "summary": "编译失败，进入编译修复。"
}
```

- For build verification, a successful build must use `verdict=pass,next_state=风险评估`.
- For build verification, do not use `verdict=pass` unless `09_build_verification.md/json` were written and the JSON has `build_completed=true`, `build_status=success`, `exit_code=0`, and `submit_eligible=true`.
- Only build repair may use `conditional_pass,next_state=风险评估` after proving a completed build failure is unrelated or after clearing pending issues.
- Build repair must never use `conditional_pass,next_state=编译修复`; use `pass,next_state=编译验证` after a repair attempt that needs re-verification.

## Workflow build configuration

For this workflow, users do not configure `context.automation.*` fields from the Web UI. Treat those fields as absent unless they are explicitly present in the YAML.

Default build settings:

- ArkWeb root: `context.codebase`
- build command: `./build_arkweb.sh rk3568_64 -t w -A`
- build output dir: `context.codebase/src/out/rk3568_64`
- timeout: `context.timeoutMinutes`

## Default build behavior

Default to incremental builds. Do not clean the tree unless the user explicitly asks for a clean build.

Never do these automatically:

- `git clean`
- `git reset --hard`
- `rm -rf src/out`
- `gn clean`
- `ninja -t clean`
- re-syncing dependencies just to "get a clean environment"

Before starting a build, always check whether the current product has been built before. Use the presence of `src/out/<product>/build.log` as the primary signal:

```bash
if [[ -f <arkweb-root>/src/out/rk3568_64/build.log ]]; then
  echo "Incremental build path"
else
  echo "First build path"
fi
```

If `build.log` does not exist yet, treat it as a first build unless the caller provides stronger evidence otherwise. The first build is usually much slower and should be called out explicitly before running it:

- expected duration: about 2 to 3 hours
- do not mislabel this as a normal incremental build
- avoid prematurely judging the build as hung just because it stays in setup or prebuild stages for a long time

Primary default command:

```bash
cd <arkweb-root>
./build_arkweb.sh rk3568_64 -t w -A
```

The most common variations are listed in [references/build-commands.md](references/build-commands.md).

## Repair responsibility and change boundaries

When the build fails, do not stop at extracting and reporting the error. The default expectation is to continue through root-cause analysis, make an allowed fix, and rerun the build to verify the result.

Allowed fixes:

- modify source files, `BUILD.gn` / `.gni`, ArkWeb-owned build scripts, or project configuration inside the current ArkWeb tree
- restore missing Git LFS assets for the current project, or rerun build commands inside the current project
- adjust the build target, resume strategy, or parallelism, then verify with another build

Explicitly forbidden changes:

- do not modify toolchains, SDK archives, install scripts, or other prebuilt payloads under `<arkweb-root>/src/ohos_sdk/`
- do not modify server files outside the current ArkWeb project directory, including other checkouts, global environment files, system directories, or unrelated files under the user home directory

If the problem can only be bypassed by touching one of those forbidden areas, call that out explicitly as a constraint and switch to an in-project alternative such as:

- rechecking and restoring the current project's Git LFS assets
- fixing dependencies, target wiring, or source errors inside the current project
- lowering parallelism and rerunning the build

## Change-first diagnosis

To localize build failures faster, inspect what the developer changed before widening the search. Most build failures are introduced by the current patch, so starting from `git` usually gives a faster and more accurate path to a minimal fix.

ArkWeb trees often come with default dirty files that should not be treated as developer edits. Start with the bundled filter script:

- `bash <skill-dir>/scripts/show_relevant_changes.sh <arkweb-root>`

Filter rules built into the bundled script:

- ignore the whole `third_party/rust-toolchain/` directory by prefix
- ignore the whole `third_party/rust/chromium_crates_io/` directory by prefix
- in the `src` repo, also ignore these exact default-noise entries:
  `third_party/ohos_ndk/includes/ohos_adapter/screenlock_manager_adapter.h`,
  `third_party/ohos_nweb_hap/hvigor/`,
  `third_party/ohos_nweb_hap/signature/`
- in the `src/arkweb` repo, also ignore this exact default-noise entry:
  `build/search_engines/prepopulated_engines.json`

If more raw git detail is still needed, check these next:

- `git -C <arkweb-root>/src status --short`
- `git -C <arkweb-root>/src diff --stat`
- `git -C <arkweb-root>/src diff --cached --stat`
- `git -C <arkweb-root>/src/arkweb status --short`
- `git -C <arkweb-root>/src/arkweb diff --stat`
- `git -C <arkweb-root>/src/arkweb diff --cached --stat`
- if `build.log` already points to a file, target, or symbol, inspect the matching path with `git diff`

Diagnosis rules:

- correlate the failing file, target, or missing symbol in the log with the current developer changes first
- filter out default dirty entries before deciding which changes are truly relevant to the failure
- if the current patch already explains the failure, do not broaden the search to unrelated directories or targets
- aim for a minimal fix, usually near the changed code or dependency declaration that introduced the failure
- only expand into broader project-level investigation when the current `git` changes do not explain the problem

## Failure stage classification

Before choosing a rerun strategy, classify the failure stage from `build.log`:

- `pre-gn/sdk-lfs`: SDK install, archive extraction, Git LFS pointer, missing package, `gzip`/`tar`/`unzip` errors before GN or Ninja. Fix assets or setup, then rerun the configured build command.
- `gn-generation`: `ERROR at //...`, `Unable to load`, bad `BUILD.gn` or `.gni` evaluation. Fix GN configuration, then rerun GN or the configured build command.
- `ninja-graph-or-target`: `ninja: error: unknown target`, missing `build.ninja`, or Ninja graph loading errors. Fix target selection or generated build graph, then rerun the configured target set.
- `ninja-compile-link`: compiler or linker failures after Ninja starts, such as `FAILED:`, `fatal error:`, `undefined reference`, `multiple definition`, `ld.lld: error`, or `clang++: error`.
- `resource-or-terminated`: explicit `killed` or `OutOfMemory`.
- `resource-or-terminated-suspected`: log tail still looks like Ninja progress, with no `FAILED:`, GN error, or Ninja target error. Treat this as a resource-pressure suspicion and inspect the latest snapshot before changing code.

Single-command quick verification is only for `ninja-compile-link`. After fixing that root cause, first `cd <arkweb-root>/src/out/<product>` and rerun the failed compiler or linker command shown after the first `FAILED:` line when it is available in `build.log`. The command is emitted relative to the Ninja output directory, so running it from the wrapper root or `src/` can fail incorrectly. If that command succeeds, switch back to the correct directory before broader verification: use `<arkweb-root>` for the full `build_arkweb.sh` command, or `<arkweb-root>/src` only when deliberately rerunning the same direct Ninja target set. Before that broader verification, still record a resource snapshot with `scripts/capture_resource_snapshot.sh`. Do not use single-command verification for `pre-gn/sdk-lfs`, `gn-generation`, or `ninja-graph-or-target`.

## Execution rules

1. Resolve the wrapper root and execute from there.
2. Prefer workflow-provided commands when present.
3. Run the build in the foreground and wait for the real exit code.
4. Use a long timeout. Default maximum wait: 4 hours.
5. Treat exit code `0` as success. Any non-zero exit, signal termination, timeout, or inability to run a trustworthy local build for the issue is a failure. In workflow build verification, every non-zero exit must use `verdict=fail` so the state machine enters build repair; do not use `conditional_pass` directly from build verification for compile failures. In build repair, unrelated failures may use `conditional_pass` only when the build command completed with a real non-zero exit code and the root cause is recorded as non-blocking risk. Signal termination, timeout, orphaned helper-only state, no real exit code, stale log, or inability to prove the main build command completed must be classified as `build_interrupted`/`build_incomplete`, not as unrelated failure.
6. On failure, inspect `src/out/<product>/build.log`, then immediately correlate it with recent developer changes from `bash <skill-dir>/scripts/show_relevant_changes.sh <arkweb-root>` so default dirty entries are filtered out first.
7. Before running the build, check whether `src/out/<product>/build.log` exists and tell the caller if this is likely a first build.
8. Record a resource snapshot for the Ninja phase. For `build_arkweb.sh`, capture it immediately before launching the build as the external baseline. For direct Ninja continuation, capture it immediately before the `ninja` command.
9. If the build stops without a compiler or linker error and the process is simply gone, suspect CPU or memory pressure first. Check the latest resource snapshot before drawing other conclusions.
10. In that silent-stop case, suggest lowering parallelism proactively, typically to `-j 32`, and then to `-j 16` if pressure remains high.
11. If `src/out/<product>/args.gn` already exists and the user is clearly continuing the same incremental build, a direct `ninja -C out/<product> <targets>` rerun from `src/` is acceptable. Reuse the same target set as the previous build, not a random single target. Do not switch to direct Ninja just to hide a `build_arkweb.sh` failure.
12. After a build error, the default flow is to complete the full loop of diagnose -> fix -> rebuild -> reverify, not just emit an error summary.
13. For `ninja-compile-link` failures, use the failed command and working directory shown by `scripts/analyze_build_error.sh` as a fast local check after fixing the issue. After that succeeds, record a new resource snapshot, then `cd <arkweb-root>` before rerunning the full configured `build_arkweb.sh` command; use `<arkweb-root>/src` only for an intentional direct Ninja target-set rerun.
14. While fixing the issue, only modify files that are allowed inside the current ArkWeb project. Do not touch `src/ohos_sdk/` and do not modify server files outside the project directory.
15. To converge faster and more accurately, try to explain the failure from the current `git` changes first and keep the repair minimal instead of editing unrelated files.
16. In batch mode, never fix one issue by editing files outside that issue's allowed file set. If a failure cannot be uniquely attributed to one issue, stop that issue and record `terminal_failed` or `pending_current_stage` in `batch_status.md/json`; it must not prevent the current stage from advancing once all pending_current_stage issues are resolved.
17. Build repair must not final-fail a patch-related build error before attempting a minimal in-scope repair. Mark an issue `terminal_failed` for `no_progress` only after the repair attempt cannot produce a repair diff, a changed root cause, a changed next build error location, a concrete retry basis, a completed rerun result, or clear evidence that the completed failure is unrelated to the current patch. If a completed build failure is proven unrelated to the current patch, mark that issue `ready_for_next` and wait for the current stage unified exit to risk assessment instead of repairing or blocking submission. If the build was interrupted, rerun first; if the rerun is still incomplete, record `submit_eligible=false` and do not return `conditional_pass` to risk assessment for that issue. If an in-scope repair was made, return top-level `pass,next_state=编译验证` so the workflow reruns build verification. If some issues become `terminal_failed` but pending is clear and ready issues remain, return top-level `conditional_pass,next_state=风险评估`, not `fail`.
18. A compile fix may intentionally differ from the upstream patch's exact text when adapting to the current ArkWeb branch, but it must be recorded as issue-scoped local adaptation. Write `compile_fix_required=true`, `compile_fix_files[]`, `local_adaptations[]`, `deviation_reason`, `upstream_patch_applied_exactly`, `semantic_landed`, and `semantic_equivalence_evidence` into `issues/{issue_id}/10_build_fix.md/json` and update the issue's merge/build status. This is success only when the original patch's security or functional semantics remain landed.
19. Build repair files must be added to the current issue's submit scope only through `local_adaptations[]` / `compile_fix_files[]`. Do not silently expand `final_changed_files` with global worktree diffs, and do not let a compile fix hide a missing upstream patch hunk. If the patch semantics are not landed, keep or add a blocker and mark the issue `pending_current_stage` or `terminal_failed`.

## Logs and diagnostics

The primary log is:

```text
<arkweb-root>/src/out/<product>/build.log
```

Older logs are usually rotated to timestamped names when a new build starts.

Always inspect the log tail first:

```bash
tail -200 <arkweb-root>/src/out/<product>/build.log
```

If that is not enough, search for:

- `error:`
- `fatal error`
- `undefined reference`
- `multiple definition`
- `ERROR at`
- `No such file`
- `cannot find`
- `killed`
- `OutOfMemory`

Use the bundled scripts:

- `scripts/analyze_build_error.sh` for a structured summary, failure stage classification, first-error context, and failed Ninja command candidate. It accepts either `<product> <arkweb-root>` or `<build.log> <arkweb-root>`.
- `scripts/find_recent_errors.sh` for a quick recent-error scan
- `scripts/inspect_build_state.sh` to inspect available output directories and recent logs
  Run this shell script with `bash <skill-dir>/scripts/inspect_build_state.sh rk3568_64 <arkweb-root>`. Do not execute it with `python3`.
- `scripts/check_lfs_artifacts.sh` to parse the relevant LFS attribute files, check required prebuilts, and detect missing files or LFS pointer files
- `scripts/capture_resource_snapshot.sh` to record CPU and memory headroom before the Ninja phase, so silent build exits can be diagnosed as likely resource pressure. Its first argument is the product name; the ArkWeb root is the third argument in the labeled form or the second argument in the short form.
- `scripts/show_relevant_changes.sh` to filter expected dirty files and show the relevant git changes separately for the `src` repo and the `src/arkweb` repo
  It uses `git status --short -uall`, prints ignored default dirty entries, and supports `--show-all` / `--no-ignore` when the full raw view is needed.

In commands below, `<skill-dir>` means the directory containing this `SKILL.md`.

See:

- [references/build-commands.md](references/build-commands.md)
- [references/common-errors.md](references/common-errors.md)
- [references/log-locations.md](references/log-locations.md)
- [examples/example-workflow.md](examples/example-workflow.md)

## Output expectations

A good build answer should include:

- the exact command used
- the working directory
- the product and target
- the exit status
- the log path checked
- the failure type and location if it failed
- the minimal next fix or next command
