# Build Error Analyzer - Usage Examples

This document provides practical examples of using the build-error-analyzer skill.

## Example 1: Analyzing Linker Errors

### User Input

```
帮我分析一下构建错误
```

### Skill Response

**Step 1: Extract error log**
```bash
./extract_last_error.sh out/rk3568/build.log
```

**Step 2: Read and analyze**
Reading `last_error.log`...

**Error Type**: Linker Error (SOLINK task)

**Error Pattern**:
```
ld.lld: error: undefined symbol: OHOS::Ace::SomeClass::SomeMethod
```

**Analysis**:
- Symbol `SomeClass::SomeMethod` is undefined at link time
- This typically means the .cpp file is not in the build system
- Or the symbol needs to be exported for cross-module use

**Recommended Actions**:

1. **Check if .cpp file exists**:
   ```bash
   find frameworks/ -name "some_class.cpp"
   ```

2. **Check if it's in BUILD.gn**:
   ```bash
   grep -r "some_class.cpp" frameworks/*/BUILD.gn
   ```

3. **If file exists but not in BUILD.gn**:
   - Add to component BUILD.gn
   - Add to frameworks/core/BUILD.gn ace_core_ng_source_set

4. **If symbol is cross-module used**:
   - Add ACE_FORCE_EXPORT to header declaration
   - Add to build/libace.map

**Reference**: See `examples/undefined-symbol-missing-cpp.md` for detailed case study

---

## Example 2: Quick Error Check

### User Input

```
检查 last_error.log
```

### Skill Response

Reading `last_error.log`...

**Error Summary**:
- Type: Compilation Error
- File: `drawing_prop_convertor.cpp`
- Line: 217

**Error Details**:
```
error: member access into incomplete type 'const OHOS::Ace::TextStyle'
```

**Root Cause**: Missing header include - `text_style.h` only forward declares `TextStyle` but needs full definition

**Quick Fix**:
```cpp
// In drawing_prop_convertor.h, change:
class TextStyle;  // ❌ Forward declaration only

// To:
#include "text_style.h"  // ✅ Full definition
```

**Verification**:
```bash
./build.sh --product-name rk3568 --build-target ace_engine --ccache
```

---

## Example 3: Symbol Export Issues

### User Input

```
timepicker 链接错误，undefined symbol DialogTypeMargin::UpdateDialogMargin
```

### Skill Response

**Error**: `ld.lld: error: undefined symbol: OHOS::Ace::NG::DialogTypeMargin::UpdateDialogMargin`

**Analysis**: Symbol used by timepicker module but not exported from libace.z.so

**Solution**:

1. **Add ACE_FORCE_EXPORT to header**:
   ```cpp
   // button_layout_property.h
   class DialogTypeMargin {
   public:
       ACE_FORCE_EXPORT static void UpdateDialogMargin(...);
   };
   ```

2. **Add to libace.map**:
   ```
   global:
     extern "C++" {
       OHOS::Ace::NG::DialogTypeMargin::UpdateDialogMargin*;
     }
   ```

3. **Verify export**:
   ```bash
   nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep DialogTypeMargin
   # Should show: T _ZN4OHOS3Ace2NG16DialogTypeMargin...
   ```

**Reference**: `examples/undefined-symbol-missing-cpp.md` - Fix 3 section

---

## Example 4: Redefinition Errors

### User Input

```
编译错误：redefinition of DRAG_BACKGROUND_OPACITY
```

### Skill Response

**Error**:
```
error: redefinition of 'DRAG_BACKGROUND_OPACITY'
error: redefinition of 'URL_DISA_OPACITY'
```

**Root Cause**: Constants defined in both header and .cpp file

**Problem**:
```cpp
// text_theme.h
inline constexpr float DRAG_BACKGROUND_OPACITY = 0.95f;

// text_theme.cpp - ❌ WRONG: redefinition
constexpr float DRAG_BACKGROUND_OPACITY = 0.95f;
```

**Solution**: Remove duplicate definition from .cpp

```cpp
// text_theme.cpp - ✅ CORRECT: remove these lines
// constexpr float DRAG_BACKGROUND_OPACITY = 0.95f;
// constexpr float URL_DISA_OPACITY = 0.4f;
```

