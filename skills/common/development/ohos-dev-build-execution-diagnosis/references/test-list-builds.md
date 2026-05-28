# Test Target List Builds

Use this reference for "编译测试列表", "按列表编译测试", or building specified tests from `unittest_targets.txt`.

## File Location

The helper searches in this order:

1. `foundation/arkui/ace_engine/unittest_targets.txt`
2. `unittest_targets.txt` in the OpenHarmony root

You can also pass an explicit list path as the third argument.

## File Format

```txt
# comments are ignored
ace_engine_test
adapter/ohos/osal/system_properties_unittest
```

Blank lines and text after `#` are ignored.

## Build Command

```bash
bash <skill-dir>/scripts/build_test_list.sh rk3568 "$OH_ROOT"
bash <skill-dir>/scripts/build_test_list.sh rk3568 "$OH_ROOT" foundation/arkui/ace_engine/unittest_targets.txt
```

The helper builds targets sequentially with `--build-target=<target>` and stops on the first failure.

## Recovery After Failure

1. Read the failing target from the helper output.
2. Inspect the product build log for that failure.
3. Fix the error.
4. Re-run the same helper command, or build the failed target directly:

```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name <product> --build-target=<failed_target> --ccache
```

## Disk Space Recovery

Test artifacts can be large. If the failure is disk pressure, only remove verified test binaries from:

```bash
out/<product>/exe.unstripped/tests/unittest/ace_engine/
```

Rules:

- Track which targets already compiled successfully.
- Delete only files in the directory above.
- Do not delete `out/<product>/libs/`, `out/<product>/packages/`, object files, or build configuration.
- Resume from the first failed target after cleanup.
