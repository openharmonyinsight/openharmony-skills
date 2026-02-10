# PIMPL Pattern Guide for ACE Engine

Complete guide for applying PIMPL (Pointer to Implementation) pattern in ace_engine header optimization.

## What is PIMPL?

PIMPL (also called "opaque pointer" or "compiler firewall") hides implementation details by moving private members to a separate Impl class accessed through a pointer.

### Benefits
- **Reduces compilation dependencies** - Implementation details don't need to be compiled when using header
- **Improves compile time** - Changes to Impl don't trigger recompilation of all includers
- **Binary compatibility** - Can change implementation without breaking ABI

### Costs
- **Runtime overhead** - Additional heap allocation and pointer indirection
- **Memory overhead** - Extra pointer member (typically 8 bytes)
- **Complexity** - More boilerplate and indirection in code

### When to Use in ace_engine

**Good candidates:**
- Pattern classes with heavy private dependencies
- Headers frequently included by many files
- Classes with unstable implementation details
- When compilation time improvement justifies runtime cost

**Poor candidates:**
- Small, lightweight classes
- Performance-critical data structures
- Classes with simple private members
- Value semantics (copyable/movable)

## PIMPL Implementation Pattern

### Basic Structure

```cpp
// header.h
#pragma once
#include <memory>

namespace OHOS::Ace::NG {

class FrameNode;  // Forward declaration

class ButtonPattern {
public:
    ButtonPattern();
    ~ButtonPattern();

    // Public interface
    void OnModifyDone();
    void OnDirtyLayoutWrapperSwap();

    // Disable copy (for typical PIMPL)
    ButtonPattern(const ButtonPattern&) = delete;
    ButtonPattern& operator=(const ButtonPattern&) = delete;

    // Enable move (optional)
    ButtonPattern(ButtonPattern&&);
    ButtonPattern& operator=(ButtonPattern&&);

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

}  // namespace OHOS::Ace::NG
```

```cpp
// button_pattern.cpp
#include "button_pattern.h"
#include "core/components_ng/base/frame_node.h"
#include "core/components_ng/property/layout_property.h"
#include "core/pipeline/base/element.h"
// ... other heavy includes

namespace OHOS::Ace::NG {

// Implementation class definition
class ButtonPattern::Impl {
public:
    void OnModifyDone(ButtonPattern* pattern)
    {
        // Access heavy dependencies here
        auto frameNode = AceType::DynamicCast<FrameNode>(pattern->GetHost());
        if (!frameNode) {
            return;
        }

        auto layoutProperty = frameNode->GetLayoutProperty<ButtonLayoutProperty>();
        if (layoutProperty) {
            layoutProperty->UpdateButtonStyle();
        }
    }

    void OnDirtyLayoutWrapperSwap()
    {
        // Implementation details with heavy dependencies
        needsLayout_ = true;
    }

    // Private members with heavy types
    RefPtr<LayoutProperty> layoutProperty_;
    RefPtr<EventHub> eventHub_;
    bool needsLayout_ = false;
};

// Constructor
ButtonPattern::ButtonPattern()
    : impl_(std::make_unique<Impl>())
{
}

// Destructor (defined here for unique_ptr completeness)
ButtonPattern::~ButtonPattern() = default;

// Move operations (optional)
ButtonPattern::ButtonPattern(ButtonPattern&&) noexcept = default;
ButtonPattern& ButtonPattern::operator=(ButtonPattern&&) noexcept = default;

// Public interface delegating to impl
void ButtonPattern::OnModifyDone()
{
    impl_->OnModifyDone(this);
}

void ButtonPattern::OnDirtyLayoutWrapperSwap()
{
    impl_->OnDirtyLayoutWrapperSwap();
}

}  // namespace OHOS::Ace::NG
```

## Common PIMPL Scenarios in ace_engine

### Scenario 1: Heavy Property Dependencies

**Before (Heavy Header):**
```cpp
// button_pattern.h
#pragma once
#include "base/memory/ace_type.h"
#include "core/components_ng/base/frame_node.h"
#include "core/components_ng/property/button_layout_property.h"
#include "core/components_ng/property/button_paint_property.h"
#include "core/components_ng/event/event_hub.h"

namespace OHOS::Ace::NG {

class ButtonPattern : public Pattern {
public:
    void OnModifyDone();

private:
    RefPtr<ButtonLayoutProperty> layoutProperty_;
    RefPtr<ButtonPaintProperty> paintProperty_;
    RefPtr<EventHub> eventHub_;
};

}
```

