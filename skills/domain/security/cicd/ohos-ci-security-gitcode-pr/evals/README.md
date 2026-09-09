# Eval Design

These evals focus on behavior that distinguishes `ohos-ci-security-gitcode-pr` from a generic `git push`:

- **intelligent remote detection**: classifying `openharmony` owner as UPSTREAM and other owners as FORK, instead of assuming remote names
- **cross-repo PR head format**: the critical `fork-owner:branch-name` format that GitCode API strictly validates
- **idempotent submission**: checking existing PRs before creating duplicates (only push when a PR already exists)
- **issue-PR linking**: creating the issue on the upstream repo and inserting `#number` into the PR template
- **edge-case handling**: prompting the user when remotes are ambiguous, and warning + terminating when the gitcode MCP is absent

## Grading approach

Cases are prompt-driven (no fixture files needed): the grader inspects whether the Agent:

- follows the skill's decision matrix rather than guessing remote roles
- produces the exact `head` parameter format `<fork-owner>:<branch-name>` with no extra prefixes
- checks for existing PRs before creating new ones
- creates the issue on the correct (upstream) repo and links it via `#number`
- asks the user when remotes are ambiguous instead of auto-selecting
- respects the MCP-absence guard (warn + terminate, no curl bypass)

These behaviors are the failure-prone parts of GitCode PR submission that a baseline Agent (without the skill) gets wrong by assuming remote names, misformatting `head`, or creating duplicate PRs.
