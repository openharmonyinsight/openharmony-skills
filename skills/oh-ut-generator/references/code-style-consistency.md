# Code Style Consistency

## Overview

This document specifies the code style consistency requirements for OpenHarmony unit tests when existing test files exist.

## Consistency Requirement

**Important Note**: The system automatically compares generated UT code with existing UT code. If existing test files exist, the generated code must be basically consistent with existing code in important scenarios.

### Consistency Threshold

- **Important scenario consistency >= 70%**: Basically consistent, acceptable
- **Important scenario consistency >= 90%**: Highly consistent, excellent
- **Important scenario consistency < 70%**: Inconsistent, needs improvement

**If important scenario consistency < 70%, the system will judge as failure and require regeneration.**

## Code Style Consistency (Must Match)

If existing test files exist, generated code must maintain consistency with existing code style:

### Copyright Notice

- ✅ If existing code has copyright notice, generated code must have the same copyright notice format
- ❌ Forbidden: Existing code has copyright notice, generated code doesn't

### Namespace

- ✅ If existing code uses `namespace OHOS { namespace MMI { ... } }`, generated code must also use the same namespace
- ❌ Forbidden: Existing code has namespace, generated code doesn't

### Test Macro

- ✅ If existing code uses `HWTEST_F`, generated code must also use `HWTEST_F`
- ✅ If existing code uses `HWTEST`, generated code must also use `HWTEST`
- ❌ Forbidden: Existing code uses `HWTEST_F`, generated code uses `HWTEST`

### TestSize

- ✅ If existing code uses `TestSize.Level1`, generated code must also use the same TestSize format
- ❌ Forbidden: Existing code uses `TestSize.Level1`, generated code uses different TestSize

### Comment Format

- ✅ If existing code has specific comment format (e.g., `@tc.name`), generated code must also use the same comment format
- ❌ Forbidden: Existing code has `@tc.name` comments, generated code doesn't

## Test Pattern Consistency (Must Match)

### Mock Usage

- ✅ If existing code uses Mock (`MockXxx`, `EXPECT_CALL`, `ON_CALL`), generated code must also use Mock
- ✅ If existing code doesn't use Mock, generated code should not use Mock either (unless necessary)
- ❌ Forbidden: Existing code uses Mock, generated code doesn't use Mock

### Assertion Method

- ✅ If existing code mainly uses `EXPECT_`, generated code should also mainly use `EXPECT_`
- ✅ If existing code mainly uses `ASSERT_`, generated code should also mainly use `ASSERT_`
- ❌ Forbidden: Existing code mainly uses `EXPECT_`, generated code mainly uses `ASSERT_`

### Instance Access

- ✅ If existing code uses `instance_`, generated code must also use `instance_`
- ❌ Forbidden: Existing code uses `instance_`, generated code doesn't use `instance_`

### Singleton Invocation

- ✅ If existing code uses `GetInstance()`, generated code must also use the same singleton invocation method
- ❌ Forbidden: Existing code uses `GetInstance()`, generated code uses different method

## Code Structure Consistency (Must Match)

### Test Class Definition

- ✅ If existing code has test class (`class XxxTest : public ::testing::Test`), generated code must also have test class
- ❌ Forbidden: Existing code has test class, generated code doesn't

### Test Fixture

- ✅ If existing code uses `HWTEST_F`, generated code must also use `HWTEST_F` and define test fixture class
- ❌ Forbidden: Existing code uses `HWTEST_F`, generated code uses `HWTEST`

### Include Order

- ✅ If existing code has specific include order, generated code should also maintain the same include order
- ❌ Forbidden: Existing code has specific include order, generated code doesn't follow that order

### Using Namespace

- ✅ If existing code uses `using namespace`, generated code should also use the same using declarations
- ❌ Forbidden: Existing code uses `using namespace`, generated code doesn't

## Important Scenario Consistency (Critical)

### Smart Pointer Type Consistency (Highest Weight)

#### Must Match Existing Code

- ✅ If existing code uses `sptr/wptr`, generated code must also use `sptr/wptr`
- ✅ If existing code uses `std::shared_ptr`, generated code must also use `std::shared_ptr`
- ❌ Forbidden to mix: Cannot have existing use sptr but generated use shared_ptr

#### OpenHarmony Projects Uniformly Use sptr/wptr

- ✅ If existing code uses sptr/wptr, generated code must use sptr/wptr

#### Example

```cpp
// If existing code uses sptr
sptr<Service> service = new Service();
service->Method();

// Generated code must also use sptr (cannot use shared_ptr)
sptr<Service> service = new Service();
service->Method();
```

### Mock Usage Method Consistency

#### Must Match Existing Code's Mock Usage Method

- Mock class definition method (`MockXxx` vs `MockXxxClass`)
- EXPECT_CALL vs ON_CALL usage preference
- Mock object creation method

#### Example

```cpp
// If existing code uses EXPECT_CALL
auto mock = std::make_shared<MockService>();
EXPECT_CALL(*mock, Method()).WillOnce(Return(true));

// Generated code should also use EXPECT_CALL (not ON_CALL)
auto mock = std::make_shared<MockService>();
EXPECT_CALL(*mock, Method()).WillOnce(Return(true));
```

