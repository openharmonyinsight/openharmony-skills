# 编译与运行错误排查指南

## 零、Anti-Patterns - 绝对禁止事项（必读）

以下操作会导致测试无法编译、运行或被OpenHarmony门禁拒绝。NEVER做这些操作：

### 编译配置类 Anti-Patterns

| ❌ 禁止操作 | 原因（为什么失败） | ✅ 正确做法 |
|------------|-------------------|------------|
| **NEVER 省略 `import("//build/test.gni")`** | ohos_unittest模板在此文件定义，缺失会报错"template 'ohos_unittest' not found" | BUILD.gn第一行必须import |
| **NEVER 在module_out_path使用绝对GN路径** | 输出路径格式必须为`子系统名/模块名`，使用`//base/xxx`会导致路径解析错误 | 使用相对格式如`hiviewdfx/hiview_test` |
| **NEVER 省略gtest_main依赖** | 缺失会导致链接错误"undefined reference to main"，测试无法启动 | deps中必须包含`//third_party/googletest:gtest_main` |
| **NEVER 访问private成员时忘记cflags_cc绕过** | private成员无法直接访问，会报编译错误"'xxx' is private within this context" | 添加`cflags_cc = ["-Dprivate=public", "-Dprotected=public"]` |
| **NEVER 混用include_dirs与configs** | 直接在ohos_unittest中使用include_dirs容易遗漏，不符合OpenHarmony规范 | 使用config()块统一管理include_dirs |
| **NEVER 在sources中遗漏测试文件** | 编译时会报"no input files"，测试目标无法生成 | sources必须包含所有*_test.cpp文件 |

### 测试代码类 Anti-Patterns

| ❌ 禁止操作 | 原因（为什么失败） | ✅ 正确做法 |
|------------|-------------------|------------|
| **NEVER 省略 `using namespace testing::ext;`** | HWTEST/HWTEST_F等宏定义在testing::ext命名空间，缺失会报"HWTEST was not declared" | 文件头必须包含该语句 |
| **NEVER 使用GTest原生 `TEST()` 或 `TEST_F()`** | OpenHarmony门禁系统无法识别GTest原生宏，缺少TestSize等级参数会被门禁拒绝 | 统一使用`HWTEST(A, B, TestSize.Level1)`或`HWTEST_F` |
| **NEVER 在HWTEST宏中忘记测试等级参数** | TestSize.Level1-4是门禁判断依据，缺失等级参数会导致测试无法按优先级执行 | 必须指定如`TestSize.Level1` |
| **NEVER 在SetUp中忘记初始化测试对象** | 未初始化的指针在测试中使用会导致Segmentation fault或NULL pointer错误 | SetUp中必须创建对象如`detector_ = new BBoxDetector()` |
| **NEVER 省略@tc.type注释** | OpenHarmony测试框架依赖@tc.type分类测试（FUNC/PERF/RELI），缺失会影响测试报告生成 | 每个HWTEST_F前必须添加完整@tc注释块 |
| **NEVER 混用测试类型概念** | OpenHarmony有FUNC/PERF/RELI/SECU/FUZZ类型，与GTest的测试概念不同，混用会导致门禁分类错误 | @tc.type使用OH定义：FUNC（功能）、PERF（性能）、RELI（可靠性） |
| **NEVER 使用EXPECT_*做前置检查** | EXPECT_*失败后会继续执行，可能导致后续代码访问无效指针引发崩溃 | 前置检查使用ASSERT_*（如ASSERT_NE(ptr, nullptr)） |

### 运行阶段类 Anti-Patterns

| ❌ 禁止操作 | 原因（为什么失败） | ✅ 正确做法 |
|------------|-------------------|------------|
| **NEVER 在SetUpTestCase中创建临时对象** | SetUpTestCase在所有测试前执行一次，创建的对象可能在后续测试中被修改导致状态污染 | SetUpTestCase仅初始化共享资源，单个对象在SetUp中创建 |
| **NEVER 忘记TearDown清理资源** | 未清理的资源会导致内存泄漏，连续运行多个测试时可能耗尽系统资源 | TearDown中必须delete/reset所有SetUp创建的对象 |
| **NEVER 在测试中使用硬编码路径** | 测试在不同设备上运行，硬编码路径如`/data/local/tmp`可能不存在 | 使用配置文件或环境变量获取路径，或通过resource_config_file加载 |

---

