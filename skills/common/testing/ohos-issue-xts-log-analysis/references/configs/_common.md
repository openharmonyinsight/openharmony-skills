# XTS测试问题分析核心配置

> **核心规范** - 适用于所有子系统

> ⚠️ **本文件为早期配置模板摘要，部分内容已过时，请勿作为执行依据**。
> 权威版本请以下列来源为准：
> - 报告格式 → `modules/L3_Report/README.md`（本文件写的"零、数据库查询记录"章节已在新版移除，现为4章节）
> - 数据库 schema 与表记录数 → `references/database_schema.md`（本文件记录数已过期）
> - 形态识别 / 时间窗 / 执行链 → `modules/L0_PreAnalyze/README.md`
> - 分层过滤 → `modules/L2_Filter/README.md`
> - 被测方 domain 映射 → `scripts/map_domain.py`（固化常量）
>
> 本文件保留仅供 `references/configs/` 配置模板体系兼容，后续将整体治理。

## 数据库规则

### 数据库位置

`data/xts_rules.db`

### 核心表

| 表名 | 记录数 | 用途 |
|------|--------|------|
| rules | 80条 | 定界规则（关键字→领域→解决方案） |
| so_mapping | 711条 | SO库映射（库名→子系统） |
| contacts | 79条 | 责任人信息（内部查询使用） |
| module_domain | 10条 | 模块级精确 domain 映射 |
| subsystem_bridge | 9条 | 子系统命名桥接 |

### 定界规则查询

**关键字→领域→解决方案**

示例：
- "App died" → 元能力 → 应用闪退
- "TypeError" → 应用框架 → 类型错误
- "Blocked" → 测试框架 → 测试阻塞

---

## 报告格式规范

### 标准格式（4章节）

**章节结构**：
- 零、数据库查询记录
- 一、测试执行概况
- 二、失败用例清单
- 三、hilog日志用例详情
- 四、总结

### 报告命名规范

`XTS_Analysis_Report_YYYYMMDD.md`

### 保存路径

日志目录（与测试日志同目录）

---

## 时间窗提取优先级

### 强制要求

**优先级**：
1. **优先**：hilog [Hypium] 标记（设备时间 + 精确行号）
2. **回退**：module_run.log（PC时间，无行号）

### 提取方法

**hilog [Hypium] 标记提取**：
```bash
grep -n "Hypium.*start.*testcase_X" hilog.txt
grep -n "Hypium.*fail.*testcase_X" hilog.txt
```

**module_run.log 提取**：
```bash
grep "FAILED.*testcase_X" module_run.log
```

---

## 输入形态识别

### 形态判定依据

| 形态 | 识别特征 | 工作流程 |
|------|----------|----------|
| ① 全量报告 | 含 `summary_report.xml` | 流程A |
| ② log 根 | 下全是 `Acts*/` 子目录 | 流程A |
| ③ 单 testsuite | 含 `module_run.log` | 流程A |
| ④ hilog 目录 | 含 `hilog.*.gz`，无 `module_run.log` | 流程B |

### 特殊要求

**形态④必须用户提供**：
- 失败用例名（必须）
- 源码路径（强烈建议）

---

## 分层过滤规范

### 分层模型

**Layer 1**：时间窗硬过滤
- 时间窗外的日志 → 硬丢弃

**Layer 2**：domain分组（软过滤）
- 主分析集 = domain 匹配失败用例引用 API 的行
- 备用集 = domain 不匹配的行（暂存）

**Layer 3**：渐进式扩展
- P1：同 (PID, TID) → 同线程因果链
- P2：同 PID、不同 TID → 同进程跨线程
- P3：位置窗口前/后各 20 行 → 上下文兜底

### 分层来源标记

- `[主]`：主分析集
- `[P1]`：同 (PID, TID) 扩展
- `[P2]`：同 PID、不同 TID 扩展
- `[P3]`：位置窗口扩展

---

## 辅助脚本定位

### 核心原则

**AI主导判断，脚本辅助查询**

### 脚本定位

| 脚本 | 定位 | 说明 |
|------|------|------|
| query_rules.py | 辅助查询 | AI调用查询定界规则 |
| query_so_mapping.py | 辅助查询 | AI调用查询SO库归属 |
| detect_logs.py | 辅助检测 | AI调用检测加密文件 |
| filter_hilog.py | 可选工具 | AI可选择使用或自己实现 |

---

## 配置优先级

**配置层级**：
```
用户自定义配置 > 模块配置 > 子系统配置 > 核心配置
```

---

**更新时间**：2026-07-03  
**适用范围**：所有子系统的基础规范