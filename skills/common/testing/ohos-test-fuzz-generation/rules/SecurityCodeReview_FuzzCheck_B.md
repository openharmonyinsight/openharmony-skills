# 规则B: BUILD.gn格式规范

**严重程度**: 中危

**问题描述**: FUZZ测试的BUILD.gn文件必须使用正确的模板名称（`ohos_fuzztest()`）、参数格式（`fuzz_config_file`而非`fuzz_config`，路径以`//`开头）和依赖配置（必须包含`group("fuzztest")`部分）。格式不规范会导致编译系统无法正确识别和构建fuzz测试目标。

**核心原则**:
1. 必须使用ohos_fuzztest()模板
2. fuzz_config_file路径必须以//开头
3. 必须包含group("fuzztest")部分

**错误示例**:
```gn
// ❌ 使用错误的模板名和参数
ohos_fuzz_test("AnimationCommand_fuzzer") {
    fuzz_config = "$root_out_dir/fuzztest/AnimationCommand_fuzzer"
    # 缺少 group("fuzztest") 部分
}
```

**正确示例**:
```gn
// ✅ 正确的BUILD.gn格式
// 规则G: ohos_fuzztest 目标名应以 FuzzTest 结尾，驼峰式命名
ohos_fuzztest("AnimationCommandFuzzTest") {
    fuzz_config_file = "//foundation/xxx/xxx/test/fuzztest/AnimationCommand_fuzzer"
    module_out_path = module_output_path
    # ...
}

group("fuzztest") {
    testonly = true
    deps = [":AnimationCommandFuzzTest"]
}
```

**检查方法**:
1. 检查是否使用 `ohos_fuzztest()` 模板（而非 `ohos_fuzz_test()`）
2. 检查参数名是否为 `fuzz_config_file`（而非 `fuzz_config`）
3. 检查 `fuzz_config_file` 路径是否以 `//` 开头
4. 检查是否包含 `group("fuzztest")` 部分
5. 检查 deps 列表中的目标名与 ohos_fuzztest 目标名是否一致

**豁免场景**: 
- 无

---
