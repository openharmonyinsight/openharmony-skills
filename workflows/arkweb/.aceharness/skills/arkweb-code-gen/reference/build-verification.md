# 编译验证与修复循环方法

本文件定义编译-修复循环的执行逻辑、Agent 指令模板和内层检视规则。
由 Team Lead 在 Phase 8 编排时读取。

## Contents

- 循环逻辑
- Agent 指令模板（builder / coder / reviewer）
- 内层检视循环规则
- 编译报告路径

## 循环逻辑

```
max_rounds = 10
current_round = 1

while current_round <= max_rounds:
    Step 8.1: Team Lead 指示 arkweb-builder 执行编译
    Step 8.2: arkweb-builder 执行编译并报告结果
        - 编译成功（exit code 0）→ Phase 8 完成
        - 编译失败 → 生成结构化报错报告，继续 Step 8.3
    Step 8.3: Team Lead 将报错报告传递给 arkweb-coder
        - arkweb-coder 仅修复报错报告中涉及的文件
        - 禁止修改与编译错误无关的代码
    Step 8.4: arkweb-reviewer 检视修复（内层循环，最多 3 轮）
    Step 8.5: current_round += 1，回到 Step 8.1

if current_round > max_rounds:
    → 向用户报告编译仍未通过
    → 列出最后一轮的错误摘要
    → 建议人工介入
```

## Agent 指令模板

### 给 builder Agent 的指令

```
请执行 ArkWeb 编译。

ArkWeb 根目录：{ARKWEB_ROOT}
产品：{product，默认 rk3568_64}
目标：{target，默认 w}

编译命令：cd {ARKWEB_ROOT} && ./build_arkweb.sh {product} -t {target} -A
超时：4 小时

编译成功 → 输出成功报告到 /tmp/arkweb_build_error_report.md
编译失败 → 运行 {skill-dir}/scripts/analyze_build_error.sh {product} {ARKWEB_ROOT}
           → 将分析结果整理为结构化报告输出到 /tmp/arkweb_build_error_report.md
```

### 给 coder Agent 的指令（编译失败时）

```
请根据编译报错报告修复编译错误。

报错报告路径：/tmp/arkweb_build_error_report.md
需求设计文档路径：{用户提供的文档路径}

【严格限制】
1. 仅修复报错报告中列出的编译错误
2. 仅修改与编译错误直接相关的文件
3. 禁止修改与编译错误无关的代码
4. 禁止做"顺便改进"或重构
5. 遵循 ArkWeb 解耦机制（_for_include 规范）

请按以下步骤执行：
1. Read 报错报告，理解每个编译错误
2. 使用 TodoWrite 创建修复任务列表
3. 逐个修复编译错误
4. 输出变更文件清单

这是编译修复循环的第 {current_round}/{max_rounds} 轮。
```

### 给 reviewer Agent 的指令（编译修复检视）

```
请检视以下编译错误修复。

报错报告路径：/tmp/arkweb_build_error_report.md
修复的文件：{本轮修复的文件列表}
检视报告输出路径：/tmp/arkweb_review_report.md

重点关注：
1. 编译错误是否已正确修复
2. 修复是否引入了新的编译错误或逻辑问题
3. 修复是否符合 ArkWeb 编码规范（_for_include 解耦机制）
4. 修复范围是否最小化（没有修改无关代码）
```

## 内层检视循环规则

```
max_inner_rounds = 3
inner_round = 1

while inner_round <= max_inner_rounds:
    reviewer 检视修复
    如果 BLOCKER/CRITICAL == 0:
        → 退出内层循环，进入下一轮编译
    如果 BLOCKER/CRITICAL > 0:
        → coder 修复 → inner_round += 1

if inner_round > max_inner_rounds:
    → 不再等待检视通过，直接进入下一轮编译
    → 让编译器验证当前修复是否足够
```

## 编译报告路径

| 文件 | 路径 |
|------|------|
| 编译报错报告 | `/tmp/arkweb_build_error_report.md` |
| 检视报告 | `/tmp/arkweb_review_report.md` |
| 错误分析脚本 | `{skill-dir}/scripts/analyze_build_error.sh` |
