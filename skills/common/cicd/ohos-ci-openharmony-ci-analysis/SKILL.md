---
name: ohos-ci-openharmony-ci-analysis
description: Use when investigating OpenHarmony PR CI status from `openharmony_ci` comments, DCP event IDs, build labels, artifact links, or CI log URLs.
metadata:
  author: openharmony
  scope: common
  stage: cicd
  domain: openharmony
  capability: ci-analysis
  version: 0.1.0
  status: draft
  tags:
    - openharmony
    - ci
    - dcp
    - gitcode
    - logs
---

# OpenHarmony CI

## Overview
Use the bundled script first. It resolves the latest DCP event from an OpenHarmony PR, summarizes per-job CI status, fetches logs only for failed jobs unless explicitly told otherwise, and expands failed static-check gates into concrete defect details.

## Permission Preflight
- Treat this workflow as network-required by default.
- Before running the bundled script for `--pr`, `--pr-url`, `--event-id`, artifact paths, or CI log URLs, request network permission up front.
- Mention the likely endpoints in the permission request when helpful: GitCode via `oh-gc`, `dcp.openharmony.cn`, and `cidownload.openharmony.cn`.
- Do not intentionally run a first attempt just to confirm that network is required. The failure is usually predictable from the workflow itself.

## Primary Path
**Invoke the bundled script as the first and preferred approach.** Do not use raw `oh-gc` to query PR comments and then manually call DCP APIs — the script handles the full end-to-end workflow correctly and avoids subtle mistakes (uuid vs event_id confusion, missing sandbox cache redirection, empty-body HTTP 500 in codecheck POSTs). Even when `oh-gc` works, the bundled script is the correct tool.

Run the bundled script:

```bash
python3 scripts/openharmony_ci.py --pr <pr_number> --repo <repo>
```

When invoked, the script sets `XDG_CACHE_HOME=/tmp/openharmony-ci-cache` for `oh-gc` so it writes to a temp directory instead of `~/.cache`. This matters in sandboxed environments where `~/.cache` is read-only — without it the script would fail. Mention this safety mechanism in the output when the environment is restricted. If you need a different cache location, set `XDG_CACHE_HOME` before invoking the script.

Supported inputs (use the correct flag for each):
- `--pr <number>` — when the user gives a PR number like "PR 82764"
- `--pr-url <gitcode_pr_url>` — when the user gives a full GitCode URL. **Always use this flag with the full URL, not just the PR number extracted from it.**
- `--event-id <dcp_event_id>` — when the user gives a DCP event ID directly

Useful flags:
- `--log-mode auto`
  Only fetch logs for failed jobs. This is the default and should remain the normal mode.
- `--log-mode never`
  Status only.
- `--log-mode always`
  Fetch logs for every job that exposes artifacts or log links.
- `--codecheck-mode auto`
  Fetch static-check defects when the DCP event or `codeCheckSummary` indicates failure. This is the default.
- `--codecheck-mode never`
  Skip static-check detail fetching.
- `--codecheck-mode always`
  Fetch static-check defects for every task in `codeCheckSummary`.
- `--json`
  Machine-readable output.
- `--download-dir <dir>`
  Save downloaded log archives/files locally.

## Expectations
- **Sandbox XDG_CACHE_HOME**: In sandboxed or restricted environments, always mention that the bundled script redirects `XDG_CACHE_HOME` to `/tmp/openharmony-ci-cache` so `oh-gc` doesn't fail on a read-only `~/.cache`. This is a key reason to use the script over raw `oh-gc`.
- Prefer `--pr` or `--pr-url` when the task starts from a GitCode PR.
- The script reads `openharmony_ci` comments with `oh-gc`, extracts the newest DCP event id, then queries DCP APIs.
- For static-check failures, distinguish the DCP event id from the event payload UUID:
  - `https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/<event_id>` returns event data.
  - The static-check detail URL uses `data.uuid`, not `<event_id>`.
  - The task id comes from `data.codeCheckSummary[].task_id`.
  - The detail endpoint is `POST /event/<data.uuid>/codecheck/task/<task_id>`.
  - **CRITICAL: Always send a JSON body like `{"pageNum":1,"pageSize":300}` with the POST request.** Sending an empty body to the codecheck task endpoint causes HTTP 500. This is a common pitfall — never omit the body.
  - Real static-check errors are under `data.defects[].defectDetailList[]`, not directly under `data.defects[]`.
