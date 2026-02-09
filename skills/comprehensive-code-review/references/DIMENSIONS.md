# Code Review Dimensions - Quick Reference

Complete reference for all 19+ code review dimensions with severity levels and detection patterns.

---

## Quick Severity Guide

🔴 **CRITICAL** - Must fix before merge
🟠 **HIGH** - Should fix before merge
🟡 **MEDIUM** - Fix soon
🟢 **LOW** - Nice to have

---

## 1. STABILITY

**Focus:** Error handling, boundary conditions, predictable behavior

**CRITICAL Issues:**
- Null pointer dereference 🔴
- Buffer overflows 🔴
- Use-after-free 🔴
- Unchecked returns from dangerous functions 🔴

**HIGH Issues:**
- Missing error handling in critical paths 🟠
- Unvalidated external input 🟠
- Missing boundary checks 🟠

**Key Checks:**
```cpp
// ✅ Check all return values
auto result = ParseData(input);
if (!result.IsValid()) {
    LOGE("Parse failed: %{public}s", result.GetError().message);
    return result.GetError();
}

// ✅ Validate all inputs
if (index < 0 || index >= items.size()) {
    LOGE("Invalid index");
    return false;
}

// ✅ Handle boundary conditions
if (container.empty()) return;

// ✅ Clean up resources on error
FILE* fp = fopen(path, "r");
if (!fp) { /* handle error */ }
// ... use fp ...
fclose(fp);
```

**See:** [STABILITY.md](STABILITY.md)

---

## 2. PERFORMANCE

**Focus:** Algorithm complexity, optimization, efficiency

**CRITICAL Issues:**
- O(n²) where O(n) possible with large n 🔴
- Memory leaks in hot paths 🔴
- Blocking UI thread 🟠

**HIGH Issues:**
- Unnecessary copies 🟠
- Missing caching 🟠
- Inefficient data structures 🟠

**Key Checks:**
```cpp
// ❌ BAD: O(n²) nested loop
bool Contains(const std::vector<std::string>& list, const std::string& target) {
    for (const auto& item : list) {
        if (item == target) return true;
    }
}

// ✅ GOOD: O(1) hash lookup
bool Contains(const std::unordered_set<std::string>& set, const std::string& target) {
    return set.find(target) != set.end();
}

// ❌ BAD: Unnecessary copy
void Process(std::string data);  // Copies data

// ✅ GOOD: Pass by reference
void Process(const std::string& data);  // No copy

// ✅ Cache expensive calculations
int CalculateLayout() {
    if (cache_valid_) return cached_size_;
    cached_size_ = DoCalculate();
    cache_valid_ = true;
    return cached_size_;
}
```

**See:** [PERFORMANCE.md](PERFORMANCE.md)

---

## 3. THREADING

**Focus:** Data races, deadlock prevention, synchronization

**CRITICAL Issues:**
- Unprotected shared mutable state 🔴
- Data races 🔴
- Deadlocks 🔴

**HIGH Issues:**
- Missing synchronization 🟠
- Incorrect lock ordering 🟠
- Unsafe callback captures 🟠

**Key Checks:**
```cpp
// ❌ BAD: Unprotected shared state
class Counter {
    int count_;  // Shared across threads
public:
    void Increment() { count_++; }  // Data race!
};

// ✅ GOOD: Protected access
class Counter {
    std::mutex mutex_;
    int count_;
public:
    void Increment() {
        std::lock_guard<std::mutex> lock(mutex_);
        count_++;
    }
};

// ❌ BAD: Unsafe callback capture
class MenuPattern {
    void ScheduleUpdate() {
        PostTask([this]() {  // Dangerous!
            Update();
        });
    }
};

// ✅ GOOD: WeakPtr capture
class MenuPattern {
    void ScheduleUpdate() {
        auto weak = AceType::WeakClaim(this);
        PostTask([weak]() {
            auto pattern = AceType::DynamicCast<MenuPattern>(weak.Upgrade());
            if (pattern) pattern->Update();
        });
    }
};

// ✅ GOOD: Consistent lock order
void Transfer(Account& a, Account& b) {
    std::scoped_lock lock(a.mutex, b.mutex);  // Prevents deadlock
}
```

**See:** [THREADING.md](THREADING.md)

---

## 4. SECURITY

**Focus:** Input validation, vulnerabilities, sensitive data

**CRITICAL Issues:**
- SQL injection 🔴
- Command injection 🔴
- Buffer overflows 🔴
- Hardcoded secrets 🔴

