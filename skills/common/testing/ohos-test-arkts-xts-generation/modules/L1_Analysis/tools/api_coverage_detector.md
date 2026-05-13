# APICoverageDetector 工具使用指南

> **模块信息**
> - 层级：L1_Analysis/Tools
> - 优先级：按需加载
> - 适用范围：精确覆盖率扫描
> - 依赖：Node.js（es2panda 解析）、OpenHarmony SDK

---

## 一、工具概述

APICoverageDetector 是 OpenHarmony API 覆盖率精确扫描工具，支持 ArkTS 和 C API 两种子系统，提供多维度覆盖率分析。

**平台限制**：仅支持 Windows 环境（核心组件为 `.bat` + `.exe`）。WSL 可通过 `/mnt/d/APICoverageDetector` 路径访问 Windows 侧工具；Linux 计算云/远程服务器不可用，只能让用户提供已有的覆盖率报告。

---

## 二、目录结构

```
APICoverageDetector/
├── arkts_entrance/arkts_entrance.exe    # ArkTS 扫描入口
├── c_entrance/c_entrance.exe            # C API 扫描入口
├── configs/                             # 配置文件
│   ├── arkts_config.json                # ArkTS 主配置
│   ├── arkts_config.json.bak            # 默认配置备份
│   ├── c_config.json                    # C API 主配置
│   ├── service/                         # 输出字段映射
│   │   ├── arkts_coverage_map.json
│   │   └── c_coverage_map.json
│   └── _configs/                        # 内部辅助配置
│       ├── arkts_subsys_config.json     # 子系统负责人映射
│       ├── arkts_inner_config.json      # 内部配置
│       ├── c_module_subsys.json         # C API 模块-子系统映射
│       ├── testcase_category.json       # 用例分类规则
│       └── kit_system_list.xlsx
├── testcase/                            # 测试用例目录（通过文件复制）
│   ├── xts_acts/  → D:/xts_acts
│   ├── xts_dcts/
│   ├── xts_hats/
│   ├── hits/
│   ├── hcts_pub/
│   └── hcts_sys/
├── sdk/                                 # SDK API 定义目录（通过文件复制）
│   ├── openharmony/ets/ → D:/interface_sdk-js
│   └── hms/
├── results/                             # 扫描结果输出（Excel）
├── data/                                # 中间数据
└── log/                                 # 运行日志
```

---

## 三、配置文件说明

**配置文件**: `.oh-xts-config.json` - 存储本地路径信息

**配置内容**（Windows）:
```json
{
  "for_windows": {
    "xts_acts_path": "D:\\path\\to\\xts_acts",
    "sdk_path": "D:\\path\\to\\sdk\\ets"
  }
}
```

**用途**: 工具在复制文件到扫描目录时从该配置文件读取路径信息。

---

## 四、ArkTS 子系统扫描配置

配置文件：`APICoverageDetector/configs/arkts_config.json`

```json
{
    "describe": "此配置文件有测试人员进行配置",
    "isCompParame": true,
    "isCaseNames": true,
    "permission_check": true,
    "param_spec_check": true,
    "return_check": true,
    "model_check": false,
    "atomic_check": false,
    "case_path": {
        "closed_source": ["hcts_pub", "hcts_sys"],
        "open_source": ["xts_dcts", "xts_acts", "hits"]
    },
    "api_path": {
        "open_source": "sdk/openharmony/ets",
        "closed_source": "sdk/hms/ets"
    },
    "ets_version": ["ets1.1","ets1.2"]
}
```

### 配置项说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `isCompParame` | bool | 检查参数个数是否匹配 |
| `isCaseNames` | bool | 检查用例命名规范 |
| `permission_check` | bool | 检查接口权限覆盖 |
| `param_spec_check` | bool | 检查参数规格覆盖 |
| `return_check` | bool | 检查返回值覆盖 |
| `model_check` | bool | 检查 @stageModelonly 标签 |
| `atomic_check` | bool | 检查 @atomicservice |
| `case_path.open_source` | string[] | 开源用例目录名（相对 `testcase/`） |
| `case_path.closed_source` | string[] | 闭源用例目录名（相对 `testcase/`） |
| `api_path.open_source` | string | 开源 SDK .d.ts 文件路径（相对工具根目录） |
| `api_path.closed_source` | string | 闭源 SDK .d.ts 文件路径 |
| `ets_version` | string[] | ETS 版本文件夹名 |

