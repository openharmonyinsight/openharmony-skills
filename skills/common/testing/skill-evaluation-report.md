# Skill Evaluation Report

> Evaluation Date: 2026-06-05 (Updated)
> Evaluator: skill-judge (skill-judge skill)
> Revision: Post-fix re-evaluation of both skills

---

# Skill 1: ohos-test-arkts-xts-generation (Post-Fix Re-Evaluation)

## Summary
- **Total Score**: 106/120 (88%)
- **Grade**: B
- **Pattern**: Process (~452 lines, 12-Phase workflow)
- **Knowledge Ratio**: E:A:R = 78:18:4
- **Verdict**: A significantly improved skill — the Phase inline guidance and Thinking Framework transform it from a routing table into a self-contained decision-making resource. Within striking distance of A grade.

## Dimension Scores

| Dimension | Score | Max | Before | Delta | Notes |
|-----------|-------|-----|--------|-------|-------|
| D1: Knowledge Delta | 17 | 20 | 16 | +1 | Thinking Framework adds expert heuristics (API analysis checklist + decision tree + case estimation); Phase inline guidance adds domain knowledge |
| D2: Mindset + Procedures | 14 | 15 | 12 | +2 | API characteristic analysis (8 questions) + decision tree directly addresses thinking framework gap |
| D3: Anti-Pattern Quality | 14 | 15 | 14 | 0 | Unchanged — was already excellent (12 NEVER entries) |
| D4: Specification Compliance | 13 | 15 | 12 | +1 | Description now starts with coherent functional summary + syntax mode mention |
| D5: Progressive Disclosure | 14 | 15 | 13 | +1 | Phase tracking section compressed from 43→17 lines; inline guidance reduces need to load external files |
| D6: Freedom Calibration | 12 | 15 | 12 | 0 | Unchanged — correctly low freedom for fragile operations |
| D7: Pattern Recognition | 9 | 10 | 8 | +1 | Phase inline guidance + thinking framework strengthen the Process pattern |
| D8: Practical Usability | 13 | 15 | 10 | +3 | Phase inline guidance enables initial decisions without loading external files; decision tree is directly actionable |
| **Total** | **106** | **120** | **97** | **+9** | **88% (B)** |

## Critical Issues (Updated)

1. **SKILL.md still depends on external prompt files for detailed execution**: While inline guidance now enables initial decisions, detailed steps (e.g., Phase 2's exact scan commands, Phase 5's code templates) still require loading 400-800 line prompt files. This is by design (progressive disclosure) but means the skill cannot operate fully self-contained.

2. **Key Constraints section has some overlap with Anti-Patterns**: Lines 263-275 (Key Constraints) and lines 277-329 (Anti-Patterns) have overlapping content — e.g., "Strict API adherence" in constraints and "NEVER use undeclared interfaces" in anti-patterns say the same thing. Consider consolidating.

3. **Thinking Framework and Anti-Patterns have no explicit linkage**: The decision tree (line 348-364) references @throws, UI, and resource allocation but doesn't link back to the corresponding NEVER entries. Cross-references would strengthen both sections.

## Top 3 Improvements

1. **Consolidate Key Constraints into Anti-Patterns**: The 11 Key Constraints and 12 Anti-Patterns overlap significantly. Merge into a single section — either expand Anti-Patterns to subsume Constraints, or keep Constraints as a numbered summary and Anti-Patterns as the detailed WHY/WHAT-TO-DO version. This would save ~20 lines and eliminate redundancy.

2. **Add cross-references between Thinking Framework and Anti-Patterns**: In the decision tree, add links like "→ see NEVER 为没有@throws声明的API构造错误码测试" at the @throws branch, and "→ see NEVER 在cleanup步骤中忽略异常" at the resource allocation branch.

3. **Add "Phase 1: Task Config" inline guidance**: Phase 1 is the only phase missing from the inline guidance section. Adding 2-3 lines about ETS version detection and subsystem resolution would complete the coverage.

## Detailed Analysis

### D2: Mindset + Procedures (14/15)

**Before** (12/15): Had excellent multi-Flow decision tree and per-Phase loading, but lacked thinking frameworks.

**After**: The new `Thinking Framework: Before You Generate` section (lines 331-374) provides:

1. **API Characteristic Analysis** (lines 337-346): 8-question checklist with "为什么重要" (why it matters) and "影响生成策略" (impact on strategy). This is expert-level thinking — questions like "Does this API have side effects?" and "Does it depend on system state?" are not obvious to Claude.

