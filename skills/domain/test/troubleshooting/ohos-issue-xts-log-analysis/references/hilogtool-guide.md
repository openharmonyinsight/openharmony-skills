# HiLogTool工具使用指南

## 目录

- 工具说明
  - 工具获取方式
- 重要提示
- 加密日志识别
- 命令参数详解
  - 核心参数
  - 命令格式
  - 字典文件说明
- 工具使用
  - Windows环境
  - Linux环境（使用wine）
  - ⚠️ 重要：不要使用gunzip解压！
  - strings提取方式（仅作为应急方案）
- 常用命令
- 快速参考
- 注意事项
- 使用流程
- 故障排查
  - Windows：Microsoft Store Python 桩程序（重要，2026-07-15 新增）
  - 通用故障表

---

## 工具说明

HiLogTool是OpenHarmony的日志解析工具，用于解析加密/压缩的hilog日志文件。

**官方文档**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hilog-tool

### 工具获取方式

1. **OpenHarmony SDK自带**：
   - 路径：`${SDK路径}/toolchains/hilogtool`
   - 版本：随SDK版本更新

2. **HarmonyOS SDK自带**：
   - 路径：`${SDK路径}/openharmony/toolchains/hilogtool`
   - 版本：随HarmonyOS版本更新

3. **本skill提供**：
   - 路径：`tools/hilogtool.exe`
   - 适用于Windows/Linux（Linux需wine）

**工具位置**: `tools/hilogtool.exe`

## 重要提示

**字典文件是必须的**：hilog日志解析需要配套的字典文件（`hilog_dict.*.zip`），否则解析会超时无响应或失败。字典文件通常与hilog日志在同一目录下。

## 加密日志识别

**加密日志特征**：
- 文件名格式: `hilog.xxx.yyyyMMdd-HHmmss.gz` 或 `hilog.*.zst`
- 文件格式: gzip/zstd压缩格式
- 直接cat显示乱码或二进制内容

**识别方法**：
```bash
# 检查文件类型
file hilog.000.gz
# 输出: gzip compressed data

# 检查文件头
hexdump -C hilog.000.gz | head -1
# gzip文件头: 1f 8b
# zstd文件头: 28 b5 2f fd
```

## 命令参数详解

### 核心参数

| 参数 | 长参数 | 说明 | 必需 |
|------|--------|------|------|
| `-i` | `--input` | 输入目录或文件路径 | 是 |
| `-o` | `--output` | 输出目录路径 | 是 |
| `-d` | `--dict` | 字典文件（zip）或目录 | 是 |
| `-h` | `--help` | 显示帮助信息 | 否 |
| `-v` | `--version` | 显示版本号 | 否 |

### 命令格式

```bash
hilogtool parse -i <输入目录或文件> -o <输出目录> -d <字典文件>
```

### 字典文件说明

字典文件是hilog解析的关键，通常位于日志同目录下：
- 文件名格式：`hilog_dict.*.zip` 或 `dict.zip`
- 必须与日志文件配套使用
- 没有字典文件会导致解析超时或失败

## 工具使用

### Windows环境

> Windows **不需要 wine**，直接运行 hilogtool.exe 原生解密。

```bash
# 1. 创建输出目录（hilogtool 不自动创建）
mkdir <日志目录>_parsed

# 2. 基本用法：解析整个目录
tools/hilogtool.exe parse -i <日志目录> -o <输出目录> -d <字典文件>

# 示例：解析单个目录
mkdir ./hilog_data_parsed
tools/hilogtool.exe parse -i ./hilog_data -o ./hilog_data_parsed -d ./hilog_data/hilog_dict.zip

# 查看帮助
tools/hilogtool.exe --help
```

> ⚠️ **Git Bash 路径转义**：在 Git Bash 中用 `cmd //c` 调用 .cmd 或 hilogtool.exe 时，路径中的反斜杠 `\` 会被 Bash 吃掉（`C:\Users\.cac` 变成 `C:\Users.cac`）。**用正斜杠 `/` 代替**：`cmd //c "C:/Users/.../scripts/check_dict.cmd" "D:/work/..."`

