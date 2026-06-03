# Public Text Redaction

GitCode Issue, commit message, PR title/body, comments, and
`12_submit_result.md` must not leak local workflow internals.

Forbidden in public text:

- local absolute filesystem paths
- `.ace-outputs`, `run-*` directories, local archive file names, temporary
  paths, token names or token values
- root batch-only context in an individual issue submission, including batch
  statistics, other issue IDs, overlap summaries, and internal failure routing

Allowed public facts:

- GitCode Issue number, Chromium issue, CVE, upstream CL/commit, Change-Id
- vulnerability description, impact summary, affected version evidence
- ArkWeb impact conclusion, owner/team, feature tree, quality/RAM/ROM notes
- relative file paths and local build conclusion

Validate generated public text before commit/PR creation:

```bash
node skills/arkweb-security-patch-gitcode-pr/scripts/validate_public_text.mjs \
  <commit_msg_file> <issue_body_file> <pr_body_file>
```
