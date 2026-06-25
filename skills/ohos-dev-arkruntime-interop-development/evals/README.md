# ArkRuntime Interop Development Skill Evals

Use `evals.json` as the benchmark seed set for `ohos-dev-arkruntime-interop-development`.

## Coverage

| ID | Scenario Name | Category | Scenario |
|----|---------------|----------|----------|
| 1 | `trigger_js_convert_unwrap` | trigger | Trigger check for interop value conversion code analysis |
| 2 | `trigger_reference_storage` | trigger | Trigger check for reference storage and GC lifecycle analysis |
| 3 | `negative_trigger_unrelated_rust` | negative_trigger | Verify skill does not trigger on unrelated Rust requests |
| 4 | `negative_trigger_sql` | negative_trigger | Verify skill does not trigger on SQL database queries |
| 5 | `scenario_napi_scope_leak` | core_scenario | Loop-based NAPI local reference exhaustion and handle scope reclamation |
| 6 | `scenario_thread_state_violation` | core_scenario | GC safepoint and thread state transitions using `ScopedManagedState` |
| 7 | `scenario_napi_callback_exception` | core_scenario | Propagating pending ETS exceptions to JS via `ThrowJSError` / `napi_throw` |
| 8 | `scenario_global_ref_gc_safety` | core_scenario | Safe management of `napi_ref` lifecycles on the main worker thread |
