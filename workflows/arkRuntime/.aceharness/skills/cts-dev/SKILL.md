---
name: cts-dev
description: ArkTS前端编译器(ets2panda)CTS测试修复开发助手。用于CTS测试用例未通过时的缺陷定位、代码修复、测试验证全流程。适用场景：(1)CTS测试用例失败需要定位根因并修复 (2)前端编译器parser/checker/lowering模块的功能开发与缺陷修复 (3)编译构建、测试运行、回归验证 (4)代码评审与重构 (5)代码修改报告生成。涉及仓库为ets_frontend和runtime_core，编译器代码路径为ets_frontend/ets2panda。本技能是spec-test-analyzer的下游技能，接收spec分析报告后执行修复。当处理CTS用例失败时，必须先使用spec-test-analyzer技能生成spec分析报告，再使用本技能进行修复。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: compiler
  capability: cts-development
  version: 0.1.0
  status: draft
---

# CTS开发修复技能

本技能提供ArkTS前端编译器(ets2panda)CTS测试用例修复的完整开发流程，涵盖问题定位、代码修改、测试验证和上库标准。

## 前置技能：Spec分析

**当处理CTS用例失败时，必须先使用 `spec-test-analyzer` 技能**，对失败用例进行spec规则召回和差异分析，生成「CTS缺陷Spec分析报告」。

本技能的修复工作基于该报告进行：
1. 报告中的「责任模块判定」→ 确定修改哪个模块
2. 报告中的「Spec与编译器行为差异分析」→ 理解根因
3. 报告中的「补充测试场景」→ 确保修复覆盖边界条件
4. 报告中的「Spec原文」→ 修复依据（spec-first原则）

如果尚未生成Spec分析报告，请先触发 `spec-test-analyzer` 技能。

## 重要约定

- **项目根目录**: 包含`runtime_core/`和`ets_frontend/`的目录（脚本自动检测，也可通过`ARK_ROOT_DIR`环境变量指定）
- **编译器代码路径**: `ets_frontend/ets2panda`（不是`ets_frontend/es2panda`）
- **涉及仓库**: `ets_frontend` 和 `runtime_core`
- **编译命令执行路径**: `runtime_core/static_core/`
- **构建目标**: `es2panda`
- **构建目录**: 自动检测（优先级：`ARK_BUILD_DIR`环境变量 > `build_release` > `out`）
- **脚本位置**: 所有脚本使用绝对路径，通过`common.sh`自动检测项目根目录，**可在任意目录执行**

### 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `ARK_ROOT_DIR` | 项目根目录（含runtime_core/和ets_frontend/） | `/home/user/arkcompile` |
| `ARK_BUILD_DIR` | 构建输出目录（绝对路径） | `/home/user/arkcompile/runtime_core/static_core/out` |

### 编译模式

所有编译命令在 `runtime_core/static_core/` 目录下执行：

```bash
# Release模式
cmake -B out -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain/host_clang_default.cmake -GNinja . && cmake --build out

# Debug模式
cmake -B out -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain/host_clang_default.cmake -GNinja . && cmake --build out

# Debug-ASAN模式
cmake -B cmake-build-debug -DPANDA_ENABLE_ADDRESS_SANITIZER=true -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain/host_clang_default.cmake -GNinja .
```

## 关键目录

| 路径 | 说明 |
|------|------|
| `ets_frontend/ets2panda` | 编译器实现代码 |
| `ets_frontend/ets2panda/test/` | 编译器测试用例（ast/compiler/ets/） |
| `runtime_core/static_core/` | 测试命令执行根目录、编译根目录 |
| `runtime_core/static_core/plugins/ets/tests/ets-templates/` | CTS测试用例模板 |
| `runtime_core/static_core/plugins/ets/doc/spec/` | ArkTS语言规范文档 |
| `runtime_core/static_core/tests/tests-u-runner/` | 测试运行器 |
| `mktemp` 生成的临时目录 | 当前运行渲染后的CTS用例代码目录（由 `runtime.sh` 自动创建和清理） |

