# Coverage Requirements

## Overview

This document specifies the coverage requirements for OpenHarmony unit tests.

## Coverage Metrics

### Minimum Requirements (Mandatory)

- **Branch Coverage**: All branches (if/else, switch, ternary operators, etc.) must be covered at least **75%**
- **Line Coverage**: All code lines must be covered at least **75%**

### Challenge Goals (Should Strive to Achieve)

- **Branch Coverage**: Strive to achieve **85%** or higher
- **Line Coverage**: Strive to achieve **85%** or higher

## Coverage Scope Requirements

### Boundary Conditions

Must test all boundary values:

- Null values (nullptr, empty strings, empty containers)
- Maximum values (INT_MAX, size limits, buffer limits)
- Minimum values (INT_MIN, negative numbers)
- Critical values (edge cases, boundary transitions)

### Exception Paths

Must test all error return codes and exception cases:

- All error code return paths
- All exception handling paths
- All error condition branches
- Resource failure scenarios

### Normal Paths

Must test all normal execution flows:

- Happy path scenarios
- Typical usage patterns
- Standard parameter ranges
- Common workflows

### Conditional Branches

Each if/else, switch case must have corresponding test cases:

- Every if condition: true and false cases
- Every switch case: each case value
- Ternary operators: both conditions
- Logical operator short-circuits

## Coverage Implementation Strategy

### Analyze Function Branch Points

Identify all branch points in the function:

- `if`, `else if`, `else` statements
- `switch` statements and `case` values
- Ternary operators (`?:`)
- Logical operator short-circuits (`&&`, `||`)

### Create Independent Test Cases for Each Branch

For each branch, create separate test cases:

- **Normal branch**: Typical valid input
- **Exception branch**: Error conditions, invalid input
- **Boundary branch**: Edge cases, limits

### Use Parameterized Tests

Cover multiple input combinations:

```cpp
class ParametrizedTest : public testing::TestWithParam<std::tuple<int, int>> {
    // Test implementation
};

INSTANTIATE_TEST_CASE_P(
    ParametrizedTests,
    ParametrizedTest,
    ::testing::Values(
        std::make_tuple(1, 1),
        std::make_tuple(0, 0),
        std::make_tuple(-1, -1)
    )
);
```

### Use Mock to Control Dependency Behavior

Ensure all code paths can be triggered:

```cpp
// Mock to return success
EXPECT_CALL(*mock, Method()).WillOnce(Return(ERR_OK));

// Mock to return error
EXPECT_CALL(*mock, Method()).WillOnce(Return(ERR_INVALID_PARAMETER));

// Mock to throw exception
EXPECT_CALL(*mock, Method()).WillOnce(Throw(std::runtime_error("error")));
```

### Verify All Return Values and Side Effects

- Check all possible return values
- Verify state changes
- Check side effects (parameter modification, callback calls)

## Coverage Improvement Tips

### Identify Uncovered Branches

After generating tests, identify uncovered code:

- Use coverage tools (gcov, lcov)
- Analyze coverage reports
- Check which branches are not executed

### Add Corresponding Test Cases

For each uncovered branch:

- Create test case that triggers the branch
- Ensure test data satisfies branch condition
- Verify expected behavior for that branch

### Use Combinatorial Tests

Cover multiple condition combinations:

```cpp
// Test multiple parameter combinations
TEST_P(CombinatorialTest, VariousCombinations) {
    auto [param1, param2, param3] = GetParam();
    // Test with different combinations
}
```

### Test All Error Code Return Paths

```cpp
// Test each error code
HWTEST_F(FuncTest, Func_InvalidParam, TestSize.Level1) {
    EXPECT_EQ(func(nullptr), ERR_INVALID_PARAMETER);
}

HWTEST_F(FuncTest, Func_InvalidValue, TestSize.Level1) {
    EXPECT_EQ(func(invalidValue), ERR_INVALID_VALUE);
}

HWTEST_F(FuncTest, Func_NoMemory, TestSize.Level1) {
    // Mock to simulate out of memory
    EXPECT_EQ(func(), ERR_NO_MEMORY);
}
```

### Test All Boundary Values

```cpp
// Test boundary conditions
HWTEST_F(FuncTest, Func_MaxValue, TestSize.Level1) {
    EXPECT_EQ(func(INT_MAX), expectedMaxResult);
}

HWTEST_F(FuncTest, Func_MinValue, TestSize.Level1) {
    EXPECT_EQ(func(INT_MIN), expectedMinResult);
}

HWTEST_F(FuncTest, Func_ZeroValue, TestSize.Level1) {
    EXPECT_EQ(func(0), expectedZeroResult);
}
```

## Branch-Assertion Correspondence (Critical)

### Must Analyze Branch-Error Code Mapping

Test case assertions must completely correspond to function's branch logic:

### Example: Correct Implementation

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
    EXPECT_EQ(result, ERR_INVALID_PARAMETER);  // CORRECT: Assert corresponding error code
}

// Test case 2: Test value < 0 branch
HWTEST_F(FuncTest, Func_003, TestSize.Level1) {
    int value = -1;  // Construct test data satisfying condition
    int result = func(&value);
    EXPECT_EQ(result, ERR_INVALID_VALUE);  // CORRECT: Assert corresponding error code
}

// Test case 3: Test normal path
HWTEST_F(FuncTest, Func_001, TestSize.Level1) {
    int value = 10;
    int result = func(&value);
    EXPECT_EQ(result, ERR_OK);  // CORRECT: Normal path returns ERR_OK
}
```

### Example: Incorrect Implementation

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

## Coverage Checking

After generating tests:

1. Ensure coverage reaches 75% or higher (mandatory)
2. Strive for 85% or higher (goal)
3. Identify uncovered branches and add corresponding test cases
4. Use combinatorial tests to cover multiple condition combinations
5. Test all error code return paths
6. Test all boundary values and critical values

## Forbidden Patterns

### Testing Only One Simple Scenario

```cpp
// WRONG: Only one simple test case
HWTEST_F(FuncTest, Func_001, TestSize.Level1) {
    EXPECT_EQ(func(10), ERR_OK);  // Only tests normal path
}
```

### Ignoring Conditional Branches

```cpp
// WRONG: Missing if/else test cases
// Function: if (condition) { ... } else { ... }
HWTEST_F(FuncTest, Func_001, TestSize.Level1) {
    func(true);  // Only tests if branch, missing else branch
}
```

### Only Normal Path Testing

```cpp
// WRONG: Only normal path, missing exception paths
HWTEST_F(FuncTest, Func_001, TestSize.Level1) {
    EXPECT_EQ(func(validParam), ERR_OK);  // Only normal path
}
```

## Coverage Best Practices

### ✅ Recommended

- Analyze all branch points before writing tests
- Create test cases for each branch (normal, exception, boundary)
- Use parameterized tests for multiple input combinations
- Use Mock to control dependency behavior
- Verify all return values and side effects
- Check coverage after generating tests
- Add test cases for uncovered branches

### ❌ Forbidden

- Only test one simple scenario
- Ignore conditional branches
- Only test normal path
- Ignore error code return paths
- Randomly select error codes (must match branch logic)
- Generate test cases with only comments
