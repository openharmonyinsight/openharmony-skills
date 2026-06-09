# 参数指南

本文档详细说明覆盖率报告生成的所有参数、解析规则、验证规则和匹配规则。

---

## 参数来源

| 参数名 | 来源 | 说明 |
|--------|------|------|
| `code_root` | `{SKILL_DIR}/config/user-config.json` 的 `code_root` 字段 | OpenHarmony 代码根目录路径 |
| `coverage_type` | 从用户输入解析 | 任务类型：`full_coverage` 或 `incremental_coverage` |
| `subsystem` | 从用户输入解析 | 子系统名称（仅全量覆盖率支持） |
| `part` | 从用户输入解析 | 部件名称（增量必须填写，全量支持多部件用逗号分隔） |
| `module` | 从用户输入解析 | 模块名称 |
| `testsuite` | 从用户输入解析 | 测试套名称 |
| `testcase` | 从用户输入解析 | 测试用例名称 |
| `diffPath` | 从用户输入解析 | diff 文件路径（仅增量覆盖率需要，不传入则自动生成） |
| `output_path` | 从用户输入解析 | 报告输出路径（可选，默认值 `{CODE_ROOT}/coverage_result`） |
| `skip_compiler` | 从用户输入解析 | 是否跳过编译（仅全量覆盖率支持，默认 false） |

---

## 参数解析规则

### 覆盖率类型识别

根据用户输入中的关键词识别任务类型：

| 关键词 | 类型 | 示例 |
|--------|------|------|
| "全量"、"full"、"complete" | 全量覆盖率 | "生成全量代码覆盖率报告" |
| "增量"、"incremental"、"diff" | 增量覆盖率 | "生成增量代码覆盖率报告" |

---

### 子系统匹配规则

**支持的表达式**:
- "对 ability 子系统" → subsystem = "ability"
- "ability 子系统" → subsystem = "ability"
- "子系统 ability" → subsystem = "ability"

**正则表达式**:
- `'对?(\w+)子系统'`
- `'?(\w+)子系统'`
- `'子系统(\w+)'`

**限制**: 仅全量覆盖率支持，增量覆盖率不支持子系统级别

---

### 部件匹配规则

**支持的表达式**:
- "对 ability_base 部件" → part = "ability_base"
- "ability_base 部件" → part = "ability_base"
- "部件 ability_base" → part = "ability_base"
- "对 ability_base, ability_runtime 部件" → part_name_list = ["ability_base", "ability_runtime"]

**正则表达式**:
- `'对?(\w+(?:,\s*\w+)*)部件'`
- `'(\w+(?:,\s*\w+)*)部件'`
- `'部件(\w+(?:,\s*\w+)*)'`

**支持**:
- 全量覆盖率：支持单个或多个部件（逗号分隔）
- 增量覆盖率：仅支持单个部件

---

### 模块匹配规则

**支持的表达式**:
- "对 want 模块" → module = "want"
- "want 模块" → module = "want"
- "模块 want" → module = "want"

**正则表达式**:
- `'?(\w+)模块'`
- `'模块(\w+)'`

**限制**: 仅全量覆盖率支持

---

### 测试套匹配规则

**支持的表达式**:
- "对 AbilityTest 测试套" → testsuite = "AbilityTest"
- "AbilityTest 测试套" → testsuite = "AbilityTest"
- "测试套 AbilityTest" → testsuite = "AbilityTest"

**正则表达式**:
- `'?(\w+)测试套'`
- `'测试套(\w+)'`

**限制**: 仅全量覆盖率支持

---

### 用例匹配规则

**支持的表达式**:
- "对 testAbility 用例" → testcase = "testAbility"
- "testAbility 用例" → testcase = "testAbility"
- "用例 testAbility" → testcase = "testAbility"

**正则表达式**:
- `'?(\w+)用例'`
- `'用例(\w+)'`

**限制**: 仅全量覆盖率支持

---

### 报告输出路径匹配规则

**支持的表达式**:
- "将报告输出到 /tmp/coverage_report" → output_path = "/tmp/coverage_report"
- "报告输出到 /tmp/coverage_report" → output_path = "/tmp/coverage_report"
- "输出到 /tmp/coverage_report" → output_path = "/tmp/coverage_report"

**默认值**: `{CODE_ROOT}/coverage_result`

---

## 参数验证规则

### 全量覆盖率验证

**必需参数**: subsystem、part、part_name_list 三个必须至少一个不为空

**验证逻辑**:
```
IF part 不为空:
    使用 part，忽略 subsystem
    解析 part 为 part_name_list（支持逗号分隔）
ELSE IF subsystem 不为空:
    使用 subsystem
    通过预编译解析生成 part_name_list
ELSE:
    错误：MISSING_TARGET_PARAMETER
```

**参数优先级**:
- 如果提供了 part → 使用 part，忽略 subsystem
- 如果未提供 part 但提供了 subsystem → 需要解析子系统获取部件列表
- part 可以是单个部件或多个部件（逗号分隔）

**可选参数**:
- module、testsuite、testcase：可选参数
- skip_compiler：可选参数，默认 false
- output_path：可选参数，默认 `{CODE_ROOT}/coverage_result`

---

### 增量覆盖率验证

