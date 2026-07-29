# 阶段 3：编译验证与修复

## 输入
- `{输出目录}/TestDemo/`（阶段2生成的代码目录）
- `{输出目录}/demo_code_manifest.md`（阶段2生成的初稿）
- `{输出目录}/demo_design.md`（阶段1输出的 Demo 设计文件，用于提取 API 清单）
- `reference/arkts-more-cases.md`（ArkTS 错误修复参考文档）

## 输出
- `{输出目录}/demo_code_manifest.md`（更新后的完整版本，含编译验证结果）

## 编译命令执行约束（强制执行）

- `hvigorw assembleHap` 是 HarmonyOS 全量编译命令
- **编译命令根据操作系统选择（强制执行）：**
  - **Windows（PowerShell）**：使用 `hvigorw.bat assembleHap`，命令链接语法使用 `; if ($?) {}`，使用 `workdir` 参数切换目录而非 `cd`
    ```powershell
    hvigorw.bat assembleHap
    ```
  - **Linux/macOS（Bash）**：使用 `./hvigorw assembleHap`，命令链接语法使用 `&&`
    ```bash
    ./hvigorw assembleHap
    ```
  - 判断方式：运行时环境信息中 `platform` 为 `win32` 时使用 Windows 命令，否则使用 Linux/macOS 命令
- 编译输出可能超过 2000 行，bash 工具会自动截断并写入文件；使用 Read 工具按需读取截断的完整输出

```
[步骤1] [Bash] 检查 hvigorw 是否存在于 PATH
  │
  ├─ hvigorw 不存在 ──→ [步骤1.2] 按调用模式分支
  │    ├─ 独立调用 → [AskUserQuestion] 询问用户安装或终止
  │    │    ├─ "已安装" → 回到步骤1.1 重新检查
  │    │    └─ "终止" → 返回摘要（HVIGORW_NOT_FOUND），结束
  │    └─ 协调器调用 → 写入返回摘要（HVIGORW_NOT_FOUND + 环境缺失详情），结束
  │
  ↓（hvigorw 存在）
  │
[Bash] 执行 hvigorw.bat assembleHap（或 ./hvigorw assembleHap）
  │
  ↓（得到结果后，进入步骤2，不做任何其他操作）
  │
[步骤2] 判断编译结果
  ├─ 输出包含 "BUILD SUCCESSFUL"
  │    → [Edit] 更新 demo_code_manifest.md
  │    → [AskUserQuestion] 确认（仅此处允许等待用户）
  │
   └─ 输出包含 "BUILD FAILED" 或 "ERROR"
        → [步骤2.5] SDK 缺失 API 门控（强制前置，不可跳过）
             │
             ├─ 检测到 SDK 缺失 API ──→ 立即终止，禁止进入修复循环
             │    → [Edit] 更新 manifest（BUILD FAILED: SDK过低）
             │    → [步骤2.5.3] 按调用模式分支
             │         ├─ 独立调用 → [AskUserQuestion] 询问用户替换 SDK 或终止
             │         └─ 协调器调用 → 写入返回摘要（SDK版本过低 + 缺失API清单），结束
             │
             └─ 非 SDK 缺失 ──→ 进入步骤3修复循环（最多5轮）
                  │
                  ┌─── 修复轮次 N（第1轮到第5轮）────────────────────┐
                  │ [3.1] 从编译输出提取错误信息                      │
                  │ [3.2] 查询修复方案 [Grep] arkts-more-cases.md    │
                  │ [3.3] 执行修复 [Edit]                             │
                  │ [3.4] 重新编译 [Bash] hvigorw.bat assembleHap    │
                  │                                                   │
                  │ [3.5] 判断本轮结果                                │
                  │   ├─ "BUILD SUCCESSFUL" → 跳出循环 → 步骤4      │
                  │   ├─ 检测到 SDK 缺失 → 立即终止循环 → 步骤2.5   │
                  │   └─ 仍失败                                       │
                  │        ├─ 轮次 < 5 → 回到 3.1 继续下一轮        │
                  │        └─ 轮次 ≥ 5 → 跳出循环 → 步骤4          │
                  └───────────────────────────────────────────────────┘
        │
        ↓
[步骤4] 更新 demo_code_manifest.md
  → [AskUserQuestion] 确认（仅此处允许等待用户）
```

