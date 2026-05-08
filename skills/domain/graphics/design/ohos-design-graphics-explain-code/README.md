# ohos-design-graphics-explain-code

OpenHarmony code explanation and documentation generation Skill.

## Purpose

This project provides code understanding and documentation generation capabilities for OpenHarmony developers. Through an interactive three-stage workflow (Alignment → Call Chain Confirmation → Document Generation), it ensures the generated code documentation is accurate and comprehensive.

## Use Cases

- Understanding the call chain and architecture of existing code
- Generating technical documentation for modules, features, or APIs
- Analyzing business logic and outputting structured descriptions
- Generating documentation with Mermaid class diagrams and sequence diagrams

## Directory Structure

```
ohos-design-graphics-explain-code/
  SKILL.md                # Main skill file, loaded by the Agent
  README.md               # This file, intended for maintainers
  references/
    mermaid-guide.md      # Mermaid diagram syntax reference
```

## Metadata

| Field | Value |
| --- | --- |
| name | `ohos-design-graphics-explain-code` |
| author | `openharmony` |
| scope | `domain` |
| stage | `design` |
| domain | `graphics` |
| capability | `explain-code` |
| version | `0.1.0` |
| status | `stable` |

## Maintenance Notes

- The YAML Front Matter in `SKILL.md` must be consistent with the directory name and the metadata in this README.
- When updating `references/mermaid-guide.md`, ensure that the syntax examples remain valid.