**必需参数**: part 必须有数据（不能为空）

**验证逻辑**:
```
IF part 为空:
    错误：MISSING_PART_FOR_INCREMENTAL
ELSE IF subsystem 不为空:
    错误：INCREMENTAL_NOT_SUPPORT_SUBSYSTEM
ELSE:
    继续执行
```

**限制条件**:
- part 必须提供，不支持子系统级别
- 如果提供了 subsystem → 报错 `INCREMENTAL_NOT_SUPPORT_SUBSYSTEM`
- part 只能是单个部件，不支持多部件

**可选参数**:
- diffPath：可选参数，不提供则自动执行 `git diff` 生成
- module、testsuite、testcase：可选参数
- output_path：可选参数，默认 `{CODE_ROOT}/coverage_result`

---

## 参数解析示例

### 示例1：全量覆盖率 - 单个部件
```
用户输入: "为 ability_base 部件生成全量代码覆盖率报告"
解析结果:
  - coverage_type: "full_coverage"
  - part: "ability_base"
  - part_name_list: ["ability_base"]
  - output_path: "{CODE_ROOT}/coverage_result"
  - skip_compiler: false
```

---

### 示例2：全量覆盖率 - 子系统
```
用户输入: "为 ability 子系统生成全量代码覆盖率报告"
解析结果:
  - coverage_type: "full_coverage"
  - subsystem: "ability"
  - part_name_list: ["dmsfwk_lite", "ability_base", "ability_runtime", ...]  (通过预编译解析)
  - output_path: "{CODE_ROOT}/coverage_result"
  - skip_compiler: false
```

---

### 示例3：全量覆盖率 - 多个部件
```
用户输入: "为 ability_base, ability_runtime 部件生成全量代码覆盖率报告"
解析结果:
  - coverage_type: "full_coverage"
  - part: "ability_base, ability_runtime"
  - part_name_list: ["ability_base", "ability_runtime"]
  - output_path: "{CODE_ROOT}/coverage_result"
  - skip_compiler: false
```

---

### 示例4：全量覆盖率 - 模块级别
```
用户输入: "为 ability_base 部件的 want 模块生成全量代码覆盖率报告"
解析结果:
  - coverage_type: "full_coverage"
  - part: "ability_base"
  - module: "want"
  - output_path: "{CODE_ROOT}/coverage_result"
  - skip_compiler: false
```

---

### 示例5：全量覆盖率 - 跳过编译
```
用户输入: "为 ability_base 部件生成全量代码覆盖率报告，跳过编译"
解析结果:
  - coverage_type: "full_coverage"
  - part: "ability_base"
  - skip_compiler: true
  - output_path: "{CODE_ROOT}/coverage_result"
```

**⚠️ 前提条件**:
- 已经完成了一次完整的覆盖率编译
- 没有修改源代码
- 编译产物完整

---

### 示例6：增量覆盖率 - 单个部件
```
用户输入: "为 ability_base 部件生成增量代码覆盖率报告"
解析结果:
  - coverage_type: "incremental_coverage"
  - part: "ability_base"
  - diffPath: 自动从 git diff 生成
  - output_path: "{CODE_ROOT}/coverage_result"
```

---

### 示例7：增量覆盖率 - 使用指定 diff 文件
```
用户输入: "为 ability_base 部件生成增量代码覆盖率报告，diff 文件路径为 /tmp/changes.patch"
解析结果:
  - coverage_type: "incremental_coverage"
  - part: "ability_base"
  - diffPath: "/tmp/changes.patch"
  - output_path: "{CODE_ROOT}/coverage_result"
```

---

## 错误场景

### 错误1：增量覆盖率使用子系统
```
用户输入: "为 ability 子系统生成增量代码覆盖率报告"
错误: INCREMENTAL_NOT_SUPPORT_SUBSYSTEM
原因: 增量覆盖率不支持子系统级别，仅支持部件级别
```

**正确做法**:
```
用户输入: "为 ability_base 部件生成增量代码覆盖率报告"
或
用户输入: "为 ability_base, ability_runtime 部件生成增量代码覆盖率报告"
```

---

### 错误2：全量覆盖率缺少必要参数
```
用户输入: "生成全量代码覆盖率报告"
错误: MISSING_TARGET_PARAMETER
原因: 全量覆盖率必须提供 subsystem、part 或 module 至少一个
```

**正确做法**:
```
用户输入: "为 ability_base 部件生成全量代码覆盖率报告"
或
用户输入: "为 ability 子系统生成全量代码覆盖率报告"
或
用户输入: "为 ability_base 部件的 want 模块生成全量代码覆盖率报告"
```

---

### 错误3：增量覆盖率缺少部件参数
```
用户输入: "生成增量代码覆盖率报告"
错误: MISSING_PART_FOR_INCREMENTAL
原因: 增量覆盖率必须提供 part 参数
```

**正确做法**:
```
用户输入: "为 ability_base 部件生成增量代码覆盖率报告"
```

---

## 更多资源

- 📚 **使用示例**: 详见 `references/usage-examples.md` - 完整场景示例
- 💡 **最佳实践**: 详见 `references/best-practices.md` - 场景选择建议
- 🔧 **问题排查**: 详见 `references/troubleshooting.md` - 错误恢复策略