## 一、编译阶段常见错误

### 1. 头文件找不到 (fatal error: xxx.h: No such file or directory)

| 项目 | 内容 |
|------|------|
| **问题现象** | 编译时报错：`fatal error: bbox_detector.h: No such file or directory` |
| **根本原因** | include_dirs配置缺失或路径错误，编译器无法找到头文件 |
| **解决方案** | 在BUILD.gn的config块中添加include_dirs |
| **验证方法** | 重新编译，错误消失；或检查`out/<product>/obj/`下是否有正确的include路径 |

**示例配置**：
```gn
config("module_private_config") {
    visibility = [ ":*" ]
    include_dirs = [
        "//base/hiviewdfx/hiview/include",
        "//base/hiviewdfx/hiview/core",
    ]
}

ohos_unittest("BBoxDetectorUnitTest") {
    configs = [ ":module_private_config" ]  # 使用config块
}
```

**排查技巧**：
- 使用`find //base -name "xxx.h"`定位头文件实际位置
- 检查头文件路径是否使用GN格式（以`//`开头）

### 2. 链接错误 (undefined reference to xxx)

| 项目 | 内容 |
|------|------|
| **问题现象** | 编译成功但链接时报错：`undefined reference to 'BBoxDetector::GetSectionInfo'` |
| **根本原因** | deps或external_deps缺少依赖项，被测模块或公共库未链接到测试目标 |
| **解决方案** | 在deps中添加被测模块路径，在external_deps中添加公共库 |
| **验证方法** | 重新编译链接，错误消失；运行测试时无"symbol not found"错误 |

**deps与external_deps区别**：
- **deps**：指向OpenHarmony内部编译目标（GN路径格式）
- **external_deps**：指向SDK提供的公共库（子系统名:库名格式）

**常见external_deps列表**：
```gn
external_deps = [
    "c_utils:utils",              # OHOS基础工具库
    "hilog:libhilog",             # 日志库（必加，用于GTEST_LOG_）
    "googletest:gtest_main",      # GTest主函数（必加）
    "googletest:gmock",           # gmock（使用Mock时必加）
    "ipc:libipc",                 # IPC通信
    "hisysevent:libhisysevent",   # 系统事件
]
```

**排查技巧**：
- 检查被测模块BUILD.gn中是否有对应library目标
- 使用`grep "ohos_shared_library" //base/xxx/BUILD.gn`确认模块名

### 3. 访问私有成员报错 ('xxx' is private within this context)

| 项目 | 内容 |
|------|------|
| **问题现象** | 编译时报错：`error: 'privateMethod_' is private within this context` |
| **根本原因** | 测试代码访问被测类的private/protected成员，C++访问控制阻止 |
| **解决方案** | 在BUILD.gn中添加cflags_cc替换访问修饰符 |
| **验证方法** | 重新编译，private成员可访问；测试代码不再报private错误 |

**解决方案代码**：
```gn
ohos_unittest("BBoxDetectorUnitTest") {
    cflags_cc = [
        "-Dprivate=public",      # 将private替换为public
        "-Dprotected=public",    # 将protected替换为public
    ]
}
```

**注意事项**：
- 此方法会修改所有private/protected标识符，包括标准库中的，可能导致冲突
- 仅用于单元测试，不得用于正式代码
- 替代方案：在被测类中使用`friend class BBoxDetectorTest`声明

**排查技巧**：
- 如果添加cflags后仍有错误，检查是否有多处BUILD.gn配置冲突
- 部分模块可能有自己的cflags配置，需合并

### 4. RTTI 错误 (cannot use 'dynamic_cast' with -fno-rtti)

| 项目 | 内容 |
|------|------|
| **问题现象** | 编译时报错：`error: 'dynamic_cast' not permitted with -fno-rtti` |
| **根本原因** | OpenHarmony部分模块默认禁用RTTI（运行时类型识别），dynamic_cast不可用 |
| **解决方案** | 在config中添加-frtti编译选项重新启用RTTI |
| **验证方法** | 重新编译，dynamic_cast正常工作；无RTTI相关错误 |

**解决方案代码**：
```gn
config("test_rtti_config") {
    cflags = [ "-frtti" ]  # 启用RTTI
}

ohos_unittest("MyTest") {
    configs += [ ":test_rtti_config" ]
}
```

**排查技巧**：
- 仅在需要dynamic_cast的测试中添加-frtti
- 如果仍报错，检查是否有其他config覆盖了cflags

