# Step 1 Scope Clarification Question Bank

When using `AskUserQuestion`, batch questions as described below. **Never stuff every question into a single call** — split by dimension across 1-2 waves.

## Wave 1: capability scope (required)

**Question**: "Which sub-properties/APIs does this feature cover?"

How to construct it:
1. Run a quick Explore agent over the feature's source files and SDK docs to enumerate candidate sub-properties
2. List candidates in `AskUserQuestion` with `multiSelect: true`
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
2. Present them in `AskUserQuestion` with `multiSelect: true`

Candidate finding types:
- Storage-layer split (which properties live in RenderContext vs LayoutProperty)
- API version behavior changes (e.g. different behavior before/after API 12)
- Mutual-exclusion priority (ordering when multiple properties are set together)
- Default values / special values (undefined, negative, NaN handling)
- RTL / localization behavior
- Dirty-flag strategy (`PROPERTY_UPDATE_MEASURE` vs `LAYOUT` vs none)

## Questioning discipline

- At most 4 questions per `AskUserQuestion` call
- At most 4 options per question
- Option labels short (1-5 words); use `description` for details
- Recommended option labeled `(Recommended)` and placed first
- Never include an "Other" option in the list (the system provides it automatically)
