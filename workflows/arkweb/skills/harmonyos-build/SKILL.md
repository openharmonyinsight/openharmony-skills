---
name: harmonyos-build
description: 当需要构建鸿蒙应用项目时，使用此 Skill 执行构建流程。此 Skill
  包含完整的构建命令、构建流程说明、构建失败处理流程。构建脚本会自动执行依赖安装、仓颉预编译、资源生成、编译、打包等步骤。
descriptionZH: 当需要构建鸿蒙应用项目时，使用此 Skill 执行构建流程。此 Skill
  包含完整的构建命令、构建流程说明、构建失败处理流程。构建脚本会自动执行依赖安装、仓颉预编译、资源生成、编译、打包等步骤。
tags:
  - 鸿蒙
  - 构建
  - HarmonyOS
  - 仓颉
---

# 鸿蒙应用构建 Skill

## 目的

执行鸿蒙应用项目的完整构建流程，包括依赖安装、编译、打包等步骤。

## ⚠️ 脚本路径提醒

构建脚本位于 `skills/utils/scripts/build.py`

## 📄 读取 build-full.log 日志文件

**⚠️ 重要**：如果日志文件存在中文内容，确保使用正确的编码读取。

### 正确的读取方式

```bash
# ✅ 正确：使用 Bash 读取日志文件
Read(file_path: "path\\to\\build-full.log")

# 如果读取失败，可尝试使用 Bash 读取
Bash(command: 'type "path\\to\\build-full.log"', timeout: 30000)
```

### 如何判断是否为 UTF-16 编码

如果执行构建后尝试用 Read 工具读取 `build-full.log` 时出现以下错误：
```
Error: Cannot read binary file: C:\path\to\build-full.log
```

则说明文件是 UTF-16 编码，可以使用 `type` 命令读取。

## 🛠️ 构建命令

### 方式 1 - 在项目根目录执行（推荐）

```bash
# 1. 先复制脚本
cd "path/to/MyApplication10"
# Windows 环境直接复制 Python 脚本
Bash(command: 'copy ".\\skills\\utils\\scripts\\build.py" ".\\build.py"')

# 2. 在根目录执行构建，并把【完整 stdout+stderr】落到日志文件
#    注意：timeout=300000 只有 5 分钟，构建常常不够；建议至少 900000(15分钟) 或更大
Bash(
    command: 'cd "path\\to\\MyApplication" && python build.py > build-full.log 2>&1',
    timeout: 900000
)

# 3. 读取日志文件来分析
Read(file_path: "path\\to\\build-full.log")
```

## 📦 构建流程说明

`build.py` 脚本会自动执行以下步骤：
1. **install** - 安装依赖
2. **CangjiePreBuild** - 仓颉预编译
3. **GenerateCangjieResource** - 生成资源
4. **CompileCangjie** - 编译仓颉代码
5. **CompileArkTS** - 编译 ArkTS
6. **PackageHap** - 打包 HAP
7. **SignHap** - 签名（未配置时跳过）
8. **assembleHap** - 组装最终 HAP

## 🚨 构建失败处理

**关键原则**: 获得足够详细的错误信息是解决问题的前提。

> **⚠️ 重要提醒**：AI 在处理构建报错时，必须严格按照以下优先级流程处理，**不允许跳步或颠倒顺序**：
> 1. **Step 1**: 优先检查 Evolution.md 中的已知问题（使用 `harmonyos-evolution` skill）
> 2. **Step 2**: 如果 Evolution.md 中没有命中，再使用 `skills/cangjie-kernel` 下的基础仓颉技能（如 `array`、`string`、`function` 等）结合报错信息调试和修复代码
> 3. **Step 3**: 如果基础技能仍无法解决，再使用 `harmonyos-vec-retriever-guide` 进行 L1 RAG 代码片段/概念检索，辅助定位问题
> 4. **Step 4**: 如果 L1 仍无法解决，最后使用 `harmonyos-doc-search-guide` 进行本地文档搜索（L3 文档检索）
> 5. **更新规则**: 只有构建成功后才能将新问题添加到 Evolution.md
>
> **必须注意**：每一次鸿蒙项目构建报错，都要严格按照本 Skill 中的步骤依次处理，不能跳过任意阶段。

### 📋 第一步：获取完整的 build.py 输出

**⚠️ 强制要求**：在分析报错信息之前，必须先确保已获得完整的构建输出。

**执行流程**：
1. **捕获完整输出**：执行构建时将 stdout/stderr 写入 `build-full.log`，并设置足够大的 `timeout`（建议 `900000ms` 起步）
2. **读取日志文件**：构建结束后（成功/失败都一样），**必须**使用 Read 工具或 Bash 读取 `build-full.log`
3. **基于日志分析**：只基于 `build-full.log` 的内容分析报错（避免 UI 截断导致误判）

**示例执行模式**：
```bash
# 始终将完整输出落盘（stdout+stderr），避免 UI 截断
Bash(
  command: 'cd "path\\to\\DevEcoStudioProjects\\MyApplication" && python build.py > build-full.log 2>&1',
  timeout: 900000
)

# 读取日志文件
Read(file_path: "path\\to\\DevEcoStudioProjects\\MyApplication\\build-full.log")
```

