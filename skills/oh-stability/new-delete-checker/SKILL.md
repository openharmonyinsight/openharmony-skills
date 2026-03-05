---
name: new-delete-checker
description: Comprehensive new/delete memory management checking for ace_engine codebase. Covers 17 critical scenarios: basic pairing, smart pointers (RefPtr/WeakPtr), exception safety, ownership transfer, container pointers, singletons, callbacks, multi-threading, cross-layer interaction, third-party libraries, special patterns, common leaks, nullptr handling, Register/Unregister, lifecycle binding, assignment updates, and function returns. Use when checking memory leaks, verifying memory safety, or analyzing new/delete patterns in ace_engine.
---

# new/delete Memory Management Checker

Comprehensive memory management analysis for ace_engine codebase covering 17 critical scenarios.

## Quick Start

Run full analysis:
```bash
# Statistical analysis
bash scripts/stats.sh

# Pattern detection
bash scripts/detect_patterns.sh

# Generate report
python scripts/generate_report.py
```

## Core Scenarios

### 1. Basic Pairing
- `new`/`delete` pairing
- `new[]`/`delete[]` pairing
- Execution path coverage

### 2. Smart Pointers
- RefPtr usage patterns
- WeakPtr for cycles
- Raw/RefPtr mixing

### 3. Exception Safety
- Exception paths
- RAII patterns
- Try-catch coverage

### 4. Ownership Transfer
- Function returns
- Parameter passing
- Cross-module transfer

### 5. Container Pointers
- STL containers
- Cleanup logic
- Iterator safety

### 6. Singletons
- Singleton leaks
- Global pointers
- Static members

### 7. Callbacks
- EventHub callbacks
- Lambda captures
- Async cleanup

### 8. Multi-threading
- Cross-thread pointers
- Async tasks
- Thread-safe delete

### 9. Cross-layer
- Bridge layer
- FrameNode/UINode
- Pattern/RenderNode

### 10. Third-party
- Rosen pointers
- Skia pointers
- V8/ArkTS pointers

### 11. Special Patterns
- Factory pattern
- Builder pattern
- Observer pattern

### 12. Common Leaks
- Constructor/destructor
- Conditional branches
- Exception paths
- Loop issues

### 13. nullptr Handling
- `delete nullptr` safety
- Unnecessary checks
- `new(std::nothrow)`

### 14. Register/Unregister
- Registration pairing
- Exception safety
- Duplicate handling

### 15. Lifecycle Binding
- Parent/child cleanup
- Circular references
- FrameNode lifecycle

### 16. Assignment Updates
- Member assignment
- Exception safety
- Self-assignment

### 17. Function Returns
- Early returns
- Multiple paths
- CheckNull cleanup

## Detailed Guidance

### Statistical Analysis

See [STATISTICS.md](references/STATISTICS.md) for comprehensive metrics and interpretation.

### Pattern Detection

See [PATTERNS.md](references/PATTERNS.md) for detection rules and examples.

### Fix Recommendations

See [FIXES.md](references/FIXES.md) for code examples and best practices.

### Report Template

See [REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md) for report structure.

## Severity Levels

- **🔴 Critical**: Definite leaks, double delete, use-after-free
- **🟠 High**: Likely leaks, exception-unsafe, missing cleanup
- **🟡 Medium**: Potential leaks, unclear ownership, inconsistent patterns
- **🟢 Low**: Style issues, unnecessary checks, documentation gaps

## Tools

### Static Analysis
```bash
# clang-tidy
clang-tidy --checks=-*,clang-analyzer-* frameworks/**/*.cpp

# cppcheck
cppcheck --enable=all frameworks/

# Custom scripts
bash scripts/stats.sh
bash scripts/detect_patterns.sh
```

### Runtime Detection
```bash
# AddressSanitizer
ASAN_OPTIONS=detect_leaks=1 ./test_executable

# LeakSanitizer
LSAN_OPTIONS=suppressions=lsan.supp ./test_executable

# Valgrind
valgrind --leak-check=full ./test_executable
```

## Best Practices

### ✅ Always Do
- Use RefPtr/WeakPtr for ownership
- Use MakeRefPtr for creation
- Use CHECK_NULL_* macros
- Implement proper destructors
- Use RAII for resources
- Document ownership for returns
- Use WeakPtr to break cycles

### ❌ Never Do
- Delete RefPtr-managed pointers
- Forget to delete raw pointers
- Use delete instead of delete[]
- Mix raw/RefPtr without clear ownership
- Skip delete on exception paths
- Create RefPtr cycles
- Assume third-party ownership

### ⚠️ Be Careful
- Exception safety in new/delete pairs
- Ownership transfer across boundaries
- Callback memory management
- Cross-thread pointer sharing
- Container pointer cleanup
- Third-party library ownership
