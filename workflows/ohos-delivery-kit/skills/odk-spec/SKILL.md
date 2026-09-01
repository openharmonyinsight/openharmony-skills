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

0. Check for subsystem profile: follow the Profile Detection rules in `using-odk` — if a profile matches, apply its `template_overrides.spec` (additional AC categories, fragments) and `agent_instructions.specify` before generating content
1. **API 仓库准备（条件触发）**：若 proposal.md `API/SDK` 维度 = 「是」，必须先确认 API 声明仓库在本地可用：
   - **询问开发者提供本地仓库路径**：
     - 涉及 ArkTS API → 需要 `interface_sdk-js` 仓库
     - 涉及 C API → 需要 `interface_sdk_c` 仓库
     - 两者都涉及 → 两个仓库都需要
     - 询问模板：
       ```
       本次变更涉及 API 设计，需要确认本地 API 声明仓库路径：
       1. interface_sdk-js 仓库本地路径（ArkTS API）：
       2. interface_sdk_c 仓库本地路径（C API）：
       请提供上述仓库的本地路径（不一定是绝对路径，只要能定位到即可）。
       ```
   - 验证仓库存在且可读（检查目录存在性、关键目录结构如 `api/`）
   - 开发者未提供路径或路径无效时，**spec 阶段不得继续**，必须等待开发者准备好仓库
   - 阅读仓库中与本次变更 Kit 相关的既有声明文件（≤10 个），提取格式规范：
     - 版权声明头格式
     - JSDoc 结构（`@file`、`@kit`、`@syscap`、`@since` 等标记格式）
     - 既有 API 的命名风格、参数模式、返回值模式
     - 提取结果仅用于本阶段撰写规格（过程信息，不写入 spec.md）
2. **API 全面规格定义（条件触发）**：若 proposal.md `API/SDK` 维度 = 「是」，在阅读既有声明文件后，参照既有格式为本次需求的新增/修改 API 进行完整的规格定义：
   - 规格必须覆盖以下全部维度（不可遗漏）：
     - 是否新增声明文件（是/否，若否则填写修改的声明文件路径）
     - API 类型（Public / System）
     - API 命名（完整的类名/方法名/函数名，须与既有命名风格一致）
     - 入参（每个参数的名称、类型、是否必填、默认值）
     - 返回值（返回值类型、Promise 包装方式等）
     - 权限（所需权限名称和权限级别）
     - @syscap（系统能力标记）
     - @since（API 版本号）
     - 错误码（每个可能抛出的错误码及其数值、触发条件）
     - 编程语言（ArkTS / C / 两者）
     - 跨平台/元服务/卡片（支持标记：@crossplatform / @atomicservice / @form）
     - FA/Stage 模型（支持标记：@famodelonly / @stagemodelonly / @FaAndStageModel）
   - 规格定义写入 spec.md 的 `## API 规格定义` 章节
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

## Quality Boundary

- This skill owns profile application, code fact checking, contradiction handling, context loading, and output path.
- `spec.md` template owns required sections, AC format (Given/When/Then) + three-tier observability guidance, verification mapping.
- Internal implementation (data structures/state machines/flows/algorithms) owned by `design.md`; code mapping (AC→implementation files + verification status) owned by `execution-plan.md`.
- `{{EXECUTABLE_ROOT}}/validate-artifacts-contract.py` owns machine-checkable AC coverage, verification mapping, and traceability checks.

## Output

Write to `codespec/changes/<repo-name>/<req-id>/spec.md`.

spec.md 固定包含 `## API 规格定义` 章节；若 `API/SDK` = 否，填写"不涉及"并说明理由。API 仓库路径/commit 与既有声明格式参考为 spec 阶段的过程信息，不写入 spec.md；支持属性（跨平台/元服务/卡片/FA-Stage 模型）作为规格表行写入 `## API 规格定义`。

Do not generate `gates/` by default. If the user explicitly wants process evidence, record approval notes under an optional evidence directory such as `evidence/gates/`.

Suggest next step: run `{{CMD_PREFIX}}design` to generate the architecture design, which will reference spec AC numbers and resolve any TBD error codes or interface signatures.
