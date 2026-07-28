## 计时与检查点数据展示模板

> 本文件定义 ohos-design-test-task-manager 模块的数据展示格式。
> **定位说明**：ohos-design-test-task-manager 定义计时协议和检查点协议，由 ohos-design-test-coordinator 按协议操作文件。本模块不独立执行，仅提供数据展示格式规范。

---

### 1. 计时数据展示格式

#### 1.1 timing.json 结构

```json
{
  "pipeline_started_at": 1746496800,
  "pipeline_completed_at": 1746500100,
  "phases": [
    {
      "name": "阶段1：需求解析",
      "phase_started_at": 1746496800,
      "agent_completed_at": 1746496830,
      "confirmation_started_at": 1746496830,
      "confirmation_completed_at": 1746496845,
      "phase_completed_at": 1746496845,
      "optimization_rounds": 0,
      "optimization_duration_seconds": 0
    },
    {
      "name": "阶段2：测试点生成",
      "phase_started_at": 1746496845,
      "agent_completed_at": 1746496920,
      "confirmation_started_at": 1746496920,
      "confirmation_completed_at": 1746496920,
      "phase_completed_at": 1746496920,
      "optimization_rounds": 0,
      "optimization_duration_seconds": 0
    },
    {
      "name": "阶段2：对抗评估",
      "phase_started_at": 1746496920,
      "agent_completed_at": 1746496960,
      "confirmation_started_at": 1746496960,
      "confirmation_completed_at": 1746496975,
      "phase_completed_at": 1746496975,
      "optimization_rounds": 1,
      "optimization_duration_seconds": 30
    },
    {
      "name": "阶段3：Demo流水线",
      "phase_started_at": 1746496975,
      "agent_completed_at": 1746497100,
      "confirmation_started_at": 1746497100,
      "confirmation_completed_at": 1746497100,
      "phase_completed_at": 1746497100,
      "optimization_rounds": 0,
      "optimization_duration_seconds": 0
    },
    {
      "name": "阶段4：用例细化",
      "phase_started_at": 1746497100,
      "agent_completed_at": 1746497250,
      "confirmation_started_at": 1746497250,
      "confirmation_completed_at": 1746497250,
      "phase_completed_at": 1746497250,
      "optimization_rounds": 0,
      "optimization_duration_seconds": 0
    },
    {
      "name": "阶段4：对抗评估",
      "phase_started_at": 1746497250,
      "agent_completed_at": 1746497300,
      "confirmation_started_at": 1746497300,
      "confirmation_completed_at": 1746497315,
      "phase_completed_at": 1746497315,
      "optimization_rounds": 0,
      "optimization_duration_seconds": 0
    },
    {
      "name": "阶段5：验证导出",
      "phase_started_at": 1746497315,
      "agent_completed_at": 1746497350,
      "confirmation_started_at": 1746497350,
      "confirmation_completed_at": 1746497350,
      "phase_completed_at": 1746497350,
      "optimization_rounds": 0,
      "optimization_duration_seconds": 0
    }
  ]
}
```

#### 1.2 计时数据读取示例

coordinator 读取 timing.json 并计算各阶段耗时：

```markdown
⏱️ 阶段耗时报告

| 阶段 | Agent耗时 | 确认耗时 | 优化耗时(轮次) | 阶段总耗时 |
|------|-----------|---------|---------------|-----------|
| 阶段1：需求解析 | 30s | 15s | 0s (0轮) | 45s |
| 阶段2：测试点生成 | 75s | 0s | 0s (0轮) | 75s |
| 阶段2：对抗评估 | 40s | 15s | 30s (1轮) | 85s |
| 阶段3：Demo流水线 | 125s | 0s | 0s (0轮) | 125s |
| 阶段4：用例细化 | 150s | 0s | 0s (0轮) | 150s |
| 阶段4：对抗评估 | 50s | 15s | 0s (0轮) | 65s |
| 阶段5：验证导出 | 35s | 0s | 0s | 35s |
| **总耗时** | | | | **485s** |

汇总：
- Agent执行总耗时：450s (占全流程 93%)
- 用户确认总耗时：45s (占全流程 9%)
- 优化轮次：1轮，总耗时30s
```

#### 1.3 耗时计算规则

| 字段 | 计算公式 | 说明 |
|------|---------|------|
| agent_duration_seconds | agent_completed_at - phase_started_at + optimization_duration_seconds | Agent执行耗时（含优化轮次累加） |
| confirmation_duration_seconds | confirmation_completed_at - confirmation_started_at | 用户确认耗时（跳过确认时为0） |
| phase_duration_seconds | phase_completed_at - phase_started_at | 阶段总耗时 |
| optimization_duration_seconds | 各优化轮次Agent耗时累加 | 优化轮次总耗时 |

