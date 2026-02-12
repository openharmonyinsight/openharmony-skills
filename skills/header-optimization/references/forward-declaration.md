# Forward Declaration Best Practices for ACE Engine

Comprehensive guide for using forward declarations to reduce header dependencies in ace_engine.

## What is Forward Declaration?

Forward declaration tells compiler that a class exists without providing its full definition:

```cpp
// Forward declaration
namespace OHOS::Ace::NG {
class FrameNode;
}

// Full include
#include "core/components_ng/base/frame_node.h"
```

### Benefits
- **Dramatically reduces compilation time** - Avoids parsing entire header
- **Breaks circular dependencies** - Headers can reference each other
- **Reduces recompilation cascade** - Changes to forwarded class don't trigger recompilation

### Limitations
- Can only use with pointers/references, not complete types
- Cannot call methods (including constructors/destructors) without definition
- Cannot use type as base class
- Cannot access members or sizeof

## When Forward Declaration is Sufficient

### ✅ CAN Use Forward Declaration

**1. Pointer/reference member variables:**
```cpp
class FrameNode;  // Forward declaration OK

class MyClass {
    FrameNode* node_;           // ✅ OK - pointer
    FrameNode& ref_;            // ✅ OK - reference
    std::unique_ptr<FrameNode> ptr_;  // ✅ OK - smart pointer
};
```

**2. Function parameters:**
```cpp
class FrameNode;  // Forward declaration OK

class MyClass {
public:
    void Process(FrameNode* node);     // ✅ OK
    void Update(FrameNode& node);      // ✅ OK
    FrameNode* GetNode();              // ✅ OK
};
```

**3. Return types:**
```cpp
class FrameNode;  // Forward declaration OK

class MyClass {
public:
    FrameNode* CreateNode();  // ✅ OK
    FrameNode& GetNodeRef();  // ✅ OK
};
```

**4. Template parameters:**
```cpp
template<typename T>
class Container;  // Forward declaration OK

void Process(Container<FrameNode>* container);  // ✅ OK
```

### ❌ CANNOT Use Forward Declaration (Need Full Include)

**1. Base class inheritance:**
```cpp
class FrameNode;  // NOT enough!

class MyNode : public FrameNode {  // ❌ ERROR - incomplete type
};
```

**2. Member variable instances:**
```cpp
class FrameNode;  // NOT enough!

class MyClass {
    FrameNode node_;  // ❌ ERROR - incomplete type
};
```

**3. Calling methods (including implicit):**
```cpp
class FrameNode;  // NOT enough!

class MyClass {
public:
    void Process() {
        node_->GetValue();  // ❌ ERROR - incomplete type
        // Can't call methods on forwarded type
    }
private:
    FrameNode* node_;
};
```

**4. Using sizeof or type traits:**
```cpp
class FrameNode;  // NOT enough!

sizeof(FrameNode);  // ❌ ERROR - incomplete type
std::is_copy_constructible<FrameNode>::value;  // ❌ ERROR
```

## Forward Declaration Patterns

### Pattern 1: Standard Forward Declaration

```cpp
// header.h
#pragma once

namespace OHOS::Ace::NG {
class FrameNode;
class UINode;
class PatternField;
}

class MyClass {
public:
    void Process(OHOS::Ace::NG::FrameNode* node);

private:
    OHOS::Ace::NG::UINode* uiNode_;
    OHOS::Ace::NG::PatternField* field_;
};
```

### Pattern 2: Using Alias

```cpp
// header.h
#pragma once

namespace OHOS::Ace::NG {
class FrameNode;
}

using FrameNodePtr = OHOS::Ace::NG::FrameNode*;

class MyClass {
public:
    void Process(FrameNodePtr node);
private:
    FrameNodePtr node_;
};
```

### Pattern 3: Nested Namespace Forward Declaration

```cpp
// header.h
#pragma once

// Forward declare nested classes
namespace Outer {
    namespace Inner {
        class MyClass;
    }
}

// Or use shorthand (C++17 and later)
namespace Outer::Inner {
    class MyClass;
}
```

### Pattern 4: Template Forward Declaration

```cpp
// header.h
#pragma once

template<typename T>
class Container;

template<typename T>
class MyClass {
public:
    void Process(Container<T>* container);
private:
    Container<T>* container_;
};
```

## Common ace_engine Forward Declarations

### NG Components (Frequently Used)

```cpp
// Core node types
namespace OHOS::Ace::NG {
class FrameNode;
class UINode;
class RenderContext;
}

// Pattern classes
namespace OHOS::Ace::NG {
class Pattern;
class PatternField;
}

// Properties
namespace OHOS::Ace::NG {
class LayoutProperty;
class PaintProperty;
class LayoutConstraint;
}

// Event handling
namespace OHOS::Ace::NG {
class EventHub;
class GestureEventHub;
}
```

