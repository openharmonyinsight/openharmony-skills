# Stability Code Review Guidelines

## Overview

Stability focuses on error handling, boundary conditions, and predictable behavior under all circumstances. Unstable code causes crashes, undefined behavior, and inconsistent results.

## Key Principles

1. **Never crash** - Handle all error paths gracefully
2. **Validate all inputs** - Trust no external data
3. **Handle boundary conditions** - Test edge cases explicitly
4. **Fail safely** - When errors occur, degrade gracefully

## Code Review Checklist

### Error Handling

**Check for:**
- [ ] All return values are checked
- [ ] All error paths are tested
- [ ] No silent failures (always log errors)
- [ ] Proper error propagation up the call stack
- [ ] Resources cleaned up on error paths

**Red Flags:**

```cpp
// ❌ BAD: Unchecked return value
void ProcessData() {
    ParseData(input);  // What if it fails?
}

// ❌ BAD: Silent failure
bool ProcessData() {
    if (!Validate(input)) {
        return false;  // No logging
    }
}

// ❌ BAD: Ignoring errors
void SaveToFile(const std::string& path) {
    FILE* fp = fopen(path.c_str(), "w");
    fprintf(fp, "%s", data.c_str());  // fp could be nullptr
    fclose(fp);
}

// ✅ GOOD: Comprehensive error handling
Result<Data> ProcessData() {
    auto result = ParseData(input);
    if (!result.IsValid()) {
        LOGE("Failed to parse data: %{public}s", result.GetError().message);
        return result.GetError();
    }

    if (!Validate(result.GetValue())) {
        LOGE("Data validation failed");
        return Error(ErrorType::VALIDATION, "Validation failed");
    }

    return result.GetValue();
}

// ✅ GOOD: Resource cleanup on error
bool SaveToFile(const std::string& path, const std::string& data) {
    FILE* fp = fopen(path.c_str(), "w");
    if (!fp) {
        LOGE("Failed to open file: %{public}s, error: %{public}s",
             path.c_str(), strerror(errno));
        return false;
    }

    if (fprintf(fp, "%s", data.c_str()) < 0) {
        LOGE("Failed to write to file: %{public}s", path.c_str());
        fclose(fp);
        return false;
    }

    fclose(fp);
    return true;
}
```

### Boundary Conditions

**Check for:**
- [ ] Empty collections (vectors, strings, maps)
- [ ] Collection boundaries (first, last)
- [ ] Integer boundaries (INT_MIN, INT_MAX, 0, -1)
- [ ] Floating point special values (NaN, Inf, -Inf)
- [ ] Null pointers/optional values
- [ ] Array/vector bounds checking

**Red Flags:**

```cpp
// ❌ BAD: No boundary checking
int GetItem(const std::vector<int>& items, int index) {
    return items[index];  // Crash if out of bounds
}

// ❌ BAD: Assumes non-empty
std::string GetFirstName(const std::string& full_name) {
    return full_name.substr(0, full_name.find(' '));  // Bad if empty
}

// ❌ BAD: Integer overflow
int CalculateTotal(int count, int value) {
    return count * value;  // Can overflow
}

// ✅ GOOD: Complete boundary checking
std::optional<int> GetItem(const std::vector<int>& items, size_t index) {
    if (index >= items.size()) {
        LOGE("Index out of bounds: %{public}zu, size: %{public}zu",
             index, items.size());
        return std::nullopt;
    }
    return items[index];
}

// ✅ GOOD: Handle empty strings
std::string GetFirstName(const std::string& full_name) {
    if (full_name.empty()) {
        LOGW("Empty name provided");
        return "";
    }

    size_t space_pos = full_name.find(' ');
    if (space_pos == std::string::npos) {
        return full_name;
    }

    return full_name.substr(0, space_pos);
}

// ✅ GOOD: Check for overflow
bool CalculateTotal(int count, int value, int& out_result) {
    if (count == 0 || value == 0) {
        out_result = 0;
        return true;
    }

    if (count > 0 && value > 0 && count > INT_MAX / value) {
        LOGE("Integer overflow: %{public}d * %{public}d", count, value);
        return false;
    }

    if (count < 0 && value < 0 && count < INT_MAX / value) {
        LOGE("Integer overflow: %{public}d * %{public}d", count, value);
        return false;
    }

    out_result = count * value;
    return true;
}

// ✅ GOOD: Floating point safety
bool IsValidCoordinate(double x, double y) {
    return std::isfinite(x) && std::isfinite(y);
}
```

### State Validation

**Check for:**
- [ ] Object state is valid before operations
- [ ] Invalid states are detected and reported
- [ ] State transitions are validated
- [ ] No operations on destroyed/invalid objects

**Red Flags:**

```cpp
// ❌ BAD: No state validation
void MenuPattern::SelectItem(int index) {
    items_[index].selected = true;  // What if initialized_ is false?
}

// ✅ GOOD: State validation
bool MenuPattern::SelectItem(int index) {
    if (!initialized_) {
        LOGE("Menu not initialized");
        return false;
    }

    if (index < 0 || index >= items_.size()) {
        LOGE("Invalid index: %{public}d", index);
        return false;
    }

    items_[index].selected = true;
    return true;
}
```

### Exception Safety (ACE Engine typically disables exceptions)

**Check for:**
- [ ] No throw statements (unless explicitly enabled)
- [ ] Error codes or Result types used instead
- [ ] No exception-based control flow

