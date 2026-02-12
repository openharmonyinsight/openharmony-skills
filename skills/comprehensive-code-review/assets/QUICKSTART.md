# Comprehensive Code Review - Quick Start Guide

## About This Skill

This skill provides AI-powered code review for ACE Engine (OpenHarmony ArkUI framework), analyzing C++, JavaScript, TypeScript, and ArkTS codebases across 19+ dimensions including stability, performance, security, memory management, and more.

## Basic Usage

### Review a Single File

```
"Review path/to/file.cpp for memory management and threading issues"
```

AI will:
- Read and analyze the file
- Check for common issues based on reference standards
- Provide detailed feedback with line numbers and suggestions

### Review a Directory

```
"Review frameworks/core/components_ng/pattern/menu for ACE Engine architecture compliance"
```

AI will:
- Analyze all relevant files in the directory
- Check architecture patterns (Pattern/Model/Property separation)
- Verify naming conventions and lifecycle methods
- Report issues with severity levels

### Review a Pull Request

```
"Review this PR focusing on security vulnerabilities and memory management"
```

AI will:
- Analyze changed files
- Identify security risks
- Check memory management patterns
- Provide prioritized action items

## Focus Areas

### By Dimension

```
"Review code for Memory issues"
"Check Security dimension"
"Analyze Stability issues"
"Review Threading safety"
"Check Performance patterns"
```

### By Severity

```
"Find only CRITICAL issues in the code"
"Focus on HIGH and CRITICAL severity issues"
```

### Specific Checks

```
"Check RefPtr usage in this code"
"Verify WeakClaim is used correctly in callbacks"
"Check for command injection vulnerabilities"
"Analyze naming convention compliance"
```

## Understanding AI Review Results

### Severity Levels

- **🔴 CRITICAL** - Must fix before merge
  - Security vulnerabilities
  - Memory leaks
  - Use-after-free, data races
  - Architecture violations

- **🟠 HIGH** - Should fix before merge
  - Performance issues
  - API violations
  - Improper RefPtr usage
  - Unsafe callback captures

- **🟡 MEDIUM** - Fix soon
  - Code smells
  - Style violations
  - Missing error handling

- **🟢 LOW** - Nice to have
  - Minor optimizations
  - Documentation improvements

### Dimension Categories

1. **Stability** - Error handling, boundary conditions
2. **Performance** - Algorithm complexity, optimization
3. **Threading** - Data races, synchronization
4. **Security** - Input validation, vulnerabilities
5. **Memory** - Smart pointers, leaks, ownership
6. **Modern C++** - C++11/14/17/20 features
7. **Code Smell** - Design issues (22 types)
8. **SOLID** - Design principles
9. **Architecture** - ACE Engine compliance

## Common Workflows

### Before Creating a PR

```
"Review these files before I submit my PR: [list files]"
```

### Architecture Review

```
"Verify that components_ng/menu follows ACE Engine four-layer architecture"
```

AI will check:
- Pattern/Model/Property separation
- No layer boundary violations
- Proper lifecycle methods
- Component structure compliance

### Security Audit

```
"Perform a security audit of this code, focus on input validation"
```

AI will check:
- Command injection risks
- Buffer overflow vulnerabilities
- Unvalidated user input
- Unsafe function usage

### Memory Review

```
"Analyze this code for memory leaks and improper smart pointer usage"
```

AI will check:
- Raw new/delete usage
- RefPtr vs raw pointers
- WeakPtr for breaking cycles
- DynamicCast with null checks

## Examples

### Example 1: Component Review

```
"Review frameworks/core/components_ng/pattern/menu for:
1. Memory management (RefPtr usage)
2. Threading safety (WeakClaim in callbacks)
3. ACE Engine architecture compliance"
```

### Example 2: PR Review

```
"Review this pull request:
[PR description or diff]

Focus on:
- Security issues
- Memory leaks
- Architecture violations
- CRITICAL and HIGH severity only"
```

### Example 3: Specific Issue Check

```
"Check this code for:
1. Raw pointer usage (should use RefPtr)
2. Static casts (should use DynamicCast)
3. Console.log statements (should use HiLog)
4. Empty catch blocks"
```

## Getting the Best Results

### 1. Be Specific About Scope

```
Good: "Review memory management in menu_pattern.cpp"
Better: "Review menu_pattern.cpp focusing on RefPtr usage and potential circular references"
```

### 2. Specify Severity Priority

```
"Review for CRITICAL and HIGH issues only" - Faster review, focuses on blockers
```

### 3. Reference Specific Dimensions

```
"Review for Security and Memory dimensions" - More targeted analysis
```

### 4. Provide Context

```
"Review this new component I'm adding. It handles user input and needs to be thread-safe."
```

## Tips and Best Practices

### 1. Iterative Review

```
# First pass: Critical issues
"Find CRITICAL issues in this code"

# After fixes: Verify
"Verify that the CRITICAL issues are resolved"

# Final: Comprehensive
"Do a full review now that critical issues are fixed"
```

### 2. Combined Reviews

```
"Review this code for:
- Memory management
- Security vulnerabilities
- Architecture compliance

Focus on CRITICAL and HIGH severity issues."
```

### 3. Learning from Reviews

Ask AI to explain:
```
"Explain why using raw pointers is problematic in ACE Engine"
"Show me an example of proper WeakClaim usage in async callbacks"
```

## Reference Documentation

For detailed information on each dimension, see:
- `references/STABILITY.md` - Error handling, boundary conditions
- `references/MEMORY.md` - Smart pointers, leaks, ownership
- `references/SECURITY.md` - Input validation, vulnerabilities
- `references/CODE_SMELLS.md` - 22 types of code smells
- `references/SOLID.md` - Five design principles
- `references/ACE_ENGINE_SPECIFIC.md` - Project-specific rules
- `references/DIMENSIONS.md` - Quick reference for all 19+ dimensions

## Traditional Tools Integration

For CI/CD automation, consider combining AI review with traditional tools:

```bash
# Pre-commit: Use clang-tidy, cppcheck, eslint
# AI review: For comprehensive analysis and design feedback
```

---

For more information, see the main [SKILL.md](../SKILL.md) file.
