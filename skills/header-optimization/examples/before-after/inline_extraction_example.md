# Inline Method Extraction - Before/After Example

Example of moving inline implementations from header to cpp for header optimization in ace_engine.

## Scenario
Button pattern class with multiple inline methods that should be moved to cpp.

## Before (Heavy Header)

```cpp
// frameworks/core/components_ng/pattern/button/button_pattern.h
#pragma once
#include "core/components_ng/base/frame_node.h"
#include "core/components_ng/pattern/pattern.h"
#include "core/components_ng/property/button_layout_property.h"
#include "core/components_ng/property/button_paint_property.h"
#include "core/event/mouse_event.h"
#include "base/log/log.h"

namespace OHOS::Ace::NG {

class ButtonPattern : public Pattern {
public:
    ButtonPattern() = default;
    ~ButtonPattern() override = default;

    // Inline implementations - HEAVY!
    void OnModifyDone() override
    {
        auto frameNode = AceType::DynamicCast<FrameNode>(GetHost());
        if (!frameNode) {
            LOGW("FrameNode is null");
            return;
        }

        auto layoutProperty = frameNode->GetLayoutProperty<ButtonLayoutProperty>();
        if (layoutProperty) {
            layoutProperty->UpdateButtonStyle();
        }

        auto paintProperty = frameNode->GetPaintProperty<ButtonPaintProperty>();
        if (paintProperty) {
            paintProperty->UpdateBorderColor();
        }
    }

    void OnDirtyLayoutWrapperSwap() override
    {
        auto frameNode = AceType::DynamicCast<FrameNode>(GetHost());
        if (!frameNode) {
            return;
        }

        auto layoutProperty = frameNode->GetLayoutProperty<ButtonLayoutProperty>();
        if (layoutProperty) {
            layoutProperty->UpdateLayoutSize();
        }
    }

    bool IsTouchable() const
    {
        auto frameNode = AceType::DynamicCast<FrameNode>(GetHost());
        if (!frameNode) {
            return false;
        }

        return frameNode->GetTouchable();
    }

    static void UpdateButtonState(FrameNode* node, bool pressed)
    {
        if (!node) {
            LOGW("FrameNode is null in UpdateButtonState");
            return;
        }

        auto paintProperty = node->GetPaintProperty<ButtonPaintProperty>();
        if (paintProperty) {
            paintProperty->UpdateState(pressed);
        }
    }

private:
    bool isPressed_ = false;
    int32_t clickCount_ = 0;
};

}  // namespace OHOS::Ace::NG
```

**Issues:**
- All method implementations in header (4 methods with 3+ lines)
- Heavy includes required in header
- Any implementation change triggers recompilation of all includers
- 5 includes in header

## After (Optimized)

### header.h (Lightweight)

```cpp
// frameworks/core/components_ng/pattern/button/button_pattern.h
#pragma once
#include "core/components_ng/pattern/pattern.h"

namespace OHOS::Ace::NG {
// Forward declarations - reduces dependencies
class FrameNode;
class ButtonLayoutProperty;
class ButtonPaintProperty;

class ButtonPattern : public Pattern {
public:
    ButtonPattern();
    ~ButtonPattern() override;

    void OnModifyDone() override;
    void OnDirtyLayoutWrapperSwap() override;
    bool IsTouchable() const;

    static void UpdateButtonState(FrameNode* node, bool pressed);

private:
    bool isPressed_ = false;
    int32_t clickCount_ = 0;
};

}  // namespace OHOS::Ace::NG
```

**Improvements:**
- All method implementations moved to cpp
- 4 includes reduced to 1 (only base Pattern class)
- 3 forward declarations instead of full includes
- Implementation changes don't trigger recompilation

### button_pattern.cpp (Implementation)

```cpp
// frameworks/core/components_ng/pattern/button/button_pattern.cpp
#include "core/components_ng/pattern/button/button_pattern.h"

#include "core/components_ng/base/frame_node.h"
#include "core/components_ng/property/button_layout_property.h"
#include "core/components_ng/property/button_paint_property.h"
#include "base/log/log.h"
#include "base/memory/ace_type.h"

namespace OHOS::Ace::NG {

ButtonPattern::ButtonPattern() = default;
ButtonPattern::~ButtonPattern() = default;

void ButtonPattern::OnModifyDone()
{
    auto frameNode = AceType::DynamicCast<FrameNode>(GetHost());
    if (!frameNode) {
        LOGW("FrameNode is null");
        return;
    }

    auto layoutProperty = frameNode->GetLayoutProperty<ButtonLayoutProperty>();
    if (layoutProperty) {
        layoutProperty->UpdateButtonStyle();
    }

    auto paintProperty = frameNode->GetPaintProperty<ButtonPaintProperty>();
    if (paintProperty) {
        paintProperty->UpdateBorderColor();
    }
}

void ButtonPattern::OnDirtyLayoutWrapperSwap()
{
    auto frameNode = AceType::DynamicCast<FrameNode>(GetHost());
    if (!frameNode) {
        return;
    }

    auto layoutProperty = frameNode->GetLayoutProperty<ButtonLayoutProperty>();
    if (layoutProperty) {
        layoutProperty->UpdateLayoutSize();
    }
}

bool ButtonPattern::IsTouchable() const
{
    auto frameNode = AceType::DynamicCast<FrameNode>(GetHost());
    if (!frameNode) {
        return false;
    }

    return frameNode->GetTouchable();
}

void ButtonPattern::UpdateButtonState(FrameNode* node, bool pressed)
{
    if (!node) {
        LOGW("FrameNode is null in UpdateButtonState");
        return;
    }

    auto paintProperty = node->GetPaintProperty<ButtonPaintProperty>();
    if (paintProperty) {
        paintProperty->UpdateState(pressed);
    }
}

}  // namespace OHOS::Ace::NG
```

## Results

### Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Header includes | 5 | 1 | **80% reduction** |
| Header lines | 82 | 35 | **57% reduction** |
| Inline methods | 4 | 0 | **100% eliminated** |
| Forward declarations | 0 | 3 | **Dependency hiding** |

### Benefits

1. **Compilation Time**: Files including button_pattern.h no longer need to parse FrameNode, Property definitions
2. **Recompilation Cascade**: Changes to implementation don't trigger recompilation of all includers
3. **Header Clarity**: Interface is clear and concise
4. **Dependency Isolation**: Heavy dependencies isolated to cpp file

### Verification

```bash
# Test standalone compilation using compile-analysis skill
# 1. Extract compilation command for button_pattern.cpp
# 2. Verify compilation succeeds
# 3. Verify no warnings or errors
# 4. Test with test_header.cpp if provided
```

## Key Points

1. **3+ line rule**: All methods with 3+ lines moved to cpp
2. **Forward declarations**: Replace includes where possible
3. **Preserve functionality**: Implementation identical, just moved
4. **Minimal changes**: Only structural optimization, no logic changes
