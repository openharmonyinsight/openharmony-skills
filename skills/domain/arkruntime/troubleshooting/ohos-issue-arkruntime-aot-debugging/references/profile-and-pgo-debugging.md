# Profile and PGO Debugging

Use this reference for `.ap` profile loading, AOT PGO attachment, class-context mismatch, branch-profile data, inline-cache state, and profile on/off isolation.

Do not use this file for PAOC pass crashes unless the crash is inside a profile reader or profile consumer. Use `paoc-compile-crash-debugging.md` for compile-time pass/helper crashes.

## Classify the Symptom

- `.ap` exists but PAOC says it cannot load or cannot use the profile.
- A profile loads but a method behaves as if no profile data exists.
- Class context, panda-file checksum, class index, or method profile mismatch appears in logs.
- Branch counters influence or fail to influence AOT/JIT/OSR compile decisions.
- Inline cache is monomorphic, polymorphic, unknown, or megamorphic and affects inlining.
- Removing `--paoc-use-profile` or profile collection changes behavior.

## .ap Load Boundary

Source anchors:

- `static_core/compiler/tools/paoc/paoc.cpp`: `Paoc::TryLoadAotProfile()` loads the profile named by `--paoc-use-profile:path=<profile.ap>[,force]`.
- `static_core/runtime/jit/profiling_loader.cpp`: `ProfilingLoader::LoadProfile()` delegates to `pgo::AotPgoFile::Load(...)`.
- `static_core/runtime/jit/libprofile/pgo_file_builder.*`: owns the serialized `.ap` profile representation.
- `static_core/runtime/jit/profiling_saver.*` and `profile_saver_worker.*`: save runtime profile data; profile saving is separate from PAOC consumption.

Debugging order:

1. Confirm the PAOC command actually passes `--paoc-use-profile:path=...`.
2. Confirm the profile file is readable and was produced for the intended panda files.
3. Confirm the loaded profile passes class-context checks before assuming consumer bugs.

## Class Context and Mismatch

Source anchors:

- `Paoc::BuildClassContext()` builds the compile-time context from loaded panda files and checksums.
- `CheckFilesInClassContext()` in `paoc.cpp` compares the profile context against the current PAOC context and warns on hash mismatch.
- `Paoc::TryLoadAotMethodProfile()` reports class-index mismatch for a method profile.
- `runtime/jit/libprofile/pgo_class_context_utils.*` parses and merges contexts and reports checksum mismatch during save/merge flows.
- `compiler/aot/aot_manager.cpp` also checks loaded AOT file class context at runtime; keep runtime AOT-file mismatch separate from `.ap` PAOC profile mismatch.

Treat class-context mismatch as a compatibility failure first. Do not use `force`, loosen checks, or silently ignore mismatch unless the task explicitly changes profile compatibility semantics.

## Branch Data Collection and Consumers

Source anchors:

- `static_core/runtime/options.yaml`: `profile-branches` controls runtime branch-profile collection.
- `runtime/jit/profiling_loader.h`: loaded branch data becomes `ProfilingData` branch records.
- `compiler/optimizer/ir/graph.cpp`: `Graph::GetBranchCounter()` is the shared compile-time access point.
- Known shared consumers include `HotnessPropagation`, `LinearOrder`, and `IfConversion`; `if_conversion.cpp` reads true/false counters through `GetBranchCounter()`.

Debugging order:

1. Confirm branch data was collected and saved. A valid `.ap` can contain methods without branch payload.
2. Confirm PAOC loaded the profile and attached method profile data to the graph.
3. Inspect the exact consumer path. Do not assume every AOT/JIT/OSR decision consumes every branch counter.
4. If a counter is missing, distinguish "no profile for this bytecode" from "consumer fallback bug".

## Inline Cache and Megamorphic Behavior

Source anchors:

- `runtime/jit/profiling_data.h`: runtime `CallSiteInlineCache` stores up to `CLASSES_COUNT = 4`; when full, it marks the first slot with `MEGAMORPHIC_FLAG`.
- `runtime/jit/libprofile/aot_profiling_data.h`: serialized AOT inline-cache records mirror `CLASSES_COUNT = 4` and `MEGAMORPHIC_FLAG`.
- `runtime/jit/profiling_saver.cpp`: writes megamorphic state into the AOT profile.
- `runtime/jit/libprofile/profile_merger.cpp`: merging more than four receiver classes escalates the callsite to megamorphic.
- `compiler/optimizer/optimizations/inlining.cpp`: `TryInlineWithInlineCaches()` treats `MEGAMORPHIC` as `FAIL_MEGAMORPHIC`.

Megamorphic means the current profile contract lost the bounded receiver set. Do not propose "inline the first four" as a current behavior; that would require a different top-k or frequency-carrying profile contract.

## Profile On/Off Isolation

Use profile toggles after proving the phase and method:

- Remove `--paoc-use-profile` to check whether the `.ap` reader or consumer path is involved.
- Re-run with the same method filter and options except profile input.
- Toggle runtime branch collection only when the question is whether branch payload exists in a newly saved profile.
- Compare profile dumps before and after only at the `.ap` boundary; compare IR/pass behavior at the PAOC consumer boundary.

- Profile off fixes a compile crash: profile reader or consumer is involved, not necessarily the final faulty line.
- Profile off changes code shape: profile data affected optimization, but link/execution still needs separate proof.

## Useful Evidence

- PAOC command line with `--paoc-use-profile`.
- Profile loader logs: load failure, cannot-use warning, class-context hash mismatch, method class-index mismatch.
- `ark_aptool`/profile dump showing class context, methods, branches, throws, and inline caches.
- Current panda files and checksums used to build class context.
- Whether branch payload exists for the target method and bytecode PC.
- Inline-cache callsite pc, receiver class list, and megamorphic marker.
- A same-method profile on/off comparison with option parity.

## Fix Direction

- Profile load failure: fix path, format/version compatibility, class context, or diagnostics.
- Class-context mismatch: preserve rejection semantics and improve evidence if needed.
- Missing branch fallback: fix reader fallback or consumer guard so absent data does not corrupt decisions.
- Branch consumer bug: fix the specific `Graph::GetBranchCounter()` consumer after confirming opcode and method scope.
- Inline-cache policy bug: preserve current megamorphic contract unless the task explicitly changes the profile format and inliner policy.

## Cannot Conclude

- `.ap` exists does not prove PAOC loaded or used it.
- A loaded profile does not prove the target method has usable profile data.
- Branch-profile support does not mean every compiler path consumes every counter.
- Megamorphic does not mean Ark keeps the hottest four receiver classes.
- Profile on/off differences prove involvement, not the final root cause.
