---
name: ohos-dev-arkui-code-review
description: >
  Use when reviewing or analyzing C++, TypeScript, or ArkTS code in OpenHarmony ArkUI
  (ACE Engine) projects. Triggers: reviewing PRs or code changes, checking memory management
  (RefPtr/WeakPtr/MakeRefPtr), verifying architecture compliance (four-layer, Pattern/Model/
  Property separation), auditing security vulnerabilities, detecting threading issues (data
  races, unsafe callback captures), analyzing code quality (code smells, SOLID violations),
  or generating review reports with severity levels.
  Also use when asked to "check code", "review PR", "audit security", "find memory leaks",
  "analyze code quality", or when encountering crash-prone patterns, unsafe pointer usage,
  or layer boundary violations.
  Use this skill whenever reading or editing files under `components_ng/`, `frameworks/core/`,
  `bridge/`, or `adapter/` directories, even without an explicit review request — any task
  involving `AceType::`, `MakeRefPtr`, `DynamicCast`, `WeakClaim`, `FrameNode`, or `RefPtr`
  warrants applying these checks.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkui
  capability: code-review
  version: 0.1.0
  status: draft
  tags:
    - arkui
    - code-review
    - ace-engine
    - cpp
    - arkts
---

# Task and Boundaries

## What This Skill Solves

Structured code review for ACE Engine (OpenHarmony ArkUI framework) codebases covering
C++, TypeScript, and ArkTS. Focuses on project-specific architecture constraints, smart
pointer conventions (RefPtr/WeakPtr/DynamicCast), component lifecycle rules, and four-layer
boundary enforcement that generic code review cannot provide.

## Input

- One or more source files (.h/.cpp/.ts/.ets)
- A diff, PR description, or directory path
- Optional: focus dimension (memory, security, threading, architecture, etc.)

## Output

- Severity-tagged findings (CRITICAL / HIGH / MEDIUM / LOW)
- Line-specific issues with before/after fix examples
- Prioritized action items grouped by dimension

## Not Applicable

- Non-ACE-Engine projects (generic C++ review should not invoke this skill)
- Build system, GN/BUILD.gn configuration, or test infrastructure issues
- UI/UX design review
- Replacing static analysis tools (clang-tidy, cppcheck, eslint)

# Trigger Signals

Activate when any of the following appear in the task:

- Task verbs: "review", "audit", "check", "analyze", "inspect" in context of ACE Engine / OpenHarmony / ArkUI code
- Task involves PR review, pre-merge quality gate, or code quality assessment
- Specific concern keywords: memory leak, RefPtr, WeakPtr, DynamicCast, data race, thread safety, security vulnerability, architecture compliance, code smell
- Code contains ACE Engine identifiers: `AceType::`, `MakeRefPtr`, `DynamicCast`, `WeakClaim`, `OnModifyDone`, `OnDirtyLayoutWrapperSwap`, `FrameNode`, `Pattern`, `LayoutProperty`, `PaintProperty`, `EventHub`, `RefPtr`, `WeakPtr`
- User asks whether code is safe, correct, or architecturally compliant

# Initial Checks

Before diving into analysis, ask yourself these questions to frame the review:

- **What changed?** Is this a new component, a bug fix, a refactor, or a performance optimization? Each type has different risk profiles.
- **Who depends on this code?** Changes to base classes or interfaces ripple across many components; changes to a leaf component are locally scoped.
- **What can break silently?** In ACE Engine, the most dangerous bugs are not crashes but silent behavior changes (e.g., layout not updating because MarkDirty was skipped).

Then determine scope with these steps (if steps conflict, file type takes priority over code location):

1. **Identify file type** -- C++ files get memory/threading/architecture focus; TS/ArkTS files get security/correctness focus
2. **Identify code location in project** -- Files under `components_ng/pattern/` require architecture compliance checks; files under `bridge/` require frontend-layer checks; files under `adapter/` require platform-abstraction checks
3. **Check task specificity** -- If user specified focus dimensions, prioritize those; otherwise apply full review
4. **Estimate scope** -- For >10 files, recommend phased review (critical scan first, then dimension deep-dive)

# Execution Strategy

## Phase 1: Blocking Issue Scan

Before detailed analysis, check for issues that block any further review:

| Check | Detection Pattern | Severity |
|-------|-------------------|----------|
| Raw `new`/`delete` without RefPtr | `new T()` not wrapped in `AceType::MakeRefPtr` | CRITICAL |
| Command injection | `system()`, `popen()` with user-influenced input | CRITICAL |
| Unsafe `this` capture in async | `[this]` inside `PostTask`, `PostDelayedTask`, or async callback | HIGH* |
| Layer boundary violation | Framework layer code calling platform API directly (e.g., `Rosen::` from Pattern) | CRITICAL |
| Buffer overflow | `strcpy`, `sprintf`, `gets`, unchecked array indexing with user-controlled size | CRITICAL |
| Circular RefPtr cycle | Parent holds `RefPtr<Child>` AND Child holds `RefPtr<Parent>` | CRITICAL |

