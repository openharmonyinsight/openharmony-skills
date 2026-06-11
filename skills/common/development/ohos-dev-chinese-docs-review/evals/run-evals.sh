#!/bin/bash
# Evaluation Runner for ohos-dev-chinese-docs-review
# This script helps run and manage evaluation test cases

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_BASE="$(dirname "$SKILL_DIR")/docs-check-workspace"
ITERATION="${1:-1}"
WORKSPACE="$WORKSPACE_BASE/iteration-$ITERATION"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Global variables
EVALS_FILE="$SCRIPT_DIR/evals.json"

# Function to extract JSON value using Python
get_json_value() {
    local key="$1"
    local id="$2"
    python3 -c "
import json
import sys
try:
    with open('$EVALS_FILE', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for eval_item in data.get('evals', []):
        if eval_item.get('id') == $id:
            if '$key' == 'assertions':
                assertions = eval_item.get('assertions', [])
                for a in assertions:
                    print(a)
            else:
                print(eval_item.get('$key', ''))
            sys.exit(0)
    sys.exit(1)
except Exception as e:
    sys.stderr.write(f'Error: {e}\\n')
    sys.exit(1)
" 2>/dev/null
}

# Function to list all test cases
list_test_cases() {
    python3 -c "
import json
try:
    with open('$EVALS_FILE', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for eval_item in data.get('evals', []):
        print(f\"{eval_item.get('id', '?')}. {eval_item.get('name', 'Unknown')}\")
except Exception as e:
    print(f'Error reading evals.json: {e}')
" 2>/dev/null
}

# Function to show test case summary
show_summary() {
    echo "Available test cases:"
    echo ""
    list_test_cases
    echo ""
}

# Function to run a single test case
run_test() {
    local test_id="$1"
    local mode="${2:-with_skill}"

    # Find test case by ID
    local test_name=$(get_json_value "name" "$test_id")
    local prompt=$(get_json_value "prompt" "$test_id")

    if [ -z "$test_name" ]; then
        echo -e "${RED}Error: Test case ID $test_id not found${NC}"
        return 1
    fi

    local eval_dir="eval-$test_name"
    local output_dir="$WORKSPACE/$eval_dir/$mode/outputs"

    echo "Running test case $test_id: $test_name ($mode)"
    echo "Output directory: $output_dir"
    echo ""
    echo "Prompt: $prompt"
    echo ""
    echo "---"
    echo ""
    echo "To run this test case in Claude Code:"
    echo ""
    echo "1. Load the skill:"
    if [ "$mode" = "with_skill" ]; then
        echo "   /skill $SKILL_DIR"
    fi
    echo ""
    echo "2. Execute the task:"
    echo "   $prompt"
    echo ""
    echo "3. Save outputs to:"
    echo "   $output_dir"
    echo ""
}

# Function to setup workspace
setup_workspace() {
    echo "Creating workspace structure..."
    mkdir -p "$WORKSPACE"

    # Create directories for all test cases
    python3 -c "
import json
import os
try:
    with open('$EVALS_FILE', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for eval_item in data.get('evals', []):
        test_name = eval_item.get('name', '')
        if test_name:
            for mode in ['with_skill', 'without_skill']:
                os.makedirs(f'$WORKSPACE/eval-{test_name}/{mode}/outputs', exist_ok=True)
            print(f'  Created: eval-{test_name}')
except Exception as e:
    print(f'Error: {e}')
" 2>/dev/null

    echo ""
    echo -e "${GREEN}Workspace setup complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run each test case with and without the skill"
    echo "2. Grade the results using the assertions in evals.json"
    echo "3. Aggregate results into benchmark.json"
    echo ""
}

# Function to show grading helper
show_grading() {
    local test_id="$1"

    echo "Grading helper for test case $test_id"
    echo ""

    local test_name=$(get_json_value "name" "$test_id")

    if [ -z "$test_name" ]; then
        echo -e "${RED}Error: Test case ID $test_id not found${NC}"
        exit 1
    fi

    echo "Assertions for $test_name:"
    echo ""

    get_json_value "assertions" "$test_id" | while IFS= read -r assertion; do
        echo "  [ ] $assertion"
    done
    echo ""
    echo "Create grading.json with:"
    echo ""
    echo '{
  "assertion_results": [
    {
      "text": "assertion text here",
      "passed": true,
      "evidence": "specific evidence from output"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  }
}'
    echo ""
}

# Main function
main() {
    echo "======================================"
    echo "Evaluation Runner for ohos-dev-chinese-docs-review"
    echo "======================================"
    echo ""
    echo "Skill directory: $SKILL_DIR"
    echo "Workspace: $WORKSPACE"
    echo "Iteration: $ITERATION"
    echo ""

    # Check if evals.json exists
    if [ ! -f "$EVALS_FILE" ]; then
        echo -e "${RED}Error: evals.json not found at $EVALS_FILE${NC}"
        exit 1
    fi

    echo "Found test case definition at $EVALS_FILE"
    echo ""

    # Parse command
    local action="${2:-list}"

    case "$action" in
        list)
            show_summary
            echo "Usage:"
            echo "  $0 [iteration] list                    # Show test cases"
            echo "  $0 [iteration] run [test_id] [mode]    # Show instructions for running a test"
            echo "  $0 [iteration] setup                   # Create workspace structure"
            echo "  $0 [iteration] grade [test_id]         # Show grading helper"
            echo ""
            echo "Example:"
            echo "  $0 1 run 1 with_skill                 # Show instructions for test 1"
            echo ""
            ;;
        run)
            run_test "$3" "$4"
            ;;
        setup)
            setup_workspace
            ;;
        grade)
            show_grading "$3"
            ;;
        *)
            show_summary
            ;;
    esac
}

# Run main function
main "$@"
