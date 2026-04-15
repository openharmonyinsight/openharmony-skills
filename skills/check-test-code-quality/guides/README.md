# Guides 目录说明

本目录包含XTS测试代码质量检查工具的修复指南。

## 修复指南索引

### Critical级别规则

| 规则 | 问题描述 | 修复指南 |
|------|----------|----------|
| R002 | 错误码断言必须是number类型 | [FIX_GUIDE.md](FIX_GUIDE.md#r002问题修复) |
| R008 | 用例声明格式不规范 | [R008_testcase_format/R008_FIX_GUIDE.md](R008_testcase_format/R008_FIX_GUIDE.md) |
| R011 | testsuite重复 | [R011_testsuite_duplicate/R011_FIX_GUIDE.md](R011_testsuite_duplicate/R011_FIX_GUIDE.md) |
| R012 | 签名证书APL等级错误 | [R012_p7b_signature/R012_FIX_GUIDE.md](R012_p7b_signature/R012_FIX_GUIDE.md) |
| R014 | 测试HAP命名不规范 | [R014_hap_naming/R014_HAP_NAMING_GUIDE.md](R014_hap_naming/R014_HAP_NAMING_GUIDE.md) |
| R016 | testcase命名规范 | [R016_testcase_naming/R016_FIX_GUIDE.md](R016_testcase_naming/R016_FIX_GUIDE.md) |
| R018 | testcase重复 | [R018_testcase_duplicate/R018_FIX_GUIDE.md](R018_testcase_duplicate/R018_FIX_GUIDE.md) |

### 补充文档

| 文档 | 说明 |
|------|------|
| [R011_testsuite_duplicate/R011_FIX_ANALYSIS.md](R011_testsuite_duplicate/R011_FIX_ANALYSIS.md) | R011修复分析 |
| [R012_p7b_signature/R012_FIX_SCRIPT_DESIGN.md](R012_p7b_signature/R012_FIX_SCRIPT_DESIGN.md) | R012修复脚本设计 |
| [R012_p7b_signature/R012_ENTERPRISE_SYSTEM_PERMISSION_GUIDE.md](R012_p7b_signature/R012_ENTERPRISE_SYSTEM_PERMISSION_GUIDE.md) | 企业/系统权限处理 |
| [R012_p7b_signature/R012_UNKNOWN_PERMISSION_GUIDE.md](R012_p7b_signature/R012_UNKNOWN_PERMISSION_GUIDE.md) | 未知权限处理 |
| [R018_testcase_duplicate/R018_DYNAMIC_FIX_SUMMARY.md](R018_testcase_duplicate/R018_DYNAMIC_FIX_SUMMARY.md) | R018动态修复总结 |
| [R018_testcase_duplicate/R018_DYNAMIC_TESTCASE_FIX.md](R018_testcase_duplicate/R018_DYNAMIC_TESTCASE_FIX.md) | R018动态修复实现 |

### 工具

| 目录 | 说明 |
|------|------|
| [R012_p7b_signature/signature_tools/](R012_p7b_signature/signature_tools/) | p7b签名工具（hap-sign-tool.jar等） |

## 添加新规则指南

1. 在 `guides/` 下创建 `R{编号}_{描述}/` 目录
2. 创建 `R{编号}_FIX_GUIDE.md` 详细修复指南
3. 更新本文件索引

## 相关文档

- [../SKILL.md](../SKILL.md) - 完整技能说明
- [../rules/](../rules/) - 23个独立规则实现
