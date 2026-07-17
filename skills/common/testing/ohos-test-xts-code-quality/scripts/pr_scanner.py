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
"""GitCode PR Scanner - Fetch PR changed files for local scanning.

v1.0.0 changes:
- Diff context awareness: parse unified diff, identify new/changed lines per file
- Existing comment dedup: fetch PR comments + diff comments, filter already-reported issues
- Unified auth: auto-detect oh-gc CLI, fallback to --token, fallback to GITCODE_TOKEN env
- oh-gc integration: use oh-gc pr:diff/pr:comments when available for richer data

Dependencies: requests (standard library alternative: urllib)
Source: Adapted from openharmony-insight/services/ai-review/app/services/gitcode_service.py
Diff parsing: Adapted from review-gitcode-pr/scripts/collect_pr_context.py::parse_unified_diff()

Usage:
    from pr_scanner import PRScanner, is_oh_gc_available
    scanner = PRScanner(token="your_gitcode_token")
    result = scanner.fetch_pr_files("https://gitcode.com/openharmony/xts_acts/pull/123")
    print(result.local_dir)
    print(result.changed_files)
    print(result.diff_context)  # {file_path: {'new_lines': set, 'hunks': [...]}}
"""
import os
import re
import sys
import json
import base64
import tempfile
import logging
import subprocess
import shutil

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    HAS_REQUESTS = False

logging.basicConfig(level=logging.INFO, format='[PR] %(message)s', stream=sys.stderr)
logger = logging.getLogger(__name__)

GITCODE_API_BASE = "https://api.gitcode.com/api/v5"

EXTS_OF_INTEREST = {'.ets', '.ts', '.js', '.json', '.json5', '.gn', '.gni', '.p7b'}
SPECIAL_FILES = {'BUILD.gn', 'Test.json'}


def is_oh_gc_available():
    """Check if oh-gc CLI is installed and accessible."""
    return shutil.which('oh-gc') is not None


def resolve_token(token=None):
    """Resolve authentication token from multiple sources.

    Priority:
    1. Explicitly provided token (--token parameter)
    2. oh-gc CLI (auto-detect if installed)
    3. GITCODE_TOKEN environment variable

    Returns (token, auth_method) where auth_method is 'token' or 'oh-gc'.
    """
    if token:
        return token, 'token'
    if is_oh_gc_available():
        return None, 'oh-gc'
    env_token = os.environ.get('GITCODE_TOKEN', '')
    if env_token:
        return env_token, 'token'
    return None, None


class PRScanResult:
    __slots__ = ['owner', 'repo', 'pr_id', 'pr_title', 'pr_description',
                 'local_dir', 'changed_files', 'file_contents', 'pr_url',
                 'diff_context', 'existing_comments', 'auth_method']

    def __init__(self, owner, repo, pr_id, pr_title, pr_description,
                 local_dir, changed_files, file_contents, pr_url,
                 diff_context=None, existing_comments=None, auth_method='token'):
        self.owner = owner
        self.repo = repo
        self.pr_id = pr_id
        self.pr_title = pr_title
        self.pr_description = pr_description
        self.local_dir = local_dir
        self.changed_files = changed_files
        self.file_contents = file_contents
        self.pr_url = pr_url
        self.diff_context = diff_context or {}
        self.existing_comments = existing_comments or []
        self.auth_method = auth_method

    def is_new_line(self, file_path, line_num):
        """Check if a line number is within a diff hunk (new/changed line or context line).

        Returns True if the line falls within any hunk range, meaning it was part
        of the PR change context (either a new/changed line or a surrounding context line).
        """
        ctx = self.diff_context.get(file_path)
        if not ctx:
            return True
        for hunk in ctx.get('hunks', []):
            if hunk['new_start'] <= line_num <= hunk['new_end']:
                return True
        return False

    def is_pure_new_line(self, file_path, line_num):
        """Check if a line number is a pure new/added line (not context).

        Returns True only for '+' lines in the diff, not context lines.
        """
        ctx = self.diff_context.get(file_path)
        if not ctx:
            return False
        return line_num in ctx.get('new_added_lines', set())

    def get_hunk_info(self, file_path, line_num):
        """Get hunk info for a line number.

        Returns dict with 'new_start', 'new_end', 'hunk_header' or None.
        """
        ctx = self.diff_context.get(file_path)
        if not ctx:
            return None
        for hunk in ctx.get('hunks', []):
            if hunk['new_start'] <= line_num <= hunk['new_end']:
                return hunk
        return None


