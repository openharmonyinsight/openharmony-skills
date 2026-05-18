# gmock 使用指南

## 概述

Google Mock (gmock) 是 Google 提供的 C++ Mock 框架，用于在单元测试中模拟依赖对象的行为。OpenHarmony 测试框架支持使用 gmock 进行依赖隔离。

## BUILD.gn 集成

在 OpenHarmony 中使用 gmock 需要在 BUILD.gn 中正确配置依赖。

### 添加 gmock 依赖

在测试目标的 `external_deps` 中添加 `googletest:gmock`：

```gn
ohos_unittest("BBoxDetectorUnitTest") {
  sources = [
    "unittest/bbox_detector_unit_test.cpp",
    "mock/bbox_detectors_mock.cpp",
    "mock/hisysevent_util_mock.cpp",
  ]
  external_deps = [
    "googletest:gmock",
    "googletest:gtest_main",
    "hilog:libhilog",
    "c_utils:utils",
  ]
}
```

### 关键配置说明

| 配置项                                            | 说明                       |
| ---------------------------------------------- | ------------------------ |
| `external_deps += [ "googletest:gmock" ]`      | 引入 gmock 库               |
| `external_deps += [ "googletest:gtest_main" ]` | 引入 gtest 主函数（含 gmock）    |
| `sources` 中包含 `mock/*.cpp`                     | Mock 实现文件必须加入编译          |
| `include_dirs` 中包含 `mock/`                     | 如果 Mock 头文件在单独目录，需添加包含路径 |

> **注意**：Mock 的 `.cpp` 文件必须加入 BUILD.gn 的 `sources`，否则链接时会报未定义引用。

## 为什么需要 Mock

### 测试隔离需求

- 依赖外部服务（数据库、网络）
- 依赖复杂组件（配置系统、日志系统）
- 依赖未实现接口
- 需要控制依赖行为

### Mock 的作用

- 隔离被测单元，只测试目标逻辑
- 控制依赖对象的行为
- 验证与依赖的交互
- 避免外部依赖影响测试稳定性

## gmock 基础

### Mock 类定义

```cpp
#include <gmock/gmock.h>

// 原始接口
class IDatabase {
public:
    virtual ~IDatabase() = default;
    virtual bool Connect(const std::string& url) = 0;
    virtual std::string Query(const std::string& sql) = 0;
    virtual void Disconnect() = 0;
};

// Mock 类
class MockDatabase : public IDatabase {
public:
    MOCK_METHOD(bool, Connect, (const std::string& url), (override));
    MOCK_METHOD(std::string, Query, (const std::string& sql), (override));
    MOCK_METHOD(void, Disconnect, (), (override));
};
```

### MOCK_METHOD 宏

**格式**：

```cpp
MOCK_METHOD(return_type, method_name, (params), (specs));
```

| 参数          | 说明     |
| ----------- | ------ |
| return_type | 返回类型   |
| method_name | 方法名称   |
| (params)    | 参数类型列表 |
| (specs)     | 可选修饰符  |

**specs 可选值**：

| 修饰符        | 说明          |
| ---------- | ----------- |
| (override) | 重写虚函数       |
| (const)    | const 方法    |
| (noexcept) | noexcept 方法 |

### 旧版 MOCK_METHODn 宏（兼容说明）

gmock 早期版本使用 `MOCK_METHODN` 系列宏（N 表示参数个数），OpenHarmony 代码库中两种风格都存在：

**旧语法**：`MOCK_METHODN(method_name, return_type(params))`

```cpp
// 旧版：参数数量编码在宏名中
MOCK_METHOD0(GetSharedWorkLoop, std::shared_ptr<EventLoop>());
MOCK_METHOD1(Connect, bool(const std::string& url));
MOCK_METHOD2(SaveData, bool(int id, const std::string& data));
```

**新语法**（推荐）：`MOCK_METHOD(return_type, method_name, (params), (specs))`

