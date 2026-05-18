# 测试用例详细规范

## 概述

本文档定义 OpenHarmony 单元测试用例编写的核心规范，包括代码结构、测试体编写、禁止事项及检查清单。

命名、注释、断言、测试等级等详细规范以索引形式引用独立文档，避免内容重复。

---

## 测试文件标准结构

### HWTEST_F 结构（带 Setup/Teardown）

```cpp
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * ...
 */

#include <gtest/gtest.h>
#include "被测模块头文件.h"

// 1. 测试类定义
class ModuleTest : public testing::Test {
public:
    static void SetUpTestCase();
    static void TearDownTestCase();
    void SetUp();
    void TearDown();

    // 测试辅助成员
};

// 2. SetUpTestCase / TearDownTestCase 实现
void ModuleTest::SetUpTestCase()
{
    // 所有测试前的一次性初始化
}

void ModuleTest::TearDownTestCase()
{
    // 所有测试后的一次性清理
}

// 3. SetUp / TearDown 实现
void ModuleTest::SetUp()
{
    // 每个测试前的初始化
}

void ModuleTest::TearDown()
{
    // 每个测试后的清理
}

// 4. 测试用例
/*
 * @tc.name: FunctionName_001
 * @tc.desc: 测试描述
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(ModuleTest, FunctionName_001, TestSize.Level1)
{
    // Step 1: 准备测试数据
    // Step 2: 调用被测函数
    // Step 3: 验证结果
}
```

### HWTEST 结构（无 Setup/Teardown）

```cpp
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * ...
 */

#include <gtest/gtest.h>

/*
 * @tc.name: SimpleTest_001
 * @tc.desc: 简单功能验证
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST(SimpleTest, SimpleCheck_001, TestSize.Level1)
{
    EXPECT_EQ(1 + 1, 2);
}
```

---

## 测试体三步结构

### 推荐结构

```cpp
HWTEST_F(ModuleTest, FunctionName_001, TestSize.Level1)
{
    // Step 1: 准备测试数据
    int input1 = 10;
    int input2 = 5;
    int expected = 15;

    // Step 2: 调用被测函数
    int result = calculator_->Add(input1, input2);

    // Step 3: 验证结果
    EXPECT_EQ(result, expected);
}
```

### 三步说明

1. **准备数据**：初始化输入、设置状态
2. **调用函数**：执行被测操作
3. **验证结果**：断言验证输出/状态

---

## 索引引用：详细规范

以下内容已拆分为独立文档，请直接查阅：

### 命名规范

详见 [naming-convention.md](naming-convention.md)

涵盖：文件命名、测试套命名、测试用例命名、序号规则等。

### 注释规范

详见 [comment-standard.md](comment-standard.md)

涵盖：文件头版权注释、@tc 注释四项字段、类型编码（FUNC/PERF/RELI/SECU/FUZZ）等。

### 断言规范

详见 [assertion-guide.md](assertion-guide.md)

涵盖：ASSERT vs EXPECT 选择、指针检查、多结果验证等。

### 测试等级

详见 [test-level.md](test-level.md)

涵盖：Level0-Level4 选择标准、等级分配原则等。

### 测试宏详解

详见 [test-macro.md](test-macro.md)

涵盖：HWTEST / HWTEST_F / HWTEST_P 等宏的使用说明。

---

## 使用 gmock 的测试用例规范

### Mock 测试类命名

- 命名规则：`Mock` + 原类名
- 示例：原类 `NetworkService` → Mock 类 `MockNetworkService`

### 文件组织

- Mock 类定义应放在独立的 `mock/` 目录下
- Mock 头文件命名为 `mock_原类名.h`，例如 `mock_network_service.h`

### BUILD.gn 配置

```gn
import("//build/test.gni")

ohos_unittest("ModuleTest") {
    sources = [
        "module_test.cpp",
        "mock/mock_network_service.cpp",  # 包含 mock 的 .cpp 文件
    ]

    include_dirs = [
        "//path/to/mock",
    ]

    external_deps = [
        "googletest:gmock",  # 必须包含 gmock 依赖
    ]

    deps = [
        "//path/to:target_under_test",
    ]
}
```

### 完整示例

```cpp
// mock/mock_network_service.h
#ifndef MOCK_NETWORK_SERVICE_H
#define MOCK_NETWORK_SERVICE_H

#include "network_service.h"
#include <gmock/gmock.h>

class MockNetworkService : public NetworkService {
public:
    MOCK_METHOD(bool, Connect, (const std::string& host), (override));
    MOCK_METHOD(void, Disconnect, (), (override));
    MOCK_METHOD(int, SendData, (const std::vector<uint8_t>& data), (override));
};

#endif  // MOCK_NETWORK_SERVICE_H
```

