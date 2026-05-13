## Phase-2 覆盖率扫描

---

### 📦 MANDATORY - 必须先加载以下模块

**在执行本 Phase 前，你必须完整阅读以下文件**（不得设置行数限制）：

```
{skill_root}/modules/L1_Analysis/tools/api_coverage_detector.md
{skill_root}/modules/L1_Analysis/analyzer/coverage_analyzer.md
```

---

### ⚙️ 按需加载（根据执行模式）

以下模块仅在你执行对应任务时才需要加载：

| 执行模式 | 加载文件 | 说明 |
|---------|---------|------|
| 异步扫描模式（Flow B） | `{skill_root}/scripts/async_coverage_scan.py` | 脚本工具，执行异步覆盖率扫描 |
| 需要额外分析参数时 | `{skill_root}/modules/L1_Analysis/analyzer/api_parameter_optional_rules.md` | 可选参数分析规则 |

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有 L2_Generation 模块（modules/L2_Generation/）
所有 L3_Validation 模块（modules/L3_Validation/）
references/conventions/ 目录
```

---

根据用户是否提供覆盖率报告，选择对应的执行流程：

| 条件 | 流程 | 说明 |
|------|------|------|
| 用户**已提供**覆盖率报告 | **Flow A**（下方第一节） | 跳过耗时扫描，直接解析用户报告 + 代码风格扫描 |
| 用户**未提供**覆盖率报告 | **Flow B**（下方第二节） | 使用 APICoverageDetector 异步扫描，获得精确覆盖率基线 |

---

### Flow A: 基于用户提供的覆盖率报告

用户已提供覆盖率报告，跳过 APICoverageDetector 扫描，仅执行以下步骤：

**支持的覆盖率报告格式**：

| 格式 | 扩展名 | 解析方式 |
|------|--------|---------|
| APICoverageDetector Excel 输出 | `.xlsx` | 通过 `scripts/convert_results.py --phase before` 转换为 CSV 后解析 |
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

**从覆盖率报告中提取缺口**：
- 未覆盖的 API 名称
- 缺失的参数组合
- 缺失的测试场景（边界值、错误码等）
- 测试类型（PARAM、ERROR、RETURN、BOUNDARY）

---

### Flow B: APICoverageDetector 异步扫描

APICoverageDetector 扫描耗时较长（30-60 分钟），必须使用异步模式避免超时。不要直接调用 `arkts_entrance.exe` 或使用管道输入，统一通过 `async_coverage_scan.py` 操作。

#### 步骤 1：准备子系统扫描环境

使用 `manage_scan_env.py` 脚本自动复制子系统文件和 SDK 文件到扫描目录、备份并修改 `arkts_config.json`。

> **工具路径**：脚本自动从 `.oh-xts-config.json` 的 `scan_tool_root` 字段读取 APICoverageDetector 的安装位置，无需手动指定。**注意：该工具仅支持 Windows 环境**（Windows 原生或 WSL），Linux 计算云环境不可用，需让用户提供覆盖率报告。

```powershell
python {skill_root}/scripts/manage_scan_env.py setup --subsystem {Subsystem}
```

脚本自动完成：
- 创建过滤目录 `testcase/xts_acts_filtered_{Subsystem}/`
- 复制子系统测试文件（从 `{xts_acts_path}\{Subsystem}` 到过滤目录）
- 复制 SDK 文件（从 `{sdk_path}\ets` 到扫描工具 SDK 目录）
- 备份 `arkts_config.json` → `arkts_config.json.bak`
- 修改 `case_path.open_source` 为 `["xts_acts_filtered_{Subsystem}"]`

**复制操作可能耗时较长**（取决于子系统文件大小），脚本会显示源目录大小和复制进度。

如需检查当前环境状态：
```powershell
python {skill_root}/scripts/manage_scan_env.py status
```

#### 步骤 2：启动异步扫描并等待完成

```powershell
# 2.1 启动异步扫描
python {skill_root}/scripts/async_coverage_scan.py start

# 2.2 轮询检查状态（每 30 秒一次，直到完成）
python {skill_root}/scripts/async_coverage_scan.py status

