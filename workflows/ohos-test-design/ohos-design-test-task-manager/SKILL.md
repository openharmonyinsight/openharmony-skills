---
name: ohos-design-test-task-manager
description: 测试设计流程的计时与检查点协议。记录各阶段 Agent 执行耗时和用户确认耗时、管理检查点保存与恢复。当 ohos-design-test-coordinator 需要追踪阶段进度、记录 timing 数据、保存 checkpoint 或恢复中断的测试设计流程时使用。当用户需要查看阶段耗时、恢复中断的测试设计流程、或排查某阶段执行异常时也可独立使用。关键词：timing protocol, checkpoint, task recovery, phase duration tracking.
---

> 本文件定义计时协议和检查点协议的核心规范。
> **数据展示格式**详见 [`templates/ui-templates.md`](templates/ui-templates.md)。

# 测试设计计时与检查点协议

## 角色定位

本技能被 ohos-design-test-coordinator 调用，定义测试设计6阶段流程中：
- 各阶段的计时数据采集协议（timing）
- 检查点的数据结构和存储规范
- 任务恢复的检查点匹配规则

coordinator 按本协议操作文件，本技能不独立执行。

---

## NEVER

- **NEVER 在 task JSON 中存储文件内容**
  - 原因：task.json 需高频读写，存内容会使其膨胀至 MB 级
  - 正确做法：只存文件路径
  - 后果：恢复时解析失败，且跨阶段内容漂移无法追踪
- **NEVER 在快速模式下弹出确认界面**
  - 原因：快速模式为无交互场景设计，弹窗会阻塞自动化流程
  - 正确做法：仅在错误时通知用户
  - 后果：交互阻塞导致流水线挂起等待无人响应
- **NEVER 跳过检查点保存**
  - 原因：检查点是阶段交付的唯一不可变快照，跳过即丢失恢复锚点
  - 正确做法：无论何种执行模式，关键检查点必须保存
  - 后果：中断后无法定位最后成功阶段，只能从阶段1重来
- **NEVER 修改已保存的检查点文件**
  - 原因：检查点是不可变审计快照
  - 正确做法：只能读取或新建
  - 后果：修改会破坏 phase 编号顺序和恢复匹配逻辑，恢复指向错误阶段
- **NEVER 在 timing.json 中写入估算值或占位符**
  - 原因：计时数据用于阶段耗时分析与瓶颈定位，估算值会污染统计
  - 正确做法：必须是 `date +%s` 的真实 epoch 秒数
  - 后果：耗时报告失真，瓶颈误判，优化方向错误
- **NEVER 在 Phase 3 子步骤合并为一个 timing 条目**
  - 原因：Phase3 三子步骤（UI/代码/编译）耗时差异大，合并掩盖瓶颈环节
  - 正确做法：步骤1/2/3 各自独立记录
  - 后果：合并后无法定位 Demo UI/代码/编译哪步耗时异常，优化无从下手

---

## 计时协议（核心）

### 计时文件结构

存储位置：`{输出目录}/tasks/timing.json`

```json
{
  "pipeline_started_at": 1746496800,
  "pipeline_completed_at": 0,
  "phases": [
    {
      "name": "阶段1：需求解析",
      "phase_started_at": 0,
      "agent_completed_at": 0,
      "confirmation_started_at": 0,
      "confirmation_completed_at": 0,
      "phase_completed_at": 0,
      "optimization_rounds": 0,
      "optimization_duration_seconds": 0
    },
    {
      "name": "阶段2：测试点生成",
      "phase_started_at": 0,
      "agent_completed_at": 0,
      "confirmation_started_at": 0,
      "confirmation_completed_at": 0,
      "phase_completed_at": 0,
      "optimization_rounds": 0,
      "optimization_duration_seconds": 0
    },
    {
      "name": "阶段2：对抗评估",
      "phase_started_at": 0,
      "agent_completed_at": 0,
      "confirmation_started_at": 0,
      "confirmation_completed_at": 0,
      "phase_completed_at": 0,
      "optimization_rounds": 0,
      "optimization_duration_seconds": 0
    }
  ]
}
```

### 6 个计时时机