### 扫描特定模块

要只扫描某个特定模块（如 `multimedia`），修改 `case_path` 缩小到模块子目录：

```json
{
    "case_path": {
        "open_source": ["xts_acts/multimedia"],
        "closed_source": []
    }
}
```

工具会只扫描 `testcase/xts_acts/multimedia/` 下的测试用例，API 侧仍匹配全量 SDK，结果报告中自然只出现该模块相关 API。

### 扫描特定子系统（动态配置）

**注意**：直接修改 `case_path` 为 `xts_acts/ability` 可能导致结果解析失败。

**推荐使用文件复制方式扫描特定子系统**：

#### 使用 manage_scan_env.py 工具

使用 `manage_scan_env.py` 工具自动复制子系统文件和 SDK 文件到扫描目录，并修改 `arkts_config.json`。

**优势**：
1. **稳定可靠**：文件复制方式确保扫描环境正常
2. **快速切换**：通过 setup/teardown 快速切换不同子系统
3. **自动配置**：工具自动修改 `arkts_config.json`，无需手动维护
4. **安全性**：仅删除副本，原始数据完全不受影响

**使用方法**：

**Step 1：准备扫描环境**

```powershell
python scripts/manage_scan_env.py setup --subsystem ability
```

此操作会：
1. 创建过滤目录 `testcase/xts_acts_filtered_ability/`
2. 复制子系统测试文件（从 `{xts_acts_path}\ability` 到过滤目录）
3. 复制 SDK 文件（从 `{sdk_path}\ets` 到扫描工具 SDK 目录）
4. 备份 `arkts_config.json` → `arkts_config.json.bak`
5. 修改 `case_path.open_source` 为 `["xts_acts_filtered_ability"]`

**复制操作可能耗时较长**（取决于子系统文件大小），脚本会显示源目录大小和复制进度。

**Step 2：运行覆盖率扫描**

```bash
cd APICoverageDetector
.\arkts_entrance\arkts_entrance.exe
```

扫描完成后，查看结果：
- 扫描结果：`results/ets1.1/open_source/sdk_result.xlsx`
- 结果只包含 ability 子系统相关的 API 和测试用例

**Step 3：恢复扫描环境** ⚠️ **危险操作 - 谨慎使用**

> **⛔ 重要警告**
>
> **一般情况下不应执行此步骤！**
>
> - **仅在以下情况执行**：用户明确要求恢复全量代码扫描环境，或需要清理配置时
> - **不要自动执行**：除非用户明确要求，否则模型不应主动执行此步骤
> - **误操作后果**：会导致配置丢失，恢复到全量扫描状态
>
> 如果需要恢复环境，请先确认用户明确要求，再执行以下命令：

```powershell
python scripts/manage_scan_env.py teardown --subsystem ability
```

脚本自动完成：
- 删除已复制的子系统文件副本（仅删除副本不影响源文件）
- 删除过滤目录
- 从备份恢复 `arkts_config.json`

**注意**：恢复操作由用户手动调用，不会自动执行。适用于完成工作后需要清理配置，或长时间工作后需要切换子系统时。

#### 目录结构示例

**准备前**：
```
APICoverageDetector/
├── testcase/
│   └── xts_acts/          # -> D:/xts_acts (文件复制，包含所有子系统)
└── configs/
    └── arkts_config.json  # case_path: ["xts_acts"]
```

**准备后**：
```
APICoverageDetector/
├── testcase/
│   ├── xts_acts/          # 原始目录（保留）
│   └── xts_acts_filtered_ability/  # 新建过滤目录
│       └── ability/          # -> D:/xts_acts/ability (文件复制，仅 ability)
└── configs/
    └── arkts_config.json  # case_path: ["xts_acts_filtered_ability"]
```

#### 支持的子系统

常用子系统示例：
- `ability` - Ability 框架
- `multimedia` - 多媒体
- `arkui` - ArkUI 框架
- `arkweb` - ArkWeb
- `testfwk` - 测试框架

#### 注意事项

