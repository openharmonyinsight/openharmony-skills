# 跨平台配置指南

## 概述

`ohos-test-arkts-xts-generation` 支持跨平台配置，支持 Windows 原生、WSL 和 Linux 三种运行环境。配置文件使用扁平结构，通过 `platform` 字段标识当前运行环境，所有路径位于同一层级。本指南说明如何正确配置跨平台路径。

## 配置文件结构

配置文件 `.oh-xts-config.json` 使用扁平 JSON 结构：

```json
{
  "platform": "wsl",
  "OH_ROOT": "/path/to/ohos",
  "scan_tool_root": "/mnt/d/APICoverageDetector",
  "skill_root": "/path/to/skills/ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "xts_acts_path": "[auto-derived from OH_ROOT if not set]",
  "sdk_path": "[auto-derived from OH_ROOT if not set]",
  "sdk_local_path": "[wsl only] Linux local SDK path",
  "use_builtin_sdk": true,
  "deveco_studio_path": "[windows only]",
  "hvigor_path_1.1": "[windows only]",
  "hvigor_path_1.2": "[windows only]",
  "docs_path": "[auto-derived from OH_ROOT if not set]"
}
```

### 字段说明

| 字段 | 必需 | 适用平台 | 说明 |
|------|------|---------|------|
| **platform** | **必需** | 全部 | 运行环境：`"wsl"` / `"windows"` / `"linux"` |
| **OH_ROOT** | **必需** | 全部 | OpenHarmony 根目录，用于构建、编译等操作 |
| **scan_tool_root** | **必需** | 全部 | APICoverageDetector 工具路径 |
| **skill_root** | **必需** | 全部 | 本 skill 的安装路径 |
| **ets_version** | **必需** | 全部 | ETS 版本列表，如 `["ets1.1"]` |
| **xts_acts_path** | 可选 | 全部 | XTS 测试用例路径，未设置时从 `OH_ROOT` 自动推导 |
| **sdk_path** | 可选 | 全部 | SDK 路径，未设置时从 `OH_ROOT` 自动推导 |
| **sdk_local_path** | 可选 | WSL | WSL 本地 SDK 路径（Linux 格式） |
| **use_builtin_sdk** | 可选 | 全部 | 是否使用内置 SDK，默认 `true` |
| **deveco_studio_path** | 可选 | Windows | DevEco Studio 安装路径，自动推导 Java 和 Node.js 路径 |
| **hvigor_path_1.1** | 可选 | Windows | ArkTS-Dyn 构建工具路径 |
| **hvigor_path_1.2** | 可选 | Windows | ArkTS-Sta 构建工具路径 |
| **docs_path** | 可选 | 全部 | 文档路径，未设置时从 `OH_ROOT` 自动推导 |

### 路径自动推导规则

以下路径在未显式配置时，将从 `OH_ROOT` 自动推导：

| 字段 | 推导规则 | 示例 |
|------|---------|------|
| **xts_acts_path** | `${OH_ROOT}/xts/acts` | `/home/user/ohos/xts/acts` |
| **sdk_path** | `${OH_ROOT}/sdk` | `/home/user/ohos/sdk` |
| **docs_path** | `${OH_ROOT}/docs` | `/home/user/ohos/docs` |

> **优先级**：显式配置 > 自动推导。如果提供了字段值，将直接使用而不再推导。

## 运行环境说明

| 环境 | `platform` 值 | APICoverageDetector | 路径格式 | 检测方式 |
|------|-------------|---------------------|---------|---------|
| **Windows 原生** | `windows` | 直接运行 `.exe` | `D:\path\to\...` | `sys.platform == 'win32'` |
| **WSL** | `wsl` | 通过 `/mnt/d/...` 调用 `.exe` | `/mnt/d/path/to/...` | `is_wsl()` 检测 `/proc/version` 含 `microsoft` |
| **纯 Linux** | `linux` | 不可用 | `/home/user/...` | `sys.platform == 'linux' and not is_wsl()` |

> **WSL 关键特性**：WSL 环境下 `sys.platform` 为 `linux`，但可以通过 `/mnt/d/...` 路径直接调用 Windows 侧的 `.exe` 工具。脚本通过检测 `/proc/version` 中是否包含 `microsoft` 来区分 WSL 和纯 Linux。

## 路径使用场景

### hvigor_path 版本化配置详解

