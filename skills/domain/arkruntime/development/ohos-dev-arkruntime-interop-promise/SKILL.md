---
name: ohos-dev-arkruntime-interop-promise
description: ETS-JavaScript interop Promise bridging system in ArkCompiler. Use this skill when working on cross-language Promise conversion between ETS (ArkTS) and JavaScript, including JSConvertPromise Wrap/Unwrap, EtsPromise proxy creation, EtsPromiseRef bridging, CreatePromiseLink, OnJsPromiseCompleted callbacks, connectPromise, SettleJsPromise, PromiseInteropResolve/Reject, EtsAwaitPromise/AwaitProxyPromise, callback queue management, or any code under js_convert.h (Promise section), js_job_queue, ets_promise, ets_promise_ref, std_core_Promise.cpp, or PromiseInterop.ets. Also use when debugging cross-VM Promise state synchronization, coroutine suspension/resumption during await, or napi_deferred lifecycle issues.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkruntime
  capability: interop-promise
  version: 0.1.0
  status: draft
  tags:
    - arkruntime
    - interop
    - promise
    - arkts
---

# Interop Promise - ETS/JS Cross-Language Promise Bridging

Guide for understanding, developing, and debugging the Promise interop system that bridges ETS (ArkTS) Promises with JavaScript Promises in the ArkCompiler hybrid runtime.

## Reference Loading

This skill ships with a detailed API reference. Load it only when the task requires exact method signatures, parameter types, or full class layouts — it is large and unnecessary for most debugging or architecture-level questions.

**Load `references/api-reference.md` when:**
- Writing or reviewing code that calls specific EtsPromise / JSConvertPromise methods and you need the exact parameter types and return values
- Understanding the full member variable layout of EtsPromise (value_, mutex_, event_, callbackQueue_, etc.)
- Tracing the complete WrapImpl / UnwrapImpl pseudocode with every NAPI call spelled out
- Looking up intrinsic function signatures (EtsPromiseResolve, EtsPromiseReject, EtsAwaitPromise, SubscribePromiseOnResultObject)
- Reviewing SettleJsPromise constraints or CreatePromiseLink implementation details

**Do NOT load `references/api-reference.md` when:**
- You only need to understand the conversion direction (JS→ETS or ETS→JS) — the "Two Core Conversion Paths" section below is sufficient
- Debugging a stuck await — the "Debugging a stuck await" checklist below walks the steps without needing exact signatures
- Understanding state transitions — the "Promise State Machine" diagram below covers all states
- Looking up source file locations — the "Source Code Locations" table below lists all paths
- The question is about type routing logic or .d.ets signatures — the "Type Routing" section below explains the compile-time mechanism

## Architecture Overview

The interop Promise system enables transparent bidirectional Promise conversion between the static ETS VM and dynamic JS VM. When ETS calls a JS async function (or vice versa), the system creates proxy objects and registers callbacks so that resolve/reject events propagate correctly across the language boundary.

```
ETS VM Side                              JS VM Side
──────────────                           ──────────────
EtsPromise                                JS Promise
    │                                          │
    ├── interopObject_ → EtsPromiseRef ────────┤
    ├── linkedPromise_ → EtsPromiseRef          │
    ├── event_ (await suspend/resume)            │
    ├── mutex_ (thread safety)                   │
    └── callbackQueue_ (.then handlers)          │
                                               │
         SharedReferenceStorage ────────────────┘
         (EtsPromiseRef ↔ JS Promise mapping)

JS→ETS path:  JS Promise → JSCONVERT_UNWRAP(Promise) → EtsPromise proxy
ETS→JS path:  EtsPromise → JSCONVERT_WRAP(Promise) → JS Promise
```

## Source Code Locations

| Component | Path |
|-----------|------|
| JSConvertPromise (Wrap/Unwrap) | `plugins/ets/runtime/interop_js/js_convert.h` |
| EtsPromise class | `plugins/ets/runtime/types/ets_promise.h/.cpp` |
| EtsPromiseRef bridge | `plugins/ets/runtime/types/ets_promise_ref.h` |
| JsJobQueue / CreatePromiseLink | `plugins/ets/runtime/interop_js/js_job_queue.h/.cpp` |
| Promise intrinsics | `plugins/ets/runtime/intrinsics/std_core_Promise.cpp` |
| SettleJsPromise / PromiseInterop | `plugins/ets/runtime/interop_js/intrinsics_api_impl.cpp` |
| PromiseInterop.ets | `plugins/ets/stdlib/std/interop/js/PromiseInterop.ets` |
| ETS Promise.ets | `plugins/ets/stdlib/std/core/Promise.ets` |
| CallJSHandler (ETS→JS calls) | `plugins/ets/runtime/interop_js/call/call_js.cpp` |
| CallETSHandler (JS→ETS calls) | `plugins/ets/runtime/interop_js/call/call_ets.cpp` |
| Type routing (ConvertArgToEts/JS) | `plugins/ets/runtime/interop_js/call/arg_convertors.h` |

