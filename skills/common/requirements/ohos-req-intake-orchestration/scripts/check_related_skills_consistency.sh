#!/usr/bin/env bash
set -euo pipefail

# POSIX wrapper. Use check_related_skills_consistency.py directly on Windows.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/check_related_skills_consistency.py" "$@"
