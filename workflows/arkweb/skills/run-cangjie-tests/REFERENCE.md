# Run Cangjie Tests Reference

## Script Arguments

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `test_path` | file path | (none) | Path to specific test case |
| `--platform` | `linux_x86_64`, `linux_aarch64`, `mac_x86_64`, `mac_aarch64` | auto-detect | Target platform |
| `--suite` | `hlt`, `llt`, `cjcov` | `hlt` | Test suite to run |
| `-j`, `--parallel` | integer | `20` | Parallel test jobs |
| `--timeout` | seconds | `180` | Timeout per test case |
| `--verbose` | flag | off | Verbose output for all tests |
| `--retry` | integer | `0` | Retry count for failed tests |
| `--fail-exit` | flag | off | Non-zero exit on failure |
| `--debug` | flag | off | Keep only failed test temp files |

## Test Framework Parameters

| Parameter | Description |
|-----------|-------------|
| `--test_cfg <file>` | Test suite config file |
| `--test_list <file1>,<file2>` | Comma-separated test list files |
| `-j <num>` | Parallel execution |
| `--timeout <seconds>` | Per-test timeout |
| `-pFAIL` / `-pPASS` | Print only failed/passed tests |
| `--verbose` | Verbose output for all tests |
| `--fail-verbose` | Verbose output only for failed tests |
| `--retry <num>` | Retry failed tests |
| `--fail_exit` | Non-zero exit code on failure |
| `--debug` | Keep only failed test temp files |
| `--keep_temp` | Keep all test temp files |

## Config Files by Platform

### HLT Configs
| Platform | Config File |
|----------|------------|
| linux_x86_64 | `cangjie2cjnative_linux_x86_test.cfg` |
| linux_aarch64 | `cangjie2cjnative_linux_arm_test.cfg` |
| mac_x86_64 | `cangjie2cjnative_mac_x86_test.cfg` |
| mac_aarch64 | `cangjie2cjnative_mac_arm_test.cfg` |

Variants: append `_O2` for O2 optimization, `_g` for debug.

### LLT Config
- Default: `cangjie_test/testsuites/LLT/configs/cjnative/cjnative_test.cfg`
- cjcov: `cangjie_test/testsuites/LLT/Tools/cjcov/configs/test.cfg`

## Test Case Directives

| Directive | Description |
|-----------|-------------|
| `EXEC` | Execute command (expects exit code 0) |
| `EXEC-NUM` | Execute command (expects exit code NUM) |
| `RUN-EXEC` | Run with configured script |
| `ERRCHECK` | Equivalent to `EXEC-PIPE-1: <cmd> 2>&1 \| compare %f` |
| `DEPENDENCE` | Declare dependency files |
| `ASSERT` | Result verification |

## Built-in Variables

| Variable | Description |
|----------|-------------|
| `%f` | Current file name |
| `%n` | File name without extension |
| `%compiler` | Compiler path (from config) |
| `%output` | Output file name |

## LSP Tests Setup

```bash
cp -r ${CANGJIE_HOME}/modules ${CANGJIE_HOME}/tools/bin
```

Then update `lsp_server` path in `cangjie_test/testsuites/HLT/Tools/cjlsp/lsp_config.txt`.