```cpp
// 新版：参数数量自动推导
MOCK_METHOD(std::shared_ptr<EventLoop>, GetSharedWorkLoop, (), (override));
MOCK_METHOD(bool, Connect, (const std::string& url), (override));
MOCK_METHOD(bool, SaveData, (int id, const std::string& data), (override));
```

> **建议**：新代码统一使用 `MOCK_METHOD` 新语法，阅读或维护旧代码时注意识别 `MOCK_METHOD0/1/2...`。

### Mock 多种方法签名

```cpp
// 无参数方法
MOCK_METHOD(void, Reset, (), (override));

// 多参数方法
MOCK_METHOD(int, Calculate, (int a, int b), (override));

// const 方法
MOCK_METHOD(std::string, GetName, (), (const, override));

// 返回指针
MOCK_METHOD(Object*, GetObject, (int id), (override));
```

## 设定 Mock 行为

### ON_CALL - 默认行为

设定 Mock 对象的默认行为：

```cpp
MockDatabase mockDb;

// 设定默认行为
ON_CALL(mockDb, Connect).WillByDefault(Return(true));
ON_CALL(mockDb, Query).WillByDefault(Return("result"));
```

### EXPECT_CALL - 预期调用

设定预期调用次数和行为：

```cpp
MockDatabase mockDb;

// 预期调用一次，返回 true
EXPECT_CALL(mockDb, Connect("test_url"))
    .Times(1)
    .WillOnce(Return(true));

// 预期不调用
EXPECT_CALL(mockDb, Disconnect())
    .Times(0);
```

### 常用行为设定器

| 设定器                       | 说明     |
| ------------------------- | ------ |
| `Return(value)`           | 返回固定值  |
| `ReturnRef(variable)`     | 返回引用   |
| `ReturnNull()`            | 返回空指针  |
| `Invoke(func)`            | 调用函数   |
| `InvokeWithoutArgs(func)` | 调用无参函数 |
| `DoDefault()`             | 执行默认行为 |

### 行为设定示例

```cpp
// 返回固定值
EXPECT_CALL(mockDb, Connect(_))
    .WillOnce(Return(true));

// 多次返回不同值
EXPECT_CALL(mockDb, Query(_))
    .WillOnce(Return("result1"))
    .WillOnce(Return("result2"))
    .WillRepeatedly(Return("default"));

// 调用实际函数
EXPECT_CALL(mockDb, Query(_))
    .WillOnce(Invoke([](const std::string& sql) {
        return "processed: " + sql;
    }));

// 返回引用
std::string buffer = "buffer";
EXPECT_CALL(mockDb, GetBuffer())
    .WillRepeatedly(ReturnRef(buffer));
```

## 调用次数匹配

### Times 匹配器

| 匹配器                    | 说明       |
| ---------------------- | -------- |
| `Times(n)`             | 精确调用 n 次 |
| `Times(AtLeast(n))`    | 至少调用 n 次 |
| `Times(AtMost(n))`     | 至多调用 n 次 |
| `Times(Between(m, n))` | 调用 m-n 次 |
| `Times(AnyNumber())`   | 任意次数     |

### 示例

```cpp
// 精确调用一次
EXPECT_CALL(mockDb, Connect(_))
    .Times(1);

// 至少调用一次
EXPECT_CALL(mockDb, Query(_))
    .Times(AtLeast(1));

// 任意次数（不关心次数）
EXPECT_CALL(mockDb, Log(_))
    .Times(AnyNumber());

// 调用范围
EXPECT_CALL(mockDb, Process(_))
    .Times(Between(1, 3));
```

## 参数匹配器

### 常用匹配器

| 匹配器                  | 说明         |
| -------------------- | ---------- |
| `_`                  | 匹配任意值      |
| `Eq(value)`          | 等于指定值      |
| `Ne(value)`          | 不等于指定值     |
| `Gt(value)`          | 大于指定值      |
| `Lt(value)`          | 小于指定值      |
| `Ge(value)`          | 大于等于       |
| `Le(value)`          | 小于等于       |
| `StrEq(str)`         | 字符串相等      |
| `StrNe(str)`         | 字符串不等      |
| `IsNull()`           | 为空指针       |
| `NotNull()`          | 非空指针       |
| `IsEmpty()`          | 为空（容器/字符串） |
| `StartsWith(prefix)` | 以指定前缀开头    |
| `EndsWith(suffix)`   | 以指定后缀结尾    |
| `Contains(str)`      | 包含指定字符串    |

