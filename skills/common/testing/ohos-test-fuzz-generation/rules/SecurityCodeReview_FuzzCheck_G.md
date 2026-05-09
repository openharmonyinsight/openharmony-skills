# 规则G: BUILD.gn目标名格式

**严重程度**: 中危

**问题描述**: BUILD.gn文件中ohos_fuzztest()的目标名必须使用正确的格式：必须以 `FuzzTest` 结尾，必须为驼峰式命名（不含下划线），格式为`XxxXxxFuzzTest`（驼峰式前缀 + FuzzTest后缀）。由目录名转换而来：去掉 `_fuzzer` 后缀，加上 `FuzzTest` 后缀。例如：`SetScreenInfo_fuzzer` → `SetScreenInfoFuzzTest`，`RSScreenManager_fuzzer1` → `RSScreenManager1FuzzTest`。格式不规范会导致编译系统无法正确识别和构建fuzz测试目标。

**核心原则**:
1. 目标名必须以FuzzTest结尾
2. 目标名必须为驼峰式（不含下划线）
3. group("fuzztest")中的deps必须引用正确的目标名

**错误示例**:
```gn
// ❌ 错误：不以FuzzTest结尾
ohos_fuzztest("SetScreenInfo_fuzzer") {
    ...
}

// ❌ 错误：包含下划线
ohos_fuzztest("Set_Screen_Info_FuzzTest") {
    ...
}

// ❌ 错误：deps未引用目标名
group("fuzztest") {
    deps = [":OtherFuzzTest"]
}
```

**正确示例**:
```gn
// ✅ 正确的目标名格式
ohos_fuzztest("SetScreenInfoFuzzTest") {
    fuzz_config_file = "//foundation/xxx/xxx/test/fuzztest/SetScreenInfo_fuzzer"
    ...
}

group("fuzztest") {
    testonly = true
    deps = [":SetScreenInfoFuzzTest"]
}
```

**检查方法**:
1. 检查ohos_fuzztest()目标名是否以FuzzTest结尾
2. 检查目标名是否为驼峰式（不含下划线）
3. 检查group("fuzztest")中的deps是否引用正确的目标名

**豁免场景**: 
- 无

---
