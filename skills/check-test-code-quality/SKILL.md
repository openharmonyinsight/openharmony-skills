---
name: check-test-code-quality
description: OpenHarmony XTS测试代码质量检查工具。检查XTS测试代码中的低级问题和编码规范违规，基于兼容性测试代码设计和编码规范2.0和用例低级问题.md。
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Check Test Code Quality (XTS测试代码质量检查)

检查XTS测试代码中的低级问题和编码规范违规，基于"兼容性测试代码设计和编码规范2.0"和"用例低级问题.md"。

## 📚 文档导航

### 📖 核心文档
- **[README.md](README.md)** - 工具概述和快速开始
- **[SKILL.md](SKILL.md)** - 本文档（编排器 - 规则总览与执行流程）
- **[guides/QUICK_START.md](guides/QUICK_START.md)** - 5分钟快速上手

### 📚 详细文档
- **[rules/](rules/)** - 23个独立规则实现（每个规则一个SKILL.md）

### 🛠 指南文档
- **[guides/FIX_GUIDE.md](guides/FIX_GUIDE.md)** - 问题修复指南
- **[guides/R008_testcase_format/](guides/R008_testcase_format/)** - R008规则修复指南
- **[guides/R011_testsuite_duplicate/](guides/R011_testsuite_duplicate/)** - R011规则修复指南
- **[guides/R012_p7b_signature/](guides/R012_p7b_signature/)** - R012规则修复指南
- **[guides/R014_hap_naming/](guides/R014_hap_naming/)** - R014规则修复指南
- **[guides/R016_testcase_naming/](guides/R016_testcase_naming/)** - R016规则修复指南
- **[guides/R018_testcase_duplicate/](guides/R018_testcase_duplicate/)** - R018规则修复指南

### 📋 参考资料
- **[references/](references/)** - 官方规范文档
- **[features/FEATURES.md](features/FEATURES.md)** - 功能增强说明
- **[skill_config.json](skill_config.json)** - 技能配置文件

## 快速开始

### 基本扫描

```bash
/check-test-code-quality /path/to/file_or_directory
```

### 扫描并自动修复

```bash
/check-test-code-quality /path/to/code --rules R002 --fix
```

### 参数说明

- `file_or_directory`: 要检查的文件或目录路径（可指定多个）
- `--rules`: 指定要扫描的规则编号（逗号分隔），如 `--rules R002,R003`
- `--skip-rules`: 跳过指定的规则（逗号分隔），如 `--skip-rules R009,R014`
- `--level`: `critical`（默认）| `warning` | `all`
- `--fix`: 扫描后自动调用修复脚本

## 执行流程

### 架构说明

v4版本将23个规则的扫描实现拆分为独立的规则技能文件（`rules/R001~R023/SKILL.md`），每个文件包含该规则的完整扫描逻辑、检测模式、陷阱警告和修复建议。主SKILL.md作为编排器，负责：

1. **规则调度**: 按参数选择需要执行的规则
2. **文件分发**: 根据各规则要求的文件类型分发文件
3. **结果汇总**: 收集所有规则的扫描结果，生成统一报告
4. **完整性保证**: 确保所有23个规则都被执行，不遗漏

### 扫描执行步骤

```
步骤1: 解析参数 → 确定要执行的规则列表（默认全部23个）
步骤2: 文件收集 → 根据各规则扫描范围收集文件
步骤3: 逐规则扫描 → 对每个规则，加载对应的rules/Rxxx/SKILL.md并执行
步骤4: 结果汇总 → 合并所有规则的结果，生成Excel和Markdown报告
步骤5: 完整性检查 → 确认23个规则全部执行，报告无遗漏
```

### 关键约束：必须逐规则独立执行

**核心原则**: 每个规则的扫描实现是独立的、自包含的。扫描时必须：

1. **逐规则加载**: 对每个规则R001-R023，读取对应的 `rules/Rxxx/SKILL.md`
2. **按规则说明实现**: 严格按照各规则文件中的检测逻辑、正则模式、陷阱警告实现
3. **独立执行**: 每个规则的检测不依赖其他规则的结果
4. **完整输出**: 每个规则都必须输出符合格式要求的结果（即使问题数为0）

### 文件扫描范围汇总

| 规则类别 | 扫描范围 | 相关规则 |
|---------|---------|---------|
| 测试代码规范 | `.test.ets`, `.test.ts`, `.test.js` | R008, R009, R013, R015, R016, R018 |
| 源代码规范 | 所有 `.ets`, `.ts`, `.js` | R001, R002, R003, R004, R005, R006, R019, R020, R022, R023 |
| 配置文件 | `Test.json` | R007 |
| 构建文件 | `BUILD.gn` | R010, R014 |
| 签名文件 | `*.p7b` | R012 |
| 能力配置 | `syscap.json` | R017 |
| 包配置 | `oh-package.json5` | R021 |

