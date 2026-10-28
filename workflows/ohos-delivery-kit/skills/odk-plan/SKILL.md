---
name: odk-plan
description: "Use when writing ODK execution-plan.md (AC-to-Task traceability, file-level scope, anti-fake checks). Default template-driven, zero plugin dependencies. Use after design.md."
license: MIT
---

# ODK Plan

## Prerequisites

- `spec.md` with numbered AC list
- `design.md` with architecture decisions (required for state ownership fields when design declares complex state)

## Input

1. Read `proposal.md` to check `API/SDK` dimension
2. Read `spec.md` AC list
3. If `design.md` contains `状态归属与不变量`, read the declared dimensions — these map to the state ownership fields each Task must fill in
4. If `design.md` contains `### DFX 故障模式处置`, read the disposition rows — ACs in the `关联 AC` column are fault-mode interception items and must be traced to Tasks (see Self-Review)
5. **国际化依赖分析（`proposal.md` 的 `国际化` 维度中判断国际化 = 「是」 时）**：读取 `design.md` 的 `## 国际化依赖分析` 章节，提取调用场景、仓路径、接口/方法，按仓路径分组作为任务生成输入

## Steps

Task 列表的「AC 映射」必须填写 AC 编号；不直接关闭 AC 的文档/基础设施 Task 填 `N/A（简短理由）`，不可留空、只写 `N/A` 或用 `—`。每条 AC 仍须在追溯表中关联 Task 和验证方式。

For configuration-dependent steps, use the effective-configuration command defined in `using-odk`; do not merge installation files independently. Stop on config errors. Existing execution-plan commands remain authoritative until explicitly changed.

0. Check for subsystem profile: read and follow `contracts/skill-guides/router/profiles.md` — if a profile matches, apply its `template_overrides.execution-plan` (additional prohibitions) and `agent_instructions.plan` before generating content
1. Read template from `runtime/assets/templates/ai/execution-plan.md`
2. **API 声明文件任务（条件触发）**：若 proposal.md `API/SDK` = 「是」，必须在所有任务的最前面插入一个 API 声明文件修改任务（排在 Task-1），任务内容为"根据 spec.md `## API 规格定义` 修改声明文件"。该任务排在第一位的原因是：后续功能实现任务依赖声明文件的修改结果，声明文件未完成时其他任务无法开展。
3. Generate `execution-plan.md` per the template. Fill the required traceability, task detail, verification, and code-scope fields enough to pass artifact contract validation. For each Task, fill「任务间接口」（Produces=供后续 Task 依赖的接口签名/错误码/innerAPI/数据结构，Consumes=来自前置 Task 的契约；无跨 Task 契约写「无」），让只读单 Task 的执行者也能对齐跨 Task 命名与签名。
   **构建与验证环境（必填）**：在生成 `execution-plan.md` 前读取 `build_products`、`build_product`、`build_command`、`emulator_command`、`test_command`（`odk_config_ext.yaml` 覆盖默认配置），先确认本次产品，再生成具体命令。
   <!-- ODK:reference contracts/skill-guides/delivery/build-products.md -->
   Read `contracts/skill-guides/delivery/build-products.md` to resolve the configured list, generate a numbered selection menu, and record the list and selected product. Do not hard-code a two-product menu or build every listed product.
   <!-- /ODK:reference -->
   确认产品后、写计划前，执行设备版本选择：
   <!-- ODK:reference contracts/skill-guides/delivery/device-version.md -->
   Read `contracts/skill-guides/delivery/device-version.md`: QEMU (`arm64_virt`) skips the daily question; every other product asks daily versus existing firmware. Record the user's choice and preparation method in the plan, even when no automatic flashing skill is available.
   <!-- /ODK:reference -->
   用确认后的产品名替换 `{product}` 占位符，然后：
   - 将完整候选列表写入 `可选编译产品`，将用户确认的单个产品写入 `编译产品`
   - 将解析后的具体命令写入 `## 构建与验证环境` 表；`emulator_command` 仅当编译产品为 `arm64_virt` 时填入，其他产品（rk3568 等物理板）该行留空或省略；`test_command` 若为空则根据 Task 的文件范围、测试框架约定推断并填入，推断结果需标注「推断：<理由>」
   - 实现阶段直接读本表，不再查 config
   For each Task's `验证命令` field: write the full concrete build + test command for that Task specifically:
   - **编译 target 推断**：根据 Task 的文件范围（`Files` 表）推断最窄的编译 target：
     - 文件范围集中在单一模块（同一 `bundle_name` 或同一组件目录）→ 查该模块的 `BUILD.gn` 或 `bundle.json` 获取真实构建 target 名称（`name` / `module_name` 字段，不是 `bundle_name`），在 `build_command` 后追加 `--target <真实target名>`，只编译该模块
     - 文件范围跨多个模块或涉及框架层 → 使用 `## 构建与验证环境` 表里的全量编译命令，不追加 target
     - 仅修改测试文件、配置文件或 API 声明文件（无 C++/ArkTS 业务代码改动）→ `验证命令` 字段只写测试命令，不写编译命令（`odk-implement` 会识别此形状并跳过编译步骤）
   - 将推断结果和理由写入 Task 的 `验证命令` 字段，格式：`<build_cmd> [--target <module>] && <test_cmd>`，不写占位符
   If any proposal `资源开销审视` dimension is `required`, expand `资源验证矩阵` (`contracts/artifacts.yaml#resource_contract`). Commands/evidence layout are subsystem-owned (often `evidence/resource/`); ODK requires the section and meaningful, non-placeholder content without imposing a subsystem measurement schema.
   涉及国际化接口调用的任务时，在「任务间接口」或备注中记录调用场景、仓路径、接口/方法，便于 implement 阶段使用。 **禁止遗漏或虚构**
4. Populate `execution-plan.md` AC-to-Task 追溯 (AC / Task / 验证状态) with the Task assignments.
5. Self-Review the generated `execution-plan.md` before handing off — find issues and fix them inline, then move on without a second self-review pass. Self-review is an AI self-check only; it does not replace human approval or `odk-review`, and the Phase Gate in `using-odk` still applies:
   - **跨 Task 契约一致性**：逐 Task 比对「任务间接口」——后续 Task 的 Consumes 是否对得上某个前置 Task 的 Produces（函数名/参数/错误码/数据结构）；`clearLayers()` 在 TASK-3 产出、TASK-7 却写成 `clearFullLayers()` 就是 bug，就地改正。
   - **占位符扫描**：确认无 `TBD`/`TODO`/`适当处理`/`补充测试`/`参考上文` 等不可执行占位（见「禁止项」）。
   - **Spec 覆盖**：确认「AC 到 Task 追溯」每个 AC 都有 Task 承接；发现未覆盖的 spec 要求就补 Task。
   - **FM 覆盖（故障模式拦截项）**：`design.md` `### DFX 故障模式处置` 关联的每个 AC 都必须有 Task 承接，且该 Task 的验证命令走故障注入或异常路径（引用处置表"验证方式/证据"列的手段，如 `手段｜注入点｜注入内容`），不得只跑正常路径回归；这些 AC 不得列入「实现边界 → 可后置」。
   四项都干净则进入下一步（写出 `execution-plan.md`），等待人工审批。

## Quality Boundary

- This skill owns routing, profile application, context loading, and populating `execution-plan.md` AC-Task 追溯.
- `execution-plan.md` template owns required tables and fields.
- `runtime/executables/validate-artifacts-contract.py` owns machine-checkable traceability and table completeness.

## Output

Write to `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md`

Suggest next step: run `{{CMD_PREFIX}}implement` to begin Task-by-Task implementation.
