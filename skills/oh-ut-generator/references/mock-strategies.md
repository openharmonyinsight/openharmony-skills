# Mock Strategies

## Overview

This document specifies Mock object creation and usage strategies for OpenHarmony unit testing.

## Mock Usage Requirements

### Mock Usage Rate

- **Mock Usage**: 26.2% usage rate in OpenHarmony test files (when dependencies require mocking)

### When to Use Mock

- When the tested function depends on external services or interfaces
- When you need to control dependency behavior for testing
- When you need to verify function calls to dependencies

## Mock Object Creation

### Standard Mock Creation

```cpp
auto mock = std::make_shared<MockClass>();
```

### Mock Inheritance Strategy (Recommended)

If the original class is not final, Mock class should inherit from the original class:

```cpp
class MockClassName : public ClassName {
public:
    MOCK_METHOD(ReturnType, MethodName, (ParamType param), (override));
};
```

This allows safe pointer type conversion:
```cpp
std::shared_ptr<MockClassName> mock = std::make_shared<MockClassName>();
std::shared_ptr<ClassName> base = mock;  // Safe upcasting
```

### Independent Mock Class (Non-Inheritance)

If Mock class does not inherit from the original class (e.g., original class is final):

#### Forbidden Pattern

```cpp
// WRONG: Cannot use static_pointer_cast for non-inheriting mock
std::shared_ptr<MockClassName> mock = std::make_shared<MockClassName>();
std::shared_ptr<ClassName> base = std::static_pointer_cast<ClassName>(mock);
```

#### Recommended Solutions

**Solution 1: Adapter Pattern (Recommended)**

```cpp
// Create adapter class inheriting from original class
class ClassNameAdapter : public ClassName {
public:
    void SetMock(std::shared_ptr<MockClassName> mock) {
        mock_ = mock;
    }

    ReturnType MethodName(ParamType param) override {
        return mock_->MethodName(param);
    }

private:
    std::shared_ptr<MockClassName> mock_;
};

// In test
auto mock = std::make_shared<MockClassName>();
auto adapter = std::make_shared<ClassNameAdapter>();
adapter->SetMock(mock);
```

**Solution 2: Direct Member Assignment**

If member variables are accessible (public or via private=public macro):

```cpp
// Directly assign mock to member variable
instance_->mockDependency_ = mock;
```

**Solution 3: Use Interface/Base Class**

If original class has interface or base class:

```cpp
// Mock the interface/base class instead
class MockIInterface : public IInterface {
    // Mock methods
};
```

## EXPECT_CALL Setup

### Basic EXPECT_CALL

```cpp
EXPECT_CALL(*mock, Method())
    .WillOnce(Return(value));
```

### Multiple Calls

```cpp
EXPECT_CALL(*mock, Method())
    .Times(2)
    .WillRepeatedly(Return(value));
```

### With Parameter Matching

```cpp
EXPECT_CALL(*mock, Method(Eq(expectedParam)))
    .WillOnce(Return(value));

// Wildcard matcher
EXPECT_CALL(*mock, Method(_))
    .WillOnce(Return(value));
```

### ON_CALL for Default Behavior

```cpp
ON_CALL(*mock, Method())
    .WillByDefault(Return(defaultValue));
```

## Mock Usage Requirements (Critical)

### Must Use Mock If Created

If a Mock object is created, it must be used in the test:

```cpp
// CORRECT: Mock created and used
auto mock = std::make_shared<MockService>();
EXPECT_CALL(*mock, Method()).WillOnce(Return(true));
instance_->SetMock(mock);
```

### Forbidden Patterns

```cpp
// WRONG: Mock created but not used
auto mock = std::make_shared<MockService>();
// No EXPECT_CALL or ON_CALL setup

// WRONG: Mock created but only commented
auto mock = std::make_shared<MockService>();
// TODO: should use mock for testing

// WRONG: Mock created in SetUp but not used in test cases
void SetUp() override {
    mock_ = std::make_shared<MockService>();
    // Never referenced in test cases
}
```

## Singleton Mock Strategy

Singletons are challenging to mock. Use the following strategies:

### Strategy 1: Mock Singleton's Return Value (Recommended)

If singleton returns an interface pointer:

```cpp
// Mock the interface
auto mockService = std::make_shared<MockIService>();

// Inject mock if testing framework supports it
// Or use test-specific initialization
```

### Strategy 2: Use Test Friend Class or Macro Injection

If singleton class supports test injection:

```cpp
class SingletonClass {
    friend class SingletonClassTest;

#ifdef TEST_MODE
    static void SetTestInstance(std::shared_ptr<SingletonClass> instance) {
        instance_ = instance;
    }
#endif
};

// In test
auto mockInstance = std::make_shared<MockSingletonClass>();
SingletonClass::SetTestInstance(mockInstance);
```

### Strategy 3: Dependency Injection

Refactor code to support dependency injection:

```cpp
class ConsumerClass {
public:
    ConsumerClass(std::shared_ptr<IService> service = nullptr)
        : service_(service ? service : SingletonClass::GetInstance()) {}

private:
    std::shared_ptr<IService> service_;
};

// In test
auto mock = std::make_shared<MockIService>();
ConsumerClass consumer(mock);
```

## Mock Verification

### Verify Mock Calls

```cpp
// After test execution
Mock::VerifyAndClearExpectations(mock.get());
```

### Expect Call Count

```cpp
EXPECT_CALL(*mock, Method())
    .Times(AtLeast(1));

EXPECT_CALL(*mock, Method())
    .Times(Exactly(2));
```

## Mock Usage Examples

### Basic Mock Example

```cpp
auto mockObserver = std::make_shared<MockObserver>();
EXPECT_CALL(*mockObserver, OnEvent(_)).WillOnce(Return(true));
instance_->SetObserver(mockObserver);
```

### Mock with Multiple Methods

```cpp
auto mockService = std::make_shared<MockService>();
EXPECT_CALL(*mockService, Initialize()).WillOnce(Return(true));
EXPECT_CALL(*mockService, ProcessData(_)).WillOnce(Return(ERR_OK));
instance_->SetService(mockService);
```

### Mock with Callback

```cpp
auto mockCallback = std::make_shared<MockCallback>();
EXPECT_CALL(*mockCallback, OnComplete(Eq(ERR_OK), _))
    .WillOnce(WithArg<1>([](const Data& data) {
        EXPECT_EQ(data.size(), 10);
    }));
```

## Mock Consistency with Existing Code

When existing test files exist, generated code must maintain consistency:

### Mock Class Definition Style

- If existing code uses `MockXxx`, generated code should use `MockXxx`
- If existing code uses `MockXxxClass`, generated code should use `MockXxxClass`

### EXPECT_CALL vs ON_CALL Preference

- If existing code mainly uses EXPECT_CALL, generated code should mainly use EXPECT_CALL
- If existing code mainly uses ON_CALL, generated code should mainly use ON_CALL

### Mock Object Creation Style

- Match existing code's mock object creation pattern
