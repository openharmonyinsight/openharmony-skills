# Memory Management Code Review Guidelines

## Overview

Memory management is critical in C++ for preventing leaks, use-after-free, and undefined behavior. ACE Engine uses smart pointers extensively to manage memory automatically.

## Key Principles

1. **RAII (Resource Acquisition Is Initialization)** - Resources acquired in constructor, released in destructor
2. **Smart pointers over raw pointers** - Use RefPtr, unique_ptr, shared_ptr
3. **Clear ownership semantics** - Know who owns what
4. **No cycles** - Break circular references with WeakPtr
5. **No manual new/delete** - Let smart pointers handle it

## ACE Engine Memory Management

### RefPtr (ACE Engine Smart Pointer)

**Creation:**
```cpp
// ✅ GOOD: Use MakeRefPtr
auto node = AceType::MakeRefPtr<FrameNode>();
auto pattern = AceType::MakeRefPtr<MenuPattern>(param1, param2);

// ❌ BAD: Manual new
RefPtr<FrameNode> node = new FrameNode();  // Wrong!
```

**Type-Safe Casting:**
```cpp
// ✅ GOOD: DynamicCast with check
auto pattern = AceType::DynamicCast<MenuPattern>(node->GetPattern());
if (!pattern) {
    LOGE("Failed to get MenuPattern");
    return false;
}

// ❌ BAD: static_cast without check
auto* pattern = static_cast<MenuPattern*>(node->GetPattern());
pattern->DoSomething();  // May crash if wrong type
```

**Breaking Cycles:**
```cpp
// ❌ BAD: Circular reference - memory leak
class Parent {
    RefPtr<Child> child_;
};

class Child {
    RefPtr<Parent> parent_;  // Cycle!
};

// ✅ GOOD: Use WeakPtr
class Child {
    WeakPtr<Parent> parent_;  // Breaks cycle
};

// Usage:
auto parent = AceType::DynamicCast<Parent>(parent_weak_.Upgrade());
if (parent) {
    parent->DoSomething();
}
```

**Callback Safety:**
```cpp
// ❌ BAD: Capturing raw this
class MenuPattern {
    void ScheduleUpdate() {
        PostTask([this]() {  // Dangerous if object destroyed
            Update();
        });
    }
};

// ✅ GOOD: Capture WeakPtr
class MenuPattern {
    void ScheduleUpdate() {
        auto weak = AceType::WeakClaim(this);
        PostTask([weak]() {
            auto pattern = AceType::DynamicCast<MenuPattern>(weak.Upgrade());
            if (pattern) {  // Check object still alive
                pattern->Update();
            }
        });
    }
};
```

## Code Review Checklist

### Smart Pointer Usage

**Check for:**
- [ ] Raw pointers that should be smart pointers
- [ ] Manual new/delete (should use MakeRefPtr)
- [ ] Missing DynamicCast before using smart pointer
- [ ] Circular references (parent-child with strong refs both ways)
- [ ] Callbacks capturing this without WeakClaim

**Red Flags:**

```cpp
// ❌ BAD: Raw pointer ownership
class Component {
    MenuPattern* pattern_;  // Who deletes this?
public:
    Component() : pattern_(new MenuPattern()) {}
    ~Component() { delete pattern_; }  // Easy to forget
};

// ✅ GOOD: Smart pointer ownership
class Component {
    RefPtr<MenuPattern> pattern_;  // Automatic cleanup
public:
    Component() : pattern_(AceType::MakeRefPtr<MenuPattern>()) {}
    // Destructor automatic
};

// ❌ BAD: Leaking in error path
bool Process() {
    auto* data = new Data();
    if (!Validate(data)) {
        return false;  // Leak!
    }
    delete data;
    return true;
}

// ✅ GOOD: Smart pointer cleans up
bool Process() {
    auto data = AceType::MakeRefPtr<Data>();
    if (!Validate(data)) {
        return false;  // Automatic cleanup
    }
    return true;
}
```

### Ownership Semantics

**Check for:**
- [ ] Clear owner for every allocated object
- [ ] No ambiguous ownership (multiple potential owners)
- [ ] Transfer of ownership is explicit
- [ ] Function signatures indicate ownership

**Red Flags:**

