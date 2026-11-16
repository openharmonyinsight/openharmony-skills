---
name: odk-spec
description: "Use when writing ODK spec.md (WHEN/THEN acceptance criteria, error codes, verification mapping). Default template-driven, zero plugin dependencies. Use after proposal.md is approved."
license: MIT
---

# ODK Spec

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

## Phase flow and next step

<!-- ODK:reference contracts/skill-guides/router/phase-flow.md -->
Before phase work, read `contracts/skill-guides/router/phase-flow.md` and apply
its configured pre_hook/post_hook order. At every completion or pause, show
the next pending action and configured hooks; omit the reminder only when
the entire applicable workflow is complete. The coordinator owns this flow.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and obtain the effective
contract before choosing artifacts, sections or phase prerequisites.
<!-- /ODK:reference -->

## Prerequisites

- `proposal.md` with finalized success criteria

## Input

1. Read `proposal.md` success criteria and triage result

## Steps

<!-- ODK:reference contracts/skill-guides/spec/contract-boundary.md -->
Read `contracts/skill-guides/spec/contract-boundary.md` before writing or revising
spec. Apply it to all sections, including business rules and test hints. Read
code for facts and compatibility; keep its internal mechanisms in design and
test implementation/results in the plan. Preserve an unchanged contract spec.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/writing/chinese.md -->
生成或修订中文 spec 前，阅读并执行 `contracts/skill-guides/writing/chinese.md`。
用中文写清适用条件、操作和结果，参照正反例检查措辞；保留固定格式、编号和技术含义。
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/writing/chinese-examples.md -->
首次撰写或修订中文 spec 时，一并阅读 `contracts/skill-guides/writing/chinese-examples.md`。
按语境学习改写方法，保留准确术语与原有约束，不套用示例的业务行为或验证结论。
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/research/codebase-understanding.md -->
Before the interview or AC generation, read
`contracts/skill-guides/research/codebase-understanding.md`. Build or refresh the
relevant implementation baseline, including integration points for new features
and consumers of executable configuration. Reuse its evidence across spec and
design; an interview summary alone does not establish code facts.
<!-- /ODK:reference -->

-1. **Shared brainstorm gate:** Run the same interview as standalone `odk-brainstorm` inline before writing ACs. Use the researched baseline for API signatures, parameter checks/defaults, return/error paths, state ownership and device variants. Focus decisions on observable outcomes: caller-visible failures, boundary inputs, timing/resource bounds and what each AC must prove. Preserve confirmed proposal decisions, but distinguish existing behavior from an agreed target.

<!-- ODK:reference contracts/skill-guides/brainstorm/interview.md -->
Read `contracts/skill-guides/brainstorm/interview.md` in full and apply its decision state, questioning, ODK coverage and completion gate before generating the specification.
<!-- /ODK:reference -->

   Pass the checked code baseline and confirmed decisions into the specification. Proceed to Step 0 only after completion or an explicit bypass, carrying unresolved items into the draft rather than inventing AC behavior.

0. Check for subsystem profile: read and follow `contracts/skill-guides/router/profiles.md` — if a profile matches, apply its `template_overrides.spec` (additional AC categories, fragments) and `agent_instructions.specify` before generating content
0.5. **Proposal 覆盖闭包**：生成 `spec.md` 前必须逐项读取 proposal 的目标、非目标、成功标准、设备差异、假设、开放问题和 API 设计属性，并生成 `### Proposal 覆盖矩阵`。每条必须映射到 AC、BR、EB、API metadata、明确 `N/A` 或 `Open`；`G-N` 仅出现在「来源目标」中是结构引用，不等于语义覆盖。业务规则必须闭环到可验证 AC；负向目标和假设必须转成负向 AC 或边界规则，不得只留作背景文字。
<!-- ODK:reference contracts/skill-guides/spec/api-specification.md -->
**Steps 1–5 — API metadata workflow (conditional):** If proposal.md `API/SDK` = 「是」, read and follow `contracts/skill-guides/spec/api-specification.md` in full before Steps 3–6. Generate the API contract skeleton, invoke the isolated API documentation subagent, merge documentation-only output, write the applicable `arkts-api-spec.yaml` and/or `c-api-spec.yaml`, and generate the `spec.md` API overview. If an isolated subagent is unavailable, fail this step; there is no main-session fallback. If `API/SDK` = 「否」, skip this workflow; keep the fixed API section and its non-involvement reason, and do not create either metadata file.
<!-- /ODK:reference -->
3. **Contract fact check:** Before generating spec, check its consequential behavior claims against the researched implementation, callers and test assertions. Cover relevant entry points, validation/defaults, observable errors and side effects, compatibility and configuration variants; new integrations and executable configuration changes also need this check.
   - Use source references for current facts and distinguish them from the confirmed target and unresolved assumptions. Search hits or declarations alone do not establish behavior.
   - Preserve stable consumer contracts in ACs; keep implementation paths and internal mechanisms in design or supporting evidence.
   - **Cross-repo interface confirmation**: If the change calls interfaces from another OpenHarmony repo, locate the upstream repo (from design.md module impact table or by asking the developer for the local path) and read the interface's actual implementation to confirm return value semantics, error conditions, threading constraints, and side effects. Do not assume interface behavior from header declarations alone. Record confirmed facts in the spec's verification mapping or code fact notes.
   - If code facts contradict assumptions from `proposal.md`, surface and resolve before writing ACs
   - For a genuinely greenfield module, state the missing baseline and inspect any available integration contract. Wording-only documentation changes need only the affected references checked.