### Base Components

```cpp
// Core types
namespace OHOS::Ace {
class Element;
class RenderNode;
class RenderContext;
class PipelineBase;
}

// Memory management
namespace OHOS::Ace {
class AceType;
template<typename T>
class RefPtr;  // Template forward declaration
}
```

### Common Patterns

```cpp
// Standard pattern in ace_engine headers
#pragma once

#include "minimal_base.h"  // Only essential includes

namespace OHOS::Ace::NG {
// Forward declarations instead of includes
class FrameNode;
class UINode;
class LayoutProperty;
}  // namespace OHOS::Ace::NG

namespace OHOS::Ace {
class PipelineBase;
}  // namespace OHOS::Ace

class MyPattern {
public:
    void OnModifyDone();
    FrameNode* GetHost();

private:
    FrameNode* host_;
    LayoutProperty* layoutProperty_;
};
```

## Converting Includes to Forward Declarations

### Step-by-Step Process

**Step 1: Identify candidates**
```bash
# Find all includes in header
grep "^#include" header.h

# Common candidates:
# - core/components_ng/base/frame_node.h
# - core/pipeline/base/element.h
# - base/memory/ace_type.h
```

**Step 2: Verify usage**
```bash
# Search for type usage in file
grep "FrameNode" header.h
grep "Element" header.h

# Look for:
# - As pointer/reference? → Can forward declare
# - As base class? → Need full include
# - As member instance? → Need full include
# - Methods called? → Need full include
```

**Step 3: Replace with forward declaration**
```cpp
// Before
#include "core/components_ng/base/frame_node.h"

// After
namespace OHOS::Ace::NG {
class FrameNode;
}
```

**Step 4: Add full include in cpp (if needed)**
```cpp
// implementation.cpp
#include "header.h"
#include "core/components_ng/base/frame_node.h"  // Full include here

void MyClass::Method() {
    node_->GetValue();  // Now we can call methods
}
```

**Step 5: Test compilation**
```bash
# Use compile-analysis skill to verify
```

## Complex Scenarios

### Scenario 1: Circular Dependencies

```cpp
// button_pattern.h
#pragma once

// Can't include - circular dependency!
// #include "text_pattern.h"

namespace OHOS::Ace::NG {
class TextPattern;  // Forward declaration breaks cycle

class ButtonPattern {
public:
    void SetTextPattern(TextPattern* text);
private:
    TextPattern* textPattern_;
};
}
```

### Scenario 2: Template with Forward Declaration

```cpp
// header.h
#pragma once

template<typename T>
class Container;  // Forward declare template

namespace OHOS::Ace::NG {
class FrameNode;  // Forward declare class
}

template<typename T>
class MyClass {
public:
    void Process(Container<FrameNode>* container);
private:
    Container<FrameNode>* container_;
};
```

### Scenario 3: Smart Pointers with Forward Declaration

```cpp
// header.h
#pragma once
#include <memory>

namespace OHOS::Ace::NG {
class FrameNode;
}

class MyClass {
public:
    MyClass();
    ~MyClass();  // Must be in cpp for unique_ptr with forward declaration

private:
    class Impl;
    std::unique_ptr<Impl> impl_;  // PIMPL pattern
    // OR
    std::unique_ptr<FrameNode> node_;  // Requires destructor in cpp
};

// cpp.cpp
#include "header.h"
#include "core/components_ng/base/frame_node.h"  // Full include

MyClass::MyClass() = default;
MyClass::~MyClass() = default;  // Requires FrameNode definition here
```

## Forward Declaration Templates

### Basic Template

```cpp
// Single class
namespace OHOS::Ace::NG {
class FrameNode;
}

// Multiple classes
namespace OHOS::Ace::NG {
class FrameNode;
class UINode;
class PatternField;
class LayoutProperty;
}

// Nested namespace
namespace OHOS {
namespace Ace {
namespace NG {
class FrameNode;
}
}
}
```

### With Comments (Recommended for ace_engine)

```cpp
// Forward declarations
namespace OHOS::Ace::NG {
class FrameNode;       // Used: GetHost() return type
class LayoutProperty;  // Used: UpdateLayout() parameter
class EventHub;        // Used: eventHub_ member
}
```

### Organized by Usage