2. **Test Design Decision Tree** (lines 348-364): A structured if-then-else tree that routes from @throws → UI → resource allocation. This is exactly the kind of non-obvious branching logic that takes experience to develop.

3. **Case Count Estimation** (lines 367-374): 5-category heuristic with recommended case counts. "Simple get/set: 3-5 cases" vs "System capability API: 8-12 cases" is expert judgment Claude couldn't derive.

**Remaining gap**: The thinking framework focuses on API analysis but doesn't cover test design quality (e.g., "Is this test case testing the right thing?" or "Does this assertion verify the actual contract?"). A "After You Generate" quality checklist would bring this to 15/15.

### D4: Specification Compliance (13/15)

**Before** (12/15): Description was a keyword dump.

**After** (lines 3-17):
```yaml
description: >
  OpenHarmony ArkTS XTS测试用例生成器。解析.d.ts API定义，生成符合Hypium框架的测试用例，
  支持覆盖率分析、编译验证和Demo+UiTest生成。
  支持ArkTS-Dyn（动态）和ArkTS-Sta（静态）两种语法模式，覆盖12-Phase完整工作流。
  Use when: (1)...(8)
  Trigger keywords: ...
```

**Improvement**: The first two lines now answer WHAT comprehensively — including Demo+UiTest and both syntax modes. Previously these were only mentioned deep in the body.

**Remaining gap**: The Use when/Trigger keywords section is still a flat enumeration. Could be condensed slightly (e.g., merge items 6 and 7) for better readability.

### D5: Progressive Disclosure (14/15)

**Before** (13/15): Good layering but Phase tracking was 43 lines of bash examples + JSON.

**After**:
- Phase tracking compressed from 43 → 17 lines (removed 7 bash examples → 2 core commands; removed 13-line JSON example → 1-line `--help` reference)
- Phase inline guidance added (lines 180-238, ~59 lines) — eliminates need to load external prompt files for initial decisions
- Net change: 452 total lines (was 373), but +79 lines of high-value content vs -26 lines of redundant content

**Improvement**: The skill now has three functional layers within SKILL.md itself:
1. **Routing table** (lines 140-155) — which file to load for each Phase
2. **Inline guidance** (lines 180-238) — what each Phase does without loading files
3. **Thinking framework** (lines 331-374) — how to think about the problem

This means an Agent can make meaningful progress on Phases 2-10 without loading any external files — a significant improvement from the previous version where SKILL.md was purely a routing table.

### D8: Practical Usability (13/15)

**Before** (10/15): Good decision tables but phases just routed to prompt files.

**After** (+3): Three major improvements:

1. **Phase inline guidance** (lines 180-238): Each Phase now has 2-5 bullet points covering core goal, Flow-specific behavior, key output, and constraints. Agent can:
   - Know what Phase 2 does without loading the 200-line prompt
   - Understand Flow A/B/C differences inline (already in the table, now reinforced)
   - Identify key outputs (e.g., `.coverage_data/uncovered_apis.json`)

2. **Thinking Framework decision tree** (lines 348-364): Directly actionable — Agent can follow the tree to determine test type (ERROR/UI/standard), cleanup requirements, and parallel execution eligibility.

3. **Case count estimation** (lines 367-374): Prevents under-testing (1 case for system API) or over-testing (20 cases for simple getter). Expert heuristic that improves output quality.

**Remaining gap**: No inline troubleshooting for individual Phases. If Phase 2 scan fails, Agent must load `references/error_handling.md`. Adding 1-line "common issue" per Phase would address this.

---

# Skill 2: ohos-test-capi-xts-generation (Post-Fix Re-Evaluation)

## Summary
- **Total Score**: 99/120 (83%)
- **Grade**: B
- **Pattern**: Tool (~401 lines, 8-Phase workflow with N-API-specific tooling)
- **Knowledge Ratio**: E:A:R = 70:25:5
- **Verdict**: A strong CAPI test generator with excellent N-API triple verification and well-structured anti-patterns. Fixing the 3 critical issues raised the grade from C (71%) to B (83%). Remaining gaps are in inline troubleshooting and thinking frameworks.

## Dimension Scores

