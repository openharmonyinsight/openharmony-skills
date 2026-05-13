# ACE Engine Architecture

Four-layer architecture, component structure, naming conventions, and separation-of-concerns rules.

---

## Four-Layer Architecture

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

// ✅ GOOD: Pattern uses abstract RenderContext
class MenuPattern {
    void Show() {
        auto* renderContext = GetRenderContext();
        if (renderContext) {
            renderContext->SetVisible(true);
        }
    }
};

// Platform abstraction: abstract base in frameworks/core/ + concrete impl in adapter/
// e.g., Clipboard (abstract) in frameworks/core/common/clipboard/clipboard.h
//       ClipboardImpl (OHOS)  in adapter/ohos/osal/clipboard_impl.cpp
//       Clipboard preview      in adapter/preview/osal/clipboard_preview.cpp
// GN build selects the correct adapter source set at compile time.
```

---

## Component Structure (NG Architecture)

Each component follows the Pattern/Model/Property separation:

```
components_ng/pattern/menu/
├── menu_pattern.h/cpp                  # Pattern (business logic, lifecycle)
├── menu_model.h                        # Abstract model interface
├── menu_model_ng.h/cpp                 # NG model implementation
├── menu_layout_property.h/cpp          # Layout properties
├── menu_paint_property.h/cpp           # Paint properties
├── menu_paint_method.h/cpp             # Paint method (drawing)
├── menu_layout_algorithm.h/cpp         # Layout algorithm
├── menu_accessibility_property.h/cpp   # Accessibility
├── menu_view.h/cpp                     # View factory
├── menu_item/                          # Sub-component
│   ├── menu_item_pattern.h/cpp
│   ├── menu_item_event_hub.h           # Sub-component event hub
│   └── ...
├── menu_item_group/                    # Sub-component
└── BUILD.gn                            # Build configuration
```

> **Note:** Not every component has an `_event_hub.h`. Some components (like Menu) handle events
> directly through Pattern members (e.g., `RefPtr<ClickEvent> onClick_`). Sub-components (like
> MenuItem) may have their own EventHub.

### Pattern

```cpp
class MenuPattern : public Pattern, public FocusView {
    DECLARE_ACE_TYPE(MenuPattern, Pattern, FocusView);
public:
    MenuPattern(int32_t targetId, std::string tag, MenuType type);

    // Lifecycle overrides
    void OnModifyDone() override;
    bool OnDirtyLayoutWrapperSwap(
        const RefPtr<LayoutWrapper>& dirty, const DirtySwapConfig& config) override;

    // Factory methods — create sub-objects for the component
    RefPtr<LayoutProperty> CreateLayoutProperty() override;
    RefPtr<PaintProperty> CreatePaintProperty() override;
    RefPtr<LayoutAlgorithm> CreateLayoutAlgorithm() override;
    RefPtr<NodePaintMethod> CreateNodePaintMethod() override;

    // Component-specific API
    void SetMenuShow();
    void HideMenu(bool isMenuOnTouch = false, OffsetF position = OffsetF(),
        const HideMenuType& reason = HideMenuType::NORMAL) const;
    MenuType GetMenuType() const;

private:
    RefPtr<ClickEvent> onClick_;
    RefPtr<TouchEventImpl> onTouch_;
    int32_t targetId_ = -1;
    std::string targetTag_;
    MenuType type_ = MenuType::MENU;
    std::vector<RefPtr<FrameNode>> options_;
    std::vector<RefPtr<FrameNode>> menuItems_;
    bool isMenuShow_ = false;
    bool isFirstShow_ = false;
};
```

**Key point:** Pattern accesses properties via template methods `GetLayoutProperty<T>()`,
`GetPaintProperty<T>()`, `GetEventHub<T>()` inherited from the `Pattern` base class.
It does NOT hold direct `RefPtr<...Property>` member fields — properties live on the FrameNode.

### Model

```cpp
// Abstract interface (menu_model.h)
class MenuModel {
public:
    static MenuModel* GetInstance();
    virtual void Create();
    virtual void SetFontSize(const Dimension& fontSize);
    virtual void SetFontWeight(FontWeight weight);
    virtual void SetFontColor(const std::optional<Color>& color);
    virtual void SetWidth(const Dimension& width);
    // Resource binding
    virtual void CreateWithColorResourceObj(
        const RefPtr<ResourceObject>& resObj, MenuColorType type) = 0;
};

// NG implementation (menu_model_ng.h) — static helpers for FrameNode manipulation
class MenuModelNG : public MenuModel {
    void Create() override;
    void SetFontSize(const Dimension& fontSize) override;
    static RefPtr<FrameNode> CreateMenu();
    static void SetWidth(FrameNode* frameNode, const Dimension& width);
    static void SetFontColor(FrameNode* frameNode, const std::optional<Color>& color);
};
```

**Key point:** Model in ACE Engine is NOT a data-access layer. It is a property-setting
interface that bridges the frontend (ArkTS) to the component framework. Each setter pushes
values onto the `ViewStackProcessor`, which later creates the FrameNode with those properties.

### LayoutProperty

```cpp
class MenuLayoutProperty : public LayoutProperty {
    DECLARE_ACE_TYPE(MenuLayoutProperty, LayoutProperty);
public:
    RefPtr<LayoutProperty> Clone() const override;
    void Reset() override;

