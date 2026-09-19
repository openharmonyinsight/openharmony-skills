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
import bz2
import gzip
import io
import http.client
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import zlib
import lzma
from collections import Counter
from typing import Any, Dict, List, Optional, Sequence, Tuple


DCP_EVENT_URL = "https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/{event_id}"
DCP_CODECHECK_TASK_URL = (
    "https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/{uuid}/codecheck/task/{task_id}"
)
DCP_FILES_URL = "https://dcp.openharmony.cn/api/dataService/ci-portal/v1/files?directoryUrl={directory}"
CI_DOWNLOAD_URL = "https://cidownload.openharmony.cn/{path}"
EVENT_ID_PATTERN = re.compile(r"/detail/([0-9a-f]{24})(?:/|$)")
PR_URL_PATTERN = re.compile(r"/(?:pull|merge_requests)/(\d+)(?:/|$)")
SUCCESS_RESULTS = {"success", "passed", "pass"}
FAILURE_RESULTS = {"failed", "fail", "error", "canceled", "cancelled"}
SKIP_RESULTS = {"skip", "skipped", "ignore"}
MAX_DOWNLOAD_BYTES = 64 * 1024 * 1024
MAX_JSON_BYTES = 16 * 1024 * 1024
MAX_ARCHIVE_BYTES = 128 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 10000
MAX_CODECHECK_PAGES = 100
MAX_CODECHECK_DETAILS = 100000
OH_GC_TIMEOUT = 60
DEFAULT_XDG_CACHE_HOME = "/tmp/openharmony-ci-cache"


class ToolError(RuntimeError):
    """Domain-specific error for user-facing failures."""


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def read_limited(stream: Any, limit: int) -> bytes:
    data = stream.read(limit + 1)
    if len(data) > limit:
        raise ToolError(f"response or archive exceeds byte limit ({limit})")
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query OpenHarmony CI status and fetch failure logs when needed."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--event-id", help="DCP event id, for example 69c51ede64650f998b1d01a4")
    source_group.add_argument("--pr", type=positive_int, help="GitCode PR number")
    source_group.add_argument("--pr-url", help="GitCode PR URL")
    parser.add_argument(
        "--repo",
        help="GitCode owner/repo; inferred from --pr-url, required with --pr",
    )
    parser.add_argument(
        "--log-mode",
        choices=("auto", "always", "never"),
        default="auto",
        help="auto: fetch logs only for failed/canceled jobs; always: fetch logs for all jobs with artifacts; never: status only",
    )
    parser.add_argument(
        "--log-lines",
        type=positive_int,
        default=80,
        help="Tail line count to keep when summarizing text logs",
    )
    parser.add_argument(
        "--download-dir",
        help="Optional directory for downloaded log archives/files",
    )
    parser.add_argument(
        "--codecheck-mode",
        choices=("auto", "always", "never"),
        default="auto",
        help="auto: fetch static check defects when DCP/codecheck failed; always: fetch every task; never: skip",
    )
    parser.add_argument(
        "--codecheck-page-size",
        type=positive_int,
        default=300,
        help="Page size for DCP static check defect details",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser.parse_args()


def http_get_json(url: str) -> Dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "openharmony-ci/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content = read_limited(response, MAX_JSON_BYTES)
    except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
        raise ToolError(f"request failed: {url}: {exc}") from exc
    try:
        return json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ToolError(f"invalid json from {url}") from exc


def http_post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "openharmony-ci/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content = read_limited(response, MAX_JSON_BYTES)
    except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
        raise ToolError(f"request failed: {url}: {exc}") from exc
    try:
        return json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ToolError(f"invalid json from {url}") from exc


def http_get_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "openharmony-ci/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return read_limited(response, MAX_DOWNLOAD_BYTES)
    except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
        raise ToolError(f"download failed: {url}: {exc}") from exc


def build_oh_gc_env() -> Dict[str, str]:
    env = os.environ.copy()
    if not env.get("XDG_CACHE_HOME"):
        env["XDG_CACHE_HOME"] = DEFAULT_XDG_CACHE_HOME
    return env


def run_oh_gc(args: Sequence[str]) -> Any:
    cmd = ["oh-gc", *args]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=True, env=build_oh_gc_env(), timeout=OH_GC_TIMEOUT)
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
    except (OSError, UnicodeError, subprocess.TimeoutExpired) as exc:
        raise ToolError(f"unable to run oh-gc: {exc}") from exc
    output = completed.stdout.strip()
    if not output:
        return []
    try:
        return json.loads(output)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ToolError(f"oh-gc returned non-json output for: {' '.join(cmd)}") from exc