## 规则总览

### Critical级别（16个规则）

| 规则 | 名称 | 复杂度 | 扫描范围 | 详细实现 |
|------|------|--------|---------|---------|
| R001 | 禁止使用getSync系统接口 | 简单 | 所有源代码文件 | [rules/R001/SKILL.md](rules/R001/SKILL.md) |
| R002 | 错误码断言必须是number类型 | 简单 | 所有源代码文件 | [rules/R002/SKILL.md](rules/R002/SKILL.md) |
| R003 | 禁止恒真断言 | 简单 | 所有源代码文件 | [rules/R003/SKILL.md](rules/R003/SKILL.md) |
| R004 | 测试用例缺少断言 | **复杂** | 所有源代码文件 | [rules/R004/SKILL.md](rules/R004/SKILL.md) |
| R006 | 禁止基于设备类型差异化 | 简单 | 所有源代码文件 | [rules/R006/SKILL.md](rules/R006/SKILL.md) |
| R007 | Test.json禁止配置项 | 简单 | Test.json | [rules/R007/SKILL.md](rules/R007/SKILL.md) |
| R010 | BUILD.gn配置错误 | **复杂** | BUILD.gn | [rules/R010/SKILL.md](rules/R010/SKILL.md) |
| R011 | testsuite重复 | **复杂** | 测试文件（工程级） | [rules/R011/SKILL.md](rules/R011/SKILL.md) |
| R012 | 签名证书APL等级错误 | 简单 | *.p7b | [rules/R012/SKILL.md](rules/R012/SKILL.md) |
| R014 | 测试HAP命名不规范 | 简单 | BUILD.gn | [rules/R014/SKILL.md](rules/R014/SKILL.md) |
| R017 | syscap.json配置多个能力 | **复杂** | syscap.json | [rules/R017/SKILL.md](rules/R017/SKILL.md) |
| R018 | testcase重复 | **复杂** | 测试文件（文件级） | [rules/R018/SKILL.md](rules/R018/SKILL.md) |
| R019 | .key重复 | **复杂** | 源代码文件（工程级） | [rules/R019/SKILL.md](rules/R019/SKILL.md) |
| R020 | .id重复 | **复杂** | 源代码文件（工程级） | [rules/R020/SKILL.md](rules/R020/SKILL.md) |
| R021 | hypium版本号>=1.0.26 | 简单 | `oh-package.json5` | [rules/R021/SKILL.md](rules/R021/SKILL.md) |
| R022 | errcode值断言使用==而非=== | 简单 | 所有源代码文件 | [rules/R022/SKILL.md](rules/R022/SKILL.md) |
| R023 | 禁止errcode值类型强转后断言 | 简单 | 所有源代码文件 | [rules/R023/SKILL.md](rules/R023/SKILL.md) |

### Warning级别（6个规则）

| 规则 | 名称 | 复杂度 | 扫描范围 | 详细实现 |
|------|------|--------|---------|---------|
| R005 | 组件尺寸使用固定值 | **复杂** | 所有源代码文件 | [rules/R005/SKILL.md](rules/R005/SKILL.md) |
| R008 | 用例声明格式不规范 | **复杂** | 测试文件 | [rules/R008/SKILL.md](rules/R008/SKILL.md) |
| R009 | @tc.number命名不规范 | 简单 | 测试文件 | [rules/R009/SKILL.md](rules/R009/SKILL.md) |
| R013 | 注释的废弃代码 | **复杂** | 测试文件 | [rules/R013/SKILL.md](rules/R013/SKILL.md) |
| R015 | Level参数缺省 | **复杂** | 测试文件 | [rules/R015/SKILL.md](rules/R015/SKILL.md) |
| R016 | testcase命名规范 | **复杂** | 测试文件 | [rules/R016/SKILL.md](rules/R016/SKILL.md) |

## 输出格式

### 问题数据结构

每条issue必须包含以下字段：

```python
{
    'rule': 'R004',
    'type': '测试用例缺少断言',
    'severity': 'Critical',
    'file': 'rel/path.test.ets',
    'line': 25,
    'testcase': 'testName',   # it()的第一个参数，无对应用例时为 '-'
    'snippet': '...',
    'suggestion': '...',
    'subsystem': '元能力',   # 从文件路径匹配 references/subsystem_mapping.md 映射表提取，未匹配到填 '-'
}
```

### 所属用例字段（testcase）

- 所有23个规则的扫描结果都必须包含此字段
- 非测试文件（BUILD.gn、syscap.json、Test.json、p7b等）: `-`
- 测试文件中不在任何`it()`块内: `-`
- 实现方式: 解析文件中所有`it()`块的范围，判断问题行号落在哪个`it()`块内

