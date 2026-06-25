# Runtime Load and Link Debugging

Use this reference when an AOT artifact exists but it is unclear whether it loaded, linked, or executed.

## Evidence Chain

1. AOT file discovery/loading.
2. AotManager records the file.
3. Method linkage attempts.
4. `Method` receives a compiled entry point.
5. Compiled code executes and reaches downstream AOT-specific runtime paths.

## Source Anchors

- `static_core/compiler/aot/aot_manager.cpp`: `AotManager::AddFile()` opens the `.an`, patches/initializes AOT tables, records `AotPandaFile` entries, and maps panda-file names.
- `static_core/runtime/class_linker.cpp`: `ClassLinker::LoadMethods()` asks `aotManager_->FindPandaFile(klass->GetPandaFile()->GetFullFileName())` when AOT entrypoint linking is enabled.
- `MaybeLinkMethodToAotCode()` calls `aotClass.FindMethodCodeEntry(methodIndex)` and then `method->SetCompiledEntryPoint(entry)` when an entry exists.
- Therefore the method-level proof chain is `AotManager::AddFile` -> `ClassLinker::LoadMethods` / `FindPandaFile` -> `MaybeLinkMethodToAotCode` -> `Method::SetCompiledEntryPoint`.

## Useful Signals

| Signal | Meaning |
|---|---|
| `MaybeLinkMethodToAotCode` | Direct method-to-AOT linkage point. |
| `RegisterAotStringRoot` | Strong downstream signal that compiled AOT code has executed string-resolution logic. |
| `HasAotFiles` | Runtime believes at least one AOT file is loaded. Useful for escape/fallback gating. |
| `aot_escape.txt` | Crash/fallback state file; check who writes it and who consumes it. |

## Debugging Steps

1. Confirm the runtime looked for the expected `.an` path.
2. Confirm the file was loaded and registered in AotManager.
3. For a target method, inspect link skip reasons.
4. Compare pre/post entrypoint values if adding temporary tracing.
5. Use downstream runtime calls as execution proof only when their call path is AOT-specific.

## Method-Level Localization

When an `.an` file exists but the symptom is method-specific, identify the current method before blaming codegen:

- log the expected panda file, class, method full name/signature, and method id;
- log whether AotManager has the file and whether the target method lookup succeeded;
- log the link decision and skip reason before changing dispatch or codegen;
- compare the method entry point before and after linkage;
- if the method did not link, do not use its machine code or runtime crash state as evidence for AOT execution.

Use `ark_aotdump` to inspect generated product metadata/code only after confirming the `.an` belongs to the same input and version path being loaded.

## Fix Direction

- Wrong file path: fix recorded path/header metadata or runtime discovery path.
- Loaded but not linked: fix method identity, class context, compatibility checks, or skip condition.
- Linked but not executed: inspect dispatch entrypoint, deopt/escape/fallback flags, and call-site behavior.
- Escape/fallback behavior: inspect `HasAotFiles` and startup option handling before changing signal handlers.

## Cannot Conclude

- `.an` exists on disk does not prove it loaded.
- Loaded `.an` does not prove a specific method linked.
- A dumped method body does not prove that runtime dispatch entered that body.
- Registered signal handlers do not prove the current crash was recovered or caused by AOT.