def parse_pr_number(pr_url: str) -> int:
    match = PR_URL_PATTERN.search(pr_url)
    if not match:
        raise ToolError(f"unable to parse pr number from url: {pr_url}")
    return int(match.group(1))


def parse_pr_repo(pr_url: str) -> str:
    try:
        parsed = urllib.parse.urlparse(pr_url)
    except ValueError as exc:
        raise ToolError(f"invalid GitCode PR URL: {pr_url}") from exc
    match = re.fullmatch(r"/([^/]+)/([^/]+)/(?:pull|merge_requests)/\d+/?", parsed.path)
    if parsed.scheme not in {"http", "https"} or parsed.hostname != "gitcode.com" or not match:
        raise ToolError(f"invalid GitCode PR URL: {pr_url}")
    return f"{match.group(1)}/{match.group(2)}"


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


def flatten_files_tree(node: Any, prefix: str = "", errors: Optional[List[str]] = None) -> List[Dict[str, str]]:
    problems = errors if errors is not None else []
    results: List[Dict[str, str]] = []
    pending = [(node, prefix)]
    visited = 0
    while pending:
        current_node, current_path = pending.pop()
        visited += 1
        if visited > MAX_ARCHIVE_MEMBERS:
            problems.append("artifact listing exceeds entry limit")
            break
        if not isinstance(current_node, dict):
            problems.append(f"invalid artifact entry at {current_path or '/'}")
            continue
        if "url" in current_node:
            url = current_node["url"]
            if not isinstance(url, str) or not url.strip():
                problems.append(f"invalid artifact URL at {current_path}")
            else:
                results.append({"name": current_path, "url": url})
            continue
        for name, value in reversed(list(current_node.items())):
            pending.append((value, f"{current_path}/{name}" if current_path else str(name)))
    if errors is None and problems:
        raise ToolError("; ".join(problems))
    return results


def normalize_job(build: Dict[str, Any]) -> Dict[str, Any]:
    debug = build.get("debug", {}) if isinstance(build.get("debug"), dict) else {}
    validation_errors = []
    for field, value in (("buildTarget", build.get("buildTarget")), ("component", debug.get("component"))):
        if value is not None and not isinstance(value, str):
            validation_errors.append(f"{field} must be a string")
    job_name = next((value for value in (build.get("buildTarget"), debug.get("component"))
                     if isinstance(value, str) and value.strip()), "unknown")
    if "debug" in build and not isinstance(build["debug"], dict):
        validation_errors.append("debug must be an object")
    for field in ("result", "startTime", "endTime", "buildFailReason", "buildFailType"):
        if field in debug and debug[field] is not None and not isinstance(debug[field], str):
            validation_errors.append(f"debug.{field} must be a string")
    if build.get("result") is not None and not isinstance(build["result"], str):
        validation_errors.append("result must be a string")
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
        "validation_errors": validation_errors,
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


def is_codecheck_failure(result: Any) -> bool:
    return str(result or "").strip().lower() in {"nopass", "failed", "fail", "error"}


def should_fetch_codecheck(event_data: Dict[str, Any], codecheck_mode: str) -> bool:
    if codecheck_mode == "never":
        return False
    summaries = event_data.get("codeCheckSummary", [])
    if not isinstance(summaries, list):
        raise ToolError("codeCheckSummary must be a list")
    if not summaries:
        return False
    if any(not isinstance(item, dict) or not isinstance(item.get("task_id"), str)
           or not item["task_id"].strip() for item in summaries):
        return True
    if codecheck_mode == "always":
        return True
    if is_failure_result(str(event_data.get("result", ""))):
        return True
    for summary in summaries:
        if isinstance(summary, dict) and is_codecheck_failure(summary.get("result")):
            return True
    return False


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
    if job_results and all(item in SUCCESS_RESULTS | SKIP_RESULTS for item in job_results):
        return "success" if any(item in SUCCESS_RESULTS for item in job_results) else "skipped"
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
    try:
        return _inspect_archive_bytes(data, line_count)
    except ToolError:
        raise
    except (zipfile.BadZipFile, tarfile.TarError, zlib.error, lzma.LZMAError,
            EOFError, OSError, RuntimeError, NotImplementedError) as exc:
        raise ToolError(f"unable to read log archive: {exc}") from exc


