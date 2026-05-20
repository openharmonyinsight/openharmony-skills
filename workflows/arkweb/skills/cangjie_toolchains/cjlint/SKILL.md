---
name: cangjie-toolchains-cjlint
description: "仓颉静态检查工具 cjlint 使用说明。"
---

# 仓颉静态检查工具 cjlint Skill

## 1. 概述

`cjlint`（Cangjie Lint）是基于仓颉语言编程规范的静态检查工具，帮助识别不符合规范的代码问题和安全漏洞。

---

## 2. 基本用法

```bash
cjlint -f src/                              # 检查 src 目录
cjlint -f "dir1 dir2" -c . -m .             # 检查多个目录
cjlint -f src/ -r csv -o ./report           # 输出 CSV 报告
cjlint -f src/ -e "test/ generated/"        # 排除目录
```

> **注意**：`-f` 后指定的是 `.cj` 文件所在的 `src` 目录，不是单个文件。

---

## 3. 命令选项

| 选项 | 说明 |
|------|------|
| `-h` | 显示帮助信息 |
| `-v` | 显示版本号 |
| `-f <dir>` | 指定检查目录（多个目录用空格分隔，双引号包裹） |
| `-e <v1:v2:...>` | 排除文件/目录（支持正则） |
| `-o <path>` | 输出报告路径 |
| `-r [csv\|json]` | 报告格式（默认 json，须配合 `-o`） |
| `-c <path>` | config 目录路径 |
| `-m <path>` | modules 目录路径 |
| `--import-path <dir>` | 添加 `.cjo` 搜索路径 |

---

## 4. 告警屏蔽

### 4.1 规则级屏蔽
编辑 `config/cjlint_rule_list.json`，仅保留需要检查的规则：
```json
{
    "RuleList": ["G.FMT.01", "G.NAM.01", "G.VAR.01"]
}
```

编辑 `config/exclude_lists.json` 屏蔽特定告警：
```json
{
    "G.OTH.01": [
        {"path": "xxx/example.cj", "line": "42"}
    ]
}
```

### 4.2 源代码注释屏蔽

**单行屏蔽**：
```cangjie
func foo(a: Int64, b: Int64, c: Int64, d: Int64) { // cjlint-ignore !G.FUN.02 描述
    return a + b + c
}
```

**多行屏蔽**：
```cangjie
// cjlint-ignore -start !G.FUN.02 描述
func foo(a: Int64, b: Int64, c: Int64, d: Int64) {
    return a + b + c
}
// cjlint-ignore -end 描述
```

> `cjlint-ignore`、选项（`-start`/`-end`）和规则名须在同一行。

### 4.3 文件级屏蔽
```bash
cjlint -f src/ -e "dir1/ dir2/a.cj test*.cj"      # 命令行排除
```
或使用 `.cfg` 配置文件批量导入，默认配置文件为 `src/cjlint_file_exclude.cfg`。

---

## 5. 常用规则分类

### 5.1 命名规范（G.NAM）
| 规则 | 说明 |
|------|------|
| G.NAM.01 | 包名全小写，允许数字和下划线 |
| G.NAM.02 | 源文件名全小写加下划线 |
| G.NAM.03 | 类/接口/struct/枚举/类型别名采用大驼峰 |
| G.NAM.04 | 函数名小驼峰 |
| G.NAM.05 | `let` 全局变量和 `static let` 全大写 |

### 5.2 声明与函数（G.DCL/G.FUN）
| 规则 | 说明 |
|------|------|
| G.DCL.01 | 避免变量遮盖（shadow） |
| G.DCL.02 | public 变量/函数显式声明类型 |
| G.FUN.01 | 函数功能单一 |
| G.FUN.02 | 禁止未使用的参数 |

### 5.3 安全相关（G.CHK/G.CON/G.SEC/G.OTH）
| 规则 | 说明 |
|------|------|
| G.CHK.01 | 跨信任边界数据须校验 |
| G.CON.01 | 禁止暴露内部锁对象 |
| G.SEC.01 | 安全检查方法禁止声明为 `open` |
| G.OTH.01 | 禁止日志中保存敏感数据 |
| G.OTH.02 | 禁止硬编码敏感信息 |

### 5.4 默认不启用规则
- G.NAM.06（变量名小驼峰）、G.VAR.03（避免全局变量）、G.FMT.13（文件头版权注释）
- 需手动添加到 `cjlint_rule_list.json` 启用

---

## 6. 语法禁用检查

启用 G.SYN.01 后，在 `structural_rule_G_SYN_01.json` 中配置禁用的语法关键字：
```json
{
    "SyntaxKeyword": ["Import", "Spawn", "Foreign"]
}
```

支持的关键字：`Import`、`Let`、`Spawn`、`Synchronized`、`Main`、`MacroQuote`、`Foreign`、`While`、`Extend`、`Type`、`Operator`、`GlobalVariable`、`Enum`、`Class`、`Interface`、`Struct`、`Generic`、`When`、`Match`、`TryCatch`、`HigherOrderFunc`、`PrimitiveType`、`ContainerType`。
