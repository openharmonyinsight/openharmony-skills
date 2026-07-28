#!/bin/bash
# Auto-fix common N-API triple verification failures
# Usage: ./auto_fix_napi_triple.sh <target_path>

set -e

# 显示帮助信息
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Auto-fix common N-API triple verification failures"
    echo ""
    echo "Usage: $0 <target_path>"
    echo ""
    echo "This script automatically fixes:"
    echo "  1. Missing N-API function registrations"
    echo "  2. Missing TypeScript declarations"
    echo ""
    echo "After fixing, run: bash scripts/verify_napi_triple.sh <target_path>"
    exit 0
fi

TARGET_PATH=${1:?Usage: $0 <target_path>}
if [ ! -d "$TARGET_PATH" ]; then
    echo "Error: Target path does not exist: $TARGET_PATH"
    exit 1
fi

NAPI_FILE="${TARGET_PATH}/entry/src/main/cpp/NapiTest.cpp"
TS_FILE="${TARGET_PATH}/entry/src/main/cpp/types/libentry/index.d.ts"

if [ ! -f "$NAPI_FILE" ]; then
    echo "Error: NapiTest.cpp not found at $NAPI_FILE"
    exit 1
fi

if [ ! -f "$TS_FILE" ]; then
    echo "Error: index.d.ts not found at $TS_FILE"
    exit 1
fi

echo "=== N-API Auto-Fix Tool ==="
echo "Target: $TARGET_PATH"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fix 1: Add missing registrations
echo "[Fix 1] Checking for missing registrations..."
defined_funcs=$(grep -oP 'static napi_value\s+\K[A-Za-z0-9_]+(?=\s*\()' "$NAPI_FILE" 2>/dev/null | sort | uniq || echo "")
registered_funcs=$(grep -A 100 'napi_property_descriptor desc\[\]' "$NAPI_FILE" 2>/dev/null | \
    grep -oP 'DECLARE_NAPI_[A-Z]+\(\s*"[^"]+"\s*,\s*\K[A-Za-z0-9_]+' | sort | uniq || echo "")

if [ -z "$defined_funcs" ]; then
    echo "  ${YELLOW}⚠️${NC} No N-API functions defined. Nothing to fix."
else
    missing_count=0
    for func in $(comm -23 <(echo "$defined_funcs") <(echo "$registered_funcs")); do
        if [ -n "$func" ]; then
            # Extract function name without _napi suffix for JS export name
            export_name=$(echo "$func" | sed 's/_napi$//')
            echo "  ${GREEN}[FIX]${NC} Adding missing registration: $func → export name: $export_name"
            # Add before closing brace of desc[]
            if grep -q "^};" "$NAPI_FILE"; then
                sed -i "/^};/i\    DECLARE_NAPI_PROPERTY(\"$export_name\", $func)," "$NAPI_FILE"
            else
                echo "  ${YELLOW}⚠️${NC} Could not find desc[] closing brace, skipping..."
            fi
            ((missing_count++))
        fi
    done

    if [ $missing_count -eq 0 ]; then
        echo "  ${GREEN}✅${NC} No missing registrations found."
    else
        echo "  ${GREEN}✅${NC} Fixed $missing_count missing registration(s)"
    fi
fi

echo ""

# Fix 2: Add missing TypeScript declarations
echo "[Fix 2] Checking for missing TypeScript declarations..."
js_names=$(grep -A 100 'napi_property_descriptor desc\[\]' "$NAPI_FILE" 2>/dev/null | \
    grep -oP 'DECLARE_NAPI_[A-Z]+\(\s*"\K[^"]+' | sort | uniq || echo "")

declared_names=$(grep 'export const' "$TS_FILE" 2>/dev/null | \
    grep -oP 'export const\s+\K[A-Za-z0-9_]+' | sort | uniq || echo "")

if [ -z "$js_names" ]; then
    echo "  ${YELLOW}⚠️${NC} No registered functions found. Nothing to fix."
else
    missing_ts_count=0
    for name in $(comm -23 <(echo "$js_names") <(echo "$declared_names")); do
        if [ -n "$name" ]; then
            echo "  ${GREEN}[FIX]${NC} Adding missing TypeScript declaration for: $name"
            # Infer parameter types from C++ signature (simplified)
            # For production, parse function signature more thoroughly
            echo "export const $name: (...args: unknown[]) => Promise<number>;" >> "$TS_FILE"
            ((missing_ts_count++))
        fi
    done

    if [ $missing_ts_count -eq 0 ]; then
        echo "  ${GREEN}✅${NC} No missing declarations found."
    else
        echo "  ${GREEN}✅${NC} Fixed $missing_ts_count missing declaration(s)"
    fi
fi

echo ""

# Fix 3: Check for orphaned TypeScript declarations
echo "[Fix 3] Checking for orphaned TypeScript declarations..."
orphan_count=0
for name in $(comm -13 <(echo "$js_names") <(echo "$declared_names")); do
    if [ -n "$name" ]; then
        echo "  ${YELLOW}[WARN]${NC} Found orphaned declaration: $name (no matching N-API registration)"
        # This requires manual review - don't auto-remove as it might be intentional
        ((orphan_count++))
    fi
done

if [ $orphan_count -eq 0 ]; then
    echo "  ${GREEN}✅${NC} No orphaned declarations found."
else
    echo "  ${YELLOW}⚠️${NC} Found $orphan_count orphaned declaration(s) - manual review recommended"
fi

echo ""
echo "=== Summary ==="
echo "Auto-fix complete."
echo ""
echo "Next steps:"
echo "  1. Review the changes made to:"
echo "     - $NAPI_FILE"
echo "     - $TS_FILE"
echo "  2. Run verification:"
echo "     bash scripts/verify_napi_triple.sh $TARGET_PATH"
echo "  3. If orphaned declarations were found, review manually"
echo ""
