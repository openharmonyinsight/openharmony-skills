# Code Smells Detection Guide

## Overview

Code smells are symptoms of deeper design problems. They don't prevent code from working but indicate areas that need refactoring.

## Classification

1. **Bloaters** - Code that grows too large
2. **Object-Orientation Abusers** - Improper use of OOP
3. **Change Preventers** - Hard to modify
4. **Dispensables** - Unnecessary code
5. **Couplers** - Excessive coupling

---

## 1. Bloaters

### Long Method

**Symptom:** Method is too long (>50 lines)

**Why it's bad:**
- Hard to understand
- Hard to reuse
- Hard to test
- Often does multiple things

**Detection:**
```cpp
// ❌ BAD: 100+ lines doing everything
void MenuPattern::ProcessMenuItem() {
    // 20 lines: validation
    // 30 lines: data loading
    // 20 lines: UI update
    // 15 lines: event handling
    // 15 lines: cleanup
}
```

**Refactoring: Extract Method**
```cpp
// ✅ GOOD: Decompose into smaller methods
void MenuPattern::ProcessMenuItem() {
    if (!ValidateMenuItem()) {
        return;
    }
    auto data = LoadMenuItemData();
    UpdateMenuItemUI(data);
    HandleMenuItemEvents();
}
```

**Severity:** MEDIUM

---

### Large Class

**Symptom:** Class is too large (>500 lines or >10 responsibilities)

**Why it's bad:**
- Does too many things (violates SRP)
- Hard to understand
- Hard to modify
- Hard to test

**Detection:**
```cpp
// ❌ BAD: God object
class MenuPattern {
    // 50 methods for layout
    // 30 methods for rendering
    // 40 methods for event handling
    // 20 methods for data management
    // 30 methods for state management
    // 100+ member variables
};
```

**Refactoring: Extract Class**
```cpp
// ✅ GOOD: Separate concerns
class MenuPattern {
    RefPtr<MenuLayoutAlgorithm> layout_;
    RefPtr<MenuRenderNode> render_;
    RefPtr<MenuEventHandler> events_;
    RefPtr<MenuStateManager> state_;
};

class MenuLayoutAlgorithm { /* Layout only */ };
class MenuRenderNode { /* Render only */ };
class MenuEventHandler { /* Events only */ };
class MenuStateManager { /* State only */ };
```

**Severity:** HIGH

---

### Primitive Obsession

**Symptom:** Using primitive types instead of small objects

**Why it's bad:**
- Loses type safety
- Hard to maintain
- Code duplication

**Detection:**
```cpp
// ❌ BAD: Primitives everywhere
void DrawMenu(int x, int y, int width, int height, int color, int z_order);
bool IsMenuVisible(int menu_id);

void SetPosition(int x, int y);
void SetSize(int width, int height);
```

**Refactoring: Replace Primitive with Object**
```cpp
// ✅ GOOD: Meaningful types
struct Point { int x; int y; };
struct Size { int width; int height; };
struct Rect { Point origin; Size size; };
struct Color { int r, g, b, a; };

void DrawMenu(const Rect& bounds, const Color& color, int z_order);
bool IsMenuVisible(MenuId id);

void SetPosition(const Point& pos);
void SetSize(const Size& size);
```

**Severity:** MEDIUM

---

### Long Parameter List

**Symptom:** More than 4 parameters

**Why it's bad:**
- Hard to remember
- Hard to use
- Often indicates missing abstraction

**Detection:**
```cpp
// ❌ BAD: Too many parameters
void CreateMenuItem(const std::string& text, int icon, bool enabled,
                    void (*callback)(), void* user_data,
                    int position, bool separator, int priority);
```

**Refactoring: Introduce Parameter Object**
```cpp
// ✅ GOOD: Parameter object
struct MenuItemConfig {
    std::string text;
    int icon = 0;
    bool enabled = true;
    std::function<void()> callback;
    int position = -1;
    bool separator = false;
    int priority = 0;
};

void CreateMenuItem(const MenuItemConfig& config);
```

**Severity:** MEDIUM

---

### Data Clumps

**Symptom:** Same group of variables always together

**Why it's bad:**
- Indicates missing abstraction
- Data should be together

**Detection:**
```cpp
// ❌ BAD: Data clumps
void Draw(int x, int y);
void Move(int x, int y);
void Resize(int width, int height);

// Always together
class MenuItem {
    int start_x, start_y;
    int end_x, end_y;
};
```

**Refactoring: Extract Class/Object**
```cpp
// ✅ GOOD: Group related data
struct Point { int x, y; };
struct Size { int width, int height; };

void Draw(const Point& pos);
void Move(const Point& pos);
void Resize(const Size& size);

class MenuItem {
    Point start;
    Point end;
};
```

