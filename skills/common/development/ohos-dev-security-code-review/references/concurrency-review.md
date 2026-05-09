# Concurrency Review

## Expert Checks

Concurrency findings need a reachable interleaving, not just a member variable. Start by proving how two paths can run at the same time: IPC calls, callbacks, death recipients, timers, work queues, async lambdas, or cross-SA notifications.

Review shared state in this order:
1. Identify mutable member/global/static state reachable from more than one thread or callback.
2. Confirm all reads and writes use the same lock or equivalent ownership model.
3. Check container operations: `push_back`, `insert`, `erase`, `operator[]`, `at`, iteration, and clear/destruction.
4. Check lock order when multiple locks are acquired.
5. Check whether a lock is held while calling external code that may call back or acquire another lock.
6. Check TOCTOU: state check and dependent action must remain atomic or revalidated.

## OpenHarmony Execution-Model Gate

Before reporting a race, identify the execution model. EventRunner/EventHandler, JS runtime loops, and worker queues can make code thread-confined, but only when all accesses to the state are posted to the same runner or protected by the same owner. IPC callbacks, death recipients, timers, native threads, async `SendRequest`, NAPI threadsafe functions, and cross-SA notifications can break that assumption.

Do not clear a finding with "single-threaded" unless the code or project documentation shows the exact state is accessed only on that event loop.

## Callback And Environment Cleanup

For callback managers, death recipients, and native async bridges, check the lifecycle as part of concurrency review:
- register and unregister paths use the same lock/owner;
- remote death removes stored callbacks and associated state;
- async tasks do not dereference service, callback, or environment objects after teardown;
- reference counts or acquire/release pairs are balanced on normal, error, and shutdown paths;
- locks are not held while invoking remote callbacks that can re-enter the service.

## High-Risk Patterns

```cpp
// VULNERABLE: write is protected, read is not
void Update(int key, const Data &data)
{
    std::lock_guard<std::mutex> lock(mutex_);
    dataMap_[key] = data;
}

Data Lookup(int key)
{
    return dataMap_[key];
}
```

```cpp
// REQUIRED: same state, same lock discipline
Data Lookup(int key)
{
    std::lock_guard<std::mutex> lock(mutex_);
    auto it = dataMap_.find(key);
    return it == dataMap_.end() ? Data{} : it->second;
}
```

## False-Positive Filter

Do not file a race finding if the state is provably thread-confined, initialized before publication and never mutated, protected by a verified higher-level lock, or only accessed on a documented single event loop. Say what evidence would change that conclusion.
