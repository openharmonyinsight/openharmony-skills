# API metadata specification workflow

This guide runs in `odk-spec` when `proposal.md` marks `API/SDK` as `是`.
The product of this guide is one or two machine-readable API contracts:
`arkts-api-spec.yaml` for ArkTS and `c-api-spec.yaml` for C. `spec.md` keeps
only an API overview and confirmation pointers; it is not the per-API
specification source.

## 0. Legacy 0.14 chain boundary

A legacy 0.14 Markdown API chain must not be consumed directly by design, plan,
implementation, or validation. Route a recognizable chain to
`odk-upgrade-api-chain`. The assistant first dry-runs deterministic
extraction from proposal, repository knowledge, and legacy spec facts; missing
or conflicting facts require developer confirmation. After it writes the current
language-specific metadata, later phases consume only that metadata. If the
assistant cannot close every fact, restart from proposal/spec.

## 1. API repository preparation

Before generating API metadata, confirm that the applicable API declaration
repository is available locally:

- ArkTS: `interface_sdk-js`
- C: `interface_sdk_c`
- If both languages are involved, both repositories are required.
- Each metadata file models exactly one language. A change that involves both
  ArkTS and C archives both `arkts-api-spec.yaml` and `c-api-spec.yaml`; the
  two language shapes must not be merged.

Ask for local paths when they are not already known. Paths need only be
resolvable; they do not have to be absolute.

If a repository is missing or unreadable, `odk-spec` must stop. Do not infer
declaration formats from remote content or unrelated repositories.

### Repository-declared prerequisites

Read the API repository root `AGENTS.md` first. It is the stable knowledge entry
for that repository, owns the applicable knowledge areas and prerequisites, and
may reference knowledge entries inside the repository. ODK and other consuming
agents must resolve those references dynamically and must not assume the
repository-internal directory layout or hardcode paths below the repository root.

When a knowledge entry declares a prerequisite, load that prerequisite exactly
in the declared order before reading the entry itself. Do not skip, replace, or
reorder repository-declared prerequisites. If a prerequisite is unavailable,
stop and follow the guidance supplied by the API repository. ODK does not own
repository prerequisites and must not hardcode them.

From the root `AGENTS.md`, dynamically resolve and read the knowledge entries
needed by this API change, including:

- API version rules and system/API version mapping
- declaration-comment rules (ArkTS JSDoc or C Doxygen/established style)
- API metadata format and schema
- device support and behavior-difference rules
- language-specific rules when applicable, such as ArkTS static-type rules

Also resolve the applicable metadata schema from the root `AGENTS.md` or the
knowledge index it references. Do not hardcode a schema location such as a
`docs/` path. If a required knowledge area or schema cannot be resolved, stop
and report the missing knowledge area; do not guess a repository-internal path.

Read at most ten relevant existing declaration files to learn:

- copyright header format
- declaration layout
- naming conventions
- parameter and return-value patterns
- JSDoc or Doxygen style

The repository guide and existing declarations together form the style
reference. If they conflict, the repository `AGENTS.md` wins.

### Repository-guide degradation

- Missing root `AGENTS.md`: stop and report that the stable API knowledge entry
  is unavailable; do not silently fall back to declaration style only.
- Missing declaration-comment rules: continue with existing declaration style.
- Missing version rules: do not derive `@since`; ask the developer for the API
  version and record that the version rule was unavailable.
- Missing metadata-schema entry: stop; the language-specific contract shape
  cannot be validated safely.
- Missing device-knowledge rules: ask the developer for device support and
  differences instead of guessing.

These degradations affect the available evidence only. They never permit
metadata or documentation fields to be guessed from unrelated context.

Ignoring an existing declaration as a contract source does not waive repository
knowledge. The root `AGENTS.md` and the knowledge entries it references must
still be loaded.

## 2. API contract skeleton and documentation context

Before creating the skeleton, extract confirmed behavioral facts from the
proposal and conversation into a documentation context file. This file is the
bounded interface to the documentation subagent; do not pass the full proposal
or unrelated design/plan context.

Select the language-specific template before generating the skeleton:

- ArkTS: `templates/api/arkts-api-spec.yaml`
- C: `templates/api/c-api-spec.yaml`

Do not use a generic API template or copy the other language's shape.

Generate a skeleton containing contract facts only:

- schema version: `1.0.0`
- language: `arkts` or `c`
- source repository, branch, commit, and path
- file-level metadata
- every API object with its applicable `kind`
- API identity and parent relationships
- ArkTS `apiMode` for static-only and dynamic&static APIs; dynamic-only is the default and may omit it
- declaration text
- source ranges
- parameters
- return types
- error codes
- permissions
- `@since`
- `@syscap`
- platform support with `enabled`, `since`, and optional `until`
- application model
- device support and differences
- confirmed behavioral facts that affect declaration documentation, such as:
  - units
  - value ranges
  - invalid-input behavior
  - default values
  - precedence
  - affected and unaffected paths
  - activation timing and lifecycle boundaries
  - per-device differences

