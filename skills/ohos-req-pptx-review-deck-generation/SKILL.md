---
name: ohos-req-pptx-review-deck-generation
description: Use when asked to generate, build, or create a PowerPoint / PPT / .pptx slide deck — especially polished multi-slide decks for requirement reviews, design reviews, or feature proposals, including ones with architecture/flow diagrams (boxes connected by arrows) and tables. Triggers on "生成PPT", "做个PPT", "make slides", "build a deck".
metadata:
  author: openharmony
  scope: common
  stage: requirements
  domain: pptx
  capability: review-deck-generation
  version: 0.1.0
  status: trial
  tags:
    - pptx
    - requirement-review
    - deck-generation
---

# OpenHarmony Requirement-Review PPTX Deck Generation

## Overview

Build clean, consistent 16:9 PowerPoint decks by calling a ready-made helper
library — **you supply only content; the library owns all coordinates, colors,
fonts, spacing, and arrow-drawing.**

**Core principle:** Never compute slide geometry or restyle shapes by hand.
Import `deckbuilder.Deck` and call its slide methods. Building raw `python-pptx`
shapes from scratch is the #1 cause of broken layouts, overlapping boxes,
text-only "diagrams", and wrong imports. Don't do it.

## When to Use

- Any request to make a `.pptx` / PowerPoint / slide deck
- Requirement-review, design-review, or feature-proposal decks
- Decks needing an **architecture / data-flow diagram** (real boxes + arrows)
- Decks with comparison or breakdown **tables**

When NOT to use: editing an existing `.pptx` the user already has (open it with
`python-pptx` directly), or when the user wants Markdown/PDF instead.

## Setup (do this first)

```bash
python3 -c "import pptx" 2>/dev/null || pip install python-pptx
```

The library file `deckbuilder.py` lives in this skill's directory, alongside
`oh_logo.png` (the OpenHarmony logo). Copy **both** next to your build script (or
add the skill dir to `sys.path` — `deckbuilder.py` auto-finds the logo in its own
directory). Then write ONE script that imports it and calls slide methods in order.

### Visual style (built in — do not re-implement)

The library renders a **light, understated theme** ("quiet ink + petrol"): titles
are **near-black ink** (subdued, not a loud color), a single **muted petrol** accent
carries each page's **conclusion** and primary path, structure is **soft neutral
grey**, and **amber** is reserved for change points. Every choice below is automatic,
you never set colors or coordinates:

- **The conclusion is the highlight, not the title.** Each page's 32pt title is calm
  near-black ink (`primary`); the eye is drawn instead to the `takeaway` conclusion
  line, rendered in muted petrol (`accent`) right under the title. The petrol accent
  also draws the title underline, table header, and primary data-flow arrows.
  **Everything else — secondary arrows, grid, connector bars, box borders — is soft
  grey** (`grey`). **Do NOT give cards/sections different accent colors** — that
  produces a rainbow ("不纯粹") deck. Leave `accent` unset (defaults to petrol).
- **Reserve hue changes for real meaning only:** `red` (a muted brick-red) for an
  actual risk/blocker; the built-in `★变更` change box (a light-amber fill with an
  amber badge, drawn for you when you pass `"change": True`) — change points are the
  one warm mark on an otherwise cool/neutral deck, so they pop. `green` (the logo
  green) exists but is rarely needed — don't sprinkle colors to "add color".
- **Cover & headers.** Cover has a thin petrol spine; each content page is a 32pt
  Microsoft YaHei **ink** title on white with a thin petrol underline and the page
  number top-right.
- **OpenHarmony logo, bottom-left of every page** (cover included) — added
  automatically from `oh_logo.png`. If the file is missing it's silently skipped.
- **Diagrams are real drawing boxes** — rounded rectangles joined by arrows.
- **Light, harmonious tables** — faint-petrol header with black bold text,
  white/very-light neutral zebra body, faint-petrol total row (`highlight_last=True`).
  All one quiet family, drawn for you.

## The Only API You Need

```python
from deckbuilder import Deck

deck = Deck()                    # 16:9; font defaults to "Microsoft YaHei"
# NOTE: every content slide below REQUIRES takeaway="结论：…" (the page's one-line
# conclusion) — pass it as a keyword. Omitting it raises ValueError. Only cover()
# takes no takeaway.
deck.cover(title, subtitle=None, meta_lines=[...])
deck.content_slide(title, cards, takeaway="结论：…", subtitle=None)
deck.banded_slide(title, sections, takeaway="结论：…", subtitle=None)
deck.bullets_slide(title, bullets, takeaway="结论：…", subtitle=None)
deck.table_slide(title, headers, rows, takeaway="结论：…", col_widths=None, highlight_last=False)
deck.flow_slide(title, stages, takeaway="结论：…", note=None, lane_label=None)
deck.layered_diagram_slide(title, layers, takeaway="结论：…", connect=None, note=None)
deck.architecture_slide(title, nodes, edges, takeaway="结论：…", note=None)
deck.save("output.pptx")
```

