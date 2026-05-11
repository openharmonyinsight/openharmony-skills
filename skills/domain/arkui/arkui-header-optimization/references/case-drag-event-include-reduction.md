# Case Study: Include Replacement Strategy

> **Component**: drag_event.h (DragEventActuator class)
> **Optimization Date**: 2026-02-09
> **Difficulty**: Easy-Medium
> **Impact**: High - Replaced heavy include with light include + forward declarations

## Problem Statement

**File**: `frameworks/core/components_ng/event/drag_event.h`

The header file had a direct dependency on `core/gestures/drag_event.h` (OHOS::Ace namespace), which contains:
- `DragEvent` class with full implementation
- `PreDragStatus` enum
- Various drag-related classes and utilities

This heavy dependency from the NG (OHOS::Ace::NG) namespace to the core (OHOS::Ace) namespace caused unnecessary recompilation.

### Before Optimization

```cpp
// drag_event.h (BEFORE)
#include <memory>
#include <mutex>
#include "base/memory/ace_type.h"
#include "base/memory/referenced.h"
#include "base/utils/noncopyable.h"
#include "core/gestures/drag_event.h"  // ❌ Heavy cross-namespace include
#include "core/components_ng/base/frame_node.h"

class DragEventActuator : public GestureEventActuator {
public:
    void SetDragExtraInfo(const std::string& extraInfo);

    const OptionsAfterApplied& GetOptionsAfterApplied() {
        if (!optionsAfterApplied_) {
            static OptionsAfterApplied defaultInstance;
            return defaultInstance;
        }
        return optionsAfterApplied_;  // ❌ Returns by value
    }

private:
    OptionsAfterApplied optionsAfterApplied_;  // ❌ Value type member
    int32_t relatedGroupId_ = 0;
};
```

**Issues**:
1. Heavy cross-namespace include brings in entire drag_event.h (~200+ lines)
2. Value type member requires complete OptionsAfterApplied definition
3. Unnecessary coupling between NG and core gesture systems
4. Any change in core drag_event.h triggers NG header recompilation

## Solution: Light Include + Forward Declarations

### Step 1: Analyze What's Actually Needed

From the heavy `core/gestures/drag_event.h`, only **one type** was actually used:
- `PreDragStatus` enum

All other types (`DragEvent`, `OptionsAfterApplied`) could use forward declarations.

### Step 2: Identify Light Include

Created `core/gestures/drag_constants.h` to contain only the enum:
```cpp
// drag_constants.h (NEW FILE)
#ifndef FOUNDATION_ACE_CORE_GESTURES_DRAG_CONSTANTS_H
#define FOUNDATION_ACE_CORE_GESTURES_DRAG_CONSTANTS_H

namespace OHOS::Ace {

enum class PreDragStatus : int32_t {
    READY = 0,
    PROCESSING = 1,
    FAILED = 2,
};

}  // namespace OHOS::Ace

#endif  // FOUNDATION_ACE_CORE_GESTURES_DRAG_CONSTANTS_H
```

### Step 3: Replace Heavy Include with Light Include

```cpp
// drag_event.h (AFTER)
#include <memory>
#include <mutex>
#include "base/memory/ace_type.h"
#include "base/memory/referenced.h"
#include "base/utils/noncopyable.h"
// ✅ Replaced: core/gestures/drag_event.h
#include "core/gestures/drag_constants.h"  // ✅ Light include - only enum
#include "core/components_ng/base/frame_node.h"

// ✅ Forward declarations for other types
namespace OHOS::Ace {
class DragEvent;  // Forward declaration
}

namespace OHOS::Ace::NG {
struct OptionsAfterApplied;  // Forward declaration
}

class DragEventActuator : public GestureEventActuator {
public:
    void SetDragExtraInfo(const std::string& extraInfo);

    // ✅ Declaration only, implementation in cpp
    const OptionsAfterApplied& GetOptionsAfterApplied();

private:
    // ✅ Smart pointer instead of value type
    std::unique_ptr<OptionsAfterApplied> optionsAfterApplied_;
    int32_t relatedGroupId_ = 0;
};
```

### Step 4: Implement in CPP File

