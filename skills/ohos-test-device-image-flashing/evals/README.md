# Evaluation Guide

Run the cases in `evals.json` with the Skill enabled and verify every listed expectation.

The cases cover:

- Daily build download behavior and fixed master-branch scope.
- Safe updater-mode flashing with fail-fast `hdc` handling.
- Tool-neutral SSH execution.
- The boundary between partial library push and full image flashing.