### 5. gmock 相关编译错误

| 错误类型 | 项目 | 内容 |
|----------|------|------|
| **MOCK_METHOD未声明** | 问题现象 | `error: 'MOCK_METHOD' was not declared in this scope` |
| | 根本原因 | BUILD.gn缺少gmock依赖或头文件未包含 |
| | 解决方案 | external_deps添加`"googletest:gmock"`，头文件添加`#include <gmock/gmock.h>` |
| | 验证方法 | MOCK_METHOD可正常使用，编译无错误 |
| **ON_CALL/EXPECT_CALL未声明** | 问题现象 | `error: 'ON_CALL' was not declared` |
| | 根本原因 | 缺少using namespace声明 |
| | 解决方案 | 添加`using namespace testing;`或`using testing::ON_CALL;` |
| | 验证方法 | gmock宏正常工作 |

### 6. 多重定义错误 (multiple definition of xxx)

| 项目 | 内容 |
|------|------|
| **问题现象** | 链接时报错：`multiple definition of 'Utility::Process()'` |
| **根本原因** | 同一源文件被多个测试目标包含，导致符号重复定义 |
| **解决方案** | 使用sources +=方式复用源文件列表变量，避免重复包含 |
| **验证方法** | 链接成功，无multiple definition错误 |

**解决方案代码**：
```gn
# 定义共享源文件变量
test_sources = [
    "//base/xxx/src/utility.cpp",
    "//base/xxx/src/common.cpp",
]

ohos_unittest("TestA") {
    sources = [ "test_a.cpp" ]
    sources += test_sources  # 复用共享源文件
}

ohos_unittest("TestB") {
    sources = [ "test_b.cpp" ]
    sources += test_sources  # 复用同一变量
}
```

**排查技巧**：
- 检查是否有两处BUILD.gn都包含同一.cpp文件
- 避免在头文件中定义非inline函数（会导致每个编译单元都有定义）

### 7. 测试模板未找到 (template 'ohos_unittest' not found)

| 项目 | 内容 |
|------|------|
| **问题现象** | GN解析时报错：`error: template 'ohos_unittest' not found` |
| **根本原因** | BUILD.gn缺少`import("//build/test.gni")`语句 |
| **解决方案** | BUILD.gn第一行添加import语句 |
| **验证方法** | GN解析成功，ohos_unittest可正常使用 |

**解决方案代码**：
```gn
import("//build/test.gni")  # 必须在第一行

module_output_path = "hiviewdfx/hiview_test"

ohos_unittest("BBoxDetectorUnitTest") { ... }
```

**NEVER忘记此项**：这是最常见的编译错误，必须养成习惯第一行import。

## 二、运行阶段常见错误

### 1. 测试用例超时

| 项目 | 内容 |
|------|------|
| **问题现象** | 测试执行一段时间后被框架终止，报"Timeout"错误 |
| **根本原因** | 等待异步回调未返回、死锁、资源竞争导致测试无法正常结束 |
| **解决方案** | 添加超时控制逻辑、检查异步操作、优化SetUp/TearDown耗时操作 |
| **验证方法** | 测试在规定时间内完成，无Timeout错误；连续运行10次以上稳定通过 |

**排查方法**：
```cpp
HWTEST_F(MyTest, TimeoutCheck_001, TestSize.Level1)
{
    GTEST_LOG_(INFO) << "Test start";
    
    auto startTime = std::chrono::steady_clock::now();
    // ... 测试代码 ...
    auto endTime = std::chrono::steady_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime);
    GTEST_LOG_(INFO) << "Test duration: " << duration.count() << "ms";
    
    EXPECT_LT(duration.count(), 5000);  // 验证执行时间小于5秒
}
```

**常见超时原因**：
- SetUp/TearDown中有阻塞操作（文件I/O、网络请求）
- 等待异步回调但未设置超时
- 死锁：两个线程互相等待对方释放资源

### 2. 段错误 (Segmentation fault)

| 项目 | 内容 |
|------|------|
| **问题现象** | 测试运行时突然崩溃，报"Segmentation fault"或"SIGSEGV" |
| **根本原因** | 空指针解引用、访问已释放内存、数组越界 |
| **解决方案** | 检查SetUp初始化、使用智能指针、添加边界检查 |
| **验证方法** | 测试稳定运行无崩溃；添加日志后能定位到具体崩溃位置 |

