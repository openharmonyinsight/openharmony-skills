# Repository-Scoped LSP Bootstrap

Read this reference only when the current environment has no working LSP/MCP service for the
OpenHarmony repository under analysis.

## Preconditions and Approval

Resolve these values from the task or environment and pass them explicitly:

- OpenHarmony source root
- Current repository root
- Product name
- Build target

Do not make the setup script search for them. The repository must be inside the source root.

Before running setup, tell the user which side effects apply and obtain approval where required:

- Download pinned Go and `mcp-language-server` dependencies when unavailable.
- Invoke an OpenHarmony build when the product compile database is missing.
- Modify detected MCP client configuration when registration is requested.

## Resource and Build Boundaries

The product-wide `out/<product>/compile_commands.json` can be several gigabytes. The setup script
streams it into a persistent repository-scoped database instead of loading it fully into memory or
configuring clangd against it directly.

clangd background indexing can still take minutes and several gigabytes of memory for a large
repository. Report this cost before setup when the environment is resource-constrained.

`--build-target` is environment-specific. Confirm it from the repository's documented build command
or existing build metadata. The repository directory name is only a fallback and may not be a valid
OpenHarmony build target.

## Setup

```bash
SETUP=/path/to/skills/ohos-dev-distributed-cpp-callgraph-analysis/scripts/setup_lsp.py
python3 "$SETUP" \
  --oh-root <openharmony-source-root> \
  --repo-root <current-repository-root> \
  --product <product-name> \
  --build-target <build-target> \
  --generate-compile-db \
  --install-hook \
  --client auto
```

If `out/<product>/compile_commands.json` already exists, omit `--generate-compile-db`.

The script:

1. Locates the OpenHarmony prebuilt clangd.
2. Streams and filters the product compile database into a repository-scoped cache.
3. Installs pinned `mcp-language-server` dependencies when missing.
4. Runs MCP tool-discovery and clangd semantic smoke tests.
5. Registers detected Codex or Claude clients when requested.
6. Prints the tool-neutral MCP bridge command for other clients.
7. With `--install-hook` and a selected Claude client: installs a Claude PreToolUse hook that
   auto-adds missing compdb entries.

Use repeated `--client codex` or `--client claude` to select supported automatic registrations. Use
`--client none` to prepare the service without registration, then register the printed bridge command
using the current MCP client's documented stdio-server configuration.

## Verification and Fallback

Require the setup script's MCP tool-discovery and semantic smoke test to pass before treating LSP as
available. Then issue `hover` on a relevant source or header location before the first global
`definition` or `references` query. A fresh clangd process may return `not found` until a relevant
file is opened.

If setup fails:

1. Record the failed stage and error.
2. Mark LSP evidence unavailable or incomplete.
3. Continue with source, build, symbol, helper, and runtime evidence.

Do not block the call-chain analysis solely because LSP setup failed.

## File Not in compile_commands.json

When the filtered compdb does not contain an entry for the target file, clangd falls back to
heuristic header resolution. This fallback is extremely slow (minutes instead of seconds) because
clangd must guess include paths without compile flags.

**Symptom**: clangd CPU stays at 100% for minutes on a single file; other files respond in seconds.

**Root cause**: The filtered compdb only contains files whose GN targets were built. New test files,
files from unbuilt targets, or files added after the last `--export-compile-commands` run are missing.

### Automated fix (Claude PreToolUse hook)

Pass `--install-hook` to `setup_lsp.py` when Claude is the selected MCP client to install a
PreToolUse hook that runs before every Claude `ohos-lsp` tool call:

1. Extracts `filePath` from the tool input.
2. Checks if the file has a compdb entry.
3. If missing, finds the most similar existing entry and clones it with adjusted paths.
4. Appends the cloned entry to the filtered compdb.
5. Only processes C/C++ files (`.cpp`, `.cc`, `.c`, `.h`, `.hpp`).

The hook has a 5-second timeout and produces a `systemMessage` when it adds an entry. The setup
script does not install this hook for Codex or other MCP clients; use the manual fix below unless
that client documents an equivalent pre-tool hook mechanism.

Claude configuration in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__ohos-lsp",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/scripts/ensure_compdb.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Manual fix

```bash
# 1. Find a similar existing entry
grep "similar_test.cpp" compile_commands.json

# 2. Clone it, replacing file/object paths
sed 's/similar_test/new_test/g; s|old/path/|new/path/|g'

# 3. Append to compdb (before closing ])

# 4. Verify (should complete in under 10 seconds)
clangd --check=<file> --compile-commands-dir=<compdb_dir>
```
