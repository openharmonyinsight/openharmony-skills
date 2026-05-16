# BUILD.gn 配置详细说明

## 概述

OpenHarmony 使用 GN (Generate Ninja) 构建系统配置测试用例编译。测试用例使用 `ohos_unittest` 或 `ohos_moduletest` 模板进行配置。

## 基础结构

```python
# Copyright (c) 2024 Huawei Device Co., Ltd.
# ...

import("//build/test.gni")  # 导入测试模板

module_output_path = "subsystem/module_test"  # 输出路径

ohos_unittest("ModuleNameTest") {  # 测试目标名称
    module_out_path = module_output_path
    
    sources = [  # 源文件列表
        "//path/to/source.cpp",
        "module_test.cpp",
    ]
    
    include_dirs = [  # 头文件目录
        "//path/to/include",
    ]
    
    deps = [  # 内部依赖
        "//third_party/googletest:gtest_main",
    ]
    
    external_deps = [  # 外部依赖
        "hiviewdfx_hilog_native:libhilog",
    ]
}

group("unittest") {  # 分组入口
    testonly = true
    deps = [":ModuleNameTest"]
}
```

## 关键配置项

### module_output_path

测试用例输出路径，必填项。

```python
module_output_path = "subsystem_name/module_name"
```

输出目录结构：
```
out/<product>/tests/unittest/<subsystem_name>/<module_name>/
```

### sources

参与编译的源文件列表。

```python
sources = [
    "//base/telephony/state_registry/test/unittest/state_test/state_registry_test.cpp",
    "//base/telephony/core_service/frameworks/native/src/telephony_state_registry_client.cpp",
]

sources += [ "additional_test.cpp" ]  # 追加文件
```

**说明**：
- 测试源文件（*_test.cpp）必须包含
- 被测源文件根据需要包含
- 使用绝对路径（//开头）或相对路径

### include_dirs

头文件包含目录。

```python
include_dirs = [
    "$SOURCE_DIR/interfaces/innerkits/include",
    "$SOURCE_DIR/frameworks/native/include",
]
```

### deps

内部依赖，指向 OpenHarmony 内部编译目标。

```python
deps = [
    "//utils/native/base:utils",
    "//third_party/googletest:gtest_main",
    "//base/subsystem/module:library",
]
```

**格式**：`//路径:目标名`

### external_deps

外部依赖，指向其他子系统/部件。

```python
external_deps = [
    "hiviewdfx_hilog_native:libhilog",  # HiLog 日志库
    "ipc:ipc_core",                      # IPC 核心
    "samgr_standard:samgr_proxy",        # Samgr
]
```

**格式**：`部件名:目标名`

#### 常见 external_deps 值

| 依赖项 | 说明 |
|--------|------|
| `c_utils:utils` | C++ 工具库 |
| `hiviewdfx_hilog_native:libhilog` | HiLog 日志库 |
| `hilog:libhilog` | HiLog 日志库（新格式） |
| `ipc:ipc_core` | IPC 通信核心 |
| `googletest:gtest_main` | GTest 主函数入口 |
| `googletest:gmock` | Google Mock 框架 |

#### gmock 依赖说明

当测试代码中使用 Mock（如 `MOCK_METHOD`、`NiceMock`、`StrictMock` 等）时，需要在 `external_deps` 中添加 `"googletest:gmock"`。

使用 Mock 的完整 external_deps 示例：

```python
external_deps = [
    "c_utils:utils",
    "googletest:gmock",
    "googletest:gtest_main",
    "hilog:libhilog",
]
```

**注意事项**：
- `googletest:gmock` 已包含 gtest，无需重复添加 `googletest:gtest`
- `googletest:gtest_main` 提供 `main()` 函数入口，如果自定义了 main 函数则不需要
- 如果同时使用 gmock 和 gtest_main，两者都需要添加

### defines

宏定义，用于在编译时注入预处理器宏。

```python
defines = [
    "TELEPHONY_LOG_TAG = \"STATE_REGISTRY_TEST\"",
    "LOG_DOMAIN = 0",
]

# 条件宏定义
if ("${product_name}" == "rk3568") {
    defines += [ "TEL_TEST_UNSUPPORT" ]
}
```

#### 条件编译宏

在测试代码中，常通过 `defines` 添加条件编译宏，以便在测试中启用/禁用特定代码路径：

```python
defines = [
    "TRACE_STRATEGY_UNITTEST",
    "__UNITTEST__",
]
```

