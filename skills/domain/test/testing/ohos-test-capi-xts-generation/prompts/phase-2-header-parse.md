## Phase 2: Header File Parsing

---

### 📚 参考文档（按需查阅）

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `modules/L1_Analysis/parser/unified_api_parser_c.md` | C 头文件解析规则（函数签名、参数类型、宏定义、枚举） | 本 Phase 必须加载 |

---

### ⚙️ 按需加载

| 任务 | 加载文件 | 说明 |
|------|---------|------|
| 需要分析已有工程结构 | `modules/L1_Analysis/parser/project_parser.md` | 工程配置解析 |

---

### 🚫 Do NOT Load

```
所有 modules/L2_Generation 模块
所有 modules/L3_Validation 模块
```

---

### 解析策略

**Info Source Priority**: `.h` 头文件（最高）→ 子系统配置 → 参考示例 → API 文档

#### 多 .h 文件处理

当目标涉及多个 .h 文件时，按子系统/模块分组并行解析。

#### 解析范围

从 .h 中提取：

| 信息 | 说明 | 后续用途 |
|------|------|---------|
| 函数签名 | 函数名、参数类型、返回值类型 | N-API 封装生成 |
| 参数约束 | const 修饰、可空性、指针方向（in/out） | 测试设计 |
| 错误码枚举/宏 | 返回值中定义的错误码 | ERROR 类型测试 |
| 枚举定义 | 枚举值和取值范围 | 参数边界测试 |
| 宏定义 | 常量宏（如 BUFFER_SIZE） | 边界值测试 |
| 结构体定义 | 参数中涉及的结构体 | N-API 类型转换 |
| typedef | 类型别名 | 参数映射 |

#### 解析输出

每个 API 的结构化信息：

```json
{
  "function_name": "OH_XXX_FunctionName",
  "header_file": "xxx/xxx.h",
  "return_type": "int",
  "params": [
    {"name": "param1", "type": "const char*", "direction": "in", "nullable": false},
    {"name": "param2", "type": "size_t*", "direction": "out", "nullable": false}
  ],
  "error_codes": ["XXX_OK", "XXX_ERROR_INVALID_PARAM"],
  "since_version": "10",
  "deprecated": false
}
```

#### 测试类型判定

根据提取的信息自动判定应生成的测试类型：

| 条件 | 测试类型 |
|------|---------|
| 有正常参数 | PARAM |
| 有错误码定义 | ERROR |
| 有明确返回值 | RETURN |
| 有数值/字符串参数 | BOUNDARY |
| 涉及内存分配 | MEMORY |

---

### Flow 差异

| Flow | 解析范围 | 说明 |
|------|---------|------|
| Flow A | 仅解析覆盖率报告中列出的未覆盖 API | 精准解析 |
| Flow C | 解析用户指定的全部目标 API | 全量解析 |
