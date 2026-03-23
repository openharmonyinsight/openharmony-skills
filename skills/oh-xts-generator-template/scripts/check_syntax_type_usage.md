# API 语法类型检查脚本使用指南

## 概述

`check_syntax_type.js` 是一个自动化检查脚本，用于在编译前验证测试用例使用的 API 是否支持目标语法类型（ArkTS-static 或 ArkTS-dynamic）。

## 快速开始

### 1. 基本用法

```bash
# 检查单个测试文件
node check_syntax_type.js --syntax-type static --test-cases UitestOnTextErrorStatic.test.ets

# 检查目录中的所有测试文件
node check_syntax_type.js --syntax-type static --test-dir ./test/

# 指定 API 信息文件
node check_syntax_type.js --syntax-type static --test-cases *.test.ets --api-info ./api_info.json

# 生成详细报告
node check_syntax_type.js --syntax-type static --test-dir ./test/ --verbose
```

### 2. ArkTS-static 语法检查

```bash
# 检查静态语法测试用例
cd /mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode_static/entry/src/main/src/test/

node /mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
  --syntax-type static \
  --test-dir ./
```

**预期输出**:
```
API 语法类型检查脚本
语法类型: static
API 信息文件: /tmp/api_info_and_style_with_syntax.json

检查 24 个测试文件...
找到 24 个测试文件

验证 API 语法类型...

=== 检查摘要 ===
语法类型: static
检查的测试文件: 24 个
使用的 API 数量: 89
有效的 API 数量: 89
无效的 API 数量: 0
成功率: 100.00%

✅ 所有 API 都支持 static 语法

报告已保存到: /tmp/syntax_type_check_report.json
```

### 3. ArkTS-dynamic 语法检查

```bash
# 检查动态语法测试用例
cd /mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest/entry/src/ohosTest/ets/test/

node /mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
  --syntax-type dynamic \
  --test-dir ./
```

## 命令行参数

| 参数 | 简写 | 必需 | 说明 |
|------|------|------|------|
| `--syntax-type` | `-s` | 是 | 任务语法类型：`static` 或 `dynamic` |
| `--test-cases` | `-t` | 否* | 测试用例文件列表（与 `--test-dir` 二选一） |
| `--test-dir` | `-d` | 否* | 测试用例目录（与 `--test-cases` 二选一） |
| `--api-info` | `-a` | 否 | API 信息文件路径（默认查找常见路径） |
| `--report` | `-r` | 否 | 报告输出路径（默认: `/tmp/syntax_type_check_report.json`） |
| `--verbose` | `-v` | 否 | 详细输出模式 |
| `--help` | `-h` | 否 | 显示帮助信息 |

* 至少需要指定 `--test-cases` 或 `--test-dir` 中的一个

## 常见使用场景

### 场景 1: 编译前检查

```bash
# 1. 进入测试目录
cd /mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode_static/entry/src/main/src/test/

# 2. 检查测试用例
node /mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
  --syntax-type static \
  --test-dir ./

# 3. 如果检查通过（退出码 0），则编译
if [ $? -eq 0 ]; then
  echo "检查通过，开始编译..."
  ./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTestErrorCodeStaticTest
else
  echo "检查失败，请修复问题后再编译"
  exit 1
fi
```

### 场景 2: 检查特定 API

```bash
# 检查使用了 On.text API 的测试用例
grep -l "ON.text(" UitestOnTextErrorStatic.test.ets | \
  xargs node /mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
    --syntax-type static
```

### 场景 3: CI/CD 集成

```bash
# 在 CI/CD 流程中使用
syntax_type="static"
test_dir="/mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode_static/entry/src/main/src/test/"

# 检查语法类型
node /mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
  --syntax-type "$syntax_type" \
  --test-dir "$test_dir"

if [ $? -eq 0 ]; then
  echo "语法类型检查通过"
  # 继续编译
else
  echo "语法类型检查失败，退出码: $?"
  exit 1
fi
```

## 报告格式

### JSON 报告

```json
{
  "timestamp": "2026-03-03T10:30:00.000Z",
  "syntaxType": "static",
  "summary": {
    "totalAPIs": 89,
    "validAPIs": 89,
    "invalidAPIs": 0,
    "successRate": "100.00%"
  },
  "invalidAPIs": [],
  "syntaxStatistics": {
    "totalAPIs": 116,
    "syntaxTypes": {
      "dynamic": 10,
      "static": 0,
      "both": 106,
      "unknown": 0
    }
  }
}
```

### 报告字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `timestamp` | string | 检查时间戳 |
| `syntaxType` | string | 任务语法类型（`static` 或 `dynamic`） |
| `summary.totalAPIs` | number | 检查的 API 总数 |
| `summary.validAPIs` | number | 有效的 API 数量 |
| `summary.invalidAPIs` | number | 无效的 API 数量 |
| `summary.successRate` | string | 成功率（百分比） |
| `invalidAPIs` | array | 无效的 API 列表 |
| `syntaxStatistics` | object | 语法类型统计信息 |

### 无效 API 条目