**Why**: `inline constexpr` in header provides definition, no need to repeat in .cpp

---

## Example 5: New .cpp File Not Building

### User Input

```
新增了 theme_manager_impl.cpp 但链接时报错找不到符号
```

### Skill Response

**Common issue**: New .cpp file not in ace_core_ng_source_set

**Diagnosis Steps**:

1. **Check component BUILD.gn**:
   ```bash
   grep "theme_manager_impl.cpp" frameworks/core/components/theme/BUILD.gn
   ```
   ✅ Found

2. **Check ace_core_ng_source_set**:
   ```bash
   grep "theme_manager_impl.cpp" frameworks/core/BUILD.gn
   ```
   ❌ Not found - This is the problem!

**Solution**: Add to `frameworks/core/BUILD.gn`:

```gn
template("ace_core_ng_source_set") {
  sources = [
    # ...
    "components/theme/theme_manager_impl.cpp",  # ✅ Add here
  ]
}
```

**Why**: libace.z.so only links ace_core_ng libraries, not component-specific libraries

---

## Example 6: Complete Workflow

### User Input

```
我修改了代码后构建失败，帮我看看
```

### Skill Workflow

**Step 1: Extract error**
```bash
./extract_last_error.sh out/rk3568/build.log
```
✅ Created last_error.log (68 lines)

**Step 2: Categorize error**
```
[666/809] SOLINK arkui/ace_engine/libace.z.so
```
→ Type: Linker Error

**Step 3: Identify pattern**
```
ld.lld: error: undefined symbol: OHOS::Ace::TextTheme::Builder::Build
```
→ Pattern: Missing .cpp in build system

**Step 4: Match case**
→ Matches: `examples/undefined-symbol-missing-cpp.md`

**Step 5: Provide solution**

Based on the case study, you need to:

1. **Verify .cpp file exists**:
   ```bash
   find frameworks/ -name "text_theme.cpp"
   ```
   ✅ Found at: frameworks/core/components/text/text_theme.cpp

2. **Check if in BUILD.gn**:
   ```bash
   grep "text_theme.cpp" frameworks/core/components/text/BUILD.gn
   ```
   ✅ In component BUILD.gn

   ```bash
   grep "text_theme.cpp" frameworks/core/BUILD.gn
   ```
   ❌ NOT in ace_core_ng_source_set ← Problem!

3. **Add to ace_core_ng_source_set**:
   Edit `frameworks/core/BUILD.gn` line 878:
   ```gn
   "components/text/text_theme.cpp",  # Add this line
   ```

4. **Rebuild**:
   ```bash
   ./build.sh --product-name rk3568 --build-target ace_engine --ccache
   ```

5. **Verify**:
   ```bash
   ./extract_last_error.sh out/rk3568/build.log
   cat last_error.log
   ```
   Should show: "build success, no error"

---

## Common Patterns

### Pattern 1: `undefined symbol` + `referred by`

→ **Cause**: .cpp not in build system or not exported
→ **Reference**: `examples/undefined-symbol-missing-cpp.md`

### Pattern 2: `incomplete type` + member access

→ **Cause**: Missing header include or forward declaration issue
→ **Solution**: Add proper header include

### Pattern 3: `redefinition of`

→ **Cause**: Duplicate definitions in .h and .cpp
→ **Solution**: Use inline constexpr in header only

### Pattern 4: Multiple undefined symbols from same module

→ **Cause**: Missing .cpp file entirely
→ **Solution**: Create .cpp and add to BUILD.gn files

---

## Tips for Best Results

1. **Always extract error first**: Use `extract_last_error.sh` before asking for analysis
2. **Provide context**: Mention which module you're working on (button, text, timepicker, etc.)
3. **Share what changed**: "I added a new .cpp file" or "I optimized headers"
4. **Include git status**: If you have uncommitted changes, the pattern might be clearer

---

## Testing the Skill

After applying fixes:

```bash
# 1. Rebuild
./build.sh --product-name rk3568 --build-target ace_engine --ccache

# 2. Extract new error (if any)
./extract_last_error.sh out/rk3568/build.log

# 3. Check result
cat last_error.log

# Expected: "build success, no error"
```

If still failing, share the new `last_error.log` content for further analysis.
