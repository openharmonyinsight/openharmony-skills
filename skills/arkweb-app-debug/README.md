# ArkWeb App Debugging Skill

**Version**: 1.0 | **Status**: Production Ready | **Python**: 3.8+ | **Dependencies**: None ✅

专业级 HarmonyOS ArkWeb 应用调试工具（ArkWeb App Debug Tool），支持 AI 自动化测试、零依赖和自动检测。

---

## 📋 前置条件

在开始使用之前，请确保满足以下条件：

### 1. HarmonyOS 开发环境

#### ✅ DevEco Studio（推荐）

**DevEco Studio** 是 HarmonyOS 官方 IDE。**ohos-app-build-debug** skill 会自动检测 DevEco Studio 安装并使用其内置工具链。

**下载**: [DevEco Studio](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download)

**最低版本**: DevEco Studio 3.1+ （推荐 4.0+）

**包含的工具**:
- ✅ **hdc** - 设备连接工具（自动检测）
- ✅ **hvigorw** - 构建工具（自动检测）
- ✅ **Java 运行时** - 无需单独安装
- ✅ **HarmonyOS SDK** - 完整开发工具包

**为什么推荐 DevEco Studio？**
- 所有必需工具都已内置，自动检测
- 无需手动配置环境变量
- **ohos-app-build-debug** skill 会自动处理所有配置

**如果没有 DevEco Studio**:
- 仍可使用本工具，只要 hdc 在 PATH 中可用
- 可单独下载 [Command Line Tools](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get)
- 需要手动配置环境变量（见下方）

**检查 hdc 是否可用**:
```bash
hdc --version
```

**如果 hdc 不可用**:
- **推荐方式**: 安装 DevEco Studio，让 ohos-app-build-debug skill 自动检测
- **手动方式**: 下载 Command Line Tools 并配置环境变量：

**macOS/Linux**:
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export PATH="/path/to/command-line-tools:/path/to/command-line-tools/sdk/default/openharmony/toolchains:$PATH"
export HDC_SERVER_PORT=7035
source ~/.bashrc
```

**Windows**:
```cmd
# 系统属性 > 高级系统设置 > 环境变量
# 添加到 Path:
# C:\path\to\command-line-tools
# C:\path\to\command-line-tools\sdk\default\openharmony\toolchains
# 新建系统变量: HDC_SERVER_PORT = 7035
```

**详细文档**:
- [hdc 命令官方文档](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hdc)
- [命令行构建工具（hvigorw）](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-hvigor-commandline)

### 2. AI 自动化调试工具（可选但推荐）

#### ✅ Chrome DevTools MCP（推荐安装）

**MCP (Model Context Protocol)** 允许 Claude AI 直接操作 Chrome DevTools，实现自动化测试。

**一键安装**:
```bash
claude mcp add --transport stdio arkweb-devtools --scope user -- \
  npx chrome-devtools-mcp@latest -y \
  --browser-url=http://127.0.0.1:9222
```

**验证安装**:
```bash
# 检查 MCP 配置
claude mcp list
# 应该看到 arkweb-devtools 在列表中
```

**如果 claude 命令不可用**:
1. 确保已安装 Claude Code CLI
2. 或使用 Claude Desktop 应用配置 MCP
3. 参考：[chrome-devtools-mcp](https://github.com/modelcontextprotocol/servers/tree/main/src/chrome-devtools)

**如果不安装 MCP**:
- ✅ 仍可使用所有基础调试功能
- ❌ 无法使用 AI 自动化测试
- ❌ 无法让 Claude 自动操作页面

### 3. 设备和开发者选项

#### ✅ HarmonyOS 设备

- 启用 **开发者选项**
- 启用 **USB 调试**
- 通过 USB 连接电脑

**验证设备连接**:
```bash
hdc list targets
# 应显示设备 ID
```

**如果无设备**:
1. 检查 USB 线连接
2. 在设备上授权 USB 调试
3. 重启 hdc: `hdc kill && hdc start`

### 4. 相关工具（推荐）

- **ohos-app-build-debug** skill: 提供 HarmonyOS 应用的编译、安装、启动等功能
  - 与 arkweb-app-debug 配合使用，获得完整的开发和调试体验
  - 自动检测 DevEco Studio 并配置所有开发工具
  - 无需手动环境配置

---

## 🚀 快速开始

### 方式1：使用便捷脚本（推荐，跨平台）

#### macOS/Linux

**使用 Bash 脚本**:
```bash
./start-debug.sh

# 带参数
./start-debug.sh --package com.example.app
```

**使用 Python 脚本（跨平台）**:
```bash
python3 start-debug.py

# 带参数
python3 start-debug.py --package com.example.app
```

#### Windows

**使用批处理脚本**:
```cmd
start-debug.bat

# 带参数
start-debug.bat --package com.example.app
```

**使用 Python 脚本（跨平台）**:
```cmd
python start-debug.py

# 带参数
python start-debug.py --package com.example.app
```

### 方式2：手动配置环境（高级用户）

#### macOS/Linux

```bash
# 1. 设置 ohos-app-build-debug 检测到的环境
cd ~/.claude/skills/ohos-app-build-debug
source <(./ohos-app-build-debug env --export)

# 2. 启动调试
cd /path/to/arkweb-app-debug
./arkweb-app-debug start
```

#### Windows (PowerShell)

```powershell
# 1. 设置 ohos-app-build-debug 检测到的环境
cd $env:USERPROFILE\.claude\skills\ohos-app-build-debug
.\ohos-app-build-debug.exe env

