# design.md Incremental Merge Guide

New feature content **must never** open a new `## Feat-XX 详细设计` top-level chapter. Everything must be merged into the existing chapters. Note: chapter titles below stay in Chinese because they refer to actual section headings in design.md.

## Merge mapping

| New feature content | Target chapter | How to merge |
|---------------------|----------------|--------------|
| Feature ID | `## 设计元数据` table → `目标 Feature` field | Append `, Feat-XX <name>` to the existing value |
| Feature goal | `## 需求基线` table → 补充说明 row | Append `；（Feat-XX）<goal description>` to the existing value |
| Newly involved source modules | `### 涉及仓和模块` table | Append new rows; `本 Feature 影响` column reads `Feat-XX: <impact>` |
| ADR decisions | `## 关键设计决策` table | Append `ADR-FX-N` rows right after existing ADR-N entries |
| Architecture diagram | `### 架构图` subsection | Below the existing ``` block, add `#### <name> 架构图（Feat-XX）` subheading + a new ``` block |
| Data model | `### 数据模型设计` subsection | Below the existing ```cpp block, add `#### <name> 数据模型（Feat-XX）` subheading + new ```typescript / ```cpp blocks |
| API signatures & permissions | `## API 签名与权限` table | Append new API rows; 新增/变更/废弃 sub-tables as applicable |
| Build system changes | `## 构建系统影响` section | Append BUILD.gn / bundle.json changes |
| Detailed design / algorithms / flow diagrams | End of `## 详细设计` chapter | Append `### <capability name>` subsections (same level as existing `### 盒模型` etc. — do NOT open a new `## ` H2) |
| Risks / compatibility | `## 风险和开放问题` table | Append new rows; `Owner` column is required |
| Task registration | `## 后续 Task 拆分` table | Append a row for the new task (Task ID / 目标 / 受影响文件 / 依赖) |

## Anti-patterns (forbidden)

❌ Opening a new `## Feat-02 位置属性 — 详细设计` at the end of design.md
❌ Adding standalone H2 chapters like `## Feat-XX 关键设计决策`, `## Feat-XX 架构图`
❌ Placing `ADR-FX-N` after `## 风险` or in a separate table
❌ Writing new data models at the end of the file instead of under `### 数据模型设计`

## Correct patterns

✅ The ADR table contains a mix like `ADR-1`...`ADR-7` + `ADR-F2-1`...`ADR-F2-7` in sequence
✅ `### 架构图` contains multiple `####` subheadings, one per Feat
✅ `## 详细设计` contains `### 盒模型`, `### 布局约束管线`, `### <Feat-XX capability>` etc. as sibling `###` subsections
✅ `## 风险和开放问题` table holds risks from all Feats mixed together
✅ `## API 签名与权限` table holds API entries from all Feats, with Feat annotations
✅ `## 构建系统影响` holds build changes from all Feats

## Verification

After merging, run:

```bash
grep -n "^## " design.md
```

Confirm the top-level chapter sequence only contains the original chapters (no `## Feat-XX ...` should appear).

```bash
grep -n "^### " design.md
```

Confirm new `### <capability>` subsections are scoped under `## 详细设计`.

## Standard top-level chapter sequence (must not be broken)

```
## 设计元数据
## 需求基线
## 上下文和现状
## 不涉及项承接
## 关键设计决策
## 设计骨架
## 后续 Task 拆分
## API 签名与权限
## 构建系统影响
## 可选设计扩展
## 详细设计
## 风险和开放问题
## 设计审批
```