4. Read template from `templates/ai/spec.md`
5. Generate or revise `spec.md` per the template for new/changed contract facts. Populate `### Proposal 覆盖矩阵` before writing AC/BR/EB prose, and use it as the semantic checklist while generating. If `API/SDK` = 「是」, first generate and validate the applicable metadata files, then generate the API overview from them; `spec.md` must not restate per-API specification tables. Fill in consumer-boundary error code values and interface signatures where discoverable from the code fact check (Step 3); private helpers and internal errors belong in design. Mark genuinely unknown contract values as `TBD` with a reason. Verification mapping and test hints describe stable acceptance scenarios, not test files, functions, commands, Red/Green or run evidence. For each `### US-N` section, fill the `**来源目标：**` field with the corresponding `G-N` goal IDs from `proposal.md ## 目标` (comma-separated if multiple, e.g. `G-1, G-2`). If `proposal.md` has no `G-N` numbered goals, write `G-?` as a placeholder and remind the user to add goal IDs to proposal.md.
6. If any proposal `资源开销审视` dimension is `required`, expand `资源验收契约` (`contracts/artifacts.yaml#resource_contract`). Table detail is subsystem-owned; ODK requires meaningful, non-placeholder content without imposing a measurement schema. Each 验收口径 must be an observable target (latency / fps / throughput / startup time / peak RAM / image delta) — never vague goals like「优化性能」.

## Key Rules

