#!/usr/bin/env python3
"""
Repository API client + code change analyzer.

Platform-agnostic support for:
- GitLab/GitCode (API v4)
- GitHub (REST API v3)
- Generic git repositories (web-based fallback)

Features:
- Create Issue and PR/MR
- Analyze git diff for change summaries
- Generate Issue/PR titles and descriptions
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional


class RepoAPI:
    """Platform-agnostic repository API client."""

    def __init__(self, token: Optional[str] = None, project_id: Optional[str] = None, repo_root: str = "."):
        self.token = token or self._load_token()
        self.repo_root = Path(repo_root).resolve()
        # Auto-detect platform and project_id from remote URL if not provided
        if project_id is None:
            self.owner, self.repo = self._detect_project_config()
        else:
            # Parse provided project_id (support both "owner/repo" and "owner%2Frepo" formats)
            import urllib.parse
            decoded = urllib.parse.unquote(project_id)
            if "/" in decoded:
                self.owner, self.repo = decoded.split("/", 1)
            else:
                self.owner, self.repo = "", project_id
        self.platform = self._detect_platform()

    def _load_token(self) -> str:
        """Load token from env, git config, or local files (in that order)."""
        # Try environment variables
        for env_var in ["GITHUB_TOKEN", "GITCODE_TOKEN", "GITLAB_TOKEN", "REPO_TOKEN"]:
            token = os.environ.get(env_var)
            if token:
                return token.strip()

        # Try git config
        for config_key in ["github.token", "gitcode.token", "gitlab.token", "repo.token"]:
            try:
                result = subprocess.run(
                    ["git", "config", "--get", config_key],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                token = result.stdout.strip()
                if token:
                    return token
            except Exception:
                pass

        # Try token files
        token_paths = [
            "~/.github-token",
            "~/.gitcode-token",
            "~/.gitlab-token",
            "~/.repo-token",
            "~/.config/github/token",
            "~/.config/gitcode/token",
        ]
        for path in token_paths:
            expanded = Path(path).expanduser()
            if expanded.exists():
                return expanded.read_text().strip()

        # No token found - will use web-based fallback
        return ""

    def _detect_platform(self) -> str:
        """Detect platform from git remote URL."""
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                check=True,
            )
            remote_url = result.stdout.strip()

            if "github.com" in remote_url:
                return "github"
            elif "gitcode.com" in remote_url:
                return "gitcode"
            elif "gitlab.com" in remote_url:
                return "gitlab"
            else:
                return "unknown"
        except Exception:
            return "unknown"

    def _detect_project_config(self) -> tuple:
        """Detect owner and repo from git remote URL.
        Returns (owner, repo) tuple.
        """
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                check=True,
            )
            remote_url = result.stdout.strip()

            # Extract owner/repo from URL
            # Supports: https://github.com/owner/repo.git or git@github.com:owner/repo.git
            match = re.search(r"[/:]([^/]+)/([^/]+?)(\.git)?$", remote_url)
            if match:
                owner, repo = match.groups()[0:2]
                return owner, repo
            return "", ""
        except Exception:
            return "", ""

    def _get_api_base(self) -> str:
        """Get API base URL for detected platform."""
        if self.platform == "github":
            return "https://api.github.com"
        elif self.platform == "gitcode":
            return "https://api.gitcode.com/api/v5"
        elif self.platform == "gitlab":
            return "https://gitlab.com/api/v4"
        else:
            # Default to GitCode-compatible API
            return "https://api.gitcode.com/api/v5"

    def _get_project_id(self) -> str:
        """Get project_id in the format expected by the detected platform."""
        import urllib.parse
        if self.platform == "github" or self.platform == "gitcode":
            # GitHub and GitCode use owner/repo format without encoding
            # Format: /repos/{owner}/{repo}/...
            return f"{self.owner}/{self.repo}"
        else:
            # GitLab uses URL-encoded owner%2Frepo format
            # Format: /projects/{owner}%2F{repo}/...
            return urllib.parse.quote(f"{self.owner}/{self.repo}", safe='')

    def _api_request(
        self, endpoint: str, data: Optional[Dict] = None, method: str = "POST"
    ) -> Dict:
        api_base = self._get_api_base()
        url = f"{api_base}/{endpoint}"

        # Different auth headers for different platforms
        if self.platform == "github":
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/vnd.github.v3+json"
            }
        else:
            headers = {
                "PRIVATE-TOKEN": self.token,
                "Content-Type": "application/json"
            }

        req_data = None
        if data is not None:
            req_data = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise RepoAPIError(
                f"API error {e.code}: {error_body}\n"
                f"URL: {url}\n"
                f"Method: {method}\n"
                f"Platform: {self.platform}\n"
                f"Project: {self.owner}/{self.repo}"
            )
        except Exception as e:
            raise RepoAPIError(
                f"Request failed: {e}\n"
                f"URL: {url}\n"
                f"Method: {method}\n"
                f"Platform: {self.platform}"
            )

    def create_issue(self, title: str, description: str, labels: Optional[List[str]] = None) -> Optional[Dict]:
        """Create an issue using the platform API."""
        if not self.token:
            print("[INFO] No API token configured, skipping Issue creation")
            return None

        if self.platform == "github" or self.platform == "gitcode":
            # GitHub & GitCode API: /repos/{owner}/{repo}/issues
            endpoint = f"repos/{self._get_project_id()}/issues"
            data = {"title": title, "body": description}
            if labels:
                data["labels"] = labels
        else:
            # GitLab API: /projects/{id}/issues
            endpoint = f"projects/{self._get_project_id()}/issues"
            data = {"title": title, "description": description}
            if labels:
                data["labels"] = ",".join(labels)

        try:
            return self._api_request(endpoint, data)
        except RepoAPIError as e:
            print(f"[WARNING] Failed to create Issue: {e}")
            return None

    def create_pr(
        self,
        source_branch: str,
        title: str,
        description: str,
        target_branch: str = "master",
        remove_source_branch: bool = False,
    ) -> Optional[Dict]:
        """Create a PR/MR using the platform API."""
        if not self.token:
            print("[INFO] No API token configured, will use web interface")
            return None

        if self.platform == "github":
            # GitHub API: /repos/{owner}/{repo}/pulls
            # For fork repos, create PR in upstream repo
            if self.is_fork() and self.get_upstream_owner():
                upstream_owner = self.get_upstream_owner()
                endpoint = f"repos/{upstream_owner}/{self.repo}/pulls"
            else:
                endpoint = f"repos/{self._get_project_id()}/pulls"
            data = {
                "head": source_branch,
                "base": target_branch,
                "title": title,
                "body": description,
            }
        elif self.platform == "gitcode":
            # GitCode API v5: /repos/{owner}/{repo}/pulls
            # For fork repos, create PR in upstream repo
            if self.is_fork() and self.get_upstream_owner():
                upstream_owner = self.get_upstream_owner()
                endpoint = f"repos/{upstream_owner}/{self.repo}/pulls"
            else:
                endpoint = f"repos/{self._get_project_id()}/pulls"
            data = {
                "head": source_branch,
                "base": target_branch,
                "title": title,
                "body": description,
            }
        else:
            # GitLab API: /projects/{id}/merge_requests
            endpoint = f"projects/{self._get_project_id()}/merge_requests"
            data = {
                "source_branch": source_branch,
                "target_branch": target_branch,
                "title": title,
                "description": description,
                "remove_source_branch": remove_source_branch,
            }

        try:
            return self._api_request(endpoint, data)
        except RepoAPIError as e:
            print(f"[WARNING] Failed to create PR: {e}")
            return None

    def is_fork(self) -> bool:
        """Check if the current repository is a fork."""
        try:
            # Try to get repository info from API
            if not self.token:
                # Without token, check git remotes
                result = subprocess.run(
                    ["git", "remote", "-v"],
                    cwd=str(self.repo_root),
                    capture_output=True,
                    text=True,
                    check=False,
                )
                remotes = result.stdout.strip()
                # If there's an 'upstream' remote, it's likely a fork
                return "upstream" in remotes
            else:
                # Use API to check
                if self.platform == "github":
                    endpoint = f"repos/{self._get_project_id()}"
                elif self.platform == "gitcode":
                    endpoint = f"repos/{self._get_project_id()}"
                else:
                    endpoint = f"projects/{self._get_project_id()}"

                repo_info = self._api_request(endpoint, method="GET")

                if self.platform == "github":
                    return repo_info.get("fork", False)
                elif self.platform == "gitcode":
                    return repo_info.get("fork", False)
                else:
                    return repo_info.get("forked_from_project", None) is not None
        except Exception:
            return False

    def get_fork_owner(self) -> Optional[str]:
        """Get the fork owner (current user/org) for fork repositories.
        Returns None if not a fork.
        """
        if not self.is_fork():
            return None
        # For fork repos, the current owner is the fork owner
        return self.owner

    def get_upstream_owner(self) -> Optional[str]:
        """Get the upstream/original repository owner for fork repositories.
        Returns None if not a fork or cannot determine.
        """
        try:
            if not self.token:
                # Try to get from git remote 'upstream'
                result = subprocess.run(
                    ["git", "config", "--get", "remote.upstream.url"],
                    cwd=str(self.repo_root),
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0 and result.stdout.strip():
                    upstream_url = result.stdout.strip()
                    match = re.search(r"[/:]([^/]+)/", upstream_url)
                    if match:
                        return match.group(1)
                return None
            else:
                # Use API to get upstream info
                if self.platform == "github":
                    endpoint = f"repos/{self._get_project_id()}"
                    repo_info = self._api_request(endpoint, method="GET")
                    return repo_info.get("parent", {}).get("owner", {}).get("login")
                elif self.platform == "gitcode":
                    endpoint = f"repos/{self._get_project_id()}"
                    repo_info = self._api_request(endpoint, method="GET")
                    # GitCode may return parent or original info
                    return repo_info.get("parent", {}).get("owner", {}).get("login") or \
                           repo_info.get("original", {}).get("owner", {}).get("login")
                else:
                    endpoint = f"projects/{self._get_project_id()}"
                    repo_info = self._api_request(endpoint, method="GET")
                    forked_from = repo_info.get("forked_from_project")
                    if forked_from:
                        # Extract owner from namespace or full_name
                        namespace = forked_from.get("namespace", {})
                        return namespace.get("path") if namespace else None
                return None
        except Exception:
            return None

    def get_web_pr_url(self) -> str:
        """Get the web URL for creating a PR manually."""
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                check=True,
            )
            remote_url = result.stdout.strip()

            # Convert git URL to web URL
            if remote_url.startswith("git@"):
                # git@github.com:owner/repo.git -> https://github.com/owner/repo
                match = re.search(r"git@[^:]+:([^/]+)/([^/]+?)(\.git)?$", remote_url)
                if match:
                    owner, repo = match.groups()[0:2]
                    domain = re.search(r"@([^:]+):", remote_url).group(1)
                    return f"https://{domain}/{owner}/{repo}/pull/new"
            elif "https://" in remote_url:
                # https://github.com/owner/repo.git -> https://github.com/owner/repo/pull/new
                match = re.search(r"https://([^/]+)/([^/]+)/([^/]+?)(\.git)?$", remote_url)
                if match:
                    domain, owner, repo = match.groups()[0:3]
                    return f"https://{domain}/{owner}/{repo}/pull/new"

            return ""
        except Exception:
            return ""


class RepoAPIError(Exception):
    pass


class CodeAnalyzer:
    """Analyze code changes to build Issue/PR descriptions."""

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root).resolve()

    def _run_git(self, *args, encoding: str = "utf-8", errors: str = "ignore") -> str:
        result = subprocess.run(
            ["git"] + list(args),
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
            encoding=encoding,
            errors=errors,
            check=False,
        )
        return result.stdout.strip()

    def _has_remote_branch(self, base_branch: str) -> bool:
        output = self._run_git("rev-parse", "--verify", f"origin/{base_branch}")
        return bool(output.strip())

    def get_current_branch(self) -> str:
        return self._run_git("rev-parse", "--abbrev-ref", "HEAD")

    def get_remote_url(self) -> str:
        return self._run_git("config", "--get", "remote.origin.url")

    def extract_fork_owner(self) -> str:
        """Extract owner from remote URL.
        For fork workflows, this should be the upstream owner, not the fork owner.
        Returns empty string if this is not a fork (most common case).
        """
        remote_url = self.get_remote_url()
        # Extract owner from URL like https://gitcode.com/owner/repo.git or git@gitcode.com:owner/repo.git
        match = re.search(r"[/:]([^/]+)/", remote_url)
        if match:
            return match.group(1)
        raise ValueError(f"Unable to extract owner from URL: {remote_url}")

    def get_changed_files(self, base_branch: str = "master") -> List[str]:
        if self._has_remote_branch(base_branch):
            output = self._run_git("diff", "--name-only", f"origin/{base_branch}...HEAD")
        else:
            output = self._run_git("diff", "--name-only", "HEAD")
        return [line for line in output.split("\n") if line]

    def get_diff_stat(self, base_branch: str = "master") -> str:
        if self._has_remote_branch(base_branch):
            return self._run_git("diff", "--stat", f"origin/{base_branch}...HEAD")
        return self._run_git("diff", "--stat", "HEAD")

    def get_diff_content(self, base_branch: str = "master", context_lines: int = 3) -> str:
        if self._has_remote_branch(base_branch):
            return self._run_git("diff", f"-U{context_lines}", f"origin/{base_branch}...HEAD")
        return self._run_git("diff", f"-U{context_lines}", "HEAD")

    def get_commit_messages(self, base_branch: str = "master") -> List[str]:
        if self._has_remote_branch(base_branch):
            output = self._run_git("log", "--oneline", f"origin/{base_branch}..HEAD")
        else:
            output = self._run_git("log", "--oneline", "-5")
        return [line for line in output.split("\n") if line]

    def analyze_change_type(self, commits: List[str], files: Optional[List[str]] = None) -> str:
        counts = {
            "feat": sum(1 for c in commits if c.startswith("feat:")),
            "fix": sum(1 for c in commits if c.startswith("fix:")),
            "docs": sum(1 for c in commits if c.startswith("docs:")),
            "refactor": sum(1 for c in commits if c.startswith("refactor:")),
            "test": sum(1 for c in commits if c.startswith("test:")),
            "chore": sum(1 for c in commits if c.startswith("chore:")),
        }
        max_type = max(counts.items(), key=lambda x: x[1])[0]
        if counts[max_type] > 0:
            return max_type

        text = " ".join(commits).lower()
        if any(k in text for k in ["fix", "bug", "issue", "error", "crash"]):
            return "fix"
        if any(k in text for k in ["refactor", "cleanup", "simplify"]):
            return "refactor"
        if any(k in text for k in ["doc", "readme", "markdown"]):
            return "docs"

        if files:
            if any("/test/" in f or "test_" in f for f in files):
                return "test"
            if any(f.endswith(".md") for f in files):
                return "docs"

        return "chore"

    def detect_affected_components(self, files: List[str]) -> List[str]:
        components = set()
        for file in files:
            if "components_ng/pattern/" in file:
                parts = file.split("components_ng/pattern/")
                if len(parts) > 1:
                    component = parts[1].split("/")[0]
                    components.add(component.capitalize())
            if "bridge/declarative_frontend" in file:
                components.add("DeclarativeFrontend")
            if "adapter/" in file:
                components.add("PlatformAdapter")
            if "test/" in file or "tests/" in file:
                components.add("Tests")
        return sorted(components)

    def analyze_code_changes(self, base_branch: str = "master") -> Dict[str, object]:
        diff_content = self.get_diff_content(base_branch)
        changes = {
            "added_functions": [],
            "removed_functions": [],
            "modified_functions": [],
            "added_classes": [],
            "removed_classes": [],
            "modified_classes": [],
            "key_changes": [],
            "file_summaries": {},
        }
        if not diff_content:
            return changes

        current_file = None
        added_funcs: List[str] = []
        removed_funcs: List[str] = []
        added_classes: List[str] = []
        removed_classes: List[str] = []

        for line in diff_content.split("\n"):
            if line.startswith("diff --git"):
                parts = line.split(" b/")
                current_file = parts[-1] if len(parts) > 1 else None
                if current_file:
                    changes["file_summaries"][current_file] = {"added": 0, "removed": 0}
                continue

            if not current_file:
                continue

            if line.startswith("+") and not line.startswith("+++"):
                changes["file_summaries"][current_file]["added"] += 1
                func_name = self._extract_function_name(line)
                if func_name:
                    added_funcs.append(f"{current_file}:{func_name}")
                class_name = self._extract_class_name(line)
                if class_name:
                    added_classes.append(f"{current_file}:{class_name}")
                continue

            if line.startswith("-") and not line.startswith("---"):
                changes["file_summaries"][current_file]["removed"] += 1
                func_name = self._extract_function_name(line)
                if func_name:
                    removed_funcs.append(f"{current_file}:{func_name}")
                class_name = self._extract_class_name(line)
                if class_name:
                    removed_classes.append(f"{current_file}:{class_name}")
                continue

        added_func_set = set(added_funcs)
        removed_func_set = set(removed_funcs)
        added_class_set = set(added_classes)
        removed_class_set = set(removed_classes)

        changes["modified_functions"] = sorted(added_func_set & removed_func_set)
        changes["added_functions"] = sorted(added_func_set - set(changes["modified_functions"]))
        changes["removed_functions"] = sorted(removed_func_set - set(changes["modified_functions"]))

        changes["modified_classes"] = sorted(added_class_set & removed_class_set)
        changes["added_classes"] = sorted(added_class_set - set(changes["modified_classes"]))
        changes["removed_classes"] = sorted(removed_class_set - set(changes["modified_classes"]))

        file_changes = sorted(
            changes["file_summaries"].items(),
            key=lambda x: x[1]["added"] + x[1]["removed"],
            reverse=True,
        )
        for file, stats in file_changes[:10]:
            total = stats["added"] + stats["removed"]
            changes["key_changes"].append(f"{file}: +{stats['added']} -{stats['removed']} ({total} lines)")

        return changes

    def _extract_function_name(self, line: str) -> Optional[str]:
        blacklist = {"if", "for", "while", "switch", "return", "catch"}
        patterns = [
            r"\bdef\s+([A-Za-z_]\w*)\s*\(",
            r"\bfunction\s+([A-Za-z_]\w*)\s*\(",
            r"\b([A-Za-z_]\w*)\s*\([^;{]*\)\s*\{?",
        ]
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                name = match.group(1)
                if name not in blacklist:
                    return name
        return None

    def _extract_class_name(self, line: str) -> Optional[str]:
        match = re.search(r"\bclass\s+([A-Za-z_]\w*)", line)
        return match.group(1) if match else None

    def generate_summary(self, commits: List[str], files: List[str], components: List[str]) -> str:
        change_type = self.analyze_change_type(commits, files)
        type_desc = {
            "feat": "feature",
            "fix": "fix",
            "docs": "docs",
            "refactor": "refactor",
            "test": "tests",
            "chore": "chore",
        }
        summary = type_desc.get(change_type, "change")
        if components:
            summary += f" | components: {', '.join(components)}"
        return summary

    def generate_issue_title(self, commits: List[str], components: List[str]) -> str:
        change_type = self.analyze_change_type(commits)
        short_desc = "Code changes"
        if commits:
            first_commit = commits[0]
            parts = first_commit.split(": ", 1)
            short_desc = parts[1] if len(parts) > 1 else first_commit
        if len(short_desc) > 60:
            short_desc = short_desc[:57] + "..."
        title = f"{change_type}: {short_desc}"
        if components:
            title += f" [{', '.join(components)}]"
        return title

    def generate_pr_title(self, commits: List[str]) -> str:
        if commits:
            first_commit = commits[0]
            parts = first_commit.split(": ", 1)
            desc = parts[1] if len(parts) > 1 else first_commit
            desc = desc[:1].upper() + desc[1:] if desc else "Code changes"
            return f"Auto PR: {desc}"
        return "Auto PR: Code changes"

    def generate_issue_description(
        self,
        commits: List[str],
        files: List[str],
        components: List[str],
        diff_stat: str,
        code_analysis: Optional[Dict] = None,
    ) -> str:
        change_type = self.analyze_change_type(commits, files)
        summary = self.generate_summary(commits, files, components)

        file_stats: Dict[str, int] = {}
        for file in files:
            ext = Path(file).suffix or "(no extension)"
            file_stats[ext] = file_stats.get(ext, 0) + 1

        desc = []
        desc.append(f"## {summary}")
        desc.append("")
        if components:
            desc.append(f"**Affected Components**: {', '.join(components)}")
        desc.append(f"**Change Type**: {change_type}")
        desc.append(f"**Changed Files**: {len(files)}")
        desc.append("")

        if code_analysis:
            if code_analysis.get("added_functions"):
                desc.append("### Added Functions")
                for func in code_analysis["added_functions"][:10]:
                    desc.append(f"- `{func}`")
                if len(code_analysis["added_functions"]) > 10:
                    desc.append(f"- ... and {len(code_analysis['added_functions']) - 10} more")
                desc.append("")
            if code_analysis.get("modified_functions"):
                desc.append("### Modified Functions")
                for func in code_analysis["modified_functions"][:10]:
                    desc.append(f"- `{func}`")
                if len(code_analysis["modified_functions"]) > 10:
                    desc.append(f"- ... and {len(code_analysis['modified_functions']) - 10} more")
                desc.append("")
            if code_analysis.get("added_classes"):
                desc.append("### Added Classes")
                for cls in code_analysis["added_classes"][:10]:
                    desc.append(f"- `{cls}`")
                if len(code_analysis["added_classes"]) > 10:
                    desc.append(f"- ... and {len(code_analysis['added_classes']) - 10} more")
                desc.append("")
            if code_analysis.get("modified_classes"):
                desc.append("### Modified Classes")
                for cls in code_analysis["modified_classes"][:10]:
                    desc.append(f"- `{cls}`")
                if len(code_analysis["modified_classes"]) > 10:
                    desc.append(f"- ... and {len(code_analysis['modified_classes']) - 10} more")
                desc.append("")
            if code_analysis.get("key_changes"):
                desc.append("### Key File Changes")
                for item in code_analysis["key_changes"]:
                    desc.append(f"- {item}")
                desc.append("")

        if file_stats:
            desc.append("### File Type Stats")
            for ext, count in sorted(file_stats.items(), key=lambda x: -x[1]):
                desc.append(f"- `{ext}`: {count} files")
            desc.append("")

        if commits:
            desc.append("### Commit History")
            for commit in commits[:10]:
                desc.append(f"- {commit}")
            if len(commits) > 10:
                desc.append(f"- ... and {len(commits) - 10} more")
            desc.append("")

        if diff_stat:
            desc.append("### Diff Stat")
            desc.append("")
            desc.append("```")
            desc.append(diff_stat)
            desc.append("```")
            desc.append("")

        desc.append("---")
        desc.append("Generated by create-pr skill")
        return "\n".join(desc)

    def generate_pr_description(
        self,
        commits: List[str],
        files: List[str],
        components: List[str],
        diff_stat: str,
        issue_number: Optional[int] = None,
        code_analysis: Optional[Dict] = None,
    ) -> str:
        change_type = self.analyze_change_type(commits, files)
        action = {
            "feat": "Add",
            "fix": "Fix",
            "docs": "Update",
            "refactor": "Refactor",
            "test": "Test",
            "chore": "Chore",
        }.get(change_type, "Change")

        main_changes = []
        for commit in commits[:5]:
            parts = commit.split(": ", 1)
            main_changes.append(parts[1] if len(parts) > 1 else commit)

        desc = []
        desc.append("## Summary")
        desc.append("")
        if main_changes:
            for change in main_changes:
                desc.append(f"- {action} {change}")
        else:
            desc.append(f"- {action} code changes")
        desc.append("")

        desc.append("## Changes")
        desc.append("")
        if code_analysis:
            if code_analysis.get("added_functions"):
                desc.append("### Added Functions")
                for func in code_analysis["added_functions"][:15]:
                    desc.append(f"- `{func}`")
                if len(code_analysis["added_functions"]) > 15:
                    desc.append(f"- ... and {len(code_analysis['added_functions']) - 15} more")
                desc.append("")
            if code_analysis.get("modified_functions"):
                desc.append("### Modified Functions")
                for func in code_analysis["modified_functions"][:15]:
                    desc.append(f"- `{func}`")
                if len(code_analysis["modified_functions"]) > 15:
                    desc.append(f"- ... and {len(code_analysis['modified_functions']) - 15} more")
                desc.append("")
            if code_analysis.get("added_classes"):
                desc.append("### Added Classes")
                for cls in code_analysis["added_classes"][:10]:
                    desc.append(f"- `{cls}`")
                desc.append("")
            if code_analysis.get("modified_classes"):
                desc.append("### Modified Classes")
                for cls in code_analysis["modified_classes"][:10]:
                    desc.append(f"- `{cls}`")
                desc.append("")

        component_files: Dict[str, List[str]] = {}
        for file in files:
            if "components_ng/pattern/" in file:
                parts = file.split("components_ng/pattern/")
                component = parts[1].split("/")[0].capitalize() + " Component" if len(parts) > 1 else "Components NG"
            elif "bridge/" in file:
                component = "Bridge Layer"
            elif "test/" in file:
                component = "Tests"
            elif "adapter/" in file:
                component = "Platform Adapter"
            else:
                component = "Other"
            component_files.setdefault(component, []).append(file)

        for component in sorted(component_files.keys()):
            desc.append(f"### {component}")
            desc.append("")
            for file in component_files[component]:
                if code_analysis and code_analysis.get("file_summaries", {}).get(file):
                    stats = code_analysis["file_summaries"][file]
                    total = stats["added"] + stats["removed"]
                    desc.append(f"**{file}**: +{stats['added']} -{stats['removed']} ({total} lines)")
                else:
                    desc.append(f"**{file}**: updated")
            desc.append("")

        desc.append("## Test Plan")
        desc.append("")
        if any(c.startswith("test:") for c in commits):
            desc.append("- [x] Unit tests added/updated")
        else:
            desc.append("- [ ] Unit tests")
        desc.append("- [ ] Manual testing")
        desc.append("- [ ] Code review")
        desc.append("")

        if issue_number:
            desc.append("## Related Issue")
            desc.append("")
            desc.append(f"Fixes #{issue_number}")
            desc.append("")

        desc.append("---")
        desc.append("Generated by create-pr skill")
        return "\n".join(desc)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Repository API helper")
    parser.add_argument("command", choices=["create-issue", "create-pr", "analyze"])
    parser.add_argument("--token", help="Personal Access Token")
    parser.add_argument("--branch", help="Source branch (default: current)")
    parser.add_argument("--target", default="master", help="Target branch")
    parser.add_argument("--title", help="Issue/PR title")
    parser.add_argument("--description", help="Issue/PR description")
    parser.add_argument("--labels", help="Issue labels (comma-separated)")

    args = parser.parse_args()

    try:
        api = RepoAPI(args.token)
        analyzer = CodeAnalyzer()

        if args.command == "analyze":
            branch = args.branch or analyzer.get_current_branch()
            files = analyzer.get_changed_files(args.target)
            commits = analyzer.get_commit_messages(args.target)
            components = analyzer.detect_affected_components(files)
            diff_stat = analyzer.get_diff_stat(args.target)

            print("=== Analysis ===")
            print(f"Branch: {branch}")
            print(f"Platform: {api.platform}")
            print(f"Changed files: {len(files)}")
            print(f"Commits: {len(commits)}")
            print(f"Affected components: {', '.join(components) if components else 'None'}")
            print(f"Change type: {analyzer.analyze_change_type(commits, files)}")
            print("")
            print("--- Diff Stat ---")
            print(diff_stat)
            return 0

        if args.command == "create-issue":
            if not args.title:
                commits = analyzer.get_commit_messages(args.target)
                files = analyzer.get_changed_files(args.target)
                components = analyzer.detect_affected_components(files)
                args.title = analyzer.generate_issue_title(commits, components)

            if not args.description:
                commits = analyzer.get_commit_messages(args.target)
                files = analyzer.get_changed_files(args.target)
                components = analyzer.detect_affected_components(files)
                diff_stat = analyzer.get_diff_stat(args.target)
                code_analysis = analyzer.analyze_code_changes(args.target)
                args.description = analyzer.generate_issue_description(
                    commits, files, components, diff_stat, code_analysis
                )

            labels = args.labels.split(",") if args.labels else None
            result = api.create_issue(args.title, args.description, labels)
            if not result:
                return 1
            print("[OK] Issue created")
            print(f"  Issue ID: {result.get('iid')}")
            print(f"  Issue URL: {result.get('web_url')}")
            return 0

        if args.command == "create-pr":
            branch = args.branch or analyzer.get_current_branch()
            try:
                fork_owner = analyzer.extract_fork_owner()
                source_branch = f"{fork_owner}/{branch}"
            except Exception:
                source_branch = branch

            if not args.title:
                commits = analyzer.get_commit_messages(args.target)
                args.title = analyzer.generate_pr_title(commits)

            if not args.description:
                commits = analyzer.get_commit_messages(args.target)
                files = analyzer.get_changed_files(args.target)
                components = analyzer.detect_affected_components(files)
                diff_stat = analyzer.get_diff_stat(args.target)
                code_analysis = analyzer.analyze_code_changes(args.target)
                args.description = analyzer.generate_pr_description(
                    commits, files, components, diff_stat, None, code_analysis
                )

            result = api.create_pr(source_branch, args.title, args.description, args.target)
            if not result:
                return 1
            print("[OK] PR created")
            print(f"  PR ID: {result.get('iid')}")
            print(f"  PR URL: {result.get('web_url')}")
            return 0

        return 1

    except RepoAPIError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