## Two Core Conversion Paths

### Path 1: JS Promise → ETS Proxy (JSCONVERT_UNWRAP)

Triggered when ETS calls a JS function that returns a Promise.

**Call chain:**
```
CallJSHandler::Handle()
  → ConvertRetval() → ConvertArgToEts() → ConvertRefArgToEts()
  → JSConvertPromise::UnwrapImpl()  [JSCONVERT_UNWRAP(Promise)]
```

**UnwrapImpl steps:**
1. **Identity check**: `SharedReferenceStorage::GetReference(env, jsVal)` — reuse existing proxy if JS Promise was already wrapped
2. **Create proxy EtsPromise**: `EtsPromise::Create(coro)` — STATE_PENDING
3. **Create EtsPromiseRef bridge**: Why? Because SharedReferenceStorage uses MarkWord for interop hash, and EtsPromise uses MarkWord for Lock — they conflict
4. **Register mapping**: `SharedReferenceStorage::CreateJSObjectRef(ctx, ref, jsVal)` — bidirectional EtsPromiseRef ↔ JS Promise
5. **Mark as proxy**: `hpromise->SetLinkedPromise(coro, href)` — enables `IsProxy()` check in await
6. **Create link**: `EtsPromise::CreateLink()` → `JsJobQueue::CreatePromiseLink()` — registers C++ callbacks on JS Promise's `.then()`

### Path 2: ETS Promise → JS Promise (JSCONVERT_WRAP)

Triggered when JS calls an ETS function that returns a Promise.

**Call chain:**
```
CallETSHandler::HandleImpl()
  → ConvertArgToJS() → ConvertRefArgToJS()
  → JSConvertPromise::WrapImpl()  [JSCONVERT_WRAP(Promise)]
```

**WrapImpl has two paths:**

**Fast path** (EtsPromise already settled when Wrap is called):
1. Identity check via `GetInteropObject()` + `HasReference()`
2. `napi_create_promise(env, &deferred, &jsPromise)` — create pending JS Promise
3. `Lock()` → check `!IsPending() && !IsLinked()` → fast path
4. Convert ETS value to JS value via `JSRefConvertResolve`
5. `napi_resolve_deferred()` or `napi_reject_deferred()` — immediately settle JS Promise
6. Create EtsPromiseRef + register in SharedReferenceStorage

**Slow path** (EtsPromise still pending):
1-2. Same as fast path
3. `Lock()` → `IsPending() || IsLinked()` → slow path
4. `Unlock()` → call `PromiseInterop.connectPromise(promise, deferred)` via Invoke
5. `connectPromise` registers `.then()` callbacks that call `PromiseInteropResolve/Reject` native methods
6. When EtsPromise resolves later: `OnPromiseCompletion()` → `LaunchCallback()` → `PromiseInteropResolve()` → `SettleJsPromise()` → `napi_resolve_deferred()`
7. Create EtsPromiseRef + register in SharedReferenceStorage

## Key Classes

### EtsPromise (`ets_promise.h`)

States: `STATE_PENDING(0)`, `STATE_RESOLVED(1)`, `STATE_REJECTED(2)`, `STATE_LINKED(3)`

| Method | Description |
|--------|-------------|
| `Create(coro)` | Create PENDING promise with mutex + event |
| `Resolve(coro, value)` | Set value, transition to RESOLVED, call OnPromiseCompletion |
| `Reject(coro, error)` | Set error, transition to REJECTED, call OnPromiseCompletion |
| `Wait()` | Block coroutine via `EtsEvent::Wait()` |
| `IsProxy()` | `linkedPromise_ != nullptr` — true for JS Promise proxies |
| `IsPending/Resolved/Rejected/Linked()` | State checkers |
| `SubmitCallback(cb, workerDomain)` | Add .then handler to callbackQueue |
| `CreateLink(source, target)` | Delegate to `JobQueue::CreateLink()` |
| `OnPromiseCompletion(coro)` | Fire event, launch queued callbacks, handle unhandled rejection |
| `LaunchCallback(coro, cb, groupId)` | Execute callback in new coroutine (PROMISE_CALLBACK priority) |
| `ChangeStateToPendingFromLinked()` | LINKED → PENDING state transition |
| `GetInteropObject()` / `SetInteropObject()` | EtsPromiseRef bridge object |
| `GetLinkedPromise()` / `SetLinkedPromise()` | For proxy detection |
| `Lock()` / `Unlock()` / `IsLocked()` | Thread-safe mutex via MarkWord |

