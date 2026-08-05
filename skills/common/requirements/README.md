# 需求分析 (Requirements Analysis)

本目录提供 OpenHarmony requirements 阶段的需求导入、可行性分析、方案决策、Feature/Proposal 评审基线、评审材料生成和评审结论回流相关 skills。

## 流程总览

```text
原始诉求
  -> ohos-req-intake-orchestration
       预检   依赖检查、流程编排、跨步骤追溯
  -> ohos-req-requirement-intake
       Step 1  生成 01-requirement.md
       Step 2  需求澄清门禁
  -> ohos-req-feasibility-analysis
       Step 3  可行性分析输入提醒
       Step 4  轻量代码预检
       Step 5  生成 02-feasibility.md
       Step 6  feasibility 澄清门禁
  -> ohos-req-arch-decision
       Step 7  生成 03-arch-decision-record.md 候选分析
       Step 8  收集用户决策结论
       Step 9  ADR 定稿
  -> ohos-req-feature-proposal-baseline
       Step 10 生成 04-feature.md
       Step 11 拆分结果确认
       Step 12 内建 Review Ready Gate + AC 校验
  -> ohos-req-value-ppt-gen
       Step 13 生成需求评审 PPT（可选）
  -> ohos-req-value-decision
       Step 14 评审决策纪要回流
```

## Skills

| Skill | 作用 | 输入 | 输出 |
|------|------|------|------|
| [ohos-req-intake-orchestration](ohos-req-intake-orchestration/) | requirements 阶段总编排入口；串联需求导入、可行性分析、方案决策、Feature/Proposal 基线、可选 PPT 和评审结论回流；负责依赖预检、强制暂停点和跨步骤追溯。 | 用户原始需求描述，可选 Issue、PRD、会议纪要；已存在的阶段产物目录；运行时可访问的 skill 目录。 | `01-requirement.md`、`02-feasibility.md`、`03-arch-decision-record.md`、`04-feature.md`、`value-decision-record.md` 的流程化产出路径和状态摘要。 |
| [ohos-req-requirement-intake](ohos-req-requirement-intake/) | 将原始诉求归一化为 requirements Step 1 的事实基线；提取背景、价值、范围、FR/NFR、优先级、受影响模块和 RR 单号；阻断占位符和模糊表述进入正文。 | 用户原始描述、Issue、PRD、会议纪要、用户反馈；已确认的范围、版本、约束、指标口径和 RR 单号。 | `{docs_dir}/01-requirement.md`；`{docs_dir}/_draft/clarification-questions.md`；回传需求方、RR 单号、目标版本、FR/NFR 数量、澄清轮次和未关闭项数量。 |
| [ohos-req-feasibility-analysis](ohos-req-feasibility-analysis/) | 基于已澄清 requirement 生成 requirements Step 5 可行性分析；评估能力差距、候选技术路径、兼容性、安全、依赖、工作量、风险和验证计划；不替用户做最终选型。 | `{docs_dir}/01-requirement.md`，可选 `{docs_dir}/_draft/feasibility-inputs.md` 和轻量代码预检证据包。 | `{docs_dir}/02-feasibility.md`；候选方案、风险、阻塞项、验证计划、工作量估算和澄清状态摘要。 |
| [ohos-req-arch-decision](ohos-req-arch-decision/) | 生成 requirements Step 7-9 架构决策记录；阶段 A 输出候选方案对比并等待用户决策，阶段 B 根据用户提供的结论定稿；单方案时支持快速确认路径。 | `{docs_dir}/01-requirement.md`、`{docs_dir}/02-feasibility.md`；阶段 B 还需要用户给出的选定方案、决策理由、决策者和遗留问题。 | `{docs_dir}/03-arch-decision-record.md`；阶段 A 为 `PendingDecision`，阶段 B 为 `Accepted`；回传选定方案、决策者、遗留问题数量和后续影响。 |
| [ohos-req-feature-proposal-baseline](ohos-req-feature-proposal-baseline/) | 生成 requirements Step 10-12 Feature/Proposal 评审基线；完成 proposal 拆分、影响性分析、工作量约束、模块覆盖、术语一致性、遗留问题闭环和内建 Review Ready Gate。 | `{docs_dir}/01-requirement.md`、`{docs_dir}/02-feasibility.md`、`{docs_dir}/03-arch-decision-record.md`；用户确认后的拆分方案。 | `{docs_dir}/04-feature.md`；Gate 结论 `Ready` / `Conditional Ready` / `Not Ready`；FR->AC 追溯表、拆分结论、影响性分析结论和阻塞项。 |
| [ohos-req-value-ppt-gen](ohos-req-value-ppt-gen/) | 可选生成 requirements Step 13 需求评审 PPT；把 OpenHarmony requirement/spec/design proposal 转换为固定 8 页 OH 评审 deck，含品牌页脚、价值页、设计页、影响性分析、交付计划、兼容性和风险页。 | OpenHarmony 需求文档、spec 或设计 proposal；可选 `04-feature.md`、架构图/流程图素材、交付计划和风险信息；本 skill 的 `scripts/deckbuilder.py` 与 `oh_logo.png`。 | `.pptx` 评审材料；固定 8 页结构的需求变更评审 deck；回传输出路径、缺失字段/TBD 清单和生成过程中发现的版式风险。 |
| [ohos-req-value-decision](ohos-req-value-decision/) | 生成 requirements Step 14 评审决策纪要并路由流程；将会议结论映射为接纳、不接纳或下次重新上会；处理歧义结论和回退 Step 判定。 | 用户提供的评审会议纪要；`01-requirement.md` 至 `04-feature.md`；`04-feature.md` 中的 Gate 结论和条件项摘要。 | `{docs_dir}/value-decision-record.md`；JSON 机读决策记录；Markdown 人读摘要；回传评审结论、评审意见数、路由动作和退回 Step。 |

## 预检

在启动完整 requirements 流程前运行：

```bash
bash skills/common/requirements/ohos-req-intake-orchestration/scripts/install_related_skills.sh --check
```

预期结果：

```text
Bundle: ohos-requirements-intake
Installed: 7/7
Required missing: 0
Version mismatch: 0
Result: READY
```