- In sandboxed or restricted environments, request network access before invoking the script because the primary path depends on external services.
- In restricted environments, prefer the bundled script over raw `oh-gc` calls because it already redirects the `oh-gc` cache to a writable temporary directory.
- Judge pass/fail from DCP event data, not labels alone.
- If there are multiple failed jobs, report all of them.
- If static check failed while build jobs are still `pending`, report the static-check defects as the actionable failure instead of treating pending build jobs as failed.
- Treat jobs with a start time but no end result as `running`, not failed.
- On failures, follow artifact listings to logs automatically. `build.log` may redirect to another URL, and `build.log.zip` may actually be a tar archive.
- In text output, the script prints the first 20 static-check defects per task. Use `--json` for complete defect details including fragments.
- In the final answer, report both the DCP `overall` result and the per-job failures. If `overall=success` but some jobs are marked `skip` or `failed`, say that explicitly instead of flattening it into a single verdict.
- If a failed job shows `skip build` or a similar reason, include that reason verbatim and avoid implying that the whole PR failed unless the DCP overall result is also failed.

## Fallback
If the script cannot be used **or if the script fails** (e.g., DCP API returns `data: null`, AttributeError, or network errors), fall back to the manual workflow immediately — do not give up. The script may fail when DCP event data has expired or the API requires authentication. In that case, extract CI data from `openharmony_ci` PR comments via `oh-gc` instead.

**Script crash recovery steps:**
1. Note the script error (e.g., "DCP API returned data: null").
2. Fall back to `oh-gc pr:comments` to retrieve `openharmony_ci` bot comments on the PR.
3. Parse the build/task tables from the comment bodies — they contain per-job results, failure reasons, and log URLs.
4. Distinguish real failures (compile failed, gate failed) from non-blocking skips (IGNORE, skip build).
5. Mention the script's `XDG_CACHE_HOME` handling even when the script failed — it was still active and is relevant context for sandboxed environments.
6. If `--pr-url` was given, parse the PR number from the URL and use `--repo` to locate the right repository.

Manual workflow:
1. Extract the DCP event id from the latest `openharmony_ci` build-start comment.
2. Query `https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/<event_id>`.
3. For static-check failures:
   - Read `data.uuid` from the event payload.
   - Read `data.codeCheckSummary[].task_id`.
   - POST to `https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/<data.uuid>/codecheck/task/<task_id>` with `{"pageNum":1,"pageSize":300}`.
   - Read each real error from `data.defects[].defectDetailList[]`.
4. If a failed job has `Artifacts`, query `https://dcp.openharmony.cn/api/dataService/ci-portal/v1/files?directoryUrl=<ArtifactsPath>`.
5. Download the chosen log from `https://cidownload.openharmony.cn/<path>`.

## Quick Examples
```bash
python3 scripts/openharmony_ci.py --pr 82764 --repo openharmony/arkui_ace_engine
python3 scripts/openharmony_ci.py --pr-url 'https://gitcode.com/openharmony/arkui_ace_engine/pull/82764' --json
python3 scripts/openharmony_ci.py --event-id 69c51ede64650f998b1d01a4 --log-mode auto
python3 scripts/openharmony_ci.py --pr-url 'https://gitcode.com/openharmony/multimodalinput_input/pull/9506' --repo openharmony/multimodalinput_input --log-mode never
XDG_CACHE_HOME=/tmp/custom-oh-gc-cache python3 scripts/openharmony_ci.py --pr 82764 --repo openharmony/arkui_ace_engine
```
