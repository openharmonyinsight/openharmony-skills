# ACE Engine Specific Code Review Guidelines

## Overview

This document covers ACE Engine (OpenHarmony ArkUI framework) specific code review guidelines, architecture rules, and best practices.

---

## Architecture Compliance

### Four-Layer Architecture

ACE Engine follows a strict four-layer architecture. Code must respect layer boundaries.

```
┌─────────────────────────────────────────────────────────┐
│  1. Frontend Bridge Layer                              │
│  frameworks/bridge/declarative_frontend/                │
│  - ArkTS/TS code parsing                               │
│  - Component tree building                              │
│  - State management                                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  2. Component Framework Layer                          │
│  frameworks/core/components_ng/                         │
│  - Pattern (business logic)                            │
│  - Model (data interface)                              │
│  - Property (layout/paint)                             │
│  - EventHub (event handling)                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  3. Layout/Render Layer                                │
│  frameworks/core/components_ng/layout/                 │
│  frameworks/core/components_ng/render/                 │
│  - Layout algorithms                                   │
│  - Render nodes                                        │
│  - Drawing pipeline                                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  4. Platform Adapter Layer                             │
│  adapter/ohos/ or adapter/preview/                     │
│  - Platform abstraction                                │
│  - OHOS: Rosen (display, window)                       │
│  - Preview: Simulation                                 │
└─────────────────────────────────────────────────────────┘
```

### Layer Boundary Rules

**❌ VIOLATIONS:**
```cpp
// ❌ BAD: Component directly calling platform
class MenuPattern {
    void Show() {
        Rosen::WindowManager::GetInstance()->Show();  // Violates layering!
    }
};

// ❌ BAD: Frontend calling render directly
class JsFrontend {
    void Render() {
        auto renderNode = new RenderNode();  // Should use Pattern!
    }
};
```

**✅ CORRECT:**
```cpp
// ✅ GOOD: Proper layering
class MenuPattern {
    void Show() {
        // Pattern uses render node abstraction
        auto renderNode = GetRenderNode();
        renderNode->SetVisible(true);
    }
};

// Render node delegates to platform adapter
class MenuRenderNode {
    void SetVisible(bool visible) {
        // Platform adapter handles platform-specific code
        Platform::GetWindowAdapter()->SetVisible(visible);
    }
};
```

---

## Component Structure

### NG Architecture Pattern

Each component must follow the Pattern/Model/Property separation:

```
components_ng/pattern/<component>/
├── <component>_pattern.h/cpp         # Main pattern class
├── <component>_model_ng.h/cpp        # Data model interface
├── <component>_layout_property.h/cpp # Layout properties
├── <component>_paint_property.h/cpp  # Render properties
└── <component>_event_hub.h/cpp       # Event handling
```

### Pattern Class Responsibilities

**MenuPattern (Business Logic):**
```cpp
class MenuPattern : public FrameNodePattern {
public:
    // Lifecycle methods
    void OnModifyDone() override;
    void OnDirtyLayoutWrapperSwap() override;

    // Public API
    void Show();
    void Hide();
    void AddMenuItem(const MenuItemConfig& config);

    // Pattern-specific logic
    bool IsMenuShown() const;
    int GetSelectedIndex() const;

private:
    // Dependencies (not implementation!)
    RefPtr<MenuLayoutProperty> layout_property_;
    RefPtr<MenuPaintProperty> paint_property_;
    RefPtr<MenuEventHub> event_hub_;
};
```

**Model (Data Interface):**
```cpp
class MenuModel {
public:
    virtual ~MenuModel() = default;

    // Data access
    virtual size_t GetItemCount() const = 0;
    virtual MenuItem GetItem(size_t index) const = 0;
    virtual void AddItem(const MenuItem& item) = 0;
    virtual void RemoveItem(size_t index) = 0;

    // State queries
    virtual bool IsEnabled() const = 0;
    virtual int GetSelectedIndex() const = 0;
};
```