```cpp
// ❌ BAD: Ambiguous ownership
class Menu {
    std::vector<MenuItem*> items_;  // Who owns these?
public:
    void AddItem(MenuItem* item) {  // Caller or Menu?
        items_.push_back(item);
    }
};

// ✅ GOOD: Clear ownership
class Menu {
    std::vector<RefPtr<MenuItem>> items_;  // Menu owns
public:
    void AddItem(const RefPtr<MenuItem>& item) {  // Shared ownership
        items_.push_back(item);
    }

    // Or unique ownership:
    void AddItem(std::unique_ptr<MenuItem> item) {  // Transfer
        items_.push_back(std::move(item));
    }
};
```

### Memory Leaks

**Common Leak Patterns:**

```cpp
// 1. Forgetting to delete
// ❌ BAD
void Process() {
    auto* data = new Data();
    // Forgot delete
}

// ✅ GOOD
void Process() {
    auto data = std::make_unique<Data>();
    // Automatic cleanup
}

// 2. Leaking in containers
// ❌ BAD
std::vector<Data*> items;
void AddData() {
    items.push_back(new Data());  // Leak when vector clears
}

// ✅ GOOD
std::vector<std::unique_ptr<Data>> items;
void AddData() {
    items.push_back(std::make_unique<Data>());
}

// 3. Leaking in maps
// ❌ BAD
std::unordered_map<std::string, Data*> cache;
void Cache(const std::string& key) {
    cache[key] = new Data();  // Old value leaked
}

// ✅ GOOD
std::unordered_map<std::string, std::unique_ptr<Data>> cache;
void Cache(const std::string& key) {
    cache[key] = std::make_unique<Data>();  // Old value auto-deleted
}

// 4. Circular reference
// ❌ BAD
class Node {
    RefPtr<Node> next_;
    RefPtr<Node> prev_;  // Cycle: next <-> prev
};

// ✅ GOOD
class Node {
    RefPtr<Node> next_;
    WeakPtr<Node> prev_;  // Breaks cycle
};
```

### Use-After-Free Detection

**Red Flags:**

```cpp
// ❌ BAD: Dangling reference
int& GetBadReference() {
    int value = 42;
    return value;  // Returns reference to local!
}

// ❌ BAD: Dangling pointer
int* GetBadPointer() {
    int value = 42;
    return &value;  // Points to stack!
}

// ✅ GOOD: Return by value
int GetValue() {
    int value = 42;
    return value;  // Copy
}

// ✅ GOOD: Return smart pointer
RefPtr<Data> GetData() {
    return AceType::MakeRefPtr<Data>();
}
```

### Buffer Overflows

**Red Flags:**

```cpp
// ❌ BAD: Unchecked array access
void Process(int* data, int size) {
    for (int i = 0; i <= size; i++) {  // Off-by-one!
        data[i] = 0;  // Buffer overflow
    }
}

// ❌ BAD: Unsafe string functions
char buffer[10];
strcpy(buffer, user_input);  // No bounds checking
sprintf(buffer, "%s %s", str1, str2);  // Can overflow

// ✅ GOOD: Bounds checking
void Process(int* data, int size) {
    for (int i = 0; i < size; i++) {
        data[i] = 0;
    }
}

// ✅ GOOD: Safe string functions
strlcpy(buffer, user_input, sizeof(buffer));
snprintf(buffer, sizeof(buffer), "%s %s", str1, str2);

// ✅ BETTER: Use std::string
std::string buffer = user_input + " " + str2;
```

## Modern C++ Memory Management

### unique_ptr - Exclusive Ownership

```cpp
// ✅ GOOD: For exclusive ownership
std::unique_ptr<MenuPattern> CreateMenu() {
    return std::make_unique<MenuPattern>();
}

// Transfer ownership
std::unique_ptr<MenuPattern> menu = CreateMenu();

// Move to another owner
std::unique_ptr<MenuPattern> menu2 = std::move(menu);
// menu is now nullptr

// ✅ GOOD: Custom deleters
std::unique_ptr<FILE, decltype(&fclose)> file(
    fopen("data.txt", "r"),
    &fclose
);  // Auto-closes
```

### shared_ptr - Shared Ownership

```cpp
// ✅ GOOD: When multiple owners needed
class SharedResource {
public:
    static std::shared_ptr<SharedResource> GetInstance() {
        static auto instance = std::make_shared<SharedResource>();
        return instance;  // Shared ownership
    }
};

// Use weak_ptr to break cycles
class Node {
public:
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;  // Doesn't increase ref count
};
```

