---
name: odk-brainstorm
description: "Use when clarifying requirements or stress-testing decisions before odk-propose, odk-spec, or odk-design. Resolve a dependency-aware decision tree through code investigation, alternatives, and failure cases before drafting documents. Zero plugin dependencies."
license: MIT
---

# ODK Brainstorm

Stress-test the user's plan until its material decisions can stand on their own.
The interview is complete when decisions are resolved, not when enough questions
have been asked or an ODK template can be filled.

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

## Phase flow and next step

<!-- ODK:reference contracts/skill-guides/router/phase-flow.md -->
Before phase work, read `contracts/skill-guides/router/phase-flow.md` and apply
its configured pre_hook/post_hook order. At every completion or pause, show
the next pending action and configured hooks; omit the reminder only when
the entire applicable workflow is complete. The coordinator owns this flow.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and use the effective
contract. It takes precedence over standard-only artifact lists below; native
OpenSpec schemas remain standard/critical and lite uses the base flow.
<!-- /ODK:reference -->

## Entry and scope

- Reuse `using-odk` if it is already loaded in the current session; do not reload it. Loading `using-odk` from brainstorm only supplements shared context (interaction mode, authorized endpoint, delivery-level contract); it does not re-enter brainstorm. The shared interview protocol runs once; after its completion gate, return to the original calling phase (brainstorm or the phase that invoked it) and continue.
- Follow `using-odk`'s interaction mode and authorized endpoint.
- Use the active change context when available. An `odk-init` frontmatter stub is
  not evidence that the interview has already happened. Exploration may start
  before initialization; initialize the archive before the next artifact phase.
- Standalone and inline callers use the same protocol. Propose explores goals,
  scope, alternatives and outcomes; spec resolves observable behavior; design
  resolves architecture, ownership, concurrency and recovery. Follow dependencies
  across those boundaries when needed, without designing unrelated components.

## Steps

<!-- ODK:reference contracts/skill-guides/brainstorm/interview.md -->
Read `contracts/skill-guides/brainstorm/interview.md` in full for decision state, questioning, ODK coverage and the completion gate.
<!-- /ODK:reference -->

## Output and handoff

- Keep the decision state and confirmed summary in the conversation; do not create
  a separate `brainstorm.md` or generate the phase document during the interview.
- After the completion gate, return to the calling phase. A standalone interview
  before proposal proceeds to `odk-propose` within the authorized endpoint.
- If interrupted, resume from the latest decision state and user answers. If that
  context is unavailable, recover facts and ask about missing decisions; do not
  invent confirmations or repeat answers that are still available.
- External interviews such as grill-me may supply decisions. Reuse their explicit
  conclusions, investigate missing facts and apply the same completion gate.
