# Patch Fetch Output

Use this as the portable output contract for `{issue_id}/02_patch_fetch.md` and `{issue_id}/02_patch_fetch.json`.

## Inputs

Use only `{issue_id}/01_issue_analysis.json.issues[].upstream_fix_prs[]` as the trusted source of upstream fix candidates.

Do not widen the search to similar titles, same directories, same authors, or nearby CLs unless the upstream fix explicitly references them.

Bug-introducing PRs/CLs are not patch-fetch targets. If a candidate is identified only by `culprit`, `bisect`, `introduced by`, `caused by`, `regression range`, `first bad`, or equivalent root-cause wording, record it as an excluded candidate and do not download it as the fix patch.

## Required Markdown Content

For each issue:

1. selected upstream fix
   - URL, CL number, commit hash, Change-Id, subject
   - author, reviewers, commit time, Cr-Commit-Position if available
2. modified file list
   - path
   - status: added, modified, deleted, renamed, copied, unknown
   - old path for renamed/copied files
3. patch file archive
   - local patch path
   - source URL
   - fetch command
   - checksum when available
   - content validation result: valid diff or invalid artifact
   - invalid reason and first-line signature for HTML/JSON/error responses
4. excluded candidates
   - rejected URL/CL
   - reason
   - whether it is a bug-introducing PR/CL rather than a fixing PR/CL
5. blocking issues

## JSON Schema

```json
{
  "issues": [
    {
      "IssueID": "",
      "selected_fix": {
        "url": "",
        "cl_number": "",
        "commit_hash": "",
        "change_id": "",
        "subject": "",
        "reviewers": [],
        "author": "",
        "commit_time": "",
        "cr_commit_position": ""
      },
      "modified_files": [
        {
          "path": "",
          "status": "added|modified|deleted|renamed|copied|unknown",
          "old_path": "",
          "language": "",
          "component_hint": ""
        }
      ],
      "patch_files": [
        {
          "path": ".ace-outputs/{runId}/{issue_id}/patches/...",
          "source_url": "",
          "format": "patch|diff|mbox|raw|unknown",
          "sha256": "",
          "content_valid": false,
          "validation_reason": "",
          "first_line_signature": ""
        }
      ],
      "fetch_commands": [],
      "excluded_candidates": [],
      "blocking_issues": []
    }
  ]
}
```

## Field Ownership

This stage owns:

- selected fix details
- modified file list
- local patch files
- fetch commands
- excluded candidates and blocking fetch issues

Patch files must live only under `.ace-outputs/{runId}/{issue_id}/patches/`. Do not create or populate `.ace-outputs/{runId}/patches/`.

This stage does not own:

- Issue base metadata
- final ArkWeb impact decision
- ownership team or feature-tree impact
- keep/drop recommendation
