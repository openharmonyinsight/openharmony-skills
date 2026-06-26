# Requirement-Review Deck Template (OpenHarmony 需求评审)

A fixed section structure for OpenHarmony-style requirement-review decks. When a
user asks for a "需求评审 PPT" or gives a page-by-page brief, **build these
sections in order** rather than inventing your own outline.

## The sections (+ cover)

Each section is one slide unless noted. Section 4 (技术方案) usually spans 2–3
slides (`可分页输出`). Use `table_slide` for the section-1/2/3 field pages (a
two-column 字段｜内容 table reads cleaner and aligns with the matrix/checklist
pages) as well as for matrices/checklists, and the diagram builders for section 4.
`banded_slide` (full-width 横框, stacked top→bottom) is an acceptable fallback for
1/2/3 only when the brief is genuinely prose with no field structure.

| # | Slide title | Builder | Required fields to cover |
|---|-------------|---------|--------------------------|
| — | Cover | `cover` | 标题、子标题、模块/日期 |
| 1 | 需求性质与工作量概览 | `table_slide` | 是否新增需求；复杂度驱动；**总工作量估算**（详见拆解页） |
| 2 | 原始需求描述 | `table_slide` | 需求来源/产品；需求场景；需求描述；特性概述；影响范围与限制；适用范围/地区/产品 |
| 3 | 特性及价值点 | `table_slide` | 用户痛点；需求价值；功能点与主要场景；可量化目标；支持产品范围 |
| 4 | 系统设计方案 (1/n) | `architecture_slide` | **框图**：本模块 ↔ 周边模块交互（见下） |
| 4 | 系统设计方案 (2/n) | `layered_diagram_slide` | 控制面/数据面拆分 + 关键变更点（框图） |
| 4 | 系统设计方案 (3/n) | `table_slide` | 数据结构变更／外部接口变更／外部依赖／性能功耗／关键KPI／对用户与周边领域影响 |
| 5 | 兼容性分析 | `table_slide` | 系统机制变化／权限管理变化／API行为变化／其它行为变化／适配方案与计划 |
| 6 | RAM / ROM 评估 | `table_slide` | RAM（新增结构/典型/极限/默认≈0）；ROM（so体积/资源）；实测要求 |
| 7 | 风险 Checklist | `table_slide` | 使用习惯／安全风险／合法合规／外部承诺／性能·功耗·RAM·ROM／其它依赖 |
| 8 | 需求拆解列表（工作量） | `table_slide` (`highlight_last=True`) | 子任务｜内容｜开发｜设计｜工作量(人月)｜**预计代码行数(估算)**；末行合计 |

## Five rules that matter most

**0. Every page leads with its conclusion.** Pass `takeaway="结论：…"` to every
section slide — one short verdict sentence rendered bold petrol under the (ink) title. The
numbered title stays the topic (`五、兼容性分析`); the takeaway states the finding
(`不改变公开 API 行为，应用无需适配`). A reviewer should get each page's point from
the takeaway alone, before reading the table.

**1. Diagrams are block diagrams (框图), never bullet lists.** Every section-4 design
slide must be boxes-and-arrows built with `architecture_slide` / `layered_diagram_slide`
/ `flow_slide`. A design slide that is a card/bullet list is wrong.

**2. The architecture slide is HIGH-LEVEL module interaction.** Section 4's first
diagram shows how THIS subsystem interacts with the modules around it — as a few
labeled boxes joined by **labeled, directional connectors**. Do NOT fill it with
internal class names / private fields; that reads as "偏实现，看不出与其他模块的交互".
Put the internal control-plane/data-plane split on the SECOND section-4 slide, and
code-level field changes in the impact TABLE. Use `architecture_slide`: central
module in the grid center, peers around it; every edge gets a **label** (what the
link is) and a **direction** — `dir:"f"` for a data/output flow, `dir:"both"` for a
依赖/查询 relationship. State the control-plane vs data-plane split in the Notes box.