**LayoutProperty (Layout Properties):**
```cpp
class MenuLayoutProperty : public LayoutProperty {
public:
    // Property setters
    void SetWidth(int width);
    void SetHeight(int height);
    void SetPosition(const Offset& pos);

    // Property getters
    int GetWidth() const;
    int GetHeight() const;
    Offset GetPosition() const;

    // Dirty marking
    void MarkDirty();

private:
    int width_ = 0;
    int height_ = 0;
    Offset position_;
};
```

**PaintProperty (Render Properties):**
```cpp
class MenuPaintProperty : public PaintProperty {
public:
    void SetBackgroundColor(const Color& color);
    void SetBorderColor(const Color& color);
    void SetBorderWidth(int width);

    Color GetBackgroundColor() const;
    Color GetBorderColor() const;
    int GetBorderWidth() const;

private:
    Color background_color_;
    Color border_color_;
    int border_width_ = 0;
};
```

**EventHub (Event Handling):**
```cpp
class MenuEventHub {
public:
    using EventCallback = std::function<void()>;

    void SetOnClick(EventCallback callback);
    void SetOnFocus(EventCallback callback);
    void SetOnBlur(EventCallback callback);

    void FireClick();
    void FireFocus();
    void FireBlur();

private:
    EventCallback on_click_;
    EventCallback on_focus_;
    EventCallback on_blur_;
};
```

### Separation of Concerns Checklist

**Pattern:**
- [ ] Only contains business logic
- [ ] Doesn't contain layout algorithms (delegates to LayoutWrapper)
- [ ] Doesn't contain drawing code (delegates to RenderNode)
- [ ] Uses properties to access data
- [ ] Uses event hub for events

**Model:**
- [ ] Only defines data interface
- [ ] No UI logic
- [ ] No rendering logic
- [ ] Platform-independent data structures

**LayoutProperty:**
- [ ] Only layout-related properties
- [ ] No business logic
- [ ] Mark dirty when properties change

**PaintProperty:**
- [ ] Only render-related properties
- [ ] No business logic
- [ ] Mark dirty when properties change

**EventHub:**
- [ ] Only event handling
- [ ] No business logic
- [ ] Callback-based events

---

## RefPtr Usage Guidelines

### Creation

```cpp
// ✅ GOOD: Use MakeRefPtr
auto pattern = AceType::MakeRefPtr<MenuPattern>();
auto node = AceType::MakeRefPtr<FrameNode>(nodeId);

// ❌ BAD: Manual new (not wrapped in RefPtr)
RefPtr<MenuPattern> pattern = new MenuPattern();  // WRONG!
```

### Type-Safe Casting

```cpp
// ✅ GOOD: DynamicCast with null check
auto menu_pattern = AceType::DynamicCast<MenuPattern>(node->GetPattern());
if (!menu_pattern) {
    LOGE("Failed to get MenuPattern from node");
    return false;
}
menu_pattern->DoSomething();

// ❌ BAD: static_cast without check
auto* menu_pattern = static_cast<MenuPattern*>(node->GetPattern());
menu_pattern->DoSomething();  // May crash if wrong type!
```

### Breaking Circular References

```cpp
// ❌ BAD: Circular reference (memory leak)
class MenuItem {
public:
    RefPtr<Menu> parent_menu_;  // Strong reference
};

class Menu {
public:
    std::vector<RefPtr<MenuItem>> items_;  // Strong references
};
// Cycle: Menu -> MenuItem -> Menu

// ✅ GOOD: Use WeakPtr to break cycle
class MenuItem {
public:
    WeakPtr<Menu> parent_menu_;  // Weak reference
};

class Menu {
public:
    std::vector<RefPtr<MenuItem>> items_;
};
// No cycle, proper cleanup

// Usage:
auto menu = AceType::DynamicCast<Menu>(parent_menu_.Upgrade());
if (menu) {
    menu->DoSomething();
}
```

### Callback Safety

