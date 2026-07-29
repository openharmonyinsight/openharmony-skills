# 阶段5：验证与导出骨架

> 本文件内容将填入SKILL.md统一Prompt模板。详细执行规则见 `rules/phase5_rules.md`。

## 任务
验证测试用例质量，导出test_cases.xlsx，清理临时文件。

## NEVER约束
- NEVER P0问题存在时导出——P0问题=0才可导出
- NEVER 导出非xlsx格式——仅允许导出xlsx格式
- NEVER xlsx列数≠18——必须使用18列导出（A-R列）
- NEVER 导出前清理临时文件——导出成功后必须立即删除临时文件
- NEVER xlsx预期结果仅依赖接口返回——必须包含外部可观测证据
- NEVER xlsx内容列含内部追溯ID——仅允许在"备注"列用于追溯

## 核心约束（必须理解）
- 验证完整性检查：预期结果验证到外部可观测效果
- P0门禁：P0问题=0才可导出
- Excel列数：18列（A-R）
- 用例编号规则：用户指定起始值或默认case_id_temp_001
- 临时文件清理：导出成功后立即删除临时文件

## 输入
- 测试用例文件：{test_cases.md路径}
- 测试点文件：{test_point_design.md路径}
- 用例编号起始值：{USER_START_ID}
- 输出目录：{output_dir}

## 输出
- {output_dir}/validation_report.md
- {output_dir}/test_cases.xlsx

## 详细规则（必须Read）
请Read {rules/phase5_rules.md}获取完整执行规则。

## 返回摘要
- 综合评分：X/100分
- P0问题：X个 / P1问题：X个 / P2问题：X个
- 验证结论：通过/不通过（P0=0且综合评分≥80分）
- 导出文件：test_cases.xlsx（X行，X字节）
- P0修复情况：未修复 / 已修复X个（如有）
- Excel一致性：通过（一次/重试1次/重试2次）或 X项不一致（已记录）
- 空值告警：X条（如有）
- 验证完整性检查：通过 / 发现X处仅依赖手段层反馈（已修复/已记录）
- 自检结果：X/X项通过