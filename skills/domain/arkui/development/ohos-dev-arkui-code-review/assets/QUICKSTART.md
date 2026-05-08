# ArkUI Code Review - Quick Start

## Basic Usage

```
"Review path/to/file.cpp for memory management and threading issues"
"Check frameworks/core/components_ng/pattern/menu for architecture compliance"
"Review this PR focusing on security vulnerabilities"
```

## Focus by Dimension

```
"Review code for Memory issues"        -> Loads MEMORY.md for detailed checks
"Check Security dimension"             -> Loads SECURITY.md for vulnerability patterns
"Verify architecture compliance"       -> Loads ACE_ENGINE_SPECIFIC.md for layer rules
"Analyze code quality and design"      -> Loads CODE_SMELLS.md + SOLID.md
```

## Focus by Severity

```
"Find only CRITICAL issues"            -> Quick scan for blockers
"Focus on HIGH and CRITICAL severity"  -> Pre-merge quality gate
```

## Specific ACE Engine Checks

```
"Check RefPtr usage in this code"              -> MakeRefPtr, DynamicCast, WeakPtr
"Verify WeakClaim is used correctly"           -> Async callback safety
"Check for layer boundary violations"          -> Four-layer architecture
"Analyze naming convention compliance"         -> PascalCase, snake_case_
```

## Understanding Results

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Must fix before merge | Blocks merge |
| HIGH | Should fix before merge | Strongly recommended |
| MEDIUM | Fix soon | Track in backlog |
| LOW | Nice to have | Address when convenient |

## Iterative Review

```
1. "Find CRITICAL issues in this code"           -> Fix blockers first
2. "Verify that CRITICAL issues are resolved"    -> Confirm fixes
3. "Do a full review now"                        -> Comprehensive analysis
```
