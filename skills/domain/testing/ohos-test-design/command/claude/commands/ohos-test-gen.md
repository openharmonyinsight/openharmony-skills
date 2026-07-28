---
description: Generate test code and demo apps by invoking XTS/CAPI/Hypium/Demo skills
argument-hint: [item-dir]
---

Read these references first:

- `{command_dir}/templates/config.md`
- `{command_dir}/templates/task-T.md`

Then:

1. Work in the item directory from `$1`.
2. Read `config.md` to get the **测试代码生成** skill mapping. Use the configured skills instead of hardcoded defaults.
3. Read `test-design.md` to get the API coverage matrix, tool matching, and **full TC list with AC mapping**.
4. **Read detailed test case steps from `test-design-output/batches/`**: this directory contains batch files (`batch_01.md`, `batch_02.md`, ...) produced by ohos-design-test-coordinator, each with **detailed preconditions, test steps (with specific data values), and expected results**. These are the authoritative source for test code generation — NOT the TC summaries in test-design.md.
5. Read all `task-T-*.md` files (created by `/ohos-plan`) to get test task cards with tool invocation parameters and per-TC implementation mode.
6. Read all `task-D-*.md` files (created by `/ohos-plan`) to get demo task cards with test point scope and domain configuration.

---

## 环境路径收集（必执行）

**在开始任何生成工作之前，必须确认以下环境信息。** 这些信息是 XTS 生成 skill 的必要输入。

从 task-T 文件的"工具调用指令"段读取环境路径。如果 task-T 中未填写或信息不完整，**必须向用户询问**：

**必要信息：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `output_target_path` | 测试用例生成的目标工程路径（xts_acts 下的子系统目录） | `D:\xts_acts_0414\graphic\graphic3D` |
| `d.ts_path` | API 定义文件（.d.ts）的完整路径 | `C:\Users\xxx\SceneBoidsSim.d.ts` |
| `build_method` | 编译验证方式 | `linux_build_sh` / `windows_hvigorw` |

**可选信息（未提供时跳过相关步骤）：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `oh_root` | OpenHarmony 源码根目录（Linux 平台） | `/home/user/openharmony` |
| `xts_acts_path` | XTS 兼容性测试套根目录 | `D:\xts_acts` |
| `sdk_path` | OpenHarmony SDK 路径 | `C:\Users\xxx\Sdk\openharmony` |
| `deveco_studio_path` | DevEco Studio 安装路径 | `D:\DevEco Studio` |

**收集方式：**

1. 优先从 task-T 文件的"环境路径"段读取
2. 如果 task-T 中缺少必要信息，使用 AskUserQuestion 向用户询问
3. 用户回答后，将收集到的路径写入各 task-T 文件的"环境路径"段（如果尚未填写）

---

## 编排策略：command 负责编排，skill 负责执行

**职责划分：**
- **command（本文件）**：读取任务卡片 → 收集环境路径 → 按 task 分配 → 为每个 task 准备输入 → 调用 skill → 汇总结果
- **skill（ohos-test-arkts-xts-generation 等）**：接收输入 → 按 Phase 1-10 流程执行（API 解析 → 代码生成 → 质量检查 → 编译验证 → 覆盖率）→ 输出结果

**禁止 command 重新实现 skill 已有逻辑。** 如果 skill 的某个 Phase 有缺陷，应修复 skill 而非在 command 中绕过。

---

## 7. 代码生成（按 task 调用 skill）

### 7.1 准备共享上下文（一次性，所有 task 共用）

在调用 skill 前，command 先准备以下共享信息，传递给每个 skill 调用：

**a) API 签名参考（必须准备）**：
- 用 `Read` 读取 `d.ts_path` 指向的 `.d.ts` 文件**完整内容**
- 提取所有被测 API 及其依赖 API 的精确签名
- 读取 `output_target_path` 下 1-2 个现有 `*.test.ets` 文件，提取 API 使用模式
- 整理为结构化的 API 签名摘要

**b) TC 详细步骤（按 task 分发）**：
- 对每个 task-T，从 batch 文件中提取该 task 负责的 TC 条目（预置条件、测试步骤、预期结果）
- 这些是代码生成的权威输入源

**c) ArkTS 语法约束摘要（所有 task 共用）**：
- 从 skill 的 `references/conventions/arkts_standards.md` 提取编译级禁止项：
  1. 禁止嵌套函数声明
  2. 禁止对象展开 `{...obj}`
  3. 禁止 `any`/`unknown` 类型
  4. 禁止对象字面量作为类型
  5. 禁止未类型化对象字面量
  6. 必须箭头函数
  7. 所有变量显式类型注解
  8. async it() 用 `async (done: Function) => {}`
  9. 同步 it() 不需要 done

### 7.2 读取 task-T 的"对接工具"字段，直接调用对应 skill

**对每个 task-T 文件，从其元数据表的"对接工具"字段读取工具名称，直接调用该 skill。不做模糊匹配或二次解析。**

task-T 模板定义的合法值（来自 task-T.md 模板）：
- `ohos-test-arkts-xts-generation` — ArkTS XTS 测试生成
- `ohos-test-capi-xts-generation` — CAPI Native 测试生成
- `gtest` — C++ 测试，手写
- `Hypium` — ArkTS 测试，手写
- `无` — 跳过自动生成