对应的 C++ 代码中可以使用 `#ifdef` 进行条件编译：

```cpp
#ifdef TRACE_STRATEGY_UNITTEST
    // 仅在单元测试时执行的代码
    void SetMockTraceCollector(std::shared_ptr<MockTraceCollector> mock);
#endif

#ifdef __UNITTEST__
    // 测试专用实现
    bool IsTestMode() { return true; }
#endif
```

**典型用法**：
- 在源码中使用 `#ifdef` 保护测试辅助函数
- 在测试 BUILD.gn 中通过 `defines` 启用这些函数
- 避免测试辅助代码进入正式发布版本

### config() 块

`config()` 用于定义一组编译配置（include_dirs、cflags、defines 等），可被多个目标复用。在 `ohos_unittest` 中通过 `configs` 引用。

**语法**：

```python
config("config_name") {
    visibility = [ ":*" ]  # 限制可见范围，":*" 表示仅当前 BUILD.gn 文件可见
    include_dirs = [
        "path/to/include",
    ]
    cflags = [
        "-Wno-unused-parameter",
    ]
    defines = [
        "UNITTEST",
    ]
}
```

**在 ohos_unittest 中引用**：

```python
ohos_unittest("TestName") {
    configs = [ ":config_name" ]
    # ...
}
```

**真实示例**（来自 hiviewdfx 仓库）：

```python
config("bbox_detector_test_config") {
    visibility = [ ":*" ]
    include_dirs = [
        "../",
        "../include",
        "mock",
        "unittest",
    ]
}

ohos_unittest("BBoxDetectorUnitTest") {
    module_out_path = module_output_path
    configs = [ ":bbox_detector_test_config" ]
    sources = [
        "unittest/bbox_detector_unit_test.cpp",
    ]
    deps = [
        "//third_party/googletest:gtest_main",
    ]
}
```

**config() 的优势**：
- 集中管理编译配置，避免重复
- 多个测试目标可以共享同一组配置
- 通过 `visibility` 控制配置的可见范围

### configs 与 public_configs 的区别

| 属性 | 作用范围 | 说明 |
|------|----------|------|
| `configs` | 仅当前目标 | 定义的配置只作用于当前编译目标本身 |
| `public_configs` | 当前目标 + 依赖它的目标 | 配置会传播到所有依赖此目标的其他目标 |

**configs 示例**：配置仅对当前测试生效：

```python
config("module_private_config") {
    visibility = [ "*" ]
    include_dirs = [ "//path/to/include" ]
}

ohos_unittest("ModuleNameTest") {
    configs = [ ":module_private_config" ]
}
```

**public_configs 示例**：库目标通过 public_configs 将 include 路径传递给依赖它的测试：

```python
# 库的 BUILD.gn
ohos_shared_library("mylib") {
    sources = [ "mylib.cpp" ]
    public_configs = [ ":mylib_public_config" ]  # 传播给依赖方
}

config("mylib_public_config") {
    include_dirs = [ "include" ]  # 依赖 mylib 的目标会自动获得此 include 路径
}
```

```python
# 测试的 BUILD.gn
ohos_unittest("MyLibTest") {
    deps = [ "//path/to:mylib" ]
    # 由于 mylib 使用了 public_configs，此测试自动获得 include 路径
    # 无需在测试中再次指定 include_dirs
}
```

**总结**：
- 在测试 BUILD.gn 中通常使用 `configs` 引入 config() 块
- 在被测库的 BUILD.gn 中使用 `public_configs` 让依赖方自动获得头文件路径等配置
- 如果只给当前目标添加配置，用 `configs`；如果需要传播给依赖方，用 `public_configs`

### 访问私有成员

测试需要访问私有成员时，添加：

```python
cflags = [
    "-Dprivate=public",
    "-Dprotected=public",
]
```

### part_name

部件名称。

```python
part_name = "state_registry"
```

## 资源配置

### resource_config_file

测试依赖外部资源时配置 `resource_config_file`。

```python
ohos_unittest("ModuleNameTest") {
    module_out_path = module_output_path
    resource_config_file = "//system/subsystem/partA/test/resource/calculator/ohos_test.xml"
}
```

#### ohos_test.xml 的作用

`ohos_test.xml` 是测试资源配置文件，用于声明测试过程中需要推送到设备上的资源文件（如配置文件、数据文件、临时文件等）。测试框架在执行测试前会根据此文件自动将资源推送到设备的指定目录。

#### 文件路径格式