### 示例

```cpp
// 匹配任意参数
EXPECT_CALL(mockDb, Connect(_));

// 匹配特定值
EXPECT_CALL(mockDb, Connect("test_url"));

// 匹配数值条件
EXPECT_CALL(mockDb, GetRecord(Gt(0)));

// 匹配字符串条件
EXPECT_CALL(mockLogger, Log(StartsWith("ERROR")));

// 匹配空指针
EXPECT_CALL(mockValidator, Validate(IsNull()))
    .WillOnce(Return(false));

// 匹配非空指针
EXPECT_CALL(mockValidator, Validate(NotNull()))
    .WillOnce(Return(true));
```

### 自定义匹配器

```cpp
using ::testing::Matcher;
using ::testing::MakeMatcher;
using ::testing::MatcherInterface;

// 自定义匹配器：验证数值在范围内
MATCHER_P(InRange, range, "") {
    return arg >= range.first && arg <= range.second;
}

// 使用自定义匹配器
EXPECT_CALL(mockDb, GetId(InRange(std::make_pair(1, 100))));
```

## 完整测试示例

### 使用 Mock 的测试类

```cpp
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * ...
 */

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "data_processor.h"

// Mock 依赖接口
class MockDatabase : public IDatabase {
public:
    MOCK_METHOD(bool, Connect, (const std::string& url), (override));
    MOCK_METHOD(std::string, GetData, (int id), (override));
    MOCK_METHOD(bool, SaveData, (int id, const std::string& data), (override));
};

class MockLogger : public ILogger {
public:
    MOCK_METHOD(void, Log, (const std::string& message), (override));
};

class DataProcessorTest : public testing::Test {
public:
    static void SetUpTestCase();
    static void TearDownTestCase();
    void SetUp();
    void TearDown();

    MockDatabase mockDb;
    MockLogger mockLogger;
    DataProcessor* processor_;
};

void DataProcessorTest::SetUpTestCase()
{
    GTEST_LOG_(INFO) << "DataProcessorTest SetUpTestCase";
}

void DataProcessorTest::TearDownTestCase()
{
    GTEST_LOG_(INFO) << "DataProcessorTest TearDownTestCase";
}

void DataProcessorTest::SetUp()
{
    // 使用 Mock 对象创建处理器
    processor_ = new DataProcessor(&mockDb, &mockLogger);

    // 设定默认行为
    ON_CALL(mockDb, Connect(_)).WillByDefault(Return(true));
    ON_CALL(mockLogger, Log(_)).WillByDefault(Return());
}

void DataProcessorTest::TearDown()
{
    delete processor_;
    processor_ = nullptr;
}

/*
 * @tc.name: ProcessData_001
 * @tc.desc: 验证数据处理成功场景
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(DataProcessorTest, ProcessData_001, TestSize.Level1)
{
    // 设定预期行为
    EXPECT_CALL(mockDb, Connect("default_url"))
        .Times(1)
        .WillOnce(Return(true));

    EXPECT_CALL(mockDb, GetData(100))
        .Times(1)
        .WillOnce(Return("test_data"));

    EXPECT_CALL(mockDb, SaveData(100, "processed_test_data"))
        .Times(1)
        .WillOnce(Return(true));

    EXPECT_CALL(mockLogger, Log(_))
        .Times(AnyNumber());  // 不关心日志次数

    // 执行测试
    bool result = processor_->Process(100);
    EXPECT_TRUE(result);
}

/*
 * @tc.name: ProcessData_002
 * @tc.desc: 验证数据库连接失败场景
 * @tc.type: FUNC
 * @tc.require: issueI56WJ7
 */
HWTEST_F(DataProcessorTest, ProcessData_002, TestSize.Level2)
{
    EXPECT_CALL(mockDb, Connect(_))
        .Times(1)
        .WillOnce(Return(false));

    // 连接失败后不应调用其他方法
    EXPECT_CALL(mockDb, GetData(_))
        .Times(0);
    EXPECT_CALL(mockDb, SaveData(_, _))
        .Times(0);

    bool result = processor_->Process(100);
    EXPECT_FALSE(result);
}
```

