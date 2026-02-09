# ArkWeb App Debugging Skill

**Name**: arkweb-app-debug
**Description**: Professional debugging tool for HarmonyOS ArkWeb applications with AI-powered automated testing, zero dependencies, and auto-detection
**Version**: 1.0 | **Author**: ArkWeb Debug Team | **License**: MIT | **Status**: Production Ready

## Overview

This skill provides automated debugging capabilities for HarmonyOS ArkWeb applications using Chrome DevTools Protocol. It streamlines the entire debugging workflow from device connection to AI-powered automated testing.

## Features

- ✅ **Zero Dependencies**: No third-party Python packages required ✨
- ✅ **Automatic Device Detection**: Finds and connects to HarmonyOS devices automatically
- ✅ **Dynamic Socket Discovery**: Handles the dynamic nature of webview_devtools sockets
- ✅ **Port Forwarding Management**: Automatic creation, cleanup, and orphan detection
- ✅ **Auto-detection**: Automatically detects project configuration from HarmonyOS project files
- ✅ **AI Automated Testing**: Integration with Chrome DevTools MCP (26 tools)
- ✅ **Session Management**: Track multiple debugging sessions with state persistence
- ✅ **Resource Cleanup**: Automatic cleanup of port forwards and sessions

---

## 📋 Prerequisites

### 1. Recommended Tool

#### ✅ DevEco Studio (Recommended)

**Purpose**: Official IDE for HarmonyOS development. The **ohos-app-build-debug** skill automatically detects DevEco Studio installation and uses its bundled toolchain.

**Download**: [DevEco Studio](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download)

**Minimum Version**: DevEco Studio 3.1+ (4.0+ recommended)

**What's Included**:
- ✅ **hdc** - Device connector tool (auto-detected)
- ✅ **hvigorw** - Build tool (auto-detected)
- ✅ **Java Runtime** - No separate installation needed
- ✅ **HarmonyOS SDK** - Complete development toolkit

**Why DevEco Studio?**
- All required tools are bundled and automatically detected
- No manual environment configuration needed
- The **ohos-app-build-debug** skill handles everything automatically

**If you don't have DevEco Studio**:
- You can still use this skill if hdc is available in your PATH
- Install [Command Line Tools](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get) separately
- Configure environment variables manually (see below)

**Check if hdc is available**:
```bash
hdc --version
```

### 2. Related Skills

- **ohos-app-build-debug** skill: Provides HarmonyOS application build, install, and launch features
  - Works with arkweb-app-debug for complete development and debugging experience
  - Automatically detects DevEco Studio and configures all development tools
  - No manual environment setup required

### 3. AI Automation Tool (Optional but Recommended)

#### ✅ Chrome DevTools MCP

**Purpose**: Allows Claude AI to directly operate Chrome DevTools for automated testing.

**One-click Installation**:
```bash
claude mcp add --transport stdio arkweb-devtools --scope user -- \
  npx chrome-devtools-mcp@latest -y \
  --browser-url=http://127.0.0.1:9222
```

**Verify Installation**:
```bash
claude mcp list
# Should see arkweb-devtools in the list
```

**If MCP is not installed**:
- ✅ All basic debugging features still work
- ❌ AI automated testing unavailable
- ❌ Claude cannot automatically operate pages

### 4. Device and Developer Options

#### ✅ HarmonyOS Device

- Enable **Developer Options**
- Enable **USB Debugging**
- Connect to computer via USB

**Verify Device Connection**:
```bash
hdc list targets
# Should display device ID
```

**If no device found**:
1. Check USB cable connection
2. Authorize USB debugging on device
3. Restart hdc: `hdc kill && hdc start`

---

## Installation

### Quick Start (Recommended - No Installation)

```bash
cd arkweb-app-debug
./arkweb-app-debug start
```

### System-wide Installation

```bash
cd arkweb-app-debug
pip install -e .
arkweb-app-debug device list
```

**Note**: The tool automatically detects project configuration from HarmonyOS project files.

---

## Requirements

