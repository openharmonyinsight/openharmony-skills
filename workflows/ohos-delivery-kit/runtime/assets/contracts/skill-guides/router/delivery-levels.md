# Effective delivery level

At the beginning of each artifact phase, after reading existing documents, run
the validator's `--effective-contract` option on the active change directory.
Resolve the executable from the resource check. The JSON is authoritative for
required artifacts/sections, dependencies, selected profiles, additional AC
categories, prohibitions, profile fragments and phase instructions. Reuse an
existing valid level; changing it is a scope decision, not a way to silence errors.

`proposal.md` frontmatter `delivery_level` accepts `lite`, `standard`, `critical`.
Older proposals without the field retain `standard` behavior. Set the level
during initial triage; record why it fits under `初始分级判断`.

| Level | Artifacts and checks |
| --- | --- |
| lite | proposal + spec + execution-plan, with the smaller required-section lists returned by the compiler. A separate design is optional; put concise approach/constraints in the plan's 实现边界. Keep AC→Task→file→verification traceability and actual verification results. |
| standard | The four main artifacts and existing API, resource, DFX and other conditional checks. |
| critical | The four main artifacts plus spec-for-validation; explicit state ownership/invariants (explain no state change when applicable); threat-model when 安全/权限=是. Keep FMEA and fault-path verification. |

Lite is only for device-independent, single-repository changes with explicit
`否` for API/SDK, security, IPC, data migration and performance; RAM/ROM review
must also be inactive. Declare external dependencies as 不涉及 with a concrete
reason. A profile requires assessment, not automatic involvement; its required
sections and other additions still apply at lite level. Invalid or
unresolved risk declarations cannot authorize a downgrade. Cross-repository,
public API, security-critical or complex lifecycle changes should use standard
or critical and retain all applicable gates. Do not silently rewrite the level.
Target build/component or internationalization analysis also requires standard
or critical; lite must not skip their design or device-dependent checks.

For lite, skip the standalone design phase and its brainstorming/FMEA interview
when no design document is needed. Preserve an existing design and its decisions;
if the user requests a design, produce/check it normally. Reuse confirmed
decisions at every level instead of repeating the entire interview. Do not
request a device/build product for Tasks verified entirely with repository-local
documentation, configuration or host tests; record that verification scope and
the actual commands in the plan. Device/build Tasks still follow the existing
product and firmware confirmation rules.

Use `--phase define|specify|design|plan` for intermediate checks. It validates the
requested artifact and its dependency closure, without treating future artifacts
as missing. `--phase design` at lite level permits an absent optional design,
but checks it when present. Final `--archive` checks the full selected level; it cannot be combined
with `--phase`. Separate design-docs publication still requires its five base
files. Complete a missing design before that publication rather than fabricating
one or changing the receiving repository's contract.