**调试方法**：
```cpp
HWTEST_F(MyTest, DebugTest_001, TestSize.Level1)
{
    GTEST_LOG_(INFO) << "Checkpoint 1: Before object creation";
    ASSERT_NE(myObject_, nullptr) << "Object creation failed in SetUp";  // 前置检查
    
    GTEST_LOG_(INFO) << "Checkpoint 2: Before method call";
    auto result = myObject_->DoSomething();
    GTEST_LOG_(INFO) << "Checkpoint 3: After method call, result=" << result;
    
    EXPECT_EQ(result, expected);
    GTEST_LOG_(INFO) << "Checkpoint 4: Test completed";
}
```

**常见段错误原因与解决**：
| 原因 | 解决方案 |
|------|----------|
| SetUp中对象未初始化（detector_为nullptr） | SetUp中必须创建：`detector_ = new BBoxDetector()` |
| 使用已delete的对象 | 使用智能指针`std::shared_ptr`，在TearDown中reset |
| 数组访问越界（index > size） | 添加边界检查：`ASSERT_LT(index, array.size())` |
| 访问空容器元素 | 检查容器非空：`ASSERT_FALSE(container.empty())` |

### 3. SetUp 失败导致所有用例失败

| 项目 | 内容 |
|------|------|
| **问题现象** | 测试套内所有用例都FAIL，报"SetUp failed"或初始化相关错误 |
| **根本原因** | SetUpTestCase或SetUp中的初始化失败（文件不存在、权限不足、平台未初始化） |
| **解决方案** | 检查文件路径、添加条件检查、确保测试目录存在 |
| **验证方法** | SetUp成功执行，测试套内至少有部分用例PASS |

**调试方法**：
```cpp
void MyTest::SetUpTestCase()
{
    GTEST_LOG_(INFO) << "SetUpTestCase: Creating test directory";
    bool result = FileUtil::ForceCreateDirectory("/data/test/mytest/");
    if (!result) {
        GTEST_LOG_(ERROR) << "Failed to create directory: /data/test/mytest/";
    }
}

void MyTest::SetUp()
{
    GTEST_LOG_(INFO) << "SetUp: Initializing object";
    detector_ = new BBoxDetector();
    ASSERT_NE(detector_, nullptr) << "detector_ creation failed";
}
```

**常见SetUp失败原因**：
- 测试目录不存在（如`/data/test/xxx`）
- 文件权限不足（无法创建目录或写入文件）
- 平台服务未启动（依赖的hilog、hisysevent等服务）
- 配置文件找不到（resource_config_file配置错误）

### 4. 资源文件找不到

| 项目 | 内容 |
|------|------|
| **问题现象** | 测试运行时报错：`Failed to load config file: xxx.xml` 或测试数据不存在 |
| **根本原因** | BUILD.gn未配置resource_config_file，或资源配置文件路径错误 |
| **解决方案** | 配置resource_config_file，创建ohos_test.xml资源映射文件 |
| **验证方法** | 测试运行时能正常加载资源文件；无资源相关错误 |

**解决方案代码**：
```gn
ohos_unittest("MyTest") {
    resource_config_file = "//base/hiviewdfx/hiview/test/resource/ohos_test.xml"
}
```

**ohos_test.xml示例**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <target name="MyTest">
        <preparer>
            <option name="push" value="test_data.txt -> /data/test/mytest/" />
        </preparer>
    </target>
</configuration>
```

### 5. HWTEST宏未识别

| 项目 | 内容 |
|------|------|
| **问题现象** | 编译报错：`error: 'HWTEST_F' was not declared in this scope` |
| **根本原因** | 文件缺少`using namespace testing::ext;`语句 |
| **解决方案** | 在测试文件头部添加命名空间声明 |
| **验证方法** | HWTEST宏可正常使用，编译无错误 |

**解决方案代码**：
```cpp
#include <gtest/gtest.h>
#include "bbox_detector.h"

using namespace testing::ext;  // 必须添加，HWTEST定义在此命名空间