### Linux环境（使用wine）

> Linux 需用 wine64 运行 hilogtool.exe。**wine 不可用时禁止降级**——先安装 wine64 再解密。

#### 环境准备

```bash
# 1. 安装wine64（如未安装）—— 禁止跳过此步直接降级
wine64 --version || sudo apt-get install -y wine64

# 2. 确保工具有执行权限
chmod +x ~/.opencode/skills/ohos-issue-xts-log-analysis/tools/hilogtool.exe

# 3. 初始化wine配置（首次运行需要，会创建~/.wine目录）
wine64 --version
```

#### 执行解析

**⚠️ 输出路径规则**

**所有输出文件存放在用户输入路径的同级 `_parsed` 目录**：

```
输入路径: /home/user/hilog_FMR0123417000740/
输出路径: /home/user/hilog_FMR0123417000740_parsed/
  ├── hilog.105.20260626-162241.txt  ← 解密日志
  ├── hilog.106.20260626-162452.txt  ← 解密日志  
  ├── hilog.107.20260626-162511.txt  ← 解密日志
  └── dict/                          ← dict临时文件（约50-100M）
```

**用户统一管理**：所有文件都在一个目录，解析完成后可删除 `_parsed` 整个目录。

#### 执行命令示例

**⚠️ 重要提示：不要cd到工具目录，直接用绝对路径执行！**

> ⚠️ **dict.zip 是 hilogtool 的 `-d` 输入参数，不要手动 `unzip` 解压 dict**。hilogtool 内部自动处理 dict。手动 unzip 只产生无用密钥文件，不能解密 hilog。

```bash
# 设置DISPLAY为空避免X11相关问题
export DISPLAY=

# 创建输出目录
mkdir -p /home/user/hilog_FMR0123417000740_parsed

# 执行解密（不要cd，直接用绝对路径）
wine64 /home/user/.opencode/skills/ohos-issue-xts-log-analysis/tools/hilogtool.exe parse \
    -i /home/user/hilog_FMR0123417000740 \
    -o /home/user/hilog_FMR0123417000740_parsed \
    -d /home/user/hilog_FMR0123417000740/hilog_dict.*.zip
```

**错误示例（dict会被放在错误位置）**：
```bash
cd ~/.opencode/skills/ohos-issue-xts-log-analysis/tools/hilogtool  # ❌ 错误！
wine64 hilogtool.exe parse ...  # dict会被放在当前工作目录
```

**dict临时文件说明**：
- hilogtool自动解压dict.zip，生成dict子目录（约50-100M）
- dict临时文件存放在输出路径下的 `dict/` 目录
- 解析完成后用户可清理：`rm -rf <输出目录>/dict/`

#### Linux常见问题及解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `Permission denied` | 文件无执行权限 | `chmod +x hilogtool.exe` |
| 首次运行超时 | wine初始化配置目录 | 先运行 `wine64 --version` 初始化，再执行实际命令 |
| 解析长时间无响应 | 未指定字典文件(-d) | 必须使用 `-d` 参数指定字典文件 |
| `MIT-SHM missing on display` | X11显示相关问题 | 设置 `DISPLAY=` 环境变量 |
| `Could not find Wine Gecko` | 缺少HTML渲染组件 | 忽略即可，不影响命令行解析 |

### ⚠️ 重要：不要使用gunzip解压！

**关键要点**：hilogtool需要原始.gz文件，不能使用gunzip解压后的GLS_BINARY文件！

**错误流程**：
```bash
# ❌ 错误：gunzip解压后再用hilogtool
gunzip hilog.000.gz           # 解压后变成GLS_BINARY格式
hilogtool parse -i hilog.000  # ❌ 失败！std::out_of_range错误
```

**正确流程**：
```bash
# ✅ 正确：直接使用.gz文件
hilogtool parse -i hilog.000.gz -o output -d dict.zip  # ✅ 成功！
```

