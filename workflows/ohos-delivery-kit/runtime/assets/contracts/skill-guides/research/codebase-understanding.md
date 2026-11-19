# Understand existing code before specifying or designing a change

Use this procedure before the spec/design interview and document generation when
existing behavior or an integration constrains the change. New features can have
existing callers, registration, build or lifecycle constraints. Configuration is
executable behavior when code consumes it; do not skip its consumers because the
edited file is YAML, JSON or a build manifest.

For a wording-only change, check the affected references without tracing runtime
code. In a genuinely empty project, state which implementation does not yet exist
and inspect available integration contracts; do not invent a current call chain.
Research is read-only and does not authorize implementation, a product build or
changes to another repository.

## Start with questions and a bounded map

Read the request, approved upstream artifacts and applicable repository/directory
instructions. Turn material uncertainties into code questions: which entry handles
this input, who owns the state, what reaches the caller on failure, and which
configurations select a different implementation? Follow the relevant source,
tests, registration/build files and local dependency repositories. Exclude
unrelated vendored/generated content unless it supplies the active implementation.

Record the repository, revision and relevant uncommitted changes, plus the product
or build configuration when behavior depends on it. If the configuration is not
confirmed, describe the relevant branches separately rather than assuming which
one is active. Locate files first; a symbol hit or a directory summary is a lead,
not a verified explanation.

## Trace behavior through the implementation

- Follow a relevant caller through dispatch/registration or bindings to the
  implementation and important dependencies, then back to its observable result.
  Read complete relevant functions and the surrounding definitions needed to
  explain them. Check defaults, validation order, transformations, side effects,
  error translation and cleanup rather than copying header comments.
- Trace the normal case and the failure/boundary cases that can change an AC or
  design decision. Include alternate entries, callbacks, feature flags, product
  branches and cross-language/proxy/stub hops when they affect this behavior.
  Explain where a failure originates, who transforms or suppresses it, and what
  state or externally visible effect remains. Do not claim every possible path
  was explored.
- Identify creation, mutation and destruction of relevant state, its owner and
  key, and the thread/queue/lock ordering around it. A type declaration or a
  matching name alone does not establish lifecycle or concurrency semantics.
- Find an analogous implementation and its tests when one exists. Read enough
  to decide what can be reused and where its assumptions differ. Search results
  with no suitable match are a scoped negative result, not proof that the whole
  repository lacks a reusable mechanism.
- Read actual test setup and assertions. They may expose intended compatibility
  or an untested branch; test names and a prior Pass do not prove current runtime
  behavior. Distinguish source inspection from tests actually executed, recording
  their command, inputs and result only when run.

Use available semantic queries to supplement the trace. For capability probing,
index limits and text-search fallback, consult the relevant sections of
[the change-impact guide](../delivery/change-impact.md). Do not install tools,
start implementation/TDD, or treat a partial index as complete just to research
spec/design. Missing tools require a stated limit and source-based fallback.

## Challenge the working explanation

For a consequential claim, try a counterexample using the code: an invalid input,
disabled feature, alternate caller, early return or cleanup path. Reconcile source,
tests and documentation when they disagree. Label a conclusion as observed,
inferred or unresolved; an inference must name its supporting evidence and limit.
Keep the current behavior separate from the user's confirmed target. Existing
defaults or swallowed failures do not decide future product policy.

For cross-repository behavior, read the relevant implementation and caller
contract when available. If a required repository or generated source is missing,
identify the exact unresolved fact and its effect. Ask for information only after
checking authorized available sources. Continue independent work, but keep the
dependent contract/design decision open instead of guessing.

## Carry evidence into the right phase

Keep a compact baseline with consequential findings, not a transcript of search
commands. A useful record contains the question, observed behavior, repository
and file:line/symbol reference, supporting test or counterexample, and its effect
on the requested change. Record unresolved facts with the source or check still
needed. Separate source-backed facts, inferences and agreed target changes.

- **Spec:** derive observable inputs, results, errors, side effects and
  compatibility constraints from this baseline and confirmed decisions. Keep
  internal call chains, private helpers and test commands out of ACs; use the
  existing verification mapping or evidence references for necessary support.
- **Design:** verify the decisive source locations, then use them in
  `代码事实基线`, `实现入口`, applicable `既有模式复用` and ownership/invariant
  decisions. Explain the current behavior, proposed change, retained constraints
  and why reuse or an alternative fits the inspected code. Each affected entry
  and relevant branch needs a proposed treatment or a concrete open issue.

Reuse the baseline across interview, spec and design; it may remain in context or
an existing evidence location. A separate research file is optional process
evidence, not a new mandatory archive artifact. If delegating research is allowed
and useful, scope read-only questions by behavior or subsystem and exchange paths
and concise findings. The document author still reads the decisive source for
the conclusions it adopts; do not substitute a researcher's summary for evidence
or create a fixed number of extra reviewer seats.

Refresh only facts affected by changed source, local edits, configuration or scope.
Before claiming the baseline is sufficient, check that each consequential
contract/design choice has supporting code or an explicitly confirmed new
requirement, and that material unknowns remain visible. This is a semantic check,
not a guarantee supplied by document structure validation.

## Method references

These are background references, not runtime dependencies. The procedure above
adapts their approaches to ODK's spec/design ownership and existing evidence flow;
it does not import their tools, output directories or approval workflows.

- Anthropic feature-dev: [code-explorer](https://github.com/anthropics/claude-plugins-official/blob/e0ab6e51219eef74e417a0e1d89e5d53e5e763d4/plugins/feature-dev/agents/code-explorer.md)
  and [code-architect](https://github.com/anthropics/claude-plugins-official/blob/e0ab6e51219eef74e417a0e1d89e5d53e5e763d4/plugins/feature-dev/agents/code-architect.md):
  follow implementation paths and ground design in concrete existing patterns.
- HumanLayer's historical [codebase-analyzer](https://github.com/humanlayer/humanlayer/blob/99abe673498cf8bdcd5f989aebe9406a27185b3b/.claude/agents/codebase-analyzer.md)
  and [codebase-pattern-finder](https://github.com/humanlayer/humanlayer/blob/99abe673498cf8bdcd5f989aebe9406a27185b3b/.claude/agents/codebase-pattern-finder.md):
  establish current behavior and comparable implementations before recommending a change.
- GitHub Spec Kit's [existing-project guidance](https://github.com/github/spec-kit/blob/979b0a3c1277283371c9901ad0eed04b64a99997/docs/how-to/existing-projects.md):
  investigate a bounded change and retain the repository's compatibility and architecture constraints.
