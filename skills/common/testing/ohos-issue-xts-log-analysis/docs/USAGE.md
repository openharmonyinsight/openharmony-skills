# 使用方式详解

> **xts-issue-analysis** - 完整使用指南

## 快速导航

- [输入形态自动识别](#输入形态自动识别)
- [使用示例](#使用示例)
- [常见使用场景](#常见使用场景)
- [常见问题](#常见问题)

---

## 输入形态自动识别

本技能支持4种输入形态，AI自动识别并选择对应工作流程：

### 形态识别方法

**AI操作**：
```bash
ls -la <日志目录>
```

### 形态判定依据

| 形态 | 识别特征 | 工作流程 | 特殊要求 |
|------|----------|----------|----------|
| ① 全量报告 | 含 `summary_report.xml` | 流程A（标准流程） | 无 |
| ② log 根 | 下全是 `Acts*/` 子目录 | 流程A（标准流程） | 无 |
| ③ 单 testsuite | 含 `module_run.log` | 流程A（标准流程） | 无 |
| ④ hilog 目录 | 含 `hilog.*.gz`，无 `module_run.log` | 流程B（受限流程） | **必须用户提供失败用例名 + 源码路径** |

### 形态对比

| 形态 | 可达文件 | 分析能力 | 定位精度 |
|------|----------|----------|----------|
| ①②③ | summary_report.xml/module_run.log/hilog | 完整（失败用例自动提取） | 高 |
| ④ | 仅 hilog | 受限（需用户提供信息） | 中 |

---

## 使用示例

### 示例1：分析日志目录（形态①②③）

**用户输入**：
```
请分析 /tmp/xts_logs/20260620 目录下的测试日志
```

**AI响应**：
```
已加载 skill: xts-issue-analysis

Step 1：识别输入形态
检测结果：形态①（全量报告）
判定依据：检测到 summary_report.xml 文件

Step 2：锁定失败用例
失败用例数：8个
失败用例清单：
  1. ActsAACommandImplicitStartTest#SUB_Ability_..._3100
  2. ...
信号源：summary_report.xml

Step 3：分析执行状态
判定结果：测试正常执行

Step 4：提取时间窗（2026-07-10改进）
时间窗来源：hilog [Hypium] 标记（精确时间窗）
起始时间：06-26 15:53:48.123，行号：1234
结束时间：06-26 15:53:52.456，行号：1567（specDone标记）
结束标记类型：specDone标记（优先级①）
边界验证：下一个用例start在1568，未越界 ✅

Step 5：分层过滤
主分析集：47行（domain匹配）
P1扩展：23行（同PID/TID）

正在生成报告...
报告已保存：XTS_Analysis_Report_20260620.md
```

---

### 示例2：分析hilog目录（形态④）

**用户输入**：
```
请分析 hilog_FMR0123417000740 目录下的日志
失败用例是 SUB_Ability_AbilityRuntime_UiTest_3100
源码路径是 /home/xianf/master/test/xts/acts/ability
```

**AI响应**：
```
已加载 skill: xts-issue-analysis

Step 1：识别输入形态
检测结果：形态④（hilog目录）
判定依据：检测到 hilog.*.gz，无 module_run.log

用户已提供必要信息：
  - 失败用例名：SUB_Ability_AbilityRuntime_UiTest_3100 ✅
  - 源码路径：/home/xianf/master/test/xts/acts/ability ✅

Step 2：解密hilog
检测结果：hilog文件已加密
解密结果：成功

Step 3：提取时间窗
时间窗来源：hilog [Hypium] 标记
...

正在生成报告...
```

---

### 示例3：指定子系统配置（未来扩展）

> 📖 **配置驱动设计**：支持子系统定制化配置

**用户输入**：
```
请使用 xts-issue-analysis 分析 ability 子系统的测试日志：
子系统: ability
日志目录: /tmp/xts_logs/20260620
```

**AI响应**：
```
已加载 skill: xts-issue-analysis
已加载子系统配置: ability

加载配置：
  - 核心配置: references/configs/_common.md
  - 子系统配置: references/configs/ability/_common.md
  - domain映射: C0013xx (AAFwk)

开始分析...
```

---

## 常见使用场景

### 场景1：快速失败用例分析

**适用**：形态①②③，需要快速定位失败原因

**操作**：
1. 提供日志目录
2. AI自动识别形态
3. AI自动提取失败用例
4. AI生成报告

### 场景2：应用崩溃分析

**适用**：所有形态，检测到 App died 关键字

**操作**：
1. 提供日志目录（形态①②③）或 hilog目录（形态④）
2. AI查询数据库规则（关键字"App died"）
3. AI提取 SO 崩溃栈
4. AI查询 SO 库归属
5. AI生成报告，定界到元能力或其他子系统

### 场景3：测试阻塞排查

**适用**：形态①②③，检测到 Blocked 关键字

**操作**：
1. 提供日志目录
2. AI检查 shell 命令执行链
3. AI分析进程状态（进程挂起、死锁）
4. AI生成报告，定界到测试框架或被测应用

---

## 常见问题

### Q1: 形态④缺少失败用例名怎么办？

**问题**：用户只提供 hilog 目录，未提供失败用例名。

**解决**：AI会提示用户提供必要信息：
```
检测到形态④（hilog目录），缺少以下信息：
1. ❌ 失败用例名（必须提供）

请提供失败用例名：如 SUB_Ability_AbilityRuntime_UiTest_3100
```

### Q2: 如何确认测试是否正常执行？

**问题**：不确定测试是否正常执行，担心环境问题。

**解决**：AI会检查 shell 命令执行链（bm install → aa test → Collected count → [Listener]），判定执行状态。

### Q3: 无源码时如何分析？

**问题**：未配置 OH_ROOT，无法关联源码。

**解决**：AI会降级处理（用 testsuite 名推断子系统），报告标注降级状态。

### Q4: hilog 文件加密如何解密？

**问题**：hilog 文件是加密的 .gz 文件，无法直接读取。

**解决**：AI会调用 hilogtool 解密，详见 [docs/tools/hilogtool-guide.md](./tools/hilogtool-guide.md)。

---

## 使用建议

### 推荐使用方式

**大多数情况** → 直接提供日志目录（形态①②③）
```
请分析 /tmp/xts_logs/20260620 目录下的测试日志
```

**特殊情况** → 提供完整信息（形态④）
```
请分析 hilog_FMR0123417000740 目录下的日志
失败用例是 SUB_Ability_..._3100
源码路径是 /home/xianf/master/test/xts/acts/ability
```

### 提高分析质量建议

✅ **配置 OH_ROOT**：如有源码，强烈推荐配置
✅ **提供源码路径**：形态④时提供源码路径可启用P0核心功能
✅ **使用子系统配置**：未来扩展功能，可提高定界准确性

---

**更新时间**：2026-07-03  
**设计理念**：自动识别输入形态，根据形态选择工作流程