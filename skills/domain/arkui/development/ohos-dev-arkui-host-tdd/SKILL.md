---
name: ohos-dev-arkui-host-tdd
description: Design, add, fix, classify, build, run, and report OpenHarmony ArkUI ace_engine host unit tests with defense-first TDD. Use when working under OpenHarmony/foundation/arkui/ace_engine on host_product gtests to determine whether an ace_unittest suite is reachable and host-compliant, remediate missing host BUILD.gn routing or mocks, reproduce failing or crashing tests with exe.unstripped symbols, delegate ace_engine_test builds through ohos-dev-arkui-ace-engine-build, run focused --gtest_filter cases, or verify drawable, image, text, frameworks, and core unit-test changes.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkui
  capability: host-tdd
  version: 0.1.2
  status: trial
  related-skills:
    - name: ohos-dev-arkui-ace-engine-build
      min_version: "0.3.0"
      required: true
      probes:
        - "test -r {dir}/scripts/build_wrapper.sh"
        - "test -r {dir}/scripts/monitor_progress.sh"
        - "test -r {dir}/scripts/build_state.py"
        - "test -r {dir}/scripts/run_build_session.sh"
---

# OHOS Dev ArkUI Host TDD

Use this process to turn an ace_engine host-test request into a verified result without confusing build eligibility, compilation, and test execution.

## Operating Model

Use these path names consistently:

- `<oh-root>`: the OpenHarmony root containing `build.sh`.
- `<ace-root>`: `<oh-root>/foundation/arkui/ace_engine`.
- `<host-out>`: `<oh-root>/out/host/host_product`.

Direct local execution in this skill applies to `host_product`. If the user requests a device product, use it only for build verification and do not apply the host binary paths or host-run claims below. A device-product build does not populate `out/host`; a separate `host_product` build is required before local host execution.

### Build Authority

When any build is required, invoke and follow `$ohos-dev-arkui-ace-engine-build`. This Host TDD skill owns **why and what** to build; the build skill owns **where and how** to launch, detect active builds, detach the process, monitor it, and classify completion. Treat the installed build skill as the current source of truth rather than copying a partial build contract here.

Treat `ohos-dev-arkui-ace-engine-build` as a required runtime dependency for every build-required route. Before emitting or executing a build plan:

1. Confirm that the available-skill catalog contains the exact skill name `ohos-dev-arkui-ace-engine-build`.
2. Resolve and read its installed `SKILL.md`; require `metadata.version` `0.3.0` or later.
3. Confirm that its resolved skill directory contains readable `scripts/build_wrapper.sh`, `scripts/monitor_progress.sh`, `scripts/build_state.py`, and `scripts/run_build_session.sh`. Resolve these paths from the installed skill location; do not guess a conventional installation directory.

If the skill is missing, unreadable, version-incompatible, or lacks any required lifecycle helper, stop the build/run route before launching or executing a test that requires new artifacts. Report `missing or incompatible required skill: ohos-dev-arkui-ace-engine-build` and the failed probe. Preserve any completed static audit or test-design findings, but do not call `./build.sh`, invoke Ninja as a fallback, copy a remembered build command, or approximate the missing lifecycle.

Never call `./build.sh` directly from this workflow. Do not replace the build skill's lifecycle with an untracked shell or background command. Use a targeted Ninja build only when the current build skill and repository rules explicitly allow it, after the same active-build and provenance guards.

In every build-related plan or report, emit an explicit environment gate before any launch instruction: **use a real writable OpenHarmony Host environment; if `<oh-root>/out` is not writable in the current sandbox, request the required permission and do not launch yet.**

Whenever a plan mentions a present or future `build_wrapper.sh` launch, immediately pair it with the corresponding `monitor_progress.sh --root <oh-root> --product <product> --target <target> --launch-id <wrapper-reported-id>` command and state that the workflow waits for its terminal result. Never leave a wrapper launch as the last build step.

Treat `monitor_progress.sh --check` as an observational query, not as a reservation. Another agent can launch after a no-active result. Only `build_wrapper.sh` provides the atomic per-product check-and-launch lock. If the wrapper rejects the launch because the lock or live metadata is owned, do not retry or touch the shared log; inspect the attributed build and wait, monitor, or report the conflict.

