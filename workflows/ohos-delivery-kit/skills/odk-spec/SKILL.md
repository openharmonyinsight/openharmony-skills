---
name: odk-spec
description: "Use when writing ODK spec.md (WHEN/THEN acceptance criteria, error codes, verification mapping). Default template-driven, zero plugin dependencies. Use after proposal.md is approved."
license: MIT
---

# ODK Spec

## Prerequisites

- `proposal.md` with finalized success criteria

## Input

1. Read `proposal.md` success criteria and triage result

## Steps

0. Check for subsystem profile: read and follow `{{ASSET_ROOT}}/contracts/skill-guides/router/profiles.md` — if a profile matches, apply its `template_overrides.spec` (additional AC categories, fragments) and `agent_instructions.specify` before generating content
<!-- ODK:reference contracts/skill-guides/spec/api-specification.md -->
**Steps 1–2.5 — API workflow (conditional):** If proposal.md `API/SDK` = 「是」, read and follow `{{ASSET_ROOT}}/contracts/skill-guides/spec/api-specification.md` in full before Steps 3–6. Steps 1, 2 and 2.5 and their cross-references are local to that guide: repository readiness, declaration guidance/fallbacks, developer-confirmed @since and API descriptions, and device scope/difference confirmation. If `API/SDK` = 「否」, skip these steps; keep the fixed API section and its non-involvement reason as required below.
<!-- /ODK:reference -->
3. **Code fact check (conditional):** If the change involves existing APIs, error codes, or data structures, search the codebase before generating spec:
   - Search for existing API signatures, error code definitions, and data structures referenced in the AC scope
   - Confirm interface details are accurate before writing ACs
   - If code facts contradict assumptions from `proposal.md`, surface and resolve before writing ACs
   - Skip this step for pure new features with no existing code dependencies, pure documentation changes, or config-only changes
4. Read template from `{{ASSET_ROOT}}/templates/ai/spec.md`
5. Generate `spec.md` per the template. Fill in error code values and interface signatures with concrete values where discoverable from the code fact check (Step 3); mark genuinely unknown values as `TBD` with a reason.
6. If any proposal `资源开销审视` dimension is `required`, expand `资源验收契约` (`contracts/artifacts.yaml#resource_contract`). Table detail is subsystem-owned; ODK requires meaningful, non-placeholder content without imposing a measurement schema. Each 验收口径 must be an observable target (latency / fps / throughput / startup time / peak RAM / image delta) — never vague goals like「优化性能」.

## Key Rules

