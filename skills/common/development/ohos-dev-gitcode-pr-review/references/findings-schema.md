# Findings Schema

Use `findings.json` to record review findings before converting them into a GitCode submission draft.

`findings.json` is the review working record. `review-draft.json` is the submission payload consumed by `prepare_review_submission.py`. Keep them separate so findings can be reviewed, skipped, or retargeted before posting.

## Shape

```json
{
  "approve": false,
  "summary": "本次检视发现 1 个需要处理的问题。",
  "findings": [
    {
      "id": "F001",
      "severity": "medium",
      "status": "draft",
      "comment_target": "line",
      "path": "src/example.cpp",
      "line": 42,
      "body": "**中** `src/example.cpp:42`\n\n这里会破坏旧调用方。\n\n建议：补充兼容分支。"
    }
  ]
}
```

## Fields

Top-level fields:

- `approve`: optional boolean. Only set `true` when no blocking findings remain and the user explicitly wants approval.
- `summary`: optional string. Prepended to the generated PR summary comment.
- `findings`: required list of finding objects.

Finding fields:

- `id`: optional stable identifier such as `F001`.
- `severity`: optional `high`, `medium`, or `low`.
- `status`: optional `draft`, `accepted`, `ready`, or `skipped`. `skipped` findings are not submitted.
- `comment_target`: optional `line`, `file`, or `general`. Defaults to `line`.
- `path`: required for `line` comments. Repository-relative path from `summary.json`.
- `line`: required integer for `line` comments. Must be a commentable new-side line from `summary.json`.
- `body`: preferred submitted comment body. If omitted, the script builds a body from `problem`, `evidence`, and `fix`.
- `problem`: optional issue explanation used when `body` is omitted.
- `evidence`: optional concrete code-path evidence used when `body` is omitted.
- `fix`: optional suggested fix used when `body` is omitted.

## Conversion Rules

Run from the repository checkout being reviewed. The example assumes this skill directory is available through `$SKILL_DIR`:

```bash
python3 "$SKILL_DIR/scripts/prepare_review_submission.py" \
  --context-dir .review-gitcode-pr/pr-123 \
  --findings findings.json \
  --write-draft review-draft.json
```

The script:

- converts non-skipped `line` findings into `line_comments`
- folds `file` and `general` findings into the PR summary comment
- validates `path` and `line` against `summary.json`
- writes `review-draft.json` only when conversion and validation pass
- does not recalculate diff line mapping

If a line is not commentable, adjust the finding using `summary.json` instead of letting the script silently retarget it.