### System Requirements
- HarmonyOS device with Developer Mode enabled
- **hdc** available in PATH or DevEco Studio installed (see Prerequisites above)
- Python 3.8 or higher
- Chrome/Chromium browser (for DevTools)

**Note**: The **ohos-app-build-debug** skill automatically detects DevEco Studio and provides all required tools for HarmonyOS development.

### Application Requirements

Your ArkWeb application **must** enable debugging in `aboutToAppear()`:

```typescript
import { webview } from '@kit.ArkWeb';

@Entry
@Component
struct Index {
  controller: webview.WebviewController = new webview.WebviewController();

  aboutToAppear() {
    // ⚠️ CRITICAL: Enable debugging BEFORE Web component renders
    webview.WebviewController.setWebDebuggingAccess(true);
  }

  build() {
    Web({ src: this.currentUrl, controller: this.controller })
  }
}
```

---

## Usage

### Quick Start (Cross-Platform)

**Recommended: Use convenience scripts (auto-configures environment)**

| Platform | Script | Command |
|----------|--------|---------|
| macOS/Linux | Bash script | `./start-debug.sh` |
| macOS/Linux | Python script | `python3 start-debug.py` |
| Windows | Batch script | `start-debug.bat` |
| Windows | Python script | `python start-debug.py` |

**Examples**:
```bash
# macOS/Linux - Bash script
./start-debug.sh

# macOS/Linux - Python script
python3 start-debug.py --package com.example.app

# Windows - Batch script
start-debug.bat

# Windows - Python script
python start-debug.py --package com.example.app
```

**All convenience scripts**:
- ✓ Automatically detect DevEco Studio installation
- ✓ Configure PATH for hdc, hvigorw, and other tools
- ✓ Check device connection
- ✓ Start debugging session

**Option 2: Manual environment setup (Advanced)**
```bash
# 1. Set up environment from ohos-app-build-debug
cd ~/.claude/skills/ohos-app-build-debug
source <(./ohos-app-build-debug env --export)  # macOS/Linux
# Or on Windows, manually set PATH based on env output

# 2. Start debugging
cd /path/to/arkweb-app-debug
./arkweb-app-debug start  # or arkweb-app-debug.exe on Windows
```

### Basic Workflow

```bash
# 1. Check device connection
arkweb-app-debug device list

# 2. Start debugging session (auto-detects project config)
arkweb-app-debug start

# 3. List active sessions
arkweb-app-debug session list

# 4. Stop session when done
arkweb-app-debug stop <session-id>
```

### What Happens Automatically

The tool automatically:
- ✓ Searches upward for HarmonyOS project root (max 5 levels)
- ✓ Extracts package name from `AppScope/app.json5`
- ✓ Finds HAP file path
- ✓ Uses default port 9222
- ✓ Creates port forwarding
- ✓ Opens DevTools (if `--open-chrome` specified)

### Environment Requirements

**IMPORTANT**: This tool requires **hdc** to be available in PATH.

**Using ohos-app-build-debug (Recommended)**:
- The `start-debug.sh` script automatically configures environment
- Detects DevEco Studio installation
- Sets up PATH for hdc, hvigorw, and other tools

**Manual Setup**:
```bash
# Check if ohos-app-build-debug detected DevEco Studio
cd ~/.claude/skills/ohos-app-build-debug
./ohos-app-build-debug env

# Export environment variables (example)
export PATH="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains:$PATH"
export HDC_SERVER_PORT=7035
```

---

## 🤖 AI Automated Testing (Requires MCP)

### After MCP Configuration

Once MCP is configured, Claude can automatically execute tests:

```
User: Please help me test the login functionality
Claude: (Automatically executes tests)
✓ Opens application
✓ Navigates to login page
✓ Fills out form
✓ Submits login
✓ Verifies results
```

### Available AI Debugging Tools (26 Tools)

- Page navigation and interaction
- Element selection and clicking
- Form filling
- Screenshots and snapshots
- JavaScript execution
- Network request inspection
- Performance tracking
- And more...

See [docs/MCP_GUIDE.md](docs/MCP_GUIDE.md) for details.