1. **路径要求**：xts_acts 路径和 APICoverageDetector 路径必须使用绝对路径
2. **磁盘空间**：文件复制需要额外的磁盘空间，脚本会显示源目录大小
3. **扫描结果**：扫描结果文件保存在 `results/` 目录，命名不变
4. **多次扫描**：可以依次扫描多个子系统，每次 setup 都会创建独立的过滤目录
5. **失败处理**：如果扫描失败，仍需运行 teardown 清理过滤目录

### 执行

Windows PowerShell:
```powershell
"1`n1`nN" | .\arkts_entrance\arkts_entrance.exe
```

Linux bash:
```bash
echo -e "1\n1\nN\nN" | ./arkts_entrance/arkts_entrance.exe
```

工具启动后有 4 个交互输入：
1. 扫描源类型：`1`=开源、`2`=闭源、`3`=全部
2. API 类型：`1`=public、`2`=system
3. API 特性：`N`=无、`1`=跨平台、`2`=支持卡片、`3`=高阶API
4. API 版本：`N`=全部

---

## 五、C API 子系统扫描配置

配置文件：`APICoverageDetector/configs/c_config.json`

### 扫描特定模块

C API 提供更精细的模块过滤机制：

**方法一：修改 `test_case_project_paths`**

```json
{
    "test_case_project_paths": [
        "testcase/xts_acts/multimedia"
    ],
    "large_ts_handle": [
        "xts_acts/multimedia"
    ],
    "exclude_ts_handle": []
}
```

| 字段 | 说明 |
|------|------|
| `test_case_project_paths` | 用例工程路径列表，配置越具体扫描越快 |
| `large_ts_handle` | 大型测试套子目录检索列表（尾部匹配） |
| `exclude_ts_handle` | 排除目录（尾部匹配） |

**方法二：通过 `large_ts_handle` 精确到子系统**

默认配置了多个子系统，只保留目标模块即可：

```json
{
    "large_ts_handle": ["xts_acts/multimedia"]
}
```

### C 配置其他重要字段

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `ohos_sdk_path` | `sdk/openharmony` | 开源 SDK 路径 |
| `hms_sdk_path` | `sdk/hms` | 闭源 SDK 路径 |
| `useWhiteList` | `true` | 是否启用白名单 |
| `taskRun.sdk_parse` | `true` | SDK API 导出（更新 SDK 后需重新执行） |
| `taskRun.testsuite_parse` | `true` | 用例接口扫描 |
| `taskRun.calc_cover` | `true` | 计算覆盖情况 |
| `taskRun.cover_statistic` | `true` | 统计覆盖度信息 |
| `taskRun.format_excel` | `true` | 格式化输出 Excel |
| `logLevel` | `INFO` | 日志级别：DEBUG / VERBOSE / INFO |
| `processPool` | `0` | 最大并行任务数（0 = 系统核心数） |
| `isCompParame` | `true` | 检查参数个数 |
| `isCompParameType` | `true` | 检查参数类型 |
| `permission_check` | `true` | 检查权限覆盖 |
| `error_code_check` | `true` | 检查错误码覆盖 |
| `param_spec_check` | `true` | 检查参数规格覆盖 |
| `return_check` | `true` | 检查返回值覆盖 |
| `statistic_include_spec` | `true` | 统计报表包含参数规格 |
| `incremental_stat` | `false` | 增量统计开关 |

### 执行

```powershell
cd APICoverageDetector
.\c_entrance\c_entrance.exe
```

---

## 六、子系统扫描环境准备

覆盖率扫描环境由 skill 根据子系统名称通过文件复制方式自动准备。

### 环境准备流程

```
Phase 1 确定子系统 → Phase 2/9 扫描前: 准备扫描环境（setup） → 扫描 → 可选恢复环境（teardown）
```

### 自动环境准备特性

1. **零配置维护**：无需为每个子系统创建配置文件
2. **即时切换**：通过 --subsystem 参数即时切换扫描目标
3. **自动复制**：自动复制子系统文件和 SDK 文件到扫描目录，并修改配置
4. **统一流程**：所有子系统使用相同的 setup/teardown 流程（详见第五章「使用方法」）

---

## 七、SDK 和测试用例准备

### SDK 准备

1. 从 OpenHarmony 每日构建下载 SDK 并解压，确保包含 `build-tools/koala-wrapper/`（es2panda 解析依赖）。
2. 将 `interface_sdk-js` 仓库复制到 SDK 目录：