**原则**: 只有在获得完整 build.py 输出后，才能进入下一步分析。

### 📋 第二步：评估报错信息充足性

在获得完整输出后，评估报错信息是否足够详细：

**❌ 报错信息不足的情况**（需要主动询问）：
- 只有简单的 "BUILD FAILED" 或 "error occurred"
- 缺少具体的错误行号和错误类型
- 缺少代码上下文（代码片段）
- 缺少宏展开后的错误信息（常见于 ArkUI 组件问题）

**✅ 报错信息充足的情况**：
- 包含完整的错误类型（如 `undefined identifier`、`invalid binary operator`）
- 或者包含具体的文件路径和行号
- 或者包含出错的代码片段
- 或者包含宏展开后的代码（问题跟踪时）

### 🔧 当报错信息不足时的处理

**⚠️ 重要前提**: 只有在已完整读取 build.py 输出log（包括截断文件）后，仍然发现信息不详细时，才建议使用 DevEco Studio。

**主动要求用户提供完整报错**：
```
已获取 build.py 的完整构建输出，但错误信息仍然不够详细，无法准确定位问题。

请在 DevEco Studio 中重新构建项目，然后将完整的错误信息复制给我。
DevEco Studio 会提供更详细的报错，包括：
- 具体的错误类型和描述
- 出错的代码位置（文件:行号）
- 宏展开后的代码（对于 ArkUI 组件问题）
- 相关的类型信息

请在 DevEco Studio 中构建后将完整报错贴出来。
```

### 🔍 当获得足够报错信息时的处理

> **🚨 AI 必须严格遵守**：以下优先级流程是处理构建报错的标准流程，不可跳过或颠倒顺序！

**严格按照以下优先级处理**：

```
获得详细报错信息
    ↓
Step 1: 检查 Evolution.md (优先级最高) - 使用 harmonyos-evolution skill
    ↓
    ├─ 找到相同问题 → 应用已验证的解决方案 → 重新构建
    │
    └─ 未找到/无法解决 → 继续 Step 2
         ↓
Step 2: 使用 skills/cangjie-kernel 中的基础仓颉技能调试代码
    ↓
    ├─ 通过代码修改解决问题 → 重新构建 → 构建成功则更新 Evolution.md
    │
    └─ 仍无法解决/缺乏思路 → 继续 Step 3
         ↓
Step 3: L1 混合搜索 - 使用 harmonyos-vec-retriever-guide这个skill
    ↓
    ├─ 找到解决方案 → 修复代码 → 重新构建 → 构建成功则更新 Evolution.md               
    │
    └─ 仍无法解决/缺乏思路 → 继续 Step 4
         ↓
Step 4: L3 本地文档搜索 - 使用 harmonyos-doc-search-guide这个skill
    ↓
    ├─ 找到解决方案 → 修复代码 → 重新构建 → 构建成功则更新 Evolution.md
    │
    │                             ↓
    │                        构建失败则重新判断报错信息是否充足，重新修正方案
    │
    └─ 未找到 → 明确告知"该功能可能不支持"
```

**Step 1 - 检查 Evolution.md 的执行要点**：
1. 使用 `harmonyos-evolution` skill 读取 `Evolution.md` 文件
2. 搜索报错中的关键词（如错误类型、相关API名称）
3. 对比错误描述是否匹配
4. 如果匹配，直接应用已记录的解决方案
5. **不要再进行 L3 搜索**，直接修复

**Step 2 - 使用 `skills/` 调试的执行要点**：
1. 仅在 Evolution.md 中找不到相关问题后才进行
2. 结合 `build-full.log` 中的报错信息，优先调用 `skills/cangjie-kernel` 下的基础仓颉技能（如 `array`、`string`、`function`、`std` 等），分析类型错误、语法错误和标准库用法
3. 根据分析结果修改代码并重新构建
4. 如果多次尝试仍无法解决或错误涉及鸿蒙 UI / 平台特性，再进入 Step 3（L3 本地文档搜索）

**Step 3 - L1 搜索的执行要点**：
1. 仅在 step2 调试都无法解决问题后才进行
2. 使用 `harmonyos-vec-retriever-guide` 指导使用的ask_cangjie.py脚本查询进行 L1 RAG 代码片段/概念检索，辅助定位问题
4. **只有在构建成功后，才将新问题添加到 Evolution.md**（使用 `harmonyos-evolution` skill）
5. 如果构建失败，说明方案错误，不能记录，需要重新根据报错信息寻找解决方案

**Step 4 - L3 搜索的执行要点**：
1. 仅在 Evolution.md 和 `skills/` 调试都无法解决问题后才进行
2. 使用 `harmonyos-doc-search-guide` skill 根据错误类型选择合适的搜索路径
3. 修复代码并重新构建
4. **只有在构建成功后，才将新问题添加到 Evolution.md**（使用 `harmonyos-evolution` skill）
5. 如果构建失败，说明方案错误，不能记录，需要重新根据报错信息寻找解决方案

