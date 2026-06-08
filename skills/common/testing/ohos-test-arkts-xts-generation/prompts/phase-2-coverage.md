## Phase 2: Initial Coverage Scan

---

> **`knowledge_root` 降级**：下文中所有 `{knowledge_root}/...` 路径，若 `knowledge_root` 未配置或路径不存在，则降级从 `{skill_root}/modules/` 和 `{skill_root}/references/` 加载对应内置知识。完整映射表见 `system.md`「知识库路径与降级规则」。

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{knowledge_root}/common/xts_experience/09_methodology/06_api_coverage_detector.md` | APICoverageDetector 工具完整手册 | 扫描命令参数不确定、结果格式异常时 |
| `{knowledge_root}/common/xts_experience/09_methodology/05_coverage_analysis.md` | 覆盖率分析方法论（8维度、缺口分级） | 需要理解覆盖率维度含义或缺口分级标准时 |

---

### ⚙️ 按需加载（根据执行模式）

以下模块仅在你执行对应任务时才需要加载：

| 执行模式 | 加载文件 | 说明 |
|---------|---------|------|
| 异步扫描模式（Flow B） | `{skill_root}/scripts/async_coverage_scan.py` | 脚本工具，执行异步覆盖率扫描 |
| 需要额外分析参数时 | `{knowledge_root}/common/xts_experience/09_methodology/04_api_parameter_rules.md` | 可选参数分析规则 |

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有 L2_Generation 相关知识（{knowledge_root}/common/xts_experience/09_methodology/ 下的 08~18号文件）
所有 L3_Validation 相关知识（{knowledge_root}/common/xts_experience/09_methodology/ 下的 19~25号文件）
```

### 常见扫描失败排查

#### 覆盖率扫描失败：路径过长
- **症状**：APICoverageDetector 在 Windows 上报路径错误
- **根因**：Windows 260 字符路径限制 + XTS 深层目录结构
- **修复**：将工具放在磁盘根目录（如 `D:\APICoverageDetector`）

本 Phase 期间禁止加载以下模块：

```
所有 L2_Generation 相关知识（{knowledge_root}/common/xts_experience/09_methodology/ 下的 08~18号文件）
所有 L3_Validation 相关知识（{knowledge_root}/common/xts_experience/09_methodology/ 下的 19~25号文件）
{knowledge_root}/common/xts_experience/ 下的 01_framework、02_arkts、03_standards、04_project、05_patterns 规范文件
```

---

根据用户是否提供覆盖率报告，选择对应的执行流程：

| 条件 | 流程 | 说明 |
|------|------|------|
| 用户**已提供**覆盖率报告 | **Flow A**（下方第一节） | 跳过耗时扫描，直接解析用户报告 + 代码风格扫描 |
| 用户**未提供**覆盖率报告 | **Flow B**（下方第二节） | 使用 APICoverageDetector 异步扫描，获得精确覆盖率基线 |
| 用户明确说明**新增接口** | **Flow C**（下方第三节） | 跳过扫描，新增接口覆盖率为 0，仅做代码风格扫描 |

---

### Flow A: 基于用户提供的覆盖率报告

用户已提供覆盖率报告，跳过 APICoverageDetector 扫描，仅执行以下步骤：

**支持的覆盖率报告格式**：

| 格式 | 扩展名 | 解析方式 |
|------|--------|---------|
| APICoverageDetector Excel 输出 | `.xlsx` | **直接使用 `scripts/extract_uncovered.py` 解析**，无需先转 CSV |
| CSV 数据表 | `.csv` | 直接读取，使用 `scripts/extract_uncovered.py` 提取未覆盖 API |
| 未覆盖 API JSON 列表 | `.json` | 直接读取为 `uncovered_apis.json` 格式 |
| Markdown 覆盖率报告 | `.md` | 手动解析，提取未覆盖 API 名称和缺失场景 |

**格式不兼容时的处理**：

若用户提供的报告格式不在上述列表中：
1. 请求用户转换为 CSV 或 JSON 格式（推荐 CSV，与 Flow B 数据流一致）
2. 若用户无法转换，尝试手动解析报告内容，提取未覆盖 API 列表
3. 解析失败则提示用户使用 APICoverageDetector 重新扫描（切换到 Flow B）

**代码风格扫描**：
1. 快速扫描 3-5 个代表性测试文件
2. 提取代码风格：导入顺序、describe/it 结构、断言方法、错误处理模式