HWTEST_F(BBoxDetectorTest, GetSectionInfo_001, TestSize.Level1)
{
    // 测试代码
}
```

**NEVER省略此项**：这是最常见的测试代码错误，每个测试文件都必须包含。

### 6. 测试等级未指定

| 项目 | 内容 |
|------|------|
| **问题现象** | 门禁系统报错：`Invalid test level`或测试无法按优先级执行 |
| **根本原因** | HWTEST宏缺少TestSize.Level参数 |
| **解决方案** | 在HWTEST宏中添加测试等级参数 |
| **验证方法** | 门禁系统正确识别测试等级；测试可按Level0-4优先级执行 |

**正确格式**：
```cpp
HWTEST_F(BBoxDetectorTest, Test_001, TestSize.Level1)  // 正确：指定Level1
// HWTEST_F(BBoxDetectorTest, Test_001)  // 错误：缺少等级参数
```

## 三、BUILD.gn 配置排查清单

### 完整配置检查表（必逐项检查）

| 检查项 | 配置项 | 必填性 | 常见问题 | 正确示例 |
|--------|--------|--------|----------|----------|
| Import语句 | `import("//build/test.gni")` | **必填** | 缺失导致template not found | BUILD.gn第一行 |
| 输出路径 | `module_out_path` | **必填** | 使用GN路径而非子系统/模块格式 | `"hiviewdfx/hiview_test"` |
| 源文件 | `sources` | **必填** | 遗漏*_test.cpp文件 | `["unittest/bbox_test.cpp"]` |
| 头文件目录 | `include_dirs`（在config块中） | **必填** | 路径错误或遗漏被测模块include | `["//base/xxx/include"]` |
| 内部依赖 | `deps` | **必填** | 缺少gtest_main或被测模块 | `["//third_party/googletest:gtest_main"]` |
| 外部依赖 | `external_deps` | 按需 | 缺少公共库导致链接错误 | `["hilog:libhilog"]` |
| 访问控制 | `cflags_cc` | 按需 | 测试private成员时未配置 | `["-Dprivate=public"]` |
| 资源配置 | `resource_config_file` | 按需 | 文件路径不存在或格式错误 | `"//base/xxx/test/ohos_test.xml"` |
| 编译宏 | `defines` | 按需 | 缺少UNIT_TEST宏影响条件编译 | `["UNIT_TEST", "HILOG_ENABLE"]` |

### BUILD.gn模板完整示例（参考）

```gn
import("//build/test.gni")  # [必须] 第一行import

module_output_path = "hiviewdfx/hiview_test"  # [必须] 输出路径

config("module_private_config") {  # [推荐] 使用config块管理include
    visibility = [ ":*" ]
    include_dirs = [
        "//base/hiviewdfx/hiview/include",
        "//base/hiviewdfx/hiview/core",
    ]
}

ohos_unittest("BBoxDetectorUnitTest") {
    module_out_path = module_output_path
    
    sources = [  # [必须] 测试源文件
        "unittest/bbox_detector/bbox_detector_test.cpp",
    ]
    
    configs = [ ":module_private_config" ]  # [推荐] 引用config块
    
    deps = [  # [必须] 内部依赖
        "//third_party/googletest:gtest_main",  # 必加
        "//base/hiviewdfx/hiview:hiview_core",  # 被测模块
    ]
    
    external_deps = [  # [按需] 外部依赖
        "hiviewdfx_hilog_native:libhilog",
        "googletest:gmock",  # Mock时必加
    ]
    
    cflags_cc = [  # [按需] 访问private成员
        "-Dprivate=public",
        "-Dprotected=public",
    ]
    
    defines = [  # [按需] 条件编译宏
        "UNIT_TEST",
        "HILOG_ENABLE",
    ]
    
    resource_config_file = "//base/hiviewdfx/hiview/test/ohos_test.xml"  # [按需]
}

group("unittest") {  # [必须] 测试入口分组
    testonly = true
    deps = [":BBoxDetectorUnitTest"]
}
```

### 编译与运行命令参考

```bash
# 编译单个测试目标
./build.sh --product-name Hi3516DV300 --build-target BBoxDetectorUnitTest

# 编译整个子系统测试
./build.sh --product-name Hi3516DV300 --build-target tests

# 运行测试（通过hdc工具）
hdc shell aa test -b <bundle_name> -m <module_name>

