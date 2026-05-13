# ACE Engine Component Lifecycle & Property System

Lifecycle methods, property access patterns, dirty marking, and correct Pattern/Model/EventHub interaction.

---

## Lifecycle Methods

### OnAttachToFrameNode

Called when pattern is attached to a frame node. **No parameters** — access the node via `GetHost()`.

```cpp
// Base class signature (pattern.h):
virtual void OnAttachToFrameNode() {}

// Source: menu_pattern.cpp
void MenuPattern::OnAttachToFrameNode()
{
    RegisterOnTouch();
    auto host = GetHost();
    CHECK_NULL_VOID(host);
    // Register key event handling for menu navigation
    // Register area-changed callback on target node
    // Initialize theme from SelectTheme
}
```

**Rule:** All initialization that requires FrameNode access goes here, NOT in the constructor. The constructor only stores parameters — `GetHost()` returns nullptr until attachment.

### OnModifyDone

Called after component properties are set/modified. Always call `Pattern::OnModifyDone()` first.

```cpp
void MenuPattern::OnModifyDone()
{
    Pattern::OnModifyDone();
    auto host = GetHost();
    CHECK_NULL_VOID(host);
    auto menuLayoutProperty = GetLayoutProperty<MenuLayoutProperty>();
    CHECK_NULL_VOID(menuLayoutProperty);
    if (menuLayoutProperty->GetBorderRadius().has_value()) {
        BorderRadiusProperty borderRadius = menuLayoutProperty->GetBorderRadiusValue();
        if (!borderRadius.HasPercentUnit()) {
            UpdateBorderRadius(host, borderRadius);
        }
    }
    SetAccessibilityAction();
    if (previewMode_ != MenuPreviewMode::NONE) {
        auto node = host->GetChildren().front();
        CHECK_NULL_VOID(node);
        auto scroll = AceType::DynamicCast<FrameNode>(node);
        CHECK_NULL_VOID(scroll);
        auto hub = scroll->GetEventHub<EventHub>();
        CHECK_NULL_VOID(hub);
        auto gestureHub = hub->GetOrCreateGestureEventHub();
        CHECK_NULL_VOID(gestureHub);
        InitPanEvent(gestureHub);
    }
}
```

**Common pitfall:** Properties may not be set yet (first call) or may have been reset. Always check `has_value()` before accessing `GetXxxValue()`.

### OnDirtyLayoutWrapperSwap

Called on main thread to check if content needs re-rendering after layout. Returns `true` to trigger re-render.

```cpp
// Base class signature (pattern.h):
virtual bool OnDirtyLayoutWrapperSwap(
    const RefPtr<LayoutWrapper>& /*dirty*/, const DirtySwapConfig& /*changeConfig*/)
{
    return false;
}

// DirtySwapConfig fields (dirty_flag.h):
struct DirtySwapConfig {
    bool frameSizeChange = false;
    bool frameOffsetChange = false;
    bool contentSizeChange = false;
    bool contentOffsetChange = false;
    bool skipMeasure = false;
    bool skipLayout = false;
};

// Override example:
bool MenuPattern::OnDirtyLayoutWrapperSwap(
    const RefPtr<LayoutWrapper>& dirty, const DirtySwapConfig& config)
{
    if (config.skipMeasure) {
        return false;
    }
    // Handle preview animation, appear animation, clip path, border radius
    return true;
}
```

---

## Property Access Patterns

### Correct: Use property template methods

```cpp
auto layoutProp = GetLayoutProperty<MenuLayoutProperty>();
if (layoutProp) {
    layoutProp->SetMenuWidth(Dimension(200));
}
```

Pattern has no `layout_property_` member — it accesses via `GetLayoutProperty<T>()` which resolves through the attached FrameNode.

### Incorrect: Bypass property system

```cpp
// ❌ BAD: Directly manipulating render context from Pattern
class MenuPattern {
    void SetBackgroundColor(const Color& color) {
        auto* rc = GetRenderContext();
        rc->SetBackgroundColor(color);  // Bypasses PaintProperty
    }
};
```

**Why dangerous:** Bypasses dirty marking, change notification, and the layout pipeline. Other components subscribed to property changes won't be notified. See CODE_SMELLS.md "Property Bypass" for more detail.

### Correct: Set through ModelNG using ACE macros

