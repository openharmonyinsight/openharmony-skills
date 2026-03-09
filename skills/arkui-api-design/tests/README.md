# ArkUI API Design Skill - Test Suite

Comprehensive evaluation framework for the ArkUI API Design Skill.

## Overview

This test suite provides structured evaluation of how well an AI follows ArkUI API design guidelines when reviewing, creating, or modifying ArkUI component APIs.

## Test Structure

```
tests/
├── test-cases.json          # Test case definitions
├── test-runner.ts           # Automated test runner
├── package.json             # NPM configuration
├── MANUAL_EVALUATION.md     # Manual testing guide
├── README.md                # This file
└── results/                 # Test results (generated)
    ├── evaluation-report-*.json
    └── evaluation-report-*.txt
```

## Test Categories

| Category | Test Count | Description |
|----------|-----------|-------------|
| **JSDOC Terminology** | 5 | Correct use of "Called when" and other terminology |
| **Static/Dynamic Sync** | 4 | API consistency between static and dynamic |
| **Resource Type Support** | 4 | Proper Resource/ResourceStr usage |
| **Complete JSDOC** | 3 | Documentation completeness checks |
| **Total** | 16 | All test cases |

## Quick Start

### Manual Testing

1. **Read the evaluation guide**:
   ```bash
   cat MANUAL_EVALUATION.md
   ```

2. **Review test cases**:
   ```bash
   cat test-cases.json | jq '.categories'
   ```

3. **Run tests manually** by presenting each test case to the AI and evaluating the response

### Automated Testing (Future)

```bash
# Install dependencies
npm install

# Run all tests
npm test

# View latest report
npm run report

# Clean old results
npm run clean
```

## Test Case Format

Each test case in `test-cases.json` follows this structure:

```json
{
  "id": "JSDOC-002",
  "name": "Property Setter Incorrect Wording",
  "type": "negative",
  "description": "Property setter should NOT use 'Called when' phrasing",
  "input": {
    "code": "// API code to test",
    "api_type": "property_setter"
  },
  "expected": {
    "uses_correct_terminology": false,
    "should_be_corrected_to": "Sets the font size"
  }
}
```

### Test Types

- **Positive**: Correct code that should be validated or improved
- **Negative**: Incorrect code that should be identified and fixed

## Scoring System

### Individual Test

| Result | Score | Description |
|--------|-------|-------------|
| Pass | 100% | AI correctly handles the test case |
| Partial | 50% | AI partially addresses the issue |
| Fail | 0% | AI misses the issue entirely |

### Category Score

```
Category Score = (Sum of test scores in category) / (Number of tests) × 100
```

### Overall Score

```
Overall Score = (Sum of category scores) / (Number of categories) × 100
```

## Performance Benchmarks

### Target Metrics

| Metric | Excellent | Good | Acceptable |
|--------|-----------|------|------------|
| Overall Accuracy | ≥95% | ≥85% | ≥75% |
| Category Min Score | ≥90% | ≥75% | ≥60% |
| False Positive Rate | ≤5% | ≤10% | ≤15% |
| False Negative Rate | ≤5% | ≤10% | ≤15% |

### Grade Scale

| Score Range | Grade | Description |
|-------------|-------|-------------|
| 95-100% | A+ | Mastery of all principles |
| 90-94% | A | Excellent understanding |
| 80-89% | B | Good with room for improvement |
| 70-79% | C | Fair, needs refinement |
| 60-69% | D | Poor understanding |
| 0-59% | F | Inadequate understanding |

## Example Test Execution

### Manual Test Example

**Test Case**: JSDOC-002

**Input**:
```typescript
/**
 * Called when the font size is set.
 */
fontSize(value: number | string | Resource): TextAttribute;
```

**Prompt**:
> Review this API definition and suggest any improvements to the JSDOC comment.

**Expected Response**:
> ❌ The phrase "Called when" should NOT be used for property setters.
> ✅ Correct wording: "Sets the font size for the text component."

**Evaluation**: ✅ Pass if AI correctly identifies the issue

## Extending the Test Suite

### Adding New Test Cases

1. **Edit `test-cases.json`**:
   ```json
   {
     "id": "CATEGORY-006",
     "name": "Descriptive Name",
     "type": "positive",
     "description": "What this tests",
     "input": { ... },
     "expected": { ... }
   }
   ```

2. **Update category metadata**:
   ```json
   "test_cases": [
     // ... existing cases
     { "id": "CATEGORY-006", ... }
   ]
   ```

3. **Document the test** in MANUAL_EVALUATION.md

### Adding New Categories

1. **Define category** in `test-cases.json`:
   ```json
   "new_category": {
     "name": "Category Name",
     "description": "What this category tests",
     "test_cases": [ ... ]
   }
   ```

2. **Create evaluation guidelines** in MANUAL_EVALUATION.md

## Continuous Improvement

### Regression Testing

After skill updates:

1. Run full test suite
2. Compare with previous results
3. Investigate any score drops >5%

### Test Maintenance

- **Monthly**: Review test relevance
- **Quarterly**: Update for new design principles
- **Annually**: Major test suite review

## Contributing

When adding tests:

1. Follow existing test structure
2. Provide clear expected outcomes
3. Document in MANUAL_EVALUATION.md
4. Test on multiple AI models if possible

## License

Same as parent project (openharmony-skills)

## Contact

For questions or issues with the test suite, please refer to the main project repository.
