# ohos-issue-graphics-cppcrash-analysis 测试用例说明

## 概述

本测试套件包含 **46个测试用例**，覆盖cppcrash分析技能的核心功能、边界情况和文档使用。

## 测试分类

### 1. 技能触发测试 (16个)

#### 应该触发 (8个)
| ID | 测试名称 | 触发词 |
|----|----------|--------|
| 1 | trigger_cppcrash_analysis | "分析cppcrash日志" |
| 2 | trigger_native_crash | "定位native崩溃原因" |
| 3 | trigger_sigsegv_analysis | "SIGSEGV图形模块崩溃" |
| 4 | trigger_uaf_keyword | "Use-After-Free崩溃" |
| 5 | trigger_wild_pointer | "野指针特征" |
| 6 | trigger_memory_stomp | "内存踩踏" |
| 7 | trigger_0x6b6b_address | "0x6b6b地址" |
| 8 | trigger_render_service_crash | "render_service崩溃" |

#### 不应触发 (8个)
| ID | 测试名称 | 场景 |
|----|----------|------|
| 9 | negative_trigger_arkts_crash | ArkTS/JS层崩溃 |
| 10 | negative_trigger_ui_development | UI界面开发 |
| 11 | negative_trigger_perf_optimization | 性能优化 |
| 12 | negative_trigger_code_review | 代码review |
| 13 | negative_trigger_build_error | 编译错误 |
| 14 | negative_trigger_git_merge | Git合并冲突 |
| 15 | negative_trigger_no_cppcrash_file | 无cppcrash日志 |
| 16 | negative_trigger_unit_test | 单元测试 |

### 2. 核心场景测试 (9个)
| ID | 测试名称 | 崩溃类型 | 测试文件 |
|----|----------|----------|----------|
| 17 | nullptr_analysis_full | SIGSEGV空指针 | cppcrash-nullptr |
| 18 | uaf_analysis_full | SIGSEGV+0x6b6b (UAF) | cppcrash-uaf |
| 19 | sigabort_analysis | SIGABRT+abort | cppcrash-sigabort |
| 20 | highbyte_corruption_analysis | SIGSEGV高位踩踏 | cppcrash-highbyte-corruption |
| 21 | cfi_failure_analysis | cfi_slowpath_comm | cppcrash-cfi-failure |
| 22 | terminate_exception_analysis | SIGABRT+terminate+异常 | cppcrash-terminate |
| 23 | race_condition_analysis | 多线程竞态+空指针 | cppcrash-race-condition |
| 24 | segv_accerr_analysis | SEGV_ACCERR权限 | cppcrash-segv-accerr |
| 25 | jemalloc_top_analysis | jemalloc栈顶 | cppcrash-jemalloc-top |

### 3. 边界情况测试 (5个)
| ID | 测试名称 | 场景 |
|----|----------|------|
| 26 | buildid_mismatch_rejection | buildId不匹配 |
| 27 | missing_so_file | 缺少符号表文件 |
| 28 | missing_code_directory | 缺少源码目录 |
| 29 | insufficient_evidence_handling | 证据不足无法确定单一根因 |
| 30 | no_guessing_root_cause | 禁止猜测根因 |

### 4. 文档使用测试 (9个)
| ID | 测试名称 | 测试文档 | 验证内容 |
|----|----------|----------|----------|
| 31 | report_template_usage | report-template.md | 报告结构与完整性 |
| 32 | stack_unwinding_reference | stack-unwinding.md | 解栈流程 |
| 33 | disassembly_reference | disassembly-analysis.md | 反汇编分析 |
| 34 | memory_pattern_reference | memory-pattern-analysis.md | 数据流追踪与地址匹配 |
| 35 | thread_competition_reference | thread-competition-analysis.md | 多线程竞争分析 |
| 36 | memory_data_reference | memory-data-analysis.md | 内存dump分析 |
| 37 | call_chain_backtrace_reference | call-chain-backtrace.md | 调用链回溯 |
| 38 | code_review_checklist_reference | code-review-checklist.md | 代码排查要点 |
| 39 | reference_on_demand_loading | 按需加载 | 不一次性加载所有reference |