```cpp
// Source: menu_model_ng.cpp
void MenuModelNG::SetFontColor(FrameNode* frameNode, const std::optional<Color>& color)
{
    CHECK_NULL_VOID(frameNode);
    if (color.has_value()) {
        ACE_UPDATE_NODE_LAYOUT_PROPERTY(MenuLayoutProperty, FontColor, color.value(), frameNode);
        ACE_UPDATE_NODE_LAYOUT_PROPERTY(MenuLayoutProperty, FontColorSetByUser, true, frameNode);
    } else {
        ACE_RESET_NODE_LAYOUT_PROPERTY(MenuLayoutProperty, FontColor, frameNode);
        ACE_RESET_NODE_LAYOUT_PROPERTY(MenuLayoutProperty, FontColorSetByUser, frameNode);
    }
}
```

---

## Pattern-Algorithm Interaction

Pattern delegates to LayoutAlgorithm through the property system, NOT by calling algorithm methods directly.

```cpp
// ❌ BAD: Pattern knows about specific layout algorithm internals
class MenuPattern {
    void DoLayout() {
        auto* algo = static_cast<MenuLayoutAlgorithm*>(GetLayoutAlgorithm());
        algo->SetForceWrap(true);  // Tight coupling
    }
};

// ✅ GOOD: Pattern delegates through property system
class MenuPattern {
    void UpdateLayout() {
        auto layoutProp = GetLayoutProperty<MenuLayoutProperty>();
        if (layoutProp) {
            layoutProp->SetMenuPlacement(Placement::BOTTOM);
            // LayoutAlgorithm reads properties, Pattern doesn't call it directly
        }
    }
};
```

Layout algorithms live in `LayoutAlgorithm` subclasses. Pattern should never contain measure/layout logic — it creates the algorithm via `CreateLayoutAlgorithm()` and the framework calls `Measure()`/`Layout()` on it.

---

## Event Handling Patterns

### Component-specific events: EventHub subclass

```cpp
auto hub = node->GetEventHub<CheckBoxEventHub>();
if (hub) {
    hub->SetOnChange([weak = WeakClaim(node)](bool checked) {
        auto node = weak.Upgrade();
        if (node) { /* handle */ }
    });
}
```

### Click/gesture events: GestureEventHub

```cpp
auto gestureHub = node->GetEventHub<EventHub>()->GetOrCreateGestureEventHub();
gestureHub->SetUserOnClick(GestureEventFunc());
// Or: gestureHub->AddClickEvent(AceType::MakeRefPtr<ClickEvent>(...));
```

### Incorrect: Storing callbacks in Pattern

```cpp
// ❌ BAD: Bypasses EventHub system
class MenuPattern {
    std::function<void()> click_callback_;
public:
    void SetOnClick(std::function<void()> callback) {
        click_callback_ = callback;
    }
};
```

---

## Dirty Marking

### Automatic via property macros

```cpp
ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(MenuWidth, Dimension, PROPERTY_UPDATE_MEASURE);
```

The macro generates an `Update##name` method that compares old vs new value using `NearEqual()` and only sets `UpdatePropertyChangeFlag(changeFlag)` when the value actually changes. `FrameNode::MarkDirtyNode()` is called by the framework when the flag is detected.

This is why manual `MarkDirty()` calls are unnecessary for macro-declared properties.

### Manual dirty marking on FrameNode

When you need to manually trigger a re-measure from Pattern (e.g., after state change not covered by property system):

```cpp
auto host = GetHost();
CHECK_NULL_VOID(host);
host->MarkDirtyNode(PROPERTY_UPDATE_MEASURE);
```

**Rule:** Only use manual `MarkDirtyNode` when the property macro system doesn't cover the change. Compare old vs new value before calling to avoid unnecessary relayouts.

---

## Quick Review Checklist

- [ ] Follows four-layer architecture (no layer boundary violations)
- [ ] Proper Pattern/Model/Property separation
- [ ] Properties accessed via `GetLayoutProperty<T>()` / `GetPaintProperty<T>()`
- [ ] Initialization in `OnAttachToFrameNode()`, not constructor
- [ ] `OnModifyDone()` checks property `has_value()` before access
- [ ] Events use EventHub subclass or GestureEventHub (not stored in Pattern)
- [ ] LayoutAlgorithm handles measure/layout (not Pattern)
- [ ] Dirty marking uses property macros (not manual MarkDirty without comparison)
- [ ] No platform-specific code in framework layer
- [ ] Follows naming conventions (PascalCase methods, snake_case_ members)
