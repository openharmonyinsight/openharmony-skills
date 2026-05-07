# 跨平台配置指南

## 概述

`ohos-test-arkts-xts-generation` 支持跨平台配置，不同平台的路径在对应平台下使用。本指南说明如何正确配置跨平台路径。

## 跨平台配置机制

### 1. 路径使用场景

| 配置项 | Windows 环境 | Linux 环境 | 用途说明 |
|-------|-------------|-----------|---------|
| **OH_ROOT** | 可选（Linux路径） | **必需** | OpenHarmony 根目录，用于构建、编译等操作 |
| **xts_acts_path** | **必需** | 可选 | XTS 测试用例本地路径，用于覆盖率扫描 |
| **sdk_path** | **必需** | 可选 | SDK 路径，用于 API 定义读取 |
| **deveco_studio_path** | **必需** | 可选 | DevEco Studio 安装路径，自动推导 Java（`jbr/`）和 Node.js（`tools/node/`）路径 |
| **hvigor_path_1.1** | **必需** | 可选 | DevEco Studio 构建工具路径，用于 ArkTS-Dyn（动态语法）项目编译 |
| **hvigor_path_1.2** | **必需** | 可选 | Hvigor 构建工具路径，用于 ArkTS-Sta（静态语法）项目编译 |
| **docs_path** | 可选 | 可选 | 文档路径，用于文档相关操作 |

### 2. hvigor_path 版本化配置详解

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

**示例路径**：
```json
// Windows 环境示例
"hvigor_path_1.1": "D:\\path\\to\\hvigor\\bin",
"hvigor_path_1.2": "D:\\path\\to\\hvigor_static\\bin"

// Linux 环境示例
"hvigor_path_1.1": "/opt/DevEco-Studio/tools/hvigor/bin",
"hvigor_path_1.2": "/opt/hvigor-static/tools/hvigor/bin"
```

**查找路径方法**：
1. 打开 DevEco Studio
2. 点击 `File` -> `Settings` -> `Build, Execution, Deployment` -> `Build Tools`
3. 查看 `HarmonyOS SDK Location` 和 `Hvigor Path` 配置

### 3. 跨平台配置示例

#### Windows 环境配置

```json
{
  "for_linux": {
    "OH_ROOT": "/path/to/ohroot"
  },
  "for_windows": {
    "xts_acts_path": "D:\\path\\to\\xts_acts",
    "sdk_path": "sdk/openharmony/ets-windows-x64-26.0.0.20-Beta",
    "hvigor_path_1.1": "D:\\path\\to\\hvigor\\bin",
    "hvigor_path_1.2": "D:\\path\\to\\hvigor_static\\bin",
    "docs_path": "D:\\path\\to\\docs"
  }
}
```

**说明**：
- `for_linux.OH_ROOT`: 保留 Linux 路径格式，当前 Windows 环境不使用
- `for_windows.xts_acts_path`: 使用 Windows 路径格式，当前环境必需
- `for_windows.sdk_path`: 可以是相对路径，当前环境必需
- `for_windows.hvigor_path_1.1`: 使用 Windows 路径格式，ArkTS-Dyn 编译必需
- `for_windows.hvigor_path_1.2`: 使用 Windows 路径格式，ArkTS-Sta 编译必需
- `for_windows.docs_path`: 文档路径，可选

#### Linux 环境配置

```json
{
  "for_linux": {
    "OH_ROOT": "/home/user/openharmony",
    "hvigor_path_1.1": "/opt/DevEco-Studio/tools/hvigor/bin",
    "hvigor_path_1.2": "/opt/hvigor-static/tools/hvigor/bin"
  },
  "for_windows": {
    "xts_acts_path": "/xts/acts",
    "sdk_path": "sdk/ohos/ets",
    "docs_path": "/docs"
  }
}
```

**说明**：
- `for_linux.OH_ROOT`: 使用 Linux 路径格式，当前环境必需
- `for_linux.hvigor_path_1.1`: 使用 Linux 路径格式，当前环境可选
- `for_linux.hvigor_path_1.2`: 使用 Linux 路径格式，当前环境可选
- 其他路径配置为 Linux 格式，当前环境可选

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
"hvigor_path_1.1": "/opt/DevEco-Studio/tools/hvigor/bin"
"hvigor_path_1.2": "/opt/hvigor-static/tools/hvigor/bin"

// 相对路径
"sdk_path": "sdk/ohos/ets"
```

### 3. 路径格式注意事项

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

**Windows 环境验证**：
- ✅ 检查 `xts_acts_path` 是否存在且可访问
- ✅ 检查 `sdk_path` 是否存在且可访问
- ✅ 检查 `hvigor_path_1.1` 是否存在且可访问
- ✅ 检查 `hvigor_path_1.2` 是否存在且可访问（如需 ArkTS-Sta 编译）
- ℹ️  提示 `for_linux` 配置（当前不使用）

**Linux 环境验证**：
- ✅ 检查 `OH_ROOT` 是否存在且可访问
- ℹ️  提示 `for_windows` 配置（当前不使用）

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
  "for_linux": {
    "OH_ROOT": "/path/to/ohroot"
  },
  "for_windows": {
    "xts_acts_path": "D:\\work\\xts_acts",
    "sdk_path": "sdk/openharmony/ets",
    "hvigor_path_1.1": "D:\\path\\to\\hvigor\\bin",
    "hvigor_path_1.2": "D:\\path\\to\\hvigor_static\\bin"
  }
}
```

