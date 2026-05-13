# SOLID Violations in ACE Engine

Detection patterns and refactoring guidance specific to the ACE Engine codebase.

---

## SRP Violation: Pattern doing layout

```cpp
class MenuPattern {
    void CalculatePosition() {
        // Complex position math that belongs in LayoutAlgorithm
    }
};

class MenuPattern {
    RefPtr<LayoutAlgorithm> CreateLayoutAlgorithm() override {
        return MakeRefPtr<MenuLayoutAlgorithm>();
    }
};
```

**Refactoring:** Extract animation into `MenuAnimationHelper`, layout coordination into `MenuLayoutAlgorithm`, theming into `MenuThemeHelper`. Pattern should orchestrate, not implement.

---

## OCP Violation: Switch on MenuType in Pattern

```cpp
void UpdateTheme() {
    switch (type_) {
        case MenuType::MENU: ApplyMenuTheme(); break;
        case MenuType::CONTEXT_MENU: ApplyContextMenuTheme(); break;
    }
}

class InnerMenuPattern : public MenuPattern {
    void InitTheme(const RefPtr<FrameNode>& host) override {
        // Desktop/Multi menu specific theme
    }
};
```

---

## LSP Violation: Pattern override changes contract

```cpp
bool IsAtomicNode() const override { return false; }
// If a parent component assumes atomicity, this breaks its behavior silently

// Menu returns false because it contains child menu items — this is correct
// because Menu is a composite node, not an atomic widget.
```

---

## ISP Violation: EventHub with unrelated events

```cpp
// One EventHub handling click, change, submit, scroll — clients forced
// to depend on methods they don't use

class CheckBoxEventHub : public EventHub {
    void SetOnChange(ChangeEvent&&);
    void SetChangeEvent(ChangeEvent&&);
};
// Click events go through GestureEventHub (separate interface)
```

---

## DIP Violation: Pattern directly calling SubwindowManager

```cpp
void HideMenu() {
    SubwindowManager::GetInstance()->HideMenuNG(false);  // Tight coupling
}

void HideMenu() {
    auto context = GetContext();
    CHECK_NULL_VOID(context);
    context->GetOverlayManager()->HideMenu();
}
```

---

## Severity

| Principle | Severity | Key Detection in ACE Engine |
|-----------|----------|-----------------------------|
| SRP | HIGH | Pattern with 200+ methods spanning lifecycle, events, animation, layout, theming, accessibility |
| OCP | HIGH | Switch on MenuType/ComponentType requiring modification for each new variant |
| LSP | MEDIUM | IsAtomicNode() / Measure() override changing semantic contract |
| ISP | MEDIUM | EventHub with click+change+submit+scroll instead of segregated interfaces |
| DIP | HIGH | Pattern calling SubwindowManager::GetInstance() or Rosen:: directly |
