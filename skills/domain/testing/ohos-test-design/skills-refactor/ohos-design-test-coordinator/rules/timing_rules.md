# 计时协议规则

## timing.json 结构

```json
{
  "pipeline_started_at": 1719234567,
  "pipeline_completed_at": 1719235678,
  "phases": [
    {
      "phase_name": "阶段1：需求解析",
      "phase_started_at": 1719234567,
      "agent_completed_at": 1719234600,
      "confirmation_started_at": 1719234600,
      "confirmation_completed_at": 1719234610,
      "optimization_duration_seconds": 30,
      "optimization_rounds": 1,
      "phase_completed_at": 1719234640
    }
  ]
}
```

---

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| pipeline_started_at | int | 流水线启动时间戳（epoch秒） |
| pipeline_completed_at | int | 流水线完成时间戳（epoch秒） |
| phases | array | 各阶段计时记录数组 |
| phase_name | string | 阶段名称 |
| phase_started_at | int | T1：阶段启动时间 |
| agent_completed_at | int | T2：Agent返回摘要时间 |
| confirmation_started_at | int | T3：确认开始时间，跳过确认时=T2 |
| confirmation_completed_at | int | T4：确认结束时间，跳过确认时=T2 |
| optimization_duration_seconds | int | 优化轮次累计耗时（秒） |
| optimization_rounds | int | 优化轮次数 |
| phase_completed_at | int | T6：阶段完成时间 |

---

## 计时时机（T1-T6）

| 时机 | 触发点 | 写入字段 |
|------|--------|---------|
| T1 | 阶段启动时 | phase_started_at |
| T2 | Agent返回摘要后 | agent_completed_at |
| T3 | AskUserQuestion调用前 | confirmation_started_at |
| T4 | 用户回复后 | confirmation_completed_at |
| - | 优化Agent完成 | optimization_duration_seconds累加 |
| T6 | 阶段完成时 | phase_completed_at |

---

## 各阶段确认策略

| 阶段 | 需要确认 | T3/T4处理 |
|------|---------|----------|
| Phase1 | 是 | 正常记录T3/T4 |
| Phase2 | 否 | T3/T4 = T2 |
| Phase2Adv | 是（不达标时） | 正常记录，优化轮次累加 |
| Phase3 | 条件（编译异常时） | 编译异常时正常记录T3/T4，否则 T3/T4 = T2 |
| Phase4 | 否 | T3/T4 = T2 |
| Phase4Adv | 是（不达标时） | 正常记录，优化轮次累加 |
| Phase5 | 否 | T3/T4 = T2 |

---

## 计算规则

| 耗时类型 | 计算公式 |
|---------|---------|
| Agent耗时 | agent_completed_at - phase_started_at |
| 确认耗时 | confirmation_completed_at - confirmation_started_at（跳过确认时为0） |
| 阶段总耗时 | phase_completed_at - phase_started_at |
| 总耗时 | pipeline_completed_at - pipeline_started_at |

---

## 计时写入方式

每次计时时机触发时：
1. 使用 `date +%s` 获取当前epoch秒数
2. Read timing.json
3. Edit 更新对应字段

---

## 优化轮次计时

用户选择"需要优化"时：
1. 记录 `optimization_start = date +%s`
2. Spawn Agent执行增量修改
3. Agent返回后记录 `optimization_end = date +%s`
4. `optimization_duration_seconds += (optimization_end - optimization_start)`
5. `optimization_rounds += 1`
6. 更新timing.json

---

## 计时报告格式

```
⏱️ 阶段耗时报告

| 阶段 | Agent耗时 | 确认耗时 | 优化耗时(轮次) | 阶段总耗时 |
|------|-----------|---------|---------------|-----------|
| 阶段1：需求解析 | Xs | Xs | Xs (N轮) | Xs |
| 阶段2：测试点生成 | Xs | 0s | Xs (N轮) | Xs |
| 阶段2：对抗评估 | Xs | Xs | Xs (N轮) | Xs |
| 阶段3：Demo流水线 | Xs | 0s | Xs (N轮) | Xs |
| 阶段4：用例细化 | Xs | 0s | Xs (N轮) | Xs |
| 阶段4：对抗评估 | Xs | Xs | Xs (N轮) | Xs |
| 阶段5：验证导出 | Xs | 0s | 0s | Xs |
| **总耗时** | | | | **Xs** |
```

超过60秒时额外显示分秒格式（如125s → 2m5s）。

---

## 特殊情况处理

| 情况 | 处理方式 |
|------|---------|
| 阶段3 Demo流水线跳过 | 记录phase_started_at=phase_completed_at=当前时间，所有耗时为0 |
| 阶段3 Demo流水线子步骤 | 各子步骤独立记录在phases数组中 |