# 阶段4对抗：测试用例对抗评估骨架

> 本文件内容将填入SKILL.md统一Prompt模板。详细执行规则见 `rules/phase4_adv_rules.md`。

## 任务
执行测试用例对抗评估，追加adversarial_report.md第二部分。

## NEVER约束
- NEVER 脱离脚本校验虚构覆盖率——必须调用脚本获取准确数据
- NEVER 超过3轮对抗循环——最多3轮，不达标则强制终止
- NEVER 脱离测试点生成补充用例——必须基于遗漏项
- NEVER 补充用例编号使用TC-ADD——必须使用TC-{NNN}顺延编号
- NEVER 跳过重复用例检测——充分性达标后必须执行
- NEVER 跳过质量检查——重复检测完成后必须执行
- NEVER 生成资料测试用例——由脚本自动生成

## 核心约束（必须理解）
- 充分性评分：测试点覆盖率≥95%、关键测试点覆盖率≥98%
- 循环对抗：最多3轮
- 重复检测：充分性达标后执行重复用例检测
- 质量检查：重复检测完成后执行质量评分
- 补充用例编号：TC-{NNN}（顺延）

## 输入
- 测试用例文件：{test_cases.md路径}
- 测试点文件：{test_point_design.md路径}
- 对抗基础数据：{phase4_adversary.json路径}
- 输出目录：{output_dir}

## 输出
- {output_dir}/adversarial_report.md（追加第二部分）
- 补充测试用例（追加写入test_cases.md）

## 详细规则（必须Read）
请Read {rules/phase4_adv_rules.md}获取完整执行规则。

## 返回摘要
- 测试点覆盖率：XX%（达标/不达标）
- 关键测试点覆盖率：XX%（达标/不达标）
- 充分性达标状态：PASS/FAIL
- 补充测试用例：X个
- 对抗轮次：X轮
- 重复用例：X个检测到（Y个自动合并删除）
- 平均质量得分：XX分（达标/不达标）
- 整体达标状态：PASS/FAIL