---
description: Generate or refresh execution-plan.md and task breakdown (dev + test + demo)
argument-hint: [item-dir]
---

Read:

- `{command_dir}/templates/execution-plan.md`

Then:

1. Work in the item directory from `$1`.
2. Break dev work into bounded tasks with explicit file scope, rule mapping, prerequisites, completion criteria, and execution mode.
3. Produce narrow-context task cards; do not re-inject all Stage 1-2 documents into every task.
4. Add verification expectations for the item and its profile, including phase-by-phase minimum verification.
5. **Create test task cards (task-T-*.md)** if `test-design.md` exists:
   - **向用户收集环境路径信息**（使用 AskUserQuestion）：
     - **必要问题**: "测试用例生成到哪个 XTS 目标工程目录？例如 `D:\xts_acts_0414\graphic\graphic3D`"
     - **必要问题**: "API 定义文件（.d.ts）的完整路径？"
     - **必要问题**: "选择编译验证方式？"（选项：`Linux build.sh 编译` / `Windows hvigorw 编译`）
     - **可选问题**: "是否需要编译验证？如果需要，请提供 xts_acts_path 和 sdk_path（Windows）或 oh_root（Linux）"
   - 收集到的路径和编译方式将写入每个 task-T 的"环境路径"段
   - **按测试目标分组**（不是按工具分组）：将 test-design.md 中的全部 TC 按测试目标（如"参数测试"、"状态机测试"、"CRUD 测试"）分组
   - **每个 task-T 必须覆盖完整的 TC 列表**，不能遗漏任何 TC。分组完成后做全量校验：∑(task-T 的 TC 数) = test-design.md 的 TC 总数
   - 每个 task-T 文件中，为每条 TC 标注**实现方式**：
     - 自动生成：列出工具调用参数（d.ts path, API list, syntax type）
     - 手写补充：说明需要手动编写的原因（无效值、边界值、异常路径、因子组合等）
   - 每个 task-T 文件包含：
     - **环境路径段**：output_target_path, d.ts_path, oh_root/xts_acts_path, sdk_path 等
     - 完整的 TC 编号列表（含实现方式标注）
     - AC 和 test case mapping（100% 覆盖）
     - Prerequisites（which dev tasks must complete first）
     - Completion criteria（all test cases implemented, quality check passed）
   - Use `task-T.md` template for each test task card
   - Test tasks are blocked by their corresponding dev tasks
   - **创建完成后，输出覆盖度校验报告**：列出 test-design.md 中的每条 TC 及其对应的 task-T 编号，确保无遗漏
   - **注意**: 如果测试任务分解和代码生成需要一步完成，可使用 `/ohos-test-generator <item-dir>` 代替本步骤 + `/ohos-test-gen`
6. **Create demo task cards (task-D-*.md)** if `test-design.md` exists and contains test point design content:
   - Analyze test-design.md to identify test points that can be mapped to interactive Demo UI
   - Determine the **domain** (e.g., ArkWeb, ArkUI, Ability) based on the APIs tested in test-design.md
   - Create one `task-D.md` per logical demo group (typically one task-D per subsystem/API area), containing:
     - **测试点范围**：从 test-design.md 中提取需要 Demo 覆盖的测试点列表
     - **领域配置**：目标 domain（对应 ohos-design-test-demo-pipeline reference/api-reference/ 下的目录）
     - **输入文件路径**：test-design.md（测试点设计）路径 + requirement.md（可选，补充上下文）路径
     - **输出目录**：Demo 工程输出路径
     - **Completion criteria**：demo_design.md 生成 + TestDemo/ 编译通过 + demo_code_manifest.md 自检全部通过
   - Demo tasks can run in parallel with test tasks (they share test-design.md as input)
   - Use `task-D.md` template for each demo task card
7. Do not modify production code; this command only prepares Stage 3 Plan outputs.
8. At the end, tell the user:
   - how many dev tasks, test tasks, and demo tasks were created
   - which tools are needed for test tasks
   - which domain is configured for demo tasks
   - the recommended next step is `/ohos-test-gen <item-dir>` to generate test code and demo apps, or `/ohos-test-generator <item-dir>` for task breakdown + generation in one step
