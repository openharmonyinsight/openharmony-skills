# No-Finding Template

Use this template when the inspected scope has no confirmed actionable findings. Do not use it until the file coverage and checklist requirements have been satisfied.

## Template

```markdown
No actionable issues found in the inspected scope.

Inspected scope:
- `path/to/file_a`: `reviewed`
- `path/to/file_b`: `mechanical-low-risk`

Key verification performed:
- Followed `caller_or_callee` for `function_or_entrypoint` and verified `contract / state transition / error path`
- Reviewed related test `test_name_or_file` for `changed branch or failure path`

Checklist coverage:
- Verified: `validation`, `error handling`, `contract consistency`, `tests`
- Not fully verified: `runtime behavior under real environment`

Residual risk:
- `brief, concrete limitation or uncertainty`
```

## Required Content

Include all of the following:

- reviewed file statuses
- at least one concrete code path, caller/callee path, or test path that was inspected
- checklist categories that were verified
- any categories or environments that were not verified
- residual risk written as a limitation, not as style commentary

## Bad Examples

Do not write outputs like:

- "LGTM"
- "No issue found"
- "No actionable issues found" with no coverage details
- "Looks good overall" with no evidence