**Member variables:** `value_`, `mutex_`, `event_`, `callbackQueue_`, `workerDomainQueue_`, `interopObject_`, `linkedPromise_`, `queueSize_`, `state_`

### EtsPromiseRef (`ets_promise_ref.h`)

Minimal bridge object to avoid MarkWord conflict between SharedReferenceStorage (interop hash) and EtsPromise (Lock).

```cpp
class EtsPromiseRef : public EtsObject {
    EtsObject *target_ {};  // Points to the actual EtsPromise
    // MarkWord used by SharedReferenceStorage for interop hash index
};
```

### JsJobQueue (`js_job_queue.h/.cpp`)

Extends `JobQueue` with JS-specific callback and promise linking.

| Method | Description |
|--------|-------------|
| `CreatePromiseLink(jsObject, etsPromise)` | Register C++ then/catch callbacks on JS Promise |
| `Post(fn, data)` | Post callback to JS job queue via JS Promise |

**Global C++ callbacks registered on JS Promise:**
- `OnJsPromiseResolved(env, info)` → delegates to `OnJsPromiseCompleted(env, info, true)`
- `OnJsPromiseRejected(env, info)` → delegates to `OnJsPromiseCompleted(env, info, false)`
- `OnJsPromiseCompleted(env, info, isResolved)`: Converts JS value to ETS, calls `EtsPromiseResolve` or `EtsPromiseReject`

## ETS Await Mechanism

```
ETS: await p;
  → EtsAwaitPromise(p)
    → IsProxy()?
      → YES: AwaitProxyPromise()
        → promise->Wait()  // EtsEvent::Wait() — coroutine suspends
        → [JS resolves → OnJsPromiseCompleted → EtsPromiseResolve → Resolve → OnPromiseCompletion → Fire()]
        → Wait() returns
        → IsResolved()? return GetValue() : throw exception
      → NO: promise->Wait()  // Direct ETS Promise await
```

**Key**: `EtsAwaitPromise` first yields CPU via `coro->GetManager()->Schedule()` to allow other coroutines (including JS microtasks) to execute before checking proxy status.

## Promise State Machine

```
                    Create()
                       │
                       ▼
                 STATE_PENDING
                /       │        \
    resolve()  /   CreateLink()  \  reject()
              /        │          \
             ▼         ▼           ▼
    STATE_RESOLVED  STATE_LINKED  STATE_REJECTED
                        │
             resolve() │ (from subscribeOnAnotherPromise)
                        ▼
                  STATE_RESOLVED
```

- **PENDING**: Initial state, or after ChangeStateToPendingFromLinked()
- **LINKED**: Proxy Promise waiting for JS source to settle
- **RESOLVED/REJECTED**: Terminal states, value_ holds result

## Callback Queue and Execution

`.then()` registration flow:
```
p.then(onResolve, onReject)
  → Promise.ets: thenImpl()
  → [native] EtsPromiseSubmitCallback(promise, callback, workerDomain)
  → SubmitCallback(): if settled → execute immediately; else → add to callbackQueue_
```

Execution on completion:
```
OnPromiseCompletion(coro)
  → Fire()  // Wake awaiters
  → for each callback in queue:
      → LaunchCallback(coro, callback, groupId)
        → Create CompletionEvent
        → coroManager->Launch(event, method, args, groupId, PROMISE_CALLBACK)
```

**Queue capacity management**: Dynamic resizing with `EnsureCapacity()` — growth strategy is `2 * oldSize + 1`.

## SettleJsPromise — ETS→JS Bridge

The final step that completes a JS Promise from ETS:

```cpp
void SettleJsPromise(EtsObject *value, napi_deferred deferred, EtsInt state)
{
    // Must run on main worker thread
    INTEROP_CODE_SCOPE_ETS_TO_JS(executionCtx);
    // Convert ETS value to JS value
    completionValue = refconv->Wrap(ctx, value);
    // Complete the JS Promise
    napi_resolve_deferred(env, deferred, completionValue);  // or napi_reject_deferred
}
```

Called from `PromiseInteropResolve()` / `PromiseInteropReject()` which are native methods invoked by `PromiseInterop.ets` callbacks.

## PromiseInterop.ets — Slow Path Connection

```typescript
final class PromiseInterop {
    static connectPromise<T>(p: Promise<T>, deferred: long): void {
        p.then<void, void>(
            (value: T): void => { PromiseInterop.resolve<T>(value, deferred); },
            (error: Any): void => { PromiseInterop.reject(error, deferred); }
        );
    }
    private static native resolve<T>(value: T, deferred: long): void;
    private static native reject(error: Any, deferred: long): void;
}
```