- **API 仓库为阻塞前置条件**：若 proposal.md `API/SDK` = 「是」，必须先获得开发者提供的本地 API 声明仓库路径（`interface_sdk-js` / `interface_sdk_c`；不一定是绝对路径，只要能定位到即可）并验证可读。仓库未就绪时 spec 阶段不得继续。
- **API 知识库闭包**：API 仓库根目录 `AGENTS.md` 是稳定知识入口。读取后必须继续解析本次 API 设计相关的引用知识，至少覆盖版本规则、声明注释规则、metadata schema、设备规则和适用语言特有规则。ODK 不得假设或写死 `interface_sdk-js` / `interface_sdk_c` 的内部目录结构；schema 与规则文档路径均由根 `AGENTS.md` 动态解析。知识区缺失时按知识区名称报告阻塞，不得猜测内部路径。
- **仓库声明的前置知识**：读取 API 仓根 `AGENTS.md` 的知识索引；若适用知识条目声明前置条件，必须按声明顺序先加载前置条件，再学习该条目。前置条件不可用时，停止生成 API 契约骨架并遵循 API 仓提供的指引；ODK 不内置或替代仓库前置知识。
- **Proposal 语义覆盖**：`spec.md` 必须包含 `### Proposal 覆盖矩阵`。机器校验中的 Goal→US coverage 只证明 G-N 被引用，不证明目标语义被展开；每个目标、非目标、假设和 API 设计事实都必须映射到具体 AC/BR/EB/metadata 位置，或显式 `N/A` / `Open`。
- **API 文档禁用词唯一数据源**：调用 API 文档 subagent 前，必须读取并传递 `contracts/api/forbidden-terms.yaml`；不得在 skill、checker 或其它文档中复制禁用词列表。
- **API 文档排版配置**：调用 API 文档 subagent 前，必须读取并传递 `contracts/api/document-style.yaml`。中文与 ASCII 字符之间是否加空格，以该配置的当前取值为准；未来需要调整时只修改该配置，不逐处修改文档。
- **文档上下文先行**：调用 API 文档 subagent 前，必须生成 `documentation-context.yaml`，只包含与该 API 直接相关且已确认的行为事实（单位、范围、默认值、非法值行为、优先级、影响/不影响范围、设备差异、生效时机等）。每条事实和文档要求必须绑定 API ID 与事实名；不得把 proposal 全文或无关 design/plan 上下文传给 subagent。
- **文档上下文机器校验**：subagent 返回后，必须先运行 `python3 "runtime/executables/check-api-documentation-context.py" --context <documentation-context.yaml> --output <api-doc-output.yaml> --skeleton <api-spec-skeleton.yaml>`，通过后才允许合并；该检查只做 API ID、参数、错误码与 skeleton 的契约闭包，并要求返回值具备双语文档描述；`returnType.text` 等契约字段仍归 metadata 所有，不在文档输出中回显，以及双语字段完整性和确认值覆盖，并拦截 API 文档禁用词，不冒充自然语言语义审查。
- **API 事实先解析再提问**：按「开发者显式确认 → API 仓库确定性规则 → 已确认代码/声明事实 → proposal 事实」的顺序解析。确定性规则可直接落盘并记录实际知识入口作为证据；例如版本规则将系统 `7.1` 映射为 API `26.1.0` 时，`since` 直接写 `26.1.0`，不得再询问开发者。只有所有权威来源耗尽、冲突或明确要求人工确认时才提问。
- **按语言选择模板**：ArkTS 使用 `templates/api/arkts-api-spec.yaml`，C 使用 `templates/api/c-api-spec.yaml`；归档文件名分别为 `arkts-api-spec.yaml` 和 `c-api-spec.yaml`；两者可同时存在，但不得混用两种语言的数据结构。
- **语言专属 API 元数据文件是唯一 API 契约源**：若 proposal.md `API/SDK` = 「是」，必须按实际语言生成 `arkts-api-spec.yaml` 和/或 `c-api-spec.yaml`，并在其中完成全面的 API 元数据定义（kind、签名、入参、返回值、权限、@syscap、@since、错误码、平台、模型、设备差异等全部维度）。`spec.md` 的 `## API 规格定义` 只保留概览和确认指引，不得重新展开逐 API 规格。
- **API 描述必须由隔离 subagent 生成**：若 proposal.md `API/SDK` = 「是」，接口定义三要素（含义/功能、使用场景、使用后效果）和接口使用五要素（相似接口差异、缺省配置、规格限制、生效机制、注意事项）必须由 API 文档 subagent 生成后合并进适用语言对应的 metadata 文件。subagent 不可用时 spec 阶段失败，禁止主会话内联生成、复用旧文案或从既有声明注释反推。
- **Subagent 只写文案，不改契约**：subagent 输出仅允许提供 description、参数描述、返回值描述和错误码描述；合并时必须校验 API ID 集合一致，并忽略其输出中的所有契约字段。
- Do not invent API signatures, error code values, or data structures. Resolve contradictions from code facts before writing ACs.
- Keep ACs concrete enough for the template's verification mapping; code mapping (AC→implementation files) lives in `execution-plan.md`.
- **保留 US-DFX 回填内容**：`spec.md` 可能在 design 阶段被 `odk-design` 第 6.4 步回填 `### US-DFX: 故障模式响应` 子节（故障模式 AC）及 `异常与边界规则`/`验证映射`/`测试设计提示` 的关联行。重新生成 `spec.md` 时必须保留该子节与关联行，不得因重建而丢失（design.md `### DFX 故障模式处置` 的关联 AC 悬空会使校验 FAIL）。
- AC 使用 Given/When/Then 格式：Given 前置条件；When 用户/业务可操作动作；Then 通过三层接口边界（public/system/inner API + 终端用户可感知）可观测的结果。
- AC 的 Then 禁止部件内部实现（数据结构/状态机/内部流程/算法）——移 `design.md`「状态归属与不变量」。判定：Then 能否仅凭公开接口判定？需查内部状态则移 design。
- **API 支持属性确认（条件触发）**：若 proposal.md `API/SDK` 维度 = 「是」，需在适用 metadata 文件的每个 API 上显式填写跨平台/元服务/卡片/FA-Stage 模型支持属性。
  - **重要：先查询根 `AGENTS.md` 引用的知识、proposal、已确认代码事实和既有开发者结论；只有无法从这些权威来源确认时才询问开发者，不得从无关上下文猜测或填写默认值**：
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

