---
name: ohos-dev-arkui-compile-analysis
description: >
  Measure compilation time, peak memory, and header dependency trees for individual ACE Engine
  source files. Generates reusable compilation scripts for before/after benchmarking.
  Use when user says 分析编译效率/analyze compilation, 头文件依赖/header dependencies,
  单独编译/compile single file, or mentions .ii files, dependency tree.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkui
  capability: compile-analysis
  version: 0.1.0
  status: trial
---

# ArkUI Compile Analysis

Analyze compilation efficiency for individual source files in the ACE Engine project.

## Critical Rules

- Execute `analyze_compile.sh` from the ace_engine project directory (auto-locates OpenHarmony root)
- Extracted compilation commands MUST execute in `out/{product}/` directory (not project root)
- All results MUST be based on actual execution — no speculation
- Header dependencies MUST be parsed via `parse_ii.py` on `.ii` files — never use `clang -E`, `gcc -M`, or manual parsing
- Always save dependency tree output to `out/{product}/{file_name}_dependency_tree.txt`

## Workflow

### Full Analysis (execute + display results)

```bash
# From ace_engine directory:
<skill_dir>/scripts/analyze_compile.sh <source-file> [product-name]

# Example:
<skill_dir>/scripts/analyze_compile.sh frameworks/core/components_ng/base/frame_node.cpp rk3568
```

### Save Reusable Script (for benchmarking)

```bash
<skill_dir>/scripts/analyze_compile.sh <source-file> [product-name] --save-script
# Creates: out/{product}/compile_single_file_{name}.sh
# Execute later: cd out/{product} && bash compile_single_file_{name}.sh
```

### Header Dependency Analysis

Decision tree for dependency analysis:

```
.ii file exists in out/{product}/obj/?
  YES → Parse directly: python3 scripts/parse_ii.py <ii-file>
  NO → compile_single_file_{name}.sh exists?
    YES → cd out/{product} && bash compile_single_file_{name}.sh
    NO → Generate script first:
         python3 scripts/get_compile_command.py <source-file> out/{product} --save-enhanced
         Then execute it to produce .ii file
```

Always save result: `python3 scripts/parse_ii.py <ii-file> --output out/{product}/{name}_dependency_tree.txt`

### Standalone Compilation

```
compile_single_file_{name}.sh exists?
  YES → cd out/{product} && bash compile_single_file_{name}.sh
  NO → Generate first:
       python3 scripts/get_compile_command.py <source-file> out/{product} --save-enhanced
       Then execute
```

## Scripts

### analyze_compile.sh (main entry point)

Orchestrates full workflow: extract compile command → execute with timing/memory profiling → parse .ii → display results.

```bash
<skill_dir>/scripts/analyze_compile.sh <source-file> [product-name] [--save-script]
```

- `source-file` — path relative to ace_engine root (or absolute)
- `product-name` — target product (default: `rk3568`)
- `--save-script` — generate standalone script at `out/{product}/compile_single_file_{name}.sh`

### get_compile_command.py

Extracts compilation command from ninja build files.

```bash
# Display commands only:
python3 <skill_dir>/scripts/get_compile_command.py <source-file> <out-dir>

# Save enhanced command (with performance monitoring, no ccache, -save-temps):
python3 <skill_dir>/scripts/get_compile_command.py <source-file> <out-dir> --save-enhanced
```

The enhanced command modifies the original by: removing ccache, adding `-save-temps=obj` (for .ii generation), wrapping with `/usr/bin/time` (for memory measurement).

### parse_ii.py

Parses `.ii` preprocessed files to extract header dependency trees filtered to `foundation/arkui/` headers.

```bash
python3 <skill_dir>/scripts/parse_ii.py <ii-file> [--output <output-file>]
```

Output: Unicode tree showing hierarchical include relationships under `foundation/arkui/ace_engine/`.

## Interpreting Results

| Metric | Normal | High (investigate) |
|--------|--------|-------------------|
| Compile time | < 5s (small), 5-15s (moderate) | > 15s |
| Peak memory | 100-500 MB | > 500 MB (excessive templates/headers) |
| Dependency depth | 3-5 levels | > 6 levels (long chains) |
| Dependency breadth | < 10 direct includes | > 10 (consider consolidation) |

## Troubleshooting