**如果 task-T 中的"对接工具"值不是上述合法值，停止并向用户报告该 task-T 的对接工具值，询问应使用哪个 skill。**

**分组执行：** 将所有 task-T 按"对接工具"字段分组，同一类型的 task 共享上下文：

| 对接工具 | 共享上下文 |
|---------|-----------|
| ohos-test-arkts-xts-generation | API 签名参考 + ArkTS 约束 + 现有测试模式 |
| ohos-test-capi-xts-generation | .h 文件解析 + N-API 模板 |
| gtest / Hypium | TC 详细步骤 |
| 无 | 跳过 |

### 7.3 按解析结果调用对应 skill

#### 7.3.1 ohos-test-arkts-xts-generation（XTS ArkTS 测试）

调用时传入以下参数：

```
invoke ohos-test-arkts-xts-generation with:
  input:
    - d.ts_path: {环境路径收集的 d.ts 路径}
    - output_target_path: {环境路径收集的目标工程路径}
    - target_apis: {task-T 中指定的被测 API 列表}
    - syntax_type: {从 task-T 读取，如 ArkTS-Dyn / ArkTS-Sta}
    - tc_list: {该 task-T 负责的 TC ID 列表，来自 test-design.md}
    - tc_detailed_steps: {从 batch 文件提取的该 task 的 TC 详细步骤}
    - api_signature_reference: {7.1a 步骤准备的 API 签名摘要}
    - existing_test_patterns: {7.1a 步骤从现有测试文件提取的 API 使用模式}
    - arkts_constraints: {7.1c 步骤的 ArkTS 语法约束摘要}
    - env:
        oh_root / xts_acts_path / sdk_path / deveco_studio_path / build_method
    - generation_scope: positive + negative + boundary + combination
  execution:
    - 严格按 skill 的 Phase 3→5→7→8 流程执行
    - Phase 3 (API 解析): 参考 api_signature_reference，深度学习每个 API 的签名和依赖
    - Phase 5 (代码生成): 基于 Phase 3 知识库 + batch TC 步骤生成代码，严格遵守 arkts_constraints
    - Phase 7 (格式验证): 运行 check-test-code-quality
    - Phase 8 (编译验证): 使用 build_method 指定的方式编译，失败自动修复（最多3次）
  skip_phases: [Phase 1 (config已在command中加载), Phase 2 (无覆盖率报告), Phase 4 (设计已在test-design.md中), Phase 6 (注册由command统一处理), Phase 9 (覆盖率可选), Phase 10 (输出由command汇总)]
```

**当使用 Task 工具并行启动子代理时**，每个子代理的 prompt 必须包含：
1. skill 的完整指令（通过 `skill` 工具加载 ohos-test-arkts-xts-generation）
2. `api_signature_reference` 的完整内容
3. `existing_test_patterns` 的完整内容
4. `arkts_constraints` 的完整内容
5. 该 task 的 `tc_detailed_steps` 完整内容
6. 明确指示：**只能使用 api_signature_reference 中列出的 API，禁止猜测不存在的 API**

#### 7.3.2 ohos-test-capi-xts-generation（CAPI Native 测试）

调用时传入以下参数：

```
invoke ohos-test-capi-xts-generation with:
  input:
    - h_file_path: {task-T 中指定的 .h 头文件路径}
    - target_functions: {task-T 中指定的 C API 函数列表}
    - output_target_path: {环境路径收集的目标工程路径}
    - env:
        oh_root / xts_acts_path / sdk_path / build_method
```

CAPI skill 自行执行其内部的 N-API 包装 + ETS 测试生成 + 编译验证流程。

#### 7.3.3 gtest / Hypium（手写测试）

当"对接工具"为 `gtest`、`Hypium` 或 `无` 时：
- 从 task-T 的"模式 C：手写"段读取测试模板
- 直接基于 batch 文件中的 TC 详细步骤生成测试代码
- 不调用 XTS skill，使用 task-T 模板中的代码骨架

### 7.4 Demo 任务

8. For each demo task (task-D-*.md), invoke the **ohos-design-test-demo-pipeline** skill:
   - Read task-D to extract: test point scope, domain configuration, input file paths, output directory
   - Invoke `ohos-design-test-demo-pipeline` skill with the task-D parameters
   - After completion, verify outputs exist: `demo_design.md`, `TestDemo/`, `demo_code_manifest.md`
   - Check `demo_code_manifest.md` self-check results

---

## 9. 汇总报告

所有 skill 执行完毕后，汇总各 task 的结果输出给用户：

- which skills were invoked and what they produced (file paths)
- **TC coverage gap**: list any TCs from test-design.md that were NOT covered by generated code and need manual completion
- AC coverage status (covered / uncovered ACs)
- quality check results (0 Critical = pass)
- **build verification results per task**: PASS/FAIL for each task-T, compilation errors if any
- **Demo generation results**: for each task-D, report demo_design.md status, TestDemo/ compilation status, and demo_code_manifest.md self-check results
- the recommended next step is to run the generated tests after corresponding Dev Tasks are complete

10. Do not modify production code.
