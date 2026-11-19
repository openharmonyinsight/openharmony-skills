"""Structural unified-diff evidence checks, not source applicability checks."""
import re


def valid_unified_diff(text: str) -> bool:
    """Require file headers, complete counted hunks and actual changed lines.

    Accept text diffs from git diff / diff -u. Binary, metadata-only and empty
    patches are not API declaration evidence. Do not execute or apply the patch.
    """
    lines = text.splitlines()
    i = 0
    files = 0
    while i < len(lines):
        # Git text-diff metadata before the ---/+++ file headers.
        while i < len(lines) and lines[i].startswith((
            'diff --git ', 'index ', 'new file mode ', 'deleted file mode ',
            'old mode ', 'new mode ', 'similarity index ', 'rename from ', 'rename to ',
        )):
            i += 1
        if i + 1 >= len(lines) or not lines[i].startswith('--- ') or not lines[i + 1].startswith('+++ '):
            return False
        if not lines[i][4:].strip() or not lines[i + 1][4:].strip():
            return False
        if lines[i][4:].strip() == lines[i + 1][4:].strip() == '/dev/null':
            return False
        i += 2
        hunks = 0
        changed = False
        while i < len(lines) and lines[i].startswith('@@ '):
            match = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: .*)?', lines[i])
            if not match:
                return False
            old = int(match[2]) if match[2] is not None else 1
            new = int(match[4]) if match[4] is not None else 1
            i += 1
            last_was_content = False
            while old or new:
                if i >= len(lines):
                    return False
                line = lines[i]
                if line == '\\ No newline at end of file' and last_was_content:
                    last_was_content = False
                    i += 1
                    continue
                if not line or line[0] not in ' +-':
                    return False
                old -= line[0] in ' -'
                new -= line[0] in ' +'
                if old < 0 or new < 0:
                    return False
                changed |= line[0] in '+-'
                last_was_content = True
                i += 1
            if i < len(lines) and lines[i] == '\\ No newline at end of file' and last_was_content:
                i += 1
            hunks += 1
        if not hunks or not changed:
            return False
        files += 1
    return files > 0


def unified_diff_additions(text: str) -> dict[str, list[str]]:
    """Return added lines grouped by the target path of each unified diff.

    The caller must first establish that the diff is structurally valid. This
    helper deliberately does not apply the patch or parse source syntax; it
    only separates ``+`` content from context and deleted lines.
    """

    additions: dict[str, list[str]] = {}
    target: str | None = None
    hunk_re = re.compile(
        r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: .*)?$"
    )
    pending_old = pending_new = 0

    for line in text.splitlines():
        if pending_old == pending_new == 0 and line.startswith("+++ "):
            value = line[4:].strip()
            # GNU diff may append a tab and timestamp after the path. Paths may
            # also be quoted when they contain spaces or non-ASCII characters.
            value = value.split("\t", 1)[0]
            if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            if value.startswith("b/"):
                value = value[2:]
            target = None if value == "/dev/null" else value
            if target is not None:
                additions.setdefault(target, [])
            continue
        hunk = hunk_re.fullmatch(line)
        if hunk:
            pending_old = int(hunk.group(2) or 1)
            pending_new = int(hunk.group(4) or 1)
            continue
        if target is None or pending_old == pending_new == 0:
            continue
        if line == "\\ No newline at end of file":
            continue
        if line.startswith("+"):
            additions[target].append(line[1:])
            pending_new -= 1
        elif line.startswith("-"):
            pending_old -= 1
        elif line.startswith(" "):
            pending_old -= 1
            pending_new -= 1
        else:
            # Structurally valid hunks only contain these prefixes. Reset rather
            # than silently misattributing later content to the current hunk.
            pending_old = pending_new = 0

    return additions


def unified_diff_sides(text: str) -> dict[str, dict[str, object]]:
    """Return continuous old/new diff segments grouped by target path.

    Each segment retains its one-based source start line, represented lines,
    and zero-based changed positions within that segment. API declaration and
    comment matching must stay inside one segment; separate hunks are not
    proof that lines are adjacent in the source file.
    """

    result: dict[str, dict[str, object]] = {}
    target: str | None = None
    old_segment: dict[str, object] | None = None
    new_segment: dict[str, object] | None = None
    hunk_re = re.compile(
        r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: .*)?$"
    )
    pending_old = pending_new = 0

    for line in text.splitlines():
        if pending_old == pending_new == 0 and line.startswith("+++ "):
            value = line[4:].strip().split("\t", 1)[0]
            if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            if value.startswith("b/"):
                value = value[2:]
            target = None if value == "/dev/null" else value
            old_segment = None
            new_segment = None
            if target is not None:
                result.setdefault(target, {
                    "oldSegments": [],
                    "newSegments": [],
                })
            continue

        hunk = hunk_re.fullmatch(line)
        if hunk:
            if target is None:
                old_segment = new_segment = None
                pending_old = pending_new = 0
                continue
            sides = result[target]
            old_segments: list[dict[str, object]] = sides["oldSegments"]  # type: ignore[assignment]
            new_segments: list[dict[str, object]] = sides["newSegments"]  # type: ignore[assignment]
            old_segment = {
                "start": int(hunk.group(1)),
                "lines": [],
                "changed": set(),
            }
            new_segment = {
                "start": int(hunk.group(3)),
                "lines": [],
                "changed": set(),
            }
            old_segments.append(old_segment)
            new_segments.append(new_segment)
            pending_old = int(hunk.group(2) or 1)
            pending_new = int(hunk.group(4) or 1)
            continue

        if (
            target is None
            or old_segment is None
            or new_segment is None
            or pending_old == pending_new == 0
        ):
            continue

        old_lines: list[str] = old_segment["lines"]  # type: ignore[assignment]
        new_lines: list[str] = new_segment["lines"]  # type: ignore[assignment]
        changed_old: set[int] = old_segment["changed"]  # type: ignore[assignment]
        changed_new: set[int] = new_segment["changed"]  # type: ignore[assignment]

        if line == "\\ No newline at end of file":
            continue
        if line.startswith("+"):
            new_lines.append(line[1:])
            changed_new.add(len(new_lines) - 1)
            pending_new -= 1
        elif line.startswith("-"):
            old_lines.append(line[1:])
            changed_old.add(len(old_lines) - 1)
            pending_old -= 1
        elif line.startswith(" "):
            content = line[1:]
            old_lines.append(content)
            new_lines.append(content)
            pending_old -= 1
            pending_new -= 1
        else:
            pending_old = pending_new = 0

    return result
