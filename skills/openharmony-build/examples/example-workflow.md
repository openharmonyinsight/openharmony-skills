# OpenHarmony Build Examples

Practical examples of using the OpenHarmony build skill.

## Example 1: Full System Build (Standard)

**User Request**: "编译 OpenHarmony 完整代码"

**Workflow**:

```bash
# Find OpenHarmony root dynamically
find_root() {
    local dir="$(pwd)"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir)"
        [[ "$dir" == "/" ]] && { echo "Error: .gn not found" >&2; return 1; }
    done
    echo "$dir"
}

# Navigate to OpenHarmony root
cd "$(find_root)"

# Execute full build with cache enabled (standard)
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache
```

# Monitor output
# Build script will show progress
# Wait for completion message
```

**Success Output**:
```
[OHOS INFO] Start building...
...
=====build rk3568 successful=====
```

**Failure Output**:
```
[OHOS ERROR] Build failed
```

**Next Steps for Failure**:
```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)

# IMPORTANT: Always check primary build log first
# The main build log contains ALL build information
grep -i "error:" "$OH_ROOT/out/rk3568/build.log" | tail -50

# Use the analysis script for comprehensive error extraction
"$OH_ROOT/foundation/arkui/ace_engine/.claude/skills/openharmony-build/scripts/analyze_build_error.sh" rk3568

# View specific error with context
grep -B 5 -A 5 "error:" "$OH_ROOT/out/rk3568/build.log" | tail -50
```

## Example 2: Component-Specific Build

**User Request**: "编译 ace_engine 组件"

**Workflow**:

```bash
# Find OpenHarmony root and navigate
find_root() {
    local dir="$(pwd)"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir)"
        [[ "$dir" == "/" ]] && { echo "Error: .gn not found" >&2; return 1; }
    done
    echo "$dir"
}

OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Build ace_engine component with cache
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache

# Check result
if [ $? -eq 0 ]; then
    echo "Build successful"
    ls -la "$OH_ROOT/out/rk3568/packages/arkui/ace_engine/"
else
    echo "Build failed, analyzing logs..."
    "$OH_ROOT/foundation/arkui/ace_engine/.claude/skills/openharmony-build/scripts/analyze_build_error.sh" rk3568
fi
```

## Example 3: Fast Rebuild (Code-only Changes)

**User Request**: "快速编译" or "跳过gn编译"

**Scenario**: Only source code changed, no BUILD.gn modifications

**Workflow**:

```bash
# Find OpenHarmony root and navigate
find_root() {
    local dir="$(pwd)"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir)"
        [[ "$dir" == "/" ]] && { echo "Error: .gn not found" >&2; return 1; }
    done
    echo "$dir"
}

OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Check if fast-rebuild is safe to use
"$OH_ROOT/foundation/arkui/ace_engine/.claude/skills/openharmony-build/scripts/check_fast_rebuild.sh" 30

# If no GN files modified, use fast rebuild
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache --fast-rebuild

# For specific component
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache --fast-rebuild
```

**Benefits**:
- 30-50% faster than standard build
- Skips GN parse and ninja file generation
- Ideal for iterative development

## Example 4: Check Before Fast Rebuild

**Scenario**: Verify if fast-rebuild is safe to use

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Check for GN file modifications in last 30 minutes
"$OH_ROOT/foundation/arkui/ace_engine/.claude/skills/openharmony-build/scripts/check_fast_rebuild.sh" 30

# Check for GN file modifications in last 60 minutes
"$OH_ROOT/foundation/arkui/ace_engine/.claude/skills/openharmony-build/scripts/check_fast_rebuild.sh" 60
```

**Output**:
- If GN files modified → Use standard build
- If no GN files modified → Safe to use `--fast-rebuild`

## Example 5: Build Failure Analysis

**Scenario**: Build failed with compilation error

**Build Log Output**:
```
[ 98% 45231/45989] Compiling src/file.cpp
FAILED: src/file.o
error: 'ClassName' was not declared in this scope
```

**Analysis Steps**:

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)

# Step 1: Check primary build log first (ALWAYS DO THIS)
grep -B 10 -A 10 "error:" "$OH_ROOT/out/rk3568/build.log" | tail -50

# Step 2: Run error analysis script for comprehensive analysis
"$OH_ROOT/foundation/arkui/ace_engine/.claude/skills/openharmony-build/scripts/analyze_build_error.sh" rk3568