This ETS code is invoked via `PlatformTypes()->interopPromiseInteropConnectPromise->GetPandaMethod()->Invoke()` from C++ during JSCONVERT_WRAP slow path.

## Type Routing — How Promise Conversion is Triggered

Promise conversion is **not** triggered by runtime type detection (e.g., `napi_is_promise`). Instead, it's driven by **compile-time type signatures** from `.d.ets` files:

```
.d.ets: export declare function jsAsync(): Promise<string>;
         ↓ (compiler generates ProtoReader type info)
ProtoReader return type = EtsPromise class
         ↓ (runtime type routing)
ConvertRefArgToEts → JSRefConvertResolve(ctx, EtsPromise.RuntimeClass)
         ↓ (finds JSConvertPromise converter)
JSConvertPromise::UnwrapImpl() or WrapImpl()
```

If `.d.ets` declares `Promise<T>` but JS returns non-Promise, `ASSERT(isPromise)` fails in Debug mode.

## Return Value Type Routing (Fast Path Reference)

| Direction | Entry Point | Router | Converter |
|-----------|-------------|--------|-----------|
| JS→ETS (return) | `CallJSHandler::ConvertRetval()` | `ConvertArgToEts()` → `ConvertRefArgToEts()` | `JSConvertPromise::UnwrapImpl()` |
| ETS→JS (return) | `CallETSHandler::ConvertArgToJS()` | `ConvertRefArgToJS()` | `JSConvertPromise::WrapImpl()` |
| JS→ETS (param) | `CallETSHandler::ConvertArgs()` | `ConvertArgToEts()` | `JSConvertPromise::UnwrapImpl()` |
| ETS→JS (param) | `CallJSHandler::ConvertArgsAndCall()` | `ConvertArgToJS()` | `JSConvertPromise::WrapImpl()` |

## Testing Patterns

Three verification patterns exist for interop Promise testing:

| Pattern | ETS Promise State at Return | JSCONVERT_WRAP Path | JS Verification |
|---------|----------------------------|---------------------|-----------------|
| A: ETS internal verify | PENDING | Slow path | Poll ETS global state |
| B: JS verify resolved | RESOLVED | Fast path | JS `.then()` on returned Promise |
| C: JS verify pending | PENDING | Slow path | JS `.then()` + setTimeout trigger resolve |

## Threading and Coroutine Considerations

- **SettleJsPromise** must execute on main worker thread (`ASSERT(IsMainWorker())`)
- **Promise callbacks** launch in new coroutines with `PROMISE_CALLBACK` priority
- **Worker domains**: MAIN or GENERAL — affects which coroutine group handles the callback
- **Coroutine switch**: `EtsAwaitPromise` yields CPU before suspending to allow JS microtask processing
- **Mutex**: EtsPromise uses MarkWord-based Lock for thread safety (hence need for EtsPromiseRef)
- **Event**: EtsEvent provides coroutine suspension/resumption for await

## Common Tasks

### Adding a new interop type that can cross Promise boundaries
1. Implement `JSConvert<YourType>::Wrap()` and `UnwrapImpl()` in `js_convert.h` — read `references/api-reference.md` for the existing `JSConvertPromise` WrapImpl/UnwrapImpl pseudocode as a template
2. Register in `JSRefConvertResolve` lookup chain
3. Handle conversion in `OnJsPromiseCompleted` and `SettleJsPromise` (already generic via `JSRefConvertResolve`)

### Debugging a stuck await
1. Check `EtsPromise::IsProxy()` — is it a JS proxy?
2. Check state — stuck in PENDING or LINKED?
3. Verify `CreatePromiseLink` registered callbacks — check JS Promise's `.then()` was called. If you need the exact NAPI calls in CreatePromiseLink, read `references/api-reference.md` → "JsJobQueue Class"
4. Check `OnJsPromiseCompleted` was invoked — JS microtask queue running?
5. Check `EtsEvent::Fire()` was called — `OnPromiseCompletion` executed?
6. Check coroutine scheduling — `Schedule()` yields properly?

### Debugging type conversion failures
1. Verify `.d.ets` type signature matches actual JS return type
2. Check `ProtoReader` type info at runtime
3. In Debug: `ASSERT(isPromise)` in UnwrapImpl catches mismatch. For the full WrapImpl/UnwrapImpl step-by-step pseudocode with exact NAPI calls, read `references/api-reference.md` → "JSConvertPromise Class"
4. Check `JSRefConvertResolve` finds the correct converter for the value type
