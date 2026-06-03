# Issue Analysis Output

Use this as the portable output contract for `{issue_id}/01_issue_analysis.md` and `{issue_id}/01_issue_analysis.json`.

## Markdown Sections

Each issue directory must contain its own `01_issue_analysis.md` using these sections:

1. Basic information
   - Issue ID and issue URL
   - original title and Chinese title
   - status, type, priority, severity, milestone
   - created/updated time if available
2. Original issue summary
   - original description
   - reporter/owner/labels when available
   - important comments and discussion timeline
3. Vulnerability or defect summary
   - problem symptom and background
   - vulnerability class, CVE/GHSA/security advisory, exploit or PoC signal
   - suspected root cause and fix intent
4. Upstream fix PR/CL extraction
   - selected upstream fix PR/CL/commit
   - source comment or source link
   - confidence and unresolved gaps
5. Link audit
   - every code-related link found in comments
   - accepted/rejected decision
   - reason for the decision

## JSON Schema

```json
{
  "issues": [
    {
      "IssueID": "",
      "Issue链接": "",
      "Issue状态": "",
      "Issue类型": "",
      "Issue标题": "",
      "Issue原始标题": "",
      "Issue原始描述": "",
      "Milestone": "",
      "Issue严重程度": "",
      "Priority": "",
      "upstream_fix_prs": [
        {
          "type": "gerrit_cl|gitiles_commit|github_pr|chromium_review|unknown",
          "url": "",
          "cl_number": "",
          "commit_hash": "",
          "change_id": "",
          "subject": "",
          "status": "merged|pending|unknown",
          "source_comment_id": "",
          "confidence": "high|medium|low"
        }
      ],
      "Issue概述": "",
      "Issue提交信息概述": "",
      "信息缺口": []
    }
  ]
}
```

## Field Ownership

This stage owns:

- Issue identity and metadata
- original issue text and discussion facts
- upstream fix PR/CL candidates and the selected fix link
- initial issue/fix summary

This stage does not own:

- modified file list
- local patch file path
- ArkWeb affected/unaffected final decision
- ownership team or feature-tree impact
- keep/drop recommendation
