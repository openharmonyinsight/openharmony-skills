# 规则扩展与自定义规则机制

> **版本**: 1.1.0
> **更新日期**: 2026-04-23

## 概述

check-xts-code-quality 采用**三层规则体系**，在29条内置规则的基础上，支持用户按业务领域添加规则扩展和自定义规则。

**扩展来源不限**: API文档分析、团队编码规范、代码评审结论、子系统特有约束、历史缺陷复盘——任何业务诉求都可以驱动规则扩展。

### 三层规则体系

```
┌─────────────────────────────────────────────┐
│  第一层: 内置规则 (R001-R023, R201-R206)     │
│  29条预构建规则，默认全部加载                  │
│  路径: scripts/scanners/r{NNN}_scan.py        │
└──────────────────┬──────────────────────────┘
                   │ 可选扩展（任意来源驱动）
┌──────────────────▼──────────────────────────┐
│  第二层: 规则扩展 (type=extension)            │
│  对内置规则追加额外的检查维度                  │
│  例: R204扩展检测ImageKit资源API释放          │
│  例: R001扩展检测子系统特有的禁止API          │
│  来源: API文档/编码规范/评审结论/任何诉求      │
└──────────────────┬──────────────────────────┘
                   │ 独立自定义
┌──────────────────▼──────────────────────────┐
│  第三层: 自定义规则 (type=custom)             │
│  独立于内置规则的新检查项                     │
│  例: 团队规范-禁止console.log                │
│  例: 团队规范-import排序检查                  │
│  来源: 编码规范/团队约定/任何诉求             │
└─────────────────────────────────────────────┘
```

## 快速上手

> **核心理念**: 用户只需用自然语言描述需求，Skill自动完成JSON配置生成、文件放置、规则执行。用户无需了解JSON格式、字段含义等实现细节。

### 用户输入方式

用户在触发本技能时，用自然语言描述需求即可。Skill根据关键词自动判断类型：

| 用户这样说... | Skill自动判断... |
|--------------|-----------------|
| "帮我扩展R001，额外检测XXX API" | → `type=extension`, `base_rule=R001`, `id=R001_EXT_XXX` |
| "测试文件必须包含@tc.number" | → `type=custom`, `id=C001` |
| "我们团队有自己的编码规范" | → `type=custom`, `id=C002` (用户自定义ID) |

**判断规则**:
- 关键词 "扩展R0XX"、"追加检测" → **规则扩展**（与内置规则关联，追加检查维度）
- 关键词 "团队要求"、"禁止"、"必须" → **自定义规则**（全新独立检查项）

### Skill自动执行流程

用户描述需求后，Skill自动完成以下5步：

```
用户输入: "帮我扩展R001，额外检测fs.writeSync同步文件写入API"
         │
         ▼
Step 1: 理解需求 → 判断为规则扩展，base_rule=R001
         │
         ▼
Step 2: 检查预置规则 → 发现已有 R001_extra_sync_api.json，直接复用
         │
         ▼
Step 3: 放置文件 → 自动创建 扫描路径/.xts_custom_rules/R001_EXT_sync_file.json
         │
         ▼
Step 4: 执行扫描 → 内置29条规则 + R001_EXT_SYNC_FILE 一起运行
         │
         ▼
Step 5: 生成报告 → 扩展规则结果与内置规则统一展示
```

### 报告展示效果

终端输出中，扩展/自定义规则结果与内置规则**合并展示**：

```
| 规则编号             | 问题类型               | 严重级别 | 问题数量 |
|---------------------|-----------------------|---------|---------|
| R001                | 禁止使用getSync系统接口 | Critical | 15      |
| R001_EXT_SYNC_FILE  | 扩展-禁止同步文件写入API | Critical | 3       |  ← 规则扩展
| R003                | 禁止恒真断言           | Critical | 0       |
| ...（其余内置规则）                                                         |
| C001                | 测试文件必须包含@tc.number | Warning | 8    |  ← 自定义规则
```

