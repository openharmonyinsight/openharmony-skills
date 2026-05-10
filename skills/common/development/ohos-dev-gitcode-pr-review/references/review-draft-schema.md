# Review Draft Schema

Use this schema when preparing comments for `prepare_review_submission.py`.

Write submitted review comments in Chinese by default, using concise Markdown that renders cleanly in GitCode.

```json
{
  "approve": false,
  "summary": "Overall review comment posted to the PR discussion.",
  "line_comments": [
    {
      "path": "src/example.ts",
      "line": 42,
      "body": "**中** `[src/example.ts:42]`\n\n当字段缺失时，这个改动会破坏现有调用方，当前实现没有兼容旧行为。\n\n建议：\n- 保持缺失字段时的原有分支\n- 补一个覆盖缺失字段场景的测试"
    }
  ]
}
```

Rules:

- `approve`: optional boolean. Only set `true` when there are no blocking findings and the user wants to approve.
- `summary`: optional string. Posted as a normal PR comment.
- `line_comments`: optional list.
- `path`: repository-relative path and must exist in the collected PR diff summary.
- `line`: new-side line number from the diff. It must match a commentable line from `summary.json`.
- `body`: required comment text.

Markdown rules for `summary` and `line_comments[].body`:

- Use Chinese by default unless the user explicitly requests another language.
- Start with a short conclusion line, typically severity plus file reference when useful.
- Put the core problem and impact in a separate paragraph.
- Use a `建议：` section with flat bullet points for fixes when a concrete action is known.
- Prefer short paragraphs and bullet lists over one long sentence.
- Wrap identifiers such as parameter names, paths, response codes, and symbols in backticks.
- Do not emit a single `severity | path | problem | fix` line as the final submitted comment.

Recommended drafting rules:

- Keep one issue per comment.
- Prefer concrete explanation over generic wording.
- Do not repeat the same problem in both the summary and line comments unless the summary is aggregating the result.
- Keep submitted comments readable in rendered Markdown, not just in raw JSON.
