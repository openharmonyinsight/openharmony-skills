# Evals for ohos-design-graphics-explain-code

This directory contains test cases for the `ohos-design-graphics-explain-code` skill.

## Test Cases

### 1. render-pipeline-architecture

Tests the skill's ability to analyze a multi-threaded rendering pipeline (RSMainThread vs RSUniRenderThread) and produce:
- Interactive clarifying questions (Phase 1)
- Call flow presentation for confirmation (Phase 2)
- Mermaid class diagram (RSRenderNode hierarchy) and sequence diagram (Vsync → Render flow) with code provenance
- Second-pass exploration capturing async/error paths

**Key assertions**: asks-clarifying-questions, presents-call-flow-for-confirmation, includes-mermaid-class-diagram, includes-mermaid-sequence-diagram, diagrams-have-code-provenance, captures-async-error-paths, produces-markdown-doc-file

### 2. fence-cache-class-hierarchy

Tests the skill's ability to document a class hierarchy with ownership/dependency relationships (SyncFence, FenceCache, SyncFenceManager, RenderFencePool) and produce:
- Interactive clarifying questions
- Call flow confirmation before documentation
- Mermaid class diagram with relationship arrows (-->)
- Sequence diagram for the fence creation lifecycle
- Error path analysis (null callback, invalid fd, expired entries)

**Key assertions**: asks-clarifying-questions, presents-call-flow-for-confirmation, includes-mermaid-class-diagram, class-diagram-shows-relationships, includes-mermaid-sequence-diagram, diagrams-have-code-provenance, captures-second-pass-error-paths, produces-markdown-doc-file

### 3. simple-config-no-diagram

Tests the skill's **diagram selection judgment** — for a simple config module (2 structs + 3 linear functions, <3 meaningful types, purely linear flow):
- Should NOT force a class diagram (too few types)
- Should NOT force a sequence diagram (no branching/multi-component interaction)
- Should use tables or text descriptions instead
- Should still ask clarifying questions and explain functions clearly

**Key assertions**: asks-clarifying-questions, does-not-force-class-diagram, does-not-force-sequence-diagram, uses-table-or-text-for-config, explains-functions-clearly

## Design Philosophy

These test cases are designed to highlight behaviors that are **unique to the skill**:

| Behavior | With Skill | Without Skill (baseline) |
|----------|-----------|------------------------|
| Interactive confirmation workflow | Follows 3-phase workflow: asks questions, presents flow, confirms before documenting | Jumps straight to output without confirmation |
| Mermaid diagrams with code provenance | Every diagram element references file paths + line numbers | Creates generic diagrams without anchoring to code |
| Second-pass exploration | Explicitly searches for error handlers, callbacks, conditional logic | Only analyzes the main/happy path |
| Diagram selection judgment | Skips diagrams when inappropriate (<3 types, linear flow, config schema) | Forces diagrams on everything regardless of complexity |

## Directory Structure

```
evals/
  evals.json          # Test case definitions and assertions
  README.md           # This file
  files/
    render_pipeline/  # Test input code for eval 1
      render_node.h
      render_thread.h
      render_thread.cpp
    fence_cache/      # Test input code for eval 2
      sync_fence_manager.h
      sync_fence_manager.cpp
    simple_config/    # Test input code for eval 3
      display_config.h
      display_config.cpp
```