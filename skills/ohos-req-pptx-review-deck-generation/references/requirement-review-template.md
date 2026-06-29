# Requirement-CHANGE-Review Deck Template (OpenHarmony 需求变更评审)

A fixed page structure for OpenHarmony-style **需求变更评审** decks. When a user
asks for a "需求变更评审 PPT" or gives a page-by-page brief, **build these pages in
order** rather than inventing your own outline.

This template has **7 pages (+ cover counts as page 1)**. Pages 2–3 reuse the two
two-column 左文右图 builders unchanged; pages 4–7 are the change-review core, built
as `table_slide` field tables.

> ⚠️ **The two failures reviewers keep reporting — do NOT repeat them:**
> 1. **Multi-colored horizontal bars / rainbow cards.** Build the field pages (4–7)
>    with **`table_slide`**, NOT `banded_slide` / `content_slide`. The bar/card
>    builders invite "give each section its own color" → a rainbow ("不纯粹") deck.
>    A two-column 分项｜内容 table is the correct, cleaner layout.
> 2. **Pages with no 突出重点.** EVERY `table_slide` page must pass `takeaway="结论：…"`.
>    A page that is just a topic title over a table has no point. **`takeaway` is
>    mandatory: a content page built without it raises `ValueError` and the deck will
>    not save** — so you cannot ship a page that lacks its 突出重点. (`value_slide` /
>    `design_slide` take `takeaway` optionally — they lead with their sections.)

## The pages (in order)

| # | Page (slide) title | Builder | Required fields to cover |
|---|--------------------|---------|--------------------------|
| 1 | Cover | `cover` | 标题、子标题、模块/日期 |
| 2 | 需求价值描述 | `value_slide` | 背景；特性及价值点；需求收益（影响）范围；右侧场景图 |
| 3 | 需求设计方案 (可多页) | `design_slide` | 设计方案重点；变更点及影响；右侧架构框图（`diagram=`）|
| 4 | 需求变更背景 | `table_slide` | ① 需裁剪/变更的需求说明（含原始需求/编号、特性概述与影响、使用场景）；② 原始被接纳时的决策纪要（SIG 评审通过记录）|
| 5 | 需求变更影响性分析 | `table_slide` | 北向应用开发者／南向开发者／分布式设备／系统开发者（跨子系统依赖）／设备使用者 —— 共 5 行 |
| 6 | 兼容性分析 | `table_slide` | 是否涉及应用兼容性；兼容性包括（机制/权限/API行为/其它）；兼容性方案；应用适配方案和计划 |
| 7 | 风险评估 | `table_slide` | **固定 2 列 8 行** checklist（见下）|

Pages 2 and 3 are **unchanged** from the standard 需求价值描述 / 需求设计方案
builders — see SKILL.md「需求价值描述 / 需求设计方案 — the two-column pages」. Do not
restyle them. The change-review content lives entirely on pages 4–7.

## Five rules that matter most

**0. Every field page leads with its conclusion — `takeaway` is REQUIRED.**
Pages 4–7 each pass `takeaway="结论：…"` — one short verdict sentence rendered bold
petrol under the (ink) title. The title stays the topic (`五、兼容性分析`); the
takeaway states the finding (`不改变公开 API 行为，应用无需适配`). Write an
**assertion**, not a restatement of the title. A content page built without
`takeaway` raises `ValueError` and the deck will not save.

**1. Keep pages 2–3 (价值/设计) as the two-column 左文右图 builders.** Do NOT convert
them to tables and do NOT change their typography. Page 3's right column must be a
real **框图** (pass `diagram=` layers, or `image=` an architecture picture) — never a
bullet list.

**2. Pages 4–7 are 分项｜内容 field tables.** Two columns: a left「分项 / 影响对象 /
评估项」label column and a right「内容 / 影响分析 / 结论·说明」column. Use `col_widths`
to keep the label column narrow (~1.8–2.6) and let the content column take the rest.

**3. Page 7 风险评估 is a fixed 2-column, 8-row checklist — these 8 rows, in order:**
   1. 对性能、功耗、RAM/ROM 是否有影响
   2. 是否存在其他依赖关系？
   3. 是否有安全风险
   4. 是否涉及合法 / 合规问题？
   5. 是否涉及外部承诺？
   6. 是否开源
   7. 是否涉及 AI
   8. 隐私风险特性识别

Header is `["评估项", "结论 / 说明"]`. Answer each row with a verdict (是/否/待评估)
plus a one-line reason — never leave a row blank.

**4. Never invent missing facts.** Frequently-absent fields: 需求编号、SIG 决策纪要、
适用地区/产品、外部承诺、合规/安全结论. Mark each `待评估 / TBD` or `待产品确认`, and
list them back to the user as "needs your input" — do not fabricate a 需求编号, a SIG
评审结论, a product name, or a region.

## Page 4 — 需求变更背景 (two sections)

