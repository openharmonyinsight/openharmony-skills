# L0_PreAnalysis - 形态④受限流程（仅hilog目录，流程B入口）

> **仅形态④时执行**。形态④（hilog目录）只有hilog日志文件，缺少summary_report.xml和module_run.log，无法自动提取失败用例信息。
> 流程总览见 [SKILL.md](../../SKILL.md)。流程A（形态①②③）见 [FormAndDecrypt.md](./FormAndDecrypt.md)。

---

## 流程B步骤路由表

> 流程B真正跳过的只有 **Step 2**（锁定失败用例，改用户提供）和 **Step 3**（执行状态分析，无module_run.log）。
> Step 2.5/2.5.6/2.7 与流程A**完全相同，必须执行**——无import提取则无domain可过滤（Step 5断链），无崩溃检测则漏根因。

| Step | 流程B操作 | 加载文件 |
|------|----------|---------|
| 1 形态识别 | ✅ 执行（见下方识别逻辑） | 本文件 |
| 1.5 解密 | ✅ 共享 | [FormAndDecrypt.md Step 1.5](./FormAndDecrypt.md) |
| 2 锁定失败用例 | ⏭️ 跳过（用户提供用例名） | — |
| 2.5 源码定位 | ✅ 共享（用户提供路径，脚本仍定位文件） | [FailureAndSource.md Step 2.5](./FailureAndSource.md) |
| 2.5.6 import提取 | ✅ 共享（必须，否则无domain） | [FailureAndSource.md Step 2.5.6](./FailureAndSource.md) |
| 2.7 崩溃/冻结检测 | ✅ 共享（crash_log仍存在） | [CrashFreezeDetect.md](./CrashFreezeDetect.md) |
| 3 执行状态分析 | ⏭️ 跳过（无module_run.log） | — |
| 4 提取时间窗 | ✅ 变体（仅hilog [Hypium]，无PC对齐） | [ExecutionAndTimeWindow.md Step 4 形态④变体](./ExecutionAndTimeWindow.md) |
| 5 分层过滤 | ✅ 共享 | [LayeredFilter.md](../L1_Filter/LayeredFilter.md) |
| 6 生成报告 | ✅ 共享+形态④标注 | [ReportGeneration.md](../L2_Report/ReportGeneration.md) |

---

## Step 1：形态识别 + 提示用户补充信息

**⚠️ 必须用户提供**：
1. **失败用例名**（必须）
2. **源码路径**（强烈建议，否则无法解析API→domain链路）

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

**输出格式（固定）**：
```
检测结果：形态④（判定依据：检测到 hilog.*.gz，无 summary_report.xml，无 module_run.log）
```

---

## 降级处理

**无源码时的降级**：
- 用 testsuite 名推断子系统
- 报告标注："未提供源码，domain 推断自 testsuite 名"
- 无法建立 API→domain 链路

**无 [Hypium] 标记时的降级**：
- 提示用户提供时间窗
- 或提示用户尝试其他定位方法
- appfreeze 场景主线程冻结、[Hypium] 可能未写入 → 见 [constraints 规则1b](../../references/constraints.md) 的回退顺序

---
