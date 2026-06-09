# 使用示例

## 全量覆盖率示例

### 示例1: 为单个部件生成全量覆盖率报告
```
用户输入: "为 ability_base 部件生成全量代码覆盖率报告"
解析结果:
  - coverage_type: "full_coverage"
  - part: "ability_base"
  - output_path: "{CODE_ROOT}/coverage_result"
```

**执行流程**:
1. 检查环境和配置
2. 预编译（如果需要）
3. 编译 ability_base 部件的用例
4. 执行测试
5. 生成覆盖率报告
6. 恢复环境

**预期耗时**: 3-5小时

---

### 示例2: 为子系统生成全量覆盖率报告
```
用户输入: "为 ability 子系统生成全量代码覆盖率报告"
解析结果:
  - coverage_type: "full_coverage"
  - subsystem: "ability"
  - 需要通过预编译解析得到部件列表: ["dmsfwk_lite", "ability_base", "ability_runtime", ...]
```

**执行流程**:
1. 检查环境和配置
2. 预编译生成子系统部件信息
3. 解析子系统得到部件列表
4. 编译所有部件的用例
5. 执行测试
6. 生成覆盖率报告
7. 恢复环境

**预期耗时**: 4-6小时（取决于子系统规模）

---

### 示例3: 为多个部件生成全量覆盖率报告
```
用户输入: "为 ability_base, ability_runtime 部件生成全量代码覆盖率报告"
解析结果:
  - coverage_type: "full_coverage"
  - part_name_list: ["ability_base", "ability_runtime"]
```

**执行流程**:
1. 检查环境和配置
2. 依次编译 ability_base 和 ability_runtime 部件
3. 执行两个部件的测试
4. 生成覆盖率报告
5. 恢复环境

**预期耗时**: 4-5小时

---

### 示例4: 为模块级别生成覆盖率报告
```
用户输入: "为 ability_base 部件的 want 模块生成全量代码覆盖率报告"
解析结果:
  - coverage_type: "full_coverage"
  - part: "ability_base"
  - module: "want"
```

**执行流程**:
1. 检查环境和配置
2. 编译 ability_base 部件的 want 模块用例
3. 执行测试
4. 生成覆盖率报告
5. 恢复环境

**预期耗时**: 2-3小时

---

### 示例5: 跳过编译生成覆盖率报告
```
用户输入: "为 ability_base 部件生成全量代码覆盖率报告，跳过编译"
解析结果:
  - coverage_type: "full_coverage"
  - part: "ability_base"
  - skip_compiler: true
```

**执行流程**:
1. 检查环境和配置
2. 跳过编译（假设已经编译完成）
3. 直接执行测试
4. 生成覆盖率报告
5. 恢复环境

**预期耗时**: 1-2小时（节省编译时间）

**⚠️ 前提条件**:
- 已经完成了一次完整的覆盖率编译
- 没有修改源代码
- 编译产物完整

---

## 增量覆盖率示例

### 示例1: 为单个部件生成增量覆盖率报告
```
用户输入: "为 ability_base 部件生成增量代码覆盖率报告"
解析结果:
  - coverage_type: "incremental_coverage"
  - part: "ability_base"
  - diffPath: 自动从 git diff 生成
```

**执行流程**:
1. 检查环境和配置
2. 执行 `git diff` 生成 diff 文件
3. 本地编译 ability_base 部件
4. 执行覆盖率计算
5. 生成增量覆盖率报告
6. 清理临时文件

**预期耗时**: 30分-2小时

---

### 示例2: 使用指定 diff 文件生成增量覆盖率报告
```
用户输入: "为 ability_base 部件生成增量代码覆盖率报告，diff 文件路径为 /tmp/changes.patch"
解析结果:
  - coverage_type: "incremental_coverage"
  - part: "ability_base"
  - diffPath: "/tmp/changes.patch"
```

**执行流程**:
1. 检查环境和配置
2. 使用指定的 diff 文件（不执行 git diff）
3. 本地编译 ability_base 部件
4. 执行覆盖率计算
5. 生成增量覆盖率报告
6. 清理临时文件

**预期耗时**: 30分-2小时

---

