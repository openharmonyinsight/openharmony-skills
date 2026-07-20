#!/usr/bin/env bash
set -euo pipefail

# POSIX wrapper. Use install_related_skills.py directly on Windows.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/install_related_skills.py" "$@"
