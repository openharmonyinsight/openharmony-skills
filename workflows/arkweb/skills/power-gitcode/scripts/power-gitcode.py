#!/usr/bin/env python3
"""
Power GitCode - GitCode 平台全能操作工具
提供 PR、Issue、模板、仓库管理等一站式 CLI 能力。
"""
import os
import sys
import json
import ssl
import http.client
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List, Tuple, Union


class GitCodeClient:
    """GitCode API 客户端"""

    API_BASE = "api.gitcode.com"

    def __init__(self, token: str = None):
        self.token = token or os.getenv("gitcode_password") or os.getenv("gitcode_token")
        if not self.token:
            print("错误: 未找到 GitCode 密钥。", file=sys.stderr)
            print("请通过以下任一方式配置（密钥仅在本地使用，不会发送给第三方）：", file=sys.stderr)
            print("  1. export gitcode_password=\"你的Token\"  (推荐)", file=sys.stderr)
            print("  2. export gitcode_token=\"你的Token\"", file=sys.stderr)
            print("获取 Token: GitCode → 设置 → 安全设置 → 私人令牌", file=sys.stderr)

    def _request(self, method: str, path: str, body: dict = None) -> Tuple[int, dict]:
        context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection(self.API_BASE, context=context)
        headers = {'Accept': 'application/json'}

        if self.token:
            if method in ("GET", "DELETE"):
                # GET/DELETE 用 query param 认证（GitCode 要求）
                sep = '&' if '?' in path else '?'
                path = f"{path}{sep}access_token={self.token}"
            else:
                # POST/PUT/PATCH 用 Bearer header
                headers['Authorization'] = f'Bearer {self.token}'

        if body:
            headers['Content-Type'] = 'application/json'

        payload = json.dumps(body, ensure_ascii=False).encode('utf-8') if body else ''
        try:
            conn.request(method, path, payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8", errors="ignore")
            try:
                parsed = json.loads(data) if data else {}
            except json.JSONDecodeError:
                parsed = {"raw_response": data}
            return res.status, parsed
        except Exception as e:
            return 0, {"error": str(e)}
        finally:
            conn.close()

    # ── PR 操作 ──

    def create_pr(self, owner, repo, title, head, base, body="",
                  fork_path=None, labels=None):
        path = f"/api/v5/repos/{owner}/{repo}/pulls"
        payload = {"title": title, "head": head, "base": base,
                   "body": body, "prune_source_branch": True, "squash": False}
        if fork_path:
            payload["fork_path"] = fork_path
        if labels:
            payload["labels"] = ",".join(labels) if isinstance(labels, list) else labels
        status, result = self._request("POST", path, payload)
        return 200 <= status < 300, result

    def get_pr(self, owner, repo, number):
        status, result = self._request("GET", f"/api/v5/repos/{owner}/{repo}/pulls/{number}",
                                       )
        return 200 <= status < 300, result

    def get_pr_commits(self, owner, repo, number):
        status, result = self._request("GET",
                                       f"/api/v5/repos/{owner}/{repo}/pulls/{number}/commits",
                                       )
        if 200 <= status < 300 and isinstance(result, list):
            return True, result
        return False, result

    def get_pr_changed_files(self, owner, repo, number, ignore_deleted=False):
        status, result = self._request("GET",
                                       f"/api/v5/repos/{owner}/{repo}/pulls/{number}/files",
                                       )
        if 200 <= status < 300 and isinstance(result, list):
            if ignore_deleted:
                result = [f for f in result if f.get("status") != "removed"]
            return True, result
        return False, result

    def get_pr_comments(self, owner, repo, number, page=1, per_page=100, direction="asc"):
        all_comments = []
        while True:
            path = (f"/api/v5/repos/{owner}/{repo}/pulls/{number}/comments"
                    f"?page={page}&per_page={per_page}&direction={direction}")
            status, result = self._request("GET", path, )
            if 200 <= status < 300 and isinstance(result, list):
                all_comments.extend(result)
                if len(result) < per_page:
                    break
                page += 1
            else:
                break
        return len(all_comments) > 0 or page == 1, all_comments

    def post_pr_comment(self, owner, repo, number, body, path=None, position=None):
        api_path = f"/api/v5/repos/{owner}/{repo}/pulls/{number}/comments"
        data = {"body": body}
        if path is not None:
            data["path"] = path
        if position is not None:
            data["position"] = position
        status, result = self._request("POST", api_path, data)
        return 200 <= status < 300, result

    def add_pr_labels(self, owner, repo, number, labels):
        path = f"/api/v5/repos/{owner}/{repo}/pulls/{number}/labels"
        label_list = labels if isinstance(labels, list) else [labels]
        status, result = self._request("POST", path, label_list)
        return 200 <= status < 300, result

    def remove_pr_labels(self, owner, repo, number, label):
        path = f"/api/v5/repos/{owner}/{repo}/pulls/{number}/labels/{label}"
        status, result = self._request("DELETE", path)
        return 200 <= status < 300, result

    def assign_pr_testers(self, owner, repo, number, testers):
        path = f"/api/v5/repos/{owner}/{repo}/pulls/{number}/testers"
        tester_list = testers if isinstance(testers, list) else [testers]
        status, result = self._request("POST", path, {"assignees": tester_list})
        return 200 <= status < 300, result

    def check_pr_mergeable(self, owner, repo, number):
        ok, pr = self.get_pr(owner, repo, number)
        if ok:
            return True, {"mergeable": pr.get("mergeable", False),
                          "state": pr.get("state"), "title": pr.get("title")}
        return False, pr

    def merge_pr(self, owner, repo, number, method="merge"):
        path = f"/api/v5/repos/{owner}/{repo}/pulls/{number}/merge"
        status, result = self._request("PUT", path, {"merge_method": method})
        return 200 <= status < 300, result

    # ── Issue 操作 ──

    def create_issue(self, owner, repo, title, body="", labels=None):
        path = f"/api/v5/repos/{owner}/issues"
        payload = {"repo": repo, "title": title, "body": body}
        if labels:
            if isinstance(labels, list):
                payload["labels"] = ",".join(str(l) for l in labels if l)
            else:
                payload["labels"] = str(labels)
        status, result = self._request("POST", path, payload)
        return 200 <= status < 300, result

    def get_issue(self, owner, repo, number):
        status, result = self._request("GET",
                                       f"/api/v5/repos/{owner}/{repo}/issues/{number}",
                                       )
        return 200 <= status < 300, result

    def add_issue_labels(self, owner, repo, number, labels):
        path = f"/api/v5/repos/{owner}/{repo}/issues/{number}/labels"
        label_list = labels if isinstance(labels, list) else [labels]
        status, result = self._request("POST", path, label_list)
        return 200 <= status < 300, result

    # ── PR-Issue 关联 ──

    def get_issues_by_pr(self, owner, repo, number):
        path = f"/api/v5/repos/{owner}/{repo}/pulls/{number}/issues"
        status, result = self._request("GET", path, )
        if 200 <= status < 300 and isinstance(result, list):
            return True, result
        return False, result

    def get_prs_by_issue(self, owner, repo, number):
        path = f"/api/v5/repos/{owner}/{repo}/issues/{number}/pull_requests"
        status, result = self._request("GET", path, )
        if 200 <= status < 300 and isinstance(result, list):
            return True, [pr for pr in result if pr.get("state") == "open"]
        return False, result

    # ── 仓库操作 ──

    def fork_repo(self, owner, repo, fork_name=None):
        path = f"/api/v5/repos/{owner}/{repo}/forks"
        payload = {}
        if fork_name:
            payload["name"] = fork_name
        status, result = self._request("POST", path, payload or None)
        return 200 <= status < 300, result

    def create_release(self, owner, repo, tag_name, name="", body="",
                       target_commitish="master"):
        path = f"/api/v5/repos/{owner}/{repo}/releases"
        payload = {"tag_name": tag_name, "name": name or tag_name,
                   "body": body, "target_commitish": target_commitish}
        status, result = self._request("POST", path, payload)
        return 200 <= status < 300, result

    def create_label(self, owner, repo, name, color="0075ff", description=""):
        path = f"/api/v5/repos/{owner}/{repo}/labels"
        payload = {"name": name, "color": color}
        if description:
            payload["description"] = description
        status, result = self._request("POST", path, payload)
        return 200 <= status < 300, result

    def check_repo_public(self, owner, repo):
        path = f"/api/v5/repos/{owner}/{repo}"
        status, result = self._request("GET", path, )
        if 200 <= status < 300:
            return True, {"public": not result.get("private", True),
                          "full_name": result.get("full_name")}
        return False, result

    def get_contents(self, owner, repo, filepath):
        """获取仓库中某个文件/目录的内容"""
        path = f"/api/v5/repos/{owner}/{repo}/contents/{filepath}"
        status, result = self._request("GET", path)
        return 200 <= status < 300, result

    def get_latest_commit(self, owner, repo, sha="master"):
        """获取最新 commit"""
        path = f"/api/v5/repos/{owner}/{repo}/commits?sha={sha}&per_page=1"
        status, result = self._request("GET", path)
        if 200 <= status < 300 and isinstance(result, list) and result:
            return True, result[0]
        return False, result

    def update_issue(self, owner, repo, number, title=None, body=None, state=None,
                      assignee=None, milestone=None, labels=None,
                      issue_severity=None, security_hole=None):
        """更新 Issue（PATCH /api/v5/repos/:owner/issues/:number）"""
        path = f"/api/v5/repos/{owner}/issues/{number}"
        payload = {"repo": repo}
        if title is not None:
            payload["title"] = title
        if body is not None:
            payload["body"] = body
        if state is not None:
            payload["state"] = state  # reopen / close
        if assignee is not None:
            payload["assignee"] = assignee
        if milestone is not None:
            payload["milestone"] = milestone
        if labels is not None:
            payload["labels"] = labels
        if issue_severity is not None:
            payload["issue_severity"] = issue_severity
        if security_hole is not None:
            payload["security_hole"] = security_hole
        status, result = self._request("PATCH", path, payload)
        return 200 <= status < 300, result

    def update_pr(self, owner, repo, number, title=None, body=None, state=None,
                  milestone_number=None, labels=None, draft=None,
                  close_related_issue=None):
        """更新 PR（PATCH /api/v5/repos/:owner/:repo/pulls/:number）"""
        path = f"/api/v5/repos/{owner}/{repo}/pulls/{number}"
        payload = {}
        if title is not None:
            payload["title"] = title
        if body is not None:
            payload["body"] = body
        if state is not None:
            payload["state"] = state
        if milestone_number is not None:
            payload["milestone_number"] = milestone_number
        if labels is not None:
            payload["labels"] = labels
        if draft is not None:
            payload["draft"] = draft
        if close_related_issue is not None:
            payload["close_related_issue"] = close_related_issue
        status, result = self._request("PATCH", path, payload)
        return 200 <= status < 300, result

    def post_issue_comment(self, owner, repo, number, body):
        """在 Issue 上发表评论"""
        api_path = f"/api/v5/repos/{owner}/{repo}/issues/{number}/comments"
        data = {"body": body}
        status, result = self._request("POST", api_path, data)
        return 200 <= status < 300, result

    def create_commit(self, owner, repo, branch, message, files,
                      committer_name=None, committer_email=None,
                      base_branch=None):
        """
        在仓库指定分支上创建提交。
        :param owner: 仓库所属空间地址
        :param repo: 仓库路径
        :param branch: 目标分支名
        :param message: 提交信息（必须符合 commitlint 格式，且为英文）
        :param files: 文件变更列表 [{"path": "file.txt", "content": "..."}]
        :param committer_name: 提交者姓名（可选，默认使用 GitCode 账户名）
        :param committer_email: 提交者邮箱（可选）
        :param base_branch: 基准分支（用于创建新分支时）
        """
        import base64
        # 获取参考 commit sha（用于指定 base）
        ref_path = f"/api/v5/repos/{owner}/{repo}/git/refs"
        ref_status, refs_data = self._request("GET", ref_path)
        ref_sha = None
        if ref_status == 200 and isinstance(refs_data, list):
            for ref in refs_data:
                if ref.get("ref") == f"refs/heads/{branch}":
                    ref_sha = ref.get("object", {}).get("sha")
                    break
        if not ref_sha and base_branch:
            ref_status2, ref2_data = self._request("GET", f"/api/v5/repos/{owner}/{repo}/git/refs")
            if ref_status2 == 200 and isinstance(ref2_data, list):
                for ref in ref2_data:
                    if ref.get("ref") == f"refs/heads/{base_branch}":
                        ref_sha = ref.get("object", {}).get("sha")
                        break

        # 创建 blob（每个文件）
        tree_items = []
        for f in files:
            blob_path = f"/api/v5/repos/{owner}/{repo}/git/blobs"
            blob_payload = {
                "content": f.get("content", ""),
                "encoding": "base64"
            }
            blob_status, blob_result = self._request("POST", blob_path, blob_payload)
            if blob_status == 200:
                blob_sha = blob_result.get("sha")
                tree_items.append({
                    "path": f["path"],
                    "type": "blob",
                    "sha": blob_sha,
                    "mode": "100644"
                })

        if not tree_items:
            return False, {"error": "No files to commit"}

        # 创建 tree
        tree_payload = {"tree": tree_items}
        if ref_sha:
            tree_payload["base_tree"] = ref_sha
        tree_status, tree_result = self._request("POST", f"/api/v5/repos/{owner}/{repo}/git/trees", tree_payload)
        if tree_status != 200:
            return False, tree_result
        tree_sha = tree_result.get("sha")

        # 创建 commit
        commit_payload = {
            "message": message,
            "tree": tree_sha,
        }
        if ref_sha:
            commit_payload["parents"] = [ref_sha]
        commit_status, commit_result = self._request("POST", f"/api/v5/repos/{owner}/{repo}/git/commits", commit_payload)
        if commit_status != 200:
            return False, commit_result
        commit_sha = commit_result.get("sha")

        # 更新 refs
        ref_update_status, ref_update_result = self._request(
            "PATCH",
            f"/api/v5/repos/{owner}/{repo}/git/refs/heads/{branch}",
            {"sha": commit_sha, "force": False}
        )
        if ref_update_status not in (200, 201):
            return False, ref_update_result
        return True, {
            "sha": commit_sha,
            "message": message,
            "url": f"https://gitcode.com/{owner}/{repo}/commit/{commit_sha}"
        }


# ── 模板操作 ──

class TemplateLoader:
    """仓库模板加载器"""

    LANG_HINTS = {"zh": ("zh", "cn", "chinese"), "en": ("en", "english")}

    def __init__(self, repo_path, language="zh"):
        self.repo_path = Path(repo_path)
        self.gitcode_path = self.repo_path / ".gitcode"
        self.language = language if language in self.LANG_HINTS else "zh"

    def _pick_by_lang(self, files):
        if not files:
            return None
        hints = self.LANG_HINTS.get(self.language, ())
        for hint in hints:
            for f in files:
                if hint in f.name.lower():
                    return f
        return files[0]

    def get_issue_template(self):
        tdir = self.gitcode_path / "ISSUE_TEMPLATE"
        if not tdir.exists():
            return None
        md = self._pick_by_lang(list(tdir.glob("*.md")))
        if md:
            return md.read_text(encoding='utf-8')
        yml_files = [f for f in tdir.glob("*.yml") if f.name != "config.yml"]
        yml = self._pick_by_lang(yml_files)
        if yml:
            return self._parse_yml_body_to_md(yml)
        return None

    def get_pr_template(self):
        tdir = self.gitcode_path / "PULL_REQUEST_TEMPLATE"
        if not tdir.exists():
            return None
        md_files = list(tdir.glob("*.md"))
        if len(md_files) == 1:
            return md_files[0].read_text(encoding='utf-8')
        picked = self._pick_by_lang(md_files)
        if picked:
            return picked.read_text(encoding='utf-8')
        return None

    def list_issue_templates(self):
        tdir = self.gitcode_path / "ISSUE_TEMPLATE"
        if not tdir.exists():
            return []
        import yaml
        templates = []
        for f in list(tdir.glob("*.md")) + [x for x in tdir.glob("*.yml") if x.name != "config.yml"]:
            info = {"file": f.name, "path": str(f.relative_to(self.repo_path))}
            if f.suffix == '.yml':
                try:
                    data = yaml.safe_load(f.read_text(encoding='utf-8'))
                    if isinstance(data, dict):
                        info.update({k: data.get(k, '') for k in ('name', 'description', 'title')})
                except Exception:
                    pass
            templates.append(info)
        return templates

    def parse_issue_template(self, template_path):
        import yaml
        full = self.repo_path / template_path
        if not full.exists():
            return {"labels": None, "body": None}
        if full.suffix == '.md':
            return {"labels": None, "body": full.read_text(encoding='utf-8')}
        try:
            data = yaml.safe_load(full.read_text(encoding='utf-8'))
            if not isinstance(data, dict):
                return {"labels": None, "body": None}
            labels = data.get('labels', [])
            body_md = self._parse_yml_body_to_md(full)
            return {"labels": labels if labels else None, "body": body_md}
        except Exception:
            return {"labels": None, "body": None}

    def _parse_yml_body_to_md(self, yml_path):
        import yaml
        try:
            data = yaml.safe_load(yml_path.read_text(encoding='utf-8'))
            if not isinstance(data, dict):
                return yml_path.read_text(encoding='utf-8')
            body = data.get('body', [])
            if not isinstance(body, list):
                return yml_path.read_text(encoding='utf-8')
            lines = []
            for item in body:
                if not isinstance(item, dict):
                    continue
                t = item.get('type', '')
                attrs = item.get('attributes', {})
                if t == 'markdown':
                    v = attrs.get('value', '')
                    if v:
                        lines.append(v.strip())
                elif t in ('textarea', 'input', 'dropdown'):
                    if attrs.get('label'):
                        lines.append(f"### {attrs['label']}")
                    if attrs.get('description'):
                        lines.append(attrs['description'])
                    if attrs.get('placeholder'):
                        lines.append(f"<!-- {attrs['placeholder']} -->")
                    lines.append("")
                elif t == 'checkboxes':
                    if attrs.get('label'):
                        lines.append(f"### {attrs['label']}")
                    for opt in attrs.get('options', []):
                        label = opt.get('label', '') if isinstance(opt, dict) else str(opt)
                        if label:
                            lines.append(f"- [ ] {label}")
                    lines.append("")
            return "\n".join(lines).strip() if lines else yml_path.read_text(encoding='utf-8')
        except Exception:
            return yml_path.read_text(encoding='utf-8')


def get_commit_title(repo_path, branch="HEAD"):
    try:
        r = subprocess.run(["git", "log", "-1", "--pretty=format:%s", branch],
                           cwd=repo_path, capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    return None


class RemoteTemplateLoader:
    """通过 GitCode API 远程加载仓库模板"""

    LANG_HINTS = {"zh": ("zh", "cn", "chinese"), "en": ("en", "english")}

    def __init__(self, client: GitCodeClient, owner: str, repo: str, language: str = "zh"):
        self.client = client
        self.owner = owner
        self.repo = repo
        self.language = language if language in self.LANG_HINTS else "zh"

    def _pick_by_lang(self, names):
        if not names:
            return None
        hints = self.LANG_HINTS.get(self.language, ())
        for hint in hints:
            for n in names:
                if hint in n.lower():
                    return n
        return names[0]

    def _fetch_file(self, filepath):
        """Fetch a single file's content from the repo via API."""
        import base64
        ok, result = self.client.get_contents(self.owner, self.repo, filepath)
        if not ok:
            return None
        if isinstance(result, dict) and result.get("content"):
            encoding = result.get("encoding", "base64")
            if encoding == "base64":
                return base64.b64decode(result["content"]).decode("utf-8", errors="ignore")
            return result["content"]
        return None

    def _list_dir(self, dirpath):
        """List files in a directory via API. Returns list of {name, path, type}."""
        ok, result = self.client.get_contents(self.owner, self.repo, dirpath)
        if ok and isinstance(result, list):
            return result
        return []

    def get_issue_template(self):
        entries = self._list_dir(".gitcode/ISSUE_TEMPLATE")
        if not entries:
            return None
        md_names = [e["path"] for e in entries if e.get("name", "").endswith(".md")]
        picked = self._pick_by_lang(md_names)
        if picked:
            return self._fetch_file(picked)
        yml_names = [e["path"] for e in entries
                     if e.get("name", "").endswith(".yml") and e.get("name") != "config.yml"]
        picked = self._pick_by_lang(yml_names)
        if picked:
            content = self._fetch_file(picked)
            return content  # Return raw yml content for remote
        return None

    def get_pr_template(self):
        entries = self._list_dir(".gitcode/PULL_REQUEST_TEMPLATE")
        if not entries:
            return None
        md_names = [e["path"] for e in entries if e.get("name", "").endswith(".md")]
        if len(md_names) == 1:
            return self._fetch_file(md_names[0])
        picked = self._pick_by_lang(md_names)
        if picked:
            return self._fetch_file(picked)
        return None

    def list_issue_templates(self):
        entries = self._list_dir(".gitcode/ISSUE_TEMPLATE")
        if not entries:
            return []
        templates = []
        for e in entries:
            name = e.get("name", "")
            if name.endswith(".md") or (name.endswith(".yml") and name != "config.yml"):
                templates.append({"file": name, "path": e.get("path", "")})
        return templates

    def parse_issue_template(self, template_path):
        content = self._fetch_file(template_path)
        if not content:
            return {"labels": None, "body": None}
        if template_path.endswith(".md"):
            return {"labels": None, "body": content}
        try:
            import yaml
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                return {"labels": None, "body": content}
            labels = data.get("labels", [])
            return {"labels": labels if labels else None, "body": content}
        except Exception:
            return {"labels": None, "body": content}


def output(ok, data):
    """统一输出"""
    result = {"success": ok}
    if isinstance(data, (dict, list)):
        result["data"] = data
    else:
        result["data"] = str(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if ok else 1)


def main():
    parser = argparse.ArgumentParser(description="Power GitCode - GitCode 平台全能操作工具")
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # ── PR commands ──
    p = sub.add_parser("create_pr", help="创建 PR")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--head", required=True, help="源分支 (格式: user:branch)")
    p.add_argument("--base", required=True, help="目标分支")
    p.add_argument("--body", default="")
    p.add_argument("--fork-path", default=None)
    p.add_argument("--labels", nargs="*", default=None)

    p = sub.add_parser("get_pr", help="获取 PR 详情")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)

    p = sub.add_parser("get_pr_commits", help="获取 PR commits")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)

    p = sub.add_parser("get_pr_changed_files", help="获取 PR 修改文件")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--ignore-deleted", action="store_true")

    p = sub.add_parser("get_pr_comments", help="获取 PR 评论")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)

    p = sub.add_parser("post_pr_comment", help="在 PR 上评论")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--body", required=True)
    p.add_argument("--path", help="文件的相对路径（代码行评论时必填）")
    p.add_argument("--position", type=int, help="代码所在行数（代码行评论时必填）")

    p = sub.add_parser("add_pr_labels", help="给 PR 添加标签")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--labels", nargs="+", required=True)

    p = sub.add_parser("remove_pr_labels", help="移除 PR 标签")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--label", required=True)

    p = sub.add_parser("assign_pr_testers", help="分配 PR 测试人员")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--testers", nargs="+", required=True)

    p = sub.add_parser("check_pr_mergeable", help="检查 PR 可合并性")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)

    p = sub.add_parser("merge_pr", help="合并 PR")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--method", default="merge", choices=["merge", "squash", "rebase"])

    # ── Issue commands ──
    p = sub.add_parser("create_issue", help="创建 Issue")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--body", default="")
    p.add_argument("--labels", nargs="*", default=None)

    p = sub.add_parser("get_issue", help="获取 Issue 详情")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)

    p = sub.add_parser("add_issue_labels", help="给 Issue 添加标签")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--labels", nargs="+", required=True)

    p = sub.add_parser("post_issue_comment", help="在 Issue 上评论")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--body", required=True)

    p = sub.add_parser("update_issue", help="更新 Issue（PATCH）")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--title", default=None)
    p.add_argument("--body", default=None)
    p.add_argument("--state", default=None, choices=["reopen", "close"])
    p.add_argument("--assignee", default=None)
    p.add_argument("--milestone", type=int, default=None)
    p.add_argument("--labels", default=None, help="逗号分隔的标签")
    p.add_argument("--issue-severity", default=None)

    p = sub.add_parser("update_pr", help="更新 PR（PATCH）")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)
    p.add_argument("--title", default=None)
    p.add_argument("--body", default=None)
    p.add_argument("--state", default=None, choices=["open", "closed"])
    p.add_argument("--milestone-number", type=int, default=None)
    p.add_argument("--labels", default=None, help="逗号分隔的标签")
    p.add_argument("--draft", type=lambda x: x.lower() == "true", default=None)
    p.add_argument("--close-related-issue", type=lambda x: x.lower() == "true", default=None)

    p = sub.add_parser("create_commit", help="创建提交（需符合 commitlint 格式）")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--branch", required=True, help="目标分支")
    p.add_argument("--message", required=True, help="提交信息（英文，必须符合 commitlint: type(scope): subject）")
    p.add_argument("--file", nargs="+", required=True, metavar="PATH=CONTENT", help="文件路径=base64内容，示例：src/main.cj=SGVsbG8gV29ybGQ=")
    p.add_argument("--base-branch", default=None, help="基准分支（目标分支不存在时以此创建）")

    # ── PR-Issue 关联 ──
    p = sub.add_parser("get_issues_by_pr", help="获取 PR 关联的 Issue")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)

    p = sub.add_parser("get_prs_by_issue", help="获取 Issue 关联的 PR")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--number", required=True, type=int)

    # ── 模板 commands ──
    p = sub.add_parser("get_issue_template", help="获取 Issue 模板")
    p.add_argument("--repo-path", default=None)
    p.add_argument("--owner", default=None)
    p.add_argument("--repo", default=None)
    p.add_argument("--language", default="zh")

    p = sub.add_parser("get_pr_template", help="获取 PR 模板")
    p.add_argument("--repo-path", default=None)
    p.add_argument("--owner", default=None)
    p.add_argument("--repo", default=None)
    p.add_argument("--language", default="zh")

    p = sub.add_parser("list_issue_templates", help="列出所有 Issue 模板")
    p.add_argument("--repo-path", default=None)
    p.add_argument("--owner", default=None)
    p.add_argument("--repo", default=None)
    p.add_argument("--language", default="zh")

    p = sub.add_parser("parse_issue_template", help="解析 Issue 模板")
    p.add_argument("--repo-path", default=None)
    p.add_argument("--owner", default=None)
    p.add_argument("--repo", default=None)
    p.add_argument("--template-path", required=True, help="模板相对路径")
    p.add_argument("--language", default="zh")

    p = sub.add_parser("get_commit_title", help="获取最新 commit 标题")
    p.add_argument("--repo-path", default=None)
    p.add_argument("--owner", default=None)
    p.add_argument("--repo", default=None)
    p.add_argument("--branch", default="HEAD")

    # ── 仓库 commands ──
    p = sub.add_parser("fork_repo", help="Fork 仓库")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--fork-name", default=None)

    p = sub.add_parser("create_release", help="创建 Release")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--tag", required=True)
    p.add_argument("--name", default="")
    p.add_argument("--body", default="")
    p.add_argument("--target", default="master")

    p = sub.add_parser("create_label", help="创建标签")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--color", default="0075ff")
    p.add_argument("--description", default="")

    p = sub.add_parser("check_repo_public", help="检查仓库是否公开")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = GitCodeClient()
    cmd = args.command

    # ── 执行 ──
    if cmd == "create_pr":
        ok, r = client.create_pr(args.owner, args.repo, args.title, args.head,
                                 args.base, args.body, args.fork_path, args.labels)
        output(ok, r)
    elif cmd == "get_pr":
        ok, r = client.get_pr(args.owner, args.repo, args.number)
        output(ok, r)
    elif cmd == "get_pr_commits":
        ok, r = client.get_pr_commits(args.owner, args.repo, args.number)
        output(ok, r)
    elif cmd == "get_pr_changed_files":
        ok, r = client.get_pr_changed_files(args.owner, args.repo, args.number,
                                            args.ignore_deleted)
        output(ok, r)
    elif cmd == "get_pr_comments":
        ok, r = client.get_pr_comments(args.owner, args.repo, args.number)
        output(ok, r)
    elif cmd == "post_pr_comment":
        ok, r = client.post_pr_comment(args.owner, args.repo, args.number, args.body,
                                       args.path, args.position)
        output(ok, r)
    elif cmd == "add_pr_labels":
        ok, r = client.add_pr_labels(args.owner, args.repo, args.number, args.labels)
        output(ok, r)
    elif cmd == "remove_pr_labels":
        ok, r = client.remove_pr_labels(args.owner, args.repo, args.number, args.label)
        output(ok, r)
    elif cmd == "assign_pr_testers":
        ok, r = client.assign_pr_testers(args.owner, args.repo, args.number, args.testers)
        output(ok, r)
    elif cmd == "check_pr_mergeable":
        ok, r = client.check_pr_mergeable(args.owner, args.repo, args.number)
        output(ok, r)
    elif cmd == "merge_pr":
        ok, r = client.merge_pr(args.owner, args.repo, args.number, args.method)
        output(ok, r)
    elif cmd == "create_issue":
        ok, r = client.create_issue(args.owner, args.repo, args.title, args.body, args.labels)
        output(ok, r)
    elif cmd == "get_issue":
        ok, r = client.get_issue(args.owner, args.repo, args.number)
        output(ok, r)
    elif cmd == "add_issue_labels":
        ok, r = client.add_issue_labels(args.owner, args.repo, args.number, args.labels)
        output(ok, r)
    elif cmd == "post_issue_comment":
        ok, r = client.post_issue_comment(args.owner, args.repo, args.number, args.body)
        output(ok, r)
    elif cmd == "update_issue":
        labels = args.labels.split(",") if args.labels else None
        ok, r = client.update_issue(args.owner, args.repo, args.number,
                                    title=args.title, body=args.body, state=args.state,
                                    assignee=args.assignee, milestone=args.milestone,
                                    labels=labels, issue_severity=args.issue_severity)
        output(ok, r)
    elif cmd == "update_pr":
        labels = args.labels.split(",") if args.labels else None
        ok, r = client.update_pr(args.owner, args.repo, args.number,
                                  title=args.title, body=args.body, state=args.state,
                                  milestone_number=args.milestone_number, labels=labels,
                                  draft=args.draft, close_related_issue=args.close_related_issue)
        output(ok, r)
    elif cmd == "create_commit":
        import base64
        files = []
        for farg in args.file:
            if "=" in farg:
                path_, content_b64 = farg.split("=", 1)
                try:
                    content = base64.b64decode(content_b64).decode("utf-8")
                except Exception:
                    content = content_b64  # treat as raw if decode fails
                files.append({"path": path_, "content": content})
            else:
                return output(False, f"Invalid --file format: {farg}. Use PATH=CONTENT (content base64).")
        ok, r = client.create_commit(args.owner, args.repo, args.branch,
                                     args.message, files, base_branch=args.base_branch)
        output(ok, r)
    elif cmd == "get_issues_by_pr":
        ok, r = client.get_issues_by_pr(args.owner, args.repo, args.number)
        output(ok, r)
    elif cmd == "get_prs_by_issue":
        ok, r = client.get_prs_by_issue(args.owner, args.repo, args.number)
        output(ok, r)
    elif cmd == "get_issue_template":
        if args.repo_path:
            loader = TemplateLoader(args.repo_path, args.language)
        elif args.owner and args.repo:
            loader = RemoteTemplateLoader(client, args.owner, args.repo, args.language)
        else:
            output(False, "需要 --repo-path 或 --owner + --repo")
            return
        t = loader.get_issue_template()
        output(t is not None, {"template": t})
    elif cmd == "get_pr_template":
        if args.repo_path:
            loader = TemplateLoader(args.repo_path, args.language)
        elif args.owner and args.repo:
            loader = RemoteTemplateLoader(client, args.owner, args.repo, args.language)
        else:
            output(False, "需要 --repo-path 或 --owner + --repo")
            return
        t = loader.get_pr_template()
        output(t is not None, {"template": t})
    elif cmd == "list_issue_templates":
        if args.repo_path:
            loader = TemplateLoader(args.repo_path, args.language)
        elif args.owner and args.repo:
            loader = RemoteTemplateLoader(client, args.owner, args.repo, args.language)
        else:
            output(False, "需要 --repo-path 或 --owner + --repo")
            return
        templates = loader.list_issue_templates()
        output(True, {"templates": templates})
    elif cmd == "parse_issue_template":
        if args.repo_path:
            loader = TemplateLoader(args.repo_path, args.language)
        elif args.owner and args.repo:
            loader = RemoteTemplateLoader(client, args.owner, args.repo, args.language)
        else:
            output(False, "需要 --repo-path 或 --owner + --repo")
            return
        r = loader.parse_issue_template(args.template_path)
        output(True, r)
    elif cmd == "get_commit_title":
        if args.repo_path:
            title = get_commit_title(args.repo_path, args.branch)
        elif args.owner and args.repo:
            branch = args.branch if args.branch != "HEAD" else None
            if not branch:
                # Fetch repo default branch
                ok_repo, repo_info = client.check_repo_public(args.owner, args.repo)
                # check_repo_public returns limited info; fetch default_branch directly
                _, repo_data = client._request("GET", f"/api/v5/repos/{args.owner}/{args.repo}")
                branch = repo_data.get("default_branch", "main") if isinstance(repo_data, dict) else "main"
            ok, commit = client.get_latest_commit(args.owner, args.repo, branch)
            title = commit.get("commit", {}).get("message", "").split("\n")[0] if ok and isinstance(commit, dict) else None
        else:
            output(False, "需要 --repo-path 或 --owner + --repo")
            return
        output(title is not None, {"title": title})
    elif cmd == "fork_repo":
        ok, r = client.fork_repo(args.owner, args.repo, args.fork_name)
        output(ok, r)
    elif cmd == "create_release":
        ok, r = client.create_release(args.owner, args.repo, args.tag, args.name,
                                      args.body, args.target)
        output(ok, r)
    elif cmd == "create_label":
        ok, r = client.create_label(args.owner, args.repo, args.name, args.color,
                                    args.description)
        output(ok, r)
    elif cmd == "check_repo_public":
        ok, r = client.check_repo_public(args.owner, args.repo)
        output(ok, r)


if __name__ == "__main__":
    main()
