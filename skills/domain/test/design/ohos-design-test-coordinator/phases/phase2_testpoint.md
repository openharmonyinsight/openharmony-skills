# 阶段2：测试点生成骨架

> 本文件内容将填入SKILL.md统一Prompt模板。详细执行规则见 `rules/phase2_rules.md`，知识库匹配规则见 `rules/knowledge_usage_guide.md`。

## 任务
经验库匹配 + 分批规划 + 并行生成测试点

## NEVER约束
- NEVER 一个US拆分到多个批次——一个US只能由一个Agent生成所有测试点
- NEVER 中途出错静默跳过——失败批次必须明确告警并记录
- NEVER 内容列使用内部追溯ID——内部ID仅出现在"来源"列

## 核心约束（必须理解）
- 验证完整性：预期结果必须包含外部可观测证据
- 零推导原则：仅输出原文档明确描述
- 风险分级：P0(高风险4-5类异常值)、P1(中风险2-3类)、P2(低风险1-2类)、P3(防御性1类)
- 测试对象差异化：判定来源为knowledge_match.md§1.1交付推断结果表，仅对测试对象生成测试点，采纳策略详见 `rules/knowledge_usage_guide.md` §2.2

---

## 两轮执行说明（强制执行）

Phase2分为两轮执行：
- **第一轮**：规划Agent执行（经验库匹配+分批规划）
- **第二轮**：协调器并行spawn多个执行Agent（≤4），注入knowledge_match.md

---

## 第一轮：经验库匹配+分批规划（规划Agent）

### 输入
- 需求文件：{requirement_analysis.md路径}
- 输出目录：{output_dir}
- 领域名称：{domain}
- 测试技术数据：{output_dir}/testing_technology.json（脚本生成）
- 经验库路径：experience_library/general/ + experience_library/domain/{领域路径}/

### 输出
- 追加到knowledge_match.md：测试经验匹配结果表格
- 分批计划：返回给协调器

### 执行步骤
1. **经验库匹配**：按知识库模式执行（mcp/local/none），匹配规则详见 `rules/knowledge_usage_guide.md` §2-3、§4层级隔离规则。经验库为空时跳过匹配，追加空§2表格头。
2. **分批规划**：一个测试对象主单元对应一个batch_id，同一主单元测试点不拆分到多批。仅写入类主单元和独立查询类主单元生成batch_id（有前置依赖的查询类主单元不生成独立batch，混合校验时仅权限/安全部分独立生成测试点）。详见 `rules/phase2_rules.md` 匹配执行步骤。
3. **前置摘要提取**：识别标注"前置依赖"的主单元，提取前置US关键信息（前置操作、可产生状态、观测方式、前置依赖→输出映射、可观测查询US）。

### 第一轮返回摘要（强制执行）

> 协调器从摘要文本中解析信息并spawn执行Agent。

```
经验库匹配完成：
- 匹配条目数：X条（经验库为空时标注0条）
- 已追加到：knowledge_match.md

批次规划完成：
| batch_id | unit_id | estimated_tps |
|----------|---------|---------------|
| batch_US_1  | US-01   | 15         |
| batch_US_2  | US-02   | 12         |
批次总数：X个
预计测试点总数：X个

前置摘要：
- US-01（写入类）→ 可观测查询US=US-02(getPreference), US-03(isEnabled)
- US-02 → 前置US-01: 前置操作=setAppClonePreference(bundleName,{mode,index?}), 可产生的状态={mode:ALWAYS_ASK,MAIN_APP,CLONE_APP(index:1-5)}, 前置依赖→输出映射=[...]
（无前置依赖的主单元不列出）
```

---

## 第二轮（及后续轮次）：并行生成测试点（执行Agent）

> 协调器根据批次总数执行多轮并行spawn，每轮≤4个Agent。Agent仅负责生成测试点，不关心轮次逻辑。

### 输入（协调器注入）
- requirement_analysis.md路径
- knowledge_match.md路径（已更新）
- testing_technology.json路径
- phase2_rules.md路径
- phase2_testpoint.md骨架文件路径
- 输出目录路径（含batches子目录）
- 分配的主单元ID
- 前置摘要（仅当前主单元有前置依赖时注入，从规划Agent摘要中提取）

### 输出
- {output_dir}/batches_phase2/batch_{unit_id}.md

### 执行步骤
1. **读取knowledge_match.md**：定位§1.1交付推断结果→获取测试策略标识；定位§2测试经验匹配结果→按主单元ID筛选关联US→提取完整经验内容→直接采纳匹配到的经验。详见 `rules/knowledge_usage_guide.md` §2.2采纳策略。
2. **生成测试点**：按场景风险驱动生成（P0场景4-5条、P1场景1-3类异常值、P2场景1-2类、P3防御性1条）。测试技术数据读取规则详见 `rules/phase2_rules.md`。
3. **防重复**：跨US重叠处理、前后场景合并与聚合规则详见 `rules/phase2_rules.md`。

**输出表格格式**、**测试点编号规则**（TP-{主单元ID}-{序号}）、**batch文件结构**详见 `rules/phase2_rules.md` 输出格式规范。

### 返回摘要（强制执行）

```
batch_id：{batch_id}（如 batch_US_1）
主单元ID：{unit_id}
生成测试点数：X个
跳过场景数：X个
经验库匹配条目使用数：X条
输出文件：batch_{unit_id}.md（如 batch_US_1.md）
```