### Test Case Structure Consistency

#### Must Match Existing Code's Test Structure

- If existing code uses `HWTEST_F`, generated code must also use `HWTEST_F`
- If existing code uses `HWTEST`, generated code must also use `HWTEST`
- Test fixture class definition method must be consistent

#### Example

```cpp
// If existing code uses HWTEST_F
class ServiceTest : public ::testing::Test {
public:
    void SetUp() override { instance_ = std::make_shared<Service>(); }
    void TearDown() override { instance_.reset(); }
protected:
    std::shared_ptr<Service> instance_;
};
HWTEST_F(ServiceTest, MethodName_001, TestSize.Level1) { ... }

// Generated code must also use HWTEST_F (cannot use HWTEST)
```

### Assertion Method Consistency

#### Must Match Existing Code's Assertion Usage Preference

- If existing code mainly uses `EXPECT_`, generated code should also mainly use `EXPECT_`
- If existing code mainly uses `ASSERT_`, generated code should also mainly use `ASSERT_`
- Assertion style must be consistent

#### Example

```cpp
// If existing code mainly uses EXPECT_
EXPECT_EQ(result, ERR_OK);
EXPECT_NE(instance_, nullptr);
EXPECT_TRUE(condition);

// Generated code should also mainly use EXPECT_ (not ASSERT_)
```

### Pointer Invocation Method Consistency

#### Must Match Existing Code's Pointer Invocation Method

- If existing code mainly uses `->`, generated code should also mainly use `->`
- If existing code mainly uses `.`, generated code should also mainly use `.`

#### Example

```cpp
// If existing code mainly uses ->
instance_->Method();
ptr->Method();

// Generated code should also mainly use -> (not .)
instance_->Method();
ptr->Method();
```

### Test Case Naming Pattern Consistency

#### Must Match Existing Code's Naming Pattern

- If existing code uses numeric suffix (`_001`, `_002`), generated code must also use numeric suffix
- If existing code doesn't use numeric suffix, generated code should not use numeric suffix either

#### Example

```cpp
// If existing code uses numeric suffix
HWTEST_F(ServiceTest, MethodName_001, TestSize.Level1) { ... }
HWTEST_F(ServiceTest, MethodName_002, TestSize.Level1) { ... }

// Generated code must also use numeric suffix (cannot use MethodName)
```

### Instance Access Method Consistency

#### Must Match Existing Code's Instance Access Method

- If existing code uses `instance_`, generated code must also use `instance_`
- If existing code doesn't use `instance_`, generated code should not use `instance_` either

#### Example

```cpp
// If existing code uses instance_
class ServiceTest : public ::testing::Test {
protected:
    std::shared_ptr<Service> instance_;
};
HWTEST_F(ServiceTest, Method_001, TestSize.Level1) {
    ASSERT_NE(instance_, nullptr);
    instance_->Method();
}

// Generated code must also use instance_
```

### Special Interface Usage Consistency

#### Must Match Existing Code's Special Interface Usage

- NDK interfaces (`OH_*`): If existing code uses NDK interfaces, generated code must also use the same NDK interfaces
- NAPI interfaces (`napi_*`): If existing code uses NAPI interfaces, generated code must also use the same NAPI interfaces
- CJSON interfaces (`cJSON*`): If existing code uses CJSON interfaces, generated code must also use the same CJSON interfaces

#### Example

```cpp
// If existing code uses NDK interfaces
OH_Pasteboard* pasteboard = OH_Pasteboard_Create();
int res = OH_Pasteboard_SetData(pasteboard, data);
OH_Pasteboard_Destroy(pasteboard);

// Generated code must also use NDK interfaces
OH_Pasteboard* pasteboard = OH_Pasteboard_Create();
int res = OH_Pasteboard_SetData(pasteboard, data);
OH_Pasteboard_Destroy(pasteboard);
```

## Consistency Check Mechanism

The system automatically compares generated code with existing code, checking:

### Code Style Matching

- copyright
- namespace
- testMacro
- testSize
- commentFormat

### Test Pattern Matching

- setupTearDown
- mockUsage
- assertion
- instanceAccess
- singleton
- sptrWptr
- sharedPtr

### Code Structure Matching

- testClass
- testFixture
- testCase
- includeOrder
- usingNamespace

### Important Scenario Matching

- Smart pointer type
- Mock usage method
- Test case structure
- Assertion method
- Pointer invocation method
- Test case naming
- Instance access method
- Special interface usage

## How to Ensure Consistency

1. **Carefully read existing test files**: The system provides existing test file content in the context. Carefully read and understand their code style, test patterns, code structure.

2. **Strictly follow existing code patterns**: Generated code must be consistent with existing code in important scenarios.

3. **Prioritize reference to existing code**: If existing test files exist, prioritize referencing existing code patterns rather than using generic patterns.

4. **Check consistency**: After generating code, check if it's consistent with existing code in important scenarios.
