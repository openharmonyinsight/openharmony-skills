#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from typing import Any, Dict, List, Optional, Sequence, Tuple


DCP_EVENT_URL = "https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/{event_id}"
DCP_FILES_URL = "https://dcp.openharmony.cn/api/dataService/ci-portal/v1/files?directoryUrl={directory}"
CI_DOWNLOAD_URL = "https://cidownload.openharmony.cn/{path}"
EVENT_ID_PATTERN = re.compile(r"/detail/([0-9a-f]{24})(?:/|$)")
PR_URL_PATTERN = re.compile(r"/(?:pull|merge_requests)/(\d+)(?:/|$)")
SUCCESS_RESULTS = {"success", "passed", "pass"}
FAILURE_RESULTS = {"failed", "fail", "error", "canceled", "cancelled", "skip", "skipped"}
DEFAULT_XDG_CACHE_HOME = "/tmp/openharmony-ci-cache"


class ToolError(RuntimeError):
    """Domain-specific error for user-facing failures."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query OpenHarmony CI status and fetch failure logs when needed."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--event-id", help="DCP event id, for example 69c51ede64650f998b1d01a4")
    source_group.add_argument("--pr", type=int, help="GitCode PR number")
    source_group.add_argument("--pr-url", help="GitCode PR URL")
    parser.add_argument(
        "--repo",
        default="openharmony/arkui_ace_engine",
        help="oh-gc repo name when querying PR comments",
    )
    parser.add_argument(
        "--log-mode",
        choices=("auto", "always", "never"),
        default="auto",
        help="auto: fetch logs only for non-success jobs; always: fetch logs for all jobs with artifacts; never: status only",
    )
    parser.add_argument(
        "--log-lines",
        type=int,
        default=80,
        help="Tail line count to keep when summarizing text logs",
    )
    parser.add_argument(
        "--download-dir",
        help="Optional directory for downloaded log archives/files",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser.parse_args()


def http_get_json(url: str) -> Dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "openharmony-ci/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read()
    except urllib.error.URLError as exc:
        raise ToolError(f"request failed: {url}: {exc}") from exc
    try:
        return json.loads(content.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ToolError(f"invalid json from {url}") from exc


def http_get_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "openharmony-ci/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()
    except urllib.error.URLError as exc:
        raise ToolError(f"download failed: {url}: {exc}") from exc


def build_oh_gc_env() -> Dict[str, str]:
    env = os.environ.copy()
    if not env.get("XDG_CACHE_HOME"):
        env["XDG_CACHE_HOME"] = DEFAULT_XDG_CACHE_HOME
    return env


def run_oh_gc(args: Sequence[str]) -> Any:
    cmd = ["oh-gc", *args]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=True, env=build_oh_gc_env())
    except FileNotFoundError as exc:
        raise ToolError("oh-gc is not installed or not in PATH") from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        stdout = (exc.stdout or "").strip()
        detail = stderr or stdout or f"exit code {exc.returncode}"
        if "Could not connect to GitCode" in detail:
            detail = (
                f"{detail}. This workflow requires network access to GitCode, "
                "and may also need access to dcp.openharmony.cn and cidownload.openharmony.cn"
            )
        raise ToolError(f"oh-gc command failed: {' '.join(cmd)}: {detail}") from exc
    output = completed.stdout.strip()
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise ToolError(f"oh-gc returned non-json output for: {' '.join(cmd)}") from exc


def parse_pr_number(pr_url: str) -> int:
    match = PR_URL_PATTERN.search(pr_url)
    if not match:
        raise ToolError(f"unable to parse pr number from url: {pr_url}")
    return int(match.group(1))


def collect_strings(value: Any) -> List[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: List[str] = []
        for nested in value.values():
            result.extend(collect_strings(nested))
        return result
    if isinstance(value, list):
        result = []
        for nested in value:
            result.extend(collect_strings(nested))
        return result
    return []


def extract_comment_author(comment: Dict[str, Any]) -> str:
    user = comment.get("user")
    if isinstance(user, dict):
        for key in ("login", "name", "username"):
            value = user.get(key)
            if isinstance(value, str) and value:
                return value
    author = comment.get("author")
    if isinstance(author, dict):
        for key in ("username", "name", "login"):
            value = author.get(key)
            if isinstance(value, str) and value:
                return value
    for key in ("author_username", "authorName", "author"):
        value = comment.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def extract_comment_text(comment: Dict[str, Any]) -> str:
    for key in ("body", "note", "content", "message"):
        value = comment.get(key)
        if isinstance(value, str) and value:
            return value
    joined = "\n".join(collect_strings(comment))
    return joined


def extract_event_id_from_text(text: str) -> Optional[str]:
    match = EVENT_ID_PATTERN.search(text)
    if match:
        return match.group(1)
    direct = re.search(r"\b([0-9a-f]{24})\b", text)
    if direct:
        return direct.group(1)
    return None


def latest_event_id_from_pr(pr_number: int, repo: str) -> Tuple[str, Dict[str, Any]]:
    comments = run_oh_gc(
        ["pr:comments", str(pr_number), "--repo", repo, "--comment-type", "pr_comment", "--json"]
    )
    if not isinstance(comments, list):
        raise ToolError("unexpected oh-gc pr:comments response")

    latest_match: Optional[Tuple[str, Dict[str, Any], str]] = None
    for comment in comments:
        if not isinstance(comment, dict):
            continue
        author = extract_comment_author(comment)
        if author != "openharmony_ci":
            continue
        text = extract_comment_text(comment)
        event_id = extract_event_id_from_text(text)
        if not event_id:
            continue
        created = ""
        for key in ("created_at", "updated_at", "create_at"):
            value = comment.get(key)
            if isinstance(value, str):
                created = value
                break
        if latest_match is None or created >= latest_match[0]:
            latest_match = (created, comment, event_id)

    if latest_match is None:
        raise ToolError(f"no DCP event id found in openharmony_ci comments for PR #{pr_number}")
    return latest_match[2], latest_match[1]


def flatten_files_tree(node: Any, prefix: str = "") -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    if not isinstance(node, dict):
        return results
    for name, value in node.items():
        current = f"{prefix}/{name}" if prefix else str(name)
        if isinstance(value, dict) and isinstance(value.get("url"), str):
            results.append({"name": current, "url": value["url"]})
            continue
        results.extend(flatten_files_tree(value, current))
    return results


def normalize_job(build: Dict[str, Any]) -> Dict[str, Any]:
    debug = build.get("debug", {}) if isinstance(build.get("debug"), dict) else {}
    job_name = build.get("buildTarget") or debug.get("component") or "unknown"
    result = classify_result(
        debug.get("result") or build.get("result") or "",
        debug.get("startTime", ""),
        debug.get("endTime", ""),
        debug.get("buildFailReason", ""),
        debug.get("buildFailType", ""),
    )
    normalized = {
        "job_name": job_name,
        "result": result,
        "fail_reason": debug.get("buildFailReason", ""),
        "fail_type": debug.get("buildFailType", ""),
        "start_time": debug.get("startTime", ""),
        "end_time": debug.get("endTime", ""),
        "pipeline_url": debug.get("pipelineUrl", ""),
        "artifacts": debug.get("Artifacts", ""),
        "build_log": debug.get("buildLog", ""),
        "raw": build,
    }
    return normalized


def classify_result(raw_result: str, start_time: str, end_time: str, fail_reason: str, fail_type: str) -> str:
    result = str(raw_result or "").strip().lower()
    if result:
        return result
    if fail_reason or fail_type:
        return "failed"
    if start_time and not end_time:
        return "running"
    if start_time and end_time:
        return "unknown"
    return "pending"


def is_failure_result(result: str) -> bool:
    return str(result).lower() in FAILURE_RESULTS


def should_fetch_logs(job: Dict[str, Any], log_mode: str) -> bool:
    if log_mode == "never":
        return False
    if log_mode == "always":
        return bool(job.get("artifacts") or job.get("build_log"))
    return is_failure_result(str(job.get("result", "")))


def infer_overall_result(raw_result: str, jobs: List[Dict[str, Any]]) -> str:
    result = str(raw_result or "").strip().lower()
    if result:
        return result
    job_results = [str(job.get("result", "")).lower() for job in jobs]
    if any(is_failure_result(item) for item in job_results):
        return "failed"
    if any(item == "running" for item in job_results):
        return "running"
    if any(item == "pending" for item in job_results):
        return "pending"
    if job_results and all(item in SUCCESS_RESULTS for item in job_results):
        return "success"
    return "unknown"


def choose_log_candidate(files: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    priorities = (
        "error.log",
        "build.log.zip",
        "build.log",
    )
    lowered = [(item, item["name"].lower()) for item in files]
    for priority in priorities:
        for item, name in lowered:
            if name.endswith(priority):
                return item
    return files[0] if files else None


def tail_text_lines(text: str, line_count: int) -> str:
    lines = text.splitlines()
    if not lines:
        return ""
    return "\n".join(lines[-line_count:])


def decode_text_payload(data: bytes) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def inspect_archive_bytes(data: bytes, line_count: int) -> Tuple[str, str]:
    buffer = io.BytesIO(data)
    if zipfile.is_zipfile(buffer):
        buffer.seek(0)
        with zipfile.ZipFile(buffer) as archive:
            names = archive.namelist()
            preferred = next((name for name in names if name.endswith("error.log")), None)
            if preferred is None:
                preferred = next((name for name in names if name.endswith("build.log")), None)
            if preferred is None and names:
                preferred = names[0]
            if preferred is None:
                raise ToolError("zip archive is empty")
            content = archive.read(preferred)
            return preferred, tail_text_lines(decode_text_payload(content), line_count)
    buffer.seek(0)
    try:
        with tarfile.open(fileobj=buffer) as archive:
            members = [member for member in archive.getmembers() if member.isfile()]
            preferred_member = next((m for m in members if m.name.endswith("error.log")), None)
            if preferred_member is None:
                preferred_member = next((m for m in members if m.name.endswith("build.log")), None)
            if preferred_member is None and members:
                preferred_member = members[0]
            if preferred_member is None:
                raise ToolError("tar archive is empty")
            extracted = archive.extractfile(preferred_member)
            if extracted is None:
                raise ToolError(f"unable to read member: {preferred_member.name}")
            return preferred_member.name, tail_text_lines(decode_text_payload(extracted.read()), line_count)
    except tarfile.TarError:
        pass
    return "", tail_text_lines(decode_text_payload(data), line_count)


def maybe_write_download(download_dir: Optional[str], source_url: str, data: bytes) -> Optional[str]:
    if not download_dir:
        return None
    os.makedirs(download_dir, exist_ok=True)
    parsed = urllib.parse.urlparse(source_url)
    name = os.path.basename(parsed.path) or "download.bin"
    path = os.path.join(download_dir, name)
    with open(path, "wb") as file_obj:
        file_obj.write(data)
    return path


def fetch_job_logs(job: Dict[str, Any], log_lines: int, download_dir: Optional[str]) -> Dict[str, Any]:
    files: List[Dict[str, str]] = []
    artifacts = job.get("artifacts") or ""
    build_log = job.get("build_log") or ""
    if artifacts:
        directory = urllib.parse.quote(artifacts, safe="/")
        listing = http_get_json(DCP_FILES_URL.format(directory=directory))
        files = flatten_files_tree(listing.get("data", {}))

    candidate = choose_log_candidate(files)
    source_path = ""
    if candidate is not None:
        source_path = candidate["url"]
    elif build_log:
        parsed = urllib.parse.urlparse(build_log)
        source_path = parsed.path.lstrip("/")

    if not source_path:
        return {
            "files": files,
            "selected_log": None,
            "downloaded_to": None,
            "archive_member": None,
            "tail": "",
        }

    source_url = CI_DOWNLOAD_URL.format(path=source_path.lstrip("/"))
    data = http_get_bytes(source_url)
    direct_text = decode_text_payload(data).strip()
    if direct_text.startswith("http://") or direct_text.startswith("https://"):
        redirected = urllib.parse.urlparse(direct_text)
        if redirected.netloc == "cidownload.openharmony.cn":
            source_url = direct_text
            data = http_get_bytes(source_url)
    downloaded_to = maybe_write_download(download_dir, source_url, data)
    archive_member, tail = inspect_archive_bytes(data, log_lines)
    return {
        "files": files,
        "selected_log": source_url,
        "downloaded_to": downloaded_to,
        "archive_member": archive_member or None,
        "tail": tail,
    }


def build_output(args: argparse.Namespace) -> Dict[str, Any]:
    pr_number: Optional[int] = args.pr
    comment: Optional[Dict[str, Any]] = None
    if args.pr_url:
        pr_number = parse_pr_number(args.pr_url)

    if args.event_id:
        event_id = args.event_id
    elif pr_number is not None:
        event_id, comment = latest_event_id_from_pr(pr_number, args.repo)
    else:
        raise ToolError("missing event source")

    event_payload = http_get_json(DCP_EVENT_URL.format(event_id=event_id))
    event_data = event_payload.get("data", {})
    builds = event_data.get("builds", []) if isinstance(event_data, dict) else []
    jobs = [normalize_job(build) for build in builds if isinstance(build, dict)]

    failures = [job for job in jobs if is_failure_result(str(job["result"]))]
    for job in jobs:
        if should_fetch_logs(job, args.log_mode):
            job["log_detail"] = fetch_job_logs(job, args.log_lines, args.download_dir)

    return {
        "pr_number": pr_number,
        "repo": args.repo,
        "event_id": event_id,
        "overall_result": infer_overall_result(event_data.get("result", ""), jobs),
        "timestamp": event_data.get("timestamp", ""),
        "end_timestamp": event_data.get("endTimestamp", ""),
        "jobs": jobs,
        "failure_count": len(failures),
        "failed_jobs": [job["job_name"] for job in failures],
        "source_comment": comment,
    }


def print_text_report(report: Dict[str, Any]) -> None:
    title_parts = [f"event_id={report['event_id']}", f"overall={report['overall_result']}"]
    if report.get("pr_number") is not None:
        title_parts.insert(0, f"pr=#{report['pr_number']}")
    print(" ".join(title_parts))
    if report.get("failed_jobs"):
        print(f"failed_jobs={', '.join(report['failed_jobs'])}")
    for job in report["jobs"]:
        print("")
        print(f"[{job['job_name']}] result={job['result']}")
        if job.get("fail_reason"):
            print(f"fail_reason={job['fail_reason']}")
        if job.get("fail_type"):
            print(f"fail_type={job['fail_type']}")
        if job.get("start_time"):
            print(f"start_time={job['start_time']}")
        if job.get("end_time"):
            print(f"end_time={job['end_time']}")
        if job.get("pipeline_url"):
            print(f"pipeline_url={job['pipeline_url']}")
        if job.get("artifacts"):
            print(f"artifacts={job['artifacts']}")
        log_detail = job.get("log_detail")
        if not isinstance(log_detail, dict):
            continue
        if log_detail.get("selected_log"):
            print(f"log_url={log_detail['selected_log']}")
        if log_detail.get("downloaded_to"):
            print(f"downloaded_to={log_detail['downloaded_to']}")
        if log_detail.get("archive_member"):
            print(f"log_member={log_detail['archive_member']}")
        tail = log_detail.get("tail") or ""
        if tail:
            print("log_tail:")
            print(tail)


def main() -> int:
    args = parse_args()
    try:
        report = build_output(args)
    except ToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
