---
name: ohos-issue-arkruntime-thread-safety-audit
description: Use this skill when auditing, reviewing, or fixing thread-safety issues in ArkCompiler Runtime Core, especially ArkTS-Sta ETS stdlib and plugin code under static_core/plugins/ets. It covers static mutable state, singleton initialization, shared maps/caches/counters/timers, taskpool/EAWorker concurrency, TSAN follow-up, and concurrent test design.
metadata:
  author: openharmony
  scope: domain
  stage: troubleshooting
  domain: arkruntime
  capability: thread-safety-audit
  version: 0.1.0
  status: draft
  tags:
    - arkruntime
    - thread-safety
    - concurrency
    - troubleshooting
  
---

# OH Ark Runtime Thread Safety Audit

Use this skill to inspect, review, or fix thread-safety issues in ArkCompiler Runtime Core, especially in:

- ETS stdlib files under `static_core/plugins/ets/stdlib/**/*.ets`
- ETS runtime/plugin support code under `static_core/plugins/ets/**`
- tests under `static_core/plugins/ets/tests/`
- related native C++ only when an ETS API crosses the native boundary or a TSAN report points there

The common trigger is ArkTS-Sta's concurrent execution model: public stdlib APIs can be called from `taskpool`, `EAWorker`, or multiple coroutines/workers, so static mutable state and global singletons must be treated as shared across threads unless proven otherwise.

## Source-Backed APIs

Use only APIs/types that can be found in this checkout or in official OpenHarmony documentation. Examples below are source-backed by this repository; treat non-exported helpers as internal implementation references, not public API recommendations.

| API/type | Source |
|---|---|
| `AtomicInt`, `AtomicLong`, `AtomicBoolean` | `static_core/plugins/ets/stdlib/std/concurrency/Atomics.ets:83`, `static_core/plugins/ets/stdlib/std/concurrency/Atomics.ets:194`, `static_core/plugins/ets/stdlib/std/concurrency/Atomics.ets:782` |
| `Atomics.load` | `static_core/plugins/ets/stdlib/std/concurrency/LegacyAtomics.ets:253` |
| `ConcurrentHashMap` | `static_core/plugins/ets/stdlib/std/containers/ConcurrentHashMap.ets:131` |
| `Mutex`, `QueueSpinlock` | `static_core/plugins/ets/stdlib/std/core/SyncPrimitives.ets:43`, `static_core/plugins/ets/stdlib/std/core/SyncPrimitives.ets:156` |
| `ConcurrencyHelpers.mutexCreate`, `ConcurrencyHelpers.lockGuard` | `static_core/plugins/ets/stdlib/std/core/ConcurrencyHelpers.ets:27`, `static_core/plugins/ets/stdlib/std/core/ConcurrencyHelpers.ets:31`; package-local variants also exist under `std/concurrency` and `std/containers` |
| `taskpool.execute` | `static_core/plugins/ets/stdlib/std/concurrency/taskpool.ets:1841`, `static_core/plugins/ets/stdlib/std/concurrency/taskpool.ets:1852`, `static_core/plugins/ets/stdlib/std/concurrency/taskpool.ets:1863` |
| `EAWorker` | `static_core/plugins/ets/stdlib/std/core/EAWorker.ets:65` |
| `CoroutineExtras.stopTaskpool` | `static_core/plugins/ets/stdlib/std/debug/concurrency/CoroutineExtras.ets:42` |

If a suggested example uses an API/type that cannot be resolved with `rg` in the target checkout, remove the example or mark it as internal pseudocode.

## Scanning Workflow

Start from the user-provided file, diff, or API surface. Use `<target-paths>` below for those files or their nearest owning directory. Only expand to all of `static_core/plugins/ets` when the request has no narrower scope.

### Phase 1: ETS Static Mutable State Detection

Find static fields, global-looking mutable objects, caches, locks, and atomics in ETS/TS files:

```bash
rg -n "static .*[:=]|private static|public static|const .*[:=]|let .*[:=]|new Map|new Array|StringBuilder|ConcurrentHashMap|Mutex|QueueSpinlock|Atomic" \
    --type-add 'ets:*.ets' --type-add 'ets:*.ts' -t ets \
    <target-paths>
```

### Phase 2: Concurrency Entry Point Analysis

Decide whether the candidate state is reachable from concurrent paths:

- public APIs and exported functions
- `taskpool.execute` / `EAWorker`
- runtime or stdlib callbacks
- ETS methods declared as native

