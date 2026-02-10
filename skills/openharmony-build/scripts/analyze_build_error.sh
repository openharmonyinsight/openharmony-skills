#!/bin/bash
# OpenHarmony Build Error Analysis Script
# Analyzes build logs and extracts relevant error information

set -e

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# OpenHarmony root directory
# Script is at: .../ace_engine/.claude/skills/openharmony-build/scripts/
# Need to go up 7 levels to reach OpenHarmony root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OH_ROOT="$(cd "$SCRIPT_DIR/../../../../../../.." && pwd)"

echo -e "${GREEN}OpenHarmony Build Error Analyzer${NC}"
echo "OpenHarmony Root: $OH_ROOT"
echo ""

# Check if product name is provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage: $0 <product-name>${NC}"
    echo "Example: $0 rk3568"
    echo ""
    echo "Available products in out/:"
    ls -1 "$OH_ROOT/out/" 2>/dev/null | grep -v "sdk\|gen\|kernel" || echo "  No products found"
    exit 1
fi

PRODUCT_NAME="$1"
BUILD_LOG="$OH_ROOT/out/$PRODUCT_NAME/build.log"

# Check if build log exists
if [ ! -f "$BUILD_LOG" ]; then
    echo -e "${RED}Error: Build log not found: $BUILD_LOG${NC}"
    echo ""
    echo "Searching for alternative log files..."
    find "$OH_ROOT/out/$PRODUCT_NAME" -name "*.log" -type f 2>/dev/null | head -5
    exit 1
fi

echo -e "${GREEN}Analyzing build log: $BUILD_LOG${NC}"
echo ""

# Extract summary information
echo -e "${YELLOW}=== Build Summary ===${NC}"
echo "Log file: $BUILD_LOG"
echo "File size: $(du -h "$BUILD_LOG" | cut -f1)"
echo "Last modified: $(stat -c '%y' "$BUILD_LOG" 2>/dev/null || stat -f '%Sm' "$BUILD_LOG")"
echo ""

# Check for build completion
if grep -q "build.*successful" "$BUILD_LOG" 2>/dev/null; then
    echo -e "${GREEN}Status: Build completed successfully${NC}"
else
    echo -e "${RED}Status: Build failed or incomplete${NC}"
fi
echo ""

# Extract error statistics
echo -e "${YELLOW}=== Error Statistics ===${NC}"
ERROR_COUNT=$(grep -ci "error:" "$BUILD_LOG" 2>/dev/null || echo "0")
WARNING_COUNT=$(grep -ci "warning:" "$BUILD_LOG" 2>/dev/null || echo "0")
FATAL_COUNT=$(grep -ci "fatal" "$BUILD_LOG" 2>/dev/null || echo "0")

echo "Total errors: $ERROR_COUNT"
echo "Total warnings: $WARNING_COUNT"
echo "Fatal errors: $FATAL_COUNT"
echo ""

# Extract fatal errors
echo -e "${YELLOW}=== Fatal Errors ===${NC}"
if grep -i "fatal" "$BUILD_LOG" 2>/dev/null | head -20 | grep -q .; then
    grep -i "fatal" "$BUILD_LOG" 2>/dev/null | head -20 | while IFS= read -r line; do
        echo -e "${RED}$line${NC}"
    done
else
    echo "No fatal errors found"
fi
echo ""

# Extract last 50 error lines (most recent errors)
echo -e "${YELLOW}=== Recent Errors (last 50) ===${NC}"
grep -i "error:" "$BUILD_LOG" 2>/dev/null | tail -50 | while IFS= read -r line; do
    echo -e "${RED}$line${NC}"
done
echo ""

# Extract FAILED sections (from ninja/make)
echo -e "${YELLOW}=== Build Failures ===${NC}"
grep -B 5 "FAILED:" "$BUILD_LOG" 2>/dev/null | tail -50 || echo "No FAILED sections found"
echo ""

# Extract undefined reference errors (linker errors)
echo -e "${YELLOW}=== Linker Errors (undefined references) ===${NC}"
grep "undefined reference" "$BUILD_LOG" 2>/dev/null | head -20 || echo "No undefined reference errors"
echo ""

# Extract file not found errors
echo -e "${YELLOW}=== File Not Found Errors ===${NC}"
grep -i "no such file\|cannot find\|file not found" "$BUILD_LOG" 2>/dev/null | head -20 || echo "No file not found errors"
echo ""

# Extract compilation errors with context
echo -e "${YELLOW}=== Compilation Errors with Context ===${NC}"
# Find lines with "error:" and show 3 lines before and after
grep -B 3 -A 3 "error:" "$BUILD_LOG" 2>/dev/null | grep -A 3 -B 3 "error:" | tail -100 || echo "No compilation errors with context"
echo ""

# Check for common OpenHarmony build issues
echo -e "${YELLOW}=== Common Issue Detection ===${NC}"

# Check for Python version issues
if grep -qi "python.*version" "$BUILD_LOG" 2>/dev/null; then
    echo -e "${YELLOW}⚠ Python version issues detected${NC}"
    grep -i "python.*version" "$BUILD_LOG" 2>/dev/null | head -5
fi

# Check for Node.js version issues
if grep -qi "node.*version" "$BUILD_LOG" 2>/dev/null; then
    echo -e "${YELLOW}⚠ Node.js version issues detected${NC}"
    grep -i "node.*version" "$BUILD_LOG" 2>/dev/null | head -5
fi

# Check for dependency issues
if grep -qi "dependenc" "$BUILD_LOG" 2>/dev/null; then
    echo -e "${YELLOW}⚠ Dependency issues detected${NC}"
    grep -i "dependenc" "$BUILD_LOG" 2>/dev/null | head -10
fi

echo ""
echo -e "${GREEN}=== Analysis Complete ===${NC}"
echo ""
echo "To view full log: less $BUILD_LOG"
echo "To search specific errors: grep -i 'keyword' $BUILD_LOG"
