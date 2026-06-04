---
name: ohos-callgraph
description: Use when an OpenHarmony C++ change must be checked for call-chain completeness, especially for groupId/displayId propagation, event flow, IPC/proxy/stub paths, virtual overrides, callbacks, or dlopen/dlsym boundaries. Produces evidence tables and modification coverage matrices; the helper script only discovers candidate edges.
---

# OpenHarmony Call-Chain Completeness Analysis

This skill has two layers:

1. **Agent workflow**: prove whether a change is complete from the call-chain perspective by using LSP/source evidence, edge classification, and a coverage matrix.
2. **Helper script**: `ohos_callgraph.py` discovers candidate direct call edges and best-effort vtable/dlopen hints from build artifacts. It is not a precision oracle.

Do not claim a call chain is complete from script output alone.

## Required Workflow

### 1. Define the Analysis Target

Before using tools, state:

- Entry point or event path, such as `HandleMouseEvent`, `UpdateMouseTarget`, `OnRemoteRequest`.
- Target data or behavior, such as `groupId`, `displayId`, pointer target routing, or device binding.
- Scope boundaries to include: client/server, IPC, callbacks, virtual interfaces, dlopen/dlsym implementations, generated code, and tests.
- Scope boundaries intentionally excluded, with reasons.

If any of these are unknown, inspect code first and make a bounded assumption. Do not skip this step.

### 2. Discover Candidate Edges

Use evidence sources in this order:

1. **LSP / clangd**: preferred static source for definitions, declarations, references, call hierarchy, override candidates, and macro-aware symbol locations.
2. **Source search**: use `rg` to find framework patterns that LSP does not model well, such as transaction codes, listener registration, `LoadLibrary<>`, `dlsym`, and generated-file names.
3. **Build graph and symbol tools**: use GN/Ninja, `llvm-nm`, `llvm-readelf`, `llvm-objdump`, and `llvm-cxxfilt` for libraries, exports, link edges, and generated artifacts.
4. **Helper script**: use `ohos_callgraph.py` to discover IR-level candidate direct edges and best-effort vtable/dlopen hints.
5. **Runtime trace**: use logs, instrumentation, or symbolized traces when static evidence cannot uniquely resolve virtual, callback, IPC, or dlopen/dlsym edges.

LSP is the first choice for language-level C++ facts, but it is not enough for runtime binding or OpenHarmony framework protocols.

When LSP/clangd is available, use it before the helper script for:

- `definition` / `declaration`
- `references`
- `call hierarchy` incoming/outgoing calls
- override and implementation candidates
- macro-expanded symbol locations

When LSP is unavailable or incomplete, say so in the evidence table and fall back to source search plus build/symbol evidence.

#### Helper Script

Recommended helper invocation when the agent knows the context:

```bash
SCRIPT=/path/to/skills/ohos-callgraph/ohos_callgraph.py
python3 "$SCRIPT" HandleMouseEvent \
  --oh-root /home/libing/work/ohos_master \
  --product rk3568 \
  --repo multimodalinput \
  --depth 4
```

Reverse direct callers:

```bash
python3 "$SCRIPT" UpdateMouseTarget \
  --oh-root /home/libing/work/ohos_master \
  --product rk3568 \
  --repo multimodalinput \
  --reverse \
  --depth 3
```

The helper script output is a candidate list. Every important edge still needs source evidence.

### 3. Classify Every Edge

Each call-chain edge must be classified:

| Type | Evidence Required |
|------|-------------------|
| `direct` | Prefer LSP call hierarchy/references; include caller line and callee definition or declaration |
| `virtual` | Prefer LSP override candidates; include interface call site, candidate overrides, and dispatch reason if known |
| `callback` | Registration site and invocation site; LSP can locate symbols but usually cannot prove registration-to-invocation flow |
| `ipc` | Proxy write, stub read, transaction code, and service handler |
| `dlopen/dlsym` | Load site, library/symbol name, factory or function pointer use; confirm with symbols or trace when needed |
| `macro/generated` | Prefer LSP macro-aware locations; include generated source or expanded target that proves the edge |
| `unknown` | Evidence gap; cannot support a completeness claim |

For virtual, callback, IPC, and dlopen/dlsym edges, list all relevant candidates or explicitly justify why only one candidate applies.

### 4. Build the Evidence Table

Output a table with these columns:

| Caller | Callee / Candidate | Edge Type | Evidence Source | Evidence | Confidence | Needs Change | Change Status |
|--------|--------------------|-----------|-----------------|----------|------------|--------------|---------------|