**hvigor 是什么**：
- DevEco Studio 的构建工具
- OpenHarmony 项目的编译和打包工具
- 类似于 Android 的 Gradle

**为什么需要两个 hvigor 路径**：
- ArkTS-Dyn（动态语法）和 ArkTS-Sta（静态语法）使用不同版本的 hvigor 工具
- ArkTS-Dyn 通常使用 DevEco Studio 自带的 hvigor（路径如 `tools/hvigor/bin`）
- ArkTS-Sta 需要特定版本的 hvigor 工具，路径可能与 ArkTS-Dyn 不同

**路径说明**：
- `hvigor_path_1.1`：用于 ArkTS-Dyn 动态语法项目的编译
- `hvigor_path_1.2`：用于 ArkTS-Sta 静态语法项目的编译
- 两者包含的可执行文件相同：`hvigorw.bat` (Windows) 或 `hvigorw.sh` (Linux)

**查找路径方法**：
1. 打开 DevEco Studio
2. 点击 `File` -> `Settings` -> `Build, Execution, Deployment` -> `Build Tools`
3. 查看 `HarmonyOS SDK Location` 和 `Hvigor Path` 配置

## 各平台配置示例

### Windows 环境配置

```json
{
  "platform": "windows",
  "OH_ROOT": "D:\\path\\to\\ohos",
  "scan_tool_root": "D:\\path\\to\\APICoverageDetector",
  "skill_root": "D:\\path\\to\\skills\\ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "xts_acts_path": "D:\\path\\to\\xts_acts",
  "sdk_path": "D:\\path\\to\\sdk\\openharmony\\ets-windows-x64-26.0.0.20-Beta",
  "deveco_studio_path": "D:\\path\\to\\DevEco Studio",
  "hvigor_path_1.1": "D:\\path\\to\\hvigor\\bin",
  "hvigor_path_1.2": "D:\\path\\to\\hvigor_static\\bin",
  "docs_path": "D:\\path\\to\\docs",
  "use_builtin_sdk": true
}
```

**说明**：
- `platform`: 设为 `"windows"`，所有路径使用 Windows 格式
- `OH_ROOT`: OpenHarmony 源码根目录，Windows 路径格式
- `xts_acts_path`: 显式指定 XTS 测试路径（也可从 `OH_ROOT` 自动推导）
- `sdk_path`: SDK 路径，Windows 环境必需
- `deveco_studio_path`: DevEco Studio 安装路径，自动推导 Java（`jbr/`）和 Node.js（`tools/node/`）路径
- `hvigor_path_1.1`: ArkTS-Dyn 编译必需
- `hvigor_path_1.2`: ArkTS-Sta 编译必需

### Linux 环境配置

```json
{
  "platform": "linux",
  "OH_ROOT": "/home/user/openharmony",
  "scan_tool_root": "/home/user/APICoverageDetector",
  "skill_root": "/home/user/.opencode/skills/ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "use_builtin_sdk": true
}
```

**说明**：
- `platform`: 设为 `"linux"`
- `OH_ROOT`: OpenHarmony 源码根目录，Linux 路径格式
- `xts_acts_path`、`sdk_path`、`docs_path`: 未设置时从 `OH_ROOT` 自动推导
- Linux 环境通常不需要 `deveco_studio_path` 和 `hvigor_path`

### WSL 环境配置

```json
{
  "platform": "wsl",
  "OH_ROOT": "/home/chen/ohos",
  "scan_tool_root": "/mnt/d/APICoverageDetector",
  "skill_root": "/home/chen/.opencode/skills/ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "sdk_local_path": "/home/chen/.sdk/ets",
  "use_builtin_sdk": true
}
```

**说明**：
- `platform`: 设为 `"wsl"`
- `OH_ROOT`: 使用 Linux 路径格式，指向 WSL 本地的 OpenHarmony 源码
- `scan_tool_root`: 使用 `/mnt/d/...` 格式，指向 Windows 侧的 APICoverageDetector
- `sdk_local_path`: WSL 专用，指定 Linux 本地的 SDK 路径
- `xts_acts_path`、`sdk_path`、`docs_path`: 未设置时从 `OH_ROOT` 自动推导
- WSL 环境下路径直接从 `OH_ROOT` 读取，不再需要从 Windows 路径转换

**WSL 路径解析规则**（优先级从高到低）：

1. **显式配置**：直接使用配置文件中指定的路径值
2. **`OH_ROOT` 推导**：未显式配置的路径从 `OH_ROOT` 自动推导
3. **`sdk_local_path`**：WSL 专用的本地 SDK 路径，优先于 `sdk_path` 使用