### 所属子系统字段（subsystem）

- 所有23个规则的扫描结果都必须包含此字段
- **必须**使用 `references/subsystem_mapping.md` 映射表进行匹配，不能简单取文件路径第一级目录
- 匹配规则：取文件相对路径，按最长目录前缀优先匹配映射表中的目录项
- 未匹配到则填 `-`
- 实现方式：
```python
SORTED_DIRS = sorted(SUBSYSTEM_MAPPING.keys(), key=len, reverse=True)
def get_subsystem(file_path: str) -> str:
    file_path = file_path.replace("\\", "/")
    for dir_prefix in SORTED_DIRS:
        if file_path.startswith(dir_prefix + "/"):
            return SUBSYSTEM_MAPPING[dir_prefix]
    return "-"
```

### Excel报告

**表头顺序（必须严格遵循）**:

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
| 9 | 所属子系统 | 从文件路径匹配 `references/subsystem_mapping.md` 映射表自动提取，未匹配到填`-` |
| 10 | 申请报备人 | 手动填写 |
| 11 | 报备原因 | 手动填写 |
| 12 | 是否报备通过 | 手动填写 |

### 报告完整性要求

在生成的报告中，必须显示所有23个规则的统计信息：
- 有问题的规则: 显示实际发现的问题数量
- 无问题的规则: 必须显示为 `0`，不能省略

```
| 规则编号 | 问题类型 | 严重级别 | 问题数量 |
|---------|---------|---------|---------|
| R001 | 禁止使用getSync系统接口 | Critical | 300 |
| R002 | 错误码断言必须是number类型 | Critical | 0 |
...
| R018 | testcase重复 | Critical | 0 |
| R019 | .key重复 | Critical | 0 |
| R020 | .id重复 | Critical | 0 |
| R021 | hypium版本号不满足要求 | Critical | 0 |
| R022 | errcode值断言使用==而非=== | Critical | 0 |
| R023 | 禁止errcode值类型强转后断言 | Critical | 0 |
```

## 规则完整性检查清单

每次执行扫描前，必须确认以下23个规则都已列入执行计划：

- [ ] R001: 禁止使用getSync系统接口 → [rules/R001/SKILL.md](rules/R001/SKILL.md)
- [ ] R002: 错误码断言必须是number类型 → [rules/R002/SKILL.md](rules/R002/SKILL.md)
- [ ] R003: 禁止恒真断言 → [rules/R003/SKILL.md](rules/R003/SKILL.md)
- [ ] R004: 测试用例缺少断言 → [rules/R004/SKILL.md](rules/R004/SKILL.md)
- [ ] R005: 组件尺寸使用固定值 → [rules/R005/SKILL.md](rules/R005/SKILL.md)
- [ ] R006: 禁止基于设备类型差异化 → [rules/R006/SKILL.md](rules/R006/SKILL.md)
- [ ] R007: Test.json禁止配置项 → [rules/R007/SKILL.md](rules/R007/SKILL.md)
- [ ] R008: 用例声明格式不规范 → [rules/R008/SKILL.md](rules/R008/SKILL.md)
- [ ] R009: @tc.number命名不规范 → [rules/R009/SKILL.md](rules/R009/SKILL.md)
- [ ] R010: BUILD.gn配置错误 → [rules/R010/SKILL.md](rules/R010/SKILL.md)
- [ ] R011: testsuite重复 → [rules/R011/SKILL.md](rules/R011/SKILL.md)
- [ ] R012: 签名证书APL等级和app-feature配置错误 → [rules/R012/SKILL.md](rules/R012/SKILL.md)
- [ ] R013: 注释的废弃代码 → [rules/R013/SKILL.md](rules/R013/SKILL.md)
- [ ] R014: 测试HAP命名不规范 → [rules/R014/SKILL.md](rules/R014/SKILL.md)
- [ ] R015: Level参数缺省 → [rules/R015/SKILL.md](rules/R015/SKILL.md)
- [ ] R016: testcase命名规范 → [rules/R016/SKILL.md](rules/R016/SKILL.md)
- [ ] R017: syscap.json配置多个能力 → [rules/R017/SKILL.md](rules/R017/SKILL.md)
- [ ] R018: testcase重复 → [rules/R018/SKILL.md](rules/R018/SKILL.md)
- [ ] R019: .key重复 → [rules/R019/SKILL.md](rules/R019/SKILL.md)
- [ ] R020: .id重复 → [rules/R020/SKILL.md](rules/R020/SKILL.md)
- [ ] R021: hypium版本号>=1.0.26 → [rules/R021/SKILL.md](rules/R021/SKILL.md)
- [ ] R022: errcode值断言使用==而非=== → [rules/R022/SKILL.md](rules/R022/SKILL.md)
- [ ] R023: 禁止errcode值类型强转后断言 → [rules/R023/SKILL.md](rules/R023/SKILL.md)

