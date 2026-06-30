# Launch and Arguments Debugging

Use this reference for AOT failures around BundleManager, installd, compiler_service, service-side validation, child compiler launch, and dynamic/static/hybrid parser selection.

## Classify the Phase

1. CLI or framework entry: `bm` / `bundle_tool`, Ability lifecycle, or another caller triggers install, update, query, or AOT-related work.
2. Argument construction: BundleManager or caller builds package/module/path/mode fields.
3. Service validation: compiler_service parses and validates arguments.
4. Child launch: service forks/execs `/system/bin/ark_aot` or `/system/bin/ark_aot_compiler`.
5. Child execution: PAOC or dynamic AOT logs appear.

If service logs do not show a child argv line, assume the child may not have started until proven otherwise.

## Signals

| Signal | Meaning |
|---|---|
| `Parser check validation failed` | compiler_service rejected the request before child compiler execution. Inspect parser selection and args. |
| `Read Int32 failed!` | Treat as a secondary wrapper until service-side status and earlier logs are known. It is not proof of IPC transport corruption. |
| `ERR_AOT_COMPILER_PARAM_FAILED` | Parameter validation or mapping failed. Inspect caller args and service parser. |
| `ERR_AOT_COMPILER_CALL_FAILED` / `CRASH` / `CANCELLED` | Child launch/execution may have occurred; inspect child logs, exit status, and signal mapping. |
| `moduleArkTSMode == dynamic` | Dynamic parser/tool path may be selected even for an app you expected to be static. |
| `/system/bin/ark_aot_compiler` | Dynamic AOT path. |
| `/system/bin/ark_aot` | Static/hybrid PAOC path. |

## Debugging Steps

1. Identify the mode source: app/module metadata, BundleManager mapping, compiler_service args.
2. If the issue is triggered from a command line or app lifecycle path, inspect `bundle_tool` / Ability entry first to confirm which package, user, module, and operation reached BundleManager.
3. Confirm parser choice: dynamic uses the dynamic parser; static/hybrid uses the static path.
4. Confirm ABC path choice: dynamic commonly expects `ets/modules.abc`; static/hybrid commonly expects `ets/modules_static.abc`.
5. Confirm child launch: find argv log, executable path, exit code, and signal mapping.
6. Only then inspect PAOC/compiler internals.

## Fix Direction

- Wrong mode: fix module metadata propagation or BundleManager-to-compiler_service mapping.
- Wrong trigger/caller context: fix `bundle_tool`, Ability runtime, or BundleManager entry handling before changing compiler args.
- Validation failure: fix argument construction, parser validation, path/package consistency, or diagnostics.
- Child crash: keep service wrapper separate from the child's root cause; pivot to startup or PAOC references depending on earliest child log.

## Cannot Conclude

- `Read Int32 failed!` alone does not prove IPC corruption.
- Outer "AOT compiler fail" logs do not identify the root cause.
- A static app-level expectation does not prove the active module used static AOT.
