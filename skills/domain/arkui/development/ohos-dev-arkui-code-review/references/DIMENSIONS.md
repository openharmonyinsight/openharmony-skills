# Code Review Dimensions — ACE Engine Focus

Quick lookup for dimensions not covered by dedicated reference files.
For Memory, Security, Stability, Code Smells, SOLID, and Architecture, use dedicated files.

---

## Performance

**ACE Engine hot paths:** `Measure()`/`Layout()` in LayoutAlgorithm, `OnModifyDone()` in Pattern, event dispatch. Any heap allocation or O(n^2) in these paths is HIGH severity.

| Issue | Severity | Detection |
|-------|----------|-----------|
| O(n^2) in layout/render/event paths | CRITICAL | Nested loops on containers in Measure/Layout/OnModifyDone |
| Blocking UI thread | HIGH | Synchronous I/O or heavy computation in main thread task |
| Unnecessary copies of large objects | HIGH | Pass-by-value for RefPtr, Dimension, std::string; missing `std::move` |
| `MarkDirtyNode(PROPERTY_UPDATE_MEASURE)` without value comparison | HIGH | Triggers full relayout even when nothing changed |
| Missing cache for expensive lookups | HIGH | Repeated theme/style lookups in hot paths |

**Decision framework:**
- Layout/render/event dispatch → any allocation or O(n^2) is HIGH
- One-time initialization paths → can tolerate lower efficiency
- When in doubt, measure before optimizing

---

## Threading

ACE Engine has a UI thread and potentially a render thread. The key rule: `WeakClaim(this)` + `Upgrade()` for all async callbacks.

| Issue | Severity | Detection |
|-------|----------|-----------|
| Shared mutable state across UI + render threads without lock | CRITICAL | Non-atomic variable accessed from PostTask and main thread |
| Data races | CRITICAL | Concurrent read+write without synchronization |
| `[this]` in PostTask without WeakClaim | HIGH | Lambda capturing raw this in PostTask/PostDelayedTask |
| Missing mutex for shared resource | HIGH | Container or counter accessed from multiple threads |

---

## Modern C++ / Effective C++

Flag these in ACE Engine code:

| Issue | Severity |
|-------|----------|
| Raw owning pointers instead of RefPtr/unique_ptr | HIGH |
| Missing `std::move` for expensive types | MEDIUM |
| `NULL` instead of `nullptr` | MEDIUM |
| `const` instead of `constexpr` for compile-time values | LOW |
| Missing `auto` where it improves readability (iterators, lambdas) | LOW |

---

## Testability

| Issue | Severity | Detection |
|-------|----------|-----------|
| Pattern calling `SubwindowManager::GetInstance()` directly | HIGH | Tight coupling to singleton — can't test without mocking entire platform |
| Hard-coded dependencies in Pattern | HIGH | Direct construction of concrete types instead of using Pipeline context |
| Static mutable variables in component code | MEDIUM | Prevents parallel test execution |

**ACE Engine test patterns:**
- `MockPipelineContext::SetUp()` / `MockContainer::SetUp()` for dependency injection
- `FrameNode::GetOrCreateFrameNode(tag, id, factory_lambda)` enables test injection
- Theme dependencies injected via `MockThemeManager` + `EXPECT_CALL`
- Components should not call platform singletons directly — prefer virtual methods or inject via Pipeline context

---

## Observability

| Issue | Severity | Detection |
|-------|----------|-----------|
| Missing logs in error paths | MEDIUM | `return false;` or `CHECK_NULL_VOID` without LOGE |
| Wrong log level | MEDIUM | `LOGE` for expected conditions; `LOGI` for errors |
| Sensitive data in `LOGE`/`LOGI` with `%{public}s` | HIGH | Passwords, tokens, user data logged publicly |

**ACE Engine log format:** `LOGI("Component::Method called, id=%{public}d", id_);`
Use `%{private}s` for sensitive data, `%{public}s` for safe values only.

---

## API Design

| Issue | Severity | Detection |
|-------|----------|-----------|
| Inconsistent naming (mixing `SetXxx` and `updateXxx`) | MEDIUM | Model API follows `SetXxx()` / `GetXxx()` pattern |
| Public methods on Pattern that should be on EventHub or Model | HIGH | Event handlers in Pattern instead of EventHub subclass |
| Too many parameters (>4) without parameter struct | MEDIUM | Should use LayoutProperty or dedicated config struct |

---

## Maintainability / Technical Debt / Backward Compatibility

| Issue | Severity |
|-------|----------|
| Cyclomatic complexity >10 in Pattern method | MEDIUM |
| Deep nesting >3 levels | MEDIUM |
| `// TODO` without issue reference | LOW |
| Breaking public API change without deprecation path | HIGH |
| Same method signature but different semantics | HIGH |

---

## Dimension-to-Reference Mapping

| Dimension | Dedicated Reference File |
|-----------|------------------------|
| Memory | `MEMORY.md` |
| Security | `SECURITY.md` |
| Stability | `STABILITY.md` |
| Code Smells | `CODE_SMELLS.md` |
| SOLID Principles | `SOLID.md` |
| Architecture | `ACE_ARCHITECTURE.md`, `ACE_LIFECYCLE.md`, `ACE_TESTING.md` |
| Performance, Threading, Modern C++, Testability, Observability, API Design, Maintainability, Technical Debt, Backward Compatibility | This file |
