# Crash, Deopt, Throw, and Fallback Debugging

Use this reference for AOT execution failures: crash in compiled code, deoptimization, exception slow path, fallback to interpreter, or bytecode/machine-code mismatch.

## Required Evidence Shape

Use whatever the user provides, but align evidence in this order:

1. Crash stack, signal, PC/LR, fault address, registers.
2. AOT machine code or disassembly around PC.
3. Bytecode disassembly for the same method.
4. Source or runtime semantic expectation.
5. AOT linkage/load evidence for the method.
6. Deopt/exception/fallback logs if present.

If the PC-to-method mapping is missing, say that compiled-code responsibility is unknown.

## Correlation Questions

- Is the PC in compiled AOT code, a runtime helper, interpreter, signal handler, or unrelated native code?
- What operation does the faulting instruction perform: object load, array length, bounds check, call, runtime call, type check, or deopt guard?
- Which bytecode operation or source expression corresponds to it?
- If a check failed, should this path throw, deopt, or continue to a runtime helper?
- Is the object/register state invalid, or is the generated instruction sequence inconsistent with bytecode semantics?

## Source Anchors

- `static_core/runtime/entrypoints/entrypoints.cpp`: `CheckCastEntrypoint()` throws `ClassCastException` and handles the pending exception when assignability fails.
- The neighboring `CheckCastDeoptimizeEntrypoint()` calls `DeoptimizeEntrypoint(...CHECK_CAST)` for the deopt variant of the same semantic check.
- `DeoptimizeEntrypoint()` logs the deopt reason and instruction id, emits a deoptimization event, then calls `Deoptimize(&stack, ...)`.
- `static_core/runtime/exceptions.cpp`: `FindCatchBlockInCFrames()` walks compiled frames, finds a catch block with `method->FindCatchBlock(...)`, and calls `Deoptimize(...)` to resume at the handler.

## Debugging Steps

1. Establish whether the crash/deopt happened after AOT code actually executed.
2. Map machine instruction to bytecode semantics.
3. Decide whether the observed behavior is a legal throw/deopt/fallback.
4. Identify whether the root cause is likely codegen, runtime state, metadata/linkage, or missing evidence.
5. Propose the smallest patch target only after that separation.
6. When the owner is narrowed enough, add one mode/feature comparison that can falsify the hypothesis without replacing bytecode/machine-code alignment.

## Artifact Boundaries

- Crash stack and registers identify the immediate fault context, not necessarily the first wrong instruction.
- AOT disassembly and `ark_aotdump` are useful only after an `.an` product exists and the target method body can be mapped; they do not explain PAOC compile-time crashes that never reached codegen.
- Bytecode disassembly is the semantic baseline. Use it to decide whether the machine instruction should load, check, call, throw, or deopt.
- Link/load logs prove whether a method could execute AOT code; they do not prove the observed runtime state is valid.
- Deopt/throw logs prove the fallback path taken; they do not by themselves prove the pass that inserted the guard is wrong.

## Runtime AOT Crash Workflow

When the process is running an emitted `.an` product and crashes in or near compiled code:

1. Decide whether the stack-top instruction is likely the first wrong point. If the top instruction directly faults on a load/store/call whose input register is invalid and the bytecode semantics match that operation, ask for the bytecode and machine code for that method first.
2. If the top frame may be a later symptom, compare interpreter and AOT behavior:
   - interpreter/non-AOT normal and AOT abnormal means the root is still likely in AOT-produced behavior, but not necessarily at the stack-top instruction;
   - both modes abnormal means investigate source/runtime state before blaming AOT;
   - AOT normal and interpreter abnormal points away from AOT codegen.
3. If the instruction maps to a feature-specific lowering, helper, check, or pass, suggest one narrow on/off comparison for that feature when an option exists. State that the comparison confirms involvement, not the final faulty line.
4. If AOT-only behavior remains but the root is not clear, guide the developer to add logs at the nearest boundary: AOT linkage, method entry, runtime helper entry, deopt/throw slow path, or the compiler pass that inserted the suspect instruction.
5. Use broad bisection only after local evidence cannot separate root from symptom. Prefer function-level or feature-level grouping over arbitrary method splitting when the developer knows the workload.

For runtime crash logging, ask for fields that connect the fault to the semantic operation: method full name, compiled entry point, PC offset, bytecode PC, faulting instruction, base/index/value registers, object/class pointer, helper name if a runtime call is entered, and whether the method was linked from AOT or fell back.

## Deopt Workflow

For an AOT deopt symptom, first identify the deopt instruction and triggering condition, not just the method:

1. Capture the deopt log or frame showing method and bytecode PC. Runtime logs such as `Deoptimize frame: <method>, pc=<bc offset>` are useful anchors when present.
2. Map the bytecode PC to IR and find the exact `Deoptimize`, `DeoptimizeIf`, `DeoptimizeCompare`, or `DeoptimizeCompareImm` instruction and its `DeoptimizeType`.
3. Identify which pass inserted or transformed that deopt instruction. The inserting pass may not be wrong; its input value may already be wrong due to an earlier pass, bad profile data, or invalid runtime metadata.
4. Inspect the deopt condition inputs. If the deopt condition is correct, the behavior may be valid. If the input is wrong, walk def-use backward and ask the developer to log the producer value or guard condition before the deopt site.
5. If a specific pass/profile/deopt mode is implicated, compare with the narrowest relevant option disabled or profile input removed. Use this only to decide whether that path is involved; still verify condition inputs.
6. Recommend targeted logging before source changes: print method, bytecode PC, deopt type, condition input value, compared constants/types, and relevant profile/class-context data.

If the deopt is valid for the observed input, do not turn it into a compiler fix. If the input is invalid, the next owner is usually the producer of that input, profile/class-context consumer, or runtime metadata path rather than the deopt instruction itself.

## Fix Direction

- Codegen/lowering bug: fix the lowering or runtime-call selection for the specific IR/bytecode shape; add an AOT-focused regression.
- Runtime state bug: fix initialization, field population, class context, or object lifetime; do not hide it with codegen guards.
- Deopt mismatch: inspect whether the IR node is deopt-capable and whether runtime resumes through the expected interpreter path.
- Throw/fallback mismatch: inspect NullCheck/BoundsCheck lowering and exception slow path before changing deopt behavior.

## Cannot Conclude

- A crash while AOT is enabled is not proof that compiled code crashed.
- A compiled-code crash is not automatically a codegen bug; runtime state can be invalid.
- A failed check in static AOT does not always deopt. Some checks throw through the normal exception path.
- A deopt inserted by a pass is not automatically that pass's bug; the pass may have encoded a valid guard for an invalid input produced earlier.
