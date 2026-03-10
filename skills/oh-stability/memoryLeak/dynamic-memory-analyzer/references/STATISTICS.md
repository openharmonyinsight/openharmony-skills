# Statistical Analysis Metrics

## Core Metrics

| Metric | Command | Interpretation |
|--------|---------|---------------|
| `new` operations | `grep -rn "new " frameworks/ --include="*.cpp" \| wc -l` | Total heap allocations |
| `delete` operations | `grep -rn "delete " frameworks/ --include="*.cpp" \| wc -l` | Total deallocations |
| `new[]` arrays | `grep -rn "new \[" frameworks/ --include="*.cpp" \| wc -l` | Array allocations |
| `delete[]` arrays | `grep -rn "delete\[\]" frameworks/ --include="*.cpp" \| wc -l` | Array deallocations |
| `RefPtr` usage | `grep -rn "RefPtr" frameworks/ --include="*.cpp" \| wc -l` | Smart pointer usage |
| `WeakPtr` usage | `grep -rn "WeakPtr" frameworks/ --include="*.cpp" \| wc -l` | Weak reference usage |
| `MakeRefPtr` calls | `grep -rn "MakeRefPtr" frameworks/ --include="*.cpp" \| wc -l` | Smart pointer creation |
| `CHECK_NULL_*` macros | `grep -rn "CHECK_NULL_VOID\|CHECK_NULL_RETURN" frameworks/ --include="*.cpp" \| wc -l` | Null check macros |
| `Register/Unregister` | `grep -rn "Register\|Unregister" frameworks/ --include="*.cpp" \| wc -l` | Registration patterns |
| `AddChild/RemoveChild` | `grep -rn "AddChild\|RemoveChild" frameworks/ --include="*.cpp" \| wc -l` | Node management |

## Analysis Guidelines

### new/delete Ratio
- **Ideal**: 1:1 (balanced)
- **Warning**: delete < new * 0.8 (potential leaks)
- **Critical**: delete < new * 0.5 (high leak risk)

### Array Operations
- **Check**: new[] count vs delete[] count
- **Mismatch**: Indicates wrong delete type used

### Smart Pointer Ratio
- **High RefPtr usage**: Good (automatic memory management)
- **Low RefPtr usage**: Review manual memory management

### Macro Usage
- **High CHECK_NULL_* usage**: Good (consistent null checking)
- **Low CHECK_NULL_* usage**: Review null safety

## ace_engine Baseline

Based on comprehensive analysis (2026-02-26):

| Metric | Count | Status |
|--------|-------|--------|
| `new` | 1160 | ✅ |
| `delete` | 283 | ⚠️ (low) |
| `new[]` | 1 | ✅ |
| `delete[]` | 71 | ✅ |
| `RefPtr` | 9781 | ✅ (high) |
| `WeakPtr` | 4633 | ✅ (high) |
| `MakeRefPtr` | 7222 | ✅ (high) |
| `CHECK_NULL_*` | 73711 | ✅ (high) |
| `Register/Unregister` | 4872 | ✅ |
| `AddChild/RemoveChild` | 1284 | ✅ |

**Note**: Low delete count is expected due to high smart pointer usage (9781 RefPtr members).
