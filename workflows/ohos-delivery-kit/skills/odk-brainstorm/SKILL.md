---
name: odk-brainstorm
description: "Use when clarifying requirements or stress-testing decisions before odk-propose, odk-spec, or odk-design. Explore code-grounded alternatives, failure paths, and unresolved constraints before drafting documents. Zero plugin dependencies."
license: MIT
---

# ODK Brainstorm

## Purpose

Interview the user relentlessly about every aspect of their plan until all branches of the design decision tree are resolved. This is **not a form to fill in** — it is an adversarial design review. The model explores the decision tree depth-first, challenges vague answers, and does not move on until each decision can stand on its own.

Focus on decisions the model **cannot derive from code** — architecture ownership, failure semantics, concurrency contracts, rollback strategy, success criteria with real numbers. Infer everything that can be inferred from the codebase; only ask the user what only they can decide.

## Preconditions

- Load `using-odk` first.
- `codespec/changes/<repo-name>/<proposal-id>/` skeleton should exist (run `odk-init` first if not).

## How to ask questions

Ask **one question at a time** as plain text, and wait for the user's answer before the next. Each question offers 2–4 concrete options grounded in what the user is actually building. Never dump multiple questions at once.

Do not call any platform-specific tool for these questions — use ordinary text so the flow works identically on Claude Code, Codex, OpenCode, and OpenClaw.

```
问题：<the question>

A) <option>
B) <option>
C) <option>

（可直接输入你的答案，或选上面的编号）
```

**On every answer:**
1. Briefly acknowledge the decision (1–2 sentences).
2. If the answer opens a new branch (a dependency, an unresolved sub-decision, a risk), go down that branch immediately before moving to the next top-level topic.
3. If the answer is vague ("先这样", "看情况", "大概"), do not accept it — name the ambiguity and re-ask with sharper options.
4. If the answer contradicts an earlier answer, surface the contradiction and ask which one stands.

## Steps

### Step 1 — Baseline from code

Before asking the user anything, explore the codebase yourself:
- Identify the modules, files, and call chains the change touches
- Note existing ownership patterns (who owns state, lifecycle, error recovery)
- Note existing concurrency contracts (which thread, which queue, which lock)
- Note existing failure patterns (how errors propagate, what callers expect)
- Note existing interface contracts (sync/async, return types, side effects)

State what you found in 2–4 sentences, then open the first question based on what is **not answerable from code**. Skip this step only for pure new modules with no existing code to reference; state "新模块，无现有代码基线" and proceed directly to Step 2.

### Step 2 — Explore the decision tree

Walk every branch of the design decision tree depth-first. Resolve dependencies between decisions one by one. The tree typically includes:

**Structural decisions** (go deep on each that is relevant):
- Module/component boundary: where does this change begin and end? Who calls in, who is called?
- State ownership: who creates, mutates, and destroys the relevant state? Is ownership changing?
- Interface contract: sync or async? Who handles errors — caller or callee? What are the invariants after the call?
- Lifecycle management: who allocates, who frees? What happens on early exit or exception?

**Flow decisions** (go deep on each that is relevant):
- Happy path: walk it step by step; confirm each handoff
- Failure path: for each failure mode, what is the recovery strategy? Retry, rollback, surface to caller, silent fail?
- Concurrency: which thread/queue/process executes this? Is there shared mutable state? What is the synchronisation contract?
- Ordering and timing: are there race windows? What happens if two calls interleave?

**Boundary decisions** (always ask these if not already answered):
- **API/SDK**: does this add, modify, or deprecate `.d.ts` / `.h` declarations? **Must be confirmed with the user — never inferred.**
- **Security/trust boundary**: does this cross an IPC/Binder/socket/shared-memory boundary, change a security level, or handle sensitive data? **Must be confirmed — one yes to any sub-question → 「是」.**
- **1+8 device variation**: does the behaviour differ across phone / tablet / pc-2in1 / wearable / tv / car / `default（其他设备）` / non-category? This is a product/business decision — **cannot be inferred from code, must be confirmed with the user for each form factor.** For each device row, get a concrete `是`/`否` with a reason; a blank is not accepted.
- **资源开销审视 (performance/RAM/ROM)**: triage each of the three dimensions as `required` / `review-required` / `not-applicable` / `waived`. Unknown risk → `review-required`, never silent `not-applicable`. Signal hints: 性能 — hot path, per-frame/event cost, wakeup frequency, lock duration, IPC round-trips; RAM — resident/peak memory, large buffers; ROM — `.so`/`.abc`/resource artifacts, large data-partition persistence. **Must be confirmed — cannot be defaulted to `not-applicable` without a named confirmer and reason.**
- **外部依赖 (external dependencies)**: what subsystems, repositories, modules, or external services does this change depend on for delivery? If none, record an explicit `不涉及` with the reason — a blank is not accepted. **Must be confirmed with the user.**
- **兼容性 (compatibility)**: does this change affect backward compatibility, wire-format compatibility, IPC protocol versioning, build/component dependencies, i18n, or data migration? For each sub-dimension, confirm 涉及/不涉及 with a concrete reason — blank is not accepted.
- **Success criteria**: what observable outcome, with a real number or a concrete system behaviour, means this change is done?

**Open questions and non-goals**: after the tree is explored, explicitly name what is out of scope and why.

### Step 3 — Cross-check for contradictions

After all branches are resolved, do one pass across the decisions:
- Do the failure-path decisions contradict the ownership decisions?
- Does the concurrency contract contradict the interface contract?
- Does the success criterion actually validate the happy path end-to-end?
- Does the security answer contradict the IPC/boundary answer from the structural decisions?
- Do the device-variation answers contradict the interface contract? (e.g. a device row marked 「是」 but the interface has no variant path)
- Do the resource verdicts contradict the hot-path/concurrency conclusions? (e.g. a high-frequency IPC path triaged as `not-applicable` for 性能)

Surface any contradiction and re-ask the relevant decision.

### Step 4 — Present summary and confirm

Present a structured **决策摘要** inline, covering:
- Each structural decision with its verdict and the reason the alternatives were rejected
- Each flow decision with its failure semantics
- API/SDK and security verdicts
- Success criteria (with numbers or observable outcomes)
- Explicit non-goals

Ask the user to confirm: "以上是访谈摘要，确认后继续生成下一阶段文档。如需调整请说明。"

If invoked standalone before `proposal.md` exists, next skill is `odk-propose`. If invoked inline from `odk-spec` Step -1, continue into odk-spec Step 0. If invoked inline from `odk-design` Step -1, continue into odk-design Step 0.

If the session is interrupted, tell the user: "访谈中断了。请重新调用已安装的 odk-brainstorm 技能继续；模型会从对话历史里恢复已确认的决策，如历史不可用则从 Step 1 重新开始。"

## Output

- A decision summary presented inline in the conversation, structured by decision with verdict + rejected-alternative + one-line reason each.
- Do NOT write to a separate `brainstorm.md` file — the summary lives in the conversation context as direct input to the next phase skill.
- Do NOT generate the full `proposal.md` / `spec.md` / `design.md` — those are the next phase skills' jobs.

## Cross-plugin note

If the user's environment has `/grill-me`, they may run it first for free-form stress-testing; `odk-brainstorm` then maps its conclusions onto the ODK structural/flow/boundary dimensions above.