```cpp
// ❌ BAD: Capturing raw this in async callback
class MenuPattern {
public:
    void ScheduleUpdate() {
        PostTask([this]() {  // Dangerous! Object may be destroyed
            UpdateMenu();
        });
    }
};

// ✅ GOOD: Capture WeakPtr
class MenuPattern {
public:
    void ScheduleUpdate() {
        auto weak = AceType::WeakClaim(this);
        PostTask([weak]() {
            auto pattern = AceType::DynamicCast<MenuPattern>(weak.Upgrade());
            if (pattern) {  // Check object still alive
                pattern->UpdateMenu();
            }
        });
    }
};
```

### Returning RefPtr

```cpp
// ✅ GOOD: Return RefPtr from factory
RefPtr<MenuPattern> MenuPattern::Create() {
    auto pattern = AceType::MakeRefPtr<MenuPattern>();
    pattern->Initialize();
    return pattern;
}

// ✅ GOOD: Pass RefPtr by const reference for efficiency
void ProcessMenu(const RefPtr<MenuPattern>& menu) {
    menu->Update();
}

// ✅ GOOD: Return RefPtr to keep object alive
RefPtr<RenderNode> GetRenderNode() {
    return render_node_;  // Caller gets shared ownership
}
```

---

## Component Lifecycle Methods

### OnModifyDone

Called when component properties are modified.

```cpp
void MenuPattern::OnModifyDone() {
    // Called after properties are set/modified
    // Use this to trigger updates based on new property values

    // Example: Update layout when size changes
    auto layout_prop = GetLayoutProperty<MenuLayoutProperty>();
    if (layout_prop && layout_prop->IsWidthChanged()) {
        MarkDirty();
    }
}
```

### OnDirtyLayoutWrapperSwap

Called when the layout wrapper is swapped (typically during rebuilds).

```cpp
void MenuPattern::OnDirtyLayoutWrapperSwap() {
    // Called when layout wrapper is being replaced
    // Use this to transfer state from old to new wrapper

    auto old_wrapper = GetOldLayoutWrapper();
    auto new_wrapper = GetNewLayoutWrapper();

    // Preserve layout state
    if (old_wrapper && new_wrapper) {
        new_wrapper->SetPosition(old_wrapper->GetPosition());
        new_wrapper->SetSize(old_wrapper->GetSize());
    }
}
```

### OnAttachToFrameNode

Called when pattern is attached to a frame node.

```cpp
void MenuPattern::OnAttachToFrameNode(FrameNode* node) {
    // One-time initialization after attachment
    // Set up event listeners, initial state, etc.

    auto hub = GetEventHub<MenuEventHub>();
    if (hub) {
        hub->SetOnClick([weak = WeakClaim(this)]() {
            auto pattern = weak.Upgrade();
            if (pattern) pattern->HandleClick();
        });
    }
}
```

---

## Naming Conventions

### Files

```
menu_pattern.h/cpp              # snake_case
menu_layout_property.h/cpp      # snake_case
```

### Classes

```cpp
class MenuPattern {};           // PascalCase
class MenuLayoutProperty {};    // PascalCase
class FrameNode {};             // PascalCase
```

### Methods

```cpp
class MenuPattern {
public:
    void OnModifyDone();              // PascalCase
    void Show();                      // PascalCase

    int GetWidth() const;             // Get prefix for getters
    void SetWidth(int width);         // Set prefix for setters
    bool IsVisible() const;           // Is prefix for booleans
};
```

### Member Variables

```cpp
class MenuPattern {
private:
    int width_;                       // snake_case_ with trailing underscore
    int height_;
    std::string component_id_;        // Abbreviations in lowercase
    RefPtr<MenuLayoutProperty> layout_property_;
};
```

### Constants

```cpp
namespace MenuConstants {
    constexpr int MAX_ITEMS = 100;           // UPPER_CASE
    constexpr int DEFAULT_WIDTH = 200;
    constexpr int DEFAULT_HEIGHT = 300;
}

enum class MenuState {
    COLLAPSED,                         // UPPER_CASE for enums
    EXPANDED,
    ANIMATING
};
```

