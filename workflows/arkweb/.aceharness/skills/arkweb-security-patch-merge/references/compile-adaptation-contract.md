# Compile Adaptation Contract

Compile fixes may make the final local code differ from the upstream patch text. That is allowed only as issue-scoped local adaptation.

Record at least:

```json
{
  "upstream_patch_applied_exactly": false,
  "semantic_landed": true,
  "compile_fix_required": true,
  "compile_fix_files": [],
  "local_adaptations": [],
  "deviation_reason": "",
  "semantic_equivalence_evidence": ""
}
```

This is success only when the original patch security or functional semantics remain landed.

Do not use compile fixes to hide missing upstream patch hunks. If patch semantics are not landed, keep or add a blocker and mark the issue `pending_current_stage` or `terminal_failed`.

Compile-fix files may enter submit scope only through `local_adaptations[]` / `compile_fix_files[]`.
