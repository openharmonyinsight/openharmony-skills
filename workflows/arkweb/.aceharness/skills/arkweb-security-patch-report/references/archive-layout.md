# Archive Layout

Use this as the portable archive contract.

## Local Issue Analysis Archive Mode

When the workflow only performs local issue analysis, patch fetch and impact analysis, write:

```text
.ace-outputs/{runId}/{issue_id}/
  01_issue_analysis.md
  01_issue_analysis.json
  02_patch_fetch.md
  02_patch_fetch.json
  03_impact_decision.md
  03_impact_decision.json
  patches/
  04_final_archive.md
  04_final_archive.json
  summary.md
  summary.json
```

`{issue_id}` is the only primary location for per-issue stage artifacts and patch files. The workflow must not write any files directly under `.ace-outputs/{runId}/`; do not create root `*.index.md/json`, root `04_final_archive.md/json`, root `01/02/03` artifacts, or `.ace-outputs/{runId}/patches/`.

`summary.json` should include:

```json
{
  "IssueID": "",
  "automation_result": "success|partial|failed",
  "issue_archive_dir": "",
  "source_issue_files": [],
  "upstream_fix_prs": [],
  "patches_found": [],
  "arkweb_impact": "affected|unaffected|unknown",
  "archive_dir": "",
  "missing_artifacts": []
}
```

## Auto Merge And Submit Report Mode

When the workflow starts from an existing issue archive and performs merge/build/submit, write:

```text
.ace-outputs/{runId}/13_final_report.md
.ace-outputs/{runId}/13_final_report.json
```

The report should include:

- source archive directory
- issue id
- selected upstream fix
- patch files and allowed modified files
- merge result
- conflict resolution result
- code review result
- build verification and build fix result
- risk assessment
- commit id, fork branch and GitCode PR link or failure reason
- unresolved issues and rollback suggestion
