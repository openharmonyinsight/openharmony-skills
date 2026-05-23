# BUILD.gn配置规则（OpenHarmony门禁要求）

---

## 一、决策总览

| 决策点 | 决策依据 | 快速判定 |
|--------|----------|----------|
| 测试模板类型 | 测试粒度 | 函数级→`ohos_unittest`，模块级→`ohos_moduletest` |
| deps vs external_deps | 依赖归属 | 同子系统→`deps`，跨子系统→`external_deps` |
| 是否需要 cflags_cc | 访问私有成员 | 测试private/protected→需要 |
| 是否需要 defines | 条件编译 | 源码有`#ifdef TEST`→需要 |
| 是否需要 gmock | Mock使用 | 使用MOCK_METHOD→需要 |
| 是否需要 resource_config_file | 外部资源 | 需推送文件到设备→需要 |

---

## 二、决策1：测试模板类型

**决策树**：
```
测试目标是什么？
├─ 单个函数/类的正确性 → ohos_unittest
├─ 需要mock外部依赖   → ohos_unittest
├─ 模块间接口调用     → ohos_moduletest
└─ 多模块协作场景     → ohos_moduletest
```

| 场景 | 选择 | 原因 |
|------|------|------|
| 测试`Calculator::Add()` | `ohos_unittest` | 单函数验证 |
| 测试类方法组合逻辑 | `ohos_unittest` | 类级别隔离 |
| 测试服务A调用服务B | `ohos_moduletest` | 模块间交互 |
| 测试完整业务流程 | `ohos_moduletest` | 多模块协作 |

---

## 三、决策2：deps vs external_deps

**快速判定**：
```
依赖目标在哪里？
├─ 同子系统内（路径以 //base/xxx 开头） → deps
│   格式: "//路径:目标名"
│   示例: "//base/telephony/core_service:core_service"
└─ 跨子系统（部件名开头） → external_deps
    格式: "部件名:目标名"
    示例: "hiviewdfx_hilog_native:libhilog"
```

### 典型依赖归属表

| 依赖 | 归属 | 配置项 |
|------|------|--------|
| `//third_party/googletest:gtest_main` | 第三方 | **deps**（必填） |
| `//base/telephony/core_service:tel_core` | 同子系统 | **deps** |
| `hiviewdfx_hilog_native:libhilog` | 跨子系统 | **external_deps** |
| `c_utils:utils` | 跨子系统 | **external_deps** |
| `googletest:gmock` | 跨子系统 | **external_deps**（Mock时） |

### 配置示例

```python
# 测试telephony子系统内模块
deps = [
    "//third_party/googletest:gtest_main",          # 第三方 → deps
    "//base/telephony/core_service:tel_core_api",   # 同子系统 → deps
]
external_deps = [
    "hiviewdfx_hilog_native:libhilog",              # 跨子系统 → external_deps
]

# 测试hiviewdfx子系统内模块
deps = [
    "//third_party/googletest:gtest_main",
    "//base/hiviewdfx/hiview:hiview_core",          # 同子系统 → deps
]
external_deps = [
    "c_utils:utils",                                 # 跨子系统 → external_deps
]
```

---

## 四、决策3：是否需要 cflags_cc

**决策条件**：
```
测试代码是否访问私有成员？
├─ 访问 private 成员变量 → 需要 cflags_cc
├─ 访问 protected 成员变量 → 需要 cflags_cc
├─ 调用 private 方法 → 需要 cflags_cc
└─ 仅访问 public 成员 → 不需要
```

**配置规则**：
| 条件 | 配置 |
|------|------|
| 需访问 private/protected | 添加 `cflags_cc = ["-Dprivate=public", "-Dprotected=public"]` |
| 仅 public 接口测试 | 不添加 |