**HIGH Issues:**
- Missing input validation 🟠
- Sensitive data in logs 🟠
- Unsafe deserialization 🟠

**Key Checks:**
```cpp
// ❌ CRITICAL: Command injection
std::string cmd = "ls " + user_input;
system(cmd.c_str());

// ✅ GOOD: Whitelist validation
bool IsValidFileName(const std::string& name) {
    return std::all_of(name.begin(), name.end(),
        [](char c) { return std::isalnum(c) || c == '_' || c == '.'; });
}

// ❌ BAD: Logging sensitive data
LOGI("Password: %{public}s", password.c_str());

// ✅ GOOD: Sanitize logs
LOGI("Password length: %{public}zu", password.size());
// or
LOGI("Password: %{private}s", password.c_str());  // Auto-sanitized

// ❌ BAD: Unchecked bounds
char buffer[10];
strcpy(buffer, user_input);  // Overflow!

// ✅ GOOD: Safe string handling
strlcpy(buffer, user_input, sizeof(buffer));
```

**See:** [SECURITY.md](SECURITY.md)

---

## 5. MEMORY

**Focus:** Smart pointers, leaks, ownership semantics

**CRITICAL Issues:**
- Memory leaks 🔴
- Use-after-free 🔴
- Double-free 🔴
- Buffer overflows 🔴

**HIGH Issues:**
- Circular references 🟠
- Raw pointers where smart pointers needed 🟠
- Unclear ownership 🟠

**Key Checks:**
```cpp
// ❌ BAD: Manual new/delete
class Component {
    Data* data_;
public:
    Component() : data_(new Data()) {}
    ~Component() { delete data_; }  // Easy to forget
};

// ✅ GOOD: Smart pointer
class Component {
    RefPtr<Data> data_;
public:
    Component() : data_(AceType::MakeRefPtr<Data>()) {}
    // Automatic cleanup
};

// ❌ BAD: Circular reference
class Parent {
    RefPtr<Child> child_;
};
class Child {
    RefPtr<Parent> parent_;  // Cycle!
};

// ✅ GOOD: Break cycle with WeakPtr
class Child {
    WeakPtr<Parent> parent_;
};

// ✅ Type-safe casting
auto pattern = AceType::DynamicCast<MenuPattern>(node->GetPattern());
if (!pattern) {
    LOGE("Failed to get pattern");
    return false;
}
```

**See:** [MEMORY.md](MEMORY.md)

---

## 6. MODERN C++

**Focus:** C++11/14/17/20 features, idiomatic C++

**HIGH Issues:**
- Using raw pointers instead of smart pointers 🟠
- Missing move semantics 🟠
- Not using constexpr/constexpr if 🟠
- Manual memory management 🟠

**MEDIUM Issues:**
- Not using auto where appropriate 🟡
- Not using range-based for loops 🟡
- Not using std::optional 🟡

**Key Checks:**
```cpp
// ✅ Use smart pointers
auto ptr = std::make_unique<Data>();
auto shared = std::make_shared<Data>();

// ✅ Use move semantics
std::vector<Data> CreateLargeVector() {
    std::vector<Data> result;
    return result;  // Move (RVO)
}

// ✅ Use auto
auto iter = container.begin();
auto callback = [](int x) { return x * 2; };

// ✅ Use range-based for
for (const auto& item : container) {
    Process(item);
}

// ✅ Use std::optional
std::optional<int> Find(const std::string& key) {
    auto it = map.find(key);
    if (it != map.end()) return it->second;
    return std::nullopt;
}

// ✅ Use constexpr
constexpr int MAX_SIZE = 100;
constexpr double PI = 3.14159;

// ✅ Use nullptr instead of NULL
void* ptr = nullptr;
```

**See:** [MODERN_CPP.md](MODERN_CPP.md)

---

## 7. EFFECTIVE C++

**Focus:** Best practices, idioms, resource management

**HIGH Issues:**
- Violating RAII 🟠
- Rule of Three/Five violations 🟠
- Resource leaks 🟠

**MEDIUM Issues:**
- Incorrect virtual destructors 🟡
- Returning references to temporaries 🟡
- Incorrect exception safety 🟡

