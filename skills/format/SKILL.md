---
name: format
description: Run clang-format on the current git changes. Only keep the formatting fix on the changed lines.
---

## Tool Locations

- **clang-format**: `../../../prebuilts/clang/ohos/linux-x86_64/llvm/bin/clang-format`
- **clang-format-diff.py**: `../../../prebuilts/clang/ohos/linux-x86_64/llvm/share/clang/clang-format-diff.py`

## Approach

Use `clang-format-diff.py` which is designed specifically for this use case - it reads a diff from stdin and only applies formatting to lines that were changed.

### Working Command

```bash
# Navigate to repo root and run:
git diff HEAD -- 'graphic_2d/**/*.cpp' 'graphic_2d/**/*.h' 2>/dev/null | \
  python3 prebuilts/clang/ohos/linux-x86_64/llvm/share/clang/clang-format-diff.py \
  -p1 -binary prebuilts/clang/ohos/linux-x86_64/llvm/bin/clang-format -i
```

### Why This Works

1. **`git diff HEAD`** - Shows all unstaged changes relative to HEAD
2. **`-- 'graphic_2d/**/*.cpp' 'graphic_2d/**/*.h'`** - Filters to C++ source files
3. **`clang-format-diff.py`** - Reads the diff and only formats changed lines
4. **`-p1`** - Strips one path component (`graphic_2d/`) from diff paths
5. **`-binary ...`** - Specifies the clang-format executable to use
6. **`-i`** - Applies edits directly to files

### Important Notes

- **Must run from repo root of OpenHarmony** so file paths in the diff match actual file locations
- The tool only applies formatting if changed lines violate style rules
- If changed lines are already properly formatted, no changes are made
- This avoids the problem of formatting thousands of unchanged lines in a file