---

## Common Patterns and Anti-Patterns

### Property Access

```cpp
// ✅ GOOD: Use property methods
auto layout_prop = pattern->GetLayoutProperty<MenuLayoutProperty>();
if (layout_prop) {
    layout_prop->SetWidth(200);
}

// ❌ BAD: Direct member access
pattern->layout_property_->SetWidth(200);  // Bypasses validation
```

### Pattern Access

```cpp
// ✅ GOOD: Safe pattern access
auto pattern = node->GetPattern<MenuPattern>();
if (!pattern) {
    LOGE("Node doesn't have MenuPattern");
    return false;
}
pattern->Show();

// ❌ BAD: Unsafe cast
auto* pattern = static_cast<MenuPattern*>(node->GetPattern());
pattern->Show();  // May crash
```

### Event Handling

```cpp
// ✅ GOOD: Use event hub
auto hub = pattern->GetEventHub<MenuEventHub>();
if (hub) {
    hub->SetOnClick([weak = WeakClaim(pattern)]() {
        auto p = weak.Upgrade();
        if (p) p->HandleClick();
    });
}

// ❌ BAD: Direct event handling
class MenuPattern {
    std::function<void()> click_callback_;
public:
    void SetOnClick(std::function<void()> callback) {
        click_callback_ = callback;  // Should use event hub
    }
};
```

---

## Build System Integration

### Component Registration

**components.gni:**
```python
# ✅ Register new component
ace_components_ng += [
  "menu",
]

# ✅ Add source files
"menu": [
  "//path/to/menu_pattern.cpp",
  "//path/to/menu_layout_property.cpp",
  "//path/to/menu_paint_property.cpp",
  "//path/to/menu_event_hub.cpp",
]
```

### Conditional Compilation

```cpp
// ✅ Use feature flags from ace_config.gni
#if defined(ENABLE_MENU_COMPONENT)
    // Menu-specific code
#endif

// ✅ Platform-specific code
#if defined(PLATFORM_OHOS)
    // OHOS-specific implementation
#elif defined(PLATFORM_PREVIEW)
    // Preview-specific implementation
#endif
```

---

## Testing Guidelines

### Unit Test Structure

```
test/unittest/components_ng/menu/
├── menu_pattern_test.cpp         # Pattern tests
├── menu_layout_property_test.cpp # Property tests
└── menu_event_hub_test.cpp       # Event tests
```

### Test Pattern

```cpp
class MenuPatternTest : public testing::Test {
public:
    void SetUp() override {
        // Create test frame node
        auto node = FrameNode::CreateFrameNode("menu", 1);
        pattern_ = node->GetPattern<MenuPattern>();
        ASSERT_NE(pattern_, nullptr);
    }

    void TearDown() override {
        pattern_.reset();
    }

protected:
    RefPtr<MenuPattern> pattern_;
};

TEST_F(MenuPatternTest, ShowMenu) {
    // Arrange
    ASSERT_FALSE(pattern_->IsShown());

    // Act
    pattern_->Show();

    // Assert
    EXPECT_TRUE(pattern_->IsShown());
}

TEST_F(MenuPatternTest, AddMenuItem_InvalidIndex) {
    // Arrange
    pattern_->AddMenuItem({"Item1"});

    // Act & Assert
    EXPECT_FALSE(pattern_->SelectItem(999));  // Out of bounds
}
```

---

## Performance Considerations

### Layout Performance

```cpp
// ❌ BAD: Always recalculates
Size MenuPattern::Measure() {
    Size size;
    // Expensive calculation every time
    for (auto& item : items_) {
        size.width += item->CalculateWidth();
    }
    return size;
}

// ✅ GOOD: Cache when possible
Size MenuPattern::Measure() {
    if (layout_cache_valid_) {
        return cached_size_;
    }

    Size size;
    for (auto& item : items_) {
        size.width += item->CalculateWidth();
    }

    cached_size_ = size;
    layout_cache_valid_ = true;
    return size;
}

void MenuPattern::MarkDirty() {
    layout_cache_valid_ = false;
    Pattern::MarkDirty();
}
```