Route the request before doing work:

| Request | Route |
|---|---|
| Add or fix a test | Inspect knowledge and source → classify host compliance → design defenses → edit → delegate build lifecycle → focused run → surrounding run |
| Audit host compliance | Inspect knowledge, source, and the GN dependency graph → report compliant or give remediation; edit only when requested |
| Reproduce a failure or crash | Discover the existing suite → establish artifact freshness and provenance → delegate build if missing, stale, or unproven → run the exact symbolized filter; diagnose before editing |
| Build or rerun only | Delegate the complete build lifecycle; skip code analysis unless the build fails and diagnosis becomes necessary |
| Suite is not host-compliant | Stop before execution and report the missing host condition; never guess a binary path |

## 1. Establish Context and Knowledge

Start source inspection from `<ace-root>`. Run builds and direct binaries from `<oh-root>` unless a step says otherwise.

For tasks that require understanding code behavior, architecture, APIs, or failure causes, query the ace_engine knowledge base before reaching source-level conclusions.

```bash
# cwd: <ace-root>
python3 docs/kb_search.py text
python3 docs/kb_search.py "image animator"
python3 docs/kb_search.py --field keywords image
```

`docs/kb_search.py` accepts at most one positional keyword, so quote multi-word terms. If the first query is weak, try one better keyword or a field-constrained query. Treat the result as routing context and verify it against real source and tests.

Skip the KB lookup for a purely mechanical build or rerun. If the script is absent or fails, record that fact and continue source-first rather than blocking the task.

## 2. Inspect Source and Classify Host Compliance

Locate the implementation, existing tests, owning `ace_unittest("<binary>")`, and relevant GN groups. Search specifically for the symbol or test name plus `ace_unittest`, `module_name`, `is_host_product`, and failure text.

Classify static eligibility and built availability separately. Call a suite **host-configured** only when all of these conditions hold:

1. Its target is reachable through the full transitive `host_product` dependency closure rooted at `test/unittest:unittest`. Trace every intermediate GN target or group regardless of its directory or name; do not assume the current `base`, `core`, and `frameworks` routes are exhaustive. In the final audit, name every intermediate target and each verified guard explicitly, such as outer `!is_asan` and inner `is_host_product`; a line-range citation alone is not enough.
2. The host branch creates an executable suite, normally:

```gn
if (is_host_product) {
  ace_unittest("<binary>") {
    type = "host_components"
    module_name = "<SuiteDirectory>"
    sources = [ ... ]
  }
}
```

3. Host `sources` are non-empty.
4. Device-only runtime calls are absent or replaced by existing host mocks.

Call an artifact **host-runnable** only when the concrete output `<host-out>/tests/unittest/ace_engine/<SuiteDirectory>/<binary>` exists and is executable. This status proves file availability only; it does not prove that the artifact corresponds to the current source, tests, or build graph.

Classify **artifact-current** separately. Treat an artifact as current only when concrete provenance establishes all of the following:

1. It was produced for the active `host_product` configuration and owning target.
2. The successful build that produced it occurred after the latest relevant production source, test source, `BUILD.gn`, and `.gni` inputs, with no relevant working-tree change afterward.
3. The generated build graph did not require regeneration after that build.
4. When both stripped and `exe.unstripped` files are used, they belong to the same build, preferably verified by matching Build IDs.

A build completed in the current workflow is sufficient provenance. A trustworthy build record or manifest tied to the current tree and GN configuration may also be sufficient. File timestamps alone are not proof of currentness, but any relevant input newer than the artifact disproves currentness. If provenance cannot be established, classify `artifact-current` as **unproven** and rebuild before execution.

Check `<binary>_path.txt` separately as discovery metadata written during GN generation: its contents are the target's GN source directory. The marker helps `run_host.py` discover an expected suite, but it is neither required nor sufficient evidence that a runnable was selected, compiled, or is current. Before a build, report the static `host-configured` result; if an old executable exists, report its `host-runnable` snapshot and `artifact-current` status separately.

When a condition fails, name that condition and propose the narrow remediation: connect the target to the host dependency graph, add the `is_host_product` branch, set `type = "host_components"`, stabilize `module_name`, enable host sources, or use an existing host mock.

