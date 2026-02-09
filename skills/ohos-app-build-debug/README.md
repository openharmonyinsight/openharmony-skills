# OHOS App Build & Debug - HarmonyOS/OpenHarmony (v2.1)

**自动检测 DevEco Studio 并使用其内置工具链进行编译调试**

HarmonyOS/OpenHarmony 应用自动化构建、部署和调试工具。支持 **Windows**、**macOS** 和 **Linux**。

## ✨ 特性

- ✅ **零配置** - 自动检测 DevEco Studio 和工具链
- ✅ **扩展工具检测** - 自动发现 LLVM、Profiler 等所有开发工具
- ✅ **开箱即用** - 无需安装配置，直接使用
- ✅ **统一 CLI** - 一个命令完成所有操作

## 📦 安装与使用

### 方式一：No Installation（推荐，无需配置）

直接使用脚本，无需安装：

```bash
cd ~/.claude/skills/ohos-app-build-debug
./ohos-app-build-debug build
```

### 方式二：System Wide Installation（可选）

安装到系统全局，可在任意目录使用：

```bash
cd ~/.claude/skills/ohos-app-build-debug
pip install -e .

# 安装后可在任意目录使用
ohos-app-build-debug build
```

**说明**：本文档后续统一使用 `ohos-app-build-debug` 命令。如未安装，请先 `cd` 到目录并使用 `./ohos-app-build-debug`。

---

## 🚀 快速开始

```bash
# 查看帮助
ohos-app-build-debug

# 查看环境信息
ohos-app-build-debug env

# 编译应用
ohos-app-build-debug build

# 安装应用
ohos-app-build-debug install -f app.hap

# 启动应用
ohos-app-build-debug launch
```

## 📖 命令参考

### build - 编译应用

```bash
ohos-app-build-debug build                              # 编译 debug 版本
ohos-app-build-debug build -m release                   # 编译 release 版本
ohos-app-build-debug build --show-env                   # 显示环境信息
ohos-app-build-debug build --dir /path/to/project       # 指定项目目录
```

### install - 安装 HAP

```bash
ohos-app-build-debug install -f app.hap                  # 安装 HAP 文件
ohos-app-build-debug install -f app.hap -d DEVICE_ID     # 安装到指定设备
```

### launch - 启动应用

```bash
ohos-app-build-debug launch                              # 启动应用（自动检测）
ohos-app-build-debug launch -b com.example.app          # 启动指定应用
ohos-app-build-debug launch --dir .                      # 从项目目录启动
```

### screenshot - 截图

```bash
ohos-app-build-debug screenshot                          # 截取设备屏幕
ohos-app-build-debug screenshot -o ./screenshots        # 保存到指定目录
```

### parse-crash - 解析崩溃

```bash
ohos-app-build-debug parse-crash -f crash.txt           # 从文件解析
ohos-app-build-debug parse-crash -c "stack..."          # 从字符串解析
```

### env - 环境信息

```bash
ohos-app-build-debug env                                 # 显示环境信息
ohos-app-build-debug env --refresh                       # 刷新缓存
```

## 💡 使用示例

### 完整工作流

```bash
# 1. 查看环境信息
ohos-app-build-debug env

# 2. 编译应用
ohos-app-build-debug build

# 3. 安装到设备
ohos-app-build-debug install -f entry/build/default/outputs/default/entry-default-signed.hap

# 4. 启动应用
ohos-app-build-debug launch
```

### 一行命令

```bash
# 编译、安装、启动
ohos-app-build-debug build && \
ohos-app-build-debug install -f entry/build/default/outputs/default/entry-default-signed.hap && \
ohos-app-build-debug launch
```

### Debug 工作流

```bash
ohos-app-build-debug build                    # 编译应用
ohos-app-build-debug launch                   # 启动应用
ohos-app-build-debug screenshot               # 截图查看结果
```

## 🔧 环境检测

OHOS 会自动检测 DevEco Studio 并配置以下工具：

### 核心工具
- **hdc** - 设备连接工具
- **hvigorw** - 构建工具
- **java** - Java 运行时

### LLVM 工具链（如果可用）
- **clang** - C/C++ 编译器
- **clang++** - C++ 编译器
- **lld** - 链接器
- **llvm-\*** - LLVM 工具集

### Profiler 工具（如果可用）
- **hiprofiler** - 性能分析器
- **hiperf** - 性能计数器

### 其他工具
- **idl** - IDL 编译器
- **restool** - 资源工具
- **syscap_tool** - 系统能力工具

## 📋 前置要求

### DevEco Studio（必需）

**下载**: [DevEco Studio](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download)

**版本**: DevEco Studio 3.1+ (推荐 4.0+)

**包含内容**：
- ✅ Java Runtime (JBR/JDK)
- ✅ HarmonyOS/OpenHarmony SDK
- ✅ 所有开发工具

### 设备要求

1. 启用**开发者选项** - 设置 > 关于手机 > 连续点击"版本号" 7次
2. 启用**USB 调试** - 设置 > 系统和更新 > 开发者选项 > USB 调试
3. 通过 USB 连接设备

## 🔍 检测示例

```
============================================================
环境检测结果
============================================================

✓ 检测源: DevEco Studio
  安装路径: /Applications/DevEco-Studio.app

✓ Java Home: /Applications/DevEco-Studio.app/Contents/jbr/Contents/Home
✓ SDK Path: /Applications/DevEco-Studio.app/Contents/sdk
✓ OpenHarmony SDK: /Applications/DevEco-Studio.app/Contents/sdk/default/openharmony

✓ 可用工具:
  核心工具:
    hdc: .../toolchains/hdc
    hvigorw: .../tools/hvigor/bin/hvigorw
    java: .../jbr/Contents/Home/bin/java

  其他工具:
    idl: .../toolchains/idl
    restool: .../toolchains/restool
    syscap_tool: .../toolchains/syscap_tool

============================================================
```

## 🛠️ 故障排除

### DevEco Studio 未检测到

**错误**: `✗ 未检测到 DevEco Studio`

**解决方案**:
1. 确认 DevEco Studio 已安装
2. 检查是否安装在标准位置
3. 设置环境变量：
   ```bash
   export DEVECO_STUDIO_PATH="/path/to/DevEco Studio"
   ```

### 设备未连接

**错误**: `✗ 未检测到已连接的设备`

**检查步骤**:
1. USB 线是否连接
2. 设备是否启用 USB 调试
3. 设备是否授权（点击信任）
4. macOS: 系统可能提示接受连接

### 工具未找到

**错误**: `✗ xxx 工具未找到`

**解决方案**:
1. 打开 DevEco Studio
2. **Settings > SDK**
3. 确保安装了 HarmonyOS SDK 或 OpenHarmony SDK
4. 确保安装了 SDK Components

### pip install 后找不到命令

**错误**: `command not found: ohos-app-build-debug`

**检查步骤**:
1. 确认安装成功：`pip show ohos-app-build-debug`
2. 检查 pip bin 目录是否在 PATH 中：`echo $PATH`
3. 查找安装位置：`pip show -f ohos-app-build-debug | grep ohos-app-build-debug`
4. 手动添加到 PATH 或使用完整路径

## 📚 更多信息

- **完整文档**: [skill.md](skill.md)
- **更新日志**: 项目目录中的 `*_SUMMARY.md` 文件

## 📄 许可

本工具为开源工具，遵循相关开源许可协议。
