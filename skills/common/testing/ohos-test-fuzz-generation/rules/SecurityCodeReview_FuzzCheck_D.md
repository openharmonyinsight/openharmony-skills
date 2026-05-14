# 规则D: 命名一致性规范

**严重程度**: 中危

**问题描述**: FUZZ测试的所有文件必须遵循统一的命名规范（`XxxXxx_fuzzer`格式，驼峰式+下划线+fuzzer后缀），目录名、文件名、FUZZ_PROJECT_NAME宏值应保持一致。命名不一致会导致编译失败或fuzz引擎无法正确识别项目。注意：本规则只检查命名一致性，不涉及BUILD.gn中ohos_fuzztest目标名的格式（目标名格式由规则G负责）。

**核心原则**:
1. 目录名、文件名必须一致
2. FUZZ_PROJECT_NAME必须与目录名匹配
3. 多fuzzer使用数字后缀区分

**错误示例**:
```
SetScreenInfo_fuzzer/
├── SetScreenInfo_fuzzer1.cpp    # 错误：文件名与目录名不一致
├── SetScreenInfo_fuzzer.h       # 错误：缺少数字后缀
└── BUILD.gn                     # 目标名格式由规则G检查
```

**正确示例**:
```
SetScreenInfo_fuzzer1/
├── SetScreenInfo_fuzzer1.cpp    # ✅ 与目录名一致
├── SetScreenInfo_fuzzer1.h      # ✅ 与目录名一致
└── BUILD.gn                     # ✅ 目标名格式见规则G
```

**检查方法**:
1. 获取目录名
2. 检查.cpp文件名前缀是否与目录名一致
3. 检查.h文件名前缀是否与目录名一致
4. 检查头文件中FUZZ_PROJECT_NAME值是否与目录名一致
5. 检查命名是否符合 `XxxXxx_fuzzer` 格式（驼峰式+下划线+fuzzer后缀）

**豁免场景**: 
- 无

---
