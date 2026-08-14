---
name: spec-test-analyzer
description: "Analyze ArkTS code snippets or CTS test cases against the specification stored in ./docs. Prefer the generated ./.agent index when available, and fall back to raw docs when the index has not been built yet."
metadata:
  author: openharmony
  scope: common
  stage: analysis
  domain: language-spec
  capability: spec-test-analysis
  version: 1.1.1
  status: stable
  compatibility:
    tools: bash, git, python3, rg, grep, read, glob
    dependencies:
      - ./docs source markdown files (required)
      - ./.agent generated retrieval index (optional, recommended)
      - ./scripts/build_agent.sh for index generation
---

# Spec Test Analyzer

This skill uses `./docs/` as the canonical ArkTS spec corpus. It prefers the generated `./.agent/` index for fast recall, but it must remain usable in a clean checkout where `./.agent/` has not been built yet.

## Directory Contract

- `./docs/`: committed raw spec Markdown files and the only long-term source of truth.
- `./.agent/`: generated retrieval index produced from `./docs/`. Do not commit it.
- `./scripts/build_agent.sh`: builds or refreshes `./.agent/` with `wiki_agentizer`.
- `./scripts/validate_agent.sh`: validates the generated index.
- `./.tooling/`: local bootstrap area for the `wiki_agentizer` tool, its virtual environment, and temporary build outputs. Do not commit it.

## Preflight

Before analyzing any snippet or CTS failure:

1. Confirm `./docs/` exists.
2. If `./.agent/manifest.json` exists, use the index-first workflow below.
3. If `./.agent/` is missing, tell the user the fast index is unavailable and choose one of these paths:
   - Recommended: run `./scripts/build_agent.sh`, then continue with the index-first workflow.
   - Fallback: continue with raw-doc retrieval from `./docs/` if the task is small, urgent, or build tooling is unavailable.
4. Never treat `./.agent/` as a committed or guaranteed input in a clean environment.

## Build and Validate the Index

`./scripts/build_agent.sh` bootstraps `wiki_agentizer` from `https://gitcode.com/anxuesm/wiki_agentizer` into `./.tooling/`, checks out the pinned default commit, verifies `HEAD`, builds into an isolated temporary output root under `./.tooling/`, then syncs the resulting `./.agent/` back into the skill root.

```bash
./scripts/build_agent.sh
./scripts/validate_agent.sh
```

Useful environment overrides:

- `WIKI_AGENTIZER_DIR`: use an already checked-out local tool directory instead of cloning.
- `WIKI_AGENTIZER_REPO`: override the clone URL.
- `WIKI_AGENTIZER_REF`: explicitly override the pinned default commit after auditing the new version.
- `GIT_BIN`: choose the Git executable used for clone, checkout, and HEAD verification.
- `WIKI_AGENTIZER_FULL_BUILD=1`: force a full rebuild instead of incremental mode.
- `WIKI_AGENTIZER_CONFIG`: pass a config file to `wiki_agentizer`.
- `WIKI_AGENTIZER_JOBS`: set build parallelism.
- `PYTHON_BIN`: choose a specific Python executable.

## Trigger Conditions

Use this skill when:

- The user provides one or more ArkTS code snippets or test cases and asks which spec rules they relate to.
- The user asks to generate or complete test cases for a given syntax feature.
- The user asks to check whether existing test cases fully cover a spec section.
- The user provides a failed CTS test case and needs spec-grounded expected behavior, rule recall, or gap analysis.

## CTS Defect Spec Analysis Mode

When the input is a failed CTS test case with an error message or unexpected behavior, switch to **CTS defect analysis mode**.

Additional work in this mode:

1. Extract the expected compiler behavior from recalled spec rules.
2. Map the observed error to a spec gap or implementation mismatch.
3. Identify the likely responsibility split:
   - Syntax parsing error -> Parser
   - Type mismatch or semantic error -> Checker
   - Code generation or desugaring error -> Lowering
4. Produce the CTS defect analysis report in the format below.

### CTS Defect Spec Analysis Report Format

````markdown
# CTS缺陷Spec分析报告

## 一、用例信息
- **用例路径**: <CTS test case path>
- **错误现象**: <error message or unexpected behavior>
- **期望行为**: <what should happen according to spec>

## 二、Spec规则召回

### 2.1 直接相关Spec
| Spec章节 | 规则描述 | 规则原文(摘要) |
|----------|----------|---------------|
| | | |

### 2.2 交叉引用Spec
| Spec章节 | 关联规则 | 与本用例的关系 |
|----------|----------|---------------|
| | | |

### 2.3 Spec原文
> {quoted spec text from source file, with source_path:line_start-line_end citation}

## 三、Spec与编译器行为差异分析