Write these facts to:

```text
<temporary-workspace>/documentation-context.yaml
```

The file must contain:

```yaml
schemaVersion: "1.0.0"
apiIds:
  - "<stable-api-id>"
confirmedFacts:
  - apiId: "<stable-api-id>"
    fact: unit
    values:
      en: "<English localized confirmed value>"
      zh: "<Chinese localized confirmed value>"
    source: "<proposal goal / developer confirmation / repository rule>"
  - apiId: "<stable-api-id>"
    fact: device-difference
    ownerField: deviceDifferences
    values:
      en: "<English localized device-difference fact>"
      zh: "<Chinese localized device-difference fact>"
    source: "<developer confirmation / repository device rule>"
documentationRequirements:
  - apiId: "<stable-api-id>"
    fact: unit
    requirement: "include the confirmed unit"
  - apiId: "<stable-api-id>"
    fact: value-range
    requirement: "include the confirmed value range"
  - apiId: "<stable-api-id>"
    fact: device-difference
    ownerField: deviceDifferences
    requirement: "record the confirmed difference in deviceDifferences only"
```

Every `confirmedFacts` entry must already be confirmed, must declare its API ID,
and must have at least one matching `documentationRequirements` entry. Do not put open
questions in this file. If a fact is unresolved, resolve it first or keep it
as an explicit open question.

`documentation-context.yaml` is for behavioral facts that need human-facing
prose. Do not create documentation requirements for structured contract facts
such as `since`, `syscap`, permissions, platform support, application model,
kit/library, declaration shape, parameter types, return type, or numeric error
codes. Those facts stay in the metadata skeleton and declaration markers; the
subagent must not copy them into description fields.

Each behavioral fact must also have exactly one authoritative owner. Do not
create two documentation requirements for the same parameter default, type
restriction, or return semantics. The subagent must deduplicate prose across
API-level description, parameters, and return value before the checker runs.

Device-specific behavior ownership:

- Behavior that varies by device category belongs once in the structured
  `deviceDifferences` fields. Mark the corresponding documentation-context
  fact with `ownerField: deviceDifferences`.
- Do not create a prose requirement that requires per-device values to appear
  in `description.defaultBehavior`, `notes`, or another description field.
- `description.defaultBehavior` may describe only a uniform default behavior
  that is independent of device category.
- If the only default behavior is device-specific, set
  `description.defaultBehavior` to `N/A` / `不适用`.
- A summary such as "the system uses the device-category default" is allowed
  only when it does not repeat the specific per-device values or device
  categories from `deviceDifferences`.

Resolve every contract fact before asking the developer, using this order:

1. developer's explicit confirmation already recorded in proposal or conversation
2. deterministic rules in the API repository root `AGENTS.md` and the knowledge
   entries it references
3. confirmed existing declarations and code facts
4. proposal facts such as `target_release`

Do not guess API facts from unrelated context or defaults. Deterministic
repository rules are not guesses: if, for example, the repository version rule
maps proposal `target_release: 7.1` to API `26.1.0`, write `since: "26.1.0"`
and record the actual knowledge-entry path as evidence. Only ask the developer
when authoritative sources are exhausted, conflict, or explicitly require human
confirmation.

ArkTS metadata uses the discriminated-union types defined by the ArkTS schema,
including `annotation` and `decorator`. C metadata uses the C schema,
including `union`. C++ `class` and `namespace` are not C API metadata.

## 3. API documentation subagent

API descriptions must be generated by an isolated subagent. Read and follow
[api-documentation.md](./api-documentation.md).

Pass only:

- the API skeleton file
- `documentation-context.yaml`
- a knowledge pack containing the API repository root `AGENTS.md` and the
  knowledge entries dynamically resolved from it for this API change
- at most ten relevant existing declarations
- the applicable metadata schema, resolved through the root `AGENTS.md`
- the plugin's `contracts/api/forbidden-terms.yaml` file
- the plugin's `contracts/api/document-style.yaml` file

The documentation context is mandatory. The subagent must consume it and must
not invent facts absent from it.

The subagent returns documentation-only output. It must not modify contract
fields.

If an isolated subagent is unavailable, `odk-spec` fails. There is no
main-session fallback, no old-description reuse, and no declaration-comment
reverse conversion.

After the subagent returns:

1. Run `check-api-documentation-context.py` before reading or merging the output.
   Use the relocated executable command from the loaded `odk-spec` skill with
   these arguments; do not reconstruct its path from the business directory or
   a plugin-root variable:

   ```text
   --context <temporary-workspace>/documentation-context.yaml \
     --output <temporary-workspace>/api-doc-output.yaml \
     --skeleton <temporary-workspace>/api-spec-skeleton.yaml
   ```