## 3. Design Defense-First Tests

Before editing, make a short defense map of the verified implementation:

- Guards and early returns that prevent null, bounds, or invalid-input faults.
- State and lifecycle transitions whose ordering can regress.
- Missing-resource, fallback, async, and callback failure paths.
- The concrete crash or defect path being protected.

Choose assertions that distinguish correct behavior from mere execution. If an important path is device-only or unreachable in host tests, state the limitation and required remediation instead of implying it was verified.

## 4. Edit Without Masking the Defect

- When a boundary or crash test exposes a production bug, fix the production path rather than weakening the test.
- When a mock expectation fails, first decide whether the production contract actually requires that call. Changing the mock to match accidental behavior can freeze the bug into the test.
- Keep the edit within the owning suite and its production path unless the verified dependency graph requires a routing change.

## 5. Build the Host Test Target

Build before executing a test when any of these conditions holds:

- The runnable or matching `exe.unstripped` artifact is missing.
- Relevant production source, test source, `BUILD.gn`, or `.gni` input changed after the artifact was produced.
- The generated Host build graph is stale or requires regeneration.
- No successful build record ties the artifact to the current working tree and Host configuration.
- Stripped and unstripped artifacts do not have matching provenance.

Skip the build only when `host-runnable` and `artifact-current` are both established with concrete evidence. If the user forbids building and currentness is stale or unproven, stop before execution and report the required build; do not reproduce against the old artifact.

Delegate the build lifecycle to `$ohos-dev-arkui-ace-engine-build` and apply its current decision tree, environment requirements, coverage policy, failure routing, and scripts. The mandatory lifecycle is:

1. Resolve `<ace-build-skill-dir>` as the directory containing the installed `ohos-dev-arkui-ace-engine-build/SKILL.md`.
2. Execute in a real writable OpenHarmony host environment. If the current sandbox cannot write `<oh-root>/out`, request the required permission before launching; do not fall back to direct `build.sh` execution.
3. Probe for an attributed build before launching:

   ```bash
   bash <ace-build-skill-dir>/scripts/monitor_progress.sh \
     --root <oh-root> --product host_product \
     --target ace_engine_test --check
   ```

4. If the probe reports a matching `active` build, record its launch ID and monitor that exact build or ask the user whether to wait. If it reports a target or attribution mismatch, stop and report the existing product/target conflict. A no-active result does not guarantee launch permission; the wrapper must still win the atomic product lock.
5. When no build is active, ask the build skill to compose the current arguments for product `host_product` and target `ace_engine_test`. Preserve the Host requirement `--no-prebuilt-sdk`; let the build skill decide coverage, ccache, and fast-rebuild policy. Launch only through its wrapper:

   ```bash
   bash <ace-build-skill-dir>/scripts/build_wrapper.sh \
     --product host_product -- \
     <arguments-composed-by-ohos-dev-arkui-ace-engine-build>
   ```

   Do not copy a stale argument list from this Host TDD skill or invoke the wrapper without first applying the build skill's current decision tree. If the wrapper returns a product-lock or active-metadata conflict, do not retry; it has atomically lost to another launch.
6. Record the wrapper-reported build PID, product, target, launch ID, `build_state.json`, exact command, revision, and `build_console.log`, then monitor the same build to a terminal result:

   ```bash
   bash <ace-build-skill-dir>/scripts/monitor_progress.sh \
     --root <oh-root> --product host_product \
     --target ace_engine_test --launch-id <wrapper-reported-launch-id>
   ```

7. Proceed to discovery or execution only after the monitor validates product, target, launch ID, build/log PID identity, metadata exit code, and terminal success. A wrapper launch or generic `host_product` success marker is not proof that `ace_engine_test` completed. On failure, follow the build skill's error-analysis route; do not rerun an unchanged command.

For a user-requested non-host product, let the build skill compose and monitor that product's command, report it only as build verification, and stop before host discovery and execution. A successful build proves compilation only, not that the intended suite was selected or passed.

## 6. Inspect the Host Discovery Snapshot

List discovered host-output entries from `<ace-root>`:

