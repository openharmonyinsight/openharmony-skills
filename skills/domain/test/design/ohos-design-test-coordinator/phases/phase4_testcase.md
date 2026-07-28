# 阶段4：测试用例细化骨架

> 本文件内容将填入SKILL.md统一Prompt模板。详细执行规则见 `rules/phase4_rules.md`，知识库匹配规则见 `rules/knowledge_usage_guide.md`。

## 任务
经验库匹配 + 分批规划 + 并行生成测试用例

## NEVER约束
- NEVER 跳过或快速执行phase4——必须完整执行
- NEVER 输出不完整测试用例——必须完整输出所有用例
- NEVER 使用省略语句代替实际用例——不得使用"..."、"等等"
- NEVER 直接引用测试点内容——预置条件、测试步骤、预期结果必须展开
- NEVER 中途出错静默跳过——失败批次必须明确告警并记录

## 核心约束（必须理解）
- 测试步骤展开完整：不直接复制测试点内容
- 验证完整性：预期结果包含外部可观测证据
- 白盒用例风格（XTS）：不出现Demo控件操作
- 内部ID隔离：用例内容不含内部追溯ID
- 继承一致性：用例字段与关联测试点一致
- 单测试点优先单用例：验证维度优先合并到同一用例不同步骤

---

## 两轮执行说明（强制执行）

Phase4分为两轮执行：
- **第一轮**：规划Agent执行（经验库匹配+分批规划）
- **第二轮**：协调器并行spawn多个执行Agent（≤4），注入knowledge_match.md

---

## 第一轮：经验库匹配+分批规划（规划Agent）

### 输入
- 测试点文件：{test_point_design.md路径}
- 输出目录：{output_dir}
- 经验库路径：experience_library/general/ + experience_library/domain/{领域路径}/

### 输出
- 追加到knowledge_match.md：细化步骤匹配结果表格
- 分批计划：返回给协调器

### 执行步骤
1. **经验库匹配**：按知识库模式执行（mcp/local/none），匹配规则详见 `rules/knowledge_usage_guide.md` §2-3、§4层级隔离规则。经验库为空时跳过匹配，追加空§3表格头。
2. **分批规划**：一个US对应一个batch_id，每批≤30个用例（防止AI输出截断），测试点范围连续，TP-ADD测试点必须单独成批（batch_ADD_1）。详见 `rules/phase4_rules.md`。

### 第一轮返回摘要（强制执行）

> 协调器从摘要文本中解析信息并spawn执行Agent。

```
经验库匹配完成：
- 匹配条目数：X条（经验库为空时标注0条）
- 已追加到：knowledge_match.md

批次规划完成：
| batch_id | tp_range | estimated_cases |
|----------|----------|-----------------|
| batch_US01_1  | TP-US01-001~TP-US01-015 | 25 |
| batch_US02_1  | TP-US02-001~TP-US02-010 | 18 |
批次总数：X个
预计用例总数：X个
```

---

## 第二轮（及后续轮次）：并行生成测试用例（执行Agent）

> 协调器根据批次总数执行多轮并行spawn，每轮≤4个Agent。Agent仅负责生成用例，不关心轮次逻辑。

### 输入（协调器注入）
- requirement_analysis.md路径
- test_point_design.md路径
- knowledge_match.md路径（已更新）
- phase4_rules.md路径
- phase4_testcase.md骨架文件路径
- 输出目录路径（含batches子目录）
- 分配的测试点范围

### 输出
- {output_dir}/batches_phase4/batch_{主单元编号}_{批次号}.md

### 执行步骤
1. **读取knowledge_match.md**：定位§3"用例细化匹配结果"章节→解析表格→按动作因子匹配当前测试点场景→补充测试步骤和预期结果→将匹配到的 CR 条目编号追加到用例来源"经验库"段。详见 `rules/knowledge_usage_guide.md`。
2. **生成测试用例**：按执行方式分流描述风格（XTS→白盒/黑盒自动化→Demo/手工→人工），测试步骤与数据合一，继承规则（测试类型/技术/级别/执行方式/来源直接继承测试点：来源继承测试点 spec+经验库(TE) 段，再追加本阶段 CR 到经验库段；对抗补旧时追加对抗段）。详见 `rules/phase4_rules.md`。

**输出格式**、**用例编号规则**（TC-{主单元编号}-{序号}）、**TP-ADD处理规则**、**Demo关联规则**详见 `rules/phase4_rules.md` 输出格式规范。

### 返回摘要（强制执行）

**第二轮返回（执行阶段）：**
```
batch_id：{batch_id}（如 batch_US01_1）
测试点范围：{tp_range}
生成用例数：X个
经验库匹配条目使用数：X条
输出文件：batch_{主单元编号}_{批次号}.md（如 batch_US01_1.md）
```