**Severity:** LOW

---

## 2. Object-Orientation Abusers

### Switch Statements

**Symptom:** Same switch scattered across code

**Why it's bad:**
- Hard to extend (violates OCP)
- Duplicated logic
- Violates polymorphism

**Detection:**
```cpp
// ❌ BAD: Repeated switches
void ProcessEvent(Event* e) {
    switch (e->type) {
        case CLICK: HandleClick(); break;
        case HOVER: HandleHover(); break;
    }
}

void RenderEvent(Event* e) {
    switch (e->type) {
        case CLICK: RenderClick(); break;
        case HOVER: RenderHover(); break;
    }
}
```

**Refactoring: Replace Conditional with Polymorphism**
```cpp
// ✅ GOOD: Polymorphism
class EventHandler {
public:
    virtual void Process() = 0;
    virtual void Render() = 0;
};

class ClickEventHandler : public EventHandler {
public:
    void Process() override { HandleClick(); }
    void Render() override { RenderClick(); }
};

// Or use std::variant (modern C++)
```

**Severity:** MEDIUM

---

### Temporary Field

**Symptom:** Variables only used in certain situations

**Why it's bad:**
- Indicates unclear class responsibility
- Hard to understand valid state

**Detection:**
```cpp
// ❌ BAD: Temporary fields
class MenuPattern {
    double temp_calculation_;  // Only used during layout
    void* temp_context_;       // Only used during initialization
};
```

**Refactoring: Extract Class**
```cpp
// ✅ GOOD: Separate class for specific use
class MenuLayoutContext {
    double calculation_;
};

class MenuPattern {
    void PerformLayout() {
        MenuLayoutContext ctx;
        // Use ctx during layout only
    }
};
```

**Severity:** LOW

---

### Refused Bequest

**Symptom:** Subclass doesn't use superclass methods

**Why it's bad:**
- Indicates wrong inheritance
- Violations of LSP

**Detection:**
```cpp
// ❌ BAD: Refused bequest
class MenuPattern {
public:
    virtual void SaveState() { /* Default impl */ }
    virtual void LoadState() { /* Default impl */ }
};

class ContextMenuPattern : public MenuPattern {
public:
    void SaveState() override {
        throw std::runtime_error("Not supported");  // Refuses bequest
    }
};
```

**Refactoring: Restructure Hierarchy**
```cpp
// ✅ GOOD: Proper hierarchy
class StatefulMenu {
public:
    virtual void SaveState() = 0;
    virtual void LoadState() = 0;
};

class StatelessMenu {
    // No state methods
};

class RegularMenu : public StatefulMenu { /* ... */ };
class ContextMenu : public StatelessMenu { /* ... */ };
```

**Severity:** MEDIUM

---

### Alternative Classes with Different Interfaces

**Symptom:** Classes that do same thing but differently

**Why it's bad:**
- Confusing to users
- Hard to switch between implementations

**Detection:**
```cpp
// ❌ BAD: Different interfaces
class MenuRenderer {
    void Draw(int x, int y);
};

class ButtonRenderer {
    void RenderAt(int x, int y);
};

// Both do same thing!
```

**Refactoring: Unify Interfaces**
```cpp
// ✅ GOOD: Common interface
class Renderer {
public:
    virtual void Draw(const Point& pos) = 0;
};

class MenuRenderer : public Renderer { /* ... */ };
class ButtonRenderer : public Renderer { /* ... */ };
```

**Severity:** MEDIUM

---

## 3. Change Preventers

### Divergent Change

**Symptom:** One class requires many different kinds of changes

**Why it's bad:**
- Violates SRP
- Changes affect unrelated code

**Detection:**
```cpp
// ❌ BAD: Divergent change
class MenuPattern {
    // Changes for layout logic
    void UpdateLayout();

    // Changes for rendering
    void UpdateRender();

    // Changes for database
    void SaveToDB();

    // Changes for networking
    void SendOverNetwork();
};
```

**Refactoring: Extract Class**
```cpp
// ✅ GOOD: Separate classes
class MenuPattern { void UpdateLayout(); };
class MenuRenderer { void UpdateRender(); };
class MenuStorage { void SaveToDB(); };
class MenuNetwork { void SendOverNetwork(); };
```

**Severity:** HIGH

---

### Shotgun Surgery

**Symptom:** One change requires modifying many classes

**Why it's bad:**
- High coupling
- Easy to miss something

**Detection:**
```cpp
// ❌ BAD: Adding new menu type requires changes in:
// - MenuPattern, MenuLayout, MenuRender, MenuEvent,
//   MenuStorage, MenuNetwork... (6+ files!)

// All have switches like:
if (type == "context") { /* ... */ }
else if (type == "dropdown") { /* ... */ }
```

