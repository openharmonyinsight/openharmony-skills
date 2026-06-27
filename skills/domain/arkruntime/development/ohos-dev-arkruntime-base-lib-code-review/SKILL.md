---
name: ohos-dev-arkruntime-base-lib-code-review
description: "审查基础库仓库（arkcompiler_runtime_core、third_party_musl、commonlibrary_c_utils 等）的 C/C++/ArkTS 代码变更，关注代码质量、语言特有问题和领域专属问题。适用于审查基础库 PR、检查信号安全性、验证 libc 符号导出兼容性、或对基础库代码进行通用审查。关键词：base library, code review, PR review, signal-safe, libc.map, 符号导出, 接口兼容性, musl, c_utils, runtime_core, 基础库, 代码审查, 代码review, 信号安全, ABI兼容"
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkruntime
  capability: code-review
  version: "0.1.0"
  status: draft
  tags:
    - base-library
    - code-review
    - signal-safety
    - abi-compatibility
---

# Base Library Code Review

## Task and Boundaries

审查基础库仓库的代码变更，重点关注 C/C++/ArkTS 代码质量、语言特有陷阱和领域专属问题。当前支持以下仓库，并提供对应的领域专属知识检查：

| 仓库名称 | Gitcode 地址 |
|---|---|
| arkcompiler_runtime_core | https://gitcode.com/openharmony/arkcompiler_runtime_core |
| third_party_musl | https://gitcode.com/openharmony/third_party_musl |
| commonlibrary_c_utils | https://gitcode.com/openharmony/commonlibrary_c_utils |

其他仓库也可以使用本 skill 进行审查，但不会执行仓库专属的领域知识检查。

**仅执行通用检查的场景：**
- 不包含 C/C++/ArkTS 代码变更的 PR（如仅文档、配置变更），无需执行语言专属和仓库专属检查

## Trigger Signals

- 用户要求审查基础库 PR（提供仓库名 + PR 号）
- 用户提及 "review" + 任意基础库名称（musl、c_utils、runtime_core 等）
- 用户提及 "基础库 review"、"基础库代码审查"、"代码审查"

## Initial Checks

1. **确定目标仓库**：解析用户输入识别仓库。仓库名支持模糊匹配（如 "musl" → third_party_musl，"runtime_core" → arkcompiler_runtime_core，"c_utils" → commonlibrary_c_utils）。若仓库不在支持列表中，仅执行通用审查（跳过第 4 步）。
2. **获取 PR 号**：从用户输入中确认 PR 编号。
3. **确认审查范围**：若未指定，默认审查 PR 中的所有变更文件。

## Execution Strategy

### Step 1: 拉取 PR 分支并收集上下文

按照 `ohos-dev-gitcode-pr-review` skill 的 Workflow Step 1-2 执行 PR 解析与远程上下文收集。该 skill 提供了标准化的 PR 引用规范化、`oh-gc` 命令调用和上下文 artifact 生成流程。

主要步骤概要：

1. **解析 PR 引用**：使用 `scripts/normalize_pr_ref.py` 规范化用户输入的 PR 号或 URL，提取 PR 编号和 `OWNER/REPO`。
2. **收集远程上下文**：使用 `scripts/collect_pr_context.py` 拉取 PR 的 diff、view、comments 等信息，生成 `summary.json`、`pr-diff.txt`、`pr-view.json` 等 artifact。

详细命令和参数请参考 `ohos-dev-gitcode-pr-review` skill 的 Quick Flow 章节。

**特别注意**：仅对这个 PR 分支涉及到的提交代码进行审查（一般情况下只有最新的一笔提交），避免检查了根本次 PR 无关的提交。

### Step 2: AI 通用代码审查

对所有变更文件进行全面的 AI 代码审查，不限定审查内容，包括但不限于：

- 逻辑错误和潜在缺陷
- 内存管理问题（内存泄漏、释放后使用、双重释放、缓冲区溢出）
- 错误处理的完整性
- 代码风格与可读性
- 线程安全与并发问题
- 性能问题
- API 使用正确性

按文件组织审查结果，附带行号引用和严重程度（严重 / 警告 / 建议）。

### Step 3: 语言补充知识审查

根据变更文件的编程语言，逐项检查对应语言知识清单中的每一项。

#### C/C++ 语言检查清单

