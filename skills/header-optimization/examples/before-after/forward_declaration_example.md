# Forward Declaration Conversion - Before/After Example

Example of converting header includes to forward declarations for header optimization in ace_engine.

## Scenario
Pattern class that includes several heavy dependencies that can be replaced with forward declarations.

## Before (Heavy Header)

```cpp
// frameworks/core/components_ng/pattern/grid/grid_pattern.h
#pragma once

#include "core/components_ng/base/frame_node.h"           // Can be forward declared
#include "core/components_ng/base/ui_node.h"              // Can be forward declared
#include "core/components_ng/pattern/pattern.h"           // Need full include (base class)
#include "core/components_ng/property/grid_layout_property.h"  // Can be forward declared
#include "core/components_ng/property/scroll_bar_property.h"   // Can be forward declared
#include "core/pipeline/base/element.h"                   // Can be forward declared
#include "core/components/common/layout.h"                // Can be forward declared

namespace OHOS::Ace::NG {

class GridPattern : public Pattern {
public:
    GridPattern() = default;
    ~GridPattern() override = default;

    void OnModifyDone() override;

    FrameNode* GetFrameNode() const;
    void SetFrameNode(FrameNode* node);

    void ProcessElement(Element* element);

private:
    FrameNode* frameNode_ = nullptr;
    UINode* uiNode_ = nullptr;
    Element* element_ = nullptr;
    GridLayoutProperty* layoutProperty_ = nullptr;
};

}  // namespace OHOS::Ace::NG
```

**Issues:**
- 7 includes in header
- Only 1 actually needed (base class Pattern)
- Other 6 can be forward declarations
- Causes cascading compilation

## After (Optimized)

```cpp
// frameworks/core/components_ng/pattern/grid/grid_pattern.h
#pragma once

#include "core/components_ng/pattern/pattern.h"  // Only essential include (base class)

// Forward declarations - eliminates 6 heavy includes!
namespace OHOS::Ace::NG {
class FrameNode;
class UINode;
class GridLayoutProperty;
}  // namespace OHOS::Ace::NG

namespace OHOS::Ace {
class Element;
}  // namespace OHOS::Ace

namespace OHOS::Ace::NG {

class GridPattern : public Pattern {
public:
    GridPattern() = default;
    ~GridPattern() override = default;

    void OnModifyDone() override;

    FrameNode* GetFrameNode() const;
    void SetFrameNode(FrameNode* node);

    void ProcessElement(Element* element);

private:
    FrameNode* frameNode_ = nullptr;
    UINode* uiNode_ = nullptr;
    Element* element_ = nullptr;
    GridLayoutProperty* layoutProperty_ = nullptr;
};

}  // namespace OHOS::Ace::NG
```

**Improvements:**
- Reduced from 7 includes to 1 include
- Added 4 forward declarations
- All functionality preserved
- Dramatic compilation improvement

### grid_pattern.cpp (Full includes here)

```cpp
// frameworks/core/components_ng/pattern/grid/grid_pattern.cpp
#include "core/components_ng/pattern/grid/grid_pattern.h"

// Full includes now in implementation file
#include "core/components_ng/base/frame_node.h"
#include "core/components_ng/base/ui_node.h"
#include "core/components_ng/property/grid_layout_property.h"
#include "core/pipeline/base/element.h"
#include "base/memory/ace_type.h"

namespace OHOS::Ace::NG {

void GridPattern::OnModifyDone()
{
    // Can now call methods on FrameNode
    auto frameNode = AceType::DynamicCast<FrameNode>(GetHost());
    if (frameNode) {
        frameNode->MarkDirtyNode(PROPERTY_UPDATE_MEASURE);
    }
}

FrameNode* GridPattern::GetFrameNode() const
{
    return frameNode_;
}

void GridPattern::SetFrameNode(FrameNode* node)
{
    frameNode_ = node;
}

void GridPattern::ProcessElement(Element* element)
{
    if (!element) {
        return;
    }
    element_ = element;
}

}  // namespace OHOS::Ace::NG
```

## Analysis

### Include Audit