**Red Flags:**

```cpp
// ❌ BAD: Using exceptions (if disabled)
void Process() {
    if (error) {
        throw std::runtime_error("Failed");  // May crash if exceptions disabled
    }
}

// ✅ GOOD: Error codes
bool Process() {
    if (error) {
        LOGE("Process failed");
        return false;
    }
    return true;
}

// ✅ GOOD: Result type
Result<Data> Process() {
    if (error) {
        return Error(ErrorType::INVALID_STATE, "Process failed");
    }
    return Ok(data);
}
```

## Common Stability Issues

### 1. Uninitialized Variables

```cpp
// ❌ BAD
void Process() {
    int value;  // Uninitialized
    if (condition) {
        value = 10;
    }
    Use(value);  // Undefined if condition is false
}

// ✅ GOOD
void Process() {
    int value = 0;  // Initialize
    if (condition) {
        value = 10;
    }
    Use(value);
}
```

### 2. Null Pointer Dereference

```cpp
// ❌ BAD
void UseComponent(Component* comp) {
    comp->Update();  // Crashes if comp is nullptr
}

// ✅ GOOD
bool UseComponent(Component* comp) {
    if (!comp) {
        LOGE("Null component");
        return false;
    }
    comp->Update();
    return true;
}

// ✅ BETTER: Use smart pointers
bool UseComponent(const RefPtr<Component>& comp) {
    if (!comp) {
        LOGE("Null component");
        return false;
    }
    comp->Update();
    return true;
}
```

### 3. Use-After-Free (C++ specific)

```cpp
// ❌ BAD
Component* comp = new Component();
delete comp;
comp->Update();  // Use-after-free

// ✅ GOOD: Use smart pointers
auto comp = AceType::MakeRefPtr<Component>();
comp->Update();
// Automatic deletion when out of scope
```

### 4. String/Array Misuse

```cpp
// ❌ BAD
char buffer[10];
strcpy(buffer, user_input);  // Buffer overflow

// ❌ BAD
std::string str = "hello";
char c = str[100];  // Undefined behavior

// ✅ GOOD
strlcpy(buffer, user_input, sizeof(buffer));  // Safe copy

// ✅ GOOD
std::string str = "hello";
if (index < str.size()) {
    char c = str[index];  // Bounds checked
}
```

## Testing for Stability

**Essential Test Cases:**
1. Empty inputs (empty string, empty vector, null pointer)
2. Boundary values (0, -1, INT_MAX, INT_MIN)
3. Invalid inputs (negative where positive expected, etc.)
4. Resource exhaustion (out of memory, file handle limits)
5. Concurrent access (if threading involved)
6. Error paths (simulate failures)

**Example:**

```cpp
TEST(MenuPatternTest, SelectItem_EmptyMenu) {
    MenuPattern menu;
    ASSERT_FALSE(menu.IsInitialized());

    // Should handle gracefully
    ASSERT_FALSE(menu.SelectItem(0));
}

TEST(MenuPatternTest, SelectItem_OutOfBounds) {
    MenuPattern menu;
    menu.Initialize({{"Item1"}, {"Item2"}});

    // Boundary cases
    ASSERT_FALSE(menu.SelectItem(-1));
    ASSERT_FALSE(menu.SelectItem(2));
    ASSERT_TRUE(menu.SelectItem(0));
    ASSERT_TRUE(menu.SelectItem(1));
}
```

## Review Questions to Ask

1. What happens if this input is empty/null?
2. What happens if this index is out of bounds?
3. What happens if this allocation fails?
4. What happens if this file doesn't exist?
5. Are all error paths tested?
6. Can this function ever return an invalid/unexpected value?
7. What happens in concurrent scenarios?
8. Are resources properly cleaned up on error?

## Refactoring Patterns

### Extract Error Handling

**Before:**
```cpp
void Process() {
    if (!Validate()) return;
    if (!CheckPermissions()) return;
    if (!AllocateResources()) return;
    // Do work
}
```

**After:**
```cpp
bool Process() {
    if (!Validate()) {
        LOGE("Validation failed");
        return false;
    }
    if (!CheckPermissions()) {
        LOGE("Permission denied");
        return false;
    }
    if (!AllocateResources()) {
        LOGE("Resource allocation failed");
        return false;
    }
    return DoWork();
}
```

### Use Result Type

**Before:**
```cpp
Data* ParseData(const std::string& input) {
    if (input.empty()) return nullptr;
    // ...
    return new Data();
}

void Use() {
    Data* data = ParseData(input);
    if (!data) {
        // What went wrong?
        return;
    }
}
```

**After:**
```cpp
Result<Data> ParseData(const std::string& input) {
    if (input.empty()) {
        return Error(ErrorType::INVALID_INPUT, "Input is empty");
    }
    // ...
    return Ok(data);
}

void Use() {
    auto result = ParseData(input);
    if (!result.IsValid()) {
        LOGE("Parse failed: %{public}s", result.GetError().message);
        return;
    }
    Data data = result.GetValue();
}
```

## Severity Guidelines

**CRITICAL:**
- Null pointer dereference
- Buffer overflows
- Use-after-free
- Unchecked returns from dangerous functions

**HIGH:**
- Missing error handling in critical paths
- Unvalidated external input
- Missing boundary checks

**MEDIUM:**
- Missing logging on error paths
- Incomplete error propagation

**LOW:**
- Minor edge case handling improvements
- Extra defensive checks
