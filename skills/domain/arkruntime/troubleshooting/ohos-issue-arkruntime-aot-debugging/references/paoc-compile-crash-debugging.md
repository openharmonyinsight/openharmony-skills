# PAOC Compile Crash Debugging

Use this reference for child `ark_aot` crashes during PAOC compilation: current method localization, pass/helper evidence, dump boundaries, method filtering, pass toggles, and parallel AOT compile pressure.

Do not use this file for `.ap` profile loading, class-context mismatch, branch-profile consumers, or inline-cache policy; use `profile-and-pgo-debugging.md` for those.

## Classify the Symptom

- `ark_aot` has launched, runtime initialization completed, and PAOC/method/pass/codegen logs or frames are present.
- The stack names compiler code such as graph creation, optimization passes, lowering, register allocation, encoder, AOT builder, or assertion helpers.
- The failure happens before app runtime execution of emitted AOT code.
- `There are no compiled methods` or method filtering issues are still compile-phase symptoms unless a completed `.an` product is being loaded.
- Parallel AOT symptoms belong here only when the evidence is compile-time memory pressure, result lifetime, or merge/emission staging.

## Compile-Time Crash Boundary

| Case | Evidence | Next step |
|---|---|---|
| Startup crash | stack/log ends around `Runtime::Create`, memory pool setup, or boot panda file loading; no PAOC method/pass logs | Use `ark-aot-startup-debugging.md`. |
| PAOC compile-time crash | child `ark_aot` started, runtime init completed, PAOC/method/pass/codegen logs or frames are present | Stay in this reference. |
| Runtime AOT execution crash | app/runtime stack or PC points at linked compiled AOT code executing after `.an` load | Use `crash-deopt-throw-debugging.md`. |

Do not label a PAOC compile-time crash as "compiled-code execution crash"; the output may never have been emitted or loaded.

## Debugging Steps

1. Confirm child `ark_aot` actually launched and runtime startup completed.
2. Identify the current panda file, class, method, pass, and backend phase from logs, stack, or filter options.
3. For a stack whose top frames name a compiler pass/helper, inspect that pass source before the final hypothesis. Report the pass enable flag/default when cheap, pipeline neighbors, the owning loop, mutation pattern, and the exact helper's transform.
4. For optimization-pass crashes, separate the immediate crash candidate from latent correctness risks. Do not promote either without pc-to-line evidence, IR, or a reproduced method.
5. For many-function panda/abc inputs, identify the method being compiled at the crash point before proposing a source fix. Filtering and bisection are fallback tools, not the default first move.
6. If crashing in a pass or lowering, inspect the IR shape and pass preconditions before patching codegen.
7. If crashing in encoder/codegen, separate illegal IR, missing lowering, relocation/slot metadata, and backend instruction selection hypotheses.
8. For parallel AOT, inspect live result retention and merge/emission staging, not only worker count.

## Compact PAOC Crash Answer Shape

For a user-provided compile-time `ark_aot` crash stack, prefer a short first answer:

1. `Short summary`: stage, source-backed suspect, next decisive evidence. If pc-to-line, current method, IR, or reproducer is missing, say "suspect" or "hypothesis", not "root cause".
2. `Classification`: distinguish child `ark_aot` PAOC compilation from compiler_service launch, startup, and emitted `.an` execution.
3. `Find the current method`: start from the last child `ark_aot` method log; mention filters only as fallback or reproducibility checks.
4. `Dump/disasm/aotdump boundary`: state what each artifact can and cannot prove at this phase.
5. `Source suspects/logging`: name the concrete pass/helper, the shortest source-backed suspects, and the exact targeted logging point.
6. `Next step`: request only the artifact that best separates the current hypotheses.

Do not front-load `--compiler-regex`, `--paoc-methods-from-file`, or bisection options before explaining why current logs/dumps cannot identify the method.

## Input-Side Method Identification

When a PAOC crash happens on a panda/abc file with many functions, identify the method being compiled at the crash point before proposing a source fix.

1. Start from the last PAOC method line:

   ```text
   [N] Compile method (id=...): <method-full-name>
   ```

   Treat it as the current candidate, not final proof if logs are buffered, incomplete, or options change execution order.