Rules:

- `Evidence Source` is one or more of `lsp`, `source`, `build`, `symbol`, `script`, `runtime`, or `manual`.
- `Evidence` must include file paths and line numbers.
- `Confidence` is `confirmed`, `candidate`, or `unknown`.
- `Needs Change` explains why the target data or behavior must pass through this edge.
- `Change Status` is `done`, `missing`, `not needed`, or `unknown`.
- `script` evidence alone cannot make a non-direct edge `confirmed`.

Do not collapse multiple edge types into one row.

### 5. Build the Modification Coverage Matrix

For propagation changes such as `groupId` or `displayId`, check each applicable surface:

| Surface | What to Check | Static Evidence | Runtime Evidence | Status |
|---------|---------------|-----------------|------------------|--------|
| Function signature | Parameter or object carries the target data | LSP definition/declaration or source line | Optional | |
| Call arguments | Caller passes the correct value, not a default or stale value | LSP call hierarchy/references or source line | Optional | |
| Event/object fields | Field is set, copied, cloned, and reset correctly | Source/LSP field references | Optional | |
| IPC proxy/stub | Parcel write/read order and transaction compatibility | Source transaction and Parcel evidence | Trace/log if ambiguous | |
| Service dispatch | Server side receives and uses the value | Source/LSP handler path | Trace/log if ambiguous | |
| Virtual overrides | All reachable overrides accept or derive the value | LSP override candidates and source evidence | Required if static dispatch is not unique | |
| Callback flow | Registration and invocation both preserve the value | Source registration/invocation evidence | Required if registration-to-call flow is ambiguous | |
| dlopen/dlsym implementation | Loaded implementation handles the value | Source + symbol/build evidence | Required if loaded target is runtime-dependent | |
| Generated code | Generated wrappers and ABI layers preserve the value | Generated source or build artifact evidence | Optional | |
| Tests | Unit/system tests exercise at least one representative path and boundary | Test source evidence | Test execution result when available | |

The final answer must say which rows are complete, missing, or unknown.

### 6. Decide Completeness

Use these labels:

- **Complete**: all relevant confirmed and candidate edges have `done` or `not needed`, and unknowns are either resolved or explicitly out of scope.
- **Incomplete**: at least one required edge or surface is `missing`.
- **Not provable**: important edges remain `unknown`, or static-only evidence cannot resolve a runtime-bound edge that affects the conclusion.

## Helper Script Scope

`ohos_callgraph.py` can help find candidates after LSP/source inspection:

- Direct IR call edges from `opt --print-callgraph`
- Best-effort vtable interface hints from LLVM IR metadata
- Best-effort dlopen hints from common `LoadLibrary<>` / `CreateInstance` patterns
- Reverse direct callers

Limitations:

- It does not prove all possible C++ calls.
- It does not resolve runtime virtual dispatch to a unique override.
- It does not prove callback, function pointer, or `std::function` targets.
- It does not prove IPC parameter propagation.
- It does not prove `groupId`/`displayId` propagation. `--name-keyword` only checks demangled function names as a rough hint.
- It may miss edges when build artifacts are stale, missing bitcode, optimized differently, or external tools fail.

Use the helper script only as a candidate discovery aid for the evidence workflow.

## LSP Guidance

Use LSP/clangd as evidence when it is backed by the correct compile context for the OpenHarmony product under review. If the repository lacks `compile_commands.json` or clangd cannot resolve includes/macros, mark LSP evidence as incomplete and rely on source/build evidence instead.

Recommended LSP-backed checks:

- For a direct function call, use outgoing call hierarchy or go-to-definition from the call site, then record the caller and callee file lines.
- For reverse analysis, use incoming call hierarchy and references, then validate the call site manually.
- For virtual calls, use implementation/override queries to list candidates. Keep candidates as `candidate` unless construction/registration/source rules or runtime trace proves the actual target.
- For macros, use the resolved symbol location from LSP, then record the macro or generated expansion source when relevant.

Do not use LSP alone to confirm callback flow, IPC dispatch, or dlopen/dlsym targets.

## Required Final Response Shape

When using this skill, end with:

1. **Scope**: entry point, target data/behavior, included boundaries.
2. **Evidence Table**: edge-by-edge evidence source, evidence, confidence, and status.
3. **Coverage Matrix**: modification surfaces with static evidence, runtime evidence, and status.
4. **Conclusion**: `Complete`, `Incomplete`, or `Not provable`, with the exact missing or unknown items.

If you cannot inspect a required boundary, say so and mark it `unknown`.
