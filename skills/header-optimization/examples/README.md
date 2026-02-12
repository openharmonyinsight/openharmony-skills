# Header Optimization Examples

This directory contains working examples demonstrating header optimization techniques for ace_engine.

## Directory Structure

```
examples/
├── before-after/
│   ├── inline_extraction_example.md    - Moving inline methods to cpp
│   ├── forward_declaration_example.md  - Converting includes to forward declarations
│   ├── pimpl_example.md                - Applying PIMPL pattern
│   └── split_header_example.md         - Splitting headers for constants/enums
├── pimpl-example/
│   ├── README.md                       - Complete PIMPL tutorial
│   ├── before/                         - Before optimization
│   └── after/                          - After optimization
└── split-header/
    ├── README.md                       - Header splitting guide
    ├── before/
    └── after/
```

## Example Categories

### 1. Before/After Comparisons

Located in `before-after/`, these examples show side-by-side comparisons of optimization techniques.

#### Inline Extraction Example
**File**: `inline_extraction_example.md`

Demonstrates moving inline method implementations from header to cpp:
- Before: Header with 4 inline methods (3+ lines each)
- After: Header with only declarations, implementations in cpp
- Results: 80% reduction in includes, 57% reduction in header lines

**When to use**: When header has multiple inline implementations

#### Forward Declaration Example
**File**: `forward_declaration_example.md`

Demonstrates converting heavy includes to forward declarations:
- Before: Header with 7 includes
- After: Header with 1 include + 4 forward declarations
- Results: 86% reduction in includes, 87% smaller header file

**When to use**: When types are only used as pointers/references

### 2. PIMPL Pattern Example

Located in `pimpl-example/`, complete working example of PIMPL implementation.

**Structure**:
- `README.md` - Detailed PIMPL tutorial
- `before/` - Original heavy header
- `after/` - Optimized with PIMPL pattern

**Benefits**:
- Hides all implementation dependencies
- Changes to Impl don't trigger recompilation
- Clean public interface

**When to use**:
- Heavy private dependencies
- Frequently included header
- Implementation changes often

### 3. Header Splitting Example

Located in `split-header/`, demonstrates extracting constants/enums to separate headers.

**Structure**:
- `README.md` - Guide for when and how to split
- `before/` - Large header with mixed concerns
- `after/` - Split into types/constants and implementation

**Benefits**:
- Files needing only constants don't pull in implementation
- Reduces cascading includes
- Improves incremental build times

**When to use**:
- Header contains frequently-used constants/enums
- Many files depend on these values
- Splitting provides measurable benefit

## How to Use These Examples

### Learning Path

1. **Start with before-after examples**:
   - Read inline_extraction_example.md
   - Understand the pattern
   - Try applying to a simple header

2. **Progress to forward declarations**:
   - Read forward_declaration_example.md
   - Practice identifying candidates
   - Learn decision flow

3. **Study PIMPL pattern**:
   - Review pimpl-example/README.md
   - Understand when to apply
   - Note the trade-offs

4. **Explore header splitting**:
   - Read split-header/README.md
   - Identify splitting opportunities
   - Measure impact

### Applying to Your Code

1. **Analyze current state**:
   ```bash
   # Use the analysis scripts
   ../scripts/analyze-includes.sh your_header.h
   python3 ../scripts/extract-includes.py your_header.h
   ```

2. **Choose appropriate technique**:
   - Many inline methods? → Inline extraction
   - Heavy includes? → Forward declarations
   - Complex private deps? → PIMPL
   - Shared constants? → Header splitting

3. **Apply optimization**:
   - Use header-optimization skill
   - Follow example patterns
   - Verify with standalone compilation

4. **Measure impact**:
   - Use compile-analysis skill
   - Compare before/after
   - Document improvements

## Common Patterns

### Pattern 1: Combination Approach

Most effective optimizations combine multiple techniques:

```cpp
// Optimized header combining techniques
#pragma once
#include "base/pattern.h"  // Only base class

// Forward declarations (technique 2)
namespace OHOS::Ace::NG {
class FrameNode;
class LayoutProperty;
}

class MyPattern : public Pattern {
    // Declarations only (technique 1)
    void OnModifyDone();
    FrameNode* GetNode();

private:
    class Impl;  // PIMPL (technique 3)
    std::unique_ptr<Impl> impl_;
};
```

### Pattern 2: Gradual Migration

Don't try to optimize everything at once:

1. **First iteration**: Forward declarations
2. **Second iteration**: Move inline methods
3. **Third iteration**: Consider PIMPL if needed
4. **Fourth iteration**: Split headers if beneficial

### Pattern 3: Measurement-Driven

Always measure impact:

```bash
# Before optimization
python3 ../scripts/extract-includes.py header.h > before.txt

# Apply optimization
# ...

# After optimization
python3 ../scripts/extract-includes.py header.h > after.txt

# Compare
diff before.txt after.txt
```

## Integration with Header-Optimization Skill

These examples demonstrate techniques used by the header-optimization skill:

1. **Step 2: Move inline implementations** → See inline_extraction_example.md
2. **Step 3: Remove unnecessary includes** → See forward_declaration_example.md
3. **Step 4: Convert to forward declarations** → See forward_declaration_example.md
4. **Step 5: Split headers** → See split-header/README.md
5. **Step 6: Apply PIMPL** → See pimpl-example/README.md

## Verification Checklist

After applying optimizations from examples:

- [ ] Header compiles standalone
- [ ] CPP file compiles with all dependencies
- [ ] No compilation warnings
- [ ] Unit tests pass
- [ ] Include count reduced
- [ ] Compilation time improved
- [ ] File size reduced
- [ ] Functionality preserved

## Troubleshooting

### Issue: Compilation errors after forward declaration

**Solution**: Check if type is used as:
- Base class → Must keep full include
- Member instance (not pointer) → Must keep full include
- Method call in header → Move to cpp or keep include

**Reference**: forward_declaration_example.md

### Issue: Incomplete type errors

**Solution**: Ensure full include is in cpp file:
```cpp
// cpp.cpp
#include "header.h"
#include "full/dependency.h"  // Add this
```

### Issue: Unique_ptr with forward declaration

**Solution**: Define destructor in cpp:
```cpp
// header.h
~MyClass();  // Declaration only

// cpp.cpp
#include "full/type.h"
MyClass::~MyClass() = default;  // Definition here
```

**Reference**: pimpl-example/README.md

## Contributing Examples

To add new examples:

1. Choose appropriate category (before-after, pimpl-example, split-header)
2. Create markdown file with:
   - Before code
   - After code
   - Explanation of changes
   - Results/metrics
3. Include verification steps
4. Add reference to this README

## Additional Resources

- **SKILL.md** - Main optimization workflow
- **references/patterns.md** - Detailed refactoring patterns
- **references/pimp-guide.md** - PIMPL comprehensive guide
- **references/forward-declaration.md** - Forward declaration best practices
- **scripts/** - Analysis and extraction utilities
