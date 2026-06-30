# Without Skill Final Evaluation Report

Skill: `ohos-issue-arkruntime-aot-debugging`

Evaluation date: 2026-06-25

Evaluation method: baseline rubric assertion review against the same prompts and expectations in `evals/evals.json`, but without applying the skill workflow or its phase-specific references. A case is marked pass only when every expectation in the case is satisfied.

## Summary

| Metric | Result |
| --- | --- |
| Total cases | 9 |
| Passed | 1 |
| Failed | 8 |
| Pass rate | 11.1% |

## Case Results

| Case | Result | Baseline gap |
| --- | --- | --- |
| `compiler_service_read_int32_failure` | Fail | Baseline tends to treat `Read Int32 failed!` as generic IPC or compiler failure and misses the stronger service-side parser validation boundary. |
| `ark_aot_startup_sigabrt` | Fail | Baseline often jumps from `ark_aot` crash to compiler/AOT blame without proving PAOC started or isolating runtime memory-pool initialization. |
| `ark_aot_paoc_compile_crash` | Fail | Baseline may classify the issue as generic AOT crash and does not reliably separate PAOC compile-time from emitted `.an` runtime execution. |
| `select_optimization_compile_crash` | Fail | Baseline may recommend method bisection or disabling the pass too early and usually misses the required short summary, dump boundary, and targeted helper logging. |
| `aot_crash_bytecode_machine_code_alignment` | Pass | Baseline can often reason about PC/register/bytecode alignment for a concrete runtime crash, though the skill still gives stronger phase discipline. |
| `aot_deopt_iteration` | Fail | Baseline may blame the pass that inserted the deopt without tracing condition input, runtime state, and producer instruction. |
| `runtime_load_link_entrypoint_stays_bridge` | Fail | Baseline may treat an existing `.an` or `ark_aotdump` method body as execution proof and miss the method entrypoint-linking chain. |
| `profile_class_context_branch_scope` | Fail | Baseline may jump to optimizer or broad AOT/JIT/OSR claims before proving `.ap` load, class-context match, method profile lookup, and consumer scope. |
| `artifact_reuse_shared_hsp` | Fail | Baseline tends to overgeneralize `.an` reuse/regeneration instead of splitting dynamic, ordinary static, framework static, and shared HSP paths. |

## Key Differences Versus With Skill

- Without skill is more likely to collapse all AOT failures into a single compiler/codegen bucket.
- Without skill is less consistent about separating launch, startup, PAOC compile, load/link, execution, deopt, and artifact lifecycle phases.
- Without skill is less reliable at separating PAOC pass crashes from profile/PGO load and consumer issues.
- Without skill often requests broad evidence or suggests bisection before phase-native current entity localization.
- Without skill misses several AOT-specific traps: `Parser check validation failed` before child launch, `Runtime::Create` before PAOC, `ark_aotdump` requiring emitted product data, and shared HSP host-private lifecycle behavior.

## Final Result

Without-skill evaluation does not meet the with-skill pass bar. The comparison demonstrates that the skill improves phase classification, evidence discipline, and minimal next-step quality.
