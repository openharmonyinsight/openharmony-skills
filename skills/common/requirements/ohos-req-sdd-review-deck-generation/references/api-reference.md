# API Quick Reference — what each method takes

> 本文件从 SKILL.md 外置，提供 `deckbuilder.Deck` 各方法的参数速查。
> 完整用法示例见 `examples/requirement_review_oneshot.py` 和 `examples/requirement_review_example.py`。

## 方法参数速查表

| Method | Key argument shape |
|--------|--------------------|
| `requirement_review_deck` | `spec={...}` — whole 8-page 需求变更评审 in one call. **Preferred for review decks.** Missing fields → 待评估/TBD. See `examples/requirement_review_oneshot.py` |
| `cover` | strings + `meta_lines=["Team", "2026-06-23"]` |
| `content_slide` | `cards=[{"title","bullets":[...]}]` (1–6 auto-grid). **Per-card `accent` is ignored — all cards render in one family** (no rainbow). For 需求变更评审 4–7 use `table_slide`, not this |
| `banded_slide` | same `sections=[{"title","bullets"}]` shape, rendered as full-width horizontal bars stacked top→bottom. **Per-section `accent` is ignored — all bars are one color.** Avoid for 需求变更评审 4–7 (use `table_slide`); the colored 横条 it used to make were the #1 "不纯粹" complaint |
| `bullets_slide` | `bullets=["text", {"text","level":1,"accent","bold"}]` |
| `table_slide` | `headers=[...]`, `rows=[[...],[...]]`, `highlight_last=True` for totals. `col_widths` are relative weights — auto-scaled to fit, never overflow |
| `flow_slide` | `stages=[{"title","lines":[...],"change":True}]` → 1 row, auto arrows |
| `layered_diagram_slide` | `layers=[{"label","nodes":[{"title","lines","change"}]}]` + optional `connect` |
| `architecture_slide` | `nodes=[{"id","title","lines","row","col","change"}]`, `edges=[{"from","to","label","dir":"f"/"both","accent"}]` — labeled directional connectors for high-level module interaction |
| `value_slide` | `background=[...]`, `features=[...]`, `scope=[...]`, `image=None`. Two-column 需求价值描述 page (see SKILL.md 需求价值描述 section). `takeaway` optional |
| `design_slide` | `design=[...]`, `changes=[...]`, `extra=[{"heading","lines"}]`, `image=None`. Two-column 需求设计方案 page (see SKILL.md 需求设计方案 section). `takeaway` optional |

## takeaway 参数说明

- **所有 content slide 必须传 `takeaway="结论：…"`**（一行结论），渲染为标题下方红色加粗行
- 省略 `takeaway` 会抛出 `ValueError`，deck 无法保存
- `cover()` 不需要 `takeaway`
- `value_slide` / `design_slide` 的 `takeaway` 为可选（这两页以分栏内容为主，非一行结论）

## 颜色参数

颜色通过**名称字符串**传递，不要用 `RGBColor(...)`：

| 名称 | 用途 |
|------|------|
| `"accent"` (red) | 默认强调色 — 结论、主路径箭头、标题下划线 |
| `"grey"` | 次要元素 — 网格、连接条、边框 |
| `"red"` | 真正的风险/阻塞项 |
| `"green"` | logo 绿，少用 |
| `"orange"` | 变更点（由 `"change": True` 自动渲染，无需手传） |
| `"primary"` | 近黑色标题墨 |

**默认省略 `accent` 参数**（自动使用红色），不要为每个卡片/分区设置不同颜色。
