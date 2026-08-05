# Issue KB Page Template

Each issue KB page follows this exact structure:

```markdown
# <问题标题> Issue Context

> 文档版本：v1.0
> 更新时间：<YYYY-MM-DD>
> 来源：`docs/context_registry.json` 主题 `<IssueID>`
> 关联功能域：<FuncID 或 FuncID 列表>

## 问题概述

<1–2 句话概括问题现象，面向排查者快速判断是否命中>

典型表现：
- <表现 1>
- <表现 2>
- <表现 3>

## 关联模块

| kind | role | name | evidence | confidence |
|------|------|------|----------|------------|
| component | symptom_surface | <问题表现的组件> | <源码/PR/用户描述> | verified / inferred / user_claimed / unknown |
| architecture | root_cause_owner | <根因所属模块> | <源码/PR/用户描述> | verified / inferred / user_claimed / unknown |
| capability | fix_location | <修复所在模块> | <PR diff> | verified / inferred / user_claimed / unknown |

kind: `component` / `capability` / `architecture`
role: `symptom_surface` / `trigger` / `root_cause_owner` / `fix_location` / `dependency`

## 根因分类

| 根因类别 | 触发条件 | 典型场景 |
|----------|----------|----------|
| <类别 A> | <条件> | <场景描述> |
| <类别 B> | <条件> | <场景描述> |
| <类别 C> | <条件> | <场景描述> |

## 排查路径

### 快速判断

<3–5 个判断步骤，帮助排查者快速定位根因类别>

### 详细排查

#### <类别 A> 排查

| 步骤 | 操作 | 预期结果 | 失败则 |
|------|------|----------|--------|
| 1 | <操作描述> | <正常结果> | <继续下一步或切换类别> |
| 2 | <操作描述> | <正常结果> | ... |

关键代码定位：
- <源码路径/函数名>：<定位说明>
- <源码路径/函数名>：<定位说明>

#### <类别 B> 排查

（同上格式）

## 修复方案

| 根因类别 | 修复策略 | 关键代码改动点 | 修复/缓解变更 | 关系证据 |
|----------|----------|---------------|---------------|----------|
| <类别 A> | <策略描述> | <改动路径> | <PR号或Commit哈希> (fixed) | <git blame/PR描述/diff证据> |
| <类别 B> | <策略描述> | <改动路径> | <PR号或Commit哈希> (mitigated) | <证据> |

## 关联变更

| 变更编号 | 变更简述 | 根因类别 | 变更关系 | 证据 | 确信度 |
|----------|----------|----------|----------|------|--------|
| CHG-01 | <简述> | <类别> | introduced / exposed / fixed / mitigated / follow_up / related / unknown | <证据来源> | verified / inferred / user_claimed / unknown |
| CHG-02 | <简述> | <类别> | fixed | <回归区间/PR diff> | verified |

## 预防措施

- <预防建议 1>
- <预防建议 2>

## 相关主题

- <关联代码型 KB 页面路径>
- <关联 Spec 域路径>
- <关联其他问题 KB>
```

## context_registry.json Registration

Each issue KB must be registered in `docs/context_registry.json`. The entry shape differs from code-based KBs:

```json
{
    "id": "MeasureInfiniteLoop",
    "name": "Measure Infinite Loop",
    "name_cn": "测量无限循环",
    "kind": "issue",
    "category": "layout",
    "keywords": [
        "MeasureInfiniteLoop",
        "测量无限循环",
        "NeedAdditionalLayout",
        "layout loop",
        "布局死循环",
        "layout count exceeds"
    ],
    "aliases": [
        "布局循环",
        "测量循环",
        "附加布局循环"
    ],
    "kb": "docs/kb/issues/layout/measure-infinite-loop.md",
    "func_ids": ["03-01-01"],
    "status": "active",
    "last_verified": "<YYYY-MM-DD>"
}
```

Key differences from code-based entries:
- `kind` is `"issue"` — ace_engine's `validate_context.py` and `kb_search.py` natively support this kind; issue KBs are exempt from `spec_status` and standard KB section validation
- `func_ids` is an array — allows associating multiple FuncIDs with a single issue KB; all listed FuncIDs are indexed for search
- No `spec_status` — issues are not tied to a single spec; `validate_context.py` skips this field for `kind: "issue"`
- No `source_paths`, `api_paths`, `test_paths` — those belong to code-based KBs
- No `spec_domain` — issues are not tied to a single spec domain

## Change Relationship Taxonomy

When referencing PRs, commits, or issues in the "关联变更" table, use these relationship values:

| Relationship | Meaning | Evidence required |
|--------------|---------|-------------------|
| `introduced` | This change introduced the bug or regression | Regression window, git blame, PR description showing the change |
| `exposed` | This change exposed a pre-existing issue | Test or scenario that surfaced the latent bug |
| `fixed` | This change directly fixes the root cause | PR diff showing the fix, linked test verification |
| `mitigated` | This change reduces impact but doesn't fix root cause | PR description stating partial workaround |
| `follow_up` | Supplemental: tests, refactoring, diagnostic enhancement | PR adding test cases or improved logging |
| `related` | Connected but causal relationship unproven | Any cross-reference without causation evidence |
| `unknown` | Evidence insufficient to determine relationship | Use when no regression window, blame, or diff available |

Only mark `introduced` or `fixed` when there is concrete evidence (regression window, git blame, PR description, or diff). Otherwise use `related` or `unknown`.

Confidence levels:

| Level | Meaning |
|-------|---------|
| `verified` | Confirmed by source code, test, or PR diff |
| `inferred` | Derived from code analysis but not directly verified |
| `user_claimed` | Stated by user without independent verification |
| `unknown` | No evidence available |