### 示例3: 为多个部件生成增量覆盖率报告
```
用户输入: "为 ability_base, ability_runtime 部件生成增量代码覆盖率报告"
解析结果:
  - coverage_type: "incremental_coverage"
  - part_name_list: ["ability_base", "ability_runtime"]
  - diffPath: 自动从 git diff 生成
```

**执行流程**:
1. 检查环境和配置
2. 执行 `git diff` 生成 diff 文件
3. 并行编译 ability_base 和 ability_runtime 部件
4. 执行覆盖率计算
5. 生成增量覆盖率报告
6. 清理临时文件

**预期耗时**: 1-2.5小时（并行执行）

---

## 输出路径示例

### 示例1: 使用默认输出路径
```
用户输入: "为 ability_base 部件生成全量代码覆盖率报告"
解析结果:
  - output_path: "{CODE_ROOT}/coverage_result"
```

**报告结构**:
```
coverage_result/
├── code_coverage/
│   ├── coverage/
│   │   └── reports/
│   │       └── cxx/
│   │           └── html/
│   │               └── index.html
│   └── interface_coverage/
│       └── result/
│           └── coverage/
│               └── interface_kits/
│                   └── ohos_interfaceCoverage.html
└── error.log
```

---

### 示例2: 使用自定义输出路径
```
用户输入: "为 ability_base 部件生成全量代码覆盖率报告，将报告输出到 /tmp/coverage_report"
解析结果:
  - output_path: "/tmp/coverage_report"
```

**报告结构**:
```
/tmp/coverage_report/
├── code_coverage/
│   ├── coverage/
│   │   └── reports/
│   │       └── cxx/
│   │           └── html/
│   │               └── index.html
│   └── interface_coverage/
│       └── result/
│           └── coverage/
│               └── interface_kits/
│                   └── ohos_interfaceCoverage.html
└── error.log
```

---

## 参数匹配规则详解

### 子系统匹配规则

**支持的表达式**:
- "对 ability 子系统" → subsystem = "ability"
- "ability 子系统" → subsystem = "ability"
- "子系统 ability" → subsystem = "ability"

**正则表达式**:
- `'对?(\w+)子系统'`
- `'?(\w+)子系统'`
- `'子系统(\w+)'`

**限制**: 仅全量覆盖率支持

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

**支持**: 全量覆盖率（支持多部件）、增量覆盖率（仅支持单部件）

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

### 覆盖率类型匹配规则

**全量覆盖率**:
- 匹配"全量"字样
- 示例: "全量代码覆盖率"、"生成全量报告"

**增量覆盖率**:
- 匹配"增量"字样
- 示例: "增量代码覆盖率"、"生成增量报告"

---

### 报告输出路径匹配规则

**支持的表达式**:
- "将报告输出到 /tmp/coverage_report" → output_path = "/tmp/coverage_report"
- "报告输出到 /tmp/coverage_report" → output_path = "/tmp/coverage_report"
- "输出到 /tmp/coverage_report" → output_path = "/tmp/coverage_report"

**默认值**: `{CODE_ROOT}/coverage_result`

---

## 错误示例

### 错误1: 增量覆盖率使用子系统
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

### 错误2: 全量覆盖率缺少必要参数
```
用户输入: "生成全量代码覆盖率报告"
错误: 缺少必要参数
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

### 错误3: 增量覆盖率缺少部件参数
```
用户输入: "生成增量代码覆盖率报告"
错误: 缺少必要参数
原因: 增量覆盖率必须提供 part 参数
```

**正确做法**:
```
用户输入: "为 ability_base 部件生成增量代码覆盖率报告"
```

---

## 更多资源

- 🚀 **快速开始**: 详见 `references/quick-start.md` - 环境配置指南
- ⚡ **性能说明**: 详见 `references/performance-guide.md` - 预期耗时、资源占用
- 📖 **参数指南**: 详见 `references/parameter-guide.md` - 参数解析规则、验证规则、匹配规则详解
- 💡 **最佳实践**: 详见 `references/best-practices.md` - 场景选择建议
- 🔧 **问题排查**: 详见 `references/troubleshooting.md` - 错误恢复策略