def _inspect_archive_bytes(data: bytes, line_count: int) -> Tuple[str, str]:
    buffer = io.BytesIO(data)
    if zipfile.is_zipfile(buffer):
        with zipfile.ZipFile(buffer) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_ARCHIVE_MEMBERS:
                raise ToolError("archive exceeds member limit")
            names = [entry.filename for entry in entries if not entry.is_dir()]
            preferred = next((name for name in names if name.endswith("error.log")), None)
            preferred = preferred or next((name for name in names if name.endswith("build.log")), None)
            preferred = preferred or (names[0] if names else None)
            if preferred is None:
                raise ToolError("zip archive is empty")
            if archive.getinfo(preferred).file_size > MAX_ARCHIVE_BYTES:
                raise ToolError("archive member exceeds byte limit")
            with archive.open(preferred) as member:
                content = read_limited(member, MAX_ARCHIVE_BYTES)
            return preferred, tail_text_lines(decode_text_payload(content), line_count)
    if data.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")):
        raise ToolError("damaged ZIP archive")
    compressed = False
    for magic, opener in ((b"\x1f\x8b", gzip.open), (b"BZh", bz2.BZ2File), (b"\xfd7zXZ\x00", lzma.LZMAFile)):
        if data.startswith(magic):
            compressed = True
            with opener(io.BytesIO(data), mode="rb") as stream:
                data = read_limited(stream, MAX_ARCHIVE_BYTES)
            break
    try:
        archive = tarfile.open(fileobj=io.BytesIO(data), mode="r:")
    except tarfile.ReadError as exc:
        if compressed or data[257:262] == b"ustar" or b"\x00" in data[:512]:
            raise ToolError("damaged or unsupported log archive") from exc
        return "", tail_text_lines(decode_text_payload(data), line_count)
    with archive:
        members = []
        for index, member in enumerate(archive):
            if index >= MAX_ARCHIVE_MEMBERS:
                raise ToolError("archive exceeds member limit")
            if member.isfile():
                if member.size > MAX_ARCHIVE_BYTES or member.offset_data + member.size > len(data):
                    raise ToolError("archive member is truncated or exceeds byte limit")
                members.append(member)
        preferred = next((m for m in members if m.name.endswith("error.log")), None)
        preferred = preferred or next((m for m in members if m.name.endswith("build.log")), None)
        preferred = preferred or (members[0] if members else None)
        if preferred is None:
            raise ToolError("tar archive is empty")
        extracted = archive.extractfile(preferred)
        if extracted is None:
            raise ToolError(f"unable to read member: {preferred.name}")
        with extracted:
            content = read_limited(extracted, MAX_ARCHIVE_BYTES)
        return preferred.name, tail_text_lines(decode_text_payload(content), line_count)


def maybe_write_download(download_dir: Optional[str], source_url: str, data: bytes) -> Optional[str]:
    if not download_dir:
        return None
    os.makedirs(download_dir, exist_ok=True)
    parsed = urllib.parse.urlparse(source_url)
    name = os.path.basename(parsed.path) or "download.bin"
    with tempfile.NamedTemporaryFile(dir=download_dir, prefix="log-", suffix=f"-{name}", delete=False) as file_obj:
        file_obj.write(data)
        return file_obj.name


