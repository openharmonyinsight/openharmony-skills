# OpenHarmony Build Commands Reference

Complete reference for building OpenHarmony codebase.

## Build Script Location

Main build script: `OpenHarmony/build.sh`

The script is a symlink to: `build/build_scripts/build.sh`

## Command Structure

```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name <PRODUCT> --build-target <TARGET> --ccache [--fast-rebuild]
```

**Default recommended options**:
- `--export-para PYCACHE_ENABLE:true` - Enable Python bytecode caching
- `--ccache` - Enable compiler cache for faster rebuilds
- `--fast-rebuild` - Skip GN generation (use when no GN files modified)

## Product Names

Commonly used product names:

| Product | Description | Use Case |
|---------|-------------|----------|
| `rk3568` | RK3568 development board | Standard development |
| `ohos-sdk` | OpenHarmony SDK | SDK building |
| `rk3588` | RK3588 development board | High-performance board |

Check available products:
```bash
ls -1 out/
```

## Build Targets

### System-level Targets

| Target | Description |
|--------|-------------|
| `ohos` | Complete OpenHarmony system |
| `image` | System image only |

### Component Targets (ACE Engine)

| Target | Description | Priority |
|--------|-------------|----------|
| `ace_engine` | Complete ACE engine library | - |
| `libace` | Main ACE library | - |
| `libace_engine` | Engine with different JS backends | - |
| `ace_engine_test` | ACE Engine unit tests only | ⭐ **Recommended** |
| `unittest` | All unit tests (full suite) | Slower |
| `benchmark_linux` | Benchmarks for Linux | - |

**Test Target Recommendation**:
- Use **`ace_engine_test`** for ACE Engine development (faster, focused)
- Use **`unittest`** only when full test suite is needed

## Common Build Patterns

### Full System Build

```bash
# Build complete OpenHarmony for rk3568 (recommended)
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache
```

### Component-specific Build

```bash
# Build only ACE engine
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache

# Build specific library
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target libace --ccache
```

### Test Build

**Build ACE Engine tests** (recommended for ACE Engine development):
```bash
# Faster - builds only ACE Engine tests
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine_test --ccache

# With fast rebuild (when only test code changed)
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine_test --ccache --fast-rebuild
```

**Build all unit tests** (full test suite):
```bash
# Slower - builds all unit tests across entire system
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target unittest --ccache

# With fast rebuild
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target unittest --ccache --fast-rebuild
```

**Build benchmarks**:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target benchmark_linux --ccache
```

**Test Target Selection Guide**:
- **ACE Engine development**: Use `ace_engine_test` (faster iteration)
- **Cross-module testing**: Use `unittest` (comprehensive)
- **Performance testing**: Use `benchmark_linux`

### Fast Rebuild (Code-only Changes)

```bash
# Fast rebuild for code changes (skip GN generation)
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache --fast-rebuild

# Fast rebuild for specific component
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache --fast-rebuild
```

**When to use**: Only source files changed, no BUILD.gn modifications

### Clean Build

```bash
# Find OpenHarmony root and clean output before building
find_root() {
    local dir="$(pwd)"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir)"
        [[ "$dir" == "/" ]] && { echo "Error: .gn not found" >&2; return 1; }
    done
    echo "$dir"
}

OH_ROOT=$(find_root)
rm -rf "$OH_ROOT/out/rk3568/"
cd "$OH_ROOT"
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache
```

## Build Options

### Component Options

```bash
# Build with specific component variant
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache
```

### Fast Rebuild Options

```bash
# Fast rebuild - skip GN generation (when no BUILD.gn files changed)
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache --fast-rebuild

