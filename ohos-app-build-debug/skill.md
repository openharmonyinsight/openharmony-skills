# name: ohos-app-build-debug
# description: HarmonyOS/OpenHarmony application automation build, deployment, and debugging tool for DevEco Studio users. Automatically detects DevEco Studio installation and SDK, then uses the bundled toolchain (hdc, java, hvigorw, llvm, profiler, etc.) for building, installing, and debugging applications. Supports Windows, macOS, and Linux.

---

# OHOS App Build & Debug - HarmonyOS/OpenHarmony

## 📦 Installation

### No Installation (Recommended)

Direct usage without installation:

```bash
cd ~/.claude/skills/ohos-app-build-debug
./ohos-app-build-debug build
```

### System Wide Installation (Optional)

Install to system for global access:

```bash
cd ~/.claude/skills/ohos-app-build-debug
pip install -e .

# Available from any directory after installation
ohos-app-build-debug build
```

**Note**: This documentation uses `ohos-app-build-debug` command. If not installed system-wide, first `cd` to the directory and use `./ohos-app-build-debug`.

---

## 📋 Prerequisites

### ✅ DevEco Studio (Required)

**Purpose**: Official IDE for HarmonyOS/OpenHarmony application development. This skill automatically detects DevEco Studio installation and uses its bundled toolchain.

**Download**: [DevEco Studio](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download)

**Minimum Version**: DevEco Studio 3.1+ (4.0+ recommended)

**What's Included in DevEco Studio**:
- ✅ Java Runtime (JBR/JDK) - No separate Java installation needed
- ✅ HarmonyOS/OpenHarmony SDK - Including hdc, hvigorw, hstack, ohpm
- ✅ LLVM Toolchain - clang, clang++, lld, and more
- ✅ Profiler Tools - hiprofiler, hiperf
- ✅ Build Tools - hvigorw for compiling applications
- ✅ Device Tools - hdc for device communication

**This Skill Automatically Detects**:
- DevEco Studio installation path
- SDK location within DevEco Studio
- Java Runtime (JBR) path
- All available tool executables (hdc, hvigorw, clang, idl, restool, etc.)

**No Manual Configuration Required** - Just install DevEco Studio and use!

---

### ✅ Device Requirements

**Device Setup**:
1. Enable **Developer Options** on your HarmonyOS/OpenHarmony device
   - Settings > About Phone > Tap "Build Number" 7 times
2. Enable **USB Debugging**
   - Settings > System & Updates > Developer Options > USB Debugging
3. Connect device to computer via USB
4. Authorize USB debugging on device when prompted

---

## 🚀 Quick Start

```bash
# Show help
ohos-app-build-debug

# View environment information
ohos-app-build-debug env

# Build application
ohos-app-build-debug build

# Install to device
ohos-app-build-debug install -f app.hap

# Launch application
ohos-app-build-debug launch
```

---

## 💡 Common Workflows

### Build, Install, and Launch

```bash
# Build the application
ohos-app-build-debug build

# Install to device
ohos-app-build-debug install -f entry/build/default/outputs/default/entry-default-signed.hap

# Launch the app
ohos-app-build-debug launch
```

### One-line Command

```bash
ohos-app-build-debug build && \
ohos-app-build-debug install -f entry/build/default/outputs/default/entry-default-signed.hap && \
ohos-app-build-debug launch
```

### View Environment

```bash
ohos-app-build-debug env                      # Show environment info
ohos-app-build-debug env --refresh            # Force refresh cache
```

### Debug with Screenshot

```bash
ohos-app-build-debug launch                   # Launch app
ohos-app-build-debug screenshot               # Take screenshot
```

---

## 📖 Command Reference

### build - Build Application

```bash
ohos-app-build-debug build                              # Build debug version
ohos-app-build-debug build -m release                   # Build release version
ohos-app-build-debug build --show-env                   # Show environment info while building
ohos-app-build-debug build --dir /path/to/project       # Specify project directory
```

### install - Install HAP to Device

```bash
ohos-app-build-debug install -f app.hap                  # Install HAP file
ohos-app-build-debug install -f app.hap -d DEVICE_ID     # Install to specific device
```

### launch - Launch Application

```bash
ohos-app-build-debug launch                              # Launch app (auto-detect)
ohos-app-build-debug launch -b com.example.app          # Launch specific bundle name
ohos-app-build-debug launch --dir .                      # Launch from project directory
```

### screenshot - Take Screenshot

```bash
ohos-app-build-debug screenshot                          # Take device screenshot
ohos-app-build-debug screenshot -o ./screenshots        # Save to specific directory
```

### parse-crash - Parse Crash Stack

```bash
ohos-app-build-debug parse-crash -f crash.txt           # Parse from file
ohos-app-build-debug parse-crash -c "stack..."          # Parse from string
```

