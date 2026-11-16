---
name: odk-plan
description: "Use when writing ODK execution-plan.md (AC-to-Task traceability, file-level scope, anti-fake checks). Default template-driven, zero plugin dependencies. Use after design.md."
license: MIT
---

# ODK Plan

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

- `spec.md` with numbered AC list
- `design.md` when required by the effective contract; lite may omit it and record concise design constraints in the plan. Read and retain any existing design regardless of level.

## Confirm the build product before planning

First classify the plan's verification scope. If every Task uses repository-local
host tests/document checks and no target build, emulator or device, record
`验证范围=host-only` plus actual commands in the environment section and skip
product/firmware selection below. Do not invent a product for that scope.
For every target-build/device plan, the following selection remains mandatory.

Before generating a plan, resolving `{product}`, or invoking any planning bridge,
run `python3 runtime/executables/lib/odk_repository.py --build-product-options`
(source checkout: `python3 scripts/lib/odk_repository.py --build-product-options`).
This returns the effective candidate list and menu default, with no product selected.

<!-- ODK:reference contracts/skill-guides/delivery/build-products.md -->
Read `contracts/skill-guides/delivery/build-products.md`. Present the numbered
menu and wait for the user's explicit product choice before writing the plan.
Reuse an actual product choice already made for this plan; configuration alone,
autonomous mode or a general request to use recommendations does not confirm it.
<!-- /ODK:reference -->

Planning records commands; it does not execute compilation. Without a confirmed
product, stop before generating the build environment or any build command.

## API hard-migration gate

If `proposal.md` marks `API/SDK` as `是`, run the design gate before planning:

1. `spec.md` must reference applicable `arkts-api-spec.yaml` and/or `c-api-spec.yaml`.
2. `spec.md` must state `API 契约版本 | 1.0.0`, and `design.md` must state `**API 契约版本：** 1.0.0`.
3. The generated `execution-plan.md` input table must contain `| API Contract Version | 1.0.0 | ... |`; this is a read-only chain marker.
4. `design.md` must exist when required by the effective contract and must not predate the language-specific API metadata chain. When design contains an API baseline/summary, it must not reference legacy `api-spec.yaml` or Markdown per-API specifications as its contract source.
4. All applicable metadata files must exist, parse, and pass the API metadata contract.
5. Any legacy or inconsistent chain is a spec/design input failure. Stop and route a recognizable 0.14 legacy API Markdown chain to `{{CMD_PREFIX}}upgrade-api-chain`; if the assistant cannot resolve every fact, require restart from `proposal`/`odk-spec`. Do not repair the contract in plan.
6. For a blocking mismatch, report every affected artifact with its declared version, required version `1.0.0`, the reason, and this action text verbatim; never suggest manually editing version fields:
   ```text
   Action:
   Restart from proposal, rerun spec and design, then generate the plan.

   Required flow:
   proposal -> spec -> design -> plan

   Migration guide:
   docs/migrations/0.15.0-api-metadata-hard-migration.md
   ```

## Input

1. Read `proposal.md` to check `API/SDK` dimension
2. Read `spec.md` AC list
3. If `design.md` contains `状态归属与不变量`, read the declared dimensions — these map to the state ownership fields each Task must fill in
4. If `design.md` contains `### DFX 故障模式处置`, read the disposition rows — ACs in the `关联 AC` column are fault-mode interception items and must be traced to Tasks (see Self-Review)
5. **国际化依赖分析（`proposal.md` 的 `国际化` 维度中判断国际化 = 「是」 时）**：读取 `design.md` 的 `## 国际化依赖分析` 章节，提取调用场景、仓路径、接口/方法，按仓路径分组作为任务生成输入

## Steps

<!-- ODK:reference contracts/skill-guides/spec/contract-boundary.md -->
Read `contracts/skill-guides/spec/contract-boundary.md`. Turn spec acceptance
scenarios into concrete test files/functions, commands and Red/Green verification
here. Update affected Tasks/results for an implementation change without writing
test implementation or run evidence back into an unchanged spec.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/delivery/change-impact.md -->
For code Tasks, read `contracts/skill-guides/delivery/change-impact.md` before
fixing the file scope and verification steps. Check usable project LSP/AST
capabilities, identify affected paths and assign their changes/tests to Tasks;
use the documented fallback when tools are unavailable. Keep evidence in the plan.
<!-- /ODK:reference -->

