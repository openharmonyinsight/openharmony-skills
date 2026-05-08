# Code Review Dimensions - Quick Reference

This file provides a quick lookup for dimensions not covered by dedicated reference files.
For Memory, Security, Stability, Code Smells, SOLID, and ACE Engine specifics, use the dedicated files.

---

## Dimension Severity Guide

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Must fix before merge | Blocks merge |
| HIGH | Should fix before merge | Strongly recommended |
| MEDIUM | Fix soon | Track in backlog |
| LOW | Nice to have | Address when convenient |

---

## 1. Performance

**Focus:** Algorithm complexity, optimization, efficiency

| Issue | Severity | Detection |
|-------|----------|-----------|
| O(n^2) where O(n) possible with large n | CRITICAL | Nested loops on containers |
| Blocking UI thread | HIGH | Synchronous I/O or heavy computation in main thread |
| Unnecessary copies | HIGH | Pass-by-value for large objects; missing `std::move` |
| Missing caching | HIGH | Repeated expensive calculations without cache |
| Inefficient data structure | HIGH | `std::vector` for frequent lookup; should be `std::unordered_set/map` |

**Decision framework:**
- Layout/render/event dispatch paths are hot paths; any allocation or O(n^2) here is HIGH
- One-time initialization paths can tolerate lower efficiency
- When in doubt, measure before optimizing

---

## 2. Threading

**Focus:** Data races, deadlock prevention, synchronization

| Issue | Severity | Detection |
|-------|----------|-----------|
| Unprotected shared mutable state | CRITICAL | Non-atomic variable accessed from multiple threads without lock |
| Data races | CRITICAL | Concurrent read+write or write+write without synchronization |
| Deadlocks | CRITICAL | Inconsistent lock ordering across code paths |
| Unsafe callback captures | HIGH | `[this]` in PostTask/async without WeakClaim |
| Missing synchronization | HIGH | Shared resource accessed without mutex/atomic |

**ACE Engine specific rule:** Always use `WeakClaim(this)` + `Upgrade()` check for PostTask callbacks. See `ACE_ENGINE_SPECIFIC.md` for details.

---

## 3. Modern C++

**Focus:** C++11/14/17/20 idiomatic usage

| Issue | Severity | Detection |
|-------|----------|-----------|
| Raw pointers instead of smart pointers | HIGH | `T*` owning memory without RAII wrapper |
| Missing move semantics | HIGH | Expensive copies where move is possible |
| Not using `constexpr` for compile-time constants | MEDIUM | `const` for values known at compile time |
| `NULL` instead of `nullptr` | MEDIUM | Legacy null pointer usage |
| Not using `auto` where appropriate | MEDIUM | Redundant type spelling (iterators, lambdas) |
| Not using range-based for | MEDIUM | Index-based iteration over containers |
| Not using `std::optional` | MEDIUM | Using sentinel values or raw pointers for "no value" |

---

## 4. Effective C++

**Focus:** RAII, Rule of Five, resource management idioms

| Issue | Severity | Detection |
|-------|----------|-----------|
| Violating RAII | HIGH | Resource acquisition not tied to object lifetime |
| Rule of Three/Five violations | HIGH | Custom destructor without copy/move operations or vice versa |
| Resource leaks | HIGH | Missing cleanup in error paths |
| Incorrect virtual destructors | MEDIUM | Base class with virtual methods but non-virtual destructor |
| Returning references to temporaries | MEDIUM | `return local_var;` as reference |

---

## 5. Robustness

**Focus:** Fault tolerance, graceful degradation

| Issue | Severity | Detection |
|-------|----------|-----------|
| No error handling | HIGH | Ignoring return values, empty catch blocks |
| Crashes on invalid input | HIGH | No input validation on external data |
| No resource exhaustion handling | HIGH | Unbounded allocations, no size limits |
| No graceful degradation | MEDIUM | All-or-nothing behavior without fallback |

---

## 6. Testability

**Focus:** Dependency injection, decoupling

