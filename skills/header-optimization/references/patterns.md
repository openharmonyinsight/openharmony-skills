# Common Refactoring Patterns for Header Optimization

This reference provides detailed patterns and examples for header optimization in ace_engine.

## Pattern 1: Inline Implementation Extraction

### When to Apply
- Methods with more than 3 lines of implementation in header
- Static methods with complex logic
- Helper functions defined in headers

### Pattern Template

**Before:**
```cpp
// header.h
#pragma once
#include <string>

class MyClass {
public:
    std::string ProcessData(const std::string& input) {
        std::string result = input;
        result.erase(std::remove(result.begin(), result.end(), ' '), result.end());
        std::transform(result.begin(), result.end(), result.begin(), ::tolower);
        return result;
    }

    static bool IsValid(const std::string& str) {
        if (str.empty()) return false;
        for (char c : str) {
            if (!std::isalnum(c)) return false;
        }
        return true;
    }
};
```

**After:**
```cpp
// header.h
#pragma once
#include <string>

class MyClass {
public:
    std::string ProcessData(const std::string& input);
    static bool IsValid(const std::string& str);
};

// cpp.cpp
#include "header.h"
#include <algorithm>
#include <cctype>

std::string MyClass::ProcessData(const std::string& input) {
    std::string result = input;
    result.erase(std::remove(result.begin(), result.end(), ' '), result.end());
    std::transform(result.begin(), result.end(), result.begin(), ::tolower);
    return result;
}

bool MyClass::IsValid(const std::string& str) {
    if (str.empty()) return false;
    for (char c : str) {
        if (!std::isalnum(c)) return false;
    }
    return true;
}
```

### Benefits
- Reduces header coupling (algorithm, cctype no longer needed in header)
- Improves compilation time for files including this header
- Hides implementation details

## Pattern 2: Include to Forward Declaration Conversion

### When to Apply
- Header only uses type as pointer/reference
- Type is used as function parameter or return type
- No inheritance from the type
- No member variables of the type

### Pattern Template

**Before:**
```cpp
// header.h
#pragma once
#include "core/components_ng/base/frame_node.h"
#include "core/components_ng/base/view_abstract.h"
#include "core/pipeline/base/element.h"

class MyPattern : public ViewAbstract {
public:
    void SetFrameNode(FrameNode* node);
    FrameNode* GetFrameNode() const;
    void ProcessElement(Element* element);

private:
    FrameNode* frameNode_ = nullptr;
    Element* element_ = nullptr;
};
```

**After:**
```cpp
// header.h
#pragma once
#include "core/components_ng/base/view_abstract.h"  // Base class - keep include

namespace OHOS::Ace::NG {
class FrameNode;
}  // namespace OHOS::Ace::NG

namespace OHOS::Ace {
class Element;
}  // namespace OHOS::Ace

class MyPattern : public ViewAbstract {
public:
    void SetFrameNode(OHOS::Ace::NG::FrameNode* node);
    OHOS::Ace::NG::FrameNode* GetFrameNode() const;
    void ProcessElement(OHOS::Ace::Element* element);

private:
    OHOS::Ace::NG::FrameNode* frameNode_ = nullptr;
    OHOS::Ace::Element* element_ = nullptr;
};
```

### Benefits
- Eliminates 2 heavy header includes
- Reduces compilation dependency chain
- No change to functionality

### Common ace_engine Forward Declarations

```cpp
// NG Components
namespace OHOS::Ace::NG {
class FrameNode;
class UINode;
class PatternField;
}

// Base Components
namespace OHOS::Ace {
class Element;
class RenderNode;
class NodePaintMethod;
}

// Pipeline
namespace OHOS::Ace {
class PipelineBase;
}
```

## Pattern 3: Unused Include Elimination

### Detection Method

For each `#include` in header:
1. Grep for types from that header
2. Check if used in: member variables, base classes, function parameters/returns
3. If not found → Remove

### Pattern Template

**Before:**
```cpp
// header.h
#pragma once
#include "base/memory/ace_type.h"          // Used: RefPtr
#include "base/utils/utils.h"              // Used: ConvertStringToUint32
#include "core/components/common/layout.h" // NOT USED - Remove
#include "core/patterns/pattern.h"         // Used: Pattern
#include "frameworks/base/log/ace_log.h"   // NOT USED - Remove

class MyPattern : public Pattern {
public:
    void Process(const std::string& value);

private:
    RefPtr<Data> data_;
};
```

**After:**
```cpp
// header.h
#pragma once
#include "base/memory/ace_type.h"
#include "base/utils/utils.h"
#include "core/patterns/pattern.h"

class MyPattern : public Pattern {
public:
    void Process(const std::string& value);

private:
    RefPtr<Data> data_;
};
```

### Verification Script
```bash
# For each include, check if type appears in file
grep -o "ClassName" header.h | wc -l
```

## Pattern 4: Constants/Enums Extraction

### When to Apply
- Header contains constants/enums used by many files
- Main header is large with heavy dependencies
- Constants can be isolated without affecting structure

### Pattern Template

**Before:**
```cpp
// button_pattern.h
#pragma once
#include "core/components_ng/base/frame_node.h"
// ... many more heavy includes

namespace OHOS::Ace::NG {
// Constants used by many components
constexpr int DEFAULT_BUTTON_WIDTH = 200;
constexpr int DEFAULT_BUTTON_HEIGHT = 40;

enum class ButtonType {
    NORMAL,
    CAPSULE,
    CIRCLE
};

class ButtonPattern : public Pattern {
    // ... hundreds of lines
};
}
```

