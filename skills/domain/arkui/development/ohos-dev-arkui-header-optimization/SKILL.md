---
name: ohos-dev-arkui-header-optimization
description: >
  Optimize C++ header files in ace_engine to reduce compilation time and memory.
  Use when user says 优化头文件/optimize header, 减少依赖/reduce dependencies, forward declaration,
  or mentions header compilation overhead.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkui
  capability: header-optimization
  version: 0.1.0
  status: trial
---

# ArkUI Header Optimization

Reduce C++ header compilation overhead in ace_engine through dependency analysis and refactoring.

## Critical Rules

- Only modify structure, never change business logic
- Verify standalone compilation after each change (no full build needed)
- After each successful optimization step, list suggested files for user to review before staging
- NEVER modify test_header.cpp (read-only reference for compilation testing)

## Analysis Workflow

### Step 1: Identify Target and Baseline

Determine the header file to optimize. If user provides a file, start there. Otherwise identify the target from context.

For compilation metrics, use `arkui-compile-analysis` skill to measure before/after.

**Quick screening** — when the header has 5+ includes and you need a first-pass triage:
```bash
python3 <skill_dir>/scripts/extract-includes.py <header_file>
```
This script scans every `#include`, resolves the exported type names (from a known list or by parsing the included header), and classifies each as `[unused]` / `[candidate]` / `[? review]` / `[unsafe]`. It is a screening tool — results must be verified before acting.

**When to skip the script** — if the header has ≤3 includes or you already know which types are pointer/ref vs value, go directly to Step 2 and classify manually by reading the code.

### Step 2: Analyze Dependencies

Read the header file. For each `#include`, classify usage:

| Usage Pattern | Forward Declare? | Keep Include? |
|---|---|---|
| Pointer/reference member (`T*`, `T&`, `RefPtr<T>`, `unique_ptr<T>`) | YES | Move to .cpp |
| Pointer/reference parameter or return type | YES | Move to .cpp |
| Base class inheritance | NO | KEEP |
| Value member (not pointer/reference) | NO | KEEP |
| Method called on type in header inline code | NO | KEEP (or extract to .cpp) |
| Template parameter to `sizeof`/`decltype`/type traits | NO | KEEP |
| Enum/constant used as default value | NO | KEEP (or split to separate header) |

**ACE Engine specific check**:
- `base/memory/ace_type.h` already includes `referenced.h` — if both are present, remove `referenced.h`
- Check for cross-namespace includes (`OHOS::Ace` types in `OHOS::Ace::NG` headers) — these are often replaceable

### Step 3: Choose Strategy by Decision Tree

```
Header analysis results
├─ Many unused includes? → Strategy: Remove Unnecessary Includes
├─ Inline methods > 3 lines? → Strategy: Extract Inline Implementations
├─ Types used only as pointer/ref? → Strategy: Forward Declarations
├─ Heavy header for enums/constants only? → Strategy: Split Enums/Constants
├─ Complex private dependencies, many includers? → Strategy: PIMPL
└─ Multiple issues? → Apply in order: remove unused → extract inline → forward declare → split
```

**Priority order** (highest impact, lowest risk first):
1. Remove unused includes
2. Remove redundant includes (e.g., `referenced.h` when `ace_type.h` present)
3. Replace includes with forward declarations
4. Extract inline implementations (>3 lines) to .cpp
5. Split enums/constants to lightweight header
6. PIMPL (only when other strategies insufficient)

## Strategies

### Strategy 1: Remove Unnecessary Includes

For each include, search the header (excluding `#include` lines) for type usage:
```bash
# Check if header_name appears in file (excluding include lines)
grep -v "^#include" <header_file> | grep -c "<ClassName>"
```

If count is 0, the include is likely unused. Remove it, then verify compilation.

### Strategy 2: Forward Declarations

Replace full includes with forward declarations when type is only used as pointer/reference.

**ACE Engine forward declaration cheat sheet**:
```cpp
// NG components (can forward declare when used as ptr/ref)
namespace OHOS::Ace::NG {
class FrameNode;
class UINode;
class PatternField;
class PatternFieldInfo;
class LayoutProperty;
class PaintProperty;
class EventHub;
class GestureEventHub;
class RenderContext;
class FrameNode;
}
// Patterns
namespace OHOS::Ace::NG { class Pattern; }
// Base
namespace OHOS::Ace {
class Element;
class RenderNode;
class PipelineBase;
}
// Template forward declaration
namespace OHOS::Ace { template<typename T> class RefPtr; }
```

