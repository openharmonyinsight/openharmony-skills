# ohos-dev-build-execution-diagnosis

OpenHarmony build execution and diagnosis skill.

This README is a repository-facing summary. Agents should use `SKILL.md` as the runtime entry point and load references only when the matching scenario requires them.

## Scope

- Full OpenHarmony product builds.
- Targeted component and test builds.
- SDK, host, minimal emulator, and full emulator builds.
- Fast rebuild decisions.
- `hb build` independent component builds.
- Test target-list builds.
- Build failure analysis from primary logs.

## Runtime Entry

Start with:

- `SKILL.md`

Load details on demand:

- `references/build-commands.md`: command matrix and product/target notes.
- `references/log-locations.md`: build output and log paths.
- `references/common-errors.md`: common error classes.
- `references/failure-analysis.md`: structured failure diagnosis.
- `references/independent-build.md`: `hb build` independent-build workflow.
- `references/test-list-builds.md`: `unittest_targets.txt` workflows and disk cleanup rules.

Use scripts for deterministic helper tasks:

- `scripts/resolve_build_log.sh`
- `scripts/analyze_build_error.sh`
- `scripts/find_recent_errors.sh`
- `scripts/check_fast_rebuild.sh`
- `scripts/build_test_list.sh`

## Validation

```bash
bash -n scripts/*.sh
```

Keep `SKILL.md` concise. Put detailed workflows in `references/` and repeatable logic in `scripts/`.