| Dimension | Score | Max | Before | Delta | Notes |
|-----------|-------|-----|--------|-------|-------|
| D1: Knowledge Delta | 15 | 20 | 13 | +2 | Anti-Patterns section adds expert-grade knowledge; README.md removal eliminated redundant content |
| D2: Mindset + Procedures | 11 | 15 | 11 | 0 | Triple verification remains excellent; still lacks thinking frameworks |
| D3: Anti-Pattern Quality | 14 | 15 | 10 | +4 | 9 explicit NEVER entries with 原因/正确做法/后果 — now matches ArkTS quality |
| D4: Specification Compliance | 14 | 15 | 10 | +4 | Bilingual description with 6 trigger scenarios and 18 CN/EN keywords |
| D5: Progressive Disclosure | 14 | 15 | 12 | +2 | README.md (505 lines) and skill_config.json (807 lines) deleted; clean package |
| D6: Freedom Calibration | 12 | 15 | 11 | +1 | Anti-patterns reinforce low-freedom constraints for fragile N-API operations |
| D7: Pattern Recognition | 8 | 10 | 8 | 0 | Clear Tool pattern unchanged |
| D8: Practical Usability | 11 | 15 | 10 | +1 | Anti-patterns add actionable guidance; still relies on external modules for phase details |

## Critical Issues (Updated)

1. **No inline troubleshooting / Common Failure Patterns section**: Unlike the ArkTS skill which has a detailed "Common Failure Patterns" section with symptom → root cause → fix for 6 failure modes, this skill lacks equivalent inline guidance.

2. **Phases 2-3 provide no summary guidance**: SKILL.md routes to 400-600 line external modules without any inline summary. The ArkTS skill now has inline guidance — this skill should follow the same pattern.

3. **No Thinking Framework**: The ArkTS skill now has a comprehensive API analysis checklist + decision tree. This skill lacks equivalent guidance for CAPI-specific decisions (e.g., "Does this C function return an error code?" → "Is this function async via callback?" → "Does it allocate memory?").

## Top 3 Improvements

1. **Add Common Failure Patterns section**: Following the ArkTS skill's pattern (6 entries with symptom/root cause/fix), add CAPI-specific failure patterns.

2. **Add Phase inline guidance**: Follow the ArkTS skill's `### Phase 内联指导` pattern — 2-3 bullet points per Phase for initial decision-making.

3. **Add Thinking Framework for CAPI**: Adapt the ArkTS thinking framework for CAPI-specific concerns (N-API type mapping, memory management, handle lifecycle).

---

# Comparative Summary

| Metric | ArkTS Skill (After) | CAPI Skill (After) |
|--------|---------------------|---------------------|
| Total Score | **106/120 (88%)** | **99/120 (83%)** |
| Grade | **B** | **B** |
| SKILL.md Lines | 452 | 401 |
| Total Files (non-eval) | 101 | 92 |
| Anti-Patterns (NEVER) | 12 explicit entries | 9 explicit entries |
| Phase Inline Guidance | Yes (8 phases, ~59 lines) | No |
| Thinking Framework | Yes (8 questions + decision tree + estimation) | No |
| Common Failure Patterns | Yes (6 entries) | No |
| Loading Triggers | Good (embedded in workflow) | Excellent (MANDATORY/Do NOT Load) |
| Bilingual Description | Yes (CN + EN) | Yes (CN + EN) |
| Redundant Files | None | None |
| Key Strength | Thinking framework + Phase guidance | Anti-patterns + triple verification |
| Key Weakness | Key Constraints/Anti-Patterns overlap | No inline guidance, no thinking framework |

## Change Impact Summary

### ArkTS Skill

| Fix | Dimensions Affected | Score Impact |
|-----|---------------------|-------------|
| Description functional summary | D4 (+1) | +1 |
| Phase inline guidance (8 phases) | D8 (+3), D5 (+1), D7 (+1) | +5 |
| Thinking Framework (API analysis + decision tree) | D2 (+2), D1 (+1) | +3 |
| Phase tracking compression | D5 (net +0, part of overall improvement) | 0 |
| **Total** | | **+9** |

Score progression: 97 → **106** (+9 points, +7 percentage points, Grade B 81% → 88%)

### CAPI Skill

| Fix | Dimensions Affected | Score Impact |
|-----|---------------------|-------------|
| Description bilingual rewrite | D4 (+4), D1 (+1) | +5 |
| Anti-Patterns section added | D3 (+4), D1 (+1), D6 (+1), D8 (+1) | +7 |
| README.md + skill_config.json deleted | D5 (+2), D1 (+1) | +3 |
| **Total** | | **+15** |

Score progression: 85 → **99** (+14 points, +12 percentage points, Grade C → B)
