# Code Review Report Template

## Header

**Project:** ACE Engine (OpenHarmony ArkUI Framework)
**Review Date:** {{DATE}}
**Reviewer:** {{REVIEWER}}
**Branch/PR:** {{BRANCH}}

---

## Executive Summary

**Overall Assessment:** {{OVERALL_GRADE}}

- Files analyzed: {{FILE_COUNT}}
- Total issues: {{TOTAL_ISSUES}}
- Critical issues: {{CRITICAL_COUNT}}
- High priority: {{HIGH_COUNT}}
- Medium priority: {{MEDIUM_COUNT}}
- Low priority: {{LOW_COUNT}}

### Risk Assessment

{{RISK_ASSESSMENT}}

---

## 🔴 CRITICAL Issues

*Must fix before merge*

{{CRITICAL_ISSUES}}

---

## 🟠 HIGH Priority Issues

*Should fix before merge*

{{HIGH_ISSUES}}

---

## 🟡 MEDIUM Priority Issues

*Fix soon*

{{MEDIUM_ISSUES}}

---

## 🟢 LOW Priority Issues

*Nice to have*

{{LOW_ISSUES}}

---

## Dimension Breakdown

| Dimension | Critical | High | Medium | Low | Total |
|-----------|----------|------|--------|-----|-------|
| Stability | {{STABILITY_CRITICAL}} | {{STABILITY_HIGH}} | {{STABILITY_MEDIUM}} | {{STABILITY_LOW}} | {{STABILITY_TOTAL}} |
| Performance | {{PERFORMANCE_CRITICAL}} | {{PERFORMANCE_HIGH}} | {{PERFORMANCE_MEDIUM}} | {{PERFORMANCE_LOW}} | {{PERFORMANCE_TOTAL}} |
| Threading | {{THREADING_CRITICAL}} | {{THREADING_HIGH}} | {{THREADING_MEDIUM}} | {{THREADING_LOW}} | {{THREADING_TOTAL}} |
| Security | {{SECURITY_CRITICAL}} | {{SECURITY_HIGH}} | {{SECURITY_MEDIUM}} | {{SECURITY_LOW}} | {{SECURITY_TOTAL}} |
| Memory | {{MEMORY_CRITICAL}} | {{MEMORY_HIGH}} | {{MEMORY_MEDIUM}} | {{MEMORY_LOW}} | {{MEMORY_TOTAL}} |
| Code Smells | {{CODE_SMELL_CRITICAL}} | {{CODE_SMELL_HIGH}} | {{CODE_SMELL_MEDIUM}} | {{CODE_SMELL_LOW}} | {{CODE_SMELL_TOTAL}} |
| SOLID Principles | {{SOLID_CRITICAL}} | {{SOLID_HIGH}} | {{SOLID_MEDIUM}} | {{SOLID_LOW}} | {{SOLID_TOTAL}} |
| Architecture | {{ARCHITECTURE_CRITICAL}} | {{ARCHITECTURE_HIGH}} | {{ARCHITECTURE_MEDIUM}} | {{ARCHITECTURE_LOW}} | {{ARCHITECTURE_TOTAL}} |

---

## File-by-File Analysis

{{FILE_DETAILS}}

---

## ACE Engine Compliance

### Architecture Compliance

- [ ] Four-layer architecture respected
- [ ] Proper Pattern/Model/Property separation
- [ ] No layer boundary violations
- [ ] Platform abstraction used correctly

### Memory Management

- [ ] RefPtr used for all allocations
- [ ] AceType::DynamicCast used for type-safe casting
- [ ] WeakPtr used to break circular references
- [ ] Callbacks use WeakClaim for this capture

### Component Lifecycle

- [ ] OnModifyDone implemented correctly
- [ ] OnDirtyLayoutWrapperSwap handled
- [ ] OnAttachToFrameNode used for initialization

### Naming Conventions

- [ ] Classes use PascalCase
- [ ] Methods use PascalCase
- [ ] Private members use snake_case_
- [ ] Constants use UPPER_CASE

---

## Detailed Findings

### Issue #{{ISSUE_NUMBER}}: {{ISSUE_TITLE}}

**File:** `{{FILE_PATH}}`
**Line:** {{LINE_NUMBER}}
**Dimension:** {{DIMENSION}}
**Severity:** {{SEVERITY}}

#### Description
{{DESCRIPTION}}

