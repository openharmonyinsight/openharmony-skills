# ArkCompiler ets Runtime

This reference provides context for the `ets_runtime`, the default execution engine for eTS (Extended TypeScript) and JavaScript.

## Core Runtime & VM
- `ecmascript/`: Core Runtime & VM
- `ecma_vm.cpp`: Entry point for VM instances.
- `interpreter/`: Bytecode execution (assembly-optimized).
- `compiler/`: AOT and JIT compiler infrastructure (Circuit-based IR).
- `mem/`: Garbage collection and memory management.
- `napi/`: JSNAPI (JavaScript Native API) implementation.
- `builtins/`: ECMAScript standard objects.

## Build and Run
- **Build Target**: `ark_js_host_linux_tools_packages`
- **Execution**: Use `ark_js_vm` to execute `.abc` (Ark Bytecode) files.

## Testing
- **Test Runner**: `test/runtest.py`
- **Unit Tests**: `ecmascript/tests/` and `test/ut/`.
- **Compliance**: `test/run_ts_test262.py`.

## Development
- **Style**: Use `bash code-format.sh` (`format-changed`, `check`, `tidy`).
- **NAPI Usage**: Headers in `ecmascript/napi/include` (e.g., `jsnapi.h`).
- **Memory**: Be mindful of GC safepoints.