2. If the method log is missing, ask for child `ark_aot` output rather than only the outer service wrapper. If temporary logging is cheaper, add it at:
   - `Paoc::Compile(Method *method, size_t methodIndex)` before and after `CompileAot`;
   - `CompileInGraph` or the method-compile entry when available;
   - `Paoc::CompileAot` around graph creation, `TryCreateGraph`, `RunOptimizations`, and finalization;
   - `PassManager::RunPass` before each pass when the failing pass is unknown.

3. Only if logs and dumps cannot identify the method, use one-method selection or bisection:
   - `--paoc-methods-from-file:path=<methods.txt>,iswhite=true`;
   - `--compiler-regex='<qualified-name-regex>'`;
   - `--compiler-regex-with-signature='<signature-regex>'`;
   - `--paoc-skip-until=<method>` / `--paoc-compile-until=<method>`;
   - `--paoc-methods-from-file:path=<methods.txt>,iswhite=false`.

Do not treat a single-method success before the fix as validation. It usually means the selected method is not the crashing method or the filter changed relevant options.

## Dump and Product Boundaries

- `--compiler-dump --compiler-dump:folder=./ir_dump` writes pass dumps after a pass returns successfully. If the crash occurs inside a pass, the dump for that pass may be absent; inspect the IR entering the crashing pass or the last successful dump for the same method.
- `--compiler-disasm-dump:file-name=./disasm.txt` is codegen/disassembly evidence. If the crash occurs before codegen, the crashing method usually will not have disassembly output.
- `ark_aotdump` is product evidence. For an optimization-stage crash, the crashing method usually has no finalized AOT method body/header to dump.

## Pass or Feature Isolation

After the current method and failing pass are identified, use pass or feature switches as secondary confirmation. For `SelectOptimization`, compare the same input/method with and without `--compiler-select-optimization=false`.

- If the default compile crashes and the disabled-pass run does not, the owner is likely that pass or an input invariant exposed there. Still inspect entering IR and helper state before patching.
- If both crash, inspect previous passes and the last successful dump.
- If disabling a pass only changes behavior in the full input, re-check method identification and option parity.

Use the narrowest equivalent toggle for other compile issues. Toggles answer "is this path involved?", not the final faulty line.

## Pass-Local Crash Checklist

- Locate the crashing helper and owning `RunImpl` or pass loop.
- Check mutation while iterating: erased, moved, replaced, or reinserted instructions.
- Check equivalence keys: opcode class, result type, operand types, condition code, constants, immediates, and input identity.
- Check replacement direction and dominance. The replacement instruction must dominate all replaced users and preserve type expectations.
- Check release behavior when preconditions are guarded only by debug `ASSERT`s.
- Prefer a minimal IR regression and run the pass under GraphChecker or the existing compiler unit target.

For `SelectOptimization::TryOptimizeSelectInstWithSameOperandsChecked`, inspect `EraseInst(selectInst)`, `foundInst->InsertAfter(selectInst)`, and `foundInst->ReplaceUsers(selectInst)`, including dominance and user type assumptions.

## Useful Evidence

- Full child `ark_aot` stack and earliest child fatal line.
- Last PAOC/method/pass log before the crash.
- Exact input panda file, output path, and method filter options.
- IR dump for the crashing method and last successful pass.
- Whether disassembly exists for the current method.
- Whether a one-method filtered compile reproduces with option parity.
- Current method bytecode or IR shape when available.

## Fix Direction

- Compile-time pass crash: fix pass preconditions, IR transform, iterator safety, or missing guard; add a regression around the method shape.
- Lowering/codegen crash: fix the lowering/encoder contract only after proving IR validity for that stage.
- Filter bug: fix option parsing or the specific match function; include positive and negative method-name tests.
- Parallel memory pressure: prefer staged compile-and-merge or bounded result lifetime over simply increasing thread count.

## Cannot Conclude

- Do not assume PAOC is whole-program SSA; verify the method-at-a-time compilation boundary.
- Do not infer app runtime AOT execution from a crash inside `ark_aot` compilation.
- Do not blame compiler_service when its only role was launching a child that later crashed inside PAOC.
- Do not call a source-backed risk the root cause until line info, IR dump, or a reduced reproducer confirms it.
- Do not assume the last disassembly, `ark_aotdump`, or IR dump entry is the crashing method without phase alignment.