| Issue | Severity | Detection |
|-------|----------|-----------|
| Hard-coded dependencies | HIGH | Direct construction of concrete types (e.g., `Database::GetInstance()`) |
| Tightly coupled code | HIGH | Direct access to internal state of other classes |
| Global state | MEDIUM | Static mutable variables, singletons |
| Static method dependencies | MEDIUM | Static calls that cannot be intercepted for testing |

---

## 7. Maintainability

**Focus:** Code complexity, readability

| Issue | Severity | Detection |
|-------|----------|-----------|
| Cyclomatic complexity > 10 | MEDIUM | Deep nesting, many branches in single function |
| Deep nesting > 3 levels | MEDIUM | Nested if/for/while blocks |
| Poor naming | MEDIUM | Single-letter variables, abbreviations without context |
| Magic numbers | MEDIUM | Unnamed numeric literals |

---

## 8. Observability

**Focus:** Logging, monitoring, debugging

| Issue | Severity | Detection |
|-------|----------|-----------|
| Missing critical logs | MEDIUM | Entry/exit of important functions not logged |
| Insufficient error context | MEDIUM | Error log without relevant state variables |
| No performance monitoring | MEDIUM | Hot paths without timing instrumentation |
| Wrong log level | MEDIUM | `LOGE` for expected conditions; `LOGI` for errors |

**ACE Engine log format:** `LOGI("Component::Method called, id=%{public}d", id_);`
Use `%{private}s` for sensitive data, `%{public}s` for safe values.

---

## 9. API Design

**Focus:** Consistency, clarity, usability

| Issue | Severity | Detection |
|-------|----------|-----------|
| Inconsistent naming | MEDIUM | `GetWidth()` vs `width()` in same codebase |
| Unexpected side effects | HIGH | `Clear()` also resets unrelated state |
| Missing overloads | MEDIUM | Only one way to call when common variations exist |
| Too many parameters (>4) | MEDIUM | Should use parameter object/struct |

---

## 10. Technical Debt

**Focus:** TODO/FIXME management, debt tracking

| Issue | Severity | Detection |
|-------|----------|-----------|
| Untracked TODOs | MEDIUM | `// TODO` without issue reference |
| Outdated TODOs | MEDIUM | `// TODO` for already-resolved issues |
| FIXME without context | MEDIUM | `// FIXME` without explanation of what's broken |

**Recommended format:** `// TODO(issue:12345): Description of what needs to be done`

---

## 11. Backward Compatibility

**Focus:** API stability, deprecation

| Issue | Severity | Detection |
|-------|----------|-----------|
| Breaking changes without deprecation | HIGH | Removing or renaming public API without migration path |
| Changing API behavior | HIGH | Same method signature but different semantics |
| Missing version tags | MEDIUM | New API without since-version annotation |

---

## Dimension-to-Reference Mapping

| Dimension | Dedicated Reference File |
|-----------|------------------------|
| Memory | `MEMORY.md` |
| Security | `SECURITY.md` |
| Stability | `STABILITY.md` |
| Code Smells | `CODE_SMELLS.md` |
| SOLID Principles | `SOLID.md` |
| Architecture | `ACE_ENGINE_SPECIFIC.md` |
| Performance, Threading, Modern C++, Effective C++, Robustness, Testability, Maintainability, Observability, API Design, Technical Debt, Backward Compatibility | This file |

---

## Common Issue Patterns Quick Table

| Pattern | Dimension | Severity | Fix |
|---------|-----------|----------|-----|
| Raw pointer instead of RefPtr | Memory | HIGH | Use `MakeRefPtr` |
| No input validation | Security | CRITICAL | Add whitelist validation |
| Nested loops on large containers | Performance | HIGH | Use hash-based lookup |
| Method > 50 lines | Code Smell | MEDIUM | Extract smaller methods |
| No error handling | Stability | HIGH | Check returns, add error paths |
| Hard-coded dependency | Testability | HIGH | Dependency injection |
| Missing logging | Observability | MEDIUM | Add contextual logs |
| Circular RefPtr reference | Memory | CRITICAL | Use `WeakPtr` in back-reference |
| `static_cast` on RefPtr | Memory | HIGH | Use `DynamicCast` + null check |
| `[this]` in PostTask | Threading | HIGH | Use `WeakClaim(this)` |