Use local call-site searches around the candidate API:

```bash
rg -n "taskpool\\.execute|EAWorker|callback|setTimeout|setInterval|native .*\\(|public .*\\(" \
    --type-add 'ets:*.ets' --type-add 'ets:*.ts' -t ets \
    <target-paths>
```

Registration or initialization functions are not concurrent entry points by themselves. Treat them as risks only if there is evidence they can be called concurrently after workers or user code start.

### Optional Native Follow-up

Check native code only when the ETS candidate is a native method, the stack trace points to C++, or the user explicitly asks for native/TSAN analysis.

```bash
rg -n "static .*|std::once_flag|std::mutex|os::memory::Mutex|std::atomic|thread_local|std::vector|std::map|std::set|ani_native_function" \
    --type cpp \
    <related-native-paths>
```

After these phases, classify each candidate before proposing a fix:

| Category                                         | Usually safe? | What to check                              |
| ------------------------------------------------ | ------------: | ------------------------------------------ |
| `static readonly` immutable constants            |           Yes | No mutable object hidden inside            |
| static primitive counters/flags                  |            No | `++`, direct read/write, visibility        |
| static `Map`/`Array`/`StringBuilder`             |            No | concurrent mutation, check-then-act        |
| singleton instance                               |            No | lazy initialization race                   |
| registry/cache                                   |            No | get-or-create, stale pairing, invalidation |
| instance fields in per-object objects            |         Maybe | object may be globally shared              |
| `ConcurrentHashMap`/Atomic/Mutex protected state |         Maybe | critical section covers whole invariant    |

Do not call a file safe only because it has a lock somewhere. Verify the lock protects the full invariant.

## Risk Criteria

Use four conditions to identify a meaningful risk:

1. Shared mutable state: static field, singleton field, global cache, or shared object reachable from a singleton.
2. Concurrent entry: API can be called by user code, stdlib callbacks, taskpool, EAWorker, timers, or worker threads.
3. Missing or incomplete synchronization: no atomic/lock/concurrent container, or lock only protects part of a check-then-act sequence.
4. Concrete impact: explain what can go wrong, such as lost update, stale state, wrong visible result, leaked task, duplicated callback, or container corruption.

Do not assign **High** just because a scan matched `static`, `ConcurrentHashMap`, `Map`, or a lazy-init shape. First prove the concurrent path and the user-visible or runtime-visible impact. If no concrete failure mode can be described, prefer leaving the code unchanged.

Risk levels:

- **High**: proven crash, deadlock, memory/object/container corruption, unbounded resource leak, or deterministic wrong result in a public concurrent API.
- **Medium**: proven lost update or broken lifecycle in a reachable concurrent path, such as leaked task metadata, duplicate execution, corrupted output, or incorrect cleanup.
- **Low**: bounded or recoverable race, such as stale cache, duplicate ID/name, inaccurate diagnostics, missed statistics, debug/introspection-only inconsistency, or rare timing window.
- **Candidate**: suspicious pattern with weak reachability evidence or unclear impact. Do not recommend code changes unless further evidence appears.
- **No risk**: immutable constants, local variables, per-call data, single-threaded initialization/registration, or fully synchronized state with clear ownership.

When in doubt, report the issue as **Candidate** instead of upgrading the severity. Prefer no code change for **Candidate** and **No risk** findings.

## Common Bad Patterns

The snippets in this section are source-backed patterns, not standalone tests. Before copying them into code, verify imports, package visibility, and whether the helper is public or stdlib-internal in the target file.

### Lazy singleton initialization

Bad:

```ets
if (Console.instance == undefined) {
    Console.instance = new Console()
}
return Console.instance!
```

Fix (using QueueSpinlock.guard):

```ets
// Field definition (pseudocode - verify visibility in target class)
private static instanceLock: QueueSpinlock = new QueueSpinlock()

Console.instanceLock.guard(() => {
    if (Console.instance == undefined) {
        Console.instance = new Console()
    }
})
return Console.instance!
```

Alternative fix (using ConcurrencyHelpers):

```ets
// Field definition (pseudocode - ConcurrencyHelpers is package-local in std.core)
private static instanceLock: Object = ConcurrencyHelpers.mutexCreate()

ConcurrencyHelpers.lockGuard(Console.instanceLock, () => {
    if (Console.instance == undefined) {
        Console.instance = new Console()
    }
})
return Console.instance!
```

