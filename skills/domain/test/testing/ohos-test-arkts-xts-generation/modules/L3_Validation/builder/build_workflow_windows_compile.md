# Windows 编译流程

> **环境准备**: `build_workflow_windows.md` 第二章
> **自动化执行**: `../executor/test_workflow_windows_automation.md`
> **静态编译**: `build_workflow_windows_static.md`

---


## 三、HAP 编译流程（DevEco Studio）

### 3.1 编译方式选择

Windows 环境下提供两种编译方式：**DevEco Studio IDE**（推荐新手）和**命令行编译**（推荐自动化）。

| 编译方式 | 优点 | 缺点 | 推荐度 |
|---------|------|------|--------|
| **DevEco Studio IDE** | 简单可靠、自动签名、可视化 | 需要 GUI 操作 | ⭐⭐⭐⭐⭐ |
| **命令行编译** | 可自动化、无需 GUI、适合 CI/CD | 需要配置路径 | ⭐⭐⭐⭐ |
| PowerShell 脚本 | 可自动化 | 配置复杂、易出错 | ⭐⭐ |

### 3.2 编译主应用 HAP（可选）

如果需要先编译主应用：

1. **打开项目**：
   - 启动 DevEco Studio
   - File → Open → 选择项目目录

2. **编译主 HAP**：
   - 菜单：Build → Build Hap(s) / APP(s) → Build Hap(s)
   - 或右键 `entry` 模块 → Build → Rebuild 'entry'

3. **输出位置**：
   ```
   entry/build/default/outputs/default/entry-default-signed.hap
   ```

### 3.3 编译测试 HAP（必须）

这是测试执行的关键步骤，提供两种编译方式：

#### 方式 1：使用 DevEco Studio IDE（推荐新手）

1. **在 DevEco Studio 中**：
   - 菜单：**Build → Build Hap(s) / APP(s) → Build OhosTest Hap(s)**
   - 或快捷键：`Ctrl + F9`

2. **编译验证**：
   - 查看 Build 窗口输出
   - 成功标志：`BUILD SUCCESSFUL`
   - 失败标志：红色错误信息

3. **Test HAP 输出位置**：
   ```
   entry/build/default/outputs/ohosTest/entry-ohosTest-signed.hap
   ```

#### 方式 2：使用命令行编译（推荐自动化）

使用 DevEco Studio 的 `hvigorw` 命令行工具进行编译，适合自动化和脚本化。

##### 3.3.2.1 查找 DevEco Studio 安装路径

```powershell
# 查找 hvigorw 工具
where hvigorw

# 预期输出示例：
# D:\DevEco Studio\tools\hvigor\bin\hvigorw
# D:\DevEco Studio\tools\hvigor\bin\hvigorw.bat
```

##### 3.3.2.2 编译命令格式

```powershell
# 完整命令格式
hvigorw.bat assembleHap --mode module -p module=entry@ohosTest -p product=default

# 参数说明
# assembleHap         : 执行 HAP 编译任务
# --mode module       : 模块模式编译
# -p module=entry@ohosTest : 编译 entry 模块的 ohosTest 目标
# -p product=default  : 使用 default 产品配置
```

##### 3.3.2.3 实际编译示例

```powershell
# 进入项目目录
cd C:\Users\{username}\DevEcoStudioProjects\MyApplication3

# 执行编译（使用完整路径）
"D:\path\to\hvigor\bin\hvigorw.bat" assembleHap --mode module -p module=entry@ohosTest -p product=default

# 或使用相对路径（如果 hvigorw 在 PATH 中）
hvigorw.bat assembleHap --mode module -p module=entry@ohosTest -p product=default
```

##### 3.3.2.4 编译输出示例

```
> hvigor UP-TO-DATE :entry:ohosTest@PreBuild...
> hvigor Finished :entry:ohosTest@CompileResource... after 378 ms
> hvigor Finished :entry:ohosTest@OhosTestCompileArkTS... after 11 s 6 ms
> hvigor Finished :entry:ohosTest@SignHap... after 209 ms
> hvigor BUILD SUCCESSFUL in 14 s 251 ms
```

**关键输出解读**：
- `BUILD SUCCESSFUL` - 编译成功
- 总耗时：约 14 秒（取决于项目大小）
- Test HAP 输出位置：`entry/build/default/outputs/ohosTest/entry-ohosTest-signed.hap`

##### 3.3.2.5 编译失败处理

如果编译失败，查看错误信息：

```powershell
# 查看详细错误日志
# 编译输出会显示具体的错误信息，包括：
# - 红色错误文本
# - 错误文件位置
# - 错误行号
# - 错误原因
```

常见编译错误：
- **签名配置错误**：检查 `File → Project Structure → Signing Configs`
- **SDK 版本不匹配**：更新 HarmonyOS SDK
- **依赖包缺失**：运行 `ohpm install`

##### 3.3.2.6 验证编译产物

```powershell
# 检查 Test HAP 是否生成
$TestHapPath = "entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap"
if (Test-Path $TestHapPath) {
    $FileSize = (Get-Item $TestHapPath).Length / 1MB
    Write-Host "✓ Test HAP found: $TestHapPath ($FileSize MB)" -ForegroundColor Green
} else {
    Write-Host "✗ Test HAP not found!" -ForegroundColor Red
    exit 1
}

# 列出所有 HAP 文件
Get-ChildItem "entry\build\default\outputs" -Recurse -Filter "*.hap" | Format-Table Name, @{Name="Size(MB)";Expression={$_.Length/1MB}}
```

##### 3.3.2.7 命令行编译优势

相比 IDE 编译，命令行编译的优势：

| 优势 | 说明 |
|------|------|
| **可自动化** | 易于集成到脚本和 CI/CD 流程 |
| **无需 GUI** | 可在无图形界面环境下执行 |
| **可重复** | 命令可以精确复现 |
| **高效** | 无需启动 IDE，节省资源 |
| **日志完整** | 所有输出都可以重定向到文件 |

### 3.4 验证编译产物

使用 PowerShell 验证 HAP 文件：

```powershell
# 进入项目目录
cd C:\Users\{username}\DevEcoStudioProjects\MyApplication3

# 检查 Test HAP 是否生成
$TestHapPath = "entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap"
if (Test-Path $TestHapPath) {
    $FileSize = (Get-Item $TestHapPath).Length / 1KB
    Write-Host "✓ Test HAP found: $TestHapPath ($FileSize KB)" -ForegroundColor Green
} else {
    Write-Host "✗ Test HAP not found!" -ForegroundColor Red
    exit 1
}

# 列出所有 HAP 文件
Get-ChildItem "entry\build\default\outputs" -Recurse -Filter "*.hap" | Format-Table Name, Length
```
