---
name: ohos-design-agent-instruction-quality-review
description: Use when auditing OpenHarmony repository coding-agent guidance such as AGENTS.md, CLAUDE.md, GEMINI.md, Codex instructions, Copilot instructions, Cursor rules, or repository agent guidance.
metadata:
  author: openharmony
  scope: common
  stage: design
  domain: agent
  capability: instruction-quality-review
  version: 0.1.0
  status: draft
  tags:
    - agent
    - instructions
    - quality-review
---

# Agent Instruction Quality Review

Review OpenHarmony repository coding-agent instruction files for whether they can reliably change agent behavior. Judge the instruction file itself, not the repository's unstated knowledge.

## Use For

- Reviewing a new or updated OpenHarmony `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Codex instruction, Copilot instruction, Cursor rule, or equivalent repository agent guidance file.
- Establishing a baseline for OpenHarmony repository-level or subsystem-level agent guidance.
- Comparing OpenHarmony agent instruction files across teams or repositories.
- Preparing a remediation plan for weak or incomplete OpenHarmony agent instructions.

Do not use for general README review, coding style review, or architecture design review unless the user explicitly asks to evaluate agent instruction quality.

## Inputs

Expected:
- Content or path of an OpenHarmony `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Codex instruction, Copilot instruction, Cursor rule, or equivalent repository agent guidance file.

Optional:
- Repository tree or relevant path map.
- Referenced docs such as `docs/agent/*`, ADRs, skills, or test instructions.
- OpenHarmony repository type, such as OS subsystem, system service, SDK, language runtime, framework, tooling repository, or monorepo.

If referenced documents are unavailable, evaluate whether routing exists but do not assume those documents are correct.

## Review Principles

- Short but actionable is better than long but vague.
- Do not reward README-style summaries unless they guide agent action.
- Do not require complete domain knowledge inside the instruction file.
- Reward routing rules that tell the agent when to read deeper documents.
- Reward constraints that prevent high-risk agent behavior.
- Reward executable, task-specific verification instructions.
- Penalize generic statements such as "follow best practices", "run tests", or "understand the architecture" when no concrete guidance is provided.
- Treat assertions without concrete evidence as weak. When the input has file paths or line numbers, every finding must cite `file:line`; when line numbers are unavailable, cite the exact section title or quoted phrase and state that line numbers were not available.

## Scoring Rubric

Total score: 100.

| Element | Weight | Core question |
| --- | ---: | --- |
| Code map | 20 | Can the agent quickly locate key paths and understand the work scope? |
| Knowledge routing | 30 | Does the agent know what docs to read for different tasks, paths, or domain terms? |
| Constraints and boundaries | 30 | Does the agent know what must not be broken or changed without escalation? |
| Verification loop | 20 | Does the agent know how to prove the task is complete? |

Grade rules:
- A: 85-100, usable as team baseline.
- B: 70-84, usable but needs improvement.
- C: 50-69, partially useful but not reliable enough.
- D: below 50, mostly README-style or incomplete.

Quality gate:
- Pass: score >= 85 and no critical gaps.
- Conditional pass: score 70-84 and no critical gaps; remediation required.
- Fail: score < 70 or any critical gap related to public API, security, permissions, protocol compatibility, generated files, destructive commands, or missing validation.

## Element 1: Code Map

Check whether the file explains:
- Applicable scope: repository root, subsystem, directory, package, or module.
- Project or module responsibility.
- Key code paths and frequently modified paths.
- Where to look for common task types.
- Nested `AGENTS.md`, `CLAUDE.md`, rules, or skills with more specific guidance.

Scoring:

| Score | Meaning |
| ---: | --- |
| 0 | No code map or scope information. |
| 5 | Basic directory list only. |
| 10 | Includes project/module responsibility and some key paths. |
| 15 | Includes key paths, high-risk or frequent-change paths, and scope. |
| 20 | Includes scope, responsibility, key paths, nested guidance, and task-to-path "where to look" mapping. |

Strong evidence names scope, important paths, nested guidance, and task-to-path mappings. Weak evidence only says source is in `src`, tests are in `test`, or docs are in `docs`.

## Element 2: Knowledge Routing

Check whether the file tells the agent when to read deeper knowledge sources.

Strong routing covers:
- Task-based routing: docs to read for API, architecture, permission, DFX, compatibility, or domain behavior changes.
- Path-based routing: docs to read when changing specific directories or modules.
- Vocabulary-based routing: docs to read when task descriptions, logs, issues, APIs, or files mention domain terms, acronyms, or internal jargon.

Scoring:

| Score | Meaning |
| ---: | --- |
| 0 | No knowledge routing. |
| 5 | Only lists documents or links with no trigger conditions. |
| 10 | Has basic task-to-document routing. |
| 20 | Has task-based and path-based routing with useful trigger conditions. |
| 25 | Also includes vocabulary-based routing for domain terms, acronyms, or internal jargon. |
| 30 | Requires the agent to state task category, documents read, and constraints found before editing. |

Evaluate domain vocabulary under this element. Do not require a full glossary in the instruction file; full terminology belongs in separate docs.

## Element 3: Constraints And Boundaries

Check whether the file explicitly tells the agent what must not be changed, bypassed, or assumed.