```cpp
// drag_event.cpp
#include "core/components_ng/event/drag_event.h"
#include "core/components_ng/gestures/gesture_info.h"  // ✅ Full include for OptionsAfterApplied
#include "core/gestures/drag_event.h"  // ✅ Full include for DragEvent

const OptionsAfterApplied& DragEventActuator::GetOptionsAfterApplied()
{
    if (!optionsAfterApplied_) {
        static OptionsAfterApplied defaultInstance;
        return defaultInstance;
    }
    return *optionsAfterApplied_;  // ✅ Dereference smart pointer
}

// Updated usages throughout drag_event.cpp
optionsAfterApplied_ = std::make_unique<OptionsAfterApplied>(
    frameNode->GetDragPreviewOption().options
);
frameNode->SetOptionsAfterApplied(
    optionsAfterApplied_ ? *optionsAfterApplied_ : OptionsAfterApplied()
);
```

## Key Optimizations Applied

### 1. Light Include Replacement
**Before**: `#include "core/gestures/drag_event.h"` (~200 lines)
**After**: `#include "core/gestures/drag_constants.h"` (~15 lines)

**Benefit**: Only includes what's actually needed (PreDragStatus enum).

### 2. Forward Declarations for Complex Types
**Added**:
```cpp
namespace OHOS::Ace {
class DragEvent;  // Forward declaration - only used in cpp
}

namespace OHOS::Ace::NG {
struct OptionsAfterApplied;  // Forward declaration - smart pointer member
}
```

**Benefit**: No need for complete DragEvent or OptionsAfterApplied definitions in header.

### 3. Smart Pointer Conversion
**Before**: `OptionsAfterApplied optionsAfterApplied_;` (value type)
**After**: `std::unique_ptr<OptionsAfterApplied> optionsAfterApplied_;`

**Benefit**: Forward declaration sufficient for unique_ptr<T> member.

### 4. Implementation Separation
**Before**: Inline method implementation in header
**After**: Declaration in header, implementation in cpp

```cpp
// Header - declaration only
const OptionsAfterApplied& GetOptionsAfterApplied();

// CPP - full implementation with complete type access
const OptionsAfterApplied& DragEventActuator::GetOptionsAfterApplied() { /* ... */ }
```

**Benefit**: Only cpp file needs full type definitions.

## Why This Works

### Split Strategy: Constants vs Implementations

The key insight is that many headers contain:
1. **Lightweight definitions** (enums, constants, simple types) - Safe to include
2. **Heavy implementations** (classes with methods, complex logic) - Avoid including

**Strategy**: Split into separate headers:
- `*_constants.h` - Enums, constants, simple types
- `*_event.h` - Full class implementations

```cpp
// ✅ Include only what you need
#include "core/gestures/drag_constants.h"  // Just enums

// ❌ Avoid when possible
#include "core/gestures/drag_event.h"  // Entire implementations
```

### Cross-Namespace Dependencies

When NG components depend on core components:
1. **Check what's actually needed** from the core header
2. **Create light include** if only enums/constants are required
3. **Use forward declarations** for complex types
4. **Move implementations** to cpp where full definitions are available

### Smart Pointer Dereference Pattern

When accessing unique_ptr members:
```cpp
// ✅ Check if pointer exists
if (!optionsAfterApplied_) {
    static OptionsAfterApplied defaultInstance;
    return defaultInstance;
}

// ✅ Dereference to return reference
return *optionsAfterApplied_;

// ✅ Conditional dereference for value parameters
frameNode->SetOptionsAfterApplied(
    optionsAfterApplied_ ? *optionsAfterApplied_ : OptionsAfterApplied()
);
```

## Results

### Dependency Reduction
- ✅ Replaced 1 heavy include (drag_event.h ~200 lines)
- ✅ Added 1 light include (drag_constants.h ~15 lines)
- ✅ Added 2 forward declarations
- ✅ 92.5% reduction in included code from that dependency

### Compilation Impact
- ✅ Changes to DragEvent class no longer trigger recompilation
- ✅ Reduced coupling between NG and core gesture systems
- ✅ Verified standalone compilation successful