```powershell
# 使用 robocopy 将 SDK 仓库复制到扫描工具目录
robocopy D:\interface_sdk-js APICoverageDetector\sdk\openharmony\ets /E
```

注意：需复制整个仓库（非仅 `api/` 子目录），因为工具依赖仓库中的 `build-tools/` 等构建产物。

### 测试用例准备

将测试用例仓库复制到 `testcase/` 目录：

**子系统选择性扫描**：
使用 `manage_scan_env.py` 工具自动复制子系统文件（详见第五章「使用方法」）。

---

## 八、异步扫描流程

### 8.1 异步扫描工具

**工具位置**: `scripts/async_coverage_scan.py`

**功能**: 后台运行覆盖率扫描，支持状态监控、进度查看、结果获取

**使用方法**:
```bash
# 启动异步扫描
python scripts/async_coverage_scan.py start

# 查看扫描状态
python scripts/async_coverage_scan.py status

# 获取扫描结果
python scripts/async_coverage_scan.py results

# 停止扫描
python scripts/async_coverage_scan.py stop
```

**特点**:
- 后台运行，不阻塞其他操作
- 实时进度监控（10个扫描阶段）
- 自动状态管理和结果保存
- 支持长时间运行的覆盖率扫描

### 8.2 异步扫描工作流程

#### Phase 3 - 初始异步扫描

1. **启动扫描**:
   ```bash
   python scripts/async_coverage_scan.py start
   ```
   - 后台启动 `arkts_entrance.exe`
   - 自动配置交互参数（开源=1, public=1, 无特性=N, 全部版本=N）
   - 保存进程PID和状态信息

2. **监控进度**:
   ```bash
   python scripts/async_coverage_scan.py status
   ```
   - 返回当前状态、进度百分比、当前阶段
   - 10个扫描阶段的实时更新

3. **等待完成**:
   - 后台线程监控日志文件，自动解析进度
   - 扫描完成后自动更新状态文件
   - 结果保存在 `APICoverageDetector/results/`

#### Phase 8 - 验证异步扫描

1. **启动验证扫描**:
   ```bash
   python scripts/async_coverage_scan.py start
   ```

2. **监控和等待**:
   - 使用相同的监控方法查看进度
   - 与初始扫描保持异步操作

3. **结果对比**:
   - 两次扫描结果自动保存
   - 通过 `coverage_verifier.md` 进行对比分析

### 8.3 状态文件说明

- `coverage_scan.pid`: 当前扫描进程PID
- `coverage_scan.status`: 扫描状态（idle/running/completed/failed）
- `coverage_scan.progress`: 当前进度信息
- `coverage_scan.log`: 扫描日志文件

---

## 九、输出结果

扫描结果保存在 `results/` 目录，Excel 格式。

### ArkTS 输出文件

| 文件 | 说明 |
|------|------|
| `sdk_result.xlsx` | 覆盖度统计结果 |
| `all_collect.xlsx` | 全量用例覆盖明细 |
| `kit_collect.xlsx` | 按 Kit 分组的覆盖明细 |
| `arkts_white_list.xlsx` | 白名单 |
| `api_param_check.xlsx` | 参数规格检查结果 |

### C API 输出文件

| 文件 | 说明 |
|------|------|
| `C_API_覆盖度统计结果.xlsx` | 统计 + 明细汇总 |
| `c_result.xlsx` | 覆盖度统计 |
| `c_result_total.xlsx` | 用例覆盖明细 |
| `c_white_list.xlsx` | 白名单 |
| `api_param_check.xlsx` | 参数规格检查 |

### 统计维度

| 维度 | 说明 |
|------|------|
| 接口覆盖率 | System API / Public API |
| API 调用覆盖率 | API 是否被用例调用 |
| 入参覆盖率 | 参数组合覆盖情况 |
| 参数规格覆盖率 | 边界值、特殊值、类型检查 |
| 错误码覆盖率 | 已测试的错误码比例 |
| 权限覆盖率 | 已测试的权限场景 |
| 返回值覆盖率 | 已测试的返回值场景 |

---

## 十、白名单

白名单用于标记已知无法自动覆盖的 API，避免计入未覆盖率。

