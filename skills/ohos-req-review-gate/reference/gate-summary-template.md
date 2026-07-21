# Review Ready Gate 判定 — {feature_id}

时间: {timestamp}
docs_dir: {docs_dir}

## Gate 结论: {Ready | Conditional Ready | Not Ready}

## 检查项汇总

| # | 检查项 | 状态 | 证据 |
|---|--------|------|------|
| 1 | 概述与价值 | ✅/⚠️/❌ | ... |
| 2 | 范围明确 | ✅/⚠️/❌ | ... |
| ... | ... | ... | ... |

## 条件项（Conditional Ready 时列出）

| 来源 | 描述 | Owner | 关闭动作 | 关闭时点 |
|------|------|-------|---------|---------|
| §3 | AC-04 缺验证方式 | <name> | 补 AC 验证列 | Phase 2 启动前 |

## Phase 0 观测项（不阻塞 Gate，Phase 1-9 跟踪闭环）

| 来源 | 描述 | Owner | 目标关闭阶段 | 计划关闭时点 |
|------|------|-------|-------------|-------------|
| §6 | 性能基准待实测 | <name> | Phase 5 | Phase 5 测试阶段 |

## 下一步
- Ready → 执行 ohos-feat-to-ir 生成 IR
- Conditional Ready → 执行 ohos-feat-to-ir，但 IR.md 末尾「条件项清单」补充章节必须填写
- Not Ready → 回 Step 0.4 补全；feature.md 不存在时直接到 Step 0.4