\* `[this]` capture is HIGH (not CRITICAL) because the crash depends on whether the object
is destroyed before the callback fires. In PostDelayedTask this is almost certain; in PostTask
on the same thread it may be safe — but the risk is high enough to flag regardless.

**Checkpoint:** If any CRITICAL issue is found, report it immediately and ask the user whether to continue with the full review or stop here to fix blockers first.

## Phase 2: Dimension Selection

Apply dimensions based on file type and context. Not every dimension applies to every file.

**Always check for C++ files:**

| Priority | Dimension | ACE Engine-Specific Focus |
|----------|-----------|---------------------------|
| 1 | Memory | DynamicCast without null check, RefPtr vs raw pointer in member fields, MakeRefPtr missing on new objects, WeakPtr missing in child-to-parent back-references |
| 2 | Stability | Unchecked DynamicCast return (null dereference), OnModifyDone not handling property == nullptr, constructor accessing not-yet-attached FrameNode |
| 3 | Threading | `[this]` in PostTask/PostDelayedTask lambda, shared mutable state accessed from UI + render threads, WeakClaim missing in async callback |

**Check when relevant:**

| Condition | Dimension | Why |
|-----------|-----------|-----|
| Code handles external input, file paths, or credentials | Security | Injection, overflow, sensitive data exposure |
| Code is under `components_ng/`, `bridge/`, or `adapter/` | Architecture | Four-layer compliance, Pattern/Model/Property separation |
| Code is in layout/render/event hot paths | Performance | Unnecessary copies, missing caches, O(n^2) algorithms |
| Comprehensive review (user says "full review", "全面审查", "all dimensions", or unspecified dimensions with >3 files) | Code Quality | Code smells, SOLID violations, design patterns |

If the user's request is vague ("看看这段代码", "帮我看看"), treat it as a focused review
of Phase 1 blocking issues + the "Always check" dimensions only. Do NOT launch a full
comprehensive review unless explicitly requested.

**Checkpoint:** After dimension selection, confirm with yourself: "Am I checking only what's relevant for this file type and location, or am I running every dimension indiscriminately?"

## Phase 3: ACE Engine Architecture Rules

For files under `components_ng/`, verify against these project-specific rules:

**Object creation and casting:**
- Create with `AceType::MakeRefPtr<T>()`, never `new T()` or `RefPtr<T>(new T())`
- Cast with `AceType::DynamicCast<T>(ptr)` followed by null check, never `static_cast<T*>`

**Circular reference prevention:**
- Child back-references to parent must use `WeakPtr<Parent>`, not `RefPtr<Parent>`

**Async callback safety:**
- Capture `AceType::WeakClaim(this)`, then check `weak.Upgrade()` before use
- Never capture raw `this` in `PostTask` or any delayed/async callback

**Component lifecycle:**
- Initialization goes in `OnAttachToFrameNode()`, not constructor (frame node not ready)
- Property change reaction goes in `OnModifyDone()`
- Layout wrapper state transfer goes in `OnDirtyLayoutWrapperSwap()`

**Property system:**
- Mutate properties through Property objects (`GetLayoutProperty<T>()`, `GetPaintProperty<T>()`), never by directly manipulating render nodes
- Call `MarkDirty()` only when value actually changed (compare old vs new first)

**Layer separation:**
- Frontend Bridge -> Component Framework -> Layout/Render -> Platform Adapter
- No skipping layers (e.g., Pattern must not call platform APIs directly)

**Naming conventions:**
- Classes/Methods: `PascalCase`
- Private members: `snake_case_` (trailing underscore)
- Constants: `UPPER_CASE`
- Getters: `GetXxx()`, Setters: `SetXxx()`, Boolean queries: `IsXxx()`

**Checkpoint:** After architecture check, if no architecture issues are found in a file under `components_ng/`, explicitly note "Architecture rules: compliant" rather than skipping silently. This confirms you actually checked.

## Phase 4: Report Generation

Structure findings as:

1. **Executive Summary** -- Issue count by severity
2. **CRITICAL issues** -- Must fix before merge; include file:line, description, before/after fix
3. **HIGH issues** -- Should fix before merge
4. **MEDIUM/LOW issues** -- Grouped by dimension
5. **Action items** -- Ordered by priority with effort estimate

When generating formal reports, read `assets/report_template.md` for the complete template.

**Finding example (shows expected detail level):**

```
## CRITICAL: Circular RefPtr reference
File: components_ng/pattern/menu/menu_pattern.cpp:142
Dimension: Memory

  class MenuItem {
      RefPtr<Menu> parent_menu_;  // Strong ref back to parent
  };

Why: MenuItem -> Menu -> MenuItem forms a reference cycle.
     Neither will ever be freed, causing a memory leak in long-running sessions.
Fix: Change to `WeakPtr<Menu> parent_menu_;` and use `Upgrade()` before access.
```

