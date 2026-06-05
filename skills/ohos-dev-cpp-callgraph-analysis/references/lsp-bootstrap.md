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
SETUP=/path/to/skills/ohos-dev-cpp-callgraph-analysis/scripts/setup_lsp.py
python3 "$SETUP" \
  --oh-root <openharmony-source-root> \
  --repo-root <current-repository-root> \
  --product <product-name> \
  --build-target <build-target> \
  --generate-compile-db \
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
