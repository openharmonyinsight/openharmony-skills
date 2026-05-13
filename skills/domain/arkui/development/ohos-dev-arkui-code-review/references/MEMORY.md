# ACE Engine Memory Management

Smart pointer conventions specific to ACE Engine. The framework uses `RefPtr` (not `std::shared_ptr`) via the `AceType` reference-counting system.

---

## Object Creation

```cpp
auto pattern = AceType::MakeRefPtr<MenuPattern>(targetId, tag, MenuType::MENU);
auto node = FrameNode::CreateFrameNode("menu", nodeId, pattern);

RefPtr<MenuPattern> pattern = new MenuPattern();  // WRONG!
RefPtr<FrameNode> node = RefPtr<FrameNode>(new FrameNode());  // WRONG!
```

`AceType::MakeRefPtr<T>()` is the only correct way to create RefPtr objects. It ensures the reference count starts at 1 and the type info is registered for DynamicCast.

---

## Type-Safe Casting

```cpp
auto menu_pattern = AceType::DynamicCast<MenuPattern>(node->GetPattern());
if (!menu_pattern) {
    LOGE("Failed to get MenuPattern from node");
    return false;
}

auto* menu_pattern = static_cast<MenuPattern*>(node->GetPattern());
menu_pattern->DoSomething();
```

`DynamicCast` performs a safe runtime type check using ACE Engine's type system. `static_cast` bypasses this and can return a wrong pointer on cross-module boundaries, causing crashes or memory corruption.

---

## Breaking Circular References

```cpp
class MenuItem {
public:
    RefPtr<Menu> parent_menu_;  // Strong reference back to parent
};

class Menu {
public:
    std::vector<RefPtr<MenuItem>> items_;  // Strong references to children
};
// Cycle: Menu -> MenuItem -> Menu — neither will ever be freed

class MenuItem {
public:
    WeakPtr<Menu> parent_menu_;
};

auto menu = AceType::DynamicCast<Menu>(parent_menu_.Upgrade());
if (menu) {
    menu->DoSomething();
}
```

**Rule:** Child-to-parent back-references MUST use `WeakPtr`, not `RefPtr`. This is the single most common cause of memory leaks in ACE Engine components.

---

## Callback Safety

```cpp
class MenuPattern {
public:
    void ScheduleUpdate() {
        PostTask([this]() {
            UpdateMenu();
        });
    }
};

class MenuPattern {
public:
    void ScheduleUpdate() {
        auto weak = AceType::WeakClaim(this);
        PostTask([weak]() {
            auto pattern = AceType::DynamicCast<MenuPattern>(weak.Upgrade());
            if (pattern) {
                pattern->UpdateMenu();
            }
        });
    }
};
```

**Rule:** Never capture raw `this` in `PostTask`, `PostDelayedTask`, or any async callback. Always use `AceType::WeakClaim(this)` + `Upgrade()` check.

The crash depends on timing — in `PostDelayedTask` the object is almost certainly destroyed before the callback fires. In `PostTask` on the same thread it may be safe, but the risk is high enough to always flag.

---

## Ownership Patterns

```cpp
class Component {
    RefPtr<MenuPattern> pattern_;
public:
    Component() : pattern_(AceType::MakeRefPtr<MenuPattern>()) {}
};

class Menu {
    std::vector<RefPtr<MenuItem>> items_;
public:
    void AddItem(const RefPtr<MenuItem>& item) {
        items_.push_back(item);
    }
};
```

## Passing RefPtr & Raw Pointer Returns

```cpp
// Pass RefPtr by const reference for efficiency
void ProcessMenu(const RefPtr<MenuPattern>& menu) {
    menu->UpdateSelectIndex(0);
}

// Some framework methods return raw pointer (not RefPtr)
// e.g., RenderContext* GetRenderContext() const
auto* rc = GetRenderContext();
CHECK_NULL_VOID(rc);
rc->SetVisible(true);
// Raw pointer is safe here — RenderContext lifetime is tied to FrameNode
// which outlives the Pattern that owns it. Just check for null.
```

---

## Severity

| Issue | Severity | Detection |
|-------|----------|-----------|
| `new T()` instead of `MakeRefPtr` | CRITICAL | Raw `new` in component code |
| Circular `RefPtr` cycle | CRITICAL | Parent holds `RefPtr<Child>` AND Child holds `RefPtr<Parent>` |
| `static_cast` on RefPtr types | HIGH | `static_cast<T*>` instead of `DynamicCast<T>()` |
| Raw `this` in PostTask/async callback | HIGH | `[this]` inside lambda passed to PostTask/PostDelayedTask |
| Raw pointer ownership ambiguity | HIGH | `T*` member without clear ownership contract |
