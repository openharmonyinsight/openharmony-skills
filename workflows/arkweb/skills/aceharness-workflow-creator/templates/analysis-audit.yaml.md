# 模板：分析审计

适用于代码审计、安全分析、技术调研。

```yaml
workflow:
  name: 分析审计
  description: 一句话描述
  mode: state-machine
  maxTransitions: 30

  states:
    - name: 数据收集
      description: 收集分析所需的数据和事实
      requireHumanApproval: true
      isInitial: true
      isFinal: false
      steps:
        - name: 收集数据
          agent: developer
          role: defender
          task: |
            收集分析所需数据：
            1. 确定分析范围和目标
            2. 收集相关代码、文档、日志
            3. 整理已知事实和初步发现
        - name: 收集裁决
          agent: fix-reviewer
          role: judge
          task: |
            评估数据收集的完整性，输出裁决 JSON：
            {"verdict":"pass|conditional_pass","summary":"..."}
      transitions:
        - to: 深度分析
          condition: { verdict: pass }
          priority: 1
          label: 数据充分
        - to: 数据收集
          condition: { verdict: conditional_pass }
          priority: 2
          label: 数据不足，继续收集

    - name: 深度分析
      description: 对收集的数据进行深度分析
      isInitial: false
      isFinal: false
      steps:
        - name: 执行分析
          agent: developer
          role: defender
          task: |
            对收集的数据进行深度分析：
            1. 按分析维度逐项展开
            2. 标注关键发现和风险点
            3. 给出初步结论和证据链
        - name: 质疑分析
          agent: code-hunter
          role: attacker
          task: 质疑分析结论和覆盖度，检查是否有遗漏维度、错误推断、证据不足
        - name: 分析裁决
          agent: fix-reviewer
          role: judge
          task: |
            评估分析质量和攻击发现，输出裁决 JSON：
            {"verdict":"pass|conditional_pass|fail","summary":"..."}
      transitions:
        - to: 交叉验证
          condition: { verdict: pass }
          priority: 1
          label: 分析充分
        - to: 深度分析
          condition: { verdict: conditional_pass }
          priority: 2
          label: 分析不足，继续深挖
        - to: 数据收集
          condition: { verdict: fail }
          priority: 3
          label: 数据不足，返回收集

    - name: 交叉验证
      description: 交叉验证分析结论
      isInitial: false
      isFinal: false
      steps:
        - name: 补充验证
          agent: developer
          role: defender
          task: |
            对分析结论进行交叉验证：
            1. 用不同方法或数据源验证关键结论
            2. 补充边界场景验证
            3. 整理最终结论和置信度
        - name: 验证裁决
          agent: fix-reviewer
          role: judge
          task: |
            裁决验证结果，输出 JSON：
            {"verdict":"pass|conditional_pass","summary":"..."}
      transitions:
        - to: 报告输出
          condition: { verdict: pass }
          priority: 1
          label: 验证通过
        - to: 交叉验证
          condition: { verdict: conditional_pass }
          priority: 2
          label: 验证不充分，继续补充

    - name: 报告输出
      description: 生成分析报告
      isInitial: false
      isFinal: false
      steps:
        - name: 撰写报告
          agent: documentation-writer
          role: defender
          task: |
            生成分析报告：
            1. 分析背景和范围
            2. 关键发现和风险等级
            3. 建议和行动项
        - name: 报告裁决
          agent: fix-reviewer
          role: judge
          task: |
            评估报告质量，输出 JSON：
            {"verdict":"pass|conditional_pass","summary":"..."}
      transitions:
        - to: 完成
          condition: { verdict: pass }
          priority: 1
          label: 报告通过
        - to: 报告输出
          condition: { verdict: conditional_pass }
          priority: 2
          label: 报告需完善

    - name: 完成
      description: 分析完成
      isInitial: false
      isFinal: true
      steps:
        - name: 交付报告
          agent: documentation-writer
          role: defender
          task: 交付最终分析报告
      transitions: []

context:
  projectRoot: /absolute/path/to/project
  requirements: |
    分析目标和范围描述
  timeoutMinutes: 180
```