## 真实 Mock 示例（hiviewdfx 仓库）

以下示例来自 OpenHarmony hiviewdfx 仓库，展示了实际项目中 Mock 的使用方式。

### Mock 类定义示例

```cpp
#include <gmock/gmock.h>
#include "hiview_context.h"
#include "event_loop.h"

// Mock HiviewContext：继承真实类并 Mock 虚方法
class MockHiviewContext : public HiviewContext {
public:
    MOCK_METHOD0(GetSharedWorkLoop, std::shared_ptr<EventLoop>());
};

// Mock EventLoop：Mock 事件循环接口
class MockEventLoop : public EventLoop {
public:
    MOCK_METHOD1(AddFileDescriptorEvent, void(FileDescriptorEvent* event));
    MOCK_METHOD1(RemoveFileDescriptorEvent, void(FileDescriptorEvent* event));
    MOCK_METHOD0(Run, void());
};
```

### 单例 Mock 模式

当被测代码通过静态单例访问依赖时（如 `HisyseventUtil::GetInstance()`），需要特殊的 Mock 模式：

```cpp
// mock_hisysevent_util.h

class MockHisyseventUtil {
public:
    static MockHisyseventUtil& GetInstance();

    // Mock 需要拦截的方法
    MOCK_METHOD0(IsEventProcessed, bool());

private:
    MockHisyseventUtil() = default;
    ~MockHisyseventUtil() = default;
    MockHisyseventUtil& operator=(const MockHisyseventUtil&) = delete;
    MockHisyseventUtil(const MockHisyseventUtil&) = delete;
};
```

```cpp
// mock_hisysevent_util.cpp

MockHisyseventUtil& MockHisyseventUtil::GetInstance()
{
    static MockHisyseventUtil instance;
    return instance;
}
```

使用单例 Mock 的测试示例：

```cpp
class BBoxDetectorUnitTest : public testing::Test {
public:
    void SetUp() override
    {
        // 通过单例获取 Mock 对象，设定预期行为
        auto& mockUtil = MockHisyseventUtil::GetInstance();
        ON_CALL(mockUtil, IsEventProcessed).WillByDefault(Return(false));
    }

    void TearDown() override
    {
        // 验证预期并清理
        auto& mockUtil = MockHisyseventUtil::GetInstance();
        ASSERT_TRUE(::testing::Mock::VerifyAndClearExpectations(&mockUtil));
    }
};

HWTEST_F(BBoxDetectorUnitTest, DetectorTest_001, TestSize.Level1)
{
    auto& mockUtil = MockHisyseventUtil::GetInstance();
    EXPECT_CALL(mockUtil, IsEventProcessed())
        .Times(AtLeast(1))
        .WillRepeatedly(Return(true));

    // 执行被测逻辑...
}
```

## 依赖注入

### 构造函数注入

```cpp
class DataProcessor {
public:
    DataProcessor(IDatabase* db, ILogger* logger)
        : db_(db), logger_(logger) {}

private:
    IDatabase* db_;
    ILogger* logger_;
};

// 测试时注入 Mock
MockDatabase mockDb;
MockLogger mockLogger;
DataProcessor processor(&mockDb, &mockLogger);
```

### 接口注入

```cpp
class DataProcessor {
public:
    void SetDatabase(IDatabase* db) { db_ = db; }
    void SetLogger(ILogger* logger) { logger_ = logger; }
};

// 测试时注入 Mock
processor.SetDatabase(&mockDb);
processor.SetLogger(&mockLogger);
```

## 注意事项

### 1. Mock 虚函数

