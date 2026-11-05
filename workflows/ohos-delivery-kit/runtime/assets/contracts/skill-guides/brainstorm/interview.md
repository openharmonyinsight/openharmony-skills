# Shared brainstorm protocol

This is the interview protocol for standalone brainstorm and the propose, spec
and design entrypoints. Phase skills supply the subject, not a shorter substitute
for this protocol. Follow `using-odk` for interaction mode and authorization.

## Facts and decisions

Investigate facts before asking the user to supply them. Trace the affected entry
points, callers/callees, API signatures, state owners, lifecycle, thread/queue/lock
boundaries and error handling. Cite file:line for consequential findings. For a
greenfield change, state the missing baseline and investigate available integration
contracts instead of inventing existing behavior.

Keep **observed behavior**, **user-confirmed target behavior** and **assumptions**
separate. Existing retry counts, swallowed errors or caller expectations describe
the current system; they do not by themselves authorize the future policy. Reuse
explicit decisions from the conversation and approved upstream documents within
their scope. Do not re-interview settled decisions unless new evidence changes them.

## Maintain the decision tree

Track material decisions in the conversation with a stable label, dependencies,
current answer/evidence and one of these states:

| State | Meaning | How it closes |
| --- | --- | --- |
| 待调查 | A factual prerequisite has not been checked | Inspect code, tools or supplied evidence |
| 待决策 | A product or design choice is still open | Obtain the user's choice, or choose within explicit delegated authority |
| 已确认 | A sufficiently concrete choice has an identified authority and scope | Reopen if a prerequisite changes or contradictory evidence appears |
| 待解矛盾 | Answers, constraints or evidence conflict | Surface the conflict and resolve which constraint stands |

Facts may settle implementation constraints, but do not mark a business choice
已确认 merely because the code supplies a plausible default. In autonomous mode,
record delegated choices, reasons and limits; delegation cannot manufacture facts
or authorize a material scope expansion. Silence, a request for explanation and
approval of one answer do not approve other decisions or the entire summary.

The **frontier** is the set of open decisions whose prerequisites are settled.
Choose the highest-impact ready decision, prioritizing the core goal, irreversible
tradeoffs, failure consequences and trust boundaries over document-field order.
Resolve its dependent branches before unrelated low-risk topics. If a fact is
missing, investigate it; independent ready decisions may continue while that
investigation runs, but downstream choices remain open.

## Ask, challenge, update

Ask one focused question at a time and wait for the answer. Use ordinary text so
the protocol works across hosts. Offer concrete alternatives and a recommendation
with its tradeoff when useful; an open question is preferable when the premise
itself is unclear. The user may give an answer outside the offered options.

For a consequential choice, connect the question to evidence or a concrete scenario:
what goal does it serve, what alternative is rejected, what fails at a boundary,
and how would the outcome be observed or tested? Do not turn these prompts into
four mandatory questions for every small decision. Respect a deliberate, informed
tradeoff; repeated persuasion after the user has settled it is not deeper analysis.

After **every answer**, update the tree before choosing the next question:

1. Record exactly what was decided and what remains unspecified. Acknowledge it
   briefly; do not silently fill the remaining gaps with recommended defaults.
2. Test the answer against a relevant failure, interleaving or boundary case.
   "失败就重试" leaves trigger, budget, duplicate-side-effect handling and exhausted
   behavior open where those affect the design. Ask the next dependent question;
   do not record the whole recovery policy as complete.
3. Add newly exposed decisions and dependencies. A vague answer such as "看情况"
   stays open: name the missing condition and sharpen the question.
4. Surface contradictions immediately. If a changed prerequisite invalidates a
   prior choice, reopen that choice and its affected dependents; do not overwrite
   the earlier answer or retain its obsolete conclusion.
5. Recompute the frontier. Show a compact update when material state changes so
   the user can see which decisions remain; do not print a large ledger every turn.

Reading code can answer "what happens now". If the user has not selected that
behavior as the target, ask whether to preserve it and expose the consequence.
An explanatory detour returns to the pending question; it does not advance it.

## Map resolved decisions to ODK coverage

Work through the core design branches before the coverage sweep. These obligations
remain in force, but reuse earlier explicit answers and present evidence-backed
candidate verdicts for confirmation rather than restarting a classification form:

- **API/SDK:** explicitly confirm whether `.d.ts` / `.h` declarations are added,
  modified or deprecated. Code inspection alone cannot supply this confirmation.
- **Security/trust:** confirm IPC/Binder/socket/shared-memory boundaries, security
  levels and sensitive data; any applicable boundary or sensitive operation means 是.
- **1+8:** confirm phone, tablet, pc/2in1, wearable, tv, car, default（其他设备）
  and non-category differences. Each row needs 是/否 with a reason. The user may
  confirm a clearly enumerated set together; blank rows are not decisions.
- **Resources:** triage performance, RAM and ROM as required / review-required /
  not-applicable / waived. Unknown risk remains review-required. not-applicable
  and waived require a named confirmer, reason and scope. Include hot-path/IPC,
  allocation/residency and artifact/persistence evidence as applicable.
- **External dependencies:** confirm dependent subsystems, repositories, modules
  or services; an empty set needs explicit 不涉及 with its reason.
- **Compatibility:** confirm backward behavior, wire format, IPC protocol,
  build/component dependencies, i18n and data migration with concrete reasons.
- **Success and scope:** agree on observable outcomes, measurable bounds where
  relevant, non-goals and the consequences of consciously excluded work.

New evidence from this sweep can reopen a core decision. Confirm only the delta;
do not demand repeated answers to unchanged, already confirmed rows.

## Completion gate

Before handing off to document generation:

1. Check ownership against failure recovery, concurrency against interface promises,
   compatibility against migration, resource verdicts against code cost, and success
   criteria against an end-to-end verification scenario. Reopen inconsistencies.
2. Verify every material branch is resolved within scope. No 待调查, 待决策 or
   待解矛盾 item may disappear into an unlabelled assumption; an empty *ready*
   frontier does not mean completion when unresolved prerequisites still exist.
3. Present the decision summary with choices, reasons/rejected alternatives,
   relevant failure semantics, verification outcomes, ODK verdicts and non-goals.
   In interactive mode ask for confirmation and wait; in autonomous mode apply
   the existing delegation and summarize the self-check. Do not broaden authority.

A fully specified request may need no new questions: reconstruct and check the
decision state from explicit inputs, then apply this same gate. A proposal stub,
code defaults or a guess that "the context answers everything" is not sufficient.

If the user explicitly skips the interview or defers a material choice, stop
questioning that scope. Return the unresolved items as assumptions/open questions
for the next draft; do not claim the interview is complete or invent mandatory
confirmations. Artifact-readiness gates and the authorized endpoint still apply.
