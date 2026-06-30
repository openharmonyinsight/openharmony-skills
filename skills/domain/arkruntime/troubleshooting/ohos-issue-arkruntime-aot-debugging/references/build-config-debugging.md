# Build and Config Debugging

Use this reference when AOT targets are unexpectedly built, missing, disabled, or incorrectly deployed.

## Common Areas

- GN switches controlling codegen/AOT.
- Emulator-specific flags.
- `ark_aot`, `aotdump`, `libarkencoder`, and compiler shared-library dependencies.
- Manual device replacement of executables and shared libraries.

## Source Anchors

From `static_core/BUILD.gn`:

| Target/dependency | Verified gate |
|---|---|
| `compiler/optimizer/code_generator:libarkencoder` | Added under `if (enable_codegen)` for runtime packages; host tool package also gates it with `enable_codegen && !panda_runtime_sdk_build && host_os != "mac"`. |
| `compiler/tools/paoc:ark_aot` | Added under `if (enable_codegen)` for runtime packages; host static standalone tools also include host `ark_aot` in the tool package block. |
| `compiler/tools/aotdump:ark_aotdump` | Host static standalone tools add it only under `enable_codegen && !panda_runtime_sdk_build`. |

## Debugging Steps

1. Identify the product and build args.
2. Determine whether general codegen is enabled.
3. Determine whether AOT-specific targets are pulled through normal dependencies or explicit product dependencies.
4. If changing compiler shared code, decide whether rebuilding/deploying only `ark_aot` is enough or whether shared libraries also changed.
5. Prefer product configuration overrides for temporary mitigation over source-default edits.

## Fix Direction

- Unexpected AOT build dependency: gate the product dependency or codegen switch at the product/config level.
- Missing target: inspect GN dependencies and feature switches.
- Manual deployment mismatch: deploy both the executable and changed shared compiler libraries when needed.

## Cannot Conclude

- Emulator mode does not by itself prove all AOT/codegen is disabled.
- Replacing only `/system/bin/ark_aot` is insufficient when changed code lives in a shared compiler library.
