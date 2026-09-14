# Eval Design

These evals focus on behavior that distinguishes `ohos-dev-security-code-check` from a generic code review or a naive `wc -l`:

- running the actual scan scripts (`scan_cpp_size.py` / `circular_header_check.py`) instead of eyeballing file sizes
- counting **effective lines** (excluding blanks, comments, preprocessor directives) rather than raw line counts
- honoring configurable thresholds (`-f` / `-F`) rather than only the 2000/50 defaults
- detecting **module-level circular dependencies** via include graph traversal, not just file-name guessing
- offering concrete refactoring entry points (via `references/refactoring.md` / `references/circular-deps.md`) after a finding
- **false-positive control**: clean code produces a no-finding conclusion with verified-checklist coverage, not invented findings

## Fixture workspaces

| Fixture | Purpose |
|---------|---------|
| `files/oversized-function/src/session_manager.cpp` | One function (`RefreshAllSessions`) exceeding the default 50-line function threshold; file stays under the 2000-line file threshold |
| `files/circular-deps/module_a/` + `files/circular-deps/module_b/` | Two modules that include each other's header, forming a clean A→B→A cycle |
| `files/clean-code/src/metrics_logger.cpp` | Small, well-structured code that must produce zero findings under default thresholds |

## Grading approach

Each case lists concrete `expectations` a grader can verify by inspecting the Agent's output:

- Did the Agent run / instruct the correct script with correct arguments?
- Did it report the right finding (correct function name, correct cycle)?
- Did it honor the requested threshold or output path?
- Did it avoid false positives (not inventing findings on clean code)?
- Did it offer actionable refactoring entry points rather than generic advice?

The fixtures are intentionally small so a grader can confirm results without running a full OpenHarmony source tree.
