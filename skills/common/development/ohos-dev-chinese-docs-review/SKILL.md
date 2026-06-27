---
name: ohos-dev-chinese-docs-review
description: Check whether OpenHarmony API documentation follows the required templates and whether public API docs, system API docs, error code docs, and interface declarations/comments/implementations are consistent. Use when the user asks to review API doc quality, compare docs against code, audit error code docs, fill missing interface documentation, or generate a doc issue report.
---

# Documentation Check

Run OpenHarmony API documentation quality checks with emphasis on template compliance, documentation consistency, error code coverage, and implementation alignment. Focus the output on issues only. Do not repeat content that already complies.

## Review Philosophy

Before beginning documentation review, ask yourself:

- **Scope**: Am I validating template compliance or discovering semantic gaps? Template compliance is automatable; semantic gaps require human judgment.
- **Audience**: Can a developer use this API without trial-and-error based on this documentation?
- **Trust**: Verify, don't assume. @since tags, @permission declarations, and version markers are often outdated.

**Decision Principles**:
- When documentation structure is unclear → Examine Kit ownership and interface type first
- When template choice is ambiguous → Prefer component template for ArkUI, JS template otherwise
- When error codes don't match → Check both d.ts declarations and documented codes, flag mismatches
- When implementation is unavailable → Proceed with doc-only checks, explicitly state unchecked scope

## Input Collection

Infer paths from the user context, current working directory, and repository layout whenever possible. Ask the user only if the needed files still cannot be located.

Collect or infer the following inputs:

- `public API` doc path, optional, usually under `/docs`
- `system API` doc path, optional, usually under `/docs`
- error code doc path, optional, usually under `/docs`
- API definition path, usually under `/interface`
- repository root path, only if interface implementations cannot be found from the current workspace

By default, resolve `/docs` first from the workspace root, then `/interface`.

If the user provides a path starting with `/docs/...` or `/interface/...`, interpret it as a repository-root path first, not as a path relative to the current module directory.

If the user provides only part of the paths, start from the known inputs and continue auto-discovery under the workspace root `/docs` and `/interface`. Explicitly state any unchecked scope in the report.

## Workflow

Follow this order.

1. Locate the documents, interface declarations, and implementation code.
2. Run `scripts/check_api_doc_consistency.py` first for the stable automatable checks.
3. Read the relevant templates and extract the actual writing requirements.
4. Perform manual review for issues that cannot be checked reliably by script.
5. Cross-check documentation against implementation behavior when needed.
6. Output a Markdown report containing issues, impact, and fixes only.

## Completion Criteria

After script execution, verify:
- [ ] List of mechanical violations generated (@systemapi placement, missing fields, broken links)
- [ ] Documentation gaps identified (missing APIs, error codes)
- [ ] Template compliance status determined

After manual review, verify:
- [ ] Semantic gaps documented (vague descriptions, missing examples)
- [ ] Explanation quality assessed (clarity, completeness)
- [ ] Implementation misalignments noted (behavior mismatches, missing constraints)

Only proceed to report generation when the above criteria are met.

## Template Selection

Use this template priority:

1. In-repo template
2. External documentation link
3. Default templates bundled with this skill

In-repo template paths:

- JS API template: `/docs/blob/master/zh-cn/contribute/template/native-template.md`
- ArkTS component API template: `/docs/blob/master/zh-cn/contribute/template/ts-template.md`
- Error code template: `/docs/blob/master/zh-cn/contribute/template/errorcodes-template.md`

External links:

- JS API template: `https://gitcode.com/openharmony/docs/blob/master/zh-cn/contribute/template/native-template.md`
- ArkTS component API template: `https://gitcode.com/openharmony/docs/blob/master/zh-cn/contribute/template/ts-template.md`
- Error code template: `https://gitcode.com/openharmony/docs/blob/master/zh-cn/contribute/template/errorcodes-template.md`

Bundled fallback templates:

- `references/js-template.md`
- `references/ts-template.md`
- `references/errorcodes-template.md`

Try the in-repo template first. If it does not exist, try the external link. If that is still unavailable, fall back to the bundled template under `references/`. State the actual template source used in the final report.

Choose the template based on the interface category:

- Regular JS APIs, C APIs, or module-oriented API docs: use the JS API template
- ArkTS component interface docs: use the ArkTS component template
- Error code docs: use the error code template

For ArkTS component detection, prefer the owning Kit:

- If the interface belongs to `ArkUI`, treat it as an ArkTS component interface and use `ts-template`
- If the interface clearly uses ArkUI component semantics such as component, property, event, Builder, or Modifier concepts, also treat it as an ArkTS component interface
- For non-ArkUI Kits, default to regular API documentation unless the existing documentation structure clearly follows the ArkTS component template

Do not choose a template from the filename alone. Consider the Kit, interface type, current document structure, and d.ts content together.

## Template Loading Triggers

**MANDATORY - Load JS Template**:
- **When**: Reviewing JS/C APIs, module-oriented APIs, or when template questions arise
- **How**: Read `references/js-template.md` completely (~570 lines) for first-time JS API reviews
- **Optimization**: Use grep to locate specific sections before reading full file if only checking one requirement
- **Do NOT load**: When reviewing ArkTS components (use ts-template instead)

**MANDATORY - Load ArkTS Template**:
- **When**: Reviewing ArkTS component interface docs or ArkUI Kit interfaces
- **How**: Read `references/ts-template.md` completely (~275 lines) for ArkTS component reviews
- **Optimization**: Search first for property/event/Builder/Modifier sections, then read full file if needed
- **Do NOT load**: When reviewing regular JS APIs (use js-template instead)

**MANDATORY - Load Error Code Template**:
- **When**: Reviewing error code documentation or validating error field requirements
- **How**: Read `references/errorcodes-template.md` completely (~122 lines)
- **Do NOT load**: When only doing API-level checks (not error code docs)

**General Guidance**:
- **Do NOT load** templates when: script catches all issues and no template questions arise
- **Do NOT load** templates when: only doing implementation alignment (not template compliance)
- **Search first**: Use grep to find specific sections before reading entire template file

## Manual Review Focus

After the script finishes, focus manual review on the parts that are not reliable to automate:

- prose clarity, ambiguity, terminology consistency, and typo-level language quality
- whether examples are genuinely useful, runnable, and well explained
- whether the document structure really follows the template in spirit, not just in surface markers
- whether scenarios, constraints, preconditions, and failure modes are explained well enough for developers
- whether the documented causes for each error code are truly the union of real triggering scenarios
- whether the documentation matches implementation behavior, capability boundaries, and product changes
- whether ArkTS component docs provide enough guidance on parameters, defaults, ranges, and edge behavior

## Anti-Patterns

**NEVER assume these are correct without verification**:

- **Template-based compliance**: Many docs mechanically follow template headings but miss semantic requirements. A doc can have all required sections while failing to explain key constraints or scenarios. Always check for substance over structure.

- **@since tags**: Implementers frequently forget to update @since when backporting features. Cross-check with actual version behavior or release notes. The documented since version often lags behind reality.

- **Permission lists**: @permission lists are often incomplete for system APIs. Verify against implementation security checks. A missing permission in docs can cause runtime failures that are hard to diagnose.

- **Error code causality**: Error code docs commonly list generic causes without enumerating actual triggering scenarios. The documented causes must be the **union of all real scenarios** that trigger the error, not just common cases.

- **Static documentation assumptions**: Documentation often drifts from implementation. Even if a doc is well-structured, verify behavior claims against actual code when available.

- **ArkTS component parameter completeness**: Component docs often show examples with parameters that aren't documented in the property table. Flag these superficial compliance issues (example shows pageSize, but table doesn't list it).