# 2.3 扫描完成后获取结果
python {skill_root}/scripts/async_coverage_scan.py get_results
```

**扫描状态**：

| 状态 | 说明 | 操作 |
|------|------|------|
| `running` | 扫描正在运行 | 继续轮询等待 |
| `completed` | 扫描完成 | 执行 `get_results` |
| `failed` | 扫描失败 | 检查 `APICoverageDetector/log/` 目录日志 |
| `not_started` | 未启动 | 执行 `start` |

扫描可能需要 30-60 分钟，`get_results` 会自动将结果保存到 `{skill_root}/.coverage_data/` 目录。

#### 步骤 3：解析扫描结果并生成覆盖率缺口列表

扫描完成后，`get_results` 已自动生成以下文件到 `.coverage_data/` 目录：

```
.coverage_data/
├── uncovered_apis_<timestamp>.json   # 未覆盖 API 列表
├── coverage_report_<timestamp>.md    # 覆盖率分析报告
└── iter-{N}/                         # 多轮迭代数据
```

使用 PowerShell 读取最新结果：

```powershell
# 读取最新的未覆盖 API 文件
$latest = Get-ChildItem {skill_root}/.coverage_data/uncovered_apis_*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Get-Content $latest.FullName

# 读取最新的覆盖率报告
$report = Get-ChildItem {skill_root}/.coverage_data/coverage_report_*.md | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Get-Content $report.FullName
```

**覆盖率统计维度**：接口覆盖率、API 调用覆盖率、方法覆盖率、入参覆盖率、参数规格覆盖率、错误码覆盖率、权限覆盖率、返回值覆盖率。

**覆盖率缺口分级**：

| 缺口类型 | 优先级 | 说明 |
|---------|--------|------|
| 完全未测试 | HIGH | 方法在测试文件中从未被调用 |
| 部分测试 | MEDIUM | 方法被调用，但缺少 null/undefined、边界值、错误码等场景 |
| 测试不完整 | LOW | 测试用例存在但无断言，或只有正向测试缺少负向测试 |

#### 步骤 3.5：将扫描结果转换为 CSV（Phase 3 的数据依赖）

Phase 3 的 `extract_uncovered.py` 脚本需要 CSV 格式的覆盖率数据。（跳过此步骤会导致 Phase 3 的 extract_uncovered.py 无法读取 XLSX 格式而报错，未覆盖 API 列表无法生成）使用 `convert_results.py` 自动为所有配置的 ETS 版本转换 Excel → CSV：

```powershell
python {skill_root}/scripts/convert_results.py --iter 1 --phase before
```

脚本自动完成：
- 从 `.oh-xts-config.json` 读取 `ets_version` 配置
- 遍历每个版本，将 `APICoverageDetector/results/{ver}/open_source/sdk_result.xlsx` 转换为 CSV
- 保存到 `.coverage_data/iter-1/before_generation_{ver}_{timestamp}.csv`

**迭代数据流**：
```
Phase 2 → iter-1/before_generation_ets1.1_*.csv  ─┐
                                                     ├→ Phase 3 (extract_uncovered.py)
Phase 2 → .coverage_data/uncovered_apis_*.json  ───┘
```

#### 步骤 4：恢复扫描环境

使用 `manage_scan_env.py` 脚本自动恢复环境：

```powershell
python {skill_root}/scripts/manage_scan_env.py teardown --subsystem {Subsystem}
```

脚本自动完成：
- 删除已复制的子系统文件副本（使用 `shutil.rmtree`，仅删除副本不影响源文件）
- 删除过滤目录
- 从备份恢复 `arkts_config.json`

如果不需要恢复（后续还要扫描同一子系统），可以跳过此步骤。

**多版本说明**：若用户配置了多个 ETS 版本（如 `ets1.1,ets1.2`，即 ArkTS-Dyn 和 ArkTS-Sta），异步扫描会自动为每个版本生成独立结果。每轮迭代的扫描结果通过时间戳区分，无需手动管理。

---

### 输出总览

| 维度 | Flow A 输出 | Flow B 输出 |
|------|------------|------------|
| 覆盖率报告 | 来自用户提供的报告 | `.coverage_data/coverage_report_<timestamp>.md` |
| 未覆盖 API 列表 | 从用户报告解析 | `.coverage_data/uncovered_apis_<timestamp>.json` |
| 覆盖率 CSV 数据 | 无 | `.coverage_data/iter-{N}/before_generation_*.csv`（供 Phase 3 使用） |
| 覆盖率缺口列表 | 基于用户报告解析 | 基于扫描结果（HIGH/MEDIUM/LOW 分级） |
| 代码风格总结 | 有 | 有 |

**关键说明**：未覆盖 API 列表是此阶段最重要的输出，将作为 Phase 3 的输入，仅针对未覆盖的接口进行深度解析，避免全量扫描。