Task 列表的「AC 映射」必须填写 AC 编号；不直接关闭 AC 的文档/基础设施 Task 填 `N/A（简短理由）`，不可留空、只写 `N/A` 或用 `—`。每条 AC 仍须在追溯表中关联 Task 和验证方式。

For configuration-dependent steps, use the effective-configuration command defined in `using-odk`; do not merge installation files independently. Stop on config errors. Existing execution-plan commands remain authoritative until explicitly changed.

0. Check for subsystem profile: read and follow `contracts/skill-guides/router/profiles.md` — if a profile matches, apply its `template_overrides.execution-plan` (additional prohibitions) and `agent_instructions.plan` before generating content
1. Read template from `templates/ai/execution-plan.md`
2. **API 声明文件任务（条件触发）**：若 proposal.md `API/SDK` = 「是」，必须先确认适用的 `arkts-api-spec.yaml` 和/或 `c-api-spec.yaml` 存在且通过结构校验，然后在所有任务的最前面插入一个 API 声明文件生成任务（排在 Task-1），任务内容为"根据适用 metadata 文件生成 `.d.ts` / `.d.ets` / `.h` 声明文件"。该任务排在第一位的原因是：后续功能实现任务依赖声明契约，声明文件未完成时其他任务无法开展。缺失或非法的 metadata 文件 是 spec 阶段问题，不得在 plan 阶段补写。
3. Generate `execution-plan.md` per the template. Fill the required traceability, task detail, verification, and code-scope fields enough to pass artifact contract validation. For each Task, fill「任务间接口」（Produces=供后续 Task 依赖的接口签名/错误码/innerAPI/数据结构，Consumes=来自前置 Task 的契约；无跨 Task 契约写「无」），让只读单 Task 的执行者也能对齐跨 Task 命名与签名。
   **风险分级**：按 `contracts/skill-guides/delivery/task-review.md` 为每个 Task 写初始 `风险等级`
   与判断依据。命中任一 R2 触发项（公共声明/接口、跨仓调用、IPC、权限/认证、并发/异步/回调、
   构建清单、资源/国际化、native↔ArkTS 边界、公共常量/错误码）写 `R2`；单模块代码或测试写 `R1`；
   仅文档/注释或不可执行配置写 `R0` 并给理由。代码变更不得写 `R0`。
   **构建与验证环境（必填；host-only 按上述例外记录实际主机验证）**：在生成 `execution-plan.md` 前读取 `build_products`、`build_product`、`build_command`、`emulator_command`、`test_command`（`odk_config_ext.yaml` 覆盖默认配置），先确认本次产品，再生成具体命令。
   Reuse the product confirmed in the pre-planning step; do not substitute `build_product` directly. Record the actual user response in `产品选择确认`.
   确认产品后、写计划前，执行设备版本选择：
   <!-- ODK:reference contracts/skill-guides/delivery/device-version.md -->
   Read `contracts/skill-guides/delivery/device-version.md`. Record `验证范围`: `build-only` needs no runtime target; `emulator`/`device` require a separately confirmed `验证产品` and `验证目标确认`. Only `device` asks daily versus existing. Never derive these choices from the concrete or abstract build name.
   <!-- /ODK:reference -->
   按 build-products 指南运行 `--resolve-product-commands`：所有命令中的 `{product}`/`{build_product}` 共用编译与 out/ 目录名；`{validation_product}` 仅显式指定验证目标，然后：
   - 将完整候选列表写入 `可选编译产品`，将用户确认的单个产品写入 `编译产品`
   - 将验证范围、验证产品、实际目标确认及解析命令写入环境表；仅 `emulator` 填模拟器命令，其他范围省略或填 `N/A`。`test_command` 为空时按 Task 范围推断并标注依据；build-only 无测试时填 `N/A`，不因此要求设备。
   - 实现阶段直接读本表，不再查 config
   For each Task's `验证命令` field: write the full concrete build + test command for that Task specifically:
   - **编译 target 推断**：根据 Task 的文件范围（`Files` 表）推断最窄的编译 target：
     - 文件范围集中在单一模块（同一 `bundle_name` 或同一组件目录）→ 查该模块的 `BUILD.gn` 或 `bundle.json` 获取真实构建 target 名称（`name` / `module_name` 字段，不是 `bundle_name`），在 `build_command` 后追加 `--target <真实target名>`，只编译该模块
     - 文件范围跨多个模块或涉及框架层 → 使用 `## 构建与验证环境` 表里的全量编译命令，不追加 target
     - 仅修改测试文件、配置文件或 API 声明文件（无 C++/ArkTS 业务代码改动）→ `验证命令` 字段只写测试命令，不写编译命令（`odk-implement` 会识别此形状并跳过编译步骤）
   - 将推断结果和理由写入 Task 的 `验证命令` 字段，格式：`<build_cmd> [--target <module>] && <test_cmd>`，不写占位符
   If any proposal `资源开销审视` dimension is `required`, expand `资源验证矩阵` (`contracts/artifacts.yaml#resource_contract`). Commands/evidence layout are subsystem-owned (often `evidence/resource/`); ODK requires the section and meaningful, non-placeholder content without imposing a subsystem measurement schema.
   涉及国际化接口调用的任务时，在「任务间接口」或备注中记录调用场景、仓路径、接口/方法，便于 implement 阶段使用。 **禁止遗漏或虚构**
