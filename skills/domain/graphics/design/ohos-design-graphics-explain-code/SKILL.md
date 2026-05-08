---
name: ohos-design-graphics-explain-code
description: Use this skill whenever you need to explain, analyze, or document code — including understanding how code works, tracing call flows, mapping architecture, documenting modules or features, analyzing business logic, or generating technical documentation with diagrams. Triggers on phrases like "explain this code", "how does this work", "document this module", "generate docs for", "draw a diagram of", "what's the architecture", or "analyze the flow". This skill uses interactive confirmation at each stage and produces markdown documentation with mermaid class and sequence diagrams.
metadata:
  author: openharmony
  scope: domain
  stage: design
  domain: graphics
  capability: explain-code
  version: 0.1.0
  status: stable
---

# Explain Code

Interactive code analysis and documentation that ensures accuracy through user confirmation at key stages.

## Workflow

Follow this three-phase workflow to create accurate code documentation:

### Phase 1: Understand and Align

Before diving into the code, ensure you understand what needs to be analyzed:

1. **Identify the target**: What code, module, or feature needs to be explained?
2. **Clarify scope**: Which files, classes, or functions are included?
3. **Understand context**: What is the user's goal? What questions do they have?
4. **Align on approach**: Discuss any uncertainties until the user confirms there are no further questions.

**Ask clarifying questions when:**
- The target module or scope is ambiguous
- Multiple interpretations exist
- You need to understand the user's depth requirement (high-level vs detailed)
- Context is missing (e.g., "explain the payment flow" - which payment system?)

**Continue only when the user confirms alignment.**

**If the codebase appears large (>50 files)**: before Phase 2 exploration,
MUST read the entire file structure first — do a tree walk of the module
directory to avoid scattershot reading.

### Phase 2: Present Call Flow for Confirmation

Before writing full documentation, present the code's call flow or architecture for verification:

1. **Explore the codebase** to understand the flow:
   - Use codebase exploration tools for comprehensive project structure mapping
   - Use file reading tools for targeted analysis of specific files
   - Use search/grep tools to find patterns, references, and dependencies

2. **Present the call flow** showing:
   - Entry points (API endpoints, main functions, event handlers)
   - Key components and their interactions
   - Data flow through the system
   - Exit points or return values

3. **Format the flow** as either:
   - A numbered list of steps
   - A simple text-based diagram
   - A high-level mermaid sequence diagram

4. **Ask for confirmation**: "Is this understanding of the flow correct? Any missing or incorrect steps?"

**Do NOT proceed to documentation until the user confirms the flow is accurate.**

#### Handling Disagreement

If the user disagrees with your call flow:

1. **Don't defend** — ask which step is wrong and what should replace it
2. **Show the evidence** — cite the specific file and line that led to
   your interpretation
3. **Re-present only the corrected segment** — not the entire flow
4. **Converge within 2 rounds** — if disagreement persists after two
   corrections, switch to a lighter format (bullet list, no diagrams)
   and flag remaining ambiguity in the "Notes" section

#### Edge Cases

- **Code with no clear entry point** (event-driven, message-loop):
  Identify the event registration sites, then trace one complete
  event cycle from registration through handling to response.

- **Code with circular module dependencies**:
  Document each module independently first, then add a cross-reference
  section describing the circularity with a note about initialization order.

- **Microservice / distributed code**:
  Each service gets its own sub-document. The main document is a
  sequence diagram showing inter-service communication with links to
  per-service detail docs.

### Phase 3: Generate Documentation

Once the call flow is confirmed, create comprehensive documentation:

1. **Create a markdown file** in the project root directory:
   - Name it descriptively (e.g., `user-authentication-flow.md`, `payment-processing-docs.md`)
   - Use a clear, professional title

2. **Include the following sections** (adapt as needed for the code being documented):

   ``````markdown
   # [Feature/Module Name] - Code Documentation

   ## Overview
   [1-2 paragraphs describing what this code does and its purpose]

   ## Architecture
   [High-level description of the main components and their roles]

   ## Flow Description
   [Detailed step-by-step explanation of how the code works]

   ## Key Components

   ### [Component 1]
   [Description of what this component does]

   ### [Component 2]
   [Description of what this component does]

   ## Class Diagram

   ```mermaid
   classDiagram
   [Classes and their relationships]
   ```

   ## Sequence Diagram

   ```mermaid
   sequenceDiagram
   [Interaction flow between components]
   ```

   ## Notes
   [Any important caveats, edge cases, or design decisions]
   ``````

3. **Include mermaid diagrams**:
   - **Class diagram**: Show the structure (classes, interfaces, relationships)
   - **Sequence diagram**: Show the runtime interaction between components
   - **MANDATORY — READ ENTIRE FILE**: Before creating ANY mermaid diagram,
     you MUST read [`references/mermaid-guide.md`](references/mermaid-guide.md)
     completely from start to finish.
     **NEVER set any range limits when reading this file.**

4. **Ensure clarity**:
   - Use precise technical terms matching the actual code
   - Include file paths and line numbers for key functions (e.g., `UserService.login()` in `src/services/user.ts:45`)
   - Explain the "why" not just the "what"
   - Keep descriptions concise but complete

#### When NOT to use a diagram

| Situation | Action |
|-----------|--------|
| Module has <3 meaningful types | Skip class diagram; use text descriptions |
| Flow is purely linear with no branches | Skip sequence diagram; use numbered list |
| User explicitly asks "no diagrams, just text" | Respect the request |
| Documentation target is a config file or data schema | Use table, not diagram |

## Anti-Patterns — NEVER Do These

These mistakes cost real hours in practice. Every item below
represents a documentation failure Claude has observed in the wild.

### Exploration anti-patterns

- **NEVER start documenting before understanding the user's goal** —
  ask "What decision will this document help you make?" first.
  Accurate docs nobody asked for are waste.

- **NEVER trust a single-pass exploration** — error handlers, callbacks,
  and edge branches are where the most important behavior lives. Do a
  second pass specifically searching for:
  - `return err`, `return nullptr`, `ERROR_CODE_*` (error paths)
  - Callbacks, listeners, observers (async flows)
  - `#ifdef`, feature flags, platform-specific code (conditional logic)

- **NEVER explore without tracking provenance** — every claim in the
  document must trace to a real file path and line number. If you
  can't cite the source, delete the claim.

### Diagram anti-patterns

- **NEVER create diagrams without code provenance** — every arrow in a
  sequence diagram must correspond to an actual function call at a
  specific line. Diagrams without code anchors are fiction.

- **NEVER force a class diagram when the code has no classes** — for
  C-style modules, procedure-heavy code, or data-pipeline code, use a
  flowchart or sequence diagram instead.

- **NEVER put more than 8 participants in a single sequence diagram** —
  split into focused views. An "overview diagram" with 20 participants
  communicates nothing.

- **NEVER include private helper methods in architecture diagrams** —
  if a method is not called across module boundaries, it doesn't belong
  in the architecture view.

### Confirmation anti-patterns

- **NEVER skip confirmation to save time** — a wrong document is worse
  than no document. Skipping Phase 2 confirmation produces confident
  but incorrect output that erodes trust in all future documentation.