## 特殊说明

### Warning级别问题

默认只扫描Critical级别问题。如需扫描Warning级别问题，请使用：
```bash
/check-test-code-quality --level warning
/check-test-code-quality --level all
```

### 已知扫描陷阱（跨规则通用）

| 陷阱 | 影响规则 | 严重性 | 说明 |
|------|---------|--------|------|
| 字符串字面量中的大括号干扰 | R004,R015,R016,R018,R019,R020 | 极严重 | 提取it()块时必须跳过字符串中的{和} |
| 反引号模板字符串中的撇号干扰 | R004,R018 | 严重 | 反引号字符串内的`'`和`"`不能作为字符串定界符，状态机必须追踪in_backtick状态 |
| p7b文件是DER二进制格式 | R012 | 极严重 | p7b是DER二进制（非纯JSON），不能用json.loads()直接解析，必须用正则从UTF-8容错解码文本中提取字段 |
| 扫描文件类型错误 | R001,R005,R006 | 严重 | 必须扫描所有源代码文件，不仅测试文件 |
| R001模块名大小写不匹配 | R001 | 严重 | `@ohos.systemParameterEnhance`（大写P）与`@ohos.systemparameter`（小写p）需分别匹配 |
| R001默认导入未识别 | R001 | 严重 | `import parameter from '@ohos.systemparameter'`（无大括号）是default import，需单独处理 |
| R002检测过于宽泛 | R002 | 中等 | 应仅检测error.code的string字面量断言 |
| R003遗漏assertEqual变体 | R003 | 中等 | 必须检测expect(true).assertEqual(true) |
| R006属性访问和日志打印误报 | R006 | 严重 | R006只应检测条件判断（if/switch/三元表达式），纯赋值（`let d = deviceInfo.deviceType`）和日志打印（`console.info(...deviceType)`）不是问题 |
| R016用命名格式检测代替特殊字符检测 | R016 | 极严重 | R016只检查testcase名称是否包含`[a-zA-Z0-9_-]`以外的字符，**不限制命名格式**。严禁使用`^(test\|IT\|it)[A-Z]\w*$`等格式正则，曾导致313条全部误报 |
| R016用@tc.name值作为检测源 | R016 | 极严重 | R016检测对象是`it()`的第一个参数，**不是`@tc.name`的值**。`@tc.name`注解格式多样（冒号分隔、多余空格等），提取其值会引入格式字符导致误报。`@tc.name`仅在修复阶段同步修改 |

详细陷阱说明见各规则的 `rules/Rxxx/SKILL.md` 文件。

## 扫描脚本

### 完整扫描脚本（所有23个规则）
```
/home/xianf/copy/xts_acts/xts_quality_check_v3.py
```

### R004专用扫描脚本（v3通用版本）
```
/home/xianf/copy/xts_acts/scan_r004_v3_generic.py
```

### 使用方法

```bash
# 完整扫描（所有18个规则）
python3 /home/xianf/copy/xts_acts/xts_quality_check_v3.py

# 后台运行（推荐，扫描时间约2小时）
nohup python3 /home/xianf/copy/xts_acts/xts_quality_check_v3.py > scan_v3.log 2>&1 &

# R004规则单独扫描
python3 /home/xianf/copy/xts_acts/scan_r004_v3_generic.py /path/to/target /path/to/output
```

## 扫描文件类型

### 测试文件
- `.test.ets` - ArkTS测试文件
- `.test.ts` - TypeScript测试文件
- `.test.js` - JavaScript测试文件

### 源代码文件
- `.ets` - ArkTS源代码文件
- `.ts` - TypeScript源代码文件
- `.js` - JavaScript源代码文件

### 配置文件
- `Test.json`, `BUILD.gn`, `syscap.json`, `*.p7b`

### 统一文件扫描函数

```python
def get_test_files(directory: str) -> List[str]:
    test_extensions = ['.test.ets', '.test.ts', '.test.js']
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in test_extensions):
                result.append(os.path.join(root, file))
    return result

def get_all_source_files(directory: str) -> List[str]:
    source_extensions = ['.ets', '.ts', '.js']
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in source_extensions):
                result.append(os.path.join(root, file))
    return result
```

### 规则与文件类型对应