**Key Checks:**
```cpp
// ✅ RAII - Resource Acquisition Is Initialization
class FileWrapper {
    FILE* fp_;
public:
    FileWrapper(const char* path) {
        fp_ = fopen(path, "r");
        if (!fp_) throw std::runtime_error("Failed to open");
    }
    ~FileWrapper() {
        if (fp_) fclose(fp_);  // Automatic cleanup
    }
    // Delete copy, enable move
    FileWrapper(const FileWrapper&) = delete;
    FileWrapper(FileWrapper&& other) noexcept : fp_(other.fp_) {
        other.fp_ = nullptr;
    }
};

// ✅ Rule of Five
class Buffer {
    char* data_;
    size_t size_;

public:
    // 1. Destructor
    ~Buffer() { delete[] data_; }

    // 2. Copy constructor
    Buffer(const Buffer& other) : data_(new char[other.size_]), size_(other.size_) {
        std::copy(other.data_, other.data_ + size_, data_);
    }

    // 3. Copy assignment
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = new char[size_];
            std::copy(other.data_, other.data_ + size_, data_);
        }
        return *this;
    }

    // 4. Move constructor
    Buffer(Buffer&& other) noexcept : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;
        other.size_ = 0;
    }

    // 5. Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }
};
```

**See:** [EFFECTIVE_CPP.md](EFFECTIVE_CPP.md)

---

## 8. CODE SMELLS

**Focus:** 22 types of code smells indicating design problems

**HIGH Severity:**
- Large Class 🟠 (>500 lines, too many responsibilities)
- Divergent Change 🟠 (multiple reasons to change)
- Shotgun Surgery 🟠 (one change affects many files)

**MEDIUM Severity:**
- Long Method 🟡 (>50 lines)
- Duplicate Code 🟡
- Feature Envy 🟡
- Switch Statements 🟡
- Primitive Obsession 🟡

**Key Smells:**
```cpp
// ❌ Long Method - Extract Method
void Process() {
    // 100 lines doing multiple things
}
// ✅ Break into smaller methods

// ❌ Large Class - Extract Class
class GodObject {
    // 1000 lines, 50 methods
};
// ✅ Split into focused classes

// ❌ Duplicate Code
void A::Process() {
    if (!Validate()) return;
    // ...
}
void B::Process() {
    if (!Validate()) return;  // Same!
}
// ✅ Extract to base class

// ❌ Switch Statements
void HandleEvent(Event e) {
    switch (e.type) {
        case CLICK: /* ... */
        case HOVER: /* ... */
    }
}
// ✅ Use polymorphism

// ❌ Primitive Obsession
void Draw(int x, int y, int width, int height);
// ✅ Use abstractions
void Draw(const Rect& bounds);
```

**See:** [CODE_SMELLS.md](CODE_SMELLS.md)

---

## 9. SOLID PRINCIPLES

**Focus:** Five design principles for maintainable code

**HIGH Issues:**
- Violating Single Responsibility Principle 🟠
- Violating Open/Closed Principle 🟠

**MEDIUM Issues:**
- Violating Liskov Substitution Principle 🟡
- Violating Interface Segregation Principle 🟡
- Violating Dependency Inversion Principle 🟡

**Key Checks:**
```cpp
// ✅ S - Single Responsibility Principle
// ❌ BAD: Class does too many things
class Menu {
    void Layout();
    void Render();
    void HandleEvents();
    void SaveToDatabase();
    void SendOverNetwork();
};
// ✅ GOOD: Split responsibilities
class Menu { void Layout(); };
class MenuRenderer { void Render(); };
class MenuEventHandler { void HandleEvents(); };

// ✅ O - Open/Closed Principle
// ❌ BAD: Need to modify for new types
void ProcessMenu(MenuType type) {
    if (type == CONTEXT) { /* ... */ }
    else if (type == DROPDOWN) { /* ... */ }
    else if (type == NEW_TYPE) { /* must modify! */ }
}
// ✅ GOOD: Open for extension, closed for modification
class MenuProcessor {
    virtual void Process() = 0;
};
class ContextMenuProcessor : public MenuProcessor { /* ... */ };
class DropdownMenuProcessor : public MenuProcessor { /* ... */ };

// ✅ L - Liskov Substitution Principle
// ❌ BAD: Subtype changes behavior
class Bird {
    virtual void Fly() { /* fly */ }
};
class Penguin : public Bird {
    void Fly() override { throw std::runtime_error("Can't fly!"); }
};
// ✅ GOOD: Proper hierarchy
class FlyingBird : public Bird { void Fly() override; };
class Penguin : public Bird { void Swim(); };

// ✅ I - Interface Segregation Principle
// ❌ BAD: Fat interface
class Component {
    virtual void Render() = 0;
    virtual void HandleClick() = 0;
    virtual void HandleKeyPress() = 0;
    virtual void Animate() = 0;
    virtual void Serialize() = 0;
};
// ✅ GOOD: Segregated interfaces
class Renderable { virtual void Render() = 0; };
class Clickable { virtual void OnClick() = 0; };
class Animatable { virtual void Animate() = 0; };

// ✅ D - Dependency Inversion Principle
// ❌ BAD: Depend on concrete
class MenuPattern {
    SQLiteDatabase db_;  // Concrete dependency
};
// ✅ GOOD: Depend on abstraction
class MenuPattern {
    std::shared_ptr<IDatabase> db_;  // Abstract dependency
};
```