```python
deck.table_slide("四、需求变更背景",
    ["分项", "说明"],
    [
        ["需裁剪/变更的需求说明\n（重点说明 2C/2D 详细价值及产生影响）",
         "原始需求（含需求背景及需求描述，如有需求编号一并附上）；"
         "概述软件所有特性/功能及该需求产生的影响 —— 给评审人一个简洁视角，"
         "快速判断有无该需求的差别；使用场景说明。"],
        ["原始被接纳时的决策纪要",
         "提供该需求最初通过 SIG 评审的记录（评审结论 / 日期 / 决策要点）。"],
    ],
    takeaway="结论：…（一句话点明本次变更的对象与核心理由）",
    col_widths=[2.6, 7])
```

- **段一「需裁剪/变更的需求说明」** —— 重点说明 **2C/2D** 的详细价值和产生的影响。
  含：原始需求（背景+描述，**如有需求编号一并附上**）；软件所有特性/功能概述 + 需求产生
  的影响（**一个简洁视角，让评审人快速判断有无该需求的差别**）；使用场景说明。
- **段二「原始被接纳时的决策纪要」** —— 提供 **SIG 评审通过的记录**。若无原始纪要，标
  `待评估 / TBD` 并向用户索取。

## Page 5 — 需求变更影响性分析 (five rows)

```python
deck.table_slide("五、需求变更影响性分析",
    ["影响对象", "影响分析"],
    [
        ["北向应用开发者",
         "是否涉及 API 变更；是否影响调试调测；对开发者体验影响（上架包尺寸、编译速度等）。"],
        ["南向开发者",
         "对南向芯片平台影响；对 OEM 适配厂商是否有影响。"],
        ["分布式设备",
         "是否涉及分布式场景体验影响（影响是什么）；是否涉及多设备互联互通调试影响（影响是什么）。"],
        ["系统开发者\n（跨子系统/部件依赖）",
         "对 <xxx> 子系统影响；若涉及架构影响，需提供评审意见。"],
        ["设备使用者\n（性能/功耗/功能/体验）",
         "是否涉及原型机/PC 等产品影响（影响的设备列表）；是否有对应领域意见；"
         "对性能功耗的影响；对用户体验的影响。"],
    ],
    takeaway="结论：…（一句话点明影响面最大/最需关注的对象）",
    col_widths=[2.4, 7])
```

Exactly **5 rows, these objects in this order**: 北向应用开发者 → 南向开发者 →
分布式设备 → 系统开发者（跨子系统/部件依赖）→ 设备使用者（性能/功耗/功能/体验）.

## Page 6 — 兼容性分析

```python
deck.table_slide("六、兼容性分析",
    ["分项", "内容"],
    [
        ["是否涉及应用兼容性",
         "是/否；如涉及，需提供兼容性方案与应用/设备适配方案及计划。"],
        ["兼容性包括",
         "系统机制或功能发生变化；系统权限管理发生变化；API 行为发生变化；"
         "其他导致应用行为发生变化的因素。"],
        ["兼容性方案",
         "…（如涉及兼容性，给出方案；不涉及则填「无兼容性影响」）。"],
        ["应用适配方案和计划",
         "…（受影响应用清单、适配方式、时间计划）。"],
    ],
    takeaway="结论：…（是否影响应用兼容性 + 是否需适配）",
    col_widths=[2.2, 7])
```

「兼容性包括」四类判定因素是固定的：**系统机制/功能变化、系统权限管理变化、API 行为
变化、其他导致应用行为变化的因素**。若任一为「是」，必须在「兼容性方案」「应用适配方案
和计划」两行给出实质内容，而非留空。

## Page 7 — 风险评估 (fixed 2×8 checklist)

```python
deck.table_slide("七、风险评估",
    ["评估项", "结论 / 说明"],
    [
        ["对性能、功耗、RAM/ROM 是否有影响", "…"],
        ["是否存在其他依赖关系？",            "…"],
        ["是否有安全风险",                   "…"],
        ["是否涉及合法 / 合规问题？",         "…"],
        ["是否涉及外部承诺？",               "…"],
        ["是否开源",                        "…"],
        ["是否涉及 AI",                     "…"],
        ["隐私风险特性识别",                 "…"],
    ],
    takeaway="结论：…（主要风险点 + 需要的后续动作/评审）",
    col_widths=[3.0, 6])
```

These **8 rows are fixed** — same wording, same order, no additions or omissions.
Each answer is a verdict (是/否/待评估) + one-line reason.

## Full worked example

`examples/requirement_review_example.py` in this skill builds the complete deck
(cover + 价值 + 设计 + 变更背景 + 影响性分析 + 兼容性 + 风险) as a **generic fill-in
template** — every string is a `<placeholder>`. Copy it, replace the placeholders,
keep the structure. It passes the overflow smoke test and every page fills the canvas.