| 规则类别 | 扫描范围 | 相关规则 |
|---------|---------|---------|
| 测试代码规范 | `.test.ets`, `.test.ts`, `.test.js` | R008, R009, R013, R015, R016, R018 |
| 源代码规范 | 所有 `.ets`, `.ts`, `.js` | R001, R002, R003, R004, R005, R006, R019, R020, R022, R023 |
| 配置文件 | `Test.json` | R007 |
| 构建文件 | `BUILD.gn` | R010, R014 |
| 签名文件 | `*.p7b` | R012 |
| 能力配置 | `syscap.json` | R017 |
| 包配置 | `oh-package.json5` | R021 |

**重要**: 必须使用 `filename.endswith()` 而不是 `file_path.suffix` 来识别 `.test.ets` 等多后缀文件。

### Static工程说明

Static工程会被正常扫描，应用所有检查规则，与普通工程使用相同的检查标准。

### 历史教训

**R018文件类型遗漏 (2026-03-11)**: 只扫描`.test.ets`和`.test.ts`，遗漏`.test.js`文件导致4个R018问题全部漏检。修复: 在文件过滤中添加`.test.js`。

**R004反引号模板字符串撇号干扰 (2026-04-07)**: 反引号模板字符串中的撇号（如`user's`）被误识别为单引号定界符，导致大括号匹配错误，有断言的用例被误判为缺少断言。修复: 状态机增加`in_backtick`状态追踪，反引号字符串内的`'`和`"`不作为字符串定界符。

**R012 p7b文件DER二进制格式解析失败 (2026-04-07)**: p7b文件是DER（ASN.1）二进制格式，`json.loads()`和`raw.decode('utf-8')`均失败，异常被静默捕获导致R012规则100%漏检（security目录71个p7b文件全部跳过，漏检1个`apl=system_core`问题）。修复: 使用`raw.decode('utf-8', errors='replace')`容错解码后，用正则直接提取`"apl"`、`"app-feature"`等字段，不依赖`json.loads()`。

## 已知扫描陷阱（跨规则通用）

### 陷阱1: it()块提取时字符串字面量中的大括号干扰
- **严重性**: 极严重，曾导致53951个R004误报
- **问题**: 朴素大括号计数会将字符串中的`{}`错误计入
- **修复**: 使用状态机解析，追踪当前是否在字符串字面量内
```python
def count_braces_outside_strings(line):
    in_single = in_double = in_backtick = False
    open_count = close_count = 0
    i = 0
    while i < len(line):
        c = line[i]
        if c == '\\\\' and (in_single or in_double or in_backtick):
            i += 2; continue
        if c == '`' and not in_single and not in_double:
            in_backtick = not in_backtick
        elif c == "'" and not in_double and not in_backtick:
            in_single = not in_single
        elif c == '"' and not in_single and not in_backtick:
            in_double = not in_double
        elif not in_single and not in_double and not in_backtick:
            if c == '{': open_count += 1
            elif c == '}': close_count += 1
        i += 1
    return open_count, close_count
```
- **影响**: R004, R015, R016, R018

### 陷阱1b: 反引号模板字符串中的撇号/引号干扰
- **严重性**: 严重，导致R004误报（有断言的用例被误判为缺少断言）
- **问题**: TypeScript/JavaScript的反引号模板字符串（`` `...` ``）中可能包含撇号（如 `user's`）或引号。如果状态机不追踪反引号状态，会将模板字符串内的`'`误识别为单引号字符串定界符的开启，导致后续代码中的`}`被跳过，大括号匹配错误，it()函数体范围计算错误。
- **触发条件**: it()块内使用反引号模板字符串，且字符串中包含`'`或`"`
- **典型代码**:
```typescript
// 反引号模板字符串中包含撇号 user's
console.info(`getCertificateStorePath Success to get user's path: ${userCACurrentPath}`);
// 上面这行中的 user's 会被没有 backtick 追踪的状态机误判：
//   's path: ${userCACurrentPath}' 被当成一个完整的单引号字符串
//   导致后续的 } catch (err) { ... } 中的 } 被跳过
//   it()函数体范围延伸到下一个it()块，断言检测失效
```
- **修复**: 状态机增加`in_backtick`状态，反引号字符串内的`'`和`"`不作为字符串定界符：
```python
if c == '`' and not in_single and not in_double:
    in_backtick = not in_backtick
elif c == "'" and not in_double and not in_backtick:  # 注意加 in_backtick 条件
    in_single = not in_single
elif c == '"' and not in_single and not in_backtick:   # 注意加 in_backtick 条件
    in_double = not in_double
