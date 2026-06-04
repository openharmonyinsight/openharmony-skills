# Batch Build Contract

For `ArkWeb 本地 Issue 分析归档与上游安全补丁自动合入`, active issues are already merged in-place in
the current ArkWeb project. Build verification must not create worktrees or
replay patches.

Rules:

- Execute the configured build once for the active batch unless the workflow
  explicitly gives another command.
- `deferred_for_archive` overlap losers are not compiled, repaired, or
  submitted.
- On build success, mark all active issues `ready_for_next`.
- On build failure, attribute the root cause to an issue only when the failed
  file, target, symbol, or dependency is inside that issue's
  `modified_files[]`, `final_changed_files[]`, `local_adaptations[]`, or
  `compile_fix_files[]`.
- In build verification, attributed patch-related failures must return
  `verdict=fail` and route to `编译修复`. This is not final archive failure; it
  means the repair state must run.
- Failures from environment, resource pressure, LFS/SDK/toolchain setup,
  historical dirty changes, existing main-tree errors, or unrelated files are
  non-blocking build risks.
- Ready issues wait until all pending build repairs are resolved, then advance
  together.
- In build repair, never return `conditional_pass,next_state=编译修复`.
  If a repair diff, changed root cause, changed next error location, or concrete
  retry basis exists, return `pass,next_state=编译验证` so the workflow reruns
  build verification. Use `conditional_pass,next_state=风险评估` only after
  `pending_current_stage` is empty and at least one `ready_for_next` issue
  remains.