确认报告格式后，进入下方「解析覆盖率结果」章节，使用 `extract_uncovered.py` 提取未覆盖 API。

---

### Flow B: APICoverageDetector 异步扫描

APICoverageDetector 扫描耗时较长（30-60 分钟），必须使用异步模式避免超时。不要直接调用 `arkts_entrance.exe` 或使用管道输入，统一通过 `async_coverage_scan.py` 操作。

#### 步骤 1：确认环境支持覆盖率扫描

**平台支持矩阵**：

| 环境 | 是否可用 | 说明 |
|------|---------|------|
| Windows 原生 | ✅ | 直接调用 `.exe`，路径使用 Windows 格式 |
| WSL | ✅ | 通过 `/mnt/d/...` 路径调用 `.exe`，`platform: "wsl"` 时从 `OH_ROOT` 推导本地路径 |
| 纯 Linux（计算云/远程服务器） | ❌ | 不可用，提示用户提供覆盖率报告 |

**环境检查**：

```bash
# 检查扫描工具目录是否存在
ls {scan_tool_root}/arkts_entrance/arkts_entrance.exe 2>/dev/null 

# 检查当前扫描环境状态
python {skill_root}/scripts/manage_scan_env.py status
```

如果工具不存在，提示用户提供覆盖率报告（切换到 Flow A）。

#### 步骤 2：准备扫描环境（测试用例 + SDK + 配置）

使用 `manage_scan_env.py setup` 一键完成环境准备，包括：复制测试文件、检查/补充 SDK、备份并修改 `arkts_config.json`（同步 ets_version + 更新 case_path）。

**仅复制指定模块**（**强烈推荐**，大幅减少复制量和扫描时间）：

> **性能提示**（问题 3 优化）：当用户指定了明确的 d.ts 文件（如 `component/text.d.ts`）或具体测试目录时，**必须优先使用 `--module` 参数**仅复制相关模块。全量子系统复制+扫描耗时 25-60 分钟，而单模块仅需 3-10 分钟。仅在用户明确要求"扫描整个子系统"时才省略 `--module`。

```bash
# 仅复制指定模块（推荐）
python {skill_root}/scripts/manage_scan_env.py setup --subsystem {Subsystem} --module {ModuleRelPath}
# 例：--subsystem arkui --module ace_ets_module_ui/ace_ets_module_imageText

# 复制整个子系统（仅在用户明确要求全量扫描时使用）
python {skill_root}/scripts/manage_scan_env.py setup --subsystem {Subsystem}
```

`manage_scan_env.py setup` 自动完成：
- 创建过滤目录 `testcase/xts_acts_filtered_{Subsystem}/`
- 复制测试文件到过滤目录
- 备份 `arkts_config.json` → `arkts_config.json.bak`（仅备份一次，避免多处修改互相覆盖）
- 同步 `ets_version`：从 `.oh-xts-config.json` 写入 `arkts_config.json`
- 更新 `case_path.open_source` → `["xts_acts_filtered_{Subsystem}"]`
- 检查 SDK 完整性：对 `ets_version` 配置的每个版本，检查 `sdk/openharmony/ets/{version}/` 是否存在且非空
  - 缺失 → 自动从 `sdk_local_path` 复制对应版本
  - 已存在 → 跳过

**手动更新 SDK**（仅在用户明确要求时执行）：

```bash
# 更新配置中 ets_version 指定的版本（已有则跳过）
python {skill_root}/scripts/manage_scan_env.py update-sdk

# 强制更新指定版本（覆盖已有内容）
python {skill_root}/scripts/manage_scan_env.py update-sdk --version ets1.1 --force

# 仅更新 ets1.2
python {skill_root}/scripts/manage_scan_env.py update-sdk --version ets1.2
```

**检查新增接口是否在 SDK 中**（Flow C 场景，确认新增 API 是否已包含在工具 SDK 中）：

```bash
# 检查单个 API
python {skill_root}/scripts/check_api_in_sdk.py --api text.d.ts

# 检查多个 API
python {skill_root}/scripts/check_api_in_sdk.py --api text.d.ts button.d.ts

# 用相对路径精确查找
python {skill_root}/scripts/check_api_in_sdk.py --api component/text.d.ts

# JSON 格式输出（供脚本处理）
python {skill_root}/scripts/check_api_in_sdk.py --api text.d.ts --json
```