## 开发流程

### 阶段零：准备基线（异步后台）

后台异步执行CTS全量测试保存基线结果，后续回归验证时对比：

```bash
SCRIPTS_DIR="...scripts目录绝对路径..."
$SCRIPTS_DIR/cts2.sh > baseline.txt 2>&1 &
```

### 阶段一：Spec分析（前置，由spec-test-analyzer执行）

> 本步骤由 `spec-test-analyzer` 技能完成，不在此技能内执行。
> 如果用户直接提供了失败用例但未附带Spec分析报告，应先触发 `spec-test-analyzer` 生成报告。

输入：失败的CTS用例 + 错误信息
输出：**CTS缺陷Spec分析报告**（包含spec规则召回、行为差异分析、责任模块判定）

### 阶段二：问题定位与修复

1. **阅读Spec分析报告**: 获取 `spec-test-analyzer` 输出的CTS缺陷Spec分析报告，重点关注：
   - 「责任模块判定」→ 确定是parser/checker/lowering中的哪个模块
   - 「Spec与编译器行为差异分析」→ 理解期望行为vs实际行为的gap
   - 「建议修复方向」→ 获取修复思路
2. **复现问题**: 使用对应测试脚本运行失败用例，确认问题可复现
   ```bash
   SCRIPTS_DIR="...scripts目录绝对路径..."
   # CTS测试用例（支持 --test-file 或 --filter）
   $SCRIPTS_DIR/cts2.sh --test-file <用例路径>
   $SCRIPTS_DIR/cts2.sh --filter "*17.experimental_features/13.adding_functionality_to_existing_types*"
   # astchecker测试
   $SCRIPTS_DIR/astcheck.sh --test-file <用例路径>
   # recheck测试
   $SCRIPTS_DIR/recheck.sh --test-file <用例路径>
   # 单元测试
   $SCRIPTS_DIR/ut.sh --test-file <用例路径>
   ```
3. **结合Spec报告定位根因**: 将Spec报告中的差异点映射到具体代码位置
   - Parser差异 → 查看 `parser/ETSParser*.cpp`
   - Checker差异 → 查看 `checker/ETSAnalyzer*.cpp` 和 `checker/ets/*.cpp`
   - Lowering差异 → 查看 `compiler/lowering/ets/*Lowering.cpp`
4. **确定修改范围**: 明确需要修改的文件和函数，参考 `reference/architecture.md`
5. **修改代码**: 根据根因分析修改对应模块代码，严格遵循代码规范
6. **增量编译**:
   ```bash
   $SCRIPTS_DIR/build_diff.sh
   ```
7. **确认目标用例通过**: 反复修改+编译+测试，直到所有目标用例通过

### 阶段三：定向回归验证

确保修复的特定CTS子类用例全部通过（每步通过后才继续下一步）：

```bash
SCRIPTS_DIR="...scripts目录绝对路径..."

# 1. 目标CTS子类测试（如：adding_functionality_to_existing_types）
$SCRIPTS_DIR/cts2.sh --filter "*17.experimental_features/13.adding_functionality_to_existing_types*"

# 2. ets-runtime测试（约8分钟）
$SCRIPTS_DIR/runtime.sh

# 3. astchecker测试（约10分钟）
$SCRIPTS_DIR/astcheck.sh
```

### 阶段四：全量回归验证

按顺序执行全量回归测试：

```bash
SCRIPTS_DIR="...scripts目录绝对路径..."

# 1. CTS全量测试（约136分钟）
$SCRIPTS_DIR/cts2.sh

# 2. ets-func-tests（约30分钟）
# 直接在 static_core 下执行
cd $ARK_ROOT_DIR/runtime_core/static_core
tests/tests-u-runner/runner.sh --ets-func-tests --show-progress --build-dir out --processes=all

# 3. parser测试（约8分钟）
$SCRIPTS_DIR/parser.sh
```

### 阶段五：代码格式检查

在项目根目录（`runtime_core/`和`ets_frontend/`同级目录）执行格式检查：

