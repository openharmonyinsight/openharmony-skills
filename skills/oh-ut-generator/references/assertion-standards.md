# Assertion Standards

## Overview

This document specifies assertion method usage standards for OpenHarmony unit tests.

## Assertion Method Usage Statistics

Based on OpenHarmony codebase analysis (6238 test files, 3960 UT tests):

| Assertion | Usage Rate | Description |
|-----------|-----------|-------------|
| EXPECT_EQ | 74.2% | Compare equal values (most common) |
| EXPECT_TRUE | 43.2% | Verify condition is true |
| EXPECT_NE | 34.4% | Compare unequal values |
| EXPECT_FALSE | 29.3% | Verify condition is false |
| ASSERT_TRUE | 27.1% | Assert condition is true (terminates on failure) |
| ASSERT_NE | 25.1% | Assert inequality (terminates on failure) |
| ASSERT_EQ | 23.9% | Assert equality (terminates on failure) |

## Assertion Methods

### EXPECT_EQ (74.2% usage rate)

Most commonly used assertion for comparing equal values.

```cpp
EXPECT_EQ(result, ERR_OK);
EXPECT_EQ(actualValue, expectedValue);
```

### EXPECT_TRUE (43.2% usage rate)

Used to verify condition is true.

```cpp
EXPECT_TRUE(condition);
EXPECT_TRUE(success);
```

### EXPECT_NE (34.4% usage rate)

Used to compare unequal values.

```cpp
EXPECT_NE(instance_, nullptr);
EXPECT_NE(result, ERR_OK);
```

### EXPECT_FALSE (29.3% usage rate)

Used to verify condition is false.

```cpp
EXPECT_FALSE(condition);
EXPECT_FALSE(isEmpty);
```

### ASSERT_* Methods

Used when test should terminate immediately on failure:

```cpp
ASSERT_NE(instance_, nullptr);  // Must check instance
ASSERT_TRUE(pointer != nullptr);
ASSERT_EQ(result, ERR_OK);
```

## Branch-Assertion Correspondence (Critical)

### Fundamental Requirement

**Branch assertions must completely correspond to branch logic.**

Test case assertions must match the function's branch logic exactly. Random error code selection is forbidden.

### System Analysis

The system automatically analyzes the function's branch structure and identifies the error code corresponding to each branch condition.

### Test Case Generation Rule

Generate test cases according to branch-error code mapping:

```cpp
// Function implementation:
// if (ptr == nullptr) {
//     return ERR_INVALID_PARAMETER;
// }
// if (value < 0) {
//     return ERR_INVALID_VALUE;
// }
// return ERR_OK;

// Test case 1: Test ptr == nullptr branch
HWTEST_F(FuncTest, Func_002, TestSize.Level1) {
    int result = func(nullptr);  // Construct test data satisfying condition
    EXPECT_EQ(result, ERR_INVALID_PARAMETER);  // CORRECT: Must assert corresponding error code
}

// Test case 2: Test value < 0 branch
HWTEST_F(FuncTest, Func_003, TestSize.Level1) {
    int value = -1;  // Construct test data satisfying condition
    int result = func(&value);
    EXPECT_EQ(result, ERR_INVALID_VALUE);  // CORRECT: Must assert corresponding error code
}

// Test case 3: Test normal path
HWTEST_F(FuncTest, Func_001, TestSize.Level1) {
    int value = 10;
    int result = func(&value);
    EXPECT_EQ(result, ERR_OK);  // CORRECT: Normal path returns ERR_OK
}
```

### Incorrect Examples

```cpp
// WRONG: Pass nullptr but assert ERR_OK
HWTEST_F(FuncTest, Func_002, TestSize.Level1) {
    int result = func(nullptr);
    EXPECT_EQ(result, ERR_OK);  // WRONG: ptr == nullptr should return ERR_INVALID_PARAMETER
}

// WRONG: Random error code selection
HWTEST_F(FuncTest, Func_002, TestSize.Level1) {
    int result = func(nullptr);
    EXPECT_EQ(result, ERR_INVALID_VALUE);  // WRONG: Should return ERR_INVALID_PARAMETER, not ERR_INVALID_VALUE
}
```

## Return Value Assertions

### Functions with Return Values

Must assert return value explicitly:

```cpp
// CORRECT: Use EXPECT_EQ with specific expected value
EXPECT_EQ(result, ERR_OK);
EXPECT_EQ(value, expected);

// CORRECT: Use EXPECT_NE for inequality
EXPECT_NE(result, ERR_OK);

// WRONG: Vague assertion with || operator
EXPECT_TRUE(result == ERR_OK || result == ERR_INVALID_VALUE);
```

### Void Functions

Must assert side effects or state changes.

See "Void Function Assertions" section below.

## Void Function Assertions

### Parameter Modification Verification

If function modifies parameters via pointer/reference:

