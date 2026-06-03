# Team And Feature Routing

Use this as the portable contract for ownership and feature-tree impact.

## Configuration Sources

Default bundled configuration:

- [team_definition.yaml](team_definition.yaml)
- [feature_tree_list.txt](feature_tree_list.txt)

The workflow may override these with project-specific paths or inline content in `context.requirements`.

If no project-specific override is provided, use the bundled defaults above. Do not assume an absolute path outside the skill directory.

## Team Routing

Ownership team must be copied exactly from the available team definition keys.

Do not translate, shorten, normalize, or invent team names.

Decision should use:

- modified file paths from `{issue_id}/02_patch_fetch.json`
- issue type and component
- fix mechanism
- build/runtime subsystem touched by the patch

## Feature Impact

Each impacted feature must be copied exactly from the available feature tree list.

Expected format:

```text
Team > Level 1 Feature > Level 2 Feature > Level 3 Feature
```

Rules:

- do not invent missing nodes
- do not shorten paths
- if exact matching is impossible, choose the closest existing full path and state uncertainty in the analysis text
- include every plausible feature path with a concrete technical reason

## Evidence Requirements

For every affected/unaffected/unknown conclusion, cite at least one of:

- modified file path
- local ArkWeb source path
- build flag or GN target
- version or branch evidence
- known platform adaptation difference
