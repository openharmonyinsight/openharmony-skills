---
name: ohos-dev-arkui-code-review
description: >
  Use this skill when the user explicitly requests a code review, quality audit, or
  safety/correctness analysis of ACE Engine (OpenHarmony ArkUI) code.
  Triggers: reviewing PRs or code changes, checking memory management
  (RefPtr/WeakPtr/MakeRefPtr), verifying architecture compliance (four-layer, Pattern/Model/
  Property separation), auditing security vulnerabilities, detecting threading issues (data
  races, unsafe callback captures), analyzing code quality (code smells, SOLID violations),
  or generating review reports with severity levels.
  Activates on explicit task verbs: "check code", "review PR", "audit security",
  "find memory leaks", "analyze code quality", "is this code safe/correct", or when asked to
  inspect crash-prone patterns, unsafe pointer usage, or layer boundary violations.
  Does NOT activate for general development, debugging, build-fix, or pure architectural
  Q&A tasks unless the user explicitly asks for review.
  The following directory contexts and symbols reinforce relevance but do not trigger
  this skill on their own: `components_ng/`, `frameworks/core/`, `bridge/`, `adapter/`,
  `AceType::`, `MakeRefPtr`, `DynamicCast`, `WeakClaim`, `FrameNode`, or `RefPtr`.
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
  related-skills:
    - ohos-dev-cpp-coding-style
---

# Task and Boundaries

Structured code review for ACE Engine (OpenHarmony ArkUI framework) codebases covering
C++, TypeScript, and ArkTS. Focuses on project-specific architecture constraints, smart
pointer conventions (RefPtr/WeakPtr/DynamicCast), component lifecycle rules, and four-layer
boundary enforcement that generic code review cannot provide.

**Input:** Source files (.h/.cpp/.ts/.ets), diffs, PR descriptions, or directory paths. Optional focus dimension.

**Output:** Severity-tagged findings (CRITICAL / HIGH / MEDIUM / LOW) with line-specific issues and before/after fix examples.

**Not applicable:** Non-ACE-Engine projects, build system (GN/BUILD.gn), UI/UX design review, or replacing static analysis tools.

# Trigger Signals

Activate when the task explicitly involves code review or quality analysis AND the code is in
an ACE Engine / OpenHarmony / ArkUI context. Do NOT activate for general development,
debugging, or build-fix tasks unless the user explicitly asks for review.

**Primary triggers (task must match at least one):**
- Task verbs: "review", "audit", "inspect" in context of ACE Engine code
- Task involves PR review, pre-merge quality gate, or code quality assessment
- User asks whether code is safe, correct, or architecturally compliant in an ACE Engine project

**Reinforcing signals (do not trigger alone):**
- Specific concern keywords: memory leak, RefPtr, WeakPtr, DynamicCast, data race, thread safety, architecture compliance
- Code contains ACE Engine identifiers: `AceType::`, `MakeRefPtr`, `OnModifyDone`, `FrameNode`, `Pattern`, `LayoutProperty`, `RefPtr`
- Files under `components_ng/`, `frameworks/core/`, `bridge/`, `adapter/`

# Initial Checks

Before diving into analysis, ask yourself:

- **What changed?** New component, bug fix, refactor, or perf optimization — each has different risk profiles.
- **Who depends on this code?** Changes to base classes ripple across many components; leaf component changes are locally scoped.
- **What can break silently?** The most dangerous ACE Engine bugs are not crashes but silent behavior changes (e.g., layout not updating because MarkDirty was skipped).

Determine scope (if steps conflict, file type takes priority over code location):

1. **Identify file type** — C++ files get memory/threading/architecture focus; TS/ArkTS files get security/correctness focus
2. **Identify code location** — `components_ng/pattern/` requires architecture compliance; `bridge/` requires frontend-layer checks; `adapter/` requires platform-abstraction checks
3. **Check task specificity** — If user specified focus dimensions, prioritize those; otherwise apply full review
4. **Estimate scope** — For >10 files, recommend phased review (critical scan first, then dimension deep-dive)

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