# 2. 手动设置环境变量（根据输出）
$env:PATH = "C:\path\to\toolchains;$env:PATH"
$env:HDC_SERVER_PORT = "7035"

# 3. 启动调试
cd \path\to\arkweb-app-debug
.\arkweb-app-debug.exe start
```

### 方式2：安装到系统

```bash
cd arkweb-app-debug
pip install -e .
arkweb-app-debug device list
```

**注意**：工具会自动检测项目配置，无需任何手动配置。

---

## ⚙️ 应用要求

**必须启用调试**，在 `aboutToAppear()` 中添加：

```typescript
import { webview } from '@kit.ArkWeb';

@Entry
@Component
struct Index {
  controller: webview.WebviewController = new webview.WebviewController();

  aboutToAppear() {
    webview.WebviewController.setWebDebuggingAccess(true);
  }

  build() {
    Web({ src: this.currentUrl, controller: this.controller })
  }
}
```

---

## ✨ 核心特性

- ✅ **零依赖** - 无需任何第三方Python库（无pyyaml）✨
- ✅ **自包含** - 无需 pip install，直接运行
- ✅ **智能项目识别** - 自动向上搜索 HarmonyOS 项目根目录
- ✅ **自动设备检测** - 自动发现 HarmonyOS 设备
- ✅ **动态 Socket 查找** - 自动处理 PID 变化
- ✅ **AI 自动化测试** - 集成 Chrome DevTools MCP（26种工具）
- ✅ **智能资源管理** - 自动清理端口转发

---

## 📋 主要命令

### 快速启动（跨平台）

**推荐方式：使用便捷脚本（自动配置环境）**

| 平台 | 命令 | 说明 |
|------|------|------|
| **macOS/Linux** | `./start-debug.sh` | Bash 脚本 |
| **macOS/Linux** | `python3 start-debug.py` | Python 脚本（跨平台） |
| **Windows** | `start-debug.bat` | 批处理脚本 |
| **Windows** | `python start-debug.py` | Python 脚本（跨平台） |

**使用示例**:
```bash
# macOS/Linux - Bash 脚本
./start-debug.sh

# macOS/Linux - Python 脚本
python3 start-debug.py --package com.example.app

# Windows - 批处理脚本
start-debug.bat

# Windows - Python 脚本
python start-debug.py --package com.example.app
```

### 其他命令

```bash
# 设备管理（需要先配置环境）
arkweb-app-debug device list

# 端口转发
arkweb-app-debug port list

# 会话管理
arkweb-app-debug session list
arkweb-app-debug stop-all

# 资源清理
arkweb-app-debug cleanup
```

---

## 🤖 AI 自动化测试（需要 MCP）

### 配置完成后的使用方式

配置 MCP 后，Claude 可以自动执行测试：

```
用户：请帮我测试登录功能
Claude：（自动执行测试）
✓ 打开应用
✓ 导航到登录页
✓ 填写表单
✓ 提交登录
✓ 验证结果
```

### 可用的 AI 调试工具（26种）

- 页面导航和交互
- 元素选择和点击
- 表单填写
- 截图和快照
- JavaScript 执行
- 网络请求检查
- 性能追踪
- 更多...

详见 [docs/MCP_GUIDE.md](docs/MCP_GUIDE.md)

---

## 📖 参考文档

- **docs/MCP_GUIDE.md** - Chrome DevTools MCP 使用指南（26种AI调试工具）
- **docs/TROUBLESHOOTING.md** - 故障排除指南

---

## ⚠️ 快速故障排除

| 问题 | 解决方法 |
|------|----------|
| **HDC tool not found** | 使用 `./start-debug.sh` 自动配置环境，或手动运行：`cd ~/.claude/skills/ohos-app-build-debug && source <(./ohos-app-build-debug env --export)` |
| **No device found** | 检查USB连接，在设备上授权USB调试，运行 `hdc kill && hdc start` |
| **应用启动失败** | 确保应用已安装，检查 bundle name 是否正确 |
| **找不到调试 socket** | 等待应用完全初始化（约10-15秒），确保 Web 组件已渲染 |
| **MCP 不可用** | 运行 `claude mcp add ...` 命令（见上方"AI自动化调试工具"章节） |
| **端口被占用** | 运行 `./arkweb-app-debug cleanup` |

### 常见问题详解

#### 1. HDC 工具找不到

**问题**: `HDC tool not found`

**原因**: 环境变量 PATH 中没有包含 DevEco Studio 的工具路径

**解决方案**:

**方式1（推荐）**: 使用快速启动脚本
```bash
./start-debug.sh
```

**方式2**: 手动配置环境
```bash
cd ~/.claude/skills/ohos-app-build-debug
source <(./ohos-app-build-debug env --export)
cd /path/to/arkweb-app-debug
./arkweb-app-debug start
```

#### 2. 应用启动但找不到调试 socket

**问题**: 应用启动成功，但显示 "Socket not found within timeout"

**原因**: Web 组件还未完全初始化

**解决方案**:
- 等待 10-15 秒让应用完全初始化
- 确保在 `aboutToAppear()` 中调用了 `setWebDebuggingAccess(true)`
- 检查 Web 组件是否已渲染

**详细问题排查**: 见 [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

---

**版本**: 1.0 | **发布**: 2025-02-08 | **状态**: Production Ready | **依赖**: 零依赖 ✅