**Every page leads with its conclusion — `takeaway` is REQUIRED.** Pass
`takeaway="结论：…"` (one short sentence) to every content slide — it renders as a bold
petrol line with a petrol kicker right under the (subdued ink) title, so the
reviewer's eye lands on the point before the detail.
The title stays the topic label (`五、兼容性分析`); the `takeaway` carries the verdict
(`不改变公开 API 行为，应用无需适配`). Write an assertion, not a restatement of the
title. `subtitle` (small grey) still exists for neutral scope notes; if both are
given, `takeaway` wins the slot. **`takeaway` is mandatory: a content slide built
without it raises `ValueError` and the deck will not save.** There is no way to ship a
page without its 突出重点 — write the one-line verdict for every slide.

Page numbers auto-increment (cover is excluded). Header band, accent colors, and
spacing are automatic. **Colors are passed by name string** — `"accent"` (petrol)
and `"grey"` (soft grey) cover almost everything; `"red"` for a genuine risk;
`"green"`, `"orange"`, `"primary"` exist but are rarely the right call. **Default to
omitting `accent` (or using `"accent"`)** so the deck stays one coordinated family —
don't vary it per card just to add color.

### Quick reference — what each method takes

| Method | Key argument shape |
|--------|--------------------|
| `cover` | strings + `meta_lines=["Team", "2026-06-23"]` |
| `content_slide` | `cards=[{"title","bullets":[...]}]` (1–6 auto-grid). **Per-card `accent` is ignored — all cards render in one family** (no rainbow). For 需求评审 1/2/3 use `table_slide`, not this |
| `banded_slide` | same `sections=[{"title","bullets"}]` shape, rendered as full-width horizontal bars stacked top→bottom. **Per-section `accent` is ignored — all bars are one color.** Avoid for 需求评审 1/2/3 (use `table_slide`); the colored 横条 it used to make were the #1 "不纯粹" complaint |
| `bullets_slide` | `bullets=["text", {"text","level":1,"accent","bold"}]` |
| `table_slide` | `headers=[...]`, `rows=[[...],[...]]`, `highlight_last=True` for totals. `col_widths` are relative weights — auto-scaled to fit, never overflow |
| `flow_slide` | `stages=[{"title","lines":[...],"change":True}]` → 1 row, auto arrows |
| `layered_diagram_slide` | `layers=[{"label","nodes":[{"title","lines","change"}]}]` + optional `connect` |
| `architecture_slide` | `nodes=[{"id","title","lines","row","col","change"}]`, `edges=[{"from","to","label","dir":"f"/"both","accent"}]` — labeled directional connectors for high-level module interaction |

## Architecture diagrams (the part models get wrong)

A design/system slide MUST be a real diagram — boxes connected by arrows — not a
bullet list. Three builders, all auto-layout and auto-draw arrows. Pick by intent:

- **`flow_slide`** — one left-to-right pipeline (data flow through stages).
- **`layered_diagram_slide`** — stacked planes (e.g. control plane over data plane).
- **`architecture_slide`** — **high-level module interaction**: how a subsystem
  touches its peers. Use this for the "系统级架构 / 对 OpenHarmony 整体影响" slide.
  Labeled, directional connectors say WHAT each link is and WHICH way it flows —
  far clearer than uniform arrows. See the requirement-review template for the
  canonical OH-module example.

**Simple pipeline** — one left-to-right flow. Mark changed components with
`"change": True` (renders a light-amber box with an amber `★变更` badge + border):

```python
deck.flow_slide("System Design — Data Flow", [
    {"title": "HID device",   "lines": ["USB / BT"]},
    {"title": "normalize",    "lines": ["resolve binding"], "change": True},
    {"title": "windows mgr",  "lines": ["hit test, isolate state"], "change": True},
    {"title": "UDS dispatch",  "lines": ["consistent ids"]},
], note=["normalize resolves the binding before coordinate calc.",
         "Light-amber ★变更 boxes are the change points."])
```

**Layered diagram** — stacked planes (e.g. control plane over data plane). Each
layer is a row; `connect` draws vertical arrows between nodes by `[layer, node]`
index:

```python
deck.layered_diagram_slide("System Design — Framework", [
    {"label": "control", "nodes": [
        {"title": "Service (SA)", "lines": ["bind request"]},
        {"title": "BindHelper",   "lines": ["runtime state", "inner API"], "change": True}]},
    {"label": "data", "nodes": [
        {"title": "device",    "lines": ["event"]},
        {"title": "normalize", "lines": ["resolve"], "change": True},
        {"title": "dispatch",  "lines": ["consistent"]}]},
], connect=[[[0, 1], [1, 1]]],   # BindHelper → normalize (down arrow)
   note="Helper feeds the normalize stage.")
```

## Requirement-review decks (需求评审) — use the fixed template