**After (Light Header):**
```cpp
// button_pattern.h
#pragma once
#include <memory>
#include "core/components_ng/pattern/pattern.h"

namespace OHOS::Ace::NG {

class ButtonPattern : public Pattern {
public:
    ButtonPattern();
    ~ButtonPattern();

    void OnModifyDone();

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

}
```

### Scenario 2: Callback/Listener Storage

**Before:**
```cpp
// pattern.h
#pragma once
#include <functional>
#include <vector>
#include "base/callback/callback.h"

class Pattern {
protected:
    std::vector<Callback>> callbacks_;
    std::function<void()> onUpdateCallback_;
};
```

**After:**
```cpp
// pattern.h
#pragma once
#include <memory>

class Pattern {
public:
    Pattern();
    ~Pattern();

protected:
    class Impl;
    std::unique_ptr<Impl> impl_;
};
```

### Scenario 3: State Management

**Before:**
```cpp
// pattern.h
#pragma once
#include "core/components/common/properties/text_style.h"
#include "core/components/common/properties/decoration.h"
#include "core/components_ng/layout/layout_property.h"

class Pattern {
protected:
    TextStyle textStyle_;
    Decoration decoration_;
    LayoutConstraint layoutConstraint_;
};
```

**After:**
```cpp
// pattern.h
#pragma once
#include <memory>

class Pattern {
public:
    Pattern();
    ~Pattern();

protected:
    class Impl;
    std::unique_ptr<Impl> impl_;
};
```

## Implementation Details

### Constructor Pattern

```cpp
// Delegating constructor
ButtonPattern::ButtonPattern()
    : impl_(std::make_unique<Impl>())
{
}

// With parameters
ButtonPattern::ButtonPattern(int param)
    : impl_(std::make_unique<Impl>(param))
{
}

// Impl constructor
ButtonPattern::Impl::Impl(int param)
    : value_(param)
{
}
```

### Destructor Requirement

**CRITICAL**: Always define destructor (even if default) in cpp file:

```cpp
// header.h
class ButtonPattern {
public:
    ~ButtonPattern();  // NOT inline
private:
    std::unique_ptr<Impl> impl_;
};

// cpp.cpp
ButtonPattern::~ButtonPattern() = default;  // Required for unique_ptr<Impl>
```

**Why**: unique_ptr requires complete type of Impl at destruction point. Inline destructor in header would require Impl definition in header, defeating PIMPL purpose.

### Move Semantics

```cpp
// header.h
class ButtonPattern {
public:
    ButtonPattern(ButtonPattern&&) noexcept;
    ButtonPattern& operator=(ButtonPattern&&) noexcept;
};

// cpp.cpp
ButtonPattern::ButtonPattern(ButtonPattern&&) noexcept = default;
ButtonPattern& ButtonPattern::operator=(ButtonPattern&&) noexcept = default;
```

### Accessing Host from Impl

Pattern: Pass `this` to Impl methods when needed:

```cpp
// cpp.cpp
void ButtonPattern::OnModifyDone()
{
    impl_->OnModifyDone(this);  // Pass pattern pointer
}

void ButtonPattern::Impl::OnModifyDone(ButtonPattern* pattern)
{
    auto frameNode = pattern->GetHost();  // Access host through pattern
    // ... use frameNode
}
```

### Managing Dependencies in Impl

```cpp
// button_pattern.cpp
class ButtonPattern::Impl {
public:
    // Forward declare when possible
    void ProcessLayout(FrameNode* node);

    // Include heavy dependencies only in cpp
    #include "core/components_ng/property/layout_property.h"

    RefPtr<ButtonLayoutProperty> layoutProperty_;
    RefPtr<ButtonPaintProperty> paintProperty_;
};
```

## Testing PIMPL Implementation

### Verification Checklist

- [ ] Header compiles without Impl definition
- [ ] No heavy includes in header
- [ ] Only forward declarations in header
- [ ] Destructor defined in cpp (not inline)
- [ ] Move operations properly declared if needed
- [ ] Standalone compilation succeeds
- [ ] Functionality verified (unit tests pass)

### Compile Verification

```bash
# Extract and test compilation command using compile-analysis skill
# 1. Analyze header dependencies
# 2. Verify reduced include count
# 3. Test standalone compilation of cpp
# 4. Verify no regression
```

