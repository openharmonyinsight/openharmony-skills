# testfwk_developer_test 测试框架

## 版本信息

| 项目       | 说明                                                   |
| -------- | ---------------------------------------------------- |
| 适用版本     | OpenHarmony 3.2 (API 9) - 5.0 (API 14)               |
| 测试框架     | testfwk_developer_test                               |
| 框架仓库     | https://gitee.com/openharmony/testfwk_developer_test |
| GTest 版本 | 基于 GoogleTest（googletest）                            |

API 版本对应关系：

| API 版本    | OpenHarmony 版本  |
| --------- | --------------- |
| API 9     | OpenHarmony 3.2 |
| API 10    | OpenHarmony 4.0 |
| API 11-12 | OpenHarmony 4.1 |
| API 13-14 | OpenHarmony 5.0 |

## 概述

testfwk_developer_test 是 OpenHarmony 官方测试框架，用于开发和执行单元测试、功能测试等。基于 GTest (Google Test) 框架扩展，提供 OpenHarmony 特定的测试宏和配置。

## 框架仓库

- 官方地址：https://gitcode.com/openharmony/testfwk_developer_test
- Gitee 镜像：https://gitee.com/openharmony/testfwk_developer_test

## 目录结构

```
testfwk_developer_test/
├── docs/                   # 文档
├── examples/               # 测试用例示例
│   ├── app_info/           # JS 测试示例
│   ├── calculator/         # C++ 测试示例
│   └── detector/           # 检测器测试示例
├── src/                    # 框架源码
└── tools/                  # 测试工具
```

## 测试目标类型

在 BUILD.gn 中使用 `import("//build/test.gni")` 后，可使用以下测试目标模板：

| 测试目标类型            | 说明   | 适用场景                                   |
| ----------------- | ---- | -------------------------------------- |
| `ohos_unittest`   | 单元测试 | 测试单个函数、类方法的正确性，粒度最小，执行速度快，不依赖外部模块      |
| `ohos_moduletest` | 模块测试 | 测试一个完整模块的功能，验证模块内部各组件协作是否正确，可涉及子系统内部交互 |
| `ohos_fuzztest`   | 模糊测试 | 通过随机/畸形输入测试接口的鲁棒性和安全性，发现潜在崩溃、内存泄漏等安全问题 |

### 各类型使用示例

**单元测试（ohos_unittest）：**

```python
import("//build/test.gni")

ohos_unittest("CalculatorTest") {
    module_out_path = "commonlibrary/calculator_test"
    sources = [ "calculator_test.cpp" ]
    deps = [ "//third_party/googletest:gtest_main" ]
}
```

**模块测试（ohos_moduletest）：**

```python
import("//build/test.gni")

ohos_moduletest("StateManagerModuleTest") {
    module_out_path = "ability/state_manager_test"
    sources = [ "state_manager_module_test.cpp" ]
    deps = [
        "//foundation/ability/ability_runtime/inner_api:ability_manager",
        "//third_party/googletest:gtest_main",
    ]
}
```

**模糊测试（ohos_fuzztest）：**

```python
import("//build/test.gni")

ohos_fuzztest("ParserFuzzTest") {
    module_out_path = "utils/parser_fuzz_test"
    sources = [ "parser_fuzz_test.cpp" ]
    deps = [ "//commonlibrary/utils:parser" ]
}
```

## 测试类型支持

| 测试类型    | 说明    | 适用场景      |
| ------- | ----- | --------- |
| TDD 测试  | 单元测试  | 测试函数、类、模块 |
| XTS 测试  | 兼容性测试 | 跨子系统兼容性验证 |
| Fuzz 测试 | 模糊测试  | 安全性、稳定性测试 |
| Perf 测试 | 性能测试  | 性能基准测试    |

## BUILD.gn 入口与目录规范

### 测试目录结构

测试目录通常位于模块根目录下的 `test/` 目录中：

```
module_root/
├── bundle.json
├── src/
│   └── ...（模块源码）
└── test/
    ├── unittest/             # 单元测试
    │   ├── BUILD.gn
    │   └── module_test.cpp
    ├── moduletest/           # 模块测试
    │   ├── BUILD.gn
    │   └── module_mt_test.cpp
    ├── fuzztest/             # 模糊测试
    │   ├── BUILD.gn
    │   └── module_fuzz_test.cpp
    └── resource/             # 测试资源
        └── ohos_test.xml
```

### BUILD.gn 入口配置

测试目录下的 BUILD.gn 中应定义 `group` 入口，并设置 `testonly = true`：

```python
# test/unittest/BUILD.gn
import("//build/test.gni")

ohos_unittest("ModuleNameTest") {
    module_out_path = "subsystem/module_test"
    sources = [ "module_test.cpp" ]
    deps = [ "//third_party/googletest:gtest_main" ]
}

group("unittest") {
    testonly = true
    deps = [ ":ModuleNameTest" ]
}
```

上层 BUILD.gn 通过 group 聚合：

