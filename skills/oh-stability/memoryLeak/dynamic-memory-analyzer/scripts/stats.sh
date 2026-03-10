#!/bin/bash
# new/delete Memory Management Statistics Script
# Part of new-delete-checker skill

TARGET_DIR=${1:-"frameworks/"}

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found"
    echo "Usage: $0 [target-directory]"
    echo "Example: $0 frameworks/"
    exit 1
fi

echo "=== new/delete Memory Management Statistics ==="
echo "Target directory: $TARGET_DIR"
echo ""

# Count new/delete operations
echo "## Basic Operations"
NEW_COUNT=$(grep -rn "new " "$TARGET_DIR" --include="*.cpp" --include="*.h" 2>/dev/null | wc -l)
DELETE_COUNT=$(grep -rn "delete " "$TARGET_DIR" --include="*.cpp" --include="*.h" 2>/dev/null | wc -l)
NEW_ARRAY_COUNT=$(grep -rn "new \[" "$TARGET_DIR" --include="*.cpp" --include="*.h" 2>/dev/null | wc -l)
DELETE_ARRAY_COUNT=$(grep -rn "delete\[\]" "$TARGET_DIR" --include="*.cpp" --include="*.h" 2>/dev/null | wc -l)

echo "new operations: $NEW_COUNT"
echo "delete operations: $DELETE_COUNT"
echo "new[] arrays: $NEW_ARRAY_COUNT"
echo "delete[] arrays: $DELETE_ARRAY_COUNT"
echo ""

# Calculate ratio
if [ $DELETE_COUNT -gt 0 ]; then
    RATIO=$(awk "BEGIN {printf \"%.2f\", $NEW_COUNT / $DELETE_COUNT}")
    echo "new/delete ratio: $RATIO"
else
    echo "new/delete ratio: N/A (no delete operations)"
fi
echo ""

# Count smart pointer usage
echo "## Smart Pointers"
REFPTR_COUNT=$(grep -rn "RefPtr" "$TARGET_DIR" --include="*.cpp" --include="*.h" 2>/dev/null | wc -l)
WEAKPTR_COUNT=$(grep -rn "WeakPtr" "$TARGET_DIR" --include="*.cpp" --include="*.h" 2>/dev/null | wc -l)
MAKEREF_COUNT=$(grep -rn "MakeRefPtr" "$TARGET_DIR" --include="*.cpp" 2>/dev/null | wc -l)

echo "RefPtr usage: $REFPTR_COUNT"
echo "WeakPtr usage: $WEAKPTR_COUNT"
echo "MakeRefPtr calls: $MAKEREF_COUNT"
echo ""

# Count null checks
echo "## Null Checks"
NULLPTR_CHECK=$(grep -rn "if.*!=.*nullptr" "$TARGET_DIR" --include="*.cpp" 2>/dev/null | wc -l)
CHECK_NULL_COUNT=$(grep -rn "CHECK_NULL_VOID\|CHECK_NULL_RETURN" "$TARGET_DIR" --include="*.cpp" 2>/dev/null | wc -l)

echo "if (xxx != nullptr) checks: $NULLPTR_CHECK"
echo "CHECK_NULL_* macros: $CHECK_NULL_COUNT"
echo ""

# Count Register/Unregister
echo "## Registration Patterns"
REGISTER_COUNT=$(grep -rn "Register\|Unregister" "$TARGET_DIR" --include="*.cpp" 2>/dev/null | wc -l)

echo "Register/Unregister calls: $REGISTER_COUNT"
echo ""

# Count AddChild/RemoveChild
echo "## Node Management"
CHILD_COUNT=$(grep -rn "AddChild\|RemoveChild" "$TARGET_DIR" --include="*.cpp" 2>/dev/null | wc -l)

echo "AddChild/RemoveChild calls: $CHILD_COUNT"
echo ""

# Analysis
echo "## Analysis"
echo ""

# Check new/delete balance
if [ $DELETE_COUNT -lt $((NEW_COUNT / 2)) ]; then
    echo "⚠️  WARNING: Low delete count relative to new"
    echo "   This may indicate memory leaks or heavy smart pointer usage"
elif [ $DELETE_COUNT -gt $((NEW_COUNT * 2)) ]; then
    echo "⚠️  WARNING: High delete count relative to new"
    echo "   This may indicate double delete issues"
else
    echo "✅ new/delete ratio appears reasonable"
fi
echo ""

# Check smart pointer usage
if [ $REFPTR_COUNT -gt 5000 ]; then
    echo "✅ High RefPtr usage (good for automatic memory management)"
elif [ $REFPTR_COUNT -gt 1000 ]; then
    echo "✅ Moderate RefPtr usage"
else
    echo "⚠️  WARNING: Low RefPtr usage - review manual memory management"
fi
echo ""

# Check null check consistency
if [ $CHECK_NULL_COUNT -gt 50000 ]; then
    echo "✅ High CHECK_NULL_* macro usage (consistent null checking)"
elif [ $CHECK_NULL_COUNT -gt 10000 ]; then
    echo "✅ Moderate CHECK_NULL_* macro usage"
else
    echo "⚠️  WARNING: Low CHECK_NULL_* macro usage - review null safety"
fi
echo ""

echo "=== Statistics Complete ==="
