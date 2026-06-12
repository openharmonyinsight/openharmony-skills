# ohos-issue-graphics-sysfreeze-analysis 测试用例说明

## 概述

本测试套件包含 **18个测试用例**，验证sysfreeze分析技能的分析结果有效性——即分析是否正确识别阻塞根因、追踪完整阻塞链、合理判定系统与业务优先级、正确过滤干扰线程、产出有效诊断结论。测试设计聚焦于**分析结论的正确性**，而非流程步骤或触发信号的识别。

## 测试分类

### 1. 核心场景测试 (8个)

验证各阻塞场景下分析结果是否正确：阻塞链追踪闭合、根因判定准确、业务场景识别有效、干扰线程正确过滤。

| ID | 测试名称 | 阻塞类型 | 测试文件 | 核心验证点 |
|----|----------|----------|----------|------------|
| 1 | service_block_mutex_blocking_chain | SERVICE_BLOCK + mutex | sysfreeze-service-block | 主线程→UniRenderThread阻塞链追踪（PostAndWait依赖），同一任务持续阻塞判定，排除4个干扰线程 |
| 2 | thread_block_vsync_mutex_chain | THREAD_BLOCK_6S + mutex | sysfreeze-thread-block | IPC线程→主线程阻塞链，hilog vsync超时佐证，排除4个干扰线程 |
| 3 | task_queue_ipc_blocking_analysis | THREAD_BLOCK_6S + IPC + 任务队列 | sysfreeze-task-queue | BinderCatcher跨进程追踪，大数据/HDI贡献因子，VIP队列阻塞，排除5个干扰线程 |
| 4 | post_and_wait_unirender_blocking | THREAD_BLOCK_6S + PostAndWait | sysfreeze-post-and-wait | PostAndWait模式识别，UniRenderThread mutex阻塞源头，排除4个干扰线程 |
| 5 | mutex_deadlock_multi_lock_chain | THREAD_BLOCK_6S + 锁排序 | sysfreeze-mutex-deadlock | 双锁排序阻塞链，从检测线程追溯阻塞链，锁资源与顺序识别，排除4个干扰线程（含相似mutex wait） |
| 6 | low_memory_primary_root_cause | SERVICE_BLOCK + 低内存 | sysfreeze-low-memory | 系统低内存优先判定，业务阻塞为次生效应，排除5个干扰线程 |
| 7 | ipc_block_cross_process_chain | SERVICE_BLOCK + IPC跨进程 | sysfreeze-ipc-block | 跨进程阻塞链闭合，对端进程mutex阻塞识别，排除4个干扰线程 |
| 8 | cond_wait_ddgr_overload_source | THREAD_BLOCK_6S + cond_wait | sysfreeze-cond-wait | DDGRTask运行态过载为阻塞源头，排除4个干扰线程（含相似RequestVsync） |

### 2. 禁止做法测试 (4个)

验证分析结果不会出现因违反禁止做法导致的**错误结论**，含干扰线程误判场景。

| ID | 测试名称 | 禁止内容 | 测试文件 | 防止的错误结论 |
|----|----------|----------|----------|----------------|
| 9 | no_isolate_single_thread | 禁止孤立分析单线程 | sysfreeze-service-block | 不遗漏阻塞链，不误将干扰线程纳入链路 |
| 10 | no_ignore_system_resource_severe | 禁止忽略严重整机资源 | sysfreeze-low-memory | 不将PostAndWait误判为独立根因，不将干扰线程误判为额外根因 |
| 11 | no_treat_running_as_blocked | 禁止将运行线程误判为阻塞 | sysfreeze-cond-wait | 不将DDGRTask state=R误判为"阻塞线程"，不将干扰RSUniRenderThre误判为阻塞源 |
| 12 | no_skip_stack_comparison_implication | 禁止忽略栈对比结论 | sysfreeze-service-block | 不将相同栈仅判为"确认阻塞"，应判定持续同一任务阻塞 |

### 3. 根因判定正确性测试 (3个)

验证根因判定在多因素场景下的正确性——优先级判断、类型区分、方向准确，含干扰项排除。

| ID | 测试名称 | 判定场景 | 测试文件 | 验证点 |
|----|----------|----------|----------|--------|
| 13 | low_memory_vs_business_priority | 系统资源 vs 业务阻塞优先级 | sysfreeze-low-memory | 低内存为首要根因，不误判干扰线程为独立根因 |
| 14 | deadlock_vs_simple_mutex_correctness | 锁排序 vs 简单mutex区分 | sysfreeze-mutex-deadlock | 正确区分多锁排序阻塞链与单锁等待，不将干扰mutex误纳入链 |
| 15 | overload_source_not_blocked_thread | 过载运行线程 vs 阻塞线程区分 | sysfreeze-cond-wait | 正确判定运行过载线程为阻塞源头，不将干扰线程误判为阻塞源 |

### 4. 报告质量测试 (2个)

验证分析报告有效传达阻塞路径和优化建议，含干扰线程排除。

| ID | 测试名称 | 验证内容 | 测试文件 |
|----|----------|----------|----------|
| 16 | blocking_path_complete_description | 阻塞路径完整性（起点→跨进程→终点），排除干扰线程 | sysfreeze-ipc-block |
| 17 | optimization_suggestion_matches_root_cause | 优化建议匹配根因（非泛泛建议，非基于干扰线程） | sysfreeze-mutex-deadlock |

### 5. 深度分析测试 (1个)

验证任务队列时序与优先级分析产出正确结论，含干扰线程排除。

| ID | 测试名称 | 分析维度 | 测试文件 |
|----|----------|----------|----------|
| 18 | task_queue_timing_and_priority_analysis | 任务队列时序 + VIP阻塞影响 + 队列停滞根因，排除干扰线程 | sysfreeze-task-queue |

