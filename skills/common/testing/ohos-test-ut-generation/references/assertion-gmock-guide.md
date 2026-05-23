# OpenHarmony gmock 配置指南

---

## 一、BUILD.gn集成配置（门禁强制要求）

**基础配置（使用gmock时必填）**：
```python
ohos_unittest("BBoxDetectorUnitTest") {
    sources = [
        "unittest/bbox_detector_unit_test.cpp",
        "mock/bbox_detectors_mock.cpp",  # Mock实现必须加入sources
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

**配置项说明**：
| 配置项 | 说明 | 必填性 |
|--------|------|--------|
| `"googletest:gmock"` | gmock库依赖 | **使用Mock时必填** |
| `//third_party/googletest:gtest_main` | gtest主函数 | **必填**（放deps） |
| `mock/*.cpp` 加入 `sources` | Mock实现文件 | **使用Mock时必填** |

**常见错误**：
```python
# ❌ 错误：Mock cpp未加入sources → 链接错误"undefined reference"
sources = [ "test.cpp" ]  # 缺失 mock/mock_service.cpp

# ❌ 错误：gmock放deps而非external_deps
deps = [ "googletest:gmock" ]  # 应放external_deps
```

---

## 二、访问私有成员（OpenHarmony特有配置）

**cflags_cc配置**：
```python
ohos_unittest("PrivateTest") {
    cflags_cc = [
        "-Dprivate=public",     # 绕过private访问控制
        "-Dprotected=public",   # 绕过protected访问控制
    ]
}
```

**原理**：编译器将 `private`/`protected` 关键字替换为 `public`，允许测试代码访问。

**何时需要**：
- 测试private成员变量
- 测试protected方法
- 验证内部状态

**NEVER忘记**：
```cpp
// 访问private成员但BUILD.gn无cflags_cc → 编译错误"is private within this context"
```

---

## 三、Mock文件组织（OpenHarmony仓库规范）

**目录结构**：
```
module/
├── unittest/
│   └── bbox_detector_unit_test.cpp
├── mock/                       # Mock文件目录
│   ├── mock_bbox_detector.h    # 命名：mock_xxx.h 或 xxx_mock.h
│   └── bbox_detectors_mock.cpp
└── BUILD.gn
```

**命名风格**（两种均可）：
- `mock_xxx.h`：如 `mock_hisysevent_util.h`
- `xxx_mock.h`：如 `bbox_detectors_mock.h`

---

## 四、真实仓库示例（hiviewdfx）

### 类继承Mock模式

```cpp
// mock/bbox_detectors_mock.h
#include <gmock/gmock.h>
#include "plugin.h"

namespace OHOS {
namespace HiviewDFX {
class MockHiviewContext : public HiviewContext {
public:
    MOCK_METHOD0(GetSharedWorkLoop, std::shared_ptr<EventLoop>());
};

class MockEventLoop : public EventLoop {
public:
    MockEventLoop() : EventLoop("testEventLoop") {};
    // 混合模式：部分方法手动覆写，部分用MOCK_METHOD
    uint64_t AddTimerEvent(...) override;  // 手动实现
    MOCK_METHOD0(GetMockInterval, uint64_t());  // gmock宏
};
}
}
```

### 单例Mock模式

```cpp
// mock/hisysevent_util_mock.h
#include <gmock/gmock.h>

namespace OHOS {
namespace HiviewDFX {
class MockHisyseventUtil {
public:
    static MockHisyseventUtil& GetInstance();  // 单例入口
    MOCK_METHOD0(IsEventProcessed, bool());

private:
    MockHisyseventUtil() = default;
    ~MockHisyseventUtil() = default;
    MockHisyseventUtil& operator=(const MockHisyseventUtil&) = delete;
    MockHisyseventUtil(const MockHisyseventUtil&) = delete;
};
}
}
```

**要点**：
- 单例Mock通过 `GetInstance()` 提供全局实例
- 构造函数/析构函数设为 `private`，确保单例语义
- 拷贝/赋值操作显式 `delete`

---

## 五、何时添加gmock依赖

**必须添加 `"googletest:gmock"` 的场景**：
- 使用 `MOCK_METHOD` 宏
- 使用 `NiceMock<>`/`StrictMock<>` 模板
- 使用 `EXPECT_CALL`/`ON_CALL` 匹配器

**判断依据**：
```cpp
// ✓ 需要gmock：使用了MOCK_METHOD
class MockService : public IService {
    MOCK_METHOD(bool, Connect, (const string&), (override));
};

// ❌ 不需要gmock：纯gtest测试
HWTEST_F(Test, Func_001, TestSize.Level1) {
    EXPECT_EQ(obj->Method(), expected);  // 仅用EXPECT_*断言
}
```

---

## 六、Mock文件完整示例

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

#endif
```

```cpp
// test.cpp使用示例
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "mock/mock_network_service.h"

using ::testing::Return;
using ::testing::_;

HWTEST_F(NetworkTest, Connect_001, TestSize.Level1)
{
    auto mockService = std::make_unique<MockNetworkService>();
    
    EXPECT_CALL(*mockService, Connect("127.0.0.1"))
        .Times(1)
        .WillOnce(Return(true));
    
    bool result = mockService->Connect("127.0.0.1");
    EXPECT_TRUE(result);
}
```

---

## 相关文档

- [framework-quickref.md](framework-quickref.md) - 测试框架速查表
- [build-rules.md](build-rules.md) - BUILD.gn配置规则
- [real-patterns.md](real-patterns.md) - 真实仓库示例（含Mock模式）