The check and assignment must be in the same critical section. Source: `QueueSpinlock.guard` at SyncPrimitives.ets:165, `ConcurrencyHelpers.lockGuard` at ConcurrencyHelpers.ets:31.

### Shared output buffer

When an API builds a string and then emits it, protect the whole operation:

```ets
// Field definition (pseudocode - verify in target class)
private outputLock: QueueSpinlock = new QueueSpinlock()

this.outputLock.guard(() => {
    let buf = this.lvl2Buf.get(level)!
    buf.append(s)
    this.printString(buf.toString(), level.valueOf())
    this.lvl2Buf.set(level, new StringBuilder)
})
```

Locking only `append` or only `printString` can still mix buffers. Source: `QueueSpinlock.guard` at SyncPrimitives.ets:165.

### Shared Map get-or-create

Bad:

```ets
let slot = map.get(key)
if (slot == undefined) {
    slot = new Slot()
    map.set(key, slot)
}
return slot
```

Fix pattern (using Mutex.lockGuard):

```ets
// Field definition (pseudocode - verify in target class)
private static slotLock: Mutex = new Mutex()

const existing = states.get(key)
if (existing !== undefined) {
    return existing
}

slotLock.lockGuard(() => {
    if (states.get(key) === undefined) {
        states.set(key, new Slot())
    }
})

const slot = states.get(key)
if (slot === undefined) {
    throw new Error(`Failed to create slot for '${key}'`)
}
return slot
```

Use `ConcurrentHashMap` for concurrent storage and a separate lock for lazy creation when no atomic `computeIfAbsent` exists. Source: `Mutex.lockGuard` at SyncPrimitives.ets:48.

### Unsynchronized counter

Bad:

```ets
private static uniqueNameCounter: long = -1
return (++Proxy.uniqueNameCounter).toString()
```

Fix:

```ets
private static uniqueNameCounter: AtomicLong = new AtomicLong(0)
return Proxy.uniqueNameCounter.fetchAdd(1).toString()
```

For post-increment from `0`:

```ets
oldCounter++
```

the atomic equivalent is also:

```ets
counter.fetchAdd(1)
```

with initial value `0`.

### Unsynchronized boolean flag

Bad:

```ets
private static LOG_ENABLED: boolean = false
Logger.LOG_ENABLED = true
if (Logger.LOG_ENABLED) { ... }
```

Fix:

```ets
private static LOG_ENABLED: AtomicBoolean = new AtomicBoolean(false)
Logger.LOG_ENABLED.store(true)
if (Logger.LOG_ENABLED.load()) { ... }
```

### Paired cache fields

Bad:

```ets
private static lastParsedTag: string | undefined = undefined
private static lastParsedResult: ParsedLocaleData | undefined = undefined
```

If `tag` and `result` must match, they are one invariant. Protect reads and writes with one lock, or replace them with one immutable cache entry object.

Minimal fix (source-backed from Intl.ets):

```ets
// Field definition (ConcurrencyHelpers.mutexCreate returns Object)
// Note: ConcurrencyHelpers is package-local (@internal) in std.core
// Real usage in Intl.ets:1456 uses this pattern
private static localeCacheMutex: Object = ConcurrencyHelpers.mutexCreate()

private static getCachedLocale(tag: string): ParsedLocaleData | undefined {
    let result: ParsedLocaleData | undefined = undefined
    ConcurrencyHelpers.lockGuard(Locale.localeCacheMutex, () => {
        if (Locale.lastParsedTag == tag && Locale.lastParsedResult != undefined) {
            result = Locale.lastParsedResult
        }
    })
    return result
}

private static setCachedLocale(tag: string, data: ParsedLocaleData): void {
    ConcurrencyHelpers.lockGuard(Locale.localeCacheMutex, () => {
        Locale.lastParsedTag = tag
        Locale.lastParsedResult = data
    })
}
```

Do not lock only one field. Do not read `tag` outside the lock and `result` inside the lock. Source: `Intl.ets:1456`, `ConcurrencyHelpers.ets:27,31`.

### Compound state inside a slot

If a value has multiple fields that must change together, use an internal lock (source-backed):

```ets
final class TimerSlot {
    public tryStart(now: long): boolean {
        let started = false
        this.lock.guard(() => {
            if (!this.active) {
                this.startTime = now
                this.active = true
                started = true
            }
        })
        return started
    }

    private startTime: long = 0
    private active: boolean = false
    private lock: QueueSpinlock = new QueueSpinlock()
}
```