**3. Always include 工作量评估 and RAM/ROM 评估.** Effort: break the work into
work-packages, size each in 人月 (rough scale S=0.5 / M=1 / L=2, or explicit), show
the **total on P1** and the **per-task breakdown + a 合计 row** on the last page
(`highlight_last=True`). The breakdown table carries a **预计代码行数(估算)** column
right after 工作量(人月); estimate it as **人月 × 500 行**（约定基准：1 人月 ≈ 500 行代码）
and label the column `估算` (it is an estimate, not measured). RAM/ROM: a dedicated table — RAM rows (新增结构估算 / 典型场景
/ 极限场景 / 默认≈0 懒创建) and ROM rows (so 体积变化 / 是否新增资源) + an "实测要求" row.
If the design doc gives real numbers use them; otherwise label estimates `估算` and
the measured values `实现阶段输出`.

**4. Never invent missing facts.** Frequently-absent brief fields: 需求来源/产品、
适用地区、工作量人月、开发/设计人员、外部承诺. Mark each `待评估 / TBD` or `待产品确认`,
and list them back to the user as "needs your input" — do not fabricate a product
name, region, or effort number.

## Module-interaction diagram pattern (section 4, slide 1)

`architecture_slide` places module boxes on a `row`/`col` grid and draws labeled,
directional connectors between them — the central module in the middle, peers
around it. Rename the generic roles below to the real modules your feature touches.

```python
deck.architecture_slide("四、系统设计方案（1/3）：本模块与周边模块交互（框图）", [
    {"id": "svc", "title": "调用方服务", "lines": ["发起请求"], "row": 0, "col": 0},
    {"id": "app", "title": "应用",       "lines": ["结果消费"], "row": 0, "col": 1},
    {"id": "drv", "title": "驱动 / HAL", "lines": ["数据来源"], "row": 1, "col": 0},
    {"id": "me",  "title": "本模块（目标子系统）", "lines": ["本需求新增能力"], "row": 1, "col": 1, "change": True},
    {"id": "pc",  "title": "周边服务 C", "lines": ["输出对接"], "row": 1, "col": 2},
    {"id": "src", "title": "外部输入源", "lines": ["<设备/数据>"], "row": 2, "col": 0},
    {"id": "pa",  "title": "周边服务 A", "lines": ["信息查询"], "row": 2, "col": 1},
    {"id": "pb",  "title": "周边服务 B", "lines": ["拓扑/状态"], "row": 2, "col": 2},
], edges=[
    {"from": "src", "to": "drv", "label": "原始输入",      "dir": "f",    "accent": "accent"},
    {"from": "drv", "to": "me",  "label": "数据/事件",      "dir": "f",    "accent": "accent"},
    {"from": "svc", "to": "me",  "label": "请求 (Binder)",  "dir": "f",    "accent": "accent"},
    {"from": "me",  "to": "app", "label": "结果输出",       "dir": "f",    "accent": "accent"},
    {"from": "me",  "to": "pa",  "label": "查询/依赖",      "dir": "both", "accent": "grey"},
    {"from": "me",  "to": "pb",  "label": "状态/拓扑",      "dir": "both", "accent": "grey"},
    {"from": "me",  "to": "pc",  "label": "输出对接",       "dir": "f",    "accent": "accent"},
], note=[
    "青绿＝数据/输出/请求主链路；灰色＝依赖/查询关系。",
    "用 2 种中性色把同类关系归一，避免每条边一个颜色显得杂乱。",
])
```

**Keep the edge palette to ~2 neutral colors** — petrol (`accent`) for data/output/
request flows, grey for 依赖/查询. (Reserve amber `orange` for `change` boxes, not
edges.) A different color per edge reads as rainbow clutter; grouping by relation
type is what makes the diagram look coordinated. Edge labels auto-fit their text
width and `layered_diagram_slide` caps + centers each layer's boxes, so rows with
different node counts still align.

Layout tips: keep peers in **distinct grid directions** from the center so
connectors don't cross boxes; horizontal edges connect to side mid-points,
vertical edges to top/bottom mid-points (handled automatically). Use `dir:"both"`
sparingly — only for genuine query/dependency links.

## Full worked example

`requirement_review_example.py` in this directory builds the complete deck (cover +
8 sections, section 4 = 3 slides) as a **generic fill-in template** — every string
is a `<placeholder>` and the effort/RAM/ROM numbers are examples. Copy it, replace
the placeholders and module names, keep the structure. It passes the overflow smoke
test and every page fills the canvas.
