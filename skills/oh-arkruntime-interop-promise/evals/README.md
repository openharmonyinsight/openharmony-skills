# Interop Promise Skill Evals

Use `evals.json` as the benchmark seed set for `oh-arkruntime-interop-promise`.

## Coverage

| ID | Scenario |
|----|----------|
| 1 | ETS→JS fast path: async returns immediate value, JSCONVERT_WRAP |
| 2 | ETS→JS rejection: Promise.reject, napi_reject_deferred |
| 3 | ETS→JS slow path: setTimeout delayed resolution, connectPromise, SettleJsPromise |
| 4 | JS→ETS unwrap: JSCONVERT_UNWRAP, proxy, CreatePromiseLink, AwaitProxyPromise |
| 5 | Promise.all with multiple interop Promises |
