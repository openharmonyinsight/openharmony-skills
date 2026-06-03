# Compile Adaptation Contract

If the build fails because the upstream patch needs ArkWeb branch adaptation,
attempt the smallest in-scope fix before final failure.

A compile fix can intentionally differ from upstream patch text when all are
true:

- upstream security or functional semantics remain landed
- changed files are inside current issue scope
- `compile_fix_required=true`
- `compile_fix_files[]` records every build-fix file
- `local_adaptations[]` records local semantic or API adjustments
- `deviation_reason` explains why exact upstream text changed
- `semantic_equivalence_evidence` explains why the fix remains equivalent
- the rerun build result is recorded

Compile fix files become submit-scope files only through
`compile_fix_files[]` or `local_adaptations[]`. Do not hide a missing upstream
hunk by adding unrelated build fixes.
