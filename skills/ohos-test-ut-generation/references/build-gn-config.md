# BUILD.gn 决策规则

## 决策总览

编写单测 BUILD.gn 时，按以下顺序决策：

| 决策点 | 决策依据 | 快速判定 |
|--------|----------|----------|
| 测试模板类型 | 测试粒度 | 函数级→`ohos_unittest`，模块级→`ohos_moduletest` |
| deps vs external_deps | 依赖归属 | 同子系统→`deps`，跨子系统→`external_deps` |
| 是否需要 cflags_cc | 访问私有成员 | 测试private/protected→需要 |
| 是否需要 defines | 条件编译 | 源码有`#ifdef TEST`→需要 |
| 是否需要 resource_config_file | 外部资源 | 需推送文件到设备→需要 |
| 是否需要 gmock | Mock使用 | 使用MOCK_METHOD→需要 |

---


## 决策1：测试模板类型

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


## 决策2：deps vs external_deps

### 快速判定

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
| `ipc:ipc_core` | 跨子系统 | **external_deps** |
| `googletest:gmock` | 跨子系统 | **external_deps**（Mock时） |

### 决策示例

```python
# 场景1: 测试 telephony 子系统内模块
deps = [
    "//third_party/googletest:gtest_main",          # 第三方 → deps
    "//base/telephony/core_service:tel_core_api",   # 同子系统 → deps
]
external_deps = [
    "hiviewdfx_hilog_native:libhilog",              # 跨子系统 → external_deps
    "ipc:ipc_core",                                  # 跨子系统 → external_deps
]
# 场景2: 测试 hiviewdfx 子系统内模块
deps = [
    "//third_party/googletest:gtest_main",
    "//base/hiviewdfx/hiview:hiview_core",          # 同子系统 → deps
]
external_deps = [
    "c_utils:utils",                                 # 跨子系统 → external_deps
]
```


---


## 决策3：是否需要 cflags_cc

### 决策条件

```
测试代码是否访问私有成员？
├─ 访问 private 成员变量 → 需要 cflags_cc
├─ 访问 protected 成员变量 → 需要 cflags_cc
├─ 调用 private 方法 → 需要 cflags_cc
└─ 仅访问 public 成员 → 不需要
```


### 配置规则

| 条件 | 配置 |
|------|------|
| 需访问 private/protected | 添加 `cflags_cc = ["-Dprivate=public", "-Dprotected=public"]` |
| 仅 public 接口测试 | 不添加 |

### 示例

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


## 决策4：是否需要 defines

### 决策条件

```
源码中是否有条件编译宏？
├─ 有 #ifdef UNITTEST → 需要 defines
├─ 有 #ifdef TRACE_STRATEGY_UNITTEST → 需要 defines
├─ 有 #ifdef __TEST__ → 需要 defines
└─ 无条件编译保护 → 不需要
```


### 常见 defines 用途

| defines | 用途 | 源码对应 |
|---------|------|----------|
| `UNIT_TEST` | 启用测试辅助函数 | `#ifdef UNIT_TEST` |
| `__UNITTEST__` | 启用测试专用实现 | `#ifdef __UNITTEST__` |
| `TRACE_STRATEGY_UNITTEST` | 启用 Mock注入接口 | `#ifdef TRACE_STRATEGY_UNITTEST` |

### 示例

```cpp
// 源码中被测类
#ifdef TRACE_STRATEGY_UNITTEST
    void SetMockTraceCollector(std::shared_ptr<MockTraceCollector> mock);
#endif
```


```python
# BUILD.gn 中启用
defines = [
    "TRACE_STRATEGY_UNITTEST",
    "__UNITTEST__",
]
```


---


## 决策5：是否需要 resource_config_file

### 决策条件

```
测试是否依赖外部资源文件？
├─ 需读取预置数据文件（JSON/XML/CSV） → 需要
├─ 需特定配置文件 → 需要
├─ 需推送资源到设备 → 需要
└─ 纯代码逻辑测试 → 不需要
```

