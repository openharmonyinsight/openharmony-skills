# Interop Promise API Reference

Complete class declarations, method signatures, enums, and key implementation details.

## Table of Contents

- [EtsPromise Class](#etspromise-class)
- [EtsPromiseRef Class](#etspromiseref-class)
- [JSConvertPromise Class](#jsconvertpromise-class)
- [JsJobQueue Class](#jsjobqueue-class)
- [Promise Intrinsics (C++)](#promise-intrinsics-c)
- [PromiseInterop.ets](#promiseinteropets)
- [SettleJsPromise](#settlejspromise)
- [Type Routing Functions](#type-routing-functions)
- [EtsPromise State Machine](#etspromise-state-machine)

---

## EtsPromise Class

**File:** `plugins/ets/runtime/types/ets_promise.h/.cpp`
**Namespace:** `ark::ets`

### States

```cpp
static constexpr uint32_t STATE_PENDING  = 0;
static constexpr uint32_t STATE_RESOLVED = 1;
static constexpr uint32_t STATE_REJECTED = 2;
static constexpr uint32_t STATE_LINKED   = 3;
```

### CoroutineMode

```cpp
enum class CoroutineMode {
    STACKFUL,   // Uses EtsEvent for suspend/resume
    STACKLESS,  // Uses EtsWasmEvent for suspend/resume
};
```

### Static Methods

```cpp
static EtsPromise *Create(EtsCoroutine *coro);
static EtsPromise *FromCoreType(ObjectHeader *obj);
static EtsPromise *FromEtsObject(EtsObject *obj);
static void CreateLink(EtsObject *source, EtsPromise *target);
static void LaunchCallback(EtsCoroutine *coro, EtsObject *callback,
                           const CoroutineWorkerGroup::Id &groupId);
```

### State Checkers

```cpp
bool IsResolved() const;
bool IsRejected() const;
bool IsPending() const;
bool IsLinked() const;
bool IsProxy() const;  // linkedPromise_ != nullptr
uint32_t GetState() const;
```

### Value Access

```cpp
EtsObject *GetValue(EtsCoroutine *coro) const;
```

### Synchronization

```cpp
void Lock();
void Unlock();
bool IsLocked() const;
EtsMutex *GetMutex(EtsCoroutine *coro) const;
void SetMutex(EtsCoroutine *coro, EtsMutex *mutex);
```

### Event Management (template)

```cpp
template <CoroutineMode MODE = CoroutineMode::STACKFUL>
auto *GetEvent(EtsCoroutine *coro) const;

void SetEvent(EtsCoroutine *coro, EtsObject *event);
```

### Promise Operations

```cpp
void Resolve(EtsCoroutine *coro, EtsObject *value);
void Reject(EtsCoroutine *coro, EtsObject *error);
void Wait();  // Suspend coroutine via EtsEvent::Wait()
void OnPromiseCompletion(EtsCoroutine *coro);
void SubmitCallback(EtsCoroutine *coro, EtsObject *callback, int32_t workerDomain);
void ChangeStateToPendingFromLinked();
```

### Interop / Proxy

```cpp
EtsObject *GetInteropObject(EtsCoroutine *coro) const;
void SetInteropObject(EtsCoroutine *coro, EtsObject *obj);
EtsObject *GetLinkedPromise(EtsCoroutine *coro) const;
void SetLinkedPromise(EtsCoroutine *coro, EtsObject *obj);
```

### Callback Queue

```cpp
EtsObjectArray *GetCallbackQueue(EtsCoroutine *coro) const;
void SetCallbackQueue(EtsCoroutine *coro, EtsObjectArray *queue);
EtsObjectArray *GetWorkerDomainQueue(EtsCoroutine *coro) const;
void SetWorkerDomainQueue(EtsCoroutine *coro, EtsObjectArray *queue);
int32_t GetQueueSize() const;
void ClearQueues(EtsCoroutine *coro);
```

### Member Variables

```cpp
ObjectPointer value_ {};              // Resolved/rejected value
ObjectPointer mutex_ {};              // Synchronization mutex (uses MarkWord)
ObjectPointer event_ {};              // Await suspend/resume event
ObjectPointer callbackQueue_ {};      // .then() callback array
ObjectPointer workerDomainQueue_ {};  // Per-callback worker domain
ObjectPointer interopObject_ {};      // EtsPromiseRef bridge
ObjectPointer linkedPromise_ {};      // Linked promise (proxy detection)
int32_t queueSize_ {0};              // Number of queued callbacks
uint32_t state_ {STATE_PENDING};     // Current state
```

---

## EtsPromiseRef Class

**File:** `plugins/ets/runtime/types/ets_promise_ref.h`
**Namespace:** `ark::ets`

```cpp
class EtsPromiseRef : public EtsObject {
public:
    static EtsPromiseRef *Create(EtsCoroutine *coro);
    static EtsPromiseRef *FromEtsObject(EtsObject *obj);

    EtsObject *GetTarget(EtsCoroutine *coro) const;
    void SetTarget(EtsCoroutine *coro, EtsObject *target);

private:
    ObjectPointer target_ {};
};
```

**Purpose:** Intermediary between EtsPromise and SharedReferenceStorage. SharedReferenceStorage uses the object's MarkWord for interop hash indexing, but EtsPromise's Lock also modifies MarkWord. EtsPromiseRef avoids this conflict.

---

## JSConvertPromise Class

**File:** `plugins/ets/runtime/interop_js/js_convert.h`
**Namespace:** `ark::ets::interop::js`

### WrapImpl — ETS Promise → JS Promise (JSCONVERT_WRAP)

```cpp
// Expanded from JSCONVERT_WRAP(Promise) macro
inline napi_value JSConvertPromise::WrapImpl(
    InteropCtx *ctx, napi_env env, EtsPromise *etsVal)
{
    // 1. Identity check — reuse existing JS Promise if already wrapped
    EtsObject *interopObj = etsVal->GetInteropObject(coro);
    if (interopObj != nullptr && storage->HasReference(interopObj, env)) {
        return storage->GetJsObject(interopObj, env);
    }
    // 2. Create JS Promise + napi_deferred
    napi_deferred deferred;
    napi_value jsPromise;
    napi_create_promise(env, &deferred, &jsPromise);

    // 3. Lock + branch: fast path (settled) or slow path (pending)
    hpromise->Lock();
    if (!hpromise->IsPending() && !hpromise->IsLinked()) {
        // FAST PATH: immediately settle JS Promise
        completionValue = refconv->Wrap(ctx, value);
        napi_resolve_deferred(env, deferred, completionValue);
        // or napi_reject_deferred for rejected
    } else {
        // SLOW PATH: connect via PromiseInterop
        hpromise->Unlock();
        PlatformTypes(coro)->interopPromiseInteropConnectPromise
            ->GetPandaMethod()->Invoke(coro, args);
        hpromise->Lock();
    }
    // 4. Create EtsPromiseRef + register mapping
    EtsPromiseRef *ref = EtsPromiseRef::Create(coro);
    ref->SetTarget(coro, hpromise->AsObject());
    hpromise->SetInteropObject(coro, ref);
    storage->CreateETSObjectRef(ctx, refHandle, jsPromise);
    hpromise->Unlock();
    return jsPromise;
}
```

### UnwrapImpl — JS Promise → ETS Promise (JSCONVERT_UNWRAP)

```cpp
// Expanded from JSCONVERT_UNWRAP(Promise) macro
inline std::optional<EtsPromise *> JSConvertPromise::UnwrapImpl(
    InteropCtx *ctx, napi_env env, napi_value jsVal)
{
    // Debug: verify jsVal is actually a Promise
    ASSERT(isPromise);  // only in debug builds

    // 1. Identity check — reuse existing EtsPromise if already unwrapped
    SharedReference *sharedRef = storage->GetReference(env, jsVal);
    if (sharedRef != nullptr) {
        EtsPromiseRef *ref = reinterpret_cast<EtsPromiseRef *>(sharedRef->GetEtsObject());
        return EtsPromise::FromEtsObject(ref->GetTarget(coro));
    }
    // 2. Create proxy EtsPromise (PENDING)
    EtsPromise *promise = EtsPromise::Create(coro);
    // 3. Create EtsPromiseRef bridge
    EtsPromiseRef *href = EtsPromiseRef::Create(coro);
    href->SetTarget(coro, promise->AsObject());
    promise->SetInteropObject(coro, href);
    // 4. Register mapping
    storage->CreateJSObjectRef(ctx, href, jsVal);
    // 5. Mark as proxy
    promise->SetLinkedPromise(coro, href->AsObject());
    // 6. Create bidirectional link (register JS .then callbacks)
    EtsPromise::CreateLink(promise->GetLinkedPromise(coro), promise);
    return promise;
}
```

---

## JsJobQueue Class

**File:** `plugins/ets/runtime/interop_js/js_job_queue.h/.cpp`
**Namespace:** `ark::ets::interop::js`

```cpp
class JsJobQueue : public JobQueue {
public:
    void Post(const std::function<void()> &fn, void *data) override;
    void CreateLink(EtsObject *jsObject, EtsPromise *etsPromise);

private:
    void CreatePromiseLink(EtsObject *jsObject, EtsPromise *etsPromise);
};
```

### CreatePromiseLink Implementation

```cpp
void JsJobQueue::CreatePromiseLink(EtsObject *jsObject, EtsPromise *etsPromise)
{
    // 1. Get original JS Promise from SharedReferenceStorage
    napi_value jsPromise = storage->GetJsObject(jsObject, env);
    // 2. Get JS Promise.then method
    napi_get_named_property(env, jsPromise, "then", &thenFn);
    // 3. Register EtsPromise as GC-safe global reference
    mem::Reference *promiseRef = vm->GetGlobalObjectStorage()->Add(etsPromise, GLOBAL);
    // 4. Create C++ callbacks with EtsPromise bound as data
    napi_create_function(env, nullptr, 0, OnJsPromiseResolved, promiseRef, &thenCallback[0]);
    napi_create_function(env, nullptr, 0, OnJsPromiseRejected, promiseRef, &thenCallback[1]);
    // 5. Register callbacks on JS Promise
    napi_call_function(env, jsPromise, thenFn, 2, thenCallback, &thenResult);
}
```

### Global Callback Functions

```cpp
static napi_value OnJsPromiseResolved(napi_env env, napi_callback_info info);
static napi_value OnJsPromiseRejected(napi_env env, napi_callback_info info);
static napi_value OnJsPromiseCompleted(napi_env env, napi_callback_info info, bool isResolved);
```

---

## Promise Intrinsics (C++)

**File:** `plugins/ets/runtime/intrinsics/std_core_Promise.cpp`
**Namespace:** `ark::ets::intrinsics`

### EtsPromiseResolve

```cpp
void EtsPromiseResolve(EtsPromise *promise, EtsObject *value, EtsBoolean wasLinked);
```

- `wasLinked = false`: Called from `OnJsPromiseCompleted` (JS callback path)
  - Lock → check PENDING → if value is Promise → `SubscribePromiseOnResultObject` (recursive)
  - else → `Resolve()` → Unlock
- `wasLinked = true`: Called from `subscribeOnAnotherPromise` then callback (ETS chain)
  - Lock → check LINKED → if value is Promise → `ChangeStateToPendingFromLinked()` → subscribe
  - else → `Resolve()` → Unlock

### EtsPromiseReject

```cpp
void EtsPromiseReject(EtsPromise *promise, EtsObject *error, EtsBoolean wasLinked);
```

- Uses RAII `EtsMutex::LockHolder` for exception safety
- State check: `wasLinked=false` requires PENDING, `wasLinked=true` requires LINKED

### EtsAwaitPromise

```cpp
EtsObject *EtsAwaitPromise(EtsPromise *promise);
```

- Yields CPU via `coro->GetManager()->Schedule()` before suspending
- Checks `IsCoroutineSwitchDisabled()` — throws if await is forbidden
- `IsProxy()` → `AwaitProxyPromise()`: Wait → check resolved/rejected
- Native ETS → `promise->Wait()` → check resolved/rejected → return or throw

### SubscribePromiseOnResultObject

```cpp
void SubscribePromiseOnResultObject(EtsPromise *outsidePromise, EtsPromise *internalPromise);
```

- Invokes `Promise.subscribeOnAnotherPromise` ETS method
- Handles Promise chaining when resolve value is itself a Promise

### EtsPromiseSubmitCallback

```cpp
void EtsPromiseSubmitCallback(EtsPromise *promise, EtsObject *callback, int32_t workerDomain);
```

- If settled → execute callback immediately
- If pending/linked → add to callbackQueue via `EnsureCapacity()` + `SubmitCallback()`

### EnsureCapacity

```cpp
static void EnsureCapacity(EtsCoroutine *coro, EtsPromise *promise);
```

- Growth strategy: `2 * oldSize + 1`
- Preserves existing callbacks and worker domain assignments

---

## PromiseInterop.ets

**File:** `plugins/ets/stdlib/std/interop/js/PromiseInterop.ets`

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

Called from `JSConvertPromise::WrapImpl()` slow path via:
```cpp
PlatformTypes(coro)->interopPromiseInteropConnectPromise->GetPandaMethod()->Invoke(coro, args);
// args = [EtsPromise*, napi_deferred as int64]
```

---

## SettleJsPromise

**File:** `plugins/ets/runtime/interop_js/intrinsics_api_impl.cpp`
**Namespace:** `ark::ets::interop::js`

```cpp
void SettleJsPromise(EtsObject *value, napi_deferred deferred, EtsInt state);

void PromiseInteropResolve(EtsObject *value, EtsLong deferred) {
    SettleJsPromise(value, reinterpret_cast<napi_deferred>(deferred), EtsPromise::STATE_RESOLVED);
}

void PromiseInteropReject(EtsObject *value, EtsLong deferred) {
    SettleJsPromise(value, reinterpret_cast<napi_deferred>(deferred), EtsPromise::STATE_REJECTED);
}
```

**Constraints:**
- Must execute on main worker thread
- Uses `INTEROP_CODE_SCOPE_ETS_TO_JS` for mode switching
- Converts ETS value to JS value via `JSRefConvertResolve` before settling

---

## Type Routing Functions

**File:** `plugins/ets/runtime/interop_js/call/arg_convertors.h`

### ConvertArgToEts — JS value → ETS value

```cpp
template <typename STORE>
bool ConvertArgToEts(InteropCtx *ctx, ProtoReader &protoReader, STORE store, napi_value jsVal);
```

- Reads type from ProtoReader (compile-time type signature from `.d.ets`)
- Primitives: direct conversion (bool, int, double, string)
- Reference types: delegates to `ConvertRefArgToEts` → `JSRefConvertResolve` → finds `JSConvertPromise` for Promise types

### ConvertArgToJS — ETS value → JS value

```cpp
bool ConvertArgToJS(InteropCtx *ctx, ProtoReader &protoReader, napi_value *jsRes,
                    const std::function<Value()> &readVal);
```

- Primitives: direct wrapping
- Reference types: delegates to `ConvertRefArgToJS` → `JSRefConvertResolve` → finds `JSConvertPromise`

### JSRefConvertResolve

```cpp
template <bool ASSERT_NOT_NULL = false>
JSRefConvert *JSRefConvertResolve(InteropCtx *ctx, Class *klass);
```

- Runtime lookup of the JS converter for a given ETS class
- For `EtsPromise` class → returns `JSConvertPromise` instance
- Returns nullptr if no converter found (triggers error path)

---

## EtsPromise State Machine

```
Create() ──→ STATE_PENDING ──┬── Resolve() ──→ STATE_RESOLVED ──→ [terminal]
                             │
                             ├── Reject() ──→ STATE_REJECTED ──→ [terminal]
                             │
                             ├── CreateLink() ──→ STATE_LINKED
                             │                       │
                             │              resolve via subscribe:
                             │              ChangeStateToPendingFromLinked()
                             │                       │
                             │                       ▼
                             │                 STATE_PENDING ──→ Resolve/Reject
                             │
                             └── SubmitCallback() ──→ (stays PENDING, callback queued)
```

**Key invariant:** A Promise can only be settled (resolved/rejected) once. All settle methods check current state and return early if already settled.