# 查看测试结果
hdc shell ls /data/local/tmp/<test_name>/
```

---

## 四、调试技巧与最佳实践

### 1. GTEST_LOG_ 日志分层使用

| 日志级别 | 使用场景 | 示例 |
|----------|----------|------|
| `GTEST_LOG_(INFO)` | 关键步骤标记、状态输出 | `GTEST_LOG_(INFO) << "Test start"` |
| `GTEST_LOG_(WARNING)` | 非预期但可继续的情况 | `GTEST_LOG_(WARNING) << "Value near boundary"` |
| `GTEST_LOG_(ERROR)` | 错误条件、失败分析 | `GTEST_LOG_(ERROR) << "Assertion failed: " << val` |

**推荐日志模式**：
```cpp
HWTEST_F(MyTest, MyTest_001, TestSize.Level1)
{
    GTEST_LOG_(INFO) << "MyTest_001: Test execution start";
    
    ASSERT_NE(myObject_, nullptr) << "MyTest_001: Object is null";  // 失败时自动输出
    
    GTEST_LOG_(INFO) << "MyTest_001: Calling method";
    auto result = myObject_->Process(input);
    GTEST_LOG_(INFO) << "MyTest_001: Result = " << result;
    
    EXPECT_EQ(result, expected) << "MyTest_001: Result mismatch";
    
    GTEST_LOG_(INFO) << "MyTest_001: Test execution end";
}
```

### 2. 逐步验证法（定位崩溃）

当测试崩溃时，使用checkpoint模式定位：

```cpp
HWTEST_F(MyTest, CrashDebug_001, TestSize.Level1)
{
    // Step 1: 前置条件检查（使用ASSERT，失败即终止）
    GTEST_LOG_(INFO) << "Checkpoint 1: Checking prerequisites";
    ASSERT_NE(myObject_, nullptr) << "Object creation failed";
    ASSERT_TRUE(myObject_->IsInitialized()) << "Object not initialized";
    
    // Step 2: 准备数据（添加日志）
    GTEST_LOG_(INFO) << "Checkpoint 2: Preparing test data";
    std::string input = "test_data";
    GTEST_LOG_(INFO) << "Checkpoint 3: Input prepared: " << input;
    
    // Step 3: 执行被测方法（关键步骤）
    GTEST_LOG_(INFO) << "Checkpoint 4: Calling Process method";
    auto result = myObject_->Process(input);
    GTEST_LOG_(INFO) << "Checkpoint 5: Process returned: " << result;
    
    // Step 4: 验证结果
    GTEST_LOG_(INFO) << "Checkpoint 6: Verifying result";
    EXPECT_EQ(result, "expected_output");
    
    GTEST_LOG_(INFO) << "Checkpoint 7: Test completed successfully";
}
```

**定位技巧**：
- 如果崩溃在Checkpoint 4和5之间 → Process方法内部问题
- 如果崩溃在Checkpoint 1 → SetUp初始化问题
- 添加足够多的checkpoint，缩小问题范围

### 3. SetUp/TearDown 最佳实践

```cpp
class BBoxDetectorTest : public testing::Test {
public:
    static void SetUpTestCase() {
        // [仅] 全局共享资源初始化（所有测试前执行一次）
        GTEST_LOG_(INFO) << "SetUpTestCase: Global initialization";
        FileUtil::ForceCreateDirectory("/data/test/bbox/");  // 创建共享目录
    }
    
    static void TearDownTestCase() {
        // [仅] 全局共享资源清理（所有测试后执行一次）
        GTEST_LOG_(INFO) << "TearDownTestCase: Global cleanup";
        FileUtil::ForceRemoveDirectory("/data/test/bbox/");
    }
    
    void SetUp() override {
        // [每个测试] 单测试对象初始化（每个测试前执行）
        GTEST_LOG_(INFO) << "SetUp: Creating test object";
        detector_ = new BBoxDetector();  // 必须初始化
        ASSERT_NE(detector_, nullptr);   // 验证初始化成功
    }
    
    void TearDown() override {
        // [每个测试] 单测试对象清理（每个测试后执行）
        GTEST_LOG_(INFO) << "TearDown: Cleaning test object";
        if (detector_ != nullptr) {
            delete detector_;  // 必须清理
            detector_ = nullptr;
        }
    }
    
    BBoxDetector* detector_;  // 测试对象成员
};
```

**NEVER违反的规则**：
- SetUp中必须初始化所有测试对象成员
- TearDown中必须清理所有SetUp创建的资源
- SetUpTestCase仅初始化全局共享资源，不创建测试对象
- 每个SetUp/TearDown操作都添加GTEST_LOG_记录

### 4. 条件编译调试（仅测试时启用）

```cpp
#ifdef UNIT_TEST  // BUILD.gn defines中定义UNIT_TEST
    // 仅在测试编译时启用的调试代码
    void PrintDebugInfo() {
        GTEST_LOG_(INFO) << "Debug: Internal state=" << internalState_;
    }