2. Verify the API ID set, parameter names, and errorCodes identity exactly
   match the skeleton. A skeleton return type requires complete bilingual
   `returnType.description`; `returnType.text` remains owned by metadata and
   is not part of documentation-only output.
3. Ignore any contract field in the subagent output.
4. Extract only documentation fields.
5. If the checker reports a missing API, a missing documentation field, a
   confirmed fact that is absent from English or Chinese output, or a forbidden
   documentation term, request one subagent correction or regenerate the
   documentation; do not silently merge incomplete or noncompliant output.
6. Merge the documentation-only output into the applicable language-specific
   metadata file.
7. Validate the merged result before writing the final file.

### ArkTS API mode

ArkTS metadata may record `apiMode` for each API:

- omitted: dynamic-only
- `dynamic`: dynamic-only; this explicit form is allowed but not required
- `static`: static-only and must be explicit
- `dynamic&static`: one declaration serves both dynamic and static SDKs

The proposal's `ArkTS 静态类型 API` declaration must agree with metadata. When it
is `是`, at least one ArkTS API must be static or dynamic&static. When it is
`否`, all ArkTS APIs must be dynamic.

Machine closure:

- explicit static-only uses either a `.d.ets` path with a `since` value containing
  `static`, or a `.static.d.ets` path with a `since` value containing
  `staticonly`
- `'use static'` is a file-level directive; do not put it in an API declaration
- dynamic and dynamic&static APIs must not use a static-only file or declaration
- dynamic APIs must not carry a static or dynamic&static `since` marker
- dynamic&static requires `dynamic&static` in `since`
- static and dynamic&static declarations must not use `any` or union types

### Supported YAML subset

API metadata intentionally uses a small YAML subset:

- top-level mappings and nested mappings with space indentation
- the `apis` list and its constrained nested fields
- quoted single-line scalars and simple inline lists such as `[]`
- comments beginning with `#`

Unsupported YAML includes block scalars (`|` and `>`), anchors and aliases,
tags, multi-document files, flow mappings, tabs in any position, and other
generic YAML syntax. The parser reports unsupported block scalars and any tab
as structured errors.

The checker enforces identity closure, complete bilingual documentation fields,
exact confirmed-value presence, forbidden documentation terms, and the
document-style Chinese/ASCII spacing switch. It intentionally does not claim to
prove natural-language semantic equivalence; `odk-spec` and review still own
that judgement.

## 4. Device behavior differences

Start from proposal-level device conclusions. If API-level conclusions
conflict with proposal conclusions, stop and ask the developer.

When repository device knowledge exists, use it to derive supported devices
from `@syscap` and to parse developer-provided differences. When it does not
exist, ask the developer for the complete support list and differences.

The developer must confirm differences before they are written to the
applicable language-specific metadata file. Do not invent or silently normalize
device behavior.

## 5. `spec.md` API overview

`spec.md` must keep `## API 规格定义`, but it is a summary only. It must not
contain per-API specification tables or `#### API:` subsections.

Required content:

- pointers to `arkts-api-spec.yaml` and/or `c-api-spec.yaml` as the API contract sources
- an API overview table with API ID, kind, complete signature, `@since`, and
  confirmation status
- an API fact-provenance table that records each resolved fact, its evidence
  source, and whether it is still pending confirmation
- a list containing only API facts that remain unresolved after repository
  knowledge, proposal facts, code facts, and prior developer confirmation have
  been exhausted

When `API/SDK=否`, `spec.md` still contains:

```text
不涉及：<具体理由>
```

and neither `arkts-api-spec.yaml` nor `c-api-spec.yaml` is generated.

## 6. Output and gate

Write:

```text
codespec/changes/<repo-name>/<proposal-id>/arkts-api-spec.yaml   # when ArkTS is involved
codespec/changes/<repo-name>/<proposal-id>/c-api-spec.yaml       # when C is involved
codespec/changes/<repo-name>/<proposal-id>/spec.md
```

The filename selects the contract shape, and its `language` field must match:
`arkts-api-spec.yaml` uses `language: arkts`; `c-api-spec.yaml` uses
`language: c`.

Before handing off:

- Every archived metadata file must parse and satisfy its applicable schema.
- API IDs must be unique.
- Parent references must resolve.
- Enum/member relationships must close.
- Required kind-specific fields must be present.
- Every API must have bilingual three-element and five-element descriptions.
- Non-applicable documentation elements must explicitly use `N/A` / `不适用`.
- Every resolved API fact must carry its evidence source in the metadata
  `confirmation` entries or in the `spec.md` fact-provenance table.
- ODK must not contain hardcoded paths inside `interface_sdk-js` or
  `interface_sdk_c`; only their root `AGENTS.md` entries are stable.

If validation fails, fix the applicable metadata file and regenerate the
`spec.md` API overview. Do not proceed to design with an invalid API contract.
