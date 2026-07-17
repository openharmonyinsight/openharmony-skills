# 工具使用指南

> **xts-issue-analysis** - 辅助脚本使用说明

## 工具概述

xts-issue-analysis 提供辅助脚本，用于数据库查询和日志检测。脚本定位为**辅助工具**，AI主导流程判断。

---

## 工具清单

### 辅助脚本

| 脚本 | 用途 | 定位 | 使用场景 |
|------|------|------|---------|
| `scripts/query_rules.py` | 查询定界规则 | 辅助查询 | AI需要查询关键字→领域→解决方案 |
| `scripts/query_so_mapping.py` | 查询SO库归属 | 辅助查询 | AI需要查询SO库名→子系统 |
| `scripts/detect_logs.py` | 检测加密文件 | 辅助检测 | AI需要检测hilog是否加密 |
| `scripts/filter_hilog.py` | 分层过滤工具 | 可选工具 | AI可选择用此脚本实现分层过滤 |

### 内置工具（skill 提供）

| 工具 | 路径 | 用途 | 使用场景 |
|------|------|------|---------|
| `hilogtool.exe` | `docs/tools/hilogtool/hilogtool.exe` | 解密加密hilog日志 | **检测到 hilog.*.gz 必须使用** |
| `xts_rules.db` | `data/xts_rules.db` | 定界规则数据库 | 查询关键字→领域映射 |

**⚠️ 重要提示**：
- **hilogtool 是强制工具**：检测到加密文件必须使用，不要降级处理
- 脚本只做辅助查询，AI主导流程判断

---

## query_rules.py - 查询定界规则

### 用途

查询数据库中的定界规则，根据关键字查找领域和解决方案。

### 使用方式

**查询所有规则**：
```bash
cd ~/.opencode/skills/xts-issue-analysis/scripts
python3 query_rules.py all
```

**查询特定关键字**：
```bash
python3 query_rules.py "App died"
```

**查询特定领域**：
```bash
python3 query_rules.py 元能力
```

### 输出示例

**查询关键字"App died"**：
```
关键字: App died
领域: 元能力
问题类型: 应用闪退
解决方案: 检查应用启动流程，验证Ability生命周期
```

### AI使用场景

**场景1**：日志中发现"App died"关键字
```bash
# AI调用辅助脚本查询定界规则
python3 query_rules.py "App died"

# AI根据查询结果定界到"元能力"
```

**场景2**：日志中发现多个关键字
```bash
# AI依次查询多个关键字
python3 query_rules.py "TypeError"
python3 query_rules.py "Cannot read property"

# AI根据查询结果综合定界
```

---

## query_so_mapping.py - 查询SO库归属

### 用途

查询数据库中的SO库映射，根据SO库名查找子系统。

### 使用方式

**查询特定SO库**：
```bash
cd ~/.opencode/skills/xts-issue-analysis/scripts
python3 query_so_mapping.py libace.z.so
```

**查询特定子系统**：
```bash
python3 query_so_mapping.py ArkUI
```

### 输出示例

**查询"libace.z.so"**：
```
SO库名: libace.z.so
子系统: ArkUI
建议: 转交责任田领域进行问题确认
```

### AI使用场景

**场景1**：崩溃栈中发现"libace.z.so"
```bash
# AI从崩溃栈提取SO库名
SO库名: libace.z.so

# AI调用辅助脚本查询SO归属
python3 query_so_mapping.py libace.z.so

# AI根据查询结果定界到"ArkUI"
```

---

## detect_logs.py - 检测加密文件

### 用途

检测日志目录中的加密文件（hilog.*.gz）。

### 使用方式

```bash
cd ~/.opencode/skills/xts-issue-analysis/scripts
python3 detect_logs.py <日志目录>
```

### 输出示例

**检测到加密文件**：
```
检测结果：发现加密文件
加密文件：hilog.489.gz
需要解密：使用 hilogtool 解密
提示：详见 docs/tools/hilogtool-guide.md
```

**未检测到加密文件**：
```
检测结果：未发现加密文件
日志文件：hilog.489.txt（已解密）
可以直接读取
```

### AI使用场景

**场景1**：形态④分析hilog目录
```bash
# AI检测加密文件
python3 detect_logs.py <hilog目录>

# 如果加密，AI调用 hilogtool 解密
```

---

## filter_hilog.py - 分层过滤工具（可选）

### 用途

实现分层过滤（时间窗过滤 → domain分组 → 渐进式扩展）。

### 定位说明

**⚠️ 重要**：此脚本为**可选工具**，AI可以选择使用此脚本，也可以自己用 grep 实现。

### 使用方式

> 📖 **详细使用说明**: [scripts/filter_hilog.py](../scripts/filter_hilog.py)

**基本用法**：
```bash
python3 filter_hilog.py -i hilog.txt -d 00310 0013X
```

**指定时间窗**：
```bash
python3 filter_hilog.py -i hilog.txt -d 00310 \
  --time-start "06-26 15:53:48" \
  --time-end "06-26 15:53:52"
```

**输出JSON格式**：
```bash
python3 filter_hilog.py -i hilog.txt -d 00310 --json
```

**提取[Hypium]标记时间窗**：
```bash
python3 filter_hilog.py -i hilog.txt --extract-hypium --testcase SUB_..._3100
```

### 输出示例

**分层过滤结果**：
```
【分层过滤结果】
主分析集：47行（domain匹配）
P1扩展：23行（同PID/TID）
P2扩展：12行（同PID不同TID）
P3扩展：40行（位置窗口）

统计信息：
时间窗过滤：10000行被丢弃
时间窗保留：500行
```

### AI使用场景

**场景1**：AI选择使用此脚本实现分层过滤
```bash
# AI提取时间窗后，调用此脚本分层过滤
python3 filter_hilog.py -i hilog.txt -d 00310 \
  --time-start "06-26 15:53:48" \
  --time-end "06-26 15:53:52"

# AI根据脚本输出的分层结果分析日志
```

**场景2**：AI选择自己用 grep 实现
```bash
# AI自己用 grep 实现时间窗过滤
sed -n '1234,1567p' hilog.txt

# AI自己用 grep 实现domain分组
grep -E 'C0031[0-9a-f]{2}/' hilog.txt

# AI根据自己实现的过滤结果分析日志
```

---

## 工具定位总结

### 核心原则

**AI主导判断，脚本辅助查询**

### 脚本定位

| 脚本类型 | 定位 | AI使用方式 |
|---------|------|-----------|
| **辅助查询脚本** | query_rules.py, query_so_mapping.py | AI调用脚本查询数据库，根据结果判断 |
| **辅助检测脚本** | detect_logs.py | AI调用脚本检测加密文件，根据结果处理 |
| **可选工具脚本** | filter_hilog.py | AI可选择使用脚本或自己实现 |

### 禁止行为

❌ 不要用脚本替代AI判断
❌ 不要跳过AI自主分析步骤
❌ 不要在未理解流程的情况下直接调用脚本

---

**更新时间**：2026-07-03  
**设计理念**：脚本辅助查询，AI主导判断