# ACE Engine Stability Patterns

Stability pitfalls specific to ACE Engine that generic C++ review misses.

---

## Unchecked DynamicCast Return

```cpp
auto pattern = AceType::DynamicCast<MenuPattern>(node->GetPattern());
pattern->DoSomething();

auto pattern = AceType::DynamicCast<MenuPattern>(node->GetPattern());
CHECK_NULL_VOID(pattern);
pattern->DoSomething();
```

`DynamicCast` returns nullptr when the type doesn't match. This is common when traversing the node tree — a node you expect to be a MenuPattern might be a different Pattern type. Every DynamicCast result must be checked before use.

---

## OnModifyDone Property Null Check

```cpp
void MenuPattern::OnModifyDone() override {
    auto prop = GetLayoutProperty<MenuLayoutProperty>();
    auto width = prop->GetMenuWidthValue();  // Crash if prop is nullptr or value not set
}

void MenuPattern::OnModifyDone() override {
    auto prop = GetLayoutProperty<MenuLayoutProperty>();
    CHECK_NULL_VOID(prop);
    if (prop->GetMenuWidth().has_value()) {
        auto width = prop->GetMenuWidthValue();
    }
}
```

`OnModifyDone` is called after property updates but properties may not be set yet (first call) or may have been reset. Always check `has_value()` before accessing `GetXxxValue()`.

---

## Constructor Accessing Not-Yet-Attached FrameNode

```cpp
MenuPattern(int32_t id) {
    auto host = GetHost();  // nullptr — node not attached
    auto prop = host->GetLayoutProperty<T>();  // Crash!
}

MenuPattern(int32_t id) : id_(id) {
    // Only store constructor params, nothing else
}

void OnAttachToFrameNode() override {
    auto host = GetHost();  // Now safe
    CHECK_NULL_VOID(host);
    RegisterOnTouch();
    InitTheme();
}
```

---

## Exception Handling Convention

ACE Engine component code does NOT use C++ exceptions. Use error codes, early returns, and null checks.

```cpp
void Process() {
    if (error) {
        throw std::runtime_error("Failed");
    }
}

void Process() {
    if (error) {
        LOGE("Process failed");
        return;
    }
}

// Or use the macro guards:
CHECK_NULL_VOID(ptr);        // Return void if ptr is null
CHECK_NULL_RETURN(ptr, val); // Return val if ptr is null
CHECK_EQUAL_VOID(a, b);      // Return void if a == b
```

---

## Severity

| Issue | Severity | Why |
|-------|----------|-----|
| DynamicCast without null check | HIGH | Null dereference crash when type mismatch occurs |
| OnModifyDone without property null check | HIGH | Crash on first call or after Reset |
| Constructor accessing FrameNode | CRITICAL | Host is nullptr — guaranteed crash |
| throw in component code | HIGH | Exceptions may be caught by unexpected handlers; ACE uses error codes |
| Missing CHECK_NULL_VOID before pointer use | HIGH | Null dereference in lifecycle methods |
