# ACE Engine Testing, Build System & Source References

Build system integration, testing patterns, property macro internals, and source file paths for verification.

---

## Build System Integration

### Component Registration

```python
# BUILD.gn — source: components_ng/pattern/menu/BUILD.gn
import("//foundation/arkui/ace_engine/frameworks/core/components_ng/components.gni")

build_component_ng("menu_pattern_ng") {
  is_component_model = true

  sources = [
    "menu_pattern.cpp",
    "menu_layout_property.cpp",
    "menu_paint_method.cpp",
    "menu_layout_algorithm.cpp",
    "menu_model_ng.cpp",
    "menu_view.cpp",
  ]

  # Sub-component sources
  sources += [
    "menu_item/menu_item_pattern.cpp",
    "menu_item/menu_item_model_ng.cpp",
    "menu_item_group/menu_item_group_pattern.cpp",
  ]

  # ArkTS bridge sources (conditional on is_component_model)
  ark_sources = [
    "bridge/menu/arkts_native_menu_bridge.cpp",
    "bridge/menu/menu_dynamic_modifier.cpp",
  ]
}
```

**Key point:** Components use `build_component_ng` GN template. It handles platform iteration, dependency collection, and conditional source inclusion.

### Conditional Compilation

```cpp
// Feature flags (ace_config.gni)
#if defined(ACE_DEBUG)
    // Debug-only code (dcheck, thread-checker)
#endif
#if defined(IS_RELEASE_VERSION)
    // Release-only code
#endif
#if defined(USE_ROSEN_DRAWING)
    // Rosen drawing backend
#endif

// Platform flags (adapter/ohos/build/common.gni)
#if defined(OHOS_PLATFORM)
    // OHOS-specific implementation
#elif defined(PREVIEW_PLATFORM)
    // Desktop preview implementation
#endif

// Feature capability flags
#if defined(WEB_SUPPORTED)
    // Web component support
#endif
#if defined(IMAGE_SUPPORTED)
    // Image component support
#endif
```

---

## Testing Guidelines

### Unit Test Structure

```
test/unittest/core/pattern/menu/
├── menu_pattern_test_ng.cpp          # MenuPattern lifecycle tests
├── menu_layout_property_test_ng.cpp  # Layout property tests
├── menu_layoutFst_test_ng.cpp        # Layout algorithm tests
├── menu_paint_test_ng.cpp            # Paint property tests
├── menu_accessibility_property_test_ng.cpp
├── menu_model_static_test_ng.cpp     # Model API tests
├── menuitem_test_ng.cpp              # MenuItem tests
└── menuwrapper_test_ng.cpp           # MenuWrapper tests
```

### Test Fixture Pattern

```cpp
class MenuPatternTestNg : public testing::Test {
public:
    static void SetUpTestCase()
    {
        MockContainer::SetUp();
    }
    static void TearDownTestCase()
    {
        MockContainer::TearDown();
    }
    void SetUp() override
    {
        MockPipelineContext::SetUp();
        auto themeManager = AceType::MakeRefPtr<MockThemeManager>();
        MockPipelineContext::GetCurrent()->SetThemeManager(themeManager);
        EXPECT_CALL(*themeManager, GetTheme(_, _))
            .WillRepeatedly(Return(AceType::MakeRefPtr<SelectTheme>()));
    }
    void TearDown() override
    {
        MockPipelineContext::TearDown();
        menuFrameNode_ = nullptr;
    }

protected:
    RefPtr<FrameNode> menuFrameNode_;
};

void MenuPatternTestNg::InitMenuTestNg()
{
    menuFrameNode_ = FrameNode::GetOrCreateFrameNode(V2::MENU_TAG,
        ViewStackProcessor::GetInstance()->ClaimNodeId(),
        []() { return AceType::MakeRefPtr<MenuPattern>(TARGET_ID, "", TYPE); });
    ASSERT_NE(menuFrameNode_, nullptr);
}

HWTEST_F(MenuPatternTestNg, MenuPatternTestNg001, TestSize.Level1)
{
    /**
     * @tc.steps: step1. Create menu frame node and get pattern.
     * @tc.expected: Pattern is not null and returns correct menu type.
     */
    InitMenuTestNg();
    auto menuPattern = menuFrameNode_->GetPattern<MenuPattern>();
    ASSERT_NE(menuPattern, nullptr);
    EXPECT_EQ(menuPattern->GetMenuType(), TYPE);
}
```