```
//<子系统路径>/test/resource/<模块名>/ohos_test.xml
```

实际文件通常位于源码树中：
```
base/subsystem/partA/test/resource/module_name/ohos_test.xml
```

#### ohos_test.xml 文件示例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration ver="2.0">
    <target name="ModuleNameTest">
        <preparer>
            <option name="push" value="test/resource/module_name/test_data.txt -> /data/local/tmp/" src="res"/>
        </preparer>
    </target>
</configuration>
```

#### 何时需要配置

- 测试需要读取预置的数据文件（如 JSON、XML、CSV 等）
- 测试需要特定的配置文件
- 测试需要向设备推送资源才能正常运行

#### 何时不需要配置

- 纯代码逻辑测试，不需要外部文件
- 测试数据在代码中内联生成
- 不依赖设备上的任何资源文件

## 测试类型：ohos_unittest 与 ohos_moduletest

OpenHarmony 提供两种测试模板，适用于不同测试场景：

### ohos_unittest — 单元测试

```python
ohos_unittest("ModuleNameTest") {
    module_out_path = module_output_path
    sources = [ "module_test.cpp" ]
    # ...
}
```

- **定位**：针对单个函数、类或模块的单元测试
- **运行环境**：运行在设备或模拟器上
- **特点**：隔离性高，测试粒度小，执行速度快
- **输出路径**：`out/<product>/tests/unittest/<module_output_path>/`

### ohos_moduletest — 模块测试

```python
ohos_moduletest("ModuleNameTest") {
    module_out_path = module_output_path
    sources = [ "module_test.cpp" ]
    # ...
}
```

- **定位**：针对模块级别的集成测试，验证模块间交互
- **运行环境**：运行在设备或模拟器上，更接近真实运行环境
- **特点**：涉及多模块协作，测试粒度较大，验证模块间接口
- **输出路径**：`out/<product>/tests/moduletest/<module_output_path>/`

### 对比

| 特性 | ohos_unittest | ohos_moduletest |
|------|---------------|-----------------|
| 测试级别 | 函数/类级 | 模块级 |
| 粒度 | 小，聚焦单个单元 | 大，验证模块间交互 |
| 依赖 | 尽量 mock 外部依赖 | 可使用真实依赖 |
| 执行速度 | 快 | 相对较慢 |
| 输出目录 | `tests/unittest/` | `tests/moduletest/` |
| 配置方式 | `import("//build/test.gni")` | `import("//build/test.gni")` |
| group 名称 | `group("unittest")` | `group("moduletest")` |

### 典型目录结构

```
test/
├── unittest/                  # 单元测试
│   ├── BUILD.gn              # 使用 ohos_unittest
│   └── module_test.cpp
└── moduletest/                # 模块测试
    ├── BUILD.gn              # 使用 ohos_moduletest
    └── module_integration_test.cpp
```

## 完整示例

### C++ 测试 BUILD.gn

```python
# Copyright (c) 2024 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# ...

import("//build/test.gni")

module_output_path = "state_registry/tel_state_registry_test"

SOURCE_DIR = "//base/telephony/state_registry"

config("module_private_config") {
    visibility = [ "*" ]
    include_dirs = [
        "$SOURCE_DIR/interfaces/innerkits/notify",
        "$SOURCE_DIR/frameworks/native/observer/include",
        "$SOURCE_DIR/frameworks/native/common/include",
    ]
}

ohos_unittest("tel_state_registry_test") {
    module_out_path = module_output_path
    
    sources = [
        "$SOURCE_DIR/test/unittest/state_test/state_registry_test.cpp",
        "//base/telephony/core_service/frameworks/native/src/telephony_state_registry_client.cpp",
    ]
    
    include_dirs = [
        "$SOURCE_DIR/interfaces/innerkits/notify",
        "$SOURCE_DIR/frameworks/native/observer/include",
    ]
    
    deps = [
        "//utils/native/base:utils",
        "//third_party/googletest:gtest_main",
    ]
    
    external_deps = [
        "core_service:tel_core_service_api",
        "ipc:ipc_core",
        "hiviewdfx_hilog_native:libhilog",
    ]
    
    defines = [
        "TELEPHONY_LOG_TAG = \"STATE_REGISTRY_TEST\"",
    ]
    
    configs = [ ":module_private_config" ]
}

group("unittest") {
    testonly = true
    deps = [":tel_state_registry_test"]
}
```

### 包含 Mock 的测试 BUILD.gn

```python
import("//build/test.gni")