- **设备行为差异确认（条件触发）**：若 proposal.md `API/SDK` 维度 = 「是」，必须分析 API 的多设备行为差异并写入适用 metadata 文件对应 API 的设备支持与差异字段。分设备默认值或分设备行为只能由 `deviceDifferences` 表达；`description.defaultBehavior` 仅描述与设备无关的统一默认行为，否则写 `N/A` / `不适用`。
  - 通过仓库根 `AGENTS.md` 动态解析并加载其引用的设备知识文档（若存在），学习设备知识（设备类型枚举、差异行为类型、差异原因、设备移除规则、自然语言解析规则）；不得写死该文档的内部路径
  - 根据 API 的 `@syscap` 确定支持设备列表及起始版本
  - 必须询问开发者是否存在设备行为差异，**不得臆造**
  - 有差异时，将开发者自然语言描述解析为结构化数据，以中文列名+中文选项值展示表格供确认，**确认后才可落盘**
  - 差异行为包含至少一个正常值（功能正常/实现一致）→ 设备保留；不包含任何正常值 → 设备从支持列表移除

## Quality Boundary

- This skill owns profile application, code fact checking, contradiction handling, context loading, and output path.
- `spec.md` template owns required sections, AC format (Given/When/Then) + three-tier observability guidance, verification mapping.
- Internal implementation (data structures/state machines/flows/algorithms) owned by `design.md`; code mapping (AC→implementation files + verification status) owned by `execution-plan.md`.
- `runtime/executables/validate-artifacts-contract.py` owns machine-checkable AC coverage, verification mapping, and traceability checks.

## Session ID 追踪

生成 `spec.md` 后，调用脚本更新 sidecar（详见 `using-odk` 的 `## Session ID 追踪契约`）。**禁止手动操作 JSON**：

1. 获取当前 session ID（**当前对话**的系统提示 "Current conversation session ID: ses_xxx"）。
2. 调用脚本（原子性 read-append-write，不丢已有 log 条目）：

   ```sh
   python3 "runtime/executables/update-sessions-sidecar.py" \
     "<变更目录绝对路径>" "spec.md" "<当前session ID>" "odk-spec" "<action>"
   ```

3. 从脚本输出的 `---MIRROR---` 段提取 `sessions` 字段和 `## 会话记录` 表格，写入交付件 frontmatter + body 开头（frontmatter 之后、正文 `#` 标题之前）。

**关键**：sidecar `.sessions.json` 是权威源。即使 `spec.md` 的 frontmatter 或表格在 body 重生成时丢失，下一个 skill 从 sidecar 读取，数据不丢。脚本保证 sidecar 的原子追加。

## Output

Write to `codespec/changes/<repo-name>/<proposal-id>/spec.md`.

同时写入 `spec.md` 和（当 `API/SDK` = 是时）`arkts-api-spec.yaml` 和/或 `c-api-spec.yaml`。`spec.md` 固定包含 `## API 规格定义` 概览章节；若 `API/SDK` = 否，按 `不涉及：<具体理由>` 填写且不得创建任何 API metadata 文件。若 `API/SDK` = 是，适用 metadata 文件是唯一逐 API 契约源，包含 API 元数据、三要素/五要素描述、参数/返回值/错误码描述和设备行为差异；`spec.md` 仅保留 API 概览和确认指引。API 仓库路径/commit 与既有声明格式参考为 spec 阶段的过程信息，不写入 spec.md。

Do not generate `gates/` by default. If the user explicitly wants process evidence, record approval notes under an optional evidence directory such as `evidence/gates/`.

For lite with no design need, proceed to `{{CMD_PREFIX}}plan`; preserve any existing design. Otherwise suggest next step: run `{{CMD_PREFIX}}design` to generate the architecture design, which will reference spec AC numbers and resolve any TBD error codes or interface signatures.