**Refactoring: Move Method/Field, Inline Class**
```cpp
// ✅ GOOD: Centralize configuration
class MenuConfig {
    std::string type_;
    LayoutStrategy layout_;
    RenderStrategy render_;
};

// Add new type by adding new config, not changing code
MenuConfig context_menu_config {
    "context",
    ContextLayoutStrategy(),
    ContextRenderStrategy()
};
```

**Severity:** HIGH

---

## 4. Dispensables

### Duplicate Code

**Symptom:** Same code in multiple files

**Why it's bad:**
- Maintenance nightmare
- Bug fixes need to be in multiple files
- Violates DRY

**Detection:**
```cpp
// ❌ BAD: Duplicate code
void ButtonPattern::UpdateLayout() {
    auto prop = GetLayoutProperty();
    if (!prop) return;
    prop->UpdateWidth(width_);
    prop->UpdateHeight(height_);
    MarkDirty();
}

void TextPattern::UpdateLayout() {
    auto prop = GetLayoutProperty();
    if (!prop) return;
    prop->UpdateWidth(width_);
    prop->UpdateHeight(height_);
    MarkDirty();
}
```

**Refactoring: Extract Method**
```cpp
// ✅ GOOD: Common base
class PatternBase {
protected:
    void UpdateCommonLayout(int w, int h) {
        auto prop = GetLayoutProperty();
        if (!prop) return;
        prop->UpdateWidth(w);
        prop->UpdateHeight(h);
        MarkDirty();
    }
};

void ButtonPattern::UpdateLayout() {
    UpdateCommonLayout(width_, height_);
}
```

**Severity:** MEDIUM

---

### Dead Code

**Symptom:** Code that's never executed

**Why it's bad:**
- Wastes space
- Confusing to readers
- Maintenance burden

**Detection:**
```cpp
// ❌ BAD: Dead code
class MenuPattern {
    void OldImplementation() { /* Never called */ }

    int unused_variable_;

    void DeadMethod() {
        if (false) { /* Never reached */ }
    }
};
```

**Refactoring: Remove Dead Code**
```cpp
// ✅ GOOD: Clean
class MenuPattern {
    // Only active code
};
```

**Severity:** LOW

---

### Lazy Class

**Symptom:** Class that does very little

**Why it's bad:**
- Unnecessary complexity
- Maintenance cost without benefit

**Detection:**
```cpp
// ❌ BAD: Lazy class
class MenuData {
public:
    int GetCount() const { return count_; }
    void SetCount(int c) { count_ = c; }
private:
    int count_;
};
// Just a wrapper around int!
```

**Refactoring: Inline Class**
```cpp
// ✅ GOOD: Just use int
int menu_count;
```

**Severity:** LOW

---

### Speculative Generality

**Symptom:** Unnecessary abstraction