```
- **影响**: R004, R018（任何依赖大括号匹配提取it()/describe()块范围的规则）

### 陷阱1c: p7b文件是DER二进制格式，json.loads()必失败
- **严重性**: 极严重，导致R012规则100%漏检
- **问题**: p7b签名文件是DER（ASN.1）二进制格式（文件头`0x30 0x82`），不是纯JSON文本。`json.loads()`或`raw.decode('utf-8')`必定失败，如果异常被静默捕获则所有p7b文件全部跳过。
- **修复**: 用`raw.decode('utf-8', errors='replace')`容错解码后，用正则提取`"apl"`、`"app-feature"`等字段，不依赖`json.loads()`。
- **影响**: R012

### 陷阱2: 扫描文件类型错误
- **严重性**: 严重
- **问题**: R001/R005/R006只扫描测试文件，遗漏非测试源代码文件
- **修复**: R001/R005/R006必须使用`get_all_source_files()`
- **影响**: R001 (~81个), R005 (47226个完全漏报), R006

### 陷阱3: R001模块名大小写不匹配
- **严重性**: 严重
- **问题**: `@ohos.systemParameterEnhance`（大写P）与正则 `@ohos.systemparameter`（小写p）不匹配，导致约70个问题漏报
- **修复**: import正则必须同时覆盖 `@ohos.systemparameter` 和 `@ohos.systemParameterEnhance` 两种大小写形式
- **影响**: R001 (~70个, 占总数32%)

### 陷阱4: R001默认导入（default import）未识别
- **严重性**: 严重
- **问题**: `import parameter from '@ohos.systemparameter'`（无大括号）是default import，仅处理named import会漏检约41个问题
- **修复**: 同时处理 `import { xxx } from`（named）和 `import xxx from`（default）两种导入形式
- **影响**: R001 (~41个, 主要集中在usb/bluetooth子系统)

### 陷阱5: R002检测过于宽泛
- **严重性**: 中等，导致3.9倍过度报告
- **修复**: 仅检测`error.code`的string字面量断言，不检测`err.code`（除非确认为别名）

### 陷阱6: R003遗漏assertEqual变体
- **严重性**: 中等，导致~2014个漏报
- **修复**: 必须检测`expect(true).assertEqual(true)`变体

### 陷阱7: R005检测需使用所有源代码文件
- **严重性**: 极严重，导致47226个问题完全漏报（0%检出率）
- **问题**: UI组件的width/height固定值存在于`.ets`页面文件中，不是`.test.ets`文件

### 陷阱8: R016用命名格式检测代替特殊字符检测
- **严重性**: 极严重，导致print子系统313条R016全部误报（0%准确率）
- **问题**: R016规则定义为"testcase名称仅允许`[a-zA-Z0-9_-]`字符"，但`scan_print.py`将其错误实现为"检查名称是否符合`testXxx`或`IT_xxx`格式"，使用正则`^(test|IT|it)[A-Z]\w*$`。例如`printExtension_function_0100`只含合规字符但被误报。
- **根因**: 实现者混淆了"命名格式建议"与"字符集硬性约束"。R016只约束字符集，不约束格式。
- **修复**: 必须使用`^[a-zA-Z0-9_-]+$`做正向字符集匹配，而非格式匹配。
- **验证**: `printExtension_function_0100`、`scan_function_0100`、`testFunc_API_v2-001`均为合规名称，不应触发R016。

### 陷阱9: R016用@tc.name值作为检测源
- **严重性**: 极严重，导致customization子系统R016大量误报
- **问题**: R016的检测对象是`it()`的第一个参数，不是`@tc.name`注解的值。`@tc.name`注解格式多样（`@tc.name: xxx`、`@tc.name    : xxx`等），用正则`@tc\.name\s+(.+)`提取会捕获冒号和空格，导致合规名称被误判。
- **典型误报**: `it("test_set_disallowed_policy_for_account_0700", ...)` 参数合规，但`@tc.name    : test_...`被提取为`: test_...`，冒号触发R016。
- **修复**: R016只检测`it()`的第一个参数。`@tc.name`仅在修复阶段同步修改。

### 陷阱10: 独立XTS工程识别时group类型父BUILD.gn的子工程被错误过滤
- **严重性**: 极严重，导致arkui子系统多层嵌套工程全部漏检（49→997个工程，80→1567个R019问题）
- **问题**: "过滤包含子BUILD.gn的父目录"这一步将所有有父BUILD.gn的子目录排除。但如果父BUILD.gn是`group()`类型（聚合构建），其子目录仍然是独立XTS工程，不应被排除。
- **典型结构**:
```
ace_ets_component_seven/           ← BUILD.gn (group类型)
  ├── ace_ets_component_seven_special/     ← BUILD.gn (独立工程，应扫描) ✗ 被错误排除
  ├── ace_ets_component_common_seven_attrs_align/  ← BUILD.gn (独立工程) ✗ 被错误排除
  └── ... (120+个子工程全部漏检)
