---
name: ohos-callgraph
description: Use when analyzing C++ function call chains in any OpenHarmony repo — tracing event flow, checking state isolation, finding callers/callees, or auditing cross-layer changes before implementation. Triggers on questions like "what calls X", "trace the event path", "is groupId/displayId passed through", "check if state is isolated".
---

# OpenHarmony Call Graph Analyzer

Analyze C++ function call chains from compiled LLVM bitcode. Crosses dlopen boundaries and resolves vtable indirect calls.

## When to Use

- **Before implementing cross-layer features**: trace the full code path to identify all files that need changes
- **After implementation**: verify keyword coverage (e.g., "is groupId passed through every function in this chain?")
- **Understanding unfamiliar code**: "what does HandleMouseEvent call?" or "who calls UpdateMouseTarget?"

## Prerequisites

- OpenHarmony **compiled successfully** for a product (e.g. rk3568) — needs `.o` bitcode files in `out/<product>/obj/`
- Run from anywhere inside the OpenHarmony source tree

## Quick Reference

```bash
SCRIPT=~/.claude/skills/ohos-callgraph/ohos_callgraph.py

# Forward: what does this function call? (depth 3)
python3 $SCRIPT UpdateMouseTarget --depth 3

# Reverse: who calls this function?
python3 $SCRIPT GetCursorPos --reverse --depth 2

# Scope to a specific repo
python3 $SCRIPT CreateWindow --repo window_manager --depth 2

# Check keyword isolation: does every node have "groupId"?
python3 $SCRIPT UpdateMouseTarget --check-isolation groupId --depth 4

# Full event chain trace (deep)
python3 $SCRIPT HandleMouseEvent --depth 5

# Override product name and OH root
python3 $SCRIPT SomeFunc --product rk3568 --oh-root /path/to/code
```

## How It Works

1. **Scans** `out/<product>/obj/` for `.o` files (LLVM bitcode, produced by `-flto=thin`)
2. **`opt --print-callgraph`** extracts direct function calls from IR
3. **`llvm-dis`** exports IR text; parses `llvm.type.test` metadata to identify vtable interface types
4. **`grep LoadLibrary<Interface>`** in source discovers dlopen mappings (Interface → .so → CreateInstance)
5. Outputs a call tree with tags: `[vtable]` for indirect calls, `[dlopen:libxxx.z.so]` for cross-.so

## Auto-Detection

| Item | Detection method |
|------|-----------------|
| OH root | Walk up from cwd looking for `build/ohos.gni` |
| Product | First dir under `out/` that contains `obj/` |
| Repo filter | Extract from cwd path (e.g. `.../foundation/multimodalinput/input` → `multimodalinput`) |
| dlopen map | `grep LoadLibrary<` + `grep CreateInstance` in source |
| LLVM tools | `prebuilts/clang/ohos/linux-x86_64/llvm/bin/` |

## Limitations

| What | Status |
|------|--------|
| Direct calls | ✅ 100% — from LLVM callgraph |
| Virtual function interface type | ✅ via `type.test` metadata |
| Virtual function concrete target | ⚠️ knows the interface, not which override runs |
| dlopen/dlsym | ✅ auto-mapped via `LoadLibrary<>` + `CreateInstance` pattern |
| Macros | ✅ already expanded in bitcode |
| Templates | ✅ already instantiated |
| Cross-.so (non-dlopen) | ❌ shows as undefined — use `--repo` to include both sides |

## Keyword Isolation Check

`--check-isolation KEYWORD` marks each node:
- ✅ = function name contains the keyword
- ⚡ = a direct callee contains the keyword (keyword is nearby but not in this function)
- (no mark) = keyword absent from this subtree — potential gap

Example: after implementing per-group routing, verify every function in the mouse path handles groupId:
```bash
python3 $SCRIPT HandleMouseEvent --check-isolation groupId --depth 5
```
