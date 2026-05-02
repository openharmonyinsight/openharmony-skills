# OpenHarmony C++ Coding Style Skill

This skill is registered as `ohos-dev-cpp-style` and lives under the common development namespace:

```text
skills/common/development/ohos-dev-cpp-style/
```

## Runtime Files

- `SKILL.md` is the agent entry point.
- `references/` contains files the agent may load during normal use.
- `scripts/` contains repeatable validation helpers used only when validation or cleanup is requested.
- `evals/` contains seed prompts and evaluation workflow notes.

## Maintenance Files

`maintenance/` contains build-time analysis and decision records for maintainers. These files are not intended to be loaded during ordinary code generation or review:

- `maintenance/rule-selection-rationale.md` explains how the OpenHarmony C++ coding rules were filtered into skill-ready guidance.
- `maintenance/tool-coverage-analysis.md` records which rules are covered by clang-format, clang-tidy, custom guard logic, or human review.

Keep operational agent guidance in `SKILL.md` and `references/`. Keep historical rationale and rule-selection notes in `maintenance/`.