## PIMPL Decision Tree

```
Is the header frequently included by many files?
├─ Yes → Continue
└─ No → Consider simpler optimization

Does the class have heavy private dependencies?
├─ Yes → Continue
└─ No → Consider simpler optimization

Is performance critical (hot path)?
├─ Yes → Avoid PIMPL, consider other optimizations
└─ No → Apply PIMPL

Is ABI stability important?
├─ Yes → PIMPL is good choice
└─ No → PIMPL still helps compile time

Decision: Apply PIMPL pattern
```

## Common Mistakes

### Mistake 1: Inline Destructor

```cpp
// ❌ WRONG
class ButtonPattern {
public:
    ~ButtonPattern() = default;  // Inline requires Impl in header!
private:
    std::unique_ptr<Impl> impl_;
};

// ✅ CORRECT
// header.h
class ButtonPattern {
public:
    ~ButtonPattern();  // Declaration only
private:
    std::unique_ptr<Impl> impl_;
};

// cpp.cpp
ButtonPattern::~ButtonPattern() = default;
```

### Mistake 2: Forgetting to Disable Copy

```cpp
// ❌ WRONG - Copy will crash with unique_ptr
class ButtonPattern {
private:
    std::unique_ptr<Impl> impl_;
};

// ✅ CORRECT - Explicitly delete
class ButtonPattern {
public:
    ButtonPattern(const ButtonPattern&) = delete;
    ButtonPattern& operator=(const ButtonPattern&) = delete;
private:
    std::unique_ptr<Impl> impl_;
};
```

### Mistake 3: Heavy Includes in Header

```cpp
// ❌ WRONG - Defeats PIMPL purpose
#pragma once
#include "heavy_dependency.h"  // Still heavy!
#include <memory>

class ButtonPattern {
private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

// ✅ CORRECT - Only forward declarations
#pragma once
#include <memory>

namespace OHOS::Ace::NG {
class HeavyClass;  // Forward declaration
}

class ButtonPattern {
private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};
```

### Mistake 4: PIMPL for Small Classes

```cpp
// ❌ WRONG - Overhead not justified
class Point {
public:
    Point();
    ~Point();
    int GetX() const { return impl_->x_; }
private:
    class Impl;
    std::unique_ptr<Impl> impl_;  // 8 bytes overhead for 2 int values!
};

// ✅ CORRECT - Keep simple
class Point {
public:
    int GetX() const { return x_; }
private:
    int x_;
    int y_;
};
```

## Migration Strategy

### Step-by-Step Migration

1. **Create Impl class skeleton**
   ```cpp
   class MyClass::Impl {
   public:
       // Move private members here
   };
   ```

2. **Add unique_ptr<Impl> to header**
   ```cpp
   class MyClass {
   private:
       class Impl;
       std::unique_ptr<Impl> impl_;
   };
   ```

3. **Update constructor/destructor**
   ```cpp
   MyClass::MyClass() : impl_(std::make_unique<Impl>()) {}
   MyClass::~MyClass() = default;
   ```

4. **Migrate private methods**
   ```cpp
   void MyClass::PrivateMethod() {
       impl_->PrivateMethod();
   }
   ```

5. **Remove heavy includes from header**
   ```cpp
   // Move to cpp.cpp
   ```

6. **Test standalone compilation**
   ```cpp
   // Verify header compiles alone
   // Verify cpp compiles with dependencies
   ```

7. **Verify functionality**
   ```cpp
   // Run unit tests
   ```

## Performance Considerations

### When to Avoid PIMPL

- **Performance-critical code**: Hot paths, inner loops
- **Small objects**: Overhead ratio too high
- **Value semantics**: Need copy/move by value
- **Template classes**: PIMPL complicates templates

### Measuring Impact

Before applying PIMPL, measure:
1. Current header include count
2. Compilation time impact
3. Class instance count
4. Performance requirements

After applying PIMPL, verify:
1. Header include reduction
2. Compilation time improvement
3. Runtime performance impact (should be minimal)
4. Memory overhead (8 bytes per instance)

## Complete Example: ButtonPattern

See `examples/pimpl-example/` for complete working example of PIMPL in ace_engine context.

## References

- Effective C++ (Scott Meyers) - Item 31: Minimize compilation dependencies
- Exceptional C++ (Herb Sutter) - PIMPL idiom
- ace_engine patterns: `frameworks/core/components_ng/pattern/`