4. Populate `execution-plan.md` AC-to-Task 追溯 (AC / Task / 验证状态) with the Task assignments. Include Verification Final Status=Blocked until executed; preserve existing results only for unchanged inputs. Keep any existing 问题闭环 dispositions and create rows only for real findings under `contracts/skill-guides/delivery/feedback.md`.
5. Self-Review the generated `execution-plan.md` before handing off — find issues and fix them inline, then move on without a second self-review pass. Self-review is an AI self-check only; it does not replace human approval or `odk-review`, and the Phase Gate in `using-odk` still applies:
   - **跨 Task 契约一致性**：逐 Task 比对「任务间接口」——后续 Task 的 Consumes 是否对得上某个前置 Task 的 Produces（函数名/参数/错误码/数据结构）；`clearLayers()` 在 TASK-3 产出、TASK-7 却写成 `clearFullLayers()` 就是 bug，就地改正。
   - **占位符扫描**：确认无 `TBD`/`TODO`/`适当处理`/`补充测试`/`参考上文` 等不可执行占位（见「禁止项」）。
   - **Spec 覆盖**：确认「AC 到 Task 追溯」每个 AC 都有 Task 承接；发现未覆盖的 spec 要求就补 Task。
   - **FM 覆盖（故障模式拦截项）**：`design.md` `### DFX 故障模式处置` 关联的每个 AC 都必须有 Task 承接，且该 Task 的验证命令走故障注入或异常路径（引用处置表"验证方式/证据"列的手段，如 `手段｜注入点｜注入内容`），不得只跑正常路径回归；这些 AC 不得列入「实现边界 → 可后置」。
   - **影响路径核对**：按共享指南核对入口/实现/配置路径的处置及测试，并记录共享文件或接口的 Task 之间的对应关系和检查结果；未查清范围如实保留，不能以 AC 追溯齐全代替影响范围检查。
   完成上述检查后写出 `execution-plan.md`，等待人工审批。

## Quality Boundary

- This skill owns routing, profile application, context loading, and populating `execution-plan.md` AC-Task 追溯.
- `execution-plan.md` template owns required tables and fields.
- `runtime/executables/validate-artifacts-contract.py` owns machine-checkable traceability and table completeness.

## Session ID 追踪

生成 `execution-plan.md` 后，调用脚本更新 sidecar（详见 `using-odk` 的 `## Session ID 追踪契约`）。**禁止手动操作 JSON**：

1. 获取当前 session ID（**当前对话**的系统提示 "Current conversation session ID: ses_xxx"）。
2. 调用脚本（原子性 read-append-write，不丢已有 log 条目）：

   ```sh
   python3 "runtime/executables/update-sessions-sidecar.py" \
     "<变更目录绝对路径>" "execution-plan.md" "<当前session ID>" "odk-plan" "<action>"
   ```

3. 从脚本输出的 `---MIRROR---` 段提取 `sessions` 字段和 `## 会话记录` 表格，写入交付件 frontmatter + body 开头（frontmatter 之后、正文 `#` 标题之前）。

**关键**：sidecar `.sessions.json` 是权威源。即使 `execution-plan.md` 的 frontmatter 或表格在 body 重生成时丢失，下一个 skill 从 sidecar 读取，数据不丢。脚本保证 sidecar 的原子追加。

## Output

Write to `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md`

Suggest next step: run `{{CMD_PREFIX}}implement` to begin Task-by-Task implementation.