## 路径格式规范

### 1. Windows 路径格式

```json
// 方式1：使用双反斜杠（推荐）
"xts_acts_path": "D:\\work\\xts_acts"

// 方式2：使用正斜杠
"xts_acts_path": "D:/work/xts_acts"

// 方式3：使用相对路径
"sdk_path": "sdk/openharmony/ets"
"hvigor_path_1.1": "DevEco Studio/tools/hvigor/bin"
"hvigor_path_1.2": "hvigor-static/tools/hvigor/bin"
```

### 2. Linux 路径格式

```json
// 绝对路径（推荐）
"OH_ROOT": "/home/user/openharmony"

// 相对路径
"sdk_path": "sdk/ohos/ets"
```

### 3. WSL 路径格式

```json
// scan_tool_root 使用 /mnt/ 格式访问 Windows 侧工具
"scan_tool_root": "/mnt/d/APICoverageDetector"

// OH_ROOT 使用 Linux 本地路径
"OH_ROOT": "/home/chen/ohos"

// sdk_local_path 使用 Linux 本地路径
"sdk_local_path": "/home/chen/.sdk/ets"

// 未显式设置的路径从 OH_ROOT 自动推导（Linux 格式）
// xts_acts_path → /home/chen/ohos/xts/acts
// sdk_path → /home/chen/ohos/sdk
// docs_path → /home/chen/ohos/docs
```

### 4. 路径格式注意事项

1. **不要混合路径分隔符**
   ```json
   // ❌ 错误：混合使用反斜杠和正斜杠
   "xts_acts_path": "D:/work\\xts_acts"
   
   // ✅ 正确：统一使用正斜杠
   "xts_acts_path": "D:/work/xts_acts"
   ```

2. **使用正确的转义**
   ```json
   // JSON 文件中需要双重转义
   "xts_acts_path": "D:\\work\\xts_acts"
   ```

3. **路径长度限制**
   - Windows: 最大 260 字符（启用长路径支持除外）
   - Linux: 一般无限制

## 配置验证

### 1. 自动验证工具

```bash
# 验证当前平台配置的有效性
python scripts/config_validator.py

# 查看配置状态（已集成在验证命令中）
```

### 2. 验证内容

验证器根据 `platform` 字段选择对应的验证逻辑：

**Windows 环境（`platform: "windows"`）验证**：
- ✅ 检查 `platform` 字段值为 `"windows"`
- ✅ 检查 `OH_ROOT` 是否存在且可访问
- ✅ 检查 `xts_acts_path` 是否存在（显式或从 `OH_ROOT` 推导）
- ✅ 检查 `sdk_path` 是否存在且可访问
- ✅ 检查 `hvigor_path_1.1` 是否存在且可访问
- ✅ 检查 `hvigor_path_1.2` 是否存在且可访问（如需 ArkTS-Sta 编译）

**Linux 环境（`platform: "linux"`）验证**：
- ✅ 检查 `platform` 字段值为 `"linux"`
- ✅ 检查 `OH_ROOT` 是否存在且可访问
- ✅ 检查自动推导的路径是否存在

**WSL 环境（`platform: "wsl"`）验证**：
- ✅ 检查 `platform` 字段值为 `"wsl"`
- ✅ 检查 `OH_ROOT` 是否存在且可访问（Linux 本地路径）
- ✅ 检查 `scan_tool_root` 指向的 `/mnt/d/APICoverageDetector` 是否存在
- ✅ 检查 `sdk_local_path` 是否存在（若已配置）
- ✅ 检查自动推导的路径是否存在
- ✅ 检查 WSL interop 是否启用（`.exe` 可执行性）

### 3. hvigor_path 验证要点

**Windows 环境验证**：
```bash
# 检查 ArkTS-Dyn hvigor 目录是否存在
dir "D:\DevEco Studio\DevEco Studio\tools\hvigor\bin"

# 检查 ArkTS-Sta hvigor 目录是否存在
dir "D:\path\to\hvigor_static\bin"

# 检查关键文件是否存在
dir "D:\DevEco Studio\DevEco Studio\tools\hvigor\bin\hvigorw.bat"
dir "D:\path\to\hvigor_static\bin\hvigorw.bat"
```