Excel Sheet 1 问题明细示例：

| 问题ID | 问题类别 | 问题类型 | 严重级别 | 文件路径 | 行号 | 代码片段 | 修复建议 |
|--------|---------|---------|---------|---------|------|---------|---------|
| R001_EXT_SYNC_FILE | 编码规范合规 | 禁止同步文件写入 | Critical | .../FileTest.test.ets | 42 | `fs.writeSync(data)` | 请使用异步方法write() |
| C001 | 团队规范 | it()缺少@tc.number | Warning | .../ApiTest.test.ets | 85 | `it('test_case', () => {` | 请在it()上方添加@tc.number注释 |

**问题ID格式**:
- 规则扩展: `R{NNN}_EXT_{标识}`（如 `R001_EXT_SYNC_FILE`）
- 自定义规则: `C{NNN}`（如 `C001`）

### Skill自动生成的文件

Skill会自动在扫描路径下创建 `.xts_custom_rules/` 目录并生成配置文件：

```
your-project/                          ← 扫描路径
├── entry/src/.../ApiTest.test.ets
└── .xts_custom_rules/                 ← Skill自动创建
    ├── R001_EXT_sync_file.json        ← Skill自动生成
    └── C001_tc_number.json            ← Skill自动生成
```

用户无需手动创建或编辑这些JSON文件。JSON格式详情见下方"配置文件格式"章节，供Skill实现参考。

### 文件放置位置与加载机制

| 放置位置 | 加载方式 | 适用场景 |
|---------|---------|---------|
| Skill目录 `extensions/` | 自动发现（扩展规则默认位置） | 预置规则，开箱即用 |
| 扫描路径下 `.xts_custom_rules/` | 自动发现（自定义规则默认位置） | 跟随代码仓库，团队共享 |
| 任意路径 | `--rules-file <文件>` | 临时规则，指定文件路径 |
| 规则ID指定 | `--rules R001_EXT` 或 `--rules C001` | 单独执行，从默认路径查找 |

**配置加载优先级**: `--rules-file` > `--rules ID` > `extensions/` > `.xts_custom_rules/`

### 预置规则（开箱即用）

以下扩展配置已预置在技能目录 `references/custom_rules/extensions/` 中，Skill在识别到相关需求时会自动复用：

| 文件 | 说明 | 触发示例 |
|------|------|---------|
| `R001_extra_sync_api.json` | 追加检测 fs.writeSync 等同步阻塞API | "扩展R001禁止同步文件写入" |

预置自定义规则在 `references/custom_rules/custom/` 中：

| 文件 | 说明 | 触发示例 |
|------|------|---------|
| `C001_tc_number_required.json` | 测试文件必须包含@tc.number注释 | "测试文件必须有@tc.number" |

## 配置文件格式

### 规则扩展配置 (extends 内置规则)

```json
{
  "type": "extension",
  "base_rule": "R001",
  "id": "R001_EXT_ARKUI",
  "name": "ArkUI子系统-额外禁止API",
  "severity": "Critical",
  "category": "编码规范合规",
  "description": "在R001基础上，额外检测ArkUI子系统禁止使用的API",
  "scope": {
    "file_types": [".ets", ".ts", ".js"],
    "target_dirs": ["arkui/"]
  },
  "patterns": [
    {
      "name": "禁止使用UIContext静态获取",
      "pattern": "\\bUIContext\\.(?:getComponentManager|getFocusController)\\s*\\(",
      "suggestion": "请通过组件上下文获取，而非静态方法"
    }
  ],
  "traps": [
    "排除注释中的匹配",
    "排除字符串中的匹配"
  ]
}
```

### 自定义规则配置 (独立新规则)