| # | 检查项 | 说明 |
|---|---|---|
| 1 | 信号安全性 | 在信号处理函数中调用的函数必须是异步信号安全的。仅有限的 POSIX 函数是信号安全的（如 `write`、`_exit`、`sigprocmask`）。在信号处理函数中使用非信号安全函数（如 `printf`、`malloc`、`free`、`pthread_mutex_lock`）属于未定义行为。详见 `references/c-cpp-checklist-details.md` 的「信号安全性」章节。 |
| 2 | 接口配对使用规范 | C/C++ 标准库中许多接口需要成对使用，用错释放方式会导致未定义行为或资源泄漏。详见 `references/c-cpp-checklist-details.md` 的「接口配对使用规范」章节。 |
| 3 | 错误处理与异常捕获 | 必须正确处理接口返回值、errno 和 C++ 异常，不得忽略错误或以粗暴方式终止程序。详见 `references/c-cpp-checklist-details.md` 的「错误处理与异常捕获」章节。 |
| 4 | 多线程调用线程不安全接口 | 部分标准库接口使用内部静态缓冲区，多线程并发调用会导致数据竞争和不可预测结果。详见 `references/c-cpp-checklist-details.md` 的「多线程调用线程不安全接口」章节。 |
| 5 | setenv/getenv 崩溃风险 | `setenv`/`getenv` 因历史实现问题，并发调用容易引起崩溃，应尽可能避免使用。详见 `references/c-cpp-checklist-details.md` 的「setenv/getenv 崩溃风险」章节。 |
| 6 | SO 库符号导出控制 | 编译为 so 动态库时必须做符号导出控制，避免暴露内部符号。详见 `references/c-cpp-checklist-details.md` 的「SO 库符号导出控制」章节。 |
| 7 | 系统资源与权限限制 | Linux 系统中资源有限（如线程号上限），需正确处理资源不足场景。详见 `references/c-cpp-checklist-details.md` 的「系统资源与权限限制」章节。 |
| 8 | POSIX void* 指针的解引用 | POSIX 标准接口中定义为 `void*` 的字段不得解引用为具体类型使用，存在 ABI 风险。详见 `references/c-cpp-checklist-details.md` 的「POSIX void* 指针解引用风险」章节。 |

**当 C/C++ 检查清单中任一检查项命中（即 PR 变更涉及该检查项对应的场景）时，读取 `references/c-cpp-checklist-details.md` 中对应章节获取详细审查依据、典型案例和审查要点。**

#### ArkTS 语言检查清单

当前暂无 ArkTS 专属审查项。若 PR 包含 ArkTS 代码变更，仅执行通用审查（Step 2），并在报告中注明 ArkTS 专属检查待补充。

### Step 4: 仓库专属知识审查

根据目标仓库，逐项检查对应仓库知识清单中的每一项。

#### third_party_musl 检查清单

| # | 检查项 | 说明 |
|---|---|---|
| 1 | 导出符号兼容性 | musl 通过 `libc.map.txt` 导出公共 API 符号。如果 PR 新增、删除或修改了 `libc.map.txt` 中的符号，需验证：(a) 新增导出符号遵循现有命名规范；(b) 没有删除已有导出符号或修改其签名（ABI 破坏）；(c) 符号版本号正确（如适用）。删除或修改已有导出符号的签名属于破坏性变更，必须标记为"严重"。 |

审查 musl 代码时，读取仓库根目录的 `libc.map.txt` 查看导出符号定义。

#### arkcompiler_runtime_core 检查清单

当前暂无 runtime_core 专属审查项，仅执行 Step 1-3。

#### commonlibrary_c_utils 检查清单

当前暂无 c_utils 专属审查项，仅执行 Step 1-3。

### Step 5: 输出审查报告

输出结构化审查报告，包含以下章节：

1. **PR 信息**：仓库名称、PR 号、变更文件概览
2. **通用审查**：Step 2 发现的问题，按文件组织，附带严重程度
3. **语言补充审查**：Step 3 检查清单结果，逐项标注通过/不通过及详情
4. **仓库专属审查**：Step 4 检查清单结果，逐项标注通过/不通过及详情
5. **总结**：按严重程度统计（严重 / 警告 / 建议的数量），给出总体评估

## Prohibited Practices

- **跳过拉取 PR 分支**：必须从远程拉取最新 PR 分支代码，不得审查过期的本地分支
- **忽略信号安全违规**：信号安全问题属于未定义行为，必须标记为"严重"
- **忽略 musl 导出符号变更**：对 `libc.map.txt` 导出符号的任何变更必须显式审查 ABI 兼容性
- **未检查所有适用检查项即通过**：每个适用的检查项都必须有明确的通过/不通过结论

## Exceptions and Fallbacks

- **仓库不在支持列表中**：跳过 Step 4，但仍然执行 Step 1-3，并在报告中注明仓库专属检查已跳过
- **PR 分支拉取失败**：若远程 URL 不可达，请用户提供正确的仓库 URL 或本地 patch 文件
- **语言检查清单为空（如 ArkTS）**：在报告中注明该语言暂无定义专属检查项，仅执行通用审查
- **仓库检查清单为空**：在报告中注明该仓库暂无定义专属检查项，仅执行 Step 1-3
- **PR 仅包含非代码文件（如文档、配置）**：跳过语言专属和仓库专属检查，仅对相关内容进行通用审查

## References

| 文件/Skill | 读取条件 |
|---|---|
| `ohos-dev-gitcode-pr-review` skill | Step 1 中拉取 PR 分支和收集远程上下文时，按照该 skill 的 Workflow Step 1-2 和 Quick Flow 执行 |
| `references/c-cpp-checklist-details.md` | Step 3 中 C/C++ 检查清单任一检查项命中时，读取对应章节获取详细审查依据、典型案例和审查要点 |
| 目标仓库根目录的 `libc.map.txt` | Step 4 中审查 third_party_musl 仓库的导出符号兼容性时读取 |
