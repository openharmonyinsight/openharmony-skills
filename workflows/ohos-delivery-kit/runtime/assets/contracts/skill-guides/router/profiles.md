## Profile Detection

Resolve paths beginning with `../` from this guide's directory; `codespec/profile.yaml` is relative to the current repository.

When generating ODK artifacts for a specific OpenHarmony module, apply subsystem-specific constraints:

1. If `codespec/profile.yaml` exists, use the declared profile IDs (e.g., `profiles: ["arkui"]`)
2. Otherwise, suggest profiles from module keywords, then record the selected IDs in `codespec/profile.yaml` before applying them. Inference alone must not add unrecorded requirements that the validator cannot reproduce.
3. Read the matching profile(s) from `../../../profiles/<id>.yaml`
4. Apply `template_overrides` to adjust dimensions and sections per phase:
   - Proposal: `required_dimensions` → explicitly assess those dimensions and record concrete reasons in the 8-dim table. Choose "是" or a justified "否" from the actual change; selecting a subsystem must not invent involvement.
   - Design: `additional_sections` → append to required sections list
   - Spec: `additional_ac_categories` → add to user story AC categories
   - Execution-plan: `additional_prohibitions` → append to 禁止项

   Dimension mapping: perf→性能, security→安全/权限, compatibility→兼容性, api-sdk→API/SDK, ipc→IPC/跨进程, build→构建/组件, i18n→国际化, data-migration→数据迁移
5. Apply `agent_instructions` for the current phase (define/specify/design/plan) to add domain-specific constraints
6. If a profile provides `fragments` with a composition strategy (prepend/append/wrap), apply to the generated artifact

Profiles compose additively — they add required sections and constraints, never remove from the base template. When multiple profiles match, sections, assessed dimensions and instructions are merged by union in priority order. See `../../../profiles/README.md` for available profiles and their activation rules.


Before applying any override, run the validator with `--effective-contract` and
use its merged JSON. It reads the recorded profile selection, validates graph
dependencies and composes required sections, dimensions, AC categories, prohibitions,
fragments and phase instructions. Both generator and validator consume this same
contract. Unknown/duplicate profile IDs or malformed declarations are errors.
Additional AC categories must appear in an actual AC entry's title or description
inside the user stories; surrounding prose, comments and code examples do not count.
additional prohibitions must appear literally in the plan's 禁止项 section.
Natural-language phase instructions still require review; structural validation
must not claim to prove their semantics.

The effective JSON declares `dimension_policy: explicit-assessment-with-reason`.
All eight dimensions must appear exactly once with 是/否 and a nonempty 依据;
annotations such as `是（IPC）` are accepted. The internationalization dimension
is named 国际化. Missing, unknown or duplicate rows fail validation.