| 时机 | 操作 | 写入字段 |
|------|------|---------|
| 1. 阶段开始 | Agent 启动前 `date +%s` | phase_started_at |
| 2. Agent 完成 | Agent 返回摘要后 `date +%s` | agent_completed_at |
| 3. 确认开始 | AskUserQuestion 调用前 `date +%s` | confirmation_started_at |
| 4. 确认完成 | 用户回复后 `date +%s`（跳过确认时等于 agent_completed_at） | confirmation_completed_at |
| 5. 优化轮次 | 用户要求优化时 rounds+1，重新执行 Agent 的耗时累加 | optimization_rounds, optimization_duration_seconds |
| 6. 阶段完成 | TaskUpdate 标记完成后 `date +%s` | phase_completed_at |

### Phase 3 子步骤拆分

子阶段1（Demo UI设计）、子阶段2（Demo代码生成）、子阶段3（编译验证）各自作为独立条目记录在 phases 数组中，命名规则：
- `阶段3-子阶段1：Demo UI设计`
- `阶段3-子阶段2：Demo代码生成`
- `阶段3-子阶段3：编译验证`

### 跳过确认的阶段处理

阶段2测试点生成、阶段3Demo流水线、阶段4用例细化、阶段5验证导出不暂停确认：`confirmation_started_at` 和 `confirmation_completed_at` 都设为 agent_completed_at 的值，confirmation_duration_seconds 为 0。

阶段1需求解析、阶段2对抗评估、阶段4对抗评估需要用户确认，正常记录确认耗时。

---

## 任务数据结构

任务 timing 子结构（领域专属字段；通用状态机 pending→in_progress→completed/failed/skipped 与 error_history 此处不展开）：

```json
{
  "timing": {
    "phase_started_at": 0,
    "agent_completed_at": 0,
    "agent_duration_seconds": 0,
    "confirmation_started_at": 0,
    "confirmation_completed_at": 0,
    "confirmation_duration_seconds": 0,
    "phase_completed_at": 0,
    "phase_duration_seconds": 0,
    "optimization_rounds": 0,
    "optimization_duration_seconds": 0
  }
}
```

| 字段 | 采集时机 | 要点 | 采集理由（专家级，为何此机点采集） |
|------|---------|------|-------------------------------------|
| phase_started_at | Agent 启动前 `date +%s` | 必须 > 0 才有效 | T1：必须在Agent启动前采，否则漏算spawn开销，阶段耗时被低估 |
| agent_completed_at | Agent 返回摘要后 `date +%s` | 含优化轮次的总执行时间 | T2：必须在摘要返回后采，早采漏算优化轮次、晚采混入确认耗时 |
| confirmation_started_at | AskUserQuestion 调用前 | 跳过确认时 = agent_completed_at | T3：隔离用户思考耗时与Agent执行耗时的边界点 |
| confirmation_completed_at | 用户回复后 | 跳过确认时 = agent_completed_at | T4：跳过时等于agent_completed_at以保持duration=0语义一致 |
| phase_completed_at | TaskUpdate 后 | 阶段2/4/6 不暂停确认 | T6：必须在标记完成后采，确保阶段总耗时含确认+优化全成本 |
| optimization_rounds | 用户要求优化时 +1 | 初始值 0 | T5轮次：单独计数，便于在报告中拆分"首次执行"与"返工"成本 |
| optimization_duration_seconds | 优化轮次 Agent 耗时累加 | 初始值 0 | T5耗时：累加各轮Agent耗时，与agent_duration配合定位瓶颈 |
| *_duration_seconds | — | 不手动写入 | 通用字段，结束-开始自动计算 |

---

## 检查点协议

### 文件位置

```
{输出目录}/tasks/
├── current_task.json
├── timing.json
├── task_history.json
└── task_checkpoints/
    ├── phase1_requirement_checkpoint.json
    ├── phase2_testpoint_checkpoint.json
    ├── phase3_demo_checkpoint.json
    ├── phase4_testcase_checkpoint.json
    └── phase5_validate_checkpoint.json
```

### 检查点数据结构

```json
{
  "checkpoint_id": "phase1_completed",
  "timestamp": "2026-06-25T16:01:30Z",
  "phase": 1,
  "phase_name": "需求解析",
  "status": "completed",
  "outputs": {
    "requirement_analysis.md": "/path/to/requirement_analysis.md",
    "knowledge_match.json": "/path/to/knowledge_match.json"
  },
  "timing_snapshot": {
    "phase_duration_seconds": 45,
    "agent_duration_seconds": 30,
    "confirmation_duration_seconds": 15,
    "optimization_rounds": 0
  },
  "error_history": []
}
```