```json
{
  "testCase": "UitestOnTextErrorStatic.test.ets",
  "api": "On.text",
  "className": "On",
  "methodName": "text",
  "syntaxType": "dynamic",
  "requiredSyntax": "static",
  "reason": "API 仅支持 dynamic 语法，但任务要求 static 语法"
}
```

## 常见问题

### 问题 1: 检查失败，退出码 1

**现象**:
```
⚠️  发现 5 个问题

详情请查看报告: /tmp/syntax_type_check_report.json
```

**原因**: 测试用例中使用了不支持目标语法类型的 API

**解决方案**:
1. 查看报告文件，了解哪些 API 有问题
2. 修改测试用例，使用支持目标语法的替代 API
3. 重新运行检查脚本
4. 确认检查通过后再编译

### 问题 2: 未找到 API 信息

**现象**:
```
警告: 未找到 API 信息: On.text
警告: API On.text 缺少语法支持信息
```

**原因**: API 信息文件中没有相关 API 的信息

**解决方案**:
1. 确认 API 信息文件路径正确
2. 确保 API 信息文件已更新并包含语法类型信息
3. 使用 `--api-info` 参数指定正确的 API 信息文件路径

### 问题 3: 文件不存在

**现象**:
```
错误: 文件不存在: UitestOnTextErrorStatic.test.ets
```

**原因**: 指定的测试文件不存在

**解决方案**:
1. 检查文件路径是否正确
2. 确认文件是否已经生成
3. 使用 `--test-dir` 参数检查整个目录

## 最佳实践

### 1. 编译前检查

在每次编译前都运行语法类型检查，可以：

- ✅ 提早发现问题，避免编译浪费
- ✅ 确保测试用例质量
- ✅ 提高编译成功率
- ✅ 节省调试时间

### 2. 集成到构建流程

```bash
# 在 build.sh 中集成检查
function check_syntax_type() {
  local syntax_type=$1
  local test_dir=$2
  
  echo "检查 API 语法类型..."
  node /mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
    --syntax-type "$syntax_type" \
    --test-dir "$test_dir"
  
  return $?
}

# 使用示例
check_syntax_type "static" "./test/"
if [ $? -eq 0 ]; then
  # 继续编译
  ./build.sh ...
fi
```

### 3. 定期检查

定期运行检查脚本，可以：

- 持续监控测试用例质量
- 及时发现新增的不兼容 API
- 维护测试用例的正确性

## 输出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 检查报告 | `/tmp/syntax_type_check_report.json` | JSON 格式的检查结果报告 |

## 退出码

| 退出码 | 含义 | 说明 |
|--------|------|------|
| 0 | 成功 | 所有 API 都支持目标语法类型 |
| 1 | 失败 | 存在不支持目标语法类型的 API |

## 脚本功能

### 自动化功能

1. **API 识别**
   - 自动识别测试用例中使用的 API
   - 支持常见的 API 模式匹配
   - 准确提取类名和方法名

2. **语法类型验证**
   - 自动检查 API 是否支持目标语法类型
   - 支持动态和静态两种语法类型
   - 提供详细的验证结果

3. **报告生成**
   - 自动生成 JSON 格式的检查报告
   - 包含详细的错误信息和建议
   - 支持自定义报告输出路径

4. **批量处理**
   - 支持同时检查多个测试文件
   - 支持检查整个测试目录
   - 提高检查效率

## 示例

### 示例 1: 检查新生成的测试用例

```bash
# 生成测试用例后，立即检查
node /mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
  --syntax-type static \
  --test-cases UitestOnTextErrorStatic.test.ets UitestOnIdErrorStatic.test.ets

# 输出
# 检查摘要
# 使用的 API 数量: 12
# 有效的 API 数量: 12
# 无效的 API 数量: 0
# 成功率: 100.00%
# ✅ 所有 API 都支持 static 语法
```

### 示例 2: 检查现有测试用例

```bash
# 检查整个测试目录
cd /mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode_static/entry/src/main/src/test/

node /mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
  --syntax-type static \
  --test-dir ./

# 输出
# 检查 24 个测试文件...
# 找到 24 个测试文件
# 验证 API 语法类型...
# 使用的 API 数量: 89
# 有效的 API 数量: 89
# 无效的 API 数量: 0
# 成功率: 100.00%
# ✅ 所有 API 都支持 static 语法
```

### 示例 3: 详细模式检查

```bash
# 使用详细模式检查
node /mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
  --syntax-type static \
  --test-cases UitestOnTextErrorStatic.test.ets \
  --verbose

# 输出（详细模式）
# ✓ UitestOnTextErrorStatic.test.ets: On.text 支持 static 语法
# ✓ UitestOnTextErrorStatic.test.ets: On.id 支持 static 语法
# ✓ UitestOnTextErrorStatic.test.ets: On.type 支持 static 语法
# ...
# 检查摘要
# 语法类型: static
# 检查的测试文件: 1 个
# 使用的 API 数量: 3
# 有效的 API 数量: 3
# 无效的 API 数量: 0
# 成功率: 100.00%
```

---

**文档版本**: 1.0.0
**创建日期**: 2026-03-03
**脚本版本**: 1.0.0
**更新日期**: 2026-03-03
