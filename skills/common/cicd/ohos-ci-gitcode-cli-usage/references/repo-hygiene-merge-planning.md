# Repo Directory Merge / Hygiene Planning (ai-code-harness family)

Use when the user asks to merge, dedupe, or consolidate directories in a numbered-domain report repo (e.g. `ai-code-harness-7.0`), or asks for a plan with "给出方案，我确认以后操作".

## Repo context: ai-code-harness-7.0
- Location: `/root/work/ai-code-harness-7.0` (GitCode org `openharmony-ai-code-harness`, clone: https://gitcode.com/openharmony-ai-code-harness/ai-code-harness-7.0.git)
- Root dirs are numbered OpenHarmony domains 01-20; **canonical numbering is defined in README.md** (both the ```text``` tree and the 目录/领域 table).
- Known numbering conflicts (as of 2026-08):
  - `08-window/` holds real window_manager audit content (23 files: current-state-review.md, merge-manifest.json, quality-ledger.*, work-items/) but README says Window = `14-window`; `08` is also claimed by `08-intelligent-foundation-platform/` (empty placeholder).
  - `14-window/`, `04-arkruntime/`, `09-arkcompiler/` are empty placeholders (only `.gitkeep`).
  - `03-distributed-ai/` holds per-repo report subdirs (communication_dsoftbus, data_object, data_share, ...).
- Merge direction decided by user (2026-08): keep the directory that already has content (`08-window`), delete the empty placeholder (`14-window`), renumber the OTHER empty placeholder to fill the freed number (`08-intelligent-foundation-platform` → `14-intelligent-foundation-platform`).

## User preference (merge planning)
- ALWAYS produce a plan first and wait for explicit confirmation before mutating (user phrase: "给出方案，我确认以后操作"). Do NOT execute git rm/mv in the same turn as presenting the plan.
- Keep the directory with real content where it is; move empty placeholders, never the content dir. Avoid renumbering content dirs (breaks manifest paths / git-history traceability).
- Present numbered options (方案A/B/C) with a clear recommendation and the trade-off.

## Analysis workflow (before proposing any merge)
1. Survey: `du -sh <dirs>` + `find <dir> -type f | wc -l` to separate real content from empty placeholders (.gitkeep only).
2. Git archaeology: `git log --oneline -- <paths>` and `git show --stat --name-status <sha>` per relevant commit — find WHERE content was placed vs where README says it belongs, and which commit created which dir.
3. Reference scan: `grep -rn "<old-dir-name>" .` for hardcoded path references INSIDE files (manifests, briefs, validator scripts). These must be updated if the dir is renamed/moved.
4. README scan: canonical numbering lives in README (tree + table); note exact line numbers for the patch.
5. Numbering check: look for duplicate numeric prefixes across dirs (e.g. two `08-*`).

## Merge safety notes
- `git mv` preserves history; a path-only move does NOT change file content, so sha256 checksums recorded in manifests (e.g. merge-manifest.json) stay valid — only the `path` strings inside the manifest need updating.
- Empty dirs are not tracked by git; deleting a placeholder = `git rm <dir>/.gitkeep`.
- Relative references between files (e.g. work-items/index.json → primary-E*.json) survive dir moves; explicit "08-window/..." strings do not.
- After moving, re-run the same grep to confirm zero stale references.

## Related
- Org discovery: `oh-gc org list` returns `No organizations found (API endpoint may not be available)`; use `oh-gc user orgs <username>` instead (see extended-commands.md → Organizations).
- Repo discovery: `oh-gc repo list --org <org> --json` + Python filtering to find the target repo before cloning.