**See:** [SOLID.md](SOLID.md)

---

## 10. DESIGN PATTERNS

**Focus:** Correct pattern usage and selection

**MEDIUM Issues:**
- Using pattern incorrectly 🟡
- Using pattern inappropriately 🟡
- Forced pattern usage 🟡

**Key Patterns:**
```cpp
// ✅ Factory Pattern
class MenuFactory {
public:
    static RefPtr<Menu> CreateMenu(MenuType type) {
        switch (type) {
            case CONTEXT: return AceType::MakeRefPtr<ContextMenu>();
            case DROPDOWN: return AceType::MakeRefPtr<DropdownMenu>();
        }
    }
};

// ✅ Observer Pattern
class Observable {
    std::vector<std::function<void()>> observers_;
public:
    void Subscribe(std::function<void()> observer) {
        observers_.push_back(observer);
    }
    void Notify() {
        for (auto& observer : observers_) observer();
    }
};

// ✅ Strategy Pattern
class LayoutStrategy {
public:
    virtual Size Measure(const LayoutConstraint&) = 0;
};

class FlexLayoutStrategy : public LayoutStrategy {
    Size Measure(const LayoutConstraint& c) override {
        // Flex layout algorithm
    }
};

// ✅ Adapter Pattern (Platform abstraction)
class WindowAdapter {
public:
    virtual void Show() = 0;
};

class OHOSWindowAdapter : public WindowAdapter {
public:
    void Show() override {
        Rosen::WindowManager::GetInstance()->Show();
    }
};
```

**See:** [PATTERNS.md](PATTERNS.md)

---

## 11. ROBUSTNESS

**Focus:** Fault tolerance, graceful degradation

**HIGH Issues:**
- No error handling 🟠
- Crashes on invalid input 🟠
- Resource exhaustion handling 🟠

**MEDIUM Issues:**
- No graceful degradation 🟡
- Poor error recovery 🟡

**Key Checks:**
```cpp
// ✅ Validate all inputs
bool SetPosition(int x, int y) {
    if (!std::isfinite(x) || !std::isfinite(y)) {
        LOGE("Invalid position");
        return false;
    }
    x_ = x; y_ = y;
    return true;
}

// ✅ Handle resource limits
bool LoadItems(const std::vector<std::string>& items) {
    const size_t MAX_ITEMS = 1000;
    if (items.size() > MAX_ITEMS) {
        LOGE("Too many items");
        return false;
    }
    // ...
}

// ✅ Graceful degradation
class MenuRenderer {
    void Render() {
        if (SupportsGPU()) {
            RenderWithGPU();
        } else {
            RenderWithCPU();  // Fallback
        }
    }
};

// ✅ Transaction-like operations
bool UpdateState(const std::string& new_state) {
    auto backup = current_state_;
    if (!ApplyNewState(new_state)) {
        current_state_ = backup;  // Rollback
        return false;
    }
    return true;
}
```

**See:** [ROBUSTNESS.md](ROBUSTNESS.md)

---

## 12. TESTABILITY

**Focus:** Dependency injection, decoupling, testability

**HIGH Issues:**
- Hard-coded dependencies 🟠
- Tightly coupled code 🟠
- No dependency injection 🟠

**MEDIUM Issues:**
- Static dependencies 🟡
- Global state 🟡

**Key Checks:**
```cpp
// ❌ BAD: Hard-coded dependency
class MenuPattern {
    void Process() {
        auto data = Database::GetInstance()->Query();  // Hard to test
    }
};

// ✅ GOOD: Dependency injection
class MenuPattern {
    IDatabase* db_;  // Abstract
public:
    MenuPattern(IDatabase* db) : db_(db) {}
    void Process() {
        auto data = db_->Query();  // Can inject mock
    }
};

// ✅ Testable
TEST(MenuPatternTest, ProcessData) {
    MockDatabase mock;
    MenuPattern menu(&mock);
    menu.Process();
    EXPECT_TRUE(mock.WasCalled());
}

// ❌ BAD: Global state
int global_counter;
void Increment() { global_counter++; }

// ✅ GOOD: Encapsulated state
class Counter {
    int count_ = 0;
public:
    void Increment() { count_++; }
    int GetCount() const { return count_; }
};
```