```bash
# cwd: <ace-root>
python3 test/unittest/scripts/run_host.py --list --filter <binary-or-keyword>
```

Use a binary name, suite-directory name, or another substring of `<category>/<binary>` for `--filter`. It matches only discovered category and binary names, case-insensitively; it does not search source-file names or gtest fixture/case names. Reserve `--gtest_filter` for selecting runtime gtest cases after the binary is known.

Treat `--list` as a filesystem discovery snapshot only. `run_host.py` scans the host output directory, reports `OK` when it finds a same-name executable file, and reports `MISSING` when it finds only a discovery marker. It does not inspect the GN dependency graph, invoke a build, establish artifact freshness or provenance, verify binary architecture, inspect the symbolized counterpart, or execute a test.

Interpret the result as follows:

| Result | Meaning | Next action |
|---|---|---|
| `OK` | Discovery found an executable file with that name in the scanned host output directory | Treat this only as artifact-presence evidence; verify GN configuration and build evidence independently, then inspect the concrete binary before running it |
| `MISSING` | Discovery found a `_path.txt` marker but no same-name executable in the scanned directory | Inspect the concrete output paths, owning `BUILD.gn`, host dependency path, and relevant build evidence; do not infer a compile failure from discovery alone |
| No matching suite | No discovered category or binary name matched the filter | Retry with the binary or suite-directory name, then inspect `module_name`, host routing, and `<binary>_path.txt`; do not infer that source files or gtest cases are absent |

If `run_host.py` itself fails, diagnose its error and inspect `_path.txt` plus the concrete output paths manually. Do not reinterpret a script failure as `MISSING`.

For `host_product`, verify these paths relative to `<oh-root>`:

- Runnable: `out/host/host_product/tests/unittest/ace_engine/<SuiteDirectory>/<binary>`
- Symbolized: `out/host/host_product/exe.unstripped/tests/unittest/ace_engine/<SuiteDirectory>/<binary>`

Before execution, verify `artifact-current` using the owning target, relevant source/test/GN inputs, working-tree changes, and successful build evidence. Treat a newer relevant input or a build graph that requires regeneration as decisive stale evidence. Do not use binary existence, executable permission, `run_host.py OK`, historical XML, or matching stripped/unstripped Build IDs by themselves as freshness proof.

Use the current symbolized binary for crash reproduction. If only the stripped binary exists, it may establish historical pass/fail behavior, but it is insufficient for a source-level crash diagnosis; rebuild or locate a current symbolized output before claiming a crash location.

If the matching symbolized binary is unavailable and commands must not be run, still give the exact future focused reproduction form, including the literal `--gtest_filter=<Suite>.<Case>`. Do not replace the flag with prose such as “run only this case.”

## 7. Run the Narrowest Useful Filter

Enter this step only after both `host-runnable` and `artifact-current` are verified. If the artifact is stale or provenance is unproven, return to the build step; if building is forbidden, stop without running the stale binary.

Run the focused case from `<oh-root>` and preserve normal console output, process exit status, and a gtest XML artifact:

```bash
# cwd: <oh-root>
out/host/host_product/exe.unstripped/tests/unittest/ace_engine/<SuiteDirectory>/<binary> \
  --gtest_filter=<Suite>.<Case> \
  --gtest_output=xml:out/host/host_product/exe.unstripped/tests/unittest/ace_engine/<SuiteDirectory>/<binary>_<case>.xml
```

For a changed test or production path, run the surrounding suite only after the focused case passes. For a reproduction-only request, stop after the requested filter unless the user asks for a broader run.

```bash
# cwd: <oh-root>
out/host/host_product/exe.unstripped/tests/unittest/ace_engine/<SuiteDirectory>/<binary> \
  --gtest_filter=<Suite>.* \
  --gtest_output=xml:out/host/host_product/exe.unstripped/tests/unittest/ace_engine/<SuiteDirectory>/<binary>_<suite>.xml
```

Prefer placing XML beside the binary. If that directory is not writable, use another explicit, persistent workspace path and report it; never claim an XML result that was not created. A hard crash may prevent XML generation, so use the exit signal, console output, and symbolized frames as evidence and state that XML was not produced.

## 8. Report Verified Evidence

Report these items separately:

