# Build Cangjie Reference

## Script Arguments

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `--platform` | `linux_x86_64`, `linux_aarch64`, `mac_x86_64`, `mac_aarch64` | auto-detect | Target platform |
| `-t`, `--build-type` | `release`, `relwithdebinfo`, `debug` | `relwithdebinfo` (prompted if interactive) | Build type |
| `--version` | version string | `0.0.1` | Version number |
| `--component` | `all`, `compiler`, `cjc`, `runtime`, `stdlib`, `stdx`, `tools` | `all` | Component to build |
| `--no-tests` | flag | off | Skip unittest compilation (recommended for faster builds) |
| `--incremental` | flag | off | Incremental build with parallel compilation (cjc only) |
| `--verify` | flag | off | Run verification after build |
| `--workspace` | path | auto-detect | Workspace root path (parent of cangjie_compiler) |

## Build Type Details

| Build Type | Optimization | Debug Info | Use Case |
|------------|--------------|------------|----------|
| `release` | Full (-O3) | None | Production builds, performance testing |
| `relwithdebinfo` | Full (-O3) | Yes | Development (default, recommended) |
| `debug` | None (-O0) | Full | Debugging, development |

## Incremental Build

The `--incremental` flag enables fast incremental compilation:
- Only rebuilds changed files
- Uses all available CPU cores (`ninja cjc -j$(nproc)`)
- Requires previous full build
- Only works with `--component cjc`

Example:
```bash
# After making changes to compiler source
python3 build-cangjie.py --incremental --component cjc
```

## Platform Configuration

### linux_x86_64
- Runtime output: `output/common/linux_release_x86_64`
- stdx target: `linux_x86_64_cjnative`
- HLT config: `cangjie2cjnative_linux_x86_test.cfg`
- LLT config: `cjnative_test.cfg`

### linux_aarch64
- Runtime output: `output/common/linux_release_aarch64`
- stdx target: `linux_aarch64_cjnative`
- HLT config: `cangjie2cjnative_linux_arm_test.cfg`
- LLT config: `cjnative_test.cfg`

### mac_x86_64
- Runtime output: `output/common/darwin_release_x86_64`
- stdx target: `darwin_x86_64_cjnative`
- HLT config: `cangjie2cjnative_mac_x86_test.cfg`
- LLT config: `cjnative_test.cfg`

### mac_aarch64
- Runtime output: `output/common/darwin_release_aarch64`
- stdx target: `darwin_aarch64_cjnative`
- HLT config: `cangjie2cjnative_mac_arm_test.cfg`
- LLT config: `cjnative_test.cfg`

## Build Order Dependencies

```
LLVM → Compiler → Runtime → Standard Library → stdx → Tools
```

Each component depends on the previous one being built. The `--component` flag allows building individual components when dependencies are already satisfied.

## Important Notes

- **Standard library build:** The `--target-lib` parameter must be an absolute path, not a relative path
- **Tools dependencies:** cjpm and cjcov depend on stdx, so stdx must be built before tools
- **Tools installation:** All tools are installed to `cangjie_compiler/output/tools/bin/`
- **RPATH:** Tools are built with appropriate RPATH for runtime library location

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CANGJIE_HOME` | Compiler output directory |
| `CANGJIE_STDX_PATH` | Path to stdx static libraries |
| `LD_LIBRARY_PATH` | Must include stdx path for runtime linking |

## Version Format

- Compiler: `1.1.0.beta.999` (dot-separated)
- Runtime: `1.1.0-beta.999` (dash before beta)

The build script handles this conversion automatically.
