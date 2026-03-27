---
name: oh-precommit-codecheck
description: |
  Run local code quality checks covering a subset of OpenHarmony gate CI
  (copyright, CodeArts C/C++) plus additional local checks (pylint/flake8,
  shellcheck/bashate, gn format). Use before committing to reduce gate failures.
  Triggers on: /oh-precommit-codecheck, "门禁检查", "门禁预检", "检查代码",
  "run codecheck", "check code quality", "lint my code", "代码检查",
  or after completing code implementation.
  WHEN to use: before git commit, before creating PR, after modifying C/C++/Python/Shell/GN files,
  when gate CI fails with codecheck defects, or when you want to preview what gate will flag.
argument-hint: "[--fix] [<commit>] [<file> ...]"
---

# OH Precommit Codecheck

Run local code quality checks. Includes gate CI checks and additional local-only checks.

**Gate CI checks** (same as OpenHarmony gate):
- **Copyright**: Header presence, year correctness, comment style (`/**` for C/C++)
- **C/C++ format**: clang-format (clang-format-14 preferred, fallback to clang-format)
- **C/C++ quality**: CodeArts Check (codecheck-ide-engine + Huawei clang-tidy: clangtidy + secfinder + fixbot)

**Additional local checks** (NOT part of gate CI, for extra quality):
- **Python**: pylint + flake8
- **Shell**: shellcheck + bashate-mod-ds
- **GN**: `gn format --dry-run`

## Notes

- First run downloads ~600MB of CodeArts tools to `~/.codecheck-tools/`
- Python/Shell linters must be pre-installed (`pylint`, `flake8`, `shellcheck`, `bashate-mod-ds`)
- C/C++ checks without `compile_commands.json` may miss some context-dependent issues
- GN format check requires `gn` in PATH

## Current limitations

This skill covers a **subset** of the full OpenHarmony gate CI checks:

- **Languages**: Only C/C++, Python, Shell, GN are checked. Java, JavaScript, TypeScript, ArkTS are NOT yet wired up (the CodeArts engine has rules for them locally).
- **C++ rules**: ~114 of ~163 gate G.* rules are covered (~70%). Missing rules are mainly C-language variants without `-CPP` suffix.
- **Not covered at all**: WordsTool sensitive-word checks (~200+ rules), OAT open-source compliance (~10 rules), security-specific checks (weak crypto, unsafe IPSI), code metrics (oversized functions/files/complexity, redundant/duplicate code).
- Local pass does NOT guarantee gate pass — this is a best-effort pre-filter.

## Quick Reference

| Invocation | Mode | Behavior |
|-----------|------|----------|
| `/oh-precommit-codecheck` (standalone) | Mode 1 | Check specified files, report results, ask before fixing |
| `/oh-precommit-codecheck --fix` | Mode 1 | Check and auto-fix up to 3 rounds |
| Auto-triggered by oh-pr-workflow | Mode 2 | Silent check + auto-fix, report only if defects remain |
| Pre-commit hook | Mode 2 | Same as auto-trigger |

## Determine trigger mode

Check whether `$ARGUMENTS` is set.

### Mode 1: User-invoked (`$ARGUMENTS` present or `/oh-precommit-codecheck` called)

Parse `$ARGUMENTS` to determine file scope and fix mode:

```
/oh-precommit-codecheck              → files from: git diff --cached --name-only
/oh-precommit-codecheck <commit>     → files from: git diff-tree --no-commit-id -r <commit> --name-only
/oh-precommit-codecheck <file ...>   → the listed files directly
/oh-precommit-codecheck --fix        → same file resolution + auto-fix mode
```

**Argument parsing rules:**
- `--fix` flag can appear anywhere in arguments
- If an argument looks like a git commit (matches `git rev-parse --verify <arg>`), treat it as a commit
- Otherwise treat arguments as file paths

**Steps:**

1. Resolve the file list using the rules above. Filter to only existing files.
2. Run checks by calling the check script:
   ```bash
   bash ~/.claude/skills/oh-precommit-codecheck/scripts/check.sh <file1> <file2> ...
   ```
3. Present results to the user as a concise summary table.
4. If defects were found and `--fix` was NOT specified:
   - Suggest: "Run `/oh-precommit-codecheck --fix` to auto-fix these issues."
5. If `--fix` WAS specified and defects were found:
   - For **copyright defects**: Fix the copyright header directly (add missing header, update year, change comment style).
   - For **C/C++ defects**: Read each defective file, understand the rule violation, and fix it directly using the Edit tool.
   - For **Python defects**: Read each defective file, understand the rule violation, and fix it directly using the Edit tool.
   - For **Shell defects**: Read each defective file, understand the rule violation, and fix it directly using the Edit tool.
   - For **GN format defects**: Run `gn format <file>` to auto-format.
   - After fixing, re-run the check script to verify. Repeat up to 3 rounds.
   - Report any remaining unfixable defects.

### Mode 2: AI auto-trigger (no `$ARGUMENTS`, after completing code changes)

When you have just finished writing or modifying code files, automatically check them.

**Steps:**