---

## Troubleshooting

### ❌ hdc: command not found

**Cause**: hdc not installed or not in PATH

**Solution**:
1. Download [Command Line Tools](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get)
2. Configure environment variables (see "Prerequisites" above)
3. Verify: `hdc --version`

### ❌ No device found

**Cause**: Device not connected or not authorized

**Solution**:
```bash
# 1. Check device
hdc list targets

# 2. Restart hdc
hdc kill
hdc start

# 3. Authorize USB debugging on device
```

### ❌ MCP not available

**Cause**: Chrome DevTools MCP not configured

**Solution**:
```bash
claude mcp add --transport stdio arkweb-devtools --scope user -- \
  npx chrome-devtools-mcp@latest -y \
  --browser-url=http://127.0.0.1:9222
```

### Socket Not Found

**Symptoms**: "Socket not found within timeout"

**Solutions**:
1. Verify app has `setWebDebuggingAccess(true)` in code
2. Ensure Web component has rendered (navigate to a URL)
3. Check if app crashed: `hdc shell ps -A | grep <package>`

### Port Forward Failed

**Symptoms**: "Failed to create port forward"

**Solutions**:
1. Remove old forwards: `hdc fport rm tcp:9222`
2. Check HDC syntax: `hdc fport --help`
3. Verify device is connected: `hdc list targets`

---

## Architecture

```
arkweb-app-debug/
├── arkweb_debug/           # Core Python package
│   ├── cli.py             # Command-line interface
│   ├── config/            # Configuration management + auto-detection
│   ├── device/            # Device detection and management
│   ├── app/               # Application lifecycle
│   ├── port/              # Port forwarding (with dynamic socket finding)
│   ├── session/           # Session management
│   └── utils/             # Utilities (HDC, Chrome, logger)
├── docs/                  # Documentation
│   ├── MCP_GUIDE.md       # MCP usage guide
│   ├── TROUBLESHOOTING.md # Troubleshooting guide
│   └── publishing/        # Distribution guides
└── arkweb-app-debug           # Wrapper script (no installation needed)
```

---

## Key Capabilities

### 1. One-Command Debugging

```bash
arkweb-app-debug start
```

Automatically:
- Detects project configuration
- Connects to device
- Installs/starts application
- Waits for Web component initialization (10s)
- Finds the debugging socket dynamically
- Creates port forwarding
- Opens Chrome DevTools (optional)

### 2. Dynamic Socket Finding

Solves the critical issue where `webview_devtools_remote_{PID}` socket name changes each app launch by:
- Searching `/proc/net/unix` for actual socket name
- Implementing retry mechanism with timeout
- Supporting PID-based lookup as fallback

### 3. Proper HDC Command Format

Uses correct HDC fport syntax:
- ✅ `hdc fport tcp:9222 localabstract:socket_name`
- ❌ `hdc fport tcplocal:9222 ...` (wrong)

---

## Critical Timing Requirements

Based on real debugging experience, the following timing is **critical**:

1. **After app start**: Wait **10 seconds** for Web component to create debugging socket
2. **After port forward**: Wait **2 seconds** for socket initialization
3. **Socket finding**: Retry every **2 seconds** for up to **15 seconds**

The tool handles these timings automatically.

---

## Contributing

When extending this skill:

1. **Maintain timing requirements**: The 10s wait after app start is critical
2. **Handle dynamic sockets**: Always find socket dynamically, never hardcode
3. **Use correct HDC syntax**: `fport tcp:{port}` not `tcplocal:{port}`
4. **Clean up resources**: Always register forwards for cleanup
5. **Log actions**: Use provided logging utilities

---

## 🔗 Related Resources

- [hdc Command Documentation](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hdc)
- [Get Command Line Tools](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get)
- [Command Line Build Tool (hvigorw)](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-hvigor-commandline)
- [Build Pipeline](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-command-line-building-app)

---

## License

MIT License - See LICENSE file for details

---

**Version**: 1.0 | **Status**: Production Ready | **Dependencies**: None ✅