### 检查点保存时机

每个阶段 Agent 执行完成且用户确认通过（或跳过确认）后，立即保存检查点。

### 保存前检查清单

> **Before 保存检查点，ask yourself**：用户已确认（或该阶段跳过确认）？输出文件可读（`ls` 通过）？timing 完整（started_at 与 completed_at 均 > 0）？前序检查点存在？任一未过则不保存。

每个检查点保存前，逐项确认：

| 检查项 | 通过标准 | 未通过时 |
|--------|---------|---------|
| 阶段确认状态 | 用户已确认 或 该阶段跳过确认 | 不保存，等待确认完成 |
| 输出文件存在性 | `ls` 验证所有 outputs 路径可读 | 记录缺失文件到 error_history，不保存 |
| timing 数据完整 | phase_started_at > 0 且 phase_completed_at > 0 | 记录异常但不阻塞保存（timing 非关键） |
| 前序检查点存在 | 前一阶段检查点文件已存在 | phase1 无前序；后续阶段缺失则告警但允许继续 |

### 恢复匹配规则

1. 扫描 `{输出目录}/tasks/task_checkpoints/` 下所有 checkpoint 文件
2. 按 phase 编号排序，找到最后一个 status=completed 的检查点
3. 该检查点的下一个阶段即为恢复起始点
4. 读取该检查点的 outputs 字段，验证所有输出文件存在且可读
5. 输出文件缺失时：降级到前一个检查点

> **为何按 phase 编号排序**：检查点可能跨会话补存（如中断后重跑前一阶段），文件 timestamp 不可靠；phase 编号单调递增，是恢复顺序的唯一可信依据。

**数据展示格式**详见 [`templates/ui-templates.md`](templates/ui-templates.md) 第3节"检查点恢复展示格式"。

### 恢复时数据有效性判断

| 异常场景 | 判断依据 | 处理策略 |
|---------|---------|---------|
| 输出文件被删除 | outputs 中的路径 `ls` 不存在 | 降级到前一检查点 |
| 输出文件被修改 | 文件修改时间 > 检查点 timestamp | 告警用户"文件可能在恢复后被手动修改"，由用户决定 |
| 所有检查点无效 | 无任何 checkpoint 文件或全部 outputs 缺失 | 从阶段1重新开始，保留已有输出文件 |
| timing.json 损坏 | JSON 解析失败 | 重建空的 timing.json，已丢失的计时数据不可恢复 |

---

## 脚本调用方式

> 脚本路径：`scripts/timing_helper.py`（相对技能根目录）。脚本按本协议操作 `{输出目录}/tasks/` 下的 timing.json 与 task_checkpoints/，可独立执行或由 coordinator 调用。

| 命令 | 调用时机 | 命令示例 |
|------|---------|---------|
| `record` | 各计时机采集时 | `python scripts/timing_helper.py record --output {dir} --phase phase1 --point phase_started_at` |
| `record`（优化轮次） | 用户要求优化时 | `python scripts/timing_helper.py record --output {dir} --phase phase2_adv --point optimization_round` |
| `record`（优化耗时） | 优化轮次结束时 | `python scripts/timing_helper.py record --output {dir} --phase phase2_adv --point optimization_duration --value 30` |
| `checkpoint save` | 阶段确认通过/跳过确认后 | `python scripts/timing_helper.py checkpoint save --output {dir} --phase phase1 --artifact requirement_analysis.md={path}` |
| `resume` | 恢复中断流程时 | `python scripts/timing_helper.py resume --output {dir}` |
| `report` | 流程结束后 | `python scripts/timing_helper.py report --output {dir}` |

**保存前检查清单（脚本内置校验）**：输出文件可读、timing 完整（非关键仅告警）、前序检查点存在；任一致命项未过则拒绝保存。检查点为不可变审计快照，禁止覆盖。

---

## 数据展示格式

**MANDATORY**：当需要展示计时数据、检查点数据、任务历史时，读取 [`templates/ui-templates.md`](templates/ui-templates.md) 获取完整展示格式：

- 计时数据展示格式 → 第1节
- 检查点数据展示格式 → 第2节
- 检查点恢复展示格式 → 第3节
- 任务历史展示格式 → 第4节
- Phase3子步骤计时展示格式 → 第5节
- 计时报告完整格式 → 第6节

**Do NOT Load**：在纯文件操作（保存检查点、更新 timing）时无需加载 ui-templates.md。
