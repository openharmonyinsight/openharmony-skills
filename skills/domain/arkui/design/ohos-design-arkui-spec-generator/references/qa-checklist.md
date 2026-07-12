# Step 1 Scope Clarification Question Bank

Batch questions as described below. Ask via your runtime's structured question tool when available; otherwise use concise plain text (the fallback, **not a reason to skip** — see SKILL.md "Questioning discipline" for the runtime-to-tool mapping). **Never stuff every question into a single call/message** — split by dimension across 1-2 waves. **After each wave, end the turn and wait** for the user response; do not infer defaults or continue to source exploration.

## Wave 1: capability scope (required)

**Question**: "Which sub-properties/APIs does this feature cover?"

How to construct it:
1. Run a quick Explore agent over the feature's source files and SDK docs to enumerate candidate sub-properties
2. List candidates using question tool with a multi-select (or a numbered plain-text list the user can pick from)
3. Always include the options "All" and "Core subset only"

Example (position properties):
- Option A: position (core positioning)
- Option B: offset (relative offset)
- Option C: markAnchor (anchor point)
- Option D: align (alignment)
- Option E: direction (layout direction)
- Option F: All 5 properties

## Wave 2: coverage breadth

**Question**: "For each property, do all setting forms need to be covered?"

Example options:
- Option A: Core form only (e.g. x/y)
- Option B: Core + edges
- Option C: Full coverage (incl. localizedEdges, Resource, percentage, etc.)

## Wave 3: design-doc strategy (only when design.md exists)

**Question**: "How should the design document be organized?"

Options:
- Option A (Recommended): **Incremental merge** into the existing design.md's chapters
- Option B: Create a separate standalone design file (only when the feature is fully independent)

If the user picks A, **explicitly state** that "content will be distributed into the existing ADR table, architecture diagram, and detailed-design chapters — no new `## Feat-XX` top-level chapter will be opened."

## Wave 4: highlight key findings (run during Step 3)

**Question**: "Which of the following design decisions should the spec emphasize?"

How to construct it:
1. After Step 2 source exploration, identify 3-7 non-obvious findings
2. Present them using question tool with a multi-select (or a numbered plain-text list)

Candidate finding types:
- Storage-layer split (which properties live in RenderContext vs LayoutProperty)
- API version behavior changes (e.g. different behavior before/after API 12)
- Mutual-exclusion priority (ordering when multiple properties are set together)
- Default values / special values (undefined, negative, NaN handling)
- RTL / localization behavior
- Dirty-flag strategy (`PROPERTY_UPDATE_MEASURE` vs `LAYOUT` vs none)

## Questioning discipline

- **Never skip a question**: if no structured question tool is available, ask the same questions as concise plain text (numbered list). Silence is not confirmation — re-ask instead of inferring a default.
- **One wave per turn**: after asking, end the turn and wait. Do not continue to source exploration or writing in the same turn.
- At most 4 questions per call/message
- At most 4 options per question
- Option labels short (1-5 words); use `description` for details (in plain text, put the detail inline after the label)
- Recommended option labeled `(Recommended)` and placed first
- Structured tools let the user pick an option or type a custom answer; in plain text, explicitly invite a free-form reply (e.g. "或直接回复你的选择")