gmock 只能 Mock 虚函数。非虚函数需要其他方法（如模板、接口隔离）。

```cpp
// ✓ 可以 Mock
class IInterface {
public:
    virtual void Method();  // 虚函数
};

// ❌ 无法直接 Mock
class ConcreteClass {
public:
    void Method();  // 非虚函数
};
```

### 2. 验证调用顺序

```cpp
using ::testing::InSequence;

InSequence seq;

EXPECT_CALL(mockDb, Connect(_));
EXPECT_CALL(mockDb, GetData(_));
EXPECT_CALL(mockDb, Disconnect());
// 按顺序验证
```

### 3. 避免过度 Mock

- 只 Mock 外部依赖
- 不要 Mock 被测对象本身
- 保持测试真实性

### 4. 访问私有成员

在单元测试中，经常需要访问或 Mock 被测类的 private/protected 成员。OpenHarmony 中常用的技巧是通过编译器宏将访问修饰符替换为 public：

在 BUILD.gn 中添加编译选项：

```gn
ohos_unittest("BBoxDetectorUnitTest") {
  sources = [
    "unittest/bbox_detector_unit_test.cpp",
    "mock/bbox_detectors_mock.cpp",
  ]
  cflags_cc = [
    "-Dprivate=public",
    "-Dprotected=public",
  ]
  external_deps = [
    "googletest:gmock",
    "googletest:gtest_main",
  ]
}
```

**原理**：`-Dprivate=public` 让预处理器将代码中所有的 `private` 关键字替换为 `public`，从而在测试中可以直接访问私有成员变量和方法。

> **注意**：此技巧仅用于单元测试，不要在正式代码中使用。某些编译器可能对此发出警告。

## Mock 文件组织

良好的 Mock 文件组织有助于维护和复用测试代码。

### 目录结构

Mock 类通常放在模块目录下单独的 `mock/` 子目录中：

```
module/
├── src/                        # 源码
│   ├── bbox_detector.cpp
│   └── hisysevent_util.cpp
├── unittest/                   # 测试代码
│   └── bbox_detector_unit_test.cpp
├── mock/                       # Mock 文件
│   ├── mock_bbox_detector.h
│   ├── bbox_detectors_mock.cpp
│   ├── mock_hisysevent_util.h
│   └── hisysevent_util_mock.cpp
├── BUILD.gn
└── bundle.json
```

### 命名规范

| 命名风格           | 示例                         | 说明       |
| -------------- | -------------------------- | -------- |
| `mock_xxx.h`   | `mock_hisysevent_util.h`   | mock_ 前缀 |
| `xxx_mock.h`   | `bbox_detectors_mock.h`    | _mock 后缀 |
| `mock_xxx.cpp` | `mock_hisysevent_util.cpp` | 配套实现文件   |

两种命名风格在 OpenHarmony 代码库中都存在，选择一种并在模块内保持一致即可。

### Mock 文件加入 BUILD.gn

Mock 的 `.cpp` 文件必须加入 BUILD.gn 的 `sources` 列表中：

```gn
ohos_unittest("BBoxDetectorUnitTest") {
  sources = [
    "unittest/bbox_detector_unit_test.cpp",
    # Mock 实现文件必须加入 sources
    "mock/bbox_detectors_mock.cpp",
    "mock/hisysevent_util_mock.cpp",
  ]
  include_dirs = [
    "mock",  # 如果 mock 头文件在单独目录
  ]
  external_deps = [
    "googletest:gmock",
    "googletest:gtest_main",
  ]
}
```

### Mock 复用

当多个测试目标需要相同的 Mock 类时，可以：

- 将通用 Mock 放在公共 `mock/` 目录
- 通过 `include_dirs` 引用 Mock 头文件
- 每个测试目标的 `sources` 中都要包含对应的 Mock `.cpp` 文件

## 相关文档

- [assertion-guide.md](assertion-guide.md) - 断言使用指南
- [test-examples.md](test-examples.md) - 测试用例示例
- [test-case-spec.md](test-case-spec.md) - 测试用例规范