**时间显示格式**：
- 不足60秒：显示"Xs"
- 60秒以上：显示"X分Y秒"（如"2分30s"）

---

### 2. 检查点数据展示格式

#### 2.1 检查点文件列表

```
{输出目录}/tasks/task_checkpoints/
├── phase1_requirement_checkpoint.json
├── phase2_testpoint_checkpoint.json
├── phase3_demo_checkpoint.json
├── phase4_testcase_checkpoint.json
├── phase5_validate_checkpoint.json
```

#### 2.2 检查点数据结构

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

#### 2.3 检查点数据展示示例

coordinator 读取检查点文件并展示：

```markdown
=== 检查点详情 ===

检查点ID：phase1_completed
保存时间：2026-06-25 16:01:30
阶段：Phase1：需求解析
状态：completed

计时信息：
- 阶段总耗时：45s
- Agent耗时：30s
- 确认耗时：15s
- 优化轮次：0轮

输出文件：
- requirement_analysis.md ✓ 存在
- knowledge_match.json ✓ 存在

错误历史：无
```

---

### 3. 检查点恢复展示格式

#### 3.1 检查点扫描结果

coordinator 扫描 task_checkpoints/ 目录并展示：

```markdown
=== 可用的检查点 ===

| 检查点文件 | 阶段 | 时间 | 输出文件状态 |
|-----------|------|------|-------------|
| phase1_requirement_checkpoint.json | Phase1：需求解析 | 2026-06-25 16:01 | ✓ 全部存在 |
| phase2_testpoint_checkpoint.json | Phase2：测试点生成 | 2026-06-25 16:15 | ✓ 全部存在 |
| phase3_demo_checkpoint.json | Phase3：Demo流水线 | 2026-06-25 16:30 | ✗ 输出文件缺失 |

恢复建议：从 Phase3 重新执行（Phase2 检查点为最后一个有效检查点）
```

#### 3.2 检查点有效性判断

| 异常场景 | 判断依据 | 处理策略 |
|---------|---------|---------|
| 输出文件被删除 | outputs 中的路径 `ls` 不存在 | 降级到前一检查点 |
| 输出文件被修改 | 文件修改时间 > 检查点 timestamp | 告警用户"文件可能在恢复后被手动修改"，由用户决定 |
| 所有检查点无效 | 无任何 checkpoint 文件或全部 outputs 缺失 | 从 Phase1 重新开始，保留已有输出文件 |
| timing.json 损坏 | JSON 解析失败 | 重建空的 timing.json，已丢失的计时数据不可恢复 |

---

### 4. 任务历史展示格式

#### 4.1 task_history.json 结构

```json
{
  "history": [
    {
      "task_id": "test_design_20260625_001",
      "started_at": "2026-06-25T16:00:00Z",
      "completed_at": "2026-06-25T16:15:00Z",
      "status": "completed",
      "phases_completed": 5,
      "total_duration_seconds": 900,
      "output_dir": "/path/to/output"
    },
    {
      "task_id": "test_design_20260624_001",
      "started_at": "2026-06-24T14:00:00Z",
      "completed_at": "2026-06-24T14:10:00Z",
      "status": "failed",
      "failed_phase": 3,
      "failed_reason": "Demo编译失败（SDK缺失API）",
      "output_dir": "/path/to/output2"
    }
  ]
}
```

#### 4.2 任务历史展示示例

```markdown
=== 任务历史 ===

| 任务ID | 开始时间 | 状态 | 阶段完成 | 总耗时 |
|--------|---------|------|---------|--------|
| test_design_20260625_001 | 2026-06-25 16:00 | ✓ 完成 | 5/5 | 15分 |
| test_design_20260624_001 | 2026-06-24 14:00 | ✗ 失败 | 2/5 | 10分 |

最近任务详情：
- 任务ID：test_design_20260625_001
- 状态：completed
- 输出目录：/path/to/output
- 检查点目录：/path/to/output/tasks/task_checkpoints/
```

---

### 5. Phase3 子步骤计时展示格式

#### 5.1 Phase3 子步骤拆分

Phase3（Demo流水线）拆分为独立计时条目：

- `阶段3-子阶段1：Demo UI设计`
- `阶段3-子阶段2：Demo代码生成`
- `阶段3-子阶段3：编译验证`

#### 5.2 timing.json 中的 Phase3 条目示例