**Linux 环境验证**：
```bash
# 检查 ArkTS-Dyn hvigor 目录是否存在
ls -la /opt/DevEco-Studio/tools/hvigor/bin

# 检查 ArkTS-Sta hvigor 目录是否存在
ls -la /opt/hvigor-static/tools/hvigor/bin

# 检查关键文件是否存在
ls -la /opt/DevEco-Studio/tools/hvigor/bin/hvigorw.sh
ls -la /opt/hvigor-static/tools/hvigor/bin/hvigorw.sh
```

## 常见配置场景

### 场景1：Windows 开发环境

```json
{
  "platform": "windows",
  "OH_ROOT": "D:\\work\\ohos",
  "scan_tool_root": "D:\\tools\\APICoverageDetector",
  "skill_root": "D:\\tools\\skills\\ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "xts_acts_path": "D:\\work\\xts_acts",
  "sdk_path": "D:\\work\\sdk\\openharmony\\ets",
  "hvigor_path_1.1": "D:\\path\\to\\hvigor\\bin",
  "hvigor_path_1.2": "D:\\path\\to\\hvigor_static\\bin",
  "use_builtin_sdk": true
}
```

**用途**：
- 本地 Windows 环境进行测试生成
- `OH_ROOT` 作为路径推导的根目录
- `hvigor_path_1.1` 用于 ArkTS-Dyn 项目构建
- `hvigor_path_1.2` 用于 ArkTS-Sta 项目构建

### 场景2：Linux 构建服务器

```json
{
  "platform": "linux",
  "OH_ROOT": "/opt/openharmony",
  "scan_tool_root": "/opt/APICoverageDetector",
  "skill_root": "/opt/skills/ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "use_builtin_sdk": true
}
```

**用途**：
- Linux 服务器进行测试生成和构建
- `xts_acts_path`、`sdk_path`、`docs_path` 从 `OH_ROOT` 自动推导
- 所有路径使用 Linux 格式

### 场景3：WSL 开发环境

```json
{
  "platform": "wsl",
  "OH_ROOT": "/home/chen/ohos",
  "scan_tool_root": "/mnt/d/APICoverageDetector",
  "skill_root": "/home/chen/.opencode/skills/ohos-test-arkts-xts-generation",
  "ets_version": ["ets1.1"],
  "sdk_local_path": "/home/chen/.sdk/ets",
  "use_builtin_sdk": true
}
```

**用途**：
- 在 WSL 中使用 opencode CLI 运行测试生成
- APICoverageDetector 的 `.exe` 通过 `/mnt/d/...` 路径调用
- `sdk_local_path` 指定 WSL 本地的 SDK 路径
- `xts_acts_path` 等路径从 `OH_ROOT` 自动推导

### 场景4：多环境切换

不同环境使用不同的配置文件，通过 `platform` 字段区分：

```bash
# Windows 环境
cp .oh-xts-config.windows.json .oh-xts-config.json

# Linux 环境
cp .oh-xts-config.linux.json .oh-xts-config.json

# WSL 环境
cp .oh-xts-config.wsl.json .oh-xts-config.json
```

每个配置文件的 `platform` 字段和路径格式不同，但结构一致。

## 故障排除

### 1. platform 字段缺失或无效

**问题**：
```
❌ platform: 字段缺失或值无效（必须为 "wsl" | "windows" | "linux"）
```

**解决方法**：
1. 确认配置文件中包含 `"platform"` 字段
2. 确认值为 `"wsl"`、`"windows"` 或 `"linux"` 之一

### 2. OH_ROOT 路径不存在

**问题**：
```
❌ OH_ROOT: 路径不存在 - /path/to/ohos
```

**解决方法**：
1. 检查路径是否存在
2. 确认当前用户是否有访问权限
3. 检查路径挂载状态（WSL 下检查 `/mnt/` 挂载）

### 3. 自动推导路径不存在

**问题**：
```
⚠️ xts_acts_path (auto-derived): /path/to/ohos/xts/acts 不存在
```

**解决方法**：
1. 检查 `OH_ROOT` 下的目录结构是否符合预期
2. 若实际路径不同，在配置文件中显式指定该字段
3. 显式配置优先于自动推导

### 4. hvigor 路径配置错误

**问题**：
构建失败，提示找不到 hvigor 工具。

**解决方法**：
1. 检查 `hvigor_path_1.1` 和 `hvigor_path_1.2` 配置是否正确
2. 确认路径包含正确的可执行文件：
   - Windows: `hvigorw.bat`
   - Linux: `hvigorw.sh`
