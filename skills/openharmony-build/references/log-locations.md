# OpenHarmony Build Log Locations

Complete guide to finding and understanding build logs.

## ⭐ Primary Build Log (Most Important)

**ALWAYS CHECK THIS FILE FIRST**

### Location

```
out/<product-name>/build.log
```

**Examples**:
- `out/rk3568/build.log` - RK3568 product build log
- `out/ohos-sdk/build.log` - SDK build log

### Why This File is Critical

The primary build log (`out/<product>/build.log`) is the **single most important log file** because it contains:

- **All build stages**: GN generation, Ninja compilation, linking, and packaging
- **All errors and warnings**: Compilation errors, linker errors, dependency issues
- **Complete build context**: Environment setup, configuration, and final status
- **Chronological order**: Build progress from start to finish

**Before checking any other log files, always examine `out/<product>/build.log` first.**

### Contents

The main build log contains:
- Build configuration and environment setup
- GN generation output
- Component build progress
- Compilation warnings and errors
- Linking output
- Final build status (success/failure)

### Size

Build logs can range from a few MB to hundreds of MB depending on:
- Build scope (full system vs component)
- Verbosity level
- Number of warnings/errors

### Quick Commands

```bash
# Check if build succeeded
grep -i "build.*successful" out/<product>/build.log

# Find all errors
grep -i "error:" out/<product>/build.log | tail -50

# Find fatal errors
grep -i "fatal" out/<product>/build.log
```

## Component-Specific Logs

### Location Pattern

```
out/<product>/logs/<component-path>/
```

**Examples**:
- `out/rk3568/logs/arkui/ace_engine/` - ACE Engine logs
- `out/rk3568/logs/third_party/` - Third-party library logs

### Structure

```
out/<product>/logs/
├── foundation/
│   └── arkui/
│       └── ace_engine/
│           ├── .ninja_log
│           └── build.ninja.d
└── third_party/
    └── <library>/
        └── .ninja_log
```

## Ninja Logs

### .ninja_log

**Location**: `out/<product>/.ninja_log`

Binary format log of Ninja build operations. Use `ninja` tool to read:

```bash
# Show recent build operations
ninja -C out/<product> -t query <target>

# Show build timeline
ninja -C out/<product> -t recompact
```

## GN Build Files

### build.ninja.d

**Location**: `out/<product>/build.ninja.d` and component subdirectories

Dependencies file showing GN build configuration.

### args.gn

**Location**: `out/<product>/args.gn`

GN build arguments for current configuration:

```bash
# View build arguments
cat out/<product>/args.gn
```

## Test Logs

### Unit Test Logs

**Location**: `out/<product>/tests/<component>/`

Contains test execution output and results.

**Example**:
```
out/rk3568/tests/ace_engine/unittest/
├── test_results.xml
└── test_output.log
```

### Benchmark Logs

**Location**: `test/benchmark/results/`

Benchmark execution results and performance metrics.

## SDK Build Logs

### Location

```
out/sdk/build.log
```

Contains SDK-specific build output when building `ohos-sdk` target.

## Error-Specific Logs

### Compilation Errors

Found in main build log with context:
```
out/<product>/build.log
```

Search pattern:
```bash
grep -B 5 -A 5 "error:" out/<product>/build.log
```

### Linker Errors

Found in main build log, usually near end of component build:
```
out/<product>/build.log
```

Search pattern:
```bash
grep -B 10 "undefined reference" out/<product>/build.log
```

### Test Failures

In component-specific test logs:
```
out/<product>/tests/<component>/test_results.xml
```

## Temporary Build Files

### Location

```
out/<product>/gen/
out/<product>/obj/
```

Contains generated files and object files during build.

**Note**: Can be safely deleted to force regeneration.

## Log Analysis Commands

### Quick Error Check

```bash
# Show recent errors
grep -i "error:" out/<product>/build.log | tail -20

# Count errors
grep -ci "error:" out/<product>/build.log

# Find fatal errors
grep -i "fatal" out/<product>/build.log
```

### Component-Specific Search

```bash
# Search for specific component in build log
grep -i "ace_engine" out/<product>/build.log

# Find component build start/end
grep -E "Building|Compiling.*ace_engine" out/<product>/build.log
```

### Context Around Errors

```bash
# Show 20 lines before and after error
grep -B 20 -A 20 "error:" out/<product>/build.log

# Find first error and show context
grep -n "error:" out/<product>/build.log | head -1 | \
  cut -d: -f1 | \
  xargs -I {} sed -n '{}-20,{}+20p' out/<product>/build.log
```

### Time-Based Analysis

```bash
# Show build progress timestamps
grep "^\[" out/<product>/build.log | \
  awk '{print $1, $2}' | \
  uniq -c

# Find slow build steps
grep "Built target" out/<product>/build.log | \
  awk '{print $1, $2, $3}'
```

## Log Rotation

Build logs are not automatically rotated. For long-running development:

```bash
# Archive old build log
mv out/<product>/build.log out/<product>/build.log.$(date +%Y%m%d_%H%M%S)

# Compress old logs
gzip out/<product>/build.log.*
```

## Remote Build Logs

For builds executed on remote systems or build farms:

```bash
# Copy log to local machine
scp user@build-server:/path/to/out/<product>/build.log ./

# Stream log in real-time during build
ssh user@build-server "tail -f /path/to/out/<product>/build.log"
```

## Log Monitoring During Build

### Real-time Monitoring

```bash
# Follow build log
tail -f out/<product>/build.log

# Follow and filter errors
tail -f out/<product>/build.log | grep --line-buffered "error:\|fatal"

# Show last 50 lines then follow
tail -50 -f out/<product>/build.log
```

### Progress Monitoring

```bash
# Monitor build progress
watch -n 5 'grep -i "built target\|compiling" out/<product>/build.log | tail -20'

# Count compiled files
watch -n 10 'grep -c "Compiling" out/<product>/build.log'
```

## Log Size Management

Large build logs can consume significant disk space:

```bash
# Check log file size
du -h out/<product>/build.log

# Compress old log
gzip out/<product>/build.log

# Find largest logs
du -h out/*/build.log | sort -h
```

## Special Log Locations

### Preloader Logs

```
out/<product>/preloader/
```

Contains bootstrap and initialization logs.

### Gen Directory

```
out/gen/
```

Contains generated files and intermediate build artifacts.

### Component Build Artifacts

```
out/<product>/packages/<component>/
```

Final build outputs for each component.

## Tips for Log Analysis

1. **⭐ Always check primary build log first**: `out/<product>/build.log` contains all build information
2. **Start from the end**: Most recent errors are at the end of the log
3. **Use context**: Always show lines around errors (grep -B -A)
4. **Search smart**: Use specific patterns ("undefined reference" vs generic "error")
5. **Component focus**: Filter by component to reduce noise
6. **Archive regularly**: Keep old logs for comparison and debugging

## Automated Log Analysis

Use the provided scripts for automated analysis:

```bash
# Comprehensive error analysis
.claude/skills/openharmony-build/scripts/analyze_build_error.sh <product>

# Quick recent error check
.claude/skills/openharmony-build/scripts/find_recent_errors.sh <product>
```
