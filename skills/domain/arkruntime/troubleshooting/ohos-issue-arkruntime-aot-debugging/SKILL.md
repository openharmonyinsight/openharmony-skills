---
name: ohos-issue-arkruntime-aot-debugging
description: Use when diagnosing, localizing, or fixing OpenHarmony ArkRuntime AOT issues, including compiler_service launch or argument failures, dynamic/static AOT mode selection, .an artifact generation or reuse, ark_aot startup/runtime initialization failures, ark_aot crashes during PAOC compilation, PAOC compilation or profile problems, AOT loading/link failures, and AOT execution issues such as crash, deopt, throw/fallback, bytecode-machine-code mismatch, or compiled-code evidence correlation.
metadata:
  author: openharmony
  scope: domain
  stage: troubleshooting
  domain: arkruntime
  capability: aot-debugging
  version: 0.1.0
  status: draft
  tags:
    - arkruntime
    - aot
    - debugging
    - troubleshooting
---

# ArkRuntime AOT Debugging

Use this skill to debug AOT-related failures as a closed loop: classify the symptom, align the available evidence, form competing root-cause hypotheses, choose the smallest source area to inspect or patch, and propose validation.

This skill complements repository `AGENTS.md` files and memory. `AGENTS.md` tells you where code lives; memory stores past conclusions. This skill forces the AOT-specific debugging shape so the agent does not jump from an outer "AOT failed" message directly to compiler/codegen blame.

## First Response Contract

Start every non-trivial answer with a three-line summary before detailed analysis:

```text
Short summary:
- Stage:
- Best current hypothesis:
- Next decisive evidence:
```

When evidence lacks pc-to-line mapping, the current method, IR, or a reproducer, phrase `Best current hypothesis` as a source-backed suspect or hypothesis, not a concluded root cause. Prefer "strongest current suspect" or "needs validation" over wording that says a release build "triggered" a specific internal failure.

Then produce these fields before proposing a fix:

```text
Problem type:
Failure stage:
Current evidence:
Confirmed facts:
Competing hypotheses:
Most likely root cause:
Minimal fix direction:
Validation:
Cannot conclude yet:
```

Keep the first response compact unless the user asks for full detail. Use at most these sections: `Short summary`, `Classification`, `Find the current method`, `Dump/disasm/aotdump boundary`, `Source suspects/logging`, and `Next step`. Omit process narration such as which docs were read.

For a stack with a named compiler pass/function, include at least one source-grounded suspect from that pass body before proposing the fix. Do not stop at phase classification when the stack names the exact helper.

If user evidence is sparse, do not ask for everything. Ask for the one or two artifacts that best split the current hypotheses.

Treat AOT debugging as iterative. Give the developer the next logging or evidence-collection point that can falsify the current hypothesis; do not jump directly to broad bisection or source patches when a targeted log, dump, or mode comparison can decide the next step.

Answer in the user's language when practical.

## Localization Rule

Before suggesting bisection or a source patch, localize the failure to the smallest current entity that the phase naturally exposes:

- Launch/service failures: current request, parser, executable path, and child argv.
- `ark_aot` startup failures: earliest fatal line and runtime initialization step.
- PAOC compile-time failures: current panda file, class, method, pass, and helper.
- Runtime load/link failures: current `.an` file, class/method identity, and link skip reason.
- Runtime compiled-code crashes: current PC-to-method mapping, bytecode operation, machine instruction, and runtime state.
- Deopt/throw/fallback failures: current method, bytecode PC, guard/check instruction, deopt type or exception path, and the producer of the condition input.

Use bisection only after phase-native evidence cannot identify that current entity or after a single-entity repro still needs input reduction.

## Hypothesis Isolation Switches

When a failure is already localized to a pass, backend feature, profile consumer, AOT linkage path, deopt mode, or runtime option, suggest a minimal on/off comparison as supporting evidence. Examples include disabling a named compiler pass such as `--compiler-select-optimization=false`, removing profile input, disabling a specialized optimization, forcing interpreter/non-AOT mode, or toggling a runtime AOT option.

Use these switches to answer "is this owner/path involved?", not as the first localization step and not as proof of the final root cause. Place them after the phase-native current entity, artifact boundary, and targeted logging/dump request. Always say what each side of the comparison would prove and what it would not prove.

## Classification

Classify the issue into one primary type. Mention secondary types only if they affect the next step.