- **Generic types without constraints**: `Array<any>`, `object`, or overly permissive types without validation rules prevent developers from understanding actual requirements. Flag insufficient type constraints.

## Implementation Alignment Checks

Use implementation code to identify missing or incorrect documentation such as:

- Incomplete feature scenarios, sub-scenarios, or functional coverage
- Missing concept, principle, or usage-scenario explanations that leave developers without enough context
- Product, interface, or behavior changes that were not synchronized into the docs
- Missing environment requirements, specification limits, preconditions, or failure scenarios

If the implementation cannot be located from the current repository, pause this part and ask the user for the correct repository path.

## Output Requirements

Produce a Markdown report focusing only on issues. Each issue should include:
- **Location**: File path and line number
- **Issue**: Clear problem description
- **Impact**: Why it matters
- **Suggested Fix**: What to do
- **Proposed Fix**: Concrete wording or code when applicable

Separately note unchecked scope, missing inputs, or limitations.

## Resource Usage

Read files under `references/` only when needed. Do not load everything by default. If a template is long, search for the relevant section first and then read only the needed part.

Use `scripts/check_api_doc_consistency.py` whenever the user provides a d.ts file together with public/system/error Markdown paths. The script already covers the repetitive high-confidence checks, including:

- d.ts tag extraction and `@throws` parsing
- public/system placement and direction-of-link checks
- structured field checks for `@syscap`, `@permission`, `@atomicservice`, `@systemapi`, model-only tags, `@deprecated`, and `@useinstead`
- section-level and document-level error-code coverage
- `-sys.md` naming, title, and `Readme-CN.md` entry checks
- mixed-module note checks for system docs
- required block checks in error-code documents
- basic version-marker checks such as module since notes and `<sup>x+</sup>` presence
- in-page and relative Markdown link resolution

For field-style checks, prefer the script result over manual keyword search. The current script parses labeled documentation fields such as `系统接口`, `模型约束`, and `需要权限`, which reduces noise from unrelated prose matches.

For `@since` handling, interpret tags from the dynamic-API documentation perspective only:

- `@since x` means the dynamic API starts at version `x`
- `@since x dynamic` means the dynamic API starts at version `x`
- `@since x dynamic&static` means both dynamic and static forms start at version `x`; for the current checker, use `x` as the dynamic version
- `@since x static` is ignored by the current doc checker
- `@since x dynamiconly` means the API is dynamic-only and starts at version `x`
- `@since x staticonly` is ignored by the current doc checker

Do not treat static-only version tags as documentation-version requirements for the current checks.

Do not hardcode evolving template wording in `SKILL.md`. The script reads its change-prone literals from `scripts/doc_check_rules.json`.

When the in-repo template or external template changes:

1. Compare the new template wording against `scripts/doc_check_rules.json`.
2. Update `scripts/doc_check_rules.json` first if only the expected text or required blocks changed.
3. Update `scripts/check_api_doc_consistency.py` only when the rule logic itself is no longer valid.
4. When template files are available locally, run the script with `--js-template`, `--ts-template`, and `--error-template` so it can warn when the configured rules no longer match the current template text.

Run it like this:

```bash
python3 scripts/check_api_doc_consistency.py \
  --api /path/to/file.d.ts \
  --public-doc /path/to/public.md \
  --system-doc /path/to/system.md \
  --error-doc /path/to/error.md \
  --readme-doc /path/to/Readme-CN.md \
  --js-template /path/to/native-template.md \
  --ts-template /path/to/ts-template.md \
  --error-template /path/to/errorcodes-template.md
```

`--readme-doc` is optional. If omitted, the script tries to infer `Readme-CN.md` from the public/system doc directory.
The template arguments are also optional, but provide an additional guard that warns when the rule file no longer matches the current template wording.

Treat the script output as the first pass. Do not duplicate those low-level rules manually in the report unless you are clarifying or confirming a script finding. Spend manual review time on semantic gaps, explanation quality, and implementation alignment instead.