```json
{
  "type": "custom",
  "id": "C001",
  "name": "团队命名规范-文件名必须小驼峰",
  "severity": "Warning",
  "category": "团队规范",
  "description": "测试文件名必须使用小驼峰命名",
  "scope": {
    "file_types": [".test.ets", ".test.ts"],
    "target_dirs": []
  },
  "patterns": [
    {
      "name": "文件名小驼峰检查",
      "pattern": null,
      "check_type": "filename",
      "filename_pattern": "^[a-z][a-zA-Z0-9]*\\.test\\.(ets|ts|js)$",
      "negate": true,
      "suggestion": "文件名应使用小驼峰命名，如: myFeatureTest.test.ets"
    }
  ],
  "traps": []
}
```

### 检查类型 (check_type)

| check_type | 说明 | 适用场景 |
|------------|------|---------|
| `content` (默认) | 正则匹配文件内容 | API调用、代码模式检测 |
| `filename` | 正则匹配文件名 | 文件命名规范 |
| `json_field` | 检查JSON文件字段值 | 配置文件合规 |
| `import_check` | 检查import语句 | 依赖合规 |

### pattern 字段说明

```json
{
  "name": "规则描述名称",
  "pattern": "正则表达式（content类型时必填）",
  "check_type": "检查类型（默认content）",
  "filename_pattern": "文件名正则（filename类型时必填）",
  "negate": false,
  "suggestion": "修复建议",
  "json_path": "JSON字段路径（json_field类型时必填）",
  "json_expected": "期望值或校验函数（json_field类型时必填）",
  "import_module": "模块名（import_check类型时必填）",
  "import_forbidden": true
}
```

## 执行流程

1. **解析规则参数**: 
   - 默认：仅执行内置规则（29条）
   - `--ext`: 内置规则 + 扩展规则（从extensions目录加载全部）
   - `--custom`: 内置规则 + 自定义规则（从.xts_custom_rules目录加载全部）
   - `--rules R001`: 仅内置规则R001
   - `--rules R001_EXT`: 仅扩展规则R001_EXT（跳过内置）
   - `--rules R001,R001_EXT`: 内置R001 + 扩展R001_EXT
   - `--rules-file xxx.json`: 仅执行指定文件的规则
2. **加载规则** (按优先级):
   - `--rules-file`: 直接加载指定文件
   - `--rules ID`: 从默认路径查找匹配ID的规则文件
   - `--ext`: 加载extensions目录全部规则
   - `--custom`: 加载.xts_custom_rules目录全部规则
3. **验证配置**: 检查JSON格式、必填字段、正则语法
4. **执行扫描**:
   - 内置规则: Python脚本执行（步骤2）
   - 扩展规则: AI读取规则描述后扫描（步骤4，需--ext或--rules指定ID）
   - 自定义规则: AI读取规则描述后扫描（步骤4，需--custom或--rules指定ID）
5. **生成报告**: 所有结果合并，步骤5统一输出

## 报告集成

自定义规则的扫描结果与内置规则**统一展示**在同一份报告中:

- Excel Sheet 1 "代码质量检查报告": 自定义规则问题与内置规则问题混合排列
- Excel Sheet 2 "问题扫描结果汇总": 自定义规则单独一行，标注来源

问题ID格式:
- 规则扩展: `R001_EXT_ARKUI` (基础规则ID + `_EXT_` + 扩展标识)
- 自定义规则: `C001`, `C002` ... (用户自定义ID)

## 最佳实践

1. **规则扩展优先**: 如果检查逻辑与已有规则相关，优先使用规则扩展而非独立自定义规则
2. **ID命名规范**: 扩展规则用 `R{NNN}_EXT_{标识}`，自定义规则用 `C{NNN}`
3. **severity对齐**: 与内置规则使用相同的 Critical/Warning 级别体系
4. **target_dirs限定**: 尽量通过 `target_dirs` 缩小扫描范围，提高性能
5. **traps记录**: 记录已知误报场景，便于后续优化
