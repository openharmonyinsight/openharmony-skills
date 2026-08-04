# L0_PreAnalysis - 形态识别与解密（Step 1-1.5）

> 适用形态①②③。形态④见 [Form4_Limited.md](./Form4_Limited.md)。流程总览见 [SKILL.md](../../SKILL.md)。约束见 [report-constraints.md](../../references/report-constraints.md)。

---

## Step 1：形态识别

用户输入可能是以下 4 种形态之一。AI**不向上回溯补全**，而是按当前目录的可达文件判定哪些步骤可执行。

**AI操作**：
```bash
ls -la <日志目录>
```

### 形态判定依据

| 形态 | 示例路径 | 识别特征 | 当前目录可达文件 |
|------|----------|----------|-----------------|
| **① 全量报告** | `.../2026-06-26-15-53-21/` | 含 `summary_report.xml` 或 `summary.ini` | summary_report.xml + 所有 log/<mod>/module_run.log + hilog + dict |
| **② log 根** | `.../2026-06-26-15-53-21/log/` | 下全是 `Acts*/` 子目录，无 xml | 所有 module_run.log + hilog + dict（无汇总 xml） |
| **③ 单 testsuite** | `.../log/ActsAACommandImplicitStartTest/` | 含 `module_run.log` | module_run.log + hilog + dict（无汇总 xml） |
| **④ hilog 目录** | `.../Acts.../hilog_FMR0123417000740/` | 含 `hilog.*.gz`，无 `module_run.log` | 仅 hilog*.gz + dict（无 module_run.log、无 xml） |

**判定逻辑**：
- 含 `summary_report.xml` → 形态①（全量报告）
- 下全是 `Acts*/` 子目录 → 形态②（log根）
- 含 `module_run.log` → 形态③（单testsuite）
- 含 `hilog.*.gz`、无 `module_run.log` → 形态④（hilog目录，见 [Form4_Limited.md](./Form4_Limited.md)）

### 各形态可执行步骤 + 用户需补充信息

| 形态 | 可执行步骤 | 跳过步骤 | 用户须额外提供（缺则降级/中止） |
|------|-----------|---------|--------------------------------|
| ① 全量报告 | Step 1-6 全部 | 无 | 源码路径（建议，非必须） |
| ② log 根 | Step 2(改用 module_run.log FAILED) + 3-6 | Step 2 xml 路径 | 无（自动扫描 FAILED 行）；可指定 testsuite 名缩小范围 |
| ③ 单 testsuite | Step 2(改用 module_run.log FAILED) + 3-6 | Step 2 xml 路径 | 无（单模块）；源码路径（建议） |
| ④ hilog 目录 | Step 1/1.5/2.5/2.5.6/2.7/4(变体)/5/6（仅跳过 Step 2 和 Step 3） | Step 2、Step 3 | **必须**：失败用例名 + 源码路径（否则无法定位目标/无法解析 domain） |

**形态④特殊要求**：
- 无 module_run.log → 无法判定执行状态（**Step 3 跳过**）
- 无 PC 时间窗（Step 4 改用 hilog `[Hypium]` 标记取设备时间窗，见 [ExecutionAndTimeWindow.md 形态④变体](./ExecutionAndTimeWindow.md)）
- **Step 2 跳过**（无 module_run.log，必须由用户提供失败用例名）
- **Step 2.5（源码定位）、2.5.6（import提取）、2.7（崩溃检测）与流程A完全相同，必须执行**
- 流程B完整步骤路由见 [Form4_Limited.md](./Form4_Limited.md)

**输出格式（固定）**：
```
检测结果：形态①（判定依据：检测到 summary_report.xml 文件）
```

---


## Step 1.5：加密文件检测与解密（强制）

> 📖 **详细工具使用**: [hilogtool-guide.md](../../references/hilogtool-guide.md)

### 加密文件识别

**检测方法**：
```bash
# 检查是否存在加密文件
ls <日志目录>/hilog.*.gz

# 或检查文件类型
file <日志目录>/hilog.*.gz
# 输出: gzip compressed data
```

**加密文件特征**：
- 文件名：`hilog.*.gz` 或 `hilog.*.zst`
- 直接 zcat 显示乱码或二进制内容

### 解密操作（必须执行）

**⚠️ 重要提示**：
- **检测到加密文件 → 必须使用 hilogtool 解密**
- **不要使用 gunzip**（会破坏 GLS_BINARY 结构，导致 std::out_of_range 错误）
- **不要降级处理**（strings 提取不完整）

**hilogtool 工具路径**（skill 已内置）：
```bash
# Linux 环境
~/.opencode/skills/ohos-issue-xts-log-analysis/tools/hilogtool.exe

# Windows 环境
tools/hilogtool.exe
```

**解密命令**：
```bash
# Linux 环境（使用 wine64）
DISPLAY= wine64 ~/.opencode/skills/ohos-issue-xts-log-analysis/tools/hilogtool.exe parse \
    -i <日志目录> \
    -o <日志目录>/parsed \
    -d <日志目录>/hilog_dict.*.zip

# Windows 环境
hilogtool.exe parse -i <日志目录> -o <日志目录>/parsed -d <日志目录>/hilog_dict.*.zip
```

**解密验证**：
```bash
# 检查输出目录
ls <日志目录>/parsed/*.txt

# 统计行数（应该有大量日志）
wc -l <日志目录>/parsed/*.txt
```

**常见问题**：
| 问题 | 解决方案 |
|------|---------|
| `Permission denied` | `chmod +x hilogtool.exe` |
| wine 未安装 | `sudo apt-get install wine64` |
| 首次运行超时 | 先执行 `wine64 --version` 初始化 |
| MIT-SHM 错误 | 设置 `DISPLAY=` 环境变量 |
| 字典文件找不到 | 检查是否存在 `hilog_dict.*.zip` |

---


## 硬条件检查（无法分析的硬条件）

| 必要条件 | 说明 | 缺失后果 |
|---------|------|---------|
| **失败信号源** | `summary_report.xml`、`module_run.log`（含 FAILED 行）、或用户口头指定失败用例名，**三者至少有一** | 无任何失败信号 → **无法定位分析目标，必须中止**并提示用户提供用例名或更完整目录 |
| **至少一份证据** | `module_run.log`、`hilog*.gz`、`result/*.xml`，**三者至少有一** | 三者全无 → **没有任何可分析内容，必须中止** |

> 只要满足上述两项硬条件，即使其他文件缺失，也能产出**至少基于 XML message 或 shell 命令链的定界结论**（精度降级，但可用）。

---

## 输入产物

- 日志目录（任一形态①②③④）
- 源码路径（可选，配置 OH_ROOT）
- 失败用例名（形态④必须用户提供）

## 输出产物

- 形态判定结果
- 失败用例清单（testsuite/modulename/testcase/message）
- 执行状态判定结果（正常执行 / install失败 / aa test失败 / 未运行）
- 时间窗（起始/结束时间 + 行号，已对齐设备时间）
- 分层过滤结果 + 分层来源标记（[主]/[P1]/[P2]/[P3]）
- 分层命中统计（主: X行 | P1: Y行 | P2: Z行 | P3: W行）
- 设备 SN（用于定位 hilog 子目录）
- PC↔设备时钟是否已同步（布尔）
- 标准分析报告（2章节）

---

