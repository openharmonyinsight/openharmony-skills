# ark_aot Startup Debugging

Use this reference when `ark_aot` fails before method compilation or the earliest stack/log points at runtime initialization.

## Boundary

`ark_aot` creates a real Ark Runtime/PandaVM so the compiler can query class linker, metadata, boot panda files, AotManager, and runtime interfaces. This does not mean method-level PAOC compilation has started.

## Startup Signals

| Signal | Likely phase |
|---|---|
| `Runtime::Create` | Runtime initialization. |
| `PoolManager::Initialize` / `MmapMemPool` | Memory pool / virtual address / resource setup. |
| boot panda file loading errors | Runtime/class linker setup. |
| no `PAOC:` or method compile logs | Compilation may not have started. |
| SIGABRT with Ark fatal log | Use the earliest fatal line, not only the final stack. |

## Source Anchors

- `static_core/compiler/tools/paoc/paoc.cpp`: `PaocInitializer::InitRuntime()` validates runtime options before runtime creation.
- In non-ASAN builds, it sets `internal-memory-size-limit` to the PAOC code-emission limit when the option was not already set.
- It sets `ArkAot=true` before creating the runtime.
- If `taskmanager-workers-count` was not set, it falls back to `1`.
- It then calls `Runtime::Create(*runtimeOptions_)`; failures here are still startup/runtime initialization, before method-level PAOC compilation.

## Debugging Steps

1. Find the earliest child-process fatal/error line.
2. Determine build flavor: ASAN/debug/release can change memory limits and failure likelihood.
3. Confirm whether PAOC method compilation logs exist after runtime init.
4. Inspect runtime option setup before `Runtime::Create`.
5. Only pivot to PAOC/codegen if there is evidence runtime initialization completed and compilation began.

## Fix Direction

- Resource/VA failure: inspect runtime memory configuration, ASAN-specific behavior, host/device limits, and mmap failure handling.
- Boot file failure: inspect boot path args and file availability.
- Runtime init option issue: fix `ark_aot` option construction or validation.

## Cannot Conclude

- A crash inside `Runtime::Create` is not automatically a PAOC/codegen bug.
- Rare startup SIGABRTs should be treated as resource/environment-sensitive until logs prove deterministic compiler behavior.