**增量同步文件**（Phase 10 复用 Phase 2 环境，仅同步生成阶段新增/修改的文件）：

```bash
python {skill_root}/scripts/manage_scan_env.py sync --subsystem {Subsystem} --manifest {manifest_json}
# manifest.json 格式：{"files": ["ace_ets_module_ui/.../NewTest.test.ets", ...]}
```

#### 步骤 3：启动异步扫描并等待完成

```bash
# 3.1 启动异步扫描（脚本会自动清理旧的 status/pid/progress 文件）
python {skill_root}/scripts/async_coverage_scan.py start

# 3.2 轮询检查状态（每 30 秒一次，直到完成）
python {skill_root}/scripts/async_coverage_scan.py status

# 3.3 扫描完成后获取结果
python {skill_root}/scripts/async_coverage_scan.py results
```

**扫描状态**：

| 状态 | 说明 | 操作 |
|------|------|------|
| `idle` | 未启动或残留文件已清理 | 执行 `start` |
| `running` | 扫描正在运行 | 继续轮询等待 |
| `completed` | 扫描完成 | 执行 `results` |
| `failed` | 扫描失败 | 检查 `APICoverageDetector/log/` 目录日志 |

扫描可能需要 10-30 分钟（单模块）或 30-60 分钟（全量子系统）。

##### ⚠️ 扫描真实性验证（必须执行）

**启动扫描后必须验证扫描是否真正在执行**，防止拿到历史结果：

```bash
# 启动后等待 10 秒
sleep 10

# 检查日志文件时间戳和内容（时间戳必须是刚刚的）
ls -la {scan_tool_root}/log/arkts_runner.log
tail -10 {scan_tool_root}/log/arkts_runner.log

# 验证日志中出现 "(1/10) count工具" 等新内容
# 如果日志时间戳是旧的 → 扫描没有真正执行
```

**常见异常与处理**：

| 异常现象 | 原因 | 处理方式 |
|---------|------|---------|
| 启动后 `status` 立即显示 `completed`，但日志时间戳是旧的 | `arkts_entrance.exe` 检测到已有结果文件后快速退出，未重新扫描 | 脚本已在 `start` 前自动清理旧 status/pid/progress 文件。如仍发生，检查 `scan_error.log` |
| PID 存活但日志不再更新（僵尸进程） | WSL 下 `cmd.exe` 进程未正常退出 | 执行 `stop` 停止僵尸进程，然后重新 `start` |
| `status` 返回历史结果（非本次扫描） | 之前扫描的 status 文件残留 | 脚本已在 `start` 前自动清理。手动清理：`rm {scan_tool_root}/coverage_scan.status {scan_tool_root}/coverage_scan.pid {scan_tool_root}/coverage_scan.progress {scan_tool_root}/scan_error.log` |
| 扫描超时未完成 | 全量子系统扫描耗时长 | 等待或使用 `--module` 参数仅扫描目标模块（推荐） |


#### 步骤 4：解析扫描结果

扫描完成并得到 Excel 结果后，进入下方「解析覆盖率结果」章节提取未覆盖 API。

#### 步骤 5：恢复扫描环境（仅在用户要求时执行）

> **默认行为**：覆盖率扫描完成后**不自动执行 teardown**，保留扫描环境以便后续复用或调试。仅在用户明确要求恢复环境时执行。

当用户明确要求恢复扫描环境时，使用 `manage_scan_env.py` 脚本：

```bash
python {skill_root}/scripts/manage_scan_env.py teardown --subsystem {Subsystem}
```

脚本自动完成：
- 删除已复制的子系统文件副本（仅删除副本不影响源文件）
- 删除过滤目录
- 从备份恢复 `arkts_config.json`

**何时需要执行 teardown**：
- 用户明确要求清理环境
- 需要切换到其他子系统扫描（当前子系统的环境会冲突）
- 所有扫描工作已全部完成，需要恢复原始状态

**多版本说明**：若用户配置了多个 ETS 版本（如 `ets1.1,ets1.2`，即 ArkTS-Dyn 和 ArkTS-Sta），异步扫描会自动为每个版本生成独立结果。每轮迭代的扫描结果通过时间戳区分，无需手动管理。

---

### Flow C: 新增接口模式（跳过覆盖率扫描）

当用户明确说明任务是**新增接口**（如"新增 API"、"新接口"、"new API"等）时使用此流程。

