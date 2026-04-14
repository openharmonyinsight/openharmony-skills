# XTS测试代码质量检查工具

> **检查XTS测试代码中的低级问题和编码规范违规**

基于"兼容性测试代码设计和编码规范2.0"和"用例低级问题.md"，提供全面的代码质量检查。

## 主要特性

- **全面扫描** - 扫描所有源代码文件（.ets/.ts/.js）和配置文件
- **23条检查规则** - 涵盖Critical和Warning两个级别
- **工程级检测** - 支持独立XTS工程边界的跨文件检测（R011/R018/R019/R020/R023）
- **Excel报告** - 自动生成UTF-8 BOM编码的详细质量报告（含12列）
- **自动修复** - 支持R002/R008/R012/R016等规则的自动修复

## 检查规则概览

### Critical级别（17条）
| 规则 | 描述 | 扫描范围 | 典型问题 |
|------|------|---------|----------|
| R001 | 禁止使用getSync系统接口 | 所有源代码文件 | `systemParameter.getSync()` |
| R002 | 错误码断言必须是number类型 | 所有源代码文件 | `expect(error.code).assertEqual("401")` |
| R003 | 禁止恒真断言 | 所有源代码文件 | `expect(true).assertTrue()` |
| R004 | 测试用例缺少断言 | 所有源代码文件 | `it()`中完全没有断言 |
| R006 | 禁止基于设备类型差异化 | 所有源代码文件 | `if (deviceType === 'phone')` |
| R007 | Test.json禁止配置项 | Test.json | `setenforce 0`, `rerun:true` |
| R010 | BUILD.gn配置错误 | BUILD.gn | `part_name`不匹配 |
| R011 | testsuite重复 | 测试文件（工程级） | 同一工程内describe命名重复 |
| R012 | 签名证书APL等级错误 | *.p7b | 使用`system_core`等级 |
| R014 | 测试HAP命名不规范 | BUILD.gn | hap_name命名不符合规范 |
| R017 | syscap.json配置多个能力 | syscap.json | 配置多个syscap |
| R018 | testcase重复 | 测试文件（文件级） | 同一describe下testcase命名重复 |
| R019 | .key重复 | 源代码文件（工程级） | 同一工程内.key()值重复 |
| R020 | .id重复 | 源代码文件（工程级） | 同一工程内.id()值重复 |
| R021 | hypium版本号>=1.0.26 | oh-package.json5 | `"@ohos/hypium": "1.0.21"` |
| R022 | errcode值断言使用==而非=== | 所有源代码文件 | `err.code == 401` |
| R023 | 禁止errcode类型强转后断言 | 所有源代码文件 | `Number(err.code) === 401` |

### Warning级别（6条）
| 规则 | 描述 | 扫描范围 | 典型问题 |
|------|------|---------|----------|
| R005 | 组件尺寸使用固定值 | 所有源代码文件 | `width: 100px` |
| R008 | 用例声明格式不规范 | 测试文件 | `@tc.level:` 冒号分隔符 |
| R009 | @tc.number命名不规范 | 测试文件 | 不符合命名格式 |
| R013 | 注释的废弃代码 | 测试文件 | 存在大量注释的废弃代码 |
| R015 | Level参数缺省 | 测试文件 | `it()`缺少Level参数 |
| R016 | testcase命名规范 | 测试文件 | 名称包含特殊字符 |

## 快速开始

### 基本使用
```bash
# 检查当前目录
/check-test-code-quality

# 检查指定目录
/check-test-code-quality /path/to/code

# 检查多个目录
/check-test-code-quality dir1/ dir2/ dir3/
```

### 高级选项
```bash
# 只扫描特定规则
/check-test-code-quality /path/to/code --rules R001,R002,R003

# 跳过某些规则
/check-test-code-quality /path/to/code --skip-rules R009,R014

# 指定级别（默认all）
/check-test-code-quality /path/to/code --level all
/check-test-code-quality /path/to/code --level critical
/check-test-code-quality /path/to/code --level warning

# 扫描并自动修复
/check-test-code-quality /path/to/code --rules R002 --fix
```

## 文档导航

### 核心文档
- **[SKILL.md](SKILL.md)** - 完整的技能说明、参数文档和执行流程
- **[guides/QUICK_START.md](guides/QUICK_START.md)** - 5分钟快速上手

### 规则文档
- **[rules/](rules/)** - 23个独立规则实现（每个规则一个SKILL.md，含检测逻辑、正则模式、陷阱警告）