**After:**
```cpp
// button_types.h (new file)
#pragma once

namespace OHOS::Ace::NG {
constexpr int DEFAULT_BUTTON_WIDTH = 200;
constexpr int DEFAULT_BUTTON_HEIGHT = 40;

enum class ButtonType {
    NORMAL,
    CAPSULE,
    CIRCLE
};
}

// button_pattern.h (modified)
#pragma once
#include "button_types.h"  // Light include
#include "core/components_ng/base/frame_node.h"
// ... other heavy includes

namespace OHOS::Ace::NG {
class ButtonPattern : public Pattern {
    // ... implementation
};
}
```

### Benefits
- Files needing only ButtonType don't pull in full ButtonPattern
- Reduces cascading includes
- Improves incremental build times

## Pattern 5: Template Method Optimization

### When to Apply
- Template has limited type usage
- Template parameter types are known
- Performance impact is acceptable

### Pattern Template

**Before:**
```cpp
// header.h
#pragma once

class MyClass {
public:
    template<typename T>
    T Process(T value) {
        // Complex logic depending on T
        if (value > 0) {
            return value * 2;
        }
        return value;
    }
};
```

**After:**
```cpp
// header.h
#pragma once

class MyClass {
public:
    template<typename T>
    T Process(T value);

    // Explicit instantiation declarations
    extern template int Process<int>(int);
    extern template float Process<float>(float);
};

// cpp.cpp
#include "header.h"

template<typename T>
T MyClass::Process(T value) {
    if (value > 0) {
        return value * 2;
    }
    return value;
}

// Explicit instantiation definitions
template int MyClass::Process<int>(int);
template float MyClass::Process<float>(float);
```

### Limitations
- Only works when types are known in advance
- Adds maintenance for new types
- May not be suitable for all templates

## Pattern 6: Conditional Include Removal

### When to Apply
- Include only used in specific #ifdef blocks
- Block is not active in current configuration

### Pattern Template

**Before:**
```cpp
// header.h
#pragma once
#include "base/log/log.h"
#include "core/components/button/button_layout_property.h"

#ifdef ENABLE_FEATURE_X
#include "feature_x/implementation.h"  // Only needed in FEATURE_X
#endif

class MyClass {
    // ...
};
```

**After:**
```cpp
// header.h
#pragma once
#include "base/log/log.h"
#include "core/components/button/button_layout_property.h"

#ifdef ENABLE_FEATURE_X
#include "feature_x/implementation.h"
#endif

class MyClass {
    // ...
};
```

Or better, move to cpp when possible:
```cpp
// header.h
#pragma once
#include "base/log/log.h"
#include "core/components/button/button_layout_property.h"

class MyClass {
    // ...
};

// cpp.cpp
#include "header.h"
#ifdef ENABLE_FEATURE_X
#include "feature_x/implementation.h"
#endif
```

## Pattern 7: std::pair/tuple Replacement

### When to Apply
- Header includes <utility> only for std::pair
- Can use custom struct or forward declare

### Pattern Template

**Before:**
```cpp
// header.h
#pragma once
#include <utility>  // Heavy include for std::pair
#include <string>

class MyClass {
public:
    std::pair<std::string, int> GetData();
};
```

**After (Option 1 - Custom Struct):**
```cpp
// header.h
#pragma once
#include <string>

struct DataResult {
    std::string name;
    int value;
};

class MyClass {
public:
    DataResult GetData();
};
```

**After (Option 2 - Return separate values):**
```cpp
// header.h
#pragma once
#include <string>

class MyClass {
public:
    std::string GetName();
    int GetValue();
};
```

### Benefits
- Eliminates <utility> dependency
- More descriptive API
- Better compile times

## Pattern 8: Member Variable Reordering

### When to Apply
- Reduce padding and improve cache locality
- Group related members together

### Pattern Template

**Before:**
```cpp
class MyClass {
    bool flag_;        // 1 byte + 7 padding
    int value_;        // 4 bytes
    double data_;      // 8 bytes
    char status_;      // 1 byte + 7 padding
};
// Total: 1+7 + 4 + 8 + 1+7 = 28 bytes
```

**After:**
```cpp
class MyClass {
    double data_;      // 8 bytes
    int value_;        // 4 bytes
    bool flag_;        // 1 byte
    char status_;      // 1 byte + 2 padding
};
// Total: 8 + 4 + 1 + 1+2 = 16 bytes
```

### Benefits
- Reduced memory usage
- Better cache locality
- Potential performance improvement

## Integration Checklist

For each pattern application:
- [ ] Verify pattern applies to current situation
- [ ] Apply refactoring following template
- [ ] Test standalone compilation
- [ ] Verify functionality unchanged
- [ ] Document change in optimization report
- [ ] Stage with git add

## Common ace_engine Types for Forward Declaration

```cpp
// Components NG
namespace OHOS::Ace::NG {
class FrameNode;
class UINode;
class PatternField;
class PatternFieldInfo;
class LayoutProperty;
class PaintProperty;
class EventHub;
}

// Patterns
namespace OHOS::Ace::NG {
class Pattern;
}

// Base
namespace OHOS::Ace {
class RenderNode;
class Element;
class PipelineBase;
class AceType;
}
```
