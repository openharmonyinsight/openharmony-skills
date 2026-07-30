# 阶段3：Demo流水线（委托ohos-design-test-demo-pipeline）

> 本文件内容将填入SKILL.md统一Prompt模板。编排器执行流程（委托prompt构造、编译异常子流程、临时文件清理）详见 `orchestration/phase3_orchestration.md`；条件执行判断/领域确认/编译状态分支决策树见 SKILL.md 阶段3章节。

## 任务
为非XTS测试点生成Demo应用，委托ohos-design-test-demo-pipeline独立技能执行。

## NEVER约束
- NEVER 所有测试点均为XTS时强制执行Demo流水线——应跳过并直接进入Phase4
- NEVER 为XTS测试点生成Demo——仅为非XTS测试点（黑盒自动化、API性能自动化、手工）生成Demo
- NEVER 跳过条件执行判断——必须先读取test_point_design.md判断是否需要执行Demo
- NEVER Demo流水线完成后不删除临时文件——必须删除demo_test_points.md
- NEVER 无领域名称时跳过领域确认——必须使用AskUserQuestion询问用户API所属领域

## 核心约束（必须理解）
- 条件执行：所有测试点为XTS时跳过，存在非XTS时执行
- 委托执行：本阶段委托ohos-design-test-demo-pipeline独立技能，包含4个子阶段（UI设计→代码生成→编译验证与修复→完成）
- 领域确认：有领域名称直接使用，无领域名称必须询问用户
- 自动执行：Agent内部自动完成所有子阶段，返回摘要后协调器按"返回摘要处理"流程检查编译状态并决定是否询问用户

---

## 输入
- 测试点文件：{output_dir}/demo_test_points.md（仅包含非XTS测试点，由协调器过滤生成）
- 需求分析文件：{output_dir}/requirement_analysis.md
- 领域名称：{domain}
- 输出目录：{output_dir}

## 输出
- {output_dir}/demo_design.md

## 执行方式

本阶段委托给ohos-design-test-demo-pipeline独立技能执行，包含4个子阶段：
- 子阶段1：Demo UI设计
- 子阶段2：Demo代码生成
- 子阶段3：编译验证与修复（独立执行编译验证和修复循环）
- 子阶段4：完成

**Agent prompt构造方式**：
1. 使用 skill 工具加载 `ohos-design-test-demo-pipeline` 获取完整指令
2. 在指令前追加上下文信息（输入文件路径、输出目录、领域名称）
3. 设置Agent为foreground模式执行
4. Agent内部自动完成所有子阶段

## 返回摘要
- Demo页面数、UI控件数、操作模式数、测试点覆盖率
- 源文件数、控件ID数、权限声明
- 编译状态（BUILD SUCCESSFUL/FAILED/SDK版本过低/HVIGORW_NOT_FOUND）
- 修复次数
- 缺失API清单（如有）
- 环境缺失详情（如有）
