# HWTEST_F Framework Specifications

## Overview

This document specifies the HWTEST_F testing framework conventions used in OpenHarmony C++ unit testing.

## Test Fixture Structure

### Standard Test Fixture Class

```cpp
class YourServiceTest : public testing::Test {
public:
    static void SetUpTestCase(void);
    static void TearDownTestCase(void);
    void SetUp();
    void TearDown();
    std::shared_ptr<YourService> instance_;
};
```

### Test Fixture Usage (95.4% usage rate)

- Must use `HWTEST_F(TestFixtureName, TestCaseName_001, TestSize.Level1)` format
- Must define test fixture class inheriting from `::testing::Test` or custom base class
- Example:

```cpp
class ServiceTest : public ::testing::Test {
public:
    void SetUp() override {
        instance_ = std::make_shared<Service>();
    }
    void TearDown() override {
        instance_.reset();
    }
protected:
    std::shared_ptr<Service> instance_;
};

HWTEST_F(ServiceTest, MethodName_001, TestSize.Level1) {
    ASSERT_NE(instance_, nullptr);
    // Test logic
}
```

## SetUp/TearDown Usage (94.1% usage rate)

- Must implement `SetUp()` and `TearDown()` methods in test fixture class
- `SetUp()`: Used to initialize test environment (create objects, set up Mocks, etc.)
- `TearDown()`: Used to clean up test environment (release resources, reset state, etc.)
- Example:

```cpp
void SetUp() override {
    mockService_ = std::make_shared<MockService>();
    instance_ = std::make_shared<Service>(mockService_);
}
void TearDown() override {
    instance_.reset();
    mockService_.reset();
}
```

## HWTEST_F Macro

### Format

```cpp
HWTEST_F(TestClassName, TestCaseName_001, TestSize.Level1)
```

### Test Case Naming Convention

- `_001`: Normal scenario test
- `_002`: Exception scenario test
- `_003`: Boundary scenario test
- `_004+`: Other special scenario tests

### Example

```cpp
HWTEST_F(ServiceTest, MethodName_001, TestSize.Level1) {
    // Normal scenario
}

HWTEST_F(ServiceTest, MethodName_002, TestSize.Level1) {
    // Exception scenario
}

HWTEST_F(ServiceTest, MethodName_003, TestSize.Level1) {
    // Boundary scenario
}
```

## Logging Standards

### Log Format

```cpp
GTEST_LOG_(INFO) << "TestClass-begin TestName";
GTEST_LOG_(INFO) << "TestClass-end TestName";
```

### Example

```cpp
HWTEST_F(ServiceTest, MethodName_001, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ServiceTest-begin MethodName_001";
    // Test logic
    GTEST_LOG_(INFO) << "ServiceTest-end MethodName_001";
}
```

## Comment Standards

### Test Case Comment Format

```cpp
/**
 * @tc.name: TestCaseName_001
 * @tc.desc: Verify method works correctly
 * @tc.type: FUNC
 * @tc.require: issueI12345
 */
```

### Example

```cpp
/**
 * @tc.name: ServiceTest_MethodName_001
 * @tc.desc: Verify MethodName returns correct value for valid input
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ServiceTest, MethodName_001, TestSize.Level1) {
    // Test implementation
}
```

## TestSize Levels

- `TestSize.Level1`: Basic test cases
- `TestSize.Level2`: Medium complexity test cases
- `TestSize.Level3`: Complex test cases

## Direct Instantiation Prohibition

### Forbidden Pattern

```cpp
// WRONG: Direct instantiation in test function
YourService service;
service.Method();
```

### Correct Pattern

```cpp
// CORRECT: Use instance_ from test fixture
instance_->Method();
```

## Singleton Invocation

### Format by Return Type

```cpp
// Returns reference: use dot
ClassName::GetInstance().Method();

// Returns pointer: use arrow
ClassName::GetInstance()->Method();

// DelayedSingleton: use arrow
DelayedSingleton<T>::GetInstance()->Method();
```

## Static Function Testing

Static functions are called directly through the class name, no object instance needed.

### Format

```cpp
// Direct call through class name
ReturnType result = ClassName::StaticMethodName(param);
```

### Example

```cpp
HWTEST_F(ClassNameUtTest, StaticMethodName_0100, testing::ext::TestSize.Level1) {
    GTEST_LOG_(INFO) << "ClassNameUtTest-begin StaticMethodName_0100";
    try {
        ParamType param = /* construct test param */;
        // Direct call through class name
        ReturnType result = ClassName::StaticMethodName(param);
        EXPECT_EQ(result, expectedValue);
    } catch (...) {
        EXPECT_TRUE(false);
        GTEST_LOG_(INFO) << "ClassNameUtTest-an exception occurred.";
    }
    GTEST_LOG_(INFO) << "ClassNameUtTest-end StaticMethodName_0100";
}
```

### Static Function Test Notes

- No object instance needed in test fixture
- No need to create instance in SetUp()
- Call static function directly via ClassName::StaticMethodName()
- Mock dependencies if static function internally depends on other objects

## Framework Selection by Source Language

### C Language (.c)

- Generate C++ test file (.cpp extension)
- Use HWTEST_F framework
- Wrap C function calls with extern "C"
- Example:

```cpp
extern "C" {
#include "original_header.h"
}

HWTEST_F(CTest, FunctionName_001, TestSize.Level1) {
    // Direct C function call
    int result = c_function_name(param);
    EXPECT_EQ(result, expected);
}
```

### C++ Language (.cpp/.cc)

- Follow HWTEST_F structure directly
- Use C++ testing framework

## Test Pattern Statistics

Based on OpenHarmony codebase analysis (6238 test files, 3960 UT tests):

1. **TestFixture Usage**: 95.4% usage rate
2. **SetUp/TearDown Usage**: 94.1% usage rate
3. **Mock Usage**: 26.2% usage rate (when needed)
4. **EXPECT_EQ**: 74.2% usage rate (most common assertion)
5. **EXPECT_TRUE**: 43.2% usage rate
6. **EXPECT_NE**: 34.4% usage rate
