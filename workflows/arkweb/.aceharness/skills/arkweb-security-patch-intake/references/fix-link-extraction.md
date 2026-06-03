# Fix Link Extraction

Use semantic review, not raw URL collection.

## Inputs

Read issue title, description, labels, metadata and comments from the local HTML/MHTML issue archive or structured issue JSON if one is available.

## Accepted Fix Events

Accept a link as an upstream fix when the surrounding text indicates one of these:

- committed or landed code
- fixed in a revision
- merged to a branch
- review URL for the actual fix
- a revert that is itself the fix
- a Gitiles commit linked by a commit notification

Common signals:

- `The following revision refers to this bug`
- `Committed`
- `Landed`
- `Fixed in`
- `Merged to`
- `Review-Url`
- `Code-Review`
- `Change-Id`

## Fix vs Bug-Introducing CL

Keep the fixing PR/CL separate from the bug-introducing PR/CL.

- A bug-introducing PR/CL is root-cause evidence, version-range evidence, or regression-source evidence. It must not be selected as `upstream_fix_prs[]`.
- Links surrounded by words such as `culprit`, `bisect`, `regression range`, `introduced by`, `caused by`, `regressed in`, `first bad`, or `bad revision` should be classified as bug-introducing candidates unless the same comment explicitly says that the linked CL is also the fix.
- A fixing PR/CL must have fix semantics such as `fix`, `fixed`, `landed`, `committed`, `submitted`, `merged`, `cherry-picked`, `revert that fixes`, `Review-Url` in a commit notification, or a commit message that references the issue as `Bug:`/`Fixed:`.
- If both introducing and fixing PR/CL links appear in the same issue, include both in the audit table, but only the fixing PR/CL belongs in `upstream_fix_prs[]`.
- If the only available link is the introducing PR/CL and no fixing PR/CL can be confirmed, output no selected fix and mark the issue blocked for patch fetch.

## Rejected Links

Reject a link when it is only:

- a culprit or bisect result
- a regression source
- a bug-introducing CL/PR, unless it is explicitly a revert/fix CL for the current issue
- a file-level diff URL rather than the CL/commit
- a preparation or unrelated dependency
- a similar title, same component, same author, or same directory without explicit issue linkage
- a test-only change when the issue fix is a separate CL

## Deduplication

Deduplicate by Gerrit CL number, commit hash, Change-Id, or semantic identity.

When multiple URLs point to the same fix event, prefer:

1. full Gerrit review URL
2. short Gerrit review URL
3. Gitiles commit URL
4. legacy review URL

## Audit Table

`01_issue_analysis.md` should include a table like:

| Comment ID | Decision | Semantic Type | URL | Reason |
| --- | --- | --- | --- | --- |
| comment12 | accepted | committed fix | https://... | bot says committed and includes Review-Url |
| comment18 | rejected | culprit | https://... | bisect identified it as the regression source |
| comment21 | rejected | bug-introducing PR | https://... | comment says introduced by this CL; no fix semantics |