```cpp
void SetValue(int* value, int newVal) { *value = newVal; }

// Test must include:
HWTEST_F(ValueTest, SetValue_001, TestSize.Level1) {
    int val = 0;
    SetValue(&val, 42);
    EXPECT_EQ(val, 42);  // CORRECT: Verify parameter was modified
}
```

### Global Variable/State Verification

If function modifies global variables or object state:

```cpp
void ResetCounter() { g_counter = 0; }

// Test must include:
HWTEST_F(CounterTest, ResetCounter_001, TestSize.Level1) {
    g_counter = 100;
    ResetCounter();
    EXPECT_EQ(g_counter, 0);  // CORRECT: Verify global variable was modified
}
```

### Callback Function Call Verification

If function calls callback:

```cpp
void ProcessData(void (*callback)(int)) { callback(42); }

// Test must include:
HWTEST_F(ProcessTest, ProcessData_001, TestSize.Level1) {
    auto mockCallback = [](int val) { EXPECT_EQ(val, 42); };
    ProcessData(mockCallback);  // CORRECT: Verify callback was called
}
```

### Object State Verification

If function modifies object member variables:

```cpp
void MyStruct::SetFlag(bool flag) { flag_ = flag; }

// Test must include:
HWTEST_F(MyStructTest, SetFlag_001, TestSize.Level1) {
    MyStruct obj;
    obj.SetFlag(true);
    EXPECT_TRUE(obj.GetFlag());  // CORRECT: Verify object state
}
```

### Container/Array Modification Verification

If function adds/deletes/modifies elements in container:

```cpp
void AddItem(std::vector<int>& vec, int value) { vec.push_back(value); }

// Test must include:
HWTEST_F(ContainerTest, AddItem_001, TestSize.Level1) {
    std::vector<int> vec;
    AddItem(vec, 42);

    EXPECT_EQ(vec.size(), 1);  // Verify size
    EXPECT_EQ(vec[0], 42);  // CORRECT: Must verify added element content
}
```

### Void Function Comment Reminder

For void function tests, add reminder comment at end of test function:

```cpp
HWTEST_F(ConnectionTest, SoftbusConnGeneralConnection_001, TestSize.Level1) {
    // Prepare test data
    int param = 0;

    // Call tested function
    SoftbusConnGeneralConnection(&param);

    // Verify side effects
    EXPECT_EQ(param, expectedValue);  // Verify parameter was modified

    // TODO: Please note to add effective assertions, verify side effects (parameter modification, state changes, callback calls, etc.)
}
```

## Forbidden Assertion Patterns

### Vague Assertions with || Operator

```cpp
// WRONG: Multiple error codes with ||
EXPECT_TRUE(result == ERR_OK || result == ERR_INVALID_VALUE);

// CORRECT: Separate test cases for each error code
HWTEST_F(FuncTest, Func_Success, TestSize.Level1) {
    EXPECT_EQ(func(validParam), ERR_OK);
}

HWTEST_F(FuncTest, Func_InvalidParam, TestSize.Level1) {
    EXPECT_EQ(func(invalidParam), ERR_INVALID_VALUE);
}
```

### Always-True Assertions

```cpp
// WRONG: Always true
EXPECT_TRUE(result == ERR_OK || result != ERR_OK);

// WRONG: Always true
EXPECT_TRUE(condition || !condition);
```

### No Assertions in Void Functions

```cpp
// WRONG: No assertions after function call
HWTEST_F(FuncTest, Func_001, TestSize.Level1) {
    Func();  // No verification
}

// CORRECT: Verify side effects
HWTEST_F(FuncTest, Func_001, TestSize.Level1) {
    int value = 0;
    Func(&value);
    EXPECT_EQ(value, expected);  // Verify side effect
}
```

## Assertion Consistency with Existing Code

### Match Existing Assertion Style

If existing test files exist:

- If existing code mainly uses `EXPECT_`, generated code should mainly use `EXPECT_`
- If existing code mainly uses `ASSERT_`, generated code should mainly use `ASSERT_`

### Example

```cpp
// If existing code mainly uses EXPECT_
EXPECT_EQ(result, ERR_OK);
EXPECT_NE(instance_, nullptr);
EXPECT_TRUE(condition);

// Generated code should also mainly use EXPECT_ (not ASSERT_)
```

## Assertion Best Practices

### ✅ Recommended

- Use EXPECT_EQ for comparing values
- Use EXPECT_NE for inequality checks
- Use EXPECT_TRUE/EXPECT_FALSE for boolean conditions
- Use ASSERT_* for critical preconditions
- Match branch assertions with branch logic exactly
- For void functions, verify side effects
- Add reminder comments for void function tests

### ❌ Forbidden

- Use vague assertions with || operator
- Use always-true assertions (condition || !condition)
- Omit assertions in void functions
- Randomly select error codes (must match branch logic)
- Only use EXPECT_NO_THROW without other verification
