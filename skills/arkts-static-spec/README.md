# ArkTS Static Language Specification

完整的 ArkTS 静态语言规范参考，包含官方规范和 TypeScript 迁移指南。

## 包含内容

### 1. ArkTS 语言规范 (spec/)

16 个官方语言规范文件，涵盖：

| 文件 | 说明 |
|------|------|
| `types.md` | 类型系统、预定义类型、类型推断 |
| `classes.md` | 类声明、访问修饰符、继承 |
| `expressions.md` | 运算符、优先级、表达式求值 |
| `statements.md` | 控制流、循环、try-catch |
| `generics.md` | 泛型类型和函数、约束 |
| `annotations.md` | 装饰器和元数据 |
| `modules.md` | Import/export、命名空间 |
| `lexical.md` | 标识符、关键字、字面量 |
| `names.md` | 声明、作用域、可见性 |
| `conversions.md` | 类型转换和上下文 |
| `interfaces.md` | 接口声明和实现 |
| `enums.md` | 枚举类型 |
| `errors.md` | 错误处理和 try 语句 |
| `concurrency.md` | Async/await、TaskPool |
| `stdlib.md` | 标准库 API |
| `experimental.md` | 实验性特性 (FixedArray、char 等) |

### 2. TypeScript 迁移指南 (cookbook/)

3 个迁移指南文件，包含：

| 文件 | 说明 |
|------|------|
| `index.md` | 迁移指南总览、设计原则 |
| `recipes.md` | 144+ 详细迁移食谱 |
| `compatibility.md` | TypeScript vs ArkTS 兼容性详情 |

## Skill 内容概览

### ArkTS 语言规范

- **类型系统**：预定义类型（byte, short, int, long, float, double, number, bigint）、特殊类型、联合类型、交集类型
- **面向对象**：类声明、接口、枚举、继承、访问修饰符、构造函数
- **表达式和运算符**：17 级优先级表、一元/二元/三元运算符
- **控制流**：if-else、switch、for/while/do-while、break/continue
- **泛型**：泛型函数、泛型类、类型约束、默认值
- **注解**：装饰器、元注解、注解处理器
- **模块系统**：import/export、命名空间
- **错误处理**：try-catch-finally、throw、Error 类
- **并发编程**：async/await、Promise、TaskPool、Workers
- **标准库**：console、Math、JSON、Array、Map、Set、Date
- **实验性特性**：FixedArray、char、函数重载等

### TypeScript 迁移指南

- **迁移概述**：为什么迁移、代码保持率（90-97%）
- **设计原则**：静态类型强制、对象布局固定、null 安全
- **144+ 迁移食谱**：
  - 语法相关：var → let、禁止 any、禁止 Symbol()
  - 类型系统：禁止调用签名、禁止 in 运算符
  - 模块系统：禁止 require、使用 ES6 import
  - 其他：不支持结构化类型、限制动态属性访问
- **兼容性详情**：29 个行为差异说明
  - 数值语义差异
  - Math.pow 差异
  - 数组赋值差异
  - 构造函数差异
  - 等...