| 场景 | 是否需要 |
|------|----------|
| 测试解析器读取配置文件 | 需要 |
| 测试算法处理输入数据 | 需要 |
| 测试纯数学计算 | 不需要 |
| 测试字符串处理 | 不需要 |

### 配置示例

```python
# 需要资源文件
ohos_unittest("ParserTest") {
    resource_config_file = "//base/subsystem/module/test/resource/parser/ohos_test.xml"
}
# 不需要资源文件
ohos_unittest("CalculatorTest") {
    # 无 resource_config_file
}
```


---


## 决策6：是否需要 gmock

### 决策条件

```
测试代码是否使用 Mock？
├─ 使用 MOCK_METHOD 宏 → 需要 gmock
├─ 使用 NiceMock/StrictMock → 需要 gmock
├─ 使用 EXPECT_CALL → 需要 gmock
└─ 无 Mock → 不需要
```


### 配置规则

| 条件 | external_deps 配置 |
|------|---------------------|
| 使用 Mock | 添加 `"googletest:gmock"` |
| 不使用 Mock | 不添加 |

### 注意事项

- `gtest_main` 统一放在 `deps` 中（`"//third_party/googletest:gtest_main"`），提供 main 函数入口

- `gmock` 放在 `external_deps` 中（`"googletest:gmock"`），gmock 已包含 gtest 头文件，无需重复添加 `"googletest:gtest"`

- 自定义 main 函数时，不需要 `gtest_main`


```python
# 使用 Mock
deps = [
    "//third_party/googletest:gtest_main",  # main 函数入口（统一放deps）
]
external_deps = [
    "googletest:gmock",       # Mock 支持
]
# 不使用 Mock
deps = [
    "//third_party/googletest:gtest_main",  # main 函数入口（统一放deps）
]
```


---


## 决策7：是否需要 config() 块

### 决策条件

```
include_dirs/cflags 是否需要复用？
├─ 多个测试目标共享相同配置 → 需要 config()
├─ 仅一个测试目标 → 直接写在 ohos_unittest 中
└─ 配置简单（1-2项） → 直接写在 ohos_unittest 中
```


### 选择规则

| 场景 | 推荐 |
|------|------|
| 单测试目标，简单配置 | 直接在 `ohos_unittest` 中写 `include_dirs` |
| 多测试目标，共享配置 | 用 `config()` + `configs` |
| 需要 visibility 控制 | 用 `config()` |

---


## 快速模板

### 最小模板（纯代码逻辑测试）

```python
import("//build/test.gni")
module_output_path = "subsystem/module_test"
ohos_unittest("SimpleTest") {
    module_out_path = module_output_path
    sources = [ "simple_test.cpp" ]
    deps = [ "//third_party/googletest:gtest_main" ]
}
group("unittest") {
    testonly = true
    deps = [ ":SimpleTest" ]
}
```


### 标准模板（带外部依赖）

```python
import("//build/test.gni")
module_output_path = "subsystem/module_test"
ohos_unittest("StandardTest") {
    module_out_path = module_output_path
    sources = [ "standard_test.cpp" ]
    deps = [
        "//third_party/googletest:gtest_main",
        "//base/subsystem/module:module_lib",
    ]
    external_deps = [
        "hiviewdfx_hilog_native:libhilog",
        "c_utils:utils",
    ]
}
group("unittest") {
    testonly = true
    deps = [ ":StandardTest" ]
}
```


### Mock模板（需要gmock）

```python
import("//build/test.gni")
module_output_path = "subsystem/module_test"
ohos_unittest("MockTest") {
    module_out_path = module_output_path
    sources = [
        "mock_test.cpp",
        "mock/mock_service.cpp",
    ]
    deps = [
        "//third_party/googletest:gtest_main",  # 必填：提供main函数入口
    ]
    external_deps = [
        "googletest:gmock",      # 使用Mock时必填
        "hilog:libhilog",
    ]
    defines = [ "__UNITTEST__" ]
}
group("unittest") {
    testonly = true
    deps = [ ":MockTest" ]
}
```


