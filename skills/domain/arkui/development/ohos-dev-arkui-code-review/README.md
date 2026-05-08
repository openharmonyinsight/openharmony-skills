# ArkUI Code Review Skill

Code review skill for OpenHarmony ArkUI (ACE Engine) projects, covering C++, TypeScript, and ArkTS codebases.

## Purpose

Provides structured code review focused on ACE Engine-specific rules: RefPtr/WeakPtr conventions, four-layer architecture compliance, component lifecycle patterns, and high-risk pattern detection. Covers 19+ review dimensions with severity-tagged findings.

## Structure

```
arkui-code-review/
├── SKILL.md                          # Main skill document (start here)
├── README.md                         # This file
├── references/
│   ├── ACE_ENGINE_SPECIFIC.md        # Architecture rules, component patterns, lifecycle, naming
│   ├── DIMENSIONS.md                 # Quick reference for all 19+ dimensions
│   ├── MEMORY.md                     # Smart pointer usage, ownership, leak detection
│   ├── SECURITY.md                   # Vulnerability patterns, input validation, sensitive data
│   ├── STABILITY.md                  # Error handling, boundary conditions, state validation
│   ├── CODE_SMELLS.md                # 22 types of code smells with refactoring guidance
│   └── SOLID.md                      # Five design principles with ACE Engine examples
└── assets/
    ├── report_template.md            # Formal review report template
    └── QUICKSTART.md                 # Usage examples and workflows
```

## Reference Files

Each reference file is loaded on demand based on review scope. SKILL.md specifies when to read each file.

| File | Content | When to Read |
|------|---------|-------------|
| `ACE_ENGINE_SPECIFIC.md` | Architecture, component structure, lifecycle, naming | Reviewing `components_ng/`, `bridge/`, `adapter/` code |
| `MEMORY.md` | RefPtr, WeakPtr, ownership, leaks | Found memory issues or suspect improper smart pointer usage |
| `SECURITY.md` | Injection, overflow, input validation, sensitive data | Code handles external input or credentials |
| `STABILITY.md` | Error handling, boundaries, null safety | Found unchecked returns or missing error paths |
| `CODE_SMELLS.md` | 22 smell types with detection and refactoring | Comprehensive design quality review |
| `SOLID.md` | SRP, OCP, LSP, ISP, DIP with examples | Reviewing class design or inheritance |
| `DIMENSIONS.md` | Performance, threading, modern C++, and 8 more dimensions | Quick lookup for dimensions without dedicated files |
| `report_template.md` | Full report template | Generating formal review reports |
