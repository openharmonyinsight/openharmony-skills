#!/usr/bin/env bash
set -euo pipefail

# POSIX wrapper. Use test_related_skills_consistency.py directly on Windows.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/test_related_skills_consistency.py" "$@"