**强制规则：**
- **首次编译完成后，必须立即进入步骤2判断结果，不允许在此之前进行任何 Read/Grep/Edit 等操作**
- 编译命令返回后，禁止输出纯文本总结后停止。必须在同一响应中继续调用工具。
- 修复循环内禁止插入 AskUserQuestion 或等待用户输入。
- 如果编译输出被截断，使用 Read 工具读取完整输出文件后继续流程。
- **SDK 门控强制规则（最高优先级）：BUILD FAILED 后必须先执行步骤2.5 的 SDK 缺失 API 门控，通过后才能进入步骤3。禁止在未完成 SDK 门控的情况下执行任何 Edit 修复或 Grep 查询修复方案操作。每次重新编译后若仍然 BUILD FAILED，必须再次通过步骤2.5 门控。**

## 步骤详解

**步骤1：执行首次编译**

1.1 **环境检查**：在执行编译命令前，先检查 `hvigorw` 是否存在于系统 PATH 中

Windows (PowerShell)：
```powershell
$hvigorCmd = Get-Command hvigorw -ErrorAction SilentlyContinue
if ($hvigorCmd -eq $null) {
    # hvigorw 不在 PATH 中，尝试在常见路径中查找
    $hvigorCmd = Get-Command "hvigorw.bat" -ErrorAction SilentlyContinue
}
```

Linux/macOS (Bash)：
```bash
if ! command -v hvigorw &> /dev/null; then
    # hvigorw 不在 PATH 中
fi
```

1.2 **命令不存在处理（按调用模式分支）**：
- 如果 `hvigorw` 不在 PATH 中，**立即终止阶段3**，不执行任何编译操作
- 根据调用模式执行不同策略：
  - **独立调用**：使用 AskUserQuestion 询问用户：
    - 问题："未在系统 PATH 中找到 hvigorw 命令。请确保已安装 HarmonyOS command-line-tools 并将其路径添加到系统 PATH 环境变量。详情请参阅：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get"
    - 选项1："我已安装并配置 PATH，重新检查" → 重新执行步骤1.1 环境检查
    - 选项2："终止阶段3" → 返回摘要（编译状态：HVIGORW_NOT_FOUND），结束阶段3
  - **协调器调用**：**禁止使用 AskUserQuestion**（子 Agent 无法将问题传递给用户）。改为将缺失信息写入返回摘要：
    - 在返回摘要的"编译状态"字段中输出 `HVIGORW_NOT_FOUND`
    - 在返回摘要中新增"环境缺失详情"字段，值为"未在系统 PATH 中找到 hvigorw 命令，需安装 HarmonyOS command-line-tools"
    - 在返回摘要中新增"环境缺失处理建议"字段，值为"需协调器询问用户：安装 command-line-tools 后重试 或 终止"
    - 返回摘要，结束阶段3

1.3 **执行编译**：
确认 `hvigorw` 存在后，使用 bash 工具执行（根据操作系统选择命令）：
- **Windows**：`workdir="{输出目录}/TestDemo"`，命令为 `hvigorw.bat assembleHap`
- **Linux/macOS**：`workdir="{输出目录}/TestDemo"`，命令为 `./hvigorw assembleHap`

**步骤2：判断编译结果**

从编译输出中提取编译状态：
- 输出包含 `BUILD SUCCESSFUL` → 记录编译状态为成功，**跳到步骤4**
- 输出包含 `BUILD FAILED` → **跳到步骤2.5**（SDK 门控）
- 输出被截断 → 使用 Read 工具读取截断提示中的完整输出文件路径，从中判断编译状态

**步骤2.5：SDK 缺失 API 门控（BUILD FAILED 后的强制前置步骤）**

**此步骤是修复循环的强制前置门控，必须在步骤3之前执行。无论编译失败多少次，每次 BUILD FAILED 后都必须先通过此门控才能进入修复循环。**

**禁止行为：** 在未完成本步骤的情况下，禁止执行任何 Edit/Grep 查询修复方案等修复操作。

2.5.1 **前置准备**：使用 Read 工具读取 `{输出目录}/demo_design.md`，提取其中定义的 API 清单（如 API 参考调用记录表中列出的所有 API 名称），作为基准 API 列表