```json
{
  "phases": [
    {
      "name": "阶段3-子阶段1：Demo UI设计",
      "phase_started_at": 1746496975,
      "agent_completed_at": 1746497020,
      "phase_completed_at": 1746497020,
      "optimization_rounds": 0
    },
    {
      "name": "阶段3-子阶段2：Demo代码生成",
      "phase_started_at": 1746497020,
      "agent_completed_at": 1746497080,
      "phase_completed_at": 1746497080,
      "optimization_rounds": 0
    },
    {
      "name": "阶段3-子阶段3：编译验证",
      "phase_started_at": 1746497080,
      "agent_completed_at": 1746497100,
      "phase_completed_at": 1746497100,
      "optimization_rounds": 2
    }
  ]
}
```

#### 5.3 Phase3 子步骤计时展示

```markdown
=== Demo流水线计时详情 ===

| 子阶段 | Agent耗时 | 优化耗时(轮次) | 子阶段总耗时 |
|--------|-----------|---------------|-------------|
| 子阶段1：Demo UI设计 | 45s | 0s (0轮) | 45s |
| 子阶段2：Demo代码生成 | 60s | 0s (0轮) | 60s |
| 子阶段3：编译验证 | 20s | 10s (2轮) | 30s |
| **Phase3总耗时** | | | **135s** |

说明：子阶段3编译验证含2轮修复，修复耗时10s
```

---

### 6. 计时报告完整格式

流程结束后，coordinator 读取 timing.json 并输出完整计时报告：

```markdown
⏱️ 阶段耗时报告

| 阶段 | Agent耗时 | 确认耗时 | 优化耗时(轮次) | 阶段总耗时 |
|------|-----------|---------|---------------|-----------|
| 阶段1：需求解析 | 30s | 15s | 0s (0轮) | 45s |
| 阶段2：测试点生成 | 75s | 0s | 0s (0轮) | 75s |
| 阶段2：对抗评估 | 40s | 15s | 30s (1轮) | 85s |
| 阶段3：Demo流水线 | 125s | 0s | 0s (0轮) | 125s |
| 阶段4：用例细化 | 150s | 0s | 0s (0轮) | 150s |
| 阶段4：对抗评估 | 50s | 15s | 0s (0轮) | 65s |
| 阶段5：验证导出 | 35s | 0s | 0s | 35s |
| **总耗时** | **485s** | **45s** | **30s** | **485s** |

汇总统计：
- Agent执行总耗时：450s (占全流程 93%)
- 用户确认总耗时：45s (占全流程 9%)
- 优化总耗时：30s (1轮)
- 平均阶段耗时：69s

执行效率分析：
- 自动执行阶段（Phase2/3/4/5）：耗时占比 91%
- 需确认阶段（Phase1/对抗评估）：耗时占比 9%
- 优化轮次效率：平均每轮30s
```

---

### 7. 数据文件位置说明

```
{输出目录}/tasks/
├── current_task.json          ← 当前任务状态
├── timing.json                 ← 计时数据（本文件核心）
├── task_history.json           ← 任务历史记录
└── task_checkpoints/           ← 检查点目录
    ├── phase1_requirement_checkpoint.json
    ├── phase2_testpoint_checkpoint.json
    ├── phase3_demo_checkpoint.json
    ├── phase4_testcase_checkpoint.json
    └── phase5_validate_checkpoint.json
```

---

### 8. 注意事项

#### 8.1 计时数据写入规则

- **MANDATORY**：所有时间戳必须是 `date +%s` 的真实 epoch 秒数，禁止写入估算值或占位符
- **MANDATORY**：跳过确认的阶段，`confirmation_started_at` 和 `confirmation_completed_at` 必须等于 `agent_completed_at`
- **MANDATORY**：Phase3 子步骤各自独立记录，不合并为一个条目

#### 8.2 检查点保存规则

- **MANDATORY**：每个阶段完成后立即保存检查点，无论执行模式
- **MANDATORY**：检查点文件只读取或新建，禁止修改已保存的检查点
- **MANDATORY**：检查点只存储文件路径，禁止存储文件内容

#### 8.3 数据有效性判断

- timing.json 中 `phase_started_at` 和 `phase_completed_at` 必须 > 0 才有效
- 检查点 outputs 中的路径必须通过 `ls` 验证存在且可读
- 文件修改时间 > 检查点 timestamp 时告警用户

---

> 本文件与 ohos-design-test-task-manager/SKILL.md 配合使用，定义计时协议和检查点协议的数据展示格式。
> 实际用户交互界面由 ohos-design-test-coordinator/templates/ui-templates.md 定义。