### Code Organization
- ✅ Cleaner separation of concerns (constants vs implementations)
- ✅ Better namespace boundaries (OHOS::Ace vs OHOS::Ace::NG)
- ✅ More maintainable code structure

## Common Pattern Summary

This case demonstrates an **include replacement strategy**:

### When to Apply

Use this strategy when:
1. Header includes another heavy header from different namespace/module
2. Only a small subset (enums, constants) is actually needed
3. Most types can be forward declared
4. Members can be converted to smart pointers

### Decision Flowchart

```
Is there a heavy cross-namespace include?
│
├─ YES → What's actually needed from it?
│         │
│         ├─ Only enums/constants?
│         │   └─ Create light include (*_constants.h)
│         │     Replace heavy include with light include
│         │     Forward declare complex types
│         │
│         ├─ Class definitions for members?
│         │   └─ Can members be smart pointers?
│         │     ├─ YES → Forward declare + unique_ptr<T>
│         │     └─ NO → Check PIMPL pattern
│         │
│         └─ Used in inline implementations?
│             └─ Move implementations to cpp
│
└─ NO → Check other optimization strategies
```

### Implementation Checklist

- [ ] Identify heavy includes (different namespace/module)
- [ ] Search for actual usage of types from that include
- [ ] Create light include header if only enums/constants needed
- [ ] Add forward declarations for complex types
- [ ] Convert value type members to smart pointers (if applicable)
- [ ] Move inline implementations to cpp
- [ ] Update cpp to include both light and heavy headers
- [ ] Verify standalone compilation
- [ ] Check that all usages are updated (dereference smart pointers)

### Light Include Template

```cpp
// *_constants.h - Lightweight header
#ifndef FOUNDATION_ACE_XXX_XXX_CONSTANTS_H
#define FOUNDATION_ACE_XXX_XXX_CONSTANTS_H

namespace OHOS::Ace {

// Only enums and constants
enum class SomeStatus : int32_t {
    READY = 0,
    PROCESSING = 1,
};

constexpr int MAX_VALUE = 100;

}  // namespace OHOS::Ace

#endif  // FOUNDATION_ACE_XXX_XXX_CONSTANTS_H
```

### Related Patterns

- **Forward Declaration + Smart Pointer** (case-drag-drop-forward-declaration.md): Converting value members to unique_ptr
- **Enum Splitting** (case-split-enums.md): Extracting enums to separate headers
- **RefPtr Forward Declaration** (case-click_event-forward-declaration.md): Using RefPtr<T> for forward declarations

## Files Modified

1. **drag_event.h**:
   - Replaced `#include "core/gestures/drag_event.h"`
   - Added `#include "core/gestures/drag_constants.h"`
   - Added forward declarations for `DragEvent` and `OptionsAfterApplied`
   - Changed member to `std::unique_ptr<OptionsAfterApplied>`
   - Moved `GetOptionsAfterApplied()` implementation to declaration

2. **drag_event.cpp**:
   - Added `#include "core/gestures/drag_event.h"`
   - Added `#include "core/components_ng/gestures/gesture_info.h"`
   - Implemented `GetOptionsAfterApplied()`
   - Updated all usages to dereference smart pointer

3. **drag_constants.h** (NEW):
   - Created lightweight header with PreDragStatus enum
   - Located at `frameworks/core/gestures/drag_constants.h`

## Comparison with Forward Declaration Pattern

| Aspect | Forward Declaration + Smart Pointer | Include Replacement |
|--------|-------------------------------------|---------------------|
| **Use case** | Value type members within same namespace | Heavy cross-namespace includes |
| **Primary technique** | unique_ptr<T> + forward declaration | Light include + forward declaration |
| **Creates new files?** | No | Yes (light headers) |
| **Destructor separation** | Required | Required |
| **Return type change** | Value → const& | May or may not need |
| **Dependency reduction** | ~300 lines → 0 lines | ~200 lines → ~15 lines |

## References

- **SKILL.md**: Step 5 - Split Headers for Constants and Enums
- **case-split-enums.md**: Extracting enums from drag_event.h (original split case)
- **forward-declaration.md**: Forward declaration best practices