```
- **根因**: 过滤`parent_dirs`时未区分group和非group父BUILD.gn。group父目录的BUILD.gn是聚合构建文件，不产生HAP，其子目录中的BUILD.gn才是真正的独立工程。
- **修复**: 只将"父目录是**非group** BUILD.gn"的子目录标记为应排除。group类型的父BUILD.gn不阻止其子目录成为独立工程。
```python
non_group_dirs = {d for d in all_build_gn_dirs if not is_group_build_gn(os.path.join(d, 'BUILD.gn'))}
parent_dirs = set()
for d in all_build_gn_dirs:
    parent = os.path.dirname(d)
    while parent != os.path.abspath(scan_root) and parent != '/':
        if parent in non_group_dirs:  # 只检查非group父目录
            parent_dirs.add(d)
            break
        parent = os.path.dirname(parent)
```
- **影响**: R011, R019, R020（所有工程级检测规则，需识别独立XTS工程边界）

## 已知限制

1. **R004跨文件调用**: 深层嵌套的跨文件函数调用可能无法完全检测
2. **R010配置验证**: 子系统-组件映射表需定期更新
3. **R011独立工程判断**: 只判断目录是否有BUILD.gn文件，可能存在边界情况

## Excel报告格式规范

### CSV/Excel编码规范

**强制要求**: Excel报告必须使用UTF-8 BOM编码，确保中文正常显示。

### 表头规范

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
| 9 | 所属子系统 | 从文件路径匹配 `references/subsystem_mapping.md` 映射表自动提取，未匹配到填`-` |
| 10 | 申请报备人 | 手动填写 |
| 11 | 报备原因 | 手动填写 |
| 12 | 是否报备通过 | 手动填写 |

### 修复建议格式

**R011**: `路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名称}' 中，describe块名称 '{describe名称}' 重复 {重复次数} 次。重复位置: {位置1}, {位置2}, ...`

**R018**: `路径: {文件路径}, 行号: {行号}, 问题描述: 在describe '{describe名称}' 内，testcase名称 '{testcase名称}' 重复 {重复次数} 次。重复行号: {行号1}, {行号2}, ...`

**R019**: `路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名称}' 中，.key值 '{key值}' 重复 {重复次数} 次。重复位置: {位置1}, {位置2}, ...`

**R020**: `路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名称}' 中，.id值 '{id值}' 重复 {重复次数} 次。重复位置: {位置1}, {位置2}, ...`

**R021**: `路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名称}' 中，oh-package.json5的devDependencies.@ohos/hypium版本号为 '{版本}'，低于最低要求版本 1.0.26。`

**R022**: `路径: {文件路径}, 行号: {行号}, 问题描述: errcode值断言使用了宽松相等运算符'=='，应使用严格相等运算符'==='。`

**R023**: `路径: {文件路径}, 行号: {行号}, 问题描述: errcode值断言使用了类型强转'Number()'，应移除强转并给开发提单修复errcode类型问题。`

## 独立XTS工程识别规范

**定义**: 独立XTS工程是指包含BUILD.gn文件且不包含子BUILD.gn的目录。

**识别逻辑**:
1. 找到所有包含BUILD.gn的目录
2. 过滤包含子BUILD.gn的父目录（仅非group类型的父BUILD.gn）
3. 检查是否包含测试文件
4. **重要**: group类型的BUILD.gn不作为独立工程
5. **重要**: group类型的父BUILD.gn不阻止其子目录成为独立工程（见陷阱10）

## 版本历史

### v4.5.0 (2026-04-13) - 新增R023规则
- 新增R023: 禁止errcode值(.code)类型强转后断言，检测`Number(.code)`规避errcode类型问题的行为
- 规则复杂度: simple（正则匹配）
- 扫描范围: 所有源代码文件（`.ets`, `.ts`, `.js`）
- 正则: `\bNumber\s*\([^)]*\.code\s*\)`
- 全仓预估问题数: ~8500+
- 规则总数从22个扩展为23个

### v4.4.0 (2026-04-13) - 新增R022规则
- 新增R022: errcode值(.code)值断言使用"==="非"=="，检测源代码文件中`.code ==`宽松相等断言
- 规则复杂度: simple（正则匹配）
- 扫描范围: 测试文件（`.test.ets`, `.test.ts`, `.test.js`）
- 正则: `\.code\s*==(?!=)`，使用负向前瞻区分`==`和`===`
- 全仓预估问题数: ~8800+
- 规则总数从21个扩展为23个

### v4.3.0 (2026-04-13) - 新增R021规则
- 新增R021: hypium版本号>=1.0.26，检测独立XTS工程oh-package.json5中@ohos/hypium版本号是否满足最低要求
- 规则复杂度: simple（配置文件字段检查）
- 扫描范围: 独立XTS工程根目录下的 `oh-package.json5`
- 使用正则提取版本号（兼容JSON5注释），与标准JSON解析不同
- 规则总数从20个扩展为23个