```cpp
// Forward declarations - Base classes
namespace OHOS::Ace::NG {
class Pattern;
}

// Forward declarations - Member variables
namespace OHOS::Ace::NG {
class FrameNode;
class LayoutProperty;
}

// Forward declarations - Function parameters
namespace OHOS::Ace {
class PipelineBase;
}
```

## Troubleshooting

### Error: Incomplete Type

```cpp
// Error: invalid use of incomplete type
node_->GetValue();
```

**Solution**: Need full include in cpp file:
```cpp
// cpp.cpp
#include "header.h"
#include "core/components_ng/base/frame_node.h"  // Add this
```

### Error: sizeof on Incomplete Type

```cpp
// Error: invalid application of 'sizeof' to incomplete type
size_t size = sizeof(FrameNode);
```

**Solution**: This operation requires full include. Move to cpp or reconsider design.

### Error: Base Class Incomplete

```cpp
// Error: base class has incomplete type
class MyNode : public FrameNode { };
```

**Solution**: Cannot forward declare base class. Must use full include.

### Error: Template Instantiation

```cpp
// Error: implicit instantiation of undefined template
std::unique_ptr<FrameNode> ptr_;
```

**Solution**: Smart pointers are OK with forward declaration, but destructor must be in cpp file:
```cpp
// header.h
class MyClass {
public:
    ~MyClass();  // Declaration only
private:
    std::unique_ptr<FrameNode> ptr_;
};

// cpp.cpp
#include "core/components_ng/base/frame_node.h"
MyClass::~MyClass() = default;  // Definition here
```

## Best Practices Summary

### ✅ DO

1. **Forward declare whenever possible**
   - Reduces compilation dependencies
   - Improves build times
   - Breaks circular dependencies

2. **Organize forward declarations**
   - Group by namespace
   - Add comments explaining usage
   - Place at top of header after includes

3. **Use standard naming**
   ```cpp
   namespace OHOS::Ace::NG {
   class FrameNode;  // Same name as actual class
   }
   ```

4. **Keep forward declarations in header**
   - Full includes go in cpp
   - Clear separation of interface and implementation

### ❌ DON'T

1. **Forward declare when full definition needed**
   - Base classes
   - Member instances
   - Method calls in header

2. **Mix forward declaration styles**
   ```cpp
   // ❌ Confusing
   namespace OHOS::Ace { class FrameNode; }
   class OHOS::Ace::NG::UINode;

   // ✅ Consistent
   namespace OHOS::Ace {
   class FrameNode;
   }

   namespace OHOS::Ace::NG {
   class UINode;
   }
   ```

3. **Forward declare in cpp files**
   - Just include the full header
   - Forward declarations provide no benefit in cpp

4. **Forward declare standard library types**
   ```cpp
   // ❌ Wrong
   class std::string;
   class std::vector;

   // ✅ Correct
   #include <string>
   #include <vector>
   ```

## Automated Analysis

### Script to Find Forward Declaration Candidates

```bash
#!/bin/bash
# find_forward_decl_candidates.sh

HEADER=$1

echo "Analyzing $HEADER for forward declaration candidates..."
echo ""

# Extract all includes
echo "Current includes:"
grep "^#include" "$HEADER" | while read include; do
    echo "  $include"
done

echo ""
echo "Potentially convertible to forward declarations:"
echo "  (Review these manually - they might be convertible)"

# Look for common patterns
grep -o "core/components_ng/[a-z_]*\.h" "$HEADER" | sort -u
```

## Integration with Header Optimization

When applying header-optimization skill:

1. **Start with forward declarations**
   - Lowest hanging fruit
   - Biggest impact
   - Minimal risk

2. **Verify with compile-analysis skill**
   - Extract compilation command
   - Test standalone compilation
   - Measure improvement

3. **Document changes**
   - List converted includes
   - Report dependency reduction
   - Note any limitations

## Reference: Common ace_engine Types

### Always Need Full Include
- `RefPtr<T>` - Template instantiation
- `std::string` - Standard library
- Base classes being inherited
- Types used as member instances (not pointers)

### Can Usually Forward Declare
- `FrameNode`, `UINode` - Node types
- `Pattern`, `PatternField` - Pattern types
- `LayoutProperty`, `PaintProperty` - Property types
- `Element`, `RenderNode` - Core types
- Event types, callback types

### Decision Matrix

| Type | Pointer/Reference | Member Instance | Base Class | Method Call |
|------|------------------|-----------------|------------|-------------|
| FrameNode | ✅ Forward declare | ❌ Include | ❌ Include | ❌ Include (in cpp) |
| Pattern | ✅ Forward declare | ❌ Include | ❌ Include | ❌ Include (in cpp) |
| std::string | ❌ Include | ❌ Include | N/A | N/A |
