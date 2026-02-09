---
name: comprehensive-code-review
description: Comprehensive code review system for ACE Engine (OpenHarmony ArkUI framework) covering C++, JavaScript, TypeScript, and ArkTS codebases. Performs automated analysis across 19+ dimensions: stability, performance, threading, security, memory management, Modern/Effective C++ practices, code smells, SOLID principles, design patterns, robustness, testability, maintainability, observability, API design, technical debt, and backward compatibility. Generates detailed review reports with severity levels (CRITICAL/HIGH/MEDIUM/LOW), actionable refactoring recommendations with before/after examples, and ACE Engine project-specific checks including Pattern/Model/Property separation, component lifecycle methods (OnModifyDone, OnDirtyLayoutWrapperSwap), RefPtr usage (MakeRefPtr, DynamicCast), WeakPtr for breaking cycles, and four-layer architecture compliance. Use when: (1) Reviewing pull requests or code changes, (2) Analyzing existing codebases for quality issues, (3) Enforcing coding standards and best practices, (4) Identifying technical debt and refactoring opportunities, (5) Validating architectural compliance, (6) Generating code quality reports with metrics and recommendations.
---

# Comprehensive Code Review for ACE Engine

## Quick Start

Perform comprehensive code review analysis:

```bash
# Analyze C++ code
python scripts/analyze_code.py path/to/code.cpp --output results.json

# Analyze directory recursively
python scripts/analyze_code.py frameworks/core/components_ng --recursive --output analysis.json

# Generate review report
python scripts/generate_report.py --analysis analysis.json --output review_report.md

# Filter by severity
python scripts/analyze_code.py path/to/code --severity CRITICAL --output critical.json

# Filter by dimension
python scripts/analyze_code.py path/to/code --dimension Memory --output memory_issues.json
```

## Review Workflow

### Phase 1: Automated Analysis

Run language-specific analysis:

```bash
# C++ analysis
python scripts/analyze_code.py <path> --recursive --output results.json

# TypeScript/ArkTS analysis
python scripts/analyze_code.py <path> --recursive --output results.json

# Architecture compliance check
python scripts/analyze_code.py <directory> --recursive
```

### Phase 2: Dimension-Based Review

Review code across 19+ dimensions. See [DIMENSIONS.md](references/DIMENSIONS.md) for complete coverage.

**High-Priority Dimensions:**
- Security (CRITICAL) - Input validation, command injection, buffer overflows
- Memory (CRITICAL) - Smart pointers, leaks, ownership semantics
- Threading (HIGH) - Data races, deadlocks, callback safety
- Stability (HIGH) - Error handling, boundary conditions

**Medium-Priority Dimensions:**
- Performance - Algorithm complexity, optimization opportunities
- SOLID Principles - Single responsibility, Open/Closed, etc.
- Code Smells - Long methods, large classes, duplicate code
- Testability - Dependency injection, decoupling

### Phase 3: Report Generation

Generate comprehensive review report:

```bash
python scripts/generate_report.py --analysis results.json --output review_report.md
```

Report includes:
- **Executive Summary** - Issue counts by severity
- **Critical Issues** (🔴) - Must fix before merge
- **High Priority Issues** (🟠) - Should fix before merge
- **Medium Priority Issues** (🟡) - Fix soon
- **Low Priority Issues** (🟢) - Nice to have
- **Dimension Breakdown** - Issues grouped by category
- **File-by-File Details** - Specific line numbers and code snippets
- **Recommendations** - Prioritized action items
- **Review Checklist** - Pre-merge verification

## Dimension Reference

Quick reference to all dimensions:

