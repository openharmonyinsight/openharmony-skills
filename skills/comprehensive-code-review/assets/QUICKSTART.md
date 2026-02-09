# Comprehensive Code Review - Quick Start Guide

## Installation

The skill should be automatically available. No installation needed.

## Basic Usage

### Review a Single File

```bash
# C++ file
analyze_code.py path/to/file.cpp

# TypeScript file
analyze_code.py path/to/file.ts

# With output
analyze_code.py path/to/file.cpp --output results.json
```

### Review a Directory

```bash
# Current directory only
analyze_code.py . --output results.json

# Recursive
analyze_code.py . --recursive --output results.json

# Specific directory
analyze_code.py frameworks/core/components_ng --recursive --output results.json
```

### Generate Report

```bash
# Generate from analysis results
generate_report.py --analysis results.json --output review_report.md

# Use custom template
generate_report.py --analysis results.json --output review.md --template assets/report_template.md
```

### Full Workflow

```bash
# Step 1: Analyze code
analyze_code.py path/to/code --recursive --output analysis_results.json

# Step 2: Generate report
generate_report.py --analysis analysis_results.json --output review_report.md

# Step 3: Review the report
cat review_report.md
```

## Filtering Results

### By Severity

```bash
analyze_code.py path/to/code --severity CRITICAL --output critical_only.json
analyze_code.py path/to/code --severity HIGH --output high_and_above.json
```

### By Dimension

```bash
analyze_code.py path/to/code --dimension Memory --output memory_issues.json
analyze_code.py path/to/code --dimension Security --output security_issues.json
```

## Common Workflows

### Pre-PR Review

```bash
# Analyze changed files
analyze_code.py path/to/pr/code --recursive --output pr_analysis.json
generate_report.py --analysis pr_analysis.json --output pr_review.md

# Check for critical issues
cat pr_review.md | grep -A 10 "CRITICAL"
```

### Component Review

```bash
# Review specific component
analyze_code.py frameworks/core/components_ng/pattern/menu --recursive --output menu_analysis.json
generate_report.py --analysis menu_analysis.json --output menu_review.md
```

### Architecture Compliance Check

```bash
# Check for ACE Engine architecture violations
analyze_code.py frameworks/core --recursive --output framework_analysis.json

# Look for architecture issues in the report
cat framework_analysis.json | grep -i "architecture"
```

### Memory Audit

```bash
# Find all memory-related issues
analyze_code.py path/to/code --recursive --output all_issues.json
generate_report.py --analysis all_issues.json --output memory_review.md

# Or filter by dimension during analysis
analyze_code.py path/to/code --dimension Memory --output memory_only.json
```

## Understanding Output

### Severity Levels

- **🔴 CRITICAL** - Must fix before merge (crashes, security vulnerabilities, memory leaks)
- **🟠 HIGH** - Should fix before merge (performance degradation, API violations)
- **🟡 MEDIUM** - Fix soon (code smells, minor issues)
- **🟢 LOW** - Nice to have (style, minor optimizations)

### Dimension Categories

The tool analyzes across these dimensions:

1. **Stability** - Error handling, boundary conditions
2. **Performance** - Algorithm complexity, optimization
3. **Threading** - Data races, synchronization
4. **Security** - Input validation, vulnerabilities
5. **Memory** - Smart pointers, leaks, ownership
6. **Modern C++** - C++11/14/17/20 features
7. **Code Smell** - Design issues (22 types)
8. **SOLID** - Design principles
9. **Architecture** - ACE Engine compliance

### Issue Format

Each issue includes:
- **File path and line number**
- **Dimension** (e.g., Memory, Security)
- **Severity** (CRITICAL, HIGH, MEDIUM, LOW)
- **Title** - Brief description
- **Detailed description** - What's wrong
- **Suggestion** - How to fix it
- **Code snippet** - The problematic code

## Integration with Development Workflow

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run on files about to be committed
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(cpp|cc|cxx|h|hpp|ts|tsx)$')

if [ -n "$CHANGED_FILES" ]; then
    echo "Running code review on changed files..."
    analyze_code.py $CHANGED_FILES --output commit_review.json

    # Check for critical issues
    CRITICAL_COUNT=$(grep -o '"severity": "CRITICAL"' commit_review.json | wc -l)

    if [ $CRITICAL_COUNT -gt 0 ]; then
        echo "❌ Found $CRITICAL_COUNT CRITICAL issues. Please fix before committing."
        exit 1
    fi
