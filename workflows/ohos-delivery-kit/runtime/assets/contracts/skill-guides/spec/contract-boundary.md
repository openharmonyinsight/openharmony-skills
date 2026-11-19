# Specification and implementation boundaries

Use this boundary when writing or revising a specification, choosing a design,
planning tests, or routing implementation/review feedback. Classify a fact by
who depends on it, not by the document or plugin filename it came from.

## Put each fact in its owning artifact

- **Spec:** agreed scenarios, behavior, business rules, inputs/outputs, boundary
  errors, permissions, compatibility and measurable resource/performance limits.
  Consumers include end users, SDK clients and other components using an
  InnerAPI. Caller-visible ownership/lifetime obligations, public data formats
  and explicitly required security/interoperability constraints remain contracts.
- **Design:** internal algorithms, data structures, private interfaces, state
  ownership, lifecycle, concurrency and recovery mechanisms chosen to satisfy
  those contracts. Reference AC IDs instead of restating their requirements.
- **Plan/evidence:** implementation/test files, test function names, commands,
  Red/Green conditions and outputs, current verification status and commit/run
  evidence. Spec verification mapping describes scenarios and acceptance methods;
  it does not depend on one test layout or contain execution status.

Apply this to the whole spec, including business-rule tables, API descriptions,
exception rules and test hints, not only AC Then clauses. A rule such as "one
active focus target" is a contract; a unique-pointer field used to maintain it
is a design choice. Required cryptography, wire formats or caller-visible
ordering are not optional merely because implementation code enforces them.

Reading existing code establishes facts and compatibility constraints; it does
not make the current mechanism a new requirement. Review this distinction
semantically, without banning words such as cache, lock or algorithm by regex.

## Decide what actually changed before writing

| Change | Artifact updates |
| --- | --- |
| Local implementation/test refactor with the same contract and design | Update affected plan/results and code/tests. Leave spec and design unwritten. |
| Different internal design with the same contract | Revise affected design decisions and plan/results. Leave spec unwritten. |
| Agreed contract changed, missing or incorrect | Revise the affected spec clauses/mapping and downstream design/Tasks; preserve stable IDs. Obtain a decision for a material change not already authorized. |

Check observable outputs, errors, permissions, ordering, timing/resource bounds
and compatibility before calling a change implementation-only. Passing the old
tests alone does not establish equivalence. A real new failure behavior found
during design/FMEA may require an AC; an internal mitigation of an existing
requirement belongs in design and a verifying Task instead.

For implementation-only changes, preserve the existing spec body, frontmatter,
AC/BR IDs and session mirror. Do not invoke spec generation or append a spec
session merely to record a design update, rerun or new code commit. Invalidate
and rerun affected verification in the plan/evidence even when spec is unchanged;
unchanged requirements do not make old execution results current.

When explicitly cleaning up a mixed existing spec, relocate internal decisions
to design (or concise plan constraints for lite) and execution details to the
plan, preserving the agreed contract and traceability. Do not bulk-migrate old
archives or reject legacy test-table columns solely for this layout change.

Bridges pass these responsibilities into native briefs. In strict/merge ODK
projections, split contract, design and execution content by meaning; a native
"spec" file can contain all three. Preserve native workspace/state and
passthrough output ownership; report a scope/contract gap to the coordinator
rather than rewriting native output or refreshing an unchanged ODK spec.
