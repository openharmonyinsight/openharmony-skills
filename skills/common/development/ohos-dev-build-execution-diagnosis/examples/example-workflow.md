# Example Workflow

This example is intentionally brief. Runtime agents should use `SKILL.md` first and load references only when needed.

## Product Build Failure

1. Run the user-provided build command from the OpenHarmony root.
2. If it fails, resolve the primary log:

```bash
bash <skill-dir>/scripts/resolve_build_log.sh rk3568 "$OH_ROOT"
```

3. Extract recent errors:

```bash
bash <skill-dir>/scripts/find_recent_errors.sh rk3568 "$OH_ROOT"
bash <skill-dir>/scripts/analyze_build_error.sh rk3568 "$OH_ROOT"
```

4. Read `references/failure-analysis.md`.
5. Fix the first real failure.
6. Rebuild narrowly when possible, then rerun the requested command.

## Independent Build

1. Read `references/independent-build.md`.
2. Verify `hb`:

```bash
command -v hb
```

3. Run the requested build:

```bash
hb build <component-name> -i
hb build <component-name> -t
```

4. Diagnose from `out/standard/`.

## Test Target List

1. Read `references/test-list-builds.md`.
2. Put targets in `foundation/arkui/ace_engine/unittest_targets.txt` or pass an explicit file.
3. Run:

```bash
bash <skill-dir>/scripts/build_test_list.sh rk3568 "$OH_ROOT"
```
