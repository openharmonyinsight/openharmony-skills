---
name: odk-brainstorm
description: "Use before odk-propose when the requirement is vague and needs structured clarification. Pure-text one-question-at-a-time interview across the ODK proposal dimensions; outputs a decision summary that feeds directly into proposal.md. Zero plugin dependencies — works on all four platforms."
license: MIT
---

# ODK Brainstorm

## Purpose

Interview the user one question at a time to resolve the ODK proposal dimensions before drafting `proposal.md`. This is the lightweight, dependency-free alternative to `odk-sp-brainstorm` (which requires Superpowers). Use it when the user describes a vague idea, says "帮我梳理需求" / "I have an idea but don't know how to write it" / "stress-test this plan", or asks for a brainstorm before proposing.

## Preconditions

- Load `using-odk` first.
- `codespec/changes/<repo-name>/<proposal-id>/` skeleton should exist (run `odk-init` first if not). If it does not exist yet, you may still interview; tell the user to run `odk-init` before `odk-propose` consumes the summary.

## How to ask questions

Ask **one question at a time** as plain text, and wait for the user's answer before the next question. Each question offers 2–4 concrete options the user can pick by typing the letter/number or writing their own. Never dump multiple questions at once.

Do not call any platform-specific popup or tool-call UI for these questions — use ordinary text so the flow works identically on Claude Code, Codex, OpenCode, and OpenClaw.

Example format for each question:

```
问题：<the question>

A) <option>
B) <option>
C) <option>

（可直接输入你的答案，或选上面的编号）
```

Generic Yes/No options are only acceptable when the question is genuinely binary. Prefer options grounded in what the user is actually building.

If a question can be answered by exploring the codebase or existing files, explore it yourself instead of asking the user. Only ask the user what only they can decide (intent, business constraints, target devices, security stance, success criteria).

## Interview dimensions

Walk the decision tree across the proposal's dimensions, in this order. Skip any dimension the user's earlier answers already resolved; do not re-ask. For each dimension, ask only what is still ambiguous.

1. **功能需求 (core capability)** — What is the change doing, in one sentence? What is explicitly out of scope (non-goals)?
2. **变更类型 (change type)** — new-feature / enhancement / optimization / bugfix / refactor / deprecation. Confirm the primary driver.
3. **1+8 设备差异规格** — Does behavior differ across phone / tablet / pc-2in1 / wearable / tv / car / `default（其他设备）` / non-category? Ask only about devices where the user has not already stated a difference.
4. **API/SDK** — Does the change add, modify, or deprecate API declarations (`.d.ts` / `.h`)? This dimension **must always be confirmed with the user, never inferred.** If yes, gather Kit, API type (public/system), and language (ArkTS/C).
5. **安全/权限** — Does the change cross a trust boundary (IPC/Binder/shared memory/Socket), cross a security level (user↔kernel, sandbox, SELinux domain), handle sensitive data, or use crypto/auth/permission? Hit any → 「是」. This is the single downstream trigger for design 安全基础检查 and threat-model.
6. **性能 / 内存(RAM) / 存储(ROM)** — Hot path, per-frame/per-event cost, wakeup frequency, lock duration, IPC round-trips; resident/peak RAM, large buffers; image artifacts (`.so`/`.abc`/resources/preset packages), data-partition persistence. Triage each as required / review-required / not-applicable / waived. Unknown risk → review-required (never silent not-applicable).
7. **DFX (故障模式)** — Which repositories are touched? Any known failure modes or fault-handling concerns the design must address?
8. **外部依赖** — Dependent subsystems / repositories / modules / external services. If none, record an explicit `不涉及` row with the reason.
9. **兼容性 / IPC·跨进程 / 构建·组件 / 国际化·无障碍 / 数据迁移** — Confirm each as 涉及 / 不涉及 with a concrete reason; no blanks.
10. **成功标准 (success criteria)** — What observable outcome means this change is done? Prefer measurable targets over vague goals.

## Steps

1. Acknowledge the user's idea in one sentence, then start the interview at dimension 1.
2. After each answer, acknowledge the decision in 1–2 sentences, then ask the next open question via the plain-text format above.
3. Explore the codebase yourself for any question you can answer without the user (existing signatures, existing dependencies, current device support). State what you found, then continue.
4. When all dimensions above are resolved, write a structured **决策摘要 (decision summary)** to `proposal.md` as a front-matter-free scratch section, or to a `brainstorm.md` next to it, covering every dimension's verdict and the user's stated reasoning. Keep it concise — this summary is input for `odk-propose`, not the final proposal.
5. Suggest the next step explicitly: invoke `odk-propose` (or `odk-sp-brainstorm` if Superpowers is installed and the user wants the heavier flow) to turn the summary into a formal `proposal.md`.

## Output

- A decision summary covering all dimensions, written to `brainstorm.md` (or appended to the proposal skeleton).
- The summary is structured by dimension with verdict + one-line reason each, plus the non-goals and success criteria.
- Do NOT generate the full `proposal.md` — that is `odk-propose`'s job. This skill only clarifies intent.

## Cross-plugin note

If the user's environment has a dedicated grilling skill (e.g. `/grill-me` on Claude Code) and they prefer it for free-form stress-testing, they may run that first; `odk-brainstorm` then focuses on mapping its conclusions onto the ODK dimensions above. This is a user choice, not a dependency.