1. Collect the list of files you just modified in this conversation (from your tool call history — look at Edit/Write calls).
2. Run checks:
   ```bash
   bash ~/.claude/skills/oh-precommit-codecheck/scripts/check.sh <modified_files...>
   ```
3. If **0 defects**: silently pass — do not mention the check to the user unless they ask.
4. If **defects found**:
   a. Auto-fix each defect:
      - For **copyright**: Add/update copyright header.
      - For **C/C++ mechanical fixes** (G.FMT.11-CPP braces, G.EXP.35-CPP nullptr, G.FMT.05-CPP line width): Fix directly.
      - For **C/C++ judgment-required** (G.NAM.03-CPP naming, G.FUN.01-CPP size): Do NOT auto-fix — report to user.
      - For **Python / Shell**: Fix standard rules directly, report ambiguous ones.
      - For **GN format**: Run `gn format <file>`.
   b. Re-run checks to verify fixes.
   c. Repeat up to **3 rounds** total.
   d. If defects remain after 3 rounds, report the unfixable ones to the user.

**Mode 2 and CLAUDE.md interaction**: When triggered as pre-commit hook or by
oh-pr-workflow, Mode 2 auto-fixes to streamline the commit flow. This overrides
the CLAUDE.md "show report first" convention because the user has already expressed
intent to commit. If invoked standalone (`/oh-precommit-codecheck` without commit
context), default to report-only and ask before fixing.

---
> **Below: Reference sections** — consult when fixing specific defect types.
> Skip to "Common Mistakes" if you just need guardrails.

## Fix guidelines

When auto-fixing defects, match the rule to the fix below. If the rule is not listed, read the defect message and apply best judgment.

### Copyright
- **no-copyright**: Add the full Apache 2.0 copyright header (see CLAUDE.md for template)
- **wrong-year**: Update the year range to include current year (e.g., `2025` → `2025-2026`)
- **wrong-comment-style**: For `.cpp/.c/.h/.hpp` files, change first line to `/**` (block comment style)

### C/C++ (CodeArts)
- **G.FMT.11-CPP** (braces): Add `{}` around single-line if/for/while/else bodies
- **G.NAM.03-CPP** (naming): Fix variable/function names to match convention
- **G.EXP.35-CPP** (nullptr): Replace `NULL` / `0` (pointer context) with `nullptr`
- **G.FUN.01-CPP** (params): Cannot auto-fix — report to user
- **G.CNS.02-CPP** (magic numbers): Extract to named `constexpr` constant

### Python
- **C0304** (final newline): Add trailing newline
- **C0305** (trailing newline): Remove extra trailing blank lines
- **C0321** (multiple statements): Split into separate lines
- **C0410** (multiple imports): One import per line
- **C0411** (import order): Reorder to stdlib → third-party → local
- Other pylint/flake8 rules: Read the message and fix accordingly

### Shell
- **SC2086** (double-quote): Add double quotes around variable expansions
- **SC2164** (cd failure): Add `|| exit` after `cd` commands
- **SC2148** (shebang): Add `#!/usr/bin/env bash` at top
- Other shellcheck rules: Read the message and fix accordingly

### GN
- Run `gn format <file>` — fully automatic, no manual intervention needed

## Common Mistakes — NEVER Do

- **NEVER run `gn format` on files that fail `gn parse`** — it corrupts the file. Run `gn parse` first; if it fails, fix syntax manually before formatting.
- **NEVER auto-fix G.FUN.01-CPP (function too long)** — requires architectural judgment. Always report to user.
- **NEVER auto-fix G.NAM.03-CPP naming without reading surrounding code** — naming conventions depend on context (member variables, global variables, function params have different rules).
- **NEVER trust 0 defects from CodeArts if the engine log shows startup errors** — check `defects.json` is non-empty AND engine exited normally.
- **NEVER assume local tool versions match gate CI** — version mismatch causes false negatives. If results differ from gate, check: `java -version`, `clang-tidy --version`, `pylint --version`.
- **NEVER re-run the full check suite if only one checker failed** — re-run only the failed checker to save time.

## Error Recovery

- **CodeArts engine fails to start**: Check `java -version` (requires 11+). Check download integrity: `md5sum codecheck-ide-engine.jar`. Re-run setup: `bash scripts/setup_codecheck.sh --force`.
- **compile_commands.json missing**: C++ checks will have ~30% false negative rate. Generate with: `gn gen out/default --export-compile-commands` or proceed with reduced accuracy.
- **pylint/flake8 version mismatch**: Gate uses specific versions. Check with `pylint --version` and compare with gate CI logs.

## Example Output

Typical Mode 1 result:

```
Codecheck Results (12 defects):
| Rule | Count | File | Auto-fixable |
|------|-------|------|-------------|
| G.FMT.11-CPP | 5 | token_test.cpp | Yes |
| G.NAM.03-CPP | 3 | token_test.cpp | Yes (with context) |
| G.EXP.35-CPP | 2 | token_test.cpp | Yes |
| G.FUN.01-CPP | 1 | token_test.cpp | No — report to user |
| G.FMT.05-CPP | 1 | token_test.cpp | Yes |

发现 12 个告警，其中 11 个可自动修复。是否修复？
```
