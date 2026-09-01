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
DRAFT_RE = re.compile(r"^draft-[0-9]{8}-[a-z0-9]+(?:-[a-z0-9]+)*$")
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


def build_plans(
    root: Path,
    rows: list[tuple[str, str]],
    discovered: set[str],
    *,
    require_sources_in_worktree: bool,
    require_targets_absent: bool,
) -> list[tuple[str, str]]:
    seen_sources: set[str] = set()
    seen_targets: set[str] = set()
    plans: list[tuple[str, str]] = []
    repo_name = repository_name(root)

    for old_path, identity in rows:
        issue_match = LEGACY_PATH_RE.fullmatch(old_path)
        flat_draft = old_path.removeprefix("codespec/changes/")
        is_flat_draft = (
            old_path == f"codespec/changes/{flat_draft}"
            and DRAFT_RE.fullmatch(flat_draft) is not None
        )

        if is_flat_draft:
            if identity != "-":
                fail(f"draft mapping must use '-' instead of a req-id: {old_path}")
            new_leaf = flat_draft
        else:
            if not REQ_ID_RE.fullmatch(identity):
                fail(f"invalid req-id: {identity}")
            flat_prefix = f"codespec/changes/{identity}-"
            if not issue_match and not old_path.startswith(flat_prefix):
                fail(f"invalid legacy path or req identity: {old_path}")
            slug = issue_match.group(1) if issue_match else old_path[len(flat_prefix):]
            if not SLUG_RE.fullmatch(slug):
                fail(f"invalid slug: {slug}")
            new_leaf = identity

        if old_path in seen_sources:
            fail(f"duplicate source mapping: {old_path}")
        if old_path not in discovered:
            fail(f"mapped source was not discovered: {old_path}")
        if require_sources_in_worktree and not (root / PurePosixPath(old_path)).is_dir():
            fail(f"missing source: {old_path}")

        new_path = f"codespec/changes/{repo_name}/{new_leaf}"
        if new_path in seen_targets:
            fail(f"duplicate planned target: {new_path}")
        if require_targets_absent and (root / PurePosixPath(new_path)).exists():
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
    return plans


def plan_migration(root: Path, map_path: Path) -> None:
    root = root.resolve()
    map_path = map_path.resolve()
    if is_within(map_path, root):
        fail("mapping file must be outside the worktree")

    discovered = discover_legacy_archives(root)
    rows = read_mapping(map_path)
    plans = build_plans(
        root,
        rows,
        discovered,
        require_sources_in_worktree=True,
        require_targets_absent=True,
    )

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


def discover_legacy_archives_in_head(root: Path) -> set[str]:
    paths = git(root, "ls-tree", "-r", "--name-only", "HEAD").stdout.splitlines()
    discovered: set[str] = set()
    for path in paths:
        if not path.endswith("/proposal.md"):
            continue
        parent = PurePosixPath(path).parent.as_posix()
        if parent.startswith(".codespec/changes/issue-"):
            if not LEGACY_PATH_RE.fullmatch(parent):
                fail(f"invalid legacy archive directory in HEAD: {parent}")
            discovered.add(parent)
            continue
        parts = PurePosixPath(parent).parts
        if len(parts) == 3 and parts[:2] == ("codespec", "changes"):
            discovered.add(parent)
    if not discovered:
        fail("no legacy flat or issue-* archives discovered in HEAD")
    return discovered


def frontmatter_req_values(frontmatter: str) -> list[str]:
    values: list[str] = []
    for match in re.finditer(r"(?m)^\s*req\s*:\s*(.*)$", frontmatter):
        value = re.sub(r"\s+#.*$", "", match.group(1)).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1].strip()
        values.append(value)
    return values


def check_staged(root: Path, map_path: Path) -> None:
    root = root.resolve()
    map_path = map_path.resolve()
    if is_within(map_path, root):
        fail("mapping file must be outside the worktree")
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

    discovered = discover_legacy_archives_in_head(root)
    plans = build_plans(
        root,
        read_mapping(map_path),
        discovered,
        require_sources_in_worktree=False,
        require_targets_absent=False,
    )
    expected_targets = {f"{target}/proposal.md" for _, target in plans}
    for source, target in plans:
        target_proposal = f"{target}/proposal.md"
        source_files = git(
            root, "ls-tree", "-r", "--name-only", "HEAD", "--", source
        ).stdout.splitlines()
        if not source_files:
            fail(f"legacy source has no tracked files in HEAD: {source}")
        for source_file in source_files:
            if git(root, "cat-file", "-e", f":{source_file}", check=False).returncode == 0:
                fail(f"legacy source remains in staged index: {source_file}")
            relative = PurePosixPath(source_file).relative_to(PurePosixPath(source))
            target_file = (PurePosixPath(target) / relative).as_posix()
            if git(root, "cat-file", "-e", f":{target_file}", check=False).returncode != 0:
                fail(f"planned target is missing migrated file: {target_file}")
        if git(root, "cat-file", "-e", f":{target_proposal}", check=False).returncode != 0:
            fail(f"planned target missing from staged index: {target}")

    staged_paths = git(
        root, "diff", "--cached", "--name-only", "--diff-filter=ACMR"
    ).stdout.splitlines()
    proposals = [
        path for path in staged_paths
        if path.startswith("codespec/changes/") and path.endswith("/proposal.md")
    ]
    if not proposals:
        fail("no staged migrated proposal under codespec/changes")
    unexpected = sorted(set(proposals) - expected_targets)
    missing = sorted(expected_targets - set(proposals))
    if unexpected or missing:
        details = []
        if unexpected:
            details.append("unexpected targets: " + ", ".join(unexpected))
        if missing:
            details.append("missing targets: " + ", ".join(missing))
        fail("staged proposals do not match migration mapping: " + "; ".join(details))

    repo_name = repository_name(root)
    for path in proposals:
        staged_text = git(root, "show", f":{path}").stdout
        frontmatter = proposal_frontmatter(staged_text, path)
        if re.search(r"(?m)^\s*issue\s*:", frontmatter):
            fail(f"{path}: staged proposal still contains legacy issue frontmatter")
        req_values = frontmatter_req_values(frontmatter)
        if len(req_values) > 1:
            fail(f"{path}: staged proposal contains duplicate req fields")
        parts = PurePosixPath(path).parts
        if len(parts) != 5 or parts[:2] != ("codespec", "changes"):
            fail(f"{path}: staged archive path must be codespec/changes/<repo-name>/<req-id>/proposal.md")
        if parts[2] != repo_name:
            fail(f"{path}: staged repository layer does not match repository identity")
        leaf = parts[3]
        if DRAFT_RE.fullmatch(leaf):
            if req_values and req_values[0]:
                fail(f"{path}: staged draft proposal req must be empty or absent")
        else:
            if len(req_values) != 1 or not req_values[0]:
                fail(f"{path}: staged proposal must contain exactly one non-empty req field")
            req_id = req_values[0]
            if not REQ_ID_RE.fullmatch(req_id):
                fail(f"{path}: invalid staged req-id: {req_id}")
            if leaf != req_id:
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
    staged.add_argument("--map", required=True, type=Path, dest="map_path")
    staged.add_argument("--repo", type=Path, default=Path.cwd())
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "plan":
            plan_migration(args.repo, args.map_path)
        else:
            check_staged(args.repo, args.map_path)
    except MigrationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
