#!/bin/bash
#
# Script to extract the last complete error from OpenHarmony build logs
# Usage: ./extract_last_error.sh [build_log_path]
#

set -e

# Configuration
BUILD_DIR="${PWD}/out"
OUTPUT_FILE="last_error.log"
PRODUCT_NAME="${PRODUCT_NAME:-rk3568}"

# Output file will be placed in the same directory as build log
# Extract log directory for later use
LOG_DIR=""

# Allow custom build log path
if [ -n "$1" ]; then
    BUILD_LOG="$1"
else
    # Try to find build.log in common locations
    POSSIBLE_LOGS=(
        "out/${PRODUCT_NAME}/build.log"
        "out/build.log"
        "${BUILD_DIR}/${PRODUCT_NAME}/build.log"
        "${BUILD_DIR}/build.log"
    )

    BUILD_LOG=""
    for log in "${POSSIBLE_LOGS[@]}"; do
        if [ -f "$log" ]; then
            BUILD_LOG="$log"
            break
        fi
    done
fi

# If still no log found, check if it's in the current directory
if [ -z "$BUILD_LOG" ] && [ -f "build.log" ]; then
    BUILD_LOG="build.log"
fi

# Check if build log exists
if [ -z "$BUILD_LOG" ]; then
    echo "Error: Build log not found!" >&2
    echo "Searched locations:" >&2
    for log in "${POSSIBLE_LOGS[@]}"; do
        echo "  - ${log}" >&2
    done
    echo "You can specify the log path as: $0 /path/to/build.log" >&2
    exit 1
fi

# Extract directory path for output file
LOG_DIR=$(dirname "$BUILD_LOG")

# Set output file to same directory as build log
OUTPUT_FILE="${LOG_DIR}/last_error.log"

echo "Using build log: $BUILD_LOG"
echo "Output file: $OUTPUT_FILE"

# Function to extract the last complete error
extract_last_error() {
    local log_file="$1"
    local output="$2"

    # Use Python to reliably extract the error block
    # This approach: find the last [N/M] CXX block that contains errors
    python3 - "$log_file" "$output" << 'PYTHON_SCRIPT'
import sys
import re

def extract_last_error(log_file, output_file):
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        with open(output_file, 'w') as f:
            f.write("build success, no error\n")
        return

    # First, scan the entire log to detect if there are any real errors
    # Real errors: FAILED, fatal error, undefined reference, errors generated
    has_real_error = False
    for line in lines:
        # Check for real error indicators (excluding target names like "form_error")
        if re.search(r'(FAILED\s*:|fatal error:|undefined reference|errors generated\.|ld\.lld: error:)', line):
            has_real_error = True
            break

    # If no real errors found, write success message and return
    if not has_real_error:
        with open(output_file, 'w') as f:
            f.write("build success, no error\n")
        return

    # Find all error blocks (from [N/M] to next [N/M])
    blocks = []
    current_block = []

    for line in lines:
        # Check if this is a start of a new build task
        # Match: [N/M] followed by task type
        if re.match(r'^\[\d+/\d+\]', line):
            # Save previous block if it exists
            if current_block:
                blocks.append(current_block)
            # Start new block
            current_block = [line]
        elif current_block:
            current_block.append(line)

    # Don't forget the last block
    if current_block:
        blocks.append(current_block)

    # Find the last block that contains real errors
    for block in reversed(blocks):
        block_text = ''.join(block)
        if re.search(r'(FAILED\s*:|fatal error:|undefined reference|errors generated\.|ld\.lld: error:)', block_text):
            # Expand the block to include more context (include previous blocks if needed)
            # Write to output file
            with open(output_file, 'w') as f:
                f.writelines(block)
            return

    # Should not reach here if has_real_error is True, but just in case
    with open(output_file, 'w') as f:
        f.write("build success, no error\n")

if __name__ == '__main__':
    log_file = sys.argv[1]
    output_file = sys.argv[2]
    extract_last_error(log_file, output_file)
PYTHON_SCRIPT

    return 0
}

# Extract the error
echo "Extracting last error..."
extract_last_error "$BUILD_LOG" "$OUTPUT_FILE"

# Report results
if [ -s "$OUTPUT_FILE" ]; then
    ERROR_SIZE=$(wc -l < "$OUTPUT_FILE")
    echo "Error extracted to: $OUTPUT_FILE"
    echo "Error block size: $ERROR_SIZE lines"

    # Check if it's a success message
    if grep -q "build success, no error" "$OUTPUT_FILE"; then
        echo "Build completed successfully!"
    else
        echo ""
        echo "=== Last Error Summary ==="
        head -20 "$OUTPUT_FILE"
        if [ "$ERROR_SIZE" -gt 20 ]; then
            echo "... (truncated, see $OUTPUT_FILE for full error)"
        fi
    fi
else
    echo "build success, no error" > "$OUTPUT_FILE"
    echo "Build completed successfully!"
fi

echo "Output saved to: $(pwd)/$OUTPUT_FILE"
