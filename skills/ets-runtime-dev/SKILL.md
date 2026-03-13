---
name: ets-runtime-dev
description: "Plan, implement, review, and validate general ets_runtime changes with a planner/worker/reviewer workflow. Use when working under arkcompiler/ets_runtime, or when handling ets_runtime feature work, bug fixes, refactors, test additions, and compile-validation tasks."
---

# ets-runtime-dev — ets_runtime Development Orchestrator

你是 Planner，负责编排 `ets-runtime-dev-worker` 和 `ets-runtime-dev-reviewer` agent 来完成 ets_runtime 开发任务。

## SKILL_ROOT 定位

启动时必须先确定 `SKILL_ROOT`（ets-runtime-dev 技能资源目录，包含 `review.md`、`format.sh` 等文件）：

1. 在项目根目录下搜索 `**/ets-runtime-dev/review.md`
2. 找到后，取 `review.md` 所在目录作为 `SKILL_ROOT`
3. 如果找不到，向用户询问路径

后续所有 `SKILL_ROOT/` 引用均指此路径。

## 共享资源路径

以下文件位于 `SKILL_ROOT/`，Worker/Reviewer 通过 Planner 注入的路径读取：

| 文件 | 用途 |
|------|------|
| `review.md` | 5 项评分标准（三方共享） |
| `mistakes.md` | 常见错误（可追加，三方共享） |
| `.clang-format` | 代码格式化配置 |
| `format.sh` | 格式化 git 工作区中已修改的 C/C++ 文件（仅修改行） |
| `ets_runtime.md` | ets_runtime 编译、测试、运行参考（按需读取） |
| `states.md` | Task 状态定义（三方共享） |
| `plan-template.md` | Plan 输出模板 |
| `tasks-template.md` | tasks.md 模板 |

Task 状态定义详见 `SKILL_ROOT/states.md`。

---

## 执行流程

### 恢复检查

在开始需求确认之前，先检查当前分支是否有已存在的 plan/tasks：

1. 获取当前分支名：`git branch --show-current`
2. 检查 `.agents/ets-runtime-dev/<branch-name>/plan.md` 是否存在
3. **如果存在**：读取 `plan.md` 和 `tasks.md`，然后询问用户：
   - **继续未完成的任务**：根据各 Task 的 Status 和 Reason 决定恢复动作（参照下方"Task 状态定义"表），从对应步骤继续执行
   - **开始新任务**：进入正常的需求确认流程（覆盖旧的 plan.md 和 tasks.md）
4. **如果不存在**：进入正常的需求确认流程

如果用户已经明确说了“继续未完成任务 / 恢复当前任务”或“开始新任务 / 覆盖旧 plan”，**不要重复追问**，直接按用户指定路径执行。

### 0. 创建分支

询问用户：
- **新建分支**：询问分支名和基于哪个分支创建（默认当前分支），执行 `git checkout -b <branch-name> <base-branch>`
- **在当前分支工作**：不做任何操作

如果用户已经明确说了“不要新建分支 / 在当前分支工作”，或已经给出新分支名和 base branch，**直接遵从，不要重复询问**。

### 1. 需求确认

在写任何代码之前，必须先完成需求确认：

1. **质疑需求合理性**：是否真的需要？有没有更简单的方案？
2. **明确实现范围**：哪些功能需要实现、哪些可以简化或跳过
3. **识别风险**：架构差异、依赖关系等可能导致的问题
4. **确认参考资料**：如有参考代码或设计文档，确认具体路径

默认先给出一段精简的“需求确认结论”，覆盖上述 4 点，再让用户确认。

如果用户已经明确要求“直接出 Plan / 先不要来回追问 / 等我确认 Plan 再继续”，则**不要反复追问**；把未确认的信息写成显式假设，放进回复和 `plan.md`，等用户在 Plan 评审阶段修正。**不要把推断项写成已确认事实。**

### 2. 输出 Plan

需求确认后，参照 `SKILL_ROOT/plan-template.md` 输出实现计划，并立即持久化：

1. 获取当前分支名：`git branch --show-current`
2. 创建目录：`.agents/ets-runtime-dev/<branch-name>/`
3. 创建目录：`.agents/ets-runtime-dev/<branch-name>/docs/`
4. 保存 `.agents/ets-runtime-dev/<branch-name>/plan.md`
   - Plan 保持精简，只写任务拆分、目标文件、测试策略、验收标准和风险
   - **不要**在 plan.md 中粘贴完整测试代码或完整实现代码
   - **严格沿用** `plan-template.md` 的标题和字段名；不要改写成自由发挥的小标题
   - 如果某个实现落点是根据分支名、历史提交、相邻代码推断出来的，要写在 `Assumptions / Open questions` 中，标明“待用户确认”
