# Skills-Repo Relocation Workflow (openharmony-skills)

Verified on PR 326: fixing misplaced skills in a skills repository (skills sitting in `skills/` root instead of `skills/common/<stage>/` or `skills/domain/<domain>/<stage>/`) and submitting the fix as a PR via personal fork.

## User workflow preference (repository restructure/merge tasks)

- **Present a plan FIRST, wait for confirmation, then operate.** The user says "给出方案，我确认以后操作" for structure changes. Offer 2-3 named options (方案 A/B/C) with a recommendation; the user replies with a single code (e.g. "方案A").
- After confirmation: operate, commit locally. The user may then say "使用个人fork仓再提交pr" — push to the personal fork and open an upstream PR.

## Detection: skills sitting in the wrong place

```bash
find skills -maxdepth 1 -type d | sort   # root-level entries that are not common/domain
```

- A skill at `skills/ohos-dev-*` (not under `common/` or `domain/`) is misplaced.
- **Split-skill trap:** one skill can exist as TWO partial copies — a root-level dir holding only `evals/` (no SKILL.md) AND a correctly-placed dir holding SKILL.md+references but no evals. The root copy may also use a different name prefix (`ohos-dev-` vs the canonical `ohos-test-`). Check `git log --all --name-only -- <path>` to find the rename history that split them (e.g. `6e5305a Rename graphics pixel test skill`).

## Relocation steps (git mv preserves history)

1. Move evals (or whole dir) into the canonical location:
   ```bash
   mkdir -p skills/domain/graphics/testing/ohos-test-xxx/evals
   git mv skills/ohos-dev-xxx/evals/evals.json skills/domain/graphics/testing/ohos-test-xxx/evals/evals.json
   git mv skills/ohos-dev-xxx/evals/README.md skills/domain/graphics/testing/ohos-test-xxx/evals/README.md
   # whole-dir move:
   git mv skills/ohos-dev-napi-memory-leak-detection skills/common/development/ohos-dev-napi-memory-leak-detection
   ```
2. Remove the emptied root dir (`rmdir` — git ignores empty dirs; `git rm -r` only if files remain).
3. Fix content that encodes the old name:
   - `evals.json` `skill_name` field
   - `evals/README.md` workspace names and any old-name references
   - SKILL.md frontmatter `name`, references to own path
4. Add/align `metadata/website/skills/<name>.yaml` (website registration). Copy structure from a sibling skill's yaml; ensure `id`, `category.scope/stage/domain/capability`, `status.version/maturity` match SKILL.md frontmatter.
5. If SKILL.md lacks a `metadata:` block in frontmatter, add one (author/scope/stage/domain/capability/version/status/tags).

## Frontmatter YAML pitfalls

- **Long English descriptions containing `that: ` / `(1): ` break YAML** — plain scalar with `: ` becomes a mapping error (`mapping values are not allowed here`). Fix with a block scalar:
  ```yaml
  description: >-
    Detect and fix ... that: (1) returns napi_value,
    (2) has napi_value& output parameters, ...
  ```
- Always verify with PyYAML after editing:
  ```python
  import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])
  ```
  A description with `that: (1)` that parsed as valid YAML before is fine, but once you ADD a metadata block the whole frontmatter must parse — this can surface a latent error that was previously invisible (the description was already broken; the new block made it load).

## Post-relocation verification

```bash
# 1. Old paths/names zero hits:
rg -n "skills/ohos-dev-graphics-pixel-tests-generator|ohos-dev-napi-memory-leak-detection" --glob '*.md' --glob '*.json' --glob '*.yaml' .
# 2. Frontmatter parse:
python3 -c "import yaml; d=yaml.safe_load(open('.../SKILL.md').read().split('---')[1]); print(d['metadata'])"
# 3. website yaml vs frontmatter 7 fields (id/scope/stage/domain/capability/version/status)
# 4. rename detection:
git diff --name-status -M origin/release...HEAD   # expect R100/R098, no accidental A/D pairs
# 5. JSON valid: jq -e . evals.json
```

## Commit hygiene

- **Do NOT `git add -A` / `git add skills/`** — it sweeps untracked `__pycache__/*.pyc` into the commit (happened twice on PR 326). Stage specific paths, or if already committed: `git rm --cached ...pyc` + amend / soft-reset + re-commit.
- If the user says "本地提交不要推送": commit on a branch, then create a separate feature branch (`git checkout -b fix-xxx`), push to the personal fork, and `oh-gc pr create --repo openharmonyinsight/openharmony-skills --head <user>:<branch> --base release`.
- PR body with backtick paths MUST go through a temp file (`--body "$(cat /tmp/body.md)"`) — inline backticks get shell-expanded and truncated (see SKILL.md "PR Creation & Merge Workflow Pitfalls").
