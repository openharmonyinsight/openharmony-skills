#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

MAX_LINE_LENGTH="${SPEC_DOC_MAX_LINE_LENGTH:-1000}"
status=0

while IFS= read -r doc; do
    long_lines=$(awk -v max="$MAX_LINE_LENGTH" 'length($0) > max { print FILENAME ":" NR ":" length($0) }' "$doc")
    if [[ -n "$long_lines" ]]; then
        printf '%s\n' "$long_lines" >&2
        status=1
    fi

    if grep -nE '^\.\. (code-block|meta|index)::|:ref:`' "$doc" >&2; then
        status=1
    fi
done < <(find "$DOCS_DIR" -type f -name '*.md' | sort)

if [[ "$status" -ne 0 ]]; then
    fail "spec docs integrity check failed"
fi
