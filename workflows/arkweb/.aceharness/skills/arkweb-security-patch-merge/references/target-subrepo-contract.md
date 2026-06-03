# Target Subrepo Contract

ArkWeb wrapper root is usually not the target git repository. Determine the target subrepo before `git apply`.

Detection inputs:

1. `02_patch_fetch.json.selected_fix.project`
2. `02_patch_fetch.json.modified_files[]`
3. normalized patch `diff --git` paths
4. local `.git` boundaries from `git rev-parse --show-toplevel`
5. `<projectRoot>/.repo/manifests` for manifest project and remote

Default mapping:

- Chromium main-tree paths such as `chrome/`, `content/`, `components/`, `third_party/` -> `<projectRoot>/src`
- V8 project or `v8/` paths -> `<projectRoot>/src/v8`
- ArkWeb project or `src/arkweb` paths -> `<projectRoot>/src/arkweb`

If a single issue spans multiple git subrepos, stop and record a blocker. This simplified workflow handles one target git subrepo per issue.

Record in `06_merge_result.md/json`:

- target git subrepo
- manifest path
- manifest project name
- remote name
- remote fetch
- inferred upstream repository
- `git apply` working directory
- strip parameter
