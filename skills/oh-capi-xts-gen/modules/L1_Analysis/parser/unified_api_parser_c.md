# 头文件解析模块

## 一、模块概述

L1_Analysis 模块负责解析 C 语言头文件（`.h`），提取 API 信息，为测试用例生成提供基础数据。

## 二、头文件解析

### 2.1 解析目标

从头文件中提取以下信息：

1. **函数声明**
   - 函数名
   - 返回值类型
   - 参数列表
   - 参数类型
   - 参数名称

2. **宏定义**
   - 宏名
   - 宏值
   - 宏类型（常量、函数式宏）

3. **类型定义**
   - 结构体定义
   - 枚举定义
   - 类型别名

4. **注释**
   - 函数文档注释
   - 参数说明
   - 返回值说明

### 2.2 解析流程

```
读取头文件
  ↓
预处理（处理 #ifdef、#include 等）
  ↓
词法分析（分词）
  ↓
语法分析（构建 AST）
  ↓
提取 API 信息
  ↓
输出 API 信息结构
```

### 2.3 API 信息结构

```json
{
  "function_name": "HiLogPrint",
  "return_type": "int",
  "parameters": [
    {
      "type": "int",
      "name": "type",
      "description": "日志类型"
    },
    {
      "type": "int",
      "name": "level",
      "description": "日志级别"
    },
    {
      "type": "unsigned int",
      "name": "domain",
      "description": "日志域"
    },
    {
      "type": "const char*",
      "name": "tag",
      "description": "日志标签"
    },
    {
      "type": "const char*",
      "name": "fmt",
      "description": "格式化字符串"
    }
  ]
}
```

## 三、API 信息提取

### 3.1 函数声明模式

```c
// 标准函数声明
int HiLogPrint(int type, int level, unsigned int domain, const char* tag, const char* fmt, ...);

// 函数指针声明
typedef int (*CallbackFunc)(int param);

// 宏函数
#define HILOG_DEBUG(fmt, ...) HiLogPrint(LOG_CORE, LOG_DEBUG, LOG_DOMAIN, TAG, fmt, ##__VA_ARGS__)
```

### 3.2 参数类型识别

| 类型 | 示例 | 说明 |
|------|------|------|
| 基本类型 | `int`, `char`, `float` | C 基本数据类型 |
| 指针类型 | `int*`, `const char*` | 指针类型 |
| 数组类型 | `int[10]`, `char[]` | 数组类型 |
| 结构体 | `struct MyStruct` | 用户定义结构体 |
| 枚举 | `enum MyEnum` | 枚举类型 |
| 函数指针 | `int (*)(int)` | 函数指针 |

### 3.3 宏定义识别

```c
// 常量宏
#define LOG_CORE 0
#define LOG_DEBUG 3

// 函数式宏
#define HILOG_DEBUG(fmt, ...) \
    HiLogPrint(LOG_CORE, LOG_DEBUG, LOG_DOMAIN, TAG, fmt, ##__VA_ARGS__)

// 条件编译宏
#ifdef ENABLE_FEATURE
#define FEATURE_MACRO 1
#else
#define FEATURE_MACRO 0
#endif
```

## 四、测试覆盖分析

### 4.1 现有测试文件扫描

扫描现有测试文件，提取以下信息：

1. **测试用例列表**
   - 测试用例编号
   - 测试用例名称
   - 测试用例描述

2. **测试覆盖的 API**
   - API 名称
   - 覆盖的参数组合
   - 覆盖的测试场景

3. **代码风格**
   - 缩进风格
   - 命名规范
   - 注释风格

### 4.2 覆盖率分析

```markdown
覆盖率分析报告：

## API 覆盖情况

| API | 总用例数 | 已覆盖 | 未覆盖 | 覆盖率 |
|-----|---------|--------|--------|--------|
| HiLogPrint | 10 | 8 | 2 | 80% |
| HiLogPrintArgs | 5 | 3 | 2 | 60% |

## 缺失测试

### HiLogPrint
- 参数测试：缺失 (LOG_CORE, LOG_DEBUG, nullptr, "%s")
- 边界值测试：缺失超长字符串测试
- 错误码测试：缺失错误码 401 测试

### HiLogPrintArgs
- 参数测试：缺失参数组合测试
```

## 五、代码风格提取

### 5.1 缩进风格

```c
// 4 空格缩进
HWTEST_F(HilogTest, HiLogPrint_Normal, TestSize.Level1)
{
    int ret = HiLogPrint(LOG_CORE, LOG_INFO, LOG_DOMAIN, "TAG", "test");
    EXPECT_GE(ret, 0);
}
```

### 5.2 命名规范

```c
// 测试套名：PascalCase + Test
HilogTest

// 测试用例名：API名 + 场景描述
HiLogPrint_NormalParam
HiLogPrint_NullPointer
HiLogPrint_BoundaryValue
```

### 5.3 注释风格

```c
/* @
 * @tc.name: SUB_HILOG_HILOG_PRINT_PARAM_001
 * @tc.desc: 测试 HiLogPrint 的正常参数
 * @tc.type: FUNC
 */
```

## 六、覆盖率报告解析

### 6.1 报告格式

```markdown
覆盖率报告：
  未覆盖的 API:
    - API1
    - API2
  缺失的参数组合:
    - API1: (param1_value, param2_value)
  缺失的测试场景:
    - API1: 边界值测试
```

### 6.2 报告解析

解析覆盖率报告，提取：

1. **未覆盖的 API**
2. **缺失的参数组合**
3. **缺失的测试场景**
4. **需要补充的测试类型**

## 七、API 语法类型过滤

### 7.1 语法类型说明

OpenHarmony API 支持不同的语法类型：

- **C API**: 纯 C 语言 API
- **C++ API**: C++ 语言 API
- **Native API**: 原生 API

### 7.2 语法类型过滤

根据测试任务过滤 API：

```c
// 如果任务明确指定 C API，只生成 C API 测试
// 如果任务明确指定 C++ API，只生成 C++ API 测试
```

## 八、常见问题

### Q1: 头文件包含条件编译导致解析失败

**解决方案**：
- 使用预处理器展开条件编译
- 分析所有可能的分支

### Q2: 宏定义展开困难

**解决方案**：
- 识别宏定义模式
- 递归展开宏定义
- 处理可变参数宏

### Q3: 函数指针类型识别

**解决方案**：
- 使用正则表达式匹配函数指针模式
- 提取返回类型、参数类型

---

**版本**: 1.0.0
**更新日期**: 2026-03-06
