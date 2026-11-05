"""Read-only publication check for explicitly reviewed business source files.

The caller supplies the source head freshly queried from the actual PR host.
This command does not query a host, publish code or authorize a push.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat
import subprocess


def check_source(repo: Path, published_head: str, scope: list[str]) -> dict:
    repo = repo.resolve()
    result = {"ready": False, "published_head": published_head, "scope": scope, "errors": []}
    errors = result["errors"]

    def git(*args: str, data: bytes | None = None) -> bytes:
        completed = subprocess.run(["git", "--literal-pathspecs", "-C", str(repo), *args],
                                   input=data, capture_output=True)
        if completed.returncode:
            raise ValueError(completed.stderr.decode("utf-8", "replace").strip())
        return completed.stdout

    try:
        if not re.fullmatch(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})", published_head):
            raise ValueError("published-head must be the full source commit SHA queried from the PR host")
        if not scope:
            raise ValueError("scope must list the reviewed business source files")
        for value in scope:
            path = Path(value)
            if not value or path.is_absolute() or ".." in path.parts or value == ".":
                raise ValueError("scope must use repository-relative file paths: " + value)
            if (repo / path).is_dir() and not (repo / path).is_symlink():
                raise ValueError("scope must list individual reviewed files, not directories: " + value)
        root = Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve()
        if root != repo:
            raise ValueError("repo must be the business Git worktree root")
        if git("cat-file", "-t", published_head).strip() != b"commit":
            raise ValueError("published-head is not a commit")
        head = git("rev-parse", "HEAD").decode().strip()
        result["local_head"] = head
        if head.lower() != published_head.lower():
            errors.append("business HEAD differs from the actual PR source head; publish/confirm the repair first")
        staged = git("diff", "--cached", "--name-only", "-z", "--no-ext-diff", "--no-textconv", published_head, "--", *scope)
        if staged:
            errors.append("unpublished index changes: " + "; ".join(
                entry.decode("utf-8", "replace") for entry in staged.split(b"\0") if entry))
        # Compare actual files as Git blobs, including untracked/ignored files:
        # index flags can suppress status, and line endings can dirty stat data
        # without changing published content. --path applies Git's clean filters.
        filemode = git("config", "--default", "true", "--bool", "--get", "core.filemode").strip() != b"false"
        for value in scope:
            path = repo / value
            entry = git("ls-tree", "-z", published_head, "--", value)
            present = path.exists() or path.is_symlink()
            if not entry:
                if present:
                    errors.append("source file is absent from the published commit: " + value)
                continue  # A deletion already present in the published commit.
            mode, kind, oid = entry.split(b"\t", 1)[0].split()
            if not present:
                errors.append("published source file is missing locally: " + value)
                continue
            if kind != b"blob" or (not path.is_file() and not path.is_symlink()):
                errors.append("scope is not a supported source file: " + value)
                continue
            if path.is_symlink():
                actual_mode = b"120000"
                actual_oid = git("hash-object", "--stdin", data=os.fsencode(os.readlink(path))).strip()
            else:
                actual_mode = b"100755" if path.stat().st_mode & stat.S_IXUSR else b"100644"
                if not filemode and mode in {b"100644", b"100755"}:
                    actual_mode = mode
                actual_oid = git("hash-object", "--path=" + value, "--stdin", data=path.read_bytes()).strip()
            if actual_mode != mode or actual_oid != oid:
                errors.append("working source differs from the published tree: " + value)
    except (ValueError, OSError) as error:
        errors.append(str(error))
    result["ready"] = not errors
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--published-head", required=True)
    parser.add_argument("--scope", action="append", default=[], help="Reviewed repository-relative file; repeat for all affected source files")
    args = parser.parse_args()
    result = check_source(args.repo, args.published_head, args.scope)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