```bash
SCRIPTS_DIR="...scripts目录绝对路径..."

# 检查所有仓库的修改文件格式（默认检查ets_frontend和runtime_core）
$SCRIPTS_DIR/format.sh

# 只检查ets_frontend
$SCRIPTS_DIR/format.sh --repo ets_frontend

# 只检查runtime_core
$SCRIPTS_DIR/format.sh --repo runtime_core

# 检查最后一次提交的文件
$SCRIPTS_DIR/format.sh log

# 检查最后一次提交，仅ets_frontend
$SCRIPTS_DIR/format.sh --repo ets_frontend log
```

根据检查结果修改代码，反复执行直到格式检查通过。

### 阶段六：生成代码修改报告

所有测试通过后，生成代码修改报告（模板见下方）。

## 测试脚本速查

所有脚本位于 `scripts/` 目录，**使用绝对路径，可在任意目录执行**。
所有脚本通过 `common.sh` 自动检测项目根目录（向上查找含`runtime_core/`和`ets_frontend/`的目录）。

| 脚本 | 用途 | 参数 |
|------|------|------|
| `build_diff.sh` | 增量编译es2panda | 无 |
| `build.sh` | 全量编译 | 无 |
| `install_build.sh` | 首次安装构建 | 无 |
| `cts2.sh` | CTS测试 | `--test-file <路径>` 或 `--filter <模式>` |
| `astcheck.sh` | astchecker测试 | `--test-file <路径>` |
| `parser.sh` | parser测试 | `--test-file <路径>` |
| `recheck.sh` | recheck测试 | `--test-file <路径>` |
| `runtime.sh` | ets-runtime测试 | 无 |
| `ut.sh` | 单元测试 | `--test-file <路径>` |
| `declgen.sh` | 声明生成测试 | `--test-file <路径>` |
| `runets.sh` | 编译运行单个ets文件 | `<文件路径>` |
| `style.sh` | ninja clang-force-format | 无 |
| `format.sh` | 代码格式检查（clang-format+clang-tidy） | `--repo <仓库>` `log` |
| `all_with_build.sh` | 构建后运行全部测试 | 无 |
| `test.sh` | 旧版全套测试（含format） | 无 |
| `common.sh` | 共享函数（自动检测路径） | （被其他脚本source） |

## 代码规范

### 命名规范

- 新增函数命名不能过长
- 函数首个单词首字母大写，首个单词为动词（如`GetTypeFor...`、`Check...`、`Resolve...`）
- 不能有魔术数字、魔术字符串，必须定义为命名常量

### 复杂度规范

- 函数圈复杂度不超过10
- 代码缩进层级不超过5
- 单个函数不能超过49行
- 函数参数个数不超过5个
- 新增代码存在重复代码时要提取为函数

### 模块约束

- **Checker**: 不改AST形状、不新建AST节点，仅修改语义元数据
- **Parser**: 仅做语法解析（token→AST），不报告语义错误
- **Lowering**: AST→AST变换，新建节点后必须re-bind/re-check
- 详细模块约束见 `reference/architecture.md`

### 类型系统规则

- 使用`TypeRelation` API（`IsSupertypeOf`、`IsIdenticalTo`）进行类型逻辑判断
- 不硬编码类型名（如`"escompat.Record"`），不用指针比较类型
- 不引入新的状态标志（`CheckerStatus`、`AstNodeFlags`等）
- 不依赖`ToString()`稳定性做语义判断，应使用类型结构/TypeRelation

### 通用工程规范

- 不使用显式`new`/`delete`管理内存
- 优先使用文件级`static`/私有辅助函数，不膨胀公共接口
- 使用arena allocation管理编译器对象
- Linux和Windows文本文件编码格式可能不同，注意换行符差异导致的crash

## 验收标准

### 必须通过项

- [ ] 修复命令中指定的所有失败用例均通过
- [ ] parser测试套无新增失败
- [ ] astchecker测试套无新增失败
- [ ] recheck测试套无新增失败
- [ ] ets-runtime测试套无新增失败
- [ ] CTS全量测试无回归（与基线对比无新增失败）
- [ ] 编译构建无error无warning
- [ ] 代码格式检查通过（format.sh）

