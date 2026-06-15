# ohos-issue-graphics-cppcrash-analysis 测试用例说明

## 概述

本测试套件包含 **23个测试用例**，覆盖cppcrash分析技能的核心分析、禁止做法、边界情况和报告质量。

## 测试分类

### 1. 核心场景测试 (9个)

| ID | 测试名称 | 崩溃类型 | 测试文件 |
|----|----------|----------|----------|
| 1 | uaf_address_pattern_and_root_cause | SIGSEGV + 0x6b6b UAF | cppcrash-uaf |
| 2 | nullptr_null_pointer_dereference | SIGSEGV + fault_addr=0x10 | cppcrash-nullptr |
| 3 | segv_accerr_access_violation | SEGV_ACCERR权限错误 | cppcrash-segv-accerr |
| 4 | sigabort_active_termination | SIGABRT + abort() | cppcrash-sigabort |
| 5 | terminate_bad_cast_with_corruption_evaluation | terminate + std::bad_cast | cppcrash-terminate |
| 6 | cfi_failure_corruption_analysis | cfi_slowpath_comm + 0xdeadbeef | cppcrash-cfi-failure |
| 7 | race_condition_thread_competition | 竞态条件 + DrawableCache | cppcrash-race-condition |
| 8 | highbyte_corruption_address_pattern | 高位字节踩踏 0x59→0x09 | cppcrash-highbyte-corruption |
| 9 | jemalloc_top_memory_stomping | jemalloc_mallctl + 0xdeadbeef | cppcrash-jemalloc-top |

### 2. 禁止做法测试 (4个)

| ID | 测试名称 | 禁止内容 | 测试文件 |
|----|----------|----------|----------|
| 10 | no_guessing_root_cause_without_evidence | 禁止猜测根因/模糊表述 | cppcrash-uaf |
| 11 | no_false_nullptr_on_segv | 禁止SIGSEGV就断定空指针 | cppcrash-uaf |
| 12 | no_skip_address_pattern_matching | 禁止跳过地址模式匹配 | cppcrash-highbyte-corruption |
| 13 | no_ignore_other_threads | 禁止忽略其它线程分析 | cppcrash-race-condition |

### 3. 边界情况测试 (4个)

| ID | 测试名称 | 场景 | 测试文件 |
|----|----------|------|----------|
| 14 | insufficient_evidence_multi_possibility | 证据不足列出多可能根因 | cppcrash-cfi-failure |
| 15 | buildid_mismatch_terminates | buildId不匹配终止分析 | cppcrash-uaf |
| 16 | missing_symbol_table_limits | 缺少符号表文件受限分析 | cppcrash-nullptr |
| 17 | missing_source_code_limits | 缺少源码受限分析 | cppcrash-segv-accerr |

### 4. 报告质量测试 (2个)

| ID | 测试名称 | 验证内容 | 测试文件 |
|----|----------|----------|----------|
| 18 | report_quality_completeness | 报告完整性（元数据/代码行/地址模式/根因/修复建议） | cppcrash-uaf |
| 19 | report_root_cause_rigor | 根因推理严谨性（数据流/地址模式/证据链） | cppcrash-highbyte-corruption |

### 5. 深度分析测试 (4个)

| ID | 测试名称 | 分析维度 | 测试文件 |
|----|----------|----------|----------|
| 20 | disassembly_and_access_address_calculation | 反汇编 + 访问地址计算 + buildId验证 | cppcrash-uaf |
| 21 | call_chain_and_parameter_source | 调用链回溯 + 参数溯源 + 对象生命周期 | cppcrash-race-condition |
| 22 | memory_dump_pattern_analysis | 内存dump布局 + 异常模式识别 + Maps对比 | cppcrash-cfi-failure |
| 23 | code_review_thread_safety | mutex使用 + 锁范围 + 迭代器失效 + shared_ptr生命周期 | cppcrash-race-condition |

## 测试文件说明

位于 `files/` 目录下，共9个cppcrash日志场景：

| 目录名 | 描述 | 关键特征 |
|--------|------|----------|
| cppcrash-uaf | Use-After-Free崩溃 | fault_addr=0x6b6b...，x8/x20含0x6b6b值 |
| cppcrash-nullptr | 空指针崩溃 | fault_addr=0x10，x0=0/x20=0 |
| cppcrash-segv-accerr | SEGV_ACCERR权限错误 | fault_addr在Maps rw-p区域内 |
| cppcrash-sigabort | SIGABRT主动终止 | abort+48栈顶，业务代码触发 |
| cppcrash-terminate | terminate异常终止 | LastFatalMessage: std::bad_cast |
| cppcrash-cfi-failure | CFI失败内存踩踏 | cfi_slowpath_comm + 0xdeadbeef |
| cppcrash-race-condition | 竞态条件崩溃 | RSUniRenderThread访问DrawableCache |
| cppcrash-highbyte-corruption | 高位字节踩踏 | fault_addr 0x09... vs 合法 0x59... |
| cppcrash-jemalloc-top | jemalloc保护终止 | jemalloc_mallctl栈顶 + 0xdeadbeef |

## 断言类型

| 断言类型 | 说明 |
|----------|------|
| uaf_pattern_identified | 验证是否识别0x6b6b UAF模式 |
| null_pointer_pattern_identified | 验证是否识别空指针+偏移模式 |
| accerr_vs_maperr_distinguished | 验证是否区分SEGV_ACCERR与SEGV_MAPERR |
| sigabort_not_segv | 验证是否识别SIGABRT为主动终止 |
| cfi_pattern_recognized | 验证是否识别cfi_slowpath_comm为CFI失败 |
| race_pattern_matched | 验证是否匹配竞态条件模式 |
| highbyte_difference_identified | 验证是否识别高位字节差异 |
| deadbeef_corruption_marker_identified | 验证是否识别0xdeadbeef踩踏标记 |
| no_vague_expression | 验证是否避免模糊表述 |
| no_false_uaf_claim | 验证是否不误判UAF |
| no_forced_single_conclusion | 验证是否不强行下结论 |
| buildid_verified_before_unwinding | 验证是否先验证buildId再解栈 |
| missing_so_detected | 验证是否检测缺少符号表文件 |
| root_cause_determined | 验证是否确定根因 |
| fix_suggestion_in_report | 验证是否提供修复建议 |
| evidence_based_conclusion | 验证是否结论基于证据 |
| crash_instruction_identified | 验证是否通过反汇编识别崩溃指令 |
| access_address_calculated | 验证是否计算实际访问地址 |
| call_layers_analyzed | 验证是否逐层分析调用链 |
| memory_layout_analyzed | 验证是否分析内存布局 |

## 测试覆盖率

| 类别 | 数量 | 覆盖率 |
|------|------|--------|
| 核心场景 | 9 | 9种崩溃类型全覆盖 |
| 禁止做法 | 4 | 禁止猜测/禁止误判/禁止跳过匹配/禁止忽略线程 |
| 边界情况 | 4 | buildId不匹配/缺符号表/缺源码/证据不足 |
| 报告质量 | 2 | 完整性 + 严谨性 |
| 深度分析 | 4 | 反汇编 + 调用链 + 内存dump + 代码review |
| **总计** | **23** | **全覆盖** |

## 版本历史

- v1.0 (2026-06-11): 初始版本，包含23个测试用例