**示例**：
```python
# 需要访问私有成员
ohos_unittest("PrivateTest") {
    cflags_cc = [
        "-Dprivate=public",
        "-Dprotected=public",
    ]
}

# 仅测试公开接口
ohos_unittest("PublicTest") {
    # 不需要 cflags_cc
}
```

---

## 五、决策4：是否需要 defines

**决策条件**：
```
源码中是否有条件编译宏？
├─ 有 #ifdef UNITTEST → 需要 defines
├─ 有 #ifdef __UNITTEST__ → 需要 defines
└─ 无条件编译保护 → 不需要
```

**常见 defines 用途**：
| defines | 用途 | 源码对应 |
|---------|------|----------|
| `UNIT_TEST` | 启用测试辅助函数 | `#ifdef UNIT_TEST` |
| `__UNITTEST__` | 启用测试专用实现 | `#ifdef __UNITTEST__` |

**示例**：
```python
ohos_unittest("TraceStrategyTest") {
    defines = [
        "TRACE_STRATEGY_UNITTEST",  # 启用Mock注入接口
    ]
}
```

---

## 六、决策5：是否需要 gmock

**判断依据**：
- 使用 `MOCK_METHOD` 宏 → 需要gmock
- 使用 `NiceMock<>`/`StrictMock<>` → 需要gmock
- 使用 `EXPECT_CALL`/`ON_CALL` → 需要gmock

**配置**：
```python
# 使用Mock时必须添加
external_deps = [
    "googletest:gmock",  # 使用Mock时必填
]

# Mock实现文件必须加入sources
sources = [
    "test.cpp",
    "mock/mock_service.cpp",  # Mock实现必须加入
]
```

---

## 七、决策6：是否需要 resource_config_file

**判断依据**：
- 需推送配置文件到设备 → 需要
- 需打包测试数据文件 → 需要
- 无外部资源依赖 → 不需要

**配置**：
```python
ohos_unittest("TraceTest") {
    resource_config_file = "$hiview_framework/.../ohos_test.xml"
}
```

---

## 八、完整BUILD.gn模板

```python
import("//build/test.gni")  # 第一行必须import

module_output_path = "subsystem/module_test"  # 格式：子系统/模块

config("test_config") {
    visibility = [ ":*" ]  # 仅本BUILD.gn可见
    include_dirs = [
        "//base/xxx/include",
        "//base/xxx/core",
    ]
}

ohos_unittest("ModuleUnitTest") {
    module_out_path = module_output_path
    
    sources = [
        "unittest/module_test.cpp",
        "mock/mock_service.cpp",  # Mock文件（如需要）
    ]
    
    configs = [ ":test_config" ]
    
    deps = [
        "//third_party/googletest:gtest_main",  # 必填
        "//base/xxx:module",  # 被测模块（同子系统）
    ]
    
    external_deps = [
        "googletest:gmock",  # 使用Mock时必填
        "hilog:libhilog",  # 跨子系统依赖
    ]
    
    cflags_cc = [
        "-Dprivate=public",  # 测试私有成员时必填
        "-Dprotected=public",
    ]
    
    defines = [
        "UNIT_TEST",  # 条件编译宏
    ]
}

group("unittest") {
    testonly = true
    deps = [":ModuleUnitTest"]
}
```

---

## 九、常见配置错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `template 'ohos_unittest' not found` | 缺少import | 第一行添加 `import("//build/test.gni")` |
| `undefined reference to main` | 缺少gtest_main | deps添加 `//third_party/googletest:gtest_main` |
| `'xxx' is private` | 访问控制 | 添加 `cflags_cc: ["-Dprivate=public"]` |
| `undefined reference to MockClass` | Mock cpp未加入sources | sources添加 `mock/mock_service.cpp` |

---

## 相关文档

- [framework-quickref.md](framework-quickref.md) - 测试框架速查表
- [error-matrix.md](error-matrix.md) - 错误排查矩阵
- [assertion-gmock-guide.md](assertion-gmock-guide.md) - Mock配置详情