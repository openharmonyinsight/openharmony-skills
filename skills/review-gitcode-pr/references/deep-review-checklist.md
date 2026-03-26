# Deep Review Checklist

Use this checklist to prevent shallow review and premature stopping. Apply it after reading `summary.json` and before concluding the review.

## Stop Only When

Do not stop because:

- one or two findings were already found
- the remaining files "look small"
- the diff seems consistent at a glance
- one test file exists somewhere in the PR

Stop only when every changed file has one final status:

- `reviewed`
- `mechanical-low-risk`
- `skipped-with-reason`

If any file has no status, the review is incomplete.

## File Triage

Classify each changed file early so depth matches risk.

### High Risk

- public API or RPC interface changes
- schema, config, persistence, migration, or serialization changes
- auth, permission, identity, tenant, or sensitive data handling
- concurrency, locking, retry, timeout, ordering, or state-machine logic
- cache invalidation, resource lifecycle, cleanup, or idempotency logic
- error handling, fallback, or rollback behavior

Expectation:

- read the changed hunk
- read surrounding implementation
- inspect at least two of: callers, callees, tests, related config/data contracts

### Medium Risk

- internal logic changes with existing call sites
- validation changes
- feature-flag or branching changes
- refactors that claim no behavior change

Expectation:

- read the changed hunk
- read surrounding implementation
- inspect at least one of: callers, callees, tests

### Low Risk

- comments only
- string or log wording with no behavior effect
- obvious rename with complete call-site updates
- formatting or mechanical code movement with no semantic drift

Expectation:

- verify the change is truly mechanical before marking `mechanical-low-risk`
- if any doubt remains, upgrade the file to `reviewed`

## Required Review Axes

For every non-trivial code file, check these axes explicitly:

1. Input and state validation
- null, empty, default, boundary, and malformed values
- assumptions that used to hold but may no longer hold after the diff

2. Control flow and failure handling
- new early returns, swallowed errors, partial updates, retry loops
- rollback, cleanup, and resource release on failure

3. Contract consistency
- caller and callee agree on parameters, return values, status codes, and side effects
- persisted or serialized formats remain compatible

4. State and ordering
- ordering assumptions, races, duplicate work, stale cache, double free, missed cleanup
- multi-step state transitions remain internally consistent

5. Security and data handling
- permission checks still happen on the effective path
- no accidental exposure, logging, or persistence of sensitive data

6. Test adequacy
- tests cover the changed branch, not just adjacent happy paths
- failure paths, boundary cases, and compatibility paths are either tested or called out as gaps

If a review concludes with no findings, be ready to say which axes were verified and which were not.

## Common Deep-Review Prompts

Use these prompts mentally when inspecting code:

- What caller assumptions become invalid if this branch behaves differently?
- What state is left behind if this function exits at each failure point?
- What old format or old caller still exists and will hit this code after rollout?
- What happens on duplicate invocation, retry, timeout, or partial success?
- Which test would fail if this behavior regressed, and does that test exist?

## No-Finding Bar

Before saying the review found no actionable issues, confirm all of the following:

- every changed file has a final status
- every high-risk file was reviewed with deeper context
- at least one concrete code path or test path was checked for each reviewed behavior change
- any unverified area is disclosed as residual risk

If these conditions are not met, the correct output is an incomplete-review limitation, not a clean review.