**核心假设**：新增接口在当前代码中不存在任何测试用例，覆盖率必为 0。无需执行耗时的 APICoverageDetector 扫描来验证这一点。

**执行步骤**：

1. **代码风格扫描**（与 Flow A 相同）：
   - 快速扫描 3-5 个同目录下的现有测试文件
   - 提取代码风格：导入顺序、describe/it 结构、断言方法、错误处理模式
   - 找到与目标 API 最相似的现有测试文件作为参考模板

2. **构建未覆盖 API 列表**：
   - 将用户提供的全部新增 API 直接标记为未覆盖（无需扫描确认）
   - 所有 API 缺口级别默认为 HIGH（新增接口，完全未测试）

3. **跳过覆盖率扫描**：
    - 不执行 `async_coverage_scan.py`

4. **Phase 9 适配**：
   - Phase 9 仅执行 after 扫描（无 before baseline 对比）
   - 覆盖率报告中"生成前"列标注为"0（新增接口）"

---

### 解析覆盖率结果（Flow A / Flow B 共用）

Flow A 和 Flow B 最终都产出覆盖率数据，需要使用 `extract_uncovered.py` 提取未覆盖 API。

**完整用法**：

```bash
# 按子系统筛选
python {skill_root}/scripts/extract_uncovered.py --subsystem "ArkUI开发框架"

# 按 d.ts 文件筛选
python {skill_root}/scripts/extract_uncovered.py --dts-file "component\\text.d.ts"

# 按类名筛选
python {skill_root}/scripts/extract_uncovered.py --class-name TextAttribute

# 按接口名筛选
python {skill_root}/scripts/extract_uncovered.py --interface-name fontFeature

# 按 Kit 筛选
python {skill_root}/scripts/extract_uncovered.py --kit ArkUI

# 组合筛选
python {skill_root}/scripts/extract_uncovered.py --subsystem ArkUI开发框架 --kit ArkUI --class-name TextAttribute

# 指定迭代阶段
python {skill_root}/scripts/extract_uncovered.py --iter-phase 2
```

**输出两个文件到 `.coverage_data/iter-{N}/`**：

| 文件 | 内容 |
|------|------|
| `uncovered_apis_{timestamp}.json` | 真正未覆盖的 API（仅含"未覆盖"状态的维度） |
| `manual_confirm_{timestamp}.json` | 需人工确认的 API（`err_desc` 含"工具暂不能识别返回值类型"） |

**8 个覆盖维度**（AQ-AX 列，每个维度独立判断）：

| 维度 | 说明 | Excel 列 |
|------|------|---------|
| `call` | 调用覆盖 | AQ |
| `param` | 入参覆盖 | AR |
| `param_spec` | 参数规格覆盖 | AS |
| `return_value` | 返回值覆盖 | AT |
| `error_code` | 错误码覆盖 | AU |
| `permission` | 权限覆盖 | AV |
| `stage` | stagemodel 标签覆盖 | AW |
| `meta` | 元服务覆盖 | AX |

**覆盖率缺口分级**：

| 缺口类型 | 优先级 | 说明 |
|---------|--------|------|
| 完全未测试 | HIGH | 方法在测试文件中从未被调用 |
| 部分测试 | MEDIUM | 方法被调用，但缺少 null/undefined、边界值、错误码等场景 |
| 测试不完整 | LOW | 测试用例存在但无断言，或只有正向测试缺少负向测试 |

---

### 输出总览

| 维度 | Flow A 输出 | Flow B 输出 | Flow C 输出 |
|------|------------|------------|------------|
| 未覆盖 API 列表 | `extract_uncovered.py` 解析用户报告 | `.coverage_data/iter-{N}/uncovered_apis_<timestamp>.json` | 用户提供的全部新增 API |
| 需人工确认列表 | `extract_uncovered.py` 生成（如有） | `.coverage_data/iter-{N}/manual_confirm_<timestamp>.json` | 无 |
| 覆盖率缺口列表 | 基于用户报告解析（8维度判断） | 基于扫描结果（8维度判断，HIGH/MEDIUM/LOW 分级） | 全部新增 API（默认 HIGH） |
| 代码风格总结 | 有 | 有 | 有 |

**关键说明**：未覆盖 API 列表是此阶段最重要的输出，将作为 Phase 3 的输入，仅针对未覆盖的接口进行深度解析，避免全量扫描。`manual_confirm` 文件中的 API 需提示用户人工审核。
