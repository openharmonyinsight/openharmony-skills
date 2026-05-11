# Case Study: Forward Declaration + Smart Pointer Optimization

> **Component**: drag_drop_related_configuration.h
> **Optimization Date**: 2026-02-09
> **Difficulty**: Medium
> **Impact**: High - Removed heavy gesture_info.h dependency

## Problem Statement

**File**: `frameworks/core/components_ng/manager/drag_drop/drag_drop_related_configuration.h`

The header file had a direct dependency on `gesture_info.h`, which contains multiple complex struct definitions:
- `DragPreviewOption` (~100 lines with many members)
- `OptionsAfterApplied` (~60 lines with BlurBackGroundInfo)
- Various enums and helper classes

This heavy dependency caused unnecessary recompilation when any gesture-related types changed.

### Before Optimization

```cpp
// drag_drop_related_configuration.h (BEFORE)
#include "base/memory/ace_type.h"
#include "core/components_ng/gestures/gesture_info.h"  // ❌ Heavy dependency
#include "core/components_ng/property/border_property.h"

class DragDropRelatedConfigurations : public AceType {
public:
    DragPreviewOption GetOrCreateDragPreviewOption() {  // ❌ Returns by value
        if (!previewOption_) {
            previewOption_ = DragPreviewOption();  // ❌ Value type member
        }
        return previewOption_;
    }

private:
    DragPreviewOption previewOption_;  // ❌ Value type - needs complete definition
    int32_t relatedGroupId_ = 0;
};
```

**Issues**:
1. Heavy include brings in entire gesture_info.h (~300+ lines)
2. Value type member requires complete definition
3. Return by value creates unnecessary copies
4. Any change in gesture_info.h triggers recompilation

## Solution: Forward Declaration + Smart Pointer

### Step 1: Replace Include with Forward Declarations

```cpp
// drag_drop_related_configuration.h (AFTER)
#include "base/memory/ace_type.h"
// ✅ Removed: #include "core/components_ng/gestures/gesture_info.h"
#include "core/components_ng/property/border_property.h"

// ✅ Forward declarations instead of full include
namespace OHOS::Ace::NG {
struct DragPreviewOption;      // Forward declaration
struct OptionsAfterApplied;    // Forward declaration
}

class DragDropRelatedConfigurations : public AceType {
public:
    // ✅ Declaration only, implementation in cpp
    ACE_FORCE_EXPORT const DragPreviewOption& GetOrCreateDragPreviewOption();

    ~DragDropRelatedConfigurations() override;  // ✅ Destructor in cpp

private:
    // ✅ Smart pointer member - forward declaration sufficient
    std::unique_ptr<DragPreviewOption> previewOption_;
    int32_t relatedGroupId_ = 0;
};
```

### Step 2: Implement in CPP File

```cpp
// drag_drop_related_configuration.cpp
#include "core/components_ng/manager/drag_drop/drag_drop_related_configuration.h"
#include "core/components_ng/gestures/gesture_info.h"  // ✅ Full include only in cpp

using namespace OHOS::Ace::NG;

DragDropRelatedConfigurations::~DragDropRelatedConfigurations() = default;

const DragPreviewOption& DragDropRelatedConfigurations::GetOrCreateDragPreviewOption()
{
    if (!previewOption_) {
        previewOption_ = std::make_unique<DragPreviewOption>();
    }
    if (!previewOption_) {
        static DragPreviewOption defaultInstance;  // ✅ Non-const static fallback
        return defaultInstance;
    }
    return *previewOption_;  // ✅ Return const reference - zero copy
}
```

## Key Optimizations Applied

### 1. Forward Declarations
**Before**: `#include "core/components_ng/gestures/gesture_info.h"`
**After**: Forward declarations for `DragPreviewOption` and `OptionsAfterApplied`

**Benefit**: Header no longer depends on complete type definitions.

### 2. Smart Pointer Member
**Before**: `DragPreviewOption previewOption_;` (value type)
**After**: `std::unique_ptr<DragPreviewOption> previewOption_;`

**Benefit**: Smart pointer templates work with forward declarations.

### 3. Const Reference Return
**Before**: Return by value (creates copy)
**After**: `const DragPreviewOption& GetOrCreateDragPreviewOption()`

**Benefit**: Zero-copy return value optimization.