| Dimension | Focus | Severity Levels | Reference |
|-----------|-------|-----------------|-----------|
| **Stability** | Error handling, boundaries | 🔴🟠🟡🟢 | [STABILITY.md](references/STABILITY.md) |
| **Performance** | Algorithms, optimization | 🔴🟠🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Threading** | Concurrency, synchronization | 🔴🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Security** | Input validation, vulnerabilities | 🔴🟠🟡 | [SECURITY.md](references/SECURITY.md) |
| **Memory** | Smart pointers, leaks | 🔴🟠🟡 | [MEMORY.md](references/MEMORY.md) |
| **Modern C++** | C++11/14/17/20 features | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Effective C++** | RAII, Rule of Five | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Code Smells** | 22 types of smells | 🟠🟡 | [CODE_SMELLS.md](references/CODE_SMELLS.md) |
| **SOLID** | Design principles | 🟠🟡 | [SOLID.md](references/SOLID.md) |
| **Design Patterns** | Pattern usage | 🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Robustness** | Fault tolerance | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Testability** | Dependency injection | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Maintainability** | Code complexity | 🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Observability** | Logging, monitoring | 🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **API Design** | Interface quality | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Technical Debt** | TODO/FIXME tracking | 🟡🟢 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Backward Compatibility** | API stability | 🟠🟡 | [DIMENSIONS.md](references/DIMENSIONS.md) |
| **Architecture** | ACE Engine compliance | 🔴🟠🟡 | [ACE_ENGINE_SPECIFIC.md](references/ACE_ENGINE_SPECIFIC.md) |

## ACE Engine Specific Checks

### Architecture Validation

**Four-Layer Architecture:**
```
Frontend Bridge Layer
    ↓
Component Framework Layer (Pattern/Model/Property)
    ↓
Layout/Render Layer
    ↓
Platform Adapter Layer (OHOS/Preview)
```

**Check:**
- No violations of layer boundaries
- Proper use of Pattern/Model/Property separation
- No direct platform calls from framework layer

### Component Structure

```
components_ng/pattern/<component>/
├── *_pattern.h/cpp         # Business logic & lifecycle
├── *_model.h/cpp           # Data model interface
├── *_layout_property.h/cpp # Layout properties
├── *_paint_property.h/cpp  # Render properties
└── *_event_hub.h/cpp       # Event handling
```

### RefPtr Usage

```cpp
// ✅ Creation
auto node = AceType::MakeRefPtr<FrameNode>();

// ✅ Type-safe casting
auto pattern = AceType::DynamicCast<MenuPattern>(node->GetPattern());
if (!pattern) {
    LOGE("Failed to get pattern");
    return false;
}

// ✅ Breaking cycles with WeakPtr
class Child {
    WeakPtr<Parent> parent_;  // Use weak, not strong
};

// ✅ Safe callbacks
auto weak = AceType::WeakClaim(this);
PostTask([weak]() {
    auto pattern = AceType::DynamicCast<MenuPattern>(weak.Upgrade());
    if (pattern) pattern->Update();
});
```

### Naming Conventions

```cpp
class MenuPattern {           // PascalCase
public:
    void OnModifyDone();      // PascalCase
    int GetWidth() const;     // Get prefix

private:
    int width_;               // snake_case_ with trailing underscore
    std::string component_id_;  // Abbreviations lowercase
};

constexpr int MAX_MENU_ITEMS = 100;  // UPPER_CASE
```

## Severity Levels

**🔴 CRITICAL** - Must fix before merge
- Security vulnerabilities (command injection, buffer overflow)
- Memory leaks in long-running processes
- Use-after-free, double-free
- Data races
- Crashes / undefined behavior
- Architecture violations

**🟠 HIGH** - Should fix before merge
- Performance degradation
- API violations
- SOLID principle violations
- Major code smells (Large Class, Shotgun Surgery)
- Improper RefPtr usage
- Unsafe callback captures

**🟡 MEDIUM** - Fix soon
- Minor performance issues
- Code smells (Long Method, Duplicate Code)
- Style violations
- Missing error handling in non-critical paths

**🟢 LOW** - Nice to have
- Missing comments
- Minor style issues
- Optimization opportunities
- Code documentation improvements

## Common Issue Patterns

| Pattern | Dimension | Severity | Detection |
|---------|-----------|----------|-----------|
| Raw pointer instead of RefPtr | Memory | HIGH | `new T()` without RefPtr |
| Command injection | Security | CRITICAL | `system(user_input)` |
| Buffer overflow | Security | CRITICAL | `strcpy()`, `sprintf()` |
| Unsafe this capture | Threading | HIGH | `[this]` in PostTask |
| Long method (>50 lines) | Code Smell | MEDIUM | Function length |
| Large class (>500 lines) | Code Smell | HIGH | Class size |
| Missing null check | Stability | HIGH | Pointer use without validation |
| static_cast instead of DynamicCast | Memory | MEDIUM | `static_cast<T*>` |

