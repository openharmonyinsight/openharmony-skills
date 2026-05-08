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