**End-to-end flow example:**

User says: "Review this PR that adds a new Menu component"
→ Initial Checks: C++ files under `components_ng/pattern/menu/` → architecture focus
→ Phase 1: Scan for raw `new`, `[this]` in PostTask, circular RefPtr, layer violations → found 0 CRITICAL
→ Phase 2: Architecture (location-based) + Memory/Stability/Threading (C++ always) + Code Quality (>3 files, comprehensive)
→ Phase 3: Check 7 rule domains against each file
→ Phase 4: Report with 2 HIGH, 5 MEDIUM, 3 LOW findings → action items ordered by priority

# Prohibited Practices

The following anti-patterns are not covered by Phase 1 scan or Phase 3 rules, but are
equally harmful. When you encounter any of these, flag them with the stated severity.

| Anti-Pattern | Consequence | Severity | Correct Approach |
|-------------|-------------|----------|------------------|
| Bypassing property system — directly manipulating render node from Pattern | Breaks dirty marking, layout pipeline, change notification; other components unaware of change | HIGH | Always go through `GetLayoutProperty<T>()` / `GetPaintProperty<T>()` to mutate state |
| Unconditional `MarkDirty()` without comparing old vs new value | Triggers unnecessary full relayout/recalc on every call, even when nothing changed; degrades scroll/frame performance | MEDIUM | `if (oldValue != newValue) { prop->Update(newValue); MarkDirty(); }` |
| Initializing component state in constructor instead of `OnAttachToFrameNode()` | Frame node not yet attached; accessing layout properties or event hub crashes or returns wrong values | HIGH | Move initialization to `OnAttachToFrameNode()` |
| `dynamic_cast` / `static_cast` on `RefPtr` types instead of `AceType::DynamicCast` | Bypasses ACE Engine type system; may return wrong pointer or leak on cross-module boundaries | HIGH | Use `AceType::DynamicCast<T>(ptr)` and check result for null |
| Throwing exceptions for error flow (exceptions disabled in ACE Engine build) | Calls `std::terminate` at runtime; use error codes or `LOGE` + return instead | CRITICAL | Return error code or use `LOGE` + early return |

# Exceptions and Fallbacks

## Information Insufficient

- **Cannot determine file type**: Ask user; default to C++ rules
- **Cannot determine code location in project**: Skip architecture compliance; apply language-level checks only
- **Ambiguous severity**: Default to higher severity; explain uncertainty in finding

## Scope Too Large

- **>10 files**: Recommend phased review: (1) blocking issue scan, (2) dimension deep-dive, (3) report
- **Entire directory**: Suggest reviewing by subdirectory or by dimension

## Conflicting Rules

- **Safety vs performance**: Safety wins (e.g., never skip null checks for speed)
- **Architecture vs backward compatibility**: Flag both; let team decide

## Fallback

If code is not ACE Engine code but user still requests review: Apply language-level checks (memory, security, stability), explicitly note that architecture-specific rules do not apply.

# References

Read these files when deeper analysis is needed. Do not load all files at once; load only what the current review scope requires.

| File | When to Read |
|------|-------------|
| `references/ACE_ENGINE_SPECIFIC.md` | Reviewing code under `components_ng/`, `bridge/`, or `adapter/`; need full architecture rules, component structure patterns, lifecycle method details, naming conventions, or build integration |
| `references/MEMORY.md` | Found or suspect memory leaks, circular references, ownership ambiguity, or improper smart pointer usage beyond the rules in this document |
| `references/SECURITY.md` | Code handles external input, file paths, credentials, cryptographic operations, or uses system commands; need detailed vulnerability patterns and fixes |
| `references/STABILITY.md` | Found unchecked returns, missing error handling, boundary condition issues, or exception safety concerns |
| `references/CODE_SMELLS.md` | Comprehensive design quality review; need detection patterns and refactoring guidance for 22 types of code smells |
| `references/SOLID.md` | Reviewing class design, inheritance hierarchies, interface structure; need detailed violation detection and refactoring examples |
| `references/DIMENSIONS.md` | Quick lookup for any dimension (performance, threading, modern C++, effective C++, robustness, testability, maintainability, observability, API design, technical debt, backward compatibility) not covered by dedicated reference files |
| `assets/report_template.md` | Generating a formal review report; provides complete template with all sections |

**Do NOT load unless the above condition is met:**
- Do NOT load `CODE_SMELLS.md` or `SOLID.md` for single-file memory/threading-focused reviews
- Do NOT load `SECURITY.md` for code that has no external input surface (e.g., internal layout algorithms)
- Do NOT load `report_template.md` for informal/quick feedback — only for formal written reports
- Do NOT load `DIMENSIONS.md` when all relevant dimensions are covered by dedicated reference files
