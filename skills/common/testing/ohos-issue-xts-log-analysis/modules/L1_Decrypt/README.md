# L1_Decrypt - 日志解密模块

## 模块概述

日志解密模块负责处理加密的 hilog 日志文件（.gz 格式），使用 hilogtool 工具解密，为后续分层过滤提供可读的日志内容。

## 加密日志识别

**加密文件特征**：
- 文件名：`hilog.*.gz` 或 `hilog.*.zst`
- 文件格式：GLS_BINARY（加密二进制）
- 直接读取：显示乱码或二进制内容

**检测方法**：
```bash
# 检查文件类型
file hilog.026.20260626-155340.gz
# 输出：gzip compressed data 或 GLS_BINARY

# 尝试直接读取
cat hilog.026.gz
# 输出：乱码或二进制内容
```

## 解密工具

### hilogtool 使用要点

**⚠️ 核心要点**：**直接使用.gz文件，不要先gunzip解压！**

**工具位置**：
- OpenHarmony SDK：`${SDK路径}/toolchains/hilogtool`
- 本技能提供：`docs/tools/hilogtool/hilogtool.exe`

**核心命令格式**：
```bash
hilogtool parse -i <输入文件.gz> -o <输出目录> -d <字典文件>
```

### Linux 环境（需 wine）

```bash
# 安装 wine64
sudo apt-get install wine64

# 使用 hilogtool 解密（推荐方式）
export DISPLAY=
wine64 ~/.opencode/skills/xts-issue-analysis/docs/tools/hilogtool/hilogtool.exe \
  parse -i hilog.107.20260626-162511.gz \
  -o decrypted_hilog \
  -d hilog_dict.20260626-144351.zip

# 批量解密多个.gz文件
for f in hilog.*.gz; do
  wine64 hilogtool.exe parse -i "$f" -o output -d hilog_dict.zip
done
```

### Windows 环境

```bash
# 直接运行 hilogtool.exe
hilogtool.exe parse -i hilog.107.gz -o decrypted -d hilog_dict.zip
```

## ❌ 错误流程（禁止使用）

```bash
# ❌ 错误：先gunzip解压再用hilogtool
gunzip hilog.107.gz                        # 解压后变成GLS_BINARY
wine64 hilogtool.exe parse -i hilog.107   # ❌ 报错：std::out_of_range
```

**原因说明**：
- hilog.gz 包含两层：gzip压缩 + GLS_BINARY加密
- hilogtool 会自动处理两层解密
- gunzip 破坏文件结构，导致 hilogtool 无法识别 GLS_BINARY 格式

## 字典文件处理

### 字典文件位置

字典文件通常与 hilog.gz 在同一目录：
- 文件名：`hilog_dict.*.zip`
- 内容：解密所需的字典数据

### 字典文件缺失处理

当字典文件缺失时，使用应急方案：

```bash
# 使用 strings 提取关键信息（不完整）
strings hilog.000.gz | grep -E "Error|FAILED|Hypium"
```

## 解密结果验证

**强制验证步骤**：

```bash
# 验证解密结果
wc -l decrypted_hilog/*.txt

# 必须输出行数（如：29692行）
# 无行数输出 → 解密失败
```

**成功标志**：
- 输出文件行数 > 0
- 文件内容可读（文本格式）
- 包含 `[Hypium]`、`OHOS_REPORT_STATUS` 等关键字

## AI 使用方式

### AI 主动解密

AI 应按照以下步骤主动解密：

1. ✅ 检测加密文件（使用 file 命令）
2. ✅ 阅读文档要点（hilogtool-guide.md）
3. ✅ 动态调用解密命令
4. ✅ 验证解密结果（行数统计）

### 辅助检测（可选）

```bash
# 使用 detect_logs.py 辅助检测
cd ~/.opencode/skills/xts-issue-analysis/scripts
python3 detect_logs.py <日志目录>

# 输出：加密文件提示 + 解密建议
# AI 根据提示主动操作
```

## 解密文件管理

### 输出目录规范

建议使用统一的输出目录名：
- `decrypted_hilog/`
- 或 `hilog_decrypted/`

### 文件命名

解密后的文件通常为：
- `hilog.txt`（单个文件）
- 或 `*.txt`（多个文件，对应不同时间段）

## 常见问题

### Q1: wine 不可用

**解决方案**：使用 strings 应急提取
```bash
strings hilog.000.gz | grep -E "Error|FAILED|Hypium"
```

### Q2: hilogtool 报错 std::out_of_range

**原因**：使用了 gunzip 解压后的文件
**解决**：直接使用原始 .gz 文件

### Q3: 字典文件缺失

**影响**：部分日志可能解析不完整
**解决**：使用 strings 应急方案 + 报告标注

### Q4: 解密后无行数输出

**原因**：解密失败
**解决**：检查 hilogtool 参数、字典文件路径

## 输出产物

供 L2_Filter 使用：
- 解密后的文本日志文件（`*.txt`）
- 日志行数统计
- 解密成功/失败状态

---

**更新时间**：2026-07-02
**文档来源**：docs/tools/hilogtool-guide.md
**适用场景**：处理加密 hilog 日志