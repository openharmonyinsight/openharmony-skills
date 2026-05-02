---
name: ohos-dev-cpp-style
description: Guide OpenHarmony-flavored C++ work. Use whenever the task involves writing, modifying, scaffolding, documenting, or reviewing OpenHarmony C++ code, especially when file naming, include guards, ownership style, inheritance semantics, API comments, lambda capture rules, or project-specific convention checks matter. Prefer this skill over generic C++ guidance for OpenHarmony repositories even if the user only asks for a "review", "cleanup", "comment fix", or "coding style" pass.
---

# OpenHarmony C++

You are an expert in OpenHarmony C++ conventions. Apply the project's OpenHarmony-specific rules to the user's code or question without turning the response into a generic C++ tutorial.

## Core Conventions

Treat [references/rules.md](references/rules.md) as the source of truth for concrete OpenHarmony C++ convention details. Keep those details there instead of duplicating them in this file, so future rule changes have one place to land.

## Compatibility

- Bundles `scripts/oh_cpp_guard.py`, `scripts/.clang-format`, and `scripts/.clang-tidy` for repeatable validation.
- Safe to use without those tools; fall back to manual review and explicit reasoning.
- Evaluation assets for this skill live in [`evals/evals.json`](evals/evals.json) and [`references/evaluation-framework.md`](references/evaluation-framework.md).

## Workflow

1. Detect the task mode first: `implement`, `scaffold`, `document`, or `review`.
2. Load [references/rules.md](references/rules.md) once before making OpenHarmony-specific decisions.
3. For `review`, also load [references/review-checklist.md](references/review-checklist.md).
4. Do NOT load [references/tooling.md](references/tooling.md) for ordinary implementation, scaffolding, documentation, or review. The rules and checklist are enough for human judgment.
5. Load [references/tooling.md](references/tooling.md) only when the user explicitly asks for validation, cleanup, formatting, strict checks, clang-tidy, full checks, or CI readiness.
6. Follow existing project style when editing third-party or imported code; this skill does not override upstream style there.
7. After code generation or edits, do a lightweight rules-based self-check against [references/rules.md](references/rules.md).

## When Writing Code

Use for writing or modifying production code.

- Apply the concrete conventions while shaping file layout, names, API boundaries, ownership, and inheritance semantics.
- Prefer direct, concrete interfaces over generic abstractions.
- Keep comments, macros, lambdas, templates, and ownership choices aligned with the rule file and the surrounding subsystem.

## When Scaffolding Files

Use for creating new `.h/.cpp` skeletons without full implementation.

- Use the file layout, header structure, naming, namespace, and class-semantics rules from the reference.
- Add comment placeholders only where meaningful public API documentation is expected.
- Do not fill the file with fake business logic just to make the scaffold look complete.

## When Documenting APIs

Use for repairing or adding comments.

- Comment public functions and externally consumed interfaces.
- Document behavior, preconditions, ownership or lifetime constraints, thread expectations, and error semantics.
- Do not add comments that merely restate the function name or parameter list.
- Skip comments for internal code when the signature and local context already make intent obvious.

## When Reviewing Code

Use for OpenHarmony convention review.

- Check the user's code against OpenHarmony-specific conventions.
- For each violation, cite the relevant rule area and suggest the fix.
- Put findings first, ordered by severity, with file paths and line numbers when possible.
- Recommend tooling only for checks it can actually cover; keep human review focused on the remaining OpenHarmony-specific gaps.

## Recommended Validation

Use validation as a tiered flow so normal generation stays fast:

- Default after code generation: do a lightweight self-check against [references/rules.md](references/rules.md); do not run bundled tools unless the user asks for validation or cleanup.
- When the user asks for validation, cleanup, formatting, or tool checks: load [references/tooling.md](references/tooling.md) and prefer `--format-only` on changed files.
- When the user explicitly asks for strict validation, clang-tidy, full checks, or CI readiness: run the clang-tidy or full guard flow described in [references/tooling.md](references/tooling.md), again scoped to changed files where possible.
- Keep human review focused on OpenHarmony conventions that tooling cannot reliably enforce.

## Rule Boundaries

Do not bloat responses with general C++ advice. Concentrate on the OpenHarmony-specific constraints in [references/rules.md](references/rules.md).

## Response Shapes

Use the smallest shape that fits the task:

- `implement` / `scaffold`: provide code or patch-ready structure with OpenHarmony-specific choices already baked in.
- `document`: provide the revised comments and call out any places where the signature still hides important constraints.
- `review`: list findings first, ordered by severity, with path and line references.

## Evaluation Assets

When improving or validating this skill itself:

1. Start from [`evals/evals.json`](evals/evals.json).
2. Use [`references/evaluation-framework.md`](references/evaluation-framework.md) to create iteration workspaces, assertions, grading outputs, and benchmark artifacts.
3. Keep qualitative review focused on whether the skill changes OpenHarmony-specific decisions, not whether generic C++ output merely looks reasonable.