#### Why This Matters
{{IMPACT}}

#### Suggested Fix
{{SUGGESTION}}

#### Before
```cpp
{{BEFORE_CODE}}
```

#### After
```cpp
{{AFTER_CODE}}
```

---

## Recommendations

### Immediate Actions (Do Before Merge)

1. {{IMMEDIATE_ACTION_1}}
2. {{IMMEDIATE_ACTION_2}}
3. {{IMMEDIATE_ACTION_3}}

### Short-term Actions (This Sprint)

1. {{SHORT_TERM_ACTION_1}}
2. {{SHORT_TERM_ACTION_2}}
3. {{SHORT_TERM_ACTION_3}}

### Long-term Actions (Technical Debt)

1. {{LONG_TERM_ACTION_1}}
2. {{LONG_TERM_ACTION_2}}
3. {{LONG_TERM_ACTION_3}}

---

## Technical Debt Inventory

| ID | Description | File | Line | Effort | Priority |
|----|-------------|------|------|--------|----------|
{{TECHNICAL_DEBT_TABLE}}

---

## Refactoring Opportunities

### {{OPPORTUNITY_TITLE}}

**Current Issues:**
- {{ISSUE_1}}
- {{ISSUE_2}}

**Proposed Refactoring:**
- {{REFACTORING_STEP_1}}
- {{REFACTORING_STEP_2}}

**Expected Benefits:**
- {{BENEFIT_1}}
- {{BENEFIT_2}}

**Estimated Effort:** {{EFFORT}}

---

## Test Coverage

**Current Coverage:** {{COVERAGE_PERCENTAGE}}

**Critical Paths Not Covered:**
- {{UNCOVERED_PATH_1}}
- {{UNCOVERED_PATH_2}}

**Recommended Tests:**
- {{RECOMMENDED_TEST_1}}
- {{RECOMMENDED_TEST_2}}

---

## Performance Impact

**Identified Performance Issues:**
{{PERFORMANCE_ISSUES}}

**Benchmark Results:**
{{BENCHMARK_RESULTS}}

**Optimization Recommendations:**
{{OPTIMIZATION_RECOMMENDATIONS}}

---

## Security Considerations

**Security Issues Found:**
{{SECURITY_ISSUES}}

**Recommendations:**
{{SECURITY_RECOMMENDATIONS}}

---

## Backward Compatibility

**Breaking Changes:**
{{BREAKING_CHANGES}}

**Deprecation Notices:**
{{DEPRECATION_NOTICES}}

---

## Review Checklist

### Code Quality
- [ ] No CRITICAL issues remain
- [ ] HIGH priority issues addressed or documented
- [ ] Code follows project style guide
- [ ] No compiler warnings
- [ ] Static analysis clean

### Architecture & Design
- [ ] Follows four-layer architecture
- [ ] Proper separation of concerns
- [ ] SOLID principles respected
- [ ] Design patterns used appropriately

### Memory & Resources
- [ ] No memory leaks
- [ ] Smart pointers used correctly
- [ ] Resources properly managed
- [ ] No circular references

### Error Handling
- [ ] All return values checked
- [ ] Error paths tested
- [ ] Graceful degradation
- [ ] Proper error logging

### Testing
- [ ] Unit tests added
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Tests pass consistently

### Documentation
- [ ] Code is self-documenting
- [ ] Complex logic explained
- [ ] Public API documented
- [ ] Knowledge base updated

---

## Sign-off

**Reviewed By:** {{REVIEWER_NAME}}
**Review Date:** {{REVIEW_DATE}}
**Approval Status:**
- [ ] Approved - Ready to merge
- [ ] Approved with minor changes
- [ ] Needs changes before approval
- [ ] Rejected - Major issues

**Comments:**
{{REVIEWER_COMMENTS}}

---

## Appendix

### Analysis Methodology

This review was conducted using:
- Automated static analysis
- Manual code review
- ACE Engine architecture validation
- Industry best practices

### Tools Used

- {{TOOL_1}}
- {{TOOL_2}}
- {{TOOL_3}}

### References

- [ACE Engine Architecture Guide](../../docs/architecture/)
- [Component Knowledge Base](../../docs/pattern/)
- [Coding Standards](../../docs/best_practices/)
- [SOLID Principles](references/SOLID.md)
- [Memory Management Guide](references/MEMORY.md)

---

*Report generated by Comprehensive Code Review Skill*
