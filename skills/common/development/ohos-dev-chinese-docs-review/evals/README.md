# Evaluation Test Cases for ohos-dev-chinese-docs-review

This directory contains evaluation test cases for the `ohos-dev-chinese-docs-review` skill, following the [Agent Skills evaluation methodology](https://agentskills.io/skill-creation/evaluating-skills).

## Structure

```
evals/
├── README.md              # This file
├── evals.json             # Test case definitions
└── files/                 # Test input files
    ├── docs/              # Sample documentation files
    ├── interface/         # Sample d.ts files
    └── workspace_root/    # Workspace for path discovery tests
```

## Test Cases Overview

| ID | Name | Focus |
|----|------|-------|
| 1 | basic-doc-consistency-check | Script execution and output structure |
| 2 | path-auto-discovery | Workspace root discovery and path resolution |
| 3 | error-code-document-check | Error code template compliance and coverage |
| 4 | template-compliance-check | ArkTS component template verification |
| 5 | manual-review-focus | Distinguishing automated vs manual checks |
| 6 | repository-root-path-interpretation | `/docs/` and `/interface/` path semantics |
| 7 | missing-files-handling | Graceful handling of incomplete inputs |
| 8 | output-format-compliance | Report structure and field requirements |
| 9 | edge-case-partial-inputs | Partial availability of documentation |
| 10 | implementation-alignment-check | Cross-checking docs against code |

## Running Evaluations

### Method 1: Using Subagents (Recommended)

For each test case, run two evaluations:

```bash
# With skill
Agent task:
  - Skill path: /path/to/ohos-dev-chinese-docs-review
  - Task: [copy prompt from evals.json]
  - Input files: [copy files from evals.json]
  - Save outputs to: workspace/iteration-1/eval-{name}/with_skill/outputs/

# Without skill (baseline)
Agent task:
  - Task: [same prompt]
  - Input files: [same files]
  - Save outputs to: workspace/iteration-1/eval-{name}/without_skill/outputs/
```

### Method 2: Using Claude Code Directly

Create a workspace directory and run each test case:

```
docs-check-workspace/
└── iteration-1/
    ├── eval-basic-doc-consistency/
    │   ├── with_skill/
    │   │   ├── outputs/
    │   │   ├── timing.json
    │   │   └── grading.json
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    └── (repeat for other test cases)
```

## Grading

After each run, grade the assertions:

```json
{
  "assertion_results": [
    {
      "text": "The script check_api_doc_consistency.py is executed with correct parameters",
      "passed": true,
      "evidence": "Script was called with --api, --public-doc, --readme-doc, and template arguments"
    }
  ],
  "summary": {
    "passed": 8,
    "failed": 2,
    "total": 10,
    "pass_rate": 0.8
  }
}
```

## Benchmark Aggregation

After grading all test cases, create `benchmark.json`:

```json
{
  "run_summary": {
    "with_skill": {
      "pass_rate": { "mean": 0.85, "stddev": 0.08 },
      "time_seconds": { "mean": 42.0, "stddev": 10.0 },
      "tokens": { "mean": 3200, "stddev": 350 }
    },
    "without_skill": {
      "pass_rate": { "mean": 0.40, "stddev": 0.12 },
      "time_seconds": { "mean": 28.0, "stddev": 6.0 },
      "tokens": { "mean": 1800, "stddev": 200 }
    },
    "delta": {
      "pass_rate": 0.45,
      "time_seconds": 14.0,
      "tokens": 1400
    }
  }
}
```

## Iteration Process

1. Run all test cases with and without skill
2. Grade assertions for each run
3. Aggregate results into benchmark.json
4. Review outputs manually, record specific feedback
5. Identify patterns: what passes with skill but fails without?
6. Update SKILL.md based on findings
7. Repeat in iteration-2/

## Test Design Principles

Following [Agent Skills best practices](https://agentskills.io/skill-creation/evaluating-skills):

1. **Vary the prompts** - Mix casual ("check this") with formal ("verify compliance")
2. **Cover edge cases** - Missing files, partial inputs, ambiguous paths
3. **Use realistic context** - Actual OpenHarmony documentation structure
4. **Focus on skill value** - What does the skill add over baseline?

## Key Assertions by Test Case

- **Tests 1-5**: Core functionality - script usage, path discovery, template checks
- **Tests 6-7**: Edge cases - path interpretation, missing files
- **Tests 8-10**: Output quality - format compliance, partial inputs, implementation alignment

## Resources

- [Agent Skills Evaluation Guide](https://agentskills.io/skill-creation/evaluating-skills)
- [Skill Creation Best Practices](https://agentskills.io/skill-creation/best-practices)
- [Optimizing Skill Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)

## Contributing

When adding new test cases:

1. Start with 2-3 cases, expand after seeing results
2. Ensure each case tests a specific aspect of the skill
3. Include concrete assertions that can be verified
4. Provide realistic input files when needed
5. Document expected outcomes clearly

## Feedback

To improve these test cases, review:

- Assertion quality (too easy/hard/unverifiable?)
- Prompt realism (would users actually say this?)
- Input file relevance (are they representative?)
- Expected output clarity (can success be recognized?)