def normalize_log_url(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ToolError("log URL must be a non-empty string")
    try:
        parsed = urllib.parse.urlparse(value)
        if parsed.scheme or parsed.netloc:
            if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username:
                raise ToolError("unsupported log URL")
            return value
        return CI_DOWNLOAD_URL.format(path=value.lstrip("/"))
    except ValueError as exc:
        raise ToolError(f"invalid log URL: {value}") from exc


def fetch_job_logs(job: Dict[str, Any], log_lines: int, download_dir: Optional[str]) -> Dict[str, Any]:
    errors: List[str] = []
    files: List[Dict[str, str]] = []
    paths = {}
    for field in ("artifacts", "build_log"):
        value = job.get(field)
        if value is not None and not isinstance(value, str):
            errors.append(f"{field} must be a string")
            value = ""
        paths[field] = value or ""
    if paths["artifacts"]:
        try:
            directory = urllib.parse.quote(paths["artifacts"], safe="/")
            listing = http_get_json(DCP_FILES_URL.format(directory=directory))
            tree = listing.get("data") if isinstance(listing, dict) else None
            if not isinstance(tree, dict):
                raise ToolError("invalid artifact listing: data must be an object")
            files = flatten_files_tree(tree, errors=errors)
        except (ToolError, OSError, ValueError) as exc:
            errors.append(str(exc))
    candidate = choose_log_candidate(files)
    result = {"files": files, "selected_log": None, "downloaded_to": None, "archive_member": None, "tail": ""}
    sources = [candidate["url"]] if candidate else []
    if paths["build_log"] and paths["build_log"] not in sources:
        sources.append(paths["build_log"])
    if not sources:
        errors.append("no downloadable log is available")
    for source in sources:
        try:
            source_url = normalize_log_url(source)
            data = http_get_bytes(source_url)
            direct_text = decode_text_payload(data).strip()
            if "\n" not in direct_text and direct_text.startswith(("http://", "https://")):
                redirected = urllib.parse.urlparse(direct_text)
                if redirected.netloc == "cidownload.openharmony.cn":
                    source_url = normalize_log_url(direct_text)
                    data = http_get_bytes(source_url)
            result["selected_log"] = source_url
            try:
                result["downloaded_to"] = maybe_write_download(download_dir, source_url, data)
            except (OSError, ValueError) as exc:
                errors.append(f"unable to save log: {exc}")
            member, tail = inspect_archive_bytes(data, log_lines)
            result.update(archive_member=member or None, tail=tail)
            break
        except (ToolError, OSError, ValueError) as exc:
            errors.append(str(exc))
    if errors:
        result["error"] = "; ".join(errors)
    return result


def normalize_codecheck_defect(detail: Dict[str, Any], defect: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": detail.get("id", ""),
        "defect_id": detail.get("defectId") or defect.get("defectId", ""),
        "task_id": detail.get("taskId", ""),
        "file": detail.get("filepath", ""),
        "file_name": detail.get("fileName", ""),
        "line": detail.get("lineNumber", ""),
        "rule": detail.get("ruleName") or detail.get("defectCheckerName", ""),
        "rule_id": detail.get("ruleId", ""),
        "checker": detail.get("defectCheckerName", ""),
        "content": detail.get("defectContent", ""),
        "level": detail.get("defectLevel", ""),
        "status": detail.get("defectStatus", ""),
        "tags": detail.get("ruleSystemTags", ""),
        "result": detail.get("result", ""),
        "created_at": detail.get("createdAt", ""),
        "updated_at": detail.get("updateTime", ""),
        "fragment": detail.get("fragment", []),
        "raw": detail,
    }


def validate_codecheck_page(page_payload: Any) -> Dict[str, Any]:
    data = page_payload.get("data") if isinstance(page_payload, dict) else None
    if not isinstance(data, dict):
        raise ToolError("invalid codecheck response: data must be an object")
    count = data.get("count")
    if isinstance(count, bool) or not isinstance(count, (int, str)) or not str(count).isdigit():
        raise ToolError("invalid codecheck response: count must be a non-negative integer")
    defects = data.get("defects")
    if not isinstance(defects, list):
        raise ToolError("invalid codecheck response: defects must be a list")
    for defect in defects:
        if not isinstance(defect, dict) or not isinstance(defect.get("defectDetailList"), list):
            raise ToolError("invalid codecheck response: each defect must contain defectDetailList")
        if not all(isinstance(detail, dict) for detail in defect["defectDetailList"]):
            raise ToolError("invalid codecheck response: defect details must be objects")
    return data


def extract_codecheck_details(page_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    data = validate_codecheck_page(page_payload)
    return [
        normalize_codecheck_defect(detail, defect)
        for defect in data["defects"]
        for detail in defect["defectDetailList"]
    ]


def fetch_codecheck_defects(uuid: str, task_id: str, page_size: int = 300) -> Dict[str, Any]:
    if page_size <= 0:
        raise ToolError("--codecheck-page-size must be greater than 0")
    url = DCP_CODECHECK_TASK_URL.format(uuid=uuid, task_id=urllib.parse.quote(task_id, safe=""))
    defects: List[Dict[str, Any]] = []
    seen_groups = set()
    seen_details = set()
    total_count: Optional[int] = None
    error = None
    try:
        for page_num in range(1, MAX_CODECHECK_PAGES + 1):
            page_payload = http_post_json(url, {"pageNum": page_num, "pageSize": page_size})
            data = validate_codecheck_page(page_payload)
            count = int(data["count"])
            if total_count is None:
                total_count = count
            elif count != total_count:
                raise ToolError("codecheck count changed during pagination")
            groups = data["defects"]
            if len(seen_groups) + len(groups) > total_count:
                raise ToolError("codecheck page exceeds reported count")
            new_groups, new_details, details = set(), set(), []
            for group in groups:
                identity = json.dumps(group.get("defectId") or group, sort_keys=True, ensure_ascii=False)
                if identity in seen_groups or identity in new_groups:
                    raise ToolError("duplicate or overlapping codecheck page")
                new_groups.add(identity)
                for detail in group["defectDetailList"]:
                    identity = json.dumps(detail.get("id") or detail, sort_keys=True, ensure_ascii=False)
                    if identity in seen_details or identity in new_details:
                        raise ToolError("duplicate codecheck detail")
                    new_details.add(identity)
                    details.append(normalize_codecheck_defect(detail, group))
            if len(defects) + len(details) > MAX_CODECHECK_DETAILS:
                raise ToolError("codecheck details exceed limit")
            seen_groups.update(new_groups)
            seen_details.update(new_details)
            defects.extend(details)
            if len(seen_groups) == total_count:
                break
            if not groups:
                raise ToolError("incomplete codecheck response: empty page before total count")
        else:
            raise ToolError("codecheck pagination exceeds page limit")
    except (ToolError, OSError, ValueError) as exc:
        error = str(exc)
    report = {"task_id": task_id, "defect_count": total_count if not error else None,
              "expected_count": total_count, "retrieved_count": len(seen_groups),
              "retrieved_detail_count": len(defects), "defects": defects, "complete": error is None}
    if error:
        report["error"] = error
    return report


def build_codecheck_report(event_data: Dict[str, Any], page_size: int) -> Dict[str, Any]:
    uuid = event_data.get("uuid", "")
    summaries = event_data.get("codeCheckSummary", [])
    if not isinstance(uuid, str) or not uuid:
        raise ToolError("DCP event is missing the UUID required for static-check details")
    if not isinstance(summaries, list):
        raise ToolError("codeCheckSummary must be a list")

    tasks = []
    defect_count = 0
    for index, summary in enumerate(summaries):
        task_id = summary.get("task_id") if isinstance(summary, dict) else None
        try:
            if not isinstance(task_id, str) or not task_id.strip():
                raise ToolError(f"codecheck summary[{index}] is missing a valid task_id")
            task_report = fetch_codecheck_defects(uuid, task_id, page_size)
        except (ToolError, OSError, ValueError) as exc:
            task_report = {"task_id": task_id, "defect_count": None, "defects": [], "error": str(exc)}
        fields = summary if isinstance(summary, dict) else {}
        task_report["summary_index"] = index
        task_report["result"] = fields.get("result", "")
        task_report["check_type"] = fields.get("check_type", "")
        task_report["issue_count"] = fields.get("issue_count", "")
        task_report["summary"] = summary
        defect_count += int(task_report.get("retrieved_count", task_report.get("defect_count")) or 0)
        tasks.append(task_report)

    return {
        "uuid": uuid,
        "summary": summaries,
        "defect_count": defect_count,
        "tasks": tasks,
    }


def build_output(args: argparse.Namespace) -> Dict[str, Any]:
    for name in ("log_lines", "codecheck_page_size"):
        value = getattr(args, name)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ToolError(f"--{name.replace('_', '-')} must be a positive integer")
    if args.pr is not None and args.pr <= 0:
        raise ToolError("--pr must be a positive integer")
    pr_number: Optional[int] = args.pr
    comment: Optional[Dict[str, Any]] = None
    repo = args.repo
    if args.pr_url:
        url_repo = parse_pr_repo(args.pr_url)
        if repo and repo != url_repo:
            raise ToolError(f"--repo {repo} conflicts with PR URL repository {url_repo}")
        repo = url_repo
        pr_number = parse_pr_number(args.pr_url)

    if args.event_id:
        event_id = args.event_id
    elif pr_number is not None:
        if not repo:
            raise ToolError("--repo owner/repo is required with --pr")
        event_id, comment = latest_event_id_from_pr(pr_number, repo)
    else:
        raise ToolError("missing event source")

    event_payload = http_get_json(DCP_EVENT_URL.format(event_id=event_id))
    event_data = event_payload.get("data") if isinstance(event_payload, dict) else None
    if not isinstance(event_data, dict) or not event_data:
        raise ToolError("DCP event data is missing or invalid; fall back to openharmony_ci PR comments when available")
    builds = event_data.get("builds", [])
    if not isinstance(builds, list):
        raise ToolError("DCP event builds must be a list")
    jobs = []
    errors = []
    for index, build in enumerate(builds):
        if not isinstance(build, dict):
            errors.append({"stage": "event", "error": f"builds[{index}] must be an object"})
            continue
        job = normalize_job(build)
        jobs.append(job)
        for problem in job["validation_errors"]:
            errors.append({"stage": "event", "job_name": job["job_name"], "error": f"builds[{index}]: {problem}"})
    failures = [job for job in jobs if is_failure_result(str(job["result"]))]
    for job in jobs:
        if should_fetch_logs(job, args.log_mode):
            try:
                job["log_detail"] = fetch_job_logs(job, args.log_lines, args.download_dir)
                if job["log_detail"].get("error"):
                    errors.append({"stage": "log", "job_name": job["job_name"], "error": job["log_detail"]["error"]})
            except (ToolError, OSError, ValueError, zipfile.BadZipFile) as exc:
                job["log_detail"] = {"error": str(exc)}
                errors.append({"stage": "log", "job_name": job["job_name"], "error": str(exc)})

    codecheck = None
    if args.codecheck_mode != "never":
        try:
            if should_fetch_codecheck(event_data, args.codecheck_mode):
                codecheck = build_codecheck_report(event_data, args.codecheck_page_size)
                for task in codecheck["tasks"]:
                    if task.get("error"):
                        errors.append({"stage": "codecheck", "task_id": task["task_id"], "error": task["error"]})
                codecheck["complete"] = not any(task.get("error") for task in codecheck["tasks"])
        except (ToolError, OSError, ValueError) as exc:
            codecheck = {"complete": False, "defect_count": None, "tasks": [], "error": str(exc)}
            errors.append({"stage": "codecheck", "error": str(exc)})

    report = {
        "pr_number": pr_number,
        "repo": repo,
        "event_id": event_id,
        "overall_result": infer_overall_result(event_data.get("result", ""), jobs),
        "timestamp": event_data.get("timestamp", ""),
        "end_timestamp": event_data.get("endTimestamp", ""),
        "jobs": jobs,
        "failure_count": len(failures),
        "failed_jobs": [job["job_name"] for job in failures],
        "source_comment": comment,
        "complete": not errors,
        "errors": errors,
    }
    if codecheck is not None:
        report["codecheck"] = codecheck
    return report


def print_text_report(report: Dict[str, Any]) -> None:
    title_parts = [f"event_id={report['event_id']}", f"overall={report['overall_result']}"]
    if report.get("pr_number") is not None:
        title_parts.insert(0, f"pr=#{report['pr_number']}")
    print(" ".join(title_parts))
    if report.get("complete") is False:
        print("report_complete=false (some details could not be fetched)")
    for error in report.get("errors", []):
        print(f"warning: {error['stage']} {error.get('job_name') or error.get('task_id', '')}: {error['error']}")
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
    codecheck = report.get("codecheck")
    if isinstance(codecheck, dict):
        print("")
        print(f"codecheck_defects={codecheck.get('defect_count', 0)}")
        all_defects = []
        for task in codecheck.get("tasks", []):
            if isinstance(task, dict):
                all_defects.extend(item for item in task.get("defects", []) if isinstance(item, dict))
        if all_defects:
            rule_counts = Counter(
                f"{detail.get('tags', '')} / {detail.get('rule', '')}".strip()
                for detail in all_defects
            )
            file_counts = Counter(str(detail.get("file", "")) for detail in all_defects)
            print("codecheck_top_rules:")
            for rule, count in rule_counts.most_common(10):
                print(f"- {rule}: {count}")
            print("codecheck_top_files:")
            for file_path, count in file_counts.most_common(10):
                print(f"- {file_path}: {count}")
        for task in codecheck.get("tasks", []):
            if not isinstance(task, dict):
                continue
            print(
                f"[codecheck] task_id={task.get('task_id', '')} "
                f"result={task.get('result', '')} defects={task.get('defect_count', 0)}"
            )
            for detail in task.get("defects", [])[:20]:
                if not isinstance(detail, dict):
                    continue
                location = detail.get("file", "")
                line = detail.get("line", "")
                if line:
                    location = f"{location}:{line}"
                print(
                    f"- {location} level={detail.get('level', '')} "
                    f"tags={detail.get('tags', '')} rule={detail.get('rule', '')}"
                )
                content = detail.get("content", "")
                if content:
                    print(f"  {content}")
            omitted = int(task.get("defect_count", 0) or 0) - len(task.get("defects", [])[:20])
            if omitted > 0:
                print(f"  ... {omitted} more defects omitted; use --json for full details")


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
