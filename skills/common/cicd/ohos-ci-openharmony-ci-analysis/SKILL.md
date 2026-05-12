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
Run the bundled script:

```bash
python3 scripts/openharmony_ci.py --pr <pr_number> --repo <repo>
```

The script sets `XDG_CACHE_HOME=/tmp/openharmony-ci-cache` for `oh-gc` by default so it does not try to write under `~/.cache` in sandboxed environments. If you already need a different cache location, set `XDG_CACHE_HOME` before invoking the script and the script will respect it.

Supported inputs:
- `--pr <number>`
- `--pr-url <gitcode_pr_url>`
- `--event-id <dcp_event_id>`

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
- Prefer `--pr` or `--pr-url` when the task starts from a GitCode PR.
- The script reads `openharmony_ci` comments with `oh-gc`, extracts the newest DCP event id, then queries DCP APIs.
- For static-check failures, distinguish the DCP event id from the event payload UUID:
  - `https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/<event_id>` returns event data.
  - The static-check detail URL uses `data.uuid`, not `<event_id>`.
  - The task id comes from `data.codeCheckSummary[].task_id`.
  - The detail endpoint is `POST /event/<data.uuid>/codecheck/task/<task_id>`.
  - Send a JSON body such as `{"pageNum":1,"pageSize":300}`. Empty bodies can return HTTP 500.
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
If the script cannot be used, fall back to the manual workflow:
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
