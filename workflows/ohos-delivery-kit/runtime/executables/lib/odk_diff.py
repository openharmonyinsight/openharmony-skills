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
