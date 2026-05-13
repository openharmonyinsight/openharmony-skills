# Report Specification

## Required Sections

### 1. Executive Summary
Issue count by severity: CRITICAL / HIGH / MEDIUM / LOW.

### 2. CRITICAL Issues (must fix before merge)
For each:
```
## CRITICAL: <short title>
File: path/to/file.cpp:line
Dimension: Memory | Security | Threading | Architecture | Stability

  <problematic code>

Why: <why this is dangerous>
Fix: <corrected code>
```

### 3. HIGH Issues (should fix before merge)
Same format as CRITICAL.

### 4. MEDIUM/LOW Issues
Group by dimension. Brief description + file:line + fix suggestion.

### 5. Action Items
Ordered by priority. Include effort estimate (small/medium/large).

### 6. ACE Engine Compliance (if applicable)
- Architecture: compliant / violations listed
- Memory: compliant / violations listed
- Lifecycle: compliant / violations listed
- Naming: compliant / violations listed

## Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Must fix before merge | Blocks merge |
| HIGH | Should fix before merge | Strongly recommended |
| MEDIUM | Fix soon | Track in backlog |
| LOW | Nice to have | Address when convenient |

## Note on Scope

For focused reviews (single dimension or <3 files), skip sections 4-6 and focus on the requested dimension only. For full reviews, include all sections.
