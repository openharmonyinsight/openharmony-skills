# 门控处理框架规则

## 各阶段门控检查点

| 阶段 | 门控类型 | 检查时机 | 具体动作 | 未通过时处理 |
|------|---------|---------|---------|-------------|
| 启动流程前 | 启动流程缺失 | 创建Phase1任务前 | 检查已完成：AskUserQuestion配置(4问) + 输入目录验证 + 输出目录创建 + 需求文档扫描 + 知识库确认 | 告警终止，重新执行启动流程 |
| Phase1完成后 | 输出文档缺失 | 进入澄清前 | requirement_analysis.md存在且非空 | 提示缺失，重试或终止 |
| Phase1澄清前 | 需求澄清未完成 | 进入Phase2前 | requirement_analysis.md待确认项表格"用户回答"列全部非空 | 告警终止，执行答疑交互(见phase1_clarify_rules.md) |
| Phase1完成后 | 数据空值 | 进入Phase2前 | 主单元数≥1 且 被测场景数≥1 | 提示用户确认文档格式 |
| Phase2规划后 | 规划步骤缺失 | spawn执行Agent前 | 返回摘要含"批次规划完成"关键字及批次表格 | 告警终止spawn，AskUserQuestion(重试规划/终止) |
| Phase2完成后 | 输出文档缺失 | 进入Phase2Adv前 | test_point_design.md存在且非空 | 提示缺失，重试或终止 |
| Phase2完成后 | 质量不达标 | 进入Phase4前 | 覆盖率≥70% 且 P0=0 | 展示差距，用户选择继续/优化 |
| Phase2Adv完成后 | 输出文档缺失 | 进入Phase3前 | adversarial_report.md存在且非空 | 提示缺失，重试或终止 |
| Phase2Adv完成后 | 对抗评分不达标 | 进入Phase3前 | 总分≥80 | 自动循环对抗(最多3轮) |
| Phase3完成后 | 输出文档缺失(可选) | 进入Phase4前 | demo_design.md存在(非XTS时) | 提示缺失，重试或终止 |
| Phase3完成后 | 编译状态异常 | 进入Phase4前 | 返回摘要无SDK过低/HVIGORW_NOT_FOUND/BUILD FAILED | 必须AskUserQuestion(见phase3_demo_pipeline.md) |
| Phase4规划后 | 规划步骤缺失 | spawn执行Agent前 | 返回摘要含"批次规划完成"关键字及批次表格 | 告警终止spawn，AskUserQuestion(重试规划/终止) |
| Phase4完成后 | 输出文档缺失 | 进入Phase4Adv前 | test_cases.md存在且非空 | 提示缺失，重试或终止 |
| Phase4Adv完成后 | 输出文档缺失 | 进入Phase5前 | adversarial_report.md追加内容 | 提示缺失，重试或终止 |
| Phase4Adv完成后 | 对抗评分不达标 | 进入Phase5前 | 总分≥80 | 自动循环对抗(最多3轮) |
| Phase5完成后 | 输出文档缺失 | 流程结束前 | validation_report.md + test_cases.xlsx存在 | 提示缺失，重试或终止 |
| Phase5导出后 | 导出空字段 | 导出Excel后 | 空单元格≤20% | 重新调用phase5_export.py |
| Phase5完成后 | 清理门控 | 流程结束前 | 临时文件已清理(见phase5_rules.md清理表) | 告警重试清理 |

---

## 通用规则

**门控检查流程**：检查依赖文件存在 → 不存在则调用脚本生成 → 输出自检结果 → 通过后进入Agent执行

**自检格式**：`[{Phase名称}自检] 检查项: {✓存在/✗不存在}` → ✗时调用脚本 → ✓已生成 → 自检通过

**降级机制**：脚本失败→修复(最多2次)→失败→AskUserQuestion(跳过/终止)

---

## 启动流程缺失门控

**触发**：创建Phase1任务前

**检查项**：①AskUserQuestion配置(4问) ②输入目录Test-Path ③输出目录创建 ④需求文档扫描 ⑤知识库确认(默认/领域/自定义)

**处理**：任一未完成 → 告警终止 → 重新执行全部启动步骤(含timing.json初始化)

---

## 需求澄清未完成门控

**触发**：Phase1完成后进入Phase2前

**检查**：requirement_analysis.md待确认项表格"用户回答"列全部非空

**处理**：未通过 → 告警终止 → 执行答疑交互(见phase1_clarify_rules.md)

**禁止**：待确认项未全部回答时禁止跳过澄清直接进入Phase2

---

## 数据空值门控

**触发**：Phase1后进入Phase2前

**检查**：主单元数=0 且 被测场景数=0

**处理**：AskUserQuestion → 返回Phase1补充 / 终止 / 继续(用户确认无测试需求)

---

## 输出文档缺失门控

**触发**：每阶段完成后进入下一阶段前

**检查**：Test-Path文件存在 + Read内容非空

**处理**：AskUserQuestion → 重试当前阶段(最多2次) / 跳过 / 终止

---

## 规划步骤缺失门控

**触发**：Phase2/Phase4规划Agent返回摘要后

**检查**：摘要含"批次规划完成"关键字及批次表格

**处理**：未通过 → 告警终止spawn → AskUserQuestion(重试规划/终止)

**禁止**：未收到规划摘要禁止spawn执行Agent

---

## 质量不达标门控

**触发**：Phase2完成后进入Phase4前

**检查**：test_point_design.md覆盖率≥70% 且 P0=0

**处理**：展示差距 → AskUserQuestion(继续/返回Phase2优化)

---

## 对抗评分不达标门控

**触发**：Phase2Adv/Phase4Adv完成后

**检查**：adversarial_report.md总分≥80(覆盖率40+场景45+变异15)

**处理**：自动循环对抗(最多3轮) → 达标自动进入下一阶段 / 不达标AskUserQuestion

---

## 导出空字段门控

**触发**：Phase5导出Excel后

**检查**：空单元格≤20%

**处理**：删除Excel → 重新调用phase5_export.py → 再次检查 → 仍不达标提示用户

---

## 清理门控

**触发**：Phase5完成后流程结束前

**检查**：phase5_rules.md清理表中所有项已清理

**处理**：告警 → 自动清理(见phase5_rules.md) → 再次检查 → 失败提示手动清理

**保留**：knowledge_match.md、adversarial_report.md、Phase3 Demo文件、用户自定义文件
