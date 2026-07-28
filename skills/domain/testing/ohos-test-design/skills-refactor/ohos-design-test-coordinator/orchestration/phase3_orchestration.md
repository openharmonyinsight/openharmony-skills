# 阶段3 编排：Demo流水线（协调器执行步骤）

> 本文件承载 Phase3 的协调器操作步骤。SKILL.md 阶段3 仅保留三决策树（条件执行判断 / 领域确认 / 编译状态四分支）+ 两条 NEVER + 配置表。
> **职责边界**：`orchestration/` = 协调器自己执行的步骤；`phases/` = Agent 骨架；`rules/` = Agent 按需 Read 的规则。

## 编排器执行流程（操作步骤）

### 步骤3：委托 ohos-design-test-demo-pipeline（spawn Agent加载 ohos-design-test-demo-pipeline skill 执行所有子阶段）

- Agent prompt构造：使用skill工具加载`ohos-design-test-demo-pipeline` → 在指令前追加上下文信息（输入文件路径、输出目录、领域名称）→ 设置foreground模式
- Agent内部自动完成4个子阶段（UI设计→代码生成→编译验证与修复→完成）
- 返回摘要：Demo页面数、UI控件数、操作模式数、测试点覆盖率、源文件数、控件ID数、权限声明、编译状态（BUILD SUCCESSFUL/FAILED/SDK版本过低/HVIGORW_NOT_FOUND）、修复次数、缺失API清单（如有）、环境缺失详情（如有）

> 步骤1「条件执行判断」、步骤2「领域确认」、步骤4「编译状态四分支表」保留在 SKILL.md 阶段3 决策树。以下为三个编译异常子流程的详细操作。

### SDK版本过低处理流程

1. 从返回摘要提取缺失API清单
2. 记录T3（confirmation_started_at）
3. AskUserQuestion：
   - 问题：`"Demo编译验证检测到SDK缺失API：{缺失API清单}，请选择处理方式："`
   - 选项①：`"我已替换SDK，重新编译"` → 记录T4，重新spawn Agent执行编译验证（耗时计入optimization_duration_seconds）
   - 选项②：`"跳过，继续后续流程"` → 记录T4，标注Demo编译为"未验证（SDK缺失）"，进入Phase4
4. 记录T6

### HVIGORW_NOT_FOUND处理流程

1. 从返回摘要提取环境缺失详情
2. 记录T3
3. AskUserQuestion：
   - 问题：`"未找到hvigorw命令，需安装HarmonyOS command-line-tools，请选择处理方式："`
   - 选项①：`"我已安装，重新检查"` → 记录T4，重新spawn Agent执行编译验证
   - 选项②：`"跳过，继续后续流程"` → 记录T4，标注Demo编译为"未验证（环境缺失）"，进入Phase4
4. 记录T6

### BUILD FAILED处理流程

1. 记录T3
2. AskUserQuestion：
   - 问题：`"Demo编译失败（已修复{修复次数}次），请选择处理方式："`
   - 选项①：`"继续重试修复"` → 记录T4，重新spawn Agent执行编译验证（耗时计入optimization_duration_seconds）
   - 选项②：`"跳过，继续后续流程"` → 记录T4，标注Demo编译为"未验证（编译失败）"，进入Phase4
3. 记录T6

### 步骤5：清理临时文件

- 删除demo_test_points.md
