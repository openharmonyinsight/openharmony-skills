# ODK resource check

Run once on first activation. Resolve the paths below from **this guide's actual
directory**, not the business repository. The resource root is three parents
above this guide: `core` in the source checkout, the plugin directory in native
packages, or `runtime/assets` in neutral packages. No injected variable is
needed, and a missing variable is not an installation error.

Required templates:

- `../../../templates/ai/proposal.md`
- `../../../templates/ai/spec.md`
- `../../../templates/ai/design.md`
- `../../../templates/ai/execution-plan.md`
- `../../../templates/ai/spec-for-validation.md`
- `../../../templates/ai/threat-model.md`

Required contracts:

- `workflow.md`
- `profiles.md`
- `../delivery/handoff.md`
- `../delivery/metadata.md`
- `../spec/api-specification.md`
- `../../artifacts.yaml`
- `../../dfx-fmea-matcher.yaml`

Check the required default configuration using the matching layout, relative
to the resource root:

| Layout | Default configuration |
| --- | --- |
| Source checkout (`core`) | `config/odk_config.yaml` |
| Native plugin | `runtime/assets/odk_config.yaml` |
| Neutral package (`runtime/assets`) | `odk_config.yaml` |

The user override file `odk_config_ext.yaml` is optional. Do not report its
absence as a failure. Do not combine resources from different installations to
make an incomplete package pass.

Report an **ODK Resource Check** with the resolved guide location and missing
paths, or success. If required files are missing, explain which phases need
them and suggest reinstalling/updating through the same installation channel.
For a source checkout, report the missing source files. Do not ask an installed
user to run development scripts that are not shipped with the package.

Do not start a phase that requires a missing resource. Any proposed degraded
workflow must identify what cannot be checked and receive explicit user approval;
it must not report the omitted check as passed.