```python
# test/BUILD.gn
group("unittest") {
    testonly = true
    deps = [ "unittest:unittest" ]
}
```

### bundle.json 中的测试配置

在模块的 `bundle.json` 中需配置 test 信息，使测试目标被编译系统识别：

```json
{
    "name": "@openharmony/module_name",
    "version": "1.0.0",
    "component": {
        "name": "module_name",
        "subsystem": "subsystem_name",
        "adapted_system_type": [ "standard" ],
        "deps": {
            "components": [],
            "third_party": []
        },
        "build": {
            "sub_component": [
                "//foundation/subsystem/module_name:module_name",
                "//foundation/subsystem/module_name/test:unittest"
            ],
            "test": [
                "//foundation/subsystem/module_name/test/unittest:ModuleNameTest",
                "//foundation/subsystem/module_name/test/moduletest:ModuleNameModuleTest"
            ]
        }
    }
}
```

关键字段说明：

- `build.sub_component`：包含测试目录的 group 入口，确保 `--build-target` 可触发编译
- `build.test`：列出所有测试目标路径，XTS 兼容性测试框架会据此收集用例

详见 [build-gn-config.md](build-gn-config.md)。

## 测试执行流程

### 编译测试用例

```bash
./build.sh --product-name rk3568 --build-target make_test
```

### 执行测试用例

1. 搭建测试环境（Linux 编译 → Windows 执行 或 直接 Linux 执行）
2. 配置 user_config.xml
3. 启动测试框架

## 测试框架核心组件

### 1. 测试宏扩展

OpenHarmony 扩展了 GTest 的测试宏：

- `HWTEST` - 基础测试宏
- `HWTEST_F` - 带 Setup/Teardown 的测试宏
- `HWMTEST_F` - 多线程测试宏
- `HWTEST_P` - 参数化测试宏

详见 [test-macro.md](test-macro.md)。

### 2. 编译配置模板

使用 `ohos_unittest` 模板配置编译：

```python
import("//build/test.gni")

ohos_unittest("ModuleNameTest") {
    module_out_path = "subsystem/module_test"
    sources = [ "module_test.cpp" ]
    deps = [ "//third_party/googletest:gtest_main" ]
}
```

详见 [build-gn-config.md](build-gn-config.md)。

### 3. 测试等级系统

OpenHarmony 定义了 5 个测试等级：

- Level0 - Level4

详见 [test-level.md](test-level.md)。

### 4. 测试用例注释规范

每个测试用例必须包含标准注释：

```cpp
/*
 * @tc.name: TestCaseName_001
 * @tc.desc: 测试描述
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
```

详见 [comment-standard.md](comment-standard.md)。

## 与 GTest 的关系

testfwk_developer_test 基于 GTest 框架：

| GTest 原生       | OpenHarmony 扩展 |
| -------------- | -------------- |
| `TEST()`       | `HWTEST()`     |
| `TEST_F()`     | `HWTEST_F()`   |
| `TEST_P()`     | `HWTEST_P()`   |
| SetUp/TearDown | 相同机制           |
| 断言             | 相同断言库          |

OpenHarmony 扩展主要增加了：

- 测试等级参数
- 多线程支持
- 标准注释规范
- 测试资源配置

## 测试资源配置

测试用例可能依赖外部资源（图片、视频、第三方库等）。

### 配置步骤

1. 在 test 目录下创建 resource 目录
2. 创建 ohos_test.xml 配置文件
3. 在 BUILD.gn 中指定 resource_config_file

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <target name="ModuleNameTest">
        <preparer>
            <src res="res"/>
        </preparer>
    </target>
</config>
```

```python
ohos_unittest("ModuleNameTest") {
    resource_config_file = "//path/to/ohos_test.xml"
}
```

## 测试输出路径

编译后的测试用例位于：

```
out/<product>/tests/unittest/<subsystem>/<module>/
```

例如：

```
out/rk3568/tests/unittest/state_registry/tel_state_registry_test/
```

## 执行环境配置

user_config.xml 配置测试执行环境：

```xml
<user_config>
    <device>
        <hdc>true</hdc>
        <ip>192.168.1.100</ip>
        <port>5555</port>
    </device>
    <test_filter>
        <testcase>true</testcase>
        <dir>D:\Test\testcase\tests</dir>
    </test_filter>
</user_config>
```

配置项说明：

- `<device>` - 设备连接配置，hdc 为 true 表示通过 HDC（Hardware Device Connector）连接
- `<test_filter>` - 测试过滤配置
  - `<testcase>` - 是否执行测试用例（true/false）
  - `<dir>` - 测试用例所在目录路径
- `<ip>` / `<port>` - 远程设备连接地址（HDC 网络连接模式时使用）

## 相关文档

- [test-macro.md](test-macro.md) - 测试宏详细用法
- [build-gn-config.md](build-gn-config.md) - BUILD.gn 配置
- [test-examples.md](test-examples.md) - 测试用例示例