- Static `host-configured` status and, when built, `host-runnable` status, with the evidence or missing condition for each.
- `artifact-current` status and the concrete freshness/provenance evidence, or the reason it is stale or unproven.
- `_path.txt` discovery-marker status and recorded source directory separately from executable availability.
- Discovery status, build result, and test execution result as three independent stages; never promote a `--list` status into a GN, build, or test conclusion.
- Product, exact build command, and build result.
- Build lifecycle evidence: observational preflight result, atomic wrapper result, PID/product/target/launch ID/state/log/command/revision metadata, whether an existing build was monitored, and attributed monitor terminal status.
- Defense points protected by the new or changed tests.
- Exact gtest filters, process result, and XML path or crash evidence.
- Focused-case result separately from the surrounding-suite result.
- Any device-only or environment limitation that prevented verification.

Before sending the final answer, apply these mandatory report checks:

- **Host audit:** explicitly list every dependency guard used in the conclusion, including `!is_asan` and `is_host_product` when present, plus `type`, `module_name`, and whether Host `sources` are non-empty.
- **Review-only fix:** when a textual diff cannot be built or run, state the remaining validation sequence exactly as Host build → exact focused case → surrounding suite. Add any repository-required full product build after those steps when production code changed. Never call the diff passing TDD before this sequence completes.
- **Crash reproduction:** print the exact focused flag, for example `--gtest_filter=CrashSuite.NullCallback`, even when the next action is blocked on a matching `exe.unstripped` artifact. Keep a process crash distinct from a normal gtest assertion failure and do not invent gtest counts without current XML.
- **Artifact freshness:** before any execution, state why the selected artifact is current. If relevant source, test, `BUILD.gn`, or `.gni` inputs changed after it, or provenance cannot be proven, require a Host build and do not run the existing binary.
- **Build delegation:** when a build was required, state that `$ohos-dev-arkui-ace-engine-build` governed the lifecycle and report its observational preflight, atomic wrapper launch, PID/product/target/launch ID/state/log/command/revision metadata, and attributed monitor terminal result. Do not describe a detached launch as a successful build.
- **Build plan:** even when commands must not be run, print the exact `monitor_progress.sh --check --target ace_engine_test` preflight form and state that it is not a reservation. State that matching `active` forbids a second build and that target mismatch blocks attribution. For a future launch, explicitly require a real writable Host environment, the wrapper's atomic lock, product `host_product`, target `ace_engine_test`, `--no-prebuilt-sdk`, the build skill's current argument policy, and `monitor_progress.sh --target ace_engine_test --launch-id <id>` through terminal completion.

## Critical Anti-Patterns

- **Never infer host compliance from a local `ace_unittest` block alone.** A target outside the `host_product` dependency graph will not be selected even if its branch looks correct.
- **Never treat `_path.txt` as a runnable path, host-selection proof, or compilation proof.** GN writes it as a source-directory discovery marker even for declared targets that are outside the selected dependency closure.
- **Never infer correct GN routing, a successful or fresh build, or a test result from `run_host.py --list`.** `OK` and `MISSING` describe only what its filesystem scan discovered.
- **Never report build success, `run_host.py --list` `OK`, or binary existence as a test pass.** Each proves a different stage and none proves execution success.
- **Never use an existing executable as sufficient reason to skip a build.** `host-runnable` is only availability; crash reproduction requires separately verified `artifact-current` provenance. A stale symbolized binary can produce a false pass, a false non-reproduction, or an unrelated stack.
- **Never call `./build.sh` directly or start a second build while the build skill reports an active build.** A separate `--check` is not atomic; use the wrapper's per-product lock, then monitor the exact launch ID so artifacts are attributed to the correct product, target, PID, command, revision, state, and log.
- **Never broaden the gtest filter after the focused case fails or crashes.** A larger run adds noise before the causal path is understood.
- **Never weaken an assertion or mock expectation solely to make the test green.** That can encode the defect as the new expected behavior.
- **Never call a device-dependent suite host-runnable without verified host mocks.** Compilation can succeed while runtime initialization still fails.
- **Never claim a source-level crash location from a stripped binary.** Without the `exe.unstripped` artifact, addresses may not map reliably to the failing code.
