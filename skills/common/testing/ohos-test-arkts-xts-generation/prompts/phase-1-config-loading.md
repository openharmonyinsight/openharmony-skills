## Phase 1: Determine Subsystem Configuration

### 步骤 0: 配置文件初始化（首次使用自动触发）

**检查配置文件是否存在**：

```
读取 {skill_root}/.oh-xts-config.json
```

**如果配置文件不存在**，执行以下初始化流程：

1. 将 `.oh-xts-config.example.json` 复制为 `.oh-xts-config.json`（包含完整字段和占位符）。

2. **检测当前平台**：使用 `platform.system()` 或 `uname` 判断 Windows/Linux。

3. 从用户消息中提取路径信息，自动填充配置。识别以下模式：
   - XTS 仓库路径：匹配 "xts 仓库在/是 X:\xxx"、"xts_acts" 等关键词
   - SDK 路径：匹配 "SDK 在/是 X:\xxx"、"interface_sdk" 等关键词
   - DevEco Studio：匹配 "DevEco Studio" 等关键词

4. 如果用户消息中未包含路径，**根据平台向用户询问**：

   **Windows 环境**：
   ```
   我需要一些环境信息来配置工具：

   必填：
   1. XTS 测试仓库路径（如 D:\xts_acts_0414）
   2. SDK 接口定义路径（如 D:\interface_sdk-js\ets）

   可选（推荐填写，可解锁编译验证和覆盖率扫描功能）：
   3. DevEco Studio 安装路径（如 D:\DevEco Studio，填后自动配置 Java/Node.js/hvigor）
   4. APICoverageDetector 安装路径（如 D:\APICoverageDetector，用于覆盖率扫描）
   5. ArkTS-Sta 静态编译 Hvigor 路径（仅做静态语法项目编译时需要）
   6. 文档路径（如 D:\docs）

   请提供以上路径，我会自动完成配置。不确定的可以跳过，后续再补充。
   ```

   **Linux 环境**：
   ```
   我需要一些环境信息来配置工具：

   必填：
   1. OpenHarmony 根目录（如 /home/user/openharmony）

   其他路径将从根目录自动推导，无需手动配置。

   注意：APICoverageDetector 仅支持 Windows，Linux 环境下覆盖率扫描不可用，可提供已有扫描结果。
   ```

   自动推导（Linux）：从 `for_linux.OH_ROOT` 推导：
   - `xts_acts_path` = `{OH_ROOT}/test/xts/acts`
   - `sdk_path` = `{OH_ROOT}/interface/sdk-js/ets`
   - `docs_path` = `{OH_ROOT}/docs`
   推导路径不存在时向用户确认实际位置。

5. **自动推导**（Windows）：对于用户未提供的可选路径，从 `deveco_studio_path` 推导：
   - `hvigor_path_1.1` = `{deveco_studio_path}\{DevEco Studio}\tools\hvigor\bin`（自动检测子目录）
   - Java = `{deveco_studio_path}\{DevEco Studio}\jbr`
   - Node.js = `{deveco_studio_path}\{DevEco Studio}\tools\node\node.exe`
   无法推导的保持占位符，不阻断流程。

6. 将用户提供的路径写入 `.oh-xts-config.json`，格式参考 `.oh-xts-config.example.json`。

7. 验证所有必填路径存在且可访问，对不存在的路径给出明确提示。

**如果配置文件已存在**，直接验证路径有效性后进入步骤 1。

**路径有效性验证**（按平台）：

| 平台 | 必须存在 | 建议存在 | 可选 |
|------|---------|---------|------|
| Windows | `for_windows.xts_acts_path`、`for_windows.sdk_path` | `for_windows.deveco_studio_path`、`for_windows.hvigor_path_1.1` | `scan_tool_root`、`for_windows.hvigor_path_1.2`、`for_windows.docs_path` |
| Linux | `for_linux.OH_ROOT` | — | `for_linux.*`、`for_windows.*`（跨平台备用） |

对于无效路径，给出警告但不阻断流程（用户可能只需要用例生成，不需要编译验证）。

### 步骤 1: 确定 ETS 版本（交互式询问）

如果用户未明确指定生成 1.1 还是 1.2 的测试用例，需要交互式询问用户。

直接向用户提问（以下仅为交互逻辑说明，实际由模型直接提问并解析回复）：

```
请选择要生成的测试用例版本：
1) ArkTS-Dyn - 动态语法项目
2) ArkTS-Sta - 静态语法项目
3) 两者都生成
```

