# new-delete-checker 测试用例说明

## 概述

本测试套件包含 **38个测试用例**，覆盖new-delete-checker技能的核心功能。

## 测试分类

### 1. 技能触发测试 (16个)
**目的**: 验证skill的description是否能正确触发

#### 应该触发 (8个)
- ID 1-8: 测试各种内存管理相关查询是否正确触发skill

| ID | 测试名称 | 触发词 |
|----|----------|--------|
| 1 | trigger_memory_leak_check | "内存泄漏检查" |
| 2 | trigger_new_delete_pairing | "new/delete配对" |
| 3 | trigger_memory_safety_verification | "内存安全验证" |
| 4 | trigger_refptr_analysis | "RefPtr使用模式" |
| 5 | trigger_ace_engine_analysis | "ace_engine内存管理" |
| 6 | trigger_cross_layer_check | "跨层内存管理" |
| 7 | trigger_register_unregister_leak | "Register/Unregister泄漏" |
| 8 | trigger_callback_memory | "回调函数内存管理" |

#### 不应触发 (8个)
- ID 9-16: 测试无关任务是否正确避免触发skill

| ID | 测试名称 | 场景 |
|----|----------|------|
| 9 | negative_trigger_fibonacci | 斐波那契函数 |
| 10 | negative_trigger_pdf | PDF文件读取 |
| 11 | negative_trigger_ui | Web界面开发 |
| 12 | negative_trigger_database | SQL查询优化 |
| 13 | negative_trigger_git | Git提交格式 |
| 14 | negative_trigger_formatting | 代码格式化 |
| 15 | negative_trigger_unit_test | 单元测试生成 |
| 16 | negative_trigger_api_docs | API文档编写 |

### 2. 核心场景测试 (17个)
**目的**: 验证17个核心场景的检测能力

| ID | 测试名称 | 场景 | 测试文件 |
|----|----------|------|----------|
| 17 | scenario_basic_pairing | 基础配对 | basic_leak.cpp |
| 18 | scenario_array_mismatch | 数组不匹配 | new_delete_mismatch.cpp |
| 19 | scenario_smart_pointer_usage | 智能指针 | smart_ptr_issue.cpp |
| 20 | scenario_exception_safety | 异常安全 | exception_leak.cpp |
| 21 | scenario_ownership_transfer | 所有权转移 | ownership_transfer.cpp |
| 22 | scenario_container_cleanup | 容器清理 | container_leak.cpp |
| 23 | scenario_register_unregister | 注册注销 | register_unregister.cpp |
| 24 | scenario_singleton_pattern | 单例模式 | - |
| 25 | scenario_callbacks | 回调函数 | - |
| 26 | scenario_multi_threading | 多线程 | - |
| 27 | scenario_cross_layer | 跨层交互 | - |
| 28 | scenario_third_party | 第三方库 | - |
| 29 | scenario_special_patterns | 特殊模式 | - |
| 30 | scenario_common_leaks | 常见泄漏 | - |
| 31 | scenario_nullptr_handling | nullptr处理 | - |
| 32 | scenario_lifecycle_binding | 生命周期绑定 | - |
| 33 | scenario_assignment_updates | 赋值更新 | - |
| 34 | scenario_function_returns | 函数返回 | - |

### 3. 文档使用测试 (4个)
**目的**: 验证Claude能否正确使用references文档

| ID | 测试名称 | 测试文档 | 验证内容 |
|----|----------|----------|----------|
| 35 | doc_statistics_usage | STATISTICS.md | 运行和解读统计 |
| 36 | doc_patterns_usage | PATTERNS.md | 应用检测规则 |
| 37 | doc_fixes_usage | FIXES.md | 提供修复建议 |
| 38 | doc_template_usage | REPORT_TEMPLATE.md | 生成报告结构 |

## 测试文件说明

### 测试代码文件 (7个)
位于 `assets/test_cases/` 目录：

| 文件名 | 描述 | 包含问题 |
|--------|------|----------|
| basic_leak.cpp | 基础内存泄漏 | 提前返回路径泄漏 |
| new_delete_mismatch.cpp | 数组分配不匹配 | new[]使用delete |
| smart_ptr_issue.cpp | 智能指针问题 | Raw/RefPtr混用，循环引用 |
| exception_leak.cpp | 异常安全问题 | 异常路径泄漏 |
| ownership_transfer.cpp | 所有权转移问题 | 不明确的所有权 |
| container_leak.cpp | 容器指针泄漏 | 缺少析构函数清理 |
| register_unregister.cpp | 注册注销问题 | 异常不安全，重复注册 |

