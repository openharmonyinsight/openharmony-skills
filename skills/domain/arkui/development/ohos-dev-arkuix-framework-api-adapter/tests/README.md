# Evaluation Test Cases

## Overview

25 evaluation cases across 5 categories that validate the `ohos-dev-arkuix-framework-api-adapter` skill works correctly.

| Category | Cases | Type | File |
|----------|-------|------|------|
| A: Script Functional | 10 | Automated (Python) | `test_scripts.py` |
| B: Decision Trees | 8 | Scenario-based (manual) | `test_decision_trees.md` |
| C: Constraint Enforcement | 4 | Scenario-based (manual) | `test_constraints.md` |
| D: NEVER List | 3 | Scenario-based (manual) | `test_never_and_triggers.md` |
| E: Skill Triggering | 2 | Scenario-based (manual) | `test_never_and_triggers.md` |

## Running Automated Tests

```bash
cd ohos-dev-arkuix-framework-api-adapter
python3 tests/test_scripts.py
```

Tests use `fixtures/` directory containing sample `.d.ts` files and mock C++ module structures.

## Manual Evaluation

Scenario-based test cases (B/C/D/E) are evaluated by:
1. Loading this skill into an AI agent
2. Presenting each test case's input
3. Verifying the agent's output matches expected behavior

Each `.md` file documents: input context, expected decision, and PASS/FAIL criteria.

## Test Fixture Structure

```
fixtures/
├── dts/                            # Sample .d.ts files
│   ├── simple_settings.d.ts        # Partial @crossplatform coverage
│   ├── no_crossplatform.d.ts       # Zero @crossplatform (bluetooth)
│   ├── partial_crossplatform.d.ts  # Mixed coverage (http)
│   └── empty.d.ts                  # Edge case: empty file
└── modules/                        # Mock C++ module structures
    ├── pure_cpp/                   # OHOS Reuse candidate (preferences)
    ├── platform_heavy/             # Independent candidate (bluetooth)
    │   ├── android/                # JNI implementation
    │   └── ios/                    # ObjC++ implementation
    └── hybrid/                     # Hybrid candidate (location)
        ├── common/                 # Shared logic
        ├── android/                # Android adapter
        └── ios/                    # iOS adapter
```