3. 检查路径访问权限
4. 注意：ArkTS-Dyn 和 ArkTS-Sta 使用不同版本的 hvigor，需分别配置

### 5. WSL 下 .exe 无法执行

**问题**：
在 WSL 中调用 `/mnt/d/APICoverageDetector/arkts_entrance/arkts_entrance.exe` 报错 `Permission denied` 或 `command not found`。

**解决方法**：
1. 检查 WSL interop 是否启用：
   ```bash
   cat /proc/sys/fs/binfmt_misc/WSLInterop
   # 应输出 enabled 相关内容
   ```
2. 若未启用，在 `/etc/wsl.conf` 中确认未禁用 interop：
   ```ini
   [interop]
   enabled=true
   appendWindowsPath=true
   ```
3. 重启 WSL：在 PowerShell 中运行 `wsl.exe --shutdown`，然后重新打开

### 6. WSL 下 /mnt/ 路径不可访问

**问题**：
配置中的 `/mnt/d/...` 路径报告不存在，但 Windows 侧路径确实存在。

**解决方法**：
1. 检查 `/mnt/d/` 挂载是否正常：
   ```bash
   ls /mnt/d/
   ```
2. 若挂载异常，手动挂载：
   ```bash
   sudo mkdir -p /mnt/d
   sudo mount -t drvfs D: /mnt/d
   ```
3. 确认 `OH_ROOT` 使用的是 WSL 本地 Linux 路径，而非 `/mnt/` 路径

## 最佳实践

### 1. 配置文件管理

1. **版本控制**：
   - 配置文件 `.oh-xts-config.json` 通常包含本地路径
   - 建议创建 `.oh-xts-config.example.json` 作为模板
   - 模板文件可以安全地提交到版本控制

2. **多环境管理**：
   - 为不同平台维护独立的配置文件
   - 通过 `platform` 字段明确标识当前环境
   - 参考 `docs/CROSS_PLATFORM_CONFIG.md` 获取详细说明

### 2. 路径配置建议

1. **优先使用 OH_ROOT 推导**：
   ```json
   // ✅ 推荐：只设置 OH_ROOT，其他路径自动推导
   {
     "platform": "linux",
     "OH_ROOT": "/home/user/openharmony"
   }
   
   // ⚠️  仅在实际路径与推导路径不同时才显式指定
   {
     "platform": "linux",
     "OH_ROOT": "/home/user/openharmony",
     "xts_acts_path": "/custom/path/to/xts_acts"
   }
   ```

2. **使用绝对路径**：
   - 推荐所有显式配置的路径使用绝对路径
   - 避免使用相对路径，防止工作目录变化导致问题

3. **定期验证**：
   - 在部署或环境变更后验证配置
   - 运行 `python scripts/config_validator.py` 检查有效性

### 3. 开发工作流

1. **首次设置**：
   ```bash
   # 复制模板
   cp .oh-xts-config.example.json .oh-xts-config.json
   
   # 编辑配置：设置 platform 和 OH_ROOT
   # 其他路径按需显式指定，否则自动推导
   
   # 验证配置
   python scripts/config_validator.py
   ```

2. **环境切换**：
   - 切换平台时，更新 `platform` 字段和对应路径
   - 运行验证确保新配置正确

3. **持续集成**：
   - 在 CI/CD 流程中集成配置验证
   - 确保构建环境配置正确

## 总结

- ✅ **支持三种运行环境**：通过 `platform` 字段区分 `"windows"` / `"wsl"` / `"linux"`
- ✅ **扁平配置结构**：所有路径位于同一层级，无嵌套平台段
- ✅ **路径自动推导**：`xts_acts_path`、`sdk_path`、`docs_path` 从 `OH_ROOT` 自动推导
- ✅ **显式覆盖**：需要时可显式指定任意路径，优先级高于自动推导
- ✅ **自动环境检测**：通过 `/proc/version` 区分 WSL 和纯 Linux
- ✅ **自动验证机制**：验证器根据 `platform` 字段执行对应的验证逻辑
- ✅ **清晰的文档说明**：详细说明各路径的使用场景
- ✅ **hvigor 版本化支持**：ArkTS-Dyn 和 ArkTS-Sta 使用独立的 hvigor 工具路径配置

通过正确配置跨平台路径，确保 ohos-test-arkts-xts-generation 在不同环境下都能正常工作。