**说明**：
- ArkTS-Dyn（ets1.1）：动态语法项目，默认选择
- ArkTS-Sta（ets1.2）：静态语法项目，需额外配置 Hvigor 1.2 路径
- 两者都生成：同时生成两种语法版本的测试用例

**重要**：配置文件必须使用数组格式：
```json
{ "ets_version": ["ets1.1"] }
```
或
```json
{ "ets_version": ["ets1.1", "ets1.2"] }
```

### 步骤 2: 同步 ETS 版本配置（仅 Windows + 需要覆盖率扫描时）

将 `.oh-xts-config.json` 中的 `ets_version` 同步到 `APICoverageDetector/configs/arkts_config.json`：

```bash
python {skill_root}/scripts/sync_ets_version.py
```

Linux 环境或不需要覆盖率扫描时跳过此步骤。

### 步骤 3: 加载全局配置

读取 `.oh-xts-config.json` 获取全局环境变量和路径配置：

**配置字段**：

| 字段 | 用途 | 平台 |
|------|------|------|
| `skill_root` | 技能根目录，所有相对路径的基准 | 全平台 |
| `scan_tool_root` | APICoverageDetector 目录 | 仅 Windows |
| `for_windows.xts_acts_path` | XTS 测试仓库根目录 | Windows |
| `for_windows.sdk_path` | SDK `.d.ts` 文件目录 | Windows |
| `for_windows.deveco_studio_path` | DevEco Studio 安装目录，自动推导 Java/Node.js/hvigor | Windows |
| `for_windows.hvigor_path_1.1` | 动态语法编译工具 | Windows |
| `for_windows.hvigor_path_1.2` | 静态语法编译工具 | Windows（仅 ArkTS-Sta） |
| `for_linux.OH_ROOT` | OpenHarmony 源码根目录 | Linux |

### 步骤 4: 加载核心配置

```
references/subsystems/_common.md
```

### 步骤 5: 确定子系统

根据用户请求确定目标子系统。检查是否已有子系统配置：

```bash
ls references/subsystems/{Subsystem}/
```

### 步骤 6: 加载配置链

按优先级加载配置：

```
1. references/subsystems/_common.md          (核心配置，必须)
2. references/subsystems/{Subsystem}/_common.md  (子系统配置，如有)
3. references/subsystems/{Subsystem}/{Module}.md  (模块配置，如需)
```

### 步骤 7: 覆盖率扫描环境准备

覆盖率扫描环境将在 Phase 2 执行扫描时通过文件复制自动准备，无需在本阶段操作。

**环境准备时机**：
- **Phase 2 Flow B（执行 APICoverageDetector 扫描时）**：由 `manage_scan_env.py` 脚本自动复制子系统文件和 SDK 文件到扫描目录，并修改 `arkts_config.json`，详见 `prompts/phase-2-coverage.md` 步骤 1
- **Phase 1**：无需操作，跳过此步骤

**说明**：
- 覆盖率扫描环境通过文件复制方式准备
- 文件的复制、检查和清理均在 Phase 2 中通过 `manage_scan_env.py` 处理

### 步骤 8: 确定需加载的模块

根据子系统类型和任务类型，确定需要加载的 L1-L4 模块（参考 SKILL.md 模块注入映射表）。

**仅加载当前阶段和后续阶段需要的模块，不要一次性加载所有模块。**

### 步骤 9: 确定项目语法类型（仅当用户指定在某个测试工程中添加用例时执行）

检查该工程的 `build-profile.json5` 中的 `arkTSVersion` 字段：
- 存在 `"arkTSVersion": "1.2"` → 静态项目
- 不存在 → 动态项目

根据用户意图与工程语法的匹配关系，采取不同策略：

| 用户要求 | 工程实际语法 | 处理方式 |
|----------|-------------|---------|
| 指定动态语法 | 静态工程 | **提示冲突**，请用户确认是否继续在静态工程中生成动态语法用例（将无法通过编译） |
| 指定静态语法 | 动态工程 | **提示冲突**，请用户确认是否继续在动态工程中生成静态语法用例（将无法通过编译） |
| 未指定语法要求 | 静态工程 | 按静态语法生成 |
| 未指定语法要求 | 动态工程 | 按动态语法生成 |

如果用户未指定具体测试工程（如仅提供 API 名称或子系统名称），则跳过此步骤，默认按动态语法处理。
