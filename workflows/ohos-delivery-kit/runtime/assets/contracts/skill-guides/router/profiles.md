## Profile Detection

Resolve paths beginning with `../` from this guide's directory; `codespec/profile.yaml` is relative to the current repository.

When generating ODK artifacts for a specific OpenHarmony module, apply subsystem-specific constraints:

1. If `codespec/profile.yaml` exists, use the declared profile IDs (e.g., `profiles: ["arkui"]`)
2. Otherwise, infer profile from module keywords in the change path or user description (see `../../../profiles/README.md` for activation rules)
3. Read the matching profile(s) from `../../../profiles/<id>.yaml`
4. Apply `template_overrides` to adjust dimensions and sections per phase:
   - Proposal: `required_dimensions` → mark those rows as "是" in the 8-dim N/A table; all others default to "视情况"
   - Design: `additional_sections` → append to required sections list
   - Spec: `additional_ac_categories` → add to user story AC categories
   - Execution-plan: `additional_prohibitions` → append to 禁止项

   Dimension mapping: perf→性能, security→安全/权限, compatibility→兼容性, api-sdk→API/SDK, ipc→IPC/跨进程, build→构建/组件, i18n→国际化/无障碍, data-migration→数据迁移
5. Apply `agent_instructions` for the current phase (define/specify/design/plan) to add domain-specific constraints
6. If a profile provides `fragments` with a composition strategy (prepend/append/wrap), apply to the generated artifact

Profiles compose additively — they add required sections and constraints, never remove from the base template. When multiple profiles match, lower `priority` values take precedence for dimension conflicts, while sections and instructions are merged by union. See `../../../profiles/README.md` for available profiles and their activation rules.