module_output_path = "hiviewdfx/hisysevent_test"

config("sysevent_test_config") {
    visibility = [ ":*" ]
    include_dirs = [
        "../include",
        "mock",
        "unittest",
    ]
}

ohos_unittest("HiSysEventUnitTest") {
    module_out_path = module_output_path
    configs = [ ":sysevent_test_config" ]
    
    sources = [
        "unittest/hisysevent_unit_test.cpp",
        "mock/mock_service.cpp",
    ]
    
    deps = [
        "//third_party/googletest:gtest_main",
    ]
    
    external_deps = [
        "c_utils:utils",
        "googletest:gmock",
        "googletest:gtest_main",
        "hilog:libhilog",
    ]
    
    defines = [
        "TRACE_STRATEGY_UNITTEST",
        "__UNITTEST__",
    ]
}
```

### 访问私有成员配置

```python
ohos_unittest("PrivateMemberTest") {
    module_out_path = module_output_path
    sources = [ "private_member_test.cpp" ]
    
    cflags = [
        "-Dprivate=public",
        "-Dprotected=public",
    ]
    
    deps = [ "//third_party/googletest:gtest_main" ]
}
```

### 带资源文件的测试配置

```python
ohos_unittest("ResourceTest") {
    module_out_path = module_output_path
    sources = [ "resource_test.cpp" ]
    
    deps = [ "//third_party/googletest:gtest_main" ]
    
    # 指定资源配置文件，测试框架会自动推送资源到设备
    resource_config_file = "//base/subsystem/partA/test/resource/module/ohos_test.xml"
}
```

## bundle.json 配置

测试入口需要在部件的 bundle.json 中配置：

```json
{
    "build": {
        "sub_component": [
            "//test/testfwk/developer_test/examples/calculator:calculator"
        ],
        "test": [
            "//test/testfwk/developer_test/examples/calculator/test:unittest"
        ]
    }
}
```

## 编译命令

### 编译单个测试目标

```bash
./build.sh --product-name rk3568 --build-target tel_state_registry_test --fast-rebuild
```

### 编译指定路径目标

```bash
./build.sh --product-name rk3568 --build-target //base/telephony/state_registry/test/unittest/utils:UtilityTest --fast-rebuild
```

### 编译所有测试

```bash
./build.sh --product-name rk3568 --build-target make_test
```

## GN 格式化

修改 BUILD.gn 后需格式化：

```bash
# 使用系统 gn
gn format ./base/xxx/test/unittest/BUILD.gn

# 或使用 OpenHarmony 预置 gn
./prebuilts/build-tools/linux-x86/bin/gn format ./base/xxx/test/unittest/BUILD.gn
```

## 常见问题

### Q: ohos_unittest 和 ohos_executable 区别？

| 模板 | 用途 | 输出 |
|------|------|------|
| `ohos_unittest` | 测试用例 | 测试可执行文件 |
| `ohos_executable` | 普通程序 | 可执行文件 |

ohos_unittest 自动包含测试框架依赖和配置。

### Q: ohos_unittest 和 ohos_moduletest 如何选择？

- **使用 ohos_unittest**：测试单个函数、类方法的正确性，mock 外部依赖，快速验证
- **使用 ohos_moduletest**：验证模块间接口调用、服务间交互、多模块协作场景

两者配置语法完全相同，只需将 `ohos_unittest` 替换为 `ohos_moduletest` 即可。

### Q: 如何判断依赖是 deps 还是 external_deps？

- **deps**: 同一子系统内的依赖，使用 `//路径:目标名` 格式
- **external_deps**: 跨子系统依赖，使用 `部件名:目标名` 格式

### Q: 测试输出文件位置？

```
out/<product>/tests/unittest/<module_output_path>/ModuleNameTest
```

### Q: 何时需要添加 googletest:gmock？

当测试代码中使用了以下功能时需要添加 `"googletest:gmock"` 到 external_deps：
- `MOCK_METHOD` / `MOCK_CONST_METHOD` 等宏
- `NiceMock<>` / `StrictMock<>` 模板
- `EXPECT_CALL` 匹配器
- 自定义 Matcher

### Q: configs 和 public_configs 怎么选？

- 在**测试 BUILD.gn** 中引用 config() 块 → 用 `configs`
- 在**库 BUILD.gn** 中让依赖方自动获得配置 → 用 `public_configs`

## 相关文档

- [test-framework.md](test-framework.md) - 测试框架介绍
- [test-examples.md](test-examples.md) - 测试用例示例
