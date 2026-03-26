# Review Rubric

Use this rubric when deciding whether to raise a finding, how severe it is, and how much evidence is required before calling the review clean.

## Raise A Finding When

Raise a finding only when the code provides concrete evidence of a review-worthy problem such as:

- Incorrect behavior under realistic inputs
- Edge cases introduced by the diff that existing tests do not cover
- Callers, downstream code, or persisted data becoming inconsistent
- Misuse of an existing abstraction, contract, or API
- Security, privacy, or data handling regressions
- Migration, compatibility, or rollout risks that are directly implied by the change

Do not raise findings for:

- Pure formatting or style preferences
- Hypothetical issues with no supporting code path
- Speculation that cannot be tied to the diff or surrounding code
- Comments already present in the PR unless the new review adds distinct evidence

## Risk Pattern Decision Table

Use the table below to decide what to inspect, what regressions to look for, and what minimum evidence is needed.

| Risk pattern | Typical regression patterns | Minimum evidence before raising a finding | Minimum evidence before saying "no finding" |
| --- | --- | --- | --- |
| Input validation or parsing | Null, empty, malformed, boundary, default-value drift, silent coercion | Concrete bad input path or caller assumption that now breaks | Checked at least one concrete input path or test covering changed validation behavior |
| Error handling or rollback | Swallowed error, partial update, retry without cleanup, wrong fallback, leaked resource | Specific failure path with wrong resulting state or missing recovery | Reviewed failure path and whether cleanup, rollback, or propagation still happens |
| Caller/callee contract | Parameter mismatch, return-value drift, status-code mismatch, changed side effects | Concrete contract mismatch across call boundary | Read at least one direct caller or callee and verified the contract still aligns |
| Persistence, schema, serialization, migration | Old data unreadable, new data incompatible, mixed-version rollout breakage | Concrete compatibility break or missing transition handling | Reviewed format compatibility or migration handling, not just the write path |
| State, ordering, concurrency, idempotency | Duplicate work, stale cache, missed transition, race, double cleanup, retry hazard | Specific state transition or ordering path that can produce inconsistent results | Reviewed at least one state transition path and one repeated/retry/ordering scenario if applicable |
| Security, permission, sensitive data | Missing permission check, bypassed auth, tenant escape, data leakage in logs or storage | Concrete effective path where protection is missing or weakened | Verified the effective execution path still includes required checks and safe data handling |
| Tests and coverage | New branch untested, failure path uncovered, test asserts old behavior only | Missing or invalid test tied to a demonstrated regression path | Checked whether tests cover the changed branch and key failure path, or disclosed the gap |

## Severity Guide

Assign severity based on user impact and confidence:

- `high`: likely correctness, security, data loss, or release-blocking issue; substantial impact if merged as-is
- `medium`: meaningful bug, regression, or contract breakage with credible impact, but not obviously release-blocking
- `low`: minor but real issue, usually localized, with clear evidence and a straightforward fix

Severity calibration rules:

- Escalate to `high` when the issue can corrupt persisted state, bypass security boundaries, break compatibility for existing callers, or leave the system in an unrecoverable or inconsistent state.
- Prefer `medium` for credible behavior regressions, contract drift, missing coverage on risky new branches, or operationally meaningful fallback failures.
- Use `low` only when the issue is real but localized, low-blast-radius, and easy to contain.
- When uncertain between two severities, prefer the lower one unless the code evidence clearly supports higher impact.

## Evidence Standard

Each finding should be defensible from code evidence. Prefer one or more of:

- A concrete execution path
- A caller/callee contract mismatch
- A specific unhandled input or state transition
- A missing or invalid test that leaves a demonstrated regression path uncovered

Evidence that is usually insufficient on its own:

- "This pattern often causes bugs"
- "The diff looks risky"
- "I did not see a test"
- "This might break something downstream"

If you cannot explain the issue without vague language, the finding is probably not ready.

## Clean Review Standard

When no valid findings are confirmed:

- State explicitly that no actionable issues were found in the inspected scope
- Use the `no-finding-template.md` structure rather than a one-line conclusion
- Mention residual uncertainty, such as missing runtime verification, missing local environment context, or limited confidence from diff-only review
- Do not pad the review with style commentary
