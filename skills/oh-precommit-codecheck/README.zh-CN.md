# OpenHarmony 门禁预检查

在本地运行代码质量检查，覆盖部分 OpenHarmony 门禁 CI 检查项（CodeArts C/C++ 静态分析、版权头），并提供额外的 Python/Shell/GN 本地检查。提交前提前发现问题，减少门禁打回。

## 检查项

### 门禁检查项（与 OpenHarmony 门禁 CI 一致）

| 检查类型 | 工具 | 说明 |
|----------|------|------|
| 版权头 | 内置脚本 | 是否存在、年份是否包含当前年、C/C++ 首行是否为 `/**` |
| C/C++ 静态分析 | CodeArts Check (codecheck-ide-engine + 华为定制 clang-tidy) | 门禁同款引擎，clangtidy + secfinder + fixbot |

### 额外检查项（门禁不包含，本地增强）

| 检查类型 | 工具 | 说明 |
|----------|------|------|
| Python lint | pylint + flake8 | 代码规范检查，非门禁项 |
| Shell lint | shellcheck + bashate-mod-ds | 脚本规范检查，非门禁项 |
| GN 格式 | `gn format --dry-run` | 格式正确性检查，非门禁项 |

## 使用方法

在 Claude Code 中通过斜杠命令调用：

```
/oh-precommit-codecheck                    # 检查暂存区（git staged）文件
/oh-precommit-codecheck <commit>           # 检查指定提交涉及的文件
/oh-precommit-codecheck <file1> <file2>    # 检查指定文件
/oh-precommit-codecheck --fix              # 检查 + 自动修复
```

也可以用自然语言触发：
- "门禁检查"
- "门禁预检"
- "检查代码"
- "run codecheck"

代码修改完成后，AI 也会自动触发检查。

## 环境准备

### 自动安装（首次运行）

以下工具会在首次运行时自动从华为 OBS 下载安装到 `~/.codecheck-tools/`：

- **CodeArts codecheck-ide-engine** (~573MB) — C/C++ 静态分析引擎
- **华为定制 clang-tidy** — C/C++ 规则检查器

### 需手动安装

以下工具需要提前安装：

```bash
# Java 运行时（CodeArts 引擎依赖）
sudo apt install default-jre

# Python lint 工具
pip install pylint flake8 flake8-coding flake8-builtins pep8-naming flake8-executable flake8-bandit

# Shell lint 工具
sudo apt install shellcheck
pip install bashate-mod-ds

# GN 格式化工具（如需检查 BUILD.gn 文件）
# 通常随 OpenHarmony 编译环境一起安装
```

## 自动修复

使用 `--fix` 参数时，AI 会自动修复以下问题：

### 版权头
| 规则 | 修复方式 |
|------|----------|
| `no-copyright` 缺失版权头 | 添加完整 Apache 2.0 版权头 |
| `wrong-year` 年份不正确 | 更新年份范围（如 `2025` → `2025-2026`） |
| `wrong-comment-style` 注释风格错误 | C/C++ 文件首行改为 `/**` |

### C/C++ (CodeArts)
| 规则 | 修复方式 |
|------|----------|
| `G.FMT.11-CPP` 花括号 | 为单行 if/for/while/else 添加 `{}` |
| `G.NAM.03-CPP` 命名规范 | 修正变量/函数名 |
| `G.EXP.35-CPP` 空指针 | `NULL`/`0` → `nullptr` |
| `G.FUN.01-CPP` 参数 | 无法自动修复，报告给用户 |
| `G.CNS.02-CPP` 魔法数字 | 提取为 `constexpr` 常量 |

### Python
| 规则 | 修复方式 |
|------|----------|
| `C0304` 缺少末尾换行 | 添加换行符 |
| `C0305` 多余空行 | 删除多余末尾空行 |
| `C0321` 多语句同行 | 拆分到独立行 |
| `C0410` 多重导入 | 每行一个 import |
| `C0411` 导入顺序 | 标准库 → 第三方 → 本地 |

### Shell
| 规则 | 修复方式 |
|------|----------|
| `SC2086` 未引用变量 | 添加双引号 |
| `SC2164` 不安全 cd | 添加 `\|\| exit` |
| `SC2148` 缺失 shebang | 添加 `#!/usr/bin/env bash` |

### GN
- 运行 `gn format <file>` 全自动格式化

## 文件结构

```
oh-precommit-codecheck/
├── SKILL.md                  # Skill 定义（Claude Code 解析用）
├── README.zh-CN.md           # 中文说明文档（本文件）
└── scripts/
    ├── setup.sh              # 工具安装脚本
    ├── check.sh              # 主入口：分发文件到各检查器
    ├── check_copyright.sh    # 版权头检查
    ├── check_python.sh       # Python lint 检查
    └── check_shell.sh        # Shell lint 检查
```

## 当前局限性

### 语言覆盖

本 skill 当前仅对以下语言实现了检查：

| 语言 | 检查方式 | 状态 |
|------|----------|------|
| C/C++ | CodeArts 引擎 (codecheck-ide-engine) | 已实现 |
| Python | pylint + flake8 | 已实现 |
| Shell | shellcheck + bashate-mod-ds | 已实现 |
| GN | `gn format --dry-run` | 已实现 |
| Java | CodeArts 引擎（已有 202+ 规则） | **未接入** |
| JavaScript | CodeArts 引擎（已有 200 规则） | **未接入** |
| TypeScript | CodeArts 引擎（已有 194 规则） | **未接入** |
| ArkTS | CodeArts 引擎（已有 122 规则） | **未接入** |

> CodeArts 引擎本地已包含 Java/JS/TS/ArkTS 的规则集，后续可接入。

### C++ 规则覆盖

门禁 CI 的 C++ 检查包含约 163 条 G.* 规则，本地 CodeArts 引擎覆盖了其中约 **114 条 (70%)**。

缺失的 49 条主要是不带 `-CPP` 后缀的 C 语言规则（如 `G.FMT.01`、`G.VAR.01` 等），这些规则在引擎的 C 语言规则集中可能存在，但当前未针对 C++ 文件启用。

### 完全未覆盖的检查类别

| 类别 | 门禁规则数 | 说明 |
|------|------------|------|
| **WordsTool 敏感词** | ~200+ | 品牌词（Android/Google/iOS 等）、营销禁用词（最强/遥遥领先等）、政治敏感词。需自行实现，CodeArts 引擎不包含 |
| **OAT 开源合规** | ~10 | LICENSE 文件检查、README 文件检查、二进制文件检测、许可证兼容性 |
| **安全专项** | ~5 | 弱加密算法检测、不安全 IPSI 算法、Coverity 告警屏蔽方式检查 |
| **代码度量（C++）** | ~5 | 超大函数、超大源文件、超大头文件、超大圈复杂度、超大深度函数、冗余/重复代码 |

### 其他限制

- 首次运行需下载约 600MB 工具，请确保网络畅通
- 没有 `compile_commands.json` 时，C/C++ 检查可能遗漏部分上下文相关问题
- Python 检查使用 pylint + flake8 而非 CodeArts 引擎（门禁两种方式都有，当前采用 lint 工具方式）
- 本地通过不等于门禁一定通过，仅覆盖门禁检查的一个子集