### v4.2.0 (2026-04-13) - 新增R020规则
- 新增R020: .id重复规则，检测同一独立XTS工程内重复的.id()字符串参数值
- 规则复杂度: complex（工程级检测，需识别独立XTS工程边界）
- 扫描范围: 同一独立XTS工程内的所有源代码文件（`.ets`, `.ts`, `.js`）
- 扫描逻辑与R019一致，仅将`.key`替换为`.id`
- 规则总数从19个扩展为23个

### v4.1.1 (2026-04-13) - 独立XTS工程识别陷阱修复
- 新增陷阱10：group类型父BUILD.gn的子工程被错误过滤，导致R011/R019工程级规则大量漏检
- 独立XTS工程识别规范更新：过滤父目录时仅排除非group类型的父BUILD.gn，group父目录的子工程仍视为独立工程
- R019/SKILL.md新增陷阱#6，含典型目录结构、错误/正确实现代码对比
- arkui子系统扫描工程数从49修正为997，R019问题数从80修正为1567

### v4.1.0 (2026-04-13) - 新增R019规则
- 新增R019: .key重复规则，检测同一独立XTS工程内重复的.key()字符串参数值
- 规则复杂度: complex（工程级检测，需识别独立XTS工程边界）
- 扫描范围: 同一独立XTS工程内的所有源代码文件（`.ets`, `.ts`, `.js`）
- 规则总数从18个扩展为19个

### v4.0.3 (2026-04-07) - 反引号模板字符串陷阱修复
- 新增陷阱1b：反引号模板字符串中的撇号/引号干扰，影响R004/R018
- `count_braces_outside_strings`和所有大括号匹配状态机增加`in_backtick`状态追踪
- R004/SKILL.md新增陷阱#1b说明，含典型代码示例和修复方案
- 新增陷阱1c：p7b文件是DER二进制格式，json.loads()必失败导致R012 100%漏检
- R012/SKILL.md新增DER二进制格式陷阱说明，含正确解析方法和验证方法
- 新增陷阱8：R016用命名格式检测代替特殊字符检测，导致313条全部误报
- R016/SKILL.md新增陷阱#5说明，含错误/正确正则对比和验证用例

### v4.0.2 (2026-04-02) - Excel报告追加报备列
- Excel/CSV报告表头从8列扩展为12列，追加：所属子系统、申请报备人、报备原因、是否报备通过
- 所属子系统从文件路径第一级目录自动提取，其余三列留空供人工填写
- 问题数据结构新增 `subsystem` 字段

### v4.0.1 (2026-04-02) - R001扫描陷阱补充
- R001规则新增3个陷阱：模块名大小写不匹配（漏检~70条）、默认导入未识别（漏检~41条）、多行导入未处理
- 主SKILL.md已知扫描陷阱从5条扩展为7条（新增陷阱3、陷阱4）

### v4.0.0 (2026-04-02) - 规则拆分重构
- 将18个规则的扫描实现拆分到独立的 `rules/R001~R018/SKILL.md` 文件中
- 主SKILL.md改为编排器，负责规则调度、文件分发和结果汇总
- 每个规则文件自包含完整的检测逻辑、正则模式、陷阱警告和修复建议
- docs/目录已移除，规则级内容迁移到对应的rules/Rxxx/SKILL.md
- 解决因规则汇总导致的问题扫描遗漏

### v3.0.0 (2026-03-24) - 完整规则覆盖
- 实现所有18个规则的完整检测（v2仅实现9个）
- 预期问题数量: 520000+

## 相关文档

- **[rules/](rules/)** - 23个独立规则实现（每个规则一个SKILL.md）
- **[guides/FIX_GUIDE.md](guides/FIX_GUIDE.md)** - 问题修复指南
- **[guides/R011_testsuite_duplicate/](guides/R011_testsuite_duplicate/)** - R011修复指南
- **[guides/R012_p7b_signature/](guides/R012_p7b_signature/)** - R012修复指南
- **[guides/R014_hap_naming/](guides/R014_hap_naming/)** - R014修复指南
- **[guides/R016_testcase_naming/](guides/R016_testcase_naming/)** - R016修复指南
- **[guides/R018_testcase_duplicate/](guides/R018_testcase_duplicate/)** - R018修复指南
- **[guides/R008_testcase_format/](guides/R008_testcase_format/)** - R008修复指南
- **[references/兼容性测试代码设计和编码规范2.0.md](references/兼容性测试代码设计和编码规范2.0.md)** - 编码规范参考
- **[references/用例低级问题.md](references/用例低级问题.md)** - 用例低级问题参考
- **[references/subsystem_mapping.md](references/subsystem_mapping.md)** - 目录-子系统映射表（用于报告"所属子系统"列）