**示例**：
```
用户报错: error: undeclared identifier 'toUInt32'
↓
Step 1: 检查 Evolution.md（使用 harmonyos-evolution skill）
    ✓ 搜索关键词: "toUInt32", "类型转换", "未定义标识符"
    ✓ 找到记录 #14: 类型转换方法不存在
    ✓ 解决方案: 使用 UInt32(e) 替代 ch.toUInt32()
    ✓ 直接应用修复，跳过 L3 搜索
↓
重新构建 → ✅ BUILD SUCCESSFUL
✓ 构建成功，方案验证有效
```

**新问题处理示例**（含失败情况）：
```
用户报错: error: invalid binary operator '==' on type 'UInt8' and 'Rune'
↓
Step 1: 检查 Evolution.md（使用 harmonyos-evolution skill）
    ✗ 搜索关键词 "UInt8", "Rune", "类型不匹配" - 未找到匹配记录
↓
Step 2: L3 本地文档搜索（使用 harmonyos-doc-search-guide skill）
    ✓ 搜索结果: String下标返回UInt8，不能与Rune直接比较
    ✓ 解决方案: 使用ASCII码值比较 (ch == 45u8)
↓
修复代码 → 重新构建
    ├─ 构建 ✅ 成功 → 将问题添加到 Evolution.md（使用 harmonyos-evolution skill）
    └─ 构建 ❌ 失败 → 方案错误，不能记录，重新寻找解决方案
```

## ✅ 构建成功标识

- 出现 `BUILD SUCCESSFUL` 表示构建成功
- 警告信息通常不影响构建（除非要签名时会提示缺少签名配置）

## 📝 构建成功后的总结要求

**⚠️ 重要原则: 只有在构建成功后才能更新 Evolution.md**

- 修复方案必须先验证（构建成功）
- 构建失败的方案不能记录（说明方案错误）
- 用户自行构建成功后，才能确认问题解决有效

**每次构建成功后，必须执行以下操作**：
1. 使用 `harmonyos-evolution` skill 将本次开发过程中遇到的**重难点**整理成几点
2. 写入 skills 目录下的 `Evolution.md` 文件（即 `skills/utils/Evolution.md`）
3. 记录内容包括：问题描述、错误代码、原因分析、解决方案、正确代码示例

> **重要**: Evolution.md 位于 skills 目录中，这样当技能迁移到其他项目时，历史问题记录也会一起迁移。

## 工作流程

1. **需求分析**（已完成）- 使用 `harmonyos-requirement-analysis` skill
2. **使用cangjie-kernel**（已完成）- 先使用 `skills/cangjie-kernel` 中的仓颉语言 skills
3. **L1 查询**（已完成）- 如需进一步查询，使用 `harmonyos-vec-retriever-guide` skill
4. **L3 查询**（已完成）- 如需本地文档搜索，使用 `harmonyos-doc-search-guide` skill
5. **构建**（本 Skill）- 使用本 Skill 进行项目构建
6. **迭代进化** - 使用 `harmonyos-evolution` skill 记录和解决问题

## ⚠️ 构建脚本执行补充说明

**正确执行 build.py 的完整流程**：

1. **复制脚本到项目根目录**（必须执行）：
   ```bash
   copy .\skills\utils\scripts\build.py .\build.py
   ```

2. **在项目根目录执行构建**：
   ```bash
   cd "path\to\DevEcoStudioProjects\MyApplication"  # 确保在项目根目录
   python build.py
   ```

3. **获取完整的构建输出**（关键步骤）：
    - 使用 Bash 工具时必须设置足够大的 `timeout`（`300000` 只有 5 分钟，常常不够；建议 `900000` 起步）
    - 不要依赖 UI 展示（会出现 `... +N lines` / 输出被截断），必须把 stdout/stderr 写入日志文件
    - 使用 Read 工具读取日志文件内容（这才是完整输出）

**错误示例**：
   - 在 `scripts/` 目录下执行构建（❌ 错误）
   - 未复制脚本直接执行（❌ 错误）
   - 只获取部分输出就分析（❌ 错误）

**正确示例**：
```bash
# 1. 先复制脚本
cd "path\to\DevEcoStudioProjects\MyApplication"
copy ".\skills\utils\scripts\build.py" ".\build.py"

# 2. 在根目录执行构建，并把【完整 stdout+stderr】落到日志文件
#    注意：timeout=300000 只有 5 分钟，构建常常不够；建议至少 900000(15分钟) 或更大
Bash(
    command: 'cd "path\\to\\DevEcoStudioProjects\\MyApplication" && python build.py > build-full.log 2>&1',
    timeout: 900000
)

# 3. 读取日志文件来做分析
Read(file_path: "path\\to\\DevEcoStudioProjects\\MyApplication\\build-full.log")
```

**重要！兼容性配置**：务必将`./entry/build-profile.json5` 文件中的""buildOption"字段配置正确，确保包含对鸿蒙构建环境的兼容性设置，严格按照如下所示配置：
```
"buildOption": {
    "cangjieOptions": {
      "abiFilters": ["arm64-v8a", "arm64-v8a", "x86_64"],
      "path": "./cjpm.toml"
    },
```