### 4. Destructor in CPP
**Before**: Default destructor in header
**After**: Declaration in header, implementation in cpp

**Benefit**: Allows unique_ptr<DragPreviewOption> to work with forward declaration.

### 5. Static Fallback Instance
**Pattern**:
```cpp
static DragPreviewOption defaultInstance;  // ✅ Non-const
return defaultInstance;
```

**Why non-const**: Const static initialization may fail for complex types with constructors.

## Why This Works

### Smart Pointer Forward Declaration Compatibility

C++ smart pointers (`std::unique_ptr`, `std::shared_ptr`, `RefPtr`, `WeakPtr`) are templates that only need the type name at declaration time:

```cpp
// ✅ This works with forward declaration
std::unique_ptr<DragPreviewOption> previewOption_;

// ✅ This also works with forward declaration
RefPtr<DragPreviewOption> previewOptionRefPtr_;

// ❌ This would require full definition
DragPreviewOption previewOptionValue_;  // Value type needs complete definition
```

### Destructor Separation Pattern

When using forward declarations with smart pointer members:
1. Declare destructor in header: `~DragDropRelatedConfigurations() override;`
2. Implement in cpp: `DragDropRelatedConfigurations::~DragDropRelatedConfigurations() = default;`

**Why**: The destructor needs to know the complete type to call the unique_ptr destructor, which in turn deletes DragPreviewOption.

### Zero-Copy Return Pattern

Returning `const T&` instead of `T`:
- Avoids unnecessary object copying
- Safe because lifetime is managed by member variable
- More efficient for large structs

## Results

### Dependency Reduction
- ✅ Removed 1 heavy include (`gesture_info.h` - ~300 lines)
- ✅ Added 2 forward declarations
- ✅ No changes to public API

### Compilation Impact
- ✅ Any change to gesture_info.h no longer triggers recompilation of this header
- ✅ Reduced memory footprint during compilation
- ✅ Verified standalone compilation successful

### Code Quality
- ✅ Zero-copy return value optimization
- ✅ Smart pointer encapsulation
- ✅ Maintained const correctness
- ✅ No performance degradation

## Common Pattern Summary

This case demonstrates a **common optimization pattern**:

### When to Apply

Use this pattern when:
1. Header has value type members from heavy dependencies
2. Members are only used in implementation (.cpp), not in public API
3. Heavy include is only needed for member variable types
4. Return values can be changed to const references

### Decision Flowchart

```
Is there a value type member from heavy include?
│
├─ YES → Can member be smart pointer?
│         │
│         ├─ YES → Convert to std::unique_ptr<T>
│         │         │
│         │         ├─ Move destructor to cpp
│         │         ├─ Return const& instead of by value
│         │         └─ Replace include with forward declaration
│         │
│         └─ NO → Consider PIMPL pattern
│
└─ NO → Check other optimization strategies
```

### Implementation Checklist

- [ ] Identify heavy includes (files > 100 lines or many dependencies)
- [ ] Find value type members from those includes
- [ ] Convert members to smart pointers
- [ ] Add forward declarations
- [ ] Move destructor to cpp
- [ ] Change return values to const references (if applicable)
- [ ] Update cpp to include full header
- [ ] Verify standalone compilation
- [ ] Check for const correctness issues

### Related Patterns

- **Include Replacement** (case-drag-event-include-reduction.md): Replace heavy include with light include
- **PIMPL Pattern** (pimp-guide.md): Hide all implementation details
- **RefPtr Forward Declaration** (case-click_event-forward-declaration.md): Using RefPtr<T> instead of std::unique_ptr

## Files Modified

1. `drag_drop_related_configuration.h`:
   - Removed `#include "core/components_ng/gestures/gesture_info.h"`
   - Added forward declarations
   - Changed member to `std::unique_ptr<DragPreviewOption>`
   - Moved destructor declaration to header

2. `drag_drop_related_configuration.cpp`:
   - Added `#include "core/components_ng/gestures/gesture_info.h"`
   - Implemented destructor
   - Implemented `GetOrCreateDragPreviewOption()`

## References

- **SKILL.md**: Step 4.1 - Smart Pointer Template Parameters (RefPtr/WeakPtr)
- **forward-declaration.md**: Forward declaration best practices
- **pimp-guide.md**: When forward declaration is not enough