- **API 仓库为阻塞前置条件**：若 proposal.md `API/SDK` = 「是」，必须先获得开发者提供的本地 API 声明仓库路径（`interface_sdk-js` / `interface_sdk_c`；不一定是绝对路径，只要能定位到即可）并验证可读。仓库未就绪时 spec 阶段不得继续。
- **API 规格完整性**：若 proposal.md `API/SDK` = 「是」，必须在 spec.md 中完成全面的 API 规格定义（命名、入参、返回值、权限、@syscap、@since、错误码等全部维度），作为 implement 阶段修改声明文件的精确蓝图。
- **API 描述完整性**：若 proposal.md `API/SDK` = 「是」，必须在 spec.md 的逐 API 子节中定义接口定义三要素（含义/功能、使用场景、使用后效果）和接口使用五要素（相似接口差异、缺省配置、规格限制、生效机制、注意事项）。这些内容直接供 implement 阶段编写声明文件注释 使用，必须与开发者确认，不得臆造或自行推断。
- Do not invent API signatures, error code values, or data structures. Resolve contradictions from code facts before writing ACs.
- Keep ACs concrete enough for the template's verification mapping; code mapping (AC→implementation files) lives in `execution-plan.md`.
- AC 使用 Given/When/Then 格式：Given 前置条件；When 用户/业务可操作动作；Then 通过三层接口边界（public/system/inner API + 终端用户可感知）可观测的结果。
- AC 的 Then 禁止部件内部实现（数据结构/状态机/内部流程/算法）——移 `design.md`「状态归属与不变量」。判定：Then 能否仅凭公开接口判定？需查内部状态则移 design。
- **API 支持属性确认（条件触发）**：若 proposal.md `API/SDK` 维度 = 「是」，需在 `## API 规格定义` 中填写跨平台/元服务/卡片/FA-Stage 模型支持属性。
  - **重要：若无法从需求描述中明确推断以下属性，必须先询问开发者确认，不得猜测或自行填写默认值**：
    - **跨平台支持**：是否支持跨平台（iOS/Android/Windows）
    - **元服务支持**：是否支持开发元服务
    - **卡片支持**：是否支持开发卡片
    - **FA模型或Stage模型支持**：以下三选一：仅支持FA模型，仅支持Stage模型(默认项)，同时支持FA和Stage模型.
  - 询问模板（当缺少信息时使用）：
    ```
    以下 API 支持属性信息不足，需要您确认：
    1. 是否支持跨平台？（增加标记 @crossplatform，表示该 API 可支持跨平台开发，如：iOS/Android/Windows）
    2. 是否支持元服务（增加标记 @atomicservice）？
    3. 是否支持卡片（增加标记 @form）？
    4. FA模型或Stage模型支持情况？（增加标记 @famodelonly, @stagemodelonly, @FaAndStageModel）？
    ```

- **设备行为差异确认（条件触发）**：若 proposal.md `API/SDK` 维度 = 「是」，必须分析 API 的多设备行为差异并输出到该 API 的 `#### API: <完整签名>` 子节下。
  - 通过仓库 `AGENTS.md` 加载其中引用的设备知识文档（若存在），学习设备知识（设备类型枚举、差异行为类型、设备移除规则、自然语言解析规则）
  - 根据 API 的 `@syscap` 确定支持设备列表及起始版本
  - 必须询问开发者是否存在设备行为差异，**不得臆造**
  - 有差异时，将开发者自然语言描述解析为结构化数据，以中文列名+中文选项值展示表格供确认，**确认后才可落盘**
  - 差异行为包含至少一个正常值（功能正常/实现一致）→ 设备保留；不包含任何正常值 → 设备从支持列表移除

## Quality Boundary

- This skill owns profile application, code fact checking, contradiction handling, context loading, and output path.
- `spec.md` template owns required sections, AC format (Given/When/Then) + three-tier observability guidance, verification mapping.
- Internal implementation (data structures/state machines/flows/algorithms) owned by `design.md`; code mapping (AC→implementation files + verification status) owned by `execution-plan.md`.
- `{{EXECUTABLE_ROOT}}/validate-artifacts-contract.py` owns machine-checkable AC coverage, verification mapping, and traceability checks.

## Output

Write to `codespec/changes/<repo-name>/<req-id>/spec.md`.

spec.md 固定包含 `## API 规格定义` 章节；若 `API/SDK` = 否，按 `不涉及：<具体理由>` 填写。API 仓库路径/commit 与既有声明格式参考为 spec 阶段的过程信息，不写入 spec.md；支持属性（跨平台/元服务/卡片/FA-Stage 模型）作为公共规格属性表行写入 `### 公共规格属性`；逐 API 的规格表、API 描述、设备行为差异写入 `#### API: <完整签名>` 子节。设备知识（设备类型枚举、差异行为分类等）来源于仓库 `AGENTS.md` 中引用的设备知识文档（若存在），属于过程信息，不写入 spec.md。

Do not generate `gates/` by default. If the user explicitly wants process evidence, record approval notes under an optional evidence directory such as `evidence/gates/`.

Suggest next step: run `{{CMD_PREFIX}}design` to generate the architecture design, which will reference spec AC numbers and resolve any TBD error codes or interface signatures.
