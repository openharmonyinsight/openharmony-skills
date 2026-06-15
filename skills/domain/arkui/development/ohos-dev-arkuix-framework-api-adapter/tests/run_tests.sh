#!/bin/bash
# Evaluation test runner for arkuix-framework-api-adapter
#
# Usage: bash tests/run_tests.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "  arkuix-framework-api-adapter Evaluation Test Suite"
echo "============================================================"
echo ""

echo "[Category A] Script Functional Tests (automated)"
echo "------------------------------------------------------------"
python3 "$SCRIPT_DIR/test_scripts.py"
echo ""

echo "[Category B-E] Scenario-based Tests (manual evaluation)"
echo "------------------------------------------------------------"
echo "See the following files for test case specifications:"
echo "  - test_decision_trees.md   (B01-B08: Decision tree scenarios)"
echo "  - test_constraints.md      (C01-C04: Constraint enforcement)"
echo "  - test_never_and_triggers.md (D01-D03, E01-E02: NEVER list + triggers)"
echo ""
echo "Evaluate by loading the skill and presenting each case to an agent."
echo ""
echo "============================================================"
echo "  Automated tests complete."
echo "============================================================"