| Type | Use when | Read | Do NOT load first |
|---|---|---|---|
| Launch and arguments | `Read Int32 failed!`, `Parser check validation failed`, `ERR_AOT_COMPILER_*`, wrong dynamic/static/hybrid path, compiler_service/BMS/installd questions | `references/launch-and-args-debugging.md` | PAOC/profile/runtime execution refs unless child `ark_aot` evidence appears |
| Artifact lifecycle | `.an` not generated, unexpectedly reused or overwritten, update cleanup, idle AOT, framework/static/shared HSP artifact path | `references/artifact-lifecycle-debugging.md` | PAOC pass/profile/execution refs unless lifecycle evidence reaches those phases |
| ark_aot startup | `ark_aot` crash before PAOC logs, `Runtime::Create`, `PoolManager`, `MmapMemPool`, boot panda file loading | `references/ark-aot-startup-debugging.md` | PAOC/profile/execution refs before runtime initialization is proven complete |
| PAOC compile crash | `ark_aot` crashes after PAOC starts, pass/codegen/assert failures, method filtering, "There are no compiled methods", parallel AOT compile-time memory pressure | `references/paoc-compile-crash-debugging.md` | Profile/PGO ref unless `.ap`, branch, or inline-cache evidence is central |
| Profile and PGO | `.ap`/PGO/profile load or save questions, class-context mismatch, branch counters, inline cache, profile on/off isolation | `references/profile-and-pgo-debugging.md` | PAOC compile-crash ref unless the stack is inside a profile consumer pass |
| Runtime load/link | `.an` exists but code may not execute, AotManager loading, `MaybeLinkMethodToAotCode`, `RegisterAotStringRoot`, `HasAotFiles` | `references/runtime-link-debugging.md` | PAOC/profile refs unless generated product or profile provenance is disputed |
| Execution semantics | crash in compiled code, deopt, throw/fallback, bytecode and machine-code correlation, check failure semantics | `references/crash-deopt-throw-debugging.md` | PAOC compile refs unless evidence points back to the producer pass |
| Build/config gating | AOT targets unexpectedly built or absent, emulator/codegen switches, deployment of `ark_aot` and compiler libraries | `references/build-config-debugging.md` | Runtime/link/execution refs until build output and deployed binaries are verified |

## Evidence Discipline

- Separate process contexts: BundleManager/installd, compiler_service, child `ark_aot` or `ark_aot_compiler`, app runtime, and signal/crash handlers.
- Separate phases: argument construction, service validation, child launch, runtime initialization, panda file loading, method compilation, output emission, runtime loading/linking, compiled-code execution.
- Treat outer errors as wrappers until the earlier, phase-specific evidence is found.
- Match artifacts to phase. IR dumps, disassembly, `ark_aotdump`, bytecode, crash stacks, and logs each prove different things; state the boundary before using an artifact as evidence.
- When asking the developer to add logs, name the function/boundary and the fields to print. Prefer one targeted log point over broad logging or arbitrary method splitting.
- For crash/deopt questions, align machine code, bytecode, registers/fault address, source semantics, and runtime state before naming codegen as the root cause.
- For lifecycle questions, answer by path. Dynamic AOT, ordinary static app idle AOT, framework static AOT, and shared HSP AOT do not share one universal reuse/cleanup rule.

## Common Traps

- Do not interpret `Read Int32 failed!` alone as IPC corruption or `MessageParcel::ReadInt32()` failure.
- Do not treat `Parser check validation failed` as proof the child compiler started.
- Do not infer static AOT from an app-level static setting if module metadata or `moduleArkTSMode` points to dynamic.
- Do not collapse "`ark_aot` created a Runtime/PandaVM" into "PAOC codegen has started".
- Do not merge `ark_aot` startup crashes, PAOC compile-time crashes, and runtime compiled-code crashes into one "AOT crash" bucket.
- Do not stop at "inside PAOC/pass X" when the stack names a concrete helper. Read that helper and distinguish source-backed suspects from generic null-pointer guesses.
- Do not recommend method bisection as the first response for `ark_aot` compile-time crashes. First use the current method log and compile artifacts to identify the method that was being compiled when the crash happened.
- Do not say an existing `.an` is always reused or always regenerated without identifying the AOT path.
- Do not call a compiled-code crash a codegen bug until bytecode/machine-code semantics and runtime state have been aligned.
- Do not treat a diagnostic artifact as proof outside its phase. For example, `ark_aotdump` needs generated AOT product data, while compiler IR dumps are pass-local and may be absent for the crashing pass.
- Do not recommend source changes before stating the minimal source owner and how to validate the hypothesis.

## Source Search Starting Points

Use these as starting points only; verify exact paths and line numbers in the active checkout.

- `static_core/compiler/tools/paoc/`
- `static_core/compiler/`
- `static_core/runtime/`
- `static_core/plugins/ets/runtime/`
- sibling `ets_runtime/compiler_service` for service-side AOT orchestration
- sibling `foundation/bundlemanager/bundle_framework` for BundleManager AOT task construction
- sibling `foundation/bundlemanager/bundle_tool` for `bm` / `bundle_test_tool` command parsing, install/uninstall/query flows, and user-facing AOT trigger paths
- sibling `foundation/ability/ability_runtime` for Ability lifecycle, process launch, app/runtime startup context, and AOT behavior that depends on ability/application state
- sibling `foundation/resourceschedule/work_scheduler` and `base/powermgr/thermal_manager` for idle/thermal scheduling questions

## Fix Strategy

Prefer the smallest behavior-only fix that matches the classified owner:

- Argument/mode failure: fix metadata propagation, parser choice, path construction, or validation message at the caller/service boundary.
- Artifact lifecycle failure: fix existence/version/path checks in the owner path, not a generic `.an` cleanup rule.
- Startup failure: fix runtime init configuration/resource handling only after proving the failure is before PAOC compilation.
- PAOC compile/profile failure: fix the pass, lowering, codegen, method selection, profile parsing/consumer fallback, result lifetime, or compile pipeline state only after identifying the current method/pass and proving the crash is inside child compilation.
- Load/link failure: fix AOT file discovery, recorded path/header metadata, skip reason, or linkage condition.
- Execution failure: fix codegen/lowering only after excluding legal throw/deopt behavior and bad runtime state.

When patching, preserve public API, persistent formats, opcode layout, object layout, and lifecycle semantics unless the user explicitly asks to change them.
