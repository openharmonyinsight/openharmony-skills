# ArkUI API Design Skill - Manual Evaluation Guide

## Overview

This guide provides instructions for manually evaluating the ArkUI API Design Skill against the test cases defined in `test-cases.json`.

## Test Categories

### 1. JSDOC Terminology Tests (JSDOC-001 to JSDOC-005)

**Objective**: Verify that the skill correctly uses "Called when" only for event callbacks and lifecycle methods.

#### Manual Test Procedure:

For each test case:

1. **Present the input to the AI**: Use the code snippet from `test-cases.json`
2. **Ask the AI**: "Review this API definition and suggest any improvements"
3. **Evaluate the response**:
   - For **positive** tests: AI should recognize the code as correct or suggest valid improvements
   - For **negative** tests: AI should identify the "Called when" misuse and suggest correct wording

#### Scoring Criteria:

- ✅ **Pass (100%)**: AI correctly identifies the issue or validates the correct usage
- ⚠️ **Partial (50%)**: AI mentions the issue but doesn't provide correct solution
- ❌ **Fail (0%)**: AI misses the issue or validates incorrect usage

#### Example Evaluation:

**Test JSDOC-002** (Negative case):
```
Input:
/**
 * Called when the font size is set.
 */
fontSize(value: number | string | Resource): TextAttribute;
```

**Expected AI Response**:
> ❌ "Called when" should NOT be used for property setters.
> ✅ Correct wording: "Sets the font size for the text component."

**Score**: Pass if AI identifies the issue and suggests correct wording.

---

### 2. Static/Dynamic API Synchronization Tests (SYNC-001 to SYNC-004)

**Objective**: Ensure the skill enforces consistency between static and dynamic APIs.

#### Manual Test Procedure:

1. **Present both APIs** to the AI
2. **Ask**: "Check if these static and dynamic APIs are properly synchronized"
3. **Evaluate**: Does AI identify mismatches in types, version tags, etc.?

#### Scoring Criteria:

- ✅ **Pass**: AI identifies all synchronization issues
- ⚠️ **Partial**: AI identifies some issues but misses others
- ❌ **Fail**: AI misses all issues

---

### 3. Resource Type Support Tests (RESOURCE-001 to RESOURCE-004)

**Objective**: Verify correct usage of Resource vs ResourceStr based on API version.

#### Manual Test Procedure:

1. **Present the API code** with version information
2. **Ask**: "Is this Resource/ResourceStr type usage correct for the given API version?"
3. **Evaluate**: Check against the rules:
   - API 12 and earlier: Use `string | Resource`
   - API 13+ (new properties): Use `ResourceStr`
   - API 12 should NOT be modified to use ResourceStr

#### Scoring Criteria:

- ✅ **Pass**: Correctly validates the type usage
- ⚠️ **Partial**: Identifies version but misses type rule
- ❌ **Fail**: Incorrect validation

---

### 4. Complete JSDOC Documentation Tests (JSDOC-COMP-001 to JSDOC-COMP-003)

**Objective**: Ensure AI checks for complete JSDOC documentation.

#### Manual Test Procedure:

1. **Present the API code** with JSDOC
2. **Ask**: "Review the JSDOC documentation for completeness"
3. **Evaluate**: Does AI identify missing tags (@unit, @since, @syscap, @param)?

#### Scoring Criteria:

- ✅ **Pass**: Identifies all missing required tags
- ⚠️ **Partial**: Identifies some missing tags
- ❌ **Fail**: Misses incomplete documentation

---

## Running Manual Evaluation

### Step 1: Prepare Test Prompts

Create a prompt for each test case:

```markdown
# Test Case: JSDOC-002

## Input Code:
\`\`\`typescript
/**
 * Called when the font size is set.
 */
fontSize(value: number | string | Resource): TextAttribute;
\`\`\`

## Question:
Review this API definition and suggest any improvements to the JSDOC comment.

## Expected Behavior:
The AI should identify that "Called when" is incorrectly used for a property setter
and suggest using "Sets the" or similar action verb instead.
```

### Step 2: Execute Test

1. Open Claude Code or your AI assistant
2. Paste the test prompt
3. Record the AI's response
4. Evaluate against expected behavior
5. Assign score (Pass/Partial/Fail)

### Step 3: Record Results

Create a results file:

```json
{
  "test_id": "JSDOC-002",
  "timestamp": "2025-03-07T10:30:00Z",
  "ai_response": "...",
  "evaluated_score": "pass",
  "notes": "AI correctly identified the issue and suggested 'Sets the font size' as replacement"
}
```

---

## Automated Evaluation (Future)

To automate these tests, you would:

1. **Integrate with Claude API**: Use Anthropic's Messages API
2. **Parse responses**: Extract key information from AI responses
3. **Compare against expected**: Use semantic similarity or exact matching
4. **Generate reports**: Automatic score calculation and reporting

Example integration:

```typescript
async function runAutomatedTest(testCase: TestCase): Promise<TestResult> {
  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-5-20250929",
    messages: [{
      role: "user",
      content: generateTestPrompt(testCase)
    }]
  });

  return evaluateResponse(response.content, testCase.expected);
}
```

---

## Benchmark Metrics

### Primary Metrics

1. **Accuracy**: Percentage of tests passed
2. **Consistency**: Repeatable results across multiple runs
3. **Coverage**: Percentage of design principles tested

### Secondary Metrics

1. **Response Quality**: Clarity and helpfulness of suggestions
2. **False Positive Rate**: Incorrect flagging of correct code
3. **False Negative Rate**: Missing actual issues

### Performance Targets

| Metric | Target | Acceptable |
|--------|--------|------------|
| Overall Accuracy | ≥95% | ≥85% |
| Category Accuracy | ≥90% | ≥75% |
| False Positive Rate | ≤5% | ≤10% |
| False Negative Rate | ≤5% | ≤10% |

---

## Continuous Improvement

### Updating Test Cases

As the skill evolves, update test cases to:

1. **Add new design principles** as they're added to the skill
2. **Refine existing tests** based on real-world usage
3. **Remove deprecated tests** for outdated practices

### Regression Testing

After skill updates:

1. **Run full test suite** to catch regressions
2. **Compare scores** with previous benchmarks
3. **Investigate drops** in accuracy

---

## Example: Complete Evaluation Session

```bash
# 1. Install dependencies
cd tests/
npm install

# 2. Run automated tests (when implemented)
npm test

# 3. View results
cat results/evaluation-report-*.txt

# 4. For manual testing, iterate through test cases
# - Open test-cases.json
# - For each test case, create prompt
# - Get AI response
# - Evaluate and record results
```

---

## Troubleshooting

### Test Fails Unexpectedly

1. **Check test case**: Is the expected outcome correct?
2. **Verify skill version**: Are you testing the latest skill version?
3. **Review prompt**: Is the test prompt clear and unambiguous?

### Inconsistent Results

1. **Test again**: Run the same test multiple times
2. **Check temperature**: If using API, lower temperature for consistency
3. **Review context**: Ensure no prior context influences the test

### Poor Overall Score

1. **Identify weak categories**: Which categories score lowest?
2. **Update skill**: Enhance skill documentation for weak areas
3. **Add more tests**: Create targeted tests for specific issues
