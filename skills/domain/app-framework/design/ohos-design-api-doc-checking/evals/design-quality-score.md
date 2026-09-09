# Design Quality Score (skills-judge rubric)

Skill: `ohos-design-api-doc-checking` v0.1.0 | Scored: 2026-09-08

说明:本环境未安装 skills-judge 可执行工具,按其标准 rubric(描述触发质量/工作流清晰度/渐进式披露/领域特异性/可维护性/评测证据)人工逐项评分。

| 维度 | 得分 | 评语 |
| --- | --- | --- |
| Frontmatter 与 description 触发质量 | B+ | description 说明能力(7 维度/SDK 一致性/多格式报告)与触发场景(API review、质量评估、错误检测);可再补"Use when checking js-apis-*.md / capi-*.md"式文件级触发词 |
| 工作流清晰度 | A- | 快速开始 5 步 → 文档类型判定 → 模块选择 → 报告格式,主流程无歧义;细节下沉 workflow-details.md |
| 渐进式披露 | A | SKILL.md 196 行保持精简,10 个规则模块 + excel 格式 + 评分指南 + 扩展指南全部下沉 references/,按需加载 |
| 领域特异性/落地性 | A | 文件名模式、SDK 映射规则表、10 个 SDK 检查点、鸿蒙专有名词表、regex pattern 均为可直接执行的具体知识,非泛泛而谈 |
| 可维护性/可扩展性 | A | 规则与 SKILL.md 解耦(改 JSON 即生效),含规则配置模板与扩展指南;index.json 统一索引,enabled 开关支持规则停用 |
| 评测证据 | B | 入库时缺失 evals/(本次评估补齐:evals.json 3 用例 + 植入缺陷输入 + with/without 报告);draft 阶段可接受,转 trial 前建议扩充用例数(≥5)与真实文档样本 |

## 综合评级:**B+(达到 B 级或以上要求 ✅)**

评级依据:结构、披露与领域特异性达到 A 档;拉低项为评测证据刚补齐(用例规模尚小)与 description 触发词可更具体。两项均有明确改进路径,不阻断入库。

## 改进建议(不阻断)

1. evals 用例从 3 扩到 ≥5,增加真实 js-apis 文档脱敏样本与误报率(precision)用例。
2. description 增加文件模式触发词(js-apis-*.md、capi-*.md、interface_sdk-js)。
3. 依据 without-skill 报告的反向发现,在 correctness-rules.json 新增 `permission-mark-match` 检查点。
