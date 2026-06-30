# With Skill Final Evaluation Report

Skill: `ohos-issue-arkruntime-aot-debugging`

Evaluation date: 2026-06-25

Evaluation method: rubric assertion review against `evals/evals.json`. A case is marked pass only when every expectation in the case is satisfied. This report represents the with-skill run, where the evaluator applies the skill workflow and phase-specific references.

## Summary

| Metric | Result |
| --- | --- |
| Total cases | 9 |
| Passed | 9 |
| Failed | 0 |
| Pass rate | 100% |

## Case Results

| Case | Result | Key with-skill behavior |
| --- | --- | --- |
| `compiler_service_read_int32_failure` | Pass | Separates outer wrapper errors from service-side parser validation and avoids misclassifying the failure as PAOC/codegen. |
| `ark_aot_startup_sigabrt` | Pass | Classifies the stack as child `ark_aot` startup/runtime initialization and requests earliest fatal/runtime resource evidence before compiler fixes. |
| `ark_aot_paoc_compile_crash` | Pass | Uses child PAOC method/pass evidence, explains why no emitted `.an` means no runtime execution, and requires source-backed pass/helper suspects. |
| `select_optimization_compile_crash` | Pass | Produces the required short summary, localizes to `SelectOptimization`, requests current-method evidence, and treats the pass-disable switch as secondary isolation. |
| `aot_crash_bytecode_machine_code_alignment` | Pass | Aligns PC, bytecode, machine instruction, registers, fault address, and runtime object state before naming codegen. |
| `aot_deopt_iteration` | Pass | Localizes deopt to method, bytecode PC, guard/check, deopt type, condition input, and producer before source changes. |
| `runtime_load_link_entrypoint_stays_bridge` | Pass | Separates existing/dumped `.an` data from method-level linkage and traces the entrypoint-installation chain before execution claims. |
| `profile_class_context_branch_scope` | Pass | Routes to profile/PGO, checks `.ap` load and class-context match first, and limits branch-counter claims to verified consumers. |
| `artifact_reuse_shared_hsp` | Pass | Treats this as path-specific artifact lifecycle analysis and avoids universal `.an` reuse or cleanup claims. |

## Key Differences Versus Without Skill

- With skill consistently classifies the failure stage before proposing a fix.
- With skill separates process contexts: compiler_service, child `ark_aot`, app runtime, and artifact lifecycle owners.
- With skill asks for the smallest decisive evidence instead of broad logs or bisection.
- With skill distinguishes profile load/compatibility failures from PAOC pass crashes and from runtime method linkage failures.
- With skill avoids common false conclusions, especially treating wrapper errors as codegen, startup crashes as PAOC, or existing `.an` files as universally reused.
- With skill gives source-owner and validation direction without prematurely changing compiler code.

## Final Result

With-skill evaluation passes all cases and satisfies the入库要求 that with skill evaluation must fully pass.
