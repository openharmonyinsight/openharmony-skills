#!/usr/bin/env python3
"""Plan and verify migration to repository-scoped ODK archive paths."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


LEGACY_PATH_RE = re.compile(
    r"^\.codespec/changes/issue-[0-9]+-([a-z0-9]+(?:-[a-z0-9]+)*)$"
)
REQ_ID_RE = re.compile(r"^[A-Za-z0-9]+(?:[A-Za-z0-9-]*[A-Za-z0-9])?$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REPOSITORY_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")


class MigrationError(RuntimeError):
    """A migration precondition or invariant failed."""


def fail(message: str) -> None:
    raise MigrationError(message)


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def read_mapping(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        fail(f"cannot read mapping file {path}: {exc}")
    for line_number, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        columns = line.split("\t")
        if len(columns) != 2 or not all(column.strip() for column in columns):
            fail(f"mapping line {line_number}: expected exactly two non-empty TSV columns")
        rows.append((columns[0].strip(), columns[1].strip()))
    if not rows:
        fail("mapping file contains no archive mappings")
    return rows


def discover_legacy_archives(root: Path) -> set[str]:
    discovered: set[str] = set()
    issue_changes = root / ".codespec" / "changes"
    if issue_changes.is_dir():
        for entry in issue_changes.iterdir():
            if not entry.is_dir() or not entry.name.startswith("issue-"):
                continue
            relative = entry.relative_to(root).as_posix()
            if not LEGACY_PATH_RE.fullmatch(relative):
                fail(f"invalid legacy archive directory: {relative}")
            discovered.add(relative)

    flat_changes = root / "codespec" / "changes"
    if flat_changes.is_dir():
        for entry in flat_changes.iterdir():
            if entry.is_dir() and (entry / "proposal.md").is_file():
                discovered.add(entry.relative_to(root).as_posix())
    if not discovered:
        fail("no legacy flat or issue-* archives discovered")
    return discovered


def repository_name(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "remote", "get-url", "origin"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        remote = result.stdout.strip().rstrip("/")
        name = remote.rsplit("/", 1)[-1].rsplit(":", 1)[-1]
        if name.endswith(".git"):
            name = name[:-4]
        if name and name not in {".", ".."} and REPOSITORY_NAME_RE.fullmatch(name):
            return name
    name = root.name
    if name in {".", ".."} or not REPOSITORY_NAME_RE.fullmatch(name):
        fail(f"invalid repository name: {name}")
    return name


def plan_migration(root: Path, map_path: Path) -> None:
    root = root.resolve()
    map_path = map_path.resolve()
    if is_within(map_path, root):
        fail("mapping file must be outside the worktree")

    discovered = discover_legacy_archives(root)
    rows = read_mapping(map_path)
    seen_sources: set[str] = set()
    seen_targets: set[str] = set()
    plans: list[tuple[str, str]] = []
    repo_name = repository_name(root)

    for old_path, req_id in rows:
        issue_match = LEGACY_PATH_RE.fullmatch(old_path)
        flat_prefix = f"codespec/changes/{req_id}-"
        if not issue_match and not old_path.startswith(flat_prefix):
            fail(f"invalid legacy path or req identity: {old_path}")
        if old_path in seen_sources:
            fail(f"duplicate source mapping: {old_path}")
        if old_path not in discovered:
            fail(f"mapped source was not discovered: {old_path}")
        if not (root / PurePosixPath(old_path)).is_dir():
            fail(f"missing source: {old_path}")
        if not REQ_ID_RE.fullmatch(req_id):
            fail(f"invalid req-id: {req_id}")

        if issue_match:
            slug = issue_match.group(1)
        else:
            slug = old_path[len(flat_prefix):]
        if not SLUG_RE.fullmatch(slug):
            fail(f"invalid slug: {slug}")
        new_path = f"codespec/changes/{repo_name}/{req_id}"
        if new_path in seen_targets:
            fail(f"duplicate planned target: {new_path}")
        if (root / PurePosixPath(new_path)).exists():
            fail(f"target exists: {new_path}")

        seen_sources.add(old_path)
        seen_targets.add(new_path)
        plans.append((old_path, new_path))

    missing = sorted(discovered - seen_sources)
    if missing:
        fail("discovered archives missing from mapping: " + ", ".join(missing))
    extras = sorted(seen_sources - discovered)
    if extras:
        fail("mapping contains undiscovered archives: " + ", ".join(extras))

    for old_path, new_path in plans:
        print(f"PLAN\t{old_path}\t{new_path}")
    print(f"PASS migration plan: {len(plans)} archive(s), all sources and targets unique")


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        fail(f"git {' '.join(args)} failed: {detail}")
    return result


def proposal_frontmatter(text: str, path: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"{path}: proposal frontmatter missing")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index])
    fail(f"{path}: proposal frontmatter is not closed")
    return ""  # Unreachable; keeps static analyzers satisfied.


def check_staged(root: Path) -> None:
    root = root.resolve()
    if git(root, "rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        fail(f"not a git worktree: {root}")
    if git(root, "diff", "--quiet", "--", check=False).returncode != 0:
        fail("unstaged tracked migration edits remain")
    untracked = git(root, "ls-files", "--others", "--exclude-standard").stdout.splitlines()
    if untracked:
        fail("untracked files remain in worktree: " + ", ".join(untracked))
    if git(root, "diff", "--cached", "--quiet", "--", check=False).returncode == 0:
        fail("no staged migration changes found")

    whitespace = git(root, "diff", "--cached", "--check", check=False)
    if whitespace.returncode != 0:
        fail("staged diff check failed: " + (whitespace.stdout or whitespace.stderr).strip())

    staged_paths = git(
        root, "diff", "--cached", "--name-only", "--diff-filter=ACMR"
    ).stdout.splitlines()
    proposals = [
        path for path in staged_paths
        if path.startswith("codespec/changes/") and path.endswith("/proposal.md")
    ]
    if not proposals:
        fail("no staged migrated proposal under codespec/changes")

    repo_name = repository_name(root)
    for path in proposals:
        staged_text = git(root, "show", f":{path}").stdout
        frontmatter = proposal_frontmatter(staged_text, path)
        if re.search(r"(?m)^\s*issue\s*:", frontmatter):
            fail(f"{path}: staged proposal still contains legacy issue frontmatter")
        req_matches = re.findall(r"(?m)^\s*req\s*:\s*[\"']?([^\s\"']+)", frontmatter)
        if len(req_matches) != 1:
            fail(f"{path}: staged proposal must contain exactly one non-empty req field")
        req_id = req_matches[0]
        if not REQ_ID_RE.fullmatch(req_id):
            fail(f"{path}: invalid staged req-id: {req_id}")
        parts = PurePosixPath(path).parts
        if len(parts) != 5 or parts[:2] != ("codespec", "changes"):
            fail(f"{path}: staged archive path must be codespec/changes/<repo-name>/<req-id>/proposal.md")
        if parts[2] != repo_name or parts[3] != req_id:
            fail(f"{path}: staged req field does not match directory identity")

    print(
        f"PASS staged migration: {len(proposals)} proposal(s), no unstaged/untracked edits, "
        "frontmatter matches directory identity"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    plan = subparsers.add_parser("plan", help="validate a legacy archive mapping and print moves")
    plan.add_argument("--map", required=True, type=Path, dest="map_path")
    plan.add_argument("--repo", type=Path, default=Path.cwd())
    staged = subparsers.add_parser("check-staged", help="verify staged migration content")
    staged.add_argument("--repo", type=Path, default=Path.cwd())
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "plan":
            plan_migration(args.repo, args.map_path)
        else:
            check_staged(args.repo)
    except MigrationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