class PRScanner:
    def __init__(self, token=None):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        self._use_oh_gc = False
        self._oh_gc_repo = None

    def _ensure_oh_gc(self):
        """Try to detect and configure oh-gc CLI usage."""
        if not is_oh_gc_available():
            return False
        if self.token:
            return False
        self._use_oh_gc = True
        return True

    def _oh_gc_run(self, args, timeout=30):
        """Run an oh-gc CLI command and return (returncode, stdout, stderr)."""
        cmd = ['oh-gc'] + args
        if self._oh_gc_repo:
            cmd.extend(['--repo', self._oh_gc_repo])
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr

    def _http_get_json(self, url):
        if HAS_REQUESTS:
            resp = requests.get(url, params={"access_token": self.token}, timeout=30)
            resp.raise_for_status()
            return resp.json()
        else:
            sep = "&" if "?" in url else "?"
            full_url = f"{url}{sep}access_token={self.token}"
            req = urllib.request.Request(full_url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))

    def _http_get_text(self, url):
        if HAS_REQUESTS:
            resp = requests.get(url, params={"access_token": self.token}, timeout=30)
            resp.raise_for_status()
            return resp.text
        else:
            sep = "&" if "?" in url else "?"
            full_url = f"{url}{sep}access_token={self.token}"
            req = urllib.request.Request(full_url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode('utf-8')

    @staticmethod
    def parse_pr_url(pr_url):
        match = re.search(r"gitcode\.com/([^/]+)/([^/]+)/pulls?/(\d+)", pr_url)
        if not match:
            raise ValueError(f"Invalid GitCode PR URL format: {pr_url}\n"
                             f"Expected: https://gitcode.com/{{owner}}/{{repo}}/pulls/{{id}}")
        return {"owner": match.group(1), "repo": match.group(2), "pr_id": match.group(3)}

    def get_pr_details(self, owner, repo, pr_id):
        url = f"{GITCODE_API_BASE}/repos/{owner}/{repo}/pulls/{pr_id}"
        return self._http_get_json(url)

    def get_pr_files(self, owner, repo, pr_id):
        url = f"{GITCODE_API_BASE}/repos/{owner}/{repo}/pulls/{pr_id}/files.json"
        data = self._http_get_json(url)
        return data.get("diffs", [])

    def get_file_content(self, owner, repo, file_path, ref):
        url = f"{GITCODE_API_BASE}/repos/{owner}/{repo}/contents/{file_path}?ref={ref}"
        try:
            data = self._http_get_json(url)
            if "content" in data and data["content"]:
                return base64.b64decode(data["content"]).decode('utf-8', errors='replace')
        except Exception as e:
            logger.warning(f"Failed to fetch file content {file_path}@{ref}: {e}")
        return None

    def get_pr_diff(self, owner, repo, pr_id):
        """Fetch unified diff text for the PR.

        Tries oh-gc CLI first (if available), falls back to REST API.
        Returns raw diff text string.
        """
        if self._use_oh_gc:
            code, stdout, stderr = self._oh_gc_run(
                ['pr:diff', str(pr_id), '--color', 'never']
            )
            if code == 0 and stdout.strip():
                return stdout
            logger.warning(f"oh-gc pr:diff failed (code={code}), falling back to REST API")

        url = f"{GITCODE_API_BASE}/repos/{owner}/{repo}/pulls/{pr_id}.diff"
        try:
            return self._http_get_text(url)
        except Exception as e:
            logger.warning(f"Failed to fetch diff via REST API: {e}")
            return None

    def get_pr_comments(self, owner, repo, pr_id):
        """Fetch existing PR comments for deduplication.

        Fetches both PR-level comments and diff-level comments.
        Returns list of dicts with keys: type, path, line, body.

        Tries oh-gc CLI first (if available), falls back to REST API.
        """
        comments = []

        if self._use_oh_gc:
            for comment_type in ('pr_comment', 'diff_comment'):
                code, stdout, stderr = self._oh_gc_run([
                    'pr:comments', str(pr_id),
                    '--json', '--comment-type', comment_type, '--limit', '100'
                ])
                if code == 0 and stdout.strip():
                    parsed = _parse_json_safe(stdout)
                    if isinstance(parsed, list):
                        for c in parsed:
                            comments.append({
                                'type': comment_type,
                                'path': c.get('path', ''),
                                'line': c.get('line'),
                                'body': c.get('body', c.get('note', '')),
                            })
                    elif isinstance(parsed, dict) and 'data' in parsed:
                        for c in parsed['data']:
                            comments.append({
                                'type': comment_type,
                                'path': c.get('path', ''),
                                'line': c.get('line'),
                                'body': c.get('body', c.get('note', '')),
                            })
                elif code != 0:
                    logger.warning(f"oh-gc pr:comments ({comment_type}) failed: {stderr.strip()}")
            if comments:
                return comments

        if not self.token:
            return comments

        pr_comments_url = f"{GITCODE_API_BASE}/repos/{owner}/{repo}/pulls/{pr_id}/comments"
        reviews_url = f"{GITCODE_API_BASE}/repos/{owner}/{repo}/pulls/{pr_id}/reviews"

        for url, ctype in [(pr_comments_url, 'pr_comment'), (reviews_url, 'diff_comment')]:
            try:
                data = self._http_get_json(url)
                items = data if isinstance(data, list) else data.get('data', [])
                if isinstance(items, list):
                    for c in items:
                        comments.append({
                            'type': ctype,
                            'path': c.get('path', ''),
                            'line': c.get('line') or c.get('new_line'),
                            'body': c.get('body', c.get('note', c.get('text', ''))),
                        })
            except Exception as e:
                logger.warning(f"Failed to fetch {ctype}: {e}")

        return comments

    def fetch_pr_files(self, pr_url, output_dir=None, fetch_diff=True, fetch_comments=True):
        """Fetch PR changed files and optionally diff context + comments.

        Args:
            pr_url: GitCode PR URL
            output_dir: Local directory for downloaded files (default: temp dir)
            fetch_diff: Whether to fetch and parse unified diff (default: True)
            fetch_comments: Whether to fetch existing PR comments (default: True)

        Returns:
            PRScanResult with diff_context and existing_comments populated
        """
        pr_info = self.parse_pr_url(pr_url)
        owner, repo, pr_id = pr_info["owner"], pr_info["repo"], pr_info["pr_id"]
        self._oh_gc_repo = f"{owner}/{repo}"

        token, auth_method = resolve_token(self.token)
        if not token and not self._ensure_oh_gc():
            raise RuntimeError(
                "No authentication available. Choose one: "
                "1) npm install -g @oh-gc-cli && oh-gc auth:login, "
                "2) --token <TOKEN>, "
                "3) export GITCODE_TOKEN=<TOKEN>. "
                "Get token at: https://gitcode.com/-/profile/personal_access_tokens"
            )
        if token and not self.token:
            self.token = token
            self.headers["Authorization"] = f"Bearer {token}"

        logger.info(f"Fetching PR: {owner}/{repo}#{pr_id} (auth: {auth_method})")

        pr_details = self.get_pr_details(owner, repo, pr_id)
        pr_title = pr_details.get("title", "")
        pr_description = pr_details.get("body", "")

        head_sha = (pr_details.get("head", {}).get("sha")
                    or pr_details.get("head_sha")
                    or pr_details.get("merge_commit_sha"))

        pr_files = self.get_pr_files(owner, repo, pr_id)
        logger.info(f"PR has {len(pr_files)} changed files")

        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix=f"xts_pr_{owner}_{repo}_{pr_id}_")

        os.makedirs(output_dir, exist_ok=True)

        changed_files = []
        file_contents = {}

        for file_info in pr_files:
            stat = file_info.get("statistic", {})
            if not isinstance(stat, dict):
                stat = {}
            new_path = (stat.get("new_path")
                        or stat.get("path")
                        or file_info.get("new_path")
                        or file_info.get("filename")
                        or file_info.get("path", ""))

            if not new_path:
                continue

            ext = os.path.splitext(new_path)[1].lower()
            status = (stat.get("type", "modified")
                      or file_info.get("status", "modified"))

            if status.lower() == "deleted":
                continue

            basename = os.path.basename(new_path)
            if ext not in EXTS_OF_INTEREST and basename not in SPECIAL_FILES:
                continue

            head_info = file_info.get("head", {})
            raw_url = head_info.get("url", "")

            local_path = os.path.join(output_dir, new_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            content = None
            if raw_url:
                try:
                    content = self._http_get_text(raw_url)
                except Exception as e:
                    logger.warning(f"  Failed to download from raw URL: {e}")

            if content is None and head_sha:
                content = self.get_file_content(owner, repo, new_path, head_sha)

            if content is not None:
                with open(local_path, 'w', encoding='utf-8', errors='replace') as f:
                    f.write(content)
                file_contents[new_path] = content
                changed_files.append(new_path)
                logger.info(f"  Downloaded: {new_path}")
            else:
                logger.warning(f"  Skipped (no content): {new_path}")

        diff_context = {}
        if fetch_diff:
            diff_text = self.get_pr_diff(owner, repo, pr_id)
            if diff_text:
                diff_context = parse_unified_diff(diff_text)
                filtered = {}
                for path, ctx in diff_context.items():
                    if path in file_contents:
                        filtered[path] = ctx
                diff_context = filtered
                logger.info(f"Diff context: {len(diff_context)} files with hunk info")

        existing_comments = []
        if fetch_comments:
            existing_comments = self.get_pr_comments(owner, repo, pr_id)
            logger.info(f"Existing comments: {len(existing_comments)} fetched")

        result = PRScanResult(
            owner=owner,
            repo=repo,
            pr_id=pr_id,
            pr_title=pr_title,
            pr_description=pr_description,
            local_dir=output_dir,
            changed_files=changed_files,
            file_contents=file_contents,
            pr_url=pr_url,
            diff_context=diff_context,
            existing_comments=existing_comments,
            auth_method=auth_method,
        )

        logger.info(f"Downloaded {len(changed_files)} files to {output_dir}")
        return result


def parse_unified_diff(diff_text):
    """Parse unified diff text into per-file diff context.

    Adapted from review-gitcode-pr/scripts/collect_pr_context.py::parse_unified_diff().

    Returns dict mapping file path -> {
        'hunks': [{'header': str, 'old_start': int, 'old_count': int,
                   'new_start': int, 'new_count': int}],
        'new_added_lines': set of line numbers that are pure '+' lines,
        'commentable_lines': sorted list of all commentable line numbers,
    }
    """
    files = {}
    current = None
    old_line = None
    new_line = None

    hunk_re = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")

    for raw_line in diff_text.splitlines():
        if raw_line.startswith("diff --git "):
            parts = raw_line.split()
            path = parts[3][2:] if len(parts) >= 4 and parts[3].startswith("b/") else None
            current = {
                "path": path,
                "hunks": [],
                "new_added_lines": set(),
                "commentable_lines": [],
            }
            files[path] = current
            old_line = None
            new_line = None
            continue

        if current is None:
            continue

        if raw_line.startswith("+++ "):
            target = raw_line[4:].strip()
            if target.startswith("b/"):
                path = target[2:]
            elif target != "/dev/null":
                path = target
            else:
                continue
            old_entry = files.pop(current["path"], None)
            current["path"] = path
            files[path] = current
            continue

        match = hunk_re.match(raw_line)
        if match:
            old_line = int(match.group(1))
            new_line = int(match.group(3))
            current["hunks"].append({
                "header": raw_line,
                "old_start": old_line,
                "old_count": int(match.group(2) or "1"),
                "new_start": new_line,
                "new_count": int(match.group(4) or "1"),
            })
            continue

        if old_line is None or new_line is None or not current["hunks"]:
            continue

        if not raw_line:
            continue

        prefix = raw_line[0]
        if prefix == "+":
            current["new_added_lines"].add(new_line)
            current["commentable_lines"].append(new_line)
            new_line += 1
        elif prefix == " ":
            current["commentable_lines"].append(new_line)
            old_line += 1
            new_line += 1
        elif prefix == "-":
            old_line += 1

    for item in files.values():
        item["commentable_lines"] = sorted(set(item["commentable_lines"]))

    return files


def deduplicate_issues(issues, existing_comments, diff_context=None):
    """Filter out issues that have already been reported in PR comments.

    Deduplication strategy:
    1. For diff-level comments: match by (file, line, rule_id)
    2. For PR-level comments: match by rule_id mention in comment body
    3. If diff_context is provided, only keep issues on new/changed lines

    Args:
        issues: List of issue dicts from scanning
        existing_comments: List of comment dicts from PRScanner.get_pr_comments()
        diff_context: Optional dict from parse_unified_diff()

    Returns:
        Filtered list of new (non-duplicate) issues
    """
    if not existing_comments and not diff_context:
        return issues

    reported = set()
    reported_rules_in_pr = set()

    for comment in existing_comments:
        path = comment.get('path', '')
        line = comment.get('line')
        body = comment.get('body', '')

        if comment.get('type') == 'diff_comment' and path and line is not None:
            try:
                line_int = int(line)
            except (TypeError, ValueError):
                continue
            rule_match = re.search(r'\b(R\d{3}|C\d{3}|R\d{3}_\w+)\b', body)
            if rule_match:
                reported.add((path, line_int, rule_match.group(1)))
            reported.add((path, line_int, '*'))

        if comment.get('type') == 'pr_comment':
            for m in re.finditer(r'\b(R\d{3}|C\d{3}|R\d{3}_\w+)\b', body):
                reported_rules_in_pr.add(m.group(1))

    new_issues = []
    for issue in issues:
        file_path = issue.get('file', '')
        line = issue.get('line', 0)
        rule = issue.get('rule', '')

        if diff_context:
            ctx = diff_context.get(file_path)
            if ctx and ctx.get('commentable_lines'):
                if line not in ctx['commentable_lines']:
                    continue

        if (file_path, line, rule) in reported:
            continue
        if (file_path, line, '*') in reported:
            continue
        if rule in reported_rules_in_pr:
            continue

        new_issues.append(issue)

    filtered_count = len(issues) - len(new_issues)
    if filtered_count > 0:
        logger.info(f"Comment dedup: removed {filtered_count} already-reported issues "
                     f"({len(issues)} -> {len(new_issues)})")

    return new_issues


def _parse_json_safe(text):
    """Parse JSON text, handling various formats."""
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description='GitCode PR File Fetcher v1.0')
    parser.add_argument('pr_url', help='GitCode PR URL (e.g., https://gitcode.com/owner/repo/pull/123)')
    parser.add_argument('--token', default=None, help='GitCode Personal Access Token (auto-detects oh-gc)')
    parser.add_argument('--output', default=None, help='Output directory (default: temp dir)')
    parser.add_argument('--json', action='store_true', help='Output result as JSON')
    parser.add_argument('--no-diff', action='store_true', help='Skip diff context fetching')
    parser.add_argument('--no-comments', action='store_true', help='Skip existing comments fetching')
    args = parser.parse_args()

    scanner = PRScanner(token=args.token)
    result = scanner.fetch_pr_files(
        args.pr_url,
        output_dir=args.output,
        fetch_diff=not args.no_diff,
        fetch_comments=not args.no_comments,
    )

    if args.json:
        info = {
            "owner": result.owner,
            "repo": result.repo,
            "pr_id": result.pr_id,
            "pr_title": result.pr_title,
            "pr_description": result.pr_description,
            "local_dir": result.local_dir,
            "changed_files": result.changed_files,
            "file_count": len(result.changed_files),
            "pr_url": result.pr_url,
            "auth_method": result.auth_method,
            "diff_files": list(result.diff_context.keys()),
            "diff_file_count": len(result.diff_context),
            "existing_comments_count": len(result.existing_comments),
        }
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        print(f"PR: {result.owner}/{result.repo}#{result.pr_id}")
        print(f"Title: {result.pr_title}")
        print(f"Auth: {result.auth_method}")
        print(f"Files: {len(result.changed_files)}")
        print(f"Diff context: {len(result.diff_context)} files")
        print(f"Existing comments: {len(result.existing_comments)}")
        print(f"Output: {result.local_dir}")
        for f in result.changed_files:
            ctx = result.diff_context.get(f)
            if ctx:
                hunks = len(ctx.get('hunks', []))
                new_lines = len(ctx.get('new_added_lines', set()))
                print(f"  {f} ({hunks} hunks, {new_lines} new lines)")
            else:
                print(f"  {f}")


if __name__ == '__main__':
    main()
