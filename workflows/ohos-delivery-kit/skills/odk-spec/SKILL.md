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
   - **阅读仓库根目录的 `AGENTS.md`**，学习 API 设计规范、命名约定、目录结构约定、声明文件格式要求等知识，以及其中引用的 声明注释规范（ArkTS 为 JSDoc，C 为 Doxygen 或仓库既有注释规范）和设备知识文档。AGENTS.md 中的内容与既有声明文件的实际格式共同构成格式参考，二者冲突时以 AGENTS.md 为准。读取结果仅用于本阶段撰写规格（过程信息，不写入 spec.md）。
   - **AGENTS.md 降级规则**：
     - **AGENTS.md 不存在**：不阻塞，退回仅参照既有声明文件格式（降级模式）。在 spec.md 中不记录降级状态，但需在交互中告知开发者"未找到 AGENTS.md，将仅参照既有声明文件格式"
     - **AGENTS.md 存在但未引用 声明注释规范（ArkTS 为 JSDoc，C 为 Doxygen 或仓库既有注释规范）**：不阻塞，API 描述定义退回参照既有声明文件的 注释风格
     - **AGENTS.md 存在但未引用设备知识文档**：不阻塞，设备行为差异步骤改为直接询问开发者全部设备支持范围（无法由 @syscap 自动确定时），开发者手动提供设备列表和差异
     - **无法由 @syscap 确定设备范围**：不阻塞，改为询问开发者手动提供支持设备列表
   - 阅读仓库中与本次变更 Kit 相关的既有声明文件（≤10 个），提取格式规范：
     - 版权声明头格式
     - 注释结构（`@file`、`@kit`、`@syscap`、`@since` 等标记格式）
     - 既有 API 的命名风格、参数模式、返回值模式
     - 提取结果仅用于本阶段撰写规格（过程信息，不写入 spec.md）
2. **API 全面规格定义（条件触发）**：若 proposal.md `API/SDK` 维度 = 「是」，在阅读既有声明文件后，参照既有格式为本次需求的新增/修改 API 进行完整的规格定义：
   - **公共规格属性**：多个 API 共享的属性（是否新增声明文件、API 类型、编程语言、@syscap、@since、权限、跨平台/元服务/卡片、FA/Stage 模型）统一定义在 `### 公共规格属性` 表中
   - **@since 版本号确认（阻塞）**：API 版本号近期有调整，不得从既有声明文件或代码中自行推断版本号后直接填写。必须先与开发者确认本次 API 的目标版本号，确认后才可写入 spec.md
   - **逐 API 规格**：每个 API 以 `#### API: <完整签名>` 子节展开，包含：
     - 规格表：入参、返回值、错误码等，以及与公共属性不一致的差异项
     - API 描述（接口定义三要素 + 接口使用五要素）
     - 设备行为差异（支持设备表（始终必填）+ 差异明细表（无差异时填"所有支持设备行为一致"））
   - **API 描述定义**：参照 API 声明仓库（Step 1 中开发者提供的 `interface_sdk-js` / `interface_sdk_c`）根目录 `AGENTS.md` 中引用的 声明注释规范（ArkTS 为 JSDoc，C 为 Doxygen 或仓库既有注释规范）（若 AGENTS.md 存在且引用了该规范），为每个 API 定义以下内容，作为 implement 阶段编写声明文件注释 的精确蓝图。这些内容是事实性信息，必须与开发者确认，不得臆造：
     - **接口定义三要素**：含义/功能、使用场景、使用后效果
     - **接口使用五要素**：相似接口差异、缺省配置、规格限制、生效机制、注意事项
   - 规格定义写入 spec.md 的 `## API 规格定义` 章节（公共规格属性 + 逐 API 规格）
2.5 **设备行为差异定义（条件触发）**：若 proposal.md `API/SDK` 维度 = 「是」：
   - **继承 proposal 设备结论**：先读取 proposal.md 的 `## 1+8 设备差异规格`（若存在），作为需求级设备范围参考。proposal 负责需求级设备范围，spec 负责逐 API 细化。若 spec 的逐 API 细化结论与 proposal 的需求级结论存在冲突，**暂停并向开发者确认**，不得自行覆盖 proposal 结论
   - 通过 Step 1 读取的仓库 `AGENTS.md` → 若 AGENTS.md 存在且引用了设备知识文档，加载并学习设备类型枚举、差异行为类型、差异原因、设备移除规则、自然语言解析规则等知识（过程信息，不写入 spec.md）。若 AGENTS.md 不存在或未引用设备知识文档，参见 Step 1 降级规则
   - 根据 API 的 `@syscap` 确定该 API 支持的设备类型列表及各设备起始版本
   - 询问开发者是否存在设备行为差异：
     ```
     本次变更涉及的 API，需要确认多设备行为差异：

     已根据 @syscap 确定支持设备范围：<列出设备类型及起始版本>

     1. 以上设备在功能行为上是否存在差异？（如某些设备不支持、返回不同错误码、行为不同等）
        - 无差异 → 所有支持设备行为一致
        - 有差异 → 请用自然语言描述每个有差异的设备的行为差异
     ```
   - **无差异**：支持设备表仍必填，差异明细表填写"所有支持设备行为一致"
   - **有差异**：
     1. 收集开发者的自然语言描述
     2. 按设备知识文档中的自然语言解析规则解析为结构化数据
     3. 以**中文列名**和**中文选项值**展示表格供开发者确认（禁止展示 JSON 字段名/英文 value）
     4. 开发者确认后才可落盘
   - 根据差异行为判定设备是否从支持列表移除（按设备知识文档中的设备移除规则）
   - 输出写入该 API 的 `#### API: <完整签名>` 子节下的设备行为差异部分（支持设备表始终必填；无差异时差异明细表填写"所有支持设备行为一致"）
   - **禁止事项**：不得臆造设备差异；不得未确认即落盘；行为一致的 API 批量处理时使用相同结果
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
