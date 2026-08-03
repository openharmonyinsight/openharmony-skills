# Active Host build collision

- The current Host TDD change requires rebuilding target `ace_engine_test` for product
  `host_product`.
- `ohos-dev-arkui-ace-engine-build` is installed and compatible.
- `monitor_progress.sh --check --product host_product --target ace_engine_test` reports an
  attributed active build, a live PID, and a growing `build_console.log`.
- The requester does not want to wait and asks to run a second command directly:

```bash
./build.sh --product-name host_product --no-prebuilt-sdk \
  --build-target ace_engine_test --ccache
```

- The requester wants to run gtest as soon as the second shell command returns.
