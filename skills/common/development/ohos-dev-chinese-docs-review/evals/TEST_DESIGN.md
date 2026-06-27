# Test Design for ohos-dev-chinese-docs-review

## Overview

This document describes the design philosophy and implementation of evaluation test cases for the `ohos-dev-chinese-docs-review` skill, following [Agent Skills evaluation best practices](https://agentskills.io/skill-creation/evaluating-skills).

## Design Philosophy

### What Makes This Skill Valuable?

The `ohos-dev-chinese-docs-review` skill addresses a critical problem: ensuring OpenHarmony API documentation quality through automated checks and expert-guided manual review. Without this skill, agents would:

1. Miss domain-specific rules (OpenHarmony doc structure, template compliance)
2. Waste time on redundant manual checks that scripts can handle
3. Fail to focus manual review on semantic quality issues
4. Not know how to resolve paths in workspace/submodule contexts
5. Miss implementation-doc mismatches

Our test cases validate that the skill solves these problems effectively.

## Test Case Categories

### Category 1: Core Functionality (Tests 1-5)

These tests validate the skill's primary value propositions.

#### Test 1: Basic Doc Consistency Check
**What it tests**: Script execution, output format, issue-only reporting

**Why it matters**: The skill should correctly use `check_api_doc_consistency.py` and not duplicate its work in manual review. The output must follow the structured format.

**Skill value**: Automation of repetitive checks (@systemapi placement, @syscap/@permission fields) with structured reporting.

#### Test 2: Path Auto-Discovery
**What it tests**: Workspace root discovery, path resolution from submodules

**Why it matters**: Users are often in submodule directories. The skill should automatically find the workspace root without asking.

**Skill value**: Reduces user friction, handles OpenHarmony's multi-repo structure.

#### Test 3: Error Code Document Check
**What it tests**: Error code template compliance, coverage verification

**Why it matters**: Error code documentation is critical for API usability but often incomplete.

**Skill value**: Ensures error codes are properly documented with required blocks and coverage.

#### Test 4: Template Compliance Check
**What it tests**: Template selection, structural vs semantic compliance

**Why it matters**: Documentation must follow templates, but superficial compliance (markers without substance) is a real problem.

**Skill value**: Validates both template structure and semantic completeness.

#### Test 5: Manual Review Focus
**What it tests**: Script-first workflow, manual review on non-automatable aspects

**Why it matters**: Manual review time is expensive. The skill should focus it on prose quality, example usefulness, and semantic gaps.

**Skill value**: Optimizes human effort by distinguishing automatable vs manual checks.

### Category 2: Edge Cases (Tests 6-7)

These tests validate robustness in exceptional situations.

#### Test 6: Repository-Root Path Interpretation
**What it tests**: `/docs/` and `/interface/` path semantics

**Why it matters**: Users provide paths assuming repository root. Incorrect interpretation leads to "file not found" errors.

**Skill value**: Correctly handles user intent in path specification.

#### Test 7: Missing Files Handling
**What it tests**: Graceful degradation when d.ts or docs are unavailable

**Why it matters**: Documentation often exists before interface definitions, or vice versa. The skill should still provide value with partial inputs.

**Skill value**: Provides useful output even with incomplete information.

### Category 3: Output Quality (Tests 8-10)

These tests validate the quality and format of skill outputs.

#### Test 8: Output Format Compliance
**What it tests**: Markdown structure, field presence, line references

**Why it matters**: Reports must be actionable. Missing Location or Suggestion fields reduce utility.

**Skill value**: Consistent, actionable report format.

#### Test 9: Edge Case - Partial Inputs
**What it tests**: Working with only public docs (no system/error docs)

**Why it matters**: Documentation is often written incrementally. The skill should check what's available and explicitly state what's not.

**Skill value**: Clear communication of checked vs unchecked scope.

#### Test 10: Implementation Alignment Check
**What it tests**: Cross-referencing docs against actual code

**Why it matters**: Documentation often drifts from implementation. The skill should identify missing features, changed behaviors, or undocumented constraints.

**Skill value**: Detects doc-code divergence that impacts users.

## Assertion Design

### Principles

1. **Concrete and verifiable**: Each assertion can be PASS/FAIL based on observable evidence
2. **Not too easy**: Doesn't always pass without the skill
3. **Not too hard**: Doesn't always fail even with good output
4. **Specific**: Targets a specific skill behavior

### Examples

**Good assertion**:
- "Report contains structured findings with Location, Issue, Suggestion fields"
  - Concrete: Can verify by parsing output
- "Manual review focuses on prose clarity, NOT script-covered checks"
  - Specific: Distinguishes skill value from baseline

**Weak assertion** (avoided):
- "The output is good" - Too vague
- "The report uses exactly word X" - Too brittle

## Test Input Design

### Realistic Context

Test inputs simulate real OpenHarmony documentation:

- **d.ts files**: Use OpenHarmony JSDoc tag conventions (@systemapi, @permission, @syscap)
- **Markdown docs**: Follow OpenHarmony doc structure (概述, 权限, 系统能力, 参数, 返回值, 错误码)
- **C++ implementation**: Simulates real code with implementation details not documented

### Intentional Issues

Test files contain intentional problems for the skill to find:

1. **example.md**: @systemapi function in public doc (wrong placement)
2. **feature.d.ts vs feature.md**: Additional error codes (500) and attributes (timeout, priority) not documented
3. **feature_impl.cpp**: Implementation behaviors not documented (negative priority, persist mapping)
4. **component.md**: Missing required sections from ArkTS component template
5. **partial.md**: Missing system API and error code docs

## Expected Skill Impact

### Baseline (Without Skill)

Without this skill, an agent would likely:

- ❌ Not know about OpenHarmony-specific doc structure
- ❌ Not use the consistency script
- ❌ Waste time checking fields the script covers
- ❌ Miss template-specific requirements
- ❌ Not know how to find workspace root
- ❌ Fail to distinguish automated vs manual checks
- ❌ Not cross-reference implementation against docs

### With Skill

With this skill, the agent should:

- ✅ Use the script for automatable checks
- ✅ Focus manual review on semantic quality
- ✅ Correctly resolve paths from any directory
- ✅ Verify template compliance deeply (not just superficially)
- ✅ Handle partial inputs gracefully
- ✅ Identify implementation-doc mismatches
- ✅ Produce structured, actionable reports

## Running the Evaluation

### Quick Start

```bash
cd /home/hh/openharmony-skills/skills/ohos-dev-chinese-docs-review/evals

# 1. Setup workspace
./run-evals.sh 1 setup

# 2. List all test cases
./run-evals.sh 1 list

# 3. Run a test case (shows instructions)
./run-evals.sh 1 run 1 with_skill

# 4. Grade results
./run-evals.sh 1 grade 1
```

### Expected Pass Rates

Based on the design:

| Scenario | Expected Pass Rate |
|----------|-------------------|
| **With skill** | 80-90% (8-9/10 assertions pass) |
| **Without skill** | 30-40% (3-4/10 assertions pass) |
| **Delta** | +40-50 percentage points |

### Cost Analysis

The skill adds value by:

- **More tokens**: Scripts + template reading adds context cost
- **More time**: Loading references adds processing time
- **Better quality**: Significantly higher pass rate justifies cost

Target: Pass rate improvement >50% with <30% token increase

## Iteration Strategy

### First Iteration

1. Run all 10 test cases with and without skill
2. Grade assertions manually
3. Identify patterns (what passes with skill, fails without)
4. Update SKILL.md based on findings

### Subsequent Iterations

1. Focus on failing assertions
2. Tighten instructions for inconsistent results
3. Remove assertions that always pass (no discrimination value)
4. Add test cases for new scenarios discovered

## Success Criteria

The skill evaluation succeeds when:

1. **Pass rate delta** >40% (skill significantly improves results)
2. **Cost ratio** <1.5x (skill doesn't dramatically increase token usage)
3. **Human review** finds no major quality issues in outputs
4. **Edge cases** handled gracefully (no crashes on missing files, bad paths)

## References

- [Agent Skills Evaluation Guide](https://agentskills.io/skill-creation/evaluating-skills)
- [Skill Creation Best Practices](https://agentskills.io/skill-creation/best-practices)
- [OpenHarmony Documentation Templates](https://gitcode.com/openharmony/docs/blob/master/zh-cn/contribute/template/)

## Contributing

When adding new test cases:

1. Identify a gap in current coverage
2. Draft test case following the 3-part structure (prompt, expected_output, files)
3. Write concrete assertions
4. Create realistic input files
5. Update this TEST_DESIGN.md
6. Run with and without skill to verify discrimination value

---

Last updated: 2025-06-11
Maintainer: OpenHarmony Skills Team