### Move Semantics

```cpp
// ❌ BAD: Unnecessary copies
std::vector<Data> Process() {
    std::vector<Data> result;
    // ... fill result
    return result;  // Copy (old C++)
}

// ✅ GOOD: Move semantics (automatic with C++11+)
std::vector<Data> Process() {
    std::vector<Data> result;
    // ... fill result
    return result;  // Move (RVO)
}

// ✅ GOOD: Explicit move
void Transfer(std::vector<Data>&& data) {
    storage_ = std::move(data);  // No copy
}
```

## Detection Tools

### Valgrind (Linux)

```bash
# Detect memory leaks
valgrind --leak-check=full --show-leak-kinds=all ./test_program

# Detect invalid access
valgrind ./test_program
```

### AddressSanitizer

```bash
# Compile with ASan
g++ -fsanitize=address -g test.cpp

# Run
./a.out

# Detects:
# - Use-after-free
# - Buffer overflows
# - Memory leaks
# - Double free
```

### Static Analysis

```bash
# Analyzer
clang --analyze -Xanalyzer -analyzer-checker=core,debug,unix test.cpp

# Cppcheck
cppcheck --enable=all --inconclusive test.cpp
```

## Common ACE Engine Patterns

### Component Lifecycle

```cpp
// ✅ GOOD: Proper lifecycle management
class MenuPattern : public PatternBase {
public:
    static RefPtr<MenuPattern> Create() {
        // Create with RefPtr
        auto pattern = AceType::MakeRefPtr<MenuPattern>();
        pattern->Initialize();
        return pattern;
    }

    ~MenuPattern() {
        // Cleanup happens automatically
        // Smart pointers clean up their members
    }

private:
    RefPtr<MenuLayoutProperty> layout_property_;
    RefPtr<MenuPaintProperty> paint_property_;
    // All automatically cleaned up
};
```

### Pattern Access

```cpp
// ✅ GOOD: Safe pattern access
RefPtr<MenuPattern> GetMenuPattern(FrameNode* node) {
    if (!node) {
        LOGE("Null node");
        return nullptr;
    }

    auto pattern = node->GetPattern<MenuPattern>();
    if (!pattern) {
        LOGE("Pattern is not MenuPattern");
        return nullptr;
    }

    return pattern;
}

// Usage:
auto pattern = GetMenuPattern(node);
if (!pattern) {
    return false;
}
pattern->DoSomething();
```

## Refactoring Examples

### Convert Raw Pointers to Smart Pointers

**Before:**
```cpp
class MenuManager {
    MenuPattern* menu_;
public:
    MenuManager() : menu_(new MenuPattern()) {}
    ~MenuManager() { delete menu_; }  // Easy to forget
};
```

**After:**
```cpp
class MenuManager {
    RefPtr<MenuPattern> menu_;
public:
    MenuManager() : menu_(AceType::MakeRefPtr<MenuPattern>()) {}
    // Automatic cleanup
};
```

### Fix Circular Reference

**Before:**
```cpp
class MenuItem {
    RefPtr<Menu> parent_;  // Strong ref
};

class Menu {
    std::vector<RefPtr<MenuItem>> items_;  // Strong refs
};
// Cycle: menu -> item -> menu (leak!)
```

**After:**
```cpp
class MenuItem {
    WeakPtr<Menu> parent_;  // Weak ref
};

class Menu {
    std::vector<RefPtr<MenuItem>> items_;
};
// No cycle, proper cleanup
```

## Review Questions

1. Who owns this memory?
2. When is this memory freed?
3. Can this pointer become dangling?
4. Are there any cycles in the ownership graph?
5. What happens if an exception is thrown?
6. Are all error paths freeing memory?
7. Is this callback safe if the object is destroyed?

## Severity Guidelines

**CRITICAL:**
- Memory leaks in long-running processes
- Use-after-free vulnerabilities
- Buffer overflows
- Double-free
- Wild pointer dereferences

**HIGH:**
- Circular references (memory leaks)
- Missing smart pointer where needed
- Raw pointer ownership ambiguity

**MEDIUM:**
- Unnecessary copies (performance)
- Missing const correctness (accidental modification)

**LOW:**
- Could use unique_ptr instead of shared_ptr
- Minor optimization opportunities
