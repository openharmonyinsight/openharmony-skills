# ETS Interop Testing Skill Evals

Use `evals.json` as the benchmark seed set for `ohos-test-arkruntime-interop-testing`.

## Coverage

| ID | Scenario Name | Category | Scenario |
|----|---------------|----------|----------|
| 1 | `trigger_create_interop_test` | trigger | Trigger check for interop test case creation and setup |
| 2 | `trigger_cmake_config` | trigger | Trigger check for interop test build configuration |
| 3 | `negative_trigger_java_junit` | negative_trigger | Verify skill does not trigger on standard Java JUnit testing |
| 4 | `negative_trigger_python_pytest` | negative_trigger | Verify skill does not trigger on Python pytest scenarios |
| 5 | `scenario_cmake_macro_setup` | core_scenario | Registering interop test cases with GTest using `panda_ets_interop_js_gtest` CMake macro |
| 6 | `scenario_arktsconfig_paths` | core_scenario | Configuring TS/JS module resolution mapping in `arktsconfig.in.json` |
| 7 | `scenario_cpp_runner_exceptions` | core_scenario | Checking and clearing pending exceptions in the C++ GTest runner via `InteropCtx` |
| 8 | `scenario_ts_ets_dets_naming` | core_scenario | Class definition matching and naming rules across TS, `.d.ets`, and ETS |