**Why it's bad:**
- Over-engineering
- Harder to understand
- YAGNI (You Aren't Gonna Need It)

**Detection:**
```cpp
// ❌ BAD: Speculative generality
template<typename T, typename U, typename V>
class AbstractMenuFactoryBuilder {
    // Complex hierarchy for... one menu type?
};
```

**Refactoring: Simplify**
```cpp
// ✅ GOOD: Simple implementation
class MenuFactory {
    RefPtr<Menu> CreateMenu();
};
```

**Severity:** LOW

---

### Comments

**Symptom:** Excessive comments explaining "what" not "why"

**Why it's bad:**
- Code should be self-documenting
- Comments get out of date
- Often indicate bad code

**Detection:**
```cpp
// ❌ BAD: Comments explaining what
// Set the width to 100
width_ = 100;

// Check if item is valid
if (item.IsValid()) {
    // Process the item
    Process(item);
}
```

**Refactoring: Rename/Extract Method**
```cpp
// ✅ GOOD: Self-documenting code
width_ = STANDARD_MENU_WIDTH;  // Comment explains why, not what

if (item.IsValid()) {
    ProcessValidItem(item);  // Method name explains
}
```

**Severity:** LOW

---

## 5. Couplers

### Feature Envy

**Symptom:** Method more interested in another class

**Why it's bad:**
- Breaks encapsulation
- High coupling

**Detection:**
```cpp
// ❌ BAD: Feature envy
class MenuPattern {
public:
    void UpdateButtonStyle() {
        auto button = GetButton();
        // Lots of accessing button's internals
        button->layout_property_->UpdateWidth(100);
        button->layout_property_->UpdateHeight(50);
        button->render_property_->SetColor(RED);
        button->SetEnabled(true);
    }
};
```

**Refactoring: Move Method**
```cpp
// ✅ GOOD: Method in right class
class MenuPattern {
public:
    void UpdateButtonStyle() {
        button_->ApplyMenuStyle();
    }
};

class ButtonPattern {
public:
    void ApplyMenuStyle() {
        layout_property_->UpdateWidth(100);
        layout_property_->UpdateHeight(50);
        render_property_->SetColor(RED);
        SetEnabled(true);
    }
};
```

**Severity:** MEDIUM

---

### Inappropriate Intimacy

**Symptom:** Classes too intimate with each other's internals

**Why it's bad:**
- Breaks encapsulation
- Tight coupling

**Detection:**
```cpp
// ❌ BAD: Inappropriate intimacy
class MenuPattern {
public:
    void AccessButtonInternals() {
        auto button = GetButton();
        button->private_data_ = 123;  // Access private!
        button->private_method_();    // Call private!
    }
};
```

**Refactoring: Use Public API**
```cpp
// ✅ GOOD: Public interface
class MenuPattern {
public:
    void ConfigureButton() {
        button_->SetConfiguration(123);
    }
};
```

**Severity:** MEDIUM

---

### Message Chains

**Symptom:** Long chains of calls

**Why it's bad:**
- Fragile (breaks if intermediate changes)
- Hard to follow

**Detection:**
```cpp
// ❌ BAD: Message chain
auto value = GetPattern()
                ->GetLayoutProperty()
                    ->GetPaddingProperty()
                        ->GetLeft()
                            ->GetValue();
```

**Refactoring: Hide Delegate**
```cpp
// ✅ GOOD: Encapsulate
class MenuPattern {
public:
    int GetLeftPadding() {
        return layout_property_->GetLeftPadding();
    }
};

auto value = GetPattern()->GetLeftPadding();
```

**Severity:** MEDIUM

---

### Middle Man

**Symptom:** Class just delegates to another

**Why it's bad:**
- Unnecessary indirection
- Often should be removed

**Detection:**
```cpp
// ❌ BAD: Middle man
class MenuPattern {
public:
    void UpdateWidth() { layout_->UpdateWidth(); }
    void UpdateHeight() { layout_->UpdateHeight(); }
    void GetPadding() { return layout_->GetPadding(); }
    // ... 20 forwarding methods
};
```

**Refactoring: Remove Middle Man**
```cpp
// ✅ GOOD: Direct access
auto layout = menu->GetLayout();
layout->UpdateWidth();
layout->UpdateHeight();
```

**Severity:** LOW

---

## Detection Tools

### Static Analysis

```bash
# PMD for Java-like smells
# Cppcheck for C++
cppcheck --enable=all path/to/code

# SonarQube (comprehensive)
# Detects complexity, duplication, etc.
```

### Metrics

- **Cyclomatic Complexity:** >10 indicates complex method
- **Lines of Code:** >50 lines per method
- **Parameters:** >4 parameters
- **Class Size:** >500 lines
- **Duplication:** >3% duplicated code

### Manual Detection Look For

- Long methods/functions
- Large classes
- Repeated code patterns
- Many similar if/else or switch statements
- Methods with many parameters
- Classes with many fields
- Deep nesting
- Comments explaining "what" code does

## Refactoring Priority

**Immediate (HIGH):**
- Large Class
- Divergent Change
- Shotgun Surgery
- Duplicate Code (significant)

**Soon (MEDIUM):**
- Long Method
- Feature Envy
- Switch Statements
- Inappropriate Intimacy
- Message Chains

**When Time (LOW):**
- Data Clumps
- Primitive Obsession
- Dead Code
- Lazy Class
- Comments
- Middle Man

## Quick Reference Table

| Smell | Severity | Refactoring | Priority |
|-------|----------|-------------|----------|
| Long Method | MEDIUM | Extract Method | Medium |
| Large Class | HIGH | Extract Class | High |
| Primitive Obsession | MEDIUM | Replace with Object | Medium |
| Long Parameter List | MEDIUM | Parameter Object | Medium |
| Data Clumps | LOW | Extract Class | Low |
| Switch Statements | MEDIUM | Polymorphism | Medium |
| Temporary Field | LOW | Extract Class | Low |
| Refused Bequest | MEDIUM | Restructure | Medium |
| Divergent Change | HIGH | Extract Class | High |
| Shotgun Surgery | HIGH | Move Field/Method | High |
| Duplicate Code | MEDIUM | Extract Method | Medium |
| Dead Code | LOW | Delete | Low |
| Lazy Class | LOW | Inline Class | Low |
| Feature Envy | MEDIUM | Move Method | Medium |
| Inappropriate Intimacy | MEDIUM | Use Public API | Medium |
| Message Chains | MEDIUM | Hide Delegate | Medium |
| Middle Man | LOW | Remove Middle Man | Low |