**原因说明**：
- hilog.gz文件包含两层：gzip压缩 + GLS_BINARY加密
- hilogtool会自动处理gzip解压和GLS_BINARY解密
- 使用gunzip手动解压会破坏文件结构，导致hilogtool无法正确解析

**错误表现**：
```
libc++abi: terminating due to uncaught exception of type std::out_of_range: basic_string
```

### strings提取方式（仅作为应急方案）

当hilogtool无法使用时，可用strings提取关键信息（不完整）：

```bash
# 应急方案：提取可读文本（不完整）
strings hilog.000.gz | grep -E "Error|FAILED|Hypium"

# 提取特定用例日志
strings hilog.000.gz | grep "textAreaLetterSpacing001"
```

对于zstd格式：

```bash
# 安装zstd工具
sudo apt-get install zstd

# 解压（解压后仍为加密二进制）
zstd -d hilog.000.zst

# 仍需使用hilogtool解密
wine64 hilogtool.exe parse -i hilog.000 -o ./output -d hilog_dict.zip
```

## 常用命令

**查看日志**：
```bash
# 查看全部日志
cat hilog.000

# 过滤特定domain
grep "D003200" hilog.000

# 过滤ERROR级别
grep "ERROR" hilog.000

# 过滤特定进程
grep "pid: 12345" hilog.000

# 过滤特定TAG
grep "/testTag:" hilog.000
```

**日志格式说明**：
```
04-19 17:02:14.735  5394  5394 I A00032/testTag: this is a info level hilog

字段说明：
- 日期: 04-19 (月-日)
- 时间: 17:02:14.735 (时:分:秒.毫秒)
- 进程号: 5394 (PID)
- 线程号: 5394 (TID)
- 级别: I (Info级别，D/I/W/E/F)
- domainID: A00032 (A=应用日志，00032=domain后5位)
- 标签: testTag (日志TAG)
- 内容: this is a info level hilog
```

## 快速参考

| 操作 | 命令 |
|------|------|
| 查看帮助 | `wine64 hilogtool.exe --help` |
| 检查文件类型 | `file hilog.*.gz` |
| 查找字典文件 | `ls -la \| grep hilog_dict` |
| 解析日志目录（Linux） | `DISPLAY= wine64 hilogtool.exe parse -i <input_dir> -o <output_dir> -d <dict_file>` |
| 解析日志目录（Windows） | `hilogtool.exe parse -i <input_dir> -o <output_dir> -d <dict_file>` |
| 查看ERROR日志 | `grep ERROR output/*.txt` |
| 查看特定domain | `grep D003200 output/*.txt` |
| 查看特定用例日志 | `grep "用例名称" output/*.txt` |

## 注意事项

1. **字典文件必需**: hilog解析必须使用 `-d` 参数指定字典文件，否则会超时无响应
2. **工具类型**: hilogtool.exe为Windows PE32+可执行文件，Linux环境需使用wine64
3. **Linux权限**: 确保hilogtool.exe有执行权限：`chmod +x hilogtool.exe`
4. **Wine初始化**: 首次使用wine时需要初始化配置目录，可能耗时较长
5. **DISPLAY设置**: Linux下建议设置 `DISPLAY=` 避免X11相关问题
6. **输入参数**: `-i` 可以是目录或单个文件，会自动解析目录下所有hilog文件
7. **输出格式**: 解析后生成 `.txt` 文本文件，可直接查看和分析
8. **SDK版本**: 建议使用最新SDK中的hilogtool，以支持最新日志格式
9. **⚠️ 工作目录**: 输出目录建议使用 `<日志目录>_parsed`，与日志同级便于管理
10. **⚠️ dict清理**: 解析完成后应清理**输出路径下**的临时dict目录：`rm -rf <输出路径>/dict/`（约50-100M）

## 使用流程

1. **识别加密日志**：检查文件名（.gz/.zst）和文件类型
2. **查找字典文件**：确认日志目录下存在 `hilog_dict.*.zip` 文件
3. **准备工具环境**：Windows直接运行；Linux安装wine64并设置执行权限
4. **Linux首次使用**：先执行 `wine64 --version` 初始化wine配置
5. **执行解析**：使用 `parse -i -o -d` 参数解析日志
6. **日志分析**：使用grep/awk等工具分析解密后的.txt文件

