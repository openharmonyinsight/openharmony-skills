# ArkTS Static Language Specification Skill

完整的 ArkTS 静态语言规范参考技能，包含官方规范和 TypeScript 迁移指南。

## ⚠️ 使用原则（重要）

在使用 oh-oh-xts-generator-template-template skill 生成 ArkTS 静态 XTS 用例并参考 arkts-static-spec 时，**必须严格遵守**以下原则：

1. **严格按照 skill 文档内容回答**
   - 所有回答必须基于 spec/ 和 cookbook/ 目录下的文档内容
   - 不添加文档之外的假设或推断

2. **明确标注文档未说明的内容**
   - 如果 skill 文档中没有明确说明某个特性，必须在回答中标注：
     - **"⚠️ skill 文档未明确说明，待使用者自行确认"**
   - 不要基于 TypeScript 或其他语言的特性进行假设

3. **将 ArkTS 视为独立的静态语言**
   - ArkTS 是一个独立的静态语言，**不是** TypeScript 的超集
   - 不要假设 TypeScript 的特性在 ArkTS 中都支持
   - 以 ArkTS 官方规范为准，不以 TypeScript 语法为准

4. **文档来源优先级**
   - ArkTS 官方规范文档（spec/ 目录）为最高优先级
   - TypeScript 迁移指南（cookbook/ 目录）作为参考
   - 未在文档中明确说明的特性，视为不确定，需明确标注

---

## 📦 包含内容

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

## 🚀 安装方法

### 方法 1：手动安装（推荐）

1. **解压文件**
   - Windows: 右键点击 `arkts-static-spec.zip` → 解压
   - Linux/Mac: `tar -xzf arkts-static-spec.tar.gz`

2. **复制到技能目录**
   ```bash
   # Windows
   xcopy arkts-static-spec %USERPROFILE%\.claude\skills\ /E /I /Y

   # Linux/Mac
   cp -r arkts-static-spec ~/.claude/skills/
   ```

3. **验证安装**
   ```
   启动 Claude Code，使用 /arkts-static-spec 命令
   ```

### 方法 2：自动安装脚本

创建安装脚本 `install.bat`（Windows）或 `install.sh`（Linux/Mac）：

#### Windows (install.bat)
```batch
@echo off
echo Installing arkts-static-spec skill...

REM 检查 Claude skills 目录
if not exist "%USERPROFILE%\.claude\skills" (
    mkdir "%USERPROFILE%\.claude\skills"
)

REM 复制 skill
xcopy arkts-static-spec "%USERPROFILE%\.claude\skills\arkts-static-spec\" /E /I /Y

echo.
echo Installation completed!
echo Please restart Claude Code to use the skill.
pause
```

#### Linux/Mac (install.sh)
```bash
#!/bin/bash
echo "Installing arkts-static-spec skill..."

# 检查 Claude skills 目录
mkdir -p ~/.claude/skills

# 复制 skill
cp -r arkts-static-spec ~/.claude/skills/

echo ""
echo "Installation completed!"
echo "Please restart Claude Code to use the skill."
```

使用方法：
```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh
./install.sh
```

## 📖 使用方法

### 基本用法

安装后，在 Claude Code 中使用：

```
/arkts-static-spec 你的问题
```

### 示例查询

```
# 查询类型系统
/arkts-static-spec ArkTS 的 int 和 number 有什么区别

# 查询类定义
/arkts-static-spec 如何定义一个 ArkTS 类

# 查询 TypeScript 迁移
/arkts-static-spec 如何在 ArkTS 中替代 TypeScript 的 var

# 查询实验性特性
/arkts-static-spec FixedArray 怎么使用

# 查询类型转换
/arkts-static-spec ArkTS 中的类型转换规则
```

## 📋 Skill 内容概览

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
  - 等等...

## 🎯 适用场景

此 skill 适用于以下场景：

1. **编写 ArkTS 代码**：查询语法、类型、最佳实践
2. **分析 ArkTS 代码**：理解代码结构、类型系统
3. **TypeScript 迁移**：了解如何将 TS 代码迁移到 ArkTS
4. **调试编译问题**：查找错误原因和解决方案
5. **学习 ArkTS**：系统地学习 ArkTS 语言特性
6. **创建开发工具**：为 ArkTS 开发编译器、IDE 插件等

## 📊 文件统计

| 类别 | 文件数 | 说明 |
|------|--------|------|
| spec/ | 16 | ArkTS 语言规范文件 |
| cookbook/ | 3 | TypeScript 迁移指南 |
| SKILL.md | 1 | 主索引文件 |
| **总计** | **20** | Markdown 文件 |

## 🔧 系统要求

- **Claude Code** 或支持自定义技能的 Claude 应用
- **操作系统**：Windows、Linux、macOS
- **磁盘空间**：约 100 KB（解压后）

## 📝 版本信息

- **名称**：arkts-static-spec
- **版本**：1.0.0
- **创建日期**：2025-02-03
- **基于**：ArkTS 官方规范和 Cookbook
- **原始文档**：
  - `D:\arkcompiler\runtime_core\static_core\plugins\ets\doc\spec\`
  - `D:\arkcompiler\runtime_core\static_core\plugins\ets\doc\cookbook\`

## 🤝 贡献和反馈

如有问题或建议，请参考原始 ArkTS 规范文档：
- OpenHarmony ArkTS 规范
- ArkCompiler 项目文档

## 📄 许可证

基于 Apache License 2.0，与 ArkTS 官方规范保持一致。

---

**注意**：此 skill 基于 ArkTS 官方规范创建，仅供学习和参考使用。实际开发请以官方最新规范为准。
