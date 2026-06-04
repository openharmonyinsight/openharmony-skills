# ohos-issue-graphics-sysfreeze-analysis 测试用例说明

## 概述

本测试套件包含 **62个测试用例**，覆盖sysfreeze/appfreeze分析技能的核心功能、边界情况、文档使用、工作流和禁止做法。

## 测试分类

### 1. 技能触发测试 (19个)

#### 应该触发 (10个)
| ID | 测试名称 | 触发词 |
|----|----------|--------|
| 1 | trigger_sysfreeze_analysis | "sysfreeze日志+进程卡住" |
| 2 | trigger_appfreeze_analysis | "appfreeze日志+线程阻塞" |
| 3 | trigger_service_block | "SERVICE_BLOCK+服务阻塞" |
| 4 | trigger_thread_block_6s | "THREAD_BLOCK_6S故障" |
| 5 | trigger_ipc_deadlock | "IPC死锁+追踪阻塞链" |
| 6 | trigger_process_stuck_keyword | "进程卡住+freeze" |
| 7 | trigger_task_queue_block | "任务队列阻塞" |
| 8 | trigger_deadlock_keyword | "死锁+互相等锁" |
| 9 | trigger_vsync_timeout | "vsync处理超时+线程阻塞" |
| 10 | trigger_block_keyword_english | "blocked/frozen (英文)" |

#### 不应触发 (9个)
| ID | 测试名称 | 场景 |
|----|----------|------|
| 11 | negative_trigger_perf_optimization | 性能优化（无阻塞） |
| 12 | negative_trigger_app_logic_error | 应用逻辑错误（无系统级阻塞） |
| 13 | negative_trigger_non_graphics_freeze | 非图形模块freeze |
| 14 | negative_trigger_ui_development | UI界面开发 |
| 15 | negative_trigger_build_error | 编译错误 |
| 16 | negative_trigger_code_review | 代码review |
| 17 | negative_trigger_unit_test | 单元测试 |
| 18 | negative_trigger_cppcrash | cppcrash崩溃（非freeze） |
| 19 | negative_trigger_log_severely_missing | 日志严重缺失 |

### 2. 核心场景测试 (14个)
| ID | 测试名称 | 阻塞类型 | 测试文件 |
|----|----------|----------|----------|
| 20 | service_block_mutex_full | SERVICE_BLOCK+互斥锁 | sysfreeze-service-block |
| 21 | thread_block_6s_full | THREAD_BLOCK_6S+mutex | sysfreeze-thread-block |
| 22 | mutex_deadlock_full | 互斥锁死锁（多线程阻塞链） | sysfreeze-mutex-deadlock |
| 23 | ipc_block_full | IPC阻塞+BinderCatcher | sysfreeze-ipc-block |
| 24 | low_memory_freeze_full | 低内存+整机资源优先 | sysfreeze-low-memory |
| 25 | task_queue_block_full | 任务队列+IPC阻塞 | sysfreeze-task-queue |
| 26 | cond_wait_full | 条件变量阻塞+DrawOp异步 | sysfreeze-cond-wait |
| 27 | post_and_wait_full | PostAndWait+RSUniRenderThread | sysfreeze-post-and-wait |
| 55 | thermal_throttle_analysis | 热限频分析 | sysfreeze-service-block |
| 56 | different_task_two_captures | 两次抓栈不同任务 | sysfreeze-task-queue |
| 57 | event_runner_idle | EventRunner空闲模式 | - |
| 58 | ipc_work_loop_idle | IPC工作线程空闲模式 | - |
| 59 | sync_task_post_blocking | PostSyncTask阻塞 | - |
| 60 | drawop_async_blocking | DrawOp异步阻塞 | sysfreeze-cond-wait |

### 3. 边界情况测试 (11个)
| ID | 测试名称 | 场景 |
|----|----------|------|
| 28 | missing_symbol_table | 缺少符号表文件 |
| 29 | only_one_stack_capture | 只有一次抓栈（缺少对比） |
| 30 | missing_hilog | 缺少hilog流水日志 |
| 31 | missing_binder_catcher | 缺少BinderCatcher信息 |
| 32 | insufficient_evidence_handling | 证据不足无法确定单一根因 |
| 33 | no_forcing_conclusion | 禁止强行下结论 |
| 34 | stack_unwinding_failure | 解栈失败处理 |
| 35 | blocking_chain_unclosed | 阻塞链无法闭合 |
| 36 | system_resource_priority | 整机与业务问题优先级判断 |
| 61 | memory_info_timestamp_check | 内存信息抓取时间校验 |
| 62 | ld_musl_alias_libc | ld-musl即libc.so识别 |