### 3.1 Spec期望行为
<!-- 从spec规则推导出的正确编译器行为 -->

### 3.2 当前编译器行为
<!-- 根据错误信息描述的当前行为 -->

### 3.3 差异点
| Spec规则 | 期望行为 | 实际行为 | 差异类型 |
|----------|----------|----------|----------|
| | | | 未实现/实现不一致/边界缺失 |

### 3.4 责任模块判定
- **主要责任模块**: <parser/checker/lowering>
- **判定依据**: <why this module is responsible>
- **可能涉及的辅助模块**: <other modules that may need changes>

## 四、补充测试场景

### 场景: {scenario name}
- Spec rule: {which normative statement}
- Expected: {compile-time pass/error/runtime behavior}
```arkts
{test code}
```

## 五、总结
- **召回Spec规则数**:
- **识别差异点数**:
- **建议责任模块**:
- **建议修复方向**: <brief fix direction derived from spec analysis>
````

## Generated Index Layout

When `./.agent/` has been built, treat these as the main retrieval artifacts:

- `./.agent/manifest.json`
- `./.agent/catalog/docs_min.jsonl`
- `./.agent/catalog/dirs_min.jsonl`
- `./.agent/documents/`
- `./.agent/sections/`
- `./.agent/cache/section_index.jsonl`
- `./.agent/graph/` as optional hints only
- `./.agent/reports/`

`graph/` data is optional acceleration data. If it is sparse or empty in the current build, the workflow must fall back to `related_docs[]`, section metadata, and fixed chapter scans instead of failing.

## Retrieval Workflow

### Step 1: Syntax Feature Extraction

From each code snippet, extract:

- **Keywords**: language keywords present such as `class`, `interface`, `extends`, `implements`, `async`, and `abstract`
- **Constructs**: structural patterns such as class declarations, generic instantiations, and enum usage
- **Types used**: concrete types, user-defined types, unions, nullable forms, and type arguments
- **Modifiers**: `public`, `private`, `static`, `readonly`, `abstract`, `override`, and related modifiers
- **Context**: whether the code is a declaration, expression, statement, module-level construct, or type position

### Step 2A: Index-First Recall

Use this path when `./.agent/manifest.json` exists.

1. Scan `./.agent/catalog/docs_min.jsonl` for candidate chapters.
2. Read matching document sidecars under `./.agent/documents/` to inspect `keywords[]`, `related_docs[]`, and entry scores.
3. Read matching section sidecars under `./.agent/sections/` to locate the most relevant headings and line ranges.
4. Scan `./.agent/cache/section_index.jsonl` for cross-document section matches when the feature spans multiple chapters.

### Step 2B: Raw-Doc Fallback

Use this path when `./.agent/` is unavailable.

1. Search `./docs/` with `rg` using extracted keywords, syntax names, and expected chapter terms.
2. Prioritize chapter files that map naturally to the feature, such as:
   - `9_classes.md` for classes and members
   - `10_interfaces.md` for interfaces
   - `11_enums.md` for enums
   - `5_generics.md` for generics
   - `6_conversions.md` for conversions
   - `15_semantics.md` for semantic rules
   - `4_names.md` for scope and declaration rules
3. Read the matched source text directly from `./docs/`.

### Step 3: Source Reading

For each matched section, read the actual spec text from the canonical source file in `./docs/`:

- Use `source_path`, `line_start`, and `line_end` when the index is available.
- Otherwise infer the section by heading and read the matching range directly from the Markdown file.
- Always cite the source file and line range in the final analysis report.

### Step 4: Cross-Chapter Expansion

For each matched rule, expand to related chapters by using this priority order:

1. `related_docs[]` from the generated document metadata, if present
2. `./.agent/graph/link_graph.json` and `./.agent/graph/backlinks.json` if they contain usable edges
3. Fixed manual chapter checks:
   - `15_semantics.md` for semantic constraints
   - `6_conversions.md` for conversion behavior
   - `4_names.md` for scope and declaration rules
   - `5_generics.md` for generic interactions

## Test Case Generation Strategy

For each recalled spec section, enumerate:

1. Valid syntax variants
2. Invalid syntax variants
3. Boundary conditions
4. Modifier combinations
5. Inheritance or implementation scenarios when relevant
6. Generic instantiations when relevant
7. Success and failure behaviors

Do not duplicate cases that only change trivial literal values without changing the spec rule being exercised.

## Report Requirements

Every analysis output must:

- cite the canonical source text from `./docs/`
- state whether the result came from index-first retrieval or raw-doc fallback
- separate directly relevant rules from cross-chapter rules
- list uncovered or ambiguous areas explicitly

For non-CTS requests, use a compact Markdown report with:

1. Overview
2. Recalled spec sections
3. Source citations
4. Generated or missing test scenarios
5. Coverage summary