```cpp
// module_test.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "mock/mock_network_service.h"

using ::testing::Return;
using ::testing::_;

class NetworkClientTest : public testing::Test {
public:
    void SetUp() override
    {
        mockService_ = std::make_unique<MockNetworkService>();
    }

    void TearDown() override
    {
        mockService_.reset();
    }

protected:
    std::unique_ptr<MockNetworkService> mockService_;
};

/*
 * @tc.name: Connect_001
 * @tc.desc: 验证连接成功场景
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(NetworkClientTest, Connect_001, TestSize.Level1)
{
    // Step 1: 设置 mock 期望
    EXPECT_CALL(*mockService_, Connect("127.0.0.1"))
        .Times(1)
        .WillOnce(Return(true));

    // Step 2: 调用被测函数
    bool result = mockService_->Connect("127.0.0.1");

    // Step 3: 验证结果
    EXPECT_TRUE(result);
}
```

### gmock 使用注意事项

- 必须在 `TearDown` 中释放 mock 对象，避免内存泄漏
- `EXPECT_CALL` 必须在调用被测函数之前设置
- 避免在多个测试用例间共享 mock 对象的状态
- 详细用法参见 [gmock-guide.md](gmock-guide.md)

---

## 版本适配说明

### 版本对应关系

| OpenHarmony 版本 | API 版本    | 备注           |
| -------------- | --------- | ------------ |
| OH 3.2         | API 9     | 早期稳定版本       |
| OH 4.0         | API 10    | 新增部分子系统      |
| OH 4.1         | API 11    | 能力增强         |
| OH 5.0         | API 12-14 | 最新版本，API 有扩展 |

### 跨版本兼容性注意事项

1. **API 变化**：不同 API 版本的接口签名、参数可能存在差异。编写测试时应确认目标 API 版本的接口定义。
2. **头文件路径**：部分子系统在不同版本的头文件路径有调整（如 `include/` → `interfaces/inner_api/`），需按目标版本确认。
3. **BUILD.gn 模板**：`ohos_unittest` 等模板在不同版本的 GN 构建系统中可能有参数变化，建议参考对应版本的构建文档。
4. **测试宏**：`HWTEST_F` 等宏从 API 9 起可用，行为一致。但在 API 9 早期版本中，部分 `TestSize.Level` 枚举值可能未完全定义。
5. **gmock 可用性**：`googletest:gmock` 外部依赖从 API 9 起支持，但部分旧版本可能需要手动添加源码编译。
6. **新增特性**：API 12+ 新增了部分异步测试框架能力，如需使用需确认最低支持版本。

### 适配建议

- 优先适配最新稳定版（当前为 API 12-14 / OH 5.0）
- 向下兼容时，在测试文件注释中标注最低支持版本
- 不同版本差异较大的接口，应编写版本条件编译或独立的测试文件

---

## 禁止事项清单

| 禁止项        | 原因     |
| ---------- | ------ |
| 无断言测试      | 无法验证结果 |
| 空测试体       | 无意义    |
| 硬编码路径      | 不可移植   |
| 真实外部依赖     | 测试不稳定  |
| 随机数据       | 结果不可预测 |
| 多个断言验证同一结果 | 掩盖失败信息 |

---

## 检查清单

编写测试用例后逐项检查：

- [ ] 文件命名符合规范（CamelCase，以 Test 结尾）
- [ ] 版权注释完整且年份正确
- [ ] @tc 注释四项完整（name/desc/type/require）
- [ ] 测试等级选择合理
- [ ] 测试用例命名正确（函数名_三位序号）
- [ ] 每个测试至少一个断言
- [ ] SetUp/TearDown 正确实现且资源释放
- [ ] 无硬编码依赖和真实外部服务
- [ ] Mock 对象正确配置和释放（如适用）
- [ ] BUILD.gn 配置正确（sources、deps、external_deps）

---

## 相关文档索引

| 文档                                           | 说明            |
| -------------------------------------------- | ------------- |
| [naming-convention.md](naming-convention.md) | 命名规范          |
| [comment-standard.md](comment-standard.md)   | 注释标准          |
| [test-level.md](test-level.md)               | 测试等级详解        |
| [assertion-guide.md](assertion-guide.md)     | 断言使用指南        |
| [test-macro.md](test-macro.md)               | 测试宏详解         |
| [gmock-guide.md](gmock-guide.md)             | gmock 使用指南    |
| [test-examples.md](test-examples.md)         | 测试用例示例集       |
| [build-gn-config.md](build-gn-config.md)     | BUILD.gn 配置说明 |
| [test-framework.md](test-framework.md)       | 测试框架概述        |