# Output will show:
# - Error summary from primary build log
# - File locations
# - Error context
```

**Resolution**:
1. Identify missing include or dependency
2. Add required header file
3. Rebuild

## Example 4: Linker Error Investigation

**Scenario**: Undefined reference error

**Build Log**:
```
ld: error: undefined reference to 'SymbolName'
```

**Analysis**:

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)

# Search for symbol definition
grep -r "SymbolName" --include="*.h" --include="*.cpp" "$OH_ROOT/foundation/arkui/ace_engine/"

# Check library dependencies
grep -r "SymbolName" "$OH_ROOT/out/rk3568/build.log"

# Find which library defines symbol
nm -D "$OH_ROOT/out/rk3568/libs/"*.so | grep SymbolName
```

**Resolution**:
- Add missing library dependency to BUILD.gn
- Ensure component is built before dependent code
- Check linking order

## Example 5: Quick Error Check

**Scenario**: Need to quickly check recent build errors

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)

# Use find_recent_errors script
"$OH_ROOT/foundation/arkui/ace_engine/.claude/skills/openharmony-build/scripts/find_recent_errors.sh" rk3568

# Output shows last 20 error lines
# Useful for monitoring active development
```

## Example 6: Clean Build After Changes

**Scenario**: Made significant changes, need clean rebuild

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Clean output
rm -rf "$OH_ROOT/out/rk3568/"

# Rebuild with cache
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache

# Monitor progress
tail -f "$OH_ROOT/out/rk3568/build.log"
```

## Example 7: Build ACE Engine Tests (Recommended)

**User Request**: "编译 ace_engine 的单元测试" or "编译测试用例"

**Recommended Approach** - Build ACE Engine tests only (faster):

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Build ACE Engine tests with cache (recommended - faster)
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine_test --ccache

# With fast rebuild (when only test code changed)
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine_test --ccache --fast-rebuild

# Check test executables
find "$OH_ROOT/out/rk3568/tests/ace_engine" -name "*test*" -executable

# Run tests (example)
"$OH_ROOT/out/rk3568/tests/ace_engine/unittest/ace_test"
```

**Alternative** - Build all unit tests (slower, comprehensive):

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Build all unit tests (full test suite - slower)
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target unittest --ccache

# Check test executables across entire system
find "$OH_ROOT/out/rk3568/tests" -name "*test*" -executable
```

**Recommendation**: For ACE Engine development, always prefer `ace_engine_test` for faster iteration. Use `unittest` only when full test suite is required.

## Example 8: Investigate Specific Component Failure

**Scenario**: Specific component failing to build

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Search for component in build log
grep -n "marquee" "$OH_ROOT/out/rk3568/build.log" | head -20

# Find error related to component
grep -B 10 "marquee" "$OH_ROOT/out/rk3568/build.log" | grep -A 10 "error:"

# Isolate component build
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache 2>&1 | tee build_output.log
```

## Example 9: Check Build Environment

**Scenario**: Suspect environment issues

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Check Python version
python3 --version

# Check Node.js version
node --version

# Verify build script
ls -la build.sh

# Check for .gn file (OpenHarmony root marker)
ls -la .gn

# Try dry run
./build.sh --help
```

## Example 10: Monitor Build Progress

**Scenario**: Long-running build, want to monitor progress

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Start build in background
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache > build_output.log 2>&1 &

# Monitor progress
tail -f build_output.log

# Or use watch
watch -n 5 "grep -c 'Compiling' '$OH_ROOT/out/rk3568/build.log'"

# Check if still running
ps aux | grep build.sh
```

## Example 11: Compare Build Logs

**Scenario**: Compare successful vs failed build

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Archive successful build log
cp "$OH_ROOT/out/rk3568/build.log" "$OH_ROOT/out/rk3568/build.log.success"

# Make changes and rebuild
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache

# Compare
diff "$OH_ROOT/out/rk3568/build.log.success" "$OH_ROOT/out/rk3568/build.log" | grep "error"

# Find what changed
diff "$OH_ROOT/out/rk3568/build.log.success" "$OH_ROOT/out/rk3568/build.log" | grep "^<" | head -20
```

## Example 12: Build Multiple Products

**Scenario**: Build for different products

```bash
# Find OpenHarmony root
OH_ROOT=$(find_root)
cd "$OH_ROOT"

# Build for rk3568
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache

# Build for ohos-sdk
./build.sh --export-para PYCACHE_ENABLE:true --product-name ohos-sdk --ccache

# Build for rk3588 (if available)
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3588 --ccache

# Check available products
ls -1 "$OH_ROOT/out/"
```

## Example Usage with Claude

When working with Claude, simply ask:

```
"请帮我编译 OpenHarmony 代码"
"编译 ace_engine 组件"
"编译测试用例"
"编译 ace_engine 的测试"
"快速编译测试"
"编译失败了，帮我分析错误"
"查看最近的编译错误"
"检查 rk3568 的编译日志"
```

Claude will:
1. Navigate to correct directory
2. Execute appropriate build command
3. Monitor build output
4. Analyze failures using provided scripts
5. Provide detailed error analysis and suggestions