\* `[this]` capture is HIGH (not CRITICAL) because the crash depends on timing. In `PostDelayedTask` the object is almost certainly destroyed before the callback fires; in `PostTask` on the same thread it may be safe — but the risk is high enough to flag regardless.

**Checkpoint:** If any CRITICAL issue is found, report it immediately and ask whether to continue or stop to fix blockers first.

## Phase 2: Dimension Selection

Not every dimension applies to every file.

**Always check for C++ files:**

| Priority | Dimension | ACE Engine-Specific Focus |
|----------|-----------|---------------------------|
| 1 | Memory | DynamicCast without null check, RefPtr vs raw pointer in member fields, MakeRefPtr missing, WeakPtr missing in child-to-parent back-references |
| 2 | Stability | Unchecked DynamicCast return, OnModifyDone not handling property == nullptr, constructor accessing not-yet-attached FrameNode |
| 3 | Threading | `[this]` in PostTask/PostDelayedTask lambda, shared mutable state accessed from UI + render threads, WeakClaim missing in async callback |

**Check when relevant:**

| Condition | Dimension | Why |
|-----------|-----------|-----|
| Code handles external input, file paths, or credentials | Security | Injection, overflow, sensitive data exposure |
| Code is under `components_ng/`, `bridge/`, or `adapter/` | Architecture | Four-layer compliance, Pattern/Model/Property separation |
| Code is in layout/render/event hot paths | Performance | Unnecessary copies, missing caches, O(n^2) algorithms |
| Comprehensive review (user says "full review" or unspecified dimensions with >3 files) | Code Quality | Code smells, SOLID violations, design patterns |

For vague requests ("看看这段代码", "帮我看看"), treat as focused review of Phase 1 blocking issues + "Always check" dimensions only.

**Checkpoint:** "Am I checking only what's relevant for this file type and location, or am I running every dimension indiscriminately?"

## Phase 3: ACE Engine Architecture Rules

For files under `components_ng/`, `bridge/`, or `adapter/`, load the relevant architecture reference:

- **MANDATORY — READ:** `references/ACE_ARCHITECTURE.md` (four-layer, component structure, naming)
- **Load when reviewing lifecycle/property code:** `references/ACE_LIFECYCLE.md` (OnModifyDone, OnAttachToFrameNode, dirty marking, event handling)
- **Load when reviewing tests or build files:** `references/ACE_TESTING.md` (build system, test patterns, source references, property macro internals)

**Do NOT load architecture references for:**
- Files outside `components_ng/`, `bridge/`, `adapter/`
- Reviews focused solely on security or threading with no architecture relevance

## Phase 4: Report Generation

Structure findings as:

1. **Executive Summary** — Issue count by severity
2. **CRITICAL issues** — Must fix before merge; include file:line, description, before/after fix
3. **HIGH issues** — Should fix before merge
4. **MEDIUM/LOW issues** — Grouped by dimension
5. **Action items** — Ordered by priority with effort estimate

For formal reports, read `assets/report_template.md` for the report specification.

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

# Prohibited Practices

| Anti-Pattern | Consequence | Severity | Correct Approach |
|-------------|-------------|----------|------------------|
| Bypassing property system — directly manipulating render node from Pattern | Breaks dirty marking, layout pipeline, change notification | HIGH | Go through `GetLayoutProperty<T>()` / `GetPaintProperty<T>()` |
| Unconditional `MarkDirtyNode()` without comparing old vs new | Triggers unnecessary full relayout on every call; degrades scroll/frame performance | MEDIUM | Use macro-declared properties (auto-dedup via `NearEqual`) or compare before marking |
| Initializing component state in constructor instead of `OnAttachToFrameNode()` | Frame node not yet attached; crashes or wrong values | HIGH | Move initialization to `OnAttachToFrameNode()` |
| `dynamic_cast` / `static_cast` on `RefPtr` types instead of `AceType::DynamicCast` | Bypasses ACE Engine type system; wrong pointer or leak on cross-module boundaries | HIGH | Use `AceType::DynamicCast<T>(ptr)` and check for null |
| Throwing C++ exceptions for error flow | May be caught by unexpected handlers; ACE uses error codes and `LOGE` + return | HIGH | Return error code or use `LOGE` + early return; use `CHECK_NULL_VOID` / `CHECK_NULL_RETURN` |