Do not use separate atomics for multi-field invariants unless the state machine is deliberately designed and reviewed. Source: `QueueSpinlock.guard` at SyncPrimitives.ets:165.

## Fix Selection Guide

Choose the narrowest synchronization that protects the real invariant:

| Problem                            | Preferred fix                              |
| ---------------------------------- | ------------------------------------------ |
| single numeric counter             | `AtomicInt` / `AtomicLong`                 |
| single boolean flag                | `AtomicBoolean`                            |
| pair/triple fields that must match | one mutex around all reads/writes          |
| singleton lazy init                | lock-guarded check-then-act                |
| shared key-value registry          | `ConcurrentHashMap` + locked get-or-create |
| per-key mutable compound state     | per-slot lock                              |
| global output line construction    | one output lock around build + emit        |

Avoid:

- locking only writes while reads remain unlocked
- adding atomics to related fields without a design for consistency
- creating a lock but leaving check-then-act outside it
- changing initial values without preserving old visible sequences

## Review Checklist

When reviewing a patch, verify:

1. The old race is actually removed, not only made harder to reproduce.
2. Public behavior is preserved.
   - Pre-increment `++x` vs `fetchAdd(1)` requires adjusting initial value.
   - Post-increment `x++` maps naturally to `fetchAdd(1)`.
3. The critical section covers the whole invariant.
4. Locks are not held while calling arbitrary user callbacks unless intended.
5. Lock order is consistent if multiple locks are acquired.
6. `ConcurrentHashMap` values do not contain unsynchronized mutable fields.
7. Unused fields are deleted or documented; do not label unused fields as fixed real races.

## Test Strategy

Use tests proportional to risk.

### Functional concurrency tests

Use existing repository tests as templates instead of inventing new API shapes:

- `taskpool.execute` with function arguments: `static_core/plugins/ets/tests/ets_func_tests/std/containers/BlockingQueue/AddAndPollStress.ets:47`
- taskpool cleanup in tests: `static_core/plugins/ets/tests/ets-common-tests/taskpool/common_tasks_new.ets:423`
- `CoroutineExtras.stopTaskpool` declaration: `static_core/plugins/ets/stdlib/std/debug/concurrency/CoroutineExtras.ets:42`
- `Atomics.load` declaration for typed-array barriers: `static_core/plugins/ets/stdlib/std/concurrency/LegacyAtomics.ets:253`

Prefer simple worker task signatures used by existing tests. If a start barrier is needed, cite the source for the atomic operation used by the barrier and keep the snippet local to the test file.

### TSAN tests

When TSAN is part of validation, keep the note short: state the raced variable/function and whether the race is in ETS code or native code.

### Targeted tests

Add focused tests for the affected shared state:

- output APIs: assert no mixed line/buffer content, avoid requiring deterministic cross-thread order unless the API promises it
- stateful counters/timers: run many concurrent calls and validate totals/state transitions
- caches: cover same-key hits, different-key replacement, options/overrides, and invalid input paths

Be careful: a test that concurrently misses a cache may enter a slower parse path instead of the cached path. Mention this only when it affects the chosen test design.

## Validation Commands

**Prerequisites**: Commands assume execution from `arkcompiler_runtime_core` checkout root, with existing build artifacts in `static_core/build/`.

Before running validation:
1. Ensure current directory is `arkcompiler_runtime_core` repository root
2. Verify `static_core/build/` exists (generated by previous build process)
3. Confirm build tools are available: `ninja`, `es2panda`, `ark`, `ark_disasm`

```bash
# Run from arkcompiler_runtime_core checkout
cd /path/to/arkcompiler_runtime_core

# Check for whitespace and formatting errors in changed files
ninja -C static_core/build plugins/ets/etsstdlib.abc
static_core/build/bin/es2panda --extension=ets --stdlib=static_core/build/plugins/ets/etsstdlib.abc --output=/tmp/test.abc <test.ets>
static_core/build/bin/ark --boot-panda-files=static_core/build/plugins/ets/etsstdlib.abc --load-runtimes=ets --verification-mode=ahead-of-time /tmp/test.abc <entrypoint>
```

Entrypoints can be discovered with:

```bash
static_core/build/bin/ark_disasm /tmp/test.abc /tmp/test.pa
rg -n "\\.function .* main\\(" /tmp/test.pa
```