| 类型 | 说明 |
|------|------|
| 已覆盖 | 额外检查用例信息后确认已覆盖 |
| 本地覆盖 | 本地环境覆盖，但不在 XTS 仓库中 |
| 澄清无法覆盖 | 经澄清确认不需要覆盖 |
| 单独代码仓 | 在其他代码仓中覆盖 |
| 手工用例 | 通过手工用例覆盖 |

白名单文件：
- ArkTS：`configs/arkts_white_list.xlsx`
- C API：`configs/c_white_list.xlsx`

---

## 十一、Kit → 子系统映射（C API 参考）

| Kit | filter 关键词 | 子系统 |
|-----|--------------|--------|
| AudioKit | `ohaudio/` | 音频 |
| CameraKit | `ohcamera/` | 相机图库框架 |
| MediaKit | `player_framework/` | 视频框架 |
| NetworkKit | `netmanager/`, `netstack/` | 网络管理 |
| ConnectivityKit | `bluetooth/`, `wifi/` | 蓝牙/基础通信 |
| TelephonyKit | `cellular_data/` | 电话服务 |
| DriverDevelopmentKit | `ddk/`, `usb/` | 驱动 |
| ArkGraphics2D | `native_drawing/`, `native_window/` | 图形图像 |
| ArkData | `database/` | 分布式数据管理 |
| ArkUI | `arkui/`, `window_manager/` | ArkUI/窗口管理 |
| ArkWeb | `web/` | web |
| CoreFileKit | `filemanagement/` | 文件管理 |
| IPCKit | `IPCKit/` | 基础通信 |
| LocalizationKit | `rawfile/`, `resource_manager/`, `i18n/` | 全球化 |
| CryptoArchitectureKit | `CryptoArchitectureKit/` | 安全基础能力 |
| NotificationKit | `NotificationKit/` | 事件通知 |

完整映射见 `configs/_configs/c_module_subsys.json`。

---

## 十二、注意事项

1. **SDK 依赖**：ArkTS 扫描依赖 `interface_sdk-js` 仓库中的 `build-tools/koala-wrapper/`（es2panda），需确保 SDK 完整。首次扫描或 SDK 更新后 `taskRun.sdk_parse` 会自动解析，耗时较长。

2. **扫描耗时**：全量扫描耗时长，缩小 `test_case_project_paths` 到具体模块可大幅加速。

3. **并行度**：`processPool` 设为 `0` 使用全部 CPU 核心，扫描速度最快。

4. **增量统计**：`incremental_stat` 设为 `true` 可只统计增量变化。

5. **日志排查**：扫描异常时查看 `log/` 目录，`logLevel` 可临时改为 `DEBUG`。

6. **配置备份**：默认配置已备份为 `arkts_config.json.bak`，`manage_scan_env.py teardown` 会从备份恢复原始配置。

7. **Windows 环境**：工具为 Windows 可执行文件，Linux 环境需要通过 Wine 运行。

---

## 十三、故障排查

| 问题 | 排查方向 |
|------|---------|
| `Cannot find module './build-tools/koala-wrapper/build/lib/es2panda'` | SDK 不完整，需从每日构建下载完整 SDK 并复制到扫描工具目录 |
| `EOFError: EOF when reading a line` | 管道输入不足，工具需 4 个交互输入（开源/闭源、public/system、API特性、API版本） |
| 扫描结果为空 | 检查 `case_path` 和 `api_path` 配置路径是否正确，确认测试用例和 SDK 文件存在 |
| 覆盖率数据异常 | 检查白名单配置、用例命名规范、API 声明文件完整性 |
| 权限不足无法删除扫描副本目录 | 使用 `cmd /c "rmdir /s /q <path>"` 强制删除 |

---

## 十四、与 coverage_analyzer.md 的配合

| 工具 | 特点 | 适用场景 |
|------|------|---------|
| `coverage_analyzer.md` | 基于测试文件分析，轻量级快速 | Flow A（有覆盖率报告）时的风格扫描 |
| `APICoverageDetector` | 精确扫描工具，重量级全面 | Flow B（无覆盖率报告）时的精确扫描 |

两者可以配合使用，APICoverageDetector 提供精确数据，coverage_analyzer.md 提供快速分析。