    // Each macro generates: SetXxx(), GetXxx(), ResetXxx(), CloneXxx()
    // Dirty flag is set automatically via PROPERTY_UPDATE_MEASURE etc.
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(MenuWidth, Dimension, PROPERTY_UPDATE_MEASURE);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(MenuMaxHeight, Dimension, PROPERTY_UPDATE_MEASURE);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(MenuOffset, NG::OffsetF, PROPERTY_UPDATE_MEASURE);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(TargetSize, NG::SizeF, PROPERTY_UPDATE_MEASURE);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(BorderRadius, NG::BorderRadiusProperty, PROPERTY_UPDATE_MEASURE);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(Title, std::string, PROPERTY_UPDATE_LAYOUT);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(MenuPlacement, Placement, PROPERTY_UPDATE_LAYOUT);
};
```

**Key point:** Properties are declared via `ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP` macro.
The third parameter (`PROPERTY_UPDATE_MEASURE`, `PROPERTY_UPDATE_LAYOUT`, `PROPERTY_UPDATE_RENDER`)
controls the dirty flag automatically — there is no manual `MarkDirty()` call.

### PaintProperty

```cpp
class MenuPaintProperty : public PaintProperty {
    DECLARE_ACE_TYPE(MenuPaintProperty, PaintProperty);
public:
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(EnableArrow, bool, PROPERTY_UPDATE_RENDER);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(ArrowOffset, Dimension, PROPERTY_UPDATE_RENDER);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(ArrowPosition, OffsetF, PROPERTY_UPDATE_RENDER);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(ArrowPlacement, Placement, PROPERTY_UPDATE_RENDER);
    ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(ClipPath, std::string, PROPERTY_UPDATE_RENDER);
};
```

### EventHub

```cpp
// Base EventHub (event_hub.h) — shared infrastructure
class EventHub : public virtual AceType {
    DECLARE_ACE_TYPE(EventHub, AceType);
public:
    const RefPtr<GestureEventHub>& GetOrCreateGestureEventHub();
    const RefPtr<FocusHub>& GetOrCreateFocusHub();
    void SetOnAppear(std::function<void()>&& callback);
    void SetOnDisappear(std::function<void()>&& callback);
    using OnAreaChangedFunc = std::function<void(
        const RectF& oldRect, const OffsetF& oldOrigin,
        const RectF& rect, const OffsetF& origin)>;
    void SetOnAreaChanged(OnAreaChangedFunc&& onAreaChanged);
};

// Component-specific subclass example — CheckBoxEventHub
class CheckBoxEventHub : public EventHub {
    DECLARE_ACE_TYPE(CheckBoxEventHub, EventHub);
public:
    void SetOnChange(ChangeEvent&& changeEvent);
    void SetChangeEvent(ChangeEvent&& changeEvent);
    void UpdateChangeEvent(bool select) const;
};
```

**Key point:** Click events (`onClick`) are NOT in EventHub subclasses — they go through
`EventHub::GetOrCreateGestureEventHub()`. EventHub subclasses handle **component-specific
semantic events** like `onChange`, `onSubmit`, `onSelect`. Some components (like Menu) have
no EventHub subclass and handle events directly in Pattern.

---

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Files | snake_case | `menu_pattern.h/cpp`, `menu_layout_property.h/cpp` |
| Classes | PascalCase | `MenuPattern`, `MenuLayoutProperty`, `FrameNode` |
| Methods | PascalCase | `OnModifyDone()`, `SetMenuShow()`, `GetMenuType() const` |
| Getters | Get prefix | `GetMenuType()`, `GetMenuWidth()` |
| Setters | Set prefix | `SetMenuShow()`, `SetTargetSize()` |
| Boolean getters | Is/Has prefix | `IsMenu()`, `HasBorderRadius()` |
| Members | snake_case_ trailing underscore | `targetId_`, `targetTag_`, `isMenuShow_` |
| Constants | UPPER_CASE | `DEFAULT_CLICK_DISTANCE`, `MAX_SEARCH_DEPTH` |
| Enums | UPPER_CASE values | `MenuType::CONTEXT_MENU`, `MenuPreviewMode::NONE` |

---

## Separation of Concerns Checklist

**Pattern:**
- Only contains business logic and lifecycle
- Creates sub-objects via `CreateLayoutProperty()`, `CreatePaintProperty()`, etc.
- Accesses properties via template methods (`GetLayoutProperty<T>()`), not direct member fields
- Doesn't contain layout algorithms (delegates to `LayoutAlgorithm`)
- Doesn't contain drawing code (delegates to `NodePaintMethod`)

**Model:**
- Provides property setters for the frontend bridge
- Each setter pushes values onto `ViewStackProcessor` or manipulates `FrameNode` directly
- NG version has both virtual overrides and static helpers for FrameNode manipulation

**LayoutProperty:**
- Declared via `ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP` / `ACE_DEFINE_PROPERTY_ITEM_WITH_GROUP` macros
- Dirty flag set automatically by macro's third parameter (`PROPERTY_UPDATE_MEASURE` etc.)
- No manual `MarkDirty()` calls — the property system handles it

**EventHub:**
- Subclass `EventHub` for component-specific semantic events
- Follow `SetXxx`/`FireXxx` naming for callback setters/firers
- Click/gesture events go through `GestureEventHub`, not EventHub subclass

---

## Severity

| Issue | Severity |
|-------|----------|
| Layer boundary violation (framework calling platform directly) | CRITICAL |
| Improper Pattern/Model/Property separation | HIGH |
| Naming convention violations | MEDIUM |
| Missing component registration in build | MEDIUM |