| Include | Usage | Action |
|---------|-------|--------|
| `frame_node.h` | Pointer member, return type | ✅ Forward declare |
| `ui_node.h` | Pointer member | ✅ Forward declare |
| `pattern.h` | Base class | ❌ Must keep (base class) |
| `grid_layout_property.h` | Pointer member | ✅ Forward declare |
| `scroll_bar_property.h` | Not used | ❌ Remove |
| `element.h` | Pointer parameter | ✅ Forward declare |
| `layout.h` | Not used | ❌ Remove |

### Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total includes | 7 | 1 | **86% reduction** |
| Forward declarations | 0 | 4 | **Dependency hiding** |
| Unused includes | 2 | 0 | **Cleaned up** |
| Header file size | ~8.2 KB | ~1.1 KB | **87% smaller** |

## Why Each Forward Declaration Works

### FrameNode (Forward Declaration Works)
```cpp
// In header
class FrameNode;  // ✅ Forward declaration

FrameNode* GetFrameNode() const;  // ✅ Used as pointer
void SetFrameNode(FrameNode* node);  // ✅ Used as pointer
private:
    FrameNode* frameNode_;  // ✅ Used as pointer member

// In cpp (full include)
#include "core/components_ng/base/frame_node.h"
frameNode_->GetValue();  // Now we can call methods
```

### Pattern (Must Keep Full Include)
```cpp
// ❌ Cannot forward declare base class
class Pattern;  // NOT sufficient

class GridPattern : public Pattern {  // ❌ ERROR: incomplete type
};

// ✅ Must include full header
#include "core/components_ng/pattern/pattern.h"

class GridPattern : public Pattern {  // ✅ Works
};
```

## Benefits

1. **Compilation Speed**: Any file including grid_pattern.h no longer parses FrameNode (~500 lines), UINode (~300 lines), GridLayoutProperty (~400 lines), Element (~200 lines)
2. **Recompilation**: Changes to FrameNode don't trigger recompilation of GridPattern includers
3. **Coupling**: Reduced coupling between GridPattern and implementation details
4. **Clarity**: Clear interface without implementation details

## Decision Flow

```
For each #include in header:
│
├─ Is it the base class?
│  └─ YES → Keep full include
│
├─ Is type used as member instance (not pointer/ref)?
│  └─ YES → Keep full include
│
├─ Are methods called on this type in header?
│  └─ YES → Keep full include (or move to cpp)
│
├─ Is type only used as pointer/reference/parameter?
│  └─ YES → Use forward declaration
│
└─ Is type not used at all?
   └─ YES → Remove include
```

## Common Patterns in ace_engine

### Pattern 1: Multiple Forward Declarations
```cpp
#pragma once
#include "core/components_ng/pattern/pattern.h"

namespace OHOS::Ace::NG {
class FrameNode;
class UINode;
class LayoutProperty;
class PaintProperty;
class EventHub;
}

class MyPattern : public Pattern {
    // ...
};
```

### Pattern 2: Nested Namespaces
```cpp
#pragma once

namespace OHOS {
class Element;
}

namespace OHOS::Ace::NG {
class FrameNode;
}

class MyClass {
    // ...
};
```

### Pattern 3: Mixed Includes and Forward Declarations
```cpp
#pragma once

// Essential includes (base classes, templates)
#include "core/components_ng/pattern/pattern.h"
#include "base/memory/ace_type.h"

// Forward declarations
namespace OHOS::Ace::NG {
class FrameNode;
class LayoutProperty;
}

class MyPattern : public Pattern {
    // ...
};
```

## Verification Steps

1. **Analyze includes**:
   ```bash
   grep "^#include" grid_pattern.h
   ```

2. **Check type usage**:
   ```bash
   grep -E "(FrameNode|UINode|Element)" grid_pattern.h
   ```

3. **Convert to forward declarations**:
   - Replace `#include` with forward declaration
   - Keep base class includes

4. **Move full includes to cpp**:
   - Add all removed includes to cpp file

5. **Test compilation**:
   ```bash
   # Use compile-analysis skill to verify
   ```

6. **Verify functionality**:
   - Run unit tests
   - Check for compilation errors

## Key Takeaways

1. **Forward declarations are powerful**: Can eliminate most heavy includes
2. **Base classes need full includes**: Cannot forward declare base classes
3. **Pointer/reference only**: Forward declarations only work for pointers/references
4. **Move method calls to cpp**: If header needs to call methods, move to cpp or include full header
5. **Measure impact**: Use compile-analysis to verify improvement