**See:** [TESTABILITY.md](TESTABILITY.md)

---

## 13. MAINTAINABILITY

**Focus:** Code complexity, readability

**MEDIUM Issues:**
- High cyclomatic complexity (>10) 🟡
- Deep nesting (>3 levels) 🟡
- Poor naming 🟡

**Key Checks:**
```cpp
// ❌ BAD: High complexity
void Process(Event e) {
    if (e.type == CLICK) {
        if (e.target == BUTTON) {
            if (e.button == LEFT) {
                if (IsEnabled()) {
                    if (HasFocus()) {
                        // 5 levels deep!
                    }
                }
            }
        }
    }
}

// ✅ GOOD: Early returns
void Process(Event e) {
    if (e.type != CLICK) return;
    if (e.target != BUTTON) return;
    if (e.button != LEFT) return;
    if (!IsEnabled()) return;
    if (!HasFocus()) return;
    // Main logic
}

// ✅ Meaningful names
// ❌
if (d > 0 && (m < 0 || y > 0)) { }

// ✅
if (IsDistanceValid() && (IsMovingNegative() || IsYearPositive())) { }
```

**See:** [MAINTAINABILITY.md](MAINTAINABILITY.md)

---

## 14. OBSERVABILITY

**Focus:** Logging, monitoring, debugging

**MEDIUM Issues:**
- Missing critical logs 🟡
- No performance monitoring 🟡
- Insufficient error context 🟡

**Key Checks:**
```cpp
// ✅ Log entry points
void MenuPattern::OnModifyDone() {
    LOGI("MenuPattern::OnModifyDone called, id=%{public}d", id_);
    // ...
}

// ✅ Log errors with context
bool Process() {
    if (!Validate()) {
        LOGE("Validation failed: id=%{public}d, state=%{public}d, items=%{public}zu",
             id_, state_, items_.size());
        return false;
    }
}

// ✅ Performance monitoring
auto start = std::chrono::high_resolution_clock::now();
UpdateLayout();
auto end = std::chrono::high_resolution_clock::now();
auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
if (duration.count() > SLOW_THRESHOLD_US) {
    LOGW("Slow layout: %{public}s took %{public}lld us",
         component_name_.c_str(), duration.count());
}

// ✅ Use proper log levels
LOGI("Info: Normal operation");
LOGW("Warning: Unexpected but recoverable");
LOGE("Error: Failure occurred");
LOGD("Debug: Detailed diagnostics");
LOGF("Fatal: Critical failure");
```

**See:** [OBSERVABILITY.md](OBSERVABILITY.md)

---

## 15. API DESIGN

**Focus:** Consistency, clarity, usability

**HIGH Issues:**
- Violating principle of least surprise 🟠
- Inconsistent APIs 🟠

**MEDIUM Issues:**
- Poor naming 🟡
- Missing overloads 🟡

**Key Checks:**
```cpp
// ✅ Consistent naming
class MenuPattern {
public:
    int GetWidth() const;
    void SetWidth(int width);
    bool IsVisible() const;
    void OnClick();
};

// ✅ Principle of least surprise
// ❌ BAD: Unexpected behavior
void Clear() {
    items_.clear();
    width_ = 0;  // Unexpected!
    height_ = 0;
}

// ✅ GOOD: Clear, predictable
void Clear() {
    items_.clear();
}

void Reset() {
    Clear();
    width_ = 0;
    height_ = 0;
}

// ✅ Default parameters for convenience
void Show(bool animated = true);
void SetPosition(const Point& pos, bool animated = false);
```

**See:** [API_DESIGN.md](API_DESIGN.md)

---

## 16. TECHNICAL DEBT

**Focus:** TODO/FIXME management, debt tracking

**MEDIUM Issues:**
- Untracked TODOs 🟡
- Missing issue references 🟡
- Outdated TODOs 🟡

**Key Checks:**
```cpp
// ✅ Proper TODO tracking
// TODO(issue:12345): Optimize O(n²) algorithm
// Current implementation slow for >100 items
std::vector<int> result;  // O(n²)

// FIXME: Temporary workaround
// Bug in framework requires this hack
// Remove after framework v2.0
void WorkaroundBug() {
    // ...
}

// HACK: Known issue
// This violates layering but is necessary for now
// Refactor when architecture allows
void TemporarySolution() {
    // ...
}

// ✅ Review TODOs regularly
// - Remove completed TODOs
// - Update stale TODOs
// - Convert old TODOs to issues
```

