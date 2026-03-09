---
name: docs-check-zh-cn
description: Check whether OpenHarmony API documentation follows the required templates and whether public API docs, system API docs, error code docs, and interface declarations/comments/implementations are consistent. Use when the user asks to review API doc quality, compare docs against code, audit error code docs, fill missing interface documentation, or generate a doc issue report.
---

# Documentation Check

Run OpenHarmony API documentation quality checks with emphasis on template compliance, documentation consistency, error code coverage, and implementation alignment. Focus the output on issues only. Do not repeat content that already complies.

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

Use this lookup order by default:

1. User-provided paths
2. Walk upward from the current working directory to locate the workspace root that contains `docs` and `interface`
3. Workspace root `/docs`
4. Workspace root `/interface`
5. Other source directories that may contain related implementations

If the current directory is a submodule, do not assume `/docs` or `/interface` exists under the current directory. Find the workspace root first.

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

## Manual Review Focus

After the script finishes, focus manual review on the parts that are not reliable to automate:

- prose clarity, ambiguity, terminology consistency, and typo-level language quality
- whether examples are genuinely useful, runnable, and well explained
- whether the document structure really follows the template in spirit, not just in surface markers
- whether scenarios, constraints, preconditions, and failure modes are explained well enough for developers
- whether the documented causes for each error code are truly the union of real triggering scenarios
- whether the documentation matches implementation behavior, capability boundaries, and product changes
- whether ArkTS component docs provide enough guidance on parameters, defaults, ranges, and edge behavior

## Implementation Alignment Checks

Use implementation code to identify missing or incorrect documentation such as:

- Incomplete feature scenarios, sub-scenarios, or functional coverage
- Missing concept, principle, or usage-scenario explanations that leave developers without enough context
- Product, interface, or behavior changes that were not synchronized into the docs
- Missing environment requirements, specification limits, preconditions, or failure scenarios

If the implementation cannot be located from the current repository, pause this part and ask the user for the correct repository path.

## Output Requirements

Produce a Markdown report with the following rules:

- Do not list content that already complies
- For each issue, include line number or location, issue description, reasoning or impact, suggested fix, and concrete wording when possible
- If you can provide corrected text directly, do so
- Separately note unchecked scope, missing inputs, or anything that cannot be confirmed

Preferred issue fields:

- `Location`
- `Issue`
- `Suggestion`
- `Proposed Fix`

## Resource Usage

Read files under `references/` only when needed. Do not load everything by default. If a template is long, search for the relevant section first and then read only the needed part.

Use `scripts/check_api_doc_consistency.py` whenever the user provides a d.ts file together with public/system/error Markdown paths. The script already covers the repetitive high-confidence checks, including:

- d.ts tag extraction and `@throws` parsing
- public/system placement and direction-of-link checks
- field presence for `@syscap`, `@permission`, `@atomicservice`, model-only tags, `@deprecated`, and `@useinstead`
- section-level and document-level error-code coverage
- `-sys.md` naming, title, and `Readme-CN.md` entry checks
- mixed-module note checks for system docs
- required block checks in error-code documents
- basic version-marker checks such as module since notes and `<sup>x+</sup>` presence
- in-page and relative Markdown link resolution

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