Important categories:
- Public API signatures, semantics, lifecycle, error codes, and compatibility.
- Permission, security, trust, authentication, and authorization boundaries.
- Protocol compatibility, persistent data formats, serialization, and cross-version behavior.
- Module layering, dependency direction, abstraction ownership, and generated-code boundaries.
- Third-party dependencies and license-sensitive changes.
- Device operations, destructive commands, or commands affecting real hardware.
- DFX, logging, observability, fault attribution, and diagnostic behavior.
- Known pitfalls and common agent failure modes.

Scoring:

| Score | Meaning |
| ---: | --- |
| 0 | No explicit constraints. |
| 5 | Generic advice only. |
| 10 | Some do-not rules exist but miss major high-risk categories. |
| 20 | Covers several high-risk boundaries with concrete rules. |
| 25 | Includes do-not rules, ask-before rules, and architecture/domain invariants. |
| 30 | Also captures project-specific pitfalls, generated-code boundaries, compatibility risks, and agent failure patterns. |

Weak evidence includes statements such as "follow the architecture", "keep code clean", or "be careful when changing APIs" without operational rules.

## Element 4: Verification Loop

Check whether the file defines how the agent should validate changes and report completion.

It should include:
- Build commands.
- Test commands.
- Lint or static analysis commands.
- API compatibility or contract checks if relevant.
- Task-specific validation guidance.
- Done definition.
- Final response expectations.
- What to do if validation cannot be run.

Scoring:

| Score | Meaning |
| ---: | --- |
| 0 | No validation guidance. |
| 5 | Generic "run tests" instruction only. |
| 10 | Provides some build/test/lint commands. |
| 15 | Provides task-specific validation and explains what to report. |
| 20 | Provides minimum checks, task-specific checks, Done definition, final response expectations, and fallback if validation cannot be run. |

## Workflow

1. Identify the file and scope:
   - File reviewed.
   - Root-level or directory-level guidance.
   - Target agent: Codex, Claude Code, Copilot, or generic coding agent.
   - Referenced docs, nested instruction files, or skills.
2. Extract evidence for each element:
   - `file:line` references for section titles, paragraphs, bullet points, referenced paths, and commands whenever the source location is available.
   - Exact section title or short quoted phrase when line numbers are unavailable.
   - Missing or weak areas.
3. Score each element:
   - Existence: `Missing`, `Partial`, or `Present`.
   - Quality: `Weak`, `Acceptable`, `Strong`, or `Excellent`.
   - Numeric score according to the rubric.
   - Evidence and gap.
4. Identify critical gaps.
5. Recommend minimal, patch-style fixes.

## Critical Gaps

Flag a gap as critical if it may cause high-risk agent behavior, such as:
- Agent changes public API without compatibility review.
- Agent modifies permissions, trust, security, protocol, or persistent data without escalation.
- Agent bypasses generated-code source of truth.
- Agent cannot find key code paths.
- Agent has no way to validate changes.
- Agent sees domain terms but does not know what knowledge to load.

## Common Anti-Patterns

Penalize:
- README duplication: repeats project introduction, installation, and directory tree but does not guide agent behavior.
- Link dump: lists many docs but does not say when to read each one.
- Generic engineering advice: "follow best practices", "keep code clean", "understand the architecture", or "run tests".
- No high-risk boundary: omits public APIs, permissions, compatibility, protocol, generated files, dependencies, or hardware/device risks.
- No validation evidence: lacks build/test/lint commands, Done criteria, or final reporting requirements.
- Overloaded instruction file: embeds long architecture docs, a full glossary, or complete process manuals instead of routing to separate docs or skills.

## Output Format

Keep the report compact and evidence-led. Use this structure:

````md
# Agent Instruction Quality Review

## Overall result

| Item | Result |
| --- | --- |
| File reviewed | `<path>` |
| Scope | `<root / subsystem / directory / unknown>` |
| Overall score | `<score>/100` |
| Grade | `<A/B/C/D>` |
| Conclusion | `<short conclusion>` |

## Score breakdown

| Element | Existence | Quality | Score | Key finding |
| --- | --- | --- | ---: | --- |
| Code map | `<...>` | `<...>` | `<n>/20` | `<file:line-backed finding>` |
| Knowledge routing | `<...>` | `<...>` | `<n>/30` | `<file:line-backed finding>` |
| Constraints and boundaries | `<...>` | `<...>` | `<n>/30` | `<file:line-backed finding>` |
| Verification loop | `<...>` | `<...>` | `<n>/20` | `<file:line-backed finding>` |

## Detailed findings

For each element, write one short subsection with:
- Evidence: cite `file:line`; if unavailable, cite the exact section or phrase and say line numbers were unavailable.
- Assessment: explain the score in one or two bullets.
- Gap: name the missing or vague behavior.
- Recommended fix: include the smallest useful patch-style addition.

## Critical gaps

`None identified` or a severity-ordered bullet list with `file:line` evidence.

## Minimal remediation plan

1. `<highest-priority fix>`
2. `<next fix>`
3. `<next fix>`

## Final judgment

One paragraph explaining whether this instruction file is ready for OpenHarmony team use, needs revision, or should not pass quality gate.
````

## Minimal Fix Patterns

Prefer small, high-leverage additions:
- Add a `Where to look` table.
- Add task-based and vocabulary-based routing.
- Add `Do not` and `Ask before` lists.
- Add minimum build/test/lint commands.
- Add a Done definition and final response expectations.