#endif

// BUILD.gn中添加
defines = [ "UNIT_TEST" ]
```

**使用场景**：
- 在正式代码中添加测试专用的调试接口
- 不影响正式编译，仅在UNIT_TEST宏定义时生效
- 可访问private成员的调试方法

### 5. Mock依赖对象模式（避免外部依赖）

当测试对象依赖外部服务（数据库、网络、IPC）时，使用gmock隔离：

```cpp
#include <gmock/gmock.h>

class MockDatabase : public DatabaseInterface {
public:
    MOCK_METHOD(bool, Connect, (const std::string&), (override));
    MOCK_METHOD(bool, Query, (const std::string&, Result&), (override));
};

HWTEST_F(MyTest, MockTest_001, TestSize.Level1)
{
    MockDatabase mockDb;
    
    // 设置期望行为
    EXPECT_CALL(mockDb, Connect("test_config"))
        .WillOnce(Return(true));
    EXPECT_CALL(mockDb, Query("SELECT *", _))
        .WillOnce(DoAll(SetArgReferee<1>( expectedResult), Return(true)));
    
    MyService service(&mockDb);
    EXPECT_TRUE(service.Process());
}
```

**NEVER忘记配置gmock依赖**：BUILD.gn中必须添加`"googletest:gmock"`到external_deps。

---

## 五、错误排查流程图

```
测试失败
  ↓
检查日志输出（GTEST_LOG_）
  ↓
┌─ 编译错误 ────────────────────┐
│  → 检查BUILD.gn配置           │
│    - import语句               │
│    - include_dirs             │
│    - deps/external_deps       │
│  → 检查测试代码                │
│    - using namespace testing::ext │
│    - HWTEST宏格式              │
└───────────────────────────────┘
  ↓
┌─ 运行错误 ────────────────────┐
│  → Segmentation fault         │
│    - 检查SetUp初始化           │
│    - 添加checkpoint日志        │
│  → Timeout                    │
│    - 检查异步操作              │
│    - 优化耗时操作              │
│  → SetUp failed               │
│    - 检查文件路径              │
│    - 检查权限                  │
└───────────────────────────────┘
  ↓
添加调试日志 → 逐步排查 → 定位问题 → 修复
```

---

## 总结：NEVER忘记的10项检查

在提交测试代码前，NEVER忘记检查以下10项：

1. **NEVER省略** `import("//build/test.gni")` - BUILD.gn第一行
2. **NEVER省略** `using namespace testing::ext;` - 测试文件头部
3. **NEVER省略** `//third_party/googletest:gtest_main` - deps必加
4. **NEVER忘记** SetUp中初始化测试对象 - 否则段错误
5. **NEVER忘记** TearDown中清理资源 - 否则内存泄漏
6. **NEVER使用** TEST()替代HWTEST() - 门禁拒绝
7. **NEVER忘记** TestSize.Level参数 - HWTEST宏必填
8. **NEVER忘记** @tc注释块 - 每个HWTEST_F前必加
9. **NEVER混用** include_dirs直接配置 - 使用config块
10. **NEVER在** module_out_path使用GN路径 - 使用子系统/模块格式

## 四、调试技巧

### 1. GTEST_LOG_ 日志

```cpp
GTEST_LOG_(INFO) << "BBoxDetectorUnitTest001 start";
GTEST_LOG_(INFO) << "result: " << result;
```

### 2. 逐步验证法

```cpp
HWTEST_F(MyTest, DebugTest001, TestSize.Level1)
{
    // Step 1: 前置检查
    ASSERT_NE(myObject, nullptr) << "Object creation failed";

    // Step 2: 逐步调用，每步加日志
    GTEST_LOG_(INFO) << "Before method call";
    auto result = myObject->DoSomething();
    GTEST_LOG_(INFO) << "After method call, result=" << result;

    // Step 3: 验证结果
    EXPECT_EQ(result, expected);
}
```

### 3. 条件编译调试

```cpp
#ifdef TRACE_STRATEGY_UNITTEST
    // 仅在测试时启用的调试代码
    GTEST_LOG_(INFO) << "Debug: strategy state=" << state;
#endif
```
