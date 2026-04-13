# Guides 目录说明

本目录包含XTS测试代码质量检查工具的修复指南和技术文档。

## 目录结构

```
guides/
├── README.md                          # 本说明文档
├── FIX_GUIDE.md                       # 通用修复指南
├── QUICK_START.md                     # 快速开始指南
│
├── R011_testsuite_duplicate/          # R011 testsuite重复修复指南
│   └── R011_FIX_GUIDE.md              # 详细修复步骤
│
├── R012_p7b_signature/                # R012 签名问题修复指南
│   ├── R012_FIX_GUIDE.md              # 主修复指南
│   ├── R012_ENTERPRISE_SYSTEM_PERMISSION_GUIDE.md  # 企业/系统权限指南
│   ├── R012_UNKNOWN_PERMISSION_GUIDE.md            # 未知权限指南
│   └── R012_FIX_SCRIPT_DESIGN.md                   # 脚本设计文档
│
├── R014_hap_naming/                   # R014 HAP命名修复指南
│   └── R014_HAP_NAMING_GUIDE.md       # 详细修复步骤
│
├── R018_testcase_duplicate/           # R018 testcase重复修复指南
│   ├── R018_FIX_GUIDE.md              # 详细修复步骤
│   ├── R018_DYNAMIC_FIX_SUMMARY.md    # 动态修复总结
│   └── R018_DYNAMIC_TESTCASE_FIX.md   # 动态修复实现
│
└── signature_tools/                   # 签名工具
```

## 修复指南索引

### Critical级别规则

| 规则 | 问题描述 | 修复指南 | 快速修复 |
|------|----------|----------|----------|
| R011 | testsuite重复 | [R011_FIX_GUIDE.md](R011_testsuite_duplicate/R011_FIX_GUIDE.md) | 在重复名称后追加`Adapt`+三位数字 |
| R012 | 签名证书APL等级错误 | [R012_FIX_GUIDE.md](R012_p7b_signature/R012_FIX_GUIDE.md) | `system_core` → `normal`，保留acls字段 |
| R014 | 测试HAP命名不规范 | [R014_HAP_NAMING_GUIDE.md](R014_hap_naming/R014_HAP_NAMING_GUIDE.md) | 以`Acts`开头，以`Test`结尾 |
| R018 | testcase重复 | [R018_FIX_GUIDE.md](R018_testcase_duplicate/R018_FIX_GUIDE.md) | 在重复名称后追加`Adapt`+三位数字 |

### R011: testsuite重复

**问题描述**: 一个独立XTS工程下不允许describe命名重复

**快速修复**:
```
原名称: XxxTest
修复后: XxxTestAdapt001
```

**修复规则**:
1. 在重复的testsuite名称后追加`Adapt`+三位数字
2. 数字从001开始递增
3. 保留第一个出现的名称不变

### R012: 签名证书APL等级和app-feature配置错误

**问题描述**: 签名证书p7b文件中使用了`system_core`等级或`app-feature`字段配置错误

**文档列表**:
- **[R012_FIX_GUIDE.md](R012_p7b_signature/R012_FIX_GUIDE.md)** - 主修复指南
- **[R012_ENTERPRISE_SYSTEM_PERMISSION_GUIDE.md](R012_p7b_signature/R012_ENTERPRISE_SYSTEM_PERMISSION_GUIDE.md)** - 企业/系统应用权限处理
- **[R012_UNKNOWN_PERMISSION_GUIDE.md](R012_p7b_signature/R012_UNKNOWN_PERMISSION_GUIDE.md)** - 未知权限处理
- **[R012_FIX_SCRIPT_DESIGN.md](R012_p7b_signature/R012_FIX_SCRIPT_DESIGN.md)** - 修复脚本设计文档

**核心要点**:
1. **acls字段必须保留**: 修复时必须保留原p7b文件中的`acls`字段
2. apl: `system_core` → `normal`
3. app-feature: `hos_system_app` → `hos_normal_app`

### R014: 测试HAP命名不规范

**问题描述**: 测试HAP命名不符合规范要求，hap包命名采用大驼峰方式

**命名规范**:

| 工程类型 | 模板名称 | 命名规范 |
|---------|---------|---------|
| JS/TS工程 | `ohos_js_app_suite` | 以`Acts`开头（A大写），以`Test`结尾（T大写） |
| JS/TS工程 | `ohos_js_app_static_suite` | 以`Acts`开头（A大写），以`StaticTest`结尾（S、T大写） |
| C++工程 | `ohos_moduletest_suite` | 模板名称以`Acts`开头（A大写），以`Test`结尾（T大写） |

**快速修复**:

| 错误类型 | 修复方法 | 示例 |
|---------|---------|------|
| 不以Acts开头 | 在名称前添加`Acts`前缀 | `MyTest` → `ActsMyTest` |
| ohos_js_app_suite不以Test结尾 | 添加`Adapt001Test`后缀 | `ActsMyHap` → `ActsMyHapAdapt001Test` |
| ohos_js_app_static_suite不以StaticTest结尾 | 添加`Adapt001StaticTest`后缀 | `ActsMyHap` → `ActsMyHapAdapt001StaticTest` |

### R018: testcase重复

**问题描述**: 一个describe下不允许testcase（@tc.name)重复

**文档列表**:
- **[R018_FIX_GUIDE.md](R018_testcase_duplicate/R018_FIX_GUIDE.md)** - 详细修复步骤
- **[R018_DYNAMIC_FIX_SUMMARY.md](R018_testcase_duplicate/R018_DYNAMIC_FIX_SUMMARY.md)** - 动态修复总结
- **[R018_DYNAMIC_TESTCASE_FIX.md](R018_testcase_duplicate/R018_DYNAMIC_TESTCASE_FIX.md)** - 动态修复实现

**快速修复**:
```
原名称: SUB_XXX_test_001
修复后: SUB_XXX_test_001_Adapt001
```

**修复规则**:
1. 在重复的testcase名称后追加`_Adapt`+三位数字
2. 数字从001开始递增
3. 保留第一个出现的名称不变

## 添加新规则指南

当需要为新规则添加修复指南时：

1. 在 `guides/` 下创建 `R{编号}_{描述}/` 目录
2. 创建 `R{编号}_FIX_GUIDE.md` 详细修复指南
3. 更新本文件的索引

### 命名规范

- **目录**: `R{编号}_{描述}` (如 `R011_testsuite_duplicate/`)
- **文档**: `R{编号}_{类型}` (如 `R011_FIX_GUIDE.md`)

## 相关文档

- [../SKILL.md](../SKILL.md) - 完整技能说明
- [../rules/](../rules/) - 18个独立规则实现（含示例和技术规范）