**Key patterns:**
- `MockPipelineContext::SetUp()` / `MockContainer::SetUp()` for dependency injection
- `FrameNode::GetOrCreateFrameNode(tag, id, factory_lambda)` enables test injection
- Theme dependencies injected via `MockThemeManager` + `EXPECT_CALL`
- Test macro: `HWTEST_F` (OpenHarmony gtest wrapper)
- Components should not call platform singletons directly — prefer virtual methods or inject via Pipeline context

---

## Property Macro Expansion

The `ACE_DEFINE_PROPERTY_ITEM_WITHOUT_GROUP(name, type, changeFlag)` macro
(source: `frameworks/core/components_ng/property/property.h:254`) generates:

| Generated method | Signature | Purpose |
|-----------------|-----------|---------|
| `Get##name()` | `const std::optional<type>&` | Returns optional value |
| `Has##name()` | `bool` | Whether value is set |
| `Get##name##Value()` | `const type&` | Direct value access (UB if unset) |
| `Get##name##Value(default)` | `const type&` | Value with fallback |
| `Clone##name()` | `std::optional<type>` | Copy for comparison |
| `Reset##name()` | `void` | Clears the optional |
| `Update##name(value)` | `void` | Sets value + flags dirty (auto-dedup via `NearEqual`) |

Member field: `std::optional<type> prop##name##_`

The `Update##name` method compares old vs new value using `NearEqual()` and only sets
`UpdatePropertyChangeFlag(changeFlag)` when the value actually changes.

---

## Cross-Component Review

When changes span multiple components, verify:

1. **Shared property types** — If two components share a `LayoutProperty` type or enum, verify changes
   don't break the other component's assumptions
2. **Lifecycle ordering** — Parent pattern's `OnModifyDone` may call child pattern methods; verify
   the child is in a valid state when called
3. **Event propagation** — Events from one component (e.g., Menu dismissal) may trigger state changes
   in another (e.g., SelectOverlay). Trace the event flow across component boundaries
4. **Pattern interaction** — `GetPattern<T>()` across nodes should use the target component's type,
   not a base class; verify the node hierarchy matches assumptions

---

## Source Code References

Verify against actual source when snippets appear outdated.

1. **Base class signatures:**
   - `frameworks/core/components_ng/pattern/pattern.h` — Pattern base class, all lifecycle methods
   - `frameworks/core/components_ng/base/frame_node.h` — FrameNode, CreateFrameNode, GetPattern\<T\>
   - `frameworks/core/components_ng/event/event_hub.h` — EventHub base class
   - `frameworks/core/components_ng/layout/layout_property.h` — LayoutProperty base
   - `frameworks/core/components_ng/render/paint_property.h` — PaintProperty base
   - `interfaces/inner_api/ace_kit/include/ui/base/ace_type.h` — AceType, DynamicCast
   - `interfaces/inner_api/ace_kit/include/ui/base/referenced.h` — MakeRefPtr, WeakPtr, WeakClaim
   - `interfaces/inner_api/ace_kit/include/ui/properties/dirty_flag.h` — DirtySwapConfig, PropertyChangeFlag

2. **Component-specific patterns:**
   - `components_ng/pattern/<component>/` — each component's Pattern, Property, Model, etc.

3. **Test patterns:**
   - `test/unittest/core/pattern/<component>/` — real test fixtures and test cases

4. **Build configuration:**
   - `ace_config.gni` — root feature flags and defines
   - `adapter/ohos/build/common.gni` — OHOS platform-specific defines
   - `components_ng/components.gni` — `build_component_ng` GN template
