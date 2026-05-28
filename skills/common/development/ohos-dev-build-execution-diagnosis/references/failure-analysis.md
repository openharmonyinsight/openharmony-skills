# OpenHarmony Build Failure Analysis

Use this reference when a build command exits non-zero or the user asks why a build failed.

## Workflow

1. Identify the exact command, product, and target that failed.
2. Locate the primary log:
   - regular product: `out/<product>/build.log`
   - SDK: `out/sdk/build.log`
   - host product: `out/host/host_product/build.log`
   - independent build: `out/standard/build.log` or relevant `out/standard/` log
3. Search from the end of the log first.
4. Extract the first real compiler/linker/GN/preloader failure, not later cascade messages.
5. Read enough surrounding lines to understand the failing target and source file.
6. Make the smallest source or build-file fix that matches the evidence.
7. Rebuild narrowly when possible, then rerun the user's requested command.

## Useful Commands

```bash
bash <skill-dir>/scripts/resolve_build_log.sh <product> "$OH_ROOT"
bash <skill-dir>/scripts/find_recent_errors.sh <product> "$OH_ROOT"
bash <skill-dir>/scripts/analyze_build_error.sh <product> "$OH_ROOT"
```

Manual fallback:

```bash
grep -i "error:" "$BUILD_LOG" | tail -50
grep -i "fatal" "$BUILD_LOG" | tail -20
grep -B 5 -A 20 "FAILED:" "$BUILD_LOG" | tail -120
```

## Failure Classes

- GN/config failure: inspect `args.gn`, product config, metadata, and generated target graph.
- Compilation failure: inspect the exact source file and include/define flags.
- Link failure: inspect missing symbol owner, target deps, source inclusion, and conditional build flags.
- Preloader/load failure: inspect generated product metadata such as `out/preloader/<product>/parts.json`.
- Packaging failure: inspect package/image stage logs after confirming compilation and link stages passed.

## Rules

- Do not infer from the terminal tail alone when `build.log` exists.
- Do not delete logic just to pass compilation.
- If the failure is due to stale generated output, explain the stale artifact and clean only the required output path.
- If a narrow rebuild passes but the full command fails later, continue from the new failure stage.