## Usage Examples

### Review a Pull Request

```bash
# Analyze PR code
python scripts/analyze_code.py path/to/pr/code --recursive --output pr_analysis.json

# Generate PR review report
python scripts/generate_report.py --analysis pr_analysis.json --output pr_review.md

# Check for critical issues
cat pr_review.md | grep -A 10 "CRITICAL"
```

### Security Audit

```bash
# Security-focused review
python scripts/analyze_code.py . --dimension Security --recursive --output security_audit.json
python scripts/generate_report.py --analysis security_audit.json --output security_report.md
```

### Memory Leak Detection

```bash
# Find memory issues
python scripts/analyze_code.py . --dimension Memory --recursive --output memory_check.json

# View memory issues
cat memory_check.json | jq '.[].issues[] | select(.dimension == "Memory")'
```

### Architecture Compliance Check

```bash
# Validate architecture
python scripts/analyze_code.py frameworks/core --recursive --output framework_analysis.json

# Look for architecture violations
cat framework_analysis.json | jq '.[].issues[] | select(.dimension == "Architecture")'
```

## Integration Examples

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(cpp|cc|cxx|h|hpp|ts|tsx)$')

if [ -n "$CHANGED_FILES" ]; then
    echo "Running code review..."
    python scripts/analyze_code.py $CHANGED_FILES --output commit_review.json

    CRITICAL_COUNT=$(grep -o '"severity": "CRITICAL"' commit_review.json | wc -l)

    if [ $CRITICAL_COUNT -gt 0 ]; then
        echo "❌ Found $CRITICAL_COUNT CRITICAL issues. Please fix before committing."
        exit 1
    fi
fi
```

### CI/CD Pipeline

```yaml
code_review:
  stage: test
  script:
    - python scripts/analyze_code.py frameworks/core --recursive --output review_results.json
    - python scripts/generate_report.py --analysis review_results.json --output review_report.md
    - |
      if grep -q '"severity": "CRITICAL"' review_results.json; then
        echo "CRITICAL issues found!"
        exit 1
      fi
  artifacts:
    paths:
      - review_results.json
      - review_report.md
```

## Scripts

**analyze_code.py** - Automated static analysis
- Detects raw pointers, unsafe casts
- Finds security vulnerabilities
- Checks RefPtr usage
- Validates naming conventions
- Supports C++ and TypeScript/ArkTS

**generate_report.py** - Report generation
- Executive summary
- Issues grouped by severity
- Dimension breakdown
- File-by-file details
- Recommendations and checklist

## References

Detailed documentation for all dimensions in `references/`:
- [DIMENSIONS.md](references/DIMENSIONS.md) - Quick reference for all 19+ dimensions
- [STABILITY.md](references/STABILITY.md) - Error handling, boundary conditions
- [MEMORY.md](references/MEMORY.md) - Smart pointers, leaks, ownership
- [SECURITY.md](references/SECURITY.md) - Input validation, vulnerabilities
- [CODE_SMELLS.md](references/CODE_SMELLS.md) - 22 types of code smells
- [SOLID.md](references/SOLID.md) - Five design principles
- [ACE_ENGINE_SPECIFIC.md](references/ACE_ENGINE_SPECIFIC.md) - Project-specific rules

## Assets

- [report_template.md](assets/report_template.md) - Customizable report template
- [QUICKSTART.md](assets/QUICKSTART.md) - Detailed usage guide with examples

## Review Checklist

Before merging code:

**Code Quality:**
- [ ] No CRITICAL issues
- [ ] HIGH priority issues addressed or documented
- [ ] No compiler warnings
- [ ] Static analysis clean

**Architecture:**
- [ ] Four-layer architecture respected
- [ ] Proper Pattern/Model/Property separation
- [ ] No layer boundary violations

**Memory:**
- [ ] No memory leaks
- [ ] RefPtr used correctly
- [ ] WeakPtr used to break cycles
- [ ] Callbacks use WeakClaim

**Security:**
- [ ] All input validated
- [ ] No command injection
- [ ] No buffer overflows
- [ ] Sensitive data protected

**Testing:**
- [ ] Unit tests added
- [ ] Edge cases covered
- [ ] Error scenarios tested