### 代码质量项

- [ ] 圈复杂度 ≤ 10
- [ ] 函数行数 ≤ 49行
- [ ] 缩进层级 ≤ 5
- [ ] 无魔术数字/字符串
- [ ] 无冗余/重复代码
- [ ] 符合命名规范

### Spec一致性项

- [ ] 行为符合最新技术预览规范（spec-first）
- [ ] 不引入spec之外的行为
- [ ] 不移除现有assertion

## 上库标准

### Commit Message格式

```
[CTS] 简短描述（首行不超过50字符）

Issue: https://gitcode.com/openharmony/arkcompiler_runtime_core/issues/<编号>
Co-Authored-By: Agent
Signed-off-by: <姓名> <邮箱>
```

- 首行和正文之间有空行
- 首行字符数不超过50
- 关联Issue链接

### 必须包含

- 修复行为的对应测试用例
- spec规范依据（如涉及）
- 代码修改报告

## 代码修改报告

每次修复完成后，必须生成代码修改报告。报告中"Spec依据"部分应引用 `spec-test-analyzer` 输出的CTS缺陷Spec分析报告中的具体spec章节和规则。

模板如下：

```markdown
# 代码修改报告

## 一、问题根因分析

### 1.1 问题描述
<!-- 描述CTS测试失败的现象：哪个用例、什么错误信息 -->

### 1.2 根因定位
<!-- 定位到具体模块（parser/checker/lowering）和具体函数/文件 -->
- **涉及模块**:
- **根因文件**:
- **根因函数**:
- **根因类型**: （逻辑错误 / 缺失功能 / 边界条件未处理 / spec实现不一致）

### 1.3 根因详细分析
<!-- 解释为什么会产生这个问题，从spec或编译器架构角度分析 -->

## 二、架构设计

### 2.1 修改方案
<!-- 描述修复方案的设计思路 -->

### 2.2 修改文件列表
| 文件路径 | 修改类型 | 说明 |
|----------|----------|------|
| | 新增/修改/删除 | |

### 2.3 模块影响分析
- **Parser影响**:
- **Checker影响**:
- **Lowering影响**:
- **其他模块影响**:

### 2.4 新增函数说明
| 函数签名 | 所在文件 | 职责 |
|----------|----------|------|
| | | |

## 三、影响范围

### 3.1 功能影响
<!-- 本次修改影响哪些语言特性/语法规则 -->

### 3.2 测试影响
- **新增测试用例**:
- **修改测试用例**:
- **预期影响的CTS章节**:

### 3.3 兼容性影响
<!-- 是否影响已有代码的编译行为 -->

### 3.4 回归测试结果
| 测试套 | 修复前结果 | 修复后结果 | 是否有回归 |
|--------|-----------|-----------|-----------|
| parser | | | |
| astchecker | | | |
| recheck | | | |
| ets-runtime | | | |
| CTS全量 | | | |

## 四、Spec依据
<!-- 引用spec-test-analyzer输出的CTS缺陷Spec分析报告中的具体spec章节和规则 -->
<!-- 包括：Spec章节编号、规则描述、原文引用 -->
<!-- 来源报告路径：{spec-test-analyzer输出的报告路径} -->
```

## 参考资源

- **前置技能**: [`../spec-test-analyzer/SKILL.md`](../spec-test-analyzer/SKILL.md) — Spec规则召回和分析，CTS修复的必经前置步骤
- **模块架构**: `reference/architecture.md` — checker/parser/lowering三大模块的详细架构知识
- **测试脚本**: `scripts/` — 所有可执行的测试和构建脚本（绝对路径，自动检测项目根目录）
- **共享函数**: `scripts/common.sh` — 路径自动检测逻辑（`detect_root_dir`、`detect_build_dir`）
- **Spec规范**: `runtime_core/static_core/plugins/ets/doc/spec/` — ArkTS语言规范