# Fast rebuild with specific component
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache --fast-rebuild
```

**When to use `--fast-rebuild`**:
- ✅ Only source code changed (.cpp, .h, .ts, .ets files)
- ✅ No BUILD.gn or *.gni files modified
- ✅ Incremental development iterations
- ✅ Quick compilation during active development

**When NOT to use `--fast-rebuild`**:
- ❌ BUILD.gn files modified
- ❌ New dependencies added
- ❌ Build configuration changed
- ❌ First build or after `rm -rf out/`

**Performance impact**:
- Typical speedup: 30-50% faster
- Skips GN parsing and ninja file generation
- Directly uses existing build.ninja files

### Parallel Build Control

The build system uses Ninja which automatically detects CPU cores for parallel builds.

### Debug vs Release

Build type is controlled by product configuration:
- Debug builds include symbols and debug info
- Release builds are optimized

## Environment Variables

### Prebuild Configuration

```bash
# Set Python path (usually auto-configured)
export PATH=/path/to/openharmony/prebuilts/python/linux-x64/*/bin:$PATH

# Set Node.js path (usually auto-configured)
export PATH=/path/to/node-v14.21.1-linux-x64/bin:$PATH
```

### Build Cache

```bash
# Use ccache for faster rebuilds
./build.sh --product-name rk3568 --ccache
```

## Build Process Flow

### Standard Build (with GN Generation)

1. **Environment Check**
   - Verify bash shell
   - Check Python version
   - Validate Node.js version (must be 14.21.1)

2. **Toolchain Setup**
   - Configure Python environment
   - Setup Node.js and npm
   - Initialize ohpm
   - Install build tools

3. **Dependency Resolution**
   - Download npm packages
   - Resolve ohpm dependencies
   - Prepare build environment

4. **GN Generation** (skipped with `--fast-rebuild`)
   - Parse BUILD.gn files
   - Generate build.ninja files
   - Process dependencies

5. **Build Execution**
   - Run hb (Harmony Build) system
   - Compile source code
   - Link binaries
   - Generate packages

6. **Output Generation**
   - Create output in `out/<product>/`
   - Generate build.log
   - Package artifacts

### Fast Rebuild Process (with `--fast-rebuild`)

1. **Environment Check** ✓
2. **Toolchain Setup** ✓
3. **Dependency Resolution** ✓
4. **GN Generation** ⏭️ **SKIPPED**
5. **Build Execution** ✓
6. **Output Generation** ✓

**Time saved**: GN generation typically takes 20-40% of total build time

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Build successful |
| 1 | Build failed |

## Output Locations

After successful build:

```bash
# Find OpenHarmony root
find_root() {
    local dir="$(pwd)"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir)"
        [[ "$dir" == "/" ]] && { echo "Error: .gn not found" >&2; return 1; }
    done
    echo "$dir"
}

OH_ROOT=$(find_root)
```

```
$OH_ROOT/out/
├── <product-name>/
│   ├── build.log          # Build log
│   ├── packages/          # Built packages
│   ├── libs/              # Compiled libraries
│   └── logs/              # Component logs
└── gen/                   # Generated files
```

## Tips for Efficient Building

1. **Incremental Builds**: The build system supports incremental builds. Only changed components are rebuilt.

2. **Use ccache**: Enables compiler caching for faster rebuilds.

3. **Use fast-rebuild**: When only source code changed (no GN files), use `--fast-rebuild` to skip GN generation:
   ```bash
   ./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache --fast-rebuild
   ```

4. **Monitor Resources**: Full builds can take significant time and CPU. Use `htop` or similar to monitor.

5. **Parallel Builds**: Ninja automatically uses all available CPU cores.

5. **Clean When Necessary**: Only clean (`rm -rf out/<product>/`) when encountering strange build errors.

## Troubleshooting Build Commands

### "command not found: ./build.sh"

Ensure you're in the OpenHarmony root directory (contains `.gn` file).

### "product-name not found"

Check `productdefine/common/products/` for available product names.

### "build-target not found"

Check component BUILD.gn files for valid target names.

### "Node.js version mismatch"

Node.js must be exactly v14.21.1. The build script should auto-configure this.
