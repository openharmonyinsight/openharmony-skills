# Security Coding Requirements

## Overview

This document specifies security coding requirements for OpenHarmony unit tests.

**Important**: Forbidden to generate test code containing security coding issues! The system will automatically detect and report security risks.

## Memory Management

### Strict Matching Principle

Smart pointer usage in test code must be consistent with the original function.

### Match Original Function's Usage Pattern

- ✅ If original function uses sptr/wptr: Test code must also use `sptr<T>` (strong reference) and `wptr<T>` (weak reference)
- ✅ If original function uses std::shared_ptr/std::unique_ptr: Test code must also use corresponding standard smart pointers
- ✅ If original function uses raw pointers: Test code can use smart pointers to wrap, but parameter types must match the original function

### OpenHarmony sptr/wptr Usage

#### sptr Creation

```cpp
sptr<ClassName> obj = new ClassName();
sptr<ClassName> obj = MakeSptr<ClassName>();
```

#### wptr Creation

```cpp
wptr<ClassName> weakObj = obj;  // For weak reference, avoiding circular references
```

#### sptr Conversion

```cpp
// Upcasting (automatic)
sptr<Base> base = obj;

// Downcasting (requires sptr_cast)
sptr<Derived> derived = sptr_cast<Derived>(base);
```

#### wptr to sptr Promotion

```cpp
sptr<ClassName> strong = weakObj.promote();  // Promote weak reference to strong reference
if (strong != nullptr) {
    strong->Method();
}
```

### Forbidden Patterns

```cpp
// WRONG: Original function doesn't use sptr/wptr, but test code uses sptr/wptr

// WRONG: Original function uses sptr/wptr, but test code uses std::shared_ptr/std::unique_ptr

// WRONG: Use new to allocate memory without using smart pointers (unless there's explicit delete)
ClassName* ptr = new ClassName();
// No delete - memory leak

// WRONG: Use new[] to allocate arrays, must use std::vector
int* array = new int[10];
delete[] array;  // Must use std::vector instead
```

### Correct Patterns

```cpp
// CORRECT: Use sptr when original function uses sptr
sptr<Service> service = MakeSptr<Service>();

// CORRECT: Use std::shared_ptr when original function uses std::shared_ptr
std::shared_ptr<Service> service = std::make_shared<Service>();

// CORRECT: Use std::vector instead of new[]
std::vector<int> array(10);
```

## Variable Initialization

### Requirement

All variables must be initialized at declaration or before use.

### Forbidden Pattern

```cpp
// WRONG: Declare uninitialized variable
int count;
int result = count;  // Undefined behavior
```

### Correct Pattern

```cpp
// CORRECT: Initialize at declaration
int count = 0;
int result = count;

// CORRECT: Initialize before use
int count;
count = 0;
int result = count;
```

## Boundary Checks

### Requirement

Must check boundaries before array/container access or use `.at()` method.

### Forbidden Pattern

```cpp
// WRONG: Direct array access without boundary check
int array[10];
int value = array[20];  // Out of bounds access

// WRONG: Vector access without boundary check
std::vector<int> vec;
int value = vec[100];  // Undefined behavior
```

### Correct Patterns

```cpp
// CORRECT: Check boundary before access
int array[10];
int index = 5;
if (index >= 0 && index < 10) {
    int value = array[index];
}

// CORRECT: Use .at() method (throws exception if out of bounds)
std::vector<int> vec;
// ... add elements to vec ...
try {
    int value = vec.at(5);  // Throws std::out_of_range if out of bounds
} catch (const std::out_of_range& e) {
    // Handle error
}

// CORRECT: Check size before access
std::vector<int> vec;
if (vec.size() > 5) {
    int value = vec[5];
}
```

## Null Pointer Checks

### Requirement

Must check if pointer is `nullptr` before use.

### Forbidden Pattern

```cpp
// WRONG: Direct pointer dereference without null check
int* ptr = /* ... */;
int value = *ptr;  // Undefined behavior if ptr is nullptr
```

### Correct Pattern

```cpp
// CORRECT: Check null pointer before dereference
int* ptr = /* ... */;
if (ptr != nullptr) {
    int value = *ptr;
}

// CORRECT: Use assertion for critical pointers
int* ptr = /* ... */;
ASSERT_NE(ptr, nullptr);  // Test will fail if ptr is nullptr
int value = *ptr;
```

## Return Value Checks

### Requirement

Return values of critical functions must be checked.

### Forbidden Pattern

```cpp
// WRONG: Ignore return value of critical function
int result = dangerousFunction();
// No check - error is ignored

// WRONG: Ignore return value of find
auto it = map.find(key);
map.erase(it);  // Undefined behavior if it == map.end()

// WRONG: Ignore return value of at()
try {
    int value = vec.at(100);
} catch (...) {
    // Error caught but not properly handled
}
```

### Correct Patterns

```cpp
// CORRECT: Check return value
int result = dangerousFunction();
if (result != ERR_OK) {
    // Handle error
}

// CORRECT: Check iterator before using
auto it = map.find(key);
if (it != map.end()) {
    map.erase(it);
}

// CORRECT: Check return value and handle error
int value;
int ret = getValue(&value);
EXPECT_EQ(ret, ERR_OK);  // In tests, use assertion
if (ret == ERR_OK) {
    // Use value
}
```

## Smart Pointer Matching with Original Function

### sptr/wptr Matching

```cpp
// If original function uses sptr
class Service {
    sptr<Dependency> dep_;
};

// Test code must also use sptr
sptr<MockDependency> mock = MakeSptr<MockDependency>();
```

### std::shared_ptr Matching

```cpp
// If original function uses std::shared_ptr
class Service {
    std::shared_ptr<Dependency> dep_;
};

// Test code must also use std::shared_ptr
std::shared_ptr<MockDependency> mock = std::make_shared<MockDependency>();
```

## Code Style Consistency

### Match Existing Code

If existing test files exist:

- ✅ If existing code uses `sptr/wptr`, generated code must also use `sptr/wptr`
- ✅ If existing code uses `std::shared_ptr`, generated code must also use `std::shared_ptr`
- ❌ Forbidden: Cannot have existing use sptr but generated use shared_ptr

### OpenHarmony Projects Uniformly Use sptr/wptr

If existing code uses sptr/wptr, generated code must use sptr/wptr.

## Automatic Security Issue Detection

The system will automatically detect the following security issues:

1. **Memory management violations**
   - Using new without smart pointers
   - Using new[] instead of std::vector
   - Memory leaks

2. **Uninitialized variables**
   - Variables declared but not initialized

3. **Boundary violations**
   - Array/container access without boundary check

4. **Null pointer violations**
   - Pointer dereference without null check

5. **Return value violations**
   - Ignoring critical function return values

**The system will automatically detect the above security issues and provide specific repair suggestions in the next round.**

## Security Coding Best Practices

### ✅ Recommended

- Use smart pointers (sptr/wptr or std::shared_ptr/std::unique_ptr) for memory management
- Initialize all variables at declaration or before use
- Check boundaries before array/container access
- Check null pointers before dereference
- Check return values of critical functions
- Use `.at()` method for container access with exception handling
- Match smart pointer usage with original function

### ❌ Forbidden

- Use new/delete for memory management (unless absolutely necessary)
- Use new[]/delete[] for arrays (use std::vector instead)
- Declare uninitialized variables
- Access arrays/containers without boundary checks
- Dereference pointers without null checks
- Ignore critical function return values
- Mix sptr/wptr with std::shared_ptr/std::unique_ptr