**SmartPointer rules**:
- `RefPtr<T>` with forward-declared T: works, T only needs to be complete where RefPtr is constructed/destroyed
- `std::unique_ptr<T>` with forward-declared T: works, but destructor MUST be defined in .cpp (not `= default` in header)
- `std::shared_ptr<T>` with forward-declared T: works without destructor trick

**Pitfall — `RefPtr<T>` requires full include when**:
- Calling `RefPtr<T>::operator->` (accessing T's members)
- Using `AceType::DynamicCast<T>(...)` in the header
- Constructing `RefPtr<T>(new T(...))` in the header

### Strategy 3: Extract Inline Implementations

Move inline methods exceeding 3 lines from header to .cpp:

1. Replace inline body with declaration in header
2. Create or append to .cpp file with full implementation
3. Add .cpp to `BUILD.gn` if new file:
   ```python
   # In ace_core_ng_source_set or relevant target
   sources += [ "path/to/new_file.cpp" ]
   ```

**Common ACE Engine pattern** — methods to extract first:
- `OnModifyDone()` — typically 20+ lines accessing many dependencies
- `OnDirtyLayoutWrapperSwap()` — complex layout logic
- `ToJsonValue()` / `FromJsonValue()` — serialization with many includes
- `GetOrCreate*()` methods — often inline with heavy dependencies

### Strategy 4: Split Enums/Constants

When a header is included only for enum/constant definitions:

1. Check if a `_constants.h` or `_types.h` already exists — reuse if possible
2. If not, create lightweight header with only enums/constants
3. Original heavy header includes the lightweight one
4. Consumers needing only enums include the lightweight one instead

**Decision**: Create new file or reuse existing?

| Scenario | Action |
|---|---|
| `_constants.h` already exists with other enums | Add enums to it (check namespace matches) |
| No constants file exists | Create new `_constants.h` |
| Enums used across NG and non-NG code | Place in `OHOS::Ace` namespace, not `OHOS::Ace::NG` |

### Strategy 5: PIMPL

Apply only when:
- Class has 5+ private members with heavy dependencies
- Header is included by 20+ files
- Implementation changes frequently
- Other strategies alone are insufficient

**ACE Engine PIMPL pattern**:
```cpp
// header.h
class MyClass : public AceType {
public:
    MyClass();
    ~MyClass() override;  // MUST be in .cpp
    // Disable copy
    MyClass(const MyClass&) = delete;
    MyClass& operator=(const MyClass&) = delete;
private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};
```

NEVER apply PIMPL to:
- Small classes with < 3 private members
- Performance-critical hot paths (gesture recognition, layout measurement)
- Classes that need value semantics (copy/move)

## Reference Cases

For real-world optimization examples with metrics and step-by-step instructions:

| Case | Technique | Impact | MANDATORY Read |
|---|---|---|---|
| [click_event.h](references/case-click_event-forward-declaration.md) | Forward decl + inline extract | 35% size reduction, 67% fewer inlines | When optimizing event/gesture headers |
| [drag_event.h include reduction](references/case-drag-event-include-reduction.md) | Replace heavy include with light include | 92.5% reduction in included code | When cross-namespace include is the bottleneck |
| [drag_drop config](references/case-drag-drop-forward-declaration.md) | Forward decl + value-to-unique_ptr | Removed gesture_info.h dependency | When value members block forward declaration |
| [split enums](references/case-split-enums.md) | Extract enums to separate header | 90%+ dependency reduction for 45+ files | When many consumers only need enums |

**Do NOT load** reference cases unless the technique matches the current optimization target.

## Scripts

- `scripts/extract-includes.py <header_file> [--format json|text]` — Quick screening tool: resolves type names from each include, classifies as unused/candidate/needs_check/unsafe. Use for first-pass triage on headers with 5+ includes. Results are heuristic — verify before acting.

## NEVER Rules

1. **NEVER** remove an include guarded by `#ifdef OHOS_BUILD_ENABLE_*` — it may be needed in other build configurations
2. **NEVER** forward-declare a type used as a base class or value member — compiler error guaranteed
3. **NEVER** move constexpr/inline functions to .cpp without checking if callers depend on compile-time evaluation
4. **NEVER** create a PIMPL for classes with < 3 private members — overhead exceeds benefit
5. **NEVER** modify `ace_type.h`, `frame_node.h`, or other "hub" headers — they are included by thousands of files
6. **NEVER** change function signatures in frequently-included headers — forces recompilation of all includers
7. **NEVER** add new public includes to a header that is being optimized — defeats the purpose
8. **NEVER** forget to add new .cpp files to BUILD.gn — silent build breakage
9. **NEVER** use PIMPL for performance-critical paths (layout, render, gesture) — pointer indirection cost is measurable