fi
```

### CI/CD Integration

Add to your CI pipeline:

```yaml
code_review:
  stage: test
  script:
    - analyze_code.py frameworks/core --recursive --output review_results.json
    - generate_report.py --analysis review_results.json --output review_report.md
    - |
      if grep -q '"severity": "CRITICAL"' review_results.json; then
        echo "CRITICAL issues found!"
        exit 1
      fi
  artifacts:
    paths:
      - review_results.json
      - review_report.md
```

## Tips and Best Practices

### 1. Start with CRITICAL Issues

```bash
# Filter only critical issues
jq '.[].issues[] | select(.severity == "CRITICAL")' analysis_results.json
```

### 2. Focus on High-Impact Files

```bash
# Find files with most issues
jq -r '.[] | "\(.file_path): \(.issues | length)"' analysis_results.json | sort -t: -k2 -rn
```

### 3. Track Progress

```bash
# Compare analyses over time
analyze_code.py . --recursive --output baseline.json
# ... make changes ...
analyze_code.py . --recursive --output current.json

# Show improvement
diff <(jq '[.[].issues | length]' baseline.json) \
     <(jq '[.[].issues | length]' current.json)
```

### 4. Custom Checks

Edit `analyze_code.py` to add project-specific patterns:

```python
# Add to CppAnalyzer._compile_patterns()
'custom_pattern': re.compile(r'YOUR_REGEX_HERE')
```

## Troubleshooting

### Issue: "File not supported"

**Solution:** Ensure file extension is one of:
- C++: `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp`, `.hxx`
- TypeScript: `.ts`, `.tsx`, `.ets`

### Issue: Too many false positives

**Solution:**
1. Review severity thresholds
2. Filter by dimension
3. Add custom patterns to ignore specific cases
4. Update code comments to suppress warnings

### Issue: Report is too long

**Solution:**
1. Filter by severity: `--severity HIGH`
2. Filter by dimension: `--dimension Memory`
3. Focus on specific files instead of full directory

## Advanced Usage

### Custom Report Templates

Create your own template based on `assets/report_template.md` and use:

```bash
generate_report.py --analysis results.json --template my_template.md --output custom_report.md
```

### Programmatic Access

```python
import json

# Load analysis results
with open('analysis_results.json') as f:
    results = json.load(f)

# Extract specific issues
for file_result in results:
    for issue in file_result['issues']:
        if issue['severity'] == 'CRITICAL':
            print(f"{file_result['file_path']}:{issue['line_number']} - {issue['title']}")
```

### Integration with Other Tools

```bash
# Combine with clang-tidy
clang-tidy path/to/code.cpp --export-fixes=clang_tidy.yaml
analyze_code.py path/to/code.cpp --output code_review.json

# Combine with valgrind
valgrind --leak-check=full ./program 2> valgrind.out
analyze_code.py path/to/code --recursive --output review.json
# Merge results in report
```

## Getting Help

For detailed information on each dimension, see:
- `references/STABILITY.md`
- `references/MEMORY.md`
- `references/SECURITY.md`
- `references/CODE_SMELLS.md`
- `references/SOLID.md`
- `references/ACE_ENGINE_SPECIFIC.md`
- And more in `references/`

## Examples

### Example 1: Review a Menu Component

```bash
analyze_code.py frameworks/core/components_ng/pattern/menu \
  --recursive --output menu_analysis.json

generate_report.py --analysis menu_analysis.json \
  --output menu_review.md

# Check for ACE Engine specific issues
grep -i "RefPtr\|WeakClaim\|OnModifyDone" menu_review.md
```

### Example 2: Security Audit

```bash
analyze_code.py . --recursive --dimension Security \
  --output security_audit.json

generate_report.py --analysis security_audit.json \
  --output security_report.md

# Look for critical security issues
jq '.[].issues[] | select(.severity == "CRITICAL")' security_audit.json
```

### Example 3: Memory Leak Detection

```bash
analyze_code.py . --recursive --dimension Memory \
  --output memory_check.json

# Find potential leaks
jq '.[].issues[] | select(.title | contains("leak") or contains("Leak"))' \
  memory_check.json
```

---

For more information, see the main [SKILL.md](../SKILL.md) file.