## 测试文件说明

位于 `files/` 目录下，共8个sysfreeze日志场景：

| 目录名 | 描述 | 关键阻塞特征 | 有效分析应识别的根因 |
|--------|------|------------|---------------------|
| sysfreeze-service-block | render_service SERVICE_BLOCK | mutex PostAndWait + RSUniRenderThread | UniRenderThread RenderFrame阻塞主线程（PostAndWait依赖） |
| sysfreeze-thread-block | render_service THREAD_BLOCK_6S | mutex RequestVsync + vsync hilog | 主线程mutex占有导致IPC线程vsync请求阻塞 |
| sysfreeze-task-queue | render_service THREAD_BLOCK_6S | IPC CommitTransaction + BinderCatcher + 大数据 | IPC阻塞+大数据/HDI延迟致VIP任务停滞 |
| sysfreeze-post-and-wait | render_service THREAD_BLOCK_6S | PostAndWait + UniRenderThread mutex | UniRenderThread Render mutex阻塞致PostAndWait无响应 |
| sysfreeze-mutex-deadlock | apsmgr THREAD_BLOCK_6S | SwingFrameRate mutex + FrameRateControl recursive_mutex | 锁排序阻塞链（IPC延长锁持有时间） |
| sysfreeze-low-memory | render_service SERVICE_BLOCK | ReclaimAvailBuffer=5000 + MemoryOverflow | 系统低内存为首要根因，业务阻塞为次生效应 |
| sysfreeze-ipc-block | render_service SERVICE_BLOCK | BinderCatcher + display_manager peer mutex | display_manager SetScreenPowerStatus mutex阻塞跨进程链 |
| sysfreeze-cond-wait | render_service THREAD_BLOCK_6S | condition_variable::wait + DDGRTask state=R utime=15000 | DDGRTask执行过载为阻塞源头 |

## 断言类型

所有断言验证**分析结论的正确性**，而非流程步骤是否执行：

| 断言类型 | 说明 |
|----------|------|
| blocking_chain_* | 验证阻塞链是否正确追踪到源头线程 |
| root_cause_* | 验证根因判定是否准确（阻塞源、优先级、类型） |
| business_scenario_* | 验证业务场景是否正确识别 |
| same_task_blocking_concluded | 验证是否从相同栈正确判定持续同一任务阻塞 |
| vip_queue_blocking_concluded | 验证是否正确判定VIP任务阻塞导致队列停滞 |
| deadlock_pattern_correctly_identified | 验证是否正确识别锁排序阻塞链模式 |
| system_resource_as_primary_root_cause | 验证是否正确优先判定系统资源问题 |
| ddgr_task_as_blocking_source_not_blocked | 验证是否正确识别运行线程为阻塞源而非被阻塞 |
| hilog_evidence_corroborates | 验证hilog证据是否用于佐证分析结论 |
| ipc_blocking_with_binder_traced | 验证是否通过BinderCatcher正确追踪跨进程链 |
| peer_mutex_blocking_identified | 验证是否正确识别对端进程线程阻塞原因 |
| suggestions_address_lock_ordering | 验证优化建议是否针对具体根因（锁排序） |
| blocking_path_start_end_marked | 验证报告中阻塞路径是否完整标注 |
| interference_threads_correctly_filtered | 验证是否正确排除干扰线程（无关空闲/表面相似/后台线程） |
| interference_threads_not_in_chain | 验证阻塞链中不含干扰线程 |
| interference_threads_not_misidentified | 验证不将干扰线程误判为阻塞源或阻塞链参与者 |
| interference_threads_not_over_interpreted | 验证不将干扰线程过度解读为额外根因 |
| interference_mutex_not_in_lock_chain | 验证不将干扰mutex误纳入锁排序阻塞链 |
| interference_threads_not_blocking_source | 验证不将干扰线程误判为阻塞源头 |
| interference_threads_excluded_from_path | 验证阻塞路径中不含干扰线程 |
| interference_render_thread_not_misidentified | 验证不将干扰渲染线程误判为阻塞源 |

## 测试覆盖率

| 类别 | 数量 | 覆盖重点 |
|------|------|----------|
| 核心场景 | 8 | 8种阻塞类型全覆盖 + 干扰线程过滤 |
| 禁止做法 | 4 | 防止遗漏阻塞链/忽略整机资源/误判运行线程/忽略栈对比含义 + 防止干扰线程误判 |
| 根因判定 | 3 | 系统vs业务优先级/锁排序vs mutex区分/过载vs阻塞区分 + 干扰线程排除 |
| 报告质量 | 2 | 阻塞路径完整性/优化建议匹配度 + 干扰线程排除 |
| 深度分析 | 1 | 任务队列时序与优先级分析 + 干扰线程排除 |
| **总计** | **18** | **分析结论有效性全覆盖 + 干扰线程过滤验证** |

## 版本历史

- v1.0 (2026-06-11): 初始版本，包含18个测试用例
- v1.1 (2026-06-12): 为每个测试数据文件添加3-5个干扰线程堆栈，新增interference_threads相关断言验证干扰线程过滤能力
- v1.2 (2026-06-12): 修复测试数据与断言问题：(1) sysfreeze-task-queue修正RSUniRenderThre线程名/栈不匹配；(2) sysfreeze-cond-wait修正栈帧编号乱序；(3) Test 1修正"lock holder"为"blocking source(PostAndWait依赖)"；(4) Test 5/14/17将"deadlock"定性改为"锁排序阻塞链"，阻塞链从检测线程9876开始追溯；(5) README同步更新描述