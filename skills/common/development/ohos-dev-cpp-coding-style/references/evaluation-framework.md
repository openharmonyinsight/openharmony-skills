# OpenHarmony C++ Skill Evaluation Framework

Load this file when the task is to benchmark, validate, or iterate on the `ohos-dev-cpp-coding-style` skill itself.

## Goal

Measure whether the skill reliably changes OpenHarmony-specific behavior compared with a baseline, not whether the model can produce acceptable generic C++.

## Evaluation Scope

Cover at least these task families:

- implementation of new production code
- scaffold generation for new `.h/.cpp` files
- public API comment repair
- review findings against OpenHarmony conventions

Use the prompts in [`../evals/evals.json`](../evals/evals.json) as the default seed set.

## Workspace Layout

Create a sibling workspace named `ohos-dev-cpp-coding-style-workspace/`.

Within that workspace, organize iterations as:

```text
ohos-dev-cpp-coding-style-workspace/
  iteration-1/
    eval-0-implementation-with-ownership-style/
      eval_metadata.json
      with_skill/
        outputs/
        timing.json
        grading.json
      old_skill/
        outputs/
        timing.json
        grading.json
```

If this is a brand new baseline run outside an improvement loop, replace `old_skill/` with `without_skill/`.

## Assertions

Prefer assertions that verify OpenHarmony-specific deltas. Good assertions usually check one of these:

- `.h/.cpp` and `snake_case` file naming decisions
- include guards instead of `#pragma once`
- class member naming with trailing underscores
- meaningful public API comments rather than template boilerplate
- avoided macros, templates, or default captures
- deleted copy or move operations where class semantics require them
- non-owning interfaces expressed with raw pointers or references
- review outputs that mention decisive convention violations with file and line references

Avoid assertions that only test generic C++ correctness unless the OpenHarmony rule depends on it.

## Grading Guidance

For each run:

1. Read `eval_metadata.json` and the generated outputs.
2. Grade assertions into `grading.json` using the exact `text`, `passed`, and `evidence` fields.
3. Call out false positives in `eval_feedback` when an assertion passes for reasons unrelated to OpenHarmony conventions.

## Benchmark Reading

When analyzing benchmark results, look for:

- assertions that pass equally with and without the skill
- prompts where the skill improves convention adherence but causes unnecessary verbosity
- prompts where the skill over-applies OpenHarmony rules to third-party or upstream-style code
- regressions where the skill gives generic C++ advice instead of OpenHarmony-specific guidance

The skill is doing its job when it changes concrete file layout, naming, ownership, review framing, and evaluation structure decisions in the OpenHarmony direction.