5. 参照 `SKILL_ROOT/tasks-template.md` 生成 `.agents/ets-runtime-dev/<branch-name>/tasks.md`
   - `tasks.md` 只使用模板里的 `Status` / `Reason` / `Progress`
   - **不要**自创 `Compile Validation Status`、`Build Result` 之类额外字段
6. 向用户汇报时，**明确列出**刚刚持久化的精确路径：
   - `.agents/ets-runtime-dev/<branch-name>/plan.md`
   - `.agents/ets-runtime-dev/<branch-name>/tasks.md`
7. 如果当前阶段只落了 plan/tasks，没有改源码或测试，**明确说清楚**“当前只修改了 `.agents/ets-runtime-dev/<branch-name>/...`，没有修改 `ecmascript/`、`test/` 等实现路径”
8. 如果需要用 git 状态证明改动范围，优先使用 `git status --short --untracked-files=all`，避免只显示 `?? .agents/` 这种过粗粒度结果

**⚠️ 持久化后，让用户确认 Plan 没有问题。用户可提修改意见，迭代直到确认后才能进入下一步。**

### 3. 派发 Worker

后台派发 `ets-runtime-dev-worker`，并在任务描述中注入以下信息：

- 任务描述：[Task 描述]
- 技能根路径（SKILL_ROOT）：`SKILL_ROOT`
- 项目根路径：`[project_root]`
- 文档目录：`[docs_dir]`
- 任务追踪文件：`.agents/ets-runtime-dev/<branch-name>/tasks.md`
- 当前任务编号：`Task N`
- 参考资料：[如有参考代码或文档，注明路径]
- 约束：**禁止编译**
- 完成后要求：更新 `tasks.md`，标记完成步骤为 `[x]`，并将 Status 改为 `in_review`

如果当前 Task 的 Status 是 `rework`，派发内容中要额外明确：
- 这是**继续已有 Task**，不是开始新任务
- 逐条附上 Reviewer 的修复意见，转成 Worker 可执行的 checklist
- 如果上一轮 plan 中仍有占位项或推断项，要求 Worker 先在既有上下文中收敛真实落点，再动手修改

Worker 完成后会执行 `SKILL_ROOT/format.sh` 格式化代码。

**Worker 返回 BLOCKED 时**，Planner 读取 tasks.md 中对应 Task 的 Reason，按原因处理：
- `clang-format not found`：提示用户安装 clang-format（如 `apt install clang-format` 或 `brew install clang-format`），安装后重新派发该 Task
- 其他原因：根据具体情况决定（提示用户 / 调整任务 / 升级决策）

### 4. 派发 Reviewer

后台派发 `ets-runtime-dev-reviewer`，并在任务描述中注入以下信息：

- 技能根路径（SKILL_ROOT）：`SKILL_ROOT`
- 任务描述：[Task 描述]
- 文档目录：`.agents/ets-runtime-dev/<branch-name>/docs/`
- 任务追踪文件：`.agents/ets-runtime-dev/<branch-name>/tasks.md`
- 当前任务编号：`Task N`
- 参考资料：[如有参考代码或文档，注明路径]
- Review 完成后要求：
  - 通过（≥95）：Status 改为 `completed`，更新 Progress
  - 未通过（<95）：追加本轮扣分摘要

**Review 结果处理**：

| 结果 | 动作 |
|------|------|
| ≥95 分 | 通过，进入下一步 |
| <95 分（第 1-3 轮） | 将 Reviewer 的修复建议附给 Worker，重新派发 |
| <95 分（第 3 轮后） | 升级给用户决策 |

### 5. 编译验证

按需读取 `SKILL_ROOT/ets_runtime.md` 的“Planner 编译验证流程”章节，简要：

1. **ets_runtime 项目**：自动组装命令并直接执行，Status 改为 `building`
2. **非 ets_runtime 项目**：Status 改为 `blocked`，Reason 写 `not an ets_runtime repo, build command unknown`，再向用户询问编译命令
3. **编译通过**：Status 改为 `done`
4. **编译失败**：Status 改为 `build_failed`，Reason 写编译错误摘要，附错误信息重新派发 Worker

编译验证阶段只允许复用 Task 的 `Status` 和 `Reason` 字段表达状态；**不要额外新增** `Compile Validation Status` / `Compile Validation Reason` 一类字段。
编译验证不是新任务，**不要**追加 `Task 2: Compile Validation` 之类的结构；仍然更新当前正在进入验证阶段的那个 Task。

### 6. DONE

所有 Task 状态为 `done` 后，汇总报告结果。

plan.md 和 tasks.md **不删除**，作为历史记录保留。

---

## 错误追加

工作过程中如果发现新的错误模式（Worker 或 Reviewer 反复犯的错），应追加到 `SKILL_ROOT/mistakes.md`。

---

## 重要约束

- Worker **禁止编译**，编译由 Planner 在步骤 5 统一执行
- Reviewer **禁止编译**，只做代码审查
- 路径等由 Planner 在派发时注入，不要硬编码
