# L1_Limited - 受限流程详细说明

> **适用形态**：形态④（hilog目录）

## 模块概述

受限流程适用于只有hilog日志文件的输入形态，缺少summary_report.xml和module_run.log，无法自动提取失败用例信息。

**⚠️ 特殊要求**：必须用户提供：
1. **失败用例名**（必须）
2. **源码路径**（强烈建议）

## 详细工作流程

### Step 1：形态识别 + 提示用户补充信息

**AI操作**：
```bash
ls -la <日志目录>
```

**判定依据**：
- 含 `hilog.*.gz` → hilog文件存在
- 无 `summary_report.xml` → 缺少失败信号源
- 无 `module_run.log` → 缺少执行状态信息

**判定结果**：形态④（hilog目录）

**提示用户**：
```
检测到形态④（hilog目录），缺少以下信息：
1. ❌ 失败用例名（必须提供）
2. ⚠️  源码路径（强烈建议提供，否则无法解析API→domain链路）

请提供：
- 失败用例名：如 SUB_Ability_AbilityRuntime_UiTest_3100
- 源码路径：如 /home/xianf/master/test/xts/acts/ability
```

---

### Step 2：解密hilog（如有加密）

**AI操作**：检测并解密加密文件

**检测加密文件**：
```bash
file hilog.*.gz
# 或使用辅助脚本
python3 scripts/detect_logs.py <日志目录>
```

**解密流程**：

> 📖 **详细解密指南**: [docs/tools/hilogtool-guide.md](../../docs/tools/hilogtool-guide.md)

**步骤1**：解压 dict 文件
```bash
unzip hilog_dict*.zip
```

**步骤2**：调用 hilogtool 解密
```bash
wine docs/tools/hilogtool/hilogtool.exe -d dict/ -i hilog.*.gz -o decrypted/
```

**步骤3**：验证解密结果
```bash
wc -l decrypted/*.txt
# 必须输出行数（如：29692行），否则解密失败
```

**输出**：
```
Step 2：解密hilog
检测结果：hilog文件已加密
解密结果：成功
解密文件：decrypted/hilog.489.txt
行数：29692行
```

---

### Step 3：提取时间窗

**AI操作**：从 hilog [Hypium] 标记提取时间窗

**提取方法**：
```bash
grep -n "Hypium.*start.*SUB_Ability_..._3100" hilog.txt
grep -n "Hypium.*fail.*SUB_Ability_..._3100" hilog.txt
```

**提取内容**：
- [Hypium]start test → 起始时间 + 行号
- [Hypium]fail test → 结束时间 + 行号
- 设备时间（无需对齐）

**如果未找到 [Hypium] 标记**：
- 提示用户："未找到 [Hypium] 标记，请提供时间窗或尝试其他定位方法"

**输出**：
```
Step 3：提取时间窗
时间窗来源：hilog [Hypium] 标记
起始时间：06-26 15:53:48.123，行号：1234
结束时间：06-26 15:53:52.456，行号：1567
持续时间：4.33秒
```

---

### Step 4：分层过滤

> 📖 **详细分层过滤说明**: [modules/L2_Filter/README.md](../L2_Filter/README.md)

**AI操作**：执行分层过滤（同标准流程）

**Layer 1**：时间窗硬过滤
**Layer 2**：domain分组
**Layer 3**：渐进式扩展

---

### Step 5：生成报告

> 📖 **详细报告生成说明**: [modules/L3_Report/README.md](../L3_Report/README.md)

**AI操作**：生成4章节标准报告（同标准流程）

**报告标注**：
- 在"一、测试执行概况"中标注："形态④（hilog目录），缺少 module_run.log，无法确认执行状态"
- 在"三、hilog日志用例详情"中标注："未提供源码，domain 推断自 testsuite名"（如无源码）

---

## 输入产物

**必须提供**：
- hilog 日志文件（加密或解密）
- 失败用例名（用户提供）

**可选提供**：
- 源码路径（强烈建议）
- 时间窗（如 [Hypium] 标记缺失）

## 输出产物

- 形态判定结果（形态④）
- 解密后的 hilog 文件（如有加密）
- 时间窗（起始/结束时间 + 行号）
- 分层过滤结果 + 分层来源标记
- 标准分析报告（4章节，标注降级状态）

---

## 关键改进说明

**与原设计对比**：

| 对比项 | 原设计 | 新设计 | 改进效果 |
|--------|--------|--------|---------|
| 用户提示 | 不明确，脚本自动化 | 明确提示用户提供必要信息 | 提高用户体验 |
| 时间窗提取 | module_run.log优先 | hilog [Hypium] 标记优先（唯一方法） | 适配形态④ |
| 降级标注 | 不明确 | 报告明确标注降级状态 | 提高报告可信度 |

---

## 降级处理

**无源码时的降级**：
- 用 testsuite 名推断子系统
- 报告标注："未提供源码，domain 推断自 testsuite 名"
- 无法建立 API→domain 链路

**无 [Hypium] 标记时的降级**：
- 提示用户提供时间窗
- 或提示用户尝试其他定位方法

---

**更新时间**：2026-07-03  
**设计理念**：文档驱动AI操作，AI主导判断，脚本辅助查询