### env - Environment Information

```bash
ohos-app-build-debug env                                 # Show environment info
ohos-app-build-debug env --refresh                       # Refresh cache and show
```

---

## 🔧 How It Works

### Automatic Environment Detection

When you run any command, the skill automatically:

1. **Detects DevEco Studio Installation**
   - Windows: `C:\Program Files\Huawei\DevEco Studio\`
   - macOS: `/Applications/DevEco-Studio.app/`
   - Linux: `~/DevEco-Studio/` or `/opt/DevEco-Studio/`

2. **Extracts Toolchain Paths**
   - Java: `{DevEco}/jbr/`
   - SDK: `{DevEco}/sdk/`
   - Tools: `{SDK}/openharmony/toolchains/`
   - LLVM: `{SDK}/openharmony/toolchains/llvm/`
   - Profiler: `{SDK}/openharmony/toolchains/profiler/`

3. **Configures Build Environment**
   - Sets `JAVA_HOME`
   - Adds all tool directories to `PATH`
   - Sets `HDC_SERVER_PORT=7035`
   - Sets `LLVM_HOME` (if LLVM available)

4. **Caches Detection Result**
   - Stores in `~/.ohos_build_debug_cache.json`
   - Speeds up subsequent builds
   - Auto-refreshes every 24 hours

### Detection Result Example

```
============================================================
Environment Detection Result
============================================================

✓ Detection Source: DevEco Studio
  Installation: /Applications/DevEco-Studio.app

✓ Java Home: /Applications/DevEco-Studio.app/Contents/jbr/Contents/Home
✓ SDK Path: /Applications/DevEco-Studio.app/Contents/sdk
✓ Available Tools:
    hdc: .../toolchains/hdc
    hvigorw: .../tools/hvigor/bin/hvigorw
    java: .../jbr/Contents/Home/bin/java
    clang: .../llvm/bin/clang
    idl: .../toolchains/idl
    restool: .../toolchains/restool

============================================================
```

---

## 🛠️ Auto-Detected Tools

### Core Tools
- **hdc** - Device connector tool
- **hvigorw** - Build tool (HarmonyOS Gradle wrapper)
- **java** - Java runtime (JBR)

### LLVM Toolchain (if available)
- **clang** - C/C++ compiler
- **clang++** - C++ compiler
- **lld** - Linker
- **llvm-ar** - Archiver
- **llvm-nm** - Symbol lister
- **llvm-objdump** - Object dumper
- **llvm-strip** - Strip symbols
- **llvm-objcopy** - Object copy utility

### Profiler Tools (if available)
- **hiprofiler** - Profiler tool
- **hiperf** - Performance counter tool

### Other Tools
- **hstack** - Stack parser for release builds
- **ohpm** - Package manager
- **idl** - IDL compiler
- **restool** - Resource tool
- **syscap_tool** - System capability tool

---

## 🎯 Response Style

When helping users with HarmonyOS/OpenHarmony development:

1. **Use `ohos-app-build-debug` command** - Always use `ohos-app-build-debug <command>` in examples
2. **Mention installation options** - Briefly explain no-install vs system-wide installation when first introducing the tool
3. **Show detection results** - Display environment info when first building
4. **Use numbered steps** - For multi-step operations
5. **Provide one-liners** - Combine build, install, launch when appropriate
6. **Bold key information** - Highlight important paths and commands
7. **Show actual paths** - Display detected tool paths

---

## 🔍 Error Handling

### DevEco Studio Not Found

**Error**: `✗ 未检测到 DevEco Studio`

**Solutions**:
1. Verify DevEco Studio is installed
2. Check if installed in standard location
3. Set environment variable:
   ```bash
   export DEVECO_STUDIO_PATH="/path/to/DevEco Studio"
   ```
4. Reinstall from official source

### SDK Not Found

**Error**: `✗ SDK components not found`

**Solutions**:
1. Open DevEco Studio
2. Go to **Settings > SDK**
3. Install **HarmonyOS SDK** or **OpenHarmony SDK**
4. Ensure SDK is installed (not just downloaded)

### Device Not Connected

**Error**: `✗ 未检测到已连接的设备`

**Check**:
1. USB cable connection
2. USB debugging enabled on device
3. Device authorization (click trust)
4. macOS: Accept connection prompt

### Command Not Found After pip install

**Error**: `command not found: ohos-app-build-debug`

**Check**:
1. Verify installation: `pip show ohos-app-build-debug`
2. Check if pip bin directory is in PATH: `echo $PATH`
3. Find installation location: `pip show -f ohos-app-build-debug | grep ohos-app-build-debug`
4. Add to PATH manually or use full path

---

Now help users build, install, and debug HarmonyOS/OpenHarmony applications using `ohos-app-build-debug` command!