**注意**: 这些文件包含LSP错误是正常的，因为它们是测试用例片段，不是完整可编译的程序。

## 断言类型

每个测试用例包含多个断言，验证以下方面：

| 断言类型 | 说明 |
|----------|------|
| skill_triggered | 验证skill是否正确触发 |
| skill_not_triggered | 验证skill是否正确避免触发 |
| issue_detected | 验证是否检测到问题 |
| severity_correct | 验证严重级别是否正确 |
| location_accurate | 验证问题位置是否准确 |
| fix_provided | 验证是否提供修复方案 |
| fix_recommended | 验证是否推荐修复方案 |
| scenario_covered | 验证场景是否被覆盖 |
| uses_*_md | 验证是否使用特定参考文档 |
| report_structure_complete | 验证报告结构是否完整 |

## 运行测试

### 手动验证

1. **触发测试**
```bash
# 测试应该触发的场景
# 在Claude Code中输入触发词，观察skill是否被调用

# 测试不应触发的场景
# 在Claude Code中输入无关任务，观察skill是否被正确避免
```

2. **场景测试**
```bash
# 在Claude Code中使用skill分析测试文件
# 验证是否正确检测到问题并提供修复建议
```

3. **文档使用测试**
```bash
# 运行统计脚本
bash scripts/stats.sh assets/test_cases/

# 验证Claude是否能正确解读结果并使用参考文档
```

### 自动化测试

使用skill-creator框架运行评估：

```bash
# 准备测试环境
mkdir -p new-delete-checker-workspace/iteration-1

# 运行测试（需要skill-creator支持）
# 参考skill-creator文档运行完整的评估流程
```

## 测试覆盖率

### 当前阶段：Phase 1 - 核心功能 (38个测试用例)

| 类别 | 数量 | 覆盖率 |
|------|------|--------|
| 技能触发 | 16 | 100% (应触发8个，不触发8个) |
| 核心场景 | 18 | 100% (17个场景+1个组合) |
| 文档使用 | 4 | 100% (4个参考文档) |
| **总计** | **38** | **100%** |

### 后续阶段规划

| 阶段 | 描述 | 测试用例数 | 预期评分提升 |
|------|------|-----------|-------------|
| Phase 1 ✅ | 核心功能 | 38 | 78 → 85 |
| Phase 2 | 深度测试 | +42 | 85 → 90 |
| Phase 3 | 全面验证 | +27 | 90 → 95 |

## 预期结果

### 通过标准

- **触发测试**: 16/16 通过 (100%)
- **场景测试**: 至少 15/18 通过 (83%+)
- **文档测试**: 4/4 通过 (100%)
- **总体**: 至少 35/38 通过 (92%+)

### 失败处理

如果测试失败，需要：

1. **触发测试失败**
   - 检查SKILL.md的description是否准确
   - 考虑调整触发关键词
   - 使用skill-creator的description优化功能

2. **场景测试失败**
   - 检查SKILL.md是否包含该场景的指导
   - 检查references文档是否有对应的检测规则
   - 添加或完善检测模式

3. **文档测试失败**
   - 验证references文档是否完整
   - 检查文档链接是否正确
   - 确保文档路径正确

## 测试数据

- **总文件数**: 8 (1个evals.json + 7个测试代码文件)
- **总代码行数**: 1109行
- **JSON测试用例**: 38个
- **断言总数**: 80+个

## 版本历史

- v1.0 (2026-03-05): 初始版本，包含38个核心测试用例

## 相关文档

- [SKILL.md](../SKILL.md) - Skill主文档
- [references/PATTERNS.md](../references/PATTERNS.md) - 模式检测规则
- [references/FIXES.md](../references/FIXES.md) - 修复建议
- [references/STATISTICS.md](../references/STATISTICS.md) - 统计指南
- [references/REPORT_TEMPLATE.md](../references/REPORT_TEMPLATE.md) - 报告模板