- **"找不到编译规则"**: File not in build database — run full build first, use relative path from ace_engine root
- **"找不到 .ii 文件"**: Enhanced compilation failed — verify compiler supports `-save-temps=obj`
- **Dependency tree too small**: Expected — `parse_ii.py` filters `foundation/arkui/` only; system headers excluded by design

## Before/After Benchmarking

```bash
# 1. Generate baseline script
<skill_dir>/scripts/analyze_compile.sh <file> rk3568 --save-script

# 2. Run baseline
cd out/rk3568 && bash compile_single_file_{name}.sh
# Record: 编译时间, 峰值内存

# 3. Apply optimizations (reduce includes, forward declarations)

# 4. Run comparison (same script, identical conditions)
bash compile_single_file_{name}.sh
```

## Optimization Guide for ACE Engine

When results show "High" (compile time >15s, memory >500MB, depth >6, breadth >10), apply these strategies in priority order:

### Priority 1: Replace full includes with forward declarations

Highest impact. Check if the header is only needed for pointer/reference types:

```cpp
// BEFORE: full include pulls entire dependency chain
#include "core/components_ng/base/frame_node.h"    // pulls 200+ transitive deps

// AFTER: forward declaration (header), include in .cpp only
class FrameNode;  // header: just the name
// .cpp: #include "core/components_ng/base/frame_node.h"  // full definition here
```

**Key pattern**: When `RefPtr<T>` or `WeakPtr<T>` is a class member and the type is only used as pointer, declare special member functions in header, implement with `= default` in .cpp. See `arkui-build-error-analyzer` skill Case 6 for the exact pattern.

### Priority 2: Remove unused includes

Use the dependency tree to identify headers that contribute no used symbols. Common in ACE Engine:
- Files that included `"core/pipeline/base/element.h"` historically but no longer use Element
- Files with leftover includes from copy-paste component creation

### Priority 3: Break deep dependency chains

Common deep chains in ACE Engine:
- `frame_node.h` → `ui_node.h` → `element.h` → `render_node.h` → ... (6+ levels)
- `gesture_event_hub.h` → `gesture_recognizer.h` → `touch_event.h` → ... (5+ levels)

Solution: Introduce interface headers that only declare (not define) the needed types.

### Priority 4: Reduce template instantiation overhead

When peak memory is the primary issue (>500MB), check for:
- `std::map<std::string, std::vector<CalcLength>>` — each unique template combination costs memory
- Heavy use of `OptionalSize<float>`, `LayoutConstraintT<float>` — explicit instantiation in .cpp reduces header bloat
- Move template implementations from header to .cpp with explicit instantiation

### High-Impact Files to Prioritize

These files have the widest include reach in ace_engine — optimizing them gives the most build-time improvement:

| File | Approximate dependents | Impact |
|------|----------------------|--------|
| `frameworks/core/components_ng/base/frame_node.h` | 500+ files | Very high |
| `frameworks/core/components_ng/base/ui_node.h` | 400+ files | Very high |
| `frameworks/core/pipeline/base/element.h` | 300+ files | High |
| `frameworks/core/event/touch_event.h` | 200+ files | High |
| `frameworks/core/components_ng/pattern/pattern.h` | 200+ files | High |
| `frameworks/base/memory/ace_type.h` | 1000+ files | Critical (rarely optimizable) |

**Strategy**: Measure these files first. If any compile >10s, optimizing them saves time across hundreds of dependents.

## NEVER Rules for Optimization

- **NEVER** remove an include without checking for conditional compilation (`#ifdef`, platform guards, `OHOS_BUILD_ENABLE_*` macros) — removing conditionally-used includes breaks non-default builds
- **NEVER** move a function from inline header definition to .cpp without verifying no other headers depend on the inline definition being visible (common with `constexpr` and template functions)
- **NEVER** add includes back to an optimized header — add them to the `.cpp` file instead. Check `git status` first to detect headers being optimized
- **NEVER** assume which file is the bottleneck without measuring — always run baseline analysis before optimization
- **NEVER** suggest precompiled headers (PCH) as first solution — PCH masks dependency problems; fix the root cause instead
- **NEVER** modify `ace_type.h` or `ref_ptr.h` — these are fundamental types used by 1000+ files; even small changes have massive rebuild impact
