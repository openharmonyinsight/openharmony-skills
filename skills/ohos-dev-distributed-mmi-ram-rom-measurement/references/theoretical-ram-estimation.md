# Theoretical RAM Estimation

Use this reference for the third RAM/ROM measurement pillar: code-level heap and runtime-state analysis.

## Discover New Data Structures

```bash
git diff <baseline>..HEAD -- '*.h' | grep -E '^\+\s+(std::(map|unordered_map|vector|set))'
git diff <baseline>..HEAD -- '*.h' | grep -E '^\+.*struct |^\+.*class '
```

For each new structure, record:

| Dimension | Check |
| --- | --- |
| New container member | `std::map`, `std::unordered_map`, `std::vector`, `std::set`, cache objects |
| Per-entry size | Value type fields plus container node/control overhead |
| Allocation timing | Eager allocation or lazy allocation on first feature use |
| Cardinality bound | Devices, windows, display groups, sessions, listeners, or event sequences |
| Cleanup path | `erase`, `clear`, remove callback, disconnect, service restart |
| Leak risk | Whether every allocation path has a matching release path |

## Size Hints

| Type | Approximate overhead | Notes |
| --- | ---: | --- |
| `Parcelable` to `RefBase` | ~80 B | vtable plus RefCounter heap allocation |
| `InputEvent` base | ~120 B | Parcelable plus common event fields |
| `shared_ptr` control block | ~16 B | Reference counts and deleter |
| `std::string` short value | ~32 B | SSO inline storage for short strings |
| `std::map<K,V>` empty object | ~48 B | Node adds roughly 48 B plus key/value |
| `std::unordered_map<K,V>` empty object | ~56 B | Node plus bucket array behavior |
| `std::vector<T>` empty object | ~24 B | Elements are contiguous and amortized |
| `std::set<T>` node | ~48 B + T | Tree node overhead |
| `std::list<T>` node | ~24 B + T | Link node overhead |

## Render Service Resources

If a change creates RS resources, estimate them separately. They can dominate ordinary C++ object cost.

| RS resource | Approximate memory |
| --- | ---: |
| `RSSurfaceNode` plus 64x64 RGBA triple buffer | ~48 KB |
| `RSSurfaceNode` plus 128x128 RGBA triple buffer | ~192 KB |
| `RSCanvasNode` plus `RSUIDirector` and `RSUIContext` | ~1.6 KB |

If the current implementation keeps the RS `shared_ptr` as `nullptr`, report both current and complete-implementation scenarios.

## Cross-Check

Compare theoretical estimates with measured libmmi PSS, native heap, and `Pss_Anon`:

- Theory much lower than measured delta: look for missed RS resources, third-party objects, or newly loaded libraries.
- Theory much higher than measured delta: check whether lazy allocation was actually triggered.
- Same order of magnitude: mark the estimate as consistent, not exact.
