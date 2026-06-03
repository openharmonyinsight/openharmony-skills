# Slim Workflow State Policy

This policy applies to `ArkWeb 本地 Issue 分析归档与上游安全补丁自动合入`.

The submit gate is:

1. the given patch semantics are landed in the target git subrepo
2. local build passed, or the build failure is proven unrelated and recorded as
   non-blocking risk

In `编译验证`, patch-related build failures must use `verdict=fail` so the
state machine enters `编译修复`. That `fail` is a routing signal for repair, not
final archive failure. Only unrelated build failures may use
`conditional_pass` to enter risk assessment directly.

Batch stages process active issues together. Ready issues wait while any
`pending_current_stage` issue remains in the same stage. When pending is empty,
all ready issues advance together. `terminal_failed` and `deferred_for_archive`
issues leave active batch and are only reported in archives.

Overlap handling belongs to the merge stage. For duplicate files, choose the
lowest numeric issue id as winner for that file group. Any issue that loses any
overlap group is excluded from active batch for this run.

Manual landing is a normal success path when it is in scope and semantics are
landed. `manual_attempted=true` alone is not success.

In `编译修复`, `conditional_pass` is overloaded and must be disambiguated with
`next_state`: use `next_state=编译修复` while any pending issue remains, and
`next_state=风险评估` only after pending is empty and at least one ready issue
remains.

Do not route verdicts back to `自动合入` after merge has already produced
artifacts. Use `冲突解决`, `编译修复`, `风险评估`, or `结果归档` according to the
workflow transition table.
