#!/bin/bash
# analyze-includes.sh
# Analyze header file include dependencies and identify optimization opportunities
# Part of header-optimization skill

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <header_file> [output_format]"
    echo "  header_file: Path to the header file to analyze"
    echo "  output_format: 'text' (default) or 'json'"
    exit 1
fi

HEADER_FILE="$1"
OUTPUT_FORMAT="${2:-text}"

if [ ! -f "$HEADER_FILE" ]; then
    echo "Error: Header file '$HEADER_FILE' not found"
    exit 1
fi

# Extract filename without path
HEADER_NAME=$(basename "$HEADER_FILE")

echo "Analyzing: $HEADER_NAME"
echo "========================================"
echo ""

# Count total lines
TOTAL_LINES=$(wc -l < "$HEADER_FILE")
echo "Total lines: $TOTAL_LINES"
echo ""

# Extract all includes
INCLUDES=$(grep -E '^#include' "$HEADER_FILE" || true)
INCLUDE_COUNT=$(echo "$INCLUDES" | grep -c . || echo "0")

echo "Include Analysis"
echo "----------------"
echo "Total includes: $INCLUDE_COUNT"
echo ""

if [ "$INCLUDE_COUNT" -gt 0 ]; then
    echo "Current includes:"
    echo "$INCLUDES" | while read -r line; do
        echo "  $line"
    done
    echo ""
fi

# Analyze each include for potential forward declaration
echo "Optimization Opportunities"
echo "--------------------------"

# Common ace_engine patterns that can often be forward declared
COMMON_FWD_DECL=(
    "core/components_ng/base/frame_node.h:FrameNode"
    "core/components_ng/base/ui_node.h:UINode"
    "core/components_ng/property/.*_layout_property.h:LayoutProperty"
    "core/components_ng/property/.*_paint_property.h:PaintProperty"
    "core/components_ng/event/event_hub.h:EventHub"
    "core/pipeline/base/element.h:Element"
    "core/pipeline/base/render_node.h:RenderNode"
)

# Check for includes that might be convertible
for pattern in "${COMMON_FWD_DECL[@]}"; do
    header=$(echo "$pattern" | cut -d: -f1)
    classname=$(echo "$pattern" | cut -d: -f2)

    if echo "$INCLUDES" | grep -q "$header"; then
        # Check if type appears in file
        if grep -q "$classname" "$HEADER_FILE"; then
            echo "  ✗ $header"
            echo "    → Contains: $classname (candidate for forward declaration)"
        fi
    fi
done

# Check for unused includes
echo ""
echo "Potential Unused Includes"
echo "-------------------------"

echo "$INCLUDES" | while read -r include; do
    # Extract header name from include
    header_path=$(echo "$include" | sed 's/#include [<"]//g' | sed 's/[>"]//g')
    header_name=$(basename "$header_path" .h)

    # Check if header name appears in file (excluding the include line itself)
    if [ -n "$header_name" ]; then
        # Remove includes temporarily and search for the class name
        usage_count=$(grep -v "^#include" "$HEADER_FILE" | grep -c "$header_name" || echo "0")

        if [ "$usage_count" -eq 0 ]; then
            echo "  ⚠ $include"
            echo "    → Possibly unused (no '$header_name' found)"
        fi
    fi
done

# Estimate impact
echo ""
echo "Impact Estimate"
echo "---------------"

if [ "$INCLUDE_COUNT" -le 3 ]; then
    echo "Include count is LOW ($INCLUDE_COUNT)"
    echo "Optimization priority: LOW"
elif [ "$INCLUDE_COUNT" -le 7 ]; then
    echo "Include count is MEDIUM ($INCLUDE_COUNT)"
    echo "Optimization priority: MEDIUM"
else
    echo "Include count is HIGH ($INCLUDE_COUNT)"
    echo "Optimization priority: HIGH"
fi

# Check for inline methods
INLINE_METHODS=$(grep -P '^\s*(\w+\s+)+\w+\s*\([^)]*\)\s*(const\s*)?\{' "$HEADER_FILE" | wc -l)
echo ""
echo "Inline implementation methods: ~$INLINE_METHODS"
if [ "$INLINE_METHODS" -gt 3 ]; then
    echo "  → Consider moving to cpp file"
fi

# Calculate potential savings (rough estimate)
POTENTIAL_FWD_DECLS=$(echo "$INCLUDES" | grep -E "(frame_node|ui_node|element|layout_property|paint_property|event_hub)" | wc -l || echo "0")
POTENTIAL_REDUCTION=$((POTENTIAL_FWD_DECLS * 100 / (INCLUDE_COUNT + 1)))

echo ""
echo "Potential Optimization Impact"
echo "----------------------------"
echo "Estimated forward declaration candidates: ~$POTENTIAL_FWD_DECLS"
if [ "$INCLUDE_COUNT" -gt 0 ]; then
    echo "Potential include reduction: ~$POTENTIAL_REDUCTION%"
fi

echo ""
echo "========================================"
echo "Analysis complete"
echo ""
echo "Next steps:"
echo "  1. Review optimization opportunities above"
echo "  2. Apply header-optimization skill"
echo "  3. Use compile-analysis skill to measure improvement"

exit 0