2.5.2 **扫描全部编译错误**：从当前编译输出中提取所有编译错误，逐一检查每个错误是否为 SDK 缺失 API 导致：
  - **SDK 缺失 API 的判定条件**（必须同时满足以下两点）：
    - 编译错误匹配以下任一模式：
      - `has no exported member 'XXX'`（模块中不存在导出成员）
      - `Cannot find name 'XXX'` 且 XXX 为系统 API 名称（非拼写错误）
      - `Property 'XXX' does not exist on type 'YYY'` 且 YYY 为 SDK 内置类型
      - `Module 'XXX' not found` 且 XXX 为系统模块路径（如 `@ohos.XXX`）
    - **且报错的 API 名称存在于 demo_design.md 的基准 API 列表中**（即该 API 是 Demo 设计阶段明确要求使用的，而非代码中误用的）
  - **排除条件**（以下情况不属于 SDK 缺失，正常进入步骤3修复）：
    - 报错的 API 不在 demo_design.md 的基准 API 列表中（可能是代码中误用，走正常修复流程）
    - 错误为 ArkTS 语法约束类（如 `arkts-no-any-unknown`、`arkts-identifiers-as-prop-names`）
    - 错误为类型推断类（如 `Object is of type 'unknown'`）
    - 错误为代码逻辑类（如变量未定义、参数类型不匹配）

2.5.3 **门控判定结果**：
   - **检测到 SDK 缺失 API**：
     1. **立即终止**，禁止执行任何代码修复操作（Edit/Grep 查询修复方案等）
     2. 收集所有 SDK 缺失的 API 名称列表（仅保留 demo_design.md API 清单中存在的 API）
     3. **跳到步骤4**，在 manifest 中记录编译状态为 `BUILD FAILED (SDK 版本过低)`，并列出缺失 API 清单
     4. 根据调用模式执行不同策略：
        - **独立调用**：使用 AskUserQuestion 询问用户：
          - 问题：`检测到 SDK 版本过低，以下 API 在当前 SDK 中不存在：{缺失 API 列表}。请在 command-line-tools 目录下替换为更高版本的 SDK，替换完成后继续。`
          - 选项1：`已完成 SDK 替换，重新编译` → 从步骤1重新执行整个阶段3（重置修复次数为 0）
          - 选项2：`终止阶段3` → 返回摘要，结束阶段3
        - **协调器调用**：**禁止使用 AskUserQuestion**。改为将缺失信息写入返回摘要：
          - 编译状态：`SDK版本过低`
          - 缺失 API 清单：列出所有缺失 API 的完整名称
          - SDK 缺失处理建议：`需协调器询问用户：替换 SDK 后重试 或 跳过继续`
          - 标注 Demo 编译验证为"未验证（SDK 缺失）"，返回摘要，结束阶段3
  - **未检测到 SDK 缺失 API** → **通过门控，进入步骤3修复循环**

**步骤3：编译失败修复（单次迭代，最多重复5次）**

**前置条件：已通过步骤2.5 的 SDK 门控检测。**

以下是单次修复迭代的完整操作序列，**严格按顺序调用工具**：

3.1 **提取错误信息**：从编译输出中提取所有编译错误（文件路径、行号、错误消息）
  - 如果输出被截断，使用 Read 工具读取完整输出文件

3.2 **查询修复方案**：使用 Grep 工具在 `reference/arkts-more-cases.md` 中搜索与错误消息匹配的修复方案
  - 搜索关键词优先使用错误消息中的错误码（如 `arkts-no-any-unknown`）或关键短语
  - 如果 Grep 无匹配结果，根据编译错误信息自行分析原因并推断修复方案
  - **禁止通过删除或替换系统 API 接口来消除编译错误**

3.3 **执行修复**：使用 Edit 工具修改报错文件，仅修复编译报错指向的具体问题
  - 记录本次修复：文件路径、错误信息、修复方案

3.4 **重新编译**：使用 bash 工具再次执行编译命令（同步骤1的操作系统对应命令），使用 `workdir` 参数指定 `{输出目录}/TestDemo`

3.5 **判断本轮结果**：从本轮编译输出中提取编译状态
  - 输出包含 `BUILD SUCCESSFUL` → 修复成功，记录总修复次数，**跳到步骤4**
  - 输出包含 `BUILD FAILED` → **回到步骤2.5 重新执行 SDK 门控**（修复可能引入新的 SDK 兼容问题）
  - 仍然失败且总修复次数 ≥ 5 → 已达最大修复次数，**跳到步骤4**，在 manifest 中记录"修复 5 次仍未通过"

