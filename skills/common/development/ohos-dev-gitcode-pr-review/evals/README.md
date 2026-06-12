# Eval Design

These evals focus on behavior that distinguishes this skill from a generic PR summary:

- collecting or using GitCode PR artifacts before reviewing
- inspecting local code context beyond the diff
- assigning coverage status for every changed file
- producing actionable findings with valid GitCode targets
- previewing submission drafts without executing GitCode mutations before confirmation

The fixture workspaces under `files/` are intentionally small so a grader can verify whether the agent read `summary.json`, `pr-diff.txt`, local callers, tests, and submission schemas.
