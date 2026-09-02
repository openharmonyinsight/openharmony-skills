# ODK 0.10.0 Proposal Contract Migration

ODK 0.10.0 increases the number of required `proposal.md` sections from 11 to 13.
Existing `codespec/changes/<repo-name>/<req-id>/proposal.md` documents must add:

- `## 1+8 Device Variation Specification`
- `## External Dependencies`

## 1. Add the 1+8 device variation table

Copy the table from the installed `templates/ai/proposal.md` and complete every row:
phone, tablet, pc/2in1, wearable, tv, car, `default (other devices)`, and functional
differences that do not follow device categories. Each row must explicitly say yes or
no and provide a concrete explanation. If there is no variation, explain which common
baseline applies.

## 2. Add the external dependencies table

Record each dependency's subsystem, repository, module/path, and dependency type. If
there are no external dependencies, use exactly one not-applicable row and explain why
in the dependency-type column. Do not mix a not-applicable row with actual dependency
rows.

## 3. Validate

Run Draft validation first to identify repairable warnings, then run Archive validation
as the pre-submission gate:

```bash
python3 "${OHOS_PLUGIN_ROOT}/runtime/executables/validate-artifacts-contract.py" \
  codespec/changes/<repo-name>/<req-id>
python3 "${OHOS_PLUGIN_ROOT}/runtime/executables/validate-artifacts-contract.py" \
  --archive codespec/changes/<repo-name>/<req-id>
```

Strict/merge proposals produced through OpenSpec, MatrixSpec, or Superpowers bridges
must contain both tables. Passthrough output does not promise compliance with the ODK
Archive contract.

## 4. GitCode submission reminder

Before committing, pushing, or opening a GitCode PR after code development is complete,
ODK reads the developer-owned design-docs repository address from
`codespec/profile.yaml`:

```yaml
design_docs_repository: "https://gitcode.com/<organization>/<design-docs-repository>.git"
```

Submit `codespec/` documents separately to that repository. When the address is absent,
ODK reports that it is pending developer input. ODK does not infer the address or gain
authorization to push across repositories automatically.
