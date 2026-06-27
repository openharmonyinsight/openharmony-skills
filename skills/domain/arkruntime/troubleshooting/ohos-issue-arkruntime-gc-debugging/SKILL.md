---
name: ohos-issue-arkruntime-gc-debugging
description: "Use when diagnosing GC-related bugs in ArkCompiler runtime, including crashes during mark/sweep, missing write barriers, dangling pointers, AfterGC verify failures, long STW pauses, or weak ref issues. Triggered when working under ecmascript/mem/**."
metadata:
  author: openharmony
  scope: domain
  stage: troubleshooting
  domain: arkruntime
  capability: gc-debugging
  version: 0.1.0
  status: draft
  tags:
    - arkruntime
    - gc
    - debugging
    - troubleshooting
---

# Task and Boundaries

Diagnose and fix GC-related bugs in the ArkCompiler runtime, including crashes during mark/sweep phases, dangling pointers from missing write barriers, AfterGC verification failures, long STW pauses, and weak reference issues.

**In scope:**
- Objects reclaimed while still reachable (post-GC crashes)
- Crashes inside mark or sweep phases
- AfterGC verification failures
- Long pause / STW spikes on specific tests
- CMC GC-only regressions
- Weak references returning stale (already-collected) objects

**Out of scope:**
- General allocator / memory pool issues unrelated to garbage collection
- Non-runtime (application-layer) memory bugs
- Build or configuration problems unrelated to GC behavior

# Trigger Signals

- Reachable object is reclaimed (crash on a still-used pointer, only after GC)
- Crash inside the mark or sweep phase
- AfterGC verify failure
- Long pause / STW spike on a specific test
- Regression that only reproduces when `ets_runtime_enable_cmc_gc` is on
- Weak ref returns a stale (already-collected) object
- User mentions: missing barrier, AfterGC, mark-sweep crash, CMC GC crash, GC stats, GC pause, weak ref bug

# Initial Checks

Use the first-cut decision tree to classify the symptom:

1. **"Reachable but freed"** → write barrier or visitor coverage gap. Start at `ecmascript/mem/barriers.h` (audit the offending field's writers) and the visitor for the involved class in `ecmascript/mem/visitor.h` / `full_gc.h`.
2. **Crash inside mark phase** → unrooted handle on the stack, OR a missing visitor on a recently added field. See gc-rooting.
3. **Crash inside sweep / compact** → suspect a stale pointer to a moved object. Audit any caller that holds a raw pointer across a possible-GC point.
4. **CMC GC-only regression** → start at `ecmascript/mem/cms_mem/sweep_gc.h` and the shared GC interaction in `ecmascript/mem/shared_heap/shared_gc.h`.
5. **AfterGC verify failure** → the verifier message names the violated invariant; the failing object's class points at the missing visitor / barrier.
6. **Pause regression** → measure with the GC stats path on `Heap` and the GC log; correlate to a pass / collector that grew its work.

# Execution Strategy

## Diagnostics Toolkit

- GC log (the GC log compile flag in `js_runtime_config.gni`; check the file for the current flag name). Captures GC events around the failure.
- Force-GC harness in unit tests; debug build has it enabled by default. To disable for QEMU runs use `disable_force_gc=true` in the GN args (per `CLAUDE.md`).
- AfterGC verify hooks on `Heap` — turn on while investigating; they fail loud at the moment of the violation rather than later.
- ASan / debug-build assertions — always reproduce in `x64.debug` first. Most "random" GC crashes are deterministic in debug.
- The existing `ecmascript/tests/gc_first_test.cpp` / `gc_second_test.cpp` / `gc_third_test.cpp` and `weak_ref_old_gc_test.cpp` as scaffolds for a fresh reproducer.

## Common Root Causes

- **Missing visitor on a new field.** Symptom: object's child becomes dangling. Fix: see gc-rooting; update every visitor.
- **Raw store to a tagged field.** Symptom: cross-region reference invisible to GC. Fix: route through `Barriers::Set*`.
- **Unrooted local across a GC trigger.** Symptom: random crash. Fix: wrap in `EcmaHandleScope` + handle.
- **Held a raw pointer across compaction.** Symptom: read returns garbage after a full GC. Fix: handles, not raw pointers.
- **MachineCodeSpace lifetime mishandled.** Symptom: AOT/JIT code space freed while still referenced. Fix: see compiler-overview for who owns this space.
- **Sendable cross-region write without a cross-region barrier.** Symptom: only fails under multi-worker. Fix: see sendable-debugging.

# Prohibited Practices

- Using raw assignment to a tagged field instead of routing through `Barriers::Set*` — bypasses the write barrier, making the reference invisible to GC, leading to dangling pointers.
- Holding raw `JSTaggedValue` pointers across any point that may trigger GC without wrapping in a handle — GC may move or reclaim the underlying object, causing the raw pointer to go stale.
- Adding a new tagged field without updating all concrete visitors — the new child reference will not be traced, causing its object to be prematurely reclaimed.

# Exceptions and Fallbacks

Bring to the next reviewer:

- The exact reproducer (single test command).
- GC log around the failing point.
- GN args used (especially `ets_runtime_enable_cmc_gc`).
- Whether the bug reproduces in `x64.debug` (assertion output, if any).
- AfterGC verify output, if the verifier was on.
- The class of the involved object (so a maintainer can audit its visitors / barriers in seconds).

If the symptom does not match any of the six categories in Initial Checks, or if the bug does not reproduce in debug builds, treat it as an unknown GC interaction and escalate with the above evidence rather than guessing.

# References

This skill is self-contained. No additional reference files need to be loaded for standard GC debugging tasks. For deeper domain context on specific subsystems mentioned in this skill (gc-rooting, compiler-overview, sendable-debugging), consult the corresponding documentation within the `ecmascript/mem/` source tree or project-level CLAUDE.md.