### 指南文档
- **[guides/FIX_GUIDE.md](guides/FIX_GUIDE.md)** - 问题修复指南总览
- **[guides/R008_testcase_format/](guides/R008_testcase_format/)** - R008用例声明格式修复指南
- **[guides/R011_testsuite_duplicate/](guides/R011_testsuite_duplicate/)** - R011 testsuite重复修复指南
- **[guides/R012_p7b_signature/](guides/R012_p7b_signature/)** - R012签名证书修复指南
- **[guides/R014_hap_naming/](guides/R014_hap_naming/)** - R014 HAP命名修复指南
- **[guides/R016_testcase_naming/](guides/R016_testcase_naming/)** - R016 testcase命名修复指南
- **[guides/R018_testcase_duplicate/](guides/R018_testcase_duplicate/)** - R018 testcase重复修复指南

### 参考资料
- **[references/兼容性测试代码设计和编码规范2.0.md](references/兼容性测试代码设计和编码规范2.0.md)** - 编码规范参考
- **[references/用例低级问题.md](references/用例低级问题.md)** - 用例低级问题参考
- **[references/subsystem_mapping.md](references/subsystem_mapping.md)** - 目录-子系统映射表

## 扫描范围

### 支持的文件类型

| 文件类型 | 扩展名 | 相关规则 |
|---------|--------|---------|
| 测试文件 | `.test.ets`, `.test.ts`, `.test.js` | R002, R003, R004, R008, R009, R013, R015, R016, R018, R022, R023 |
| 源代码文件 | `.ets`, `.ts`, `.js` | R001, R002, R003, R004, R005, R006, R019, R020, R022, R023 |
| 配置文件 | `Test.json`, `BUILD.gn`, `syscap.json`, `*.p7b`, `oh-package.json5` | R007, R010, R012, R014, R017, R021 |

**重要**: 必须使用 `filename.endswith()` 而不是 `file_path.suffix` 来识别 `.test.ets` 等多后缀文件。

### 工程级检测规则

以下规则需要识别独立XTS工程边界，在工程内进行跨文件检测：

| 规则 | 检测对象 | 边界说明 |
|------|---------|---------|
| R011 | describe()块名称 | 同一独立XTS工程内 |
| R018 | it()第一个参数 | 同一文件内的同一describe内 |
| R019 | .key()字符串参数 | 同一独立XTS工程内所有源代码文件 |
| R020 | .id()字符串参数 | 同一独立XTS工程内所有源代码文件 |
| R023 | Number(.code)调用 | 同一独立XTS工程内所有源代码文件 |

独立XTS工程识别逻辑：包含BUILD.gn文件且不包含子BUILD.gn的目录（group类型的BUILD.gn不作为独立工程，但其子目录仍视为独立工程）。

## 输出报告

### Excel/CSV报告格式

报告使用UTF-8 BOM编码，12列：

| 列序 | 列名 | 说明 |
|------|------|------|
| 1 | 问题ID | R001-R023 |
| 2 | 问题类型 | 问题描述 |
| 3 | 严重级别 | Critical/Warning |
| 4 | 文件路径 | 相对路径 |
| 5 | 行号 | 问题所在行号 |
| 6 | 所属用例 | it()的第一个参数或`-` |
| 7 | 代码片段 | 问题代码片段 |
| 8 | 修复建议 | 路径+行号+问题描述 |
| 9 | 所属子系统 | 从subsystem_mapping.md自动提取 |
| 10-12 | 报备信息 | 手动填写 |

## 已知扫描陷阱

| 陷阱 | 影响规则 | 严重性 | 说明 |
|------|---------|--------|------|
| 字符串字面量中的大括号干扰 | R004,R015,R016,R018,R019,R020 | 极严重 | it()块提取时必须跳过字符串中的{和} |
| 反引号模板字符串中的撇号干扰 | R004,R018 | 严重 | 状态机必须追踪in_backtick状态 |
| p7b文件是DER二进制格式 | R012 | 极严重 | 不能用json.loads()，必须用正则提取 |
| 扫描文件类型错误 | R001,R005,R006 | 严重 | 必须扫描所有源代码文件，不仅测试文件 |
| group父BUILD.gn的子工程被错误过滤 | R011,R019,R020 | 极严重 | group父目录不阻止子工程成为独立工程 |
| R016用命名格式检测代替特殊字符检测 | R016 | 极严重 | 只检查`[a-zA-Z0-9_-]`字符集，不限制命名格式 |

详细陷阱说明见各规则的 `rules/Rxxx/SKILL.md` 文件。

## 版本历史

### v4.5.0 (2026-04-13)
- 新增R023: 禁止errcode值类型强转后断言（`Number(.code)`）
- 新增R022: errcode值断言必须使用`===`非`==`
- 新增R021: hypium版本号>=1.0.26
- 新增R020: .id重复（与R019逻辑一致）
- R002/R003/R004/R022扫描范围扩展为所有源代码文件
- 规则总数: 23个（17 Critical + 6 Warning）

### v4.1.0 (2026-04-13)
- 新增R019: .key重复（工程级跨文件检测）
- 修复独立XTS工程识别：group类型父BUILD.gn的子工程不再被错误过滤

---

**版本**: v4.5.0
**最后更新**: 2026-04-13
