# Read existing artifacts before changing them

This procedure is the first artifact operation of every ODK skill, including
direct invocations, bridge commands, init, implementation, review and submission.
Resolve the active change and installation first; do this before an interview,
template load, external workflow invocation or document write.

1. Identify the skill's existing targets. Read each existing target's **full
   frontmatter and body**, in chunks when necessary. Also read the relevant
   upstream decisions. A summary is for handoff; it does not replace reading the
   document being edited. An unreadable existing target is an error, never an
   absent document. Do not follow a symlink to an unexpected publication target.
2. Treat those documents as the current baseline. Preserve confirmed decisions,
   custom sections, author metadata, stable goal/US/AC/Task IDs, dependencies,
   implementation progress, verification commands, results and evidence links.
   Ask only about unresolved or changed decisions. The current user request can
   amend a prior decision; identify that amendment and its affected dependents.
3. **Existing target: revise it in place.** Apply the smallest coherent patch;
   use templates to find missing structure. Do not recreate from a template,
   truncate the document, copy over a native bridge file, or write a new variant
   to replace it. Missing target: create it from the effective contract only when
   its phase/level requires it. Init reuses an existing proposal instead of
   replacing it with a stub. A template migration is a separate, explicit change.
4. Before writing, recheck that the baseline has not changed since it was read.
   If it changed, reread and reconcile; do not overwrite another writer. Inspect
   the resulting diff for lost decisions, custom content, IDs and evidence.
   Changed behavior/code invalidates affected approval/test results; mark those
   results pending and revalidate rather than retaining a stale passing claim.
5. Report the files updated, decisions amended and remaining gaps. Repeated
   invocation with no changed inputs should leave the artifacts unchanged.

When implementation, review, tests or validation reveal a deviation, follow
[the feedback procedure](../delivery/feedback.md) to route the correction to its
owning artifact, record disposition in the existing plan and reverify affected
inputs. A review report alone does not replace updating the delivery baseline.

Targets by operation:

| Operation | Existing targets to read first |
| --- | --- |
| init / propose / brainstorm | proposal.md and any existing decision notes |
| spec / delta-spec | spec.md, including US-DFX and related verification rows |
| design / delta-design | design.md and any spec.md rows that will be amended |
| plan / tasks | execution-plan.md, including all Task progress and evidence |
| implement / apply | execution-plan.md and relevant spec/design; source files before editing |
| review / validate | delivery artifacts and any report that will be updated |
| threat model / validation spec | threat-model.md / spec-for-validation.md |
| FMEA | existing analysis/export and knowledge files at the selected destination |
| link proposal / submit design docs | proposal.md, metadata_tracking.yaml and affected references |
| combined bridge commands | every ODK target and every native target they will update |

OpenSpec's native workspace and its task file retain their own state ownership.
Read both native and ODK artifacts first; reconcile a projection without deleting
native delta operations or overwriting ODK-only decisions.