### 访问私有成员模板

```python
import("//build/test.gni")
module_output_path = "subsystem/module_test"
ohos_unittest("PrivateMemberTest") {
    module_out_path = module_output_path
    sources = [ "private_member_test.cpp" ]
    cflags_cc = [
        "-Dprivate=public",
        "-Dprotected=public",
    ]
    deps = [ "//third_party/googletest:gtest_main" ]
}
group("unittest") {
    testonly = true
    deps = [ ":PrivateMemberTest" ]
}
```


### 资源文件模板

```python
import("//build/test.gni")
module_output_path = "subsystem/module_test"
ohos_unittest("ResourceTest") {
    module_out_path = module_output_path
    sources = [ "resource_test.cpp" ]
    deps = [ "//third_party/googletest:gtest_main" ]
    resource_config_file = "//base/subsystem/module/test/resource/module/ohos_test.xml"
}
group("unittest") {
    testonly = true
    deps = [ ":ResourceTest" ]
}
```


### 多配置组合模板（config块）

```python
import("//build/test.gni")
module_output_path = "subsystem/module_test"
config("test_config") {
    visibility = [ ":*" ]
    include_dirs = [
        "//base/subsystem/module/include",
        "mock",
    ]
    defines = [ "__UNITTEST__" ]
}
ohos_unittest("ComplexTest") {
    module_out_path = module_output_path
    configs = [ ":test_config" ]
    sources = [
        "complex_test.cpp",
        "mock/mock_impl.cpp",
    ]
    deps = [
        "//third_party/googletest:gtest_main",
        "//base/subsystem/module:module_lib",
    ]
    external_deps = [
        "googletest:gmock",
        "hilog:libhilog",
    ]
    cflags_cc = [
        "-Dprivate=public",
    ]
}
group("unittest") {
    testonly = true
    deps = [ ":ComplexTest" ]
}
```


---


## 常见错误速查

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `template 'ohos_unittest' not found` | 缺少 import | 第一行添加 `import("//build/test.gni")` |
| `fatal error: xxx.h: No such file` | include_dirs 缺失 | 添加 `include_dirs` 或检查路径 |
| `undefined reference to xxx` | deps 缺失 | 添加缺失的依赖到 `deps` 或 `external_deps` |
| `'xxx' is private` | 访问私有成员 | 添加 `cflags_cc = ["-Dprivate=public"]` |
| `undefined reference to main` | 缺 gtest_main | `deps` 添加 `"//third_party/googletest:gtest_main"` |
| `gtest_main` 链接错误 | gmock 冲突 | `gmock` 已含 gtest，`gtest_main` 需单独添加 |

---


## module_out_path 规则

### 格式

```python
module_output_path = "子系统名/模块名_test"
```


### 示例

| 模块路径 | module_output_path |
|----------|---------------------|
| `base/telephony/core_service` | `"telephony/core_service_test"` |
| `base/hiviewdfx/hiview` | `"hiviewdfx/hiview_test"` |
| `foundation/ability/ability_runtime` | `"ability/ability_runtime_test"` |

### 输出位置

```
out/<product>/tests/unittest/<module_output_path>/TestName
```


---


## 编译命令

```bash
# 编译单个测试
./build.sh --product-name rk3568 --build-target TestName --fast-build
# 编译指定路径
./build.sh --product-name rk3568 --build-target //base/xxx/test/unittest:TestName
# 编译所有测试
./build.sh --product-name rk3568 --build-target make_test
```


---


## 相关文档

- [test-framework.md](test-framework.md) - 测试框架介绍

- [troubleshooting.md](troubleshooting.md) - 编译错误排查