### 5. 工作流测试 (4个)
| ID | 测试名称 | 验证内容 |
|----|----------|----------|
| 40 | workflow_path_selection | SIGSEGV+0x6b6b → UAF路径 |
| 41 | workflow_sigabort_path | SIGABRT → 业务代码分析路径 |
| 42 | workflow_cfi_path | CFI → 踩内存分析路径 |
| 43 | precheck_crash_type | 前置检查：崩溃类型、地址、多线程 |
| 44 | precheck_input_integrity | 前置检查：输入完整性顺序 |

### 6. 禁止做法测试 (2个)
| ID | 测试名称 | 禁止内容 |
|----|----------|----------|
| 45 | forbidden_skip_multithread | 禁止忽略多线程分析 |
| 46 | forbidden_skip_address_pattern | 禁止跳过地址模式匹配 |

## 测试文件说明

位于 `files/` 目录下，共8个cppcrash日志场景：

| 目录名 | 描述 | 关键特征 |
|--------|------|----------|
| cppcrash-nullptr | 空指针崩溃 | fault_addr=0x10, x0=0 |
| cppcrash-uaf | Use-After-Free | fault_addr=0x6b6b..., 内存dump 6b6b填充 |
| cppcrash-sigabort | abort终止 | SIGABRT, 栈顶abort() |
| cppcrash-highbyte-corruption | 高位字节踩踏 | 0x59→0x09高位差异 |
| cppcrash-cfi-failure | CFI失败 | cfi_slowpath_comm, 0xdeadbeef |
| cppcrash-terminate | 异常terminate | std::bad_cast, terminate |
| cppcrash-race-condition | 多线程竞态 | 其它线程访问相同DrawableCache |
| cppcrash-segv-accerr | 权限错误 | SEGV_ACCERR而非MAPERR |
| cppcrash-jemalloc-top | jemalloc栈顶 | jemalloc_mallctl, 0xdeadbeef |

## 断言类型

| 断言类型 | 说明 |
|----------|------|
| skill_triggered | 验证skill是否正确触发 |
| skill_not_triggered | 验证skill是否正确避免触发 |
| crash_type_identified | 验证是否正确识别崩溃类型 |
| address_pattern_matched | 验证是否进行地址模式匹配 |
| data_flow_traced | 验证是否追溯数据流 |
| uaf_pattern_detected | 验证是否识别UAF模式 |
| memory_pattern_analyzed | 验证是否分析内存模式 |
| other_thread_analyzed | 验证是否分析其它线程 |
| race_condition_detected | 验证是否检测竞态条件 |
| cfi_pattern_detected | 验证是否识别CFI模式 |
| special_case_handled | 验证是否正确处理特殊情况 |
| fix_suggestion_provided | 验证是否提供修复建议 |
| buildid_verified | 验证是否检查buildId |
| analysis_terminated | 验证是否在条件不满足时终止 |
| no_vague_expression | 验证是否避免模糊表述 |
| uses_*_ref | 验证是否使用特定参考文档 |
| correct_path_selected | 验证是否选择正确分析路径 |

## 测试覆盖率

| 类别 | 数量 | 覆盖率 |
|------|------|--------|
| 技能触发 | 16 | 8应触发 + 8不触发 |
| 核心场景 | 9 | 9种崩溃类型全覆盖 |
| 边界情况 | 5 | buildId/文件缺失/证据不足/禁止猜测 |
| 文档使用 | 9 | 8个reference + 按需加载 |
| 工作流 | 4 | 路径选择 + 前置检查 |
| 禁止做法 | 2 | 多线程 + 地址匹配 |
| **总计** | **46** | **全覆盖** |

## 版本历史

- v1.0 (2026-06-03): 初始版本，包含46个测试用例