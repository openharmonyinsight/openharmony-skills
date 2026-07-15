# Common Mistakes

The top mistakes when building OpenHarmony requirement-review decks, and their
fixes. For the full builder API and palette rules, see SKILL.md.

| Mistake | Fix |
|---------|-----|
| Hand-assembling a 需求评审 deck page by page (and picking a wrong builder) | Use `deck.requirement_review_deck(spec)` — one call, fixed 8 pages |
| 价值/设计页做成 `content_slide` 四格 / bullet 列表 | 用 `value_slide` / `design_slide`（左文右图；设计页右侧传 `diagram=`）— the library warns if you don't |
| Building shapes with raw `python-pptx` and hand-picked inches | Use `Deck` methods; they place everything for you |
| `from pptx.dgm...` / guessing import paths | The library already imports correctly — just `from deckbuilder import Deck` |
| Design slide is a bullet list, not a diagram | Use `flow_slide` or `layered_diagram_slide` |
| Passing `RGBColor(...)` everywhere | Pass color **names**; default to `"accent"`/`"grey"`, names map to the palette (见 色彩不变量) |
| Giving every card/section a different `accent` (rainbow 横条) | Don't — per-card/section colors are ignored by design; for 需求变更评审 4–7 use `table_slide` (见 色彩不变量) |
| Pages 4–8 as colored `banded_slide` bars | Use `table_slide` (分项｜内容 / 计划宽表) — the bars invite the "不纯粹" rainbow |
| Pages with no point — just a topic title over a table | Give every content slide a `takeaway="结论：…"` one-liner; it's required — a slide without it raises `ValueError` |
| Cramming 8+ cards on one slide | Max 6 per `content_slide`; split across slides |
| Putting >8 rows in one table at full font | The library auto-shrinks; still split very long tables |
| Claiming done without running it | Run the script + the overflow check, report path & slide count |
