# Smart Pointer Usage

## Overview

This document specifies smart pointer usage rules for OpenHarmony unit tests.

## Strict Matching Principle

**Smart pointer usage in test code must be consistent with the original function.**

### Matching Rules

- ✅ If original function uses sptr/wptr: Test code must also use `sptr<T>` (strong reference) and `wptr<T>` (weak reference)
- ✅ If original function uses std::shared_ptr/std::unique_ptr: Test code must also use corresponding standard smart pointers
- ✅ If original function uses raw pointers: Test code can use smart pointers to wrap, but parameter types must match the original function

### Forbidden Patterns

- ❌ Original function doesn't use sptr/wptr, but test code uses sptr/wptr
- ❌ Original function uses sptr/wptr, but test code uses std::shared_ptr/std::unique_ptr

## OpenHarmony sptr/wptr Usage

### sptr (Strong Reference)

When original function uses sptr:

```cpp
// sptr creation
sptr<ClassName> obj = new ClassName();
sptr<ClassName> obj = MakeSptr<ClassName>();

// sptr usage
obj->Method();

// sptr in test fixture
void SetUp() override {
    instance_ = MakeSptr<YourService>();
    // or: instance_ = new YourService();
}
void TearDown() override {
    instance_ = nullptr;
}
```

### wptr (Weak Reference)

When original function uses wptr (avoiding circular references):

```cpp
// wptr creation
wptr<ClassName> weakObj = obj;

// wptr to sptr promotion
sptr<ClassName> strong = weakObj.promote();
if (strong != nullptr) {
    strong->Method();
}
```

### sptr Conversion

```cpp
// Upcasting (automatic)
sptr<BaseClass> base = MakeSptr<DerivedClass>();

// Downcasting (requires sptr_cast)
sptr<DerivedClass> derived = sptr_cast<DerivedClass>(base);
```

### sptr/wptr Example

```cpp
class ServiceTest : public ::testing::Test {
public:
    void SetUp() override {
        service_ = MakeSptr<Service>();
        weakService_ = service_;  // Create weak reference
    }
    void TearDown() override {
        service_ = nullptr;
        weakService_.clear();
    }

protected:
    sptr<Service> service_;
    wptr<Service> weakService_;
};

HWTEST_F(ServiceTest, MethodName_001, TestSize.Level1) {
    // Use strong reference
    service_->Method();

    // Promote weak reference to strong
    sptr<Service> strong = weakService_.promote();
    if (strong != nullptr) {
        strong->Method();
    }
}
```

## Standard Smart Pointer Usage

### std::shared_ptr

When original function uses std::shared_ptr:

```cpp
// shared_ptr creation
std::shared_ptr<ClassName> obj = std::make_shared<ClassName>();

// shared_ptr usage
obj->Method();

// shared_ptr in test fixture
void SetUp() override {
    instance_ = std::make_shared<YourService>();
}
void TearDown() override {
    instance_.reset();
}
```

### std::unique_ptr

When original function uses std::unique_ptr:

```cpp
// unique_ptr creation
std::unique_ptr<ClassName> obj = std::make_unique<ClassName>();

// unique_ptr usage
obj->Method();
```

## Raw Pointer Usage

### Matching Original Function

If original function uses raw pointers, test code parameter types must match:

```cpp
// Original function signature
void Function(ClassName* ptr);

// Test code
HWTEST_F(Test, Function_001, TestSize.Level1) {
    ClassName* ptr = new ClassName();
    Function(ptr);
    delete ptr;  // Must clean up
}
```

### Smart Pointer Wrapping

Test code can use smart pointers internally, but parameter types must match:

```cpp
// Original function signature
void Function(ClassName* ptr);

// Test code with smart pointer wrapping
HWTEST_F(Test, Function_001, TestSize.Level1) {
    auto obj = std::make_unique<ClassName>();
    Function(obj.get());  // Pass raw pointer to match signature
    // obj automatically cleaned up
}
```

## Memory Management Requirements

### Forbidden Patterns

```cpp
// WRONG: Use new without delete (unless wrapped in smart pointer)
ClassName* ptr = new ClassName();
// No delete - memory leak

// WRONG: Use new[] without delete[]
int* array = new int[10];
// Must use std::vector instead

// CORRECT: Use smart pointers
auto ptr = std::make_unique<ClassName>();
auto array = std::vector<int>(10);
```

### Correct Patterns

```cpp
// CORRECT: Use sptr
sptr<ClassName> obj = new ClassName();

// CORRECT: Use std::shared_ptr
std::shared_ptr<ClassName> obj = std::make_shared<ClassName>();

// CORRECT: Use std::unique_ptr
std::unique_ptr<ClassName> obj = std::make_unique<ClassName>();
```

## Code Style Consistency

### Match Existing Code

If existing test files exist:

- ✅ If existing code uses `sptr/wptr`, generated code must also use `sptr/wptr`
- ✅ If existing code uses `std::shared_ptr`, generated code must also use `std::shared_ptr`
- ❌ Forbidden to mix: Cannot have existing use sptr but generated use shared_ptr

### OpenHarmony Projects Uniformly Use sptr/wptr

If existing code uses sptr/wptr, generated code must use sptr/wptr.

## Best Practices

### ✅ Recommended

- Match original function's smart pointer usage exactly
- Use sptr for OpenHarmony code that uses sptr
- Use wptr to avoid circular references
- Use std::shared_ptr for standard C++ code
- Use std::unique_ptr for exclusive ownership
- Use std::vector instead of new[]

### ❌ Forbidden

- Mix sptr/wptr with std::shared_ptr/std::unique_ptr
- Use new without smart pointer wrapping (unless explicit delete)
- Use new[] for arrays (must use std::vector)
- Forget to clean up raw pointers