# Exceptions and Fallbacks

## Information Insufficient

- **Cannot determine file type**: Ask user; default to C++ rules
- **Cannot determine code location**: Skip architecture compliance; apply language-level checks only
- **Ambiguous severity**: Default to higher severity; explain uncertainty in finding

## Scope Too Large

- **>10 files**: Recommend phased review: Phase A (blocking scan on all files) → Phase B (dimension deep-dive on files with issues) → Phase C (consolidated report)
- **Entire directory**: Review by subdirectory or by dimension
- **Cross-component changes**: Verify component interactions — event propagation, shared property types, lifecycle ordering between parent and child patterns

## ArkTS / TypeScript Files

When reviewing `.ets` / `.ts` files in ACE Engine context:

- **Bridge layer** (`bridge/declarative_frontend/`): Verify ArkTS property setters correctly call `ModelNG::SetXxx()` and parameter types match C++ side
- **Type safety**: Ensure `@Component` structs use proper types, not `any` or unchecked casts
- **Resource handling**: Verify `ResourceType` usage — raw strings should go through `$r()` or `Resource` wrapper
- **Lifecycle**: ArkTS `aboutToAppear`/`aboutToDisappear` map to C++ Pattern lifecycle; verify alignment
- For non-bridge ArkTS code (application-level), apply general TypeScript/ArkTS best practices

## Conflicting Rules

- **Safety vs performance**: Safety wins (never skip null checks for speed)
- **Architecture vs backward compatibility**: Flag both; let team decide

# References

Read only what the current review scope requires. Do not load all files at once.

| File | When to Read |
|------|-------------|
| `references/ACE_ARCHITECTURE.md` | Reviewing code under `components_ng/`, `bridge/`, or `adapter/` — four-layer architecture, component structure, naming |
| `references/ACE_LIFECYCLE.md` | Reviewing lifecycle methods, property access, dirty marking, event handling patterns |
| `references/ACE_TESTING.md` | Reviewing tests, build files, or need property macro details / source references |
| `references/MEMORY.md` | Found or suspect memory leaks, circular references, ownership ambiguity, or improper smart pointer usage |
| `references/SECURITY.md` | Code handles external input, file paths, credentials; need ACE Engine-specific security patterns |
| `references/STABILITY.md` | Found unchecked DynamicCast returns, missing error handling, lifecycle timing issues |
| `references/CODE_SMELLS.md` | Need ACE Engine-specific code smell detection (God Pattern, Property Bypass, EventHub Bypass, etc.) |
| `references/SOLID.md` | Need ACE Engine-specific SOLID violation patterns (SRP in Pattern, DIP with platform singletons, etc.) |
| `references/DIMENSIONS.md` | Quick lookup for dimensions without dedicated files (performance, threading, modern C++, testability, etc.) |
| `assets/report_template.md` | Generating a formal review report |

**Do NOT load unless the above condition is met:**
- Do NOT load `ACE_LIFECYCLE.md` or `ACE_TESTING.md` for security-only or threading-only reviews
- Do NOT load `CODE_SMELLS.md` or `SOLID.md` for single-file memory/threading-focused reviews
- Do NOT load `SECURITY.md` for code with no external input surface (e.g., internal layout algorithms)
- Do NOT load `report_template.md` for informal/quick feedback
- Do NOT load `DIMENSIONS.md` when all relevant dimensions are covered by dedicated reference files