## 故障排查

### Windows：Microsoft Store Python 桩程序（重要，2026-07-15 新增）

**症状**：在 Windows 上运行 `python3 scripts/check_dict.py` 或 `python3 scripts/parallel_decrypt.py` 后**零输出**，也没有报错，且 `_parsed/` 目录未生成——脚本像“没反应”。

**根因**：`python3`/`python` 解析到 Microsoft Store 的“应用执行别名”桩程序：
```
C:\Users\<用户>\AppData\Local\Microsoft\WindowsApps\python3.exe
```
这不是真正的 Python。在非交互终端（如 opencode 的 shell）中它会**静默退出、返回 0、零输出**，脚本主体根本不会执行——所以任何 `.py` 内部自检都无法捕获此情况（自检代码跑不到）。

**判定方法**（功能探测，比看路径更可靠）：
```bat
REM 若以下输出 PYOK → 真 Python；若无输出 → 桩程序/无 Python
python3 -c "import sys;sys.stdout.write('PYOK')"
```
或查路径是否指向 `WindowsApps`：
```bat
where python3
```

**解决方案（任选其一）**：

1. **用 `.cmd` 启动器（推荐，零配置）**——自动探测真 Python，探测不到时直接调 `hilogtool.exe` 原生解密（无需 Python）：
   ```bat
   cmd /c scripts\check_dict.cmd <hilog日志目录>
   cmd /c scripts\parallel_decrypt.cmd <hilog日志目录>
   REM Git Bash 下用：cmd //c scripts\\check_dict.cmd <dir>
   ```

2. **直接跑 hilogtool.exe**（Windows 原生二进制，完全绕开 Python）：
   ```bat
   "<skill根>\tools\hilogtool.exe" parse -i <hilog目录> -o <hilog目录>_parsed -d <dict.zip>
   ```
   > `-d` 需填入 dict 的实际文件名（Windows cmd 不展开 `*`，先用 `dir hilog_dict.*.zip` 查出）。

3. **安装真正的 Python**（后续 `filter_hilog.py` / `validate_report.py` 等分析脚本仍需要）：
   - https://www.python.org/downloads/（安装时勾选 “Add python.exe to PATH”），或
   - `winget install Python.Python.3.12`
   - 装后用 `py` 启动器调用，避开别名：`py scripts\check_dict.py <dir>`

> ⚠️ 即使先用方案 1/2 完成了解密，**后续分析阶段**（`filter_hilog.py` 取行号/时间窗、`validate_report.py` 校验报告）仍依赖真正的 Python，建议按方案 3 安装。

### 通用故障表

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| Windows 下 `.py` 脚本零输出、无 `_parsed/` | `python3` 是 Microsoft Store 桩程序，脚本未执行 | 见上方“Windows Python 桩程序”小节，用 `.cmd` 启动器或直跑 `hilogtool.exe` |
| `Permission denied` | 文件无执行权限 | `chmod +x hilogtool.exe` |
| `wine: command not found` | wine未安装 | `sudo apt-get install wine64` |
| 解析长时间无响应/超时 | 未指定字典文件 | 必须使用 `-d` 参数指定字典文件 |
| 首次运行超时 | wine初始化配置 | 先执行 `wine64 --version` 初始化 |
| `MIT-SHM missing on display` | X11显示问题 | 设置 `DISPLAY=` 环境变量 |
| `Could not find Wine Gecko` | 缺少HTML组件 | 忽略，不影响命令行解析 |
| 解析后内容乱码 | 使用gunzip直接解压 | 必须使用hilogtool解析 |
| 无法识别日志格式 | hilogtool版本过旧 | 更新到最新SDK版本 |
| 字典文件找不到 | 日志目录缺少字典 | 检查是否存在 `hilog_dict.*.zip` |

---

**更新时间**: 2026-06-27  
**工具版本**: v2.0  
**官方文档**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hilog-tool  
**工具位置**: `tools/hilogtool.exe`