When the user asks for a 需求评审 / requirement-review deck, or gives a page-by-page
brief (新增需求与工作量 → 原始需求 → 特性价值 → 系统方案 → 兼容性 → RAM/ROM → 风险
checklist → 需求拆解), **follow the 8-section structure** in
[requirement-review-template.md](references/requirement-review-template.md) instead of inventing
an outline. `examples/requirement_review_example.py` is a complete, generic fill-in deck.

What this page reliably gets wrong (the top two are the most-reported):

- **Pages 1/2/3 must be `table_slide`, never `banded_slide` / `content_slide`.** The
  bar/card builders tempt you to color each section differently → multi-colored 横条
  ("不纯粹"). Build the 字段｜内容 pages as two-column tables. (The engine also forces
  those builders to one color now, but tables are the right layout here.)
- **Every page must pass `takeaway="结论：…"`** — a topic title over a table with no
  conclusion has no 突出重点. This is enforced: a slide without `takeaway` raises
  `ValueError`, so the deck will not build until every page has its verdict.
- **Design diagrams must be 框图 (boxes + arrows), never bullet lists** — use
  `architecture_slide` / `layered_diagram_slide` / `flow_slide` for every section-4 slide.
- **Section 4's first diagram is HIGH-LEVEL module interaction** — this module ↔ the
  modules around it, as a few labeled boxes with directional connectors. Internal class
  names / private fields there read as "偏实现，看不出与其他模块的交互"; keep those in the
  control-plane/data-plane diagram and the impact table.
- **Always include 工作量评估 and RAM/ROM 评估** — total effort on P1, per-task 人月
  breakdown + 合计 row on the last page; a dedicated RAM/ROM table (新增结构/典型/极限/
  默认≈0；so 体积/资源；实测要求).
- **Mark absent brief fields `待评估 / TBD`** (需求来源/产品、适用地区、工作量人月、
  开发/设计人员、外部承诺) and list them back to the user — never fabricate them.

## Workflow

1. Install python-pptx if missing; make `deckbuilder.py` importable.
2. If the source is a spec/doc, read it and pull the real content per slide.
   Don't invent technical facts; if a number (e.g. effort) isn't given, label it
   an estimate or use `TBD`.
3. Write one build script: `Deck()` → one method call per slide → `deck.save()`.
4. Run it. Then **verify** (next section). Report the output path + slide count.

## Verification before claiming done

Always run this after building — it confirms the file opens and nothing
overflows the canvas:

```python
from pptx import Presentation
from pptx.util import Emu
p = Presentation("output.pptx"); W, H = p.slide_width, p.slide_height
bad = 0
for i, s in enumerate(p.slides):
    for sh in s.shapes:
        if sh.left is None: continue
        if sh.left < 0 or sh.top < 0 or sh.left+sh.width > W+2000 or sh.top+sh.height > H+2000:
            bad += 1; print("overflow on slide", i+1)
print("slides:", len(p.slides._sldIdLst), "overflow:", bad)   # overflow must be 0
```

No renderer (LibreOffice) is needed; the bounds check is the smoke test.

**`takeaway` is enforced — the build fails without it.** A content slide built
without `takeaway="结论：…"` raises `ValueError` naming the slide, so a deck that saves
successfully already has a conclusion on every page. If your script errors with
`slide '…' was built without takeaway=`, add the one-line verdict to that slide and
rerun — do not work around it.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Building shapes with raw `python-pptx` and hand-picked inches | Use `Deck` methods; they place everything for you |
| `from pptx.dgm...` / guessing import paths | The library already imports correctly — just `from deckbuilder import Deck` |
| Design slide is a bullet list, not a diagram | Use `flow_slide` or `layered_diagram_slide` |
| Passing `RGBColor(...)` everywhere | Pass color **names**; default to `"accent"`/`"grey"`, names map to the palette |
| Giving every card/section a different `accent` (rainbow 横条) | Don't — per-card/section colors are ignored by design; for 需求评审 1/2/3 use `table_slide` |
| Pages 1/2/3 as colored `banded_slide` bars | Use `table_slide` (字段｜内容 two-column) — the bars invite the "不纯粹" rainbow |
| Pages with no point — just a topic title over a table | Give every content slide a `takeaway="结论：…"` one-liner; it's required — a slide without it raises `ValueError` |
| Cramming 8+ cards on one slide | Max 6 per `content_slide`; split across slides |
| Putting >8 rows in one table at full font | The library auto-shrinks; still split very long tables |
| Claiming done without running it | Run the script + the overflow check, report path & slide count |

## Real-World Impact

This skill was distilled from building 11-slide OpenHarmony requirement-review
decks (cover, agenda, requirement, value, framework/module-interaction diagram,
control/data-plane change-impact, compatibility, risk checklist, task breakdown,
acceptance). The diagram slides — control/data-plane layers with badged change
points and auto-drawn arrows — are reproducible in a few lines via
`layered_diagram_slide` / `flow_slide`.
