# ACE Engine Specific Code Smells

Domain-specific smells that generic code review misses. These patterns indicate misunderstanding of ACE Engine architecture.

---

## God Pattern (Bloater)

Pattern class handling business logic, event registration, animation, AND layout coordination.

```cpp
class MenuPattern : public Pattern {
    void OnModifyDone() override;       // lifecycle
    void RegisterOnTouch();             // event setup
    void ShowPreviewAnimation();        // animation
    void CalculateMenuPosition();       // layout coordination
    void InitTheme();                   // theming
    void SetAccessibilityAction();      // accessibility
};
```

**Refactoring:** Extract animation into `MenuAnimationHelper`, layout coordination into `MenuLayoutAlgorithm`, theming into `MenuThemeHelper`. Pattern should orchestrate, not implement.

---

## Property Bypass (Coupler)

Pattern directly manipulating render context instead of going through the property system.

```cpp
auto* rc = GetRenderContext();
rc->SetBackgroundColor(color);

auto layoutProp = GetLayoutProperty<MenuLayoutProperty>();
layoutProp->UpdateFontColor(color);
```

**Why dangerous:** Bypasses dirty marking, change notification, and the layout pipeline. Other components subscribed to property changes won't be notified.

---

## Model Used as Data Access (OO Abuser)

Model class providing getters for data access when its real role is property-setting for the frontend bridge.

```cpp
class MenuModel {
    virtual size_t GetItemCount() const = 0;
    virtual MenuItem GetItem(size_t index) const = 0;
};

class MenuModel {
    virtual void SetFontSize(const Dimension& fontSize) = 0;
    virtual void SetWidth(const Dimension& width) = 0;
};
```

**Remember:** Model in ACE Engine is NOT a data-access layer. It is a property-setting interface that bridges ArkTS to the component framework.

---

## Constructor Initialization (Change Preventer)

Pattern accessing FrameNode-dependent resources in constructor when the node is not yet attached.

```cpp
MenuPattern() {
    auto host = GetHost();  // nullptr!
    auto prop = GetLayoutProperty<MenuLayoutProperty>();  // nullptr!
}

void OnAttachToFrameNode() override {
    RegisterOnTouch();
    InitTheme(host, theme);
}
```

---

## EventHub Bypass (Coupler)

Pattern storing event callbacks directly instead of using EventHub subclass or GestureEventHub.

```cpp
class MenuPattern {
    std::function<void()> onClickCallback_;
public:
    void SetOnClick(std::function<void()> cb) { onClickCallback_ = cb; }
};

auto gestureHub = GetEventHub<EventHub>()->GetOrCreateGestureEventHub();
gestureHub->SetUserOnClick(std::move(callback));
```

---

## Severity & Priority

| Smell | Severity | Priority | Refactoring |
|-------|----------|----------|-------------|
| God Pattern | HIGH | Immediate | Extract helper classes, Pattern orchestrates |
| Property Bypass | HIGH | Immediate | Use property system (GetLayoutProperty/GetPaintProperty) |
| Constructor Init | HIGH | Immediate | Move to OnAttachToFrameNode() |
| Model as Data Access | HIGH | Soon | Model = property-setting bridge for frontend |
| EventHub Bypass | MEDIUM | Soon | Use EventHub subclass or GestureEventHub |