**步骤4：更新 manifest**

无论成功还是失败，使用 Edit 工具将编译结果记录到 demo_code_manifest.md：
- 编译状态
- 修复次数
- 每次修复的详情（文件、错误信息、修复方案）

## 常见编译错误与修复参考

| 编译错误类别 | 典型错误信息 | 处理方式 |
|-------------|-------------|---------|
| **SDK 缺失 API（终止编译）** | `has no exported member 'XXX'`、`Cannot find name 'XXX'`（系统 API）、`Property 'XXX' does not exist on type 'YYY'`（SDK 内置类型）| **立即终止修复循环**，输出缺失 API 清单告警，提示用户升级 SDK |
| arkts-no-any-unknown | `Cannot find name 'any'` | 替换为具体类型 |
| arkts-identifiers-as-prop-names | 属性名不应使用引号 | 移除引号 |
| arkts-no-standalone-this | `Using "this" inside stand-alone functions` | 静态方法中使用类名替代 this |
| JSON.parse 返回值 | `Return type not typed` | 使用 `Record<string, Object>` 标注 |
| 类型推断失败 | `Object is of type 'unknown'` | 添加类型声明或断言 |

## 自检清单

1. 已检查 hvigorw 命令存在于系统 PATH（如不存在，已终止并告警）
2. 编译命令已执行（如 hvigorw 存在）
3. 每次 BUILD FAILED 后，已先执行步骤2.5 SDK 门控再进入修复循环（未跳过门控）
4. 编译状态已记录（SUCCESS 或 FAILED）
5. 如检测到 SDK 缺失 API，已立即终止修复循环并输出告警（未执行任何代码修复）
6. 修复循环次数正确（未超过5次）
7. 所有修复操作已记录详情
8. 未通过删除或替换系统 API 接口来消除编译错误

## 确认机制

**所有模式统一执行**：分两种场景：

### 场景 A：SDK 版本过低
完成后显示 SDK 缺失告警（缺失 API 清单，仅列出 demo_design.md 中定义的 API），根据调用模式执行不同策略：

- **独立调用**：使用 AskUserQuestion 询问用户：
  - 问题：`检测到 SDK 版本过低，以下 API 在当前 SDK 中不存在：{缺失 API 列表}。请在 command-line-tools 目录下替换为更高版本的 SDK，替换完成后继续。`
  - 选项1：`已完成 SDK 替换，重新编译` → 从步骤1重新执行阶段3（重置修复次数为 0，从头编译）
  - 选项2：`终止阶段3` → 返回摘要，结束阶段3

- **协调器调用**：**禁止使用 AskUserQuestion**。改为将缺失信息写入返回摘要：
  - 编译状态：`SDK版本过低`
  - 缺失 API 清单：列出所有缺失 API 的完整名称
  - SDK 缺失处理建议：`需协调器询问用户：替换 SDK 后重试 或 跳过继续`
  - 标注 Demo 编译验证为"未验证（SDK 缺失）"，返回摘要，结束阶段3

### 场景 B：hvigorw 未安装
编译命令不存在于系统 PATH 中，根据调用模式执行不同策略：

- **独立调用**：使用 AskUserQuestion 询问用户：
  - 问题：`未在系统 PATH 中找到 hvigorw 命令，请安装 HarmonyOS command-line-tools 并配置 PATH`
  - 选项1：`我已安装，重新检查` → 从步骤1.1 重新执行环境检查
  - 选项2：`终止阶段3` → 返回摘要（编译状态：HVIGORW_NOT_FOUND），结束阶段3

- **协调器调用**：**禁止使用 AskUserQuestion**。改为将缺失信息写入返回摘要：
  - 编译状态：`HVIGORW_NOT_FOUND`
  - 环境缺失详情：`未在系统 PATH 中找到 hvigorw 命令，需安装 HarmonyOS command-line-tools`
  - 环境缺失处理建议：`需协调器询问用户：安装 command-line-tools 后重试 或 终止`
  - 返回摘要，结束阶段3

### 场景 C：编译成功或普通编译失败
完成后显示摘要（编译状态/修复次数/输出目录），使用 AskUserQuestion 询问用户确认。
- **确认完成** → 进入阶段 4
- **输入优化建议** → 手动修复代码、重新编译验证、更新 manifest、再次确认，循环直到确认完成