### 4. 文档使用测试 (6个)
| ID | 测试名称 | 测试文档 | 验证内容 |
|----|----------|----------|----------|
| 37 | blocking_patterns_reference | blocking-patterns.md | mutex阻塞模式识别 |
| 38 | hilog_reference | hilog-refernce.md | 异常日志识别 |
| 39 | ipc_blocking_patterns_reference | blocking-patterns.md | IPC阻塞模式识别 |
| 40 | post_and_wait_patterns_reference | blocking-patterns.md | PostAndWait模式识别 |
| 41 | reference_on_demand_loading | 按需加载 | 不一次性加载所有reference |
| 42 | reference_skip_when_not_needed | 不需要时不加载 | 阻塞链明确时跳过reference |

### 5. 工作流测试 (7个)
| ID | 测试名称 | 验证内容 |
|----|----------|----------|
| 43 | workflow_fault_type_identification | 前置检查：故障类型、时间戳、两次抓栈、符号表 |
| 44 | workflow_task_queue_analysis | 任务队列分析流程 |
| 45 | workflow_blocking_chain_three_questions | 阻塞链三问：类型/源头/闭合 |
| 46 | workflow_thread_state_analysis | 线程状态解读（state/utime/stime） |
| 47 | workflow_time_validation | 两次抓栈时间合理性验证 |
| 48 | workflow_ipc_binder_handling | IPC Binder处理流程 |
| 49 | workflow_report_generation | 报告生成与保存 |

### 6. 禁止做法测试 (5个)
| ID | 测试名称 | 禁止内容 |
|----|----------|----------|
| 50 | forbidden_skip_stack_unwinding | 禁止跳过解栈直接猜测 |
| 51 | forbidden_ignore_system_resources | 禁止忽略整机资源状态 |
| 52 | forbidden_isolate_single_thread | 禁止孤立分析单个线程 |
| 53 | forbidden_force_conclusion | 禁止信息不足时强行结论 |
| 54 | forbidden_ignore_time_info | 禁止忽略时间信息 |

## 测试文件说明

位于 `files/` 目录下，共8个sysfreeze日志场景：

| 目录名 | 描述 | 关键特征 |
|--------|------|----------|
| sysfreeze-service-block | SERVICE_BLOCK互斥锁阻塞 | main线程等mutex in FlushFrame |
| sysfreeze-thread-block | THREAD_BLOCK_6S+vsync超时 | mutex阻塞+vsync日志 |
| sysfreeze-mutex-deadlock | 互斥锁死锁+阻塞链 | 5566→54719→61947→IPC链 |
| sysfreeze-ipc-block | IPC阻塞+BinderCatcher | main→IPC→display_manager mutex |
| sysfreeze-low-memory | 低内存+整机资源 | ReclaimAvailBuffer=5000 |
| sysfreeze-task-queue | 任务队列+IPC阻塞 | VIP/High队列+TransactionData |
| sysfreeze-cond-wait | 条件变量+DrawOp异步 | cond_wait+DDGRTask |
| sysfreeze-post-and-wait | PostAndWait阻塞 | main→RSUniRenderThread mutex |

## 断言类型

| 断言类型 | 说明 |
|----------|------|
| skill_triggered | 验证skill是否正确触发 |
| skill_not_triggered | 验证skill是否正确避免触发 |
| fault_type_identified | 验证是否正确识别故障类型 |
| blocking_pattern_matched | 验证是否匹配阻塞模式 |
| blocking_chain_traced | 验证是否追踪阻塞链 |
| blocking_chain_closed | 验证阻塞链是否闭合 |
| ipc_pattern_detected | 验证是否识别IPC阻塞模式 |
| binder_catcher_used | 验证是否使用BinderCatcher信息 |
| peer_thread_analyzed | 验证是否分析IPC对端线程 |
| task_queue_analyzed | 验证是否分析任务队列 |
| stack_comparison_done | 验证是否对比两次抓栈 |
| hilog_analyzed | 验证是否分析hilog日志 |
| system_resource_checked | 验证是否检查整机资源 |
| resource_issue_prioritized | 验证是否正确判断优先级 |
| root_cause_determined | 验证是否确定根因 |
| fix_suggestion_provided | 验证是否提供修复建议 |
| limited_analysis | 验证是否说明分析受限 |
| report_saved | 验证是否保存报告文件 |
| uses_blocking_patterns_ref | 验证是否使用blocking-patterns.md |
| uses_hilog_ref | 验证是否使用hilog-refernce.md |

## 测试覆盖率

| 类别 | 数量 | 覆盖率 |
|------|------|--------|
| 技能触发 | 19 | 10应触发 + 9不触发 |
| 核心场景 | 14 | 8种阻塞类型全覆盖 + 6种blocking-pattern |
| 边界情况 | 11 | 文件缺失/证据不足/解栈失败/链不闭合 |
| 文档使用 | 6 | 2个reference + 按需加载 + 跳过加载 |
| 工作流 | 7 | 前置检查 + 任务队列 + 阻塞链 + 线程状态 + 时间 + IPC + 报告 |
| 禁止做法 | 5 | 跳过解栈 + 忽略资源 + 孤立线程 + 强行结论 + 忽略时间 |
| **总计** | **62** | **全覆盖** |

## 版本历史

- v1.0 (2026-06-03): 初始版本，包含62个测试用例