**See:** [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md)

---

## 17. BACKWARD COMPATIBILITY

**Focus:** API stability, deprecation

**HIGH Issues:**
- Breaking changes without deprecation 🟠
- Changing API behavior 🟠

**MEDIUM Issues:**
- Missing version tags 🟡

**Key Checks:**
```cpp
// ✅ Deprecate before removing
class MenuPattern {
public:
    // @deprecated Use GetItem(size_t) instead
    // Will be removed in version 2.0
    ACE_DEPRECATED("Use GetItem(size_t) instead")
    MenuItem* GetItemById(int id);

    // New API
    MenuItem* GetItem(size_t index);
};

// ✅ Default parameters for compatibility
void Process(bool enable_new_feature = true);  // Opt-in

// ✅ Version-specific code
#if ACE_VERSION >= ACE_VERSION_CHECK(2, 0, 0)
    // New implementation
#else
    // Legacy implementation
#endif
```

**See:** [COMPATIBILITY.md](COMPATIBILITY.md)

---

## ACE ENGINE SPECIFIC CHECKS

### Architecture Compliance

**Four-Layer Architecture:**
```
Frontend Bridge
    ↓
Component Framework (Pattern/Model/Property)
    ↓
Layout/Render
    ↓
Platform Adapter (OHOS/Preview)
```

**Check:**
- No violations of layer boundaries
- No direct calls to platform from framework layer
- Proper use of interfaces between layers

### Component Structure

```
components_ng/pattern/<component>/
├── *_pattern.h/cpp         # Business logic
├── *_model.h/cpp           # Data model
├── *_layout_property.h/cpp # Layout props
├── *_paint_property.h/cpp  # Render props
└── *_event_hub.h/cpp       # Event handling
```

**Check:**
- Proper separation of concerns
- Pattern only uses Model/Properties/EventHub
- No cross-contamination

### RefPtr Usage

```cpp
// ✅ Creation
auto node = AceType::MakeRefPtr<FrameNode>();

// ✅ Type-safe casting
auto pattern = AceType::DynamicCast<MenuPattern>(node->GetPattern());
if (!pattern) { /* handle */ }

// ✅ Breaking cycles
class Child {
    WeakPtr<Parent> parent_;  // Use weak, not strong
};

// ✅ Safe callbacks
auto weak = AceType::WeakClaim(this);
PostTask([weak]() {
    auto pattern = AceType::DynamicCast<MenuPattern>(weak.Upgrade());
    if (pattern) pattern->Update();
});
```

### Naming Conventions

```cpp
class MenuPattern {           // PascalCase
public:
    void OnModifyDone();      // PascalCase
    int GetWidth() const;     // Get prefix

private:
    int width_;               // snake_case_ with trailing underscore
    std::string component_id_;  // Abbreviations lowercase
};

constexpr int MAX_MENU_ITEMS = 100;  // UPPER_CASE for constants
```

---

## Review Workflow

1. **Quick Scan** (5 min)
   - Check CRITICAL issues
   - Verify architecture compliance
   - Review naming conventions

2. **Detailed Review** (15-30 min)
   - Go through each dimension
   - Document issues with severity
   - Provide specific examples

3. **Report Generation**
   - Prioritize by severity
   - Include refactoring suggestions
   - Track technical debt

---

## Common Issue Patterns

| Pattern | Dimension | Severity | Fix |
|---------|-----------|----------|-----|
| Raw pointer | Memory | HIGH | Use RefPtr |
| No input validation | Security | CRITICAL | Add validation |
| Nested loops | Performance | HIGH | Use hash table |
| Long method | Code Smell | MEDIUM | Extract method |
| No error handling | Stability | HIGH | Add error checks |
| Hard-coded dependency | Testability | HIGH | Dependency injection |
| Missing logging | Observability | MEDIUM | Add logs |
| Circular reference | Memory | HIGH | Use WeakPtr |

---

## Tools Integration

```bash
# Static analysis
cppcheck --enable=all path/to/code

# Memory checking
valgrind --leak-check=full ./program

# Thread checking
helgrind ./program

# Complexity
lizard path/to/code

# Duplication
cpd --minimum-tokens 100 path/to/code
```

---

For detailed information on each dimension, see the specific reference files.
