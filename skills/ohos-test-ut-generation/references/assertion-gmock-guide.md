# GTest 断言与 gmock 使用指南（OpenHarmony版）

---

## 一、断言使用

### 核心选择原则

| 类型         | 失败行为   | 使用场景              |
| ---------- | ------ | ----------------- |
| `ASSERT_*` | 终止当前测试 | 前置条件检查（指针非空、状态验证） |
| `EXPECT_*` | 继续执行测试 | 结果验证（可收集多个失败）     |

### 前置条件检查（必须用 ASSERT）

```cpp
// ✓ 正确：前置条件失败应终止
ASSERT_NE(obj, nullptr);
EXPECT_EQ(obj->GetValue(), 100);

// ❌ 错误：前置条件用EXPECT会导致空指针崩溃
EXPECT_NE(obj, nullptr);
obj->GetValue();  // 空指针崩溃
```

### 多结果验证（必须用 EXPECT）

```cpp
EXPECT_EQ(value1, expected1);
EXPECT_EQ(value2, expected2);
EXPECT_EQ(value3, expected3);
```

### 断言速查表

| 验证内容  | 推荐断言                     | 使用场景 |
| ----- | ------------------------ | ---- |
| 数值相等  | `EXPECT_EQ(a, b)`        | 结果验证 |
| 数值不等  | `EXPECT_NE(a, b)`        | 结果验证 |
| 条件为真  | `EXPECT_TRUE(cond)`      | 结果验证 |
| 指针非空  | `ASSERT_NE(p, nullptr)`  | 前置条件 |
| 状态检查  | `ASSERT_TRUE(condition)` | 前置条件 |
| 大于/小于 | `EXPECT_GT/LT(a, b)`     | 性能指标 |
| 字符串相等 | `EXPECT_STREQ(s1, s2)`   | C字符串 |
| 浮点近似  | `EXPECT_FLOAT_EQ(a, b)`  | 浮点数  |
| 抛出异常  | `EXPECT_THROW(stmt, ex)` | 异常处理 |

### 断言顺序最佳实践

```cpp
HWTEST_F(DatabaseTest, Insert_001, TestSize.Level1)
{
    // 1. 前置条件（ASSERT）
    ASSERT_TRUE(db->Connect());

    // 2. 执行操作
    bool inserted = db->Insert(data);

    // 3. 结果验证（EXPECT）
    EXPECT_TRUE(inserted);
    EXPECT_EQ(db->Count(), oldCount + 1);
}
```

---

## 二、gmock 配置

### BUILD.gn 集成（必须配置）

```gn
ohos_unittest("BBoxDetectorUnitTest") {
  sources = [
    "unittest/bbox_detector_unit_test.cpp",
    "mock/bbox_detectors_mock.cpp",
  ]
  deps = [
    "//third_party/googletest:gtest_main",  # 必填：提供main函数入口
  ]
  external_deps = [
    "googletest:gmock",      # 使用Mock时必填
    "hilog:libhilog",
  ]
}
```

| 配置项                                   | 说明                 | 必填性       |
| ------------------------------------- | ------------------ | --------- |
| `"googletest:gmock"`                  | 引入 gmock 库         | 使用Mock时必填 |
| `//third_party/googletest:gtest_main` | gtest 主函数（统一放deps） | 必填        |
| `mock/*.cpp` 加入 `sources`             | Mock实现文件           | 使用Mock时必填 |

> **注意**：Mock 的 `.cpp` 文件必须加入 BUILD.gn 的 `sources`，否则链接时报未定义引用。

### Mock 文件组织

```
module/
├── unittest/
│   └── bbox_detector_unit_test.cpp
├── mock/                       # Mock 文件目录
│   ├── mock_bbox_detector.h
│   └── bbox_detectors_mock.cpp
└── BUILD.gn
```

| 命名风格         | 示例                       |
| ------------ | ------------------------ |
| `mock_xxx.h` | `mock_hisysevent_util.h` |
| `xxx_mock.h` | `bbox_detectors_mock.h`  |

### Mock 模式示例（OpenHarmony hiviewdfx仓库）

```cpp
#include <gmock/gmock.h>

// 类继承 Mock
class MockHiviewContext : public HiviewContext {
public:
    MOCK_METHOD(std::shared_ptr<EventLoop>, GetSharedWorkLoop, (), (override));
};

// 单例 Mock 模式
class MockHisyseventUtil {
public:
    static MockHisyseventUtil& GetInstance();
    MOCK_METHOD(bool, IsEventProcessed, (), ());

private:
    MockHisyseventUtil() = default;
    MockHisyseventUtil& operator=(const MockHisyseventUtil&) = delete;
};
```

### 访问私有成员

```gn
ohos_unittest("BBoxDetectorUnitTest") {
  cflags_cc = [
    "-Dprivate=public",
    "-Dprotected=public",
  ]
}
```

**原理**：`-Dprivate=public` 将 `private` 替换为 `public`。

### 何时需要添加 gmock

使用了以下功能时必须添加 `"googletest:gmock"`：

- `MOCK_METHOD` 宏
- `NiceMock<>` / `StrictMock<>` 模板
- `EXPECT_CALL` / `ON_CALL` 匹配器

### gmock 只能 Mock 虚函数

```cpp
// ✓ 可以 Mock：虚函数
class IInterface { virtual void Method(); };

// ❌ 无法直接 Mock：非虚函数
class ConcreteClass { void Method(); };
```

---

## 相关文档

- [test-macro.md](test-macro.md) - 测试宏详细用法
- [test-examples.md](test-examples.md) - 测试用例示例