**用途**：
- 本地 Windows 环境进行测试生成
- `OH_ROOT` 保留用于远程 Linux 构建环境
- `hvigor_path_1.1` 用于 ArkTS-Dyn 项目构建
- `hvigor_path_1.2` 用于 ArkTS-Sta 项目构建

### 场景2：Linux 构建服务器

```json
{
  "for_linux": {
    "OH_ROOT": "/opt/openharmony",
    "hvigor_path_1.1": "/opt/DevEco-Studio/tools/hvigor/bin",
    "hvigor_path_1.2": "/opt/hvigor-static/tools/hvigor/bin"
  },
  "for_windows": {
    "xts_acts_path": "/opt/xts/acts",
    "sdk_path": "/opt/sdk/ohos/ets"
  }
}
```

**用途**：
- Linux 服务器进行测试生成和构建
- 所有路径都使用 Linux 格式

### 场景3：跨平台协作

```json
{
  "for_linux": {
    "OH_ROOT": "/home/jenkins/ohroot",
    "hvigor_path_1.1": "/home/jenkins/DevEco-Studio/tools/hvigor/bin",
    "hvigor_path_1.2": "/home/jenkins/hvigor-static/tools/hvigor/bin"
  },
  "for_windows": {
    "xts_acts_path": "D:\\jenkins\\xts_acts",
    "sdk_path": "sdk/openharmony/ets",
    "hvigor_path_1.1": "D:\\path\\to\\hvigor\\bin",
    "hvigor_path_1.2": "D:\\path\\to\\hvigor_static\\bin"
  }
}
```

**用途**：
- Jenkins 跨平台构建环境
- 不同平台使用不同的路径配置

## 故障排除

### 1. Windows 环境路径验证失败

**问题**：
```
❌ hvigor_path_1.1: 路径不存在 - D:\DevEco Studio\DevEco Studio\tools\hvigor\bin
❌ hvigor_path_1.2: 路径不存在 - D:\path\to\hvigor_static\bin
```

**解决方法**：
1. 检查 DevEco Studio 安装路径
2. 确认 hvigor 工具实际位置
3. 使用 DevEco Studio 设置中的路径

### 2. Linux 环境路径验证失败

**问题**：
```
❌ OH_ROOT: 路径不存在 - /path/to/ohroot
```

**解决方法**：
1. 检查路径是否存在
2. 确认当前用户是否有访问权限
3. 检查路径挂载状态

### 3. hvigor 路径配置错误

**问题**：
构建失败，提示找不到 hvigor 工具。

**解决方法**：
1. 检查 `hvigor_path_1.1` 和 `hvigor_path_1.2` 配置是否正确
2. 确认路径包含正确的可执行文件：
   - Windows: `hvigorw.bat`
   - Linux: `hvigorw.sh`
3. 检查路径访问权限
4. 注意：ArkTS-Dyn 和 ArkTS-Sta 使用不同版本的 hvigor，需分别配置

### 4. 跨平台混合路径问题

**问题**：
配置文件中混合使用了不同平台的路径格式。

**解决方法**：
- 确保每个平台的路径使用对应平台的格式
- Windows 环境使用 Windows 格式
- Linux 环境使用 Linux 格式
- 不要混合使用反斜杠和正斜杠

## 最佳实践

### 1. 配置文件管理

1. **版本控制**：
   - 配置文件 `.oh-xts-config.json` 通常包含本地路径
   - 建议创建 `.oh-xts-config.example.json` 作为模板
   - 模板文件可以安全地提交到版本控制

2. **文档注释**：
   - 在配置文件中添加路径使用说明
   - 标注哪些路径用于哪些平台
   - 参考 `docs/CROSS_PLATFORM_CONFIG.md` 获取详细说明

### 2. 路径配置建议

1. **使用绝对路径**：
   ```json
   // ✅ 推荐：绝对路径
   "xts_acts_path": "D:\\work\\xts_acts"
   "hvigor_path_1.1": "D:\\path\\to\\hvigor\\bin"
   "hvigor_path_1.2": "D:\\path\\to\\hvigor_static\\bin"
   
   // ⚠️  相对路径可能导致问题
   "sdk_path": "sdk/openharmony/ets"
   ```

2. **路径可移植性**：
   - 考虑使用环境变量或相对路径提高可移植性
   - 为不同的开发人员或构建环境提供灵活的配置方式

3. **定期验证**：
   - 在部署或环境变更后验证配置
   - 运行 `python scripts/config_validator.py validate` 检查有效性

### 3. 开发工作流

1. **首次设置**：
   ```bash
   # 复制模板
   cp .oh-xts-config.example.json .oh-xts-config.json
   
   # 编辑配置
   # 根据当前平台修改相应路径
   
   # 验证配置
   python scripts/config_validator.py validate
   ```

2. **环境切换**：
   - 切换平台时，更新对应平台的路径配置
   - 运行验证确保新配置正确

3. **持续集成**：
   - 在 CI/CD 流程中集成配置验证
   - 确保构建环境配置正确

## 总结

- ✅ **支持跨平台配置**：不同平台使用不同的路径
- ✅ **灵活的路径配置**：支持绝对路径和相对路径
- ✅ **自动验证机制**：提供配置验证工具
- ✅ **清晰的文档说明**：详细说明各路径的使用场景
- ✅ **hvigor 版本化支持**：ArkTS-Dyn 和 ArkTS-Sta 使用独立的 hvigor 工具路径配置

通过正确配置跨平台路径，确保 ohos-test-arkts-xts-generation 在不同环境下都能正常工作。