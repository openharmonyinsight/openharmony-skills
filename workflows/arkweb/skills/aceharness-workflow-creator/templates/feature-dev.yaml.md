# 模板：功能开发（红蓝对抗）

适用于新功能开发、重构、迁移等需要设计→实施→验证的场景。

```yaml
workflow:
  name: 功能名称
  description: 一句话描述
  mode: state-machine
  maxTransitions: 30

  states:
    - name: 设计
      description: 设计方案
      requireHumanApproval: true
      isInitial: true
      isFinal: false
      steps:
        - name: 方案设计
          agent: architect
          role: defender
          task: |
            设计完整方案：
            1. 模块划分和职责
            2. 接口定义和数据结构
            3. 关键流程和边界处理
        - name: 方案攻击
          agent: design-breaker
          role: attacker
          task: 攻击设计方案，寻找缺陷、遗漏、安全问题、边界条件
        - name: 方案裁决
          agent: design-judge
          role: judge
          task: |
            评估方案和攻击发现，输出裁决 JSON：
            {"verdict":"pass|conditional_pass|fail","summary":"..."}
      transitions:
        - to: 实施
          condition: { verdict: pass }
          priority: 1
          label: 方案通过
        - to: 设计
          condition: { verdict: conditional_pass }
          priority: 2
          label: 需修复设计
        - to: 终止
          condition: { verdict: fail }
          priority: 3
          label: 设计不可行

    - name: 实施
      description: 编码实现
      isInitial: false
      isFinal: false
      steps:
        - name: 编码
          agent: developer
          role: defender
          task: 根据设计方案实现功能
        - name: 代码攻击
          agent: code-hunter
          role: attacker
          task: 攻击代码，寻找 bug、安全漏洞、边界问题
        - name: 代码裁决
          agent: fix-judge
          role: judge
          task: |
            裁决代码质量，输出 JSON：
            {"verdict":"pass|conditional_pass","summary":"..."}
      transitions:
        - to: 验证
          condition: { verdict: pass }
          priority: 1
          label: 代码通过
        - to: 实施
          condition: { verdict: conditional_pass }
          priority: 2
          label: 需继续修复

    - name: 验证
      description: 构建和测试
      isInitial: false
      isFinal: false
      steps:
        - name: 构建测试
          agent: developer
          role: defender
          task: 执行构建和测试
        - name: 验证裁决
          agent: tester
          role: judge
          task: |
            验证结果，输出 JSON：
            {"verdict":"pass|fail","summary":"..."}
      transitions:
        - to: 完成
          condition: { verdict: pass }
          priority: 1
          label: 验证通过
        - to: 实施
          condition: { verdict: fail }
          priority: 2
          label: 验证失败，返回修复

    - name: 完成
      description: 开发完成
      isInitial: false
      isFinal: true
      steps:
        - name: 交付报告
          agent: documentation-writer
          role: defender
          task: 生成交付报告
      transitions: []

    - name: 终止
      description: 异常终止
      isInitial: false
      isFinal: true
      steps:
        - name: 终止记录
          agent: documentation-writer
          role: defender
          task: 记录终止原因
      transitions: []

context:
  projectRoot: /absolute/path/to/project
  requirements: |
    需求描述和验收标准
  timeoutMinutes: 180
```