### Dirty Marking

```cpp
// ✅ GOOD: Mark dirty only when needed
void MenuLayoutProperty::SetWidth(int width) {
    if (width_ != width) {
        width_ = width;
        MarkDirty();  // Only when actually changed
    }
}

// ❌ BAD: Always marks dirty
void MenuLayoutProperty::SetWidth(int width) {
    width_ = width;
    MarkDirty();  // Unnecessary if value unchanged
}
```

---

## Common Mistakes to Avoid

### 1. Bypassing Property System

```cpp
// ❌ BAD: Directly manipulating render node
class MenuPattern {
    void SetBackgroundColor(const Color& color) {
        GetRenderNode()->SetBackgroundColor(color);  // Bypasses property
    }
};

// ✅ GOOD: Use property system
class MenuPattern {
    void SetBackgroundColor(const Color& color) {
        auto paint_prop = GetPaintProperty<MenuPaintProperty>();
        if (paint_prop) {
            paint_prop->SetBackgroundColor(color);  // Proper channel
        }
    }
};
```

### 2. Tight Coupling to Implementation

```cpp
// ❌ BAD: Pattern knows about specific render implementation
class MenuPattern {
    void Render() {
        auto* menu_render = static_cast<MenuRenderNode*>(GetRenderNode());
        menu_render->DrawMenuBackground();  // Tight coupling
    }
};

// ✅ GOOD: Pattern delegates through interface
class MenuPattern {
    void Render() {
        auto render_node = GetRenderNode();
        render_node->Invalidate();  // Abstract interface
    }
};
```

### 3. Ignoring Lifecycle

```cpp
// ❌ BAD: Initialization in constructor
class MenuPattern {
public:
    MenuPattern() {
        // Don't do heavy init here - node not ready
        LoadMenuItems();
        RegisterEventListeners();
    }
};

// ✅ GOOD: Initialization in lifecycle methods
class MenuPattern {
public:
    void OnAttachToFrameNode(FrameNode* node) override {
        LoadMenuItems();
        RegisterEventListeners();
    }
};
```

---

## Integration with Knowledge Base

When reviewing ACE Engine code:

1. **Check component-specific guidance:**
   ```bash
   grep -r "MenuPattern" docs/pattern/
   ```

2. **Review architecture decisions:**
   ```bash
   grep -r "architecture" docs/
   ```

3. **Consult best practices:**
   ```bash
   grep -r "performance" docs/best_practices/
   ```

4. **Update knowledge base:**
   - Document new patterns discovered
   - Record lessons learned
   - Update code references (file:line)

---

## Quick Review Checklist

- [ ] Follows four-layer architecture
- [ ] Proper Pattern/Model/Property separation
- [ ] Uses RefPtr correctly (MakeRefPtr, DynamicCast)
- [ ] Breaks circular references with WeakPtr
- [ ] Callbacks capture WeakPtr
- [ ] Follows naming conventions
- [ ] Proper lifecycle method usage
- [ ] Uses property system (not direct render access)
- [ ] Marks dirty appropriately
- [ ] No platform-specific code in framework layer
- [ ] Component registered in components.gni
- [ ] Has unit tests
- [ ] Integrates with knowledge base

---

## Severity Guidelines for ACE Engine

**CRITICAL:**
- Layer boundary violations 🔴
- Memory leaks in components 🔴
- Crashes in lifecycle methods 🔴
- Missing RefPtr where needed 🔴

**HIGH:**
- Improper Pattern/Model/Property separation 🟠
- Not using property system 🟠
- Unsafe callback captures 🟠
- Missing lifecycle method implementations 🟠

**MEDIUM:**
- Naming convention violations 🟡
- Missing dirty marking 🟡
- Performance issues 🟡

**LOW:**
- Minor style issues 🟢
- Missing documentation 🟢
